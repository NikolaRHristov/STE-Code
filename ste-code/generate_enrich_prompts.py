#!/usr/bin/env python3
"""Generate second-pass enrichment prompts for refined files."""
import os, re
from pathlib import Path

PROMPTS_DIR = ".agents/prompts/enrich"
os.makedirs(PROMPTS_DIR, exist_ok=True)

REFINED_DIR = Path("ste-code/refined")
def sort_key(fname):
    m = re.search(r'r(\d+)', fname)
    return int(m.group(1)) if m else 0
files = sorted(
    [f for f in os.listdir(REFINED_DIR) if f.startswith('r') and f.endswith('.md')],
    key=sort_key
)

# Split into 12 batches of ~9 files each
BATCH_SIZE = 10
batches = [files[i:i+BATCH_SIZE] for i in range(0, len(files), BATCH_SIZE)]

prompt_template = """TASK: Second-pass enrichment — elevate refined spec files to highest quality.

Read each of these files from ste-code/refined/ and apply ALL improvements below, overwriting each file with the enriched version:

{file_list}

ENRICHMENT RULES (apply to EVERY file):

1. DICTIONARY TAGGING: Every #### dictionary entry MUST end with " — APPROVED" (UPPERCASE word) or " — UNAPPROVED" (lowercase word). Scan each entry's heading text — if the word is in ALL CAPS, tag APPROVED; if lowercase, tag UNAPPROVED.

2. HEADING HIERARCHY: Rules MUST use ### (not ##). Dictionary entries use ####. Sections use ##. Fix all violations. Replace ## Rule X.Y with ### Rule X.Y.

3. RAW TABLE CONVERSION: If you find dictionary entries in raw table format (single-row | Word | Meaning | tables), convert them to proper #### WORD (POS) — APPROVED/UNAPPROVED format with - bullet lists for meanings, forms, STE examples, and Non-STE examples.

4. EXAMPLE COMPLETENESS: Every > **STE:** and > **Non-STE:** blockquote must contain the COMPLETE example text. Never use "..." to abbreviate. If the source has a partial example, complete it from context.

5. CROSS-REFERENCES: Where a rule mentions a dictionary word, add: > **See:** Dictionary entry for WORD (POS).

6. SPACING PERFECTION: 
   - Exactly one blank line after every heading (##, ###, ####)
   - Exactly one blank line before/after every table block
   - Exactly one blank line between sections
   - Never triple blank lines
   - Never two consecutive blank lines
   - No trailing whitespace on any line

7. CONSISTENCY: Ensure every file follows the exact same structure:
   - Line 1: # Page NNN of 434
   - Line 2: blank
   - Line 3: > **Source:** ASD-STE100 Issue 9, January 2025
   - Line 4: > **Pages:** NN–MM of 434
   - Line 5: blank
   - Then content with proper heading hierarchy

8. CONTENT PRESERVATION: Never delete content. Never summarize. Never truncate. Only ADD missing structure (tags, proper headings, complete examples). If content is missing from the source, note it but don't fabricate.

Output: Overwrite each input file with the enriched version. No commentary, no explanations — just the enriched markdown files.
"""

for i, batch in enumerate(batches):
    batch_id = i + 1
    file_list = "\n".join(f"- ste-code/refined/{f}" for f in batch)
    prompt = prompt_template.format(file_list=file_list)
    path = os.path.join(PROMPTS_DIR, f"enrich-batch{batch_id:02d}.txt")
    with open(path, 'w') as f:
        f.write(prompt)

print(f"Generated {len(batches)} enrichment prompts in {PROMPTS_DIR}/")
for i in range(len(batches)):
    print(f"  enrich-batch{i+1:02d}.txt — {len(batches[i])} files")
