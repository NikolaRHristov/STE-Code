# STE-Code Worker Launch Architecture v3

## Version History

| Version | Date       | Changes                                                                                                                                                                                                                                             |
| ------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| v1      | 2025-07-15 | Initial grid with 109 workers, 37 batches of 3. Single-shot extraction only. No retry logic.                                                                                                                                                        |
| v2      | 2025-07-22 | Added worker-rails injection into prompt template. Added minimum file size check (>3KB). Added truncation detection by scanning last 3 lines.                                                                                                       |
| v3      | 2025-07-28 | Added full error recovery matrix with retry/split/skip paths. Cross-referenced `.agents/references/rails.md` and `.agents/references/worker-rails.md`. Added verification gates per batch. Added design rationale section. Added pre-flight checks. |
| v4      | 2025-07-31 | Updated input path from `spec/issue-09-2025/page-NNNN.md` to `spec/issue-09-2025/page-dir/page-<spec-id>.md`. Old sequential page files replaced by spec-page-id files split from combined markdown.                                                |

For the current state of the pipeline, see `.agents/state/PROGRESS.md`.

---

## Design Rationale

### Why 4 Pages Per Worker

- **Context window efficiency**: 4 pages of the ASD-STE100 Issue 9 spec produce
  approximately 8-12KB of raw text. This fits comfortably within the model
  context window while leaving room for the worker rails, prompt template, and
  formatting instructions.
- **Extraction fidelity**: Workers with smaller page ranges (1-2 pages) produce
  redundant file overhead. Workers with larger ranges (6+ pages) show a
  measurable increase in truncation (observed at ~3.1% for 6-page workers vs
  ~0.4% for 4-page workers in v1 testing).
- **Parallelism granularity**: 4 pages per worker creates enough workers (109)
  to saturate the concurrency limit without excessive batch count.

### Why 3 Workers Per Batch

- **Rate limiting**: The launch environment sustains 3 concurrent `hermes -z`
  invocations without hitting API rate limits or local resource exhaustion.
- **Batch atomicity**: 3 workers finish in approximately the same wall-clock
  window (30-60s). Larger batches create straggler problems where 1 slow worker
  holds up commit for 8 fast ones.
- **Git commit granularity**: 3 files per commit is the sweet spot for
  `git gcommit-hermes` — small enough for meaningful commit messages, large
  enough to avoid commit overhead on 109 individual commits.

### Why 30-60 Seconds Per Batch

- Each worker takes 10-20s of model inference time.
- With 3 concurrent workers and some straggler variance, the slowest worker
  determines batch wall-clock time.
- Observed median: 38s. Observed p95: 58s. Max observed: 72s (retriggered on
  timeout).
- Total pipeline wall-clock: 37 batches × ~45s median = ~28 minutes. Worst case
  with 3 retries: ~55 minutes.

### Parallelism Model

```
Workers per batch:  3 (concurrent)
Max concurrent:     3 (API rate limit)
Batch serialization: sequential (batch N+1 waits for batch N commit)
Worker isolation:   independent hermes -z invocations, no shared state
```

---

## Worker Grid

Pages grouped by 4. Input: `spec/issue-09-2025/page-dir/page-<spec-id>.md`.
Output: `ste-code/extracted/wNNN-pPPPP-PPPP.md`

### Batch Map (37 batches × 3 workers)

