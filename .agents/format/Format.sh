#!/usr/bin/env bash

#===============================================================================
# Format.sh - Format Markdown, JSON, YAML, and shell sources for STE-Code.
#===============================================================================
#
# Usage:
#   .agents/format/Format.sh              # dry run (default: changes nothing)
#   .agents/format/Format.sh dryrun       # report what every stage would do
#   .agents/format/Format.sh check        # prettier --check; non-zero on drift
#   .agents/format/Format.sh audit        # visual-standard findings only
#   .agents/format/Format.sh dos2unix     # normalize line endings only
#   .agents/format/Format.sh shell        # format shell scripts only
#   .agents/format/Format.sh tables       # Markdown.py structural pass only
#   .agents/format/Format.sh markdown     # tables + prettier (the write path)
#   .agents/format/Format.sh prettier     # prettier --write only
#   .agents/format/Format.sh all          # dos2unix, shell, tables, prettier
#
# Ported from <repo>/Land/Maintain/Format.sh. Two deliberate
# divergences from upstream:
#
#   1. DEFAULT IS A DRY RUN. Upstream's no-arg invocation writes every file.
#      This repository ships generated artifacts and is edited by concurrent
#      sessions, so the write path must be asked for by name.
#   2. NO STAGE MAY ESCAPE .agents/format's scope. Every stage formats exactly
#      two trees - ste-code/ and .agents/ - and every stage honours the same
#      exclusions. The repository root deliberately holds no package.json and
#      no prettier config; nothing here creates one.
#
# Stages with no target files in this repository are omitted rather than
# stubbed: there is no Rust (no .rs), no TypeScript (no .ts/.tsx), and no
# mermaid content. Add them back from upstream if that changes.
#
# Configuration:
#   prettier.config.js  - Prettier options (printWidth 80, tabs, proseWrap)
#   .prettierignore     - Canonical exclusions; the other two files mirror it
#   .editorconfig       - Shared indent/newline rules (shfmt reads this)
#   Markdown.py         - STE-Code visual-standard normalizer (runs first)
#
#===============================================================================

set -eu

Current=$(cd -- "$(dirname -- "$0")" >/dev/null 2>&1 && pwd)

# `.git` is the AUTHORITATIVE root marker, matching jail_find_root in
# .agents/hermes/jail/scripts/jail-lib.sh and _find_root in
# .agents/benchmark/harness_config.py. package.json is NOT a marker: the
# tooling monorepo lives at .agents/package.json and would resolve one level
# too deep.
Root=$Current
while [ "$Root" != "/" ] && [ ! -d "$Root/.git" ]; do
	Root=$(dirname "$Root")
done
if [ ! -d "$Root/.git" ]; then
	echo "Error: cannot locate repository root (no .git above $Current)." >&2
	exit 1
fi

Agents="$Root/.agents"
Standard="$Root/ste-code"
Config="$Current/prettier.config.js"
Ignore="$Current/.prettierignore"

# pnpm may hoist the binary to the workspace root (.agents/node_modules) or
# keep it in this package (.agents/format/node_modules). Accept either.
if [ -x "$Current/node_modules/.bin/prettier" ]; then
	Prettier="$Current/node_modules/.bin/prettier"
else
	Prettier="$Agents/node_modules/.bin/prettier"
fi

Banner() {
	echo "========================================"
	echo "$1"
	echo "========================================"
	shift
	for Line in "$@"; do echo "$Line"; done
	echo "========================================"
	echo ""
}

# Shared exclusion set for the find-driven stages. Mirrors .prettierignore
# and the `ExcludePrefix` tuple in Markdown.py. Prefixes are anchored to the
# two scope roots, so `.agents/tools/artifacts/` is still formatted while
# `ste-code/artifacts/` is not.
FindExcluded() {
	find "$@" \
		-not -path "*/.git/*" \
		-not -path "*/node_modules/*" \
		-not -path "*/__pycache__/*" \
		-not -path "*/.pytest_cache/*" \
		-not -path "*/.venv/*" \
		-not -path "$Agents/hermes/*" \
		-not -path "$Agents/tmp/*" \
		-not -path "$Agents/skills/*" \
		-not -path "$Agents/_scratch/*" \
		-not -path "$Agents/archive/*" \
		-not -path "$Agents/audit/*" \
		-not -path "$Agents/telemetry/*" \
		-not -path "$Agents/vendor/*" \
		-not -path "$Agents/benchmark/tests/*" \
		-not -path "$Agents/benchmark/report/*" \
		-not -path "$Agents/benchmark/sample-session/*" \
		-not -path "$Agents/benchmark/test-cases-adhoc/*" \
		-not -path "$Agents/tools/linkcheck/reports/*" \
		-not -path "$Standard/artifacts/*" \
		-not -path "$Standard/audit/*"
}

RequirePrettier() {
	if [ ! -x "$Prettier" ]; then
		echo "Error: prettier not found at $Prettier"
		echo "  Run: cd $Agents && pnpm install"
		exit 1
	fi
}

#===============================================================================
# Format Functions
#===============================================================================

