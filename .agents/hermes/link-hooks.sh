#!/usr/bin/env bash
# link-hooks.sh — make .agents/hermes/hooks/ the single source of truth for every
# STE-Code Hermes profile's pre/post tool-call hooks, distributed via relative
# symlinks:
#
#   .agents/hermes/hooks/                              (SOURCE OF TRUTH, tracked)
#        ^  .agents/hermes/profiles/<p>/hooks             (profile repo dir — pointer)
#               ^  ~/.hermes/profiles/<p>/hooks           (live profile — loads these)
#
# Every profile therefore loads the SAME canonical hook set through the symlink
# chain on every session start. Editing a hook updates every profile at once;
# nothing can drift, because the live profile reads the file through the link.
#
# This mirrors link-skills.sh (directory-level variant: hooks are a flat set
# shared by all profiles, not a per-profile selected bucket subset). The global
# agent hook dir (~/.hermes/hermes-agent/hooks) is expected to be a symlink to
# the same canonical source; this script links the per-PROFILE hook dirs, which
# is what makes each profile (dev-ste-code, ste-code, benchmark-ste-code) pick
# up the hooks independently of the global default.
#
# A profile's hooks/ may be a real (empty) directory left by Hermes at runtime.
# An EMPTY real dir is safely removed and replaced by the symlink. A NON-EMPTY
# real dir is left alone (warn + skip) so authored runtime content is never
# clobbered.
#
# A non-empty real dir can be repaired with --force. --force never blind-deletes:
# it removes an entry only when the entry is positively classified as disposable
# (a stale copy of a canonical hook, or a known-retired hook), moves the
# hook-generated logs/ dir aside instead of deleting it, and KEEPS plus REPORTS
# anything it does not recognise. If unrecognised entries remain the directory is
# still refused, naming exactly what blocked it.
#
# Usage:
#   link-hooks.sh --all [--dry-run] [--force]
#   link-hooks.sh <profile> [--dry-run] [--force]
#   link-hooks.sh --status
#   link-hooks.sh --help
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/.." && pwd)"       # .agents
SOURCE="$(cd "$REPO/hermes/hooks" && pwd)" # .agents/hermes/hooks  (single source)
PROFILE_SRC="$REPO/hermes/profiles"        # .agents/hermes/profiles
LIVE="$HOME/.hermes/profiles"
GLOBAL_HOOKS="$HOME/.hermes/agent-hooks"

DRY_RUN=0
ALL=0
STATUS=0
FORCE=0

log() { printf '%s\n' "$*"; }
run() { if [ "$DRY_RUN" = 1 ]; then log "  would: $*"; else "$@"; fi; }

# --- classification predicates (link-skills.sh idiom) -----------------------
# Only entries a predicate can positively identify are ever removed. Anything
# unrecognised is kept and reported for the operator to handle by hand.

# Hooks deleted from the canonical source (commit f3b8a3d) that may survive as
# stale copies in a runtime hooks dir.
RETIRED_HOOKS="pre-tool-call-diagnostic.sh pre-tool-call-modify-terminal.sh \
test-pre-modify.sh"

is_retired_hook() {
	local n="$1"
	for r in $RETIRED_HOOKS; do [ "$n" = "$r" ] && return 0; done
	return 1
}

# A file whose name matches a hook in the canonical source: a stale copy, safe
# to drop because the symlink restores the authoritative version.
is_canonical_hook() {
	[ -f "$SOURCE/$1" ]
}

# Runtime log dir created by the hooks themselves. Never deleted — relocated
# next to the hooks dir so nothing an operator may want is destroyed.
is_runtime_logs() { [ "$1" = "logs" ]; }

resolve() {
	python3 -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' "$1" 2>/dev/null || echo "$1"
}

# Emit a relative symlink target (repo convention: links stay relocatable).
relpath() {
	python3 - "$1" "$2" <<'PY'
import os, sys
dest, src = sys.argv[1], sys.argv[2]
dest_dir = os.path.dirname(os.path.abspath(dest))
print(os.path.relpath(os.path.abspath(src), dest_dir))
PY
}

