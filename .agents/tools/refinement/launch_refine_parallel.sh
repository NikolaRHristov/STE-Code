#!/usr/bin/env bash
# Launch all 37 refinement batches with LIMITED concurrency.
#
# Design (per user request: "parallel in groups of 2-3, 2-3 workers per batch"):
#   - Each BATCH = 1 invocation of refine_batch.py <b> 1  -> processes 3 workers
#     sequentially inside that process (the "2-3 workers per batch").
#   - BATCHES are launched in WAVES of $CONCURRENCY concurrent processes
#     (default 3) so we never blow the API rate limit (the earlier 36-at-once
#      run caused 429 + git collisions).
#   - Git commits are already serialized inside refine_batch.py via a lock, so
#     concurrent batches won't collide on git.
#   - The checkpoint (refine-checkpoint.json) records passes, so a re-run
#     skips already-refined workers.
#
# Usage:
#   bash .agents/tools/refinement/launch_refine_parallel.sh [concurrency] [start_batch] [end_batch]
# Defaults: concurrency=3, start=1, end=37
#
# MUST be run from the STE-Code repo root with the ste-code Hermes profile:
#   export HERMES_HOME=~/.hermes/profiles/ste-code
#   export STE_MODEL=tencent/hy3:free

set -u
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)" || exit 1

CONCURRENCY=${1:-3}
START=${2:-1}
END=${3:-37}

export HERMES_HOME="${HERMES_HOME:-$HOME/.hermes/profiles/ste-code}"
export STE_MODEL="${STE_MODEL:-tencent/hy3:free}"

echo "Refinement parallel launcher"
echo "  profile:    $HERMES_HOME"
echo "  model:      $STE_MODEL"
echo "  batches:    $START..$END"
echo "  concurrency:$CONCURRENCY batches at a time (3 workers each)"
echo

total=$(( END - START + 1 ))
wave=0
launched=0

run_one() {
  local b="$1"
  python3 .agents/tools/refinement/refine_batch.py "$b" 1 \
    > "/tmp/refine-b${b}.log" 2>&1
  echo "batch $b finished (exit $?)"
}

for (( b=START; b<=END; b++ )); do
  run_one "$b" &
  launched=$(( launched + 1 ))
  wave=$(( wave + 1 ))
  # When we've filled a wave, or this is the last batch, wait for the wave.
  if (( wave >= CONCURRENCY )) || (( b == END )); then
    wait
    echo "--- wave done (launched $launched / $total) ---"
    wave=0
  fi
done

wait
echo
echo "All refinement batches launched. Verify with:"
echo "  python3 -c \"import json;print(sum(1 for v in json.load(open('.agents/state/refine-checkpoint.json')).values() if False else json.load(open('.agents/state/refine-checkpoint.json')).values() if v.get('passed')))\""
echo "  (count of passed workers in refine-checkpoint.json should approach 109)"
