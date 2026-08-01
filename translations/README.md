# Translations — Phase E

10 locales. Directory scaffolding created; no content files exist yet. Each
locale currently holds only `.gitkeep` placeholders.

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
├── artifacts/         ← level system prompts
├── templates/         ← STE-Code templates
├── data/vocabulary/   ← approved and unapproved words
└── rules/             ← one summary per rule (54 rules + 4 GR)
```

## Translatable content per locale (planned)

1. System prompts: one per artifact tier (levels -2 to 5)
2. Templates: micro, full, agentic, developer
3. Vocabulary (4 files): approved verbs, approved adjectives, unapproved entries, code dictionary
4. Rules: 58 summaries (54 rules + 4 General Rules)

## Process

Each locale uses 3 discovery-based workers that scan source directories, create blank placeholder files with source references, and record progress in locale-specific state files.

Total: 10 locales × 3 workers = 30 workers.
