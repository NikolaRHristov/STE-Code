#!/usr/bin/env python3
"""Phase F Runner — final artifact assembly (orchestrated).

Delegates to .agents/tools/artifacts/artifact_batch.py, which deterministically
consolidates ste-code/adapted/ into the canonical deliverables
(ste-code-rules.md + ste-code-system-prompt.md) and verifies rule coverage.

Legacy one-shot CLI (`--agent`, `--model`) is accepted and forwarded as
informational no-ops; the real pipeline is artifact_batch.py.

Usage:
  python3 phase-f-run.py                 # assemble artifacts
  python3 phase-f-run.py --dry-run       # plan only
  python3 phase-f-run.py --verify        # run verify-artifacts.py only
"""
import os
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
ARTIFACT_BATCH = PROJECT / ".agents" / "tools" / "artifacts" / "artifact_batch.py"
VENV = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")


def main():
    args = sys.argv[1:]
    cmd = [VENV, str(ARTIFACT_BATCH), *args]
    env = {**os.environ, "STE_MODEL": os.environ.get("STE_MODEL", "tencent/hy3:free")}
    sys.stdout.write("Phase F (artifacts) is assembled by artifact_batch.py.\n"
                     "Launching: " + " ".join(cmd) + "\n")
    sys.stdout.flush()
    os.execvpe(VENV, cmd, env)


if __name__ == "__main__":
    main()
