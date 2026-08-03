#!/usr/bin/env python3
"""Level 4 Assembly — read Level 5 summaries, assemble compact ~50K prompt.

Designed for a new session. One poll worker reads all 51 Level 5 summaries,
extracts compact versions, and assembles with synonym table + dictionary.

Usage: python3 .agents/tools/refinement/assemble-level4.py [--agent hermes|claude|codex] [--dry-run]
Output: ste-code/artifacts/level4/system-prompt.txt (~50K tokens)
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

LEVEL5_DIR = PROJECT / "ste-code" / "artifacts" / "level5"
LEVEL4_DIR = PROJECT / "ste-code" / "artifacts" / "level4"
OUTPUT = LEVEL4_DIR / "system-prompt.txt"


def build_prompt():
    summaries = sorted(LEVEL5_DIR.glob("sec*/a-sec*/summary.md"))
    sections = {}
    for sf in summaries:
        sec = sf.parent.parent.name
        sections.setdefault(sec, []).append(str(sf.relative_to(PROJECT)))

    input_list = ""
    for sec in sorted(sections):
        input_list += f"\n## Section {sec.replace('sec', '')}\n"
        for s in sections[sec]:
            input_list += f"  {s}\n"

    return f"""You are STE-Code. Assemble the Level 4 system prompt (~50,000 tokens).

Read ALL {len(summaries)} rule summaries from the Level 5 directory tree:

{input_list}

For each rule, extract a compact 3-4 sentence version that includes:
1. Rule title and number
2. What the rule requires (1 sentence)
3. One Non-STE/STE example pair (complete, with both versions)

Then assemble the final prompt with this structure:

## STE-Code Level 4 — Standard Compliance

[Identity + attribution paragraph]

## Rules (51 rules)
[Each rule as a compact ~3 sentence block with 1 example pair]

## Synonym Table
[Read from ste-code/data/synonym-table.json — top 50 pairs]

## Dictionary Excerpt
[Minimum 60 approved words with meanings, code-domain examples, and usage notes.
Read ste-code/adapted/a-dictionary.md — at least lines 1-800 (the file is 5,943 lines).
For each word include: UPPERCASE word, part of speech, approved meaning, and a code-domain example sentence.
This section should be ~15,000-20,000 tokens.]

## Output Rules
[Active voice, sentence length, anti-patterns]

---

> Adapted from ASD-STE100 Issue 9 (January 2025), ASD Europe. (c) ASD, 2025.
> STE is EU Trade Mark 017966390. Independent adaptation.

CRITICAL:
- Every Non-STE MUST have a complete STE correction
- TARGET IS MANDATORY: 40,000–55,000 tokens (characters / 4)
- If output is below 40,000 tokens, ADD more dictionary entries (up to 120 approved words from lines 1-1500 of a-dictionary.md), ADD more synonym pairs (up to 100), and ADD a second Non-STE/STE example pair for rules that need it
- Clean paragraph breaks, no mangled text
- Use write_file to save to: {OUTPUT}
- After writing the file, verify: if file size is below 160,000 chars (40K tokens), you have NOT completed the task — expand and rewrite

Report: rule count, total tokens, example count.
"""


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    dry_run = "--dry-run" in sys.argv
    prompt = build_prompt()
    print(f"Level 4 prompt: {len(prompt)} chars (~{len(prompt) // 4} tokens)")

    if dry_run:
        print(
            f"\nWould process {len(list(LEVEL5_DIR.glob('sec*/a-sec*/summary.md')))} summaries"
        )
        return

    mkdir(LEVEL4_DIR)
    result = run_agent(prompt, agent=agent, model=CFG.model, cwd=PROJECT)
    print(f"Exit: {result.returncode}")
    if result.stdout:
        print(result.stdout[-500:])
    if OUTPUT.exists():
        chars = OUTPUT.stat().st_size
        print(f"\nOutput: {chars:,} chars (~{chars // 4:,} tokens)")
    else:
        print("\nOutput file not created!")


if __name__ == "__main__":
    main()
