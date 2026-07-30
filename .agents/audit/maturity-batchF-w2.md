### SCE/compute/prompts/rule-adaptation.prompt.md
- **Level:** 2
- **Summary:** Worker prompt that adapts an existing STE-Code rule from a source domain to a target domain, replacing domain-specific vocabulary and generating 3 example pairs.
- **Strengths:**
  - Clear 6-step numbered instruction sequence with distinct verbs (READ, IDENTIFY, REPLACE, GENERATE, VERIFY, OUTPUT)
  - Structured output format template with all required frontmatter fields
  - Explicit cross-reference to `SCE/compute/schemas/rule-frontmatter.schema.json` for output validation
  - Valid frontmatter with declared variables (`source_rule_id`, `source_domain`, `target_domain`, `source_text`)
- **Gaps:**
  - No worked example - the prompt tells the worker to generate 3 example pairs but shows zero examples of what a good adaptation looks like
  - No edge-case guidance: what if source and target domains overlap (e.g., both are backend languages)? What if the target domain has no direct equivalent for a source-domain term?
  - No failure recovery: what should the worker do if the structural constraint cannot be preserved after domain adaptation?
  - No rationale for the "3 example pairs" requirement - why 3? What makes an example pair adequate?
  - No quality gate or self-verification checklist beyond step 5's vague "VERIFY"
- **What Level 3 Would Add:** At least one fully worked adaptation example showing source rule, target rule, and all 3 example pairs. Cross-reference to at least one existing adapted rule in `ste-code/adapted/` as a model. Explicit handling for the case where target domain terms don't exist (fallback to nearest equivalent with a warning annotation). A self-check rubric referencing `SCE/compute/checklists/pre-commit-checklist.json`.
- **Priority:** medium

### SCE/compute/prompts/compliance-check.prompt.md
- **Level:** 2
- **Summary:** Worker prompt for auditing text against STE-Code compliance rules - checks nouns, verbs, sentence length, term consistency, and anti-patterns.
- **Strengths:**
  - Concrete, measurable thresholds (20 words for procedural sentences, 25 words for descriptive)
  - Three explicit cross-references to structured data files: `SCE/core/categories/noun-categories.json`, `SCE/core/categories/synonym-table.json`, `SCE/compute/checklists/pre-commit-checklist.json`
  - Structured output format with a changes table (Line / Original / Corrected / Rule columns)
  - Distinct check categories (nouns, verbs, length, consistency, anti-patterns) covering the main compliance dimensions
- **Gaps:**
  - No examples of violations or passing text - the worker has no reference for what a "correct" compliance report looks like
  - No edge-case handling: compound technical nouns (e.g., `HashMap<String, List<Integer>>`), inline code snippets within prose, URLs/file paths that inflate word counts, multi-word approved terms
  - No scoring or severity rubric - all violations treated equally regardless of whether they're blocking vs advisory (cf. `SCE/core/README.md` severity values)
  - No partial compliance guidance: what if `rule_subset` is "all" but the worker runs out of context window? What if cross-referenced JSON files don't exist or are stale?
  - No handling for mixed prose+code documents (e.g., markdown with code blocks) - should code blocks be excluded from sentence-length checks?
- **What Level 3 Would Add:** One fully worked compliance report example with both passing and failing text. Explicit rules for excluding code blocks/URLs/file paths from sentence-length checks. Severity classification per violation (blocking/warning/advisory). Guidance on partial-runs when `rule_subset` filters to a manageable scope. Cross-reference to specific anti-pattern IDs in `pre-commit-checklist.json`.
- **Priority:** high

### SCE/README.md
- **Level:** 2
- **Summary:** Top-level architecture document describing the 4-stratum SCE design (core/data/compute/narratives), benchmark results, and loading strategies for different LLM context budgets.
- **Strengths:**
  - Clear 4-stratum architecture table with directory, type, and purpose columns
  - Loading strategy section with token-quantified options (500 / 4,000 / 2,500 / full) mapped to specific file paths
  - Relationship table clarifying the division of labor between `ste-code/`, `.agents/`, and `SCE/`
  - Version history table with dates and summary of changes
  - Includes benchmark results (96.6% pass rate) establishing credibility
