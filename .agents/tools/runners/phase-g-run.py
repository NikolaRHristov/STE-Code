#!/usr/bin/env python3
"""Phase G Runner — finalize the enriched STE-Code standard (single combined step).

Delegates to .agents/tools/finalize/finalize_batch.py, which regenerates the
enriched standard into ste-code/final/ (cross-references, traceability, example
completeness) in ONE step, superseding the old three-pass expansion/enrich pipeline.
Optional gated LLM polish available via --polish.

Phase F (artifacts) is a SEPARATE step that assembles deliverables FROM ste-code/final/.

Usage:
  python3 phase-g-run.py                # enrich + verify
  python3 phase-g-run.py --polish       # also run gated LLM polish
  python3 phase-g-run.py --enrich-only
  python3 phase-g-run.py --verify       # run verify_final.py only
"""
import os
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
FINALIZE = PROJECT / ".agents" / "tools" / "finalize" / "finalize_batch.py"
VERIFY = PROJECT / ".agents" / "tools" / "finalize" / "verify_final.py"
VENV = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")


def main():
    args = sys.argv[1:]
    if "--verify" in args:
        os.execv(VENV, [VENV, str(VERIFY)])
        return
    cmd = [VENV, str(FINALIZE), *args]
    env = {**os.environ, "STE_MODEL": os.environ.get("STE_MODEL", "tencent/hy3:free")}
    sys.stdout.write("Phase G (finalize) — single combined enrichment step.\n"
                     "Launching: " + " ".join(cmd) + "\n")
    sys.stdout.flush()
    os.execvpe(VENV, cmd, env)


if __name__ == "__main__":
    main()