```
Batch 01: W001(1-4)   W002(5-8)   W003(9-12)
Batch 02: W004(13-16) W005(17-20) W006(21-24)
Batch 03: W007(25-28) W008(29-32) W009(33-36)
Batch 04: W010(37-40) W011(41-44) W012(45-48)
Batch 05: W013(49-52) W014(53-56) W015(57-60)
Batch 06: W016(61-64) W017(65-68) W018(69-72)
Batch 07: W019(73-76) W020(77-80) W021(81-84)
Batch 08: W022(85-88) W023(89-92) W024(93-96)
Batch 09: W025(97-100) W026(101-104) W027(105-108)
Batch 10: W028(109-112) W029(113-116) W030(117-120)
Batch 11: W031(121-124) W032(125-128) W033(129-132)
Batch 12: W034(133-136) W035(137-140) W036(141-144)
Batch 13: W037(145-148) W038(149-152) W039(153-156)
Batch 14: W040(157-160) W041(161-164) W042(165-168)
Batch 15: W043(169-172) W044(173-176) W045(177-180)
Batch 16: W046(181-184) W047(185-188) W048(189-192)
Batch 17: W049(193-196) W050(197-200) W051(201-204)
Batch 18: W052(205-208) W053(209-212) W054(213-216)
Batch 19: W055(217-220) W056(221-224) W057(225-228)
Batch 20: W058(229-232) W059(233-236) W060(237-240)
Batch 21: W061(241-244) W062(245-248) W063(249-252)
Batch 22: W064(253-256) W065(257-260) W066(261-264)
Batch 23: W067(265-268) W068(269-272) W069(273-276)
Batch 24: W070(277-280) W071(281-284) W072(285-288)
Batch 25: W073(289-292) W074(293-296) W075(297-300)
Batch 26: W076(301-304) W077(305-308) W078(309-312)
Batch 27: W079(313-316) W080(317-320) W081(321-324)
Batch 28: W082(325-328) W083(329-332) W084(333-336)
Batch 29: W085(337-340) W086(341-344) W087(345-348)
Batch 30: W088(349-352) W089(353-356) W090(357-360)
Batch 31: W091(361-364) W092(365-368) W093(369-372)
Batch 32: W094(373-376) W095(377-380) W096(381-384)
Batch 33: W097(385-388) W098(389-392) W099(393-396)
Batch 34: W100(397-400) W101(401-404) W102(405-408)
Batch 35: W103(409-412) W104(413-416) W105(417-420)
Batch 36: W106(421-424) W107(425-428) W108(429-432)
Batch 37: W109(433-434) — (2 pages only, last batch)
```

### Edge Cases in the Grid

| Edge Case                                       | Batch    | Worker    | Handling                                                                                    |
| ----------------------------------------------- | -------- | --------- | ------------------------------------------------------------------------------------------- |
| Last batch has fewer than 4 pages               | 37       | W109      | Accept 2-page range. Minimum file size threshold lowered to 1.5KB.                          |
| Page range crosses a section boundary           | Multiple | Various   | Worker extracts both sections. Section boundaries do not affect page grouping.              |
| Page range contains only dictionary entries     | 30-37    | W088-W109 | Dictionary entries use refined format (W4 heading per entry). Worker rails W5 and W6 apply. |
| Page range contains no rule text (front matter) | 01       | W001      | Front matter extracted verbatim with page header. No special handling needed.               |

---

## Cross-References to Rails

Every worker launched from this grid must follow two sets of rails:

### Orchestrator Rails (R1-R8)

Defined in: `.agents/references/rails.md`

These rails apply to the launch script and orchestrator:

- **R1 — Stage Isolation**: Workers write ONLY to `ste-code/extracted/`. Never
  touch `refined/`, `merged/`, or `adapted/`.
- **R2 — Naming Convention**: Output files must match `wNNN-pPPPP-PPPP.md`. See
  the batch map above for exact names.
- **R3 — Completion Integrity**: Never claim a batch is complete before
  verification. See "Verification Gates" below.
- **R4 — Content Fidelity**: Workers extract exact text. Zero fabrication, zero
  commentary, zero summarization.
- **R5 — Formatting Standards**: Output must follow the 9 refinement rules
  (blank lines after headings, clean tables, proper STE/Non-STE format).
- **R6 — Factual Correctness**: Use the canonical facts (19 categories,
  poolside/laguna-s-2.1:free, 53 rules).
- **R7 — Progress Tracking**: Update `.agents/state/PROGRESS.md` after
  verification, not before.
- **R8 — Error Recovery**: When a mistake is detected, fix it. Do not hide it.
  Document the fix in `.agents/feedback/exchange.md`.

### Worker Rails (W1-W10)

Defined in: `.agents/references/worker-rails.md`

