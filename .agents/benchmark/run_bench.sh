#!/usr/bin/env bash
# run_bench.sh — launch the STE-Code adversarial benchmark under a bench-confined
# shell WITHOUT touching jail-lib.sh. See HANDOFF-bench-jail-mismatch.md.
#
# The kernel (Seatbelt) jail layer only allows `.agents/benchmark/tests/`, so the
# harness's py_compile cache writes next to source are denied. Routing __pycache__
# to a kernel-allowed dir (PYTHONPYCACHEPREFIX=/tmp/...) removes that denial.
#
# PROVEN GREEN inside the bench jail (bench session SELFTEST = 181/181 with this env).
set -euo pipefail

cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
export PYTHONPYCACHEPREFIX=/tmp/ste-bench-pycache
export PYTHONDONTWRITEBYTECODE=0

# Run under the bench jail (kernel layer). Adjust the policy env if your
# jail-exec wrapper differs.
exec env STE_CODE_JAIL_POLICY=bench \
  .agents/hermes/jail/scripts/jail-exec.sh /bin/sh -c \
  "STE_CODE_JAILED=1 exec python3 .agents/benchmark/run_pipeline.py $*"
