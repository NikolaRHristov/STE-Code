#!/usr/bin/env python3
"""repair_markers.py — deterministic repair of refined-file page markers.

WHY: group_engine.slice_pages refuses to slice a file unless its in-file page
markers resolve EXACTLY to the file's declared page range (rf.pages). ~44
finished refined files have marker drift (duplicates, missing leading marker,
or merged pages with no interior boundary), so their groups are dropped from
ste-code/grouped/. The byte CONTENT of those files is intact — only the markers
are wrong. This tool rewrites ONLY marker lines, deterministically, so the
existing engine slices them correctly. No LLM, no content re-typing, no loss.

Strategy per category (categories from diagnose_markers.py):
  A_dupes        : keep the first marker per position; delete redundant marker
                  lines that resolve to an already-covered position (they are
                  page-stamp boilerplate, stripped in parity anyway -> lossless).
  B_missing_lead : insert `# Page {start} of 434` right after the metadata block
                  (content before the first real marker IS page start).
  C_merged       : only `# Page {start}` exists; insert `# Page {start+1..end}`
                  at deterministic interior points (even line-split, snapped to
                  the nearest entry heading). Exact intra-file page breaks are
                  unknown, but for SINGLE-GROUP files grouping only needs the
                  whole file assigned to its group -> parity still holds.
  STRADDLER      : like C_merged, BUT the group-boundary page marker is placed
                  at the first dictionary entry whose letter >= the next group's
                  start letter (entries are alphabetical -> deterministic split
                  at the true letter boundary). Other interior pages split evenly.

Self-check: after repair, content_tokens(whole original) must be a SUPERSET of
content_tokens(whole repaired) — i.e. NO content word is lost (boilerplate
page-stamp edits may add a few tokens; that is tolerated, never a loss).

Idempotent: a file already resolving exactly to its range is never touched.

Usage:
  python3 .agents/tools/grouping/repair_markers.py --dry-run   # report only
  python3 .agents/tools/grouping/repair_markers.py --apply     # rewrite + commit
"""

import re
import subprocess
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
from ste_io import write_text  # noqa: E402

REFINED_DIR = PROJECT / "ste-code" / "refined"

_ENTRY_RE = re.compile(r"^#{1,4}\s+([A-Za-z][A-Za-z\-\']*)\s*\(", re.M)
_HEADING_RE = re.compile(r"^#{1,4}\s+\S")
_METADATA_END_RE = re.compile(r"^#\s+Page\s+\d", re.I)


def _first_letter_of_heading(line: str) -> str:
    m = _ENTRY_RE.match(line)
    if m:
        return m.group(1)[0].upper()
    return ""


def _snap_to_heading(lines, idx, window=6):
    """Snap a split index to the nearest entry/heading line within ±window."""
    best = idx
    for d in range(window + 1):
        for j in (idx - d, idx + d):
            if 0 <= j < len(lines) and _HEADING_RE.match(lines[j]):
                return j
    return idx


def _interior_splits(body_lines, n_splits):
    """Return n_splits line indices that split body_lines into n_splits+1 parts,
    snapped to nearest heading where possible."""
    n = len(body_lines)
    if n == 0 or n_splits <= 0:
        return []
    cuts = []
    for i in range(1, n_splits + 1):
        raw = (n * i) // (n_splits + 1)
        cuts.append(_snap_to_heading(body_lines, raw))
    return cuts


def _next_group_start_letter(rf, plan):
    """For a straddler, the letter the NEXT group starts at (>= boundary page)."""
    # map page -> group, find boundary page (first page not in the first group)
    page_group = {}
    for g in plan:
        for p in g.pages:
            page_group[p] = g.gid
    groups = [page_group.get(p) for p in rf.pages]
    if len(set(groups)) < 2:
        return None
    first_gid = groups[0]
    boundary_page = next(p for p, g in zip(rf.pages, groups) if g != first_gid)
    # letter of the group that boundary_page belongs to:
    for g in plan:
        if g.gid == page_group.get(boundary_page) and g.section == "DICT":
            return g.key[0] if g.key else None
    return None


