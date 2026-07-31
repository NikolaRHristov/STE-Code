#!/usr/bin/env python3
"""Phase B1 Runner — continuation refinement worker.

Usage: python3 .agents/tools/phase-b1-run.py [--agent hermes|claude|codex]
"""

import os, sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    prompt = """You are STE-Code Continuation Refinement Worker (Phase B1).
Continue refining extracted text from where previous workers left off.
"""

    tmp = PROJECT / ".agents" / "tmp" / "phase-b1-prompt.txt"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(prompt)

    cmd, env = get_agent_command(agent=agent, model="poolside/laguna-s-2.1:free",
                                  cwd=PROJECT, prompt_file=tmp)
    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    main()
