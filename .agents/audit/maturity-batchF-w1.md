### SCE/narratives/system-prompts/ste-code-developer.md
- **Level:** 2
- **Summary:** Developer guide for extending the STE-Code standard - covers the four-stratum architecture, step-by-step procedures for adding domains/rules/vocabulary/prompts/rails, and a PR validation checklist.
- **Strengths:**
  - Clear architectural model (Four Strata) with a change-velocity table showing who changes what and when
  - Numbered step-by-step procedures for all five extension workflows
  - Cross-references to specific schema files and directory paths (e.g., `SCE/compute/schemas/vocabulary-entry.schema.json`)
  - Explicit narrative-generation principle ("Narratives are generated, not edited")
  - Validation checklist with 5 concrete items before PR
  - Versioned frontmatter (v2.0.0) with token budget
- **Gaps:**
  - No concrete examples of JSON entries, rule frontmatter, or prompt templates - procedures reference formats but never show them
  - No edge case guidance (e.g., what if a vocabulary term spans multiple domains? what if a rule conflicts with an existing synonym mapping?)
  - No failure recovery paths - what to do if validation fails, if schema rejects an entry, or if a narrative regeneration produces unexpected output
  - No rationale for design decisions (why four strata? why this directory layout? why `{{variable}}` templating over alternatives?)
  - Cross-references assume referenced files exist but provide no "if missing, create it" fallback for `README.md` files and some schema paths
  - No performance considerations for large domains (hundreds of terms, dozens of rules)
  - No version history or changelog
  - No known limitations or common pitfalls
  - No meta-instructions for self-improvement or self-audit
- **What Level 3 Would Add:** Concrete JSON/YAML examples for at least one vocabulary entry, one rule frontmatter, and one prompt template, embedded inline with the procedures. Cross-references to the actual schema files with brief summaries of what each schema enforces. At least one edge case documented per workflow (e.g., "If the term belongs to an existing category, skip step 2 justification"). A troubleshooting subsection covering the 3 most common validation failures and their fixes.
- **Priority:** medium

### SCE/narratives/system-prompts/ste-code-agentic.md
- **Level:** 2
- **Summary:** Behavioral constraint layer for STE-Code pipeline agents - defines 8 blocking/warning rails (R001-R008), 5 gate conditions (GATE-0 through GATE-4), and a worker contract with must/must-not clauses and a state block format.
- **Strengths:**
  - Clean, scannable structure with distinct sections for rails, gates, and contract
  - Each rail has a severity level (blocking vs. warning) and a concise one-sentence description
  - Gate conditions table links each gate to a pipeline stage and a concrete test
  - Worker contract clearly separates must/must-not with a specified state block format
  - Explicit scope boundary ("This file covers ONLY agent behavior - for vocabulary and rule content, load ste-code-micro.md or ste-code-full.md")
- **Gaps:**
  - No examples of rail violations vs. compliant behavior - rails are stated as imperatives without illustration
  - No cross-references to the pipeline files they govern (worker prompts, skill definitions, adaptation scripts)
  - No edge case handling (e.g., what if GATE-3 fails after 54 of 55 rule files are written? what if R001 and R002 conflict in a long-running task?)
  - No failure recovery guidance - gate failures have no documented remediation steps
  - No rationale for why these 8 rails were chosen or why some are warnings vs. blocking
  - Rails lack detection patterns - R001 says "never invent page numbers" but gives no regex or scan pattern an auditor agent could use
  - No performance considerations (e.g., R004 state-report-every-turn overhead on batch workers)
  - No version history or changelog
  - No known limitations (e.g., R007 sentence length is not machine-checkable without a validator)
- **What Level 3 Would Add:** A before/after example for at least 3 rails (one blocking, one warning, one involving the worker contract) showing a violation and its correction. Cross-references to the worker prompt files and skill definitions governed by these rails. A gate-failure recovery subsection with concrete actions per gate. Detection pattern examples (regex or grep strings) for R001, R005, and R006 so an auditor agent can mechanize checks.
- **Priority:** medium

