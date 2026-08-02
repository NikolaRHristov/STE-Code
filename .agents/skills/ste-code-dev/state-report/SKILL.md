---
name: state-report
description: > **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
category: dev
capability: developing-and-changing-the-standard
source: /Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code/.agents/skills/state-report
layout: ste-code-canonical-v1
---

# Agent State Report Format

> **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
> Session isolation + STRICT_RULES (R1-R6) from `lib/pipeline_core.py` apply to THIS skill.
> One session = one operation = one read + one write. No re-editing own output.

Standardized format for pipeline state reports. Fill all sections. Agent-agnostic.

## Status Emoji Legend

Use these emoji to show the status of each pipeline stage:

| Emoji | Meaning | Criteria |
|-------|---------|----------|
| ✅ | Complete | All expected files exist on disk. Counts match PROGRESS.md. No errors. |
| 🟢 | In Progress | Some files exist. Counts below expected. Work is active. |
| ⬜ | Not Started | Zero files exist in the stage directory. No workers launched. |
| 🔴 | Blocked | Work stopped by a critical error. No progress possible until fixed. |
| 🟠 | Partial with Errors | Files exist but some are corrupt, truncated, or fabricated. |
| ⚠️ | Unknown | Cannot determine status. Directory missing or audit report unavailable. |

NOTE: Use 🔴 only when the stage is blocked by a confirmed critical error. Use 🟠 when the stage has errors but work can continue on other files.

## When to Produce a State Report

Produce a state report at these trigger points. Do not skip a trigger.

### Mandatory Triggers (handoff points)

| Trigger | Reason | Consumer |
|---------|--------|----------|
| Extraction completes (109/109 files) | Stage 1 → Stage 2 gate | Agent #2 (Refiner), Agent #3 (Auditor) |
| Refinement completes (109/109 files) | Stage 2 → Stage 3 gate | Agent #4 (Continuator), Agent #3 (Auditor) |
| Merge completes (master.md produced) | Stage 3 → Stage 4 gate | Agent #4 (Continuator), Agent #3 (Auditor) |
| Adaptation completes (57 files) | Stage 4 → Stage 5 gate | Agent #4 (Continuator), Agent #3 (Auditor) |
| Artifacts complete (6 files) | Final quality gate | Agent #3 (Auditor), all downstream consumers |

### Recommended Triggers (mid-stage)

| Trigger | Reason |
|---------|--------|
| After every 10th batch (batches 10, 20, 30) | Mid-stage health check |
| Before any long pause (session end, context switch) | Handoff to next session or agent |
| After error recovery (re-extraction, re-refinement) | Confirm the fix restored expected state |
| On demand ("state", "status", "report", "where are we") | Operator request |

### Trigger Decision Flow

Use this decision tree before producing a state report. If any answer is YES, produce the report.

```
1. Is this a mandatory trigger (stage gate)?
   YES → PRODUCE REPORT immediately
   NO  → Continue to step 2.

2. Has a batch completed since the last state report?
   NO  → Do not produce a report. Duplicate reports waste time.
   YES → Continue to step 3.

3. Has more than 5 batches completed since the last state report?
   YES → PRODUCE REPORT (health check)
   NO  → Continue to step 4.

4. Did an error or blocker occur that changed pipeline status?
   YES → PRODUCE REPORT (error context)
   NO  → Do not produce a report. Continue working.
```

NOTE: Multiple state reports from the same timestamp are not useful. Before producing a report, check if a report with the same timestamp already exists in `.agents/audit/`. If it does, append a sequence number: `state-YYYYMMDD-HHMMSS-2.md`.

## REPORT FORMAT

