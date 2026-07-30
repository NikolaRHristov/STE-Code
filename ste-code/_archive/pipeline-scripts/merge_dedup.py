#!/usr/bin/env python3
"""Deduplicate and organize master-raw.md into master.md"""
import re

RAW = "ste-code/merged/master-raw.md"
MASTER = "ste-code/merged/master.md"

with open(RAW) as f:
    lines = f.readlines()

clean = []
seen_meta = False  # Track if we've already output the main metadata block
last_line = ""

for i, line in enumerate(lines):
    stripped = line.strip()
    
    # Skip duplicate page headers: "# Page NNN of 434"
    if re.match(r'^# Page \d+ of 434$', stripped):
        continue
    
    # Skip duplicate Source/Pages metadata blocks (only keep first occurrence)
    if stripped.startswith('> **Source:') and 'ASD-STE100' in stripped:
        continue
    if stripped.startswith('> **Pages:') and 'of 434' in stripped:
        continue
    
    # Skip standalone horizontal rules that separate duplicate headers
    if stripped == '---' and (i == 0 or (i > 0 and lines[i-1].strip() == '')):
        continue
    
    # Skip completely empty lines that create triple+ blanks
    if stripped == '' and last_line == '':
        continue
    
    clean.append(line)
    last_line = stripped

# Now add the single metadata block at the top
metadata = [
    "# ASD-STE100 Simplified Technical English — Complete Specification\n\n",
    "> **Source:** ASD-STE100 Issue 9, January 2025\n",
    "> **Pages:** 1–434 of 434\n",
    "> **Generated:** 2026-07-30 — Merged from 109 refined files\n\n",
    "---\n\n",
]

# Find where the actual content starts (first non-metadata section)
# and organize sections
final = metadata.copy()

# Re-process to build clean organized structure
content_started = False
for line in clean:
    s = line.strip()
    if s and not content_started:
        content_started = True
    if content_started:
        final.append(line)

# Remove trailing blank lines
while final and final[-1].strip() == '':
    final.pop()
final.append('\n')

with open(MASTER, 'w') as f:
    f.writelines(final)

# Stats
content = ''.join(final)
rule_count = len(re.findall(r'^### Rule \d+\.\d+', content, re.MULTILINE))
gr_count = len(re.findall(r'^### GR\d+', content, re.MULTILINE))
approved_count = len(re.findall(r'#### \w+ \([^)]+\)$', content, re.MULTILINE))
unapproved_count = len(re.findall(r'#### \w+ \([^)]+\) — UNAPPROVED', content, re.MULTILINE))
total_lines = len(final)

print(f"master.md: {total_lines} lines ({len(''.join(final))} chars)")
print(f"Writing Rules: {rule_count} individual rules + {gr_count} GR rules = {rule_count + gr_count} total")
print(f"Dictionary: {approved_count} approved entries, {unapproved_count} unapproved entries")
