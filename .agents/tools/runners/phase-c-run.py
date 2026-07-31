#!/usr/bin/env python3
"""Phase C Runner — merge worker for refined text.

Usage: python3 .agents/tools/runners/phase-c-run.py [--agent hermes|claude|codex]
"""

import os, sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

REFINED_DIR = PROJECT / "ste-code" / "refined"
MERGED_DIR = PROJECT / "ste-code" / "merged"


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    prompt = f"""You are STE-Code Merge Worker (Phase C).
Read all refined files from {REFINED_DIR}, merge into master document.
Save to {MERGED_DIR}/master.md.
"""

    tmp = PROJECT / ".agents" / "tmp" / "phase-c-prompt.txt"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(prompt)

    cmd, env = get_agent_command(agent=agent, model="poolside/laguna-s-2.1:free",
                                  cwd=PROJECT, prompt_file=tmp)
    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    main()
