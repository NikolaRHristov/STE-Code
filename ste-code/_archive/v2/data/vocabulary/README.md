# STE-Code Vocabulary Data

This directory contains the living vocabulary for all STE-Code domains. These files are the only place where vocabulary is defined. Rules in `core/rules/` reference these files but do not duplicate their content.

## File Structure

```
vocabulary/
  approved-nouns.json       — all approved nouns, tagged by domain and category
  approved-verbs.json       — all approved verbs, tagged by domain and category
  approved-adjectives.json  — all approved adjectives
  approved-prepositions.json — all approved prepositions
exceptions/
  domain-extensions.json    — organization-specific approved additions
```

## Schema

Every entry must conform to `compute/schemas/vocabulary-entry.schema.json`.

Required fields: `term`, `type`, `category-id`, `domain`, `severity`
Optional fields: `note`, `added-by`, `added-date`

## Adding New Terms

1. Run `compute/prompts/vocabulary-review.prompt.md` to classify the new terms.
2. Add approved terms to the correct file with all required fields.
3. Tag with the correct `domain` array — never add a term without a domain.
4. Add corresponding non-STE synonyms to `data/synonyms/synonym-table.json`.
5. Submit a PR for review.

## Domain Tags

| Tag | Description |
|-----|-------------|
| `code` | Software development documentation |
| `aerospace` | Aircraft maintenance documentation (original STE domain) |
| `medical` | Medical device documentation |
| `legal` | Legal and compliance documentation |
| `finance` | Financial system documentation |
