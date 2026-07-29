#!/usr/bin/env python3
"""Fix blank lines between markdown table rows — re-join broken tables."""
import re, sys
from pathlib import Path

def fix_table_row_gaps(text: str) -> str:
    """Remove blank lines between consecutive markdown table rows."""
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        is_row = stripped.startswith('|') and stripped.endswith('|')
        
        result.append(line)
        
        if is_row and i + 1 < len(lines):
            # Look ahead: if next non-blank line is also a table row, remove the blank
            next_idx = i + 1
            while next_idx < len(lines) and lines[next_idx].strip() == '':
                next_idx += 1
            if next_idx < len(lines):
                next_stripped = lines[next_idx].strip()
                next_is_row = next_stripped.startswith('|') and next_stripped.endswith('|')
                if next_is_row:
                    # Skip blank lines between this row and the next row
                    i = next_idx
                    continue
        i += 1
    
    return '\n'.join(result)

def fix_file(path: str) -> bool:
    p = Path(path)
    original = p.read_text(encoding='utf-8')
    fixed = fix_table_row_gaps(original)
    if fixed != original:
        p.write_text(fixed, encoding='utf-8')
        return True
    return False

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('target', help='Directory or file')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    
    target = Path(args.target)
    files = sorted(target.glob('*.md')) if target.is_dir() else [target]
    
    fixed = sum(1 for f in files if fix_file(str(f)))
    verb = 'Would fix' if args.dry_run else 'Fixed'
    print(f'{verb} {fixed}/{len(files)} files')
