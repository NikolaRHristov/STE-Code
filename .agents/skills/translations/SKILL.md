---
description: "Translation discovery + scaffolding — explore pipeline output, reason about translatability, create fully blank placeholders across 9 locales. Discovery-based, not fixed-grid. Re-scans find new enrichment automatically."
version: "2.0.0"
related: [".agents/references/translation-grid.md", ".agents/references/worker-rails.md", ".agents/agent/agent-9-translations.md"]
---

# Translation Discovery + Scaffolding

Set up a multi-locale translation pipeline by **discovering** translatable content, not following a fixed inventory. Workers explore source directories, reason about what's worth translating, and create fully blank placeholder files at the correct paths for all 9 target locales.

**Why discovery:** Enrichment is ad-hoc across sessions — new words, rules, categories, and examples get added at different times by different agents. A fixed file grid rots immediately. Discovery workers find whatever is on disk right now. Re-run after enrichment to catch new files.

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

## Placeholder Format

**Fully blank.** No YAML frontmatter, no metadata headers, no placeholder text, no locale markers. Just an empty file at the correct path:

```
translations/<locale>/<source-relative-path>/<filename>
```

The path itself carries the information:
- `<locale>` tells you the target language
- `<source-relative-path>` mirrors the original source directory
- `<filename>` matches the source filename

The catalog (`translations/catalog.md`) tracks what exists and where it came from.

## What's Translatable?

Workers reason about each file:

| Include | Skip |
|---------|------|
| `.md` rule files (adapted rules, core rules) | `.schema.json` (JSON schemas) |
| `.txt` system prompts and artifacts | `.py` scripts |
| `.md` README files | Config files (`.json` without prose) |
| `.md` narrative examples | Generated `.json` data (nouns-batch-*.json, verbs-batch-*.json — unless they contain descriptive definitions) |
| `.md` narrative system prompts | `worker-contract.json`, `rails.json`, `gate-conditions.json` |
| `.json` vocabulary files (approved-verbs.json, approved-adjectives.json, synonym-table.json) — translate definitions | Scoring/compliance `.json` |
| `.prompt.md` compute prompts | |

**Reasoning rule of thumb:** If a human developer would read this file and extract meaning from the words, it's translatable. If it's purely structural (schema, config, generated data), skip it.

## Worker Protocol

Batch of 3 workers, each handling 3 locales:

```bash
hermes -z "$(cat .agents/prompts/translations/discovery-NNN-prompt.txt)" -m deepseek-v4-pro --yolo
```

**Worker task:**
1. List all files in the assigned discovery target directory
2. For each file, reason: translatable or not? (include reasoning in report)
3. For each translatable file, create a blank placeholder at `translations/<locale>/<source-relative>/<filename>` for all 3 assigned locales
4. Report discoveries (list every file, decision, created paths)

**Per batch:**
- Worker 1: locales zh-CN, ja, ko
- Worker 2: locales es, fr, de
- Worker 3: locales pt-BR, ru, ar

All 3 workers discover the same source directory but create placeholders for different locale subsets.

## Discovery Targets (10)

In priority order:

| # | Source Directory | Expected Size |
|---|-----------------|:---:|
| 1 | `ste-code/artifacts/` | 6 files |
| 2 | `ste-code/adapted/` | 57 files |
| 3 | `SCE/narratives/system-prompts/` | 4 files |
| 4 | `SCE/narratives/examples/` | 2 files |
| 5 | `SCE/core/rules/` | growing (1+ files) |
| 6 | `ste-code/v2/narratives/system-prompts/` | 4 files |
| 7 | `ste-code/v2/narratives/examples/` | 2 files |
| 8 | `ste-code/v2/core/rules/` | growing (3+ files) |
| 9 | `SCE/compute/prompts/` | 2 files |
| 10 | `ste-code/v2/compute/prompts/` | 4 files |

## Quality Checks (Per Batch)

1. For each claimed placeholder: `test -f translations/<locale>/<path>` → exists
2. Each placeholder: `wc -c translations/<locale>/<path>` → 0 (fully blank)
3. Path correctness: `dirname translations/<locale>/<path>` matches the source directory structure
4. Catalog consistency: `translations/catalog.md` includes all discoveries from this batch
5. No false positives: skips are justified with reasons
6. No false negatives: all readable prose/markdown files are included

## Progress Tracking

File: `.agents/state/TRANSLATIONS-PROGRESS.md`

Format after each batch:
```markdown
## Batch N — YYYY-MM-DD HH:MM
- Target: <source_directory>
- Workers: 3/3 complete
- Discovered: <count> translatable files
- Locales processed: <locale subsets per worker>
- Placeholders created: <count> (files × 9 locales)
- Skipped: <count> files (list with reasons)
- Catalog: updated
- Next: Batch N+1 (<next_target>)
```

## Re-Discovery (Post-Enrichment)

After any enrichment session adds files, re-run discovery on the affected target(s). Workers will find:
- Net-new files (create new placeholders)
- Previously discovered files (skip — already have placeholders)

The catalog prevents duplicate work. A re-scan that finds nothing new completes instantly.

## Communication

Signal batch completions in `.agents/feedback/exchange.md`:

```markdown
## Agent #9 (Translation Orchestrator) → All Agents — YYYY-MM-DD
- Discovery: ste-code/artifacts/ (6 translatable, 6 skipped)
- Placeholders: 54 created (6 × 9 locales)
- Catalog: 54 entries tracked
- Next: ste-code/adapted/ (57 files expected)
```

## Key Facts

- 9 locales, discovery-based (not fixed-grid)
- Placeholders are fully blank (zero bytes)
- 3 workers per batch, each handles 3 locales
- 10 discovery targets, re-scannable after enrichment
- Catalog tracks all discoveries in `translations/catalog.md`
- deepseek-v4-pro exclusively
