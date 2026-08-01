### .agents/skills/extraction/SKILL.md
- **Level:** 3
- **Summary:** Orchestrates 109 parallel `hermes -z` workers for ASD-STE100 Issue 9 spec extraction. Defines launch rules, batch-of-3 coordination, quality checks, and mandatory PROGRESS.md tracking.
- **Strengths:**
  - Concrete, copy-paste-ready bash command templates
  - Version history (v3 changes enumerated: file I/O support verified, 4 pages/worker, 109 workers)
  - 6 quality checks per batch with specific thresholds (file existence, size >30 lines, truncation detection, content signals, fabrication detection, tracking update)
  - Explicit "Never" rules (never >4 pages, never inline extraction, never >3 workers/batch, never skip PROGRESS.md)
  - Clear failure recovery path: re-extract with page range split in half
  - Cross-references to `references/rails.md`, `references/worker-grid.md`, `references/section-types.md`, `.agents/state/PROGRESS.md`
  - Uses RAILS guardrail pattern with bold visual markers
- **Gaps:**
  - No edge case handling beyond truncation: worker hangs, timeout, output is directory not file, corrupted markdown, git commit failures
  - No rationale for the "batches of 3" design constraint - why not 4 or 5?
  - No performance estimates: total wall-clock time for 37 batches, token costs per worker, rate limit considerations
  - No known limitations documented (e.g., "dictionary pages with dense 4-column tables may still need manual fixes after extraction")
  - No meta-instructions for self-improvement or self-rewriting
  - Incomplete rails reference at line 30: "validate against ." - dangling period, missing path
  - Cross-references don't verify that referenced files exist at adequate maturity levels
  - No example of a correct output file (what good extraction looks like)
  - No differentiation between worker failure modes (empty output vs fabricated output vs partial output)
- **What Level 4 Would Add:** Dedicated edge-case section covering worker hangs, timeouts, corrupt output, and git commit failures with per-case recovery protocols. Design rationale for batch size, page count, and model choice. Performance benchmarks with timing data. Known limitations section with workarounds. Example of correct output format.
- **Priority:** medium

### .agents/skills/extraction/references/worker-prompts.md
- **Level:** 1
- **Summary:** Reference catalog of 9 worker prompts (W1-W9) used to extract the 434-page ASD-STE100 spec, covering front matter through appendices. Each prompt specifies page ranges, INCLUDE lists, and FORMAT instructions.
- **Strengths:**
  - Contains fully executable prompts - concrete and copyable
  - Consistent structure across all 9 entries: EXHAUSTIVE header, PAGES, TASK, INCLUDE, FORMAT
  - Specific page ranges, output paths, and content requirements per worker
  - Format instructions vary by content type (tables for rules, blockquotes for dictionary entries)
- **Gaps:**
  - **CRITICAL: Out of sync with parent skill.** `ste-code-workers/SKILL.md` is at v3 (4 pages/worker, 109 workers), but this file contains only 9 v2-style prompts with large page ranges (W1: 30 pages, W2: 36 pages, W6: 112 pages). No note explaining the discrepancy.
  - No introductory explanation of what these prompts are, when they were used, or how they relate to the current skill version
  - No cross-reference back to the parent `SKILL.md` or the v3 109-worker prompt generation approach
  - No version tracking or date stamps
  - No instructions for how to regenerate prompts if page splits change
  - No edge cases or failure documentation
  - No rationale for the 9 specific page-range splits (W5 is 14 pages, W6 is 112 pages - why?)
- **What Level 2 Would Add:** A header explaining these are v2 legacy prompts and how they differ from v3. Cross-reference to the parent SKILL.md. Instructions for generating v3-style 109-worker prompts. Rationale for the 9-way split. Version date and author.
- **Priority:** high

### .agents/skills/validation/SKILL.md
- **Level:** 3
- **Summary:** Systematic validation protocol for worker extraction output, with per-batch checks (file existence, content signals, truncation, fabrication) and full-extraction audits (coverage, volume, rule completeness). Includes a periodic spot-check protocol.
- **Strengths:**
  - Highly concrete - every check has a runnable bash snippet with specific thresholds
  - Content signal table maps 5 page ranges to expected keywords (grep commands provided)
  - Truncation detection lists 3 specific red flags (mid-word cutoff, partial table row, missing footer)
  - Fabrication detection enumerates 4 concrete anti-patterns (modern software examples, commentary language, missing boilerplate, smooth prose)
  - Rule completeness check has explicit enumeration of all 53 rules across sections 1-9
  - Specific numeric thresholds: <30 lines = FAIL, <80 lines = WARN, ≥80 lines = PASS
  - Spot-check protocol has concrete output format example with PASS/FAIL structure
  - Diff command provided for fabrication verification against original pages
