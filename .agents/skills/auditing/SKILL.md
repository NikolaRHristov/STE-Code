# Execution Auditor Protocol

Hidden verification skill. Validates actions against `.agents/references/rails.md` - 8 immutable guardrails. Agent-agnostic.

## Core Principle

Trust nothing. Verify everything against files on disk. A file on disk is evidence. A file with matching content is proof.

## Audit Cadence

Run an audit at these points:

- After each stage completes (Extraction, Refinement, Merge, Adaptation, Artifacts)
- After any batch claim of "complete" from a worker or orchestrator
- On-demand when a discrepancy is reported or suspected

Do not run an audit after every batch of 3 workers. Use per-batch validation from `.agents/skills/validation/SKILL.md` for that frequency. The audit protocol is a stage-level quality gate. Use validation checks for batch-level progress.

### Audit Scope Selection

Not every audit must cover the full pipeline. Choose a scope based on the trigger:

| Trigger | Recommended Scope | Rationale |
|---------|-------------------|-----------|
| Stage N completed | Full pipeline (Stages 1-N) | Confirm all prior stages are intact before Stage N+1 starts |
| Single batch claim | That stage only | Narrow scope for fast turnaround |
| Discrepancy reported | The reported stage + one stage up/down | Discrepancies often cascade across boundaries |
| Fabrication suspected | Full pipeline | One fabrication means all output is suspect |
| Pre-release / pre-merge | Full pipeline (all 5 stages) | Final quality gate before artifacts ship |
| Continuation after pause | Current stage + one prior stage | Confirm nothing degraded while idle |

When time is limited, prioritize in this order: (1) the current stage, (2) fabrication checks on the current stage, (3) cross-stage isolation checks, (4) prior stage integrity.

## Audit Protocol

1. **Collect Claims** - Read PROGRESS.md, exchange.md, all claim sources
2. **Collect Evidence** - File existence, content, timestamps on disk
3. **Cross-Reference** - Claim vs evidence for each file (see Cross-Reference Guidance below)
4. **Flag Discrepancies** - 🔴 Critical, 🟠 Error, 🟡 Warning (see Severity Classification below)
5. **Produce Report** - Write to `.agents/audit/audit-YYYYMMDD-HHMMSS.md`

### Cross-Reference Guidance

For each file, compare the claim against the evidence. Classify the result into one of three levels:

**Match** - The file on disk agrees with the claim. Criteria:
- File exists at the claimed path
- File content matches the claimed content or purpose
- File timestamp is recent and consistent with the claim
- File size falls in the expected range for its type

**Near-Match** - The file exists but has a small deviation. Criteria:
- File exists but has a naming convention error (for example, `w1-sec1.md` instead of `w001-p1-4.md`)
- File exists but content is stale (timestamp older than the claimed completion time)
- File exists but content is truncated (last line ends mid-word)
- File exists but has a factual error (wrong model name, wrong category count)

**Mismatch** - The claim and the evidence disagree. Criteria:
- File does not exist at the claimed path
- File exists but content is completely wrong (wrong stage, wrong page range)
- File contains fabricated content with no source backing
- Claim says "complete" but evidence shows missing or empty files

For each near-match or mismatch, record the specific rail violated from rails.md.

#### Cross-Reference Decision Tree

Use this ordered decision tree for each file. Stop at the first rule that matches:

```
1. Does the file exist at the claimed path?
   NO  → MISMATCH (RAIL 3: Completion Integrity)
   YES → Continue to step 2.

2. Does the file size fall in the expected range?
   - Extraction workers: >3KB, >30 lines
   - Refinement workers: >2KB, >20 lines
   - Adaptation workers: >1KB, >15 lines
   - Artifact files: >500 bytes
   NO  → MISMATCH (RAIL 3: Completion Integrity) or NEAR-MATCH if slightly below
   YES → Continue to step 3.

3. Does the filename match the stage naming convention?
   NO  → NEAR-MATCH (RAIL 2: Naming Convention)
   YES → Continue to step 4.

4. Is the file content consistent with its claimed stage and page range?
   NO  → MISMATCH (RAIL 4: Content Fidelity - wrong content)
   YES → Continue to step 5.

5. Does the file contain any fabrication signals?
   YES → MISMATCH (RAIL 4: Content Fidelity - fabricated)
   NO  → Continue to step 6.

6. Is the file timestamp consistent with the claimed completion time?
   NO  → NEAR-MATCH (RAIL 5: Formatting Standards - stale)
   YES → Continue to step 7.

7. Does the file content match the expected factual baseline?
   - Category count: 19 (not 22)
   - Model name: poolside/laguna-s-2.1:free
   - Rule count: 53 writing rules + 4 GR rules
   NO  → NEAR-MATCH (RAIL 6: Factual Correctness)
   YES → MATCH
```

