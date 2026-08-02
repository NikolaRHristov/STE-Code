#!/usr/bin/env python3
"""Phase D Runner — STE→STE-Code adaptation (orchestrated).

Delegates to .agents/tools/adaptation/adapt_batch.py, which launches one
adaptation worker per rule section (1-9 + GR), embeds the adaptation SKILL.md,
and commits each section only after its deterministic verification gate passes.

This runner keeps the legacy one-shot CLI (`--agent`, `--model`) for ad-hoc
single-worker use, but the real pipeline is adapt_batch.py. `--agent`/`--model`
are accepted and forwarded as informational no-ops (model also via STE_MODEL).

Usage:
  python3 phase-d-run.py                      # run full orchestrated adaptation
  python3 phase-d-run.py --resume             # resume from checkpoint
  python3 phase-d-run.py 3 1                  # only section 3
  python3 phase-d-run.py --verify             # run verify-adaptation.py only
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
ADAPT_BATCH = PROJECT / ".agents" / "tools" / "adaptation" / "adapt_batch.py"
VERIFY = PROJECT / ".agents" / "tools" / "adaptation" / "verify-adaptation.py"
VENV = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")


def main():
    args = sys.argv[1:]
    if "--verify" in args:
        os.execv(VENV, [VENV, str(VERIFY)])
        return

    cmd = [VENV, str(ADAPT_BATCH), *args]
    env = {**os.environ, "STE_MODEL": CFG.model}
    sys.stdout.write(
        "Phase D (adaptation) is orchestrated by adapt_batch.py.\n"
        "Launching: " + " ".join(cmd) + "\n"
    )
    sys.stdout.flush()
    os.execvpe(VENV, cmd, env)


if __name__ == "__main__":
    main()
