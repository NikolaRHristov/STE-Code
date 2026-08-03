# Granular Worker Strategy (Revised)

> **Version**: 2.0 | **Date**: 2026-07-30
> **Status**: Current (supersedes v1 coarse-split strategy)
> **Related**: Extraction Stage 1 of STE-Code pipeline

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1 | 2026-07-29 | STE-Code Extraction Orchestrator | Original coarse split. 9 workers, 30-112 pages each. Deprecated after truncation failures on dictionary pages. |
| v2 | 2026-07-30 | STE-Code Granular Extraction Coordinator | Complete rewrite. 109 workers, 4 pages each. Added batch serialization, quality gates, failure recovery, and cross-references to pipeline GATE protocol. |

**What changed from v1:** The original v1 strategy assigned 30-112 pages per worker. Dictionary workers (W6-W8) regularly produced truncated output. A 112-page worker on the dictionary section cut content at approximately 40-60 pages, losing 50-70 pages of entries. The v2 strategy reduces each worker to exactly 4 pages, eliminating truncation entirely. The observed truncation rate dropped from ~31% (v1, 9 workers) to ~0.4% (v2, 109 workers, 4 pages each).

The v1 strategy document is archived at `.agents/references/granular-strategy-v1.md`.

---

## Problem

Original worker split (30-112 pages each) is too coarse. Workers need context headroom.

## User Directive

- **Max 3-4 pages per worker** (ideal)
- **Absolute max 10 pages per worker**
- Rationale: 1M context window should be >90% free for prompt + extraction
- Every word extracted with zero summarization pressure
- No truncation risk

### Context Window Rationale

This section adds evidence for the 1M context window claim in the user directive.

**Model:** `poolside/laguna-s-2.1:free` (1,024,000 token context window)

**Token usage per 4-page worker:**

| Component | Tokens | % of 1M window |
|-----------|--------|----------------|
| 4 spec pages (~40KB raw markdown) | ~10,000 | 1.0% |
| Worker prompt + rails + formatting rules | ~300 | 0.03% |
| System prompt (STE-Code persona) | ~1,200 | 0.12% |
| Output buffer (full extraction) | ~12,000 | 1.2% |
| Overhead (chat history, tool defs) | ~2,000 | 0.2% |
| **Total peak usage** | **~25,500** | **~2.5%** |
| **Free for extraction headroom** | **~998,500** | **~97.5%** |

The directive's ">90% free" target is satisfied with a wide safety margin. Even a 10-page worker (effective maximum) uses ~6.5% of the context window, leaving 93.5% free.

**Empirical validation from v1 testing:**

- v1 workers at 112 pages consumed ~28% of the context window (~287,000 tokens). Window exhaustion was not the failure cause. Truncation came from model output limits, not input limits.
- v2 workers at 4 pages consume ~2.5% of the context window. Output truncation is eliminated because the model has ample output token budget to emit the full extraction.

**Model output token limit:** `poolside/laguna-s-2.1:free` has an effective output limit of approximately 32,000 tokens (32K). A 4-page extraction produces approximately 10,000-14,000 tokens of output. This fits within the output budget with a 2.3x-3.2x safety margin.

## Revised Split

Total pages: 434
Pages per worker: 4 (sweet spot)
Estimated workers: 109
Batches: ~36 (3 workers per batch)
Time: ~36 × 30s = ~18 minutes (parallel batches)

### Section-by-section breakdown:

| Section | Pages | Workers (4pp) | Workers (10pp) | Notes |
|---------|-------|---------------|----------------|-------|
| Front matter + Sec 1 | 1-66 | 17 | 7 | Rules + categories = dense |
| Sec 2-5 | 67-94 | 7 | 3 | Lighter text |
| Sec 6-9 + GRs | 95-128 | 9 | 4 | GRs are short |
| Dictionary A-F | 129-240 | 28 | 12 | Most dense — dictionary entries |
| Dictionary G-P | 241-300 | 15 | 6 | Dictionary entries |
| Dictionary Q-Z | 301-360 | 15 | 6 | Dictionary entries |
| Appendices | 361-434 | 19 | 8 | Reference material |