### Severity Classification

Use these definitions to assign a severity to each discrepancy:

**🔴 Critical** - A discrepancy that causes data loss or indicates fabrication:
- Fabricated content detected (violates RAIL 4: Content Fidelity)
- Deleted or overwritten source files (violates RAIL 1: Stage Isolation)
- Progress claims that contradict disk evidence (violates RAIL 7: Progress Tracking)
- Wrong factual claims about immutable facts (violates RAIL 6: Factual Correctness)

Action: Stop the pipeline. Delete fabricated files. Report immediately.

**🟠 Error** - A discrepancy that blocks correct pipeline operation:
- Missing required file (violates RAIL 3: Completion Integrity)
- Wrong naming convention (violates RAIL 2: Naming Convention)
- Truncated worker output (violates RAIL 3: Completion Integrity)
- File in wrong stage directory (violates RAIL 1: Stage Isolation)

Action: Mark the affected batch or stage as incomplete. Trigger re-extraction or re-generation.

**🟡 Warning** - A discrepancy that does not block operation but reduces quality:
- Stale content with timestamp older than expected
- Minor formatting deviations (violates RAIL 5: Formatting Standards)
- Empty stale directories that should be cleaned
- Near-match content that is usable but imperfect

Action: Record in the audit report. Fix if a safe auto-fix pattern exists. Flag for manual review otherwise.

#### Severity Escalation Path

When discrepancies persist across multiple audits, escalate the severity:

| Condition | Escalation |
|-----------|------------|
| Same 🟡 Warning appears in 3 consecutive audits | Promote to 🟠 Error |
| Same 🟠 Error appears in 2 consecutive audits | Promote to 🔴 Critical |
| 🔴 Critical not resolved within 1 audit cycle | Escalate to pipeline owner. Do not proceed to next stage. |
| 5 or more 🟡 Warnings in a single audit | Bundle and treat as 1 🟠 Error for the affected stage |
| Fabrication detected in 3 or more files in one stage | Promote the entire stage to 🔴 Critical regardless of individual file severity |

Record all escalations in the audit report with a reference to the prior audit that first flagged the discrepancy.

## Fabrication Detection

Files with these patterns were likely fabricated:
- Modern software terms in spec extraction ("React", "Docker", "npm")
- Commentary language ("This page describes...", "The key point is...")
- Missing spec boilerplate (no "ASD-STE100" header)
- Smooth flowing prose (spec is terse/instructional)
- Identical content across workers

### Additional Fabrication Signals

These signals are less common but equally strong indicators:

- **Time-travel content**: File references dates, versions, or events that post-date the source material. For example, a spec extraction mentioning "2026 release" when the spec is Issue 9 from 2025.
- **Hallucinated structure**: File invents section numbers, rule numbers, or page references that do not exist in the source. Cross-check all rule numbers against `.agents/references/rails.md` RAIL 6 table.
- **Confident wrongness**: File makes assertive claims with no hedging that are factually false. Real extractions preserve ambiguity from the source. Fabricated content sounds authoritative.
- **Template echo**: File reproduces the worker prompt instructions verbatim instead of extracted content. For example, "Extract pages X through Y and format as markdown" appearing in the output.
- **Cross-worker collusion**: Two or more files from different workers share identical fabricated passages. Real extractions from different page ranges never produce identical text.
- **Category inflation**: File claims "22 categories" or any count other than 19 for STE technical noun categories.
- **Wrong stage markers**: File uses refinement-stage language ("reformatted for clarity") in an extraction-stage file. Extraction output must be raw spec text only.

### Fabrication Confidence Scoring

When a signal is detected, assign a confidence score to guide the response:

| Score | Meaning | Action |
|-------|---------|--------|
| **HIGH** (3+ signals, or any hard-fact error) | Certainly fabricated | Delete immediately. Re-extract. Check siblings. |
| **MEDIUM** (2 signals, no hard-fact error) | Likely fabricated | Flag as 🔴 Critical. Spot-check against source page. If confirmed, delete and re-extract. |
| **LOW** (1 signal, ambiguous) | Possibly fabricated | Flag as 🟡 Warning. Note the signal. Compare against source on next spot-check cycle. |

