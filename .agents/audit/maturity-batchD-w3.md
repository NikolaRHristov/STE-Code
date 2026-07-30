### .agents/references/granular-strategy.md
- **Level:** 2
- **Summary:** Defines a revised worker-split strategy for spec extraction, shrinking from coarse 30-112 page ranges to 4-page sweet spots (109 workers in ~36 batches), with launch templates and merge protocols.
- **Strengths:**
  - Concrete, executable math: 434 pages / 4 ppw = 109 workers, ~18 minutes estimate
  - Section-by-section breakdown table with per-segment worker counts for both 4pp and 10pp variants
  - Working bash launch template with actual `hermes -z` invocation
  - Git-based incremental save protocol and simple concatenation merge
- **Gaps:**
  - No cross-references to any other file - never mentions STE-CODE-IMPLEMENTATION.md even though the worker strategy directly feeds GATE 1 of that protocol
  - No failure modes: what if a batch times out mid-extraction, what if duplicate page ranges are assigned, what if a worker produces empty output
  - No edge cases: how to handle the 434th page when workers are 4pp (final worker gets 2 pages), how to handle sections that don't divide evenly into 4-page chunks
  - No rationale for the 1M context window claim - no load testing evidence, no memory profiling
  - No version history or revision tracking - if this is "Revised" (from what?), the original strategy is neither linked nor summarized
- **What Level 3 Would Add:** Cross-references to STE-CODE-IMPLEMENTATION.md (noting this strategy feeds GATE 1 worker assignments), explicit edge-case handling for uneven page splits and partial-batch failures, a rationale section explaining why 4pp was chosen over 6pp or 8pp with context-window measurements, and a "known limitations" note about the 1M window assumption being untested at scale.
- **Priority:** medium

---

### .agents/references/STE-CODE-IMPLEMENTATION.md
- **Level:** 3
- **Summary:** The master implementation protocol for the STE-Code pipeline - 5 hard-gated phases (environment setup, worker extraction, merge/validation, adaptation, artifact output) with JSON schemas, worker prompt templates, batch launch protocols, failure recovery, and final verification steps.
- **Strengths:**
  - Hard-gate architecture with explicit file-existence checks at every phase boundary - no phase can start without its prerequisite passing
  - Complete worker JSON schema (8 top-level arrays: rules, categories, dictionary_entries, synonyms, polysemy, pipeline_steps, evolution_history) with exact field descriptions
  - Concrete validation scripts: JSON validity check, content-quality check (non-empty arrays), merge deduplication, random spot-check of 10 pages against master state
  - Failure protocol: mark failed, re-launch same prompt, halve page range on second failure - a real recovery path, not just "try again"
  - Batch-of-3 constraint with explicit verification loop between batches - prevents resource exhaustion and promotes incremental progress tracking
  - Anti-fabrication preamble at the top: 5 rules establishing data-provenance discipline before any action
  - Output artifact specifications for all 6 deliverable files with structural templates and final token-budget verification
- **Gaps:**
  - No version history or change log - the document is a living protocol but has no record of what changed, when, or why
  - No meta-instructions for self-rewriting - if the worker schema needs a new field (e.g., `cross_references`), there's no protocol for updating the schema itself
  - Cross-references are implicit (references PROGRESS.md and worker output paths) but never explicitly link to granular-strategy.md (which defines the page-split rationale GATE 1 depends on), translation-grid.md (which would need to translate the 6 output artifacts), or the agent role definitions
  - Known limitations are absent: what happens if spec pages are malformed markdown, if spec/issue-09-2025/ has fewer than 434 pages, if the 1M context window isn't available on the target model
  - No measurable quality gates - verification is binary (file exists, JSON parses, non-empty arrays) but there's no quantitative threshold for extraction completeness (e.g., "at least 95% of expected rule numbers present")
  - The worker prompt template is embedded but never cross-referenced to the actual worker skill files in .agents/skills/ - if the prompt changes, no link ensures the skill file is updated
