# AI Coding Agents supervision & monitoring tools

[bpftrace](https://github.com/bpftrace/bpftrace) scripts to monitor what a process and all its descendants are doing on your system, using kernel tracepoints, kprobes, and uprobes.

Requires: Linux with BTF support (`CONFIG_DEBUG_INFO_BTF=y`), bpftrace >= 0.21.

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
./trace-process.sh -c confs/claude.conf -- claude --resume

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
| `confs/claude.conf` | [Claude Code](https://github.com/anthropics/claude-code) |
| `confs/codex.conf` | [OpenAI Codex CLI](https://github.com/openai/codex) |
| `confs/aider.conf` | [Aider](https://github.com/paul-gauthier/aider) |
| `confs/cline.conf` | [Cline](https://github.com/cline/cline) |
| `confs/goose.conf` | [Goose](https://github.com/block/goose) |
| `confs/continue.conf` | [Continue](https://github.com/continuedev/continue) |
| `confs/openhands.conf` | [OpenHands](https://github.com/All-Hands-AI/OpenHands) |

Precedence: defaults < env vars < config file < CLI options.
