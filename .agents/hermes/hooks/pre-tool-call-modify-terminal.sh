#!/bin/bash
# pre_tool_call modification hook - prepends a visible echo banner
# to terminal commands by modifying the 'command' parameter.
# For testing PR #28953: pre_tool_call modify action

INPUT=$(cat)
LOG_DIR="$HOME/.hermes/agent-hooks/logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)
printf '\n--- MODIFY %s ---\n%s\n' "$TIMESTAMP" "$INPUT" >>"$LOG_DIR/pre_tool_call_modify.log"

TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty')

if [ "$TOOL_NAME" != "terminal" ]; then
	printf '{}'
	exit 0
fi

COMMAND=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
	printf '{}'
	exit 0
fi

# Prepend a visible echo banner so we can SEE the modification in output
MODIFIED_COMMAND="echo '[PRE_TOOL_CALL_HOOK] command modified @ $(date -u +%Y-%m-%dT%H:%M:%SZ)' && $COMMAND"

jq -nc --arg cmd "$MODIFIED_COMMAND" '{"action": "modify", "args": {"command": $cmd}}'

exit 0
