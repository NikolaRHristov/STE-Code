#!/bin/bash
# pre_tool_call test hook for write_file/patch - logs the target path and
# passes the payload through unchanged.
# Contract (same as sibling pre-tool-call-* hooks):
#   - reads the JSON payload from stdin
#   - MUST print the (possibly modified) payload to stdout
#   - may emit {"action":"modify","args":{...}} to alter tool arguments
# This hook is an observer: it records what file is about to be written and
# lets the call proceed unmodified. Safe for production use.
#
# For testing PR #28953: pre_tool_call modify action.

INPUT=$(cat)
LOG_DIR="$HOME/.hermes/agent-hooks/logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)
printf '\n--- TEST-PRE-MODIFY %s ---\n%s\n' "$TIMESTAMP" "$INPUT" >> "$LOG_DIR/pre_tool_call_test_pre_modify.log"

TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty')

# Only act on file-writing tools (matcher in config.yaml already restricts to
# write_file|patch, but guard anyway).
case "$TOOL_NAME" in
  write_file|patch)
    FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.path // empty')
    if [ -n "$FILE_PATH" ]; then
      printf '[%s] test-pre-modify: about to write %s\n' "$TIMESTAMP" "$FILE_PATH" \
        >> "$LOG_DIR/pre_tool_call_test_pre_modify.log"
    fi
    ;;
  *)
    : # no-op for other tools
    ;;
esac

# Pass the payload through unchanged (observer only).
printf '%s\n' "$INPUT"

exit 0
