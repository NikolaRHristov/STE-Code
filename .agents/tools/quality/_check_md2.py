#!/usr/bin/env python3
"""Quick markdown format checker — checks line 12 heading format.

Usage: python3 .agents/tools/quality/_check_md2.py [filepath]
  Default: ste-code/adapted/a-categories.md
"""
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
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
