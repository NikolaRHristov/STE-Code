#!/usr/bin/env python3
"""Phase E Runner — STE-Code gap-fill extensions (orchestrated, markdown-first).

Delegates to .agents/tools/extension/extend_batch.py, which launches LLM workers
that emit MARKDOWN (ste-code/extensions/<area>.md), derives JSON deterministically
via md_to_json.py, and commits each area only after verify_extensions.py passes.

Legacy one-shot CLI (--agent, --model) accepted as informational no-ops. The real
pipeline is extend_batch.py.

Usage:
  python3 phase-e-run.py                 # all six gap areas
  python3 phase-e-run.py verbs          # one area
  python3 phase-e-run.py --resume       # skip passed areas
  python3 phase-e-run.py --verify       # run verify_extensions.py only
"""

import os
import sys
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path

_R = next(
    p
    for p in _Path(__file__).resolve().parents
    if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
from ste_paths import venv_python  # noqa: E402

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402

CFG = _load_config(__file__)
EXT_BATCH = PROJECT / ".agents" / "tools" / "extension" / "extend_batch.py"
VERIFY = PROJECT / ".agents" / "tools" / "extension" / "verify_extensions.py"
VENV = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")


def main():
    args = sys.argv[1:]
    if "--verify" in args:
        os.execv(VENV, [VENV, str(VERIFY)])
        return
    cmd = [VENV, str(EXT_BATCH), *args]
    env = {**os.environ, "STE_MODEL": CFG.model}
    sys.stdout.write(
        "Phase E (extensions) is orchestrated by extend_batch.py.\n"
        "Launching: " + " ".join(cmd) + "\n"
    )
    sys.stdout.flush()
    os.execvpe(VENV, cmd, env)


if __name__ == "__main__":
    main()