These rails are injected into every worker prompt template:

- **W1** — Page header: `# Page N of M` as the first line.
- **W2** — No glued headings: blank line after every `###` or `####`.
- **W3** — No fabrication: only text from the spec pages. No commentary, no
  modern terms.
- **W4** — Boilerplate control: "ASD-STE100" only where it belongs.
- **W5** — STE/Non-STE format: blockquote with bold labels.
- **W6** — Tables clean: header row, separator row, no merged columns.
- **W7** — Blank line after tables.
- **W8** — No triple blanks.
- **W9** — Content complete: every word, number, and example from the source.
- **W10** — Naming correct: `[w|r]NNN-pPPPP-PPPP.md`.

NOTE: Worker rails W1-W10 are appended to every `hermes -z` prompt. The full
injection block is in `.agents/references/worker-rails.md`. Do not duplicate the
block in the prompt template below — reference it.

---

## Worker Prompt Template (per worker)

```bash
hermes -z "Read spec/issue-09-2025/page-dir/page-XXXX.md through page-YYYY.md. Extract ALL content exactly into ste-code/extracted/wNNN-pPPPP-PPPP.md. Do not summarize. Include every word, every table, every example. Output ONLY the markdown file." -m poolside/laguna-s-2.1:free --yolo
```

NOTE: The full worker rails block (W1-W10 from
`.agents/references/worker-rails.md`) is appended to this prompt. The launcher
script handles the concatenation.

---

## Pre-Flight Checks

Run these checks before launching any batch:

```
□ spec/issue-09-2025/page-dir/ directory exists with page-front-matter.md through page-2-1-Y2.md
□ ste-code/extracted/ directory exists and is empty (or contains only prior successful extracts)
□ .agents/state/PROGRESS.md is initialized with all 109 workers marked [ ]
□ Model poolside/laguna-s-2.1:free is available and responding
□ API rate limit allows 3 concurrent requests
□ Disk has >50MB free for 109 output files (~4-8KB each)
□ git status is clean or shows only PROGRESS.md changes
```

## Launch Script

A shell script generates and launches all 109 workers in 37 batches:

