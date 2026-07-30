# Translations — Phase E

9 locales. ~540 target files. Scaffolding created. Population pending.

## Locales

| Code | Language | Status |
|------|----------|:------:|
| bg | Bulgarian | ⬜ |
| de | German | ⬜ |
| es | Spanish | ⬜ |
| fr | French | ⬜ |
| it | Italian | ⬜ |
| ja | Japanese | ⬜ |
| pl | Polish | ⬜ |
| pt-BR | Portuguese (Brazil) | ⬜ |
| uk | Ukrainian | ⬜ |
| zh-CN | Chinese (Simplified) | ⬜ |

## Directory Structure

```
translations/{locale}/
├── artifacts/         ← 4 level system prompts
├── templates/         ← 4 STE-Code templates
├── data/vocabulary/   ← approved and unapproved words
└── rules/             ← 51 rule summaries
```

## Translatable Content (~60 files per locale)

1. System prompts (4 files): Level 1 through Level 4
2. Templates (4 files): micro, full, agentic, developer
3. Vocabulary (4 files): approved verbs, approved adjectives, unapproved entries, code dictionary
4. Rules (51 files): One summary per rule

## Process

Each locale uses 3 discovery-based workers that scan source directories, create blank placeholder files with source references, and record progress in locale-specific state files.

Total: 10 locales × 3 workers = 30 workers.
