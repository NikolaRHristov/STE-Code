#!/usr/bin/env bash
# link-memory.sh — make .agents/hermes/memory/<profile>/ the single source of
# truth for each profile's persistent memory (USER.md, MEMORY.md), linked into
# the live profile as relative symlinks:
#
#   .agents/hermes/memory/<profile>/USER.md    (SOURCE OF TRUTH, tracked)
#        ^  ~/.hermes/profiles/<profile>/memories/USER.md   (live profile)
#
# The canonical copy is version-controlled; the live profile loads it through
# the symlink on every session start, so memory is shared across machines and
# survives a profile wipe. Mirrors the skills convention in link-skills.sh.
#
# Usage:
#   link-memory.sh --all [--dry-run]
#   link-memory.sh <profile> [--dry-run]
#   link-memory.sh --status
#   link-memory.sh --help
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/.." && pwd)"          # .agents
MEM_SRC="$REPO/hermes/memory"                 # .agents/hermes/memory  (canonical, tracked)
LIVE="$HOME/.hermes/profiles"

DRY_RUN=0
ALL=0
STATUS=0

log()  { printf '%s\n' "$*"; }
run()  { if [ "$DRY_RUN" = 1 ]; then log "  would: $*"; else "$@"; fi; }

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

# Link a profile's persistent memory (USER.md, MEMORY.md) into the repo-tracked
# canonical copy. Refuses to replace a non-symlink real file (same safety as the
# skills link_level): a real file means the operator hand-authored memory in the
# profile and we must not clobber it.
link_memory() {
    local profile="$1"
    local memdir="$MEM_SRC/$profile"
    local live_mem="$LIVE/$profile/memories"
    if [ ! -d "$memdir" ]; then
        log "  [memory] canonical dir missing: $memdir (create it first)"; return 1
    fi
    if [ ! -d "$live_mem" ]; then
        log "  [memory] live memories dir missing: $live_mem (create profile first)"; return 1
    fi
    for f in USER.md MEMORY.md; do
        local src="$memdir/$f" dest="$live_mem/$f"
        if [ ! -e "$src" ]; then
            log "  [memory] canonical $f missing in $memdir — create it first"; continue
        fi
        if [ -L "$dest" ]; then
            rel="$(relpath "$dest" "$src")"
            if [ "$(readlink "$dest")" = "$rel" ]; then log "  [memory] = $f"; continue; fi
            run rm -f "$dest"
        elif [ -e "$dest" ]; then
            log "  [memory] ✗ $f exists and is NOT a symlink — refusing to replace"; continue
        fi
        run ln -sfn "$(relpath "$dest" "$src")" "$dest"
        log "  [memory] → $f"
    done
}

show_memory_status() {
    local profile="$1"
    local memdir="$MEM_SRC/$profile"
    local live_mem="$LIVE/$profile/memories"
    log "  --- memory ---"
    if [ ! -d "$memdir" ]; then log "  [memory] canonical dir missing: $memdir"; return; fi
    if [ ! -d "$live_mem" ]; then log "  [memory] live dir missing: $live_mem"; return; fi
    for f in USER.md MEMORY.md; do
        local dest="$live_mem/$f"
        if [ ! -e "$dest" ]; then log "  [memory] $f: absent"; continue; fi
        if [ ! -L "$dest" ]; then log "  [memory] $f: REAL FILE (not linked)"; continue; fi
        local rt; rt="$(resolve "$dest")"
        case "$rt" in
            "$memdir"/*) log "  [memory] $f: ok -> $rt" ;;
            *)           log "  [memory] $f: WRONG TARGET -> $rt" ;;
        esac
    done
}

usage() { sed -n '2,22p' "$0"; }

targets=()
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
        --status)  STATUS=1 ;;
        --all)     ALL=1 ;;
        --help|-h) usage; exit 0 ;;
        -*)        log "unknown option: $arg"; exit 2 ;;
        *)         targets+=("$arg") ;;
    esac
done

[ "$DRY_RUN" = 1 ] && log "(dry run — nothing will change)"

if [ "$STATUS" = 1 ]; then
    for p in dev-ste-code ste-code benchmark-ste-code; do
        log "=== $p ==="
        show_memory_status "$p"
    done
    exit 0
fi

if [ "$ALL" = 1 ]; then targets=(dev-ste-code ste-code benchmark-ste-code); fi
if [ "${#targets[@]}" -eq 0 ]; then
    log "usage: link-memory.sh <profile> | --all | --status [--dry-run]"
    exit 2
fi

status=0
for p in "${targets[@]}"; do
    log ""
    log "profile: $p"
    link_memory "$p" || status=1
done
log ""
if [ "$status" = 0 ]; then log "done. verify with: link-memory.sh --status"; else log "completed with errors."; fi
exit $status
