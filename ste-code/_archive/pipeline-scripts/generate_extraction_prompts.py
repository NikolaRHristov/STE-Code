#!/usr/bin/env python3
"""Generate 109 extraction worker prompts for the STE-Code pipeline.

Uses the new page-dir/ naming convention with spec page identifiers.
Workers read 4 pages each from spec/issue-09-2025/page-dir/ and output
to ste-code/extracted/wNNN-pPPPP-PPPP.md
"""
import os
import re

OUTPUT_DIR = "ste-code/prompts"
SPEC_DIR = "spec/issue-09-2025"
PAGE_DIR = os.path.join(SPEC_DIR, "page-dir")
WORKERS = 109
PAGES_PER_WORKER = 4

# Read the MANIFEST to get the ordered list of page IDs
def get_page_ids():
    """Read MANIFEST.md and extract the ordered list of page IDs."""
    manifest_path = os.path.join(PAGE_DIR, "MANIFEST.md")
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"MANIFEST.md not found at {manifest_path}")
    
    page_ids = []
    with open(manifest_path, 'r') as f:
        for line in f:
            # Lines look like: | 1 | FRONT-MATTER | page-front-matter.md | 78 | 4024 |
            match = re.match(r'\|\s*\d+\s*\|\s*(.+?)\s*\|', line)
            if match:
                page_ids.append(match.group(1))
    
    return page_ids

os.makedirs(OUTPUT_DIR, exist_ok=True)

page_ids = get_page_ids()
print(f"Found {len(page_ids)} page IDs from MANIFEST.md")

# Worker rails block (W1-W10 from worker-rails.md)
WORKER_RAILS = """
WORKER RAILS (validate before writing output):
W1 — Page Header: Output starts with # Page N of M or **Page <ID>**
W2 — No Glued Headings: Blank line after every ### or #### heading
W3 — No Fabrication: Only text from the spec pages. No commentary, no modern terms.
W4 — Boilerplate Control: "ASD-STE100" only where it belongs.
W5 — STE/Non-STE Format: > **STE:** and > **Non-STE:** blockquote format
W6 — Tables Clean: Header row + separator row + data rows
W7 — Blank Line After Tables: Blank line after every table
W8 — No Triple Blanks: Zero instances of 3+ consecutive blank lines
W9 — Content Complete: Every word, number, and example from the source
W10 — Naming Correct: Output filename matches wNNN-pPPPP-PPPP.md
"""

template = (
    "Read {spec_page_dir}/page-{start_id}.md through page-{end_id}.md. "
    "Extract ALL content exactly into ste-code/extracted/w{wnum:03d}-p{start_pdf}-p{end_pdf}.md. "
    "Do not summarize. Include every word, every table, every example. "
    "Output ONLY the markdown file. "
    "Apply these worker rails: {rails}"
)

count = 0
for wnum in range(1, WORKERS + 1):
    start_idx = (wnum - 1) * PAGES_PER_WORKER
    end_idx = min(start_idx + PAGES_PER_WORKER, len(page_ids))
    
    if start_idx >= len(page_ids):
        break
    
    start_id = page_ids[start_idx]
    end_id = page_ids[end_idx - 1]
    
    # For the filename, use PDF page numbers (sequential 1-434)
    # The MANIFEST lists pages in order, so we can use the row number as the PDF page number
    start_pdf = start_idx + 1
    end_pdf = end_idx
    
    prompt = template.format(
        spec_page_dir=PAGE_DIR,
        start_id=start_id,
        end_id=end_id,
        wnum=wnum,
        start_pdf=start_pdf,
        end_pdf=end_pdf,
        rails=WORKER_RAILS.strip()
    )
    outfile = os.path.join(OUTPUT_DIR, f"w{wnum:03d}-prompt.txt")
    with open(outfile, "w") as f:
        f.write(prompt + "\n")
    count += 1

print(f"Generated {count} prompt files in {OUTPUT_DIR}/")
