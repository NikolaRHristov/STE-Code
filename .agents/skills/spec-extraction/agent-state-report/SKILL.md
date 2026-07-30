---
name: agent-state-report
description: "Force any agent to produce a full-page current state report. Standardized format covering all pipeline stages, file counts, errors, and next actions."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [state, report, status, dashboard, all-agents]
---

# Agent State Report

## Trigger

When any agent receives: "state", "status", "report", "where are we", or "progress" —
produce this exact report format. Do not summarize. Fill every section.

---

## Pre-Flight Checks

Before you start the report, run these checks in order. If any check fails, see the
Edge Case Handling section below.

1. Confirm the pipeline root directory exists. Use: `test -d ste-code/ && echo "OK" || echo "MISSING"`
2. Confirm at least one stage directory exists. Use: `find ste-code/ -maxdepth 1 -type d | wc -l`
3. Confirm PROGRESS.md is readable. Use: `test -f .agents/state/PROGRESS.md && echo "OK" || echo "MISSING"`
4. Confirm a git repository is present. Use: `git rev-parse --git-dir 2>/dev/null && echo "OK" || echo "NO GIT"`
5. Record your current working directory. Use: `pwd`

NOTE: You can still produce a report if some checks fail. Use the edge case
protocols to fill each section honestly.

---

## REPORT FORMAT (fill all sections)

```markdown
# Agent State Report — YYYY-MM-DD HH:MM:SS

## Agent Identity
- **Role**: [extraction-orchestrator | refinement-orchestrator | execution-auditor | reviewer]
- **Session**: [identifier]
- **Last action**: [what I just did]
- **Time since last batch**: [minutes]

---

## Pipeline Status

| Stage | Directory | Expected | Actual | % | Status |
|-------|-----------|----------|--------|---|--------|
| 1 — Extract | `extracted/` | 109 | ?? | ??% | [✅/🟢/⬜] |
| 2 — Refine | `refined/` | 109 | ?? | ??% | [✅/🟢/⬜] |
| 3 — Merge | `merged/` | 2 files | ?? | — | [✅/⬜] |
| 4 — Adapt | `adapted/` | TBD | ?? | — | [✅/⬜] |
| 5 — Artifacts | `artifacts/` | 6 | ?? | — | [✅/⬜] |

---

## Active Workers

| Worker ID | Pages | Status | Output Size | Issues |
|-----------|-------|--------|-------------|--------|
| [list any actively running or recently completed workers] |

---

## Errors & Blockers

| Severity | Description | File/Worker | Action Needed |
|----------|-------------|-------------|---------------|
| 🔴 | [critical blocker] | | |
| 🟠 | [error] | | |
| 🟡 | [warning] | | |

---

## Rails Compliance

| Rail | Status | Issues Found |
|------|--------|-------------|
| R1 — Stage Isolation | [PASS/FAIL] | |
| R2 — Naming Convention | [PASS/FAIL] | |
| R3 — Completion Integrity | [PASS/FAIL] | |
| R4 — Content Fidelity | [PASS/FAIL] | |
| R5 — Formatting Standards | [PASS/FAIL] | |
| R6 — Factual Correctness | [PASS/FAIL] | |
| R7 — Progress Tracking | [PASS/FAIL] | |
| R8 — Error Recovery | [PASS/FAIL] | |

---

## Files on Disk (verified, not claimed)

```
[Run: find ste-code/ -name "*.md" -o -name "*.txt" | wc -l] total files
[Run: du -sh ste-code/] total size

extracted/: [count] files, [size]
refined/: [count] files, [size]
merged/: [count] files, [size]
adapted/: [count] files, [size]
artifacts/: [count] files, [size]
audit/: [count] files, [size]
prompts-refine/: [count] files, [size]
```

---

## Next Actions (prioritized)

1. [Immediate — what I'm doing now]
2. [Next batch to launch]
3. [Verification pending]
4. [Blocked on]

---

## Git State

```
[Run: git status --short]
[Run: git log --oneline -3]
```

---

## Notes

[Any observations, warnings, or context for other agents]
```

## Execution Rules

1. **Run shell commands** to populate counts — never estimate from memory.
2. **Verify file existence** with `ls` or `test -f` — never trust PROGRESS.md alone.
3. **Update PROGRESS.md** after producing this report if discrepancies found.
4. **Write report** to `.agents/audit/state-YYYYMMDD-HHMMSS.md`.
5. **If any section cannot be filled**, write "UNKNOWN — needs investigation" — never leave blank.

---

## Filled Example

This section shows a real completed report. Use it as a model. Replace the values
with your own shell output. Do not copy the numbers without verification.

