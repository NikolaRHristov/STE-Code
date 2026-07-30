---
id: ste-code-developer
version: 2.0.0
tokens: ~2000
use-when: extending the standard, adding domain support, building tooling
source: Adapted from ASD-STE100 Issue 9 (January 2025), ASD Europe, Brussels. © ASD, 2025. STE is EU Trade Mark 017966390. Independent adaptation not endorsed by ASD. asd-ste100.org
---

# STE-Code Developer Guide

This guide is for developers who extend the STE-Code standard itself — adding new domains, new vocabulary, new rules, or building tooling on top of the SCE architecture.

---

## The Four Strata

The SCE architecture separates concerns into four strata. Each stratum has a different change velocity and a different audience.

| Stratum | Changes When | Changed By |
|---------|-------------|------------|
| `core/` | Spec updates (rare) | Standard maintainers only |
| `data/` | Domain expansion, org needs | Domain leads, contributors |
| `compute/` | Tooling improvements, new validators | Engineers |
| `narratives/` | Regenerated from strata 1–3 | Automated pipeline |

**Narratives are generated, not edited.** If you need to change a narrative file, change the source stratum and regenerate.

---

## Adding a New Domain

To adapt STE-Code to a new domain (e.g. `aerospace`, `medical`, `legal`):

1. **Add noun categories** — create a new entry in `SCE/core/categories/noun-categories.json` with `"domain": ["your-domain"]`.
2. **Add approved terms** — create `SCE/data/vocabulary/domain-extensions.json` entries tagged with your domain.
3. **Adapt rules** — use `SCE/compute/prompts/rule-adaptation.prompt.md` with `target_domain: your-domain`.
4. **Generate narratives** — run the compliance check prompt with the new domain slice to produce `ste-code-{domain}.md` in `SCE/narratives/system-prompts/`.
5. **Validate** — run all entries through `SCE/compute/schemas/vocabulary-entry.schema.json`.

---

## Adding a New Rule

1. Create `SCE/core/rules/rule-{section}.{number}.md`.
2. Add valid YAML frontmatter conforming to `SCE/compute/schemas/rule-frontmatter.schema.json`.
3. Add 3 non-STE/STE example pairs with explicit spec justifications.
4. Update `SCE/core/rules/README.md` rule index.
5. If the rule adds vocabulary, update `SCE/data/vocabulary/approved-verbs.json` or `approved-adjectives.json`.
6. If the rule adds synonyms, update `SCE/core/categories/synonym-table.json`.

---

## Adding a New Vocabulary Term

1. Identify the correct stratum: base standard terms go in `SCE/data/vocabulary/`. Org-specific terms go in `SCE/data/vocabulary/domain-extensions.json`.
2. Confirm the term belongs to an existing category (noun categories 1–19, verb categories 1–4) or justify a new category.
3. Add the entry conforming to `SCE/compute/schemas/vocabulary-entry.schema.json`.
4. Add the canonical synonym mapping to `SCE/core/categories/synonym-table.json` if the term replaces existing non-STE terms.
5. Open a PR against `Current` with a clear rationale in the commit message.

---

## Adding a New Prompt Template

1. Create `SCE/compute/prompts/{name}.prompt.md`.
2. Add frontmatter: `id`, `version`, `variables` (list all `{{variable}}` slots).
3. Use only `{{variable}}` syntax for slots — no other templating format.
4. Document the prompt in `SCE/compute/prompts/README.md` (create if missing).

---

## Agentic Rail Extensions

To add a new behavioral rail:

1. Add an entry to `SCE/compute/agentic/rails.json` with a new `id` (R009+).
2. Set `severity`: `blocking` for must-not violations, `warning` for should-not.
3. Add `detection` patterns — specific strings or patterns an auditor agent can scan for.
4. Update `SCE/narratives/system-prompts/ste-code-agentic.md` to include the new rail summary.

---

## Validation

Before opening a PR, confirm:

- [ ] All rule frontmatter validates against `rule-frontmatter.schema.json`
- [ ] All vocabulary entries validate against `vocabulary-entry.schema.json`
- [ ] All synonym table entries have both `non-ste` array and `approved` string
- [ ] No narrative files were edited directly (regenerate from strata instead)
- [ ] Commit message follows `<type>(<scope>): <description>` format
