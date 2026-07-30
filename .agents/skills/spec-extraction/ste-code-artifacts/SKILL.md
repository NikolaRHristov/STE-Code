---
name: ste-code-artifacts
description: "Generate the 6 STE-Code artifact files from the master extraction state, following the adaptation protocol."
version: 1.0.1
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [ste-code, artifacts, generation, system-prompt, manual]
---

# STE-Code Artifact Generation

## Overview

> **RAILS**: Validate every action against `references/rails.md` — 8 immutable guardrails.

After merge and validation, produce the 6 STE-Code artifact files by adapting
the extracted spec data from `ste-code/merged/master.md`.


> **RAILS**: Before any action, validate against .
> All 8 rails apply: stage isolation, naming, completion integrity, content fidelity,
> formatting standards, factual correctness, progress tracking, error recovery.

## Prerequisites

- [ ] GATE 2 complete: `ste-code/merged/master.md` exists and validated
- [ ] All 53 rules present in master.md
- [ ] All 19 categories enumerated
- [ ] Dictionary entries available
- [ ] Synonym and polysemy tables extracted

## Dependency on Adaptation Rules

This skill depends on the preserve/replace rules defined in `ste-code-adaptation/SKILL.md`
(`.agents/skills/spec-extraction/ste-code-adaptation/SKILL.md`). Every artifact must
enforce these adaptation contracts:

