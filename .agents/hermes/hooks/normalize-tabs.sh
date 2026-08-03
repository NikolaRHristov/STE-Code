#!/bin/bash
# normalize-tabs.sh — Post-tool-call hook for Hermes Agent
# Replaces literal \t (backslash + t) with actual tab characters (0x09)
# after write_file or patch tool calls. Prevents the patch tool from
# corrupting file indentation.
#
# The patch tool occasionally writes literal \t sequences instead of
# real tab characters when processing JSON-escaped tab content. This
# hook catches and fixes those after the fact.
#
# Uses the same stdin JSON protocol as normalize-dashes.sh:
#   Hermes: .tool_input.path
#   Claude: .tool_input.file_path (different field name)

INPUT=$(cat)
FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.path // empty')

# Skip if no path provided
[ -z "$FILE_PATH" ] && exit 0

# Skip if file doesn't exist (e.g., the tool didn't actually write)
[ -f "$FILE_PATH" ] || exit 0

# Skip binary files
file --brief --mime-encoding "$FILE_PATH" 2>/dev/null | grep -q 'binary' && exit 0

# Replace literal \t at line-start positions with real tab characters.
# The patch tool writes \t as literal backslash-t for indentation;
# this restores them to real tabs.
#
# We anchor to start-of-line or after existing real tabs so we don't
# accidentally replace \t inside string literals or comments.
perl -i -pe '
  # Replace \t only when it appears as part of indentation:
  # at the start of a line, or preceded only by real tabs
  while (/^(?:\t|\\t)*\K\\t/) {
    my $pos = pos;
    substr($_, $-[0], 2) = "\t";
    pos = $pos - 1;
  }
' "$FILE_PATH" 2>/dev/null

exit 0