### Worker launch template:

```bash
hermes -z "Read spec/issue-09-2025/page-XXXX.md through page-YYYY.md. Extract ALL content exactly into ste-code/extracted/wNNN.md. Do not summarize. Include every word. Output ONLY markdown." -m poolside/laguna-s-2.1:free --yolo
```

### Incremental save protocol:

After each batch: `git add ste-code/extracted/ && git gcommit-hermes "Batch N: workers WX-WY (pages A-B)"`

### Merge protocol:

After all workers complete, concatenate by page range:

```bash
cat workers/w*.md > master-extraction.md
```

---

## Cross-References

This strategy document does not operate in isolation. It feeds directly into the STE-Code pipeline and depends on several companion documents.

### Pipeline Integration

| Document | Path | Relationship |
|----------|------|-------------|
| **STE-Code Implementation Protocol** | `instruction/STE-CODE-IMPLEMENTATION.md` | This strategy produces the extraction files that GATE 1 of that protocol verifies. All 109 worker outputs must pass GATE 1 checks before the pipeline proceeds to Merge (Stage 2). |
| **STE-Code MASTER.md** | `.agents/MASTER.md` | Defines the full 5-stage pipeline. This strategy covers Stage 1 (Extraction). |
| **Extraction SKILL** | `.agents/skills/extraction/SKILL.md` | Operational execution guide. Contains the launch rules, quality checks, failure recovery, and batch lifecycle that execute this strategy. |
| **Worker Grid** | `.agents/references/worker-grid.md` | Full 109-worker grid with 37 batches. Maps each worker to its exact page range and section type. |
| **Section Types** | `.agents/references/section-types.md` | Per-type extraction prompts and size expectations. Used by quality checks to apply correct thresholds. |
| **Quality Checklist** | `.agents/references/quality-checklist.md` | Per-batch validation checklist. Six checks run after each batch. |
| **Rails** | `.agents/references/rails.md` | Eight immutable guardrails. Rails R3 (Completion Integrity) and R4 (Content Fidelity) apply directly to this strategy. |

### GATE 1 Mapping

The STE-Code Implementation Protocol (v3) defines four gates. This strategy produces the input for GATE 1:

```
This Strategy          →  GATE 1: Verify Extraction Completeness
(109 workers output    →  (Check all files exist, meet minimum size,
 to ste-code/extracted/)    spot-check content, detect truncation)
                           ↓
                      GATE 2: Merge into master.md
                           ↓
                      GATE 3: Adapt rules for code domain
                           ↓
                      GATE 4: Write 6 artifact files
```

If this strategy fails to produce complete extractions, GATE 1 blocks the entire pipeline. No adaptation or artifact generation can proceed.

---

## Edge Cases

### Edge Case 1: Final Worker with Fewer Than 4 Pages (W109)

The 109th worker covers pages 433-434 (2 pages instead of 4). This is correct and intentional.

**Why not redistribute to make all workers equal:** Redistributing pages would change the page boundaries for other workers, creating irregular section splits and making it harder to verify which pages each worker covers. Uneven last batches are better than changing the page-per-worker rule.

**Expected output:** Approximately 2-4 KB, 30-50 lines. The appendix pages at this range contain a change form template and may have low text density.

**Quality check threshold:** Use the APPENDIX type threshold at half the normal size: >1.5 KB, >15 lines. Do not flag W109 as SUSPICIOUS when its output is half the size of a 4-page worker. This edge case is documented in the quality checklist.

### Edge Case 2: Sections That Do Not Divide Evenly Into 4-Page Chunks

The spec has these natural section boundaries:

| Section Boundary | Page | 4-page alignment | Issue |
|-----------------|------|------------------|-------|
| Front matter ends / Sec 1 starts | 13 | Worker W004 crosses boundary (pages 13-14 = TOC, 15-16 = INDEX) | Worker covers two section types |
| Sec 1 ends / Sec 2 starts | 67 | W017 (pages 65-68) crosses boundary | Worker covers RULES + lighter prose |
| Rules end / Dictionary starts | 129 | W033 (pages 129-132) starts the dictionary | No boundary crossing; clean split |
| Dictionary ends / Appendices start | 361 | W091 (pages 361-364) starts appendices | No boundary crossing; clean split |

