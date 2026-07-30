# Execution Auditor Protocol

Hidden verification skill. Validates actions against `.agents/references/rails.md` — 8 immutable guardrails. Agent-agnostic.

## Core Principle

Trust nothing. Verify everything against files on disk. A file on disk is evidence. A file with matching content is proof.

## Audit Protocol

1. **Collect Claims** — Read PROGRESS.md, exchange.md, all claim sources
2. **Collect Evidence** — File existence, content, timestamps on disk
3. **Cross-Reference** — Claim vs evidence for each file
4. **Flag Discrepancies** — 🔴 Critical, 🟠 Error, 🟡 Warning
5. **Produce Report** — Write to `.agents/audit/audit-YYYYMMDD-HHMMSS.md`

## Fabrication Detection

Files with these patterns were likely fabricated:
- Modern software terms in spec extraction ("React", "Docker", "npm")
- Commentary language ("This page describes...", "The key point is...")
- Missing spec boilerplate (no "ASD-STE100" header)
- Smooth flowing prose (spec is terse/instructional)
- Identical content across workers

## Auto-Fixes (safe patterns only)

| Pattern | Fix |
|---------|-----|
| `22 categories` | → 19 |
| `deepseek-pro` | → deepseek-v4-pro |
| Empty stale directories | Remove |
| Fabricated artifact files | Delete (must be regenerated) |

Never fix missing worker files (requires re-extraction) or truncated content (requires re-extraction with smaller range).

References: `.agents/references/rails.md`, `.agents/skills/state-report.md`
