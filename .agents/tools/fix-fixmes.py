#!/usr/bin/env python3
"""Fix remaining FIXME markers by generating missing STE corrections.

Targets files with FIXME content gaps. Launches parallel agent workers
to read each file, generate STE corrections for all FIXMEs, and apply them.

Usage: python3 .agents/tools/fix-fixmes.py [--agent hermes|claude|codex] [--dry-run]
"""

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

TMP_DIR = PROJECT / ".agents" / "tmp" / "fixme"

# Files known to have FIXME markers — edit this list as needed
FILES_WITH_FIXMES = [
    "ste-code/adapted/a-sec6-rule6.4.md",
    "ste-code/adapted/a-sec6-rule6.5.md",
    "ste-code/adapted/a-sec4-rule4.4.md",
    "ste-code/adapted/a-sec4-rule4.5.md",
]


def build_worker_prompt(relpath):
    return f"""You are STE-Code. Fix all FIXME placeholder markers in this file:

FILE: {relpath}

Your task:
1. Read the file with read_file
2. Find all lines containing "[FIXME: generate STE correction for: ...]"
3. For each FIXME, the text after "generate STE correction for:" is the Non-STE
   text that needs an STE-compliant correction
4. Generate the correct STE version for each one following STE-Code rules:
   - Active voice, approved vocabulary, max 20/25 word sentences
   - No semicolons, no contractions, no -ing as verb
   - One topic per sentence, consistent terminology
5. Use patch to replace each "[FIXME: generate STE correction for: ...]"
   with the actual STE correction text

CRITICAL:
- Generate REAL STE corrections — do NOT just remove the FIXME marker
- Each STE correction must be a complete, grammatically correct sentence
- Follow the sentence length limits (20 procedural, 25 descriptive)
- Use approved vocabulary (prefer: use/start/stop/show/make/get/set/check/do)
- If the Non-STE text is truncated with "...", infer the full meaning from context

After fixing all FIXMEs, report: how many FIXMEs were found and fixed.
Save the report to: {TMP_DIR}/{Path(relpath).stem}-fixme-report.md
"""


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    dry_run = "--dry-run" in sys.argv
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    if dry_run:
        print(f"Would process {len(FILES_WITH_FIXMES)} files:")
        for f in FILES_WITH_FIXMES:
            print(f"  {f}")
        return

    processes = []
    for relpath in FILES_WITH_FIXMES:
        prompt = build_worker_prompt(relpath)
        proc = launch_agent(prompt, agent=agent, model="deepseek-v4-pro", cwd=PROJECT)
        processes.append((relpath, proc))
        print(f"Launched: {relpath} (PID {proc.pid})")

    print(f"\nWaiting for {len(processes)} workers...")
    for relpath, proc in processes:
        stdout, stderr = proc.communicate(timeout=600)
        status = "OK" if proc.returncode == 0 else f"FAIL ({proc.returncode})"
        print(f"{relpath}: {status}")

    # Verify — check remaining FIXMEs
    print("\n=== POST-FIX CHECK ===")
    for relpath in FILES_WITH_FIXMES:
        abspath = PROJECT / relpath
        if abspath.exists():
            count = abspath.read_text().count("[FIXME:")
            print(f"  {relpath}: {count} FIXME(s) remaining")


if __name__ == "__main__":
    main()