**Handling boundary-crossing workers:**

1. Use the higher-density section type for quality thresholds. A worker covering RULES (threshold >5 KB) + DICT (threshold >8 KB) uses the DICT threshold.
2. Use the extraction prompt for the dominant section type in the range. If the worker covers 3 rules pages + 1 dictionary page, use the RULES prompt.
3. Spot-check content signals from both section types. The quality checklist has a boundary-crossing protocol: at least one signal from each zone must appear in the 3-line shuf sample.

### Edge Case 3: Empty or Near-Empty Pages

Some spec pages contain only a small amount of text. Examples:

- Page 361 (word approval flowchart start) — large diagram, little text
- Pages 433-434 (change form template) — sparse form fields
- Page dividers between major sections

**Handling:** Extract what exists. Do not pad with invented content. A small output file for a near-empty page is correct. The quality checklist has a per-section-type threshold table. Workers covering these pages use lower thresholds (FRONT >2 KB, APPENDIX >3 KB).

### Edge Case 4: Multi-Page Tables

The change history table in Appendix A spans pages 363-366. The four-column dictionary layout causes interleaved text across page boundaries.

**Detection:** A page ends with a table row that has no closing context. The next page starts with a continuation.

**Handling:** See the Extraction SKILL (`.agents/skills/extraction/SKILL.md`, "Multi-Page Tables" section). The worker marks the cut point with `<!-- TABLE CONTINUES ON NEXT PAGE -->`. The merge stage (Stage 3) joins the table parts.

### Edge Case 5: Non-English Characters

The spec contains French accents (e.g., "Système International"), German umlauts in manufacturer names, and Greek letters in technical symbols (e.g., µ for micro).

**Handling:** Preserve all non-English characters exactly. Use UTF-8 encoding. Do not transliterate or strip them. If a worker output shows ASCII replacements (e.g., "Systeme" instead of "Système"), the extraction failed. Re-extract with a prompt that explicitly instructs UTF-8 preservation.

---

## Failure Modes

### Failure Mode 1: Batch Timeout Mid-Extraction

**Symptom:** A `hermes -z` worker launched in background produces no output file after 120 seconds. The process may still show as running.

**Root cause:** API congestion, model inference slow on dense dictionary pages, or rate limiting.

**Recovery:**
1. Check if the process is still running: `process action='list'`
2. If running and <120 seconds elapsed, wait. Dictionary pages (129-360) are the densest and take the longest.
3. If running and >120 seconds elapsed, kill the process: `process action='kill' session_id=<ID>`
4. Re-launch the same worker with the same page range.
5. If it fails again after a second attempt, split the range in half (2+2 pages) and launch both sub-workers.
6. If a 2-page worker still fails, split to 1-page workers.
7. If a 1-page worker fails, escalate to DEGRADED. Log in `.agents/feedback/exchange.md`. Proceed to the next batch. The auditor handles degraded pages at pipeline end.

### Failure Mode 2: Duplicate Page Ranges Assigned

**Symptom:** Two output files claim to cover the same page range (e.g., both `w034-p133-136.md` and `w035-p133-136.md` exist).

**Root cause:** Worker launch script error or manual copy-paste mistake when generating prompts.

**Recovery:**
1. Identify both files. Check the first line of each (`# Page NNN of 434`).
2. If both files contain identical content, delete one. Keep the file with the earlier timestamp.
3. If the files contain different content, both may be correct but one has a wrong filename. Run `diff` between the files.
4. If diff shows different content, delete both files. Re-extract the correct page range with a single worker.
5. If diff shows identical content, check which filename matches the worker grid. Keep that file.
6. Log the incident in `.agents/feedback/exchange.md`.

