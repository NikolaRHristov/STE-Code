# STE-Code — Developer Guide

> You are extending, adapting, or building tooling for the STE-Code standard. This guide explains how the standard is structured and how to change it correctly.

---

## Architecture Overview

STE-Code v2 is a four-stratum system. Each stratum has a single responsibility and must not cross-contaminate with others.

```
core/         Immutable rules. Change only when the spec changes.
data/         Living vocabulary. Add terms here without touching rules.
compute/      Logic layer. Checklists, schemas, scoring, agentic rails, prompt templates.
narratives/   Assembled outputs. Generated from the other strata. Never hand-authored.
```

---

## How to Add a New Rule

1. Create `core/rules/rule-N.N.md` using the frontmatter schema in `compute/schemas/rule-frontmatter.schema.json`.
2. Validate the frontmatter against the schema before committing.
3. Add the principle to `compute/scoring/compliance-rubric.json` with a weight (weights must sum to 100).
4. If the rule introduces new anti-patterns, add them to `compute/checklists/pre-commit-checklist.json`.
5. Update the narrative files that reference principle counts (e.g., "14 core principles").

## How to Add New Vocabulary

1. Run `compute/prompts/vocabulary-review.prompt.md` to classify the new terms.
2. Add approved terms to the correct file in `data/vocabulary/`.
3. Add non-STE synonyms to `data/synonyms/synonym-table.json`.
4. Tag every entry with a `domain` array.
5. Do not modify `core/rules/` for vocabulary additions.

## How to Adapt to a New Domain

1. Run `compute/prompts/rule-adaptation.prompt.md` for each rule, with `target_domain` set to your new domain.
2. Adapted rules go in a new `core/rules/domains/{{domain}}/` subdirectory.
3. Domain vocabulary goes in `data/vocabulary/` with a new domain tag.
4. Add a new narrative file `narratives/system-prompts/ste-code-{{domain}}-full.md` assembled from the adapted rules.
5. Do not modify the code-domain rules.

## How to Update the Agentic Rails

1. Edit `compute/agentic/rails.json` directly.
2. Rails changes require a gate bump — update `compute/agentic/gate-conditions.json` if any gate assertions change.
3. Update `narratives/system-prompts/ste-code-agentic.md` to reflect the new rail table.
4. Never embed rails logic inside content rules (`core/rules/`).

## How to Add a Prompt Template

1. Create `compute/prompts/{{name}}.prompt.md`.
2. Use `{{variable}}` slots for all runtime-determined values.
3. Declare all variables in the frontmatter `variables:` list.
4. Declare all data files the template loads in the `loads-from:` list.
5. Prompt templates must be parameterized — never hardcode domain, document type, or rule subset.

## Schema Validation

Every JSON file in `data/` and `compute/` has a corresponding `$schema` reference. Run schema validation in CI:

```bash
npx ajv validate -s compute/schemas/rule-frontmatter.schema.json -d core/rules/*.md
npx ajv validate -s compute/schemas/synonym-table.schema.json -d data/synonyms/synonym-table.json
npx ajv validate -s compute/schemas/vocabulary-entry.schema.json -d data/vocabulary/**/*.json
```

## Stratum Isolation Rules

- `core/` never imports from `data/` (rules are domain-agnostic structurally)
- `data/` never imports from `core/` or `compute/`
- `compute/` reads from both `core/` and `data/`, never from `narratives/`
- `narratives/` is assembled from all other strata — treat it as a build artifact
- All cross-references use relative paths from the repo root
