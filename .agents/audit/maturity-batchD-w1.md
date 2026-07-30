### .agents/references/worker-rails.md
- **Level:** 3
- **Summary:** Injected worker self-validation checklist with 10 numbered rails (W1-W10) covering page headers, glued headings, fabrication prevention, boilerplate control, STE/Non-STE formatting, table hygiene, blank-line rules, content completeness, and naming conventions. Includes bash verification commands.
- **Strengths:**
  - Concrete, numbered rails with checkbox format - workers can self-validate mechanically
  - Verification commands are executable bash snippets (wc -l, grep, head), not vague suggestions
  - Formatting examples are exact and unambiguous (STE/Non-STE blockquote format, table structure)
  - Clear distinction between "before writing" checklist and "after writing" verification
- **Gaps:**
  - No cross-references to `.agents/references/rails.md` (the broader 8-rail process guard) or `.agents/references/worker-grid.md` - rails W3/W6/W9 overlap with rails.md Rail 4/5 but the relationship is never stated
  - No edge cases: what if `grep` isn't available (non-POSIX environment)? What if a 4-page extraction legitimately produces < 30 lines?
  - No failure recovery guidance - if a rail fails, what should the worker do? Delete and restart? Fix inline?
  - No version history or changelog - unclear when rails were added, which are new vs. mature
  - No rationale for design decisions - why 10 rails? Why is the line-count threshold 30? Why 4-page grouping?
  - Rail W9 ("Content Complete") is non-mechanically-checkable - it relies on worker honesty with no verification command
- **What Level 4 Would Add:** Explicit cross-references to rails.md for each overlapping rail (W3→Rail 4, W6→Rail 5, W9→Rail 4); edge case handling per rail (e.g., "if page range has no tables, skip W6-W7"); failure recovery procedures tied to rails.md Rail 8; rationale section explaining why each rail exists and what failure mode it prevents; known false-positive situations (e.g., `grep` for glued headings may fail on non-GNU grep).
- **Priority:** low

### .agents/references/worker-grid.md
- **Level:** 2
- **Summary:** Launch architecture document describing the 109-worker extraction pipeline: 434 pages grouped by 4 into 109 workers, batched 3-at-a-time into 37 batches. Contains the full batch map (all 37 batches with page ranges), a worker prompt template, and a high-level launch script description.
- **Strengths:**
  - Batch map is exhaustive and mechanically verifiable - every page range is accounted for
  - Concrete prompt template with exact hermes -z invocation syntax
  - Clear design summary with time estimates (20-37 minutes total)
  - References an implementation file (`launch-workers.sh`)
- **Gaps:**
  - No error recovery or failure modes - what happens when a batch worker times out, produces truncated output, or fabricates content? No procedure for retry, splitting, or skipping
  - No cross-references to `.agents/references/worker-rails.md` or `.agents/references/rails.md` - workers launched from this grid must follow those rails, but the grid never mentions them
  - No verification gates - the launch script description says "Wait for batch completion" but never defines what "completion" means (all files >3KB? rails passed?)
  - No rationale for design choices: why 4 pages per worker? Why 3 workers per batch? Why 30-60s per batch?
  - No version history - the header says "v3" but there's no changelog explaining what changed from v1/v2
  - Batch 37 is a special case (2 pages, not 4) - noted but no special handling documented (different line-count threshold? different prompt?)
  - No mention of the 109-worker naming convention's relationship to the wNNN-pPPPP-PPPP.md pattern in rails.md Rail 2
- **What Level 3 Would Add:** Failure recovery section with specific procedures (truncated output → split page range; timeout → retry with notify_on_complete); cross-references to worker-rails.md (validation checklist) and rails.md (stage isolation, naming, completion integrity); per-batch verification gates with pass/fail criteria; rationale for 4-page grouping and 3-worker batching; version history documenting v1→v2→v3 changes; special-case handling for Batch 37.
- **Priority:** high

