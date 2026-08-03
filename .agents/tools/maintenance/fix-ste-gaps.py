#!/usr/bin/env python3
"""Fix STE-Code content gaps — target specific rule files with missing content.

Usage: python3 .agents/tools/maintenance/fix-ste-gaps.py [--agent hermes|claude|codex] [--dry-run]
"""

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

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402

CFG = _load_config(__file__)
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

ADAPTED_DIR = PROJECT / "ste-code" / "adapted"


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    target = (
        sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None
    )
    dry_run = "--dry-run" in sys.argv

    if not target:
        print("Usage: fix-ste-gaps.py <secN-ruleY.Z>")
        sys.exit(1)

    adapted_file = ADAPTED_DIR / f"a-{target}.md"
    if not adapted_file.exists():
        print(f"ERROR: {adapted_file} not found")
        sys.exit(1)

    if dry_run:
        print(f"Would fill gaps in {adapted_file}")
        return

    prompt = f"""You are STE-Code. Fill content gaps in this file:
  {adapted_file}

Read the file. Look for:
1. Missing Non-STE/STE example pairs — generate complete pairs
2. Truncated sections — complete them
3. Placeholder text — replace with real content

Fix all gaps. Report changes made.
"""
    result = run_agent(prompt, agent=agent, model=CFG.model, cwd=PROJECT)
    print(f"Exit: {result.returncode}")


if __name__ == "__main__":
    main()
