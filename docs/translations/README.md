# Translations

STE-Code documentation is scaffolded for translation into 9 target languages.
Placeholders are blank files ready for content population.

## Target Locales

| Locale | Language | Script | RTL |
|--------|----------|--------|:---:|
| `zh-CN` | Chinese (Simplified) | Hans | No |
| `ja` | Japanese | Jpan | No |
| `ko` | Korean | Hang | No |
| `es` | Spanish | Latn | No |
| `fr` | French | Latn | No |
| `de` | German | Latn | No |
| `pt-BR` | Portuguese (Brazil) | Latn | No |
| `ru` | Russian | Cyrl | No |
| `ar` | Arabic | Arab | Yes |

## Architecture

Translation uses discovery-based scaffolding — workers explore source directories
and reason about translatability rather than following a fixed file grid. When
enrichment adds new files, the next discovery pass finds them automatically.

```
translations/
├── catalog.md              ← Auto-generated file inventory
├── zh-CN/
│   ├── ste-code/artifacts/
│   ├── ste-code/adapted/
│   ├── SCE/narratives/
│   └── ste-code-v2/
├── ja/  (same structure)
├── ko/  (same structure)
... etc for all 9 locales
```

## Placeholders

Placeholders are fully blank (zero-byte) files at the correct path. The path
itself encodes the locale and source. The catalog (`translations/catalog.md`)
tracks what exists and where it came from.

## Discovery Targets

Workers explore 10 source directories:

1. `ste-code/artifacts/` — 6 deployable files
2. `ste-code/adapted/` — 57 adapted rule files
3. `SCE/narratives/system-prompts/` — 4 system prompts
4. `SCE/narratives/examples/` — Example README + commit message
5. `SCE/core/rules/` — Rule files (growing)
6. `ste-code/v2/narratives/system-prompts/` — 4 v2 prompts
7. `ste-code/v2/narratives/examples/` — v2 examples
8. `ste-code/v2/core/rules/` — v2 rule files
9. `SCE/compute/prompts/` — Agent-facing compute prompts
10. `ste-code/v2/compute/prompts/` — v2 compute prompts

## What Gets Skipped

- JSON schemas (structural, not translatable)
- Python scripts (not user-facing)
- Generated JSON data (translate definitions only)
- Configuration contracts (worker-contract.json, rails.json, gate-conditions.json)

## Re-Discovery

After any enrichment session adds files, re-run discovery. Workers skip files
that already have placeholders and find only net-new content.

## Launch

```bash
hermes -z "$(cat .agents/agent/agent-9-translations.md)" -m deepseek-v4-pro
```
