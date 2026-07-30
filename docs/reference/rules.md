# Rule Reference

53 writing rules + 4 grammar rules adapted from ASD-STE100 Issue 9.

**Source files:** `ste-code/adapted/a-secN-ruleX.Y.md` (57 files)
**Master reference:** `ste-code/merged/master.md` (20,794 lines)
**SCE frontmatter:** `SCE/core/rules/rule-X.Y.md`

## Sections

| Section | Rules | Topic | Severity |
|---------|-------|-------|----------|
| 1 | 1.1–1.14 | Words — vocabulary, parts of speech, technical nouns, consistency | Blocking |
| 2 | 2.1–2.2 | Sentence structure — length, clarity | Warning |
| 3 | 3.1–3.7 | Verbs — forms, tenses, voice | Blocking |
| 4 | 4.1–4.5 | Adjectives and adverbs — approved forms | Warning |
| 5 | 5.1–5.5 | Technical nouns — keywords, frameworks, tools | Blocking |
| 6 | 6.1–6.5 | Non-approved words — exception rules | Advisory |
| 7 | 7.1–7.3 | Noun clusters — maximum depth, clarity | Blocking |
| 8 | 8.1–8.6 | Procedural writing — instructions, warnings | Advisory |
| 9 | 9.1–9.4 | Grammar — articles, prepositions, conjunctions | Advisory |
| GR | GR1–GR4 | General grammar — punctuation, capitalization | Warning |

## File Format

Each adapted rule file contains:
```markdown
# Rule X.Y — <Title>

## Original STE Rule
[Original aerospace rule text from ASD-STE100]

## Code-Domain Adaptation
[Rule rewritten for code documentation context]

## Examples

> **STE:** [Code documentation example following the rule]

> **Non-STE:** [Code documentation example violating the rule]
```

## Frontmatter

SCE rule files add YAML frontmatter:
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
