#!/usr/bin/env python3
"""Generate max-size system prompt from all Level 5 content.

Usage: python3 .agents/tools/generate-max-prompt.py [--agent hermes|claude|codex] [--dry-run]
"""

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

OUTPUT = PROJECT / "ste-code" / "artifacts" / "ste-code-level5-max.txt"


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print(f"Would generate {OUTPUT}")
        return

    prompt = f"""You are STE-Code. Generate the maximum-size system prompt from all
available STE-Code content. Read all files in:
  ste-code/adapted/
  ste-code/artifacts/level5/

Produce the most comprehensive prompt possible, including all rules,
all dictionary entries, all synonym pairs, and all example pairs.

Save to: {OUTPUT}
Use write_file. Report token count.
"""
    result = run_agent(prompt, agent=agent, model="poolside/laguna-s-2.1:free", cwd=PROJECT)
    print(f"Exit: {result.returncode}")
    if OUTPUT.exists():
        print(f"Output: {OUTPUT.stat().st_size:,} chars")


if __name__ == "__main__":
    main()
