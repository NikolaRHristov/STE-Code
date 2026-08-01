# Phase C Grouping — Full-Fix Work Order (zero content loss)

Status: IN PROGRESS. Goal: produce legible, uniform grouped/*.md so Phase D
(adapt) and Phase E (extend) can run, with **zero content loss vs
ste-code/extracted/ AND the spec**. Deterministic-first (LLM only as a
last-resort fallback for pages that fail deterministic parity).

## Ground truth established (evidence)
- The spec dictionary is CANONICALLY a 4-column table:
  `Word (POS) | Approved meaning / ALTERNATIVES | STE example | Non-STE example`.
  Confirmed in ste-code/extracted/ (raw spec text) — e.g. w072 page 286.
- The refined corpus is NOT format-uniform:
  - 36 dict files = clean `| Word (POS) |` GFM tables (TARGET shape).
  - 42 dict files = `#### WORD (POS) — APPROVED/UNAPPROVED` heading blocks.
  - Several "table" pages use a MESSY multi-column shape `|||**Word**<br>...`
    with empty leading cells + `<br>` line-wraps + continuation rows (empty
    first cell = continues the entry above).
- MANIFEST page-IDs drift ~1 page AHEAD of actual letter content across the
  WHOLE dictionary (32 boundary pages). e.g. pages 219–224 are labelled
  `2-1-E1..E6` but contain D-words; real E starts page 225. This is baked into
  the spec's pagination (blank pages carry the next letter's ID). SYMPTOM the
  user saw: group-017-dict-e-f starts with D-words (differentiate, difficult…).

## The four fixes

### Fix A — content-based DICT letter classification  [OWNER: main agent] — DONE (partial, honest scope)
IMPLEMENTED in group_engine.py: `_page_entry_letters`, `_build_page_letter_cache`,
`dict_letter_for_page`, wired into `classify_page`. Section classification still
comes from the MANIFEST; only the DICT letter key is content-derived.

SCOPE LIMIT (verified, do not "fix" naively): the override applies ONLY to pages
that are their own segment (`start == end`). Merged (C_merged) segments — where
a refined file has no internal page markers — keep the MANIFEST letter.
Rationale, learned the hard way by trying the alternatives:
  - Attributing a merged segment's dominant letter to every page it spans makes
    buckets OVERLAP (018 became 258-292 while 019 became 282-316) and breaks the
    `groups are contiguous page ranges` self-test.
  - Attributing the merged segment's FIRST letter to its first page, plus a
    monotonic high-water clamp, went badly wrong (pages classified 'W', buckets
    collapsed to a single `dict-d-m` 214-306). Content letters are not reliably
    monotonic across merged bodies, and the clamp then pins everything forward.
Net: pages 219-224 (D-words carrying `2-1-E*` IDs) still sit in 017-dict-e-f
because r055/r056 are merged files. The straddler splitter (`_maybe_split_straddler`)
is the correct place to fix that — it splits a merged body at the letter change —
and it already handles files that CROSS a boundary. Remaining gap: a merged file
wholly INSIDE the wrong bucket is not split by it.
STATE: 54/54 self-tests pass, COVERAGE 434/434 contiguous, CORPUS READY YES.

### Fix B — DICT table normalizer (block + messy-multicol → clean 4-col GFM) [OWNER: subagent]
A deterministic transform applied at grouping assembly time (NOT a refined-file
edit — we do not touch ste-code/refined/). For each dict page body:
  - BLOCK format (`#### WORD (POS) — STATUS` + `- **Meaning:**` / `- **Approved
    alternative:**` / `> **STE:**` / `> **Non-STE:**`): emit one table row per
    WORD. c1=`WORD (POS)` (+status kept), c2=meaning/alternative(s) joined with
    `<br>`, c3=STE example(s), c4=Non-STE example(s). Multi-alternative entries:
    keep every alternative and its example pair (either multiple rows sharing the
    word, or `<br>`-joined within cells — pick one and keep ALL tokens).
  - MESSY multi-col (`|||**Word**...`): drop the empty leading columns, unwrap
    `**bold**`, fold continuation rows (empty first cell → append to the row
    above), strip in-cell `<br>` per the refinement rule (lossless), keep header
    once.
  - CLEAN table: pass through (already correct).
Non-dict content (rules prose, examples, picture text) is emitted verbatim.

PARITY REQUIREMENT (the hard gate — Lesson #2): the normalizer must lose ZERO
CONTENT tokens. Format labels that a clean table legitimately drops are NOT
content and must be normalized away on BOTH sides before comparing:
  page markers, `> **Source:**`/`> **Pages:** N–M of 434` file boilerplate,
  the `Approved Words`/`Unapproved Words`/`Dictionary Entries` subheadings,
  the `**Meaning:** **Approved alternative:** **Examples:** **STE:** **Non-STE:**`
  role labels, `<br>`, markup tags, HTML comments. REAL content that must be
  preserved: every word, POS, status (APPROVED/UNAPPROVED), meaning text,
  alternative words, both example sentences, editorial notes ("page 294 is
  blank"), and reference-table rows (r100: `reference t7…`).
Prototype already shows block→table loses only boilerplate + labels after this
normalization — deterministic is viable; do NOT introduce an LLM unless a
specific page fails deterministic parity, and even then prefer fixing the parser.

### Fix C — section-heading matching for Phase D  [OWNER: main agent] — DONE
IMPLEMENTED in .agents/tools/adaptation/adapt_batch.py:
  - `_SECTION_GROUP_RE` — matches the header Phase C ACTUALLY emits, `# Rules Sec N`.
  - `_SECTION_HEAD_RE` — canonical `# N. Title` kept as fallback (raw/refined text).
  - `_find_section_head()` — tries group shape first, then canonical.
  - `_NON_RULES_GROUP_RE` — terminator for the last rule section.
  - `extract_section_source()` — rewritten to use them, and the next-heading
    search is now done on absolute offsets (the old code searched a `rest` slice
    but compared offsets against the full string).
WHY sec9 needed special handling: it is the last rule section, so with no
section-10 heading the slice ran to EOF and swallowed the whole dictionary
(569,561 chars). It now stops at the first non-rules group header
(`# Dictionary Intro`), giving 27,912 chars.
VERIFIED against the real ste-code/grouped/ text (776,247 chars):
  sec1 38,785ch 13/14 rules | sec2 7,942ch | sec3 15,028ch 6/7 | sec4 16,106ch 4/5
  sec5 12,452ch 4/5 | sec6 15,694ch 5/6 | sec7 6,942ch 3/3 | sec8 15,880ch 7/7
  sec9 27,912ch 3/4        →  RESOLVED 9/9 (was 0/9).
Note: a missing `Rule N.1` in the id scan is not missing text — several sections
introduce their first rule as a prose heading rather than `### Rule N.1`; the
rule body is still inside the slice the worker receives.

### Fix D — verifier one-table check format-aware  [OWNER: subagent, after B]
After Fix B every dict group SHOULD be a single clean table again, so the
existing `hdrs == 1` check will pass. Keep the check but make it tolerant: a dict
group passes if it has exactly one table header AND no stray `#### WORD` blocks
left (i.e. normalization was complete). Report, don't hard-fail, on a group that
is legitimately all-prose.

## Final gates (must all pass before downstream)
1. phase-c-run.py --verify → all 24 groups parity OK + marks OK + one-table OK.
2. Cross-check vs ste-code/extracted/: content-token multiset of grouped/ ⊇
   content tokens of extracted/ (after boilerplate normalization) — zero missing.
3. Cross-check vs spec MANIFEST page coverage: 434/434, no gap/overlap.
4. Spot-check the 6 straddler boundaries + the D/E boundary the user flagged.

## Constraints (from user + exchange.md)
- DO NOT edit ste-code/refined/ (normalize at grouping time only).
- DO NOT write helper scripts that silently transform then vanish; the normalizer
  is a committed, tested engine function with a parity gate.
- Deterministic-first; LLM only as explicit, parity-gated fallback.
- Keep prompt/skill/gate in agreement (one engine module).
