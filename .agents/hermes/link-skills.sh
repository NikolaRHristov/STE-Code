#!/usr/bin/env bash
# link-skills.sh — make .agents/skills/ the single source of truth for every
# STE-Code Hermes profile, distributed via two-level symlinks:
#
#   .agents/skills/<bucket>                            (SOURCE OF TRUTH)
#        ^  .agents/hermes/profiles/<p>/skills/<bucket>    (profile repo dir)
#               ^  ~/.hermes/profiles/<p>/skills/<bucket> (live profile)
#
# Every enabled skill bucket therefore lives ONCE in the repository. Editing a
# skill updates every profile at once; nothing can drift, because the live
# profile loads the file through the symlink chain on every session start.
#
# A profile's bucket set is derived, not hard-coded: it is whatever the
# profile's repo skills dir already symlinks into the source, plus any buckets
# named in an optional .agents/hermes/profiles/<p>/SKILLS manifest (one per
# line). Use --add <bucket> to push a new bucket onto a profile. This keeps the
# intentional per-profile subsets (dev gets all four, bench gets one) while
# guaranteeing every linked bucket resolves into the single source.
#
# Known foreign buckets (real-copy Hermes defaults that must never load inside a
# STE profile) are pruned by name; any OTHER leak is genuine authored content
# that --prune only flags for manual relocation into .agents/skills/.
#
# Usage:
#   link-skills.sh --all [--dry-run] [--prune]
#   link-skills.sh <profile> [--dry-run] [--prune] [--add <bucket>]
#   link-skills.sh --status
#   link-skills.sh --help
#
#   --prune   Remove foreign default skill buckets from the LIVE profile.
#             Off by default — pruning changes what the profile loads.
#   --add     Add <bucket> (must exist in .agents/skills/) to the profile's set.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/.." && pwd)"          # .agents
SOURCE="$(cd "$REPO/skills" && pwd)"          # .agents/skills  (single source)
PROFILE_SRC="$REPO/hermes/profiles"           # .agents/hermes/profiles
LIVE="$HOME/.hermes/profiles"

DRY_RUN=0
PRUNE=0
ADDS=()
ALL=0
STATUS=0

log()  { printf '%s\n' "$*"; }
run()  { if [ "$DRY_RUN" = 1 ]; then log "  would: $*"; else "$@"; fi; }

resolve() {
    python3 -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' "$1" 2>/dev/null || echo "$1"
}

STATE_FILES=".bundled_manifest .usage.json .usage.json.lock"

is_state_file() {
    local n; n="$(basename "$1")"
    for s in $STATE_FILES; do [ "$n" = "$s" ] && return 0; done
    return 1
}

# Foreign Hermes default skill buckets that must NOT load inside a STE profile.
# Pruned by name; everything else that is a leak is treated as authored content.
FOREIGN_DEFAULTS="apple autonomous-ai-agents creative email github media mlops \
note-taking productivity research smart-home social-media software-development"