```markdown
# Agent State Report — 2026-07-30 14:23:05

## Agent Identity
- **Role**: extraction-orchestrator
- **Session**: batch-37-final
- **Last action**: launched workers W107, W108, W109 for pages 425-434
- **Time since last batch**: 4 minutes

---

## Pipeline Status

| Stage | Directory | Expected | Actual | % | Status |
|-------|-----------|----------|--------|---|--------|
| 1 — Extract | `extracted/` | 109 | 109 | 100% | ✅ |
| 2 — Refine | `refined/` | 109 | 87 | 80% | 🟢 |
| 3 — Merge | `merged/` | 2 files | 0 | — | ⬜ |
| 4 — Adapt | `adapted/` | TBD | 0 | — | ⬜ |
| 5 — Artifacts | `artifacts/` | 6 | 0 | — | ⬜ |

---

## Active Workers

| Worker ID | Pages | Status | Output Size | Issues |
|-----------|-------|--------|-------------|--------|
| W107 | 425-428 | RUNNING | — | — |
| W108 | 429-432 | RUNNING | — | — |
| W109 | 433-436 | RUNNING | — | — |
| W106 | 421-424 | COMPLETE | 12K | None |

---

## Errors & Blockers

| Severity | Description | File/Worker | Action Needed |
|----------|-------------|-------------|---------------|
| 🟡 | W088 refinement output is 0 bytes | refined/r088-p349-352.md | Re-run refinement for pages 349-352 |

---

## Rails Compliance

| Rail | Status | Issues Found |
|------|--------|-------------|
| R1 — Stage Isolation | PASS | No cross-stage writes detected |
| R2 — Naming Convention | PASS | All 87 refined files match rNNN-pPPPP-PPPP.md |
| R3 — Completion Integrity | PASS | Extraction count verified: 109 on disk |
| R4 — Content Fidelity | PASS | Spot-checked 5 files, all valid markdown |
| R5 — Formatting Standards | PASS | No broken tables or missing headers |
| R6 — Factual Correctness | PASS | PROGRESS.md claims match disk counts |
| R7 — Progress Tracking | PASS | PROGRESS.md updated within last hour |
| R8 — Error Recovery | WARN | One zero-byte refined file (r088), re-run scheduled |

---

## Files on Disk (verified, not claimed)

```
109 total files (101 .md + 8 .txt)
12M    ste-code/

extracted/: 109 files, 8.2M
refined/: 87 files, 3.1M
merged/: 0 files, 0
adapted/: 0 files, 0
artifacts/: 0 files, 0
audit/: 3 files, 48K
prompts-refine/: 37 files, 340K
```

---

## Next Actions (prioritized)

1. Wait for workers W107-W109 to complete (extraction stage finish)
2. Launch refinement batch 30 (workers R088-R090)
3. Verify refined file count reaches 109 after current batch
4. None — no blockers active

---

## Git State

```
 M .agents/state/PROGRESS.md
?? .agents/audit/state-20260730-142305.md
abc1234 fix: extraction batch 36 — workers W104-W106 complete
def5678 chore: update PROGRESS.md after batch 35 verification
ghi9012 feat: refinement batch 29 — workers R085-R087 complete
```

---

## Notes

Extraction is 99% complete. Three workers (W107-W109) are running now. They cover
the final 10 dictionary pages. After they finish, Stage 1 is closed. Refinement
has 22 workers remaining. The zero-byte file r088 was a network timeout during
worker launch. Re-run it after the current extraction batch completes.
```

---

## Edge Case Handling

### No Pipeline Directory Found

If `test -d ste-code/` returns false:

1. Check if you are in the wrong directory. Run `pwd` and compare with the expected
   project root (usually the directory that contains `.agents/`).
2. Search for the pipeline root. Use: `find / -maxdepth 4 -name "ste-code" -type d 2>/dev/null`
3. If the directory is not found anywhere, set every Files on Disk count to "0 (directory missing)".
4. In the Notes section, write: "Pipeline directory `ste-code/` not found. Possible wrong working directory. Current: `$(pwd)`."
5. Still produce the report. The report is useful even with missing directories.

### Zero Files Found

If `find ste-code/ -name "*.md" -o -name "*.txt" | wc -l` returns 0:

1. Do not treat this as an error. The pipeline may be freshly initialized.
2. Set all stage file counts to 0.
3. Set all Pipeline Status percentages to 0%.
4. In the Notes section, write: "Pipeline directory exists but contains no .md or .txt files. Pipeline may be freshly initialized or files were removed."
5. Compare with PROGRESS.md. If PROGRESS.md claims non-zero counts, flag a discrepancy in Errors & Blockers with severity 🟠.

### No Git Repository

