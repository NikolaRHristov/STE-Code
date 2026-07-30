---
id: rule-adaptation
version: 1.0.0
variables: [source_domain, target_domain, rule_id, source_rule_text]
loads-from: [core/rules/{{rule_id}}.md, core/categories/]
output-format: adapted-rule-file
---

# STE-Code Rule Adaptation Prompt

> Use this prompt when extending STE-Code to a new domain (e.g., aerospace → medical, code → legal).

---

You are adapting **{{rule_id}}** from the **{{source_domain}}** domain to the **{{target_domain}}** domain.

Source rule text:
```
{{source_rule_text}}
```

## Your Task

1. Read the source rule. Identify the **invariant core** — the part that is domain-independent.
2. Identify the **domain-specific elements** — vocabulary, examples, categories.
3. Replace domain-specific elements with **{{target_domain}}** equivalents.
4. Preserve all constraint logic, severity, and principle mapping.
5. Add `{{target_domain}}`-specific violation patterns and correct patterns.
6. Output a complete rule file in the standard frontmatter + markdown format.

## Invariant Core (do not change)

- The principle number (P1–P14)
- The severity level
- The constraint-type
- The detection query structure

## Domain-Specific (adapt these)

- examples in violation/correct patterns
- category names and examples
- related compute references

## Output Format

Output a complete `core/rules/{{rule_id}}.md` file with YAML frontmatter, adapted for `{{target_domain}}`.
