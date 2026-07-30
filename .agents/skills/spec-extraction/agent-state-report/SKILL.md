---
name: agent-state-report
description: "Force any agent to produce a full-page current state report. Standardized format covering all pipeline stages, file counts, errors, and next actions."
version: 1.0.0
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

## Quick Launch

```
State report now. Full format. All sections. Verify against disk.
Write to .agents/audit/state-YYYYMMDD-HHMMSS.md.
```