def repair_text(text: str, rf, plan, id2pos) -> str:
    """Return repaired text (marker lines normalized to `# Page N of 434`).

    Builds ONE authoritative array `bounds[k]` = line index where page
    expected[k] starts (in increasing document order), drops all old markers,
    and emits exactly one canonical marker per page at its bound.
    """
    lines = text.splitlines()
    expected = list(rf.pages)
    n = len(expected)

    # 1) existing resolved marker positions (dedup: first per position)
    marks = []
    seen = set()
    for i, ln in enumerate(lines):
        tok = ge._match_page_marker(ln)
        if tok is None:
            continue
        pos = ge._token_to_position(tok, id2pos)
        if pos is None or pos in seen:
            continue
        seen.add(pos)
        marks.append((i, pos))
    known = {p: i for i, p in marks}  # pos -> line (first occurrence)

    bounds = [None] * n
    for k, p in enumerate(expected):
        if p in known:
            bounds[k] = known[p]

    # 2) fill missing bounds
    # leading page missing -> after the metadata block (first "# Page N of 434")
    if bounds[0] is None:
        sl = 0
        for j, ln in enumerate(lines):
            if _METADATA_END_RE.match(ln.strip()):
                sl = j
                break
        bounds[0] = sl
    # interior / trailing missing -> even split between neighbours, snapped
    prev_b = 0
    for k in range(1, n):
        if bounds[k] is None:
            prev = bounds[k - 1]
            nxt_idx = next((j for j in range(k + 1, n) if bounds[j] is not None), n)
            nxt = bounds[nxt_idx] if nxt_idx < n else len(lines)
            span = lines[prev:nxt] if nxt > prev else lines[prev:]
            raw = (
                (len(span) * (k - prev_b)) // (nxt_idx - prev_b)
                if (nxt_idx - prev_b)
                else prev + 1
            )
            bounds[k] = prev + _snap_to_heading(span, raw)
        prev_b = k

    # 3) straddler: force the boundary page's bound to the letter transition
    ng_letter = _next_group_start_letter(rf, plan)
    if ng_letter:
        page_group = {p: g.gid for g in plan for p in g.pages}
        first_gid = page_group.get(expected[0])
        boundary_page = next(
            (p for p in expected if page_group.get(p) != first_gid), None
        )
        if boundary_page is not None:
            bk = expected.index(boundary_page)
            for j in range(bounds[0] + 1, len(lines)):
                L = _first_letter_of_heading(lines[j])
                if L and L >= ng_letter:
                    bounds[bk] = j
                    break

    # 4) enforce strictly increasing (repair any snap collisions)
    for k in range(1, n):
        if bounds[k] is None or bounds[k] <= bounds[k - 1]:
            bounds[k] = bounds[k - 1] + 1
    # clamp trailing to len (EOF marker handled below)
    for k in range(n):
        if bounds[k] >= len(lines):
            bounds[k] = len(lines) - 1

    # 5) rebuild: drop every old marker; emit canonical markers at bounds
    out = []
    for i, ln in enumerate(lines):
        if ge._match_page_marker(ln) is not None:
            continue  # drop all old markers (replaced below)
        # emit any page whose bound is exactly this line, BEFORE the content
        for k in range(n):
            if bounds[k] == i:
                out.append(f"# Page {expected[k]} of 434")
        out.append(ln)
        # emit any page whose bound is right AFTER this line
        for k in range(n):
            if bounds[k] == i + 1:
                out.append(f"# Page {expected[k]} of 434")
    # emit pages whose bound is at EOF (>= len)
    for k in range(n):
        if bounds[k] >= len(lines):
            out.append(f"# Page {expected[k]} of 434")
    return "\n".join(out) + "\n"


def _gid_of(rf, plan, page):
    for g in plan:
        if page in g.pages:
            return g.gid
    return None


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    ap.add_argument(
        "--apply", action="store_true", help="rewrite refined files + git commit"
    )
    args = ap.parse_args()
    if not (args.dry_run or args.apply):
        args.dry_run = True

    man = ge.parse_manifest()
    id2pos = ge.id_to_position(man)
    idx = ge.index_refined()
    plan = ge.build_plan(man)

    changed = []
    problems = []
    for name, rf in sorted({rf.path.name: rf for rf in idx.values()}.items()):
        # already clean?
        if ge.slice_pages(rf, id2pos):
            continue
        orig = rf.path.read_text(encoding="utf-8", errors="ignore")
        repaired = repair_text(orig, rf, plan, id2pos)
        # self-check: no content loss
        o_tokens = ge.content_tokens(orig)
        r_tokens = ge.content_tokens(repaired)
        lost = o_tokens - r_tokens
        if sum(lost.values()) > 0:
            problems.append(
                f"{name}: CONTENT LOSS detected ({dict(lost.most_common(5))})"
            )
            continue
        if repaired == orig:
            continue  # nothing changed (shouldn't happen for flagged, but safe)
        changed.append((rf.path, repaired))

    print("=" * 70)
    print(f"REPAIR MARKERS — {'DRY RUN' if args.dry_run else 'APPLY'}")
    print("=" * 70)
    print(f"Files to rewrite: {len(changed)}")
    for path, _ in changed:
        print(f"  {path.name}")
    if problems:
        print("\nPROBLEMS (skipped, NOT rewritten):")
        for p in problems:
            print(f"  ! {p}")
    if args.dry_run or problems:
        print("\n(dry-run or had problems — nothing written)")
        return

    # APPLY
    for path, repaired in changed:
        write_text(path, repaired)
    # verify: re-run slice_pages
    bad = [rf.path.name for rf in idx.values() if not ge.slice_pages(rf, id2pos)]
    print(
        f"\nAfter repair: {len(bad)} files still unsliceable (was {len(changed) + len(bad)})."
    )
    if bad:
        print("  still bad: " + ", ".join(bad))
    # commit
    subprocess.run(["git", "add", "-A", "ste-code/refined"], cwd=PROJECT, check=True)
    msg = (
        f"Refinement markers: deterministic repair of {len(changed)} flagged files "
        f"(A_dupes/B_missing_lead/C_merged/straddler) so grouping slices cleanly"
    )
    subprocess.run(["git", "commit", "-q", "-m", msg], cwd=PROJECT, check=True)
    print("Committed repaired refined files.")


if __name__ == "__main__":
    main()
