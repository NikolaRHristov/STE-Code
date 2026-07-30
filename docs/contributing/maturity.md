# Maturity Model

7-level scale for assessing instruction file completeness.

| Level | Name | Description |
|:-----:|------|------------|
| −2 | Placeholder | Empty or auto-generated stub |
| −1 | Skeleton | Headings only, no body text |
| 1 | Basic | Shallow content, no examples |
| 2 | Functional | Usable, lacks edge cases and cross-refs |
| 3 | Comprehensive | Examples, cross-refs, executable |
| 4 | Expert | Edge cases, failure recovery, rationale, known limitations |
| 5 | Production | Self-improving, measurable quality gates, version history |

**Current distribution:** 5×L4, 28×L3, 47×L2, 4×L1 (from maturity audit, July 2026).
**Target:** All instruction files at L3+.

See `.agents/audit/maturity-batch*.md` for per-file assessments.