# Prune a non-empty real hooks dir down to nothing, conservatively.
# Removes only entries a predicate positively identifies; keeps and reports the
# rest. Echoes the names of blocking entries on stdout via BLOCKERS.
# $1 = dir (absolute)
BLOCKERS=()
prune_hooks_dir() {
	local dir="$1" e nm
	BLOCKERS=()
	for e in "$dir"/* "$dir"/.[!.]*; do
		[ -e "$e" ] || [ -L "$e" ] || continue
		nm="$(basename "$e")"
		if is_retired_hook "$nm"; then
			log "    prune: $nm (retired hook, removed from source in f3b8a3d)"
			run rm -f "$e"
		elif [ -L "$e" ]; then
			log "    prune: $nm (symlink into the canonical source)"
			run rm -f "$e"
		elif is_canonical_hook "$nm"; then
			log "    prune: $nm (stale copy of a canonical hook)"
			run rm -f "$e"
		elif is_runtime_logs "$nm"; then
			log "    relocate: $nm -> $dir-logs (runtime logs, never deleted)"
			run mv "$e" "$dir-logs"
		else
			log "    keep (unrecognised — handle by hand): $nm"
			BLOCKERS+=("$nm")
		fi
	done
}

# Link a hook directory (level dest) to the canonical source dir.
# $1 = dest symlink (absolute)   $2 = source dir (absolute, must exist)
link_dir() {
	local dest="$1" src="$2" name rel
	name="$(basename "$dest")"
	if [ ! -e "$src" ]; then
		log "  ✗ source missing: $src"
		return 1
	fi
	if [ -L "$dest" ]; then
		rel="$(relpath "$dest" "$src")"
		if [ "$(readlink "$dest")" = "$rel" ]; then
			log "  = $name"
			return 0
		fi
		run rm -f "$dest"
	elif [ -e "$dest" ]; then
		if [ -d "$dest" ] && [ -z "$(find "$dest" -maxdepth 1 -mindepth 1 2>/dev/null)" ]; then
			log "  ~ $name is an empty real dir — replacing with symlink"
			run rmdir "$dest"
		elif [ -d "$dest" ] && [ "$FORCE" = 1 ]; then
			log "  ! $name is a non-empty real dir — --force: pruning what is provably disposable"
			prune_hooks_dir "$dest"
			if [ "${#BLOCKERS[@]}" -gt 0 ]; then
				log "  ✗ $name still holds ${#BLOCKERS[@]} unrecognised entr$([ "${#BLOCKERS[@]}" = 1 ] && echo y || echo ies) — refusing to replace:"
				for b in "${BLOCKERS[@]}"; do log "      $b"; done
				log "      move or delete them by hand, then re-run with --force"
				return 1
			fi
			if [ "$DRY_RUN" = 1 ]; then
				log "  would: rmdir $dest (empty after prune)"
				log "  would: ln -sfn $(relpath "$dest" "$src") $dest"
				return 0
			fi
			rmdir "$dest"
		else
			log "  ✗ $name exists and is NOT a symlink (non-empty?) — refusing to replace$([ "$FORCE" = 1 ] || echo " (retry with --force)")"
			return 1
		fi
	fi
	run ln -sfn "$(relpath "$dest" "$src")" "$dest"
	log "  → $name"
}

install_profile() {
	local profile="$1"
	local l1="$PROFILE_SRC/$profile/hooks" # level 1: profile repo dir
	local l2="$LIVE/$profile/hooks"        # level 2: live profile
	log ""
	log "profile: $profile"
	if [ ! -d "$LIVE/$profile" ]; then
		log "  ✗ live profile missing: $LIVE/$profile (create it first)"
		return 1
	fi
	[ -d "$PROFILE_SRC/$profile" ] || run mkdir -p "$PROFILE_SRC/$profile"
	# Level-2's source is the level-1 pointer we create in the same run; if it
	# does not exist yet (e.g. dry-run, which writes nothing), fall back to the
	# canonical source so the link target is computed against the real dir.
	if [ -e "$l1" ]; then
		link_dir "$l2" "$l1"
	else
		link_dir "$l2" "$SOURCE"
	fi
	link_dir "$l1" "$SOURCE"
}

install_global() {
	log ""
	log "global: ~/.hermes/agent-hooks"
	if [ ! -d "$(dirname "$GLOBAL_HOOKS")" ]; then
		log "  ✗ ~/.hermes missing"
		return 1
	fi
	link_dir "$GLOBAL_HOOKS" "$SOURCE"
}

show_status() {
	local profile="$1"
	local l1="$PROFILE_SRC/$profile/hooks"
	local l2="$LIVE/$profile/hooks"
	log ""
	log "=== $profile ==="
	for d in "$l1" "$l2"; do
		local nm
		nm="$(basename "$d")"
		if [ ! -e "$d" ] && [ ! -L "$d" ]; then
			log "  [$nm] absent"
			continue
		fi
		if [ ! -L "$d" ]; then
			log "  [$nm] REAL DIR/$([ -d "$d" ] && echo dir || echo file) (not linked)"
			continue
		fi
		local rt
		rt="$(resolve "$d")"
		case "$rt" in
		"$SOURCE" | "$SOURCE"/*) log "  [$nm] ok -> $rt" ;;
		*) log "  [$nm] WRONG TARGET -> $rt" ;;
		esac
	done
}

usage() { sed -n '2,37p' "$0"; }

targets=()
for arg in "$@"; do
	case "$arg" in
	--dry-run) DRY_RUN=1 ;;
	--status) STATUS=1 ;;
	--force) FORCE=1 ;;
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
	log ""
	log "=== global agent hooks (expect symlink -> canonical) ==="
	for g in "$HOME/.hermes/hermes-agent/hooks" "$GLOBAL_HOOKS"; do
		if [ -L "$g" ]; then
			log "  [$g] ok -> $(resolve "$g")"
		elif [ -d "$g" ]; then
			log "  [$g] REAL DIR ($(find "$g" -maxdepth 1 -mindepth 1 2>/dev/null | wc -l | tr -d ' ') entries) — repair with: link-hooks.sh --all --force"
		else
			log "  [$g] absent"
		fi
	done
	exit 0
fi

if [ "$ALL" = 1 ]; then targets=(dev-ste-code ste-code benchmark-ste-code); fi
if [ "${#targets[@]}" -eq 0 ]; then
	log "usage: link-hooks.sh <profile> | --all | --status [--dry-run] [--force]"
	exit 2
fi

status=0
for p in "${targets[@]}"; do
	install_profile "$p" || status=1
done
if [ "$ALL" = 1 ]; then
	install_global || status=1
fi
log ""
if [ "$status" = 0 ]; then log "done. verify with: link-hooks.sh --status"; else log "completed with errors."; fi
exit $status
