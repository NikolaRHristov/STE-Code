#!/usr/bin/env python3
"""Quick markdown format checker — checks line 12 heading format.

Usage: python3 .agents/tools/quality/_check_md2.py [filepath]
  Default: ste-code/adapted/a-categories.md
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

# Just check line 12 specifically
line = lines[11]  # 0-indexed
print(f"Line 12 raw repr: {repr(line[:60])}")
stripped = line.strip()
print(f"Stripped repr: {repr(stripped[:60])}")
print(f"Starts with '###': {stripped.startswith('###')}")
print(f"Starts with '### ': {stripped.startswith('### ')}")
print(f"Chars 0-5 ord: {[ord(c) for c in stripped[:6]]}")