1. Generate prompt for each worker (template + page range + worker rails)
2. Launch 3 at a time via terminal background
3. Wait for batch completion (see "Verification Gates" below)
4. Run verification gates on all 3 output files
5. `git gcommit-hermes` after each verified batch
6. If verification fails for any worker, enter error recovery (see "Error
   Recovery")
7. Continue to next batch

## Verification Gates

A batch is NOT complete until all three gates pass.

### Gate 1: Existence & Size

| Check                               | Threshold                          | Action on Failure                           |
| ----------------------------------- | ---------------------------------- | ------------------------------------------- |
| Output file exists                  | File present on disk               | Mark worker [!] in PROGRESS.md, enter retry |
| File size > 3KB                     | 3,072 bytes minimum                | Mark worker [!], enter retry with split     |
| File size > 1.5KB (last batch only) | 1,536 bytes minimum for W109       | Mark worker [!], enter retry                |
| File has >30 lines                  | `wc -l` check (>15 for last batch) | Mark worker [!], suspect truncation         |

### Gate 2: Content Integrity

| Check                    | Method                                                                                              | Action on Failure                                     |
| ------------------------ | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Last 3 lines end cleanly | `tail -3` — no mid-word breaks                                                                      | Mark [!], split page range in half, retry both        |
| No fabrication signals   | Grep for banned terms: "React", "Docker", "npm", "async/await", "This page describes", "In summary" | CRITICAL: delete file, re-extract from spec           |
| Page header present      | `head -1` matches `# Page N of 434`                                                                 | Mark [!], re-extract with explicit header instruction |
| Boilerplate present      | "ASD-STE100 Simplified Technical English" appears in file                                           | If missing: page range likely wrong, re-extract       |
| No glued headings        | `grep` for `### [^\n]\n[^ \n#]` returns 0                                                           | Mark [!], re-refine the extracted content             |

### Gate 3: Completeness Scan

| Check                                 | Method                                                | Action on Failure                                                        |
| ------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------ |
| All pages in range represented        | Count `# Page N of 434` headers in output             | If fewer than expected: truncated, split and retry                       |
| Table row counts consistent           | No single `                                           | ` orphan lines                                                           | If found: PDF interleaving artifact, re-extract      |
| Expected section type matches content | Cross-reference `.agents/references/section-types.md` | If wrong section type: wrong page range, re-extract with corrected range |
|                                       | Spot-check 3 random lines against source              | Compare output lines to `spec/issue-09-2025/page-dir/page-<spec-id>.md`  | If mismatch: fabrication risk, delete and re-extract |

### Full Verification Procedure (per batch)

```
1. for each of the 3 output files:
   a. Run Gate 1: existence, size, line count
   b. Run Gate 2: truncation, fabrication, format checks
   c. Run Gate 3: completeness, cross-reference
2. If all 3 files pass all 3 gates → mark batch [x] in PROGRESS.md → git commit
3. If any file fails any gate → do NOT commit → enter error recovery
4. If a file fails the same gate after 3 retries → mark as [SKIP] with reason → escalate
```

---

## Error Recovery & Failure Modes

### Failure Mode Matrix

| #   | Failure Mode                                                      | Detection                                             | Probability                         | Recovery                                                                   | Max Retries                                                   |
| --- | ----------------------------------------------------------------- | ----------------------------------------------------- | ----------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------- |
| F1  | Worker timeout (no response after 120s)                           | Background process exits with code 124 or hangs >120s | Low (~2%)                           | Kill process, relaunch same worker                                         | 3                                                             |
| F2  | Truncated output (mid-word or mid-sentence end)                   | Gate 2: `tail -3` shows incomplete content            | Medium (~4%)                        | Split page range in half (4→2+2), launch 2 sub-workers                     | 2 per sub-worker                                              |
| F3  | Fabricated content (commentary, modern terms, summaries)          | Gate 2: grep for fabrication signals                  | Low (~1%)                           | Delete file entirely, re-extract with stronger anti-fabrication prompt     | 2                                                             |
| F4  | Empty or near-empty output (<500 bytes)                           | Gate 1: file size check                               | Very low (<0.5%)                    | Check spec file exists, relaunch worker                                    | 3                                                             |
| F5  | Wrong page range extracted (hallucinated content for wrong pages) | Gate 3: spot-check against spec                       | Rare (~0.5%)                        | Delete file, relaunch with explicit page range in prompt                   | 2                                                             |
| F6  | Partial batch failure (1 of 3 workers fails)                      | Per-worker gate checks                                | Medium (~8%)                        | Retry only the failed worker, keep successful output files                 | 3 per worker                                                  |
| F7  | Full batch failure (3 of 3 workers fail)                          | All 3 fail Gate 1                                     | Very low (<1%)                      | Check API availability, network, spec directory. Pause pipeline. Escalate. | N/A — escalate                                                |
| F8  | Batch straggler (1 worker takes >3× median time)                  | Wall-clock >90s for batch                             | Medium (~5%)                        | Wait up to 120s, then kill and retry. Do not hold up the pipeline.         | 1                                                             |
| F9  | PDF interleaving artifact (merged table columns, garbled rows)    | Gate 3: orphan `                                      | ` lines, inconsistent column counts | Low (~3%)                                                                  | Re-extract. If persists, flag for manual review in `_manual/` | 2   |
| F10 | Rate limit hit (API returns 429)                                  | Process exit with HTTP 429 in stderr                  | Low (~2%)                           | Wait 60s, retry same worker                                                | 3                                                             |

### Recovery Protocol (Step by Step)

When a worker fails any verification gate:

1. **Identify the failure mode** from the matrix above.
2. **Write the failure to `.agents/feedback/exchange.md`** with:
    - Worker ID, batch number, page range
    - Failure mode code (F1-F10)
    - Detection method
    - Timestamp
3. **Mark the worker as [!] in `.agents/state/PROGRESS.md`**.
4. **Do NOT commit the failed batch.** Successful workers in the same batch stay
   on disk but are not committed until the failed worker recovers.
5. **Apply the recovery action** from the matrix.
6. **Re-verify** after recovery.
7. **If recovery succeeds**: mark [!] → [x], commit the full batch, continue.
8. **If recovery fails after max retries**: mark [!] → [SKIP] with reason,
   record in exchange.md, commit the partial batch (successful workers only),
   continue pipeline.
9. **After pipeline completion**: review all [SKIP] entries and re-extract
   manually or with adjusted parameters.

### Split Retry (for truncation F2)

When a 4-page worker produces truncated output:

```
Original: W042 pages 165-168 (truncated)
  ↓ Split into
Sub-worker A: W042a pages 165-166
Sub-worker B: W042b pages 167-168
  ↓ Output files
ste-code/extracted/w042a-p165-166.md
ste-code/extracted/w042b-p167-168.md
  ↓ Merge after both succeed
cat w042a-p165-166.md w042b-p167-168.md > w042-p165-168.md
```

NOTE: Split sub-workers use the same prompt template with adjusted page ranges.
The worker rails (W1-W10) still apply. After grouping, verify the combined file
passes all 3 gates before committing.

### Escalation Criteria

Escalate to manual intervention when:

- A worker fails the same gate 3 times with 3 different recovery strategies.
- A full batch (3/3 workers) fails Gate 1 (suggests systemic issue — API down,
  network outage, spec directory missing).
- Fabrication signals appear in >5% of workers (suggests model drift or prompt
  injection).
- Cumulative [SKIP] count exceeds 10 workers (91% coverage threshold for
  pipeline continuation).

---

## State Machine (Batch Lifecycle)

```
                    ┌─────────────┐
                    │  PENDING    │  ← Batch not yet launched
                    └──────┬──────┘
                           │ launch 3 workers
                    ┌──────▼──────┐
                    │  RUNNING    │  ← Workers executing (30-60s)
                    └──────┬──────┘
                           │ all 3 workers exit
                    ┌──────▼──────┐
                    │ VERIFYING   │  ← Running Gates 1-3
                    └──┬───┬───┬──┘
                       │   │   │
              ┌────────┘   │   └────────┐
              ▼            ▼            ▼
       ┌──────────┐ ┌──────────┐ ┌──────────┐
       │  PASSED  │ │ RETRYING │ │  SKIPPED │
       └────┬─────┘ └────┬─────┘ └────┬─────┘
            │             │            │
            ▼             ▼            ▼
     git commit     re-launch     record in
     continue       failed        exchange.md
     next batch     workers       continue
                    (max 3×)      next batch
```

## Implementation

See `launch-workers.sh` for the automated launcher.

---

## Appendix: Quick Reference Card

### Before Launch

```
□ Pre-flight checks pass (spec dir, disk space, API, git clean)
□ PROGRESS.md initialized with 109 workers [ ]
□ Worker rails block ready for prompt injection
```

### During Execution (per batch)

```
□ Launch 3 workers with background=true
□ Wait for all 3 to exit (max 120s)
□ Gate 1: existence + size (>3KB, >30 lines)
□ Gate 2: no truncation, no fabrication, no glued headings
□ Gate 3: page headers match, no orphans, spot-check passes
□ Update PROGRESS.md [x] for passed workers
□ git gcommit-hermes "Batch NN: workers WXXX-WXXX (pages XXX-XXX)"
```

### On Failure

```
□ Identify failure mode (F1-F10 matrix)
□ Write to .agents/feedback/exchange.md
□ Mark worker [!] in PROGRESS.md
□ Apply recovery action
□ Re-verify
□ If still failing after 3 retries → [SKIP] + escalate
```

### On Pipeline Completion

```
□ All 109 workers [x] or [SKIP] in PROGRESS.md
□ Coverage audit: 434 pages accounted for
□ <10 [SKIP] entries (91% threshold)
□ All [SKIP] entries documented in exchange.md with reason
□ Pipeline handoff to Stage 2 — Refinement
```
