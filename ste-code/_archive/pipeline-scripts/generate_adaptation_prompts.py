#!/usr/bin/env python3
"""Generate 11 adaptation worker prompts from master.md sections."""
import os

OUTPUT_DIR = "ste-code/prompts-adapt"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SECTIONS = [
    ("a001", "Section 1 — Words", "Rules 1.1 through 1.14", "a-sec1-rules.md"),
    ("a002", "Section 2 — Noun Clusters", "Rules 2.1 through 2.3", "a-sec2-rules.md"),
    ("a003", "Section 3 — Verbs", "Rules 3.1 through 3.7", "a-sec3-rules.md"),
    ("a004", "Section 4 — Sentences", "Rules 4.1 through 4.4", "a-sec4-rules.md"),
    ("a005", "Section 5 — Procedures", "Rules 5.1 through 5.5", "a-sec5-rules.md"),
    ("a006", "Section 6 — Descriptive Writing", "Rules 6.1 through 6.6", "a-sec6-rules.md"),
    ("a007", "Section 7 — Safety Instructions", "Rules 7.1 through 7.3", "a-sec7-rules.md"),
    ("a008", "Section 8 — Punctuation and Word Counts", "Rules 8.1 through 8.7", "a-sec8-rules.md"),
    ("a009", "Section 9 — Writing Practices + General Rules", "Rules 9.1-9.4 + GR1-GR4", "a-sec9-rules.md"),
    ("a010", "Technical Noun Categories", "All 19 categories with descriptions and examples", "a-categories.md"),
    ("a011", "Dictionary + Appendices", "Dictionary A-Z entries + change history + index + forms", "a-dictionary.md"),
]

template = (
    "Read ste-code/merged/master.md. Focus ONLY on <<SECTION>>: <<RULES>>. "
    "Adapt every rule, category, and example from aerospace to code documentation domain. "
    "PRESERVE: rule numbers, section structure, STE/non-STE pair format. "
    "REPLACE: aerospace examples with code examples (API docs, commit messages, README sections, code comments). "
    "For each rule: show original rule text, then code-domain rewrite, then STE/non-STE code example pairs. "
    "Every adapted rule MUST reference its original rule number from master.md. "
    "Write to ste-code/adapted/<<OUTPUT>>. Output ONLY the adaptation file."
)

count = 0
for worker_id, section, rules, output_file in SECTIONS:
    prompt = template.replace("<<SECTION>>", section).replace("<<RULES>>", rules).replace("<<OUTPUT>>", output_file)
    outfile = os.path.join(OUTPUT_DIR, f"{worker_id}-prompt.txt")
    with open(outfile, "w") as f:
        f.write(prompt + "\n")
    count += 1

print(f"Generated {count} adaptation prompts in {OUTPUT_DIR}/")
