#!/usr/bin/env python3
"""
Advanced PDF-to-Markdown page extractor.
Usage: python3 extract_page.py <pdf_path> <page_number> <output_path>

Extracts a single page with:
- Heading detection (centered, all-caps short lines)
- Table detection and markdown formatting
- Dictionary entry detection (WORD (POS), meaning, examples)
- STE/non-STE example detection
- List detection
- Proper paragraph reconstruction
"""

import pdfplumber
import sys
import re
import os


def is_heading(line):
    """Detect potential headings: short, centered, often all-caps or title case."""
    stripped = line.strip()
    if not stripped or len(stripped) > 80:
        return False
    # All caps short line (likely section title)
    if stripped.isupper() and len(stripped) > 3:
        return True
    # Title case with keywords
    keywords = ['Section', 'Rule', 'Part', 'Issue', 'Copyright', 'Introduction',
                'Highlights', 'Table of', 'Chapter', 'Standard', 'Specification']
    for kw in keywords:
        if stripped.startswith(kw):
            return True
    return False


def is_dictionary_entry(text):
    """Detect if text contains STE dictionary entries."""
    # Pattern: WORD (POS) or word (POS)
    if re.match(r'^[A-Z][A-Z\s\-]+(\s*\([a-z]+[,0-9\s]*\))', text):
        return True
    if re.match(r'^[a-z][a-z\s\-]+(\s*\([a-z]+\))', text):
        return True
    return False


def is_ste_example(text):
    """Detect STE example lines (all caps, imperative)."""
    stripped = text.strip()
    if not stripped:
        return False
    # STE examples typically ALL CAPS and start with a verb
    if stripped.isupper() and len(stripped) > 15:
        return True
    if re.match(r'^[A-Z][A-Z\s,;.()]+$', stripped) and len(stripped) > 20:
        return True
    return False


def is_list_item(line):
    """Detect list items: starts with number, letter, or bullet."""
    stripped = line.strip()
    return bool(re.match(r'^(\d+[\.\)]|[a-zA-Z][\.\)]|[-•*])\s', stripped))


def format_table_as_markdown(table):
    """Convert pdfplumber table to markdown table."""
    if not table or len(table) < 1:
        return ""

    # Clean cells
    cleaned = []
    for row in table:
        cleaned_row = [(cell or '').replace('\n', ' ').strip() for cell in row]
        cleaned.append(cleaned_row)

    # Remove empty columns
    non_empty_cols = []
    for col_idx in range(len(cleaned[0])):
        if any(row[col_idx] for row in cleaned):
            non_empty_cols.append(col_idx)

    if not non_empty_cols:
        return ""

    # Build markdown
    lines = []
    # Header
    header_cells = [cleaned[0][i] for i in non_empty_cols]
    lines.append('| ' + ' | '.join(header_cells) + ' |')
    # Separator
    lines.append('|' + '|'.join([' --- ' for _ in non_empty_cols]) + '|')
    # Body
    for row in cleaned[1:]:
        cells = [row[i] if i < len(row) else '' for i in non_empty_cols]
        lines.append('| ' + ' | '.join(cells) + ' |')

    return '\n'.join(lines)


def format_dictionary_page(lines):
    """
    Format dictionary page text. Since the 4-column layout is hard to parse,
    use a simpler approach: group entries by blank-line separators.
    """
    md_lines = []
    md_lines.append('')
    md_lines.append('| Word (POS) | Meaning & Examples |')
    md_lines.append('|------------|-------------------|')

    current_word = ''
    current_text = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_word and current_text:
                text = ' '.join(current_text).replace('|', '\\|')
                md_lines.append(f'| **{current_word}** | {text} |')
                current_word = ''
                current_text = []
            continue

        # Detect new entry: WORD (POS) at start
        entry_match = re.match(r'^([A-Z][A-Z\s\-/]+)\s*(\([a-z]+[,0-9\s]*\))', stripped)
        if entry_match:
            if current_word and current_text:
                text = ' '.join(current_text).replace('|', '\\|')
                md_lines.append(f'| **{current_word}** | {text} |')
            current_word = entry_match.group(1).strip()
            pos = entry_match.group(2).strip()
            rest = stripped[entry_match.end():].strip()
            current_word = f'{current_word} {pos}'
            current_text = [rest] if rest else []
            continue

        # Lowercase unapproved entry
        entry_lower = re.match(r'^([a-z][a-z\s\-/]+)\s*(\([a-z]+[\s,]*[a-z]*\))', stripped)
        if entry_lower:
            if current_word and current_text:
                text = ' '.join(current_text).replace('|', '\\|')
                md_lines.append(f'| **{current_word}** | {text} |')
            word = entry_lower.group(1).strip()
            pos = entry_lower.group(2).strip()
            rest = stripped[entry_lower.end():].strip()
            current_word = f'{word} {pos} — UNNAPROVED'
            current_text = [rest] if rest else []
            continue

        # Page number / footer — skip
        if re.match(r'^(Issue \d+|Page \d+|Part \d+|2025-)', stripped):
            continue

        if current_word:
            current_text.append(stripped)

    # Flush final entry
    if current_word and current_text:
        text = ' '.join(current_text).replace('|', '\\|')
        md_lines.append(f'| **{current_word}** | {text} |')

    md_lines.append('')
    return '\n'.join(md_lines)


