#!/usr/bin/env python3
"""STRICT content-preservation guard for STE-Code pipeline.

This is the enforcement layer. It runs BEFORE a worker touches a file and
AFTER it finishes. Any violation = hard fail, no exceptions.

The 6 strict rules (injected into every worker prompt via STRICT_RULES below):

R1 — VERBATIM ORIGINAL: Extraction output MUST be byte-faithful to source
    page files. No summarization, no "cleanup", no reformatting beyond the
    exact markdown the spec uses (tables, <br>, **bold**).

R2 — TABLE INTEGRITY: A table row is an atomic unit. Never split a row across
    files. Never merge two tables. Never reorder columns. If a table spans a
    page boundary, emit `<!-- TABLE CONTINUES ON NEXT PAGE -->` and continue.

R3 — NO FREELANCE: Workers do NOT add commentary, examples, headers, footers,
    section titles, or "helpful" notes. Output = exactly the extracted content
    + the required `# Page N of 434` / `**Page X**` markers. Nothing else.

R4 — NO CROSS-FILE WRITES: A worker writes exactly ONE output file. It never
    touches another worker's file. Appends to shared group files are done ONLY
    via the lock-group.sh mechanism, never directly.

R5 — RE-BATCH IDEMPOTENCE: Re-running a worker MUST produce identical output.
    If the file already exists and passes verify-batch.py, the worker SKIPS.
    No "improvements", no re-formatting of existing files.

R6 — CONTEXT WINDOW SAFETY: If 4 pages exceed the model's safe context, the
    worker MUST request a smaller page range (2 pages) rather than truncate.
    Truncation is a hard fail. Partial output is NEVER written.

Usage:
  python3 .agents/tools/quality/strict-guard.py check <file>     # verify a file is clean
  python3 .agents/tools/quality/strict-guard.py emit-rules     # print STRICT_RULES for prompt injection
  python3 .agents/tools/quality/strict-guard.py scan <dir>      # scan all files in dir

Exit: 0 = clean, 2 = violation found
"""

import argparse
import json
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

STRICT_RULES = """STRICT EXTRACTION RULES — VIOLATION = HARD FAIL:
R1: Output MUST be verbatim from source pages. No summary, no cleanup, no reformat.
R2: Table rows are atomic. Never split/merge/reorder. Use <!-- TABLE CONTINUES ON NEXT PAGE --> at spans.
R3: NO freelance content — no commentary, examples, headers, footers, or notes. Only # Page N + **Page X** + verbatim body.
R4: Write exactly ONE file. Never touch another worker's file. Shared appends use lock-group.sh only.
R5: Re-runs are idempotent. If output exists and is valid, SKIP. No "improvements".
R6: If context is too small for 4 pages, request 2 pages. NEVER truncate. Never write partial output."""


def check_file(filepath: Path) -> list:
    """Return list of violations (empty = clean)."""
    violations = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return [f"read_error: {e}"]

    lines = content.split("\n")

    # R3: Detect freelance commentary (heuristic — non-spec phrasing)
    freelance_patterns = [
        r"^Here is the extraction",
        r"^I have extracted",
        r"^This page describes",
        r"^Below is",
        r"^Note:",
        r"^Summary:",
        r"^The following content",
        r"shutting down",
        r"Let me (check|verify|confirm)",
    ]
    for i, line in enumerate(lines[:5]):  # Check first 5 lines (preface area)
        for pat in freelance_patterns:
            if re.match(pat, line.strip(), re.I):
                violations.append(f"R3: freelance preface at L{i+1}: {line[:60]!r}")

    # R1/R2: Table column consistency
    header_cols = None
    for i, line in enumerate(lines):
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
                header_cols = len(cells)
            elif header_cols and len(cells) != header_cols:
                # Could be intentional (continuation) — only flag if NOT preceded by marker
                prev = lines[i - 1] if i > 0 else ""
                if "<!-- TABLE CONTINUES" not in prev:
                    violations.append(f"R2: column mismatch at L{i+1}: got {len(cells)}, expected {header_cols}")

    # R6: Truncation signal — file ends mid-table or mid-word without page marker
    last_content = lines[-1].strip() if lines else ""
    if last_content.startswith("|") and not last_content.strip().endswith("|"):
        violations.append("R6: possible truncation — last line is incomplete table row")

    return violations


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["check", "emit-rules", "scan"])
    ap.add_argument("target", nargs="?", default=".")
    args = ap.parse_args()

    if args.action == "emit-rules":
        print(STRICT_RULES)
        sys.exit(0)

    if args.action == "check":
        f = Path(args.target)
        if not f.exists():
            print(f"ERROR: {f} not found", file=sys.stderr)
            sys.exit(2)
        v = check_file(f)
        if v:
            for x in v:
                print(f"VIOLATION: {x}")
            sys.exit(2)
        else:
            print(f"CLEAN: {f}")
            sys.exit(0)

    if args.action == "scan":
        d = Path(args.target)
        files = sorted(d.rglob("*.md"))
        total_v = 0
        for f in files:
            v = check_file(f)
            if v:
                total_v += len(v)
                for x in v:
                    print(f"{f.relative_to(PROJECT)}: {x}")
        if total_v:
            print(f"\n{total_v} violations found")
            sys.exit(2)
        else:
            print("All files clean")
            sys.exit(0)


if __name__ == "__main__":
    main()
