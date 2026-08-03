#!/usr/bin/env bash
# lock-group.sh — Advisory file lock for STE-Code grouping/adaptation workers.
#
# Prevents two agents from writing the same group/adapted file simultaneously.
# Usage:
#   ./lock-group.sh acquire <group-file> [agent-id]   # exits 0 if locked, 1 if busy
#   ./lock-group.sh release <group-file> [agent-id]   # removes lock
#   ./lock-group.sh check  <group-file>               # exits 0 if free, 1 if locked
#
# Lock files live in .agents/state/locks/ next to the target file's stem.

set -euo pipefail

LOCKDIR=".agents/state/locks"
mkdir -p "$LOCKDIR"

ACTION="${1:-}"
TARGET="${2:-}"
AGENT="${3:-$$}"

if [[ -z "$TARGET" ]]; then
	echo "Usage: lock-group.sh <acquire|release|check> <target-file> [agent-id]" >&2
	exit 2
fi

STEM=$(basename "$TARGET" .md)
LOCKFILE="$LOCKDIR/${STEM}.lock"

case "$ACTION" in
acquire)
	# Atomic mkdir-based lock (mkdir fails if exists)
	if mkdir "$LOCKFILE" 2>/dev/null; then
		echo "$AGENT $(date -u +%Y-%m-%dT%H:%M:%SZ)" >"$LOCKFILE/owner"
		echo "LOCKED: $TARGET by $AGENT"
		exit 0
	else
		OWNER=$(cat "$LOCKFILE/owner" 2>/dev/null || echo "unknown")
		echo "BUSY: $TARGET locked by $OWNER" >&2
		exit 1
	fi
	;;
release)
	if [[ -d "$LOCKFILE" ]]; then
		# Only release if we own it (or force)
		if grep -q "$AGENT" "$LOCKFILE/owner" 2>/dev/null || [[ "${4:-}" == "--force" ]]; then
			rm -rf "$LOCKFILE"
			echo "RELEASED: $TARGET"
			exit 0
		else
			echo "DENIED: $TARGET owned by $(cat "$LOCKFILE/owner" 2>/dev/null)" >&2
			exit 1
		fi
	else
		echo "FREE: $TARGET (no lock)"
		exit 0
	fi
	;;
check)
	if [[ -d "$LOCKFILE" ]]; then
		echo "LOCKED: $TARGET by $(cat "$LOCKFILE/owner" 2>/dev/null || echo unknown)"
		exit 1
	else
		echo "FREE: $TARGET"
		exit 0
	fi
	;;
*)
	echo "Unknown action: $ACTION" >&2
	exit 2
	;;
esac