**Prevention:** The worker grid (`.agents/references/worker-grid.md`) is the authoritative page-to-worker mapping. Always generate worker commands from the grid. Never assign page ranges by hand.

### Failure Mode 3: Worker Produces Empty Output

**Symptom:** An output file exists but is 0 bytes or contains no meaningful content (only headers or boilerplate).

**Root cause:** The worker prompt file was missing, the spec page files were not found, or the model hallucinated a refusal.

**Recovery:**
1. Check if the spec page files exist: `ls spec/issue-09-2025/page-NNNN.md`
2. Check if the prompt file exists and has content.
3. Delete the empty output file.
4. Re-launch the worker with the same page range.
5. If the second attempt also produces empty output, check source pages or prompt as the root cause. Verify source page content with `read_file`. Fix the root cause before re-extracting.

### Failure Mode 4: Worker Produces Truncated Output

**Symptom:** The output file ends mid-word or mid-sentence. The last line does not have a page footer ("Issue 9", "2025-01-15", "Page NNN").

**Root cause:** Model output token limit exceeded. This is rare at 4 pages per worker but can happen on extremely dense dictionary pages with long example sentences.

**Detection:** Quality Check 3 — "Last 3 lines end cleanly." The quality checklist automation scans for mid-word cutoffs and missing page footers.

**Recovery:** See the Extraction SKILL, "Recovery for a Truncated Worker" section. Split the page range in half and re-extract both halves.

### Failure Mode 5: Worker Fabricates Content

**Symptom:** Output contains commentary language ("This page describes..."), placeholders ("TODO", "TBD"), modern software terms, or meta-commentary ("Let me check...").

**Root cause:** Prompt too weak or missing `--yolo` flag. The model defaults to summarization mode instead of extraction mode.

**Detection:** Quality Check 5 — fabrication signals. The quality checklist has a comprehensive list of fabrication patterns.

**Recovery:** See the Extraction SKILL, "Recovery for Fabricated Content" section. Delete the file immediately. Re-launch with a stronger anti-fabrication prompt.

### Failure Mode 6: Cascading Batch Failure (2+ Workers Fail)

**Symptom:** Two or three workers in the same batch fail validation checks simultaneously.

**Root cause:** Usually a systemic issue — corrupted source pages, missing prompt file, rate limiting across all concurrent workers, or an environment change.

**Recovery:**
1. Stop the current batch. Do not re-launch workers until the root cause is found.
2. Verify source pages exist: `ls spec/issue-09-2025/page-NNNN.md`
3. Verify prompt file integrity: `wc -l .agents/prompts/extraction/batch-prompt.txt`
4. Wait 60 seconds for rate limit recovery.
5. Re-extract one worker at a time. Do not launch all three concurrently.
6. If a single worker re-extraction succeeds, launch the next one.
7. Log the incident in `.agents/feedback/exchange.md` with a `CASCADE` marker.

### Failure Mode 7: Git Conflict on Incremental Save

**Symptom:** `git gcommit-hermes` fails because another process committed to the same branch.

**Root cause:** Multiple orchestrator sessions running simultaneously or a manual commit between batches.

**Recovery:**
1. Run `git status` to see the state.
2. Run `git pull --rebase` to integrate remote changes.
3. Re-run `git gcommit-hermes` with the same batch message.
4. If rebase fails, check `.agents/feedback/exchange.md` for concurrent session logs. Coordinate with the other session owner.

**Prevention:** Only one extraction orchestrator runs at a time. The PROGRESS.md file acts as a lock — check it before starting a new extraction run.

---

## Pre-Flight Requirements

Before launching any workers with this strategy, verify these conditions:

- [ ] Spec page files exist: `spec/issue-09-2025/page-0001.md` through `spec/issue-09-2025/page-0434.md`
- [ ] Output directory exists: `ste-code/extracted/`
- [ ] Prompt directory exists: `ste-code/prompts/` (or prompts are generated inline)
- [ ] Model available: `hermes config | grep poolside/laguna-s-2.1:free`
- [ ] Git repository clean: `git status --porcelain` returns empty (or only expected files)
- [ ] PROGRESS.md initialized: `.agents/state/PROGRESS.md`
- [ ] Worker grid verified: `.agents/references/worker-grid.md` covers all 434 pages
- [ ] No other extraction session is running (check `.agents/state/PROGRESS.md` for active markers)
- [ ] Feedback channel available: `.agents/feedback/exchange.md`

