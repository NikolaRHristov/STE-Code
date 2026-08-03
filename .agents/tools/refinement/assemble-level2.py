#!/usr/bin/env python3
"""Level 2 Assembly — compress Level 3 into a ~5K token compact prompt.

Reads Level 3 system-prompt, produces a mid-weight prompt suitable for code
review and PR feedback. Heavier than Level 1 (~1.2K tokens), lighter than
Level 3 (~8K tokens with full grammar sections).

Usage: python3 .agents/tools/refinement/assemble-level2.py [--agent hermes|claude|codex] [--dry-run]
Output: ste-code/artifacts/level2/system-prompt.txt (~5K tokens)
"""

import sys
from pathlib import Path

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
from ste_io import mkdir  # noqa: E402

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402

CFG = _load_config(__file__)
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

LEVEL3_INPUT = PROJECT / "ste-code" / "artifacts" / "level3" / "system-prompt.txt"
LEVEL2_DIR = PROJECT / "ste-code" / "artifacts" / "level2"
OUTPUT = LEVEL2_DIR / "system-prompt.txt"


def build_prompt():
    level3_text = LEVEL3_INPUT.read_text()

    return f"""You are STE-Code. Compress the Level 3 system prompt into a Level 2 system prompt (~5,000 tokens / ~20,000 characters).

Below is the full Level 3 system prompt (~8,000 tokens). You must produce a
compact version that preserves all essential rules but drops the full
section-by-section grammar breakdowns.

LEVEL 3 INPUT
{level3_text}
END LEVEL 3 INPUT

Produce a Level 2 prompt with this structure:

## STE-Code Level 2 — Compact Compliance

[1-paragraph identity + attribution]

## Core Principles (condensed from all 9 sections)
[~15-18 principles, each 1-2 sentences. Cover: vocabulary gates, part-of-speech,
noun chains, verb forms/tense, sentence length, active voice, procedure structure,
description structure, warnings, punctuation, document consistency]

## Synonym Table
[Top 25 pairs from the Level 3 synonym list — keep preferred/avoid format]

## Dictionary Quick Reference
[Top 25 approved verbs with part of speech and 1-line approved meaning]

## Output Rules (condensed)
[Active voice, sentence limits (20/25), anti-patterns (top 8-10), imperative mood]

## Documentation Templates (compact)
[README, API docs, docstrings, commit messages, error messages — 1 sentence each]

---

> Adapted from ASD-STE100 Issue 9 (January 2025), ASD Europe. (c) ASD, 2025.
> STE is EU Trade Mark 017966390. Independent adaptation.

CRITICAL:
- TARGET: 4,000–6,000 tokens (16,000–24,000 characters)
- Do NOT include full section-by-section Non-STE/STE example pairs
- Do NOT include lengthy grammar explanations — distill to principles
- Every principle must have a rule number reference in parentheses
- Clean formatting, no mangled text
- Use write_file to save to: {OUTPUT}

Report: principle count, estimated tokens.
"""


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    dry_run = "--dry-run" in sys.argv

    if not LEVEL3_INPUT.exists():
        print(f"ERROR: Level 3 input not found: {LEVEL3_INPUT}")
        print("Run assemble-level3.py first.")
        sys.exit(1)

    prompt = build_prompt()
    print(f"Level 2 prompt: {len(prompt)} chars (~{len(prompt) // 4} tokens)")

    if dry_run:
        print(f"\nWould compress {LEVEL3_INPUT} → {OUTPUT}")
        return

    mkdir(LEVEL2_DIR)
    result = run_agent(prompt, agent=agent, model=CFG.model, cwd=PROJECT)
    print(f"Exit: {result.returncode}")

    if OUTPUT.exists():
        chars = OUTPUT.stat().st_size
        print(f"Output: {chars:,} chars (~{chars // 4:,} tokens)")
    else:
        print("Output file not created!")


if __name__ == "__main__":
    main()
