# STE-Code Grouping (Phase C) — Analysis, Tips & Tool Improvements

> Author: Grouping agent. Companion to `.agents/feedback/exchange.md`
> (extraction + refinement lessons). This file records what the grouping stage
> found in the refined corpus, the bugs/fragilities discovered in the grouping
> tooling, and the fixes that make Phase C run clean. Written to
> `ste-code/grouping/` per the user's instruction so the next agent inherits it.

---

## TL;DR

Grouping is deterministic pure-Python (no LLM in the copy path — bytes are moved,
never re-typed), so *content* cannot be lost. But it is only as good as its two
assumptions about the refined input:

1. **Every refined file resolves cleanly to its page range** via internal page
   markers (`corpus_ready()` gate). **44/109 files failed this** on first
   inspection — not from content loss, but from three benign *marker-drift*
   patterns the strict slicer rejected.
2. **Dictionary pages are `| Word (POS) |` markdown tables.** **This is false for
   ~42/109 files**, which are `#### WORD (POS)` heading blocks. The table-merge
   and the verifier's "one-table-per-dict-group" check are built for tables and
   **misfire on block-format groups**.

Both are input-shape problems, not grouping-logic problems. Neither risks content
loss (the parity gate is a content-token multiset diff), but #1 blocks assembly
and #2 makes the post-assembly verifier report false failures. Fixes for both are
below.

---

## Finding 1 — Marker drift blocks `corpus_ready()` (3 patterns)

`group_engine.slice_pages()` splits a refined file into `{page: body}` by reading
its internal page markers and requires the resolved sequence to EXACTLY equal the
file's declared range (from its `rNNN-pA-B.md` name). Any deviation → the file is
"unsliceable" → `corpus_ready()` returns NO → assembly refuses. That strictness
is correct (never slice a half-rewritten corpus blind), but it also trips on
*finished* files whose markers merely drifted in format. The 44 flagged files
fell into exactly three shapes:

| Pattern | Example | Markers found vs expected | Why it fails |
|---|---|---|---|
| **A — dual co-located markers** | `r008-p29-32` | `[29,29,30,30,31,31,32,32]` vs `[29,30,31,32]` | Each page has BOTH `# Page 29 of 434` AND a spec page-ID `**Page TOC-2**`; both resolve to pos 29 → duplicates. |
| **B — missing leading marker** | `r030-p117-120` | `[118,119,120]` vs `[117,118,119,120]` | The first page's per-page marker is absent (only the `# Page 117–120 of 434` *range header* exists, which the slicer ignores) → range starts one short. |
| **C — collapsed to first marker** | `r054-p213-216` | `[213]` vs `[213,214,215,216]` | Block-format dict pages kept only the FIRST `# Page N` marker; pages 214-216 have no per-page marker at all. |

### The 6 that actually matter (cross-boundary straddlers)

Most flagged files sit **wholly inside one group**, so even a wrong internal split
doesn't change which group their content lands in — the group takes all their
pages regardless. The dangerous ones are files that **span a group boundary**,
where the page split decides which side each entry goes to:

```
r055-p217-220  D→E-F  (016-dict-d | 017-dict-e-f)
r078-p309-312  J-N→O-P (019-dict-j-n | 020-dict-o-p)
r085-p337-340  O-P→Q-R (020-dict-o-p | 021-dict-q-r)
r090-p357-360  Q-R→S   (021-dict-q-r | 022-dict-s)
r098-p389-392  S→T-Y   (022-dict-s | 023-dict-t-y)
r107-p425-428  T-Y→APP (023-dict-t-y | 024-appendix)
```

For these six, the repair MUST restore a correct per-page marker at each page
boundary so entries land in the right alphabetical bucket. For the other 38, a
marker repair is still needed to pass the gate, but a mis-split would be
cosmetically invisible (same destination group).

### ⚠️ A parity-gate blind spot the straddlers expose

`parity_diff()` compares the multiset of content tokens between *source slices*
and *output* — but BOTH sides come from the SAME `slice_pages()`. So if a page is
mis-attributed (content assigned to page 214 instead of 213), the source-of-record
and the output are mis-attributed *identically*, and parity still passes. **The
parity gate cannot detect a page-boundary mis-split within a straddler file.**
That is why the straddlers must be repaired at the source (correct markers),
not papered over downstream. See "Tool improvement 3" for a boundary-integrity
check that closes this hole.

