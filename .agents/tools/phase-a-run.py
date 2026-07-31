#!/usr/bin/env python3
"""Phase A Runner — launches extraction workers for spec pages.
Pattern from benchmark orchestrator: fork + exec via agent-runner.

Usage: python3 .agents/tools/phase-a-run.py [--agent hermes|claude|codex]
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

    # Build worker prompt for extraction phase
    prompt = """You are STE-Code Extraction Worker (Phase A).
Read spec pages and extract raw text into structured markdown.
Follow the extraction methodology in .agents/skills/spec-extraction/ste-code-workers/SKILL.md
"""

    tmp = PROJECT / ".agents" / "tmp" / "phase-a-prompt.txt"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(prompt)

    cmd, env = get_agent_command(agent=agent, model="poolside/laguna-s-2.1:free",
                                  cwd=PROJECT, prompt_file=tmp)
    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    main()