FormatLineEndings() {
	Banner "Format Line Endings" "Tooling: dos2unix" "Scope:   ste-code/ + .agents/"

	if ! command -v dos2unix >/dev/null 2>&1; then
		echo "dos2unix is not installed - skipping this stage."
		echo "  macOS:  brew install dos2unix"
		echo "  Linux:  apt install dos2unix  /  dnf install dos2unix"
		echo ""
		echo "Prettier's endOfLine: \"lf\" already normalizes every file it"
		echo "formats, so this stage only covers file types prettier skips."
		echo ""
		return 0
	fi

	# dos2unix skips binary files automatically.
	FindExcluded "$Standard" "$Agents" -type f \
		-not -name "*.pyc" \
		-not -name ".DS_Store" \
		-print0 | xargs -0 dos2unix -q

	echo ""
	echo "Line ending conversion complete."
	echo ""
}

FormatShell() {
	Banner "Format Shell" "Tooling: shfmt" "Config:  .editorconfig (tabs, indent=4)"

	if ! command -v shfmt >/dev/null 2>&1; then
		echo "shfmt is not installed - skipping this stage."
		echo "  macOS:  brew install shfmt"
		echo "  Linux:  apt install shfmt  /  go install mvdan.cc/sh/v3/cmd/shfmt@latest"
		echo "  https://github.com/mvdan/sh"
		echo ""
		return 0
	fi

	# shfmt reads .editorconfig for indent style/size automatically. The
	# hermes/ scripts are excluded by FindExcluded: they belong to the jail
	# session and are verified byte-for-byte there.
	FindExcluded "$Standard" "$Agents" -name "*.sh" -print0 |
		xargs -0 shfmt -w

	echo ""
	echo "Shell formatting complete."
	echo ""
}

FormatTables() {
	Banner "Format Markdown Structure" \
		"Tooling: Markdown.py (STE-Code visual standard)" \
		"Rules:   blank line between sections, heading hierarchy," \
		"         isolated tables and fenced blocks, LF, no trailing space" \
		"Safety:  refuses any rewrite that changes non-whitespace content"

	python3 "$Current/Markdown.py" --All

	echo ""
	echo "Markdown structure pass complete."
	echo ""
}

FormatPrettier() {
	Banner "Format Prettier" \
		"Tooling: Markdown.py (structure, first)" \
		"         Prettier   (prose width + tables, second)" \
		"Config:  prettier.config.js" \
		"Ignore:  .prettierignore"

	RequirePrettier

	# Pass 1: structural normalizer, mirroring how upstream runs
	# TypeScript.py / Rust.py before prettier and rustfmt.
	python3 "$Current/Markdown.py" --All

	# Pass 2: prettier reflows prose to printWidth and aligns markdown
	# tables. || true keeps one unparsable file from aborting the sweep.
	"$Prettier" --config "$Config" --ignore-path "$Ignore" \
		--write "$Standard" "$Agents" || true

	echo ""
	echo "Prettier formatting complete."
	echo ""
}

CheckPrettier() {
	Banner "Check Prettier" "Tooling: prettier --check" "Ignore:  .prettierignore"

	RequirePrettier

	"$Prettier" --config "$Config" --ignore-path "$Ignore" \
		--check "$Standard" "$Agents"
}

AuditMarkdown() {
	Banner "Audit Markdown" \
		"Tooling: Markdown.py --Audit" \
		"Reports: heading hierarchy, table shape, bullet consistency" \
		"Writes:  nothing"

	python3 "$Current/Markdown.py" --Audit --All
}

DryRun() {
	Banner "Dry Run" \
		"Nothing is written. Run 'markdown' or 'all' to apply." \
		"Scope:   $Standard" \
		"         $Agents"

	python3 "$Current/Markdown.py" --DryRun --All || true

	echo ""
	if [ -x "$Prettier" ]; then
		"$Prettier" --config "$Config" --ignore-path "$Ignore" \
			--check "$Standard" "$Agents" || true
	else
		echo "Prettier not installed - skipping the prettier preview."
		echo "  Run: cd $Agents && pnpm install"
	fi

	echo ""
	echo "Dry run complete. No files were modified."
	echo ""
}

#===============================================================================
# Main Command Router
#===============================================================================

case "${1:-}" in
dos2unix)
	FormatLineEndings
	;;
shell)
	FormatShell
	;;
tables)
	FormatTables
	;;
prettier)
	RequirePrettier
	"$Prettier" --config "$Config" --ignore-path "$Ignore" \
		--write "$Standard" "$Agents" || true
	;;
markdown)
	FormatPrettier
	;;
check)
	CheckPrettier
	;;
audit)
	AuditMarkdown
	;;
all)
	FormatLineEndings
	FormatShell
	FormatPrettier
	;;
"" | dryrun)
	DryRun
	;;
--help | -h)
	echo "Usage: $0 [dryrun|check|audit|dos2unix|shell|tables|markdown|prettier|all]"
	echo ""
	echo "  dryrun    Report every pending change; write nothing (DEFAULT)"
	echo "  check     prettier --check; exits non-zero when files drift"
	echo "  audit     Report visual-standard findings from Markdown.py"
	echo "  dos2unix  Normalize line endings (CRLF -> LF) with dos2unix"
	echo "  shell     Format shell scripts with shfmt"
	echo "  tables    Markdown.py structural pass only"
	echo "  markdown  Markdown.py + prettier --write (the usual write path)"
	echo "  prettier  prettier --write only"
	echo "  all       dos2unix, shell, then markdown"
	echo ""
	echo "Scope is always ste-code/ and .agents/, minus .prettierignore."
	;;
*)
	echo "Unknown target: $1"
	echo "Use --help for usage information"
	exit 1
	;;
esac
