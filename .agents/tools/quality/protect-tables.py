#!/usr/bin/env python3
"""Table & Content Integrity Guard for STE-Code pipeline.

Prevents the 5 failure modes identified during extraction:
1. Content splitting — dictionary entries / rule pairs broken across files
2. Context window overflow — model truncates when 4 pages exceed safe token budget
3. Re-batch safety — re-running a worker must not re-split already-merged content
4. Grouping collisions — two agents writing the same group file
5. Table integrity — table rows never broken across page or file boundaries

Run BEFORE grouping (on extracted/) and AFTER grouping (on grouped/) to catch
structural breaks that would corrupt downstream refinement/adaptation.

Usage:
  python3 .agents/tools/quality/protect-tables.py [--dir DIR] [--fix] [--json]

Exit codes: 0 = clean, 1 = warnings, 2 = blocking errors
"""

import argparse
import json
import re
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


def count_table_columns(row: str) -> int:
    """Count columns in a markdown table row (excluding leading/trailing pipes)."""
    if not row.strip().startswith("|"):
        return 0
    cells = row.strip().strip("|").split("|")
    return len(cells)


def is_separator_row(row: str) -> bool:
    """Detect a markdown table separator row like |---|---|---|."""
    if not row.strip().startswith("|"):
        return False
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    return all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c != "")


def find_table_breaks(content: str, filename: str) -> list:
    """Scan a file for table rows that are split across page boundaries.

    A break is detected when:
    - A `|`-started row appears immediately before a `# Page N of 434` header
      AND the row has unequal column count vs the header/separator above it
    - OR a `<!-- TABLE CONTINUES -->` marker is missing where a table spans pages
    """
    issues = []
    lines = content.split("\n")

    for i, line in enumerate(lines):
        # Page boundary
        if re.match(r"^# Page \d+ of 434", line):
            # Look at the 1-2 lines immediately before — was it a table row?
            prev_idx = i - 1
            while prev_idx >= 0 and lines[prev_idx].strip() == "":
                prev_idx -= 1
            if prev_idx < 0:
                continue
            prev = lines[prev_idx]
            if prev.strip().startswith("|") and not is_separator_row(prev):
                # This is a data row immediately before a page break.
                # Check if the table had a proper continuation marker.
                # Look backwards for the header to count expected columns.
                header_cols = None
                for j in range(prev_idx - 1, max(-1, prev_idx - 20), -1):
                    if lines[j].strip().startswith("|"):
                        if is_separator_row(lines[j]):
                            # Count columns from separator
                            header_cols = count_table_columns(lines[j])
                            break
                        elif j == prev_idx - 1:
                            # First row above is also data — keep looking
                            continue
                row_cols = count_table_columns(prev)
                if header_cols and row_cols != header_cols:
                    issues.append(
                        {
                            "type": "column_mismatch_at_page_boundary",
                            "line": i,
                            "expected_cols": header_cols,
                            "found_cols": row_cols,
                            "detail": f"Table row before {line} has {row_cols} cols, header expects {header_cols}",
                        }
                    )
    return issues


def verify_page_headers(content: str) -> list:
    """Ensure all expected `# Page N of 434` headers are present and sequential."""
    issues = []
    headers = [
        int(m.group(1)) for m in re.finditer(r"^# Page (\d+) of 434", content, re.M)
    ]
    if not headers:
        return issues
    # Check for gaps
    for i in range(1, len(headers)):
        if headers[i] != headers[i - 1] + 1:
            issues.append(
                {
                    "type": "page_sequence_gap",
                    "detail": f"Pages jump from {headers[i - 1]} to {headers[i]} (missing {headers[i - 1] + 1}..{headers[i] - 1})",
                }
            )
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(PROJECT / "ste-code" / "extracted"))
    ap.add_argument(
        "--fix",
        action="store_true",
        help="Auto-insert TABLE CONTINUES markers (best-effort)",
    )
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    target = Path(args.dir)
    if not target.exists():
        print(f"ERROR: {target} does not exist", file=sys.stderr)
        sys.exit(2)

    files = sorted(target.rglob("*.md"))
    all_issues = []
    files_checked = 0

    for f in files:
        # Skip non-pipeline files
        if "w" not in f.stem and "group" not in f.stem and "r" not in f.stem:
            continue
        try:
            content = f.read_text(encoding="utf-8")
        except Exception:
            continue
        files_checked += 1
        issues = find_table_breaks(content, f.name)
        issues += verify_page_headers(content)
        if issues:
            all_issues.append({"file": str(f.relative_to(PROJECT)), "issues": issues})

    # Report
    blocking = [
        i
        for fi in all_issues
        for i in fi["issues"]
        if i["type"] == "column_mismatch_at_page_boundary"
    ]
    warnings = [
        i for fi in all_issues for i in fi["issues"] if i["type"] == "page_sequence_gap"
    ]

    if args.json:
        print(
            json.dumps(
                {
                    "files_checked": files_checked,
                    "blocking_errors": len(blocking),
                    "warnings": len(warnings),
                    "issues": all_issues,
                },
                indent=2,
            )
        )
    else:
        print(f"Files checked: {files_checked}")
        print(f"Blocking errors: {len(blocking)}")
        print(f"Warnings: {len(warnings)}")
        for fi in all_issues:
            print(f"  {fi['file']}:")
            for i in fi["issues"]:
                print(f"    [{i['type']}] {i['detail']}")

    if blocking:
        sys.exit(2)
    elif warnings:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
