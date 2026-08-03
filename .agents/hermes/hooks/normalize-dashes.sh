#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.path // empty')

[ -z "$FILE_PATH" ] && exit 0

[ -f "$FILE_PATH" ] || exit 0
file --brief --mime-encoding "$FILE_PATH" 2>/dev/null | grep -q 'binary' && exit 0

perl -i -CSD -pe \
	's/[\x{058A}\x{05BE}\x{1400}\x{1806}\x{2010}-\x{2015}\x{2E17}\x{2E1A}\x{2E3A}-\x{2E3B}\x{2E40}\x{2E5D}\x{301C}\x{3030}\x{30A0}\x{FE31}-\x{FE32}\x{FE58}\x{FE63}\x{FF0D}]/-/g' \
	"$FILE_PATH" 2>/dev/null

exit 0
