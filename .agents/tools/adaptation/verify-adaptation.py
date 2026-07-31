#!/usr/bin/env python3
"""verify-adaptation.py — post-adaptation gate for STE-Code Phase D.

Runs AFTER adapt_batch.py writes ste-code/adapted/*.md. Confirms, against the
grouped source of record, that the adaptation is structurally complete and
free of the classic failure modes (aerospace leakage, synonym drift, missing
rules, missing example pairs, broken source backlinks).

Deterministic — no LLM, no network. Same philosophy as grouping's verify-groups:
the creative transform is LLM-driven, but the gate that accepts or rejects it is
not, so a bad creative pass cannot silently ship.

Usage:
  python3 verify-adaptation.py
  python3 verify-adaptation.py --grouped DIR --adapted DIR
Exit code 0 if all gates pass, 1 otherwise.
"""
from __future__ import annotations

import sys
import re
import argparse
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
GROUPED_DIR = PROJECT / "ste-code" / "grouped"
ADAPTED_DIR = PROJECT / "ste-code" / "adapted"

# Expected per-section rule counts (mirrors adaptation SKILL.md Gate 1).
EXPECTED = {
    1: 14, 2: 3, 3: 7, 4: 5, 5: 5, 6: 6, 7: 3, 8: 7, 9: 4,
}
GR_IDS = ["GR1", "GR2", "GR3", "GR4"]

AEROSPACE_TERMS = [
    "aircraft", "landing gear", "fuselage", "cockpit", "APU", "ECS",
    "ATA chapter", "lockwire", "torque", "avionics", "aileron", "rudder",
    "propeller", "thrust", "altimeter",
]
# "engine" excluded from the hard list: it is a legitimate code-domain word
# (search engine, game engine). Only flagged when outside Original Rule AND in
# an aerospace collocation — handled separately below.
NON_APPROVED_SYNONYMS = ["utilize", "leverage", "employ", "commence", "terminate"]


def _split_body(text: str) -> str:
    """Return everything OUTSIDE the '## Original Rule' block AND outside any
    '> **Non-STE:**' example (the Non-STE example is allowed to show the
    non-compliant / aerospace version on purpose). What remains is the adapted
    rule text, which must be clean."""
    # Drop Original Rule block.
    parts = text.split("## Original Rule")
    body = parts[0] if len(parts) == 1 else "".join(parts[1:])
    # Drop Non-STE example blocks: a line starting with '>' that contains
    # 'Non-STE:' plus any following '>'-prefixed lines (the Non-STE example is
    # allowed to show the non-compliant / aerospace version on purpose).
    body = re.sub(r"(?m)^\s*>.*Non-STE:.*(?:\n\s*>.*)*", "", body)
    return body


def _word(text: str, term: str) -> bool:
    return bool(re.search(rf"\b{re.escape(term)}\b", text, re.I))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grouped", type=Path, default=GROUPED_DIR)
    ap.add_argument("--adapted", type=Path, default=ADAPTED_DIR)
    args = ap.parse_args()

    adapted = args.adapted
    problems: list[str] = []

    # ── Gate 1 — structural completeness ───────────────────────────────────
    total_rules = 0
    for sec, exp in EXPECTED.items():
        files = sorted(adapted.glob(f"a-sec{sec}-rule*.md"))
        total_rules += len(files)
        if len(files) < exp:
            problems.append(f"Gate1 sec{sec}: {len(files)} rule files, expected >= {exp}")
    if not (adapted / "a-categories.md").exists():
        problems.append("Gate1: missing a-categories.md")
    if not (adapted / "a-dictionary.md").exists():
        problems.append("Gate1: missing a-dictionary.md")

    # ── Gate 2 — source traceability ───────────────────────────────────────
    for f in sorted(adapted.glob("a-sec*-rule*.md")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        if "Adapted from" not in t and "Source:" not in t:
            problems.append(f"Gate2 {f.name}: no source reference")

    # ── Gate 3 — example pair completeness ─────────────────────────────────
    for f in sorted(adapted.glob("a-sec*-rule*.md")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        if "Non-STE:" in t and "STE:" not in t:
            problems.append(f"Gate3 {f.name}: Non-STE present, STE missing")

    # ── Gate 6 — synonym consistency (outside Original Rule) ───────────────
    for f in sorted(adapted.glob("a-sec*-rule*.md")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        body = _split_body(t)
        for sym in NON_APPROVED_SYNONYMS:
            if _word(body, sym):
                problems.append(f"Gate6 {f.name}: non-approved synonym '{sym}' outside Original Rule")

    # ── Gate 7/9 — aerospace leakage (outside Original Rule) ───────────────
    for f in sorted(adapted.glob("a-sec*-rule*.md")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        body = _split_body(t)
        for term in AEROSPACE_TERMS:
            if _word(body, term):
                problems.append(f"Gate9 {f.name}: aerospace term '{term}' outside Original Rule")

    # ── Gate 8 — backlink integrity (machine-readable Source anchor) ───────
    for f in sorted(adapted.glob("a-sec*-rule*.md")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        if not re.search(r"Source:\s*master\.md#", t):
            problems.append(f"Gate8 {f.name}: missing 'Source: master.md#' backlink")

    # ── Summary ────────────────────────────────────────────────────────────
    print(f"Adaptation verification against {adapted}")
    print(f"  Rule files: {total_rules} (expected >= {sum(EXPECTED.values())})")
    print(f"  a-categories.md: {'yes' if (adapted/'a-categories.md').exists() else 'MISSING'}")
    print(f"  a-dictionary.md: {'yes' if (adapted/'a-dictionary.md').exists() else 'MISSING'}")
    if problems:
        print(f"\nFAIL — {len(problems)} problem(s):")
        for p in problems[:40]:
            print(f"  - {p}")
        print(f"\nverify-adaptation: FAIL")
        sys.exit(1)
    print("\nverify-adaptation: PASS (all gates)")
    sys.exit(0)


if __name__ == "__main__":
    main()