A hard-fact error is any claim that contradicts the immutable facts in RAIL 6. A single hard-fact error always produces a HIGH confidence score.

### Detected Fabrication Procedure

When fabrication is detected, do these steps:

1. Mark the discrepancy as 🔴 Critical in the audit report.
2. Delete the fabricated file from disk immediately.
3. Check all other files from the same worker batch. Fabrication in one file often means fabrication in sibling files.
4. Record the fabrication pattern in the audit report. Include the specific signal that triggered detection.
5. Trigger re-extraction for the affected page range. Do not attempt to salvage any content from the fabricated file.
6. After re-extraction, run a spot-check on the new output. Compare it against the original spec page.

NOTE: Fabrication is a RAIL 4 violation. One fabrication detection requires a full batch re-audit.

### False Positive Handling

Not every fabrication signal means actual fabrication. Some signals have legitimate explanations:

| Signal | Legitimate Explanation | How to Verify |
|--------|----------------------|---------------|
| Modern software term | The spec page genuinely discusses software (rare but possible in appendices) | Check the source page directly |
| Commentary language | The source page contains an introduction or overview section | Cross-reference with source page content |
| Identical content across workers | Two adjacent workers share a page boundary with repeated boilerplate | Check if the identical content spans a page boundary |
| Smooth prose | The source section is a narrative introduction, not a rule | Verify the source page style matches the extraction |

When a fabrication signal has a legitimate explanation, do not delete the file. Record the signal and the explanation in the audit report as a NOTE entry. Downgrade the severity from 🔴 Critical to 🟡 Warning with the annotation "false positive - verified against source."

## Auto-Fixes (safe patterns only)

| Pattern | Fix |
|---------|-----|
| `22 categories` | → 19 |
| `deepseek-pro` | → poolside/laguna-s-2.1:free |
| Empty stale directories | Remove |
| Fabricated artifact files | Delete (must be regenerated) |

Never fix missing worker files (requires re-extraction) or truncated content (requires re-extraction with smaller range).

## Edge Case Handling

### Missing rails.md

If `.agents/references/rails.md` does not exist at the expected path:

1. Search for rails.md in alternative locations: `.agents/references/`, `ste-code/references/`, project root.
2. If found at an alternative path, copy it to `.agents/references/rails.md`. Record the move in the audit report.
3. If not found anywhere, the audit cannot proceed. Report the missing rails file as 🔴 Critical. Do not perform an audit without the rails reference. The 8 guardrails are the audit's measurement standard.
4. If rails.md exists but is corrupt or empty, load a clean copy from the project's canonical source. Record the replacement in the audit report.

### Corrupt rails.md

If rails.md exists but its content is malformed or unreadable:

1. Check the file size. An empty file (0 bytes) or a file under 500 bytes is certainly corrupt.
2. Check for the 8 RAIL headers. Run: `grep -c "^## RAIL" .agents/references/rails.md`. The expected count is 8. If the count is less than 8, rails.md is incomplete.
3. If corrupt, restore from the last known good version. Check `.agents/audit/` for a prior audit report that includes a rails.md checksum or integrity note.
4. If no backup exists, fetch rails.md from the project's canonical source (version control or reference copy).
5. Record the corruption and restoration in the audit report as 🔴 Critical. The audit cannot proceed with a corrupt measurement standard.

### Missing PROGRESS.md

If PROGRESS.md does not exist:

1. Record the absence as 🟠 Error. A missing PROGRESS.md means no claims exist to audit against.
2. Run the audit from exchange.md alone. Check file existence and content fidelity against the exchange log claims.
3. Report that the audit scope is reduced to exchange.md only.
4. After the audit, request that PROGRESS.md be regenerated from the state report skill (`.agents/skills/state-report.md`).

### Missing exchange.md

If exchange.md does not exist:

1. Record the absence as 🟠 Error.
2. Run the audit from PROGRESS.md alone. Check batch and stage completion claims against disk evidence.
3. Report that the audit scope is reduced to PROGRESS.md only.

### Both PROGRESS.md and exchange.md Missing

