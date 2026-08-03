#!/usr/bin/env python3
"""diagnose_markers.py — READ-ONLY audit of refined-file page markers.

Why: group_engine.slice_pages refuses to slice a file unless its in-file page
markers resolve EXACTLY to the file's declared page range (rf.pages). During
refinement the marker FORMAT drifted, so ~44 finished files fail that check and
their groups are dropped from `ste-code/grouped/`. This script categorises every
refined file WITHOUT writing anything, so the failure modes can be reviewed
before any repair.

Categories:
  CLEAN        markers resolve exactly -> already sliceable, no action.
  A_dupes      two markers resolve to the same position (e.g. "# Page 29"
               + "**Page TOC-2**" both -> 29). Slicer should collapse dupes.
  B_missing_lead  first page marker absent; resolved positions are a contiguous
               SUFFIX of the expected range (page 117 has no marker, 118-120 do).
  C_merged     only the FIRST page has a marker; pages 2-4 are merged in with no
               interior boundary (typical for post-r054 dictionary files).
  STRADDLER    file's pages span MORE THAN ONE group boundary AND it is merged/
               missing interior markers -> needs a mid-file split (letter-based
               for DICT) before it can be assigned to two groups correctly.
  OTHER        some other mismatch (flagged for manual review).

Usage: python3 .agents/tools/grouping/diagnose_markers.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import group_engine as ge

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
REFINED_DIR = PROJECT / "ste-code" / "refined"


def categorize(rf, id2pos):
    text = rf.path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    marks = []
    for i, ln in enumerate(lines):
        tok = ge._match_page_marker(ln)
        if tok is None:
            continue
        pos = ge._token_to_position(tok, id2pos)
        if pos is None:
            continue
        marks.append((i, pos))
    got = [pos for _, pos in marks]
    expected = list(rf.pages)

    if got == expected:
        return "CLEAN", got, marks

    # collapse consecutive duplicate positions
    dedup = []
    for p in got:
        if not dedup or p != dedup[-1]:
            dedup.append(p)

    if dedup == expected:
        return "A_dupes", got, marks
    # contiguous suffix of expected (missing only leading pages)
    if len(dedup) >= 1 and dedup == expected[-len(dedup) :] and dedup[0] > expected[0]:
        return "B_missing_lead", got, marks
    # single marker == first page -> merged rest
    if len(dedup) == 1 and dedup[0] == expected[0]:
        return "C_merged", got, marks
    return "OTHER", got, marks


def main():
    man = ge.parse_manifest()
    id2pos = ge.id_to_position(man)
    idx = ge.index_refined()
    plan = ge.build_plan(man)

    # page -> group id (for straddler detection)
    page_group = {}
    for g in plan:
        for p in g.pages:
            page_group[p] = g.gid

    cats = {
        "CLEAN": [],
        "A_dupes": [],
        "B_missing_lead": [],
        "C_merged": [],
        "OTHER": [],
        "STRADDLER": [],
    }
    straddlers = []
    for name, rf in sorted({rf.path.name: rf for rf in idx.values()}.items()):
        cat, got, marks = categorize(rf, id2pos)
        if cat != "CLEAN":
            # straddler?
            groups = {
                page_group.get(p) for p in rf.pages if page_group.get(p) is not None
            }
            if len(groups) > 1:
                cat = "STRADDLER"
                straddlers.append((name, sorted(groups)))
        cats[cat].append(name)

    total = sum(len(v) for k, v in cats.items() if k != "CLEAN")
    print("=" * 70)
    print("REFINED MARKER DIAGNOSTIC (read-only)")
    print("=" * 70)
    print(f"Total refined files : {len(cats['CLEAN']) + total}")
    print(f"CLEAN (sliceable)   : {len(cats['CLEAN'])}")
    print(f"Flagged (not clean) : {total}")
    for cat in ("A_dupes", "B_missing_lead", "C_merged", "STRADDLER", "OTHER"):
        files = cats[cat]
        if files:
            print(f"\n[{cat}] {len(files)} file(s):")
            print("  " + ", ".join(files))
    if straddlers:
        print("\nSTRADDLER detail (file -> groups it spans):")
        for name, gs in straddlers:
            print(f"  {name}: {gs}")

    print("\n" + "=" * 70)
    print("TIPS")
    print("=" * 70)
    print("- A_dupes: slicer should `dedup` consecutive equal positions (keep first).")
    print("- B_missing_lead: infer the missing leading page(s) from rf.pages; the")
    print("  file body before the first real marker belongs to page rf.start.")
    print("- C_merged (single marker): if the WHOLE file's pages fall inside ONE")
    print("  group, assign the entire file to that group (no interior split).")
    print("- STRADDLER: split at the group boundary. For DICT straddlers the")
    print("  boundary is a DICT letter change (entries are alphabetical) -> split")
    print("  at the first entry heading whose letter >= the next group's start")
    print("  letter. Deterministic, no LLM needed.")
    print("- Repair tool: .agents/tools/grouping/repair_markers.py (parity-checked).")
    print(f"\nFlagged total: {total}  (STRADDLER={len(straddlers)})")

    # exit code: 0 if no flags (clean corpus), else 1 (still work to do)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
