#!/usr/bin/env python3
"""Fix empty STE lines — fill in missing STE corrections for orphan Non-STE examples."""

import os, sys, subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"

FILES = [
    "a-sec1-rule1.11.md", "a-sec1-rule1.8.md", "a-sec2-rule2.2.md",
    "a-sec3-rule3.1.md", "a-sec3-rule3.7.md", "a-sec4-rule4.1.md",
    "a-sec4-rule4.2.md", "a-sec4-rule4.4.md", "a-sec4-rule4.5.md",
    "a-sec5-rule5.5.md", "a-sec6-rule6.4.md", "a-sec6-rule6.5.md",
    "a-sec9-rule9.4.md",
]

for fname in FILES:
    f = PROJECT / "ste-code" / "adapted" / fname
    content = f.read_text()
    
    prompt = f"""You are STE-Code. Fix this rule file. Some Non-STE examples have empty STE corrections (just ">" with no content after "**STE:**").

For EVERY Non-STE example that has a missing or empty STE line, write the correct STE-Code compliant version. Follow the same style as the other complete pairs in the file.

Current file: ste-code/adapted/{fname}

{content}

## INSTRUCTIONS
1. Find all Non-STE examples with empty/missing STE corrections
2. Write the correct STE version for each one
3. Use the write_file tool to save the complete fixed file to: ste-code/adapted/{fname}
4. PRESERVE everything else exactly as-is. Only fill in the missing STE lines.
5. Report how many STE lines you fixed.
"""
    
    tmp = PROJECT / ".agents" / "tmp" / f"fix-ste-{fname.replace('.md', '')}.txt"
    tmp.write_text(prompt)
    
    print(f"Fixing {fname}...")
    result = subprocess.run(
        [VENV_PYTHON, str(WRAPPER), str(tmp), "--model", "deepseek-v4-pro"],
        cwd=str(PROJECT), capture_output=True, text=True, timeout=300,
        env={**os.environ, "HERMES_REASONING_EFFORT": "medium"},
    )
    print(f"  Exit: {result.returncode}")

print("\nDone fixing STE gaps.")
