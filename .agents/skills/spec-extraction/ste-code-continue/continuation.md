# Agent #3 — Continued Orchestrator

You are the STE-Code Continued Orchestrator. Stages 1–3 are DONE — verified by the
execution auditor (see `.agents/audit/` for reports). Your job: drive Stages 4
(adaptation) and 5 (artifacts) to completion.

```
STAGE 1 — EXTRACT   ✅ 109/109  (912K, 10,927 lines in ste-code/extracted/)
STAGE 2 — REFINE     ✅ 109/109  (916K, 21,852 lines in ste-code/refined/)
STAGE 3 — MERGE      ✅ Ready    (ste-code/merged/master-raw.md + master.md, 708K)
STAGE 4 — ADAPT      ⬜ 0 files  (ste-code/adapted/ is empty — YOU START HERE)
STAGE 5 — ARTIFACTS  ⬜ 0 files  (ste-code/artifacts/ is empty — after adaptation)
```

## Verify State (do not skip)

```bash
find ste-code/extracted -name 'w*-p*.md' -type f | wc -l   # Must be 109
find ste-code/refined -name 'r*.md' -type f | wc -l         # Must be 109
ls ste-code/merged/                                          # Must show master-raw.md + master.md
head -5 ste-code/merged/master.md                            # Must show "ASD-STE100 Issue 9"
mkdir -p ste-code/adapted ste-code/artifacts
```

If any check fails, STOP. Report the discrepancy. Do not fabricate.

## Prerequisite Reading

1. `.agents/MASTER.md` — Full mission plan and launch protocol
2. `.agents/skills/spec-extraction/references/rails.md` — 8 guardrails
3. `.agents/skills/spec-extraction/ste-code-adaptation/SKILL.md` — Adaptation protocol
4. `.agents/skills/spec-extraction/ste-code-artifacts/SKILL.md` — Artifact protocol
5. `.agents/skills/spec-extraction/ste-code-validate/SKILL.md` — Validation protocol
6. `.agents/skills/spec-extraction/ste-code-adaptation/references/category-mapping.md` — 19 categories

## Stage 4 — Adaptation

Read `ste-code/merged/master.md` (structural index). Use it to find which files contain
each rule, category, and dictionary entry. Produce adaptation files in `ste-code/adapted/`.

### Output

1. **All 53 writing rules** (1.1–9.4 + GR1–GR4) with code-domain examples:
   ```
   ste-code/adapted/a-sec1-rule1.1.md through a-sec9-gr4.md
   ```

2. **19 technical noun categories** — remapped per `category-mapping.md`

3. **Synonym table** — every canonical pair gets a code-domain equivalent

4. **Polysemy resolution table** — every entry adapted

5. **Dictionary entries** — approved words with code-domain equivalents in `a-dictionary.md`

### File Naming Convention

```
a-sec{N}-rule{Y}.{Z}.md    — adapted rule (e.g., a-sec1-rule1.1.md, a-sec3-rule3.2.md)
a-sec{N}-gr{M}.md           — adapted general recommendation (e.g., a-sec6-gr1.md)
a-category-{N}.md            — adapted category (e.g., a-category-1.md through a-category-19.md)
a-synonym.md                 — canonical synonym table with code-domain equivalents
a-polysemy.md                — polysemy resolution table
a-dictionary.md              — approved word dictionary (~5,943 lines)
```

### Adapted Output Example — Rule File

Each adaptation file follows this structure. Use this as the template for all 57 files.

#### File: `ste-code/adapted/a-sec1-rule1.1.md`

```markdown
# Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.1

## Original Rule

**Rule 1.1** Use words that are:
- Approved in the dictionary
- Technical nouns
- Technical verbs.

[Original rule text from master.md — preserved verbatim]

## STE-Code Adaptation

**Rule 1.1** In code documentation, use words that are:
- Approved in the project controlled terminology
- Code-domain technical nouns
- Code-domain technical verbs.

[Adapted rule text — every STE concept replaced with code-domain equivalent]

### Examples

[Each example is an adaptation of a real STE/non-STE pair from the extracted spec.
The format is: code-domain scenario → BEFORE (non-STE) → AFTER (STE-Code)]

#### Code-Domain Example 1

[Brief code scenario description — 1 sentence]

> **Non-STE:** Execute the script to do the task.
> **STE:** Run the script to do the task.

> *Adapted from spec example: "The word 'use' is an approved verb in the dictionary."*

#### Code-Domain Example 2

[Brief code scenario description — 1 sentence]

> **Non-STE:** Utilize the library to parse JSON.
> **STE:** Use the library to parse JSON.

> *Adapted from spec example: "Use approved words from the dictionary instead of non-approved synonyms."*

#### Code-Domain Example 3 — Dictionary Entry

[If this rule covers specific dictionary words, add a #### section for each word]

#### Word: "use"

| Property | Value |
|----------|-------|
| **STE approved** | Yes (verb) |
| **STE non-approved** | utilize (v), leverage (v), employ (v) |
| **Code-domain equivalent** | A function calls a utility. A module imports a library. |
| **Code example (non-STE)** | The application leverages Redis for caching. |
| **Code example (STE-Code)** | The application uses Redis for caching. |
```

