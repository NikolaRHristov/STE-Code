---
id: rule-adaptation
version: 1.0.0
variables: [source_rule_id, source_domain, target_domain, source_text]
---

# STE-Code Rule Adaptation

You are adapting an existing STE-Code rule from one domain to another.

## Context
- Source rule: `{{source_rule_id}}`
- Source domain: `{{source_domain}}`
- Target domain: `{{target_domain}}`

## Source Rule Text

```
{{source_text}}
```

## Instructions

1. READ the source rule and identify its core constraint (what it restricts and why).
2. IDENTIFY which parts are domain-specific (vocabulary, examples) vs universal (the structural constraint).
3. REPLACE domain-specific vocabulary with equivalent terms from the target domain.
4. GENERATE 3 non-STE / STE example pairs for the target domain.
5. VERIFY the adapted rule still satisfies the same structural constraint as the original.
6. OUTPUT the adapted rule file with valid frontmatter conforming to `SCE/compute/schemas/rule-frontmatter.schema.json`.

## Output Format

```markdown
---
id: {{source_rule_id}}
section: [section number]
principle: [principle ID]
constraint-type: [type]
scope: [scopes]
severity: [severity]
agentic-load: [load]
domain: ["{{target_domain}}"]
---

# Rule [ID] — [Title]

[rule body with adapted examples]
```
