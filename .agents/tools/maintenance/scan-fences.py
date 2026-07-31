#!/usr/bin/env python3
"""Find nested code fence issues: triple-backtick fence inside another."""
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent

for f in sorted(PROJECT.rglob("*.md")):
    if ".git/" in str(f) or "spec/" in str(f) or "__pycache__" in str(f):
        continue
    try:
        lines = f.read_text().split("\n")
    except:
        continue

    stack = []  # (line_num, bt_count, indent)

    for i, line in enumerate(lines):
        s = line.strip()
        m = re.match(r"^(\s*)(`{3,})(\S*)$", s)
        if not m:
            continue

        indent = len(m.group(1))
        bt = len(m.group(2))
        lang = m.group(3)

        if not stack:
            stack.append((i + 1, bt, indent, lang))
        else:
            top_bt = stack[-1][1]
            top_indent = stack[-1][2]

            if bt >= top_bt and indent == top_indent and not lang:
                # Closing fence
                stack.pop()
            elif stack:
                # New fence inside another = nested
                print(f"NESTED: {f.relative_to(PROJECT)}:{i+1} BT={bt} lang='{lang}' inside BT={top_bt} at L{stack[-1][0]}")
                stack.append((i + 1, bt, indent, lang))
            else:
                stack.append((i + 1, bt, indent, lang))
