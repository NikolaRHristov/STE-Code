#!/usr/bin/env python3
"""Gap Filler — generate missing Non-STE/STE example pairs for adapted rule files.

Audits all adapted files, identifies files with fewer than 8 example pairs,
and launches parallel workers to generate additional pairs.

Usage: python3 .agents/tools/maintenance/fill-gaps.py [--agent hermes|claude|codex] [--dry-run] [--min-pairs N]
"""

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())

ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
TMP_DIR = PROJECT / ".agents" / "tmp" / "gaps"
MIN_PAIRS = 8  # Target minimum example pairs per file


def count_pairs(filepath):
    """Count Non-STE/STE example pairs in a file."""
    content = filepath.read_text()
    return content.count("> **Non-STE:**")


def find_gaps(min_pairs=MIN_PAIRS):
    """Find files with fewer than min_pairs example pairs."""
    gaps = []
    for f in sorted(ADAPTED_DIR.glob("a-sec*.md")):
        pairs = count_pairs(f)
        if pairs < min_pairs:
            gaps.append((f, pairs))
    return gaps


def build_worker_prompt(filepath, current_pairs, target_pairs):
    """Build prompt for a worker to generate example pairs."""
    rule_text = filepath.read_text()
    rule_name = filepath.stem.replace("a-", "")
    # Truncate rule text to keep prompt manageable (first 150 lines)
    rule_preview = "\n".join(rule_text.split("\n")[:150])

    return f"""You are STE-Code. Generate additional Non-STE/STE example pairs for this rule.

RULE: {rule_name}
CURRENT PAIRS: {current_pairs}
TARGET: Generate {target_pairs - current_pairs} more pairs

RULE CONTENT (first 150 lines):
```
{rule_preview}
```

TASK:
1. Read the full file at: {filepath}
2. Understand the rule's requirements
3. Generate {target_pairs - current_pairs} new Non-STE/STE example pairs
4. Each pair must have:
   - A Non-STE version (realistic code documentation that violates the rule)
   - An STE version (the corrected, compliant version)
5. Insert the new pairs into the Examples section using patch
6. If an Examples section does not exist, create one

EXAMPLE PAIR FORMAT:
> **Non-STE:** [The non-compliant code documentation text]
> **STE:** [The STE-Code compliant correction]

CRITICAL:
- Each Non-STE must be a REALISTIC example from code documentation
- Each STE must be a COMPLETE, grammatically correct correction
- Use approved STE-Code vocabulary (prefer: use, start, stop, show, make, get, set, check, do)
- Follow sentence length limits (20 procedural, 25 descriptive)
- Use active voice, no semicolons, no contractions
- Cover different documentation types: README, API docs, docstrings, commit messages, error messages
- If you cannot generate a good example for a specific scenario, use:
  > [PLACEHOLDER: <scenario description>]

After generating pairs, report: how many pairs were added, file state.
"""
    return rule_preview  # Return just the prompt


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    min_pairs = MIN_PAIRS
    for i, arg in enumerate(sys.argv):
        if arg == "--min-pairs" and i + 1 < len(sys.argv):
            min_pairs = int(sys.argv[i + 1])

    dry_run = "--dry-run" in sys.argv

    gaps = find_gaps(min_pairs)
    print(f"Files with < {min_pairs} example pairs: {len(gaps)}")
    for f, pairs in gaps:
        print(f"  {f.stem}: {pairs} pairs ({f.stat().st_size:,} bytes)")

    if dry_run:
        print("\nDry run. Use without --dry-run to fill gaps.")
        return

    TMP_DIR.mkdir(parents=True, exist_ok=True)

    # Group into batches of 4 files per worker
    batch_size = 4
    batches = [gaps[i:i+batch_size] for i in range(0, len(gaps), batch_size)]

    processes = []
    for i, batch in enumerate(batches):
        batch_files = [f for f, _ in batch]
        file_list = "\n".join(f"  {f.stem} (current: {p} pairs)" for f, p in batch)

        prompt = f"""You are STE-Code Gap Filler (batch {i+1}/{len(batches)}).

Generate additional Non-STE/STE example pairs for these {len(batch)} rule files:
{file_list}

For each file:
1. Read the file with read_file
2. Find where examples are or where they should go
3. Generate 5-10 new Non-STE/STE example pairs for each rule
4. Use patch to insert them into the file
5. Format each pair as:
   > **Non-STE:** [realistic code doc that violates the rule]
   > **STE:** [STE-Code compliant correction]

CRITICAL:
- Use approved vocabulary, active voice, sentence length limits
- Cover different doc types: README, API, docstrings, commits, errors
- If you cannot generate a good example, use: [PLACEHOLDER: description]
  (leave these for later training — do NOT fabricate)
- Only add pairs where you are confident the correction is correct

Report for each file: pairs added, any placeholders used.
"""

        proc = launch_agent(prompt, agent=agent, model="poolside/laguna-s-2.1:free", cwd=PROJECT)
        processes.append((i + 1, proc))
        print(f"Launched batch {i+1}/{len(batches)} ({len(batch)} files, PID {proc.pid})")

    print(f"\nWaiting for {len(processes)} gap-filler workers...")
    for batch_num, proc in processes:
        proc.communicate(timeout=900)
        print(f"  Batch {batch_num}: done")


if __name__ == "__main__":
    main()
