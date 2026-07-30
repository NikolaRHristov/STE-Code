#!/usr/bin/env python3
"""Strip FIXME markers from STE-Code adapted files, keeping the actual STE content."""
import re
import sys

FILES = [
    "ste-code/adapted/a-sec2-rule2.2.md",
    "ste-code/adapted/a-sec4-rule4.1.md",
    "ste-code/adapted/a-sec4-rule4.2.md",
]

BASE = "/Volumes/CORSAIR/Developer/macOS/Application/Manual"

for relpath in FILES:
    path = f"{BASE}/{relpath}"
    with open(path, "r") as f:
        content = f.read()

    # Pattern: > **STE:** [FIXME: ...anything...]
    # Replace with: > **STE:**
    new_content = re.sub(
        r'> \*\*STE:\*\* \[FIXME:[^\]]*\]',
        r'> **STE:**',
        content
    )

    if new_content != content:
        with open(path, "w") as f:
            f.write(new_content)
        count = content.count("[FIXME:")
        print(f"FIXED: {relpath} — stripped {count} FIXME marker(s)")
    else:
        print(f"OK: {relpath} — no FIXME markers found")

print("Done.")
