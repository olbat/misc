#!/usr/bin/env bash
#
# trace-all.sh
#
# Concatenates trace-common.bt with all trace-*.bt modules and runs
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

# Build combined script: common preamble + all tracer modules + postamble
COMBINED=$(mktemp "/tmp/trace-all.XXXXXX.bt")
trap 'rm -f "$COMBINED"' EXIT INT TERM QUIT HUP

cat "$SCRIPT_DIR/trace-common.bt" > "$COMBINED"

for module in "$SCRIPT_DIR"/trace-{execs,files,netcalls,suspicious}.bt; do
    cat "$module" >> "$COMBINED"
done

# Shared postamble: process-exit cleanup and root-exit handler
cat >> "$COMBINED" << 'POSTAMBLE'

// --- Shared process tracking (appended by trace-all.sh) ---

tracepoint:sched:sched_process_exit
/(@watched[(int64)pid]) && tid == pid/
{
    delete(@watched[(int64)pid]);
}

tracepoint:sched:sched_process_exit
/(tid == (uint64)@root_pid)/
{
    printf("\nRoot process %d exited. Stopping monitor.\n", @root_pid);
    exit();
}

END
{
    clear(@watched);
    delete(@root_pid);
}
POSTAMBLE

bpftrace -B line "$COMBINED" "$PID"