1. Record the absence of both files as 🔴 Critical.
2. Run a pure evidence audit. Check every stage directory for file existence, naming, size, and content signals. Do not use claims - use only disk evidence and rails.md rules.
3. Report all findings as a raw evidence audit with no claim cross-reference.

### Empty Directories

When a stage directory exists but contains no files:

1. Record as 🟡 Warning if the stage has not started yet (expected).
2. Record as 🟠 Error if the stage was claimed complete but has no files.
3. Remove empty directories only if they are stale and no work depends on them. Use the Auto-Fixes table pattern.

### Stale Audit Reports

Audit reports in `.agents/audit/` accumulate over time. Manage them:

1. Keep all audit reports for the current pipeline run. Do not delete any report from an active run.
2. After a pipeline run completes successfully (all 5 stages pass), archive reports older than 7 days:
   ```
   mkdir -p .agents/audit/archive/
   mv .agents/audit/audit-202607*.md .agents/audit/archive/
   ```
3. Keep the most recent 3 audit reports in `.agents/audit/` even after archiving. These serve as quick-reference for the current state.
4. Never delete an audit report that contains an unresolved 🔴 Critical or 🟠 Error. These reports are evidence of known issues.

### Race Conditions

When an audit and a worker run at the same time:

1. File timestamps may change during the audit. If a timestamp shifts between evidence collection and cross-reference, re-check the file.
2. A file that "does not exist" at evidence collection may appear mid-audit. Re-scan the directory before finalizing the report.
3. PROGRESS.md may be updated by a worker while the audit reads it. Read PROGRESS.md twice: once at the start and once at the end. If the two reads differ, note the change in the audit report.
4. If a race condition is detected, add a NOTE to the audit report: "Race condition detected - PROGRESS.md changed during audit. Results reflect state at [timestamp of second read]."

### Audit of a Running Pipeline

When an audit is requested mid-stage (pipeline is active, workers are running):

1. Clearly mark the audit report header: "**INTERIM AUDIT - Pipeline Active**".
2. Only audit completed batches (marked [x] in PROGRESS.md). Skip in-progress batches (marked [ ] or [!]).
3. Note in the report: "Stage N is in progress. This audit covers completed batches only. A full stage audit will run after stage completion."
4. Interim audits use a narrower scope. Focus on: completed batch file existence, naming conventions, and fabrication signals on completed output.

## Cross-Reference to Validation Skill

The audit protocol works together with `.agents/skills/validation/SKILL.md`. They have different scopes:

| Aspect | Auditing (this skill) | Validation (validation skill) |
|--------|----------------------|-------------------------------|
| Frequency | After each stage or on-demand | After every batch of 3 workers |
| Scope | Full pipeline, all stages | Per-batch extraction quality |
| Reference | rails.md (8 guardrails) | Spec pages, expected content signals |
| Output | Audit report in `.agents/audit/` | Validation log in `ste-code/validation-log.md` |
| Severity | 🔴/🟠/🟡 against rails | PASS/FAIL/WARN against thresholds |

Use validation for batch-level quality checks during extraction. Use auditing for stage-level integrity checks across the full pipeline. When a validation check finds a FAIL, the next audit must verify that the failure was resolved.

### Information Flow Between Skills

The two skills exchange information in both directions:

**Validation → Auditing**: Before running a stage audit, read `ste-code/validation-log.md` to learn:
- Which batches had FAIL results (target these first in the audit)
- Which workers were re-extracted (check the replacement output)
- Which spot-checks found issues (cross-reference with disk evidence)

**Auditing → Validation**: After an audit, the validation skill uses audit findings to:
- Adjust its threshold sensitivity (if audits find false positives, loosen WARN thresholds)
- Skip re-validating files that the audit confirmed as correct
- Prioritize spot-checks on files the audit flagged as near-match

### When to Choose Auditing vs Validation

| Situation | Use |
|-----------|-----|
| Just finished batch 5 of 37 | Validation |
| Just finished all 109 extraction workers | Auditing |
| Single worker produced suspicious output | Validation (spot-check) |
| About to start Stage 2 (Refinement) | Auditing (Stage 1 gate) |
| Someone reported a missing file | Auditing (on-demand) |
| Need a quick check that a batch is complete | Validation |
| Need to confirm the full pipeline is clean before release | Auditing |

## Quick Audit Checklist

Run this checklist before finalizing any audit report. Answer every question with file evidence, not memory:

