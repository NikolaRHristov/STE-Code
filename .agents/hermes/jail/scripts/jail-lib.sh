#!/usr/bin/env bash
# jail-lib.sh — shared shell library for the jail script packet.
#
# Single source of truth for the SHELL side, mirroring core/policy.py on the
# Python side. Source it; do not execute it.
#
#   source "$(dirname "$0")/jail-lib.sh"
#   jail_resolve_policy
#   jail_build_roots
#
# Provides:
#   jail_find_root          locate the project root by marker (no hop counting)
#   jail_resolve_policy     profile -> policy, failing closed
#   jail_build_roots        populate JAIL_ROOTS / JAIL_DENY for the policy
#   jail_emit_seatbelt      macOS Seatbelt profile on stdout
#   jail_bwrap_args         Linux bubblewrap arguments on stdout
#
# Sets: JAIL_POLICY, JAIL_PROJECT_ROOT, JAIL_PROFILE, JAIL_ROOTS[], JAIL_DENY[]

set -uo pipefail

JAIL_ROOT_MARKERS=(".git" "Makefile" "pyproject.toml")

# --- project root -------------------------------------------------------------
# Walk up from $1 (default: this library's directory) to the nearest marker.
#
# .git is the AUTHORITATIVE repo-root marker: it is scanned first across every
# ancestor so a weaker marker (package.json, pyproject.toml, Makefile) that
# lives in a subdirectory such as .agents/ can never hijack root detection.
# Only when no .git exists (detached, non-git checkout) do the weaker markers
# apply.
jail_find_root() {
    local dir="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
    local depth=0
    # Pass 1 — authoritative .git marker wins regardless of depth.
    local gdir="$dir"
    while [ "$depth" -lt 24 ]; do
        if [ -e "$gdir/.git" ]; then
            (cd "$gdir" && pwd -P)
            return 0
        fi
        local gparent
        gparent="$(dirname "$gdir")"
        [ "$gparent" = "$gdir" ] && break
        gdir="$gparent"
        depth=$((depth + 1))
    done
    # Pass 2 — weaker markers only when no .git is present.
    depth=0
    while [ "$depth" -lt 24 ]; do
        local marker
        for marker in "${JAIL_ROOT_MARKERS[@]}"; do
            if [ "$marker" = ".git" ]; then
                continue
            fi
            if [ -e "$dir/$marker" ]; then
                (cd "$dir" && pwd -P)
                return 0
            fi
        done
        local parent
        parent="$(dirname "$dir")"
        [ "$parent" = "$dir" ] && break
        dir="$parent"
        depth=$((depth + 1))
    done
    return 1
}

# --- profile / policy ---------------------------------------------------------
jail_active_profile() {
    if [ -n "${HERMES_PROFILE:-}" ]; then
        printf '%s\n' "$HERMES_PROFILE"
        return
    fi
    local home="${HERMES_HOME:-$HOME/.hermes}"
    if [ "$(basename "$(dirname "$home")")" = "profiles" ]; then
        basename "$home"
    else
        echo "default"
    fi
}

# Resolution order matches core/policy.py exactly.
jail_resolve_policy() {
    if [ -n "${STE_CODE_JAIL_POLICY:-}" ]; then
        JAIL_POLICY="$STE_CODE_JAIL_POLICY"
    else
        JAIL_PROFILE="$(jail_active_profile)"
        case "$JAIL_PROFILE" in
            dev-ste-code)       JAIL_POLICY="dev" ;;
            ste-code)           JAIL_POLICY="user" ;;
            benchmark-ste-code) JAIL_POLICY="bench" ;;
            # Fail closed: an unmapped profile gets the most restrictive policy.
            *)                  JAIL_POLICY="bench" ;;
        esac
    fi
    JAIL_PROFILE="${JAIL_PROFILE:-$(jail_active_profile)}"
    export JAIL_POLICY JAIL_PROFILE
}

# --- roots --------------------------------------------------------------------
_jail_push_root() { [ -n "${1:-}" ] && [ -d "$1" ] && JAIL_ROOTS+=("$(cd "$1" && pwd -P)"); }
_jail_push_deny() { [ -n "${1:-}" ] && JAIL_DENY+=("$1"); }