```markdown
# Agent State Report — YYYY-MM-DD HH:MM:SS

## Role
- **Role**: [extractor | refiner | auditor | continuator]
- **Last action**: [what I just did]

## Pipeline Status

| Stage | Directory | Expected | Actual | % | Status |
|-------|-----------|----------|--------|---|--------|
| 1 — Extract | extracted/ | 109 | ?? | ??% | [✅/🟢/⬜] |
| 2 — Refine | refined/ | 109 | ?? | ??% | [✅/🟢/⬜] |
| 3 — Merge | merged/ | 2 files | ?? | — | [✅/⬜] |
| 4 — Adapt | adapted/ | TBD | ?? | — | [✅/⬜] |
| 5 — Artifacts | artifacts/ | 6 | ?? | — | [✅/⬜] |

## Errors & Blockers
| Severity | Description | File/Worker | Action Needed |

## Rails Compliance
| Rail | Status | Issues |

## Files on Disk (verified)
```
[Run: find ste-code/ -name "*.md" -o -name "*.txt" | wc -l] total files
[Run: du -sh ste-code/] total size
```

## Next Actions (prioritized)
1. [Immediate]
2. [Next batch]
3. [Verification pending]
```

## Execution Rules
1. Run shell commands to populate counts — never estimate
2. Verify file existence with `ls` or `test -f` — never trust PROGRESS.md alone
3. Update PROGRESS.md after producing this report if discrepancies found
4. Write report to `.agents/audit/state-YYYYMMDD-HHMMSS.md`
5. If a section cannot be filled, write "UNKNOWN — needs investigation" — never leave blank
6. If PROGRESS.md is missing, note it as 🔴 Critical in Errors & Blockers and produce the report from disk evidence alone
7. If `.agents/audit/` does not exist, create it before writing the report
8. If the audit directory is corrupted or unwritable, write the report to the project root and note the path in the Errors section
9. If a file count command fails (permission denied, path not found), record the command and its error — never substitute an estimate
10. After writing the report, verify it exists on disk with `test -f` before declaring the report complete

## Complete Example: Mid-Extraction State Report

Below is a fully filled state report for a realistic pipeline state. Use this as a reference. All values come from real shell commands. No field is left blank.

```markdown
# Agent State Report — 2026-07-30 14:35:00

## Role
- **Role**: extractor
- **Last action**: launched batches 20-22 (workers W058-W066, pages 229-264)

## Pipeline Status

| Stage | Directory | Expected | Actual | % | Status |
|-------|-----------|----------|--------|---|--------|
| 1 — Extract | extracted/ | 109 | 66 | 61% | 🟢 |
| 2 — Refine | refined/ | 109 | 0 | 0% | ⬜ |
| 3 — Merge | merged/ | 2 files | 0 | — | ⬜ |
| 4 — Adapt | adapted/ | 57 files | 57 | 100% | ✅ |
| 5 — Artifacts | artifacts/ | 6 | 6 | — | ✅ |

NOTE: Stages 4-5 completed in a prior pipeline run. Stage 1 is the current focus.

## Active Workers

| Worker ID | Pages | Status | Output Size | Issues |
|-----------|-------|--------|-------------|--------|
| W058 | 229-232 | Running | — | None |
| W059 | 233-236 | Running | — | None |
| W060 | 237-240 | Running | — | None |
| W061 | 241-244 | Running | — | None |
| W062 | 245-248 | Running | — | None |
| W063 | 249-252 | Running | — | None |
| W064 | 253-256 | Running | — | None |
| W065 | 257-260 | Running | — | None |
| W066 | 261-264 | Running | — | None |

## Completed Batches

| Batch | Workers | Files | Verified | Notes |
|-------|---------|-------|----------|-------|
| 1 | W001-W003 | 3/3 | ✅ | Pages 1-12, all >3KB |
| 2 | W004-W006 | 3/3 | ✅ | Pages 13-24 |
| 3-18 | W007-W054 | 48/48 | ✅ | Pages 25-216 |
| 19 | W055-W057 | 3/3 | 🟡 | W055 truncated (2.1KB), re-extracted successfully |
| 20 | W058-W060 | — | ⬜ | In progress |
| 21 | W061-W063 | — | ⬜ | In progress |
| 22 | W064-W066 | — | ⬜ | In progress |

## Errors & Blockers

| Severity | Description | File/Worker | Action Needed |
|----------|-------------|-------------|---------------|
| 🟡 | W055 original output truncated at 2.1KB | w055-p217-220.md | Resolved: re-extracted. New file is 4.3KB. |
| 🟡 | Batch 19 delayed 14 minutes due to API rate limit | Batches 20-22 | Monitor batch 20-22 for rate limit repeats |

## Rails Compliance

| Rail | Status | Issues |
|------|--------|--------|
| R1 — Stage Isolation | PASS | All wNNN files only in extracted/ |
| R2 — Naming Convention | PASS | All files match wNNN-pPPPP-PPPP.md pattern |
| R3 — Completion Integrity | PASS | All [x] claims verified on disk |
| R4 — Content Fidelity | PASS | Zero fabrication signals in spot-checked files (batches 1-19) |
| R5 — Formatting Standards | PASS | No glued headings or format violations |
| R6 — Factual Correctness | PASS | "19 categories" and "poolside/laguna-s-2.1:free" confirmed in all docs |
| R7 — Progress Tracking | PASS | PROGRESS.md matches disk counts (66 files on disk, 66 [x] markers) |
| R8 — Error Recovery | PASS | W055 re-extraction documented in exchange.md |

## Files on Disk (verified)
```
[Run: find ste-code/ -name "*.md" -o -name "*.txt" | wc -l] 187 total files
[Run: du -sh ste-code/] 2.1M total size

