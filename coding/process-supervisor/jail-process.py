#!/usr/bin/env python3
"""
jail-process.py

Sandboxes processes using one of three backends (mutually exclusive):

  bwrap        — bubblewrap namespace isolation: separate mount, PID, network,
                 user, IPC, and UTS namespaces; filesystem and command allowlists;
                 environment clearing. Requires bwrap to be installed. Linux only.

  sandbox-exec — macOS Seatbelt sandbox: SBPL-based filesystem access control,
                 network isolation, exec allowlisting, and environment clearing.
                 Requires macOS with sandbox-exec (available by default). macOS only.

  landlock     — Linux Landlock LSM: kernel-enforced filesystem allowlist and
                 exec filtering, plus environment isolation. No extra privileges
                 or binaries required. Requires Linux 5.13+.

The default backend is whichever is available, preferring bwrap (strongest
isolation) on Linux and sandbox-exec on macOS.

Usage:
  jail-process.py -c CONFIG -p PROFILE [--ro PATH] [--rw PATH]
                [--bwrap | --sandbox-exec | --landlock] [--dry-run] [--] COMMAND [ARGS...]

Example:
  jail-process.py -c confs/jail.toml -p claude -- claude --resume
  jail-process.py -c confs/jail.toml -p aider --dry-run -- aider
  jail-process.py -c confs/jail.toml -p shell --rw ~/project --ro /opt/data -- bash
  jail-process.py -c confs/jail.toml -p shell --sandbox-exec -- bash
  jail-process.py -c confs/jail.toml -p shell --landlock -- bash
  jail-process.py -c confs/jail.toml -p shell --bwrap -- bash
"""

import abc
import argparse
import ctypes
import ctypes.util
import functools
import os
import platform
import re
import shlex
import shutil
import stat
import sys
from typing import NoReturn

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:
        tomllib = None  # type: ignore[assignment]


