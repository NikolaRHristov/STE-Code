#!/usr/bin/env python3
"""Pre-generate enhanced Phase A prompts for a range of batches.

Usage:
  python3 .agents/tools/runners/phase-a-gen.py <start-batch> [end-batch]

Generates enhanced prompt files in .agents/tmp/phase-a-<worker-id>.txt

The creative-license and execution blocks are externalized to templates/ so they
can be edited without touching this script.
"""

import re
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
from ste_io import write_text  # noqa: E402
PROMPTS_DIR = PROJECT / ".agents" / "prompts" / "maturity-fixes"
TMP_DIR = PROJECT / ".agents" / "tmp"

# External markdown blocks live in templates/ (edit those, not the f-strings).
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import Templater
TPL = Templater(__file__)


def enhance_prompt(prompt_text):
    """Add creative license and write_file tool instruction."""
    m = re.search(r'TARGET FILE:\s*(\S+)', prompt_text)
    target = m.group(1) if m else None
    if not target:
        return None, None

    creative_block = TPL.render("phase-a-creative-block")
    tool_block = TPL.render("phase-a-execution-block", target=target)

    if 'Do NOT create files. Output the improved file content to stdout only.' in prompt_text:
        enhanced = prompt_text.replace(
            'Do NOT create files. Output the improved file content to stdout only.',
            creative_block + tool_block
        )
    else:
        enhanced = prompt_text + "\n" + creative_block + tool_block

    return enhanced, target


def main():
    if len(sys.argv) < 2:
        print("Usage: phase-a-gen.py <start-batch> [end-batch]")
        sys.exit(1)

    start = int(sys.argv[1])
    end = int(sys.argv[2]) if len(sys.argv) > 2 else start

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    all_prompts = sorted(PROMPTS_DIR.glob("fix-*.txt"))

    for batch_num in range(start, end + 1):
        start_idx = (batch_num - 1) * 3
        batch_prompts = all_prompts[start_idx:start_idx + 3]

        print(f"Batch {batch_num}:")
        for prompt_file in batch_prompts:
            worker_id = prompt_file.stem
            prompt_text = prompt_file.read_text()
            enhanced, target = enhance_prompt(prompt_text)

            if not enhanced:
                print(f"  ✗ {worker_id}: No target found")
                continue

            tmp_path = TMP_DIR / f"phase-a-{worker_id}.txt"
            write_text(tmp_path, enhanced)
            print(f"  ✓ {worker_id} → {target} ({len(enhanced)} chars)")

    print(f"\nAll prompts for batches {start}-{end} generated in {TMP_DIR}/")


if __name__ == "__main__":
    main()