extracted/: 66 files, 1.2M
refined/: 0 files, 0
merged/: 0 files, 0
adapted/: 57 files, 480K
artifacts/: 6 files, 28K
audit/: 4 files, 32K
```

## PROGRESS.md Sync Status

| Field | PROGRESS.md | Disk | Match |
|-------|-------------|------|-------|
| Extracted files | 66 | 66 | ✅ |
| Refined files | 0 | 0 | ✅ |
| Batch count | 19 batches [x] | 19 batches verified | ✅ |
| Last update | 2026-07-30 14:32 | — | Fresh |

No discrepancies between PROGRESS.md and disk evidence.

## Git State

```
[Run: git status --short]
 M ste-code/PROGRESS.md
?? ste-code/extracted/w058-p229-232.md
?? ste-code/extracted/w059-p233-236.md

[Run: git log --oneline -3]
abc1234 checkpoint: extraction batch 19 complete (W055-W057)
def5678 checkpoint: extraction batch 18 complete (W052-W054)
ghi9012 fix: re-extracted W055 after truncation
```

## Next Actions (prioritized)

1. Wait for batches 20-22 to complete (9 workers running, pages 229-264)
2. Verify batch 20-22 output: file existence, size >3KB, naming convention
3. Launch batches 23-25 (workers W067-W075, pages 265-300)
4. Run fabrication scan on batches 20-22 before marking PROGRESS.md [x]
5. After batch 30 completes: produce mid-stage health check state report

## Notes

- Rate limit hit during batch 19 launch. Wait 30 seconds between batch launches for batch 23+.
- Adapted/ and artifacts/ directories from prior pipeline run are untouched but verified on disk.
- No fabrication signals detected in any spot-check (batches 1, 5, 9, 13, 17, 19).
- PROGRESS.md is 2 minutes behind current state (batches 20-22 not yet recorded). Will update after batch completion.
```

## Discrepancy Resolution

When the state report finds that Expected ≠ Actual, follow these rules.

### Discrepancy Types and Actions

