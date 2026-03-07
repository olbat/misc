#!/usr/bin/env python3
"""
jail-process.py

Sandboxes processes using one of two backends (mutually exclusive):

  bwrap     — bubblewrap namespace isolation: separate mount, PID, network,
              user, IPC, and UTS namespaces; filesystem and command allowlists;
              environment clearing. Requires bwrap to be installed.

  landlock  — Linux Landlock LSM: kernel-enforced filesystem allowlist and
              exec filtering, plus environment isolation. No extra privileges
              or binaries required. Requires Linux 5.13+.

The default backend is whichever is available, preferring bwrap (stronger
isolation). The two backends cannot be combined: Landlock requires
prctl(PR_SET_NO_NEW_PRIVS), which prevents the user-namespace creation
that bwrap relies on.

Usage:
  jail-process.py -c CONFIG -p PROFILE [--ro PATH] [--rw PATH]
                [--bwrap | --landlock] [--dry-run] [--] COMMAND [ARGS...]

Example:
  jail-process.py -c confs/jail.yaml -p claude -- claude --resume
  jail-process.py -c confs/jail.yaml -p aider --dry-run -- aider
  jail-process.py -c confs/jail.yaml -p shell --rw ~/project --ro /opt/data -- bash
  jail-process.py -c confs/jail.yaml -p shell --landlock -- bash
  jail-process.py -c confs/jail.yaml -p shell --bwrap -- bash
"""

import argparse
import ctypes
import ctypes.util
import functools
import os
import platform
import re
import shutil
import sys

import yaml


