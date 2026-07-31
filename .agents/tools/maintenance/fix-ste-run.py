#!/usr/bin/env python3
"""Fix STE-Code compliance issues across adapted files.

Usage: python3 .agents/tools/maintenance/fix-ste-run.py [--agent hermes|claude|codex] [--dry-run]
"""

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

ADAPTED_DIR = PROJECT / "ste-code" / "adapted"


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    target = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None
    dry_run = "--dry-run" in sys.argv

    if not target:
        print("Usage: fix-ste-run.py <secN-ruleY.Z>")
        print("       fix-ste-run.py --all")
        sys.exit(1)

    if target == "--all":
        files = sorted(ADAPTED_DIR.glob("a-sec*.md"))
        print(f"Would process {len(files)} files")
        if dry_run:
            return
        # Process all in sequence (could be parallelized)
        for f in files:
            rule = f.stem.replace("a-", "")
            print(f"Processing {rule}...")
            # Launch worker per file
    else:
        adapted_file = ADAPTED_DIR / f"a-{target}.md"
        if not adapted_file.exists():
            print(f"ERROR: {adapted_file} not found")
            sys.exit(1)

        if dry_run:
            print(f"Would fix {adapted_file}")
            return

        prompt = f"""You are STE-Code. Fix STE compliance issues in this file:
  {adapted_file}

Check for:
1. Unapproved synonyms — replace with approved alternatives
2. Passive voice — rewrite as active
3. Semicolons — split into separate sentences
4. Overlong sentences — break into shorter ones
5. Missing rule references

Fix all issues. Report changes made.
"""
        result = run_agent(prompt, agent=agent, model="poolside/laguna-s-2.1:free", cwd=PROJECT)
        print(f"Exit: {result.returncode}")


if __name__ == "__main__":
    main()