- **Gaps:**
  - No rationale for the 4-stratum design - why 4? Why these boundaries? What problem does immutability of Stratum 1 solve vs mutability of Stratum 2?
  - No guidance on when to modify each stratum: "Change only when the spec changes" (Stratum 1) is stated in `core/README.md` but not here; no equivalent guidance for strata 2-4
  - No troubleshooting or FAQ section (e.g., "Why isn't my domain extension showing up? Check Stratum 2 load order")
  - No known limitations: which parts of ASD-STE100 are NOT covered? What's the token overhead at each loading level?
  - No contribution guide or instructions for adding a new stratum or category
  - Version history is minimal (2 entries) - no granular change log per stratum
- **What Level 3 Would Add:** Design rationale section explaining the immutability/mutability boundary decisions. Per-stratum modification guidance. FAQ covering common integration issues (load order, missing files, schema validation errors). A "What's Not Covered" section listing gaps vs the full ASD-STE100 spec. Cross-references from each stratum row to the stratum's own README.
- **Priority:** medium

### SCE/core/README.md
- **Level:** 2
- **Summary:** Stratum 1 documentation - describes the immutable rule directory, 14 principles (P1-P14) table, and the frontmatter schema required for every rule file.
- **Strengths:**
  - Complete P1-P14 principles table with rule name and type classification (Vocabulary/Grammar/Semantics/Style/Domain/Consistency/Orthography)
  - Explicit frontmatter schema with field-by-field descriptions
  - Enumerated `severity` values (blocking/warning/advisory) with clear definitions
  - Enumerated `agentic-load` values (required/optional/conditional) with context-sensitive definitions
  - States the immutability contract upfront: "Change only when the spec changes"
- **Gaps:**
  - No examples of an actual rule file - the frontmatter schema is shown in isolation without a complete rule body example
  - No cross-references to any actual rule file in `rules/` (e.g., "see `rules/rule-1.1.md` for a complete example")
  - No validation instructions: how does a developer verify that all rule files conform to the schema?
  - No explanation of how `agentic-load: conditional` is resolved (which domain tags trigger it?)
  - No enumeration of exactly which rule files exist - only a range (`rule-1.1.md through rule-9.4.md + gr-1.md through gr-4.md`) with no count or categorized listing
  - No rationale for the frontmatter field choices (why `constraint-type` has the values it does? Why is `scope` an array?)
- **What Level 3 Would Add:** One complete rule file example with frontmatter + body. A table of all rule files organized by section with file paths. Validation instructions referencing `SCE/compute/schemas/rule-frontmatter.schema.json`. Explanation of `conditional` agentic-load resolution (domain tag mapping). Cross-reference to `SCE/data/` for domain-specific extensions.
- **Priority:** medium

## Batch Summary
- Files scored: 4
- Level distribution: -2:0 -1:0 1:0 2:4 3:0 4:0 5:0
- Highest priority: `SCE/compute/prompts/compliance-check.prompt.md` - it's the most execution-critical (compliance checking is the core value proposition), has the most cross-references that could be stale/broken, and lacks examples for what a correct report looks like
- Pattern observations:
  - All 4 files share the same gap pattern: they define structure and process but provide zero worked examples, making them hard for a new worker or developer to calibrate against
  - Cross-references are present in 3 of 4 files but none verify that the referenced files actually exist or are at an adequate maturity level - this is a systemic risk if referenced schemas/checklists are also at Level 2 or below
  - None of the files include error/failure handling or fallback behavior, which matters especially for the two worker prompts that operate autonomously in a pipeline
  - The SCE/README.md and SCE/core/README.md both describe architecture well for a human reader but provide no programmatic hooks (no JSON/YAML manifest, no machine-readable file index) that a pipeline could consume - the architecture is documented for humans only
