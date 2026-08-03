#!/usr/bin/env bash
# jail-exec.sh — run a command under KERNEL-ENFORCED write confinement.
#
# The plugin layer inspects tool arguments and cannot see inside an opaque
# subprocess: `python3 build.py` may call os.makedirs("../out") and no
# argument analysis can know that. This script closes that gap by asking the
# OS to refuse the write:
#
#   macOS  sandbox-exec with a generated Seatbelt profile
#   Linux  bubblewrap (bwrap)
#
# The policy comes from jail-lib.sh — the same profile mapping the plugins
# use, so the shell and Python sides can never disagree.
#
# Usage:
#   jail-exec.sh <command> [args...]
#   jail-exec.sh --print-profile     show the generated policy and exit
#   jail-exec.sh --check             verify confinement actually works
#   jail-exec.sh --show              print the resolved policy and roots
#
# Environment:
#   STE_CODE_JAIL_POLICY   force dev|user|bench
#   JAIL_BENCHMARK_OUTPUT  writable output dir for the bench policy
#   JAIL_WORKSPACE         the user's own project dir for the user policy
#   JAIL_VERBOSE=1         log backend and roots to stderr
#
# Exit codes: 0 ok · 1 command failed · 126 no backend · 127 usage error

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=jail-lib.sh
source "$SCRIPT_DIR/jail-lib.sh"

if ! jail_init "$SCRIPT_DIR"; then
	exit 127
fi

if [ "${JAIL_VERBOSE:-0}" = "1" ]; then
	echo "jail-exec: profile=$JAIL_PROFILE policy=$JAIL_POLICY" >&2
	echo "jail-exec: project root: $JAIL_PROJECT_ROOT" >&2
	for r in ${JAIL_ROOTS[@]+"${JAIL_ROOTS[@]}"}; do echo "jail-exec: rw  $r" >&2; done
	for r in ${JAIL_DENY[@]+"${JAIL_DENY[@]}"}; do echo "jail-exec: ro  $r" >&2; done
fi

case "${1:-}" in
--show)
	echo "profile      : $JAIL_PROFILE"
	echo "policy       : $JAIL_POLICY"
	echo "project root : $JAIL_PROJECT_ROOT"
	echo "writable:"
	for r in ${JAIL_ROOTS[@]+"${JAIL_ROOTS[@]}"}; do echo "  + $r"; done
	echo "denied:"
	for r in ${JAIL_DENY[@]+"${JAIL_DENY[@]}"}; do echo "  - $r"; done
	exit 0
	;;
--print-profile)
	if [ "$(uname -s)" = "Darwin" ]; then
		jail_emit_seatbelt
	else
		echo "bwrap $(jail_bwrap_args) -- <command>"
	fi
	exit 0
	;;
--check)
	# A writable location under the current policy, used to prove that
	# confinement does not break legitimate work.
	inside=""
	for r in ${JAIL_ROOTS[@]+"${JAIL_ROOTS[@]}"}; do
		case "$r" in
		/tmp | /private/tmp | /var/folders* | /private/var/folders*) continue ;;
		esac
		inside="$r/.jail-exec-selfcheck-$$"
		break
	done

	# Always outside every policy's roots.
	outside="$HOME/.jail-exec-selfcheck-$$"

	if "$0" /bin/sh -c "mkdir -p '$outside'" 2>/dev/null; then
		rmdir "$outside" 2>/dev/null || true
		echo "jail-exec: FAIL — write outside the jail SUCCEEDED"
		exit 1
	fi

	if [ -n "$inside" ]; then
		if ! "$0" /bin/sh -c "mkdir -p '$inside' && rmdir '$inside'" 2>/dev/null; then
			echo "jail-exec: FAIL — write INSIDE the jail was refused ($inside)"
			exit 1
		fi
	fi

	if ! "$0" /bin/sh -c 'head -1 /etc/hosts >/dev/null' 2>/dev/null; then
		echo "jail-exec: FAIL — read outside the jail was refused"
		exit 1
	fi

	echo "jail-exec: ok (policy=$JAIL_POLICY, writes confined, reads unrestricted)"
	exit 0
	;;
"")
	echo "usage: jail-exec.sh <command> [args...]" >&2
	echo "       jail-exec.sh --check | --show | --print-profile" >&2
	exit 127
	;;
esac

case "$(uname -s)" in
Darwin)
	command -v sandbox-exec >/dev/null 2>&1 || {
		echo "jail-exec: sandbox-exec not found" >&2
		exit 126
	}
	profile="$(mktemp -t jail-exec)"
	trap 'rm -f "$profile"' EXIT
	jail_emit_seatbelt >"$profile"
	exec sandbox-exec -f "$profile" "$@"
	;;
Linux)
	command -v bwrap >/dev/null 2>&1 || {
		echo "jail-exec: bwrap not found (apt/dnf install bubblewrap)" >&2
		exit 126
	}
	read -r -a bwrap_args <<<"$(jail_bwrap_args)"
	exec bwrap "${bwrap_args[@]}" -- "$@"
	;;
*)
	echo "jail-exec: no sandbox backend for $(uname -s)" >&2
	exit 126
	;;
esac
