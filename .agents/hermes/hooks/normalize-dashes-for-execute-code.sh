#!/bin/bash
# normalize-dashes-for-execute-code.sh
#
# Companion to normalize-dashes.sh - handles execute_code tool calls.
#
# Hook payload (stdin JSON) for post_tool_call / execute_code:
#   tool_name       = "execute_code"  (matched by the regex)
#   tool_input.code = the Python source that just ran (may contain dashes)
#   tool_input.path = NOT PRESENT for execute_code
#   cwd             = working directory at execution time
#
# Strategy:
#   1. Find source files in cwd (handles files created via write_file() /
#      open() inside execute_code).
#   2. Skip binary files.
#   3. Run the same perl substitution as normalize-dashes.sh.
#
# Note: No grep -P pre-filter - macOS BSD grep has no -P (Perl-regex) flag;
# perl is a no-op on already-clean files so the savings would be zero.
#
INPUT=$(cat)
CWD=$(printf '%s' "$INPUT" | jq -r '.cwd // empty')

[ -z "$CWD" ] && exit 0

find "$CWD" \
	-maxdepth 1 \
	\( \
	-name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' \
	-o -name '*.json' -o -name '*.yaml' -o -name '*.yml' -o -name '*.toml' \
	-o -name '*.md' -o -name '*.mdx' -o -name '*.rs' -o -name '*.py' \
	-o -name '*.c' -o -name '*.h' -o -name '*.sh' -o -name '*.bash' -o -name '*.zsh' \
	-o -name '*.astro' -o -name '*.css' -o -name '*.scss' -o -name '*.less' \
	-o -name '*.html' -o -name '*.htm' -o -name '*.xml' -o -name '*.ini' \
	-o -name '*.cfg' -o -name '*.conf' -o -name '*.env' \
	\) \
	-type f |
	while IFS= read -r FILE; do
		[ -f "$FILE" ] || continue
		file --brief --mime-encoding "$FILE" 2>/dev/null | grep -q 'binary' && continue
		perl -i -CSD -pe \
			's/[\x{058A}\x{05BE}\x{1400}\x{1806}\x{2010}-\x{2015}\x{2E17}\x{2E1A}\x{2E3A}-\x{2E3B}\x{2E40}\x{2E5D}\x{301C}\x{3030}\x{30A0}\x{FE31}-\x{FE32}\x{FE58}\x{FE63}\x{FF0D}]/-/g' \
			"$FILE" 2>/dev/null
	done

exit 0
