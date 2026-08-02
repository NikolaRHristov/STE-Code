#!/usr/bin/env python3
"""Gap Filler — generate missing Non-STE/STE example pairs for adapted rule files.

Audits all adapted files, identifies files with fewer than 8 example pairs,
and launches parallel workers to generate additional pairs.

Usage: python3 .agents/tools/maintenance/fill-gaps.py [--agent hermes|claude|codex] [--dry-run] [--min-pairs N]
"""

import os
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
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())

import sys as _sys
_sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import Templater
TPL = Templater(__file__)

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
    """Build prompt for a worker to generate example pairs.

    NOTE: previously this function returned rule_preview (a copy-paste bug);
    it now returns the rendered worker prompt.
    """
    rule_text = filepath.read_text()
    rule_name = filepath.stem.replace("a-", "")
    # Truncate rule text to keep prompt manageable (first 150 lines)
    rule_preview = "\n".join(rule_text.split("\n")[:150])

    return TPL.render(
        "fill-gaps-worker",
        rule_name=rule_name,
        current_pairs=current_pairs,
        needed=target_pairs - current_pairs,
        rule_preview=rule_preview,
        filepath=filepath,
    )


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

        prompt = TPL.render(
            "fill-gaps-batch",
            batch_num=i + 1,
            total_batches=len(batches),
            count=len(batch),
            file_list=file_list,
        )

        proc = launch_agent(prompt, agent=agent, model=os.environ.get("STE_MODEL", "poolside/laguna-s-2.1:free"), cwd=PROJECT)
        processes.append((i + 1, proc))
        print(f"Launched batch {i+1}/{len(batches)} ({len(batch)} files, PID {proc.pid})")

    print(f"\nWaiting for {len(processes)} gap-filler workers...")
    for batch_num, proc in processes:
        proc.communicate(timeout=900)
        print(f"  Batch {batch_num}: done")


if __name__ == "__main__":
    main()
