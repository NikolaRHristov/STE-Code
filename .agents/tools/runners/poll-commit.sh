#!/usr/bin/env bash
# Periodic poll-commit worker for the RED/BLUE/PURPLE/WHITE benchmark build-out.
#
# Scope discipline (multi-session safety): this worker ONLY stages paths that
# THIS session owns. It never touches ste-code/refined/, ste-code/grouped/, or
# any other stage directory that a concurrent Hermes session may own.
#
# Usage:  bash .agents/tools/runners/poll-commit.sh [interval_seconds] [max_iterations]
set -uo pipefail

# Never hardcode a machine path: walk up to a repository marker so a clone
# works anywhere. Mirrors .agents/tools/lib/repo_root.py and jail-lib.sh.
find_root() {
	local d
	d="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
	while [ "$d" != "/" ]; do
		if [ -d "$d/.git" ] || [ -f "$d/Makefile" ]; then
			printf '%s\n' "$d"
			return 0
		fi
		d="$(dirname "$d")"
	done
	return 1
}

ROOT="$(find_root)" || {
	echo "cannot locate repository root" >&2
	exit 1
}
INTERVAL="${1:-300}"
MAX_ITER="${2:-288}" # 288 * 300s = 24h
LOG="$ROOT/.agents/tmp/poll-commit.log"

# Paths this session owns. Everything else is left alone.
OWNED=(
	".agents/benchmark"
	".agents/tools/runners/poll-commit.sh"
	".agents/skills/benchmarking"
)

mkdir -p "$(dirname "$LOG")"
cd "$ROOT" || exit 1

log() { printf '[%s] %s\n' "$(date -u +%H:%M:%SZ)" "$*" >>"$LOG"; }

log "poll-commit start interval=${INTERVAL}s max_iter=${MAX_ITER} branch=$(git rev-parse --abbrev-ref HEAD)"

i=0
while [ "$i" -lt "$MAX_ITER" ]; do
	i=$((i + 1))

	# 1. Sync with origin first so we never build on a stale base.
	git fetch --quiet origin 2>>"$LOG"
	BRANCH="$(git rev-parse --abbrev-ref HEAD)"
	BEHIND="$(git rev-list --count "HEAD..origin/$BRANCH" 2>/dev/null || echo 0)"

	# 2. Stage only owned paths (ignored output is filtered by .gitignore).
	STAGED=0
	for p in "${OWNED[@]}"; do
		[ -e "$p" ] || continue
		git add -- "$p" 2>>"$LOG"
	done
	if ! git diff --cached --quiet; then
		STAGED=1
	fi

	# 3. Rebase onto origin when behind and nothing conflicting is in flight.
	if [ "$BEHIND" -gt 0 ]; then
		if [ "$STAGED" -eq 1 ]; then
			git stash push --quiet --staged -m "poll-commit-autostash" 2>>"$LOG" &&
				STASHED=1 || STASHED=0
		else
			STASHED=0
		fi
		if git pull --rebase --quiet origin "$BRANCH" 2>>"$LOG"; then
			log "pulled $BEHIND commit(s) from origin/$BRANCH"
		else
			git rebase --abort 2>/dev/null
			log "WARN pull --rebase failed; left local state untouched"
		fi
		if [ "${STASHED:-0}" -eq 1 ]; then
			git stash pop --quiet 2>>"$LOG" || log "WARN stash pop conflict"
			for p in "${OWNED[@]}"; do [ -e "$p" ] && git add -- "$p" 2>>"$LOG"; done
		fi
	fi

	# 4. Commit whatever is staged.
	if ! git diff --cached --quiet; then
		FILES="$(git diff --cached --name-only | wc -l | tr -d ' ')"
		SUMMARY="$(git diff --cached --name-only | sed 's|.*/||' | head -4 | paste -sd, -)"
		if git commit --quiet -m "chore(benchmark): poll-commit ${FILES} file(s) — ${SUMMARY}" 2>>"$LOG"; then
			log "committed $FILES file(s): $SUMMARY"
			if git push --quiet origin "$BRANCH" 2>>"$LOG"; then
				log "pushed to origin/$BRANCH"
			else
				log "WARN push failed (will retry next tick)"
			fi
		else
			log "WARN commit failed"
		fi
	else
		log "no owned changes (iter $i)"
	fi

	sleep "$INTERVAL"
done

log "poll-commit finished after $MAX_ITER iterations"
