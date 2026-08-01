#!/usr/bin/env python3
"""Rewrite drifted version, badge, and count claims to match disk.

Runs `scan.py`, then applies every finding as a surgical in-place edit. Only
the matched number is replaced — surrounding prose is untouched.

Ambiguous count findings (a claim whose fact set holds more than one candidate,
such as "categories" being either 14 benchmark categories or 22 technical-noun
categories) are NOT auto-fixed; they are listed for a human. Use
`--pick <claim-id>=<value>` to resolve one explicitly.

Usage:
    python3 .agents/tools/release/sync.py --dry-run
    python3 .agents/tools/release/sync.py
    python3 .agents/tools/release/sync.py --pick categories-count=22
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from facts import collect  # noqa: E402
from scan import registry, resolve, scan_counts, scan_stamps, tracked_files  # noqa: E402


def apply_line_fix(rel: str, line_no: int, found: str, expected: str, pattern: str) -> bool:
    """Replace the matched number on one line, leaving the rest intact."""
    path = PROJECT / rel
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    if line_no < 1 or line_no > len(lines):
        return False
    rx = re.compile(pattern)
    line = lines[line_no - 1]
    out, cursor, changed = [], 0, False
    for m in rx.finditer(line):
        if m.group("value") != found:
            continue
        s, e = m.span("value")
        out.append(line[cursor:s])
        out.append(expected)
        cursor = e
        changed = True
    if not changed:
        return False
    out.append(line[cursor:])
    lines[line_no - 1] = "".join(out)
    path.write_text("".join(lines), encoding="utf-8")
    return True


def apply_stamp_fix(rel: str, pattern: str, expected: str) -> bool:
    path = PROJECT / rel
    text = path.read_text(encoding="utf-8", errors="replace")
    rx = re.compile(pattern, re.M)
    m = rx.search(text)
    if not m or "value" not in (m.groupdict() or {}):
        return False
    s, e = m.span("value")
    path.write_text(text[:s] + expected + text[e:], encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="report, change nothing")
    ap.add_argument("--wide", action="store_true", help="scan every tracked document")
    ap.add_argument(
        "--pick",
        action="append",
        default=[],
        metavar="CLAIM=VALUE",
        help="resolve an ambiguous claim to one value (repeatable)",
    )
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    picks = dict(p.split("=", 1) for p in args.pick)
    facts = collect()
    reg = registry()
    claim_pat = {c["id"]: c["pattern"] for c in reg["count_claims"]}
    stamp_pat = {
        c["id"]: c for group in ("badges", "version_stamps") for c in reg[group]
    }

    findings = scan_stamps(facts, reg) + scan_counts(
        facts, reg, tracked_files(reg, args.wide)
    )

    applied, skipped = [], []
    for f in findings:
        if f["kind"] == "count":
            candidates = f["expected"].split(" or ")
            target = picks.get(f["claim"])
            if target is None and len(candidates) == 1:
                target = candidates[0]
            if target is None:
                skipped.append({**f, "reason": "ambiguous — use --pick"})
                continue
            ok = args.dry_run or apply_line_fix(
                f["file"], f["line"], f["found"], target, claim_pat[f["claim"]]
            )
            (applied if ok else skipped).append({**f, "applied": target})
        else:
            claim = stamp_pat[f["claim"]]
            expected = resolve(facts, claim["fact"])
            if expected is None or f["found"] is None:
                skipped.append({**f, "reason": "no value to write"})
                continue
            ok = args.dry_run or apply_stamp_fix(
                f["file"], claim["pattern"], str(expected)
            )
            (applied if ok else skipped).append({**f, "applied": str(expected)})

    if args.json:
        print(json.dumps({"applied": applied, "skipped": skipped}, indent=2))
        return 0

    verb = "Would fix" if args.dry_run else "Fixed"
    print(f"{verb} {len(applied)} claim(s); {len(skipped)} need a decision.\n")
    for f in applied:
        print(f"  {f['file']}:{f['line']}  {f['claim']}  {f['found']} -> {f['applied']}")
    if skipped:
        print("\nUnresolved:")
        for f in skipped:
            print(f"  {f['file']}:{f['line']}  {f['claim']}  found {f['found']!r}")
            print(f"    expected {f['expected']!r} — {f.get('reason', 'no rewrite')}")
            print(f"    {f['text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