is_foreign_default() {
    local n="$1"
    for f in $FOREIGN_DEFAULTS; do [ "$n" = "$f" ] && return 0; done
    return 1
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

# $1 = absolute source path (must exist)   $2 = dest symlink (absolute)
link_level() {
    local src="$1" dest="$2" name rel
    name="$(basename "$dest")"
    if [ ! -e "$src" ]; then log "  ✗ source missing: $src"; return 1; fi
    rel="$(relpath "$dest" "$src")"
    if [ -L "$dest" ]; then
        if [ "$(readlink "$dest")" = "$rel" ]; then log "  = $name"; return 0; fi
        run rm -f "$dest"
    elif [ -e "$dest" ]; then
        log "  ✗ $name exists and is NOT a symlink — refusing to replace"; return 1
    fi
    run ln -sfn "$rel" "$dest"
    log "  → $name"
}

# Build the desired bucket list for a profile (POSIX-safe, no readarray).
desired_buckets() {
    local profile="$1" src_skills="$PROFILE_SRC/$profile/skills" mfile manifest
    manifest="$(mktemp)"
    # 1) buckets the profile already symlinks into the source
    if [ -d "$src_skills" ]; then
        for e in "$src_skills"/*; do
            [ -L "$e" ] || continue
            local rt; rt="$(resolve "$e")"
            case "$rt" in
                "$SOURCE"/*) basename "$e" >> "$manifest" ;;
            esac
        done
    fi
    # 2) optional explicit manifest
    mfile="$PROFILE_SRC/$profile/SKILLS"
    if [ -f "$mfile" ]; then
        while IFS= read -r line; do
            [ -z "${line:-}" ] && continue
            case "$line" in \#*) continue ;; esac
            echo "$line" >> "$manifest"
        done < "$mfile"
    fi
    # 3) --add overrides
    local i
    for i in "${!ADDS[@]}"; do
        [ -n "${ADDS[$i]:-}" ] && echo "${ADDS[$i]}" >> "$manifest"
    done
    # dedupe, preserve order
    awk '!seen[$0]++' "$manifest"
    rm -f "$manifest"
}

install_profile() {
    local profile="$1"
    local src_skills="$PROFILE_SRC/$profile/skills"
    local live_skills="$LIVE/$profile/skills"
    log ""
    log "profile: $profile"

    if [ ! -d "$LIVE/$profile" ]; then
        log "  ✗ live profile missing: $LIVE/$profile (create it first)"; return 1
    fi

    [ -d "$src_skills" ] || run mkdir -p "$src_skills"
    [ -d "$live_skills" ] || run mkdir -p "$live_skills"

    local buckets="" b
    buckets="$(desired_buckets "$profile")"
    if [ -z "$buckets" ]; then
        log "  (no buckets declared for this profile)"
    fi

    # shellcheck disable=SC2086
    for b in $buckets; do
        local src="$SOURCE/$b"
        if [ ! -d "$src" ]; then
            log "  ✗ bucket '$b' not found in source ($SOURCE) — skipping"
            continue
        fi
        # level 1: profile repo dir -> single source
        link_level "$src" "$src_skills/$b"
        # level 2: live profile -> profile repo dir
        link_level "$src_skills/$b" "$live_skills/$b"
    done

    if [ "$PRUNE" = 1 ]; then
        log "  [prune] scanning live skills for foreign default entries"
        for e in "$live_skills"/*; do
            [ -e "$e" ] || continue
            is_state_file "$e" && continue
            local nm; nm="$(basename "$e")"
            if [ -L "$e" ]; then
                local rt; rt="$(resolve "$e")"
                case "$rt" in
                    "$SOURCE"/*) continue ;;                       # good
                    *) if is_foreign_default "$nm"; then
                           log "  prune: $nm -> $rt (foreign default)"; run rm -f "$e"
                       else
                           log "  keep (relocate to .agents/skills/): $nm -> $rt"
                       fi ;;
                esac
            else
                if is_foreign_default "$nm"; then
                    log "  prune: $nm is a real copy (foreign default)"; run rm -rf "$e"
                else
                    log "  keep (relocate to .agents/skills/): $nm is a real copy"
                fi
            fi
        done
    fi
}

show_status() {
    for profile in dev-ste-code ste-code benchmark-ste-code; do
        local live_skills="$LIVE/$profile/skills"
        log ""
        log "=== $profile ==="
        if [ ! -d "$live_skills" ]; then log "  (no live skills dir)"; continue; fi
        local leaks=0
        for e in "$live_skills"/*; do
            [ -e "$e" ] || continue
            is_state_file "$e" && continue
            local nm; nm="$(basename "$e")"
            if [ -L "$e" ]; then
                local rt; rt="$(resolve "$e")"
                case "$rt" in
                    "$SOURCE"/*) log "  [ok]   $nm -> $rt" ;;
                    *) if is_foreign_default "$nm"; then
                           log "  [LEAK] $nm -> $rt (foreign default)"; leaks=$((leaks+1))
                       else
                           log "  [RELOCATE] $nm -> $rt (authored; move to .agents/skills/)"; leaks=$((leaks+1))
                       fi ;;
                esac
            else
                if is_foreign_default "$nm"; then
                    log "  [LEAK] $nm is a real copy (foreign default)"; leaks=$((leaks+1))
                else
                    log "  [RELOCATE] $nm is a real copy (authored; move to .agents/skills/)"; leaks=$((leaks+1))
                fi
            fi
        done
        if [ "$leaks" -eq 0 ]; then
            log "  result: OK — only symlinked STE skills"
        else
            log "  result: $leaks item(s) to fix; run: skills-link.sh $profile --prune"
        fi
    done
}

usage() { sed -n '2,50p' "$0"; }

targets=()
expect_add=0
for arg in "$@"; do
    if [ "$expect_add" = 1 ]; then
        ADDS+=("$arg"); expect_add=0; continue
    fi
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
        --prune)   PRUNE=1 ;;
        --status)  STATUS=1 ;;
        --all)     ALL=1 ;;
        --add)     expect_add=1 ;;
        --help|-h) usage; exit 0 ;;
        -*)        log "unknown option: $arg"; exit 2 ;;
        *)         targets+=("$arg") ;;
    esac
done

[ "$DRY_RUN" = 1 ] && log "(dry run — nothing will change)"

if [ "$STATUS" = 1 ]; then show_status; exit 0; fi

if [ "$ALL" = 1 ]; then targets=(dev-ste-code ste-code benchmark-ste-code); fi
if [ "${#targets[@]}" -eq 0 ]; then
    log "usage: skills-link.sh <profile> | --all | --status [--dry-run] [--prune] [--add <bucket>]"
    exit 2
fi

status=0
for p in "${targets[@]}"; do
    install_profile "$p" || status=1
done
log ""
if [ "$status" = 0 ]; then log "done. verify with: skills-link.sh --status"; else log "completed with errors."; fi
exit $status
