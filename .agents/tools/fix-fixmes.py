#!/usr/bin/env python3
"""Fix remaining FIXME markers by generating missing STE corrections.

Targets 4 files with 34 FIXME content gaps. Launches one oneshot worker
per file to read the file, generate STE corrections for all FIXMEs, and apply.

Usage: python3 .agents/tools/fix-fixmes.py [--dry-run]
"""

import os, sys, subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"
TMP_DIR = PROJECT / ".agents" / "tmp" / "fixme"

FILES_WITH_FIXMES = [
    "ste-code/adapted/a-sec6-rule6.4.md",   # 15 FIXMEs
    "ste-code/adapted/a-sec6-rule6.5.md",   # 7 FIXMEs
    "ste-code/adapted/a-sec4-rule4.4.md",   # 7 FIXMEs
    "ste-code/adapted/a-sec4-rule4.5.md",   # 1 FIXME
]


def build_worker_prompt(relpath):
    abspath = PROJECT / relpath
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
    dry_run = "--dry-run" in sys.argv
    os.makedirs(TMP_DIR, exist_ok=True)

    if dry_run:
        print(f"Would process {len(FILES_WITH_FIXMES)} files:")
        for f in FILES_WITH_FIXMES:
            print(f"  {f}")
        return

    processes = []
    for relpath in FILES_WITH_FIXMES:
        prompt = build_worker_prompt(relpath)
        prompt_file = TMP_DIR / f"prompt-{Path(relpath).stem}.txt"
        prompt_file.write_text(prompt)

        proc = subprocess.Popen(
            [VENV_PYTHON, str(WRAPPER), str(prompt_file),
             "--model", "deepseek-v4-pro"],
            cwd=str(PROJECT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**os.environ, "HERMES_REASONING_EFFORT": "high"},
        )
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