def die(msg) -> NoReturn:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def warn(msg):
    print(f"Warning: {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_profile(config_path, profile_name):
    """Load a named profile from the TOML config, with ~ expansion."""
    if tomllib is None:
        die("TOML support requires Python 3.11+ (stdlib tomllib) "
            "or the 'tomli' package (pip install tomli)")
    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        die(f"config file not found: {config_path}")
    except tomllib.TOMLDecodeError as e:
        die(f"config file parse error: {e}")

    profiles = config.get("profiles") or die("config file has no 'profiles' key")
    if profile_name not in profiles:
        die(f"profile '{profile_name}' not found "
            f"(available: {', '.join(sorted(profiles))})")

    profile = profiles[profile_name]
    _expand_paths(profile)
    return profile


def _expand_paths(profile):
    """Expand ~ in all path-valued fields of a profile."""
    exp = os.path.expanduser

    for key in ("ro_paths", "rw_paths"):
        if key in profile:
            profile[key] = [exp(p) for p in profile[key]]

    if "allowed_commands" in profile:
        # TOML bare true/false are booleans; restore the command name if a
        # boolean somehow ends up in the array (e.g. in a mixed-type array).
        profile["allowed_commands"] = [
            {True: "true", False: "false"}.get(cmd, str(cmd))
            for cmd in profile["allowed_commands"]
        ]

    if "tmpfs" in profile:
        for i, entry in enumerate(profile["tmpfs"]):
            if isinstance(entry, dict):
                entry["path"] = exp(entry["path"])
            else:
                profile["tmpfs"][i] = exp(entry)

    if "symlinks" in profile:
        profile["symlinks"] = {exp(k): exp(v) for k, v in profile["symlinks"].items()}

    if "env" in profile:
        profile["env"] = {
            k: exp(v) if isinstance(v, str) else v
            for k, v in profile["env"].items()
        }


# ---------------------------------------------------------------------------
# Script dependency scanning
# ---------------------------------------------------------------------------

_EXEC_RE = re.compile(r'^\s*exec\s+(?:-\w+\s+)*"?(/\S+)"?')


def scan_script_deps(path, _seen=None):
    """Find paths a shell script needs: shebang interpreter and exec targets.

    Returns a list of (original_path, real_path) tuples.
    Recurses into exec targets that are themselves scripts.
    """
    if _seen is None:
        _seen = set()
    if path in _seen:
        return []
    _seen.add(path)

    try:
        with open(path, "r", errors="replace") as f:
            lines = [f.readline() for _ in range(50)]
    except OSError:
        return []

    deps = []

    # Shebang
    if lines and lines[0].startswith("#!"):
        parts = lines[0][2:].strip().split()
        if parts:
            interp = parts[0]
            if interp.endswith("/env") and len(parts) > 1:
                resolved = shutil.which(parts[1])
                if resolved:
                    deps.append((interp, os.path.realpath(interp)))
                    deps.append((resolved, os.path.realpath(resolved)))
            else:
                deps.append((interp, os.path.realpath(interp)))

    # exec lines
    for line in lines:
        m = _EXEC_RE.match(line)
        if m:
            target = m.group(1).rstrip('"')
            real_target = os.path.realpath(target)
            deps.append((target, real_target))
            if os.path.isfile(real_target):
                deps.extend(scan_script_deps(real_target, _seen))

    return deps


def _resolve_binary_paths(name):
    """Resolve a binary name or absolute path to all its canonical filesystem paths.

    Returns a set containing the which/given path, its realpath, and paths for
    any shebang interpreters or exec targets found in the script (recursively).
    Returns an empty set if the binary cannot be found.
    """
    p = name if os.path.isabs(name) else shutil.which(name)
    if not p:
        return set()
    real = os.path.realpath(p)
    paths = {p, real}
    for orig, dep in scan_script_deps(real):
        if os.path.exists(dep):
            paths.add(dep)
            if orig != dep:
                paths.add(orig)
    return paths


# ---------------------------------------------------------------------------
# Bwrap command builder
# ---------------------------------------------------------------------------

class BwrapBuilder:
    """Accumulates bwrap arguments with deduplication of bind mounts."""

    def __init__(self):
        self.argv = ["bwrap"]
        self._bound = set()   # sandbox paths already bound (for binaries)
        self._mounts = set()  # filesystem paths already mounted (for ro/rw)

    # -- Low-level helpers --

    def _add(self, *args):
        self.argv.extend(args)

    def _flag_if(self, flag, condition):
        if condition:
            self._add(flag)

    def _ro_bind_at(self, real_path, sandbox_path):
        """Add --ro-bind if sandbox_path not already bound."""
        if sandbox_path not in self._bound:
            self._bound.add(sandbox_path)
            self._add("--ro-bind", real_path, sandbox_path)

    # -- Profile sections --

    def add_isolation(self, profile):
        self._add("--unshare-all")
        self._flag_if("--share-net", profile.get("share_net", False))
        self._flag_if("--new-session", profile.get("new_session", True))
        self._flag_if("--die-with-parent", profile.get("die_with_parent", True))
        hostname = profile.get("hostname")
        if hostname:
            self._add("--hostname", hostname)
        self._add("--dev", "/dev", "--proc", "/proc")

    def add_mounts(self, profile):
        for path in profile.get("ro_paths", []):
            self._mount(path, readonly=True)
        for path in profile.get("rw_paths", []):
            self._mount(path, readonly=False)
        for entry in profile.get("tmpfs", []):
            if isinstance(entry, dict):
                if "size" in entry:
                    self._add("--size", str(entry["size"]))
                self._add("--tmpfs", entry["path"])
            else:
                self._add("--tmpfs", entry)

    def _mount(self, path, readonly):
        path = os.path.abspath(path)
        if path in self._mounts:
            return
        self._mounts.add(path)
        self._bound.add(path)  # prevent bind_binary from emitting a duplicate bind
        if os.path.exists(path):
            self._add("--ro-bind" if readonly else "--bind", path, path)
        else:
            kind = "ro_path" if readonly else "rw_path"
            warn(f"{kind} does not exist, using try variant: {path}")
            self._add(("--ro-bind-try" if readonly else "--bind-try"), path, path)

    def add_allowed_commands(self, profile):
        for name in profile.get("allowed_commands", []):
            self.bind_binary(name)

    def add_symlinks(self, profile):
        for link_path, target in profile.get("symlinks", {}).items():
            self._add("--symlink", target, link_path)

    def add_env(self, profile):
        if "env" not in profile:
            return  # bwrap inherits calling process's environment by default
        self._add("--clearenv")
        for var, value in profile["env"].items():
            value = str(value)
            if value.startswith("$"):
                value = os.environ.get(value[1:], "")
            self._add("--setenv", var, value)

    # -- Binary resolution --

    def bind_binary(self, name):
        """Resolve a binary by name and bind it into the sandbox.

        Binds at up to three locations (deduplicated):
          /usr/bin/<name>, the which path, and the realpath.
        Also scans shell script wrappers for shebang/exec dependencies.

        Returns the which path on success, None if not found.
        """
        which_path = shutil.which(name)
        if not which_path:
            return None
        real_path = os.path.realpath(which_path)

        for sandbox_path in (f"/usr/bin/{name}", which_path, real_path):
            self._ro_bind_at(real_path, sandbox_path)

        # Bind script dependencies (shebang interpreters, exec targets)
        for orig, real in scan_script_deps(real_path):
            if os.path.exists(real):
                self._ro_bind_at(real, real)
                if orig != real:
                    self._ro_bind_at(real, orig)

        return which_path

    def bind_command(self, command):
        """Ensure the command to run is available inside the sandbox.

        Resolves the command binary and returns the (possibly rewritten)
        command list with sandbox paths.
        """
        exe = command[0]

        if not os.path.isabs(exe):
            which_path = self.bind_binary(exe)
            if not which_path:
                die(f"command '{exe}' not found on host")
            return [which_path, *command[1:]]

        # Absolute path
        real_path = os.path.realpath(exe)
        if not os.path.exists(real_path):
            die(f"command '{exe}' does not exist")
        self._ro_bind_at(real_path, exe)
        if real_path != exe:
            self._ro_bind_at(real_path, real_path)
        # Bind script dependencies (shebang interpreters, exec targets)
        for orig, real in scan_script_deps(real_path):
            if os.path.exists(real):
                self._ro_bind_at(real, real)
                if orig != real:
                    self._ro_bind_at(real, orig)
        return list(command)

    def finalize(self, command):
        self.argv.extend(["--", *command])
        return self.argv



# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _build_env(profile):
    """Build a clean environment dict from the profile's env section.

    Returns a dict with only the profile-specified variables, resolving any
    $VAR references from the current environment.  If the profile has no 'env'
    key, returns a copy of the current environment (no isolation).
    """
    if "env" not in profile:
        return dict(os.environ)
    return {
        var: (os.environ.get(str(val)[1:], "") if str(val).startswith("$") else str(val))
        for var, val in profile["env"].items()
    }


# ---------------------------------------------------------------------------
# Sandbox backends
# ---------------------------------------------------------------------------

class SandboxBackend(abc.ABC):
    """Abstract base class for sandbox backends."""

    name: str       # Human-readable name shown in warnings (e.g. "bwrap")
    flag_attr: str  # argparse attribute name for explicit selection (e.g. "bwrap")

    @classmethod
    @abc.abstractmethod
    def available(cls) -> bool:
        """Return True if this backend is usable on the current system."""

    @abc.abstractmethod
    def check_compat(self, profile) -> None:
        """Warn about profile options that this backend does not enforce."""

    @abc.abstractmethod
    def exec(self, profile, command) -> None:
        """Apply sandbox restrictions and exec command (never returns)."""

    def dry_run(self, profile, command) -> None:
        """Print what would be executed; default warns that it has no effect."""
        warn(f"--dry-run has no effect in {self.name} mode")

    # -- Shared helpers available to all backends --

    def _warn_compat(self, warnings: list[str]) -> None:
        """Emit a '<name> mode: <msg>' warning for each entry in warnings."""
        for msg in warnings:
            warn(f"{self.name} mode: {msg}")

    @staticmethod
    def _resolve_exe(command: list[str]) -> list[str]:
        """Resolve command[0] to an absolute path; dies if not found on PATH."""
        exe = command[0]
        if not os.path.isabs(exe):
            exe = shutil.which(exe) or die(f"command '{exe}' not found on host")
        elif not os.path.exists(exe):
            die(f"command '{exe}' does not exist")
        return [exe, *command[1:]]

    @staticmethod
    def _maybe_setsid(profile) -> None:
        """Call os.setsid() when the profile requests a new session (default: True)."""
        if profile.get("new_session", True):
            try:
                os.setsid()
            except OSError as e:
                # EPERM means we are already a session leader; that's fine
                if e.errno != 1:  # EPERM
                    die(f"setsid: {e}")
                warn(f"setsid: already session leader (pid {os.getpid()})")

    @staticmethod
    def _close_nonstandard_fds() -> None:
        """Close all file descriptors above stderr (3+) before exec.

        Prevents leaking parent/Python-internal fds into the sandboxed process,
        which could bypass filesystem restrictions via inherited open handles.
        """
        try:
            max_fd = os.sysconf("SC_OPEN_MAX")
        except (ValueError, OSError):
            max_fd = 1024
        os.closerange(3, max_fd)

    @staticmethod
    def _shell_quote(s: str) -> str:
        """Quote a token for display as part of a shell command."""
        return shlex.quote(s)

    def _collect_paths(self, profile, command):
        """Return (ro_paths, rw_paths) as sets of absolute paths.

        Combines the profile's ro/rw path lists with the resolved binary paths
        for command and every entry in allowed_commands (including shebang deps).
        """
        ro = {os.path.abspath(p) for p in profile.get("ro_paths", [])}
        rw = {os.path.abspath(p) for p in profile.get("rw_paths", [])}
        for name in [*profile.get("allowed_commands", []), command[0]]:
            ro |= _resolve_binary_paths(name)
        return ro, rw


class BwrapBackend(SandboxBackend):
    """bubblewrap namespace sandbox (Linux only)."""

    name      = "bwrap"
    flag_attr = "bwrap"

    # Number of arguments consumed by each bwrap option (beyond the flag itself)
    _OPT_ARITY = {
        "--ro-bind": 2, "--ro-bind-try": 2, "--bind": 2, "--bind-try": 2,
        "--setenv": 2, "--symlink": 2,
        "--hostname": 1, "--tmpfs": 1, "--dev": 1, "--proc": 1, "--size": 1,
    }

    @classmethod
    def available(cls) -> bool:
        return bool(shutil.which("bwrap"))

    def check_compat(self, profile) -> None:
        broad = {"/usr", "/usr/bin", "/bin", "/sbin", "/usr/sbin"}
        for path in profile.get("ro_paths", []) + profile.get("rw_paths", []):
            if os.path.abspath(path) in broad:
                warn(f"bwrap: {path} in paths exposes all host binaries "
                     f"and defeats allowed_commands allowlisting")

    def _build_argv(self, profile, command):
        """Build the full bwrap argv for the given profile and command."""
        builder = BwrapBuilder()
        builder.add_isolation(profile)
        builder.add_mounts(profile)
        builder.add_allowed_commands(profile)
        builder.add_symlinks(profile)
        builder.add_env(profile)
        return builder.finalize(builder.bind_command(command))

    @classmethod
    def _format_argv(cls, argv):
        """Format a bwrap argv as a readable, copy-pasteable shell command."""
        parts, i = [], 0
        while i < len(argv):
            arity = cls._OPT_ARITY.get(argv[i], 0)
            parts.append(" ".join(cls._shell_quote(argv[i + j]) for j in range(arity + 1)))
            i += arity + 1
        return " \\\n  ".join(parts)

    def exec(self, profile, command) -> None:
        bwrap = shutil.which("bwrap") or die("bwrap not found")
        os.execv(bwrap, self._build_argv(profile, command))

    def dry_run(self, profile, command) -> None:
        print(self._format_argv(self._build_argv(profile, command)))


class LandlockBackend(SandboxBackend):
    """Linux Landlock LSM sandbox (kernel 5.13+, no extra binaries required)."""

    name      = "Landlock"
    flag_attr = "landlock"

    # Architectures sharing the generic Landlock syscall numbers
    _ARCHES   = frozenset({"x86_64", "aarch64", "riscv64"})
    # landlock_create_ruleset, landlock_add_rule, landlock_restrict_self
    _SYSCALLS = (444, 445, 446)

    # Filesystem access rights
    _FS_EXECUTE    = 1 << 0
    _FS_WRITE_FILE = 1 << 1
    _FS_READ_FILE  = 1 << 2
    _FS_READ_DIR   = 1 << 3
    _FS_REMOVE_DIR  = 1 << 4
    _FS_REMOVE_FILE = 1 << 5
    _FS_MAKE_CHAR  = 1 << 6
    _FS_MAKE_DIR   = 1 << 7
    _FS_MAKE_REG   = 1 << 8
    _FS_MAKE_SOCK  = 1 << 9
    _FS_MAKE_FIFO  = 1 << 10
    _FS_MAKE_BLOCK = 1 << 11
    _FS_MAKE_SYM   = 1 << 12
    _FS_REFER      = 1 << 13  # ABI v2 (Linux 5.19)
    _FS_TRUNCATE   = 1 << 14  # ABI v3 (Linux 6.2)
    _FS_IOCTL_DEV  = 1 << 15  # ABI v5 (Linux 6.10)
    # Rights valid only for regular files (not directories)
    _FS_FILE_ONLY = _FS_EXECUTE | _FS_WRITE_FILE | _FS_READ_FILE | _FS_TRUNCATE | _FS_IOCTL_DEV
    _FS_READ_ONLY = _FS_EXECUTE | _FS_READ_FILE  | _FS_READ_DIR

    _RULE_PATH_BENEATH      = 1
    _CREATE_RULESET_VERSION = 1 << 0
    _PR_SET_NO_NEW_PRIVS    = 38
    _PR_SET_PDEATHSIG       = 1
    _SIGTERM                = 15

    # Paths that bwrap provides via --proc/--dev; always added as ro/rw since
    # Landlock has no mount namespace and processes need these pseudo-fs paths.
    _ESSENTIAL_RO_PATHS = ("/proc", "/sys")
    _ESSENTIAL_RW_PATHS = ("/dev",)   # /dev/null, /dev/urandom, /dev/tty, etc.

    class _RulesetAttr(ctypes.Structure):
        _fields_ = [("handled_access_fs", ctypes.c_uint64)]

    class _PathBeneathAttr(ctypes.Structure):
        _layout_ = "ms"
        _pack_ = 1
        _fields_ = [("allowed_access", ctypes.c_uint64), ("parent_fd", ctypes.c_int32)]

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _libc():
        """Load libc via ctypes, configuring syscall/prctl prototypes."""
        try:
            lib = ctypes.CDLL(ctypes.util.find_library("c") or "libc.so.6",
                              use_errno=True)
            lib.syscall.restype = ctypes.c_long
            lib.prctl.restype = ctypes.c_int
            return lib
        except Exception:
            return None

    @classmethod
    @functools.lru_cache(maxsize=None)
    def version(cls) -> int:
        """Return the supported Landlock ABI version, or 0 if unavailable."""
        if platform.machine() not in cls._ARCHES:
            return 0
        libc = cls._libc()
        if libc is None:
            return 0
        # Kernel requires attr=NULL and size=0 when LANDLOCK_CREATE_RULESET_VERSION is set
        ret = libc.syscall(
            ctypes.c_long(cls._SYSCALLS[0]),
            ctypes.c_void_p(None),
            ctypes.c_size_t(0),
            ctypes.c_uint32(cls._CREATE_RULESET_VERSION),
        )
        return int(ret) if ret >= 0 else 0

    @classmethod
    def _fs_all_rights(cls, version) -> int:
        """Return full FS access rights mask for the given Landlock ABI version."""
        rights = (1 << 13) - 1  # v1 (5.13): bits 0–12
        if version >= 2: rights |= cls._FS_REFER      # v2 (5.19)
        if version >= 3: rights |= cls._FS_TRUNCATE   # v3 (6.2)
        # v4 (6.7) added network rights only; no new FS rights
        if version >= 5: rights |= cls._FS_IOCTL_DEV  # v5 (6.10)
        return rights

    @classmethod
    def _add_path(cls, libc, add_nr, ruleset_fd, path, access):
        """Add a landlock_add_rule for path; silently skips non-existent paths.

        The kernel rejects directory-only rights (READ_DIR, MAKE_*, ...) for
        regular files, so we mask access to file-only rights for non-directories.
        """
        try:
            fd = os.open(path, os.O_PATH | os.O_CLOEXEC)
        except OSError:
            warn(f"landlock: path does not exist, skipping: {path}")
            return
        try:
            if not stat.S_ISDIR(os.fstat(fd).st_mode):
                access &= cls._FS_FILE_ONLY
            if not access:
                return
            rule = cls._PathBeneathAttr(allowed_access=access, parent_fd=fd)
            ret = int(libc.syscall(
                ctypes.c_long(add_nr),
                ctypes.c_int(ruleset_fd),
                ctypes.c_int(cls._RULE_PATH_BENEATH),
                ctypes.byref(rule),
                ctypes.c_uint32(0),
            ))
            if ret != 0:
                err = ctypes.get_errno()
                raise OSError(err, f"landlock_add_rule({path}): {os.strerror(err)}")
        finally:
            os.close(fd)

    @classmethod
    def _restrict(cls, ro_paths, rw_paths) -> bool:
        """Apply Landlock filesystem restrictions before exec.

        Grants read-only (execute/read) access to ro_paths and full access to
        rw_paths. Paths that do not exist are silently skipped.

        Note: calls prctl(PR_SET_NO_NEW_PRIVS), which prevents privilege
        escalation and new user namespaces, making Landlock incompatible with
        bubblewrap (which requires user namespaces).

        Returns True if restrictions were applied, False if unsupported.
        Raises OSError on syscall failure.
        """
        version = cls.version()
        if version == 0:
            return False
        libc = cls._libc()  # guaranteed non-None when version > 0

        create_nr, add_nr, restrict_nr = cls._SYSCALLS
        all_rights = cls._fs_all_rights(version)
        ro_rights  = cls._FS_READ_ONLY & all_rights

        attr = cls._RulesetAttr(all_rights)
        ruleset_fd = int(libc.syscall(
            ctypes.c_long(create_nr),
            ctypes.byref(attr),
            ctypes.c_size_t(ctypes.sizeof(attr)),
            ctypes.c_uint32(0),
        ))
        if ruleset_fd < 0:
            err = ctypes.get_errno()
            raise OSError(err, f"landlock_create_ruleset: {os.strerror(err)}")

        try:
            for path in sorted(ro_paths):
                cls._add_path(libc, add_nr, ruleset_fd, path, ro_rights)
            for path in sorted(rw_paths):
                cls._add_path(libc, add_nr, ruleset_fd, path, all_rights)

            ret = libc.prctl(
                ctypes.c_int(cls._PR_SET_NO_NEW_PRIVS),
                ctypes.c_ulong(1),
                ctypes.c_ulong(0), ctypes.c_ulong(0), ctypes.c_ulong(0),
            )
            if ret != 0:
                err = ctypes.get_errno()
                raise OSError(err, f"prctl(PR_SET_NO_NEW_PRIVS): {os.strerror(err)}")

            ret = int(libc.syscall(
                ctypes.c_long(restrict_nr),
                ctypes.c_int(ruleset_fd),
                ctypes.c_uint32(0),
            ))
            if ret != 0:
                err = ctypes.get_errno()
                raise OSError(err, f"landlock_restrict_self: {os.strerror(err)}")
        finally:
            os.close(ruleset_fd)

        return True

    @classmethod
    def available(cls) -> bool:
        return cls.version() > 0

    def check_compat(self, profile) -> None:
        self._warn_compat([
            msg for cond, msg in [
                (not profile.get("share_net", False),
                 "share_net: false (network is NOT isolated)"),
                (profile.get("hostname"),
                 "hostname (no UTS namespace)"),
                (profile.get("tmpfs"),
                 "tmpfs (no mount namespace)"),
                (profile.get("symlinks"),
                 "symlinks (no mount namespace)"),
                (profile.get("allowed_commands"),
                 "allowed_commands (exec filtering is less strict than bwrap: "
                 "binaries under ro_paths/rw_paths directories are also executable)"),
            ] if cond
        ])

    def _collect_paths(self, profile, command):
        """Extend the base path collection with Landlock-specific requirements.

        Adds _ESSENTIAL_RO_PATHS and _ESSENTIAL_RW_PATHS (which bwrap provides
        via --proc/--dev) since Landlock has no mount namespace and processes
        need these pseudo-fs paths (e.g. Bun/JSC reads /proc/self/maps for GC,
        /dev/urandom for crypto).

        Also promotes tmpfs paths to host rw_paths since Landlock cannot create
        new mounts; the process will access the real host path instead of a
        fresh tmpfs — this is already flagged by check_compat.
        """
        ro, rw = super()._collect_paths(profile, command)

        for p in self._ESSENTIAL_RO_PATHS:
            if os.path.exists(p):
                ro.add(p)
        for p in self._ESSENTIAL_RW_PATHS:
            if os.path.exists(p):
                rw.add(p)

        for entry in profile.get("tmpfs", []):
            path = entry["path"] if isinstance(entry, dict) else entry
            rw.add(os.path.abspath(path))

        return ro, rw

    def dry_run(self, profile, command) -> None:
        """Print the paths, environment, and command that would be sandboxed."""
        command = self._resolve_exe(command)
        ro, rw = self._collect_paths(profile, command)
        env = _build_env(profile)

        print("# Landlock ABI version:", self.version())
        print("# Read-only paths:")
        for p in sorted(ro - rw):
            print(f"  {p}")
        print("# Read-write paths:")
        for p in sorted(rw):
            print(f"  {p}")
        print("# Environment:")
        for k, v in sorted(env.items()):
            print(f"  {k}={v}")
        print("# Command:")
        print(" ".join(self._shell_quote(a) for a in command))

    def exec(self, profile, command) -> None:
        command = self._resolve_exe(command)
        ro, rw = self._collect_paths(profile, command)
        try:
            if not self._restrict(ro - rw, rw):
                die("landlock: not available on this kernel; "
                    "refusing to run unrestricted")
        except OSError as e:
            die(f"landlock: {e}")

        # Environment isolation (mutate os.environ so execv inherits it)
        if "env" in profile:
            os.environ.clear()
            os.environ.update(_build_env(profile))

        # setsid before PR_SET_PDEATHSIG (setsid may clear it on some kernels)
        self._maybe_setsid(profile)

        # die_with_parent: send SIGTERM when parent exits
        if profile.get("die_with_parent", True):
            libc = self._libc()
            if libc:
                ret = libc.prctl(
                    ctypes.c_int(self._PR_SET_PDEATHSIG), ctypes.c_ulong(self._SIGTERM),
                    ctypes.c_ulong(0), ctypes.c_ulong(0), ctypes.c_ulong(0),
                )
                if ret != 0:
                    die(f"prctl(PR_SET_PDEATHSIG): {os.strerror(ctypes.get_errno())}")
        self._close_nonstandard_fds()
        try:
            os.execv(command[0], command)
        except OSError as e:
            die(f"exec {command[0]!r}: {e}")


class SandboxExecBackend(SandboxBackend):
    """macOS Seatbelt sandbox via sandbox-exec and SBPL profiles."""

    name      = "sandbox-exec"
    flag_attr = "sandbox_exec"

    # Minimum SBPL rules required for any sandboxed process on macOS.
    _SBPL_BASELINE = """\
(version 1)
(deny default)
(allow signal (target self))
(allow process-fork)
(allow process-info-pidinfo)
(allow sysctl-read)
(allow file-read-metadata)
(allow file-read*
  (literal "/") (literal "/dev/null") (literal "/dev/random")
  (literal "/dev/urandom") (literal "/dev/zero") (literal "/dev/stdin")
  (literal "/dev/stdout") (literal "/dev/stderr")
  (subpath "/usr/lib") (subpath "/usr/share/locale") (subpath "/usr/share/icu")
  (subpath "/usr/share/zoneinfo") (subpath "/System/Library"))
(allow file-write*
  (literal "/dev/null") (literal "/dev/stdout") (literal "/dev/stderr"))
(allow file-ioctl
  (literal "/dev/tty") (regex #"^/dev/ttys[0-9]+$"))"""

    @classmethod
    def available(cls) -> bool:
        return sys.platform == "darwin" and bool(shutil.which("sandbox-exec"))

    def check_compat(self, profile) -> None:
        self._warn_compat([
            msg for cond, msg in [
                (profile.get("hostname"),
                 "hostname (no UTS namespace)"),
                (profile.get("tmpfs"),
                 "tmpfs (no mount namespace)"),
                (profile.get("symlinks"),
                 "symlinks (no mount namespace)"),
                (profile.get("die_with_parent", True),
                 "die_with_parent (not supported on macOS)"),
                (profile.get("allowed_commands"),
                 "allowed_commands (exec filtering is path-based only, "
                 "less strict than bwrap)"),
                (not profile.get("mach_services"),
                 "mach_services not set: all Mach IPC lookups are allowed "
                 "(set mach_services list in profile to restrict)"),
            ] if cond
        ])

    @staticmethod
    def _quote(path):
        """Quote a path for use in an SBPL expression."""
        return '"' + path.replace('\\', '\\\\').replace('"', '\\"') + '"'

    @classmethod
    def _path_rule(cls, ops, path):
        """Return an SBPL allow rule using (subpath ...) for dirs, (literal ...) for files."""
        kind = "subpath" if os.path.isdir(path) else "literal"
        return f"(allow {ops} ({kind} {cls._quote(path)}))"

    def _exec_paths(self, profile, command):
        """Return the set of binary paths allowed for process-exec, or None.

        Returns None when allowed_commands is absent, meaning all exec is allowed.
        Otherwise returns the resolved binary paths for command and allowed_commands
        only (not all ro_paths), since exec allowlisting is restricted to explicitly
        listed commands.
        """
        allowed = profile.get("allowed_commands", [])
        if not allowed:
            return None
        paths = set()
        for name in [*allowed, command[0]]:
            paths |= _resolve_binary_paths(name)
        return paths

    @staticmethod
    def _traversal_dirs(paths):
        """Return intermediate parent directories needed for SBPL path traversal.

        SBPL requires file-read* on each ancestor directory for the kernel to
        resolve path components when opening a target file.  Returns ancestors
        not already covered by an existing path (exact match or subpath of a
        directory in *paths*).
        """
        # Collect directory paths that have subpath coverage (directories get
        # (subpath ...) rules, so anything underneath is already covered)
        dir_paths = {p for p in paths if os.path.isdir(p)}

        parents = set()
        for path in paths:
            parent = os.path.dirname(path)
            while parent != '/':
                if parent in dir_paths:
                    break  # already covered by (subpath ...) rule
                parents.add(parent)
                parent = os.path.dirname(parent)
        parents -= paths
        return parents

    def _build_profile(self, profile, ro, rw, exec_paths, traversal_dirs=frozenset()):
        """Build an SBPL sandbox profile string from a jail profile."""
        lines = [self._SBPL_BASELINE]

        # Mach IPC: restrict to listed services if configured, otherwise allow all
        mach_services = profile.get("mach_services")
        if mach_services:
            for svc in mach_services:
                lines.append(f"(allow mach-lookup (global-name {self._quote(svc)}))")
        else:
            lines.append("(allow mach-lookup)")

        # Intermediate directory rules for path traversal (listing only)
        if traversal_dirs:
            literals = " ".join(f"(literal {self._quote(p)})" for p in sorted(traversal_dirs))
            lines.append(f"(allow file-read* {literals})")

        for path in sorted(ro - rw):
            lines.append(self._path_rule("file-read*", path))
        for path in sorted(rw):
            lines.append(self._path_rule("file-read* file-write*", path))

        if profile.get("share_net", False):
            lines += ["(allow network-outbound)", "(allow network-inbound)",
                      "(allow network-bind)"]

        if exec_paths is None:
            lines.append("(allow process-exec)")
        else:
            for path in sorted(exec_paths):
                lines.append(f"(allow process-exec (literal {self._quote(path)}))")

        return "\n".join(lines)

    def _prepare(self, profile, command):
        """Resolve the command and build the SBPL profile. Returns (command, sbpl)."""
        command = self._resolve_exe(command)
        ro, rw = self._collect_paths(profile, command)
        traversal = self._traversal_dirs(ro | rw)
        sbpl = self._build_profile(profile, ro, rw,
                                   self._exec_paths(profile, command), traversal)
        return command, sbpl

    def exec(self, profile, command) -> None:
        command, sbpl = self._prepare(profile, command)
        self._maybe_setsid(profile)
        # Note: no _close_nonstandard_fds() here — sandbox-exec is an external
        # wrapper; os.execvpe needs Python-internal fds until the exec completes.
        # sandbox-exec itself handles the sandboxed child's fd inheritance.
        os.execvpe("sandbox-exec", ["sandbox-exec", "-p", sbpl, *command],
                   _build_env(profile))

    def dry_run(self, profile, command) -> None:
        command, sbpl = self._prepare(profile, command)
        print("# SBPL sandbox profile:")
        print(sbpl)
        print()
        print("# Command:")
        cmd = ["sandbox-exec", "-p", "<profile above>", *command]
        print(" ".join(self._shell_quote(a) for a in cmd))


# Preferred auto-detection order: strongest isolation first
_BACKENDS: list[type[SandboxBackend]] = [BwrapBackend, SandboxExecBackend, LandlockBackend]


def _select_backend(args, profile) -> SandboxBackend:
    """Return the appropriate backend instance for the given args and profile.

    Explicit flags (--bwrap / --sandbox-exec / --landlock) take precedence.
    Otherwise, the first available backend in _BACKENDS order is used,
    skipping bwrap when the profile sets ``bwrap: false``.
    """
    # Honour explicit backend flags
    for cls in _BACKENDS:
        if getattr(args, cls.flag_attr, False):
            if not cls.available():
                die(f"--{cls.flag_attr.replace('_', '-')} requested "
                    f"but {cls.name} is not available")
            return cls()

    # Auto-detect: first available backend, optionally excluding bwrap
    skip_bwrap = not profile.get("bwrap", True)
    candidates = (cls for cls in _BACKENDS if not (skip_bwrap and cls is BwrapBackend)
                  and cls.available())
    cls = next(candidates, None)

    if cls is None:
        if skip_bwrap:
            die("profile sets bwrap: false but no alternative backend is available "
                "(sandbox-exec on macOS or Landlock on Linux 5.13+)")
        die("no sandbox backend available "
            "(install bwrap, use macOS with sandbox-exec, "
            "or use a kernel with Landlock support, Linux 5.13+)")

    if cls is LandlockBackend and not skip_bwrap:
        warn("bwrap not found, falling back to Landlock")

    return cls()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Sandbox a process using bubblewrap (default on Linux), macOS sandbox-exec "
            "(default on macOS), or Linux Landlock LSM. Backends are mutually exclusive."
        ),
        usage="%(prog)s -c CONFIG -p PROFILE [--ro PATH] [--rw PATH] "
              "[--bwrap | --sandbox-exec | --landlock] [--dry-run] [--] COMMAND [ARGS...]",
    )
    parser.add_argument("-c", "--config", required=True, help="Path to TOML config file")
    parser.add_argument("-p", "--profile", required=True, help="Profile name to use")
    parser.add_argument("--ro", action="append", default=[], metavar="PATH",
                        help="Additional read-only path (repeatable)")
    parser.add_argument("--rw", action="append", default=[], metavar="PATH",
                        help="Additional read-write path (repeatable)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--bwrap", action="store_true",
                       help="Use bubblewrap (default on Linux if installed)")
    group.add_argument("--sandbox-exec", dest="sandbox_exec", action="store_true",
                       help="Use macOS sandbox-exec (default on macOS)")
    group.add_argument("--landlock", action="store_true",
                       help="Use Linux Landlock LSM (default if bwrap is not installed)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the sandbox command without executing")
    parser.add_argument("command", nargs=argparse.REMAINDER,
                        help="Command to run inside the sandbox")
    args = parser.parse_args()

    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("no command specified")
    args.command = command

    return args


def main():
    args = parse_args()
    profile = load_profile(args.config, args.profile)

    profile.setdefault("rw_paths", []).append(os.getcwd())

    if args.ro:
        profile.setdefault("ro_paths", []).extend(os.path.abspath(p) for p in args.ro)
    if args.rw:
        profile.setdefault("rw_paths", []).extend(os.path.abspath(p) for p in args.rw)

    sandbox_backend = _select_backend(args, profile)
    sandbox_backend.check_compat(profile)

    if "env" not in profile:
        die("no 'env' key in profile: the full host environment would be passed "
            "to the sandbox (add an 'env' key to the profile to specify allowed variables)")

    if args.dry_run:
        sandbox_backend.dry_run(profile, args.command)
    else:
        sandbox_backend.exec(profile, args.command)


if __name__ == "__main__":
    main()
