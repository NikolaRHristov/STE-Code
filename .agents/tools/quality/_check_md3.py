#!/usr/bin/env python3
"""Markdown formatting checker — trailing whitespace, headings, tables.

Usage: python3 .agents/tools/quality/_check_md3.py [filepath]
  Default: ste-code/adapted/a-categories.md
"""

import sys
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path

_R = next(
    p
    for p in _Path(__file__).resolve().parents
    if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
target = sys.argv[1] if len(sys.argv) > 1 else "ste-code/adapted/a-categories.md"
filepath = PROJECT / target

with open(filepath, "r") as f:
    lines = f.readlines()

issues = []

# 1. Check trailing whitespace
for i, line in enumerate(lines, 1):
    if line.rstrip("\n\r") != line.rstrip():
        issues.append(f"Line {i}: trailing whitespace: {repr(line[-10:])}")

# 2. Check headings without space
for i, line in enumerate(lines, 1):
    s = line.strip()
    if s.startswith("#"):
        # Find where hashes end
        j = 0
        while j < len(s) and s[j] == "#":
            j += 1
        if j > 0 and j < len(s) and s[j] != " ":
            issues.append(f'Line {i}: heading without space after #: "{s[:40]}"')

# 3. Check missing blank lines before headings
for i, line in enumerate(lines, 1):
    s = line.strip()
    if s.startswith("## ") or s.startswith("### ") or s.startswith("#### "):
        if i > 1:
            prev = lines[i - 2].strip()
            if prev and prev != "---":
                issues.append(
                    f'Line {i}: missing blank line before heading (prev non-empty: "{prev[:40]}")'
                )

# 4. Check pipe tables for column consistency
in_table = False
header_cols = 0
table_start = 0
for i, line in enumerate(lines, 1):
    s = line.strip()
    cols = [c.strip() for c in s.split("|")]
    # Remove empty strings at start/end
    if cols and cols[0] == "":
        cols = cols[1:]
    if cols and cols[-1] == "":
        cols = cols[:-1]

    if s.startswith("|"):
        if not in_table:
            in_table = True
            header_cols = len(cols)
            table_start = i
        elif s.startswith("|---") or s.startswith("|:--"):
            # separator row - check it matches header
            if len(cols) != header_cols:
                issues.append(
                    f"Line {i}: separator column count ({len(cols)}) != header ({header_cols})"
                )
        else:
            if len(cols) != header_cols:
                issues.append(
                    f"Line {i}: row column count ({len(cols)}) != header ({header_cols}) at table starting line {table_start}"
                )
    else:
        if in_table:
            in_table = False

if issues:
    for issue in issues:
        print(issue)
else:
    print("No markdown formatting issues found")
