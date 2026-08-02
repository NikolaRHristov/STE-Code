#!/usr/bin/env python3
"""Markdown format checker — validates formatting consistency in adapted files.

Checks for: trailing whitespace, headings without space after #, missing blank lines before headings,
table column count consistency.

Usage: python3 .agents/tools/quality/_check_md.py [relative-path-from-project-root]
"""
import sys
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)

target = sys.argv[1] if len(sys.argv) > 1 else "ste-code/adapted/a-categories.md"
filepath = PROJECT / target

with open(filepath, 'r') as f:
    lines = f.readlines()

issues = []
for i, line in enumerate(lines, 1):
    # Check trailing whitespace
    if line.rstrip('\n\r') != line.rstrip():
        issues.append(f'Line {i}: trailing whitespace')
    
    # Check headings without space after #
    stripped = line.strip()
    for level in range(2, 5):
        prefix = '#' * level
        if stripped.startswith(prefix) and not stripped.startswith(prefix + ' '):
            issues.append(f'Line {i}: heading without space: "{stripped[:30]}"')

# Check blank lines before headings
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped.startswith('##') and stripped.startswith('## ') and i > 1:
        prev = lines[i-2].strip()
        if prev and prev != '---':
            # previous line is not blank and is not a horizontal rule
            pass  # Need to check if previous is blank
    if (stripped.startswith('## ') or stripped.startswith('### ') or stripped.startswith('#### ')) and i > 1:
        prev_line = lines[i-2].rstrip('\n\r')
        if prev_line and prev_line != '---':
            issues.append(f'Line {i}: missing blank line before heading "{stripped[:40]}" (prev: "{prev_line[:40]}")')

# Check pipe tables for column count consistency
in_table = False
header_cols = 0
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped.startswith('|') and '|' in stripped[1:]:
        cols = [c for c in stripped.split('|') if c]
        if not in_table:
            in_table = True
            header_cols = len(cols)
        else:
            if cols and len(cols) != header_cols:
                issues.append(f'Line {i}: table column count mismatch (expected {header_cols}, got {len(cols)})')
    else:
        if in_table and not stripped:
            in_table = False

if issues:
    for issue in issues:
        print(issue)
else:
    print('No issues found')
