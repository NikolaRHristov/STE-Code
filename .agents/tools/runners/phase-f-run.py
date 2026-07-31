#!/usr/bin/env python3
"""Phase F Runner — final artifact generation worker.

Usage: python3 .agents/tools/runners/phase-f-run.py [--agent hermes|claude|codex]
"""

import os, sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
ARTIFACTS_DIR = PROJECT / "ste-code" / "artifacts"

import sys as _sys
_sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import Templater
TPL = Templater(__file__)


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    prompt = TPL.render("phase-f-worker",
                        adapted_dir=ADAPTED_DIR,
                        artifacts_dir=ARTIFACTS_DIR)

    tmp = PROJECT / ".agents" / "tmp" / "phase-f-prompt.txt"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(prompt)

    cmd, env = get_agent_command(agent=agent, model=os.environ.get("STE_MODEL", "tencent/hy3:free"),
                                  cwd=PROJECT, prompt_file=tmp)
    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    main()
