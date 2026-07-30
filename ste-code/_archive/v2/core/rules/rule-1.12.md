---
id: rule-1.12
section: 1
principle: P12
title: Technical Verbs Must Belong to a Category
constraint-type: vocabulary
scope: [verb]
severity: blocking
agentic-load: required
domain: [code]
related-rules: [rule-1.7, rule-1.13]
anti-patterns: [AP2]
synonym-table: true
---

# Rule 1.12 — Technical Verbs Must Belong to a Category

## Statement

Every technical verb must belong to one of the 4 STE-Code verb categories: development operations, data operations, application operations, or communication operations.

## The 4 Verb Categories (Summary)

| Category | Key Verbs |
|----------|-----------|
| Development Operations | build, compile, test, lint, deploy, rollback, run, start, stop |
| Data Operations | read, write, parse, query, insert, migrate, cache, serialize |
| Application Operations | handle, route, authenticate, authorize, validate, render, dispatch |
| Communication Operations | send, receive, publish, subscribe, stream, connect, broadcast |

Full lists: `core/categories/verb-categories.json`

## Violation Pattern

```
❌ "do the migration"     → do is not in any verb category (use run)
❌ "perform the build"    → perform is not approved (use run)
❌ "execute the query"    → execute is not approved for data ops (use query)
```

## Correct Pattern

```
✅ "run the migration"
✅ "run the build"
✅ "query the database"
```
