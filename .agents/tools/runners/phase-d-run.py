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

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
ADAPT_BATCH = PROJECT / ".agents" / "tools" / "adaptation" / "adapt_batch.py"
VERIFY = PROJECT / ".agents" / "tools" / "adaptation" / "verify-adaptation.py"
VENV = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")


def main():
    args = sys.argv[1:]
    if "--verify" in args:
        os.execv(VENV, [VENV, str(VERIFY)])
        return

    cmd = [VENV, str(ADAPT_BATCH), *args]
    env = {**os.environ, "STE_MODEL": os.environ.get("STE_MODEL", "tencent/hy3:free")}
    sys.stdout.write(
        "Phase D (adaptation) is orchestrated by adapt_batch.py.\n"
        "Launching: " + " ".join(cmd) + "\n"
    )
    sys.stdout.flush()
    os.execvpe(VENV, cmd, env)


if __name__ == "__main__":
    main()
