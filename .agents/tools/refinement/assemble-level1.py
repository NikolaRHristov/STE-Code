#!/usr/bin/env python3
"""Level 1 Assembly — compress Level 2 into a ~1.2K token ultra-compact prompt.

Reads Level 2 system-prompt, produces the lightest-weight prompt suitable for
interactive sessions and low-context scenarios.

Usage: python3 .agents/tools/refinement/assemble-level1.py [--agent hermes|claude|codex] [--dry-run]
Output: ste-code/artifacts/level1/system-prompt.txt (~1.2K tokens)
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
from ste_io import mkdir  # noqa: E402

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402

CFG = _load_config(__file__)
# Make .agents/tools/lib/ importable as a flat namespace (templater,
# skill_prompt, agent_runner, ...). See .agents/tools/lib/templater.py.
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import lib_import, Templater

_ar = lib_import("agent_runner")
run_agent = _ar.run_agent
TPL = Templater(__file__)

LEVEL2_INPUT = PROJECT / "ste-code" / "artifacts" / "level2" / "system-prompt.txt"
LEVEL1_DIR = PROJECT / "ste-code" / "artifacts" / "level1"
OUTPUT = LEVEL1_DIR / "system-prompt.txt"


def build_prompt():
    level2_text = LEVEL2_INPUT.read_text()
    return TPL.render("level1-worker", level2_text=level2_text, OUTPUT=str(OUTPUT))


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    dry_run = "--dry-run" in sys.argv

    if not LEVEL2_INPUT.exists():
        print(f"ERROR: Level 2 input not found: {LEVEL2_INPUT}")
        print("Run assemble-level2.py first.")
        sys.exit(1)

    prompt = build_prompt()
    print(f"Level 1 prompt: {len(prompt)} chars (~{len(prompt) // 4} tokens)")

    if dry_run:
        print(f"\nWould compress {LEVEL2_INPUT} → {OUTPUT}")
        return

    mkdir(LEVEL1_DIR)
    result = run_agent(prompt, agent=agent, model=CFG.model, cwd=PROJECT)
    print(f"Exit: {result.returncode}")

    if OUTPUT.exists():
        chars = OUTPUT.stat().st_size
        print(f"Output: {chars:,} chars (~{chars // 4:,} tokens)")
    else:
        print("Output file not created!")


if __name__ == "__main__":
    main()