def extract_page_to_markdown(pdf_path, page_number):
    """Extract a single PDF page to advanced markdown."""
    pdf = pdfplumber.open(pdf_path)

    if page_number < 1 or page_number > len(pdf.pages):
        pdf.close()
        return None, None

    page = pdf.pages[page_number - 1]
    raw_text = page.extract_text() or ""
    tables = page.extract_tables() or []

    lines = raw_text.split('\n')
    total_pages = len(pdf.pages)
    pdf.close()

    # Build markdown
    md_lines = []
    md_lines.append(f"# Page {page_number} of {total_pages}\n")

    # Detect page type
    is_dict_page = sum(1 for line in lines if is_dictionary_entry(line)) > 2
    has_tables = len(tables) > 0

    # Process lines
    i = 0
    processed_table_regions = set()

    while i < len(lines):
        line = lines[i].rstrip()

        # Skip empty lines at boundaries
        if not line:
            md_lines.append('')
            i += 1
            continue

        # Check if this is a table region
        table_applied = False
        for table in tables:
            # Rough check: do the first cells of this table appear in the current text?
            if table and table[0]:
                first_cell = (table[0][0] or '').strip()
                if first_cell and first_cell in line:
                    # Render the table
                    table_md = format_table_as_markdown(table)
                    if table_md:
                        md_lines.append('')
                        md_lines.append(table_md)
                        md_lines.append('')
                        table_applied = True
                        # Skip lines until we're past the table content
                        skip_count = len(table)
                        i += skip_count
                        break

        if table_applied:
            continue

        # Heading detection
        if is_heading(line):
            stripped = line.strip()
            if stripped.isupper():
                # Preserve exact casing for acronyms like ASD-STE100
                md_lines.append(f"### {stripped}")
            else:
                md_lines.append(f"## {stripped}")
            i += 1
            continue

        # Dictionary entry detection
        if is_dictionary_entry(line):
            # Format as dictionary table
            remaining = lines[i:]
            md_lines.append(format_dictionary_page(remaining))
            break  # Rest of page is dictionary entries
            i += 1
            continue

        # STE example (all caps)
        if is_ste_example(line):
            md_lines.append(f'> **STE:** {line.strip()}')
            i += 1
            continue

        # List item
        if is_list_item(line):
            md_lines.append(f'{line.strip()}')
            i += 1
            # Collect continuation lines for this list item
            while i < len(lines) and lines[i].strip() and not is_list_item(lines[i]) and not is_heading(lines[i]):
                md_lines.append(f'  {lines[i].strip()}')
                i += 1
            continue

        # Regular paragraph text
        md_lines.append(line.strip())
        i += 1

    return collapse_blank_lines('\n'.join(md_lines)), raw_text


def collapse_blank_lines(markdown):
    """Collapse 3+ consecutive blank lines to max 2."""
    while '\n\n\n\n' in markdown:
        markdown = markdown.replace('\n\n\n\n', '\n\n\n')
    return markdown


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: extract_page.py <pdf_path> <page_number> <output_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    page_num = int(sys.argv[2])
    output_path = sys.argv[3]

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

    markdown, raw = extract_page_to_markdown(pdf_path, page_num)

    if markdown is None:
        print(f"ERROR: Page {page_num} not found in {pdf_path}")
        sys.exit(1)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"OK: Page {page_num} → {output_path} ({len(markdown)} chars)")
