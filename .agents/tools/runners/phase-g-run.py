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

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402
CFG = _load_config(__file__)
FINALIZE = PROJECT / ".agents" / "tools" / "finalize" / "finalize_batch.py"
VERIFY = PROJECT / ".agents" / "tools" / "finalize" / "verify_final.py"
VENV = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")


def main():
    args = sys.argv[1:]
    if "--verify" in args:
        os.execv(VENV, [VENV, str(VERIFY)])
        return
    cmd = [VENV, str(FINALIZE), *args]
    env = {**os.environ, "STE_MODEL": CFG.model}
    sys.stdout.write("Phase G (finalize) — single combined enrichment step.\n"
                     "Launching: " + " ".join(cmd) + "\n")
    sys.stdout.flush()
    os.execvpe(VENV, cmd, env)


if __name__ == "__main__":
    main()
