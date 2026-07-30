  ┊ 📖 read      agent-3-auditor.md  0.2s
  ┊ 📖 read      SKILL.md  0.2s
  ┊ 📖 read      SKILL.md  0.2s
  ┊ 📖 read      agent-1-extractor.md  0.2s
  ┊ 📖 read      agent-2-refiner.md  0.2s
  ┊ 📖 read      rails.md  0.1s
  ┊ 📖 read      exchange.md  0.1s
  ┊ 📖 read      quality-checklist.md  0.1s
The file has been written with all 5 improvements applied. Here is a summary of what was added while preserving all existing content:

Improvements applied to `.agents/agent/agent-3-auditor.md` (74 lines → 416 lines):

**1. Full Example Audit Report** (lines 194–298)
A complete realistic audit report showing: 12 claims analyzed, 281 evidence files checked, 4 discrepancies (2 critical, 1 error, 1 warning), 8 verified claims, pipeline dashboard with percentages, rails compliance table (6 PASS / 2 FAIL), file counts with sizes, agent trust scores, auto-fixes applied, and prioritized next actions.

**2. Verification Procedures for R4, R5, R8** (lines 27–136)
- R4 (Content Fidelity): 5-file statistical sampling + 4 grep commands for fabrication markers (modern terms, commentary, placeholders, wrong facts) + spot-check protocol. Verdic criteria defined.
- R5 (Formatting Standards): Automated heading format check (loop over all files), glued heading detection, STE/Non-STE pair count balance check per file, table format check, 3-file spot-check against all 9 refinement rules.
- R8 (Error Recovery): Grep for recovery keywords in feedback history, stale file check, correction trace protocol (error documented → fix documented → disk state matches fix → no residuals).

**3. Edge Case Decision Table** (lines 308–324)
11 specific scenarios with severity and action: 107 files (2 missing), 100-106 files, <100 files, 109 files but 3 zero-byte, 109 files but 5 truncated <1KB, PROGRESS.md fabrication, 6/8 rails pass, 4/8 rails pass, wrong page content, no prior audits, extraction gap with refinement complete.

**4. Escalation Path with Priority Levels** (lines 326–398)
Four priority levels: BLOCKER (halt pipeline), HIGH (stop stage, re-launch workers), MEDIUM (flag for continuator, pipeline may continue), LOW (auto-fix or flag). ASCII workflow diagram, blocking criteria (5 conditions that prevent stage gate passage), and resolution workflow (5-step process: assess → write finding → auto-fix → re-audit → close).

**5. Rail Rationale Section** (lines 151–182)
Each rail (R1-R8) gets a paragraph explaining the real observed failure mode that created it, plus a consequence table showing what happens if each rail is violated. Examples: R1 prevents adaptation workers from fabricating artifacts from nonexistent source data; R3 came from PROGRESS.md claiming 109/109 when only 18 files existed.