### SCE/narratives/examples/example-readme-section.md
- **Level:** 1
- **Summary:** A single before/after example demonstrating STE-Code compliance for a README "Getting Started" section - shows a non-STE paragraph with 5 annotated violations and its compliant rewrite with 0 violations.
- **Strengths:**
  - Concrete, side-by-side non-STE/STE-Code pair with explicit violation annotations
  - Each violation tagged with the rule it breaks (P1, P10, P11) and a brief explanation
  - Compliance section verifies 0 violations and explains why each verb is approved
  - Clean markdown formatting with code blocks
  - Frontmatter identifies the document type and rules demonstrated
- **Gaps:**
  - Only ONE example pair - covers a single README section style with no variants
  - No edge cases or tricky scenarios (e.g., READMEs with mixed content types like API references, configuration tables, or troubleshooting sections)
  - No cross-references to the full rule definitions or the synonym table being invoked
  - No explanation of why specific rules were chosen - labels are applied without context on how to generalize
  - No guidance on how a developer should use this example for their own READMEs
  - No handling of different project types (library vs. CLI tool vs. web app READMEs)
  - No variants showing partial compliance (e.g., "this is better but still has 1 violation")
- **What Level 2 Would Add:** At least 2-3 additional example pairs covering different README section types (installation instructions, API usage examples, configuration tables). Cross-references to the specific rule definitions in the adapted rules directory. A brief usage note explaining how to apply the patterns shown. One edge case example where a judgment call is needed (e.g., a technical term that has no approved synonym).
- **Priority:** high

### SCE/narratives/examples/example-commit-message.md
- **Level:** 1
- **Summary:** A single before/after example demonstrating STE-Code compliance for a commit message - shows a non-STE commit message with 5 annotated violations and its compliant rewrite using conventional commit format with STE-Code verbs.
- **Strengths:**
  - Concrete, side-by-side non-STE/STE-Code pair with explicit violation annotations
  - Each violation tagged with the rule it breaks (P1, P4, P11) and a brief explanation
  - Compliant example integrates conventional commit format (`type(scope): description`) with STE-Code vocabulary
  - Multi-line commit body demonstrated with active voice
  - Frontmatter identifies the document type and rules demonstrated
- **Gaps:**
  - Only ONE example pair - covers a single `repair` commit type with no variants
  - No edge cases (merge commits, revert commits, commits with breaking changes, co-authored commits, commits with issue references)
  - No cross-references to the approved verb list or rule definitions being applied
  - No explanation of why specific rules were chosen - labels are applied without generalization context
  - No guidance on how a developer should apply STE-Code to their own commit workflow
  - No variants for other conventional commit types (`feat`, `docs`, `chore`, `perf`, `test`)
  - No handling of the interaction between conventional commit format constraints and STE-Code vocabulary constraints (e.g., what if the approved verb doesn't fit the conventional type?)
- **What Level 2 Would Add:** At least 3-4 additional example pairs covering different commit types (feat, docs, chore, revert) and edge cases (breaking change with BREAKING marker, merge commit, co-authored commit). Cross-references to the approved verb list and the specific rule files in the adapted rules directory. A brief usage note explaining how to integrate STE-Code commit linting into a pre-commit hook or CI pipeline.
- **Priority:** high

## Batch Summary
- Files scored: 4
- Level distribution: -2:0 -1:0 1:2 2:2 3:0 4:0 5:0
- Highest priority: `SCE/narratives/examples/example-readme-section.md`, `SCE/narratives/examples/example-commit-message.md` - both are single-example files with no depth, no cross-references, and no edge cases; they are the thinnest artifacts in the batch and block the narratives stratum from serving as effective teaching material
- Pattern observations: All 4 files share the same structural gaps - no edge case handling, no failure recovery paths, no version history, and no meta-instructions. The example files are uniformly Level 1 (single demonstration, no depth). The system prompts (developer + agentic) both land at Level 2 (functional procedures without concrete examples). None of the files cross-reference each other despite clear relationships: `ste-code-agentic.md` governs the agents that `ste-code-developer.md` instructs developers to extend, and the example files demonstrate rules that both system prompts reference. This isolation suggests the narratives were authored independently rather than as a cohesive stratum.