If `git rev-parse --git-dir` fails:

1. In the Git State section, write: "No git repository detected in this directory."
2. Skip the `git status --short` and `git log --oneline -3` commands.
3. Do not mark this as an error in Errors & Blockers. A missing git repository is a state fact, not a failure.
4. In the Notes section, write: "No git repository found. Version tracking is not available for this pipeline run."

### Wrong Working Directory

If the agent is not in the pipeline project root:

1. Run `pwd` and record the current directory.
2. Run `find / -maxdepth 5 -path "*/ste-code/extracted" -type d 2>/dev/null | head -1` to discover the pipeline root.
3. If found, use absolute paths for all shell commands. Example: `find /path/to/ste-code/ -name "*.md" | wc -l`
4. In the Notes section, write: "Running from non-standard directory: `$(pwd)`. Used absolute paths for all disk checks."
5. Write the report to `.agents/audit/state-YYYYMMDD-HHMMSS.md` using the discovered pipeline root path.

### Missing Stage Directories

If a stage directory (for example, `ste-code/adapted/`) does not exist:

1. Set that stage's file count to "0 (directory does not exist)".
2. Set that stage's status to ⬜ (not started).
3. Do not create the directory. This report is read-only.
4. In the Notes section, list all missing stage directories.

### PROGRESS.md Is Missing or Unreadable

If `test -f .agents/state/PROGRESS.md` returns false:

1. In the Pipeline Status table, set all Expected counts to "UNKNOWN".
2. In the Notes section, write: "PROGRESS.md is missing or unreadable. Expected file counts are unknown. Refer to `.agents/MASTER.md` for pipeline constants."
3. Use MASTER.md Factual Constants table (109 workers, 434 pages, etc.) to cross-check if available.
4. Flag this as 🟡 warning in Errors & Blockers.

### Git Status Fails (Dirty State or Permissions)

If `git status --short` returns an error:

1. In the Git State section, write: "Git command failed: [paste the error message]."
2. Try `git log --oneline -3` independently. It may succeed even if status fails.
3. Flag as 🟡 warning in Errors & Blockers if the failure is permission-related.

---

## Failure Modes & Recovery

### Disk Verification Shows PROGRESS.md Is Stale

If the file counts on disk differ from PROGRESS.md claims:

1. Run a full disk count for each stage directory. Use the Discovery Protocol below.
2. Compare each stage count with the claims in PROGRESS.md.
3. List every discrepancy in the Errors & Blockers table with severity:
   - 🔴 if PROGRESS.md claims a stage is complete but disk shows fewer files
   - 🟠 if PROGRESS.md claims a stage is in progress but disk shows more files
   - 🟡 if the difference is less than 3 files
4. In the Notes section, write the exact discrepancies found.
5. After writing the report, update PROGRESS.md using the Update Protocol below.

### Discovery Protocol for File Counts

Run these commands to get verified counts for every stage:

```bash
# Count files per stage directory
for dir in extracted refined merged adapted artifacts audit prompts-refine; do
  if [ -d "ste-code/$dir" ]; then
    count=$(find "ste-code/$dir" -maxdepth 1 -type f | wc -l | tr -d ' ')
    size=$(du -sh "ste-code/$dir" 2>/dev/null | cut -f1)
    echo "$dir: $count files, $size"
  else
    echo "$dir: directory does not exist"
  fi
done
```

Use the output to populate the Files on Disk section. Do not round or estimate.

### Rails Compliance Cannot Be Assessed

If you cannot assess all 8 rails:

1. Mark rails you cannot check as "UNKNOWN — see Notes".
2. In Notes, explain what blocks the assessment. Example: "Cannot assess R3 (Completion Integrity) because PROGRESS.md is missing."
3. For rails that need cross-reference files, check if those files exist:
   - Rail definitions: `.agents/references/rails.md` or `.agents/skills/spec-extraction/references/rails.md`
   - Worker rails: `.agents/references/worker-rails.md`
   - Quality checklist: `.agents/references/quality-checklist.md`
4. If the reference files are missing, note this in the Issues Found column.

### Partial Pipeline State

If some stages have data but others are empty:

1. This is normal during active pipeline execution. Do not flag as an error.
2. Mark empty stages with ⬜ (not started) in the Pipeline Status table.
3. In the Notes section, identify the current active stage and the transition boundary.
   Example: "Stage 1 complete, Stage 2 in progress. Transition boundary is between refined/ and merged/."

### Worker Count Mismatch

If the number of files in a stage directory does not divide evenly by the batch
size (3 for extraction, 3 for refinement):