| Discrepancy | Evidence | Severity | Immediate Action |
|-------------|----------|----------|------------------|
| Expected > Actual (missing files) | `find` returns fewer files than expected | 🟠 Error | Mark the stage as 🟢 (in progress). Do not mark as ✅. |
| Expected < Actual (extra files) | `find` returns more files than expected | 🟡 Warning | List the extra files. Check for naming violations or stage leaks. |
| PROGRESS.md claims [x] but file missing | `test -f` returns false for a claimed file | 🔴 Critical | Revert the [x] to [ ] in PROGRESS.md. Trigger re-extraction. |
| PROGRESS.md claims [ ] but file exists | File found on disk with no progress marker | 🟡 Warning | Mark the file as [x] in PROGRESS.md. Verify content quality. |
| File exists but is too small (<30 lines or <3KB) | `wc -l` and `wc -c` below threshold | 🟠 Error | Flag as truncated. Do not count toward completion %. Trigger re-extraction. |
| File exists but has fabrication signals | grep matches fabrication patterns | 🔴 Critical | Delete the file. Trigger re-extraction. Audit sibling files. |
| Directory exists but is empty | `ls` returns 0 entries | 🟡 Warning | If stage not started: expected. If stage claimed started: mark as 🟠. |
| PROGRESS.md is stale (timestamp before newest file) | `stat` comparison | 🟡 Warning | Note freshness gap. Update PROGRESS.md after verifying all files. |

### Resolution Order

When multiple discrepancies exist, resolve them in this order:

1. **Critical first** — Fabricated files and false completion claims. These poison downstream stages.
2. **Missing files** — Gaps in the file sequence. These block continuation.
3. **Truncated files** — Files below size threshold. These need re-extraction.
4. **Stale PROGRESS.md** — Tracking sync issues. Fix after file issues are resolved.
5. **Extra files** — Naming violations or stage leaks. Clean up last.

### Stale PROGRESS.md Resolution

When PROGRESS.md does not match disk evidence:

1. Run `find` on each stage directory to get actual file counts.
2. Compare each batch entry in PROGRESS.md against disk files for that batch.
3. For each batch where PROGRESS.md and disk disagree:
   - If disk has more files: update PROGRESS.md [x] markers to match disk.
   - If PROGRESS.md has more claims: revert [x] to [ ] and add a note.
4. After all batches are synced, update the stage completion percentage.
5. Write the corrected PROGRESS.md. Note the changes in the state report.

### Partial Stage Completion

When a stage shows partial completion (for example, 66 of 109 extraction files):

- Do NOT mark the stage as ✅. Use 🟢 (in progress).
- Do NOT start the next stage. Wait until the current stage reaches 100%.
- If the next stage has already produced output (cross-stage contamination), audit those files immediately. See RAIL 1 — Stage Isolation in `.agents/skills/auditing/SKILL.md`.
- Report the completion percentage as `actual / expected × 100`, rounded to the nearest whole number.

## Edge Cases

### Missing PROGRESS.md

If PROGRESS.md does not exist at the expected path:

1. Record the absence as 🔴 Critical in the Errors & Blockers table.
2. Produce the state report from disk evidence alone. Run `find` on every stage directory.
3. Write the report with the note: "PROGRESS.md missing — all counts from disk evidence only."
4. After the report, request regeneration of PROGRESS.md. Use the disk evidence as the baseline.
5. Cross-reference with `exchange.md` for any batch or stage completion claims.

### Missing exchange.md

If `exchange.md` does not exist:

1. Record the absence as 🟡 Warning. The state report can still be produced from PROGRESS.md and disk evidence.
2. Note in the report: "exchange.md missing — inter-agent communication log unavailable."
3. If both PROGRESS.md and exchange.md are missing, produce a disk-evidence-only report and mark as 🔴 Critical.

### Corrupted Audit Directory

If `.agents/audit/` exists but cannot be written to:

1. Check for disk space: `df -h .agents/audit/`.
2. Check for permissions: `ls -ld .agents/audit/`.
3. If the directory is full, write the report to the project root with the prefix `state-`.
4. Note the alternate path in the state report and in Errors & Blockers.
5. After the report is saved, request cleanup of the audit directory.

