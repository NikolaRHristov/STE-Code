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

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
from ste_paths import venv_python  # noqa: E402

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402
CFG = _load_config(__file__)
ARTIFACT_BATCH = PROJECT / ".agents" / "tools" / "artifacts" / "artifact_batch.py"
VENV = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")


def main():
    args = sys.argv[1:]
    cmd = [VENV, str(ARTIFACT_BATCH), *args]
    env = {**os.environ, "STE_MODEL": CFG.model}
    sys.stdout.write("Phase F (artifacts) is assembled by artifact_batch.py.\n"
                     "Launching: " + " ".join(cmd) + "\n")
    sys.stdout.flush()
    os.execvpe(VENV, cmd, env)


if __name__ == "__main__":
    main()
