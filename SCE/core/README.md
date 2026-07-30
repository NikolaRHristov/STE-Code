# Stratum 1 — Static Core

Immutable rule definitions derived directly from ASD-STE100 Issue 9 (January 2025). Change only when the spec changes.

## Contents

- `rules/` — One file per rule (rule-1.1.md through rule-9.4.md + gr-1.md through gr-4.md)
- `categories/noun-categories.json` — 19 technical noun categories (machine-readable)
- `categories/verb-categories.json` — 4 technical verb categories
- `categories/synonym-table.json` — Canonical synonym table (12 preferred/avoided pairs)

## 14 Principles (P1-P14)

| P# | Rule | Type |
|----|------|------|
| P1 | Approved words only | Vocabulary |
| P2 | Words as specified part of speech | Grammar |
| P3 | Words with approved meanings only | Semantics |
| P4 | Active voice; imperative for instructions | Style |
| P5 | Technical code nouns allowed | Domain |
| P6 | Non-approved words only as technical nouns | Domain |
| P7 | No technical nouns as verbs | Grammar |
| P8 | Standard, well-known technical nouns | Style |
| P9 | Short, clear technical nouns | Style |
| P10 | No slang, jargon, or regional terms | Vocabulary |
| P11 | One term per concept | Consistency |
| P12 | Technical verbs allowed (build, deploy, test, lint) | Domain |
| P13 | No technical verbs as nouns | Grammar |
| P14 | American English spelling | Orthography |

## Frontmatter Schema

Every rule file MUST have valid YAML frontmatter:

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
