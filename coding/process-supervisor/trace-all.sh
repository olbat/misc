#!/usr/bin/env bash
#
# trace-all.sh
#
# Runs all trace-*.bt bpftrace scripts in the same directory in parallel
# against the same target PID. Ctrl-C stops all.
#
# Usage: sudo ./trace-all.sh <PID>

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
trap cleanup EXIT INT TERM QUIT HUP

for script in "$SCRIPT_DIR"/trace-*.bt; do
    bpftrace "$script" "$PID" &
done

wait