- **Gaps:**
  - No edge case handling: full batch failure (all 3 workers produce empty output), timeout during validation, file system errors
  - No recovery protocol beyond the extraction skill's "split in half" - what if fabrication is confirmed? What if a worker produced output but it's entirely wrong?
  - No cross-reference to the extraction `SKILL.md` explaining how validation integrates with the orchestrator workflow
  - No rationale for threshold values (why 30 lines for FAIL, not 25 or 35?)
  - No known limitations (e.g., "grep-based content signal check can produce false negatives if page headers use variant formatting," "fabrication detection cannot catch subtle paraphrasing")
  - Incomplete rails reference at line 23: "validate against ." - same dangling period bug
  - Does not mention the PROGRESS.md file that the extraction skill mandates, despite being closely coupled to it
  - Spot-check protocol says "every 10th batch" but batches are defined as 3 workers - "10th batch" is ambiguous in a 37-batch pipeline
  - No meta-instructions for self-improvement or adjustment of thresholds based on observed failure rates
- **What Level 4 Would Add:** Edge case handling for all 4 check types with decision trees. Recovery protocols for each failure mode (fabrication confirmed → re-extract with stricter prompt; truncation → split range; empty output → retry with different model or context window). Rationale for all numeric thresholds. Known limitations per check type. Integration guide showing where validation fits in the overall pipeline. Meta-instructions for threshold tuning based on observed data.
- **Priority:** medium

### .agents/skills/refinement/SKILL.md
- **Level:** 3
- **Summary:** Second-pass worker swarm orchestrator that reformats extracted spec files into clean, standardized markdown. Defines 9 non-negotiable formatting rules with ✅/❌ examples, worker prompt template, launch protocol, and verification checks.
- **Strengths:**
  - Excellent "What This Fixes" table: 9 specific problem→solution pairs with concrete before/after descriptions
  - Rich ✅/❌ examples throughout, especially Rule 9 (spacing) which shows 3 wrong patterns and 1 correct pattern
  - Rule 6 (dictionary entry format) precisely specifies both APPROVED and UNAPPROVED entry structures
  - Clear worker prompt template with 9 rules in the same order as the skill, ensuring consistency
  - Output structure tree diagram showing extraction→refinement→master pipeline
  - Self-contained single-prompt launch block for bootstrapping a new session
  - Verification checks are concrete and testable (line count comparison, page number grep, header repetition check, STE format check, table header check)
  - Mandatory progress tracking section mirrors the extraction skill's pattern (REFINE-PROGRESS.md)
- **Gaps:**
  - No edge case handling: refined output shorter than input (content loss detected during verification) - what's the recovery? What if a table genuinely can't be reconstructed from 4-column interleaving?
  - No design rationale: why 9 rules? Why this exact dictionary entry format? What formatting decisions were rejected and why?
  - No known limitations (e.g., "4-column PDF interleaving recovery has a ~95% accuracy rate - some complex tables with merged cells may still need manual fixes," "page range boundaries that split dictionary entries mid-word require manual reattachment")
  - No performance estimates: refinement time per file, total wall-clock for 109 workers, token cost comparison vs extraction
  - No meta-instructions for self-improvement - no version history for refinement rules, no mechanism to add Rule 10 based on discovered patterns
  - Incomplete rails reference at line 32: "validate against ." - same dangling period bug
  - Rule 7 (metadata) has malformed formatting: lines 117-124 interleave prose, code block markers, and rule text in a confusing way that makes the expected output ambiguous
  - No cross-reference to the extraction or validation skills (refinement is pipeline stage 2, but doesn't acknowledge stages 1 or 3)
  - No guidance on what to do when verification checks fail per-batch
- **What Level 4 Would Add:** Edge case section covering content loss detection, unreconstructable tables, split dictionary entries, and corrupted source files with per-case recovery. Design rationale for each of the 9 rules. Known limitations with quantified accuracy estimates. Performance benchmarks. Cross-references to extraction and validation skills explaining pipeline integration. Failure recovery protocols for verification check failures. Meta-instructions for evolving the rule set.
- **Priority:** low

## Batch Summary
- Files scored: 4
- Level distribution: -2:0 -1:0 1:1 2:0 3:3 4:0 5:0
- Highest priority: `.agents/skills/extraction/references/worker-prompts.md` - critically out of sync with the v3 extraction skill (9 prompts vs 109 workers), needs immediate reconciliation or deprecation notice
- Pattern observations:
  1. **Dangling rails reference bug shared across all 3 SKILL.md files.** Each contains a `> **RAILS**: Before any action, validate against .` line where the path after "against" is missing (just a period). This appears to be a copy-paste artifact. Fix once in a shared template.
  2. **No file reaches Level 4 due to missing edge case handling.** All three Level 3 files are strong on the happy path but silent on what happens when things go wrong - worker hangs, corrupt output, verification failures, file system errors. This single gap is the primary blocker to Level 4 for the entire batch.
  3. **Cross-references are one-directional and unverified.** Files mention `references/rails.md`, `references/worker-grid.md`, etc., but don't verify these exist, aren't at adequate maturity levels, and don't cross-reference back. The validation and refinement skills don't reference each other despite being adjacent pipeline stages.
  4. **v2→v3 migration incomplete.** `ste-code-workers/SKILL.md` documents the v3 approach (109 workers, 4 pages each), but `worker-prompts.md` still contains v2 prompts (9 workers, 14-112 pages each). No bridging documentation exists.
  5. **No performance or cost data anywhere.** For a pipeline launching 109+ workers across 37+ batches, there are no estimates of wall-clock time, token consumption, or API costs. This makes it impossible to budget or optimize.
