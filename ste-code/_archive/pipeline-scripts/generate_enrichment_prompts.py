#!/usr/bin/env python3
"""Generate 109 enrichment prompts for second-pass extraction verification."""
import os

OUTPUT_DIR = "ste-code/prompts-enrich"
SPEC_DIR = "spec/issue-09-2025"
EXTRACTED_DIR = "ste-code/extracted"
ENRICHED_DIR = "ste-code/enriched"
WORKERS = 109
PAGES_PER_WORKER = 4

os.makedirs(OUTPUT_DIR, exist_ok=True)

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
    "Read ste-code/extracted/w{wnum:03d}-p{start}-{end}.md AND spec/issue-09-2025/page-{start:04d}.md through page-{end:04d}.md. "
    "Cross-reference: verify every word, table, example, rule number, and page footer matches source exactly. "
    "Fix any errors, missing content, broken tables, or wrong numbers. "
    "Add metadata header at top: <!-- section: {section_type} | pages: {start}-{end} | verified: true -->. "
    "Write enriched output to ste-code/enriched/w{wnum:03d}-p{start}-{end}.md. "
    "Do not summarize, paraphrase, or add commentary. Preserve all correct content as-is. "
    "Output ONLY the enriched markdown file."
)

count = 0
for wnum in range(1, WORKERS + 1):
    start = (wnum - 1) * PAGES_PER_WORKER + 1
    end = min(start + PAGES_PER_WORKER - 1, 434)
    if start > 434:
        break
    section_type = get_section_type(start, end)
    prompt = prompt_template.format(
        extracted_dir=EXTRACTED_DIR, enriched_dir=ENRICHED_DIR,
        spec_dir=SPEC_DIR, start=start, end=end, wnum=wnum,
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
    "DICT_A-F": "Verify every dictionary entry: word, POS, status, meaning, alternatives, examples. Table format intact.",
    "DICT_G-P": "Verify every dictionary entry: word, POS, status, meaning, alternatives, examples. Table format intact.",
    "DICT_Q-Z": "Verify every dictionary entry: word, POS, status, meaning, alternatives, examples. Table format intact.",
    "APPENDIX": "Verify change history, flowcharts, index, forms. All issue evolution data present.",
}

# Write section instructions reference
with open(os.path.join(OUTPUT_DIR, "section-instructions.md"), "w") as f:
    f.write("# Section-Specific Enrichment Instructions\n\n")
    for stype, instr in section_instructions.items():
        f.write(f"## {stype}\n{instr}\n\n")

print(f"Generated {count} enrichment prompts in {OUTPUT_DIR}/")
print(f"Section instructions: {OUTPUT_DIR}/section-instructions.md")
