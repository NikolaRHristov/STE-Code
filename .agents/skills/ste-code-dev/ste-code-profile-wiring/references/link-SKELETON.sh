#!/usr/bin/env bash
# link-<thing>.sh — make .agents/hermes/<thing>/ the single source of truth for
# every STE-Code Hermes profile, distributed via relative symlinks:
#
#   .agents/hermes/<thing>/                          (SOURCE OF TRUTH, tracked)
#        ^  .agents/hermes/profiles/<p>/<thing>         (level-1 pointer)
#               ^  ~/.hermes/profiles/<p>/<thing>        (level-2, live profile)
#
# Mirrors link-skills.sh / link-memory.sh / link-hooks.sh. Edit <thing> and
# SOURCE only; the link logic is shared. Empty real dirs at the target are
# replaced; non-empty real dirs are skipped (never clobber authored runtime).
#
# Usage:
#   link-<thing>.sh --all [--dry-run]
#   link-<thing>.sh <profile> [--dry-run]
#   link-<thing>.sh --status
#   link-<thing>.sh --help
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/.." && pwd)"         # .agents
SOURCE="$(cd "$REPO/hermes/<thing>" && pwd)" # .agents/hermes/<thing>
PROFILE_SRC="$REPO/hermes/profiles"
LIVE="$HOME/.hermes/profiles"

DRY_RUN=0
ALL=0
STATUS=0

log() { printf '%s\n' "$*"; }
run() { if [ "$DRY_RUN" = 1 ]; then log "  would: $*"; else "$@"; fi; }

resolve() {
	python3 -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' "$1" 2>/dev/null || echo "$1"
}
relpath() {
	python3 - "$1" "$2" <<'PY'
import os, sys
dest, src = sys.argv[1], sys.argv[2]
dest_dir = os.path.dirname(os.path.abspath(dest))
print(os.path.relpath(os.path.abspath(src), dest_dir))
PY
}

# Refuse to replace a non-empty real dir; replace empty real dirs; otherwise
# symlink. (Pitfall #4: never clobber authored runtime content.)
link_dir() {
	local dest="$1" src="$2" name rel
	name="$(basename "$dest")"
	[ -e "$src" ] || {
		log "  source missing: $src"
		return 1
	}
	if [ -L "$dest" ]; then
		rel="$(relpath "$dest" "$src")"
		[ "$(readlink "$dest")" = "$rel" ] && {
			log "  = $name"
			return 0
		}
		run rm -f "$dest"
	elif [ -e "$dest" ]; then
		if [ -d "$dest" ] && [ -z "$(find "$dest" -maxdepth 1 -mindepth 1 2>/dev/null)" ]; then
			log "  ~ $name is an empty real dir — replacing with symlink"
			run rmdir "$dest"
		else
			log "  $name exists and is NOT a symlink (non-empty?) — refusing"
			return 1
		fi
	fi
	run ln -sfn "$(relpath "$dest" "$src")" "$dest"
	log "  -> $name"
}

install_profile() {
	local profile="$1"
	local l1="$PROFILE_SRC/$profile/<thing>"
	local l2="$LIVE/$profile/<thing>"
	log ""
	log "profile: $profile"
	[ -d "$LIVE/$profile" ] || {
		log "  live profile missing"
		return 1
	}
	[ -d "$PROFILE_SRC/$profile" ] || run mkdir -p "$PROFILE_SRC/$profile"
	# Pitfall #2: level-2 source is the l1 pointer this run creates; fall back
	# to SOURCE for dry-run (where l1 doesn't exist yet).
	if [ -e "$l1" ]; then link_dir "$l2" "$l1"; else link_dir "$l2" "$SOURCE"; fi
	link_dir "$l1" "$SOURCE"
}

show_status() {
	local profile="$1"
	local l1="$PROFILE_SRC/$profile/<thing>"
	local l2="$LIVE/$profile/<thing>"
	log ""
	log "=== $profile ==="
	for d in "$l1" "$l2"; do
		local nm
		nm="$(basename "$d")"
		[ -e "$d" ] || [ -L "$d" ] || {
			log "  [$nm] absent"
			continue
		}
		[ -L "$d" ] || {
			log "  [$nm] REAL (not linked)"
			continue
		}
		local rt
		rt="$(resolve "$d")"
		# Pitfall #1: match the dir itself, not just its children.
		case "$rt" in
		"$SOURCE" | "$SOURCE"/*) log "  [$nm] ok -> $rt" ;;
		*) log "  [$nm] WRONG TARGET -> $rt" ;;
		esac
	done
}

usage() { sed -n '2,20p' "$0"; }

targets=()
for arg in "$@"; do
	case "$arg" in
	--dry-run) DRY_RUN=1 ;;
	--status) STATUS=1 ;;
	--all) ALL=1 ;;
	--help | -h)
		usage
		exit 0
		;;
	-*)
		log "unknown option: $arg"
		exit 2
		;;
	*) targets+=("$arg") ;;
	esac
done
[ "$DRY_RUN" = 1 ] && log "(dry run — nothing will change)"
if [ "$STATUS" = 1 ]; then
	show_status dev-ste-code
	show_status ste-code
	show_status benchmark-ste-code
	exit 0
fi
[ "$ALL" = 1 ] && targets=(dev-ste-code ste-code benchmark-ste-code)
[ "${#targets[@]}" -eq 0 ] && {
	log "usage: link-<thing>.sh <profile> | --all | --status [--dry-run]"
	exit 2
}
status=0
for p in "${targets[@]}"; do install_profile "$p" || status=1; done
log ""
[ "$status" = 0 ] && log "done. verify with: link-<thing>.sh --status" || log "completed with errors."
exit $status
