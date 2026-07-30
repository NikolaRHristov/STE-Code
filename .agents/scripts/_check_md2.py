#!/usr/bin/env python3
with open('ste-code/adapted/a-categories.md', 'r') as f:
    lines = f.readlines()

# Just check line 12 specifically
line = lines[11]  # 0-indexed
print(f"Line 12 raw repr: {repr(line[:60])}")
stripped = line.strip()
print(f"Stripped repr: {repr(stripped[:60])}")
print(f"Starts with '###': {stripped.startswith('###')}")
print(f"Starts with '### ': {stripped.startswith('### ')}")
print(f"Chars 0-5 ord: {[ord(c) for c in stripped[:6]]}")
