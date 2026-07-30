---
id: rule-1.11
section: 1
principle: P11
title: One Term Per Concept
constraint-type: vocabulary
scope: [noun]
severity: blocking
agentic-load: required
domain: [code]
related-rules: [rule-1.1, rule-1.3]
anti-patterns: [AP6]
synonym-table: false
---

# Rule 1.11 — One Term Per Concept

## Statement

Use exactly one technical noun for each concept throughout a document. Do not alternate between synonymous terms for the same component, service, or entity.

## Violation Pattern

```
❌ Alternating: "auth service" / "authentication module" / "login handler" (same component)
❌ Alternating: "user store" / "user repository" / "user DB" (same data layer)
❌ Alternating: "CI pipeline" / "build system" / "automation" (same tool)
```

## Correct Pattern

```
✅ Choose one: "AuthService" — use it throughout
✅ Choose one: "UserRepository" — use it throughout
✅ Choose one: "CI pipeline" — use it throughout
```

## Detection Query

```json
{ "check": "term-consistency", "action": "group-by-concept", "flag": "synonym-drift" }
```

## Agent Note

This rule requires document-level memory — the agent must track all technical nouns seen so far and flag when a new term appears to refer to an already-named concept.
