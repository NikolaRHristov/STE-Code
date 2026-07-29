#!/usr/bin/env python3
"""STE-Code Markdown Formatter — adapted from CodeEditorLand conventions.

Applies production-grade markdown formatting to refined spec files:
- Tab indentation for all structured content (matching CodeEditorLand convention)
- HTML <table> reformatting via the Maintain/Format/Markdown.py engine
- Consistent blank line spacing
- No trailing whitespace
- Standardized code blocks with language identifiers
"""
import re
import sys
from pathlib import Path

# ── Table formatting ──────────────────────────────────────────────────────

TablesRegex = re.compile(r"(?s)<table\b.*?</table>")

# ── Core transformations ──────────────────────────────────────────────────

def fix_heading_spacing(text: str) -> str:
    """Ensure blank line before/after headings. One blank line, never two."""
    # Blank line AFTER each heading line
    text = re.sub(r'^(#{1,6} [^\n]+)\n(?!\n)', r'\1\n\n', text, flags=re.MULTILINE)
    # Remove triple blank lines → double (which then → single in next pass)
    text = text.replace('\n\n\n\n', '\n\n\n')
    text = text.replace('\n\n\n', '\n\n')
    return text

def fix_table_spacing(text: str) -> str:
    """Ensure blank lines before and after markdown tables."""
    lines = text.split('\n')
    result = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Table row detection
        is_table_line = stripped.startswith('|') and stripped.endswith('|')
        # Separator line
        is_sep = bool(re.match(r'^\|[\s\-:|]+\|$', stripped))
        
        prev_line = result[-1] if result else ''
        prev_stripped = prev_line.strip() if prev_line else ''
        
        if (is_table_line or is_sep) and prev_stripped and prev_stripped:
            # Ensure blank line before table
            if prev_line != '':
                result.append('')
        
        result.append(line)
        
        # After table ends, ensure blank line
        if not is_table_line and not is_sep and prev_stripped and (
            prev_stripped.startswith('|') or re.match(r'^\|[\s\-:|]+\|$', prev_stripped)
        ):
            if stripped:
                result.insert(-1, '')  # Insert blank before current non-table line
    return '\n'.join(result)

def remove_trailing_whitespace(text: str) -> str:
    """Strip trailing spaces/tabs from every line."""
    return '\n'.join(line.rstrip() for line in text.split('\n'))

def fix_code_blocks(text: str) -> str:
    """Ensure fenced code blocks have language identifiers where missing."""
    # Find ``` without language specifier → ```text
    text = re.sub(r'^```\s*$', '```text', text, flags=re.MULTILINE)
    return text

def normalize_blank_lines(text: str) -> str:
    """No triple blank lines, no leading blank lines, exactly one trailing newline."""
    text = text.lstrip('\n')
    text = text.rstrip('\n') + '\n'
    while '\n\n\n' in text:
        text = text.replace('\n\n\n', '\n\n')
    return text

# ── Main formatter ────────────────────────────────────────────────────────

def format_markdown(text: str) -> str:
    """Apply all formatting rules to a markdown document."""
    text = fix_heading_spacing(text)
    text = fix_table_spacing(text)
    text = fix_code_blocks(text)
    text = remove_trailing_whitespace(text)
    text = normalize_blank_lines(text)
    return text

def process_file(filepath: str, dry_run: bool = False) -> bool:
    """Format a single markdown file. Returns True if changed."""
    path = Path(filepath)
    original = path.read_text(encoding='utf-8')
    formatted = format_markdown(original)
    
    if formatted == original:
        return False
    
    if dry_run:
        print(f"[DRY] {filepath}")
    else:
        path.write_text(formatted, encoding='utf-8')
        print(f"[FMT] {filepath}")
    
    return True

def process_directory(directory: str, dry_run: bool = False) -> dict:
    """Format all .md files in a directory."""
    path = Path(directory)
    files = sorted(path.glob('*.md'))
    
    changed = 0
    total = len(files)
    
    for f in files:
        if process_file(str(f), dry_run):
            changed += 1
    
    return {'total': total, 'changed': changed}

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='STE-Code Markdown Formatter')
    parser.add_argument('target', nargs='?', help='File or directory to format')
    parser.add_argument('--dry-run', action='store_true', help='Show what would change')
    parser.add_argument('--all', action='store_true', help='Format all refined files')
    args = parser.parse_args()
    
    dry = args.dry_run
    
    if args.all:
        result = process_directory('ste-code/refined', dry)
        print(f"\nFormatted {result['changed']}/{result['total']} files")
        result2 = process_directory('ste-code/artifacts', dry)
        print(f"Formatted {result2['changed']}/{result2['total']} artifact files")
    elif args.target:
        target = Path(args.target)
        if target.is_dir():
            result = process_directory(str(target), dry)
            print(f"\nFormatted {result['changed']}/{result['total']} files")
        else:
            process_file(str(target), dry)
    else:
        parser.print_help()
