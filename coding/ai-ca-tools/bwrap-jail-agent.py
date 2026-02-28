#!/usr/bin/env python3
"""
bwrap-jail-agent.py

Sandboxes AI coding agent processes using bubblewrap (bwrap).
Builds a bwrap command from a named YAML profile that specifies
filesystem mounts, allowed commands, environment, and isolation options.

Usage:
  bwrap-jail-agent.py -c CONFIG -p PROFILE [--ro PATH] [--rw PATH] [--dry-run] [--] COMMAND [ARGS...]

Example:
  bwrap-jail-agent.py -c confs/jail.yaml -p claude --dry-run -- /bin/bash
  bwrap-jail-agent.py -c confs/jail.yaml -p claude --rw ~/project --ro /opt/data -- ls /
"""

import argparse
import os
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
        description="Sandbox AI coding agents using bubblewrap (bwrap).",
        usage="%(prog)s -c CONFIG -p PROFILE [--ro PATH] [--rw PATH] [--dry-run] [--] COMMAND [ARGS...]",
    )
    parser.add_argument("-c", "--config", required=True, help="Path to YAML config file")
    parser.add_argument("-p", "--profile", required=True, help="Profile name to use")
    parser.add_argument("--ro", action="append", default=[], metavar="PATH",
                        help="Additional read-only bind mount (repeatable)")
    parser.add_argument("--rw", action="append", default=[], metavar="PATH",
                        help="Additional read-write bind mount (repeatable)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the bwrap command without executing")
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

    argv = build_bwrap_argv(profile, args.command)

    if args.dry_run:
        print(format_argv(argv))
    else:
        os.execvp("bwrap", argv)


if __name__ == "__main__":
    main()
