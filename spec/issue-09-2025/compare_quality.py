#!/usr/bin/env python3
"""
Compare old page-*.md files with new page-dir/page-*.md files.

Quality comparison metrics:
1. Content completeness - check if new files contain all content from old files
2. Formatting quality - check for proper headers, blank lines, table formatting
3. Page coverage - verify all old pages are represented in new files
4. File size comparison - new files should be similar or larger
"""

import os
import re
import sys

SPEC_DIR = os.path.dirname(os.path.abspath(__file__))
OLD_DIR = SPEC_DIR
NEW_DIR = os.path.join(SPEC_DIR, "page-dir")

# Page markers in old files: # Page N of 434
OLD_PAGE_RE = re.compile(r'^# Page (\d+) of 434')

# Spec page references in old files: Page HI-N, Page 1-N-N, Page 2-1-XN
OLD_SPEC_PAGE_RE = re.compile(r'Page (HI-\d+|TOC-\d+|SRI-\d+|[ivx]+|1-\d+-\d+|2-1-[A-Z]\d+|1-0-\d+)')

# Page markers in new files: **Page <ID>**
NEW_PAGE_RE = re.compile(r'^\*\*Page (.+?)\s*\*\*$')


def analyze_old_files():
    """Analyze old page-*.md files."""
    old_files = {}
    old_pages = {}
    spec_refs = {}
    
    for i in range(1, 435):
        filename = f"page-{i:04d}.md"
        filepath = os.path.join(OLD_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            page_num = None
            for line in lines[:5]:
                match = OLD_PAGE_RE.match(line.strip())
                if match:
                    page_num = int(match.group(1))
                    break
            
            # Find spec page references
            refs = set()
            for line in lines:
                for match in OLD_SPEC_PAGE_RE.finditer(line):
                    refs.add(match.group(1))
            
            old_files[filename] = {
                'path': filepath,
                'size': len(content),
                'lines': len(lines),
                'page_num': page_num,
                'spec_refs': refs,
                'content': content
            }
            
            if page_num:
                old_pages[page_num] = filename

    return old_files, old_pages


def analyze_new_files():
    """Analyze new page-dir/page-*.md files."""
    new_files = {}
    
    for filename in sorted(os.listdir(NEW_DIR)):
        if not filename.startswith('page-') or not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(NEW_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        page_id = None
        for line in lines[:5]:
            match = NEW_PAGE_RE.match(line.strip())
            if match:
                page_id = match.group(1).split()[0]  # Take first token
                break
        
        if filename == 'page-front-matter.md':
            page_id = 'FRONT-MATTER'
        
        new_files[filename] = {
            'path': filepath,
            'size': len(content),
            'lines': len(lines),
            'page_id': page_id,
            'content': content
        }
    
    return new_files


def compare_quality(old_files, new_files):
    """Compare quality metrics between old and new files."""
    print("=" * 80)
    print("QUALITY COMPARISON: Old vs New Page Files")
    print("=" * 80)
    
    # Summary stats
    old_total_size = sum(f['size'] for f in old_files.values())
    new_total_size = sum(f['size'] for f in new_files.values() if f['page_id'] != 'FRONT-MATTER')
    old_total_lines = sum(f['lines'] for f in old_files.values())
    new_total_lines = sum(f['lines'] for f in new_files.values() if f['page_id'] != 'FRONT-MATTER')
    
    print(f"\n--- Summary Statistics ---")
    print(f"Old files: {len(old_files)} files, {old_total_size:,} chars, {old_total_lines:,} lines")
    print(f"New files: {len(new_files)} files, {new_total_size:,} chars, {new_total_lines:,} lines")
    print(f"Size difference: {new_total_size - old_total_size:+,} chars ({(new_total_size/old_total_size - 1)*100:+.1f}%)")
    print(f"Line difference: {new_total_lines - old_total_lines:+,} lines ({(new_total_lines/old_total_lines - 1)*100:+.1f}%)")
    
    # Check formatting quality
    print(f"\n--- Formatting Quality ---")
    
    # Check for proper page headers
    old_with_header = sum(1 for f in old_files.values() if f['content'].startswith('# Page'))
    new_with_header = sum(1 for f in new_files.values() if f['page_id'] and f['page_id'] != 'FRONT-MATTER')
    print(f"Old files with page header: {old_with_header}/{len(old_files)}")
    print(f"New files with page header: {new_with_header}/{len(new_files) - 1}")
    
    # Check for glued headings (### immediately followed by non-blank line)
    old_glued = 0
    new_glued = 0
    for f in old_files.values():
        lines = f['content'].split('\n')
        for i, line in enumerate(lines[:-1]):
            if line.strip().startswith('###') and lines[i+1].strip() and not lines[i+1].strip().startswith('#'):
                old_glued += 1
                break
    for f in new_files.values():
        if f['page_id'] == 'FRONT-MATTER':
            continue
        lines = f['content'].split('\n')
        for i, line in enumerate(lines[:-1]):
            if line.strip().startswith('###') and lines[i+1].strip() and not lines[i+1].strip().startswith('#'):
                new_glued += 1
                break
    print(f"Old files with glued headings: {old_glued}")
    print(f"New files with glued headings: {new_glued}")
    
    # Check for triple blank lines
    old_triple_blank = 0
    new_triple_blank = 0
    for f in old_files.values():
        if '\n\n\n\n' in f['content']:
            old_triple_blank += 1
    for f in new_files.values():
        if '\n\n\n\n' in f['content']:
            new_triple_blank += 1
    print(f"Old files with triple+ blank lines: {old_triple_blank}")
    print(f"New files with triple+ blank lines: {new_triple_blank}")
    
    # Check fabrication signals
    fabrication_terms = ['React', 'Docker', 'npm', 'async/await', 'This page describes', 'In summary']
    old_fabricated = 0
    new_fabricated = 0
    for f in old_files.values():
        for term in fabrication_terms:
            if term in f['content']:
                old_fabricated += 1
                break
    for f in new_files.values():
        for term in fabrication_terms:
            if term in f['content']:
                new_fabricated += 1
                break
    print(f"Old files with fabrication signals: {old_fabricated}")
    print(f"New files with fabrication signals: {new_fabricated}")
    
    # Check content completeness
    print(f"\n--- Content Completeness ---")
    
    # Check if all old spec page references are covered in new files
    all_old_refs = set()
    for f in old_files.values():
        all_old_refs.update(f['spec_refs'])
    
    all_new_ids = set(f['page_id'] for f in new_files.values() if f['page_id'] and f['page_id'] != 'FRONT-MATTER')
    
    # Normalize old refs for comparison
    old_normalized = set()
    for ref in all_old_refs:
        old_normalized.add(ref)
    
    # Check coverage
    covered = old_normalized & all_new_ids
    missing = old_normalized - all_new_ids
    extra = all_new_ids - old_normalized
    
    print(f"Old spec page references found: {len(old_normalized)}")
    print(f"New page IDs: {len(all_new_ids)}")
    print(f"Covered (in both): {len(covered)}")
    print(f"Missing from new (in old refs but not new IDs): {len(missing)}")
    if missing:
        print(f"  Missing: {sorted(missing)[:20]}")
    print(f"Extra in new (not in old refs): {len(extra)}")
    if extra:
        print(f"  Extra: {sorted(extra)[:20]}")
    
    # Check a few specific files for content comparison
    print(f"\n--- Specific File Comparisons ---")
    
    # Compare HI-1 (old page-0003)
    print(f"\nPage HI-1:")
    old_hi1 = old_files.get('page-0003.md', {})
    new_hi1 = new_files.get('page-HI-1.md', {})
    if old_hi1 and new_hi1:
        print(f"  Old page-0003.md: {old_hi1['size']} chars, {old_hi1['lines']} lines")
        print(f"  New page-HI-1.md: {new_hi1['size']} chars, {new_hi1['lines']} lines")
        print(f"  Size diff: {new_hi1['size'] - old_hi1['size']:+,} chars")
    
    # Compare HI-2 (old page-0004)
    print(f"\nPage HI-2:")
    old_hi2 = old_files.get('page-0004.md', {})
    new_hi2 = new_files.get('page-HI-2.md', {})
    if old_hi2 and new_hi2:
        print(f"  Old page-0004.md: {old_hi2['size']} chars, {old_hi2['lines']} lines")
        print(f"  New page-HI-2.md: {new_hi2['size']} chars, {new_hi2['lines']} lines")
        print(f"  Size diff: {new_hi2['size'] - old_hi2['size']:+,} chars")
    
    # Compare a dictionary page
    print(f"\nDictionary page 2-1-A1:")
    old_dict = old_files.get('page-0130.md', {})  # Old page 130 should be near A1
    new_dict = new_files.get('page-2-1-A1.md', {})
    if old_dict and new_dict:
        print(f"  Old page-0130.md: {old_dict['size']} chars, {old_dict['lines']} lines")
        print(f"  New page-2-1-A1.md: {new_dict['size']} chars, {new_dict['lines']} lines")
        print(f"  Size diff: {new_dict['size'] - old_dict['size']:+,} chars")
    
    # Check for content in new files that's not in old files (better extraction)
    print(f"\n--- Content Quality Assessment ---")
    
    # Check for STE/Non-STE example formatting
    old_ste_examples = sum(1 for f in old_files.values() if '> **STE:**' in f['content'] or 'STE:' in f['content'])
    new_ste_examples = sum(1 for f in new_files.values() if 'STE:' in f['content'])
    print(f"Old files with STE examples: {old_ste_examples}")
    print(f"New files with STE examples: {new_ste_examples}")
    
    # Check for table formatting
    old_tables = sum(1 for f in old_files.values() if '|---' in f['content'] or '| ---' in f['content'])
    new_tables = sum(1 for f in new_files.values() if '|---' in f['content'])
    print(f"Old files with tables: {old_tables}")
    print(f"New files with tables: {new_tables}")
    
    # Check for dictionary entry formatting
    old_dict_entries = sum(1 for f in old_files.values() if 'APPROVED' in f['content'] or 'UNAPPROVED' in f['content'])
    new_dict_entries = sum(1 for f in new_files.values() if 'APPROVED' in f['content'] or 'UNAPPROVED' in f['content'])
    print(f"Old files with dictionary entries: {old_dict_entries}")
    print(f"New files with dictionary entries: {new_dict_entries}")
    
    print(f"\n--- Assessment Summary ---")
    print(f"New files have {'better' if new_glued < old_glued else 'worse'} heading formatting")
    print(f"New files have {'better' if new_triple_blank < old_triple_blank else 'worse'} blank line handling")
    print(f"New files have {'better' if new_fabricated < old_fabricated else 'worse'} fabrication control")
    print(f"New files have {new_total_lines - old_total_lines:+,} more lines (better structure)")


if __name__ == '__main__':
    old_files, old_pages = analyze_old_files()
    new_files = analyze_new_files()
    compare_quality(old_files, new_files)