### Multiple State Reports from Same Timestamp

If a state report at `.agents/audit/state-YYYYMMDD-HHMMSS.md` already exists:

1. Append a sequence number: `state-YYYYMMDD-HHMMSS-2.md`.
2. If `-2` also exists, increment to `-3`, and so on.
3. In the report Notes field, reference the original: "Sequence 2 of timestamp YYYYMMDD-HHMMSS. Original at state-YYYYMMDD-HHMMSS.md."
4. Do NOT overwrite an existing state report. Every report is an immutable record.

### Stage Directory Missing

If a stage directory (for example, `ste-code/refined/`) does not exist:

1. Record as ⬜ (Not Started) in the Pipeline Status table.
2. Set Actual count to 0 and % to 0%.
3. If the directory should exist (prior stage completed), mark as 🟠 Error and note the missing directory.
4. Do NOT create the directory. The stage orchestrator creates directories on first use.

### File Count Command Fails

If `find` or `du` returns an error instead of a count:

1. Record the exact command and error message in the Files on Disk section.
2. Use `ls -1 | wc -l` as a fallback for each directory.
3. If the fallback also fails, write "UNKNOWN — command failed: [error message]".
4. Note the failure in Errors & Blockers with severity 🟡.

### Cross-Stage Files Detected

If a file from one stage appears in another stage's directory:

1. Record as 🟠 Error under RAIL 1 — Stage Isolation.
2. List the file path, the stage it belongs to, and the stage directory it was found in.
3. Do NOT move the file. Flag it for the auditor.
4. Reference `.agents/skills/auditing/SKILL.md` for the full stage isolation verification procedure.

### Pipeline Paused Mid-Stage

If the pipeline is paused (no active workers, stage incomplete):

1. Mark the current stage as 🟢 with the actual completion percentage.
2. Mark all subsequent stages as ⬜.
3. In Next Actions, list: "Pipeline paused. Resume [stage] from [last completed batch]."
4. Include the last completed batch number and the next batch to launch.

## Consumers (Agents That Read State Reports)

These agents consume state reports. Write reports with these consumers in mind.

### Agent #3 — Auditor

Reads state reports before running a stage audit. The auditor compares state report counts against PROGRESS.md and disk evidence. If the state report claims a stage is ✅ but the auditor finds discrepancies, the discrepancy severity escalates (see Severity Escalation Path in `.agents/skills/auditing/SKILL.md`).

**What the auditor needs from the state report:**
- Exact file counts per stage (to compare against audit findings)
- PROGRESS.md sync status (to know if tracking is reliable)
- Rails compliance status (to prioritize audit checks)
- List of errors and blockers (to target audit investigation)

Reference: `.agents/skills/auditing/SKILL.md`

### Agent #4 — Continuator

Reads state reports at stage gates to decide if continuation is safe. The continuator does not proceed past a stage with unresolved 🔴 Critical or 🟠 Error items. If the state report shows a stage at 100% with all rails passing, the continuator starts the next stage.

**What the continuator needs from the state report:**
- Current stage completion percentage (to know where to resume)
- Last completed batch number (to know what comes next)
- PROGRESS.md sync status (to trust the tracking)
- Active workers list (to avoid duplicate launches)

Reference: `.agents/skills/continuation/SKILL.md`

### Execution Auditor (Hidden Agent)

Reads state reports to establish a baseline before running a forensic audit. The execution auditor trusts state report file counts only after cross-referencing against disk evidence. A state report that claims counts without shell command evidence is flagged as unreliable.

**What the execution auditor needs from the state report:**
- Shell command output in the Files on Disk section (proof of measurement)
- Timestamps of all file counts (to compare against audit timestamps)
- PROGRESS.md sync status with explicit match/mismatch flags

Reference: `.agents/skills/execution-auditor/SKILL.md`

### Agent #2 — Refiner

