#!/bin/bash
# pre-tool-call-block-sed.sh — Hard guard against in-place file editing
# via sed/awk/perl/python on the TERMINAL tool.
#
# Wiring (config.yaml):
#   hooks.pre_tool_call:
#     - command: ~/.hermes/agent-hooks/pre-tool-call-block-sed.sh
#       matcher: terminal
#       timeout: 5
#
# Stdin : JSON { tool_name: "terminal", tool_input: { command: "..." } }
# Stdout: { "action": "block", "message": "..." } to abort the call,
#         or {} (empty JSON / no action) to allow it.
#
# Rationale: sed/awk/perl -i / python -c file rewrites are the #1 source
# of silent corruption (over-consumed regions, mangled boundaries, lost
# footers). The model MUST use read_file + write_file / patch instead.
# These tool calls are cheap, precise, and recoverable.

INPUT=$(cat)

# Only act on terminal tool calls.
[ "$(printf '%s' "$INPUT" | jq -r '.tool_name // empty')" = "terminal" ] || exit 0

CMD=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')

# If we cannot read the command, fail closed (block) to be safe.
[ -z "$CMD" ] && {
  printf '%s' '{"action":"block","message":"Could not read terminal command; blocked by sed/awk guard."}'
  exit 0
}

# Normalise for matching: strip common quoting/escapes is unnecessary because
# we match on token boundaries.
BLOCKED=0
REASON=""

# 1. sed, with any of: -i (in-place), s/... (substitution), or a file arg rewrite.
if printf '%s' "$CMD" | grep -Eq '(^|[^[:alnum:]_./-])sed([[:space:]]|$)'; then
  if printf '%s' "$CMD" | grep -Eq '\bs/|sed[[:space:]]+-[a-zA-Z]*i|sed[[:space:]]+.*[<>]|sed .*-i'; then
    BLOCKED=1
    REASON="sed is forbidden for file editing (rule #1/#5). Use patch or write_file instead."
  fi
fi

# 2. awk editing a file (awk can rewrite files via > or by being an editor).
if [ "$BLOCKED" -eq 0 ] && printf '%s' "$CMD" | grep -Eq '(^|[^[:alnum:]_./-])awk([[:space:]]|$)'; then
  BLOCKED=1
  REASON="awk is forbidden for file editing (rule #5). Use patch or write_file instead."
fi

# 3. perl in-place (-i) or perl -e/-0777 that rewrites files.
if [ "$BLOCKED" -eq 0 ] && printf '%s' "$CMD" | grep -Eq '(^|[^[:alnum:]_./-])perl([[:space:]]|$)'; then
  if printf '%s' "$CMD" | grep -Eq '\B-i\b|-i[[:space:]]|perl[[:space:]]+-[a-zA-Z]*i|-0777'; then
    BLOCKED=1
    REASON="perl -i / -0777 file rewriting is forbidden (rule #5). Use patch or write_file instead."
  fi
fi

# 4. python/pypy one-liner that writes or rewrites a file.
if [ "$BLOCKED" -eq 0 ] && printf '%s' "$CMD" | grep -Eq '(^|[^[:alnum:]_./-])(python3?|pypy3?)([[:space:]]|$)'; then
  if printf '%s' "$CMD" | grep -Eq '\-c\b|--command|\.write\(|open\([^)]*[,][[:space:]]*[\"'\''w]'; then
    BLOCKED=1
    REASON="Python one-liners that write files are forbidden (rule #5). Put the script in ~/Developer/Maintain/ or use patch/write_file."
  fi
fi

if [ "$BLOCKED" -eq 1 ]; then
  printf '%s' "{\"action\":\"block\",\"message\":\"$REASON\"}"
  exit 0
fi

# Allow the command.
printf '%s' '{}'
exit 0
