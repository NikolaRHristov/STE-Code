# Execution Auditor Protocol

Hidden verification skill. Validates actions against `.agents/references/rails.md` — 8 immutable guardrails. Agent-agnostic.

## Core Principle

Trust nothing. Verify everything against files on disk. A file on disk is evidence. A file with matching content is proof.

## Audit Cadence

Run an audit at these points:

- After each stage completes (Extraction, Refinement, Merge, Adaptation, Artifacts)
- After any batch claim of "complete" from a worker or orchestrator
- On-demand when a discrepancy is reported or suspected

Do not run an audit after every batch of 3 workers. Use per-batch validation from `.agents/skills/validation/SKILL.md` for that frequency. The audit protocol is a stage-level quality gate. Use validation checks for batch-level progress.

## Audit Protocol

1. **Collect Claims** — Read PROGRESS.md, exchange.md, all claim sources
2. **Collect Evidence** — File existence, content, timestamps on disk
3. **Cross-Reference** — Claim vs evidence for each file (see Cross-Reference Guidance below)
4. **Flag Discrepancies** — 🔴 Critical, 🟠 Error, 🟡 Warning (see Severity Classification below)
5. **Produce Report** — Write to `.agents/audit/audit-YYYYMMDD-HHMMSS.md`

### Cross-Reference Guidance

For each file, compare the claim against the evidence. Classify the result into one of three levels:

**Match** — The file on disk agrees with the claim. Criteria:
- File exists at the claimed path
- File content matches the claimed content or purpose
- File timestamp is recent and consistent with the claim
- File size falls in the expected range for its type

**Near-Match** — The file exists but has a small deviation. Criteria:
- File exists but has a naming convention error (for example, `w1-sec1.md` instead of `w001-p1-4.md`)
- File exists but content is stale (timestamp older than the claimed completion time)
- File exists but content is truncated (last line ends mid-word)
- File exists but has a factual error (wrong model name, wrong category count)

**Mismatch** — The claim and the evidence disagree. Criteria:
- File does not exist at the claimed path
- File exists but content is completely wrong (wrong stage, wrong page range)
- File contains fabricated content with no source backing
- Claim says "complete" but evidence shows missing or empty files

For each near-match or mismatch, record the specific rail violated from rails.md.

### Severity Classification

Use these definitions to assign a severity to each discrepancy:

**🔴 Critical** — A discrepancy that causes data loss or indicates fabrication:
- Fabricated content detected (violates RAIL 4: Content Fidelity)
- Deleted or overwritten source files (violates RAIL 1: Stage Isolation)
- Progress claims that contradict disk evidence (violates RAIL 7: Progress Tracking)
- Wrong factual claims about immutable facts (violates RAIL 6: Factual Correctness)

Action: Stop the pipeline. Delete fabricated files. Report immediately.

**🟠 Error** — A discrepancy that blocks correct pipeline operation:
- Missing required file (violates RAIL 3: Completion Integrity)
- Wrong naming convention (violates RAIL 2: Naming Convention)
- Truncated worker output (violates RAIL 3: Completion Integrity)
- File in wrong stage directory (violates RAIL 1: Stage Isolation)

Action: Mark the affected batch or stage as incomplete. Trigger re-extraction or re-generation.

**🟡 Warning** — A discrepancy that does not block operation but reduces quality:
- Stale content with timestamp older than expected
- Minor formatting deviations (violates RAIL 5: Formatting Standards)
- Empty stale directories that should be cleaned
- Near-match content that is usable but imperfect

Action: Record in the audit report. Fix if a safe auto-fix pattern exists. Flag for manual review otherwise.

## Fabrication Detection

Files with these patterns were likely fabricated:
- Modern software terms in spec extraction ("React", "Docker", "npm")
- Commentary language ("This page describes...", "The key point is...")
- Missing spec boilerplate (no "ASD-STE100" header)
- Smooth flowing prose (spec is terse/instructional)
- Identical content across workers

### Detected Fabrication Procedure

When fabrication is detected, do these steps:

1. Mark the discrepancy as 🔴 Critical in the audit report.
2. Delete the fabricated file from disk immediately.
3. Check all other files from the same worker batch. Fabrication in one file often means fabrication in sibling files.
4. Record the fabrication pattern in the audit report. Include the specific signal that triggered detection.
5. Trigger re-extraction for the affected page range. Do not attempt to salvage any content from the fabricated file.
6. After re-extraction, run a spot-check on the new output. Compare it against the original spec page.

NOTE: Fabrication is a RAIL 4 violation. One fabrication detection requires a full batch re-audit.

## Auto-Fixes (safe patterns only)

| Pattern | Fix |
|---------|-----|
| `22 categories` | → 19 |
| `deepseek-pro` | → deepseek-v4-pro |
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
2. Run a pure evidence audit. Check every stage directory for file existence, naming, size, and content signals. Do not use claims — use only disk evidence and rails.md rules.
3. Report all findings as a raw evidence audit with no claim cross-reference.

### Empty Directories

When a stage directory exists but contains no files:

1. Record as 🟡 Warning if the stage has not started yet (expected).
2. Record as 🟠 Error if the stage was claimed complete but has no files.
3. Remove empty directories only if they are stale and no work depends on them. Use the Auto-Fixes table pattern.

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

## Example Audit Report

Below is a complete example audit report. Use this as a template for all audit output.

---

# Audit Report — 20260730-143022

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

## References

- `.agents/references/rails.md` — 8 immutable guardrails (audit measurement standard)
- `.agents/skills/state-report.md` — Standardized pipeline state format
- `.agents/skills/validation/SKILL.md` — Per-batch validation checks (complementary, higher frequency)
- `.agents/audit/` — Audit report output directory
