#!/usr/bin/env bash
# jail-exec.sh — run a command under KERNEL-ENFORCED write confinement.
#
# Layer 1 of ste-code-jail (the pre_tool_call hook) inspects tool arguments.
# It cannot see inside an opaque subprocess: `python3 build.py` may call
# os.makedirs("../out") and no argument analysis can know that.
#
# This script closes that gap. It asks the OS to refuse the write:
#
#   macOS  sandbox-exec with a generated Seatbelt profile
#   Linux  bubblewrap (bwrap) with a read-only bind of / and read-write
#          binds of the allowed roots
#
# Reads stay unrestricted on both platforms — only writes are confined.
#
# Usage:
#   ./jail-exec.sh <command> [args...]
#   ./jail-exec.sh --print-profile        # show the generated policy and exit
#   ./jail-exec.sh --check                # verify confinement actually works
#
# Environment:
#   JAIL_EXTRA_ROOTS  colon-separated extra writable roots
#   JAIL_VERBOSE=1    log the backend and roots to stderr
#
# Exit codes:
#   0    command succeeded
#   1    command failed
#   126  no sandbox backend available on this platform
#   127  usage error
#
# Example — wrap a whole pipeline stage so even its subprocesses are confined:
#   .agents/hermes/plugins/ste-code-jail/scripts/jail-exec.sh \
#       python3 .agents/tools/runners/phase-a-run.py

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- locate the project root (same markers as the plugin) --------------------
find_root() {
    local dir="$SCRIPT_DIR"
    for _ in $(seq 1 24); do
        if [ -e "$dir/.git" ] || [ -e "$dir/Makefile" ]; then
            printf '%s\n' "$dir"
            return 0
        fi
        local parent
        parent="$(dirname "$dir")"
        [ "$parent" = "$dir" ] && break
        dir="$parent"
    done
    return 1
}

if ! PROJECT_ROOT="$(find_root)"; then
    echo "jail-exec: cannot locate project root above $SCRIPT_DIR" >&2
    exit 127
fi
PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd -P)"

# --- assemble the writable roots ---------------------------------------------
ROOTS=("$PROJECT_ROOT")

HERMES_ROOT="${HERMES_HOME:-$HOME/.hermes}"
[ -d "$HERMES_ROOT" ] && ROOTS+=("$(cd "$HERMES_ROOT" && pwd -P)")

for tmp in /private/tmp /tmp /private/var/folders /var/folders "${TMPDIR:-}"; do
    [ -n "$tmp" ] && [ -d "$tmp" ] && ROOTS+=("$(cd "$tmp" && pwd -P)")
done

if [ -n "${JAIL_EXTRA_ROOTS:-}" ]; then
    IFS=':' read -r -a extra <<< "$JAIL_EXTRA_ROOTS"
    for path in "${extra[@]}"; do
        [ -n "$path" ] && [ -d "$path" ] && ROOTS+=("$(cd "$path" && pwd -P)")
    done
fi

# de-duplicate while preserving order
UNIQUE=()
for root in "${ROOTS[@]}"; do
    seen=0
    for existing in ${UNIQUE[@]+"${UNIQUE[@]}"}; do
        [ "$existing" = "$root" ] && seen=1 && break
    done
    [ "$seen" -eq 0 ] && UNIQUE+=("$root")
done
ROOTS=("${UNIQUE[@]}")

if [ "${JAIL_VERBOSE:-0}" = "1" ]; then
    echo "jail-exec: project root: $PROJECT_ROOT" >&2
    for root in "${ROOTS[@]}"; do echo "jail-exec: writable: $root" >&2; done
fi

# --- macOS: generate a Seatbelt profile --------------------------------------
build_seatbelt_profile() {
    cat <<'HEADER'
(version 1)

;; Allow everything by default, then subtract write access. Reads, network,
;; and process execution are untouched — this profile confines writes only.
(allow default)

;; Revoke all filesystem writes...
(deny file-write*)

;; ...then grant them back for the allowed roots.
HEADER
    for root in "${ROOTS[@]}"; do
        printf '(allow file-write* (subpath "%s"))\n' "$root"
    done
    cat <<'MIDDLE'

;; Re-deny the project's PARENT directory. A checkout inside an allowed tree
;; (e.g. /tmp) would otherwise inherit write access one level up -- exactly
;; the escape this jail exists to stop. Seatbelt applies the LAST matching
;; rule, so this deny follows the allows, and the allow for the project root
;; itself is reinstated immediately after.
MIDDLE
    printf '(deny file-write* (subpath "%s"))\n' "$(dirname "$PROJECT_ROOT")"
    printf '(allow file-write* (subpath "%s"))\n' "$PROJECT_ROOT"
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

# --- entry points -------------------------------------------------------------
case "${1:-}" in
    --print-profile)
        if [ "$(uname -s)" = "Darwin" ]; then
            build_seatbelt_profile
        else
            printf 'bwrap --ro-bind / /'
            for root in "${ROOTS[@]}"; do printf ' --bind %s %s' "$root" "$root"; done
            printf ' --dev /dev --proc /proc -- <command>\n'
        fi
        exit 0
        ;;
    --check)
        # Prove the jail actually refuses a write outside the roots.
        outside="$(dirname "$PROJECT_ROOT")/.jail-exec-selfcheck-$$"
        if "$0" /bin/sh -c "mkdir -p '$outside'" 2>/dev/null; then
            rmdir "$outside" 2>/dev/null || true
            echo "jail-exec: FAIL — write outside the jail SUCCEEDED"
            exit 1
        fi
        inside="$PROJECT_ROOT/.agents/tmp/.jail-exec-selfcheck-$$"
        if ! "$0" /bin/sh -c "mkdir -p '$inside' && rmdir '$inside'" 2>/dev/null; then
            echo "jail-exec: FAIL — write INSIDE the jail was refused"
            exit 1
        fi
        if ! "$0" /bin/sh -c 'head -1 /etc/hosts >/dev/null' 2>/dev/null; then
            echo "jail-exec: FAIL — read outside the jail was refused"
            exit 1
        fi
        echo "jail-exec: ok (writes confined, reads unrestricted)"
        exit 0
        ;;
    "")
        echo "usage: jail-exec.sh <command> [args...]" >&2
        echo "       jail-exec.sh --print-profile | --check" >&2
        exit 127
        ;;
esac

# --- dispatch to the platform backend ----------------------------------------
case "$(uname -s)" in
    Darwin)
        if ! command -v sandbox-exec >/dev/null 2>&1; then
            echo "jail-exec: sandbox-exec not found" >&2
            exit 126
        fi
        profile="$(mktemp -t jail-exec)"
        trap 'rm -f "$profile"' EXIT
        build_seatbelt_profile > "$profile"
        exec sandbox-exec -f "$profile" "$@"
        ;;
    Linux)
        if ! command -v bwrap >/dev/null 2>&1; then
            echo "jail-exec: bwrap (bubblewrap) not found." >&2
            echo "  Debian/Ubuntu: apt install bubblewrap" >&2
            echo "  Fedora:        dnf install bubblewrap" >&2
            exit 126
        fi
        args=(--ro-bind / / --dev /dev --proc /proc)
        for root in "${ROOTS[@]}"; do args+=(--bind "$root" "$root"); done
        exec bwrap "${args[@]}" -- "$@"
        ;;
    *)
        echo "jail-exec: no sandbox backend for $(uname -s)" >&2
        exit 126
        ;;
esac
