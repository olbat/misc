# AI Agents supervision & monitoring tools

Tools to monitor and sandbox AI coding agent processes on Linux.

- **Monitoring** — [bpftrace](https://github.com/bpftrace/bpftrace) scripts that trace what a process and all its descendants are doing (exec, file, network, suspicious ops) using kernel tracepoints, kprobes, and uprobes. Requires Linux with BTF support (`CONFIG_DEBUG_INFO_BTF=y`), bpftrace >= 0.21.
- **Sandboxing** — a [bubblewrap](https://github.com/containers/bubblewrap) wrapper that jails agent processes with configurable filesystem, command, and network restrictions. Requires bwrap, Python 3.6+, PyYAML.

## Scripts

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

- **Credential/secret access** — opening SSH keys, GPG keyrings, `.aws/`, `.env`, token/secret files, `.netrc`
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

### trace-process.sh

Wrapper that launches or attaches to a process and runs the bpftrace scripts in parallel. Traces are written to a log file (not the terminal). Supports selective tracer disabling and file-tracer output filtering.

```
# Run mode — launch a command and trace it
./trace-process.sh -- <COMMAND> [ARGS...]

# Attach mode — trace an already-running process
./trace-process.sh -p <PID>

# With a config file (e.g. for Claude Code)
./trace-process.sh -c confs/trace-claude.conf -- claude --resume

# Disable specific tracers
./trace-process.sh -EN -- my-program run

# Follow traces in real time from another terminal
tail -f <log-file>
```

See `./trace-process.sh -h` for all options.

### Configuration

`trace-process.sh` options can be set via CLI flags, environment variables, or a config file sourced with `-c`. Process-specific config files are provided in the `confs/` directory for popular AI coding agents:

| Config file | Tool |
|---|---|
| `confs/trace-claude.conf` | [Claude Code](https://github.com/anthropics/claude-code) |
| `confs/trace-codex.conf` | [OpenAI Codex CLI](https://github.com/openai/codex) |
| `confs/trace-aider.conf` | [Aider](https://github.com/paul-gauthier/aider) |
| `confs/trace-cline.conf` | [Cline](https://github.com/cline/cline) |
| `confs/trace-goose.conf` | [Goose](https://github.com/block/goose) |
| `confs/trace-continue.conf` | [Continue](https://github.com/continuedev/continue) |
| `confs/trace-openhands.conf` | [OpenHands](https://github.com/All-Hands-AI/OpenHands) |

Precedence: defaults < env vars < config file < CLI options.

## Sandboxing

### bwrap-jail-agent.py

Wraps [bubblewrap](https://github.com/containers/bubblewrap) to sandbox AI coding agents with least-privilege restrictions. Uses YAML profiles to configure what the agent can access.

**What it restricts:**
- **Filesystem** — only explicitly listed paths are mounted (read-only or read-write)
- **Commands** — only whitelisted binaries are available; `/usr/bin` is NOT mounted wholesale
- **Namespaces** — `--unshare-all` by default (PID, mount, network, user, IPC, UTS, cgroup)
- **Network** — denied by default, must be explicitly enabled per profile
- **Environment** — cleared and rebuilt from config only

```
# Dry-run — inspect the generated bwrap command
python3 bwrap-jail-agent.py -c confs/jail.yaml -p claude --dry-run -- claude

# Run an agent inside the sandbox
python3 bwrap-jail-agent.py -c confs/jail.yaml -p claude -- claude

# Add extra mounts from the command line
python3 bwrap-jail-agent.py -c confs/jail.yaml -p claude --rw ~/myproject --ro /opt/data -- claude
```

See `python3 bwrap-jail-agent.py -h` for all options.

**Features:**
- Profiles defined in YAML (`confs/jail.yaml`), one per agent
- `~` expansion in all path fields for portable configs
- Automatic script dependency scanning — shell wrapper shebangs and `exec` targets are resolved and bound
- Binaries are bound at all their paths (canonical, `which`, and realpath) so they work regardless of how they're referenced
- `--dry-run` prints a readable, copy-pasteable bwrap command
- `--ro`/`--rw` CLI flags to add extra mounts without editing the config

### Sandbox profiles

Pre-configured profiles are provided in `confs/jail.yaml`:

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
