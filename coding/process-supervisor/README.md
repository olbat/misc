# Process supervision & monitoring tools

Tools to monitor and sandbox processes on Linux and macOS. While primarily developed to supervise AI coding agents, all tools work with any process.

- **Monitoring** — [bpftrace](https://github.com/bpftrace/bpftrace) scripts that trace what a process and all its descendants are doing (exec, file, network, suspicious ops) using kernel tracepoints, kprobes, and uprobes. Requires Linux with BTF support (`CONFIG_DEBUG_INFO_BTF=y`), bpftrace >= 0.21.
- **Sandboxing** — a multi-backend jailing script that sandboxes processes with configurable filesystem, command, and network restrictions. Requires Python 3.6+ and PyYAML. Backend-specific requirements: [bubblewrap](https://github.com/containers/bubblewrap) (`bwrap`) on Linux, `sandbox-exec` on macOS (available by default), or Linux kernel 5.13+ for Landlock (no extra dependencies).

Example configuration files for popular AI coding agents are provided in the `confs/` directory.

## Table of Contents

- [Key tools](#key-tools)
  - [monitor-process.sh](#monitor-processsh) — all-in-one bpftrace monitoring wrapper
  - [jail-process.py](#jail-processpy) — multi-backend process sandboxing / jailing
- [Individual bpftrace scripts](#individual-bpftrace-scripts)
  - [trace-execs.bt](#trace-execsbt)
  - [trace-netcalls.bt](#trace-netcallsbt)
  - [trace-files.bt](#trace-filesbt)
  - [trace-suspicious.bt](#trace-suspiciousbt)
- [Configuration files](#configuration-files)
- [Sandbox profiles](#sandbox-profiles)

## Key tools

### monitor-process.sh

The main entry point for monitoring. Launches or attaches to any process and runs all [bpftrace](https://github.com/bpftrace/bpftrace) scripts in parallel. Traces are written to a log file (not the terminal). Supports selective tracer disabling and file-tracer output filtering.

```
# Run mode — launch a command and trace it
./monitor-process.sh -- <COMMAND> [ARGS...]

# Attach mode — trace an already-running process
./monitor-process.sh -p <PID>

# With a config file (e.g. for Claude Code)
./monitor-process.sh -c confs/monitor-claude.conf -- claude --resume

# Disable specific tracers
./monitor-process.sh -EN -- my-program run

# Follow traces in real time from another terminal
tail -f <log-file>
```

See `./monitor-process.sh -h` for all options.

### jail-process.py

Sandboxes any process using one of three backends, selected automatically based on the platform or overridden with a flag. Uses YAML profiles to configure what the process can access.

**Backends (mutually exclusive):**

| Flag | Backend | Platform | Isolation strength |
|---|---|---|---|
| `--bwrap` | [bubblewrap](https://github.com/containers/bubblewrap) | Linux | Strongest — full namespace isolation (PID, mount, network, user, IPC, UTS) |
| `--sandbox-exec` | macOS Seatbelt (`sandbox-exec`) | macOS | SBPL-based filesystem + network + exec control |
| `--landlock` | Linux Landlock LSM | Linux 5.13+ | Kernel-enforced filesystem allowlist; no namespace isolation |

The default is the first available backend in the order above. On Linux, bwrap is preferred; if absent, Landlock is used. On macOS, `sandbox-exec` is used. A profile can set `bwrap: false` to skip bwrap and prefer Landlock instead.

**What it restricts (bwrap, strongest):**
- **Filesystem** — only explicitly listed paths are mounted (read-only or read-write)
- **Commands** — only allowlisted binaries are available; `/usr/bin` is NOT mounted wholesale
- **Namespaces** — `--unshare-all` by default (PID, mount, network, user, IPC, UTS, cgroup)
- **Network** — denied by default, must be explicitly enabled per profile
- **Environment** — cleared and rebuilt from config only

Landlock and `sandbox-exec` enforce filesystem and exec restrictions but do not provide namespace or network isolation (Landlock) or mount/UTS namespaces (both). Warnings are printed when a profile option is unsupported by the selected backend.

```
# Dry-run — inspect what the sandbox would do (output depends on backend)
./jail-process.py -c confs/jail.yaml -p claude --dry-run -- claude

# Run a process inside the sandbox (auto-selects backend)
./jail-process.py -c confs/jail.yaml -p claude -- claude

# Add extra mounts from the command line
./jail-process.py -c confs/jail.yaml -p claude --rw ~/myproject --ro /opt/data -- claude

# Explicitly select a backend
./jail-process.py -c confs/jail.yaml -p claude --bwrap -- claude
./jail-process.py -c confs/jail.yaml -p claude --landlock -- claude
./jail-process.py -c confs/jail.yaml -p claude --sandbox-exec -- claude
```

See `./jail-process.py -h` for all options.

**Features:**
- Profiles defined in YAML (`confs/jail.yaml`), one per process/agent
- `~` expansion in all path fields for portable configs
- Automatic script dependency scanning — shell wrapper shebangs and `exec` targets are resolved and bound
- Binaries are bound at all their paths (canonical, `which`, and realpath) so they work regardless of how they're referenced
- `--dry-run` prints a readable summary of what would be sandboxed (bwrap command, Landlock path list, or SBPL profile)
- `--ro`/`--rw` CLI flags to add extra mounts without editing the config

## Individual bpftrace scripts

### trace-execs.bt

Monitors sub-processes spawned by the target process. Logs every `execve` call with the full command line.

```
sudo bpftrace trace-execs.bt <PID>
```

### trace-netcalls.bt

Monitors outbound network activity: TCP connects, DNS lookups (UDP port 53), data transfer (TX/RX for TCP and UDP), and hostname resolution via `getaddrinfo`. When a hostname is resolved before a connection, subsequent TCP events display the hostname alongside the IP address. Consecutive TCP send/receive events for the same connection are aggregated into a single line showing total bytes and call count.

```
sudo bpftrace trace-netcalls.bt <PID>
```

### trace-files.bt

Monitors file operations: opens (read/write/create), reads, writes, directory creation, deletes, renames, chmod, and chown. Tracks fd-to-filename mappings so that read/write syscalls display the file path and byte count.

```
sudo bpftrace trace-files.bt <PID>
```

### trace-suspicious.bt

Monitors suspicious or potentially dangerous operations:

- **Credential/secret access** — opening SSH keys, GPG keyrings, Cloud credentials, `.env`, token/secret files, etc.
- **Privilege escalation** — `setuid`/`setgid`/`setresuid`/`setresgid`, `capset`
- **Persistence mechanisms** — writing to crontabs, systemd unit files, shell startup files (`.bashrc`, `.zshrc`, etc.)
- **System manipulation** — `ptrace` (process injection), `mount`/`umount`, kernel module loading, hostname changes
- **Covert execution** — `memfd_create` (fileless execution), raw socket creation
- **Listening sockets / reverse shells** — `bind`, `listen`, `accept`/`accept4`
- **Cross-process memory access** — `process_vm_readv`/`process_vm_writev`
- **Namespace / sandbox escape** — `unshare`, `chroot`, `pivot_root`
- **Code injection / anti-forensics** — `mprotect` with PROT_EXEC, `prctl` PR_SET_DUMPABLE=0, `seccomp`, `personality`, `userfaultfd`
- **Symlink / hardlink attacks** — `symlinkat`, `linkat`
- **Credential keyring access** — `keyctl`
- **Destructive actions** — `reboot`, `kill` outside watched process tree
- **Permission manipulation** — `chmod` with setuid/setgid bits

```
sudo bpftrace trace-suspicious.bt <PID>
```

## Configuration files

`monitor-process.sh` options can be set via CLI flags, environment variables, or a config file sourced with `-c`. Example config files for popular AI coding agents are provided in the `confs/` directory:

| Config file | Tool |
|---|---|
| `confs/monitor-claude.conf` | [Claude Code](https://github.com/anthropics/claude-code) |
| `confs/monitor-codex.conf` | [OpenAI Codex CLI](https://github.com/openai/codex) |
| `confs/monitor-aider.conf` | [Aider](https://github.com/paul-gauthier/aider) |
| `confs/monitor-cline.conf` | [Cline](https://github.com/cline/cline) |
| `confs/monitor-goose.conf` | [Goose](https://github.com/block/goose) |
| `confs/monitor-continue.conf` | [Continue](https://github.com/continuedev/continue) |
| `confs/monitor-openhands.conf` | [OpenHands](https://github.com/All-Hands-AI/OpenHands) |

Precedence: defaults < env vars < config file < CLI options.

## Sandbox profiles

Pre-configured profiles for popular AI coding agents are provided in `confs/jail.yaml`. Any process can be jailed by adding a new profile to this file.

| Profile | Tool | Agent state directory |
|---|---|---|
| `claude` | [Claude Code](https://github.com/anthropics/claude-code) | `~/.claude`, `~/.claude.json` |
| `codex` | [OpenAI Codex CLI](https://github.com/openai/codex) | `~/.codex` |
| `aider` | [Aider](https://github.com/paul-gauthier/aider) | `~/.config/aider`, `~/.aider.conf.yml` |
| `cline` | [Cline](https://github.com/cline/cline) | `~/.cline` |
| `goose` | [Goose](https://github.com/block/goose) | `~/.config/goose` |
| `continue` | [Continue](https://github.com/continuedev/continue) | `~/.continue` |
| `openhands` | [OpenHands](https://github.com/All-Hands-AI/OpenHands) | `~/.openhands` |

Each profile mounts shared libraries (`/usr/lib`, `/lib`, `/lib64`) read-only, the agent's state directory read-write, and whitelists a minimal set of commands. Edit `~/project` in the config to point at your working directory.
