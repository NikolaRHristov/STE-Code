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


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    prompt = f"""You are STE-Code Artifact Generator (Phase F).
Read all adapted rule files from {ADAPTED_DIR}.
Generate final deployable artifacts.
Save to {ARTIFACTS_DIR}/.
"""

    tmp = PROJECT / ".agents" / "tmp" / "phase-f-prompt.txt"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(prompt)

    cmd, env = get_agent_command(agent=agent, model=os.environ.get("STE_MODEL", "tencent/hy3:free"),
                                  cwd=PROJECT, prompt_file=tmp)
    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    main()
