#!/usr/bin/env python3
"""Scan and fix nested code fence issues in markdown files.

Rule: When a code fence contains another code fence, the outer fence
must use more backticks. Standard is 3 (```), so nested blocks need
4 (````) and double-nested need 5 (`````).

Fixes: upgrades outer fence backtick count when inner fences detected.
"""

import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent

def scan_file(filepath):
    """Find nested fence issues. Returns list of (line_num, description)."""
    try:
        content = filepath.read_text()
    except:
        return []
    
    lines = content.split('\n')
    issues = []
    
    # Track fence stack: (line_num, indent, backtick_count, lang)
    fence_stack = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Detect code fence start/end
        fence_match = re.match(r'^(\s*)(`{3,})(\S*)\s*$', stripped)
        if fence_match:
            indent = len(fence_match.group(1))
            backtick_count = len(fence_match.group(2))
            lang = fence_match.group(3)
            
            if not fence_stack:
                fence_stack.append((i + 1, indent, backtick_count, lang))
            else:
                prev = fence_stack[-1]
                # Same indent + backtick count = closing fence
                if indent == prev[1] and backtick_count == prev[2]:
                    fence_stack.pop()
                else:
                    fence_stack.append((i + 1, indent, backtick_count, lang))
    
    # Now scan inside each fence for nested fences at same or lower backtick count
    in_fence = False
    fence_start = 0
    fence_bt = 0
    fence_lang = ''
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        fence_match = re.match(r'^(\s*)(`{3,})(\S*)\s*$', stripped)
        
        if fence_match:
            indent = len(fence_match.group(1))
            bt = len(fence_match.group(2))
            lang = fence_match.group(3)
            
            if not in_fence:
                in_fence = True
                fence_start = i + 1
                fence_bt = bt
                fence_lang = lang
            else:
                # Check if this is closing fence
                if indent == 0 and bt >= fence_bt:
                    in_fence = False
                    continue
                
                # Nested fence detected INSIDE a code block
                if bt <= fence_bt:
                    issues.append({
                        'file': str(filepath),
                        'line': i + 1,
                        'outer_fence_line': fence_start,
                        'outer_bt': fence_bt,
                        'inner_bt': bt,
                        'inner_lang': lang,
                    })
    
    return issues


def fix_file(filepath):
    """Fix nested fence issues by upgrading outer fence backtick count."""
    issues = scan_file(filepath)
    if not issues:
        return 0
    
    content = filepath.read_text()
    lines = content.split('\n')
    
    # Group issues by outer fence and determine needed upgrade
    # For each fenced block, find max inner backtick count and upgrade outer
    fixes = {}
    for issue in issues:
        outer_line = issue['outer_fence_line']
        needed = max(issue['inner_bt'] + 1, 4)
        if outer_line not in fixes or needed > fixes[outer_line]:
            fixes[outer_line] = needed
    
    # Apply fixes from bottom to top to preserve line numbers
    for outer_line in sorted(fixes.keys(), reverse=True):
        idx = outer_line - 1  # 0-indexed
        
        # Fix opening fence
        old_open = lines[idx]
        new_bt = fixes[outer_line]
        new_open = re.sub(r'^(\s*)(`{3,})', f'\\1{\"`\" * new_bt}', old_open)
        lines[idx] = new_open
        
        # Find and fix closing fence
        fence_open_bt = len(re.match(r'^(\s*)(`{3,})', old_open).group(2))
        for j in range(idx + 1, len(lines)):
            close_match = re.match(r'^(\s*)(`{3,})\s*$', lines[j])
            if close_match and len(close_match.group(2)) == fence_open_bt:
                old_close = lines[j]
                new_close = re.sub(r'^(\s*)(`{3,})', f'\\1{\"`\" * new_bt}', old_close)
                lines[j] = new_close
                break
    
    filepath.write_text('\n'.join(lines))
    return len(fixes)


def main():
    import sys
    dry_run = '--dry-run' in sys.argv
    
    md_files = []
    for f in PROJECT.rglob('*.md'):
        if '.git/' in str(f) or '__pycache__' in str(f):
            continue
        md_files.append(f)
    
    total_fixes = 0
    files_fixed = 0
    
    for f in sorted(md_files):
        issues = scan_file(f)
        if not issues:
            continue
        
        if dry_run:
            print(f"\n{f.relative_to(PROJECT)}: {len(issues)} issue(s)")
            for iss in issues:
                print(f"  L{iss['line']}: inner `{'>'*iss['inner_bt']}` inside outer `{'>'*iss['outer_bt']}` (L{iss['outer_fence_line']})")
        else:
            n = fix_file(f)
            if n:
                print(f"  Fixed {f.relative_to(PROJECT)}: {n} fence(s) upgraded")
                total_fixes += n
                files_fixed += 1
    
    if dry_run:
        print(f"\nDry run: {len([f for f in md_files if scan_file(f)])} files with issues")
    else:
        print(f"\nFixed {total_fixes} fences in {files_fixed} files")


if __name__ == "__main__":
    main()
