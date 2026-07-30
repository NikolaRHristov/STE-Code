# Agent State Report Format

Standardized format for pipeline state reports. Fill all sections. Agent-agnostic.

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
