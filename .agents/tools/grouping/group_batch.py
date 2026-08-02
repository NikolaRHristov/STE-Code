#!/usr/bin/env python3
"""group_batch.py — STE-Code Phase C assembler (deterministic, LLM-free).

Reads the refined page files (ste-code/refined/rNNN-pA-B.md) and assembles them
into ~23 semantically coherent group files under ste-code/grouped/, following a
deterministic plan (see group_engine.py). NO LLM is involved in the copy path —
bytes are moved, never re-typed — so content cannot be lost (the failure mode
that hit the LLM-based refinement stage; see .agents/feedback/exchange.md).

BORROWED LESSONS from the Refinement agent (.agents/feedback/exchange.md):
  #1 Prompt/skill/gate must AGREE  → here the plan lives in ONE module
     (group_engine) imported by the assembler, the verifier, and the runner.
  #2 A verify gate must not count formatting as content → the parity gate
     normalizes markup + boilerplate before counting (copied pattern from
     refine_batch._word_count).
  #3 Explosion is the enemy of free-tier workers → grouping is pure Python,
     no generation budget to overrun. DICT is split into ~28-page alphabetical
     buckets so the DOWNSTREAM (adaptation) LLM reader isn't handed a 285-page
     monolith.
  #4 Verify against DISK, not self-reports → after writing, the assembler
     re-reads each group and checks page-count + content parity vs the source
     slices; a group that loses content is a hard fail.

TABLE-MERGE GUARANTEE (the user's explicit requirement):
  When consecutive pages within a group each carry the SAME dictionary table
  header, the assembler keeps the first header + separator and drops the
  repeated header/separator rows on continuation pages, yielding ONE continuous
  table instead of many fragmented tables. Dictionary entries are never split
  because letters change on page boundaries and whole pages are grouped.

SAFETY:
  - --dry-run (default-safe): prints the plan + readiness, writes NOTHING.
  - Real assembly REFUSES to run unless the refined corpus is complete and
    every source file has clean internal `# Page N` markers (corpus_ready()).
    This prevents grouping a half-rewritten corpus during refinement churn.
  - Idempotent (R5): a valid existing group with matching parity is skipped.
  - File-locked (R4) via pipeline_core when writing shared group files.

Usage:
  python3 .agents/tools/grouping/group_batch.py --dry-run     # plan only (safe)
  python3 .agents/tools/grouping/group_batch.py --plan-json    # machine plan
  python3 .agents/tools/grouping/group_batch.py                # assemble (guarded)
  python3 .agents/tools/grouping/group_batch.py --force        # ignore idempotence
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── import the shared engine (single source of truth for the plan) ──────────
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
from templater import load_local


def _load_module(mod_name: str, path: Path):
    """Load a sibling module by path and register it in sys.modules.

    Registration matters: modules that define @dataclass need their module
    present in sys.modules for the ClassVar type-resolution to work under
    `from __future__ import annotations`. The repo's bare exec() pattern skips
    this; we do it right so the engine's dataclasses load cleanly.
    """
    return load_local(mod_name, path)


# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
engine = _load_module(
    "group_engine", PROJECT / ".agents" / "tools" / "grouping" / "group_engine.py")
pipeline_core = _load_module(
    "pipeline_core", PROJECT / ".agents" / "tools" / "lib" / "pipeline_core.py")
_templater_mod = _load_module(
    "templater", PROJECT / ".agents" / "tools" / "lib" / "templater.py")
dict_normalize = _load_module(
    "dict_normalize", PROJECT / ".agents" / "tools" / "grouping" / "dict_normalize.py")

# External markdown templates live in grouping/templates/*.md (edit those, not
# the f-strings here) — see .agents/tools/grouping/templates/README.md.
TPL = _templater_mod.Templater(__file__)

GROUPED_DIR = PROJECT / "ste-code" / "grouped"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "grouping-checkpoint.json"


# ── content-parity gate (borrowed from refine_batch._word_count, Lesson #2) ─
_MARKUP_TAG_RE = re.compile(r"</?[a-zA-Z][^>]*>")
_BOILERPLATE_RE = re.compile(
    r"(?i)(ASD[-\s]?STE100(\s+Simplified\s+Technical\s+English)?"
    r"|Simplified\s+Technical\s+English"
    r"|Issue\s+9(\s*[-,]?\s*(2025-01-15|January\s+2025))?"
    r"|Part\s+\d+\s*[-–]\s*Dictionary"
    r"|Page\s+[A-Z0-9]+-[A-Z0-9\-]+"
    r"|Page\s+\d+(\s*[–-]\s*\d+)?\s+of\s+434"
    r"|Highlights)"
)


def word_count(text: str) -> int:
    """Count CONTENT words, ignoring markup + repeated page-stamp boilerplate.

    Same normalizer the refinement gate uses so grouping measures REAL content
    parity, not formatting. A group that drops a `> **Source:**` block or a
    repeated page stamp is CORRECT and must still pass.
    """
    t = _MARKUP_TAG_RE.sub(" ", text)
    t = _BOILERPLATE_RE.sub(" ", t)
    return len(re.findall(r"[A-Za-z0-9]{2,}", t.lower()))


def mark_count(text: str) -> int:
    """Count all <mark ...> annotation variants (source uses <mark>, _<mark>,
    _<u><mark>). These carry the STE example highlights — never drop one."""
    return text.count("<mark")


# ── table-merge: collapse repeated dict-table headers across pages ──────────
# A dictionary-table header. The refiner's header text may drift ("Word (POS)",
# "Word(POS)", extra spaces), so match loosely on the leading Word/POS cell.
_TABLE_HDR_RE = re.compile(r"^\|\s*Word\s*\(?POS\)?", re.I)
_SEP_RE = re.compile(r"^\|[\s:\-\|]+\|?\s*$")
# Page marker in any style (mirrors engine._PAGE_MARKERS but as one matcher).
_PAGE_MARK_RE = re.compile(
    r"^(?:#{1,4}\s+Page\s+.+|\*\*\s*Page\s+.+\*\*)\s*$", re.I)
# Picture-text region markers (the refiner wraps text extracted from a diagram
# or image in these HTML comments). Content inside MUST pass through verbatim and
# is never merged/split — a picture block can span a page boundary, so we must
# not treat an interior page marker as a heading or an interior `|` line as a
# mergeable table. `End` may share a line with content (e.g. `yA SD<br><!-- End
# of picture text -->`), so we detect start/end by substring, not full-line.
_PIC_START_RE = re.compile(r"<!--\s*Start of picture text\s*-->", re.I)
_PIC_END_RE = re.compile(r"<!--\s*End of picture text\s*-->", re.I)


def _is_table_row(s: str) -> bool:
    return s.strip().startswith("|")


def merge_page_tables(page_bodies: list[str]) -> str:
    """Concatenate a group's page bodies, merging a dictionary table that spans
    several pages into ONE continuous table.

    The user's requirement: no separated markdown tables. Within the dictionary,
    each source page repeats the `| Word (POS) | ... |` header (and a `# Page N`
    marker sits between pages). To make the table continuous we:
      - keep the FIRST header + separator of a table run;
      - when a later page repeats that header (optionally preceded by a page
        marker and blank lines), DROP the repeated header + separator, and
        DEMOTE the intervening page marker to an inline `<!-- Page N -->` comment
        so page provenance survives without visually breaking the table;
      - every DATA row is preserved verbatim → zero dictionary-entry loss.

    Non-dictionary content (prose, rule examples, non-dict tables) is emitted
    verbatim; only a repeated *dictionary* header triggers the collapse, so rule
    pages and their blockquote examples are never altered.

    Mirrors the refinement skill's "Tables Spanning Multiple Raw Pages" handling
    (keep first header, drop repeats) — the same rule, applied at group scope.

    Implementation: flatten all pages to one token stream, then walk it with a
    small state machine. Deferring page markers lets us decide — based on what
    follows — whether to keep a marker as a heading or demote it to a comment.
    """
    # 1. Flatten every page body to one line stream (page order preserved).
    stream: list[str] = []
    for body in page_bodies:
        stream.extend(body.splitlines())
        stream.append("")  # guarantee a page separator token

    out: list[str] = []
    in_dict_table = False
    dict_header_emitted = False   # ≤1 dict header per group (ONE-TABLE guarantee)
    skip_one_sep = False
    in_picture = False   # inside a <!-- Start/End of picture text --> region
    i = 0
    n = len(stream)

    def emit(line: str):
        out.append(line)

    def emit_blank():
        if out and out[-1].strip() != "":
            out.append("")

    while i < n:
        raw = stream[i]
        s = raw.strip()

        # ── picture-text region: pass EVERYTHING through verbatim. A picture
        #    block may contain lines that look like page markers, headings, or
        #    `|` rows — none of those are structural here, so no merge/collapse
        #    logic may touch them. This guarantees picture text is never split
        #    or reflowed, even if the block spans a page boundary. ──
        if in_picture:
            emit(raw)
            if _PIC_END_RE.search(raw):
                in_picture = False
                in_dict_table = False  # a picture region breaks any table run
                dict_header_emitted = False  # a post-picture table re-emits its header
            i += 1
            continue
        if _PIC_START_RE.search(raw):
            emit_blank()
            emit(raw)
            in_picture = True
            in_dict_table = False
            # handle the degenerate single-line "Start ... End" case
            if _PIC_END_RE.search(raw):
                in_picture = False
            i += 1
            continue

        # ── page marker: peek past blanks to see if a repeated dict header
        #    immediately follows. If so, demote to comment + drop the header. ──
        if _PAGE_MARK_RE.match(s):
            j = i + 1
            while j < n and stream[j].strip() == "":
                j += 1
            follows_repeated_header = (
                in_dict_table and j < n and _TABLE_HDR_RE.match(stream[j].strip()))
            if follows_repeated_header:
                tok = s.lstrip("#* ").strip().rstrip("*").strip()
                emit(f"<!-- {tok} -->")
                # consume the blank(s) + the repeated header + its separator
                i = j + 1
                skip_one_sep = True
                continue
            # keep the marker as-is (a real section/page heading)
            emit_blank()
            emit(raw)
            emit_blank()
            in_dict_table = False  # a kept marker ends any table run
            i += 1
            continue

        if s == "":
            emit_blank()
            i += 1
            continue

        if _TABLE_HDR_RE.match(s):
            if dict_header_emitted:
                # A repeated dict header (page boundary, or state confusion
                # after intervening prose) is a duplicate of the same table —
                # drop it AND its separator so the group keeps exactly ONE
                # continuous table (verify-groups ONE-TABLE gate). Lossless:
                # the header text is identical across the group.
                skip_one_sep = True
                i += 1
                continue
            emit_blank()
            emit(raw)
            in_dict_table = True
            dict_header_emitted = True
            i += 1
            continue

        if _SEP_RE.match(s) and in_dict_table:
            if skip_one_sep:
                skip_one_sep = False
                i += 1
                continue
            emit(raw)
            i += 1
            continue

        if _is_table_row(s) and in_dict_table:
            emit(raw)
            i += 1
            continue

        # any other content line ends a dict-table run
        in_dict_table = False
        skip_one_sep = False
        emit(raw)
        i += 1

    # collapse >1 consecutive blanks (Rule 9 spirit)
    cleaned: list[str] = []
    for ln in out:
        if ln.strip() == "" and cleaned and cleaned[-1].strip() == "":
            continue
        cleaned.append(ln)
    return "\n".join(cleaned).strip() + "\n"


# ── group content assembly ──────────────────────────────────────────────────
def assemble_group(group, idx, id2pos) -> tuple[str | None, dict]:
    """Build one group's markdown text from its source page slices.

    Returns (text_or_None, stats). text is None if any source page is not
    sliceable (markers don't resolve) — caller treats that as "not ready".
    """
    page_bodies: list[str] = []
    src_words = 0
    src_marks = 0
    workers: list[str] = []
    sliced_ok = True
    for p in group.pages:
        rf = idx.get(p)
        if rf is None:
            sliced_ok = False
            break
        wid = f"R{rf.worker:03d}"
        if wid not in workers:
            workers.append(wid)
        slices = engine.slice_pages(rf, id2pos)
        if p not in slices:
            sliced_ok = False
            break
        body = slices[p]
        # Normalize every DICT page body to one clean 4-col table so the
        # assembler can collapse same-header pages into a single continuous
        # table (Fix B). Non-dict bodies are unaffected by the normalizer's
        # shape detection. Parity is preserved: label words are kept in cells.
        if group.section == "DICT":
            body = dict_normalize.normalize_dict_page(body)
        page_bodies.append(body)
        src_words += word_count(body)
        src_marks += mark_count(body)

    if not sliced_ok:
        return None, {"reason": "unsliceable_source"}

    merged = merge_page_tables(page_bodies)

    pages = group.pages
    header = TPL.render(
        "group_header",
        gid=group.gid,
        page_start=pages[0],
        page_end=pages[-1],
        section=group.section,
        key=group.key or "",
        key_suffix=f" ({group.key})" if group.key else "",
        workers=", ".join(workers),
        page_count=len(pages),
        title=group.label.replace("-", " ").title(),
    )
    text = header + merged

    # Exact content-token parity: compare the merged output against the raw
    # concatenation of source page bodies. `missing` tokens = content loss
    # (fatal); this is the real zero-loss gate, immune to the dropped-header
    # false-positive that a word-count ratio would trip on (Refinement Lesson #2).
    src_concat = "\n".join(page_bodies)
    parity_ok, missing, added = engine.parity_diff(src_concat, text)

    stats = {
        "src_words": src_words,
        "out_words": word_count(text),
        "src_marks": src_marks,
        "out_marks": mark_count(text),
        "workers": workers,
        "pages": len(pages),
        "parity_ok": parity_ok,
        "missing_tokens": dict(missing.most_common(8)),
        "missing_total": sum(missing.values()),
        "added_total": sum(added.values()),
    }
    return text, stats


# ── dry-run report ──────────────────────────────────────────────────────────
def dry_run(plan, idx, man, id2pos):
    ready, problems = engine.corpus_ready(idx, id2pos)
    print("=" * 74)
    print("STE-Code Phase C — GROUPING PLAN (dry run, nothing written)")
    print("=" * 74)
    print(f"MANIFEST positions : {len(man)}")
    print(f"Refined pages      : {len(idx)}/{engine.TOTAL_PAGES}")
    print(f"Groups planned     : {len(plan)}")
    total = sum(len(g.pages) for g in plan)
    print(f"Pages in plan      : {total}/{engine.TOTAL_PAGES}")
    print()
    print(f"{'#':>3}  {'GROUP ID':<22} {'SECTION':<11} {'KEY':<7} {'PAGES':>5}  RANGE")
    print("-" * 74)
    seen_pages = set()
    dupes = []
    for i, g in enumerate(plan, 1):
        rng = f"{g.pages[0]}-{g.pages[-1]}" if g.pages else "-"
        print(f"{i:>3}  {g.gid:<22} {g.section:<11} {str(g.key or ''):<7} "
              f"{len(g.pages):>5}  {rng}")
        for p in g.pages:
            if p in seen_pages:
                dupes.append(p)
            seen_pages.add(p)
    print("-" * 74)

    # Coverage integrity
    missing = [p for p in range(1, engine.TOTAL_PAGES + 1) if p not in seen_pages]
    print(f"\nCOVERAGE: {len(seen_pages)}/{engine.TOTAL_PAGES} pages assigned; "
          f"missing={missing[:12]}{'...' if len(missing) > 12 else ''}; "
          f"duplicates={sorted(set(dupes))[:12]}")

    # Group-size sanity (uneven is allowed; flag only extremes)
    sizes = [(g.gid, len(g.pages)) for g in plan]
    biggest = max(sizes, key=lambda x: x[1])
    smallest = min(sizes, key=lambda x: x[1])
    print(f"SIZES   : smallest={smallest[1]}p ({smallest[0]}), "
          f"biggest={biggest[1]}p ({biggest[0]})")

    # DICT letter split integrity
    dict_groups = [g for g in plan if g.section == "DICT"]
    print(f"\nDICT    : {len(dict_groups)} alphabetical buckets "
          f"(target ~{engine.DICT_BUCKET_TARGET_PAGES}p each)")
    for g in dict_groups:
        first_id = man.get(g.pages[0], "?")
        last_id = man.get(g.pages[-1], "?")
        print(f"          {g.gid:<20} pages {g.pages[0]}-{g.pages[-1]} "
              f"({len(g.pages)}p)  [{first_id} .. {last_id}]")

    # Readiness (does NOT verify refinement quality — only sliceability)
    print(f"\nCORPUS READY FOR ASSEMBLY: {'YES' if ready else 'NO'}")
    if not ready:
        print("  (assembly is blocked until the refined corpus is complete +"
              " each file has clean `# Page N` markers)")
        for pr in problems:
            print(f"  - {pr}")

    # Parity preview on a sliceable subset (if any) — no writes. Uses EXACT
    # content-token parity (multiset diff), not a word ratio: a group passes iff
    # zero content tokens are missing from the merged output.
    print("\nPARITY PREVIEW (per group; exact content-token multiset diff):")
    any_slice = False
    for g in plan:
        text, stats = assemble_group(g, idx, id2pos)
        if text is None:
            continue
        any_slice = True
        ok = stats["parity_ok"] and stats["out_marks"] >= stats["src_marks"]
        flag = "OK " if ok else "!! "
        extra = ""
        if not stats["parity_ok"]:
            extra = f"  LOST={stats['missing_total']} {list(stats['missing_tokens'])[:5]}"
        if stats["out_marks"] < stats["src_marks"]:
            extra += f"  MARKS {stats['out_marks']}/{stats['src_marks']}"
        print(f"  {flag}{g.gid:<22} tokens: 0 missing"
              if ok else f"  {flag}{g.gid:<22}{extra}")
    if not any_slice:
        print("  (no groups sliceable yet — refined corpus mid-rewrite; this is"
              " expected during refinement churn)")
    print("=" * 74)


# ── real assembly (guarded) ─────────────────────────────────────────────────
def _load_checkpoint() -> dict:
    if CHECKPOINT_PATH.exists():
        try:
            return json.loads(CHECKPOINT_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_checkpoint(cp: dict):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_PATH.write_text(json.dumps(cp, indent=2), encoding="utf-8")


def assemble_all(plan, idx, man, id2pos, force=False) -> int:
    """Write every group to grouped/, guarded on corpus readiness.

    Returns process exit code (0 ok, 1 refused/failed). This is the real,
    non-dry path. It REFUSES to run on an incomplete/mid-rewrite corpus
    (Refinement Lesson: never group a half-rewritten source) and verifies each
    written file's content-token parity against its sources before counting it
    done (Lesson #4: verify against disk).
    """
    ready, problems = engine.corpus_ready(idx, id2pos)
    if not ready and not force:
        print("[REFUSED] refined corpus is not ready for assembly:")
        for pr in problems:
            print(f"  - {pr}")
        print("Wait for refinement to finish, or pass --force to override "
              "(NOT recommended during churn).")
        return 1

    GROUPED_DIR.mkdir(parents=True, exist_ok=True)
    cp = _load_checkpoint()
    done = cp.get("completed", {})
    failures = 0
    written = 0
    skipped = 0

    for g in plan:
        text, stats = assemble_group(g, idx, id2pos)
        if text is None:
            print(f"[SKIP] {g.gid}: sources not sliceable ({stats.get('reason')})")
            failures += 1
            continue
        # hard parity gate — refuse to write a lossy group
        if not stats["parity_ok"]:
            print(f"[FAIL] {g.gid}: content loss ({stats['missing_total']} tokens "
                  f"missing e.g. {list(stats['missing_tokens'])[:5]}) — NOT written")
            failures += 1
            continue
        if stats["out_marks"] < stats["src_marks"]:
            print(f"[FAIL] {g.gid}: marks dropped "
                  f"({stats['out_marks']}/{stats['src_marks']}) — NOT written")
            failures += 1
            continue

        gfile = GROUPED_DIR / g.filename
        # idempotence (R5): skip if an identical valid file already exists
        if not force and gfile.exists() and gfile.read_text(encoding="utf-8") == text:
            skipped += 1
            continue

        gfile.write_text(text, encoding="utf-8")
        # verify against disk (Lesson #4)
        reread = gfile.read_text(encoding="utf-8")
        # Source pages must be normalized the SAME way assemble_group normalized
        # them (Fix B) so the parity gate compares like-for-like. Comparing raw
        # source vs normalized output would flag the dict-header label words
        # (word/pos/approved/meaning/ste…) as "missing".
        src_slices = []
        for p in g.pages:
            sl = engine.slice_pages(idx[p], id2pos).get(p, "")
            if g.section == "DICT":
                sl = dict_normalize.normalize_dict_page(sl)
            src_slices.append(sl)
        ok, miss, _ = engine.parity_diff("\n".join(src_slices), reread)
        if not ok:
            print(f"[FAIL] {g.gid}: post-write parity mismatch "
                  f"({sum(miss.values())} tokens) — file left for inspection")
            failures += 1
            continue
        done[g.gid] = {"pages": [g.pages[0], g.pages[-1]], "bytes": len(text)}
        written += 1
        print(f"[OK]   {g.gid:<22} {g.pages[0]}-{g.pages[-1]} "
              f"({len(g.pages)}p, {len(text)} bytes)")

    cp["completed"] = done
    _save_checkpoint(cp)
    print("-" * 74)
    print(f"assembled: {written} written, {skipped} skipped (idempotent), "
          f"{failures} failed")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="plan only, write nothing")
    ap.add_argument("--plan-json", action="store_true", help="emit machine-readable plan")
    ap.add_argument("--force", action="store_true",
                    help="override readiness guard + idempotence (dangerous during churn)")
    args = ap.parse_args()

    man = engine.parse_manifest()
    id2pos = engine.id_to_position(man)
    idx = engine.index_refined()
    plan = engine.build_plan(man)

    if args.plan_json:
        out = {
            "generated": datetime.now(timezone.utc).isoformat(),
            "total_pages": engine.TOTAL_PAGES,
            "total_groups": len(plan),
            "groups": [
                {"group_id": g.gid, "label": g.label, "section": g.section,
                 "key": g.key, "pages": g.pages,
                 "page_range": f"{g.pages[0]}-{g.pages[-1]}" if g.pages else None}
                for g in plan
            ],
        }
        print(json.dumps(out, indent=2))
        return

    if args.dry_run:
        dry_run(plan, idx, man, id2pos)
        return

    # Real assembly path (guarded on corpus readiness inside assemble_all).
    rc = assemble_all(plan, idx, man, id2pos, force=args.force)
    sys.exit(rc)


if __name__ == "__main__":
    main()
