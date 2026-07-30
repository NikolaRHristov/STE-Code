#!/usr/bin/env python3
"""Generate improved refinement prompts — section-aware, with embedded quality gates.
Reads enriched extracted files and produces highest-quality refined markdown.
"""
import os, re, glob
from pathlib import Path

ENRICHED = "ste-code/enriched"
PROMPTS_DIR = ".agents/prompts/refine"
os.makedirs(PROMPTS_DIR, exist_ok=True)

# Detect source: use enriched if complete, fall back to extracted
enriched_count = len(glob.glob(f"{ENRICHED}/w*-p*.md"))
SOURCE = ENRICHED if enriched_count >= 100 else "ste-code/extracted"
print(f"Source: {SOURCE} ({enriched_count} enriched, using {'enriched' if SOURCE == ENRICHED else 'extracted'})")

# Get all source files sorted by page number
def file_sort_key(x):
    m = re.search(r'w(\d+)', x)
    return int(m.group(1)) if m else 0

source_files = sorted(glob.glob(f"{SOURCE}/w*-p*.md"), key=file_sort_key)

# Section mapping — detect what each file contains
SECTIONS = {
    "FRONT": range(1, 11),      # w001-w010: front matter
    "RULES_S1": range(11, 18),  # w011-w017: Section 1 — Words
    "RULES_S2_S3": range(18, 28), # w018-w027: Sections 2-3
    "RULES_S4_S5": range(28, 38), # w028-w037: Sections 4-5
    "RULES_S6_S7": range(38, 45), # w038-w044: Sections 6-7
    "RULES_S8_S9_GR": range(45, 55), # w045-w054: Sections 8-9 + GR
    "DICT_A_E": range(55, 70),  # w055-w069: Dictionary A-E
    "DICT_F_L": range(70, 83),  # w070-w082: Dictionary F-L
    "DICT_M_R": range(83, 96),  # w083-w095: Dictionary M-R
    "DICT_S_Z": range(96, 110), # w096-w109: Dictionary S-Z + Appendices
}

# Common rules — applied to ALL sections
COMMON_RULES = """## UNIVERSAL RULES (apply to EVERY file)

1. **HEADER**: First line MUST be `# Page NNN of 434`. Second line blank. Third line `> **Source:** ASD-STE100 Issue 9, January 2025`. Fourth line `> **Pages:** NN–MM of 434`. Fifth line blank.

2. **SPACING**: Exactly one blank line after every heading (`#`, `##`, `###`, `####`). Exactly one blank line before and after every table block. Exactly one blank line between sections. Never two consecutive blank lines. Never trailing whitespace.

3. **HEADING HIERARCHY**: 
   - `#` — Page header only (line 1)
   - `##` — Major sections (Part 1, Part 2, Section N)
   - `###` — Rules, subsections
   - `####` — Dictionary entries, sub-subsections
   - Never use `#` or `##` for rules — rules are `### Rule X.Y`
   - Proper names like ASD-STE100 get `**bold**`, never `###`

4. **CONTENT**: Never delete a single word. Never summarize. Never use "..." to abbreviate examples. If source has 500 words, output must have ≥500 words. Every table cell, every example, every number preserved.

5. **TYPO FIX**: Replace ALL occurrences of `UNNAPROVED` with `UNAPPROVED` wherever found.

6. **OUTPUT ONLY**: No commentary, no "I have reformatted..." text. Just the refined markdown file."""