```
□ Claims collected: Did I read PROGRESS.md and exchange.md?
□ Evidence collected: Did I check file existence, size, and timestamp for every claimed file?
□ Cross-reference complete: Did I run the decision tree for every file?
□ Severity assigned: Does every discrepancy have a severity tag with a rail reference?
□ Fabrication scanned: Did I check all files for the 11 fabrication signals?
□ Edge cases handled: Did I check for missing rails.md, PROGRESS.md, exchange.md, and empty directories?
□ Race conditions checked: Did I read PROGRESS.md twice and compare?
□ Auto-fixes applied: Did I apply safe auto-fixes (category count, model name, empty dirs)?
□ Report written: Did I save to .agents/audit/audit-YYYYMMDD-HHMMSS.md?
□ Report complete: Does the report include Summary, Critical, Error, Warning, Pass, and Cross-Reference sections?
```

## Example Audit Report

Below is a complete example audit report. Use this as a template for all audit output.

---

# Audit Report - 20260730-143022

**Audit scope**: Stage 1 (Extraction) completion
**Rails reference**: `.agents/references/rails.md`
**Claim sources**: PROGRESS.md, exchange.md

## Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 Error | 2 |
| 🟡 Warning | 3 |
| ✅ Pass | 101 |

## 🔴 Critical

### C-001: Fabricated content in w042-p165-168.md

- **Rail violated**: RAIL 4 (Content Fidelity)
- **Evidence**: File contains commentary language ("This page describes the procedure for..."). Original spec page 165 does not contain this text.
- **Detection signal**: Commentary language pattern
- **Action taken**: File deleted. Re-extraction queued for pages 165-168.
- **Sibling check**: w043-p169-172.md and w044-p173-176.md show no fabrication signals.

## 🟠 Error

### E-001: Missing file w089-p353-356.md

- **Rail violated**: RAIL 3 (Completion Integrity)
- **Evidence**: PROGRESS.md claims batch 30 complete. File w089-p353-356.md does not exist on disk. Sibling files w088-p349-352.md and w090-p357-360.md exist.
- **Claim**: Batch 30 marked [x] in PROGRESS.md
- **Action required**: Re-extract pages 353-356. Revert batch 30 to [ ] in PROGRESS.md.

### E-002: Wrong naming convention w1-sec4-rule5.1.md

- **Rail violated**: RAIL 2 (Naming Convention)
- **Evidence**: File named `w1-sec4-rule5.1.md`. Correct pattern is `a-sec4-rule5.1.md` for adaptation stage. File is in `adapted/` directory but uses extraction prefix.
- **Action required**: Rename to `a-sec4-rule5.1.md`.

## 🟡 Warning

### W-001: Stale timestamp on refined/r001-p1-4.md

- **Rail violated**: RAIL 5 (Formatting Standards)
- **Evidence**: File timestamp is 2026-07-28. Extraction completed 2026-07-30. Content is correct but timestamp suggests no re-refinement after latest extraction.
- **Action**: Flag for manual review. Content may need re-refinement from latest extraction.

### W-002: Empty directory ste-code/_scratch/

- **Rail violated**: RAIL 1 (Stage Isolation)
- **Evidence**: Directory `ste-code/_scratch/` exists but contains 0 files.
- **Action taken**: Directory removed (safe auto-fix).

### W-003: Wrong category count in adapted/a-sec1-rule1.5.md

- **Rail violated**: RAIL 6 (Factual Correctness)
- **Evidence**: File claims "22 categories". Immutable fact is 19 categories.
- **Action taken**: Patched to "19 categories" (safe auto-fix).

## ✅ Pass (sample)

| File | Check | Result |
|------|-------|--------|
| extracted/w001-p1-4.md | Exists, 127 lines, correct naming | PASS |
| extracted/w002-p5-8.md | Exists, 142 lines, correct naming | PASS |
| refined/r001-p1-4.md | Exists, content matches extraction source | PASS |
| ... | ... | ... |

101 files passed all checks.

## Cross-Reference

- Validation log: `ste-code/validation-log.md` shows 3 WARN entries for batch 28. This audit confirms 2 of 3 were false positives.
- State report: `.agents/skills/state-report.md` shows Stage 1 at 98% before audit. After audit: Stage 1 at 98% (1 file missing).

---

## Inter-Agent Handoff

After an audit report is written, the following agents consume the report:

### Agent #3 (Auditor) → Agent #4 (Continuator)

