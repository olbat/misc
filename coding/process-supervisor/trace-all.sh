#!/usr/bin/env bash
#
# trace-all.sh
#
# Concatenates common.bt with all trace-*.bt modules and runs
# them as a single bpftrace process against the target PID.
#
# Usage: sudo ./trace-all.sh <PID>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [[ ${1:-} == "" || ${1:-} == "0" ]]; then
    echo "Usage: sudo $0 <PID>" >&2
    exit 1
fi

PID="$1"

# Build combined script: common preamble + all tracer modules + cleanup
COMBINED=$(mktemp "/tmp/trace-all.XXXXXX.bt")
trap 'rm -f "$COMBINED"' EXIT INT TERM QUIT HUP

cat "$SCRIPT_DIR/common.bt" > "$COMBINED"

for module in "$SCRIPT_DIR"/trace-{execs,files,netcalls,suspicious}.bt; do
    cat "$module" >> "$COMBINED"
done

# Shared cleanup: process-exit shrinking and root-exit handler
# Must come last so module-specific END handlers fire before @watched is cleared.
cat "$SCRIPT_DIR/cleanup.bt" >> "$COMBINED"

bpftrace -B line "$COMBINED" "$PID"
