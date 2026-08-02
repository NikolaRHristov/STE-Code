#!/usr/bin/env python3
"""Populate Level 5 summaries for all 51 rules.

Reads adapted rule files, produces summary.md for each rule in the
level5 directory tree. Self-execs into agent for each rule.

Usage: python3 .agents/tools/refinement/populate-level5.py [--agent hermes|claude|codex] [--dry-run]
"""

import os, sys
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
from ste_io import write_text, mkdir  # noqa: E402

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402
CFG = _load_config(__file__)
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
LEVEL5_DIR = PROJECT / "ste-code" / "artifacts" / "level5"


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    dry_run = "--dry-run" in sys.argv

    if dry_run:
        files = sorted(ADAPTED_DIR.glob("a-sec*.md"))
        print(f"Would process {len(files)} adapted files")
        return

    # Single-rule mode: self-exec into agent for one rule
    rule = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None
    if not rule:
        print("Usage: populate-level5.py <rule>  (e.g., sec1-rule1.1)")
        sys.exit(1)

    adapted_file = ADAPTED_DIR / f"a-{rule}.md"
    if not adapted_file.exists():
        print(f"ERROR: {adapted_file} not found")
        sys.exit(1)

    section = rule.split("-")[0]
    out_dir = LEVEL5_DIR / section / f"a-{rule}"
    mkdir(out_dir)
    output = out_dir / "summary.md"

    prompt = f"""You are STE-Code. Read the adapted rule at:
  {adapted_file}

Produce a 3-5 sentence summary that captures:
1. Rule number and title
2. What the rule requires
3. One Non-STE/STE example pair

Save to: {output}
Use write_file.
"""

    tmp = PROJECT / ".agents" / "tmp" / f"pop-{rule}.txt"
    mkdir(tmp.parent)
    write_text(tmp, prompt)

    cmd, env = get_agent_command(agent=agent, model=CFG.model,
                                  cwd=PROJECT, prompt_file=tmp)
    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    main()
