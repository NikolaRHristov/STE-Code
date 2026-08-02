#!/usr/bin/env python3
"""Fix STE-Code compliance issues across adapted files.

Usage: python3 .agents/tools/maintenance/fix-ste-run.py [--agent hermes|claude|codex] [--dry-run]
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
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

import sys as _sys
_sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import Templater
TPL = Templater(__file__)

ADAPTED_DIR = PROJECT / "ste-code" / "adapted"


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    target = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None
    dry_run = "--dry-run" in sys.argv

    if not target:
        print("Usage: fix-ste-run.py <secN-ruleY.Z>")
        print("       fix-ste-run.py --all")
        sys.exit(1)

    if target == "--all":
        files = sorted(ADAPTED_DIR.glob("a-sec*.md"))
        print(f"Would process {len(files)} files")
        if dry_run:
            return
        # Process all in sequence (could be parallelized)
        for f in files:
            rule = f.stem.replace("a-", "")
            print(f"Processing {rule}...")
            # Launch worker per file
    else:
        adapted_file = ADAPTED_DIR / f"a-{target}.md"
        if not adapted_file.exists():
            print(f"ERROR: {adapted_file} not found")
            sys.exit(1)

        if dry_run:
            print(f"Would fix {adapted_file}")
            return

        prompt = TPL.render("fix-ste-worker", adapted_file=adapted_file)
        result = run_agent(prompt, agent=agent, model=CFG.model, cwd=PROJECT)
        print(f"Exit: {result.returncode}")


if __name__ == "__main__":
    main()
