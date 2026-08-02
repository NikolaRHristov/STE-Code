---
name: grouping
description: > **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
category: dev
capability: developing-and-changing-the-standard
source: /Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code/.agents/skills/grouping
layout: ste-code-canonical-v1
---

# Grouping & Semantic Chunk Assembly (Phase C)

> **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
> STRICT_RULES (R1–R6) from `lib/pipeline_core.py` apply.

## What changed (read this first)
Grouping is now **deterministic pure Python** — there is **no LLM in the copy
path**. The old runner handed the entire 109-file → ~24-group concatenation
(~600 KB of output) to a single free-tier agent and asked it to re-emit every
byte; per the Refinement agent's lessons (`.agents/feedback/exchange.md`) that
guarantees mid-stream truncation, i.e. silent corpus-wide content loss. Because
grouping only **moves bytes, never re-types them**, content cannot be lost. The
prompt/skill/gate agree because the plan lives in ONE module shared by the
assembler, verifier, and runner (Refinement Lesson #1).

## The tools
| File | Role |
|---|---|
| `.agents/tools/grouping/group_engine.py` | Section oracle + plan + parity primitives (imported by everything else — single source of truth) |
| `.agents/tools/grouping/group_batch.py` | Assembler: slices refined pages, merges dict tables, writes groups, enforces parity gate |
| `.agents/tools/grouping/verify-groups.py` | Post-assembly verifier (coverage, parity, marks, one-table, picture integrity) |
| `.agents/tools/grouping/test_grouping.py` | Self-tests (dry-run tuning harness) — run after any change |
| `.agents/tools/runners/phase-c-run.py` | Thin CLI wrapper delegating to the above (legacy flags preserved) |

## Input / Output
- **Input:** `ste-code/refined/rNNN-pA-B.md` (109 refined page files) +
  `spec/issue-09-2025/page-dir/MANIFEST.md` (position → page-ID).
- **Output:** `ste-code/grouped/group-NNN-<label>.md` (~24 groups) +
  `.agents/state/grouping-checkpoint.json`.

## The section oracle — MANIFEST page-IDs, NOT section-types.md
Section membership is read from **MANIFEST page-ID prefixes**, which are the
spec's own churn-proof pagination. Do **not** trust:
- `references/section-types.md` — its ranges are **STALE** (it claims DICT ends
  p360 / APPENDIX 361-434, but the dictionary runs A..Y through **page 426**).
- the refined files' internal page markers — they churn during refinement and
  the refiner is **evolving the marker format** (some files use `# Page 12 of
  434`, others `## Page 1-2-2`). The slicer tolerates BOTH via the MANIFEST.

Prefix → section mapping (`classify_page` in group_engine.py):
`FRONT-MATTER`/`HI-*` → FRONT · `TOC*`/`SRI*`/roman → NAV · `1-0-*` → INTRO ·
`1-N-*` → RULES chapter N · `2-0-*` → DICT_INTRO · `2-1-<Letter>*` → DICT letter ·
past-manifest / unknown → APPENDIX (never dropped).

## Grouping rules (enforced in code, not prose)
1. **Never split a dictionary entry** — letters change on page boundaries and we
   group whole pages, so an entry (which lives within a page's table) is intact.
2. **One continuous table per dict group** — consecutive pages repeat the
   `| Word (POS) | … |` header; the assembler keeps the FIRST header+separator,
   drops repeats, and demotes the intervening page marker to an inline
   `<!-- Page N -->` comment (provenance kept, table unbroken). See
   `merge_page_tables`.
3. **Never split picture text** — content inside `<!-- Start of picture text -->`
   … `<!-- End of picture text -->` passes through verbatim; interior page
   markers / `|` rows are never treated as structural, even across a page break.
4. **Group by logical section** — RULES split one group per chapter (Sec 1..9);
   FRONT/NAV/INTRO/DICT_INTRO/APPENDIX each one group; uneven page counts are
   fine (e.g. INTRO is a single page — that's correct).
5. **DICT split into balanced alphabetical buckets** — `_bucket_dict_letters`
   targets ~26p, caps ~36p, keeps whole letters together, never orphans a tiny
   tail letter (Y merges into T-Y). Split so the DOWNSTREAM adaptation LLM reader
   isn't handed a 285-page monolith (Lesson #3 applies to the consumer).

## The parity gate — exact content-token multiset, NOT a word ratio
`group_engine.parity_diff(src, out)` compares the multiset of content tokens
after stripping ONLY structural boilerplate (page markers, dict headers/
separators, HTML comments, markup tags, repeated page stamps). A group passes iff
**zero content tokens are missing**. This is stronger than the refinement ratio
gate and immune to its failure mode: dropped repeated headers legitimately lower
a word count, so a ratio would wrongly fail correct output (Refinement Lesson #2:
never count formatting as content). Marks (`<mark>` highlights) must also never
decrease.

## Execution
```bash
# 1. Preview the plan + readiness + per-group parity (writes NOTHING) — do this
#    freely, any time, even while refinement is still running:
python3 .agents/tools/runners/phase-c-run.py --dry-run

# 2. Run the self-tests after ANY change to the engine/assembler:
python3 .agents/tools/grouping/test_grouping.py

# 3. Real assembly — REFUSES unless the refined corpus is complete and every
#    file's page markers cleanly resolve (corpus_ready guard). Never group a
#    half-rewritten corpus. Add --verify to run the post-assembly gate:
python3 .agents/tools/runners/phase-c-run.py --verify

# machine-readable plan:
python3 .agents/tools/grouping/group_batch.py --plan-json
```

Legacy `--agent` / `--model` flags are accepted but ignored (grouping is
deterministic — there is no agent to select). `--force` overrides the readiness
guard + idempotence (dangerous during churn — avoid).

## Safety / idempotence
- `--dry-run` is the default-safe mode: plan only, zero writes.
- Real assembly is **gated on `corpus_ready()`** — refuses on an incomplete or
  mid-rewrite corpus.
- Idempotent (R5): a group whose on-disk bytes already match is skipped.
- Every written group is re-read and parity-checked against its sources before
  being counted done (Lesson #4: verify against disk, not self-reports).

## Quality checks
- Coverage: all 434 pages in exactly one group (no gap/overlap) — asserted in
  `test_grouping.py::t_plan_coverage` and `verify-groups.py`.
- Parity: 0 content tokens missing per group.
- Marks: `<mark>` count never decreases.
- One table per dict group; picture blocks balanced within each group.

## References
- Section oracle: MANIFEST page-IDs (NOT `references/section-types.md`, which is stale)
- Refinement lessons borrowed: `.agents/feedback/exchange.md`
- Group naming: `group-NNN-<semantic-label>.md`
