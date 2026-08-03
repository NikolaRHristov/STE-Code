#!/usr/bin/env python3
"""Phase A Runner — launches extraction workers for spec pages.
Pattern from benchmark orchestrator: fork + exec via agent-runner.

Usage: python3 .agents/tools/runners/phase-a-run.py [--agent hermes|claude|codex]
"""

import os, sys
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
from ste_io import write_text, mkdir  # noqa: E402

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402

CFG = _load_config(__file__)
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

import sys as _sys

_sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import Templater

TPL = Templater(__file__)


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    # Build worker prompt for extraction phase (externalized in templates/)
    prompt = TPL.render("phase-a-worker")

    tmp = PROJECT / ".agents" / "tmp" / "phase-a-prompt.txt"
    mkdir(tmp.parent)
    write_text(tmp, prompt)

    cmd, env = get_agent_command(
        agent=agent, model=CFG.model, cwd=PROJECT, prompt_file=tmp
    )
    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    main()
