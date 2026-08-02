#!/usr/bin/env sh
# run_linkcheck.sh - lychee link check for STE-Code markdown.
#
# Scans `ste-code/final/**/*.md` and `ste-code/artifacts/**/*.md` for broken
# links using .agents/tools/linkcheck/lychee.toml. Writes one markdown report
# per target into .agents/tools/linkcheck/reports/ and prints a summary.
#
# Usage:
#   .agents/tools/linkcheck/run_linkcheck.sh              # all targets
#   .agents/tools/linkcheck/run_linkcheck.sh final        # stable rules only
#   .agents/tools/linkcheck/run_linkcheck.sh artifacts    # generated output
#   .agents/tools/linkcheck/run_linkcheck.sh --offline    # local links only
#   .agents/tools/linkcheck/run_linkcheck.sh --no-cache final
#
# Exit codes: 0 = no broken links, 1 = lychee missing / bad usage,
#             2 = broken links found.
#
# Structure adapted from REPxREP/Repository/Maintain/Check/Links.sh.

set -e

Current=$(cd -- "$(dirname -- "$0")" >/dev/null 2>&1 && pwd)
Root=$(cd -- "$Current/../../.." >/dev/null 2>&1 && pwd)
Config="$Current/lychee.toml"
Reports="$Current/reports"

Targets=""
Extra=""

for Argument in "$@"; do
	case "$Argument" in
	final) Targets="$Targets final" ;;
	artifacts) Targets="$Targets artifacts" ;;
	all) Targets="final artifacts" ;;
	--offline) Extra="$Extra --offline" ;;
	--no-cache) Extra="$Extra --cache=false" ;;
	--suggest) Extra="$Extra --suggest" ;;
	-h | --help)
		sed -n '2,25p' "$0"
		exit 0
		;;
	*)
		echo "Error: unknown argument '$Argument'" >&2
		echo "Valid: final | artifacts | all | --offline | --no-cache | --suggest" >&2
		exit 1
		;;
	esac
done

[ -z "$Targets" ] && Targets="final artifacts"

if ! command -v lychee >/dev/null 2>&1; then
	echo "Error: lychee is not installed." >&2
	echo "  macOS:  brew install lychee" >&2
	echo "  Linux:  cargo install lychee" >&2
	echo "  https://github.com/lycheeverse/lychee" >&2
	exit 1
fi

cd "$Root"
mkdir -p "$Reports"

Stamp=$(date +%Y%m%d-%H%M%S)
Status=0

echo ""
echo "STE-Code Link Check"
echo ""
echo "Tooling: $(lychee --version)"
echo "Config:  ${Config#"$Root"/}"
echo "Root:    $Root"
echo "Targets: $Targets"
echo ""
echo ""

for Target in $Targets; do
	Directory="ste-code/$Target"

	if [ ! -d "$Directory" ]; then
		echo "SKIP  $Directory (directory not found)"
		echo ""
		continue
	fi

	Count=$(find "$Directory" -name '*.md' -type f | wc -l | tr -d ' ')
	Report="$Reports/$Target-$Stamp.md"
	Latest="$Reports/$Target-latest.md"

	echo "----------------------------------------"
	echo "Target: $Directory ($Count markdown files)"
	echo "----------------------------------------"

	# Single-quoted glob: lychee expands it, not the shell, so exclude_path
	# from lychee.toml is applied consistently.
	# shellcheck disable=SC2086
	if lychee --config "$Config" $Extra \
		--format markdown \
		--output "$Report" \
		"$Directory/**/*.md"; then
		echo "OK    no broken links in $Directory"
	else
		Code=$?
		if [ "$Code" -eq 2 ]; then
			Status=2
			echo "FAIL  broken links found in $Directory"
		else
			Status=1
			echo "ERROR lychee exited with code $Code for $Directory"
		fi
	fi

	if [ -f "$Report" ]; then
		cp "$Report" "$Latest"
		echo ""
		echo "Report: ${Report#"$Root"/}"
		echo ""
		sed -n '1,60p' "$Report"
	fi
	echo ""
done

echo ""
if [ "$Status" -eq 0 ]; then
	echo "Link check complete. No broken links."
else
	echo "Link check complete. Broken links found (exit $Status)."
	echo "Full reports: ${Reports#"$Root"/}/"
fi
echo ""

exit "$Status"