### WHAT TO PRESERVE (unchanged structure)
- All 53 rules — same numbers, same 9-section organization
- 6-pass transformation pipeline
- Dictionary architecture (APPROVED/UNAPPROVED)
- 19 Technical Code Noun categories (adapted from STE's 19)
- 4 Technical Code Verb categories
- Safety instruction format (WARNING/CAUTION → BREAKING/DEPRECATED)

### WHAT TO REPLACE (adapted for code domain)
- All STE/non-STE example pairs → code documentation examples
- Technical noun categories → code-domain categories
- Vocabulary → code-domain approved words
- Safety WARNING/CAUTION → BREAKING/DEPRECATED

### Cross-Reference Validation

Before writing any artifact, verify:
- [ ] Preserve rules are enforced — no rule numbers, section counts, or structural elements changed
- [ ] Replace rules are enforced — no aerospace examples, no non-code-domain vocabulary
- [ ] Category mapping matches `references/category-mapping.md`
- [ ] No fabricated content — every claim traces to a specific line in master.md

## Master.md → Artifact Mapping

Each artifact draws from specific sections of master.md. Read only the sections
you need; do not load the entire master.md into context for every artifact.

| Artifact | Master.md Sections Required | Approx. Source Lines |
|----------|---------------------------|---------------------|
| Artifact 1 (system prompt) | P1-P14 principles, synonym table, dictionary architecture | ~150 lines |
| Artifact 2 (manual) | All 53 rules, 19 categories, polysemy, synonym, pipeline | ~2,000 lines |
| Artifact 3 (methodology) | Pipeline structure, extraction types, UML format | ~300 lines |
| Artifact 4 (example) | ONE specific STE/non-STE pair (see sourcing rules below) | ~10 lines |
| Artifact 5 (deployment) | Token budgets, artifact file list (derived, not extracted) | 0 lines (synthesized) |
| Artifact 6 (README) | Overview summary, file list, architecture | ~100 lines |

## Artifact 1: ste-code-distilled-system-prompt.txt

**Target**: ~1,200 tokens (~4,800 chars)
**Purpose**: System prompt constraining any LLM to STE-Code output

Must contain:
1. **IDENTITY block** (2-3 sentences) — "You are a STE-Code compliant technical writer..."
2. **14 CORE PRINCIPLES** (P1-P14) with exact STE rule source references
3. **CANONICAL SYNONYM TABLE** — adapted from master.md's synonym table
4. **APPROVED VOCABULARY POLICY** — adapted from master.md's dictionary architecture
5. **DOCUMENT INTERACTION PROTOCOL** — 10-step protocol for code documents
6. **OUTPUT FORMAT** — standardized sections
7. **ANTI-PATTERNS** — 10 rules for code domain

**Quality gates:**
- [ ] All 14 principles reference specific STE rules from master.md
- [ ] Synonym table uses actual canonical forms (not invented ones)
- [ ] Anti-patterns are code-specific (not copy-pasted from aerospace)
- [ ] ~4,800 chars total

### Artifact 1 Failure Recovery

If any quality gate fails:

- **Gate: principle references missing** → Re-read master.md P1-P14 section. Cross-check each
  principle against its `Rule X.Y` source. Re-generate the principles block only.
- **Gate: synonym table has invented forms** → Load master.md synonym table. Compare every
  entry pair-by-pair. Remove any pair not present in source. Re-generate the table only.
- **Gate: anti-patterns not code-specific** → Cross-reference anti-patterns against the
  adapted code-domain examples from `ste-code/adapted/`. Replace any generic pattern with
  a code-specific equivalent (e.g., "do not use passive voice" becomes "do not use passive
  voice in function descriptions").
- **Gate: character budget exceeded by >10%** → Identify the longest principle text. Reduce
  its word count by removing redundant qualifiers. If still over budget, merge adjacent short
  anti-patterns into compound rules.

**Recovery protocol:**
1. Log the failed gate(s) to `ste-code/artifacts/.generation-log.md`
2. Revert Artifact 1 file (delete, or restore from `.backup` if atomic write was used)
3. Re-read ONLY the failing master.md sections
4. Re-generate Artifact 1 with fixes applied
5. Re-validate all gates
6. Do NOT proceed to Artifact 2 until all gates pass

## Artifact 2: ste-code-self-reading-manual.txt

**Target**: ~7,000 tokens (~28,000 chars)
**Purpose**: 8-section self-reading manual following SSRM v1.0 structure

Must contain:
- **S0**: How to use this manual (recursive loop: read S3→read document→read S4→extract→...)
- **S1**: Core STE-Code principles (14 principles with code-domain examples)
- **S2**: Knowledge base — all 53 rules adapted, 19 categories, polysemy, synonym, pipeline
- **S3**: Page-reading protocol (document state tracking, page classification for code docs)
- **S4**: Skill extraction framework (5 patterns for code documentation)
- **S5**: UML extraction (code UML: class diagrams, sequence diagrams, flowcharts)
- **S6**: Recursive questioning protocol (13 questions adapted for code documents)
- **S7**: Output format (per-turn + final consolidated)
- **S8**: Context window management (keep manual + state, discard raw pages)

**Quality gates:**
- [ ] All 8 sections present and numbered
- [ ] All 53 adapted rules have code-domain example pairs
- [ ] 19 categories listed with code examples
- [ ] Recursive loop diagram present in S0
- [ ] S6 contains exactly 13 questions

### Artifact 2 Failure Recovery

If any quality gate fails:

- **Gate: section count < 8** → Identify which section(s) are missing. Check if the missing
  section was silently merged into an adjacent section. Re-generate the missing section from
  master.md source material. Insert it at the correct S0-S8 position.
- **Gate: rule count < 53** → Count rules with adapted code-domain examples. Identify which
  rule numbers have no example pair. For each gap, read the specific rule from master.md and
  adapt its STE/non-STE pair to a code-domain pair. Append the adapted example to the rule.
- **Gate: category count < 19** → Compare listed categories against the 19 from master.md.
  For each missing category: read its definition from master.md, create a code-domain example
  (e.g., "DEFINITIONS → function signatures and type definitions"), add to S2.
- **Gate: recursive loop diagram missing** → The diagram must show the flow:
  `S0(orient)→S3(page protocol)→Document(text)→S4(extract)→S6(question)→S7(output)→S8(trim)→S0(next page)`.
  Generate this as a Mermaid flowchart in S0. If diagram is present but inaccurate, fix
  the arrow directions.
- **Gate: S6 not exactly 13 questions** → Count current questions. If < 13: consult
  master.md recursive questioning section for missing questions. If > 13: merge redundant
  questions, prioritizing code-domain specificity.

**Recovery protocol:**
1. Log failed gate(s) to `.generation-log.md`
2. Revert Artifact 2 file
3. Re-read ONLY the failing master.md sections (not all 2,000 lines)
4. Apply the section-specific fix
5. Re-validate all gates for Artifact 2
6. Do NOT proceed to Artifact 3 until all gates pass

## Artifact 3: ste-code-extraction-methodology.txt

**Target**: ~1,400 tokens (~5,600 chars)
**Purpose**: Turn-by-turn protocol for processing code documents

Must contain:
- Turn 0: Initialization (read title, TOC, identify document type)
- Turns 1+: READ→TOKENIZE→LEXICAL CHECK→EXTRACT STRUCTURAL DATA→OPTIMIZE→OUTPUT→ADVANCE
- 5 structural extraction types adapted for code (classes, associations, procedures, conditions, safety)
- Final turn: Consolidation
- UML output format (Mermaid class + flowchart)
- State persistence between turns

**Quality gates:**
- [ ] Turn 0 initialization step present
- [ ] All 7 pipeline steps documented for Turns 1+
- [ ] All 5 extraction types have code-domain examples
- [ ] Consolidation procedure described
- [ ] State persistence mechanism specified

### Artifact 3 Failure Recovery

If any quality gate fails:

- **Gate: Turn 0 missing** → Read master.md initialization section. Write Turn 0 as:
  "Read the document title, table of contents, and first 50 lines. Classify document type
  as one of: README, API reference, inline comment, error message, configuration file."
- **Gate: pipeline steps < 7** → The 7-step pipeline is READ→TOKENIZE→LEXICAL CHECK→
  EXTRACT STRUCTURAL DATA→OPTIMIZE→OUTPUT→ADVANCE. If any step is missing, re-read the
  master.md pipeline section and insert the missing step with its sub-steps.
- **Gate: extraction types incomplete** → The 5 types are: classes/structs, associations/
  dependencies, procedures/functions, conditions/branches, safety/breaking changes. For
  each missing type, write a 2-sentence description with a code-specific extraction
  example (e.g., "CLASSES: identify class declarations and their method signatures").
- **Gate: state persistence unspecified** → Add: "After each turn, write current state
  to `ste-code/state/turn-N.json` containing: document position, extracted structures
  count, unresolved references list, next-turn cursor."

**Recovery protocol:**
1. Log failed gate(s) to `.generation-log.md`
2. Revert Artifact 3 file
3. Re-read ONLY the missing pipeline/master.md sections
4. Re-generate Artifact 3 with fixes
5. Re-validate all gates
6. Do NOT proceed to Artifact 4 until all gates pass

## Artifact 4: ste-code-example-turn.txt

**Target**: ~500 tokens (~2,000 chars)
**Purpose**: Single worked example showing non-STE-Code input → STE-Code output

### Sourcing Rule (Anti-Fabrication)

Artifact 4 MUST adapt a specific, real STE/non-STE pair from master.md. Do NOT
invent an example. Use this procedure:

1. Open `ste-code/merged/master.md`
2. Locate a rule with a clear STE/non-STE pair (e.g., Rule 3.5, Rule 1.7, Rule 5.2)
3. Extract both the non-STE text and the STE correction
4. Adapt both to the code domain using the replacement rules from
   `ste-code-adaptation/SKILL.md` (aerospace terms → code terms)
5. Cite the source rule number in the artifact

**Recommended source**: Rule 3.5 (Approved Verb Forms) or Rule 1.7 (Technical Names
as Verbs). These rules have the most direct code-domain analogs.

**Example sourcing trace:**
```
Source: master.md Rule 3.5, STE/non-STE pair #3
Non-STE: "The system utilizes the cache to leverage faster response times."
STE:     "The system uses the cache to get faster response times."
Adapted for code: "The function utilizes the cache to leverage faster response times."
                → "The function uses the cache to get faster response times."
Source line reference: master.md:88-95 (or actual line numbers from the file)
```

Must contain:
- Non-STE-Code INPUT (a real code comment, commit message, or README section)
- Source rule citation (e.g., "Adapted from master.md Rule X.Y, line N-M")
- ## COMPLIANCE STATUS: N violations found
- ## STE-CODE OUTPUT: corrected text
- ## UML EXTRACTION: Mermaid diagrams
- ## OPTIMIZATIONS: table with before/after metrics

Example input format:
```
Non-STE-Code: "The function should be called with the user object and
the return value needs to be checked for null before proceeding."
```

### Artifact 4 Failure Recovery

- **Gate: no source rule citation** → DO NOT fabricate. Re-read master.md, locate a rule
  with a clear STE/non-STE pair, adapt it for code, cite the rule number and line range.
- **Gate: example has no detected violations** → The example must show at least 3 violations
  (synonym, passive voice, ambiguous term). If violations < 3, choose a different source pair
  or expand the example to include more non-STE-Code patterns.
- **Gate: UML extraction missing or invalid** → Generate at minimum: one Mermaid class
  diagram showing the entities referenced in the example, and one Mermaid flowchart showing
  the corrected procedure flow.

**Recovery protocol:**
1. Log failed gate(s) to `.generation-log.md`
2. Revert Artifact 4 file
3. Re-select source pair from master.md if current choice is insufficient
4. Re-generate with source citation
5. Re-validate all gates
6. Do NOT proceed to Artifact 5 until all gates pass

## Artifact 5: ste-code-deployment-guide.txt

**Target**: ~1,800 tokens (~7,200 chars)
**Purpose**: Deployment instructions for Ollama, LM Studio, Python+llama.cpp

Must cover:
- Option A: Ollama Modelfile with baked-in system prompt
- Option B: LM Studio GUI steps
- Option C: Python + llama.cpp programmatic loop
- Option D: Full conversation export as additional context
- Token budget breakdown
- Expected output after processing

**Quality gates:**
- [ ] All 4 deployment options documented
- [ ] Each option has step-by-step instructions (max 20 words per step)
- [ ] Token budget table matches artifact totals
- [ ] Expected output examples are realistic and code-domain

### Artifact 5 Failure Recovery

Artifact 5 is synthesized content (not directly extracted from master.md). Recovery
actions differ:

- **Gate: deployment option missing** → Options A-D are: Ollama, LM Studio, Python+llama.cpp,
  Conversation Export. If an option is missing, write it from the deployment template:
  1. Prerequisites list, 2. Step-by-step (max 5 steps per option), 3. Verification command.
- **Gate: token budget mismatch** → Calculate token budgets from Artifacts 1-4 and 6 actual
  sizes. Update Artifact 5's budget table to match reality. Do NOT force artifacts to
  match the budget — the budget must reflect the artifacts.
- **Gate: output examples unrealistic** → Replace with output derived from Artifact 4's
  worked example. Show what the system prompt + example turn produces when deployed.

**Recovery protocol:**
1. Log failed gate(s) to `.generation-log.md`
2. Revert Artifact 5 file
3. Read current sizes of Artifacts 1-4 and 6 for accurate budget
4. Re-generate Artifact 5
5. Re-validate all gates
6. Do NOT proceed to Artifact 6 until all gates pass

## Artifact 6: README.md

**Target**: ~500 tokens (~2,000 chars)
**Purpose**: Project overview and quick start

Must contain:
- What STE-Code is (2-3 sentences)
- File listing with sizes
- Quick start (3 steps)
- Architecture summary (preserve/replace)
- Design principles
- References to ASD-STE100 Issue 9

**Quality gates:**
- [ ] STE-Code description is accurate and concise
- [ ] File listing includes all 6 artifacts with actual sizes
- [ ] Quick start has exactly 3 steps
- [ ] Architecture summary references preserve/replace rules from adaptation skill
- [ ] ASD-STE100 Issue 9 citation present

### Artifact 6 Failure Recovery

- **Gate: file listing incomplete** → Count files in `ste-code/artifacts/`. List all 6
  with their actual byte sizes. Do not estimate.
- **Gate: quick start not 3 steps** → The 3 steps are: (1) Choose deployment option from
  Artifact 5, (2) Load system prompt, (3) Run on your code documentation. Rewrite to match.
- **Gate: ASD-STE100 citation missing** → Add: "Based on ASD-STE100 Issue 9 (Simplified
  Technical English, aerospace maintenance documentation standard), adapted for software
  code documentation under the STE-Code protocol."

**Recovery protocol:**
1. Log failed gate(s) to `.generation-log.md`
2. Revert Artifact 6 file
3. Re-read Artifacts 1-5 for accurate file listing and descriptions
4. Re-generate Artifact 6
5. Re-validate all gates
6. Mark generation complete in `.generation-log.md`

## Generation Protocol

### Atomic Write Model

Write each artifact using an atomic rename pattern. This prevents partial
files from polluting the output directory if generation is interrupted.

```
For each artifact N (1 to 6):
  1. Write to ste-code/artifacts/.tmp/artifact-N.txt
  2. Run quality gate checks on the temp file
  3. If all gates pass: mv .tmp/artifact-N.txt → ste-code/artifacts/artifact-N.txt
  4. If any gate fails: delete .tmp/artifact-N.txt, log failure, begin recovery
  5. Copy the successfully-moved file to ste-code/artifacts/.backup/artifact-N.txt
```

### Sequential Order

Generate artifacts in order (1→6). For each artifact:

1. Read the relevant master.md sections (use the mapping table above — do not load all)
2. Adapt using the preserve/replace rules from `ste-code-adaptation/SKILL.md`
3. Write the artifact to `.tmp/` (atomic write)
4. Run the quality gate checklist
5. If all gates pass, move to `ste-code/artifacts/` and proceed to next artifact
6. If any gate fails, follow the per-artifact failure recovery protocol above

### Error Recovery Tiers

| Tier | Condition | Action |
|------|-----------|--------|
| **TIER 1: Gate failure** | A single quality gate fails on one artifact | Follow per-artifact recovery. Re-generate only the failed artifact. Proceed. |
| **TIER 2: Cascade failure** | Artifact N fails, then Artifact N+1 fails with the same gate | Halt generation. This indicates a source data problem. Re-validate master.md before continuing. |
| **TIER 3: Structural failure** | Master.md rule count < 53, or dictionary has letter gaps | Abort all artifact generation. Trigger re-extraction of missing pages via the extraction skill. Do NOT generate partial artifacts. |
| **TIER 4: Dependency failure** | Artifact N depends on Artifact N-1 which was never generated | This is a protocol violation. Start from Artifact 1 and generate sequentially. |

### Partial Output Policy

If generation is interrupted (by error, timeout, or instruction):

- **Keep**: All successfully-validated artifacts already in `ste-code/artifacts/`
- **Discard**: All `.tmp/` files (they failed validation)
- **Resume**: From the next ungenerated artifact number
- **Do NOT**: Distribute partial artifact sets — all 6 must be present for a valid release

### Edge Case Decision Matrix

| Edge Case | Detection | Action |
|-----------|-----------|--------|
| master.md has 52 rules (not 53) | Count rules with `grep -c '^### Rule'` | **TIER 3**: Abort generation. Trigger re-extraction of the missing rule's source page. Do NOT generate with 52 rules. |
| master.md has >53 rules | Count rules, compare to expected 53 | **Warn**: Log the extra rule numbers. If extras are duplicates, skip them. If extras are valid additions, include them and update this skill's expected count. |
| Dictionary missing entries for letters A, B, C | Check `a-dictionary.md` for letter section completeness | **Abort Artifact 2 only**: Artifact 2 requires full dictionary. Generate Artifacts 1, 3, 4, 5, 6 without full dictionary. Flag Artifact 2 with TODO markers where dictionary entries are missing. |
| Category count < 19 | Count categories in master.md | **TIER 3 if < 17**: 17+ is recoverable (some categories may be empty for code domain). < 17 indicates extraction failure. |
| Synonym table has duplicate entries | Check for identical prefer/avoid pairs | **Auto-fix**: Deduplicate. Keep the first occurrence. Log the removal. |
| Character budget exceeded by 10-20% | `wc -c` comparison | **Warn, then accept**: 20% over budget is acceptable if content quality is high. Log the oversize for future optimization. |
| Character budget exceeded by >20% | `wc -c` comparison | **Gate failure**: Follow per-artifact recovery. Reduce content, not quality. |

### Generation Log Format

Write to `ste-code/artifacts/.generation-log.md`:

```markdown
# STE-Code Artifact Generation Log
## Run: YYYY-MM-DD HH:MM:SS

### Artifact 1: ste-code-distilled-system-prompt.txt
- Status: PASS / FAIL (gate: <name>)
- Chars: NNNN / 4800 target
- Source: master.md lines N-M
- Recovery actions: <if any>

### Artifact 2: ste-code-self-reading-manual.txt
- Status: PASS / FAIL (gate: <name>)
- Chars: NNNN / 28000 target
- Source: master.md lines N-M
- Recovery actions: <if any>

... (repeat for artifacts 3-6)

### Summary
- Passed: N/6
- Failed: N/6
- Total chars: NNNNN / 49600 target
- Recovery loops: N
```

## Anti-Fabrication Rules

- Every adapted rule MUST reference a specific rule_number from master.md
- Every synonym MUST trace to an entry in master.md's synonym table
- Every category MUST match one of the 19 from master.md
- Every example MUST be an adaptation of a real STE/non-STE pair from master.md
- No invented code terms without a master.md source
- **NEW: Artifact 4 MUST cite the exact master.md source line range (e.g., `master.md:88-95`)**
- **NEW: If a required element cannot be found in master.md, mark it with `TODO(<reason>)` — do not fabricate**

## Verification After All Artifacts

```bash
# Count all artifacts
for f in ste-code/artifacts/ste-code-*.txt ste-code/artifacts/README.md; do
  chars=$(wc -c < "$f")
  echo "$(basename $f): $chars chars ~$((chars/4)) tokens"
done

# Verify no .tmp files remain
ls ste-code/artifacts/.tmp/ 2>/dev/null && echo "WARNING: temp files present" || echo "OK: no temp files"

# Check generation log
cat ste-code/artifacts/.generation-log.md
```

Expected totals:
- System prompt: ~4,800 chars (~1,200 tokens)
- Manual: ~28,000 chars (~7,000 tokens)
- Methodology: ~5,600 chars (~1,400 tokens)
- Example: ~2,000 chars (~500 tokens)
- Deployment: ~7,200 chars (~1,800 tokens)
- README: ~2,000 chars (~500 tokens)
- **Total: ~49,600 chars (~12,400 tokens)**

## Quick Recovery Reference

| Problem | Go To |
|---------|-------|
| Artifact N failed a gate | "Artifact N Failure Recovery" section |
| Two artifacts failed the same gate | Error Recovery Tiers → TIER 2 |
| Master.md has wrong rule count | Edge Case Decision Matrix → row 1 |
| Not sure which master.md section to read | Master.md → Artifact Mapping table |
| Need preserve/replace rules | Dependency on Adaptation Rules section |
| Example seems fabricated | Artifact 4 Sourcing Rule |
| Generation interrupted mid-way | Partial Output Policy |
