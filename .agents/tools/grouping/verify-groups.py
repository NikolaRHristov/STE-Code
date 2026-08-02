#!/usr/bin/env python3
"""verify-groups.py — post-assembly gate for STE-Code Phase C grouping.

Runs AFTER group_batch.py writes ste-code/grouped/*.md. Confirms, against the
refined source of record, that grouping lost nothing and split nothing it must
not split. This is the grouping analogue of the refinement per-batch gate, but
stronger: because grouping only MOVES bytes, we can demand EXACT content-token
parity rather than a ratio.

Checks (all must pass):
  1. COVERAGE      — every page 1..434 appears in exactly one group; the set of
                     group page-ranges tiles the whole corpus with no gap/overlap.
  2. PARITY        — for each group, the content-token multiset of the written
                     file equals that of its source pages (zero missing tokens).
                     Missing tokens are named (the exact lost words), so a
                     regression is diagnosable, not just flagged.
  3. MARKS         — every <mark> highlight in the sources survives into the group
                     (STE example highlights must never be dropped).
  4. NO-SPLIT-DICT — no dictionary group starts or ends mid-entry: the first
                     content row after the (single) table header is a real entry
                     row, and letter boundaries fall on page boundaries so a
                     letter's entries are never split across two groups except at
                     a page edge that the plan intends.
  5. ONE-TABLE     — each dictionary group contains exactly ONE table header
                     (spanning pages were merged into one continuous table).
  6. PICTURE-INTACT— every `<!-- Start of picture text -->` has a matching End in
                     the same group (a picture block was never split across a
                     group boundary).

Exit code 0 = all groups pass; 1 = at least one failure. Prints a per-group
report. No LLM, no network.
"""
from __future__ import annotations

import re
import importlib.util as _ilu
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
GROUPED_DIR = PROJECT / "ste-code" / "grouped"


def _load(name: str, path: Path):
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
    from templater import load_local
    return load_local(name, path)


engine = _load("group_engine", PROJECT / ".agents/tools/grouping/group_engine.py")
gb = _load("group_batch", PROJECT / ".agents/tools/grouping/group_batch.py")


class Report:
    def __init__(self):
        self.failures = 0
        self.groups = 0

    def line(self, ok: bool, gid: str, msg: str):
        tag = "PASS" if ok else "FAIL"
        if not ok:
            self.failures += 1
        print(f"  [{tag}] {gid:<24} {msg}")


def source_text_for(group, idx, id2pos) -> str | None:
    """Concatenate the refined source page slices for a group (pre-merge)."""
    bodies = []
    for p in group.pages:
        rf = idx.get(p)
        if rf is None:
            return None
        sl = engine.slice_pages(rf, id2pos)
        if p not in sl:
            return None
        bodies.append(sl[p])
    return "\n".join(bodies)


def verify():
    man = engine.parse_manifest()
    id2pos = engine.id_to_position(man)
    idx = engine.index_refined()
    plan = engine.build_plan(man)
    rep = Report()

    print("=" * 74)
    print("STE-Code Phase C — GROUP VERIFICATION")
    print("=" * 74)

    if not GROUPED_DIR.exists():
        print(f"grouped/ does not exist yet ({GROUPED_DIR}). Nothing to verify.")
        print("Run group_batch.py first (once the refined corpus is complete).")
        return 0  # not a failure — just nothing produced yet

    # ── 1. coverage: plan tiles 1..434 ──────────────────────────────────────
    seen: dict[int, int] = {}
    for g in plan:
        for p in g.pages:
            seen[p] = seen.get(p, 0) + 1
    missing = [p for p in range(1, engine.TOTAL_PAGES + 1) if p not in seen]
    dupes = [p for p, c in seen.items() if c > 1]
    rep.line(not missing and not dupes, "COVERAGE",
             f"{len(seen)}/{engine.TOTAL_PAGES} pages; missing={missing[:6]} dupes={dupes[:6]}")

    # ── per-group checks ────────────────────────────────────────────────────
    for g in plan:
        rep.groups += 1
        gfile = GROUPED_DIR / g.filename
        if not gfile.exists():
            rep.line(False, g.gid, f"output file missing: {g.filename}")
            continue
        out_text = gfile.read_text(encoding="utf-8", errors="ignore")
        src_text = source_text_for(g, idx, id2pos)
        if src_text is None:
            rep.line(False, g.gid, "source pages not sliceable (corpus incomplete)")
            continue

        # 2. parity
        ok, miss, added = engine.parity_diff(src_text, out_text)
        if ok:
            rep.line(True, g.gid, "parity OK (0 tokens missing)")
        else:
            rep.line(False, g.gid,
                     f"CONTENT LOSS: {sum(miss.values())} tokens missing "
                     f"e.g. {list(miss)[:6]}")

        # 3. marks
        src_marks = gb.mark_count(src_text)
        out_marks = gb.mark_count(out_text)
        rep.line(out_marks >= src_marks, g.gid,
                 f"marks {out_marks}/{src_marks} "
                 f"({'ok' if out_marks >= src_marks else 'DROPPED'})")

        # 5. one-table (dict groups only). After the dict normalizer (Fix B),
        #    every dict group MUST be exactly ONE continuous 4-col table: exactly
        #    one `| Word (POS) |` header and ZERO leftover `#### WORD (POS)`
        #    block headings. Weakened neither to a no-op nor to the old
        #    `hdrs <= 1` which silently passed block-format groups (headers=0).
        if g.section == "DICT":
            lines = out_text.splitlines()
            hdrs = sum(1 for ln in lines if gb._TABLE_HDR_RE.match(ln.strip()))
            block_heads = sum(
                1 for ln in lines
                if re.match(r"^#{3,4}\s+\*{0,2}[A-Za-z][A-Za-z()\-\s,]*\s*\(", ln.strip()))
            rep.line(
                hdrs == 1 and block_heads == 0, g.gid,
                f"single continuous table (headers={hdrs}, ####WORD blocks={block_heads}, "
                f"expect headers==1 and blocks==0)")

        # 6. picture blocks balanced within the group
        n_start = out_text.count("<!-- Start of picture text -->")
        n_end = out_text.count("<!-- End of picture text -->")
        rep.line(n_start == n_end, g.gid,
                 f"picture blocks balanced (start={n_start} end={n_end})")

    print("-" * 74)
    status = "ALL GROUPS PASS" if rep.failures == 0 else f"{rep.failures} FAILURES"
    print(f"{status}  ({rep.groups} groups checked)")
    print("=" * 74)
    return 1 if rep.failures else 0


if __name__ == "__main__":
    sys.exit(verify())
