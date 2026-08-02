#!/usr/bin/env python3
"""Phase B1 Runner — continuation / redo refinement (orchestrated).

Delegates to .agents/tools/continuation/continue_batch.py, which re-processes
specific refined pages from an explicit queue (produced by verify_continuation.py)
using a checkpoint + per-item git commit. B1 writes into ste-code/refined/, which
the Refinement agent also owns, so it REQUIRES an explicit --queue and must not
run while the Refinement agent is actively writing.

Usage:
  python3 phase-b1-run.py                         # prints usage (needs --queue)
  python3 phase-b1-run.py --queue Q.json [--resume]
  python3 phase-b1-run.py --scan                  # run verify_continuation.py
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
CONT_DIR = PROJECT / ".agents" / "tools" / "continuation"
CONTINUE_BATCH = CONT_DIR / "continue_batch.py"
VERIFY = CONT_DIR / "verify_continuation.py"
VENV = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")


def main():
    args = sys.argv[1:]
    if "--scan" in args:
        os.execv(VENV, [VENV, str(VERIFY)])
        return
    if not any(a.startswith("--queue") for a in args):
        sys.stdout.write(
            "Phase B1 (continuation) needs an explicit redo queue.\n"
            "  1) python3 phase-b1-run.py --scan          # build queue from refined/\n"
            "  2) review ste-code/extensions/.continue-queue.json\n"
            "  3) python3 phase-b1-run.py --queue <q>.json [--resume]\n"
            "Do NOT run while the Refinement agent is writing refined/.\n"
        )
        sys.exit(2)
    os.execv(VENV, [VENV, str(CONTINUE_BATCH), *args])


if __name__ == "__main__":
    main()