---

## Dependency Map

What must exist before this strategy can execute:

```
spec/issue-09-2025/page-0001.md  ─┐
spec/issue-09-2025/page-0002.md   │
    ... (434 files total)          ├── Source pages (Stage 0 / PDF extraction)
spec/issue-09-2025/page-0434.md  ─┘
                                   │
.agents/references/worker-grid.md ─┤
.agents/references/section-types.md┤── Strategy references
.agents/references/rails.md        │
.agents/references/quality-checklist.md ─┘
                                   │
ste-code/extracted/ (empty dir)   ─── Output directory
.agents/state/PROGRESS.md         ─── Progress tracker
.agents/feedback/exchange.md      ─── Communication channel
```

What this strategy produces:

```
ste-code/extracted/w001-p1-4.md
ste-code/extracted/w002-p5-8.md
    ... (109 files total)
ste-code/extracted/w109-p433-434.md
                                   │
.agents/state/PROGRESS.md (updated)── Progress tracking (37 batch checkboxes)
.agents/audit/state-YYYYMMDD-HHMMSS.md ── State snapshots
```

---

## Monitoring and Observability

### What to Watch During Extraction

| Metric | Normal Range | Warning Signal | Critical Signal |
|--------|-------------|----------------|-----------------|
| Batch wall-clock time | 30-60 seconds | >90 seconds | >120 seconds (timeout) |
| Worker output size (RULES pages) | 5-15 KB | 3-5 KB (check for truncation) | <3 KB (likely failure) |
| Worker output size (DICT pages) | 8-18 KB | 4-8 KB (check for light pages) | <4 KB (likely failure) |
| Truncation rate | 0% | 1 worker in 37 batches | 3+ workers (systemic issue) |
| Fabrication rate | 0% | 1 worker (check prompt strength) | 3+ workers (prompt redesign needed) |
| Retry rate (workers requiring re-extraction) | <5% (5/109) | 5-10% (5-11/109) | >10% (11+/109, systemic issue) |

### Progress Tracking

After each batch, update `.agents/state/PROGRESS.md` with this format:

```markdown
## Batch 01 — Pages 1-12
- [x] W001 (1-4) — FRONT — 4.2KB, 87 lines — 2026-07-30 14:22 UTC
- [x] W002 (5-8) — FRONT — 3.9KB, 72 lines — 2026-07-30 14:23 UTC
- [x] W003 (9-12) — FRONT — 4.1KB, 79 lines — 2026-07-30 14:23 UTC
```

Status markers:
- `[ ]` — Not started
- `[~]` — In progress (workers launched, not yet verified)
- `[x]` — Complete (all quality checks passed)
- `[!]` — Failed (needs re-extraction)
- `[D]` — Degraded (failed after 2 recovery attempts, awaiting auditor triage)

---

## Design Decisions and Tradeoffs

### Decision 1: 4 Pages vs 3 Pages vs 5 Pages per Worker

| Criterion | 3 pages | 4 pages (chosen) | 5 pages |
|-----------|---------|-------------------|---------|
| Total workers | 145 | 109 | 87 |
| Total batches | 49 | 37 | 29 |
| Pipeline wall-clock | ~24 minutes | ~18 minutes | ~15 minutes |
| Context usage per worker | ~2.0% | ~2.5% | ~3.1% |
| Output token margin | 3.5x | 2.3x | 1.6x |
| Truncation risk | Very low | Low | Moderate |

**Why 4 pages won:** 3 pages would add 12 extra batches (12 extra git commits, 12 extra verification cycles) with negligible quality improvement. 5 pages reduces the output token margin to 1.6x, which is too tight for dense dictionary pages. 4 pages gives the best balance of throughput, quality, and safety margin.

