# Schemas

JSON schemas for validating pipeline output.

**Location:** `ste-code/v2/compute/schemas/` (authoritative), `SCE/compute/schemas/` (populated during Phase C)

| Schema | Validates |
|--------|----------|
| `rule-frontmatter.schema.json` | YAML frontmatter in rule files |
| `vocabulary-entry.schema.json` | Dictionary entry format |
| `synonym-table.schema.json` | Synonym pair format |
| `worker-contract.json` | Worker behavioral contract |
| `rails.json` | 8 behavioral guardrails |
| `gate-conditions.json` | Stage transition gates |
| `anti-fabrication.json` | Fabrication detection rules |
| `violation-severity-map.json` | Severity weighting for violations |
| `compliance-rubric.json` | Scoring rubric for compliance checks |
