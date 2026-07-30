#!/usr/bin/env python3
"""
Split issue-09-2025.md into individual page files in a page-dir subdirectory.

The combined markdown file uses spec page identifiers like **Page HI-1**, 
**Page 1-1-1**, **Page 2-1-A1** as page boundaries. This script splits the 
file at each page marker, creating one output file per spec page.

Output files are named using the spec page identifier:
  page-dir/page-HI-1.md, page-dir/page-1-1-1.md, page-dir/page-2-1-A1.md, etc.

The front matter (content before the first page marker) is saved as
page-dir/page-front-matter.md.

Usage:
  python3 split_spec.py
"""

import re
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "issue-09-2025.md")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "page-dir")

# Pattern: **Page <ID>** possibly followed by additional text like "Part 2 - Dictionary"
PAGE_MARKER_RE = re.compile(r'^\*\*Page\s+(.+?)\s*\*\*$')


def parse_page_id(marker_text):
    """
    Extract the page ID from a marker like 'Page HI-1' or 'Page 2-1-A1 Part 2 - Dictionary'.
    Returns the clean page ID (e.g., 'HI-1', '1-1-1', '2-1-A1').
    """
    parts = marker_text.strip().split()
    page_id = parts[0]
    return page_id


def sanitize_filename(page_id):
    """Convert page ID to a safe filename: HI-1 -> page-HI-1.md"""
    safe = page_id.replace('/', '-').replace('\\', '-')
    return f"page-{safe}.md"


def collapse_blank_lines(content):
    """Collapse 3+ consecutive blank lines to max 2."""
    while '\n\n\n\n' in content:
        content = content.replace('\n\n\n\n', '\n\n\n')
    return content


def add_unapproved_markers(content):
    """
    Add '— UNNAPPROVED' markers to lowercase dictionary entries.
    
    In the combined file, dictionary entries use:
      **ABOUT (prep)**  for approved (uppercase) words
      **abrupt (adj)**  for unapproved (lowercase) words
    
    The old extraction script added '— UNNAPPROVED' to lowercase entries.
    This function replicates that behavior for consistency with the old files.
    
    Pattern in combined file: |**word (POS)**|
    Pattern in old files:     | **word (POS) — UNNAPPROVED** |
    """
    # Match dictionary entry patterns: |**lowercase_word (POS)**|
    # where the word starts with lowercase (unapproved)
    # Pattern: |**word (pos)**|  -> | **word (pos) — UNNAPPROVED** |
    pattern = re.compile(
        r'\|(\s*)\*\*(?P<word>[a-z][a-z\s\-]*?)\s*(?P<pos>\([a-z][a-z\s,]*\))\*\*\|'
    )
    
    def replace_unapproved(match):
        prefix = match.group(1)
        word = match.group('word')
        pos = match.group('pos')
        return f'|{prefix}**{word} {pos} — UNNAPPROVED**|'
    
    return pattern.sub(replace_unapproved, content)


def split_spec(input_path, output_dir):
    """Split the combined spec markdown into individual page files."""
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Find all page marker positions
    page_markers = []  # (line_index, page_id, raw_marker)
    for i, line in enumerate(lines):
        stripped = line.strip()
        match = PAGE_MARKER_RE.match(stripped)
        if match:
            marker_text = match.group(1)
            page_id = parse_page_id(marker_text)
            page_markers.append((i, page_id, marker_text))

    print(f"Found {len(page_markers)} page markers")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    segments = []
    
    # Handle preamble (content before first page marker)
    if page_markers:
        first_marker_idx = page_markers[0][0]
        if first_marker_idx > 0:
            preamble_lines = lines[:first_marker_idx]
            preamble_content = ''.join(preamble_lines).strip()
            preamble_content = collapse_blank_lines(preamble_content)
            preamble_content = add_unapproved_markers(preamble_content)
            if preamble_content:
                segments.append({
                    'page_id': 'FRONT-MATTER',
                    'filename': 'page-front-matter.md',
                    'content': preamble_content,
                    'line_start': 0,
                    'line_end': first_marker_idx
                })

    # Handle each page segment
    for idx, (marker_idx, page_id, raw_marker) in enumerate(page_markers):
        # Determine end of this segment
        if idx + 1 < len(page_markers):
            next_marker_idx = page_markers[idx + 1][0]
            segment_lines = lines[marker_idx:next_marker_idx]
        else:
            # Last page - go to end of file
            next_marker_idx = len(lines)
            segment_lines = lines[marker_idx:]

        content = ''.join(segment_lines).strip()
        content = collapse_blank_lines(content)
        content = add_unapproved_markers(content)
        
        filename = sanitize_filename(page_id)
        segments.append({
            'page_id': page_id,
            'filename': filename,
            'content': content,
            'line_start': marker_idx,
            'line_end': next_marker_idx
        })

    # Write output files
    written = 0
    for seg in segments:
        output_path = os.path.join(output_dir, seg['filename'])
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(seg['content'])
            f.write('\n')
        written += 1
        if written <= 10 or written % 50 == 0:
            print(f"  {seg['page_id']:>15s} → {seg['filename']:>25s} ({len(seg['content'])} chars)")
        elif written == len(segments):
            print(f"  ...")
            print(f"  {seg['page_id']:>15s} → {seg['filename']:>25s} ({len(seg['content'])} chars)")

    print(f"\nWrote {written} page files to {output_dir}")
    
    # Write a manifest file
    manifest_path = os.path.join(output_dir, "MANIFEST.md")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write("# Page File Manifest\n\n")
        f.write(f"Generated from: issue-09-2025.md\n")
        f.write(f"Total page markers found: {len(page_markers)}\n")
        f.write(f"Total segments (including front matter): {len(segments)}\n\n")
        f.write("| # | Page ID | Filename | Lines | Chars |\n")
        f.write("|---|---------|----------|-------|-------|\n")
        for i, seg in enumerate(segments):
            line_count = seg['content'].count('\n') + 1
            f.write(f"| {i+1} | {seg['page_id']} | {seg['filename']} | {line_count} | {len(seg['content'])} |\n")
    
    print(f"Manifest written to {manifest_path}")
    return written


if __name__ == '__main__':
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: Input file not found: {INPUT_FILE}")
        sys.exit(1)
    
    split_spec(INPUT_FILE, OUTPUT_DIR)
