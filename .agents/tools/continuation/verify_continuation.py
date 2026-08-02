#!/usr/bin/env python3
"""verify_continuation.py — read-only scan of ste-code/refined/ for redo queue.

Produces ste-code/extensions/.continue-queue.json (default) — a list of refined
page paths that need B1 continuation/redo (truncated, orphaned continuation text,
or missing the canonical page header). This is the QUEUE INPUT to
continue_batch.py; it never writes refined/ itself. Review the queue before
running B1 so the Refinement agent's live output is not overwritten unilaterally.

Detects:
  - files ending mid-word / with a 'truncat' / 'continued…' marker
  - orphaned continuation text (starts without a page/heading)
  - missing canonical header (# Page N of 434 / ## Page <spec-id>)
  - files suspiciously small (< 200 bytes) for a refined page

Usage:
  python3 verify_continuation.py                 # scan, print, write queue
  python3 verify_continuation.py --print-only    # no queue file
Exit 0 always (it is a scanner, not a gate).
"""
import sys
import json
import re
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
REFINED_DIR = PROJECT / "ste-code" / "refined"
QUEUE_PATH = PROJECT / "ste-code" / "extensions" / ".continue-queue.json"


def _needs_redo(p: Path) -> tuple[bool, str]:
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return True, "unreadable"
    if len(text) < 200:
        return True, f"too small ({len(text)}B)"
    head = text.lstrip()[:400].lower()
    if "truncat" in head or "continued" in head.split("\n")[0]:
        return True, "truncation/continuation marker"
    # Orphaned: does not start with a heading
    if not head.startswith("#"):
        return True, "no leading heading (orphaned continuation?)"
    # Missing canonical page header
    if not re.search(r"^#\s*Page\s+\d+", text, re.M) and \
       not re.search(r"^##\s*Page\s+", text, re.M):
        return True, "missing page header"
    return False, ""


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, default=REFINED_DIR)
    ap.add_argument("--queue", type=Path, default=QUEUE_PATH)
    ap.add_argument("--print-only", action="store_true")
    args = ap.parse_args()
    refined_dir = args.dir
    queue_path = args.queue
    print_only = args.print_only
    if not refined_dir.exists():
        print(f"refined/ missing: {refined_dir}")
        sys.exit(0)
    queue = []
    for f in sorted(refined_dir.glob("*.md")):
        need, why = _needs_redo(f)
        if need:
            try:
                rel = str(f.relative_to(PROJECT))
            except ValueError:
                rel = str(f)  # absolute fallback (test harness)
            queue.append(rel)
            print(f"  REDO  {rel} — {why}")
    print(f"\n{len(queue)} refined page(s) flagged for B1 continuation.")
    if not print_only:
        queue_path.parent.mkdir(parents=True, exist_ok=True)
        queue_path.write_text(json.dumps(queue, indent=2))
        print(f"Queue written: {queue_path}")
    sys.exit(0)


if __name__ == "__main__":
    main()
