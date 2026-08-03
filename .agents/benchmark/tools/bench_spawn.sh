#!/usr/bin/env bash
# bench_spawn.sh - launch ONE contained mini-session for the benchmark.
#
# This is the single choke point through which the benchmark-ste-code profile
# spawns its child "generate / debug / penetrate" sessions. Isolation is carried
# by the ENVIRONMENT, never by the prompt:
#
#   HERMES_HOME=~/.hermes/profiles/benchmark-ste-code
#       -> the child loads the benchmark-ste-code profile config, where the
#          ste-code-jail plugin (now with read-gating + neutral refusals) is
#          enabled. The child therefore runs jailed and blind, with no mention
#          of the jail anywhere in its prompt.
#   STE_CODE_JAIL_POLICY=bench
#       -> force the policy even if the child somehow resolved a different
#          profile, so a spawned session can never widen its own cage.
#   HERMES_PROFILE=benchmark-ste-code
#       -> matches jail-exec-wrap's force-pin so delegated grandchildren inherit
#          the same policy.
#
# The prompt file is read verbatim and passed as a vanilla oneshot (-z). It must
# NOT contain jail / policy / root language - the orchestrator composes it from
# the bare task only. Output lands in the benchmark tree, which is the only
# writable root the child has.
#
# Usage:
#   bench_spawn.sh <stage> <prompt-file> [run-name]
#     stage      : generate | debug | penetrate | <any>
#     prompt-file: path to a file holding the vanilla prompt
#     run-name   : subdirectory under .agents/benchmark/tests (default: auto-ts)
set -euo pipefail

STAGE="${1:?usage: bench_spawn.sh <stage> <prompt-file> [run-name]}"
PROMPT_FILE="${2:?usage: bench_spawn.sh <stage> <prompt-file> [run-name]}"
RUN="${3:-run-$(date +%Y%m%dT%H%M%S)}"

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd -P)"
OUT_DIR="$REPO_ROOT/.agents/benchmark/tests/$RUN/$STAGE"
mkdir -p "$OUT_DIR"

BENCH_HOME="$HOME/.hermes/profiles/benchmark-ste-code"

if [ ! -f "$PROMPT_FILE" ]; then
	echo "bench_spawn: prompt file not found: $PROMPT_FILE" >&2
	exit 2
fi

# Launch the contained mini-session. Isolation is in the env, not the prompt.
# Output is written by the child itself to OUT_DIR/out.txt (the prompt tells it
# where); we also tee the session log here for the operator.
HERMES_HOME="$BENCH_HOME" \
	STE_CODE_JAIL_POLICY=bench \
	HERMES_PROFILE=benchmark-ste-code \
	hermes -z "$(cat "$PROMPT_FILE")" --cli --yolo \
	>"$OUT_DIR/session.log" 2>&1

echo "$OUT_DIR"
