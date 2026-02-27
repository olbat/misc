# AI Coding Agents supervision & monitoring tools

[bpftrace](https://github.com/bpftrace/bpftrace) scripts to monitor what AI coding agents are doing on your system. They trace a target process and all its descendants using kernel tracepoints, kprobes, and uprobes.

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

Monitors file operations: opens (read/write/create), reads, writes, deletes, renames, chmod, and chown. Tracks fd-to-filename mappings so that read/write syscalls display the file path and byte count.

```
sudo bpftrace trace-files.bt <PID>
```

### trace-suspicious.bt

Monitors suspicious or potentially abusive operations that a legitimate coding agent should rarely or never perform:

- **Credential/secret access** — opening SSH keys, GPG keyrings, `.aws/`, `.env`, token/secret files, `/etc/shadow`
- **Privilege escalation** — `setuid`/`setgid`/`setresuid`/`setresgid`, `capset`
- **Persistence mechanisms** — writing to crontabs, systemd unit files, shell startup files (`.bashrc`, `.zshrc`, etc.)
- **System manipulation** — `ptrace` (process injection), `mount`/`umount`, kernel module loading, hostname changes
- **Covert execution** — `memfd_create` (fileless execution), raw socket creation
- **Permission manipulation** — `chmod` with setuid/setgid bits

```
sudo bpftrace trace-suspicious.bt <PID>
```

### spy-agent.sh

Runs all four scripts in parallel against the same target PID. Ctrl-C stops all.

```
sudo ./spy-agent.sh <PID>
```
