#!/usr/bin/env bash
#
# trace-process.sh
#
# Attaches bpftrace scripts (execs, files, netcalls, suspicious) with
# elevated privileges to monitor a process and all its descendants.
#
# Two modes:
#   Run mode:    Launch a command and trace it (default)
#   Attach mode: Attach to an already-running process (-p PID)
#
# In run mode, trace output is written to a log file (not the terminal)
# to avoid interleaving with the process's own output. Use -o/--output
# to set a custom path, otherwise a temporary file is used.
# In attach mode (-p), traces go to stdout by default.
#
# Options can also be set via environment variables or a config file
# sourced with -c/--config (see --help for details).
#
# Stops tracing when the process exits or on Ctrl-C / SIGTERM.
#
# Usage:
#   ./trace-process.sh [OPTIONS] -- <COMMAND> [ARGS...]
#   ./trace-process.sh [OPTIONS] -p <PID>
#
# Options:
#   -c, --config FILE          Source env vars from FILE before applying
#                              defaults (CLI options override config)
#   -p, --pid PID              Attach to an existing process instead of
#                              launching a new one
#   -o, --output FILE          Write traces to FILE (default: temp file)
#   -f, --filter REGEX         Exclude file-tracer lines matching REGEX
#                              (grep -vE; see trace-claude.conf for an example)
#       --no-filter            Disable the exclusion filter
#   -E, --disable-execs        Disable subprocess/exec tracing
#   -F, --disable-files        Disable file operation tracing
#   -N, --disable-netcalls     Disable network call tracing
#   -S, --disable-suspicious   Disable suspicious operation tracing
#   -h, --help                 Show this help message

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# --- Defaults (env vars and config file values take precedence) ---
TRACE_EXECS="${TRACE_EXECS:-1}"
TRACE_FILES="${TRACE_FILES:-1}"
TRACE_NETCALLS="${TRACE_NETCALLS:-1}"
TRACE_SUSPICIOUS="${TRACE_SUSPICIOUS:-1}"
LOG_FILE="${LOG_FILE:-}"
ATTACH_PID="${ATTACH_PID:-}"
FILE_FILTER="${FILE_FILTER:-}"

# --- Usage ---
usage() {
    cat >&2 <<EOF
Usage:
  $0 [OPTIONS] -- <COMMAND> [ARGS...]   (run mode)
  $0 [OPTIONS] -p <PID>                 (attach mode)

Attach bpftrace monitors to a process.

In run mode, the command is launched as the current user and traced.
In attach mode (-p), tracers attach to an already-running process.

This script must NOT be run as root — the traced process should run
unprivileged. Sudo credentials will be requested for bpftrace only.

In run mode, trace output goes to a log file (to avoid interleaving with
the process's own output). To follow traces in real time, open another
terminal and run:

  tail -f <log-file>

In attach mode (-p), traces go to stdout by default. Use -o/--output to
redirect to a file instead.

Options:
  -c, --config FILE          Source env vars from FILE (see below)
  -p, --pid PID              Attach to an existing process instead of
                             launching a new one
  -o, --output FILE          Write traces to FILE (default: temp file)
  -f, --filter REGEX         Exclude file-tracer lines matching REGEX
                             (grep -vE; see trace-claude.conf for an example)
      --no-filter            Disable the exclusion filter
  -E, --disable-execs        Disable subprocess/exec tracing
  -F, --disable-files        Disable file operation tracing
  -N, --disable-netcalls     Disable network call tracing
  -S, --disable-suspicious   Disable suspicious operation tracing
  -h, --help                 Show this help message

Configuration:
  Use -c/--config or set env vars directly. The config file is sourced
  as bash and can set any of these variables:

    TRACE_EXECS=0
    TRACE_NETCALLS=0
    FILE_FILTER="/dev/tty|/proc/"
    LOG_FILE="/tmp/my-traces.log"

  Precedence: defaults < env vars < config file < CLI options.
  Process-specific configs can be provided (e.g. trace-claude.conf).

Example:
  $0 -c trace-claude.conf -- claude --resume
  $0 -p 12345
  $0 -c my.conf -o traces.log -- my-program run
  $0 -EN -- my-program run
  $0 --no-filter -- aider
  TRACE_EXECS=0 $0 -- codex
EOF
    exit 1
}

# --- Refuse to run as root ---
if [[ $(id -u) -eq 0 ]]; then
    echo "Error: do not run this script as root or via sudo." >&2
    echo "The traced process must run as an unprivileged user." >&2
    echo "Sudo will be used internally for bpftrace only." >&2
    exit 1
fi

# --- Parse options with getopt ---
OPTS=$(getopt -o 'c:p:o:f:EFNSh' -l 'config:,pid:,output:,filter:,no-filter,disable-execs,disable-files,disable-netcalls,disable-suspicious,help' -n "$0" -- "$@") || usage
eval set -- "$OPTS"

while true; do
    case "$1" in
        -c|--config)             source "$2";          shift 2 ;;
        -p|--pid)                ATTACH_PID="$2";     shift 2 ;;
        -o|--output)             LOG_FILE="$2";       shift 2 ;;
        -f|--filter)             FILE_FILTER="$2";    shift 2 ;;
        --no-filter)             FILE_FILTER="";      shift ;;
        -E|--disable-execs)      TRACE_EXECS=0;       shift ;;
        -F|--disable-files)      TRACE_FILES=0;       shift ;;
        -N|--disable-netcalls)   TRACE_NETCALLS=0;    shift ;;
        -S|--disable-suspicious) TRACE_SUSPICIOUS=0;  shift ;;
        -h|--help)               usage ;;
        --)                      shift; break ;;
    esac
