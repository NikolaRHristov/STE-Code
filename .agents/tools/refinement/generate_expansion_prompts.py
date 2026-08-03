#!/usr/bin/env python3
"""Generate expansion worker prompts for Agent #4 Pass 1 (Rule Examples).
Each prompt contains: system rules + agent protocol + task + input files + dedup blacklist."""

import os, glob, json

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path

_R = next(
    p
    for p in _Path(__file__).resolve().parents
    if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
from ste_io import write_text  # noqa: E402

PROMPTS_DIR = os.path.join(PROJECT, ".agents", "prompts", "expansion-pass1")
ADAPTED_DIR = os.path.join(PROJECT, "ste-code", "adapted")
MASTER_FILE = os.path.join(PROJECT, "ste-code", "merged", "master.md")
SYNONYM_FILE = os.path.join(PROJECT, "SCE", "core", "categories", "synonym-table.json")
DICT_FILE = os.path.join(PROJECT, "SCE", "data", "vocabulary", "code-dictionary.json")

os.makedirs(PROMPTS_DIR, exist_ok=True)

# Load base templates
with open(
    os.path.join(
        PROJECT, "ste-code", "artifacts", "ste-code-distilled-system-prompt.txt"
    )
) as f:
    SYSTEM_PROMPT = f.read()

with open(os.path.join(PROJECT, ".agents", "skills", "continuation", "SKILL.md")) as f:
    AGENT_PROTOCOL = f.read()

with open(SYNONYM_FILE) as f:
    SYNONYMS = json.load(f)

with open(DICT_FILE) as f:
    DICTIONARY = json.load(f)

# Build dedup blacklist from existing adapted files
dedup_examples = []
for af in sorted(glob.glob(os.path.join(ADAPTED_DIR, "a-sec*-*.md"))):
    with open(af) as f:
        content = f.read()
        # Extract STE/non-STE pairs
        import re

        pairs = re.findall(r"\*\*STE:\*\*\s*(.*?)(?:\n|$)", content)
        for p in pairs:
            if len(p) > 10 and len(p) < 200:
                dedup_examples.append(p.strip())

# Get adapted rule files grouped by section
sec_files = {}
for af in sorted(glob.glob(os.path.join(ADAPTED_DIR, "a-sec*-*.md"))):
    sec = af.split("/")[-1].split("-")[1].replace("sec", "")
    if sec not in sec_files:
        sec_files[sec] = []
    sec_files[sec].append(af)

# Generate prompts — one per rule file (each rule file gets 3-5 new examples)
batch_num = 0
for sec in sorted(sec_files.keys()):
    for fpath in sec_files[sec]:
        fname = os.path.basename(fpath).replace(".md", "")
        batch_num += 1

        with open(fpath) as f:
            rule_content = f.read()

        # Build dedup section (first 20 existing examples, grows with each batch)
        dedup_section = "\n".join(f"- {ex}" for ex in dedup_examples[:20])

        # Build synonym reference
        synonym_ref = "\n".join(
            f"  {p['approved']} → NOT: {', '.join(p['avoid'])}"
            for p in SYNONYMS["pairs"][:15]
        )

        prompt = f"""{SYSTEM_PROMPT}

{AGENT_PROTOCOL[:2000]}

═══════════════════════════════════════
TASK: Pass 1 — Rule Examples (Batch {batch_num})
═══════════════════════════════════════

Generate 3-5 NEW STE/non-STE code documentation example pairs for this rule.
Each new example must:
- Replace ALL aerospace terms (engine, aircraft, ream, flange, screw, etc.) with code-domain equivalents
- Follow the SAME principle violation → fix pattern as the original rule
- NOT match any example in the DEDUP BLACKLIST below
- Include an explanation of which principle (P1-P14) was applied

═══════════════════════════════════════
RULE TO EXPAND:
═══════════════════════════════════════
{rule_content[:4000]}

═══════════════════════════════════════
SYNONYM TABLE (use these):
═══════════════════════════════════════
{synonym_ref}

═══════════════════════════════════════
DEDUP BLACKLIST (do NOT generate these):
═══════════════════════════════════════
{dedup_section}

═══════════════════════════════════════
OUTPUT FORMAT (valid JSON only):
═══════════════════════════════════════
{{"pass": "rule-examples", "batch": {batch_num}, "rule_file": "{fname}", "entries": [
  {{"rule": "rule-X.Y", "principle": "P#", "ste_example": "...", "non_ste_example": "...", "explanation": "..."}}
]}}

Do NOT create files. Output JSON to stdout only.
"""
        prompt_file = os.path.join(PROMPTS_DIR, f"pass1-batch-{batch_num:03d}.txt")
        write_text(prompt_file, prompt)

print(f"Generated {batch_num} prompts in {PROMPTS_DIR}/")
print(f"Dedup blacklist: {len(dedup_examples)} existing examples loaded")
