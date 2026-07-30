---
id: rule-1.1
section: 1
principle: P1
title: Use Approved Vocabulary Only
constraint-type: vocabulary
scope: [noun, verb, adjective, adverb]
severity: blocking
agentic-load: required
domain: [code]
related-rules: [rule-1.2, rule-1.3, rule-1.5, rule-1.6]
anti-patterns: [AP1, AP3]
synonym-table: true
---

# Rule 1.1 — Use Approved Vocabulary Only

## Statement

Use only terms approved in the STE-Code vocabulary. An approved term is any term listed in `data/vocabulary/` or belonging to one of the 19 technical noun categories or 4 technical verb categories defined in `core/categories/`.

## Code Domain Scope

Approved vocabulary includes: language keywords, framework names, tool names, package names, deployment targets, module and class names, algorithmic terms, route paths, data sizes, string literals, role names, UI terms, config files, error states, spec files, runtime conditions, terminal colors, bug types, and network protocols.

## Violation Pattern

```
❌ "fetch the data"         → fetch is not the approved verb (use read)
❌ "grab the config"        → grab is not approved (use read)
❌ "nuke the database"      → nuke is not approved (use delete)
❌ "yolo-deploy to prod"    → yolo-deploy is not an approved term
```

## Correct Pattern

```
✅ "read the data from the cache"
✅ "read the config file"
✅ "delete the database records"
✅ "deploy to production"
```

## Detection Query

```json
{ "check": "vocabulary", "action": "tokenize", "lookup": "data/vocabulary/", "flag": "not_found" }
```

## Related Compute

- `data/synonyms/synonym-table.json` — canonical replacement map
- `compute/checklists/pre-commit-checklist.json` → item `vocab-check`
- `compute/scoring/compliance-rubric.json` → P1 weight: 20
