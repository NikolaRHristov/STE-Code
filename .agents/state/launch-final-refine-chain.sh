#!/bin/bash
# Launch the final re-refinement chain (batches 31-36) only when the number of
# concurrent LLM workers drops below 3 — the free tier 429s above that.
# Poll, never block: this script itself runs in the background.
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT" || exit 1

while true; do
  # Count live parent chains from the earlier wave.
  alive=0
  for pid in 7516 7570 7577; do
    kill -0 "$pid" 2>/dev/null && alive=$((alive+1))
  done
  if [ "$alive" -lt 3 ]; then
    echo "[$(date +%H:%M:%S)] slot free (chains alive=$alive) — launching batches 31-36"
    STE_MODEL=tencent/hy3:free exec python3 .agents/tools/refinement/refine_batch.py 31 6 2>&1
  fi
  echo "[$(date +%H:%M:%S)] waiting — chains alive=$alive"
  sleep 30
done
