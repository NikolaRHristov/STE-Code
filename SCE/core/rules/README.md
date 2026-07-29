# SCE Core Rules

This directory contains one file per STE-Code rule, adapted to the code domain.

## Source

All rules are derived from `ste-code/adapted/` (the pipeline Stage 4 output) with structured YAML frontmatter added.

## File Naming

```
rule-{section}.{number}.md    e.g. rule-1.1.md, rule-9.4.md
gr-{number}.md                e.g. gr-1.md, gr-4.md
```

## Frontmatter

Every file must have valid YAML frontmatter conforming to `../../compute/schemas/rule-frontmatter.schema.json`.

## Loading by Severity

- **blocking rules only** (fast compliance check): filter `severity: blocking`
- **agentic-required rules** (pipeline agents): filter `agentic-load: required`
- **full standard** (developer / audit): load all files

## Rule Index

| Rule | Principle | Constraint | Severity | Agentic |
|------|-----------|------------|----------|---------|
| rule-1.1 | P1 | vocabulary | blocking | required |
| rule-1.2 | P2 | vocabulary | blocking | required |
| rule-1.3 | P3 | vocabulary | blocking | required |
| rule-1.4 | P4 | grammar | blocking | required |
| rule-1.5 | P5 | vocabulary | blocking | optional |
| rule-1.6 | P6 | vocabulary | warning | optional |
| rule-1.7 | P7 | grammar | blocking | required |
| rule-1.8 | P8 | vocabulary | advisory | optional |
| rule-1.9 | P9 | vocabulary | advisory | optional |
| rule-1.10 | P10 | vocabulary | blocking | required |
| rule-1.11 | P11 | vocabulary | blocking | required |
| rule-1.12 | P12 | vocabulary | blocking | required |
| rule-1.13 | P13 | grammar | blocking | required |
| rule-1.14 | P14 | format | advisory | optional |
| rule-2.1 | P15 | grammar | warning | optional |
| rule-2.2 | P16 | grammar | warning | optional |
| rule-3.1 | P17 | grammar | blocking | required |
| rule-3.2 | P18 | grammar | blocking | required |
| rule-3.3 | P19 | grammar | blocking | required |
| rule-3.4 | P20 | grammar | warning | optional |
| rule-3.5 | P21 | grammar | warning | optional |
| rule-3.6 | P22 | grammar | advisory | optional |
| rule-3.7 | P23 | grammar | advisory | optional |
| rule-4.1 | P24 | structure | blocking | required |
| rule-4.2 | P25 | structure | blocking | required |
| rule-4.3 | P26 | structure | blocking | required |
| rule-4.4 | P27 | safety | blocking | required |
| rule-4.5 | P28 | structure | warning | optional |
| rule-5.1 | P29 | structure | blocking | required |
| rule-5.2 | P30 | structure | warning | optional |
| rule-5.3 | P31 | structure | warning | optional |
| rule-5.4 | P32 | structure | advisory | optional |
| rule-5.5 | P33 | structure | advisory | optional |
| rule-6.1 | P34 | safety | blocking | required |
| rule-6.2 | P35 | safety | blocking | required |
| rule-6.3 | P36 | safety | blocking | required |
| rule-6.4 | P37 | safety | blocking | required |
| rule-6.5 | P38 | safety | blocking | required |
| rule-7.1 | P39 | format | advisory | optional |
| rule-7.2 | P40 | format | advisory | optional |
| rule-7.3 | P41 | format | advisory | optional |
| rule-8.1 | P42 | format | warning | optional |
| rule-8.2 | P43 | format | warning | optional |
| rule-8.3 | P44 | format | warning | optional |
| rule-8.4 | P45 | format | warning | optional |
| rule-8.5 | P46 | format | advisory | optional |
| rule-8.6 | P47 | format | advisory | optional |
| rule-9.1 | P48 | agentic | blocking | required |
| rule-9.2 | P49 | agentic | blocking | required |
| rule-9.3 | P50 | agentic | blocking | required |
| rule-9.4 | P51 | agentic | blocking | required |
| gr-1 | GR1 | agentic | blocking | required |
| gr-2 | GR2 | agentic | blocking | required |
| gr-3 | GR3 | agentic | blocking | required |
| gr-4 | GR4 | agentic | blocking | required |