### .agents/references/rails.md
- **Level:** 4
- **Summary:** Comprehensive process guardrail document with 8 rails covering stage isolation, naming conventions, completion integrity, content fidelity, formatting standards, factual correctness, progress tracking, and error recovery. Includes formatting examples with ✅/❌ pairs, fabrication detection signals, an immutable facts table, an error recovery action table, and an 8-item quick self-check.
- **Strengths:**
  - Eight distinct rails covering the full lifecycle: directory discipline, naming, verification, content honesty, formatting, factual grounding, progress tracking, and error recovery
  - Fabrication detection signals are specific and grep-able (exact strings: "React", "Docker", "This page describes")
  - Error recovery table maps specific mistakes to concrete recovery actions - this is rare and valuable
  - Formatting standards use ✅/❌ visual pairs that are unambiguous and testable
  - Immutable facts table with wrong-claim examples prevents hallucination about project constants
  - Quick self-check consolidates all 8 rails into a single actionable checklist
  - Cross-references PROGRESS.md explicitly (Rail 3, Rail 7)
- **Gaps:**
  - No version history or changelog - unclear which rails were added when, making it hard to assess whether recent additions are battle-tested
  - No measurable quality gates with numeric thresholds - Rail 3 has ">3KB (>30 lines)" but other rails lack pass/fail criteria (e.g., "glued headings detected: allowed ≤0")
  - No known limitations section - e.g., the `grep` glued-heading check may produce false positives/negatives on different grep implementations; the 30-line threshold may be wrong for 2-page extractions
  - Rail 6 (Factual Correctness) has static hardcoded facts that could drift - no meta-instruction to update this rail when project constants change (e.g., model name, rule counts)
  - No cross-reference to `worker-rails.md` - the worker-level rails (W1-W10) are a subset/specialization of these process rails, but the relationship is never documented
  - No agentic-load specification - unclear which rails an orchestrator must check vs. which a worker checks vs. which an auditor/verifier checks
- **What Level 5 Would Add:** Version history table with dates and rationale for each rail addition; meta-instructions for self-rewriting when project constants change (e.g., "when model name changes, update Rail 6 facts table and this sentence"); measurable quality gates per rail with numeric pass/fail thresholds; known limitations section documenting false-positive scenarios and platform-specific issues; explicit mapping between process rails and worker rails (which W-rail maps to which process rail); agentic-load assignments specifying which agent role owns which rail.
- **Priority:** medium

## Batch Summary
- Files scored: 3
- Level distribution: -2:0 -1:0 1:0 2:1 3:1 4:1 5:0
- Highest priority: `.agents/references/worker-grid.md` (Level 2 - missing error recovery, cross-references, and verification gates; this is the launch document that drives 109 workers and it has no failure handling)
- Pattern observations:
  - **Missing cross-reference mesh:** All three files govern the same pipeline but none reference each other. `worker-rails.md` (the worker checklist) never cites `rails.md` (the process guardrails). `worker-grid.md` (the launch doc) never cites either. `rails.md` never cites `worker-rails.md`. This creates a fragmented governance surface where workers launched via the grid don't know they must satisfy both rail sets.
  - **No version history anywhere:** Despite `worker-grid.md` being labeled "v3", none of the three files have a changelog or version table. This makes it impossible to audit which rules are recent and potentially undertested vs. which have survived many pipeline runs.
  - **Error recovery is siloed:** `rails.md` Rail 8 has an excellent error recovery table, but neither `worker-grid.md` nor `worker-rails.md` defer to it or extend it for their domain-specific failure modes (batch timeouts, truncated extractions, grep unavailability).
  - **Verification is uneven:** `worker-rails.md` has executable bash verification. `rails.md` has a checkbox self-check. `worker-grid.md` has no verification at all beyond "Wait for batch completion." The launch document that orchestrates 109 workers should be the most verification-heavy of the three, but it's the weakest.