- **What Level 4 Would Add:** Explicit cross-reference map to all dependent files (granular-strategy.md, translation-grid.md, agent definitions, skill files), a rationale section explaining WHY batch-of-3, WHY 4pp workers, WHY deepseek-v4-pro, known limitations with workarounds (e.g., "if spec pages are fragmented, pre-merge adjacent pages before extraction"), measurable quality gates with numeric thresholds (expected rule count: 53, expected dictionary entries: ~875), and performance considerations with actual extraction throughput measurements.
- **Priority:** high

---

### .agents/references/translation-grid.md
- **Level:** 2
- **Summary:** A discovery-based translation tracking grid for 9 locales across 10 source directories, defining which files need translation placeholders, worker-locale assignments (3 workers × 3 locales), and a re-discovery protocol for incremental runs.
- **Strengths:**
  - Clear discovery-over-prescription philosophy: "this document tracks what's been found, not what should exist"
  - Expected file counts enumerated for all 10 target directories with per-file naming conventions (e.g., a-sec1-rule1.1.md through a-sec1-rule1.14.md)
  - Explicit skip rules with rationale per file pattern - prevents workers from trying to translate JSON schemas, Python scripts, structural configs, and scoring data
  - Placeholder directory layout defined across all 9 locales with nested source-directory preservation
  - Batch worker assignments clear: W1 handles CJK, W2 handles Romance+Germanic, W3 handles everything else
  - Re-discovery protocol with 5 concrete steps including placeholder-existence checks and catalog updates
- **Gaps:**
  - All 10 discovery targets are marked "⬜ Pending" with no last-scan timestamp - this is a planning document, not a log of actual discoveries
  - No cross-references to STE-CODE-IMPLEMENTATION.md (which defines the 6 artifact files this grid needs to translate) or to granular-strategy.md (which defines the batch-of-3 worker pattern this grid inherits)
  - No edge case handling: what happens when a source directory doesn't exist (e.g., `ste-code/v2/core/rules/` has only 4 files listed but the grid says "growing"), what happens when a worker encounters a new file type not in the skip list, what happens when two locales produce conflicting translations for the same shared term
  - No failure modes: what if a worker creates a placeholder but with wrong encoding, what if the locale directory structure doesn't match expectations
  - No examples of actual discoveries - the grid is entirely theoretical because no worker has run
  - The re-discovery protocol says "Workers skip files that already have placeholders" but doesn't define how workers distinguish a stale placeholder (source changed since last translation) from a current one
- **What Level 3 Would Add:** Cross-references to STE-CODE-IMPLEMENTATION.md (mapping the 6 artifact files to their translation targets), cross-references to granular-strategy.md (batch-of-3 justification), at least one completed discovery target with real file counts and timestamps, edge case handling for missing directories and new unlisted file types, a staleness-detection rule for the re-discovery protocol (compare source file mtime against placeholder creation timestamp), and an example of a successful placeholder write showing exact output format.
- **Priority:** medium

---

## Batch Summary
- Files scored: 3
- Level distribution: -2:0 -1:0 1:0 2:2 3:1 4:0 5:0
- Highest priority: STE-CODE-IMPLEMENTATION.md - the master protocol governs all pipeline execution but lacks explicit cross-references, numeric quality gates, known limitations, and version tracking, making it fragile under real usage when something goes wrong
- Pattern observations:
  - **Zero cross-references across all three files.** granular-strategy.md feeds GATE 1 of STE-CODE-IMPLEMENTATION.md, which produces 6 artifacts that translation-grid.md lists as translation targets, yet none of the three documents link to each other. This is the single biggest maturity gap - the files form a pipeline but are written as isolated islands.
  - **No version history anywhere.** All three documents have been revised or marked as "dynamic" / "revised" but none carry a change log, date stamp, or prior-version reference. Level 4+ requires this.
  - **Planning-heavy, execution-light.** translation-grid.md is entirely a scaffolding document (all targets pending). granular-strategy.md is a plan with no execution evidence (no throughput measurements). Only STE-CODE-IMPLEMENTATION.md reads like it was written after real runs, but it still lacks measured results.
  - **Concrete where it counts, abstract at the boundaries.** All three files excel at specifics within their scope (exact page counts, exact JSON schemas, exact file paths) but go silent at the edges: no "what if this fails" narratives, no assumed-environment violations, no stale-data detection.
