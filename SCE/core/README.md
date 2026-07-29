# Stratum 1 — Static Core

Immutable rule definitions derived directly from ASD-STE100 Issue 9. Change only when the spec changes.

## Contents

- `rules/` — One file per rule (rule-1.1.md through rule-9.4.md + gr-1.md through gr-4.md)
- `categories/noun-categories.json` — 19 technical noun categories (machine-readable)
- `categories/verb-categories.json` — 4 technical verb categories
- `categories/synonym-table.json` — Canonical synonym map

## Frontmatter Schema

Every rule file MUST have valid YAML frontmatter conforming to `../../compute/schemas/rule-frontmatter.schema.json`.

```yaml
---
id: rule-1.1
section: 1
principle: P1
constraint-type: vocabulary
scope: [noun, verb, adjective]
severity: blocking
agentic-load: required
---
```

### `severity` values
- `blocking` — Violation must be corrected before output
- `warning` — Violation must be flagged
- `advisory` — Violation should be noted

### `agentic-load` values
- `required` — Always load in agentic context
- `optional` — Load only when relevant to document type
- `conditional` — Load based on domain tag
