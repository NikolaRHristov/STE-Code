# Translation Discovery Grid — Dynamic

> **Status:** Discovery-based — this document tracks what has been found, not what should exist.
> **Last full scan:** Not yet performed
> **Locales:** zh-CN, ja, ko, es, fr, de, pt-BR, ru, ar (9 total)

## Cross-References

This grid does not operate in isolation. It depends on these documents and feeds into these pipelines.

### Documents This Grid DEPENDS ON (must exist and be correct)

| Reference | Path | What It Provides | Why This Grid Needs It |
|-----------|------|------------------|------------------------|
| STE-Code Implementation Protocol | `.agents/references/STE-CODE-IMPLEMENTATION.md` | Master protocol that defines the 6 artifact files (GATE 4), quality gates, anti-fabrication rules, and pipeline stages | This grid translates those 6 artifacts. The master protocol defines what the artifacts contain and how they are generated. |
| Granular Strategy | `.agents/references/granular-strategy.md` | Batch-of-3 worker pattern, 4-page per worker sweet spot, failure recovery, monitoring thresholds | This grid inherits the same batch-of-3 concurrent worker pattern. The discovery workers use the same launch protocol. |
| Agent #9 (Translation Orchestrator) | `.agents/agent/agent-9-translations.md` | Full orchestrator role: poll system, locale assignments, quality gates (G1-G6), recovery protocols, self-discovery of new targets | This grid is the tracking document that Agent #9 reads and updates. The orchestrator cannot run without this grid. |
| Translations SKILL | `.agents/skills/translations/SKILL.md` | Operational protocol: worker prompt template, decision tree for translatability, placeholder format, catalog schema, validation commands | This grid's discovery targets and batch worker assignments mirror the SKILL's protocol. |
| Worker Rails | `.agents/references/worker-rails.md` | 10 output-format rails injected into every worker prompt | Discovery workers self-validate their output against these rails. |
| Quality Checklist | `.agents/references/quality-checklist.md` | Per-batch verification checklist | Translation batches use the same 6-check pattern adapted for placeholder validation. |

### Documents That EXTEND This Grid (read when relevant)

