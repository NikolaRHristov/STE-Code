#!/usr/bin/env python3
"""Extract dictionary entries from spec page markdown files into worker output files."""
import os, re

SPEC = '/Volumes/CORSAIR/Developer/macOS/Application/Manual/spec/issue-09-2025'
WORKERS = '/Volumes/CORSAIR/Developer/macOS/Application/Manual/ste-code/workers'

def extract_dict_pages(start_page, end_page, output_file, section_label):
    """Read spec pages and extract dictionary content."""
    entries = []
    pages_read = 0
    
    for pg in range(start_page, end_page + 1):
        path = os.path.join(SPEC, f'page-{pg:04d}.md')
        if not os.path.exists(path):
            continue
        with open(path) as f:
            content = f.read()
        pages_read += 1
        
        # Extract the markdown table rows (dictionary entries)
        # Format: | **WORD (POS)** | meaning and examples |
        # or: | **word (POS) — UNNAPROVED** | ... |
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('| **') and '|' in line[4:]:
                entries.append(line)
    
    # Write output
    with open(output_file, 'w') as f:
        f.write(f'# ASD-STE100 Issue 9 — Dictionary {section_label}\n\n')
        f.write(f'> Source: pages {start_page}-{end_page} ({pages_read} pages read)\n\n')
        f.write('| Word (POS) | Meaning & Examples |\n')
        f.write('|------------|-------------------|\n')
        for entry in entries:
            f.write(entry + '\n')
    
    return pages_read, len(entries)

# Extract W6: Dictionary A-F (pages 181-240)
pages, entries = extract_dict_pages(181, 240, 
    os.path.join(WORKERS, 'w6-dict-a-f.md'), 'A–F')
print(f'W6: {pages} pages, {entries} entries → w6-dict-a-f.md')

# Extract W7: Dictionary G-P (pages 241-300)
pages, entries = extract_dict_pages(241, 300,
    os.path.join(WORKERS, 'w7-dict-g-p.md'), 'G–P')
print(f'W7: {pages} pages, {entries} entries → w7-dict-g-p.md')

# Extract W8: Dictionary Q-Z (pages 301-360)
pages, entries = extract_dict_pages(301, 360,
    os.path.join(WORKERS, 'w8-dict-q-z.md'), 'Q–Z')
print(f'W8: {pages} pages, {entries} entries → w8-dict-q-z.md')

# Extract W9: Appendices (pages 361-434)
# For appendices, extract ALL content (not just tables)
with open(os.path.join(WORKERS, 'w9-appendices.md'), 'w') as out:
    out.write('# ASD-STE100 Issue 9 — Appendices, Index, and History\n\n')
    out.write(f'> Source: pages 361-434\n\n')
    
    pages_read = 0
    total_chars = 0
    for pg in range(361, 435):
        path = os.path.join(SPEC, f'page-{pg:04d}.md')
        if not os.path.exists(path):
            continue
        with open(path) as f:
            content = f.read()
        pages_read += 1
        # Strip page header and write body
        body = re.sub(r'^# Page \d+ of 434\n', f'## Page {pg}\n', content)
        out.write(body + '\n\n---\n\n')
        total_chars += len(content)
    
    print(f'W9: {pages_read} pages, {total_chars} chars → w9-appendices.md')

print('\nDone. All 4 worker files written.')