### Fix (deterministic, no LLM, no content touched)

Restore one clean `# Page N of 434` marker per page in each flagged file:
- **Pattern A:** keep the sequential `# Page N of 434`, drop/keep the spec
  `**Page …**` as an inline provenance comment (never as a second position-
  resolving marker).
- **Pattern B/C:** re-insert the missing per-page markers at the correct entry
  boundaries. For block-format dict files this means placing `# Page N of 434`
  before the first `#### WORD` entry that belongs to page N. The page→first-entry
  boundary is recoverable from the extracted source (`ste-code/extracted/`),
  which retained per-page structure, and cross-checked against the MANIFEST
  letter ranges.

This is exactly what `.agents/tools/grouping/repair_markers.py` does (authored by
the refinement/repair agent). Only marker lines are added/normalized — **zero
content bytes change** — verifiable with `git diff --stat` (only marker lines
move) and re-confirmed by the content-token parity gate after grouping.

---

## Finding 2 — Dictionary is NOT format-uniform (tables vs blocks)

The refinement fix (exchange.md Bug 1) mandates dictionary pages be kept as
`| Word (POS) | meaning | STE | Non-STE |` markdown tables (1:1 with source →
no free-tier truncation). But the corpus on disk is **mixed**:

```
TABLE-format  (| Word (POS) |) : 36 files
BLOCK-format  (#### WORD (POS)): 42 files   ← the old truncation-prone shape
neither/prose                  : 31 files
```

Per-DICT-group composition (what the merge + verifier actually see):

```
014-dict-a-b   142-175  TABLE:34
015-dict-c     176-199  TABLE:24
016-dict-d     200-218  TABLE:13 BLOCK:6
017-dict-e-f   219-250  TABLE:24 BLOCK:6 NONE:2
018-dict-g-i   251-282  TABLE:22 NONE:10
019-dict-j-n   283-310  BLOCK:26 TABLE:2
020-dict-o-p   311-338  BLOCK:28
021-dict-q-r   339-358  BLOCK:20
022-dict-s     359-390  BLOCK:32
023-dict-t-y   391-426  BLOCK:36
```

### Consequences for the grouping tools