| Reference | Path | What It Provides | When to Read It |
|-----------|------|------------------|-----------------|
| Category Mapping | `.agents/references/category-mapping.md` | 19 technical noun categories | When a worker finds a file with technical nouns that need category-aware translation |
| Section Types | `.agents/references/section-types.md` | Content signature per page range | When a worker encounters content that spans section boundaries and needs to determine the dominant type |
| Worker Grid | `.agents/references/worker-grid.md` | Full 109-worker launch architecture | When discovery needs to scale to many small files (similar to the extraction grid pattern) |
| Auditor (Agent #3) | `.agents/agent/agent-3-auditor.md` | Ground-truth verification | When the orchestrator needs to verify a worker's discovery claims against disk evidence |

### Documents This Grid DRIVES

| Artifact | Path | Created By | When |
|----------|------|-----------|------|
| Translation Catalog | `translations/catalog.md` | Orchestrator (Agent #9) | After each batch completion |
| Translation Progress | `.agents/state/TRANSLATIONS-PROGRESS.md` | Orchestrator (Agent #9) | After each batch completion |
| Blank Placeholders | `translations/<locale>/<source-path>/<file>` | Discovery workers | During each batch |

## How Discovery Works

Workers explore source directories and **reason** about translatability. This grid is populated as discoveries happen — it is a running log, not a prescription. After each batch, discovered files get recorded here.

The discovery loop mirrors the batch-of-3 pattern from the granular strategy (`.agents/references/granular-strategy.md`). Each batch launches 3 workers. Each worker handles 3 locales. The orchestrator verifies output after all 3 workers exit. This pattern keeps rate limit usage low and makes failure isolation straightforward.

## Discovery Targets

| # | Target | Status | Last Scan | Files Expected | Files Found | Notes |
|---|--------|--------|-----------|:---:|:---:|-------|
| 1 | `ste-code/artifacts/` | ⬜ Pending | — | 6 | — | Defined by STE-CODE-IMPLEMENTATION.md GATE 4 |
| 2 | `ste-code/adapted/` | ⬜ Pending | — | 57 | — | Largest single target. 513 placeholders after discovery |
| 3 | `SCE/narratives/system-prompts/` | ⬜ Pending | — | 4 | — | Agent-facing prompts |
| 4 | `SCE/narratives/examples/` | ⬜ Pending | — | 2 | — | User-facing examples |
| 5 | `SCE/core/rules/` | ⬜ Pending | — | growing (1+) | — | Expands as enrichment adds rules |
| 6 | `ste-code/v2/narratives/system-prompts/` | ⬜ Pending | — | 4 | — | v2 pipeline prompts |
| 7 | `ste-code/v2/narratives/examples/` | ⬜ Pending | — | 2 | — | v2 user-facing examples |
| 8 | `ste-code/v2/core/rules/` | ⬜ Pending | — | growing (3+) | — | Currently 4 files on disk: README.md, rule-1.1.md, rule-1.11.md, rule-1.12.md |
| 9 | `SCE/compute/prompts/` | ⬜ Pending | — | 2 | — | Rule adaptation and compliance prompts |
| 10 | `ste-code/v2/compute/prompts/` | ⬜ Pending | — | 4 | — | v2 compute prompts |

**Status legend:**
- ⬜ Pending — not yet discovered
- 🔄 In Progress — workers launched, not yet verified
- ✅ Complete — all placeholders created and verified
- ⚠️ Partial — some locales completed, some pending recovery
- ❌ Failed — batch failed, needs re-launch
- 🔁 Re-scan Needed — enrichment has added files since last scan

## Expected File Counts (from current disk state)

### ste-code/artifacts/ — 6 files expected
```
ste-code-distilled-system-prompt.txt
ste-code-self-reading-manual.txt
ste-code-extraction-methodology.txt
ste-code-example-turn.txt
ste-code-deployment-guide.txt
README.md
```

NOTE: These 6 files are defined by the STE-Code Implementation Protocol (`.agents/references/STE-CODE-IMPLEMENTATION.md`, GATE 4). The protocol lists these as the 6 output artifacts. Do not add or remove files from this list unless the master protocol changes.

### ste-code/adapted/ — 57 files expected
```
a-dictionary.md
a-categories.md
a-sec1-rule1.1.md through a-sec1-rule1.14.md (14 files)
a-sec2-rule2.1.md through a-sec2-rule2.2.md (2 files)
a-sec3-rule3.1.md through a-sec3-rule3.7.md (7 files)
a-sec4-rule4.1.md through a-sec4-rule4.5.md (5 files)
a-sec5-rule5.1.md through a-sec5-rule5.5.md (5 files)
a-sec6-rule6.1.md through a-sec6-rule6.5.md (5 files)
a-sec7-rule7.1.md through a-sec7-rule7.3.md (3 files)
a-sec8-rule8.1.md through a-sec8-rule8.6.md (6 files)
a-sec9-rule9.1.md through a-sec9-rule9.4.md (4 files)
a-sec9-gr1.md through a-sec9-gr4.md (4 files)
```

### SCE/narratives/system-prompts/ — 4 files expected
```
ste-code-micro.md
ste-code-full.md
ste-code-agentic.md
ste-code-developer.md
```

### SCE/narratives/examples/ — 2 files expected
```
example-readme-section.md
example-commit-message.md
```

### SCE/core/rules/ — growing (1+ files expected)
Currently: `README.md`. More rules added as enrichment progresses.

### ste-code/v2/narratives/system-prompts/ — 4 files expected
```
ste-code-user.md
ste-code-micro.md
ste-code-developer.md
ste-code-agentic.md
```

### ste-code/v2/narratives/examples/ — 2 files expected
```
example-readme.md
example-commit-message.md
```

### ste-code/v2/core/rules/ — growing (3+ files expected)
Currently: `README.md`, `rule-1.1.md`, `rule-1.11.md`, `rule-1.12.md`

### SCE/compute/prompts/ — 2 files expected
```
rule-adaptation.prompt.md
compliance-check.prompt.md
```

### ste-code/v2/compute/prompts/ — 4 files expected
```
vocabulary-review.prompt.md
rule-adaptation.prompt.md
compliance-check.prompt.md
agentic-worker.prompt.md
```

## What Gets Skipped (no placeholders)

| File Pattern | Reason |
|-------------|--------|
| `*.schema.json` | JSON schema, structural |
| `*.py` | Python scripts, not translatable |
| `*worker-contract.json` | Agent configuration, structural |
| `*rails.json` | Agent configuration, structural |
| `*gate-conditions.json` | Agent configuration, structural |
| `*violation-severity-map.json` | Scoring config |
| `*compliance-rubric.json` | Scoring config |
| `*generated/*.json` (nouns-batch, verbs-batch, adjectives-batch, anti-patterns-batch) | Generated data — translate definitions only |
| `*verb-categories.json` | Category definitions (translate if prose, skip if structural IDs) |
| `*noun-categories.json` | Category definitions (translate if prose, skip if structural IDs) |

## Placeholder Directory Layout

```
translations/
├── catalog.md
├── zh-CN/
│   ├── ste-code/artifacts/*
│   ├── ste-code/adapted/*
│   ├── SCE/narratives/system-prompts/*
│   ├── SCE/narratives/examples/*
│   ├── SCE/core/rules/*
│   ├── SCE/compute/prompts/*
│   ├── ste-code-v2/narratives/system-prompts/*
│   ├── ste-code-v2/narratives/examples/*
│   ├── ste-code-v2/core/rules/*
│   └── ste-code-v2/compute/prompts/*
├── ja/ (same)
├── ko/ (same)
├── es/ (same)
├── fr/ (same)
├── de/ (same)
├── pt-BR/ (same)
├── ru/ (same)
└── ar/ (same)
```

Note: Paths use the source directory name as-is (e.g., `ste-code/`, `SCE/`, `ste-code-v2/`), not flattened.

## Batch Worker Assignments

Per discovery target, 3 workers × 3 locales each. This split follows the Agent #9 contract (`.agents/agent/agent-9-translations.md`, §CONCURRENCY COORDINATION).

| Worker | Locales | Script Families | Rationale |
|--------|---------|-----------------|-----------|
| W1 | zh-CN, ja, ko | CJK (Hans, Jpan, Hang) | Shared character-based script properties |
| W2 | es, fr, de | Latin European | Shared Latin-script European languages |
| W3 | pt-BR, ru, ar | Latin Americas, Cyrillic, Arabic RTL | Mixed scripts — W3 handles the most diverse encoding set |

All 3 workers explore the same source directory. Each creates placeholders for its 3 assigned locales.

## Re-Discovery Protocol

After any enrichment session:

1. Re-launch discovery on affected target(s)
2. Workers skip files that already have placeholders (check `test -f translations/<locale>/<path>` before creating)
3. Net-new files get fresh placeholders
4. Update this grid's status and last-scan timestamp
5. Update catalog.md with additions

Re-scan cost is approximately 20 percent of a first-pass batch. Workers re-list all files but only create placeholders for net-new files. See Agent #9 §AGENTIC-LOAD for token estimates.

## Discovery Records

This section logs actual discoveries as workers complete batches. Each entry records what was found, what was created, and any anomalies.

### Record Format

```markdown
#### Batch NN — YYYY-MM-DD HH:MM — Target #T: <target-path>
- **Worker 1** (<locale>, <locale>, <locale>): Discovered N files, created M placeholders. Status: PASS/FAIL
- **Worker 2** (<locale>, <locale>, <locale>): Discovered N files, created M placeholders. Status: PASS/FAIL
- **Worker 3** (<locale>, <locale>, <locale>): Discovered N files, created M placeholders. Status: PASS/FAIL
- **Quality Score:** X.XX / 1.00 (G1: pass/fail, G2: pass/fail, G3: pass/fail, G4: pass/fail, G5: pass/fail, G6: pass/fail)
- **Git commit:** <hash>
- **Delta from expected:** +N new files, -M removed files, ~K renamed files
- **Notes:** <any anomalies, edge cases hit, decisions made>
```

### Example Record (showing expected format — no worker has run yet)

```
#### Batch 01 — 2025-07-30 14:22 — Target #1: ste-code/artifacts/
- **Worker 1** (zh-CN, ja, ko): Discovered 6 files, created 15 placeholders. Status: PASS
- **Worker 2** (es, fr, de): Discovered 6 files, created 15 placeholders. Status: PASS
- **Worker 3** (pt-BR, ru, ar): Discovered 6 files, created 15 placeholders. Status: PASS
- **Quality Score:** 1.00 / 1.00 (G1: pass, G2: pass, G3: pass, G4: pass, G5: pass, G6: pass)
- **Git commit:** a1b2c3d
- **Delta from expected:** 0 new, 0 removed, 0 renamed
- **Notes:** Clean first-target discovery. All 6 artifacts match STE-CODE-IMPLEMENTATION.md GATE 4 expected list. 5 of 6 marked translatable. ste-code-example-turn.txt skipped — contains generated example turn data, not human-readable prose. If audit later flags it as translatable, re-scan will catch it.
```

### Actual Records

No discovery batches have run yet. Records appear here as workers complete.

---

## Edge Cases

### EC1: Source Directory Does Not Exist

The grid lists 10 targets. Some targets reference directories that are planned but not yet created. For example, `ste-code/v2/core/rules/` currently has 4 files but the grid says "growing (3+ files expected)." A different pipeline stage may not have created the directory at all.

**Detection:** Worker pre-flight check (`test -d <SOURCE_DIR>`) fails. Worker reports: "ERROR: source directory <SOURCE_DIR> not found. Cannot proceed."

**Handling:**
1. Worker reports the missing directory. Do not create placeholders for a directory that does not exist.
2. Orchestrator marks the target as ⚠️ Partial with note: "Source directory not found on disk."
3. Orchestrator skips this target and proceeds to the next target.
4. The missing target stays in the grid. A future re-scan retries it.
5. If all 10 targets are missing, the pipeline is not ready for discovery. Stop and report.

**Do NOT create the source directory.** The grid is a tracking document, not a provisioning tool. Missing source directories indicate that the pipeline stage that produces them has not run yet.

### EC2: Worker Encounters a New File Type Not in the Skip List

The skip list covers known patterns: `.schema.json`, `.py`, `worker-contract.json`, and so on. A new file type may appear that is not in the skip list. For example, a `.yaml` configuration file or a `.toml` settings file.

**Detection:** Worker runs the decision tree (`.agents/skills/translations/SKILL.md`, §Decision Tree). The file reaches the DEFAULT branch: "no matching translatable category."

**Handling:**
1. Worker records the file under SKIPPED with reason: "Unknown file type: .yaml — not in translatability decision tree."
2. Orchestrator reviews the skip reason during quality gate G6 (spot-check 20 percent of skipped files).
3. If the file contains human-readable prose, mark it as a false negative. Create placeholders for it.
4. If the file is structural, add it to the skip list in this document. Update the decision tree in the SKILL.
5. If the file type is genuinely ambiguous, flag it for auditor review.

**Examples of ambiguous file types:**

| Extension | Likely Translatable? | Rationale |
|-----------|:---:|-----------|
| `.yaml` | Depends | Configuration files: skip. Documentation frontmatter: skip. Prose content: translate. |
| `.toml` | No | Configuration format. No prose. Skip. |
| `.rst` | Yes | ReStructuredText documentation. Prose. Translate. |
| `.adoc` | Yes | AsciiDoc documentation. Prose. Translate. |
| `.csv` | No | Data tables. No prose. Skip. |
| `.xml` | Depends | Configuration XML: skip. Documentation XML (DITA, DocBook): translate. |

### EC3: Conflicting Translations for Shared Terms Across Locales

The STE-Code dictionary defines approved words with exact meanings. Different locales may translate the same approved word differently. For example, the word "make" (approved meaning: to create) could be translated as "crear" (Spanish), "créer" (French), or "erstellen" (German). These are correct independent translations. The conflict arises when a shared technical term (for example, "worker" as an agent name) gets different translations across locales.

**Detection:** Not detectable at placeholder stage — placeholders are blank. This edge case applies during content translation, which is downstream of discovery.

**Prevention at scaffolding stage:**
1. The catalog (`translations/catalog.md`) groups files by source directory. All locales share the same source file names.
2. When translation content is added later, a glossary file per locale (`translations/<locale>/glossary.md`) records term-to-translation mappings.
3. Before translating, consult the glossary. If a term has no entry, add the translation to the glossary. If a term already has an entry, use the existing translation.
4. The orchestrator does NOT enforce cross-locale consistency. Each locale is independent. Consistency within a locale matters. Consistency across locales is not required.

### EC4: Growing Directory — File Count Mismatch on Re-Scan

Targets 5 (`SCE/core/rules/`) and 8 (`ste-code/v2/core/rules/`) are marked "growing." The file count changes between scans as enrichment adds rules.

**Handling:**
1. First scan: worker discovers N files. Creates N × 3 placeholders per worker (N × 9 total).
2. Re-scan after enrichment: worker discovers N+M files. Existing N placeholders are skipped. Only M new placeholders are created.
3. The grid's "Files Expected" column shows the minimum known count ("growing (1+)", "growing (3+)"). After each scan, update the "Files Found" column with the actual count.
4. If a file is removed between scans (source file deleted but placeholder remains), it becomes an orphan. See EC5.

### EC5: Orphaned Placeholder — Source File Deleted After Discovery

A placeholder file exists at `translations/<locale>/<path>/<file>` but the source file at `<path>/<file>` has been deleted or renamed.

**Detection:** Run the orphan check from Agent #9 §RECOVERY PROTOCOLS:
```bash
for placeholder in $(find translations/ -type f -size 0); do
  source_path=$(echo "$placeholder" | sed 's|translations/[^/]*/||')
  [ ! -f "$source_path" ] && echo "ORPHAN: $placeholder (source $source_path missing)"
done
```

**Handling:**
1. Do not delete orphans automatically. Review each one.
2. If the source was intentionally deleted: remove the orphan placeholder from all 9 locales.
3. If the source was renamed: move the placeholder to the new path (all 9 locales).
4. If unsure: flag for auditor review. Leave the orphan in place.
5. Record cleanup actions in `.agents/state/TRANSLATIONS-PROGRESS.md`.

### EC6: RTL Locale — Arabic Path Structure

The `ar` (Arabic) locale uses right-to-left script. Blank placeholder files have no text direction issues because they are zero bytes. When translation content is added later:

**Rules:**
- Directory paths remain LTR: `translations/ar/ste-code/artifacts/...`
- File contents must use UTF-8 encoding without BOM.
- Do not add Unicode RTL markers (U+200F, U+202A-U+202E) to blank placeholders.
- Do not mirror the directory structure. The path is a filesystem identifier, not a reading order.

### EC7: Nested Source Directory Structure

Most targets are flat — all files sit directly in the target directory. If a source directory has nested subdirectories (for example, `SCE/core/rules/subsection/deep/file.md`), the placeholder path must preserve the full relative structure:

```
Source: SCE/core/rules/subsection/deep/file.md
Placeholder: translations/zh-CN/SCE/core/rules/subsection/deep/file.md
```

**Handling:**
1. Worker uses `find <SOURCE_DIR> -type f` to list all files recursively.
2. Worker preserves the relative path from the source root.
3. Worker creates intermediate directories: `mkdir -p translations/<locale>/<relative-dir>/`
4. Validation command (`diff` between source and placeholder directory trees) catches depth mismatches.

### EC8: File with Mixed Content — Part Prose, Part Code

Some files contain both human-readable prose and machine-readable code. For example, a markdown file with embedded YAML frontmatter or a JSON file with both structural keys and descriptive text fields.

**Detection:** The decision tree in the SKILL handles this case. A `.json` file with `"definition"` fields is translatable — translate the definition values only. A `.md` file with YAML frontmatter is translatable — translate the prose body, preserve the frontmatter.

**Handling at placeholder stage:** Create a blank placeholder. The placeholder is zero bytes. The decision about what to translate within the file is deferred to the content translation phase. The placeholder reserves the file path. Content translation handles mixed-content extraction later.

### EC9: Target Directory Contains Only Skippable Files

A discovery target exists on disk but every file inside matches a skip pattern. For example, a future target might contain only `.schema.json` files.

**Detection:** Worker reports DISCOVERED: N files, TRANSLATABLE: 0 files, SKIPPED: N files.

**Handling:**
1. Worker creates zero placeholders. The report shows CREATED: 0.
2. Orchestrator marks the target as ✅ Complete with note: "No translatable files found. All N files skipped."
3. Update the grid's "Files Found" column with the actual count. Add a note: "All skipped."
4. This is not an error. Some targets may legitimately contain only structural files.

---

## Failure Modes

### FM1: Worker Creates Placeholder with Wrong Encoding

**Symptom:** A placeholder file is not zero bytes. It contains BOM markers (U+FEFF), null bytes, or encoding artifacts.

**Root cause:** Worker used `echo "" > file` instead of `touch file`. Some shells add a trailing newline or encoding prefix to empty echoes. Or the worker wrote a UTF-8 BOM before an empty body.

**Detection:** Quality gate G2 (Zero Content). Run `wc -c` on every placeholder. Any non-zero byte is a failure.

**Recovery:**
1. Delete the non-empty placeholder file.
2. Re-create it with `touch`: `touch translations/<locale>/<path>/<file>`
3. Verify: `wc -c translations/<locale>/<path>/<file>` must return 0.
4. Flag the worker that created the non-empty file. Check if other files from the same worker also have encoding artifacts.
5. If the worker repeats this error, review the worker prompt template. The prompt must say "create a fully blank (zero-byte) file" not "create an empty file."

### FM2: Locale Directory Structure Does Not Match Expectations

**Symptom:** Placeholders exist at `translations/zh-CN/ste-code/artifacts/file.md` but also at `translations/zh-CN/ste-code-artifacts/file.md` (flattened path). The directory structure does not mirror the source.

**Root cause:** Worker interpreted "mirror the source path" differently. Some workers may flatten the path (replace `/` with `-`). Others may nest incorrectly.

**Detection:** Quality gate G3 (Path Correctness). Run the `diff` validation command:
```bash
diff <(cd "$source_dir" && find . -type f | sort) \
     <(cd "translations/$locale/$source_dir" && find . -type f | sort)
```

**Recovery:**
1. Identify all misplaced placeholders.
2. Move them to the correct paths. Use `mkdir -p` for intermediate directories.
3. Delete any empty directories left behind.
4. Re-run the `diff` check. It must show MATCH for all 9 locales.
5. Fix the worker prompt template to include an explicit path example with slashes.

### FM3: Worker Timeout — Batch Incomplete

**Symptom:** One or more workers in a batch do not exit within 120 seconds. The orchestrator receives only partial reports.

**Root cause:** API congestion, model inference slow on large targets (target 2 with 57 files), or rate limiting.

**Recovery:**
1. Poll remaining workers: `process action='poll' session_id=<ID>`
2. If running and less than 120 seconds elapsed, wait. Target 2 (ste-code/adapted/, 57 files) is the slowest.
3. If running and more than 120 seconds elapsed, kill the process: `process action='kill' session_id=<ID>`
4. Do not re-launch the failed worker with the same locale assignment. Partial placeholders would cause duplicates.
5. Drop the failed worker's locale subset from this batch. Add those locales to the next batch as a recovery set.
6. Record the incident in `.agents/state/TRANSLATIONS-PROGRESS.md`.

### FM4: Placeholder Has Content — Worker Wrote Prose Instead of Blank File

**Symptom:** A placeholder file contains text such as "TODO: translate later" or "Placeholder for <filename>" or YAML frontmatter.

**Root cause:** Worker misunderstood the instruction. The prompt says "blank" but the worker interpreted it as "blank content with a placeholder note."

**Detection:** Quality gate G2 (Zero Content). `wc -c` returns a non-zero value.

**Recovery:**
1. Truncate the file: `: > translations/<locale>/<path>/<file>`
2. Verify: `wc -c` must return 0.
3. If the worker wrote content to all its files, truncate all of them.
4. Review the worker prompt template. The prompt must include an explicit "DO NOT write any content" instruction.
5. If the worker repeats this error, add a strong negative example to the prompt: "WRONG: echo 'TODO' > file. CORRECT: touch file."

### FM5: Duplicate Placeholder — Two Workers Create the Same File

**Symptom:** Two placeholder files exist at the same path for the same locale. Both are zero bytes. The second `touch` overwrote the first with no visible conflict.

**Root cause:** Worker locale assignment overlap. Worker 1 (zh-CN, ja, ko) and Worker 2 (es, fr, de) both created files for `ja`. This should not happen if the orchestrator assigns locales correctly.

**Detection:** Quality gate G4 (Worker Reports). The orchestrator checks that each locale appears in exactly one worker report per batch. A locale appearing in two reports is a conflict.

**Recovery:**
1. Check which worker correctly assigned the locale. The fixed split is canonical.
2. Delete placeholders created by the wrong worker for that locale.
3. Verify the remaining placeholders match the expected count: `translatable_files × 1` per locale.
4. Fix the worker launch script. The locale assignment must be explicit and non-overlapping.
5. Prevention: the orchestrator writes the locale assignment into the prompt template. Workers do not choose locales.

### FM6: Git Conflict on catalog.md

**Symptom:** `git commit` fails because another orchestrator session committed to `translations/catalog.md` since the last pull.

**Root cause:** Two discovery sessions ran concurrently on different targets. Both tried to update the catalog.

**Detection:** Git reports a merge conflict on `translations/catalog.md`.

**Recovery:**
1. Run `git status` to confirm the conflict.
2. The catalog is append-only. Accept both entries. Merge the two versions by concatenating the new entries from both sessions.
3. Run `git add translations/catalog.md` and `git commit` with a merge message.
4. If the conflict is complex, regenerate the catalog from disk state:
   ```bash
   find translations/ -type f -not -name "catalog.md" | sort > /tmp/actual-placeholders.txt
   ```
5. Rebuild the catalog from the actual file list.
6. Prevention: only one discovery orchestrator runs at a time. Check `.agents/state/TRANSLATIONS-PROGRESS.md` for active sessions before starting.

### FM7: Race Condition — Enrichment Adds Files During Discovery

**Symptom:** A discovery worker lists N files at time T1. Between T1 and placeholder creation at T2, an enrichment worker adds M new files. The discovery worker creates placeholders for N files, missing the M new files.

**Root cause:** Concurrent Agent #8 (Extension Worker) and Agent #9 (Translation Orchestrator) sessions. Both target overlapping directory trees.

**Detection:** The re-scan protocol catches this. Next discovery pass finds the M new files that were missed.

**Prevention:**
1. Before starting a discovery batch, check git log for recent commits to the target directory.
2. If commits occurred in the last 2 minutes, wait and re-check.
3. Coordinate via `.agents/feedback/exchange.md`. Post a message: "Agent #9 starting discovery on target N. Hold enrichment on this tree."
4. Agent #8 posts: "Enrichment complete on SCE/core/rules/. Discovery may proceed."

### FM8: Worker Skips a File That Should Be Translatable (False Negative)

**Symptom:** A file that contains human-readable prose is incorrectly marked as SKIPPED. For example, a `.md` file with documentation is skipped with reason "generated data."

**Root cause:** Worker misapplied the decision tree. The file extension matched a skip pattern or the worker's reasoning was incorrect.

**Detection:** Quality gate G6 (No False Negative). The orchestrator spot-checks 20 percent of skipped files per batch.

**Recovery:**
1. Identify the false negative. Confirm the file contains translatable prose.
2. Create placeholders for the missed file across all 9 locales.
3. Add a note to the catalog: "Reclassified: <file> moved from SKIPPED to TRANSLATABLE after G6 spot-check."
4. If 3 or more false negatives occur in one batch, revise the translatability criteria in the worker prompt template.
5. Do not penalize the worker. False negatives are tolerated by design. Re-scans catch them.

### FM9: Worker Creates Wrong Number of Placeholders

**Symptom:** Worker report says DISCOVERED: 6 files, TRANSLATABLE: 5 files, CREATED: 12 placeholders. Expected: 5 × 3 locales = 15 placeholders. Mismatch of 3.

**Root cause:** Worker missed one locale during file creation. Or worker double-counted a file. Or worker created placeholders for a skipped file.

**Detection:** Report validation. The orchestrator checks `CREATED = TRANSLATABLE × 3`.

**Recovery:**
1. Count actual placeholders on disk: `find translations/<locale>/<target>/ -type f | wc -l`
2. Compare against the worker report. Identify which locales are missing files.
3. Create the missing placeholders manually or re-launch a single-locale worker for the gap.
4. Update the catalog with the corrected count.
5. Flag the worker for review. If the worker consistently miscounts, the prompt template may be unclear about the multiplier.

---

## Dependency Map

What must exist before discovery can start:

```
Source files on disk:
  ste-code/artifacts/          ─┐
  ste-code/adapted/             │
  SCE/narratives/system-prompts/│
  SCE/narratives/examples/      │
  SCE/core/rules/               ├── Source content (produced by pipeline stages)
  ste-code/v2/narratives/...    │
  ste-code/v2/core/rules/       │
  SCE/compute/prompts/          │
  ste-code/v2/compute/prompts/ ─┘
                                 │
Reference documents:             │
  .agents/agent/agent-9-translations.md ─┤
  .agents/skills/translations/SKILL.md    ├── Orchestrator instructions
  .agents/references/worker-rails.md      │
  .agents/references/quality-checklist.md ─┘
                                 │
Infrastructure:                  │
  translations/ (empty root)    ─── Output root directory
  .agents/state/TRANSLATIONS-PROGRESS.md ─── Progress tracker
  .agents/feedback/exchange.md  ─── Communication channel
```

What discovery produces:

```
translations/
├── catalog.md                  ─── Auto-generated inventory
├── zh-CN/                      ─┐
│   ├── ste-code/artifacts/      │
│   ├── ste-code/adapted/        │
│   └── ...                      ├── 9 locale trees
├── ja/ (same structure)         │   with blank placeholders
├── ...                          │
└── ar/ (same structure)        ─┘
                                 │
.agents/state/TRANSLATIONS-PROGRESS.md ─── Updated progress tracker
.agents/references/translation-grid.md ─── Updated grid (this document)
```

---

## Version History

| Version | Date | Author | Change | Rationale |
|---------|------|--------|--------|-----------|
| 1.0 | 2025-07-25 | Agent #9 (Translation Orchestrator) | Initial grid — 10 discovery targets, expected file counts, skip list, placeholder layout, batch-of-3 worker assignments, re-discovery protocol | First draft for discovery-based translation scaffolding |
| 1.1 | 2025-07-30 | Hermes (maturity audit) | Added cross-reference index (6 documents depended on, 4 documents extended, 3 documents driven). Added 9 edge cases (EC1-EC9) covering missing directories, unknown file types, conflicting translations, growing directories, orphaned placeholders, RTL paths, nested structures, mixed content, and all-skippable targets. Added 9 failure modes (FM1-FM9) covering encoding errors, path mismatches, timeouts, content-in-placeholder, duplicates, git conflicts, race conditions, false negatives, and count mismatches. Added discovery records section with format and example. Added status legend with 6 states (Pending, In Progress, Complete, Partial, Failed, Re-scan Needed). Added dependency map. Added version history block. Expanded discovery targets table with Files Expected, Files Found, and Notes columns. Linked targets 1 and 5-8 to STE-CODE-IMPLEMENTATION.md GATE 4 and granular-strategy.md batch-of-3 pattern. | Maturity audit found the grid was theoretical-only with no operational guardrails. These additions make the grid a working operational document. |
