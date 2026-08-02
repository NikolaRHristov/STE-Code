#!/usr/bin/env python3
"""Standardize Non-STE/STE markers across all adapted files.

Canonical format:
    > **Non-STE:** text
    > **STE:** text

Fixes:
1. > **Non-STE (Rule X.Y violation — description):** → > **Non-STE:**
2. > **STE-Code:** → > **STE:**
3. > **Non-STE (P11, P1 violation):** → > **Non-STE:**

Usage: python3 .agents/tools/maintenance/standardize-markers.py [--dry-run]
"""

import re, sys
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
ADAPTED_DIR = PROJECT / "ste-code" / "adapted"


def standardize_file(filepath, dry_run=False):
    """Standardize markers in one file. Returns (original, modified, changes)."""
    content = filepath.read_text()
    original = content
    changes = 0

    # Fix 1: Non-STE with parenthetical descriptions
    # Pattern: > **Non-STE (anything):** → > **Non-STE:**
    pattern_nonste = re.compile(r'> \*\*Non-STE\s*\([^)]*\):\*\*')
    new_content, n = pattern_nonste.subn('> **Non-STE:**', content)
    if n > 0:
        content = new_content
        changes += n

    # Fix 2: STE-Code → STE
    pattern_stecode = re.compile(r'> \*\*STE-Code:\*\*')
    new_content, n = pattern_stecode.subn('> **STE:**', content)
    if n > 0:
        content = new_content
        changes += n

    # Fix 3: Double spaces after markers
    pattern_doublespace = re.compile(r'(> \*\*(?:Non-STE|STE):\*\*)  +')
    new_content, n = pattern_doublespace.subn(r'\1 ', content)
    if n > 0:
        content = new_content
        changes += n

    if changes > 0 and not dry_run:
        write_text(filepath, content)

    return original, content, changes


def main():
    dry_run = "--dry-run" in sys.argv

    files = sorted(ADAPTED_DIR.glob("a-sec*.md"))
    total_changes = 0
    files_changed = 0

    for f in files:
        _, _, changes = standardize_file(f, dry_run=dry_run)
        if changes > 0:
            print(f"  {f.stem}: {changes} fixes")
            total_changes += changes
            files_changed += 1

    print(f"\nFiles changed: {files_changed}/{len(files)}")
    print(f"Total fixes: {total_changes}")
    if dry_run:
        print("DRY RUN — no files modified. Remove --dry-run to apply.")


if __name__ == "__main__":
    main()