# Section-specific rules
SECTION_RULES = {
    "FRONT": """## FRONT MATTER RULES

- Convert FAQ entries to proper `#### Question?` format with answer text
- Copyright notices: preserve all text but format as `> ` blockquotes
- Highlight summaries: convert to `**bold**` list items
- Remove repeated "ASD-STE100 Simplified Technical English" page headers — keep only in metadata block
- Page break markers and repeated page numbers: remove all duplicates""",

    "RULES_S1": """## WRITING RULES — SECTION 1 (Words)

- Each rule: `### Rule X.Y — [Full Title]` followed by blank line, then rule text
- Examples format: `> **Non-STE:** [text]` / `> **STE:** [text]` as blockquote pairs
- Technical noun categories: format as numbered list `1. ` through `19. `
- Technical verb categories: same format
- Sub-rules and methods: use `####` level
- Cross-reference dictionary words mentioned in rules:
  `> **See:** Dictionary entry for WORD (POS)`""",

    "RULES_S2_S3": """## WRITING RULES — SECTIONS 2-3 (Nouns, Verbs)

- Each rule: `### Rule X.Y — [Full Title]`
- Verb form tables: convert to clean markdown tables with headers
- Tense examples: format as Non-STE/STE pairs
- Method descriptions: numbered `1. ` `2. ` `3. ` `4. `
- Active/passive voice examples: clearly labeled pairs""",

    "RULES_S4_S5": """## WRITING RULES — SECTIONS 4-5 (Sentences, Procedures)

- Each rule: `### Rule X.Y — [Full Title]`
- Procedural vs descriptive distinction: clearly label each example
- Word count limits: annotate examples with `[N words]` where the spec indicates
- Vertical list examples: proper markdown list formatting
- Safety instruction format: preserve WARNING/CAUTION/NOTE in ALL CAPS""",

    "RULES_S6_S7": """## WRITING RULES — SECTIONS 6-7 (Descriptive, Safety)

- Each rule: `### Rule X.Y — [Full Title]`
- Descriptive writing: gradual disclosure structure preserved
- Key words/phrases: underline or bold the key connectors
- Safety levels: WARNING (injury/death), CAUTION (damage) clearly labeled
- Risk explanations: preserve the "because" structure""",

    "RULES_S8_S9_GR": """## WRITING RULES — SECTIONS 8-9 + GR (Punctuation, Practice, Grammar)

- Each rule: `### Rule X.Y — [Full Title]` or `### GR-X — [Full Title]`
- Punctuation rules: examples showing correct/incorrect usage
- Word count rules: annotate with `[counts as N words]`
- GR rules: standard format like writing rules
- Practice rules: construction examples with before/after pairs""",

    "DICT_A_E": """## DICTIONARY — A through E

- EVERY entry: `#### WORD (POS) — APPROVED` (UPPERCASE) or `#### word (POS) — UNAPPROVED` (lowercase)
- Alphabetical section headers: `### A`, `### B`, `### C`, etc.
- APPROVED entries format:
  ```
  #### WORD (POS) — APPROVED
  - **Meaning:** [exact approved meaning]
  - **Forms:** [form1, form2, form3] (if verb/adjective)
  - **STE:** [STE example in ALL CAPS]
  ```
- UNAPPROVED entries format:
  ```
  #### word (POS) — UNAPPROVED
  - **Approved alternative:** ALTERNATIVE (POS)
  - **STE:** [example using approved alternative]
  - **Non-STE:** [example using unapproved word]
  ```
- Multiple alternatives: list each as separate `- **Approved alternative:**`
- Convert ALL raw PDF table entries to this format""",

    "DICT_F_L": """## DICTIONARY — F through L
[Same format as DICT_A_E — see rules above]
- EVERY entry tagged APPROVED or UNAPPROVED
- Alphabetical section headers: `### F`, `### G`, etc.
- Convert all raw tables to proper #### format""",

    "DICT_M_R": """## DICTIONARY — M through R
[Same format as DICT_A_E — see rules above]
- EVERY entry tagged APPROVED or UNAPPROVED
- Alphabetical section headers: `### M`, `### N`, etc.
- Convert all raw tables to proper #### format""",

    "DICT_S_Z": """## DICTIONARY — S through Z + Appendices
[Same format as DICT_A_E — see rules above]
- EVERY entry tagged APPROVED or UNAPPROVED
- Alphabetical section headers: `### S`, `### T`, etc.
- Appendices: format as `## Appendix N — [Title]`
- Change forms: preserve as tables or lists
- Convert all raw tables to proper #### format""",
}

# Self-verification checklist
SELF_CHECK = """## SELF-VERIFICATION (apply before writing output)

Check each of these and fix before outputting:
- [ ] First line is `# Page NNN of 434`
- [ ] Source line present with correct page range
- [ ] No "ASD-STE100 Simplified Technical English" repeated in body
- [ ] Every #### dictionary entry ends with `— APPROVED` or `— UNAPPROVED`
- [ ] No `UNNAPROVED` typos remain
- [ ] No `## Rule` headings — all rules use `###`
- [ ] No raw table rows with `| **word (POS)**` format — all converted to `####`
- [ ] No "..." abbreviations in examples
- [ ] No double blank lines
- [ ] File ends with exactly one newline"""

def worker_num(filepath):
    m = re.search(r'w(\d+)', os.path.basename(filepath))
    return int(m.group(1)) if m else 0

# Generate prompts
count = 0
for section_name, worker_range in SECTIONS.items():
    section_files = [f for f in source_files if worker_num(f) in worker_range]
    
    if not section_files:
        continue
    
    # Split into batches of 3
    for batch_start in range(0, len(section_files), 3):
        batch = section_files[batch_start:batch_start+3]
        count += 1
        
        file_list = "\n".join(f"- {f}" for f in batch)
        output_list = "\n".join(
            f"- ste-code/refined/{os.path.basename(f).replace('w', 'r')}" 
            for f in batch
        )
        
        prompt = f"""TASK: Refine extracted spec files into highest-quality standardized markdown.

INPUT FILES:
{file_list}

OUTPUT FILES:
{output_list}

{COMMON_RULES}

{SECTION_RULES[section_name]}

{SELF_CHECK}

IMPORTANT: Output ONLY the refined markdown files. No explanations, no commentary, no preambles. Write each file completely before moving to the next.
"""
        
        out_path = os.path.join(PROMPTS_DIR, f"refine-{count:03d}.txt")
        with open(out_path, 'w') as f:
            f.write(prompt)

print(f"Generated {count} refinement prompts in {PROMPTS_DIR}/")
print(f"Source: {SOURCE} ({len(source_files)} files)")
