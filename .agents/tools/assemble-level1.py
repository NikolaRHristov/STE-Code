#!/usr/bin/env python3
"""Level 1 Assembly — compress Level 2 into a ~1.2K token ultra-compact prompt.

Reads Level 2 system-prompt, produces the lightest-weight prompt suitable for
interactive sessions and low-context scenarios.

Usage: python3 .agents/tools/assemble-level1.py [--dry-run]
Output: ste-code/artifacts/level1/system-prompt.txt (~1.2K tokens)
"""

import os, sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
LEVEL2_INPUT = PROJECT / "ste-code" / "artifacts" / "level2" / "system-prompt.txt"
LEVEL1_DIR = PROJECT / "ste-code" / "artifacts" / "level1"
OUTPUT = LEVEL1_DIR / "system-prompt.txt"
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"

os.makedirs(LEVEL1_DIR, exist_ok=True)


def build_prompt():
    level2_text = LEVEL2_INPUT.read_text()

    return f"""You are STE-Code. Compress the Level 2 system prompt into a Level 1 system prompt (~1,200 tokens / ~5,000 characters).

Below is the full Level 2 system prompt (~4,500 tokens). You must produce an
ultra-compact version that preserves only the most essential rules.

=== LEVEL 2 INPUT ===
{level2_text}
=== END LEVEL 2 INPUT ===

Produce a Level 1 prompt with this structure:

## STE-Code Level 1 — Essential Principles

[1-line identity + 1-line attribution]

## Core Principles
[Exactly 14 principles, each 1 sentence. Cover: vocabulary gates, part-of-speech,
single meaning, noun chain limit (3), verb tenses (6 only), active voice,
sentence length (20/25), one instruction per step, condition before command,
warnings with consequences, no semicolons, no contractions, consistent
terminology, no phrasal verbs. Each with rule ref in parens.]

## Synonym Table
[Top 15 pairs — short format: "use X, not Y, Z"]

## Output Rules
[Active voice, sentence limits, imperative mood — 3-4 lines]

## Critical Anti-Patterns
[Top 8 — one line each]

---

> Adapted from ASD-STE100 Issue 9 (January 2025), ASD Europe. (c) ASD, 2025.
> STE is EU Trade Mark 017966390. Independent adaptation.

CRITICAL:
- TARGET: 900–1,500 tokens (3,600–6,000 characters)
- Be ruthless — cut everything non-essential
- No dictionary entries, no doc structure, no templates
- No verbose explanations — one sentence per principle
- Synonyms in compact format: "use X, not Y, Z"
- Use write_file to save to: {OUTPUT}

Report: principle count, estimated tokens.
"""


def main():
    dry_run = "--dry-run" in sys.argv

    if not LEVEL2_INPUT.exists():
        print(f"ERROR: Level 2 input not found: {LEVEL2_INPUT}")
        print("Run assemble-level2.py first.")
        sys.exit(1)

    prompt = build_prompt()
    print(f"Level 1 prompt: {len(prompt)} chars (~{len(prompt)//4} tokens)")

    if dry_run:
        print(f"\\nWould compress {LEVEL2_INPUT} → {OUTPUT}")
        return

    tmp = PROJECT / ".agents" / "tmp" / "level1-assemble.txt"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(prompt)

    import subprocess
    result = subprocess.run(
        [VENV_PYTHON, str(WRAPPER), str(tmp), "--model", "deepseek-v4-pro"],
        cwd=str(PROJECT), capture_output=True, text=True, timeout=600,
        env={**os.environ, "HERMES_REASONING_EFFORT": "high"},
    )
    print(f"Exit: {result.returncode}")

    if OUTPUT.exists():
        chars = OUTPUT.stat().st_size
        print(f"Output: {chars:,} chars (~{chars//4:,} tokens)")
    else:
        print("Output file not created!")


if __name__ == "__main__":
    main()
