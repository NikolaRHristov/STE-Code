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

### Adapted Output Example

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

> **Non-STE:** Execute the script to do the task.
> **STE:** Run the script to do the task.

> *Adapted from spec example: "The word 'use' is an approved verb in the dictionary."*
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

### Non-Negotiable Rules

- Every adapted rule MUST reference its original rule number from master.md
- Every synonym MUST trace to master.md's synonym table
- Every category MUST match one of the 19 from master.md
- Every example MUST be an adaptation of a real STE/non-STE pair from the extracted spec
- No invented code terms without a master.md source
- 19 categories (NOT 22), deepseek-v4-pro (NOT deepseek-pro or deepseek-v4-flash)

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

NOTE: If 3 or more rules are marked `⚠️ SOURCE-MISSING`, stop adaptation. The master.md is not complete enough to proceed. Report all missing rule numbers.

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

## Performance Considerations

Adaptation and artifact generation are compute-intensive. Plan for these estimates.

### Stage 4 Estimates

| Metric | Per Rule | Total (57 rules) |
|--------|---------|-------------------|
| Time | 1–3 minutes | 2–5 hours |
| Tokens (input) | ~3,000 | ~170,000 |
| Tokens (output) | ~1,500 | ~85,000 |
| Tokens (total) | ~4,500 | ~255,000 |

NOTE: These are estimates for deepseek-v4-pro. Actual performance depends on rule complexity. Rules with many sub-sections (Section 1, Section 3) take longer than simple rules (Section 9, GR rules).

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

## Rails (8 Guardrails)

| Rail | Rule |
|------|------|
| R1 | Write ONLY to `ste-code/adapted/` and `ste-code/artifacts/`. Never touch earlier stages. |
| R2 | Naming: `a-secN-ruleY.Z.md` for adaptation, `ste-code-<name>.txt` for artifacts |
| R3 | NEVER claim a file complete until it EXISTS on disk with real content (>30 lines) |
| R4 | Every claim backed by source data from master.md. No fabrication. |
| R5 | `#` page, `##` section, `###` rule, `####` dictionary. Blank line after every heading. |
| R6 | 19 categories, deepseek-v4-pro, 53 rules + 4 GR. Never claim otherwise. |
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

## Known Limitations

These limitations are inherent to the pipeline. They are not bugs.

1. **Adaptation quality depends on master.md completeness.** Gaps in the merged spec will propagate to adapted rules. If a rule's source pages are incomplete, the adaptation will also be incomplete. Always verify master.md before starting adaptation.

2. **Code-domain examples are derived, not original.** Every code-domain example is an adaptation of an aerospace example from ASD-STE100 Issue 9. The code-domain vocabulary is limited to what the aerospace examples can map to. Some code-specific scenarios (async await, TypeScript generics, Rust lifetimes) have no aerospace analog and cannot be directly adapted. Extension workers fill these gaps in a later phase.

3. **The 19 categories are a remapping, not a redesign.** The category architecture comes directly from ASD-STE100 Issue 9 pages 47–52. The STE-Code categories are the closest code-domain equivalents. Some categories map imperfectly: "Parts of the body" → "UI/UX interaction terms" is an analogical mapping, not a literal one.

4. **Dictionary adaptation is partial.** The full ASD-STE100 dictionary has 5,943 lines. Only approved words with direct code-domain equivalents are adapted. Words like "aircraft," "fuselage," and "landing gear" have no code-domain analog and are not adapted.

5. **Token budgets are approximate.** Actual token counts vary by model tokenizer. deepseek-v4-pro tokenization differs from GPT-4 or Claude tokenization. Budgets are guidelines, not hard limits. Validate with the target model when precision matters.

6. **The pipeline produces Level 4 output (~50K tokens).** Lower levels (1–3) are extracted subsets of the Level 4 output. Higher levels (5) require extension workers to fill code-domain gaps. This orchestrator produces Level 4 only.

7. **No automatic verification of code-domain correctness.** The validation checks structure (line count, rule presence) but not semantic correctness of the code-domain examples. A human reviewer must check that code examples are idiomatic and correct for the target language.

8. **Single-pass adaptation. No iterative refinement.** Each rule is adapted once from its master.md source. If the adaptation produces a poor result, the orchestrator fixes it immediately (R8) but does not re-read and re-adapt the rule from scratch. Complex rules may need manual review.

## Scratch Warning

Premature adaptation files exist in `.agents/_scratch/`. They were created before
extraction completed and moved there by RAILS. **Do NOT reuse them.** Regenerate
everything from `ste-code/merged/master.md`.

## Immutable Facts

- 19 technical noun categories (NOT 22)
- 53 writing rules + 4 GR rules (NOT 65)
- Model: deepseek-v4-pro (NOT deepseek-pro or deepseek-v4-flash)
- 434 pages in ASD-STE100 Issue 9
- Output: .md for adaptation, .txt for artifacts

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
