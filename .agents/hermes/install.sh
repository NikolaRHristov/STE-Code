#!/usr/bin/env bash
# install.sh — wire every STE-Code Hermes profile to the repository's single
# sources in one step. Runs the three linkers (skills, memory, hooks); each
# handles its own idempotency and status reporting.
#
# Usage:
#   install.sh            # link skills + memory + hooks for all three profiles
#   install.sh --status   # report drift for all three, change nothing
#   install.sh --dry-run  # show what would change
#   install.sh --force    # additionally repair a drifted real hooks dir
#                         # (link-hooks.sh prunes only entries it can positively
#                         #  classify; unrecognised files are kept and reported)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DRY=""
STATUS=""
FORCE=""
for arg in "$@"; do
	case "$arg" in
	--dry-run) DRY="--dry-run" ;;
	--status) STATUS="--status" ;;
	--force) FORCE="--force" ;;
	--help | -h)
		sed -n '2,13p' "$0"
		exit 0
		;;
	*)
		echo "unknown option: $arg" >&2
		exit 2
		;;
	esac
done

if [ -n "$STATUS" ]; then
	bash "$SCRIPT_DIR/link-skills.sh" --status
	bash "$SCRIPT_DIR/link-memory.sh" --status
	bash "$SCRIPT_DIR/link-hooks.sh" --status
	exit 0
fi

bash "$SCRIPT_DIR/link-skills.sh" --all $DRY
bash "$SCRIPT_DIR/link-memory.sh" --all $DRY
bash "$SCRIPT_DIR/link-hooks.sh" --all $DRY $FORCE
