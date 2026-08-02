#!/usr/bin/env python3
"""Level 3 Assembly — ~20K tokens: section-specific grammar rules + dictionary excerpt.

Reads Level 5 summaries, extracts grammar-focused content per section.
Output: ste-code/artifacts/level3/system-prompt.txt

Usage: python3 .agents/tools/refinement/assemble-level3.py [--agent hermes|claude|codex] [--dry-run]
"""

import sys
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402
CFG = _load_config(__file__)
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

LEVEL5_DIR = PROJECT / "ste-code" / "artifacts" / "level5"
LEVEL3_DIR = PROJECT / "ste-code" / "artifacts" / "level3"
OUTPUT = LEVEL3_DIR / "system-prompt.txt"

# Section descriptions for grammar context
SECTION_GRAMMAR = {
    "sec1": "Words — approved vocabulary, parts of speech, technical nouns/verbs",
    "sec2": "Noun Phrases — article use, noun clusters",
    "sec3": "Verbs — tense, voice, mood, verb forms",
    "sec4": "Sentences — length, clarity, contractions, completeness",
    "sec5": "Procedures — instructional writing, step structure",
    "sec6": "Descriptions — descriptive writing, comparisons",
    "sec7": "Warnings — BREAKING, DEPRECATED, NOTE formatting",
    "sec8": "Punctuation — commas, hyphens, parentheses, lists",
    "sec9": "Document Structure — headings, lists, tables, organization",
}


def build_prompt():
    summaries = sorted(LEVEL5_DIR.glob("sec*/a-sec*/summary.md"))
    sections = {}
    for sf in summaries:
        sec = sf.parent.parent.name
        sections.setdefault(sec, []).append(str(sf.relative_to(PROJECT)))

    input_list = ""
    for sec in sorted(sections):
        desc = SECTION_GRAMMAR.get(sec, "")
        input_list += f"\n## {sec} — {desc}\n"
        for s in sections[sec]:
            input_list += f"  {s}\n"

    return f"""You are STE-Code. Assemble the Level 3 system prompt (~20,000 tokens).

Read ALL {len(summaries)} rule summaries from the Level 5 directory tree:

{input_list}

For each SECTION (not each rule), produce a compact grammar summary:
1. Section name and purpose (1 sentence)
2. Key grammar rules for that section (2-3 sentences)
3. One representative example pair per section

SECTIONS TO PRODUCE (9 sections):
{SECTION_GRAMMAR}

Then assemble:

## STE-Code Level 3 — Grammar-Focused

[Identity + attribution]

## Section Grammar Rules (9 sections)
[Each section: 3-4 sentences + 1 example pair]

## Vocabulary Quick Reference
[Top 30 approved words from ste-code/data/vocabulary/approved-verbs.json]

## Synonym Table
[Top 20 pairs from ste-code/data/synonym-table.json]

## Output Rules
[Active voice, sentence limits, anti-patterns]

---

> Adapted from ASD-STE100 Issue 9 (January 2025), ASD Europe. (c) ASD, 2025.
> STE is EU Trade Mark 017966390. Independent adaptation.

CRITICAL:
- Every example MUST have complete Non-STE and STE
- Target: 15,000–25,000 tokens
- Clean formatting, no mangled text
- Use write_file to save to: {OUTPUT}

Report: section count, example count, estimated tokens.
"""


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    dry_run = "--dry-run" in sys.argv
    prompt = build_prompt()
    print(f"Level 3 prompt: {len(prompt)} chars (~{len(prompt)//4} tokens)")

    if dry_run:
        print(f"\nWould process {len(list(LEVEL5_DIR.glob('sec*/a-sec*/summary.md')))} summaries")
        return

    LEVEL3_DIR.mkdir(parents=True, exist_ok=True)
    result = run_agent(prompt, agent=agent, model=CFG.model, cwd=PROJECT)
    print(f"Exit: {result.returncode}")
    if OUTPUT.exists():
        chars = OUTPUT.stat().st_size
        print(f"Output: {chars:,} chars (~{chars//4:,} tokens)")


if __name__ == "__main__":
    main()
