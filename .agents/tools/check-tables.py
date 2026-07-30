#!/usr/bin/env python3
"""Table integrity checker for STE-Code pipeline.

Scans refined files for broken table continuations:
- Files ending mid-row (table splits across pages)
- Missing separator rows
- Header/separator mismatches

Usage:
  python3 .agents/tools/check-tables.py [--fix]
"""

import sys, re
from pathlib import Path
from collections import defaultdict

PROJECT = Path(__file__).resolve().parent.parent.parent
REFINED = PROJECT / "ste-code" / "refined"


def find_table_breaks():
    """Find files where tables are split across page boundaries."""
    refined = sorted(REFINED.glob("r*-p*.md"))
    breaks = []

    for i, f in enumerate(refined):
        content = f.read_text()
        lines = content.split("\n")

        # Get last non-empty content lines
        last = [l.strip() for l in lines[-10:] if l.strip()]
        ends_table = any(l.startswith("|") for l in last[-3:]) if last else False

        if not ends_table or i + 1 >= len(refined):
            continue

        next_f = refined[i + 1]
        next_lines = [
            l.strip()
            for l in next_f.read_text().split("\n")[:10]
            if l.strip()
        ]
        next_starts_table = any(
            l.startswith("|") for l in next_lines[:5]
        ) if next_lines else False

        if not next_starts_table:
            # Verify this is a real break (not a legitimate end-of-table)
            breaks.append({
                "file": f.name,
                "next_file": next_f.name,
                "page_range": f.name.split("-p")[1].replace(".md", "") if "-p" in f.name else "?",
            })

    return breaks


def find_table_anomalies():
    """Find tables with missing headers, separator rows, or orphan cells."""
    refined = sorted(REFINED.glob("r*-p*.md"))
    anomalies = []

    for f in refined:
        content = f.read_text()
        lines = content.split("\n")

        # Find table blocks: header row | separator row | data rows
        in_table = False
        has_header = False
        has_separator = False
        row_count = 0
        table_start = 0

        for i, line in enumerate(lines):
            s = line.strip()

            if s.startswith("|") and "---" in s:
                # Separator row
                if in_table:
                    has_separator = True
                else:
                    # Separator without preceding header? Check previous line
                    prev = lines[i - 1].strip() if i > 0 else ""
                    if prev.startswith("|"):
                        in_table = True
                        has_header = True
                        has_separator = True
                        table_start = i - 1
                        row_count = 0

            elif s.startswith("|") and not in_table:
                # Potential header row
                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                if "---" in next_line:
                    in_table = True
                    has_header = True
                    table_start = i
                    row_count = 0
                else:
                    # Orphan table row without separator
                    anomalies.append({
                        "file": f.name,
                        "line": i + 1,
                        "issue": "orphan row (no separator follows)",
                    })

            elif s.startswith("|") and in_table:
                row_count += 1

            elif not s.startswith("|") and in_table:
                # End of table
                if has_header and has_separator and row_count == 0:
                    anomalies.append({
                        "file": f.name,
                        "line": table_start + 1,
                        "issue": "empty table (header + separator, no data rows)",
                    })
                in_table = False
                has_header = False
                has_separator = False
                row_count = 0

    return anomalies


def main():
    breaks = find_table_breaks()
    anomalies = find_table_anomalies()

    print(f"=== Table Integrity Report ===\n")
    print(f"Table breaks (split across pages without continuation): {len(breaks)}")
    for b in breaks:
        print(f"  {b['file']} → {b['next_file']} (pages {b['page_range']})")

    print(f"\nTable anomalies (malformed tables): {len(anomalies)}")
    for a in anomalies:
        print(f"  {a['file']}:{a['line']} — {a['issue']}")

    if not breaks and not anomalies:
        print("  All tables intact. ✓")

    total = len(breaks) + len(anomalies)
    print(f"\nTotal issues: {total}")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
