# Translations — Phase E (pending)

**9 locales, ~540 target files. Scaffolding created. Population pending.**

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

Each locale mirrors the source structure:

```
translations/{locale}/
├── artifacts/         ← 6 system prompt templates
├── templates/         ← 4 STE-Code templates
├── data/vocabulary/   ← approved/unapproved words
└── rules/             ← 51 rule summaries
```

## Translatable Content (~60 files per locale)

1. **Artifacts (6 files):** distilled-prompt, self-reading-manual, methodology, example-turn, deployment-guide, README
2. **Templates (4 files):** micro, full, agentic, developer
3. **Vocabulary (4 files):** approved-verbs, approved-adjectives, unapproved-entries, code-dictionary
4. **Rules (51 files):** One summary per rule (rule title + key examples)

## Process (Phase E Workers)

Each locale: 3 discovery-based workers that:
1. Scan source directories for translatable files
2. Create blank placeholder files with source reference
3. Record progress in locale-specific state files

Total: 10 batches × 3 workers = 30 workers.