def die(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def warn(msg):
    print(f"Warning: {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_profile(config_path, profile_name):
    """Load a named profile from the YAML config, with ~ expansion."""
    with open(config_path) as f:
        config = yaml.safe_load(f)

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
        # YAML parses bare `true`/`false` as Python booleans; restore the command name
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
            lines = f.readlines(4096)
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
        if os.path.exists(path):
            self._add("--ro-bind" if readonly else "--bind", path, path)
        else:
            kind = "ro_path" if readonly else "rw_path"
            warn(f"{kind} does not exist, using try variant: {path}")
            self._add(("--ro-bind-try" if readonly else "--bind-try"), path, path)

    def add_allowed_commands(self, profile):
        for name in profile.get("allowed_commands", []):
            if not self.bind_binary(name):
                die(f"allowed_command '{name}' not found on host")

    def add_symlinks(self, profile):
        for link_path, target in profile.get("symlinks", {}).items():
            self._add("--symlink", target, link_path)

    def add_env(self, profile):
        self._add("--clearenv")
        for var, value in profile.get("env", {}).items():
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
        return list(command)

    def finalize(self, command):
        self.argv.extend(["--", *command])
        return self.argv


def build_bwrap_argv(profile, command):
    """Build the full bwrap argument vector from a profile and command."""
    b = BwrapBuilder()
    b.add_isolation(profile)
    b.add_mounts(profile)
    b.add_allowed_commands(profile)
    command = b.bind_command(command)
    b.add_symlinks(profile)
    b.add_env(profile)
    return b.finalize(command)


# ---------------------------------------------------------------------------
# Landlock LSM support
# ---------------------------------------------------------------------------

# Syscall numbers for landlock_create_ruleset / landlock_add_rule / landlock_restrict_self.
# All supported architectures share the same numbers (generic kernel syscall table).
_LANDLOCK_ARCHES   = frozenset({"x86_64", "aarch64", "riscv64"})
_LANDLOCK_SYSCALLS = (444, 445, 446)

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

_FS_READ_ONLY = _FS_EXECUTE | _FS_READ_FILE | _FS_READ_DIR

_RULE_PATH_BENEATH      = 1
_CREATE_RULESET_VERSION = 1 << 0
_PR_SET_NO_NEW_PRIVS    = 38
_PR_SET_PDEATHSIG       = 1
_SIGTERM                = 15


class _RulesetAttr(ctypes.Structure):
    _fields_ = [("handled_access_fs", ctypes.c_uint64)]


class _PathBeneathAttr(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("allowed_access", ctypes.c_uint64),
        ("parent_fd", ctypes.c_int32),
    ]


def _fs_all_rights(version):
    """Return full FS access rights mask for the given Landlock ABI version."""
    rights = (1 << 13) - 1  # v1 (5.13): bits 0–12
    if version >= 2:
        rights |= _FS_REFER      # v2 (5.19)
    if version >= 3:
        rights |= _FS_TRUNCATE   # v3 (6.2)
    # v4 (6.7) added network rights only; no new FS rights
    if version >= 5:
        rights |= _FS_IOCTL_DEV  # v5 (6.10)
    return rights


@functools.lru_cache(maxsize=None)
def _get_libc():
    """Load libc via ctypes, configuring syscall/prctl prototypes."""
    try:
        lib = ctypes.CDLL(ctypes.util.find_library("c") or "libc.so.6",
                          use_errno=True)
        lib.syscall.restype = ctypes.c_long
        lib.prctl.restype = ctypes.c_int
        return lib
    except Exception:
        return None


@functools.lru_cache(maxsize=None)
def landlock_version():
    """Return the supported Landlock ABI version, or 0 if not available."""
    if platform.machine() not in _LANDLOCK_ARCHES:
        return 0
    libc = _get_libc()
    if libc is None:
        return 0
    # Kernel requires attr=NULL and size=0 when LANDLOCK_CREATE_RULESET_VERSION is set
    ret = libc.syscall(
        ctypes.c_long(_LANDLOCK_SYSCALLS[0]),
        ctypes.c_void_p(None),
        ctypes.c_size_t(0),
        ctypes.c_uint32(_CREATE_RULESET_VERSION),
    )
    return int(ret) if ret >= 0 else 0


def _ll_add_path(libc, add_nr, ruleset_fd, path, access):
    """Add a landlock_add_rule for path; silently skips non-existent paths.

    The kernel rejects directory-only rights (READ_DIR, MAKE_*, ...) for
    regular files, so we mask access to file-only rights for non-directories.
    """
    try:
        fd = os.open(path, os.O_PATH | os.O_CLOEXEC)
    except OSError:
        return
    try:
        if not os.path.isdir(path):
            access &= _FS_FILE_ONLY
        if not access:
            return
        rule = _PathBeneathAttr(allowed_access=access, parent_fd=fd)
        ret = int(libc.syscall(
            ctypes.c_long(add_nr),
            ctypes.c_int(ruleset_fd),
            ctypes.c_int(_RULE_PATH_BENEATH),
            ctypes.byref(rule),
            ctypes.c_uint32(0),
        ))
        if ret != 0:
            err = ctypes.get_errno()
            warn(f"landlock: add_rule failed for {path}: {os.strerror(err)}")
    finally:
        os.close(fd)


def apply_landlock(ro_paths, rw_paths):
    """Apply Landlock filesystem restrictions before exec.

    Grants read-only (execute/read) access to ro_paths and full access to
    rw_paths. Paths that do not exist are silently skipped.

    Note: this calls prctl(PR_SET_NO_NEW_PRIVS), which prevents the process
    from gaining privileges via setuid/capabilities and also prevents creating
    new user namespaces. This makes Landlock incompatible with bubblewrap
    (which creates user namespaces for isolation); the two backends are mutually exclusive.

    Returns True if Landlock was applied, False if the kernel does not support
    it or the architecture is unsupported. Raises OSError on syscall failure.
    """
    version = landlock_version()
    if version == 0:
        return False
    libc = _get_libc()  # guaranteed non-None when version > 0

    create_nr, add_nr, restrict_nr = _LANDLOCK_SYSCALLS
    all_rights = _fs_all_rights(version)
    ro_rights = _FS_READ_ONLY & all_rights

    attr = _RulesetAttr(all_rights)
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
            _ll_add_path(libc, add_nr, ruleset_fd, path, ro_rights)
        for path in sorted(rw_paths):
            _ll_add_path(libc, add_nr, ruleset_fd, path, all_rights)

        ret = libc.prctl(
            ctypes.c_int(_PR_SET_NO_NEW_PRIVS),
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


# ---------------------------------------------------------------------------
# Profile compatibility checks
# ---------------------------------------------------------------------------

def _check_profile_compat(profile, use_bwrap):
    """Warn about profile options that won't be enforced by the selected backend."""
    if use_bwrap:
        # bwrap enforces all options; warn about paths that undermine isolation
        broad = {"/usr", "/usr/bin", "/bin", "/sbin", "/usr/sbin"}
        for path in profile.get("ro_paths", []) + profile.get("rw_paths", []):
            if os.path.abspath(path) in broad:
                warn(f"bwrap: {path} in paths exposes all host binaries "
                     f"and defeats allowed_commands allowlisting")
    else:
        # Landlock cannot enforce namespace-based features
        not_enforced = []
        if not profile.get("share_net", False):
            not_enforced.append("share_net: false (network is NOT isolated)")
        if profile.get("hostname"):
            not_enforced.append("hostname (no UTS namespace)")
        if profile.get("tmpfs"):
            not_enforced.append("tmpfs (no mount namespace)")
        if profile.get("symlinks"):
            not_enforced.append("symlinks (no mount namespace)")
        if profile.get("allowed_commands"):
            not_enforced.append(
                "allowed_commands (exec filtering is less strict than bwrap: "
                "binaries under ro_paths/rw_paths directories are also executable)"
            )
        for msg in not_enforced:
            warn(f"Landlock mode: {msg}")


# ---------------------------------------------------------------------------
# Landlock mode
# ---------------------------------------------------------------------------

def _apply_env(profile):
    """Clear the environment and rebuild it from the profile's env section."""
    os.environ.clear()
    for var, val in profile.get("env", {}).items():
        val = str(val)
        os.environ[var] = os.environ.get(val[1:], "") if val.startswith("$") else val


def collect_landlock_paths(profile, command):
    """Collect host filesystem paths needed for Landlock mode.

    Returns (ro_paths, rw_paths) as sets of absolute paths.
    Includes ro_paths/rw_paths from the profile, plus the resolved binary
    paths for all allowed_commands and the command itself.
    """
    ro = {os.path.abspath(p) for p in profile.get("ro_paths", [])}
    rw = {os.path.abspath(p) for p in profile.get("rw_paths", [])}

    names = [*profile.get("allowed_commands", []), command[0]]

    for name in names:
        p = name if os.path.isabs(name) else shutil.which(name)
        if not p:
            continue
        real = os.path.realpath(p)
        ro.update([p, real])
        for orig, dep in scan_script_deps(real):
            if os.path.exists(dep):
                ro.add(dep)
                if orig != dep:
                    ro.add(orig)

    return ro, rw


def exec_landlock(profile, command):
    """Apply Landlock + env isolation and exec the command directly.

    Provides:
      - Filesystem access allowlist (Landlock)
      - Exec allowlist via Landlock EXECUTE right on specific binary paths
      - Environment isolation (clearenv + setenv)
      - die_with_parent (prctl PR_SET_PDEATHSIG)
      - new_session (os.setsid)

    Does NOT provide: network isolation, mount/PID/UTS namespace, tmpfs, symlinks.
    """
    # Resolve command executable
    exe = command[0]
    if not os.path.isabs(exe):
        exe = shutil.which(exe) or die(f"command '{exe}' not found on host")

    # Apply Landlock filesystem restrictions
    ro, rw = collect_landlock_paths(profile, command)
    try:
        if not apply_landlock(ro - rw, rw):
            warn("landlock: not available on this kernel, running unrestricted")
    except OSError as e:
        warn(f"landlock: {e}")

    # Environment isolation
    if "env" in profile:
        _apply_env(profile)

    # die_with_parent: send SIGTERM when parent exits
    if profile.get("die_with_parent", True):
        libc = _get_libc()
        if libc:
            libc.prctl(
                ctypes.c_int(_PR_SET_PDEATHSIG), ctypes.c_ulong(_SIGTERM),
                ctypes.c_ulong(0), ctypes.c_ulong(0), ctypes.c_ulong(0),
            )

    # new_session
    if profile.get("new_session", True):
        try:
            os.setsid()
        except OSError:
            pass

    os.execv(exe, [exe, *command[1:]])


# ---------------------------------------------------------------------------
# Dry-run formatting
# ---------------------------------------------------------------------------

# Number of arguments each bwrap option consumes
_BWRAP_OPT_ARITY = {
    "--ro-bind": 2, "--ro-bind-try": 2, "--bind": 2, "--bind-try": 2,
    "--setenv": 2, "--symlink": 2,
    "--hostname": 1, "--tmpfs": 1, "--dev": 1, "--proc": 1, "--size": 1,
}


def format_argv(argv):
    """Format a bwrap argv as a readable, copy-pasteable shell command."""
    def quote(s):
        return f"'{s}'" if " " in s or not s else s

    parts = []
    i = 0
    while i < len(argv):
        arity = _BWRAP_OPT_ARITY.get(argv[i], 0)
        parts.append(" ".join(quote(argv[i + j]) for j in range(arity + 1)))
        i += arity + 1
    return " \\\n  ".join(parts)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Sandbox a process using bubblewrap (default) or Linux Landlock LSM. "
            "The two backends are mutually exclusive."
        ),
        usage="%(prog)s -c CONFIG -p PROFILE [--ro PATH] [--rw PATH] "
              "[--landlock] [--dry-run] [--] COMMAND [ARGS...]",
    )
    parser.add_argument("-c", "--config", required=True, help="Path to YAML config file")
    parser.add_argument("-p", "--profile", required=True, help="Profile name to use")
    parser.add_argument("--ro", action="append", default=[], metavar="PATH",
                        help="Additional read-only path (repeatable)")
    parser.add_argument("--rw", action="append", default=[], metavar="PATH",
                        help="Additional read-write path (repeatable)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--bwrap", action="store_true",
                       help="Use bubblewrap (default if installed)")
    group.add_argument("--landlock", action="store_true",
                       help="Use Linux Landlock LSM (default if bwrap is not installed)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the bwrap command without executing (bwrap mode only)")
    parser.add_argument("command", nargs=argparse.REMAINDER,
                        help="Command to run inside the sandbox")
    args = parser.parse_args()

    # Strip leading '--' separator
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

    # Merge CLI paths into profile
    if args.ro:
        profile.setdefault("ro_paths", []).extend(os.path.abspath(p) for p in args.ro)
    if args.rw:
        profile.setdefault("rw_paths", []).extend(os.path.abspath(p) for p in args.rw)

    bwrap_available    = bool(shutil.which("bwrap"))
    landlock_available = landlock_version() > 0

    # Resolve which backend to use
    if args.bwrap:
        if not bwrap_available:
            die("--bwrap requested but bwrap is not installed")
        use_bwrap = True
    elif args.landlock:
        if not landlock_available:
            die("--landlock requested but Landlock is not supported on this kernel")
        use_bwrap = False
    elif not profile.get("bwrap", True):
        # Profile explicitly opts in to Landlock mode
        if not landlock_available:
            die("profile sets bwrap: false but Landlock is not supported on this kernel")
        use_bwrap = False
    elif bwrap_available:
        use_bwrap = True
    elif landlock_available:
        warn("bwrap not found, falling back to Landlock")
        use_bwrap = False
    else:
        die("no sandbox backend available "
            "(install bwrap or use a kernel with Landlock support, Linux 5.13+)")

    _check_profile_compat(profile, use_bwrap)

    # --- Landlock mode ---
    if not use_bwrap:
        if args.dry_run:
            warn("--dry-run has no effect in Landlock mode")
            return
        exec_landlock(profile, args.command)
        return  # unreachable — exec replaces the process

    # --- Bwrap mode ---
    argv = build_bwrap_argv(profile, args.command)

    if args.dry_run:
        print(format_argv(argv))
        return

    os.execvp("bwrap", argv)


if __name__ == "__main__":
    main()
