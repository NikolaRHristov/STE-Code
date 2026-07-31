#!/usr/bin/env python3
"""Phase D Runner — adaptation worker for STE→STE-Code transformation.

Usage: python3 .agents/tools/runners/phase-d-run.py [--agent hermes|claude|codex] [rule_id]
"""

import os, sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

MERGED_DIR = PROJECT / "ste-code" / "merged"
ADAPTED_DIR = PROJECT / "ste-code" / "adapted"


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    rule = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None

    prompt = f"""You are STE-Code Adaptation Worker (Phase D).
Read the merged master document at {MERGED_DIR}/master.md
{f'Adapt rule {rule}.' if rule else 'Adapt all rules from aerospace to code domain.'}
Save adapted rule files to {ADAPTED_DIR}/.
"""

    tmp = PROJECT / ".agents" / "tmp" / f"phase-d{'-'+rule if rule else ''}.txt"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(prompt)

    cmd, env = get_agent_command(agent=agent, model="poolside/laguna-s-2.1:free",
                                  cwd=PROJECT, prompt_file=tmp)
    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    main()