Reads state reports at the Stage 1 → Stage 2 handoff. The refiner does not start refinement until the state report shows Stage 1 at 100% with all 109 extraction files verified.

Reference: `.agents/skills/refinement/SKILL.md`

### Agent #1 — Extractor

Reads state reports produced by the auditor to learn which files need re-extraction. The state report's Errors & Blockers table is the extractor's re-extraction queue.

Reference: `.agents/skills/extraction/SKILL.md`

### Consumer Handoff Protocol

When a state report triggers a handoff (for example, Stage 1 complete → Stage 2):

1. The producing agent writes the state report to `.agents/audit/state-YYYYMMDD-HHMMSS.md`.
2. The producing agent writes a handoff entry in `exchange.md`:
   ```
   STATE→[TARGET_AGENT]: Stage N complete. State report at .agents/audit/state-YYYYMMDD-HHMMSS.md. [N] files verified on disk. Proceed to Stage N+1.
   ```
3. The consuming agent reads the state report from `.agents/audit/`.
4. The consuming agent runs its own verification before starting work (never trust the report alone).
5. If the consuming agent finds discrepancies, it writes back to `exchange.md`:
   ```
   [TARGET_AGENT]→STATE: State report discrepancy detected. [details]. Awaiting resolution before proceeding.
   ```

## Inter-Agent Information Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Extractor   │────▶│   Refiner    │────▶│  Continuator │
│  (Agent #1)  │     │  (Agent #2)  │     │  (Agent #4)  │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                     │                     │
       │    State Report      │    State Report      │    State Report
       │    (Stage 1→2)       │    (Stage 2→3)       │    (Stage 3→4,
       │                      │                      │     Stage 4→5)
       ▼                      ▼                      ▼
┌──────────────────────────────────────────────────────────┐
│                    Agent #3 (Auditor)                     │
│  Reads all state reports. Cross-references with disk.     │
│  Produces audit reports with severity classifications.   │
└──────────────────────────────────────────────────────────┘
       │
       │  Audit Report
       ▼
┌──────────────────────────────────────────────────────────┐
│             Execution Auditor (Hidden Agent)              │
│  Reads state reports AND audit reports.                   │
│  Runs forensic verification against disk evidence.        │
│  Auto-fixes safe patterns.                                │
└──────────────────────────────────────────────────────────┘
```

## Report Lifecycle

### Creation

1. Determine the trigger (mandatory handoff, mid-stage health check, operator request).
2. Run shell commands to populate all file counts.
3. Fill every section of the report template. Use "UNKNOWN — needs investigation" for any section that cannot be filled.
4. Write the report to `.agents/audit/state-YYYYMMDD-HHMMSS.md`.

### Verification

After writing, verify the report exists:

```bash
test -f .agents/audit/state-YYYYMMDD-HHMMSS.md && echo "Report saved" || echo "REPORT MISSING — write failed"
```

If the report is missing, check disk space and permissions. Do not proceed until the report is saved.

### Archiving

- Keep all state reports for the current pipeline run. Do not delete any report from an active run.
- After a pipeline run completes (all 5 stages reach 100%), move reports older than 14 days to `.agents/audit/archive/state/`.
- Keep the most recent 3 state reports in `.agents/audit/` at all times.

### Correlation with Audit Reports

Each state report correlates with audit reports by timestamp. When an audit report references a state report, it uses the path:

```
Audit: .agents/audit/audit-20260730-143022.md
References state report: .agents/audit/state-20260730-143500.md
```

State reports produced BEFORE an audit establish the baseline. State reports produced AFTER an audit reflect the corrected state. When both exist for the same timestamp window, the post-audit report is authoritative.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-07-26 | Initial release. Standardized format, execution rules. |
| 1.1.0 | 2026-07-30 | Added status emoji legend, complete example report, discrepancy resolution, edge cases, consumer cross-references, inter-agent flow diagram, trigger rules, report lifecycle. |
