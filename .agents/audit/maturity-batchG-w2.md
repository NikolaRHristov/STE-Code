# Maturity Audit - Batch G, Wave 2

> Auditor: poolside/laguna-s-2.1:free
> Date: 2026-07-30
> Template: `.agents/prompts/maturity-audit/worker-template.txt`
> Files: 6 (3 rule files, 2 READMEs, 1 top-level README)

---

### ste-code/v2/core/rules/rule-1.1.md
- **Level:** 3
- **Summary:** Defines the foundational vocabulary constraint - only STE-Code approved terms may be used. Covers code-domain scope (19 noun + 4 verb categories), provides violation/correct pattern pairs, and includes a programmatic detection query.
- **Strengths:**
  - Complete YAML frontmatter with all metadata fields (related-rules, anti-patterns, severity, agentic-load)
  - 4 violation/correct pattern pairs covering distinct error classes
  - Language-agnostic detection query in JSON format
  - "Related Compute" section cross-references 3 external artifacts (synonym-table.json, pre-commit-checklist.json, compliance-rubric.json)
  - Code Domain Scope section enumerates the 19 noun + 4 verb category framework
- **Gaps:**
  - No edge cases (e.g., what happens when a term is approved in one domain but not another; how to handle project-specific internal jargon that isn't in vocabulary)
  - No failure recovery instructions - if vocabulary lookup fails or vocabulary files are missing, what should the agent do?
  - No rationale section explaining why vocabulary-first is the P1 principle and how it interacts with rule-1.2 (approved meaning) vs rule-1.3 (technical nouns)
  - No version history or known limitations
  - No agentic-load specification beyond the frontmatter tag - doesn't explain what "required" means in pipeline context
- **What Level 4 Would Add:**
  - Edge case handling: domain-scoped term conflicts, project-internal terminology policy, vocabulary file missing/unreachable fallback
  - Rationale: why vocabulary is P1, how it chains with rules 1.2/1.3/1.5/1.6
  - Performance note: vocabulary lookup cost for large documents, caching strategy
  - Cross-reference integrity check: verify that `data/vocabulary/`, `data/synonyms/synonym-table.json`, `compute/checklists/pre-commit-checklist.json`, and `compute/scoring/compliance-rubric.json` all exist and are schema-valid
- **Priority:** low - already a strong Level 3 rule file; gaps are aspirational polish

---

### ste-code/v2/core/rules/rule-1.11.md
- **Level:** 3
- **Summary:** Enforces term consistency - one technical noun per concept throughout a document. Prevents synonym drift where the same entity is called by different names (e.g., "auth service" / "authentication module" / "login handler").
- **Strengths:**
  - Clear, focused scope - applies only to nouns, single responsibility
  - 3 violation/correct pattern pairs demonstrating real synonym-drift scenarios
  - "Agent Note" section explicitly states the document-level memory requirement - acknowledges that this rule is harder to implement than vocabulary lookup
  - Detection query is well-specified: `group-by-concept` with `flag: synonym-drift`
  - Cross-references to rule-1.1 (vocabulary) and rule-1.3 (technical nouns) in frontmatter
- **Gaps:**
  - No "Related Compute" section - unlike rule-1.1, doesn't reference scoring weights, checklists, or schemas that implement this rule
  - No edge cases: how to handle acronyms/initialisms (e.g., "API Gateway" vs "AGW"), generated vs human-authored text, multi-document consistency
  - No failure recovery - what should the agent do when it detects synonym drift mid-document? Rewrite retroactively or flag only?
  - No rationale for why this is a blocking rule and not a warning
  - No version history
- **What Level 4 Would Add:**
  - Edge cases: acronym resolution, multi-document scope, code-generated identifiers vs human text, casing variations
  - Related compute artifacts: link to scoring rubric weight for P11, pre-commit checklist item for term-consistency
  - Failure recovery protocol: flag-and-suggest vs auto-rewrite strategy, agent decision tree
  - Rationale: why one-term-per-concept matters for LLM comprehension and downstream tooling
- **Priority:** low - solid Level 3; missing "Related Compute" section is a consistency gap with rule-1.1 but minor

---

### ste-code/v2/core/rules/rule-1.12.md
- **Level:** 3
- **Summary:** Constrains all technical verbs to one of 4 approved categories (development, data, application, communication operations). Prevents vague verbs like "do", "perform", "execute" from entering code documentation.
- **Strengths:**
  - Summary table of the 4 verb categories with representative key verbs - makes the rule instantly grokkable
  - 3 violation/correct pattern pairs showing common verb substitution errors
  - Cross-reference to `core/categories/verb-categories.json` for the authoritative full list
  - Frontmatter correctly tags scope as `[verb]` and links to related rules 1.7 and 1.13
- **Gaps:**
  - No detection query - unlike rule-1.1 and rule-1.11, missing the JSON detection block entirely
  - No "Related Compute" section - doesn't reference scoring weights, checklists, or synonym table
  - No edge cases: what about multi-word verb phrases ("set up" vs "configure"), phrasal verbs in code comments, verbs that span categories (e.g., "validate" could be application or data ops)
  - No agent note or implementation guidance - rule-1.11 has one, this doesn't
  - No rationale for why 4 categories were chosen or how they map to ASD-STE100's original verb structure
- **What Level 4 Would Add:**
  - Detection query block formatted like rule-1.1 and rule-1.11
  - Edge case resolution: cross-category verbs, phrasal verb handling, verb+preposition combinations
  - Related compute: scoring rubric weight for P12, pre-commit checklist item, synonym table entries for common verb substitutions
  - Agent implementation guidance: lookup strategy, caching for verb-categories.json, flag-vs-rewrite decision tree
  - Rationale: design decision behind 4 categories, how they differ from ASD-STE100's original verb taxonomy
- **Priority:** medium - missing detection query and related compute section are structural inconsistencies with sibling rules 1.1 and 1.11; should be fixed for pipeline uniformity

---

### ste-code/v2/core/rules/README.md
- **Level:** 3
- **Summary:** Meta-documentation for the rules directory. Defines the YAML frontmatter schema, severity levels with CI behaviour, constraint types, and agent loading strategies.
- **Strengths:**
  - Complete YAML frontmatter schema with field descriptions and allowed values
  - Severity levels table maps each level to CI behaviour (fail/warn/info)
  - Constraint types table defines 5 categories with clear descriptions
  - "Loading by Agent" section provides two concrete loading scenarios (vocabulary-only vs full compliance)
  - Clean, scannable structure - tables for quick reference
- **Gaps:**
  - No example of a complete rule file - only shows frontmatter, not the markdown body sections
  - No guidance on adding a new rule: what sections are mandatory vs optional, naming convention enforcement, PR process
  - No cross-reference to `compute/schemas/` for frontmatter validation - the README says every JSON file has a schema, but doesn't say whether the YAML frontmatter itself has one
  - No version history or known limitations
  - No reference to which rules exist or a rule index - just describes format, not content
- **What Level 4 Would Add:**
  - Full example rule file (frontmatter + all recommended body sections)
  - Process documentation: how to add a new rule, mandatory vs optional body sections, naming scheme rule
  - Cross-reference to frontmatter schema if it exists in `compute/schemas/`
  - Rule index: table of all existing rules with id, title, constraint-type, severity (programmatic discoverability)
  - Edge cases: what happens if two rules have conflicting severities for the same violation type
- **Priority:** low-medium - solid documentation; adding a rule index and new-rule process would benefit contributors

---

### ste-code/v2/data/vocabulary/README.md
- **Level:** 2
- **Summary:** Documents the vocabulary data directory structure, JSON entry schema, and a 5-step process for adding new terms across approved word lists and the synonym table.
- **Strengths:**
  - Clear file structure tree showing all vocabulary data files and the exceptions directory
  - Schema reference to `compute/schemas/vocabulary-entry.schema.json` for validation
  - Concrete 5-step process for adding new terms with specific file paths at each step
  - Domain tags table covering 5 domains with descriptions
  - States the single-source-of-truth principle: "These files are the only place where vocabulary is defined"
- **Gaps:**
  - No example vocabulary entry - the schema is referenced but never shown with actual data (what does a real entry look like with all required fields populated?)
  - No edge cases: term conflicts across domains, term deprecation/removal process, handling terms that exist in ASD-STE100 but aren't applicable to code
  - Process step 1 references `compute/prompts/vocabulary-review.prompt.md` - if this file doesn't exist, the process breaks; no fallback
  - No guidance on how domain tagging affects vocabulary loading or conflict resolution
  - No version history or changelog for vocabulary additions
- **What Level 3 Would Add:**
  - A full example vocabulary entry with all required and optional fields populated (e.g., a noun entry, a verb entry, an adjective entry)
  - Term lifecycle documentation: add → review → deprecate → remove
  - Cross-domain conflict policy: what happens when the same term has different approved meanings in different domains
  - Validation instructions: how to run the schema validator against vocabulary files
  - Reference integrity: confirm that the referenced schema file, prompt file, and synonym table all exist and are at adequate maturity
- **Priority:** medium - only Level 2 file in the batch; vocabulary is foundational to the entire STE-Code system and this README is the entry point for contributors

---

### ste-code/v2/README.md
- **Level:** 3
- **Summary:** Top-level architecture document for STE-Code v2. Defines the four-strata directory layout (core, data, compute, narratives), provides a 7-consumer loading strategy table, and lists 7 design principles.
- **Strengths:**
  - Full directory tree map with file-level granularity and concise descriptions
  - Loading strategy table covers 7 distinct consumers (LLMs at 3 window sizes, developers, humans, CI tools, agentic pipelines) - highly specific and actionable
  - 7 design principles clearly stated with one-line rationales
  - Version and source attribution (2.0.0-alpha, ASD-STE100 Issue 9, v1 commit hash)
  - Principle 6 ("Strata never cross-contaminate") is a strong architectural constraint that's testable
- **Gaps:**
  - No version history or changelog - what changed from v1 to v2 beyond architecture?
  - No known limitations or workarounds - what doesn't work yet in this alpha? Which files from the tree map are placeholders?
  - No quality gates or measurable criteria - how do you verify the strata aren't cross-contaminated? How do you validate that loading strategies produce correct results?
  - No meta-instructions for self-updating - if new strata are added or consumers change, how is this README kept in sync?
  - No cross-reference integrity check - do all referenced files actually exist? (e.g., `narratives/system-prompts/ste-code-full.md`, `compute/agentic/gate-conditions.json`)
  - Design principles are stated but not defended - no rationale for why these 7 were chosen or what alternatives were rejected
- **What Level 4 Would Add:**
  - Version changelog (v1 → v2 delta) and roadmap for beta/stable
  - File existence audit: a programmatic check that every file in the directory tree and loading strategy table actually exists on disk
  - Quality gates: measurable assertions for each design principle (e.g., "zero imports from core/ to data/")
  - Known limitations: what's alpha-quality, what's missing, what's planned
  - Rationale appendix: why 4 strata instead of 3 or 5, why these 7 principles, design alternatives considered
- **Priority:** low - strong architectural overview; gaps are documentation maturity polish, not structural defects

---

## Batch Summary
- Files scored: 6
- Level distribution: -2:0  -1:0  1:0  2:1  3:5  4:0  5:0
- Highest priority:
  - **ste-code/v2/data/vocabulary/README.md** (Level 2 - only sub-Level-3 file; vocabulary is foundational, missing examples and lifecycle docs)
  - **ste-code/v2/core/rules/rule-1.12.md** (Level 3 but missing detection query and related compute section - structural inconsistency with sibling rules)
- Pattern observations:
  - **Section inconsistency across rule files:** rule-1.1 has "Related Compute" and "Detection Query" sections; rule-1.11 has "Agent Note" but no "Related Compute"; rule-1.12 has neither. The rule file template isn't uniformly applied - consider defining a canonical rule file skeleton in `rules/README.md`.
  - **No rule file reaches Level 4:** all three rules are missing edge cases, failure recovery protocols, rationale, and performance considerations - the standard gap between Level 3 and 4. The rules are executable but not resilient.
  - **No file has a version history:** zero of 6 files include changelogs or modification dates - Level 5 is unreachable without this.
  - **Cross-reference integrity is assumed, not verified:** multiple files reference external artifacts (schemas, checklists, synonym tables, prompt files) but no file includes an assertion that those references resolve. A cross-reference linter would surface gaps.
  - **vocabulary/README.md is the quality floor:** at Level 2 it's one tier below the rest of the batch. As the entry point for vocabulary contribution, it should be Level 3 minimum - add example entries, term lifecycle docs, and conflict resolution policy.