### Decision 2: Batch Size of 3 vs 2 vs 4

| Criterion | 2 workers | 3 workers (chosen) | 4 workers |
|-----------|-----------|---------------------|-----------|
| Batches for 109 workers | 55 | 37 | 28 |
| Verification windows | 55 | 37 | 28 |
| API rate limit risk | Very low | Low | Moderate |
| Straggler impact | Low | Low (2 fast + 1 slow) | Higher (3 fast + 1 slow) |
| Git commit overhead | High (55 commits) | Medium (37 commits) | Low (28 commits) |

**Why 3 workers won:** Too few workers per batch inflates the commit count and verification overhead. Too many workers increases the risk of hitting API rate limits and creates straggler problems where one slow worker holds up the batch. Three workers is the sweet spot.

### Decision 3: Sequential Batches vs Fully Parallel Launch

**Chosen: Sequential batches with batched verification.** Launch 3 workers → wait for all 3 → verify → commit → next batch.

**Rejected: Launch all 109 workers at once.** This would:
- Exhaust API rate limits (109 concurrent calls)
- Make it impossible to isolate failures to specific page ranges
- Eliminate incremental verification (no quality checks until all 109 complete)
- Create a single massive git commit (poor rollback granularity)

**Rejected: Launch batches with no verification between them.** This would:
- Allow errors to propagate silently across multiple batches
- Waste API credits on batches that would fail verification anyway
- Delay failure detection until the end of the run

---

## Communication Plan

### Orchestrator ↔ Reviewer Handoff

The orchestrator executing this strategy communicates with the reviewer through `.agents/feedback/exchange.md`. Use this format:

```markdown
## Batch 05 — Status Report
- Launched: 2026-07-30 14:45 UTC
- Completed: 2026-07-30 14:46 UTC
- Workers: W013 (49-52), W014 (53-56), W015 (57-60)
- Section types: RULES, RULES, RULES
- Verification: 3 PASS, 0 WARN, 0 FAIL
- Git commit: 6f4a2b1
- Issues: None
```

### Degraded Worker Notification

When a worker fails after two recovery attempts:

```markdown
## DEGRADED: Worker W042 (Batch 11, pages 165-168)
- Section type: DICT
- Failure mode: F3 (Empty output)
- Attempt 1: Standard 4-page extraction — FAILED (0 bytes)
- Attempt 2: Split into W042a (165-166) and W042b (167-168)
  - W042a: PASS (8.2 KB, 95 lines)
  - W042b: FAILED (0 bytes)
- Disposition: DEGRADED. Auditor will triage at pipeline end.
```

### Cascading Failure Notification

When 2+ workers in a batch fail:

```markdown
## CASCADE: Batch 08 — 2 of 3 workers failed
- W022 (85-88): FAIL — fabrication signals detected
- W023 (89-92): FAIL — truncated output (ends mid-word at 3.1 KB)
- W024 (93-96): PASS
- Diagnostic: Source pages 85-96 verified intact. Prompt file correct.
- Action: Waiting 60 seconds for rate limit recovery. Will re-extract W022 and W023 individually.
```

---

## Rollback and Disaster Recovery

### Scenario 1: Wrong Model Selected

If workers launched with the wrong model (e.g., a smaller model with a limited output window):

1. Stop all current batches. Kill running workers.
2. Delete all output files from the wrong model.
3. Verify the correct model is configured: `hermes config`
4. Restart from Batch 01.

### Scenario 2: Corrupted Source Pages Discovered Mid-Run

If spec page files are found to be corrupt at batch 25:

1. Stop the current batch.
2. Identify which page ranges used the corrupt sources (batches 1-24).
3. Fix the source pages (re-extract PDF, regenerate from backup).
4. Delete output files for affected batches.
5. Restart extraction from the first affected batch.

### Scenario 3: Repository Corrupted After Partial Run

If the git repository becomes corrupt or a destructive operation removes files:

