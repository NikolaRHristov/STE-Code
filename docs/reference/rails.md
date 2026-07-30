# Rails Reference

8 behavioral guardrails for all pipeline agents.

**Source:** `.agents/references/rails.json`

| Rail | Rule | Severity | Detection | Violation Action |
|------|------|----------|-----------|-----------------|
| R1 | Stage Isolation — never cross-contaminate directories | Critical | File age comparison across stages | Halt — do not commit |
| R2 | Naming Convention — `wNNN-pPPPP-PPPP.md` | Critical | Regex pattern match | Halt — rename before commit |
| R3 | Completion Integrity — verify before claim | Critical | PROGRESS.md vs disk diff | Halt — sync tracker to reality |
| R4 | Content Fidelity — zero fabrication | Critical | Statistical sampling + grep | Halt — raise R001-FABRICATION |
| R5 | Formatting Standards — 9 refinement rules | Critical | Automated format checks | Halt — re-refine |
| R6 | Factual Correctness — immutable facts | Blocking | Grep for wrong values | Flag — do not block commit |
| R7 | Progress Tracking — PROGRESS.md matches disk | Blocking | Count comparison | Flag — sync tracker |
| R8 | Error Recovery — fixes documented | Blocking | Grep recovery keywords in exchange.md | Write recovery flag to audit/ |

## Rail Rationale

Each rail prevents a specific failure observed in real pipeline execution:

- **R1:** Adaptation workers wrote fabricated artifacts before extraction completed
- **R2:** Non-standard names made gap detection impossible
- **R3:** PROGRESS.md claimed 109/109 when disk held 18 files
- **R4:** Adapted files contained invented code examples with no source reference
- **R5:** Inconsistent formatting broke downstream merge and adaptation workers
- **R6:** "22 categories" and "deepseek-pro" propagated through all stages
- **R7:** Orchestrator ran 26 batches but PROGRESS.md showed only 1
- **R8:** Truncated output stayed on disk with no retry
