#!/usr/bin/env bash
# launch-downstream.sh — run STE-Code stages C→D→E→F after refinement completes.
#
# Safe to run in a FRESH session once ste-code/refined/ is stable (refiner done).
# Each stage refuses to launch if its input isn't ready, so an early abort is a
# hard stop, not a silent failure. Nothing here touches ste-code/refined/ as input
# mutation — grouping only READS refined/, adaptation READS grouped/.
#
# Usage:
#   bash .agents/tools/runners/launch-downstream.sh          # full C→D→E→F
#   bash .agents/tools/runners/launch-downstream.sh --dry    # grouping dry-run only
#
# Model is read from STE_MODEL (default tencent/hy3:free).
set -u
REPO="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$REPO" || exit 1
RUN=".agents/tools/runners"
export STE_MODEL="${STE_MODEL:-tencent/hy3:free}"

echo "== STE-Code downstream launch =="
echo "Repo: $REPO"
echo "Model: $STE_MODEL"
echo "Refined files: $(ls ste-code/refined/*.md 2>/dev/null | wc -l)"

# 0) Safety: confirm refined/ looks complete before we build on it.
if [ "$(ls ste-code/refined/*.md 2>/dev/null | wc -l)" -lt 100 ]; then
  echo "ABORT: refined/ has <100 files; refiner may still be running. Wait."
  exit 2
fi

# 1) GROUPING (deterministic, pure Python) — reads refined/, writes grouped/.
echo; echo "== [C] Grouping =="
if [ "${1:-}" = "--dry" ]; then
  python3 "$RUN/phase-c-run.py" --dry-run
  echo "(dry-run only; exiting)"; exit 0
fi
python3 "$RUN/phase-c-run.py" --verify || { echo "GROUPING FAILED"; exit 3; }

# 2) ADAPTATION (LLM per-section, gated) — reads grouped/, writes adapted/.
echo; echo "== [D] Adaptation =="
python3 "$RUN/phase-d-run.py" || { echo "ADAPTATION FAILED"; exit 4; }

# 3) EXTENSION (LLM gap-fills, markdown-first, gated) — writes extensions/.
echo; echo "== [E] Extension =="
python3 "$RUN/phase-e-run.py" || { echo "EXTENSION FAILED"; exit 5; }

# 4) ARTIFACTS (deterministic assembly) — reads adapted/, writes artifacts/.
echo; echo "== [F] Artifacts =="
python3 "$RUN/phase-f-run.py" || { echo "ARTIFACTS FAILED"; exit 6; }

echo; echo "== DONE: grouped/ adapted/ extensions/ artifacts/ produced =="
echo "Verify: python3 .agents/tools/extension/verify_extensions.py"