- **`merge_page_tables()`** only collapses repeated `| Word (POS) |` headers.
  On a block-format group there are no table headers to merge, so it passes the
  content through verbatim — **safe, no loss**, but the group is NOT a single
  continuous table (it's a run of `#### WORD` blocks).
- **`verify-groups.py` one-table check** (`hdrs == 1`) then **FALSELY FAILS**
  every block-format dict group (they have `hdrs == 0`). Groups 019–023 (and
  partially 016–018) would all report `FAIL … single continuous table
  (headers=0, expect 1)` even though grouping did everything correctly.

### Two valid resolutions

1. **(Preferred, aligns with refinement fix) Normalize block→table upstream.**
   The refinement stage should re-emit the 42 block files as GFM tables so the
   *entire* dictionary is uniform. This is a refinement-stage job (it owns the
   format contract), removes the truncation-prone shape from the corpus, and
   makes the grouping verifier's one-table invariant true everywhere. Grouping
   should NOT silently convert format — that would be an LLM-free regex rewrite
   of content structure, exactly the "helper-script silently corrupts content"
   anti-pattern (exchange.md ⚠️). Grouping moves bytes; it does not re-shape them.

2. **(If block format is intentionally kept) Make the verifier format-aware.**
   Change the one-table check to: *"a dict group has EITHER exactly one table
   header OR zero table headers with well-formed `#### WORD (POS)` entry blocks,
   and never a mix that fragments a single letter."* i.e. assert structural
   coherence per group, not "table-ness". See "Tool improvement 2".

Until one of these lands, treat a `headers=0` one-table failure on a
block-format dict group as a **known false positive**, not a grouping defect —
confirm via the parity + marks lines on the same group (those are the real
content gates).

---

## Tool improvements (recommended patches to `.agents/tools/grouping/`)

### 1. Make `corpus_ready()` / `slice_pages()` tolerate the 3 marker patterns
Rather than reject any file whose markers ≠ exact range, add a *reconciliation*
step BEFORE declaring unsliceable:
- collapse consecutive duplicate positions (Pattern A: `[29,29,30,30]`→`[29,30]`);
- if the first declared page has no marker but the rest form a contiguous tail,
  treat the file's leading block (up to the first found marker) as that missing
  first page (Pattern B);
- if only the first marker is present and the file declares N pages, fall back to
  MANIFEST letter-range boundaries or extracted-source page splits to place the
  missing interior markers (Pattern C).
Keep the STRICT behavior available behind a flag for churn detection, but let a
finished-but-drifted corpus group without a manual repair pass. (The repair-file
approach also works and is more auditable — pick one and make it the documented
path so prompt/skill/gate agree, per exchange.md Lesson #1.)

### 2. Make the one-table verifier format-aware (see Finding 2, option 2)
`verify-groups.py`: replace the hard `hdrs == 1` with a per-group structural
check that accepts either a single merged table OR a clean sequence of
`#### WORD (POS)` blocks, and independently asserts "no letter is split across
two groups except at an intended page edge".

### 3. Add a boundary-integrity check for straddler files (closes the parity blind spot)
Because `parity_diff()` uses the same slicer on both sides, it can't catch a
page-boundary mis-split inside a file that spans two groups. Add a check that,
for each of the 6 straddler files, the LAST entry before the boundary and the
FIRST entry after it match the MANIFEST's expected letter for those pages (e.g.
r055 boundary: page 218 must still be 'D…', page 219 must be 'E…'). This is a
cheap alphabetical-monotonicity assertion at the 6 known boundaries.

### 4. Orchestration (borrowed from exchange.md Lesson #5 + poll-vs-wait.md)
Grouping itself is a single fast deterministic process (no worker fan-out), so
the free-tier/429 concerns don't apply to Phase C. But when this stage is chained
into `launch-downstream.sh` (C→D→E→F), the DOWNSTREAM adaptation workers DO fan
out — for those, keep ≤3 concurrent, launch each as its own `background=true`
process (not a parent for-loop that gets reaped ~30-40s), and MONITOR with quick
`ps | grep` + log tails + output mtimes. **Never** use long foreground
`sleep`/`wait` or `process(action='wait')` blockers — they freeze the turn and
block mid-turn steering. Poll, don't wait.

---

## Borrowed lessons applied (from exchange.md)

1. **Prompt/skill/gate must agree** → the plan lives in ONE module
   (`group_engine.py`) imported by assembler + verifier + runner. When changing
   the marker or dict-format contract, update the engine, the SKILL.md, AND the
   verifier together.
2. **Never count formatting as content** → the parity gate is a content-token
   MULTISET diff after stripping markers/headers/tags/boilerplate, not a word
   ratio. Dropping a repeated dict header legitimately lowers word count; the
   multiset diff correctly passes it.
3. **Explosion is the enemy of free-tier workers** → DICT is split into ~26-page
   alphabetical buckets so the downstream adaptation LLM isn't handed a 285-page
   monolith. (Grouping has no generation budget itself.)
4. **Verify against DISK, not self-reports** → every written group is re-read and
   re-parity-checked against its source slices before being counted done.
5. **No helper-script content transforms** → grouping never regex-rewrites entry
   content; it only relocates whole page bodies and drops *repeated structural*
   headers. Any format normalization (block→table) belongs to refinement, done
   with fidelity, not to a grouping-time script.

---

## Run recipe (once corpus_ready == YES)

```bash
cd <repo-root>
# 1. Preview — plan + readiness + per-group parity, writes nothing (safe anytime):
python3 .agents/tools/runners/phase-c-run.py --dry-run

# 2. Assemble + post-assembly verify (parity, marks, coverage, one-table, pics):
python3 .agents/tools/runners/phase-c-run.py --verify

# 3. Machine-readable plan if needed:
python3 .agents/tools/grouping/group_batch.py --plan-json
```

Output: `ste-code/grouped/group-NNN-<label>.md` (24 groups) +
`.agents/state/grouping-checkpoint.json`. Assembly is idempotent (R5) and
REFUSES on an incomplete/mid-rewrite corpus (never group half-rewritten input).

## Verified plan (24 groups, 434/434 pages, no gap/overlap)

```
001-front-matter    FRONT        1-27   (27p)
002-toc-and-nav     NAV         28-40   (13p)
003-introduction    INTRO       41-41    (1p)
004..012 rules-sec-1..9  RULES  42-124
013-dictionary-intro DICT_INTRO 125-141 (17p)
014-dict-a-b .. 023-dict-t-y  DICT  142-426 (10 buckets, ~26p target)
024-appendix        APPENDIX   427-434  (8p)
```
