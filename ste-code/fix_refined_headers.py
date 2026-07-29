#!/usr/bin/env python3
"""Fix all refined files: add proper # Page NNN of 434 headers, clean up body headers, fix spacing."""
import os
import re
import sys

REFINED_DIR = os.path.join(os.path.dirname(__file__), 'refined')
TOTAL_PAGES = 434

def parse_pages(filename):
    """Extract start_page, end_page from rNNN-pSTART-END.md"""
    m = re.match(r'r\d+-p(\d+)-(\d+)\.md', filename)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None, None

def fix_file(filepath):
    filename = os.path.basename(filepath)
    start_page, end_page = parse_pages(filename)
    if start_page is None:
        return "SKIP", f"Cannot parse pages from {filename}"
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    fixed_count = 0
    
    # 1. Build the proper header block
    proper_header = f"# Page {start_page} of {TOTAL_PAGES}\n\n> **Source:** ASD-STE100 Issue 9, January 2025\n> **Pages:** {start_page}–{end_page} of {TOTAL_PAGES}\n\n"
    
    # 2. Remove any existing header lines at the top that look like:
    #    - "# ASD-STE100..." 
    #    - "# Dictionary..." 
    #    - "# Issue..."
    #    - "> **Source:** ..." block
    #    - "> **Pages:** ..." block
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    in_header = True
    removed_front_headers = []
    
    while i < len(lines) and in_header:
        line = lines[i]
        stripped = line.strip()
        
        # Check if this is a header-type line to remove
        is_old_header = False
        
        if stripped.startswith('# ') and any(kw in stripped.lower() for kw in 
            ['asd-ste100', 'dictionary', 'issue', 'simplified technical', 'standard for']):
            is_old_header = True
            removed_front_headers.append(stripped)
        elif stripped.startswith('> **Source:') or stripped.startswith('> **Pages:'):
            is_old_header = True
            removed_front_headers.append(stripped)
        elif stripped.startswith('# ') and re.match(r'#\s+(Part|Section|Rule)\s', stripped):
            # Keep section/part/rule headings
            in_header = False
            continue
        elif stripped == '' and i < 5:
            # Blank lines in the header area are OK to skip
            is_old_header = True
        else:
            in_header = False
            continue
        
        if is_old_header:
            i += 1
        else:
            in_header = False
    
    # 3. Now build the new content
    # Start with proper header
    body_lines = lines[i:]
    
    # Remove leading blank lines from body
    while body_lines and body_lines[0].strip() == '':
        body_lines.pop(0)
    
    # 4. Remove "ASD-STE100 Simplified Technical English" from body content
    cleaned_body = []
    body_fixes = 0
    for line in body_lines:
        stripped = line.strip()
        # Remove heading-like ASD-STE100 lines
        if re.match(r'^#+\s*ASD-STE100\s*Simplified\s*Technical\s*English', line, re.IGNORECASE):
            body_fixes += 1
            continue
        if re.match(r'^#+\s*ASD-STE100\s*[-—]\s*Dictionary', line, re.IGNORECASE):
            body_fixes += 1
            continue
        # Remove repeated metadata blocks nested in body (from PDF page breaks)
        if stripped.startswith('> **Source:') and 'ASD-STE100' in stripped:
            body_fixes += 1
            continue
        if stripped.startswith('> **Pages:') and 'of 434' in stripped:
            body_fixes += 1
            continue
        # Remove duplicate page headers embedded by extraction workers
        if re.match(r'^# Page \d+ of 434$', stripped):
            body_fixes += 1
            continue
        cleaned_body.append(line)
    
    body = '\n'.join(cleaned_body)
    
    # 5. Fix triple blank lines → double blank lines
    while '\n\n\n\n' in body:
        body = body.replace('\n\n\n\n', '\n\n\n')
        fixed_count += 1
    while '\n\n\n' in body:
        body = body.replace('\n\n\n', '\n\n')
        fixed_count += 1
    
    # 6. Remove trailing whitespace
    body_lines2 = body.split('\n')
    trailing_fixes = 0
    for j in range(len(body_lines2)):
        if body_lines2[j].rstrip() != body_lines2[j]:
            body_lines2[j] = body_lines2[j].rstrip()
            trailing_fixes += 1
    body = '\n'.join(body_lines2)
    fixed_count += trailing_fixes
    
    # 7. Assemble final content
    new_content = proper_header + body
    
    # Ensure file ends with newline
    if not new_content.endswith('\n'):
        new_content += '\n'
    
    if new_content != original:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return "FIXED", f"{len(removed_front_headers)} headers removed, {body_fixes} body headers, {fixed_count} spacing fixes"
    else:
        return "OK", "No changes needed"

def main():
    if not os.path.isdir(REFINED_DIR):
        print(f"ERROR: {REFINED_DIR} not found")
        sys.exit(1)
    
    raw_files = [
        f for f in os.listdir(REFINED_DIR) 
        if f.startswith('r') and '-p' in f and f.endswith('.md')
    ]
    def sort_key(fname):
        m = re.search(r'r(\d+)', fname)
        return int(m.group(1)) if m else 0
    files = sorted(raw_files, key=sort_key)
    
    stats = {"FIXED": 0, "OK": 0, "SKIP": 0}
    
    for f in files:
        filepath = os.path.join(REFINED_DIR, f)
        status, detail = fix_file(filepath)
        stats[status] = stats.get(status, 0) + 1
        if status != "OK":
            print(f"{status}: {f} — {detail}")
    
    print(f"\nSummary: {stats['FIXED']} fixed, {stats['OK']} OK, {stats['SKIP']} skipped out of {len(files)} files")

if __name__ == '__main__':
    main()
