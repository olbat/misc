#!/usr/bin/env bash
#
# spy-agent.sh
#
# Runs the four individual bpftrace scripts (execs, files, netcalls,
# suspicious) in parallel against the same target PID. Ctrl-C stops all.
#
# Usage: sudo ./spy-agent.sh <PID>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [[ ${1:-} == "" || ${1:-} == "0" ]]; then
    echo "Usage: sudo $0 <PID>" >&2
    exit 1
fi

PID="$1"

# Kill all child bpftrace processes on exit
cleanup() {
    kill 0 2>/dev/null
    wait 2>/dev/null
}
trap cleanup EXIT

bpftrace "$SCRIPT_DIR/trace-execs.bt" "$PID" &
bpftrace "$SCRIPT_DIR/trace-files.bt" "$PID" &
bpftrace "$SCRIPT_DIR/trace-netcalls.bt" "$PID" &
bpftrace "$SCRIPT_DIR/trace-suspicious.bt" "$PID" &

wait
