#!/usr/bin/env python3
"""Generate adaptation worker prompts — one per rule section batch."""
import os, re

PROMPTS_DIR = ".agents/prompts/adapt"
os.makedirs(PROMPTS_DIR, exist_ok=True)

# Rule batches for adaptation (9 sections × ~6 rules each)
rule_batches = {
    "sec1": "Rules 1.1 through 1.14 — Words (14 rules)",
    "sec2": "Rules 2.1 through 2.2 — Multi-word Nouns (2 rules)",
    "sec3": "Rules 3.1 through 3.7 — Verbs (7 rules)",
    "sec4": "Rules 4.1 through 4.5 — Sentences (5 rules)",
    "sec5": "Rules 5.1 through 5.5 — Procedural Writing (5 rules)",
    "sec6": "Rules 6.1 through 6.5 — Descriptive Writing (5 rules)",
    "sec7": "Rules 7.1 through 7.3 — Safety Instructions (3 rules)",
    "sec8": "Rules 8.1 through 8.6 — Punctuation (6 rules)",
    "sec9": "Rules 9.1 through 9.4 + GR1-GR4 — Writing Practice (8 rules)",
}

prompt_template = """TASK: Adapt STE writing rules to STE-Code (code documentation domain).

Read ste-code/merged/master.md and find {section_name}. For each rule, produce an adapted file in ste-code/adapted/ with:

1. The original rule number and text from the spec
2. A code-domain rewrite of the rule (replace aerospace examples with code docs examples)
3. At least one STE/non-STE code-domain example pair
4. File naming: a-secN-ruleX.Y.md

RULES:
- Every adapted rule MUST reference its original rule number from master.md
- Every example MUST be an adaptation of a real STE/non-STE pair from the spec
- No invented code terms without a master.md source
- 19 categories (NOT 22), deepseek-v4-pro (NOT deepseek-pro)
- Never use "..." to abbreviate
- Output format:
  # Rule X.Y — [Title]
  > **Source:** Adapted from ASD-STE100 Issue 9, Rule X.Y
  
  ## Original Rule
  [the original rule text from the spec]
  
  ## STE-Code Adaptation
  [code-domain version of the rule]
  
  ### Examples
  > **Non-STE:** [code-domain non-compliant example]
  > **STE:** [code-domain compliant example]

Output ONLY the adapted markdown files. One file per rule.
"""

for batch_id, section_name in rule_batches.items():
    prompt = prompt_template.format(section_name=section_name)
    path = os.path.join(PROMPTS_DIR, f"adapt-{batch_id}.txt")
    with open(path, 'w') as f:
        f.write(prompt)

print(f"Generated {len(rule_batches)} adaptation prompts in {PROMPTS_DIR}/")
for b in sorted(rule_batches):
    print(f"  adapt-{b}.txt — {rule_batches[b]}")
