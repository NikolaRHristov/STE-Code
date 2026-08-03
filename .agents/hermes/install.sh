#!/usr/bin/env bash
# install.sh — wire every STE-Code Hermes profile to the repository's single
# sources in one step. Runs the two linkers (skills, then memory); each handles
# its own idempotency and status reporting.
#
# Usage:
#   install.sh            # link skills + memory for all three profiles
#   install.sh --status   # report drift for both, change nothing
#   install.sh --dry-run  # show what would change
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DRY=""
STATUS=""
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY="--dry-run" ;;
        --status)  STATUS="--status" ;;
        --help|-h) sed -n '2,10p' "$0"; exit 0 ;;
        *) echo "unknown option: $arg" >&2; exit 2 ;;
    esac
done

if [ -n "$STATUS" ]; then
    bash "$SCRIPT_DIR/link-skills.sh"  --status
    bash "$SCRIPT_DIR/link-memory.sh"  --status
    exit 0
fi

bash "$SCRIPT_DIR/link-skills.sh"  --all $DRY
bash "$SCRIPT_DIR/link-memory.sh"  --all $DRY