done

# --- Validate mode ---
if [[ -n "$ATTACH_PID" && $# -gt 0 ]]; then
    echo "Error: -p/--pid and a command are mutually exclusive" >&2
    usage
fi

if [[ -z "$ATTACH_PID" && $# -eq 0 ]]; then
    echo "Error: specify a command or use -p/--pid to attach" >&2
    usage
fi

# --- Output setup ---
# In attach mode, default to stdout (no interleaving risk since we
# didn't launch the process). In run mode, default to a temp file.
LOG_TO_STDOUT=0
if [[ -z "$LOG_FILE" ]]; then
    if [[ -n "$ATTACH_PID" ]]; then
        LOG_TO_STDOUT=1
    else
        LOG_FILE=$(mktemp "/tmp/trace-process.XXXXXX.log")
    fi
fi
if [[ "$LOG_TO_STDOUT" -eq 0 ]]; then
    : > "$LOG_FILE"
fi

# --- Acquire sudo credentials upfront ---
# Prompt once for the password before starting the process, so the
# process's stdout/stdin are not interleaved with a sudo prompt.
echo "[trace-process] bpftrace requires root — requesting sudo credentials..."
sudo -v

# --- Child PID tracking ---
BPFTRACE_PIDS=()
TARGET_PID=""
TARGET_OWNED=0
CLEANING_UP=0

# --- Cleanup ---
cleanup() {
    # Guard against re-entrant cleanup (e.g. EXIT firing after INT)
    [[ "$CLEANING_UP" -eq 1 ]] && return
    CLEANING_UP=1

    echo ""
    echo "[trace-process] Cleaning up..."

    # Tracked PIDs may be root-owned (bpftrace/sudo) or user-owned
    # (grep, when filtering is active). Try both; one will succeed.
    for child_pid in "${BPFTRACE_PIDS[@]}"; do
        kill "$child_pid" 2>/dev/null || sudo kill "$child_pid" 2>/dev/null || true
    done

    # We never kill the target — we only trace, we don't own its lifecycle.
    if [[ -n "$TARGET_PID" ]] && kill -0 "$TARGET_PID" 2>/dev/null; then
        echo "[trace-process] Process (PID $TARGET_PID) is still running."
    fi

    wait 2>/dev/null || true
    if [[ "$LOG_TO_STDOUT" -eq 0 ]]; then
        echo "[trace-process] Traces saved to: $LOG_FILE"
    fi
    echo "[trace-process] Done."
}

trap cleanup EXIT
trap 'trap - EXIT; cleanup; exit 130' INT
trap 'trap - EXIT; cleanup; exit 143' TERM
trap 'trap - EXIT; cleanup; exit 131' QUIT
trap 'trap - EXIT; cleanup; exit 134' HUP

# --- Resolve target PID ---
if [[ -n "$ATTACH_PID" ]]; then
    # Attach mode: verify the target PID is alive
    TARGET_PID="$ATTACH_PID"
    if ! kill -0 "$TARGET_PID" 2>/dev/null; then
        echo "[trace-process] Process $TARGET_PID is not running." >&2
        exit 1
    fi
    echo "[trace-process] Attaching to PID: $TARGET_PID"
else
    # Run mode: launch the command (unprivileged)
    TARGET_OWNED=1
    echo "[trace-process] Starting: $*"
    "$@" &
    TARGET_PID=$!
    echo "[trace-process] PID: $TARGET_PID"

    # Give the process a moment to start (bpftrace needs a live PID)
    sleep 0.2
    if ! kill -0 "$TARGET_PID" 2>/dev/null; then
        echo "[trace-process] Process exited immediately." >&2
        exit 1
    fi
fi

# --- Attach bpftrace scripts (elevated) ---
# Each bpftrace is wrapped with stdbuf -oL to force line-buffered
# output. This ensures lines are flushed to the log file promptly and
# that concurrent writers don't interleave partial lines (each line
# write is a single write() call, well under the PIPE_BUF atomic
# guarantee of 4096 bytes on Linux).
#
# When outputting to stdout, we open fd 3 as a copy of stdout so that
# backgrounded processes can write to it reliably.
if [[ "$LOG_TO_STDOUT" -eq 1 ]]; then
    exec 3>&1
    OUT_REDIR="/dev/fd/3"
else
    OUT_REDIR="$LOG_FILE"
fi

if [[ "$TRACE_EXECS" -eq 1 ]]; then
    echo "[trace-process] Attaching exec tracer..."
    sudo stdbuf -oL bpftrace "$SCRIPT_DIR/trace-execs.bt" "$TARGET_PID" >> "$OUT_REDIR" 2>&1 &
    BPFTRACE_PIDS+=($!)
fi

if [[ "$TRACE_FILES" -eq 1 ]]; then
    echo "[trace-process] Attaching file tracer..."
    if [[ -n "$FILE_FILTER" ]]; then
        sudo stdbuf -oL bpftrace "$SCRIPT_DIR/trace-files.bt" "$TARGET_PID" 2>&1 \
            | stdbuf -oL grep --line-buffered -vE "$FILE_FILTER" >> "$OUT_REDIR" &
    else
        sudo stdbuf -oL bpftrace "$SCRIPT_DIR/trace-files.bt" "$TARGET_PID" >> "$OUT_REDIR" 2>&1 &
    fi
    BPFTRACE_PIDS+=($!)
fi

if [[ "$TRACE_NETCALLS" -eq 1 ]]; then
    echo "[trace-process] Attaching network tracer..."
    sudo stdbuf -oL bpftrace "$SCRIPT_DIR/trace-netcalls.bt" "$TARGET_PID" >> "$OUT_REDIR" 2>&1 &
    BPFTRACE_PIDS+=($!)
fi

if [[ "$TRACE_SUSPICIOUS" -eq 1 ]]; then
    echo "[trace-process] Attaching suspicious ops tracer..."
    sudo stdbuf -oL bpftrace "$SCRIPT_DIR/trace-suspicious.bt" "$TARGET_PID" >> "$OUT_REDIR" 2>&1 &
    BPFTRACE_PIDS+=($!)
fi

if [[ ${#BPFTRACE_PIDS[@]} -eq 0 ]]; then
    echo "[trace-process] All tracers disabled, nothing to do." >&2
    exit 1
fi

echo "[trace-process] ${#BPFTRACE_PIDS[@]} tracer(s) attached."
if [[ "$LOG_TO_STDOUT" -eq 0 ]]; then
    echo "[trace-process] Traces: $LOG_FILE"
    echo "[trace-process] Follow live with: tail -f $LOG_FILE"
fi
echo ""

# --- Wait for the process to exit, then tear down ---
if [[ "$TARGET_OWNED" -eq 1 ]]; then
    # We spawned the process — wait(2) works on our own children
    wait "$TARGET_PID" 2>/dev/null || true
else
    # Attach mode — poll since we can't wait on a foreign process
    while kill -0 "$TARGET_PID" 2>/dev/null; do
        sleep 1
    done
fi
echo ""
echo "[trace-process] Process (PID $TARGET_PID) exited."
