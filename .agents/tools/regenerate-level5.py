#!/usr/bin/env python3
"""Regenerate all Level 5 summaries — re-reads 51 rule adaptation files, produces fresh summaries.

Usage: python3 .agents/tools/regenerate-level5.py [--agent hermes|claude|codex] [--dry-run]
"""

import os, sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
LEVEL5_DIR = PROJECT / "ste-code" / "artifacts" / "level5"


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    dry_run = "--dry-run" in sys.argv
    rule = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None

    if not rule or dry_run:
        files = sorted(ADAPTED_DIR.glob("a-sec*.md"))
        secs = set()
        for f in files:
            secs.add(f.stem.replace("a-", ""))
        print(f"Rules to regenerate: {len(files)} in {len(secs)} sections")
        if dry_run:
            return
        sys.exit(0)

    # Single-rule mode: self-exec into agent
    adapted_file = ADAPTED_DIR / f"a-{rule}.md"
    if not adapted_file.exists():
        print(f"ERROR: Adapted file not found: {adapted_file}")
        sys.exit(1)

    section = rule.split("-")[0]
    out_dir = LEVEL5_DIR / section / f"a-{rule}"
    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / "summary.md"

    prompt = f"""You are STE-Code. Produce a Level 5 summary for Rule {rule}.

Read the full adapted rule at: {adapted_file}

Produce a compact summary with:
1. Rule number and title
2. What the rule requires (1 sentence)
3. One complete Non-STE/STE example pair
4. Key vocabulary notes

Save to: {output}

Use write_file. Report: rule number, estimated tokens.
"""

    tmp = PROJECT / ".agents" / "tmp" / f"regen-{rule}.txt"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(prompt)

    cmd, env = get_agent_command(agent=agent, model="deepseek-v4-pro",
                                  cwd=PROJECT, prompt_file=tmp)
    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    main()
