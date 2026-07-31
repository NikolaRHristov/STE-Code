#!/usr/bin/env python3
"""Phase B Runner — refinement workers for extracted text.
Self-execs into agent to process refinement batch.

Usage: python3 .agents/tools/runners/phase-b-run.py [--agent hermes|claude|codex] [batch_num]
"""

import os, sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

import sys as _sys
_sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import Templater
TPL = Templater(__file__)

EXTRACTED_DIR = PROJECT / "ste-code" / "extracted"
REFINED_DIR = PROJECT / "ste-code" / "refined"


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    batch = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "1"

    prompt = TPL.render("phase-b-worker",
                        batch=batch,
                        extracted_dir=EXTRACTED_DIR,
                        refined_dir=REFINED_DIR)

    tmp = PROJECT / ".agents" / "tmp" / f"phase-b-{batch}.txt"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(prompt)

    cmd, env = get_agent_command(agent=agent, model=os.environ.get("STE_MODEL", "tencent/hy3:free"),
                                  cwd=PROJECT, prompt_file=tmp)
    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    main()
