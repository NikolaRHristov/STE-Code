---
description: "Translation orchestration — set up multi-locale placeholder structure for STE-Code documentation using parallel hermes -z workers. Placeholders only, no translation content yet."
version: "1.0.0"
related: [".agents/references/translation-grid.md", ".agents/references/worker-rails.md", ".agents/agent/agent-9-translations.md"]
---

# Translation Orchestration

Set up a multi-language translation pipeline for STE-Code documentation into 9 target developer languages. This skill handles infrastructure setup and placeholder population — actual translation content comes later.

## Target Locales (9)

| Locale | Language | Script | RTL |
|--------|----------|--------|-----|
| `zh-CN` | Chinese (Simplified) | Hans | No |
| `ja` | Japanese | Jpan | No |
| `ko` | Korean | Hang | No |
| `es` | Spanish | Latn | No |
| `fr` | French | Latn | No |
| `de` | German | Latn | No |
| `pt-BR` | Portuguese (Brazil) | Latn | No |
| `ru` | Russian | Cyrl | No |
| `ar` | Arabic | Arab | Yes |

## Directory Layout

Each locale gets a mirror of the STE-Code source structure:

```
translations/<locale>/
├── README.md                    # Locale metadata + status
├── artifacts/                   # 6 artifact files
├── adapted/                     # 57 adapted rule files
├── rules/                       # SCE core/rules/ mirror
├── dictionary/                  # JSON vocabulary files
└── system-prompts/              # SCE system prompts
```

## Placeholder Format

Every placeholder file starts with a YAML frontmatter metadata block:

```yaml
---
locale: <ISO-639-1>
language: <Language Name>
script: <Script Code>
rtl: <true|false>
source: ste-code/<original-path>
status: placeholder
translated: false
last_updated: null
---
```

Followed by the placeholder body:

```
[TRANSLATION PENDING — placeholder only]
```

## Worker Protocol

Same batch-of-3 pattern as other pipeline agents:

```bash
hermes -z "$(cat .agents/prompts/translations/trNNN-prompt.txt)" -m deepseek-v4-pro --yolo
```

**Rules:**
- Always write prompt to file, pass via `$(cat file)` — never embed multi-line in shell
- 3 workers per batch, background + notify_on_complete=true
- Verify after each batch: file exists, metadata header present, placeholder marker present
- Commit after each batch: `git gcommit-hermes "translations: Batch N — <locale>"`

## Quality Checks (Per Batch)

1. Output file exists: `test -f translations/<locale>/<path>`
2. Non-empty: `wc -c` > 0
3. Metadata header present: contains `locale:` in first 5 lines
4. Placeholder marker: contains `[TRANSLATION PENDING — placeholder only]`
5. No premature translation: does NOT contain translated STE-Code rule text

## Phase Plan

1. **Infrastructure** — directories, READMEs, references, this skill
2. **Placeholders** — ~540 empty files across 9 locales (~81 workers, ~27 batches)
3. **Translation** (future) — actual content by locale-specific translation workers

## Progress Tracking

File: `.agents/state/TRANSLATIONS-PROGRESS.md`

After each batch, update with: batch number, locale, worker IDs, files written, next actions. Never let tracking fall behind — the auditor cross-references against disk.

## Communication

Signal phase completions in `.agents/feedback/exchange.md`:
```markdown
## Agent #9 (Translation Orchestrator) → All Agents — YYYY-MM-DD
- Phase 1 complete: directories, READMEs, references
- Phase 2 started: N/540 placeholder files (X%)
```

## Key Facts

- 9 locales, ~60 files each, ~540 total placeholders
- Placeholder only — no translation content
- deepseek-v4-pro exclusively
- Batch size: 3, commit per batch
- Source: STE-Code pipeline output (ste-code/*, SCE/*)