#### Heading Structure (All Files)

The heading hierarchy is fixed:

```
# — page title (the rule number and name)
## — major section (Original Rule, STE-Code Adaptation, Examples, Category Mapping)
### — sub-section (individual example groups, category groups)
#### — dictionary entry (individual approved/unapproved word entries)
```

Always include a blank line after every heading.

#### Required Elements Per Rule File

- Source reference to ASD-STE100 Issue 9 rule number (line 2)
- Original rule text verbatim from master.md
- STE-Code adapted rule text
- At least 2 code-domain examples adapted from spec pairs
- Each example marked with `> *Adapted from spec example: ...*`
- At least 1 dictionary-level entry (####) if the rule covers specific words

#### Category Files

Each of the 19 category files uses this format:

```markdown
# Category N — [Category Name]

> **Source:** Adapted from ASD-STE100 Issue 9, Technical Noun Category N
> **Category mapping:** `references/category-mapping.md`

## Original Category

[Category definition from master.md — preserved verbatim]

## STE-Code Category Remap

[Category name adapted for code domain per category-mapping.md]

### Representative Examples

- `example1` — [explanation]
- `example2` — [explanation]
```

#### Synonym Table File

Each canonical pair maps to a code-domain pair:

```markdown
# Synonym Table — STE-Code Adaptation

> **Source:** Adapted from ASD-STE100 Issue 9, Dictionary Part 2 Synonym Entries

## Canonical Synonym Table

| Prefer | Avoid |
|--------|-------|
| use | utilize, leverage, employ |
| start | initiate, commence, bootstrap |
...

## Code-Domain Equivalents

| STE Canonical | Code-Domain Scenario |
|---------------|---------------------|
| use | A function calls a utility. Say "use" instead of "leverage". |
| start | A server begins. Say "start" instead of "bootstrap". |
...
```

#### Polysemy Resolution Table File

Every polysemy entry from master.md gets a code-domain resolution. The file identifies words with two meanings and specifies which domain each meaning applies to.

```markdown
# Polysemy Resolution Table — STE-Code Adaptation

> **Source:** Adapted from ASD-STE100 Issue 9, Dictionary Part 1 Polysemy Entries

## Original Polysemy Table

| Word | Part of Speech | Meaning 1 | Meaning 2 |
|------|---------------|-----------|-----------|
| close | verb / adjective | to shut | near |
| ... | ... | ... | ... |

## STE-Code Resolution

| Word | Code-Domain Meaning 1 | Code-Domain Meaning 2 | Resolution Rule |
|------|----------------------|----------------------|-----------------|
| close | Close a file handle or connection. | A value near a threshold. | Use only as a verb for resource cleanup. Use "near" for proximity. |
| ... | ... | ... | ... |

### Resolution Patterns

Each polysemy word follows one of these patterns:

1. **Verb restriction.** Use the word only as its approved part of speech. The other meaning uses a different word. Example: "close" → verb only. "near" replaces the adjective meaning.
2. **Domain split.** Meaning 1 applies to code structure. Meaning 2 applies to runtime behavior. Use the correct meaning for each domain. Example: "run" → execute code (verb) vs. a sequence of operations (noun, use "workflow").
3. **Context signal.** The word has one meaning in code documentation. The other meaning is not used. Document both meanings. Mark the unused meaning as "not applicable to code domain."

### Unresolved Polysemy Entries

Entries that have no clear code-domain resolution:

| Word | Issue | Status |
|------|-------|--------|
| *(filled during adaptation)* | — | — |
```

#### Dictionary Entry File

The full approved word dictionary adapts every entry from master.md:

```markdown
# Approved Word Dictionary — STE-Code Adaptation

> **Source:** Adapted from ASD-STE100 Issue 9, Dictionary Part 1 (Approved Words)
> **Entries:** ~5,943 lines from master.md
> **Coverage:** Approved words with code-domain equivalents only. Aerospace-specific words without code-domain analogs are not adapted.

## Reading Guide

Each entry has this structure:

#### Word: "accept"

| Property | Value |
|----------|-------|
| **Part of speech** | verb (TECHNICAL VERB) |
| **Approved STE meaning** | To agree to receive (TECHNICAL) |
| **NOT approved STE meaning** | To agree, to say yes (NON-TECHNICAL) |
| **Code-domain equivalent** | A function accepts an argument. A server accepts a connection. |
| **Code example (STE-Code)** | The `handleRequest` function accepts a `Request` object and returns a `Response`. |
| **Code example (non-STE)** | The callback receives and processes the user input. → The handler accepts the input and returns the result. |

## Dictionary

[5,943 lines of adapted word entries — each word from master.md that has a code-domain equivalent]
```

### Non-Negotiable Rules

- Every adapted rule MUST reference its original rule number from master.md
- Every synonym MUST trace to master.md's synonym table
- Every category MUST match one of the 19 from master.md
- Every example MUST be an adaptation of a real STE/non-STE pair from the extracted spec
- No invented code terms without a master.md source
- 19 categories (NOT 22), poolside/laguna-s-2.1:free (NOT deepseek-pro or deepseek-v4-flash)

### Stage 4 Failure Modes

These failures can occur during adaptation. Check for each condition.

| Failure Mode | Symptoms | Recovery |
|-------------|----------|----------|
| master.md corrupted or truncated | Missing rule sections. Unexpected EOF. Checksum mismatch. | STOP. Report the exact offset and missing rule numbers. Run the merge stage again. Do not fabricate missing content. |
| Rule source pages not found | A rule in master.md has a page reference that does not exist in `ste-code/extracted/` or `ste-code/refined/`. | Search for the rule text with `search_files` across `ste-code/refined/`. If found, note the corrected page reference. If not found, mark the rule as `⚠️ SOURCE-MISSING` and skip it. Continue with rules that have sources. |
| master.md references non-existent extracted file | A file reference points to a path that does not exist on disk. | Verify with `ls ste-code/extracted/<path>`. If missing, trace back to the refinement stage. Re-run refinement for that batch if possible. |
| Adaptation produces < 30 lines per file | The adapted file is a stub or has no real content. | Delete the file and regenerate from master.md. Check that the rule's source pages contain enough content to adapt. |
| Category count differs from 19 | master.md lists more or fewer than 19 categories. | Verify against `category-mapping.md`. If master.md is wrong, use the mapping file as the source of truth and note the discrepancy. |
| Synonym table incomplete | Some canonical pairs in master.md have no code-domain equivalent produced. | For each missing pair: search the spec for usage examples, then derive the code-domain equivalent from those examples. If no spec example exists, mark the pair as `⚠️ NO-EXAMPLE` and skip. |
| Polysemy entries missing | master.md polysemy table has entries but no adapted output is produced. | Each polysemy entry must have a code-domain resolution: state the two meanings and which domain each applies to. Do not skip polysemy entries. |
| Deeply nested spec structure | A rule spans 50+ pages or 10+ sub-sections. | Split the adaptation into multiple files: `a-secN-ruleY.Z.md`, `a-secN-ruleY.Z-pt2.md`, etc. Cross-reference them. |
| Fabrication detected | An adapted file contains code terms not found anywhere in master.md or the extracted spec. | Delete the file immediately. Regenerate from master.md only. Document the incident in PROGRESS.md. |
| Context window exhausted mid-rule | The adaptation process stops before a rule is complete. The output file ends with a partial sentence or truncated markdown. | Identify the break point in the partial output. Restart adaptation from the last completed heading (### or ####). Do not reuse the partial file — start fresh for that rule. If the rule is too large for a single pass, split it per the "deeply nested spec structure" recovery above. |
| Circular rule reference | Rule A's adaptation references Rule B, and Rule B's adaptation references Rule A. Neither can be completed first. | Adapt Rule A with a placeholder: `[See adapted Rule B — adaptation pending]`. Adapt Rule B. Return to Rule A and replace the placeholder with the real reference. Document the circular dependency in PROGRESS.md. |
| Semantic fabrication | An adapted file contains correct structure (headings, line count, references) but the code-domain meaning is wrong. Example: a synonym mapping claims "initiate → start" is a file I/O concept when it is a process lifecycle concept. | Cross-check 3 random examples per file against the original spec pages. If any are wrong, re-read the spec page and re-adapt that rule. Spot-check is the only defense — no automated tool detects semantic drift. |
| Heading structure deviation | An adapted file uses `##` where `###` is required, or omits the `####` level for dictionary entries. | Verify against the heading hierarchy in this document. Fix the file. Re-check with `grep '^#' ste-code/adapted/<file>`. |
| Dictionary entry without code-domain equivalent | An approved STE word (e.g., "aircraft") has no code-domain analog. The agent fabricates a forced equivalent. | If a word has no code-domain analog, skip it. Write `⚠️ NO-CODE-EQUIVALENT — aerospace term` in the dictionary entry. Do not force a mapping. Only words with genuine code-domain uses are adapted. |

NOTE: If 3 or more rules are marked `⚠️ SOURCE-MISSING`, stop adaptation. The master.md is not complete enough to proceed. Report all missing rule numbers.

### Adaptation Batch Strategy

Process adaptations in batches of 10 rules. This strategy prevents errors from propagating across all 57 files and allows early validation.

1. Select 10 rules by section priority: Section 1 first, then Section 3, then Section 4, then Sections 2, 5, 6, 7, 8, 9, and GR rules.
2. Adapt each rule one at a time. Write the file to `ste-code/adapted/`.
3. Validate the batch: check line counts, rule references, and source tracing for all 10 files.
4. Update PROGRESS.md for all 10 rules.
5. Commit the batch with: `git add ste-code/adapted/ .agents/state/PROGRESS.md && git commit -m "adapt: rules <range> (batch N/M)"`.
6. Continue with the next batch.

#### Batch Sequence

| Batch | Rules | Risk |
|-------|-------|------|
| 1 | 1.1 | High — largest rule, many examples |
| 2 | 1.2 through 1.9 | Medium — dictionary-dependent rules |
| 3 | 3.1 through 3.7 | Medium — complex grammar rules |
| 4 | 4.1 through 4.6 | High — procedural writing, many examples |
| 5 | 2.1 through 2.4 | Low — short rules |
| 6 | 5.1 through 5.7 | Medium — procedural conventions |
| 7 | 6.1 through 6.7 + GR1, GR2 | Low — shorter rules |
| 8 | 7.1 through 7.3 + GR3, GR4 | Low — short rules |
| 9 | 8.1 through 8.6 | Medium — dictionary-dense rules |
| 10 | 9.1 through 9.4 + categories 1–10 | Medium — categories |
| 11 | Categories 11–19 + synonym table + polysemy table | Medium — final adaptation files |
| 12 | Dictionary (a-dictionary.md) | Critical — largest file, split into segments |

Schedule bottleneck rules (1.1, 3.1, Section 4) in the first 4 batches. Do not leave them for the end. If a batch takes more than 30 minutes, pause and run per-file validation before continuing.

### Resume Protocol

If the adaptation process stops before completion, do not restart from the beginning.

1. Count completed files: `find ste-code/adapted -name 'a-*.md' -type f | wc -l`.
2. Identify the last completed rule from PROGRESS.md: `grep '✅' .agents/state/PROGRESS.md | tail -1`.
3. Verify the last 3 adapted files are valid (>30 lines, correct heading structure).
4. If any of the last 3 files are invalid, delete them. Re-adapt those rules.
5. If the last file is a partial write (ends with truncated markdown), delete it. Re-adapt that rule.
6. Continue with the next uncompleted rule from the batch sequence above.

NOTE: Never skip to Stage 5 after a resume without running the full verification sweep on all adapted files.

## Stage 5 — Artifacts

After all adaptation files exist, generate 6 artifact files in `ste-code/artifacts/`:

| # | File | Target |
|---|------|--------|
| 1 | ste-code-distilled-system-prompt.txt | ~1,200 tokens |
| 2 | ste-code-self-reading-manual.txt | ~7,000 tokens |
| 3 | ste-code-extraction-methodology.txt | ~1,400 tokens |
| 4 | ste-code-example-turn.txt | ~500 tokens |
| 5 | ste-code-deployment-guide.txt | ~1,800 tokens |
| 6 | README.md | ~500 tokens |

Full specs in `ste-code-artifacts/SKILL.md`.

### Stage 5 Failure Modes

These failures can occur during artifact generation.

| Failure Mode | Symptoms | Recovery |
|-------------|----------|----------|
| Adaptation incomplete when artifact generation starts | Fewer than 57 adaptation files exist. Some rule numbers are missing. | STOP. Complete all adaptation files first. Count with: `find ste-code/adapted -name 'a-*.md' -type f | wc -l`. Must be at least 57. |
| Token budget exceeded | An artifact file is larger than its target by 20% or more. | Trim examples first. Then trim explanatory text. Keep all rule references. If still over budget, split the artifact into a primary file and an appendix file. |
| Token budget far below target | An artifact file is less than 50% of its target size. | Check that all required sections per SKILL.md are present. Add missing sections before declaring the file complete. |
| Artifact references missing adaptation file | An artifact cites a rule that has no adaptation file. | Verify the adaptation file exists: `ls ste-code/adapted/a-secN-ruleY.Z.md`. If missing, go back to Stage 4 and adapt that rule. |
| Cross-reference mismatch | An artifact cites "65 rules" instead of "53 rules" or "22 categories" instead of "19 categories". | Fix the number. Use only the immutable facts from this document. |
| File encoding issue | An artifact contains non-ASCII characters that cause parsing failures. | Re-save as UTF-8. Strip BOM if present. Verify with `file ste-code/artifacts/<name>`. |
| Artifact 2 (self-reading manual) missing sections | Fewer than 8 sections (S0–S8) present. | Each section is mandatory. If a section has no content, write a placeholder with the heading and a NOTE listing what source data is needed. |
| Fabrication in artifacts | An artifact contains a claim not backed by any adaptation file or master.md. | Delete the claim. Trace every assertion to a specific source file. If no source exists, remove the assertion. |
| Cross-artifact terminology mismatch | Artifact 1 uses "code-domain technical nouns" but Artifact 2 uses "technical code nouns" for the same concept. Or artifact token estimates disagree with each other. | Standardize on the terminology from this continuation document. Search all 6 artifacts for the inconsistent term with `search_files`. Fix all occurrences to match. |
| Artifact ordering dependency failure | Artifact 2 (manual) references Artifact 1 (system prompt) for its S0 section, but Artifact 1 has not been generated yet. | Generate artifacts in order: 1 → 2 → 3 → 4 → 5 → 6. Each artifact may reference earlier artifacts. Never reference a later artifact from an earlier one. If Artifact 6 (README) must reference all artifacts, generate it last. |
| System prompt parse failure | Artifact 1 (system prompt) uses markdown code fences that would break when embedded in a larger prompt. Or it contains unescaped special characters. | Test the system prompt by embedding it in a test prompt. If parsing fails, replace triple-backtick code fences with indented code blocks. Escape any `>` characters that appear at line starts. |
| Artifact token count miscalculation | The artifact's token count was estimated with a generic 4 chars/token rule but poolside/laguna-s-2.1:free tokenization produces 15% more tokens for the same text. | After all artifacts are written, run them through a token counter: `wc -c` gives char count. Multiply by 0.29 for a conservative poolside/laguna-s-2.1:free token estimate. Re-trim if needed. |

BREAKING: Do not generate artifacts if fewer than 57 adaptation files exist. The artifact quality depends on complete adaptation coverage.

### Artifact Verification

After all 6 artifacts are written, run this verification:

```bash
for f in ste-code/artifacts/ste-code-*.txt ste-code/artifacts/README.md; do
  if [ ! -f "$f" ]; then
    echo "MISSING: $f"
  else
    chars=$(wc -c < "$f")
    lines=$(wc -l < "$f")
    echo "$(basename $f): $lines lines, $chars chars ~$((chars/4)) tokens"
  fi
done
```

Expected minimums:
- System prompt: 30+ lines, ~4,800 chars
- Manual: 200+ lines, ~28,000 chars
- Methodology: 80+ lines, ~5,600 chars
- Example: 30+ lines, ~2,000 chars
- Deployment: 100+ lines, ~7,200 chars
- README: 25+ lines, ~2,000 chars

### Cross-Artifact Consistency Checks

After all 6 artifacts pass individual verification, run these cross-artifact checks:

1. **Rule count consistency.** Every artifact that mentions a rule count must say "53 writing rules + 4 GR rules." Search with: `grep -n 'rule' ste-code/artifacts/*.txt ste-code/artifacts/README.md`.
2. **Category count consistency.** Every artifact must cite "19 categories." Search with: `grep -n 'categor' ste-code/artifacts/*.txt ste-code/artifacts/README.md`.
3. **Model name consistency.** Every artifact must use "poolside/laguna-s-2.1:free." Search with: `grep -n 'deepseek' ste-code/artifacts/*.txt ste-code/artifacts/README.md`.
4. **Terminology alignment.** The terms "code-domain technical noun," "code-domain technical verb," and "project controlled terminology" must be used consistently. Search for variants like "technical code noun" or "code technical noun" and fix them.
5. **Cross-reference validity.** If Artifact 2 says "see Section 3.1 of the system prompt," verify that Artifact 1 actually has a Section 3.1 with that content.
6. **Level consistency.** If any artifact mentions adaptation levels (1–5), verify the level descriptions match the definitions in `.agents/AGENTS.md`.

Document all fixes in PROGRESS.md.

## Performance Considerations

Adaptation and artifact generation are compute-intensive. Plan for these estimates.

### Stage 4 Estimates

| Metric | Per Rule | Total (57 rules) |
|--------|---------|-------------------|
| Time | 1–3 minutes | 2–5 hours |
| Tokens (input) | ~3,000 | ~170,000 |
| Tokens (output) | ~1,500 | ~85,000 |
| Tokens (total) | ~4,500 | ~255,000 |

NOTE: These are estimates for poolside/laguna-s-2.1:free. Actual performance depends on rule complexity. Rules with many sub-sections (Section 1, Section 3) take longer than simple rules (Section 9, GR rules).

### Stage 5 Estimates

| Metric | Per Artifact | Total (6 artifacts) |
|--------|-------------|---------------------|
| Time | 3–8 minutes | 30–50 minutes |
| Tokens (input) | ~8,000 | ~48,000 |
| Tokens (output) | ~3,000 | ~18,000 |
| Tokens (total) | ~11,000 | ~66,000 |

### Combined Estimates

| Metric | Stage 4 | Stage 5 | Total |
|--------|---------|---------|-------|
| Time | 2–5 hours | 0.5–1 hour | 2.5–6 hours |
| Tokens | ~255,000 | ~66,000 | ~321,000 |

NOTE: Run adaptation in batches of 10 rules with validation between batches. This catches errors early and prevents large-scale rework.

### Bottleneck Rules

These rules take the most time because of their size and complexity:

1. **Rule 1.1** (approved words) — ~3,900 chars output, many examples
2. **Rule 3.1** (sentence structure) — many sub-rules, complex grammar
3. **Section 4 rules** (procedural writing) — 6 sub-rules, many example pairs
4. **Dictionary entries** — 5,943 lines of approved/unapproved words

Schedule these rules early in the batch sequence. Do not leave them for the end.

### Memory and Context Window Constraints

poolside/laguna-s-2.1:free has a 128K token context window. Some rules need special handling because the source material plus the adaptation output approaches this limit.

| Rule | Estimated Input Tokens | Output Tokens | Total | Risk |
|------|----------------------|---------------|-------|------|
| Rule 1.1 (approved words) | ~15,000 | ~4,000 | ~19,000 | Medium — many dictionary references |
| Rule 3.1 (sentence structure) | ~12,000 | ~3,500 | ~15,500 | Medium — complex grammar rules |
| Section 4 (procedural writing) | ~25,000 | ~6,000 | ~31,000 | High — 6 sub-rules, many examples |
| Rule 8.x (dictionary-dense) | ~18,000 | ~4,500 | ~22,500 | Medium — many word-level entries |
| Dictionary (a-dictionary.md) | ~60,000 | ~25,000 | ~85,000 | Critical — the single largest file |

For rules that exceed 25,000 total tokens:
1. Split the source material into logical segments (by sub-section or by page range).
2. Adapt each segment separately. Write to `a-secN-ruleY.Z-pt1.md`, `a-secN-ruleY.Z-pt2.md`.
3. Merge the segments into a single file after all segments are adapted.
4. Verify the merged file has no duplicate headings and no broken cross-references.

For the dictionary (a-dictionary.md):
- Process in segments of 500 lines from master.md.
- Adapt each segment independently.
- Concatenate segments in order. Do not attempt to merge dictionary entries — each entry is self-contained.
- Verify the final file has exactly the expected number of entries.

### Token Budget Optimization

To stay within token budgets for artifacts:

1. Trim examples before explanatory text. Examples are the most token-dense content.
2. Remove redundant cross-references. If Artifact 2 and Artifact 3 both explain the same concept, keep the explanation in the more comprehensive artifact and reference it from the other.
3. Use compact table formats instead of bullet lists for structured data.
4. Keep all rule numbers and category references. Trim only the commentary around them.
5. If an artifact exceeds budget by more than 20% after trimming, split into a primary file and an appendix file. Name the appendix `ste-code-<name>-appendix.txt`.
6. Verify the appendix with: `wc -c ste-code/artifacts/ste-code-<name>-appendix.txt`. The appendix should be less than 50% of the primary file size. If larger, the split point is wrong — move more material to the primary file.

## Rails (8 Guardrails)

| Rail | Rule |
|------|------|
| R1 | Write ONLY to `ste-code/adapted/` and `ste-code/artifacts/`. Never touch earlier stages. |
| R2 | Naming: `a-secN-ruleY.Z.md` for adaptation, `ste-code-<name>.txt` for artifacts |
| R3 | NEVER claim a file complete until it EXISTS on disk with real content (>30 lines) |
| R4 | Every claim backed by source data from master.md. No fabrication. |
| R5 | `#` page, `##` section, `###` rule, `####` dictionary. Blank line after every heading. |
| R6 | 19 categories, poolside/laguna-s-2.1:free, 53 rules + 4 GR. Never claim otherwise. |
| R7 | Update `.agents/state/PROGRESS.md` after EVERY completed file. |
| R8 | Fix mistakes immediately. Document what happened. |

## 🔴 MANDATORY: Progress Tracking

The extraction and refinement orchestrators executed at 100% but tracked at 0%.
The auditor had to fix PROGRESS.md 3 times. **Do not repeat this.**

After every adaptation file:

1. Update `.agents/state/PROGRESS.md` — flip the rule's checkbox to `✅`
2. `git add` and `git commit` with descriptive message
3. Verify: `grep '✅' .agents/state/PROGRESS.md | wc -l` should increase

## Validation

Run after each batch of 10 rules:

1. **Per-file**: Line count > 30, no fabrication signals, correct rule references
2. **Spot-check**: 3 adaptations against original spec pages
3. **Full sweep**: After all 53 rules, verify all rule numbers present

Run after all adaptation files complete:

4. **Category sweep**: Verify 19 category files exist with `find ste-code/adapted -name 'a-category-*.md' | wc -l`
5. **Dictionary sweep**: Verify `a-dictionary.md` exists and has >1,000 lines
6. **Synonym sweep**: Verify `a-synonym.md` exists and has a table with at least 10 rows
7. **Polysemy sweep**: Verify `a-polysemy.md` exists with content

### Semantic Quality Checks

Structure validation (line count, heading hierarchy) catches mechanical errors. Semantic quality checks catch meaning errors. Run these on 10% of adapted files (6 files from the 57).

1. **Source tracing.** Pick a random example from the adapted file. Find its original in `ste-code/refined/`. Verify the code-domain adaptation preserves the original meaning.
2. **Terminology consistency.** Search the adapted file for non-STE terms from the synonym table (utilize, leverage, initiate, etc.). If any appear in the adapted rule text itself, fix them.
3. **Example direction.** Each example must show a NON-STE (bad) pattern followed by an STE-Code (good) pattern. If the direction is reversed, the example teaches the wrong lesson.
4. **Category assignment.** Pick a random term from a category file. Verify it maps to the correct category per the decision table in `category-mapping.md`.
5. **Dictionary entry completeness.** Pick 3 random entries from `a-dictionary.md`. Verify each has: part of speech, approved meaning, non-approved meaning, code-domain equivalent, and at least 1 code example.
6. **No speculative entries.** Verify dictionary entries do not contain words absent from master.md. Every adapted word must have a source in the original ASD-STE100 dictionary.

### Cross-Referencing Protocol

After all adaptation files are written, verify cross-file consistency:

1. **Rule inter-reference.** If Rule 3.1 says "see Rule 1.1 for approved word requirements," verify that `a-sec1-rule1.1.md` exists and contains the referenced content.
2. **Category back-reference.** If a rule file references "Category 7 — Algorithmic terms," verify that `a-category-7.md` exists.
3. **Synonym cross-link.** If a dictionary entry says "see Synonym Table for full list," verify that `a-synonym.md` has the referenced synonyms.
4. **Polysemy cross-link.** If a word entry says "⚠️ POLYSEMY — see polysemy table," verify that `a-polysemy.md` has an entry for that word.

Fix broken cross-references immediately. A broken reference is worse than no reference — it misleads the reader.

## Known Limitations

These limitations are inherent to the pipeline. They are not bugs.

1. **Adaptation quality depends on master.md completeness.** Gaps in the merged spec will propagate to adapted rules. If a rule's source pages are incomplete, the adaptation will also be incomplete. Always verify master.md before starting adaptation.

2. **Code-domain examples are derived, not original.** Every code-domain example is an adaptation of an aerospace example from ASD-STE100 Issue 9. The code-domain vocabulary is limited to what the aerospace examples can map to. Some code-specific scenarios (async await, TypeScript generics, Rust lifetimes) have no aerospace analog and cannot be directly adapted. Extension workers fill these gaps in a later phase.

3. **The 19 categories are a remapping, not a redesign.** The category architecture comes directly from ASD-STE100 Issue 9 pages 47–52. The STE-Code categories are the closest code-domain equivalents. Some categories map imperfectly: "Parts of the body" → "UI/UX interaction terms" is an analogical mapping, not a literal one.

4. **Dictionary adaptation is partial.** The full ASD-STE100 dictionary has 5,943 lines. Only approved words with direct code-domain equivalents are adapted. Words like "aircraft," "fuselage," and "landing gear" have no code-domain analog and are not adapted.

5. **Token budgets are approximate.** Actual token counts vary by model tokenizer. poolside/laguna-s-2.1:free tokenization differs from GPT-4 or Claude tokenization. Budgets are guidelines, not hard limits. Validate with the target model when precision matters.

6. **The pipeline produces Level 4 output (~50K tokens).** Lower levels (1–3) are extracted subsets of the Level 4 output. Higher levels (5) require extension workers to fill code-domain gaps. This orchestrator produces Level 4 only.

7. **No automatic verification of code-domain correctness.** The validation checks structure (line count, rule presence) but not semantic correctness of the code-domain examples. A human reviewer must check that code examples are idiomatic and correct for the target language.

8. **Single-pass adaptation. No iterative refinement.** Each rule is adapted once from its master.md source. If the adaptation produces a poor result, the orchestrator fixes it immediately (R8) but does not re-read and re-adapt the rule from scratch. Complex rules may need manual review.

9. **Context window exhaustion risk for large rules.** Section 4 (procedural writing) and the dictionary file approach poolside/laguna-s-2.1:free's 128K context limit. Split adaptation into segments as described in "Memory and Context Window Constraints." If a rule cannot be split (tightly coupled content), the adaptation quality will degrade toward the end of the file as context compression increases.

10. **Model-specific tokenization differences.** The token budgets in this document use a 4 chars/token estimate. poolside/laguna-s-2.1:free's actual tokenizer produces approximately 3.5 chars/token for English prose and 2.8 chars/token for code-heavy text. Artifacts with many code examples will have more tokens than the char-based estimate suggests. Use the conservative 0.29 multiplier for final token verification.

11. **No l10n/i18n support.** All adapted content is produced in English (American spelling per Rule 1.14). The translation pipeline is a separate phase managed by the Translation Orchestrator (Agent #9). Do not attempt to adapt rules into other languages during Stage 4.

12. **Polysemy resolution is manual.** The polysemy table requires human judgment to determine which meaning applies to the code domain. Automated rules (verb restriction, domain split) handle common cases but edge cases need review. Mark unresolved entries clearly.

13. **Adaptation order affects quality.** Rules adapted later in the sequence benefit from terminology decisions made earlier. Rules adapted first (especially Rule 1.1) set the vocabulary standard. If a later rule introduces a term that conflicts with an earlier rule, re-adapt the earlier rule with R8.

## Scratch Warning

Premature adaptation files exist in `.agents/_scratch/`. They were created before
extraction completed and moved there by RAILS. **Do NOT reuse them.** Regenerate
everything from `ste-code/merged/master.md`.

## Immutable Facts

- 19 technical noun categories (NOT 22)
- 53 writing rules + 4 GR rules (NOT 65)
- Model: poolside/laguna-s-2.1:free (NOT deepseek-pro or deepseek-v4-flash)
- 434 pages in ASD-STE100 Issue 9
- Output: .md for adaptation, .txt for artifacts
- 128K token context window (poolside/laguna-s-2.1:free)
- Token multiplier for poolside/laguna-s-2.1:free: 0.29 (chars × 0.29 ≈ tokens)

## Start Now

```
Read .agents/skills/spec-extraction/ste-code-continue/continuation.md and execute.

1. Verify pipeline state (109 extracted, 109 refined, 2 merged)
2. Read master.md, adapt all 53 rules + 19 categories + synonym/polysemy tables
3. Write to ste-code/adapted/, update PROGRESS.md after every file
4. Generate 6 artifacts in ste-code/artifacts/
5. Validate everything. No fabrication. Update tracking.

Start with Rule 1.1 adaptation.
```
