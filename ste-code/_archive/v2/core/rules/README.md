# STE-Code Core Rules

Each file in this directory contains one rule from ASD-STE100 Issue 9 (September 2025), adapted to the code domain.

## File Format

Every rule file uses the following YAML frontmatter:

```yaml
---
id: rule-1.1
section: 1
principle: P1
title: Use Approved Vocabulary Only
constraint-type: vocabulary        # vocabulary | grammar | structure | safety | agentic
scope: [noun, verb, adjective]      # which POS this rule applies to
severity: blocking                  # blocking | warning | advisory
agentic-load: required              # required | optional | conditional
domain: [code]                      # domains this rule applies to
related-rules: [rule-1.2, rule-1.3] # cross-references
anti-patterns: [AP1, AP2]           # which anti-patterns this rule guards
---
```

## Severity Levels

| Level | Meaning | CI Behaviour |
|-------|---------|-------------|
| `blocking` | Violation must be fixed before commit | CI fails |
| `warning` | Violation should be fixed, not required | CI warns |
| `advisory` | Suggestion for improvement | CI info only |

## Constraint Types

| Type | Description |
|------|-------------|
| `vocabulary` | Controls what words/terms are allowed |
| `grammar` | Controls sentence structure and voice |
| `structure` | Controls document layout and formatting |
| `safety` | Controls BREAKING/DEPRECATED/NOTE usage |
| `agentic` | Controls agent behavior in pipeline context |

## Loading by Agent

An agent performing a vocabulary-only check loads only `constraint-type: vocabulary` rules.  
An agent running a full compliance check loads all rules where `agentic-load: required`.
