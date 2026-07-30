#!/bin/bash
# Convenience wrapper: telemetry-worker.sh <worker-id> <prompt-file> [--output OUTPUT_FILE]
# Example: .agents/tools/telemetry-worker.sh b1-004 .agents/prompts/expansion-pass1/pass1-batch-004.txt --output ste-code/adapted/expanded/pass1-batch-004.json
PROJECT="$(cd "$(dirname "$0")/../.." && pwd)"
exec python3 "$PROJECT/.agents/tools/telemetry-worker.py" "$@"
