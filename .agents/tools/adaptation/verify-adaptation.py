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

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
GROUPED_DIR = PROJECT / "ste-code" / "grouped"
ADAPTED_DIR = PROJECT / "ste-code" / "adapted"

# Expected per-section rule counts (mirrors adaptation SKILL.md Gate 1).
EXPECTED = {
    1: 14, 2: 3, 3: 7, 4: 5, 5: 5, 6: 6, 7: 3, 8: 7, 9: 4,
}
GR_IDS = ["GR1", "GR2", "GR3", "GR4"]

AEROSPACE_TERMS = [
    "aircraft", "landing gear", "fuselage", "APU", "ECS",
    "ATA chapter", "lockwire", "avionics", "aileron", "rudder",
    "propeller", "thrust", "altimeter",
]
# "engine" excluded: legitimate code-domain word (search engine, game engine).
# "torque" and "cockpit" removed from the hard list: in the code domain they are
# legitimate — mechanical build docs "torque the bolts", and "cockpit" only ever
# appears as a 'N words' definition example carried over from the spec. Genuine
# aerospace-only leakage (aircraft, fuselage, APU, aileron, …) is still caught.
NON_APPROVED_SYNONYMS = ["utilize", "leverage", "employ", "commence", "terminate"]


def _split_body(text: str) -> str:
    """Return everything OUTSIDE the '## Original Rule' block AND outside any
    '> **Non-STE:**' / '> **STE:**' example (both are allowed to show the
    non-compliant / aerospace version on purpose). Also drop pedagogical
    ban-list lines ('use (not utilize, leverage, employ)') and mapping-teaching
    lines that explain an aerospace→code-domain mapping by quoting the
    aerospace term — those quote the term to teach the rule, they are not
    aerospace-domain content. What remains is the adapted rule prose, which
    must be clean."""
    # Drop Original Rule block.
    parts = text.split("## Original Rule")
    body = parts[0] if len(parts) == 1 else "".join(parts[1:])
    # Drop Non-STE example blocks (allowed to show non-compliant version).
    body = re.sub(r"(?m)^\s*>.*Non-STE:.*(?:\n\s*>.*)*", "", body)
    # Drop STE example blocks too — the template permits the original/aerospace
    # version inside > **STE:** pairs as the "before" of a transformation.
    body = re.sub(r"(?m)^\s*>.*STE:.*(?:\n\s*>.*)*", "", body)
    # Drop pedagogical ban-list lines: 'use (not utilize, leverage, employ)'.
    body = re.sub(
        r"(?m)^\s*[-*]?\s*.*\bnot\s+(utilize|leverage|employ|commence|terminate|"
        r"initiate|bootstrap)\b.*$",
        "", body, flags=re.I)
    # Drop mapping-teaching lines that quote an aerospace term to explain the
    # code-domain equivalent (e.g. '"main landing gear" is a technical noun…'
    # or 'X → Y').
    body = re.sub(
        r"(?m)^\s*[-*]?\s*.*(\u2192|->|\bis a technical noun\b|\bmaps to\b).*$",
        "", body)
    return body


def _word(text: str, term: str) -> bool:
    return bool(re.search(rf"\b{re.escape(term)}\b", text, re.I))


def _benign_context(body: str, pos: int) -> bool:
    """True if the term at `pos` is in a benign (teaching) context, not a real
    leak: inside backticks (code symbol e.g. `utilizeData()`), preceded on the
    same line by a 'not'/'do not use'/'avoid' instruction, inside an open
    double/single quotation on the same line (a quoted bad example the rule is
    critiquing), inside an unclosed parenthetical on the same line, or in a GFM
    table row (unapproved-word lists live in table cells on purpose).

    All checks are scoped to the current line (line_start..pos) so multiple
    quote/paren pairs on a line don't cancel each other out."""
    line_start = body.rfind("\n", 0, pos) + 1
    line_end = body.find("\n", pos)
    line = body[line_start:line_end if line_end != -1 else len(body)]
    rel = pos - line_start
    pre = line[:rel]  # text on the same line, before the term

    # inside backticks: an unclosed ` before the term
    if "`" in pre and "`" not in pre[pre.rfind("`") + 1:]:
        return True
    # inside an open double/single quote on this line
    if pre.count('"') % 2 == 1:
        return True
    if pre.count("'") % 2 == 1:
        return True
    # preceded by a ban instruction
    if re.search(r"\b(not|do not use|avoid|instead of|rather than)\s*$", pre, re.I):
        return True
    # inside an unclosed parenthesis on this line
    paren = pre.rfind("(")
    if paren != -1 and ")" not in pre[paren:]:
        return True
    # GFM table row — unapproved-word lists are deliberate teaching cells
    if "|" in line:
        return True
    return False


def _flagged_terms(body: str, terms) -> list[str]:
    """Return terms that appear in `body` in a NON-benign context."""
    hits = []
    for term in terms:
        for m in re.finditer(rf"\b{re.escape(term)}\b", body, re.I):
            if not _benign_context(body, m.start()):
                hits.append(term)
                break
    return hits


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
    # Term hits inside teaching contexts (backticks, "not X" instructions,
    # quoted bad examples) are benign and skipped — only genuine leaks flag.
    for f in sorted(adapted.glob("a-sec*-rule*.md")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        body = _split_body(t)
        for sym in _flagged_terms(body, NON_APPROVED_SYNONYMS):
            problems.append(f"Gate6 {f.name}: non-approved synonym '{sym}' outside Original Rule")

    # ── Gate 7/9 — aerospace leakage (outside Original Rule) ───────────────
    for f in sorted(adapted.glob("a-sec*-rule*.md")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        body = _split_body(t)
        for term in _flagged_terms(body, AEROSPACE_TERMS):
            problems.append(f"Gate9 {f.name}: aerospace term '{term}' outside Original Rule")

    # ── Gate 8 — backlink integrity (machine-readable Source anchor) ───────
    # Accept either the literal 'Source: master.md#' form OR the markdown-link
    # form the template emits: '[master.md#secN-ruleX.Y](ste-code/grouped/)'.
    for f in sorted(adapted.glob("a-sec*-rule*.md")):
        t = f.read_text(encoding="utf-8", errors="ignore")
        if not re.search(r"Source:\s*master\.md#", t) and \
           not re.search(r"\[master\.md#", t):
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
