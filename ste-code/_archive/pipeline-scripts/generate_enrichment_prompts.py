#!/usr/bin/env python3
"""Generate 109 enrichment prompts for second-pass extraction verification.

Uses the new page-dir/ naming convention with spec page identifiers.
Workers cross-reference extracted output against source page files.
"""
import os
import re

OUTPUT_DIR = "ste-code/prompts-enrich"
SPEC_DIR = "spec/issue-09-2025"
PAGE_DIR = os.path.join(SPEC_DIR, "page-dir")
EXTRACTED_DIR = "ste-code/extracted"
ENRICHED_DIR = "ste-code/enriched"
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
            match = re.match(r'\|\s*\d+\s*\|\s*(.+?)\s*\|', line)
            if match:
                page_ids.append(match.group(1))
    
    return page_ids

os.makedirs(OUTPUT_DIR, exist_ok=True)

page_ids = get_page_ids()
print(f"Found {len(page_ids)} page IDs from MANIFEST.md")

# Section type mapping for metadata enrichment
SECTION_TYPES = {
    (1, 12): "FRONT",
    (13, 16): "TOC",
    (17, 24): "INDEX",
    (25, 42): "INTRO",
    (43, 66): "RULES+CAT",
    (67, 94): "RULES",
    (95, 128): "RULES",
    (129, 240): "DICT_A-F",
    (241, 300): "DICT_G-P",
    (301, 360): "DICT_Q-Z",
    (361, 434): "APPENDIX",
}

def get_section_type(start, end):
    for (s, e), stype in SECTION_TYPES.items():
        if start <= e and end >= s:
            return stype
    return "UNKNOWN"

prompt_template = (
    "Read ste-code/extracted/w{wnum:03d}-p{start_pdf}-{end_pdf}.md AND "
    "{page_dir}/page-{start_id}.md through page-{end_id}.md. "
    "Cross-reference: verify every word, table, example, rule number, and page footer matches source exactly. "
    "Fix any errors, missing content, broken tables, or wrong numbers. "
    "Add metadata header at top: <!-- section: {section_type} | pages: {start_pdf}-{end_pdf} | verified: true -->. "
    "Write enriched output to ste-code/enriched/w{wnum:03d}-p{start_pdf}-{end_pdf}.md. "
    "Do not summarize, paraphrase, or add commentary. Preserve all correct content as-is. "
    "Output ONLY the enriched markdown file."
)

count = 0
for wnum in range(1, WORKERS + 1):
    start_idx = (wnum - 1) * PAGES_PER_WORKER
    end_idx = min(start_idx + PAGES_PER_WORKER, len(page_ids))
    
    if start_idx >= len(page_ids):
        break
    
    start_id = page_ids[start_idx]
    end_id = page_ids[end_idx - 1]
    start_pdf = start_idx + 1
    end_pdf = end_idx
    
    section_type = get_section_type(start_pdf, end_pdf)
    prompt = prompt_template.format(
        wnum=wnum,
        start_pdf=start_pdf,
        end_pdf=end_pdf,
        start_id=start_id,
        end_id=end_id,
        page_dir=PAGE_DIR,
        section_type=section_type
    )
    outfile = os.path.join(OUTPUT_DIR, f"w{wnum:03d}-enrich.txt")
    with open(outfile, "w") as f:
        f.write(prompt + "\n")
    count += 1

# Also generate section-type-specific enrichment instructions
section_instructions = {
    "FRONT": "Verify title page, copyright, EU trademark, highlights table. Every row must match source.",
    "TOC": "Verify table of contents structure. All page references must be exact.",
    "INDEX": "Verify subject-to-rule index mappings. Every entry must match source.",
    "INTRO": "Verify Q&A format, reference documents list, release history table.",
    "RULES+CAT": "Verify all rules AND categories. Every rule number, STE/non-STE pair must be exact.",
    "RULES": "Verify rule statements, examples, explanatory text. Page boundary continuations must be complete.",
    "DICT_A-F": "Verify every dictionary entry: word, POS, status, meaning, forms, alternatives, examples. Table format intact.",
    "DICT_G-P": "Verify every dictionary entry: word, POS, status, meaning, forms, alternatives, examples. Table format intact.",
    "DICT_Q-Z": "Verify every dictionary entry: word, POS, status, meaning, forms, alternatives, examples. Table format intact.",
    "APPENDIX": "Verify change history, flowcharts, index, forms. All issue evolution data present.",
}

# Write section instructions reference
with open(os.path.join(OUTPUT_DIR, "section-instructions.md"), "w") as f:
    f.write("# Section-Specific Enrichment Instructions\n\n")
    for stype, instr in section_instructions.items():
        f.write(f"## {stype}\n{instr}\n\n")

print(f"Generated {count} enrichment prompts in {OUTPUT_DIR}/")
print(f"Section instructions: {OUTPUT_DIR}/section-instructions.md")
