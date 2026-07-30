---
description: "Translation discovery + scaffolding — explore pipeline output, reason about translatability, create fully blank placeholders across 9 locales. Discovery-based, not fixed-grid. Re-scans find new enrichment automatically."
version: "2.0.0"
related: [".agents/references/translation-grid.md", ".agents/references/worker-rails.md", ".agents/agent/agent-9-translations.md"]
---

# Translation Discovery + Scaffolding

Set up a multi-locale translation pipeline by **discovering** translatable content, not following a fixed inventory. Workers explore source directories, reason about what's worth translating, and create fully blank placeholder files at the correct paths for all 9 target locales.

**Why discovery:** Enrichment is ad-hoc across sessions — new words, rules, categories, and examples get added at different times by different agents. A fixed file grid rots immediately. Discovery workers find whatever is on disk right now. Re-run after enrichment to catch new files.

## Architecture Overview

The discovery pipeline uses a five-phase loop. Each batch of 3 workers processes one source directory.

```
EXPLORE source directory
  → REASON about each file (translatable or skip?)
    → CREATE blank placeholders for 3 assigned locales
      → REPORT discoveries to the orchestrator
        → NEXT target directory
```

**Key architectural decisions (rationale in Agent #9 contract):**

| Decision | Value | Why |
|----------|-------|-----|
| Workers per batch | 3 | Rate limit headroom. Verification window stays under 60 seconds. Failure isolates to 3 workers. |
| Locales per worker | 3 | Keeps token output under model limit. Fits 57-file targets comfortably. |
| Placeholder format | Blank (zero bytes) | Path-encoded metadata. No format lock-in. Deterministic verification with `wc -c`. |
| Target ordering | User-facing first | If discovery is interrupted, the most visible content already has placeholders. |
| Catalog ownership | Orchestrator only | Workers report. Only the orchestrator writes `translations/catalog.md`. Prevents merge conflicts. |

NOTE: The full design rationale, performance benchmarks, token budgets, and recovery protocols live in `.agents/agent/agent-9-translations.md`. This document is the operational protocol. The agent definition is the strategic plan.

## Agent Contract (Agent #9)

This skill is the operational protocol for **Agent #9 — Translation Orchestrator**. The agent's role definition lives in `.agents/agent/agent-9-translations.md`.

**Agent #9 contract summary:**

- **Role:** Discovery + scaffolding. The agent explores source directories, reasons about translatability, and creates blank placeholder files for all 9 locales.
- **Architecture:** Discovery loop — EXPLORE → CATALOG → CREATE PLACEHOLDERS → COMMIT → NEXT.
- **Worker pattern:** Poll system with 3 parallel workers per batch. Each worker handles 3 locales. Use `background=true` and `notify_on_complete=true`.
- **Scope:** 10 discovery targets in priority order. Re-scans after enrichment find new files automatically.
- **Model:** `deepseek-v4-pro` exclusively.
- **Output:** Blank placeholder files at correct paths. The catalog (`translations/catalog.md`) tracks all discoveries.
- **Communication:** Batch completions go to `.agents/feedback/exchange.md`. State updates go to `.agents/state/TRANSLATIONS-PROGRESS.md`.

See `.agents/agent/agent-9-translations.md` for the full role definition including the poll system, failure handling, and step-by-step launch instructions.

### Agent #9 Role Contract (Inline Summary)

The following table summarizes the agent's full contract. For details, consult the agent definition file.

| Contract Element | Specification | Source Section in Agent #9 |
|-----------------|---------------|----------------------------|
| **Skills to load** | This SKILL.md, spec-extraction worker orchestration, worker rails, auditor reference | Agent #9 §SKILLS |
| **Poll system** | 3 workers per batch, bg + notify_on_complete, never exceed 3 concurrent | Agent #9 §POLL SYSTEM |
| **Locale split** | Worker 1: zh-CN/ja/ko. Worker 2: es/fr/de. Worker 3: pt-BR/ru/ar | Agent #9 §CONCURRENCY COORDINATION |
| **Quality gates** | 6 weighted gates (G1-G6). Score ≥ 0.95 = EXCELLENT, ≥ 0.80 = ACCEPTABLE, < 0.80 = BLOCKED | Agent #9 §QUALITY GATES |
| **Failure handling** | Dead worker recovery: drop failed locale subset, add to next batch. Full batch failure: split target into subdirectories | Agent #9 §RECOVERY PROTOCOLS |
| **Self-discovery** | After every full re-scan, sweep for new source directories not in the targets table | Agent #9 §META-INSTRUCTIONS |
| **Token budget** | ~35K-105K tokens for full 10-target pass. Largest single worker (target 2): ~8K tokens | Agent #9 §AGENTIC-LOAD |
| **Performance** | 513 placeholder files created in ~500ms filesystem time. Full pass: 15-30 minutes wall time | Agent #9 §PERFORMANCE BENCHMARKS |

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

### Decision Tree

Workers use this decision tree for each file. Start at the top. Follow the first matching branch.

```
FILE FOUND
  │
  ├─ Is the file extension .py, .js, .ts, .sh, .rb, or .go?
  │    YES → SKIP (source code, not localizable prose)
  │    NO  → Continue
  │
  ├─ Is the file extension .schema.json or .config.json?
  │    YES → SKIP (structural schema, no prose)
  │    NO  → Continue
  │
  ├─ Is the file named worker-contract.json, rails.json, or gate-conditions.json?
  │    YES → SKIP (machine-readable contract, no human prose)
  │    NO  → Continue
  │
  ├─ Does the filename match *-batch-*.json or *-generated-*.json?
  │    YES → Check file content. Does it contain "definition" or "description" fields?
  │           YES → TRANSLATABLE (translate the definition/description values)
  │           NO  → SKIP (generated data, no prose)
  │    NO  → Continue
  │
  ├─ Is the file extension .md, .txt, or .prompt.md?
  │    YES → TRANSLATABLE (prose content a human reads)
  │    NO  → Continue
  │
  ├─ Is the file a .json vocabulary file with human-readable field values?
  │    YES → TRANSLATABLE (translate the definition/description fields)
  │    NO  → Continue
  │
  └─ DEFAULT: SKIP. If no branch matched, the file is not translatable.
       Record the skip reason as "no matching translatable category."
```

NOTE: The decision tree tolerates false negatives. A file skipped today may be flagged as translatable by a later audit. Re-scans catch these cases. The catalog keeps skip records for traceability.

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

## Worker Prompt Template

Write the prompt to `.agents/prompts/translations/discovery-NNN-prompt.txt` before each batch. Replace `<SOURCE_DIR>`, `<LOCALE_1>`, `<LOCALE_2>`, and `<LOCALE_3>` for the current target.

```text
You are a translation discovery worker. Your job: explore a source directory, reason about translatability, and create blank placeholder files.

## Pre-Flight Checks
Before you start discovery, do these checks:
1. Confirm the source directory exists: test -d <SOURCE_DIR>
2. If the directory does not exist, report: "ERROR: source directory <SOURCE_DIR> not found. Cannot proceed."
3. List the directory contents: ls -1 <SOURCE_DIR> (or find for nested trees)
4. Count the files: echo "Files found: $(ls -1 <SOURCE_DIR> | wc -l)"
5. Report the file count before reasoning starts. This number must match the DISCOVERED count in your report.

## Discovery Target
Directory: <SOURCE_DIR>

## Assigned Locales
Create blank placeholders for these 3 locales only:
- <LOCALE_1>
- <LOCALE_2>
- <LOCALE_3>

## Reasoning Loop
For each file in <SOURCE_DIR>, follow this decision path:

1. LIST all files in the directory. Use `ls` or `find` to get the complete list.
2. For each file, ask: "Does a human developer read this file and extract meaning from the words?"
3. If YES → TRANSLATABLE. Create a blank placeholder for each assigned locale.
4. If NO → SKIP. The file is structural (schema, config, generated data, script).

## Include / Skip Reference

| Include | Skip |
|---------|------|
| `.md` rule files | `.schema.json` |
| `.md` README files | `.py` scripts |
| `.md` narrative examples | `.json` config files without prose |
| `.txt` system prompts and artifacts | `worker-contract.json`, `rails.json`, `gate-conditions.json` |
| `.prompt.md` compute prompts | Generated `.json` data (`*-batch-*.json`) unless it contains descriptive definitions |
| `.json` vocabulary files with `"definition"` fields — translate the definitions | Scoring/compliance `.json` |

## File Creation
For each translatable file found at `<SOURCE_DIR>/<relative-path>/<filename>`:
- Create the directory: `mkdir -p translations/<locale>/<relative-path>/`
- Create a blank file: `touch translations/<locale>/<relative-path>/<filename>`
- Do this for all 3 assigned locales.
- Result: each placeholder is a zero-byte file with no content.

For nested source directories, preserve the full relative path. Example:
  Source: <SOURCE_DIR>/subdir/deep/file.md
  Placeholder: translations/<locale>/<SOURCE_DIR>/subdir/deep/file.md

Do NOT flatten the directory structure. The placeholder path must mirror the source path exactly.

## Post-Creation Self-Check
After creating all placeholders, check your own work:
1. For each created file, run: test -f translations/<locale>/<path>/<file> && echo "EXISTS: <path>"
2. For each created file, run: wc -c translations/<locale>/<path>/<file> — must return 0
3. Count total created files: find translations/<locale>/<SOURCE_DIR>/ -type f | wc -l
4. Compare the count against: translatable_files × 3 locales = expected total
5. Report any mismatch. A mismatch means a file was missed or double-created.

## Report Format
After creating all placeholders, produce this exact report:

```
DISCOVERED: <N> files in <SOURCE_DIR>
TRANSLATABLE: <N> files
  - <file1> (reason: <why translatable>)
  - <file2> (reason: <why translatable>)
SKIPPED: <N> files
  - <file1> (reason: <why skipped>)
  - <file2> (reason: <why skipped>)
CREATED: <N> blank placeholders across <3> locales
SELF-CHECK: <PASS or FAIL> (expected <N>, found <N>)

If SELF-CHECK is FAIL, list the specific files that are missing or non-empty.
```

Submit only blank files on disk plus this report. Do not write any content into the placeholder files.
```

### Prompt Template Variables

The orchestrator replaces these tokens before writing the prompt file:

| Token | Replaced With | Example |
|-------|--------------|---------|
| `<SOURCE_DIR>` | Path to the discovery target | `ste-code/artifacts/` |
| `<LOCALE_1>` | First assigned locale | `zh-CN` |
| `<LOCALE_2>` | Second assigned locale | `ja` |
| `<LOCALE_3>` | Third assigned locale | `ko` |
| `<NNN>` | Batch sequence number (zero-padded) | `001`, `002`, ..., `010` |

The batch number `<NNN>` is also used in the prompt filename: `discovery-<NNN>-prompt.txt`. This keeps prompt files traceable to their batch.

## Example Discovery Report

The example below shows the output from a worker that explored `ste-code/artifacts/` for locales `zh-CN`, `ja`, `ko`.

```
DISCOVERED: 6 files in ste-code/artifacts/
TRANSLATABLE: 5 files
  - README.md (reason: user-facing documentation with prose)
  - ste-code-distilled-system-prompt.txt (reason: system prompt used by end users)
  - ste-code-self-reading-manual.txt (reason: manual with procedural instructions)
  - ste-code-extraction-methodology.txt (reason: methodology document with narrative)
  - ste-code-deployment-guide.txt (reason: deployment steps with prose)
SKIPPED: 1 files
  - ste-code-example-turn.txt (reason: generated example turn data, not prose — skip)
CREATED: 15 blank placeholders across 3 locales

Placeholder paths created:
  translations/zh-CN/ste-code/artifacts/README.md
  translations/zh-CN/ste-code/artifacts/ste-code-distilled-system-prompt.txt
  translations/zh-CN/ste-code/artifacts/ste-code-self-reading-manual.txt
  translations/zh-CN/ste-code/artifacts/ste-code-extraction-methodology.txt
  translations/zh-CN/ste-code/artifacts/ste-code-deployment-guide.txt
  translations/ja/ste-code/artifacts/README.md
  translations/ja/ste-code/artifacts/ste-code-distilled-system-prompt.txt
  translations/ja/ste-code/artifacts/ste-code-self-reading-manual.txt
  translations/ja/ste-code/artifacts/ste-code-extraction-methodology.txt
  translations/ja/ste-code/artifacts/ste-code-deployment-guide.txt
  translations/ko/ste-code/artifacts/README.md
  translations/ko/ste-code/artifacts/ste-code-distilled-system-prompt.txt
  translations/ko/ste-code/artifacts/ste-code-self-reading-manual.txt
  translations/ko/ste-code/artifacts/ste-code-extraction-methodology.txt
  translations/ko/ste-code/artifacts/ste-code-deployment-guide.txt
```

NOTE: The `ste-code-example-turn.txt` file is skipped in this example. An auditor may later flag it as translatable if it contains readable prose. The discovery model tolerates false negatives — re-scans catch them.

### Annotated Report Walkthrough

Each section of the worker report serves a specific purpose in the pipeline:

**DISCOVERED: 6 files** — Raw file count from `ls` or `find`. This number anchors the report. The orchestrator checks that `TRANSLATABLE + SKIPPED = DISCOVERED`. Any arithmetic mismatch means the worker missed a file during reasoning.

**TRANSLATABLE: 5 files** — Each file has a reason. Reasons use the format `(reason: <why>)`. The orchestrator reads these reasons to spot false positives. Example: a `.schema.json` file tagged as translatable with reason "has prose" is a likely error. The orchestrator flags it for audit.

**SKIPPED: 1 files** — Skip reasons must be specific. A bad reason: "not needed." A good reason: "generated example turn data, not prose." Specific reasons let the orchestrator and auditor challenge skips during quality gate G6 (spot-check 20 percent of skipped files).

**CREATED: 15 blank placeholders** — Must equal `TRANSLATABLE × 3 locales`. For this example: `5 × 3 = 15`. If the count does not match, the worker failed to create some placeholders. The orchestrator checks this before accepting the report.

**Placeholder paths** — The full path list is the canonical record of what was created. The orchestrator uses this list to run `test -f` and `wc -c` checks. After verification, the orchestrator appends these entries to `translations/catalog.md`.

### Report Validation by the Orchestrator

After receiving a worker report, the orchestrator runs these checks before accepting it:

1. **Count consistency:** `DISCOVERED = TRANSLATABLE + SKIPPED`. Reject the report if the numbers do not add up.
2. **Placeholder count:** `CREATED = TRANSLATABLE × 3`. Reject if mismatch.
3. **Path list completeness:** The number of paths listed equals CREATED. Reject if fewer paths are listed than claimed.
4. **Reason presence:** Every TRANSLATABLE and SKIPPED entry has a `(reason: ...)` annotation. Reject entries without reasons.
5. **Self-check result:** If the worker included a SELF-CHECK line, accept PASS. Investigate FAIL before accepting.

A report that fails any of these checks is rejected. The orchestrator re-launches that worker with the same assignment. The worker's file creation is idempotent — existing placeholders are not overwritten by a re-launch.

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

## Validation Commands

Use these exact shell commands to check worker output. Run them from the project root.

### Check Placeholder Existence

```bash
# Check that all placeholder paths from a worker report exist on disk
# Paste the placeholder path list into a temp file, then:
while read -r path; do
  test -f "$path" && echo "OK: $path" || echo "MISSING: $path"
done < /tmp/placeholder-paths.txt
```

### Check Placeholders Are Empty

```bash
# Find all non-empty placeholders (violation of blank format)
find translations/ -type f -not -empty -name "*.md" -o -name "*.txt" -o -name "*.json" | while read -r f; do
  size=$(wc -c < "$f")
  echo "VIOLATION: $f has $size bytes (must be 0)"
done
```

### Count Placeholders Per Locale

```bash
# Verify all 9 locales have the same number of placeholders for a target
for locale in zh-CN ja ko es fr de pt-BR ru ar; do
  count=$(find "translations/$locale/ste-code/artifacts/" -type f 2>/dev/null | wc -l | tr -d ' ')
  echo "$locale: $count placeholders"
done
```

All 9 counts must be equal. A mismatch means a worker missed a locale during creation.

### Check Path Structure Mirrors Source

```bash
# For a given source directory, check that placeholder paths match
source_dir="ste-code/artifacts"
for locale in zh-CN ja ko es fr de pt-BR ru ar; do
  diff <(cd "$source_dir" && find . -type f | sort) \
       <(cd "translations/$locale/$source_dir" && find . -type f | sort) \
       && echo "$locale: MATCH" || echo "$locale: MISMATCH"
done
```

### Batch-Scoped wc Check

```bash
# Run wc -c only on files created in the current batch (not the whole tree)
# Replace <BATCH_PATHS> with the specific paths from the worker report
wc -c <BATCH_PATHS> | awk '$1 != 0 {print "NON-EMPTY:", $2, "(" $1 " bytes)"}'
```

NOTE: Do not run `find translations/ -type f -exec wc -c {} +` on the full tree after every batch. At 2,700+ placeholders this takes 5-10 seconds. Limit the check to files touched by the current batch.

## Catalog Schema

File: `translations/catalog.md`

The catalog is an auto-generated inventory of all discovered files. Workers and the orchestrator update it after each batch. It tracks what was found, where it came from, and which skip reasons apply.

### Schema Definition

| Field | Type | Description |
|-------|------|-------------|
| `last_discovery` | datetime | Timestamp of the most recent discovery scan. Format: `YYYY-MM-DD HH:MM`. |
| `locales` | list | All active target locales. Format: comma-separated BCP-47 tags. Example: `zh-CN, ja, ko, es, fr, de, pt-BR, ru, ar`. |
| `total_placeholders` | integer | Total placeholder files on disk. Formula: `translatable_files × locale_count`. |
| `sections` | map | One section per source directory. Key is the source path. Value is a list of discovered files. |
| `discovered_file` | object | A single translatable file entry with fields: `path` (source-relative), `type` (file extension), `reason` (why translatable). |
| `skipped` | list | Files that were examined but skipped. Each entry has `path` and `reason`. |

### Catalog Template

```markdown
# Translation Catalog — Auto-Generated

> Last discovery: YYYY-MM-DD HH:MM
> Locales: zh-CN, ja, ko, es, fr, de, pt-BR, ru, ar (9 total)
> Total placeholders: N files × 9 locales = 9N placeholder files

## Discovered Files

### <source-directory> (N translatable)
- <filename> — <reason translatable>
- <filename> — <reason translatable>

### <source-directory> (N translatable)
- <filename> — <reason translatable>

## Skipped Files

### <source-directory> (N skipped)
- <filename> — <reason skipped>
- <filename> — <reason skipped>
```

NOTE: The catalog is a living document. Re-scans add new sections without overwriting old ones. A skipped file that moves to translatable in a later scan gets a new entry — do not delete the old skip entry.

### Catalog Validation Rules

The orchestrator checks the catalog after every update. These rules keep the catalog consistent with disk state.

**R1: Header accuracy.** The `Last discovery` timestamp must match the most recent batch completion time. The `Locales` list must match the current locale table. The `Total placeholders` count must equal `find translations/ -type f -not -name "catalog.md" | wc -l`.

**R2: No duplicate entries.** A file must not appear under both Discovered and Skipped for the same source directory in the same batch. If a file was skipped in batch N and later found translatable in batch N+1, keep both entries. The older skip entry provides audit trail.

**R3: Source directory grouping.** Every entry must appear under a `### <source-directory>` heading. No entry may float outside a section. The section heading must match an actual source directory on disk.

**R4: Section ordering.** Source directory sections appear in discovery target order (1-10). New sections from self-discovery append at the end (11, 12, and so on).

**R5: Separator consistency.** Discovered and Skipped sections use `###` (H3) headings. The top-level headings `## Discovered Files` and `## Skipped Files` use `##` (H2). Do not mix heading levels.

**R6: Catalog overwrite protection.** Only the orchestrator writes the catalog. Workers report discoveries. The orchestrator merges. If a merge conflict occurs (two orchestrator sessions), accept both entries. The catalog is append-only.

To check the catalog quickly:

```bash
# R1: Header consistency
grep "^> Last discovery:" translations/catalog.md
grep "^> Locales:" translations/catalog.md
actual_count=$(find translations/ -type f -not -name "catalog.md" | wc -l | tr -d ' ')
catalog_count=$(grep "^> Total placeholders:" translations/catalog.md | grep -o '[0-9]\+' | head -1)
[ "$actual_count" = "$catalog_count" ] && echo "R1 PASS: count $actual_count matches" || echo "R1 FAIL: catalog=$catalog_count, disk=$actual_count"

# R2: Duplicate check (same file in both Discovered and Skipped in the same batch)
echo "R2: Manual check — review catalog for files appearing in both sections under the same source directory."

# R3: Orphan entry check (entries without a source directory section)
echo "R3: Manual check — every file entry must be under a ### section heading."
```

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

## Edge Cases

### Encoding: CJK Locales (zh-CN, ja, ko)

Placeholder files for CJK locales are blank — they contain no text. Encoding issues do not affect empty files. However, when translation content gets added later:

- Use UTF-8 without BOM for all locale files. BOM can break text processing tools on macOS and Linux.
- Filenames that contain CJK characters must be valid UTF-8. Avoid non-ASCII characters in filenames. Use ASCII filenames only.
- The directory path segment `zh-CN/`, `ja/`, `ko/` uses ASCII identifiers. No encoding concerns.

### Encoding: Arabic (ar) and RTL

The `ar` locale uses Arabic script (Arab) and is right-to-left (RTL). Placeholder files are blank, so RTL has no effect during scaffolding. When translation content gets added later:

- Do not add Unicode RTL markers (U+200F) or bidirectional overrides (U+202A–U+202E) to blank placeholder files.
- File content for `ar` translations must use UTF-8 encoding.
- Directory paths remain LTR (`translations/ar/...`). The locale tag `ar` is ASCII.

### Path Collisions: Same File Name in Different Source Trees

A file name can appear in more than one source directory. Example: `README.md` exists in `ste-code/artifacts/` and `SCE/core/rules/`. The placeholder path includes the source-relative directory, so these files get distinct paths:

```
translations/zh-CN/ste-code/artifacts/README.md
translations/zh-CN/SCE/core/rules/README.md
```

No collision occurs. The path structure mirrors the source tree exactly. Workers must use the full source-relative path when creating placeholders — never flatten directory structures.

### Adding a New Locale (10th Locale)

To add a locale after the initial discovery:

1. Create the locale directory: `mkdir -p translations/<new-locale>/`
2. Add the locale to the catalog metadata under `locales` and update `total_placeholders`.
3. Run discovery on all 10 targets again. Workers create blank placeholders under `translations/<new-locale>/` for all already-discovered files.
4. Update the locale table in this document and in the Agent #9 contract.
5. Update `translations/catalog.md` header to reflect the new locale count.

New placeholders for the added locale mirror the existing path structure. No changes are needed for the other 9 locales.

NOTE: Adding a locale after translations have started means the new locale starts with blank placeholders only. It is behind the other locales. Plan for a dedicated translation pass to catch up.

### Source File Deleted After Discovery

If a source file is deleted after placeholders were created:

- The placeholder remains on disk. It is a valid path but orphans from the source.
- A re-scan does NOT delete placeholder files. The orchestrator only adds placeholders, never removes them.
- To clean up orphaned placeholders, run a manual audit: compare `translations/catalog.md` entries against current disk state. Remove placeholder files with no matching source file.

### Source Directory Does Not Exist

A discovery target may not exist yet. Example: target 5 (`SCE/core/rules/`) is listed as "growing" and may be empty or absent when discovery starts.

Worker behavior for a missing source directory:

1. The pre-flight check (`test -d <SOURCE_DIR>`) fails.
2. The worker reports: "ERROR: source directory <SOURCE_DIR> not found. Cannot proceed."
3. The worker creates zero placeholders. Its report shows DISCOVERED: 0, TRANSLATABLE: 0, SKIPPED: 0, CREATED: 0.
4. The orchestrator records the batch as "TARGET NOT FOUND — deferred" in the progress tracker.
5. The target stays in the discovery queue. A later re-scan will find it when it is created.

Do not remove targets from the queue just because they are empty. The "growing" targets (5, 8) are expected to populate over time.

### Worker Failure and Retry

A worker can fail for several reasons:

| Failure Mode | Symptom | Recovery |
|-------------|---------|----------|
| API timeout | Worker process exits with no output after 5 minutes | Re-launch that worker with the same prompt. Check API status first. |
| Partial output | Worker creates some placeholders but crashes before finishing | Accept the partial set. The next batch covers missing locales per the dead worker recovery protocol in Agent #9. |
| Wrong locale subset | Worker creates placeholders for locales it was not assigned (e.g., zh-CN instead of es) | Remove the wrong-locale placeholders. Re-launch with corrected prompt. This error usually means the prompt template was not filled correctly. |
| Hallucinated files | Worker reports creating placeholders for files that do not exist in the source directory | Reject the report. The orchestrator's `test -f` check on source files catches this. Re-launch the worker. |
| Non-empty placeholders | Worker writes content into placeholder files (violates blank format) | Remove the non-empty files. Run `touch` to recreate blank versions. Flag the worker prompt for review — the "Do not write any content" instruction may need emphasis. |

### Symlinks in Source Trees

If a source directory contains symbolic links:

- Workers list symlinks as regular files. The symlink target is not resolved during listing.
- If a symlink points to a translatable file (`.md`, `.txt`, `.prompt.md`), the worker may create a placeholder for the symlink name.
- The placeholder mirrors the symlink path, not the target path.
- This is usually correct: the symlink name is what appears in the source tree. Translators will see the symlink name.

NOTE: If a symlink creates a loop (A → B → A), `find` with `-follow` may hang. Workers must use `ls -1` or `find` without `-follow` to avoid symlink loops.

### Empty Source Directory

If a source directory exists but contains zero files:

1. Worker pre-flight check passes (`test -d` succeeds).
2. File listing returns zero files.
3. Worker reports: DISCOVERED: 0, TRANSLATABLE: 0, SKIPPED: 0, CREATED: 0.
4. The orchestrator records the batch as "EMPTY TARGET — nothing to translate."
5. The catalog is not updated (no entries to add).

An empty target is not an error. It is normal for targets that are listed as "growing." The batch completes instantly.

### Locale Directory Conflict

If a placeholder path already exists and contains content (non-zero bytes):

1. The worker's `touch` command does not overwrite content. `touch` only updates the modification timestamp.
2. The post-creation self-check (`wc -c`) returns a non-zero value.
3. The worker reports this as a SELF-CHECK FAIL with the specific file path and byte count.
4. The orchestrator sees the FAIL and investigates: was this file translated already? Is it a stale file from a previous pipeline version?
5. Decision: if the file contains a valid translation, keep it and update the catalog to note "content present." If the file contains garbage or stale data, remove it and create a fresh blank placeholder.

The orchestrator must not blindly overwrite files that already have translation content. The `touch` command is safe because it does not truncate files.

## Troubleshooting

### Symptom: Worker Report Shows DISCOVERED ≠ TRANSLATABLE + SKIPPED

**Cause:** The worker listed N files but only reported reasoning for fewer than N files. One or more files were silently dropped during reasoning.

**Fix:**
1. Reject the report. Do not update the catalog.
2. Check the worker report for files that appear in the file listing but not in the TRANSLATABLE or SKIPPED lists.
3. Re-launch the worker. Add instruction: "You must include EVERY file from the directory listing in your report. No file may be omitted."

### Symptom: Placeholder Count Mismatch Between Locales

**Cause:** A worker created placeholders for some but not all assigned locales. Example: 5 placeholders under `zh-CN/` but only 4 under `ja/`.

**Fix:**
1. Run the per-locale count check (see Validation Commands).
2. Identify which locale is short.
3. Re-launch a single worker targeting only the missing locale and the specific source directory.
4. Use the command: `hermes -z "Create blank placeholders for locale <LOCALE> for files in <SOURCE_DIR>. Files: <list>" -m deepseek-v4-pro --yolo`

### Symptom: Catalog Count Does Not Match Disk Count

**Cause:** The catalog header says `Total placeholders: 450` but `find translations/ -type f -not -name catalog.md | wc -l` returns 447.

**Fix:**
1. Find the 3 missing files: compare the catalog entry list against actual disk files.
2. If files exist on disk but are missing from the catalog: append them to the catalog.
3. If catalog entries exist but files are missing from disk: re-create the missing placeholders with `touch`.
4. Update the catalog header count after fixing.

### Symptom: Worker Creates Placeholders Under Wrong Root

**Cause:** The worker ran from the wrong working directory. Placeholders ended up at `~/Developer/macOS/Application/Manual/translations/...` instead of `<project_root>/translations/...`.

**Fix:**
1. Always launch workers from the project root directory.
2. The orchestrator must `cd` to the project root before launching any worker.
3. Add `--workdir <project_root>` to the hermes launch command if the orchestrator session started elsewhere.

### Symptom: Git Merge Conflict on catalog.md

**Cause:** Two orchestrator sessions wrote to `translations/catalog.md` concurrently. This happens when enrichment and discovery run at the same time on overlapping directory trees.

**Fix:**
1. Open `translations/catalog.md`. Git marks the conflicting regions with `<<<<<<<`, `=======`, and `>>>>>>>`.
2. Accept both entries. The catalog is append-only. Both sessions found valid discoveries.
3. If both sessions discovered the same file, keep one entry (they are identical).
4. Update the header: `Last discovery` gets the later timestamp. `Total placeholders` gets the new count.
5. Commit the merge: `git add translations/catalog.md && git commit -m "translations: merge concurrent catalog updates"`

## Worker Lifecycle

Each worker follows a defined lifecycle from launch to completion. The orchestrator tracks each phase.

```
LAUNCH
  │
  ├─ PRE-FLIGHT (5-10 seconds)
  │   test -d <SOURCE_DIR>
  │   ls -1 <SOURCE_DIR> (or find for nested)
  │   Report file count
  │   ↓
  ├─ REASONING (10-60 seconds, depends on file count)
  │   For each file: apply decision tree
  │   Build TRANSLATABLE list with reasons
  │   Build SKIPPED list with reasons
  │   ↓
  ├─ FILE CREATION (1-5 seconds filesystem time)
  │   mkdir -p translations/<locale>/<path>/
  │   touch translations/<locale>/<path>/<file>
  │   Repeat for all 3 assigned locales
  │   ↓
  ├─ SELF-CHECK (1-3 seconds)
  │   test -f on each created placeholder
  │   wc -c on each created placeholder (must be 0)
  │   Count created files per locale
  │   ↓
  └─ REPORT (instant)
      Print DISCOVERED / TRANSLATABLE / SKIPPED / CREATED
      Print full placeholder path list
      Print SELF-CHECK result
      ↓
    EXIT (notify_on_complete fires)
```

**Orchestrator actions after worker exit:**
1. Receive worker report via `notify_on_complete`.
2. Validate report (count consistency, placeholder count, path completeness, reasons).
3. Run disk checks (`test -f`, `wc -c`) on the reported paths.
4. Accept or reject the report.
5. If accepted: update `translations/catalog.md`.
6. Update `.agents/state/TRANSLATIONS-PROGRESS.md`.
7. Commit: `git add -A && git gcommit-hermes "translations: discovered N files in <target>"`
8. Proceed to next discovery target or signal completion.

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