When the audit finds no 🔴 Critical or 🟠 Error issues, the continuator can proceed:

1. The continuator reads the most recent audit report from `.agents/audit/`.
2. If the report shows all PASS for the current stage, the continuator starts the next stage.
3. If the report shows unresolved issues, the continuator waits. It does not proceed past a stage with open Critical or Error items.

### Agent #3 (Auditor) → Agent #1 (Extractor)

When the audit finds missing or fabricated extraction files:

1. The auditor writes the re-extraction requirements in the audit report (page ranges, worker IDs).
2. The extractor reads the audit report and launches replacement workers for the affected pages.
3. After re-extraction, the extractor notifies the auditor to re-run the audit on the affected batch.

### Agent #3 (Auditor) → Agent #5 (SCE Populator) / Agent #6 (STE-Code Analysis)

When the audit finds factual errors in adaptation or artifact files:

1. The auditor records the specific factual errors with the correct values.
2. The adaptation/artifact agents read the audit report and apply corrections.
3. After correction, the agents notify the auditor for a spot-check re-audit on the corrected files.

### Handoff Protocol

Every handoff must include:
- The audit report path (for traceability)
- The specific discrepancy IDs that require action (for example, "E-001, E-002")
- The expected action (re-extract, rename, patch, regenerate)
- A deadline or priority (immediate, before next stage, before release)

Record all handoffs in `exchange.md` with the format:
```
AUDIT→[TARGET_AGENT]: [discrepancy IDs] - [action required] - [priority]
```

## Audit Report Lifecycle

### Creation

Write every audit report to `.agents/audit/audit-YYYYMMDD-HHMMSS.md`. The timestamp uses the audit start time, not the completion time. Use 24-hour format.

### Naming Convention

```
audit-YYYYMMDD-HHMMSS.md
audit-20260730-143022.md   ← Stage 1 completion audit, started 14:30:22 on 2026-07-30
audit-20260730-182145.md   ← Stage 2 completion audit, started 18:21:45 on 2026-07-30
```

### Status Tracking

Each audit report has an implicit status derived from its findings:

| Report Contains | Status | Meaning |
|----------------|--------|---------|
| Zero discrepancies (all PASS) | CLEAN | Pipeline is healthy. Proceed. |
| 🟡 Warnings only, no Critical or Error | PASS WITH NOTES | Pipeline is operational. Warnings do not block progress. |
| 🟠 Errors, no Critical | BLOCKED | Pipeline cannot proceed past this stage. Fix errors first. |
| 🔴 Critical | STOPPED | Pipeline is halted. Immediate action required. |
| Interim audit | IN PROGRESS | Audit is partial. Do not use for stage gating. |

The status is not written in the report file. It is derived by the consumer agent when reading the report.

### Archival

After a full pipeline run completes with CLEAN status on all 5 stage audits:

1. Move all audit reports from that run to `.agents/audit/archive/run-YYYYMMDD/`.
2. Keep the archive directory. Audit reports are evidence of pipeline integrity.
3. The archive naming pattern is `run-YYYYMMDD` where the date is the pipeline start date.

### Report Index

Maintain `.agents/audit/INDEX.md` with a summary of every audit report:

```markdown
# Audit Report Index

| Report | Date | Stage | Status | Critical | Error | Warning |
|--------|------|-------|--------|----------|-------|---------|
| audit-20260730-143022.md | 2026-07-30 | Stage 1 | BLOCKED | 1 | 2 | 3 |
| audit-20260730-182145.md | 2026-07-30 | Stage 2 | PASS WITH NOTES | 0 | 0 | 2 |
| audit-20260731-091530.md | 2026-07-31 | Stage 3 | CLEAN | 0 | 0 | 0 |
```

Update INDEX.md after every audit report is written. The index gives agents a quick overview of pipeline health without reading every report.

## References

- `.agents/references/rails.md` - 8 immutable guardrails (audit measurement standard)
- `.agents/skills/state-report.md` - Standardized pipeline state format
- `.agents/skills/validation/SKILL.md` - Per-batch validation checks (complementary, higher frequency)
- `.agents/audit/` - Audit report output directory
- `.agents/audit/INDEX.md` - Audit report index for quick pipeline health overview
- `.agents/audit/archive/` - Archived audit reports from completed pipeline runs
- `exchange.md` - Inter-agent communication log (handoff protocol)