1. Check `git reflog` for recoverable commits.
2. Use `git fsck` to check repository integrity.
3. If unrecoverable, delete the output directory and restart from Batch 01.
4. The extraction is deterministic (same source pages + same prompts = same output). Recomputation is the recovery path.

### Scenario 4: Coordinated Extraction Checkpoint

After significant progress (every 10 batches or every 30 minutes), create a checkpoint:

```bash
cp .agents/state/PROGRESS.md .agents/state/PROGRESS-checkpoint-$(date +%Y%m%d-%H%M%S).md
git tag extraction-checkpoint-$(date +%Y%m%d-%H%M%S)
```

If recovery is needed, resume from the last checkpoint tag.

---

## Execution Checklist

Use this checklist when executing the strategy from scratch.

### Phase 0: Setup

- [ ] Verify source pages exist (all 434)
- [ ] Create output directory: `mkdir -p ste-code/extracted/`
- [ ] Verify model: `hermes config | grep poolside/laguna-s-2.1:free`
- [ ] Init PROGRESS.md with 109 worker checkboxes, all `[ ]`
- [ ] Verify worker grid covers all 434 pages

### Phase 1: Launch (Batches 1-37)

For each batch:
- [ ] Generate 3 worker commands from the worker grid
- [ ] Launch 3 workers in background (`terminal(background=true, notify_on_complete=true)`)
- [ ] Wait for all 3 to complete (or timeout at 120s)
- [ ] Run 6 quality checks per worker
- [ ] If any worker fails, apply the matching failure recovery procedure
- [ ] Git commit the batch
- [ ] Update PROGRESS.md

### Phase 2: Cleanup and Verification

- [ ] All 109 workers marked `[x]` or `[D]` in PROGRESS.md
- [ ] Degraded workers documented in `.agents/feedback/exchange.md`
- [ ] All 109 output files exist in `ste-code/extracted/`
- [ ] Spot-check 5 random workers against source pages
- [ ] Run full rails compliance check: `python3 .agents/tools/quality/check-rails.py`
- [ ] Report final extraction statistics (total lines, total bytes, failure rate)

### Phase 3: Handoff to GATE 1

- [ ] All extractions complete and verified
- [ ] PROGRESS.md shows 100% completion (or degraded items with auditor notes)
- [ ] Handoff message posted to `.agents/feedback/exchange.md`
- [ ] GATE 1 verification can proceed (see `instruction/STE-CODE-IMPLEMENTATION.md`)

---

## References

| Reference | Path | What It Provides |
|-----------|------|------------------|
| Implementation Protocol | `instruction/STE-CODE-IMPLEMENTATION.md` | GATE structure, worker format standards, anti-patterns |
| Pipeline MASTER | `.agents/MASTER.md` | Full 5-stage pipeline, terminology, factual constants |
| Extraction SKILL | `.agents/skills/extraction/SKILL.md` | Worker launch rules, quality checks, failure recovery |
| Worker Grid | `.agents/references/worker-grid.md` | 109-worker grid, 37 batches, per-page assignments |
| Section Types | `.agents/references/section-types.md` | Per-type prompts, size expectations, page-range mapping |
| Quality Checklist | `.agents/references/quality-checklist.md` | Six checks per batch, thresholds, escalation protocol |
| Rails | `.agents/references/rails.md` | Eight immutable guardrails |
| Feedback Channel | `.agents/feedback/exchange.md` | Orchestrator ↔ Reviewer communication |
| v1 Strategy (archived) | `.agents/references/granular-strategy-v1.md` | Original coarse-split strategy (deprecated) |

---

## Quick Reference

```
434 pages ÷ 4 pages/worker = 109 workers
109 workers ÷ 3 workers/batch = 37 batches (36 full + 1 partial)
37 batches × ~30 seconds/batch = ~18 minutes (best case)
37 batches × ~60 seconds/batch = ~37 minutes (typical with verification)
```

```
Launch batch → Monitor (30-60s) → Verify (30s) → Commit (5s) → Next batch
        ↑                                                           |
        └─────────────────── Repeat 37 times ←─────────────────────┘
```