jail_build_roots() {
    JAIL_ROOTS=()
    JAIL_DENY=()

    local hermes_home="${HERMES_HOME:-$HOME/.hermes}"
    local tmp

    case "$JAIL_POLICY" in
        dev)
            _jail_push_root "$JAIL_PROJECT_ROOT"
            _jail_push_deny "$(dirname "$JAIL_PROJECT_ROOT")"
            _jail_push_deny "$JAIL_PROJECT_ROOT/.git"
            ;;
        user)
            # The STE-Code checkout is read-only; the user's own workspace is
            # writable only when it sits outside the checkout.
            local workspace="${JAIL_WORKSPACE:-$PWD}"
            workspace="$(cd "$workspace" && pwd -P)"
            case "$workspace" in
                "$JAIL_PROJECT_ROOT"|"$JAIL_PROJECT_ROOT"/*) ;;
                *) _jail_push_root "$workspace" ;;
            esac
            _jail_push_deny "$JAIL_PROJECT_ROOT"
            ;;
        bench)
            local out="${JAIL_BENCHMARK_OUTPUT:-$JAIL_PROJECT_ROOT/.agents/benchmark/tests}"
            mkdir -p "$out" 2>/dev/null || true
            _jail_push_root "$out"
            _jail_push_deny "$JAIL_PROJECT_ROOT"
            _jail_push_deny "$(dirname "$JAIL_PROJECT_ROOT")"
            ;;
        *)
            echo "jail-lib: unknown policy '$JAIL_POLICY'" >&2
            return 1
            ;;
    esac

    # Telemetry stays writable under every policy so runs remain inspectable.
    _jail_push_root "$hermes_home"
    for tmp in /private/tmp /tmp /private/var/folders /var/folders "${TMPDIR:-}"; do
        _jail_push_root "$tmp"
    done

    # de-duplicate, preserving order
    local unique=() root existing seen
    for root in ${JAIL_ROOTS[@]+"${JAIL_ROOTS[@]}"}; do
        seen=0
        for existing in ${unique[@]+"${unique[@]}"}; do
            [ "$existing" = "$root" ] && seen=1 && break
        done
        [ "$seen" -eq 0 ] && unique+=("$root")
    done
    JAIL_ROOTS=(${unique[@]+"${unique[@]}"})
}

# --- backends -----------------------------------------------------------------
# Seatbelt applies the LAST matching rule, so ordering is: allow all, deny all
# writes, allow the roots, then re-apply the denies.
jail_emit_seatbelt() {
    cat <<'HEADER'
(version 1)

;; Allow everything by default, then subtract write access. Reads, execution
;; and network are untouched here -- this profile confines WRITES only.
;; (Network egress is handled by the jail-net plugin.)
(allow default)
(deny file-write*)
HEADER
    local root
    for root in ${JAIL_ROOTS[@]+"${JAIL_ROOTS[@]}"}; do
        printf '(allow file-write* (subpath "%s"))\n' "$root"
    done
    echo
    echo ";; Denies applied last so they win over any broader allow above."
    for root in ${JAIL_DENY[@]+"${JAIL_DENY[@]}"}; do
        printf '(deny file-write* (subpath "%s"))\n' "$root"
    done
    # Re-allow the specific roots that are nested inside a denied tree
    # (the bench output dir lives under the denied project root).
    for root in ${JAIL_ROOTS[@]+"${JAIL_ROOTS[@]}"}; do
        local denied
        for denied in ${JAIL_DENY[@]+"${JAIL_DENY[@]}"}; do
            case "$root" in
                "$denied"/*) printf '(allow file-write* (subpath "%s"))\n' "$root" ;;
            esac
        done
    done
    cat <<'FOOTER'

;; Devices and stdio the toolchain needs regardless of the jail.
(allow file-write-data
    (literal "/dev/null")
    (literal "/dev/zero")
    (literal "/dev/dtracehelper")
    (literal "/dev/tty")
    (regex #"^/dev/fd/[0-9]+$")
    (regex #"^/dev/ttys[0-9]+$"))
FOOTER
}

jail_bwrap_args() {
    printf -- '--ro-bind / / --dev /dev --proc /proc'
    local root
    for root in ${JAIL_ROOTS[@]+"${JAIL_ROOTS[@]}"}; do
        printf -- ' --bind %s %s' "$root" "$root"
    done
    # bwrap has no deny primitive; re-bind denied trees read-only.
    for root in ${JAIL_DENY[@]+"${JAIL_DENY[@]}"}; do
        [ -d "$root" ] && printf -- ' --ro-bind %s %s' "$root" "$root"
    done
    # Nested allows must come back after the read-only rebind.
    for root in ${JAIL_ROOTS[@]+"${JAIL_ROOTS[@]}"}; do
        local denied
        for denied in ${JAIL_DENY[@]+"${JAIL_DENY[@]}"}; do
            case "$root" in
                "$denied"/*) printf -- ' --bind %s %s' "$root" "$root" ;;
            esac
        done
    done
}

# --- one-shot initialisation --------------------------------------------------
jail_init() {
    if ! JAIL_PROJECT_ROOT="$(jail_find_root "${1:-}")"; then
        echo "jail-lib: cannot locate a project root" >&2
        return 1
    fi
    export JAIL_PROJECT_ROOT
    jail_resolve_policy
    jail_build_roots
}