1. Flag as 🟡 warning in Errors & Blockers.
2. Check if partial batches are expected. The last batch may have fewer than 3 workers.
3. List the worker IDs that appear missing. Use the naming pattern to find gaps.
   For extraction: `wNNN-pPPPP-PPPP.md` — check for gaps in the NNN sequence.
   For refinement: `rNNN-pPPPP-PPPP.md` — check for gaps in the NNN sequence.

---

## PROGRESS.md Update Protocol

When you find discrepancies between the disk state and PROGRESS.md, update
PROGRESS.md after writing the state report.

### Format for PROGRESS.md Updates

Use the existing PROGRESS.md structure. Do not change its format. Add or modify
only the sections that need correction:

1. **Update the "Last updated" timestamp** at the top of PROGRESS.md.
   Format: `> **Last updated:** YYYY-MM-DD — [brief description of what changed]`

2. **Update stage completion status** — If a stage moved from in-progress to complete,
   change the header status. Example: `## Extraction ... ✅ COMPLETE`

3. **Update batch status rows** — If individual batch statuses changed, mark them
   accordingly. Use: `✅` for complete, `🟢` for in-progress, `⬜` for not started.

4. **Add a change log entry** at the bottom of PROGRESS.md (create the section if it
   does not exist):

```markdown
## Change Log

| Date | Report | Changes Made |
|------|--------|-------------|
| YYYY-MM-DD | `state-YYYYMMDD-HHMMSS.md` | [list of specific changes] |
```

5. **Do not** delete old entries. Append to the change log.
6. **Do not** rewrite sections that are still correct.
7. **Do not** change the existing section structure or add new tracked metrics
   without explicit instruction.

### Example PROGRESS.md Update

If the disk shows 87 refined files but PROGRESS.md claims 80:

```markdown
> **Last updated:** 2026-07-30 — corrected refined file count (disk audit)
```

And in the Refinement stage batch table, update any batches that moved from
🟢 to ✅.

### When NOT to Update PROGRESS.md

Skip the PROGRESS.md update if:

1. The discrepancy is a single missing file that may be in-flight (worker still running).
2. The discrepancy is in a stage you did not launch (another orchestrator owns it).
3. You cannot confirm the disk count with at least two independent commands.
   Use both `find ste-code/refined/ -maxdepth 1 -type f | wc -l` and
   `ls ste-code/refined/ | wc -l` for confirmation.

---

## Cross-References

This section lists all external files that define terms, rules, or constants
used in this report. Use these files to populate the Rails Compliance and
Errors & Blockers sections.

| Reference | Path | Use |
|-----------|------|-----|
| **MASTER.md** | `.agents/MASTER.md` | Pipeline constants (109 workers, 434 pages, 19 categories, 53 rules). Terminology map. Naming conventions. Factual constants table. |
| **Rails (8-rail definitions)** | `.agents/references/rails.md` | Full definitions for all 8 process rails (R1-R8). Violation examples. Stage isolation rules. |
| **Worker Rails** | `.agents/references/worker-rails.md` | Worker-specific guardrails. Input validation rules. Output format requirements. |
| **PROGRESS.md** | `.agents/state/PROGRESS.md` | Authoritative progress tracker. Batch completion status. Expected file counts per stage. |
| **Quality Checklist** | `.agents/references/quality-checklist.md` | Per-stage quality criteria. Spot-check sampling rules. Acceptance thresholds. |
| **Pipeline Spec** | `.agents/MASTER.md` (sections: Pipeline Stages, Naming Conventions) | Directory map. Stage definitions. Expected file patterns. |
| **Worker Grid** | `.agents/references/worker-grid.md` | Complete worker-to-page mapping. Batch grouping. Worker ID ranges. |
| **Section Types** | `.agents/references/section-types.md` | Spec section classifications. Which pages contain rules vs dictionary vs examples. |

If any reference file is missing or unreadable, note it in the Notes section.
Do not fabricate reference content.

---

## Quick Launch

```
State report now. Full format. All sections. Verify against disk.
Write to .agents/audit/state-YYYYMMDD-HHMMSS.md.
```

---

## Safety Checklist

Before you claim the report is complete, verify these items:

- [ ] All shell commands returned real output (no fabricated numbers)
- [ ] The report file was written to `.agents/audit/state-YYYYMMDD-HHMMSS.md`
- [ ] The timestamp in the filename matches the timestamp in the report header
- [ ] Every section in the report format has content (no blank sections)
- [ ] The Files on Disk section uses verified counts, not PROGRESS.md claims
- [ ] The Pipeline Status table shows Actual counts that match the Files on Disk section
- [ ] Any UNKNOWN entries have a corresponding note explaining why
- [ ] If PROGRESS.md was updated, the change log entry was added
