#!/bin/bash
# pre_tool_call diagnostic hook - logs payload, passes through unchanged
# For testing PR #28953: pre_tool_call modify action

LOG_DIR="$HOME/.hermes/agent-hooks/logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)
LOG_FILE="$LOG_DIR/pre_tool_call_${TIMESTAMP}.json"

INPUT=$(cat)

# Save raw input for inspection
printf '%s\n' "$INPUT" >"$LOG_FILE"

# Append to running log
printf '\n--- %s ---\n%s\n' "$TIMESTAMP" "$INPUT" >>"$LOG_DIR/pre_tool_call_all.log"

# Pass through unchanged
printf '%s\n' "$INPUT"

exit 0
