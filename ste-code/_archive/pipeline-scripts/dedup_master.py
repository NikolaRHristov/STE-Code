#!/usr/bin/env python3
"""Deduplicate and clean master.md — strip metadata, page header dupes, blank lines."""
import re

with open('ste-code/merged/master.md') as f:
    text = f.read()

# Strip enrichment metadata headers
text = re.sub(r'<!-- section:.*?verified: true -->\n?', '', text)

# Remove duplicate page headers (keep first)
seen = set()
lines = text.split('\n')
out = []
for line in lines:
    m = re.match(r'^# Page (\d+) of 434', line)
    if m:
        pn = int(m.group(1))
        if pn in seen:
            continue
        seen.add(pn)
    out.append(line)

text = '\n'.join(out)

# Collapse excessive blank lines
text = re.sub(r'\n{4,}', '\n\n\n', text)

# Remove leading whitespace on empty lines
text = re.sub(r'\n[ \t]+\n', '\n\n', text)

with open('ste-code/merged/master.md', 'w') as f:
    f.write(text)

# Stats
rules = len(set(re.findall(r'Rule (\d+\.\d+)', text)))
pages = len(seen)
size = len(text)
lines = text.count('\n')
print(f"master.md cleaned: {lines:,} lines, {size:,} bytes")
print(f"Unique page headers: {pages}")
print(f"Unique rules referenced: {rules}")
