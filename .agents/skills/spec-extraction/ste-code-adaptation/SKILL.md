---
name: ste-code-adaptation
description: "Take extracted spec worker output and produce STE-Code artifacts (system prompt, self-reading manual, methodology)."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [ste-code, adaptation, spec, system-prompt, documentation]
    related_skills: [ste-code-worker-orchestration]
---

# STE-Code Adaptation Phase

## Overview

> **RAILS**: Validate every action against `references/rails.md` — 8 immutable guardrails.

After 9 workers extract the full ASD-STE100 spec, the coordinator reads all worker output and produces STE-Code: the coding-domain adaptation preserving the exact architecture.

> **RAILS**: Before any action, validate against .
> All 8 rails apply: stage isolation, naming, completion integrity, content fidelity,
> formatting standards, factual correctness, progress tracking, error recovery.

## Input

All 9 worker `.md` files in `ste-code/extracted/`:
- `w1-sec1-rules.md` through `w9-appendices.md`

### Concrete Input Sources

The adaptation phase reads from these concrete files. Do not proceed if any file is missing or truncated.

| File | Path | Content |
|------|------|---------|
| master.md (merged spec) | `ste-code/merged/master.md` | Complete ASD-STE100 Issue 9 — 53 rules across 9 sections, 19 technical noun categories, full dictionary (20,794 lines, 685 KB). This is the single source of truth for all aerospace examples and rule text. |
| category mapping | `.agents/skills/spec-extraction/ste-code-adaptation/references/category-mapping.md` | 19 STE categories → 19 STE-Code categories with representative examples |
| quality checklist | `.agents/skills/spec-extraction/references/quality-checklist.md` | Per-batch quality checks for file integrity, truncation, and fabrication detection |
| rails | `.agents/skills/spec-extraction/references/rails.md` | 8 immutable guardrails — stage isolation, naming, completion integrity, content fidelity, formatting, facts, progress, error recovery |

## Output Artifacts

| File | Size | Description |
|------|------|-------------|
| `ste-code-self-reading-manual.txt` | ~30KB | Long form — S0–S8, all 53 rules, 19 categories, pipeline |
| `ste-code-distilled-system-prompt.txt` | ~5.5KB | Short form — ~1,200 tokens, 14 principles, synonym table |
| `ste-code-extraction-methodology.txt` | ~4KB | 6-pass pipeline, turn-by-turn protocol |
| `ste-code-example-turn.txt` | ~3KB | Worked example: non-STE comment → STE-Code |
| `ste-code-deployment-guide.txt` | ~4KB | Ollama, LM Studio, OpenAI, Claude, LangChain |
| `README.md` | ~2.5KB | Overview, quick start |

### Intermediate Adapted Files

Before producing the 6 final artifacts, the adaptation phase writes one adapted rule file for each STE rule. These files go to `ste-code/adapted/` and follow the naming convention `a-secN-ruleY.Z.md`.

| Section | Rules | Adapted Files |
|---------|-------|---------------|
| Section 1 — Words | Rules 1.1 through 1.14 | `a-sec1-rule1.1.md` through `a-sec1-rule1.14.md` |
| Section 2 — Noun Phrases | Rules 2.1 through 2.5 | `a-sec2-rule2.1.md` through `a-sec2-rule2.5.md` |
| Section 3 — Verbs | Rules 3.1 through 3.9 | `a-sec3-rule3.1.md` through `a-sec3-rule3.9.md` |
| Section 4 — Sentences | Rules 4.1 through 4.8 | `a-sec4-rule4.1.md` through `a-sec4-rule4.8.md` |
| Section 5 — Procedures | Rules 5.1 through 5.8 | `a-sec5-rule5.1.md` through `a-sec5-rule5.8.md` |
| Section 6 — Description | Rules 6.1 through 6.7 | `a-sec6-rule6.1.md` through `a-sec6-rule6.7.md` |
| Section 7 — Warnings | Rules 7.1 through 7.3 | `a-sec7-rule7.1.md` through `a-sec7-rule7.3.md` |
| Section 8 — Punctuation | Rules 8.1 through 8.7 | `a-sec8-rule8.1.md` through `a-sec8-rule8.7.md` |
| Section 9 — Writing Practice | Rules 9.1 through 9.5 | `a-sec9-rule9.1.md` through `a-sec9-rule9.5.md` |
| General Rules (GR) | GR-1 through GR-4 | `a-gr-rule1.md` through `a-gr-rule4.md` |

Total: 53 adapted rule files (49 section rules + 4 general rules).

## Execution Protocol

Follow these steps in order. Complete each step before you start the next. Do not skip steps.

### Phase 4A — Load and Validate Input

**Step 1: Validate master.md.**
Read `ste-code/merged/master.md` and confirm:
- File exists and has 20,000 or more lines
- Contains "## Part 1 – Writing Rules" heading
- Contains "## Part 2 – Dictionary" heading
- Last 3 lines end cleanly (no mid-word truncation)

**Step 2: Load the category mapping.**
Read `references/category-mapping.md` and confirm:
- Contains exactly 19 rows in the mapping table
- Each row has an Original STE Category and an STE-Code Category

**Step 3: Load the rails check.**
Read `references/rails.md` and run the quick self-check:
- Stage 4 directory: `ste-code/adapted/`
- Adapted file naming: `a-secN-ruleY.Z.md`

### Phase 4B — Adapt Each Rule (53 iterations)

For each of the 53 rules, do these sub-steps in order.

**Step 4: Find the rule in master.md.**
Search `ste-code/merged/master.md` for the rule heading (example: "Rule 1.1"). Read the complete rule block — from the heading through the last example pair for that rule.

**Step 5: Extract the aerospace example pairs.**
For each example pair in the rule, record:
- The NON-STE aerospace example (bold label, blockquote format)
- The STE aerospace example (bold label, blockquote format)

**Step 6: Identify the code-domain analogue.**
For each aerospace example pair, find a structurally equivalent code-domain example. The analogue must have:
- Same grammatical structure as the aerospace pair
- Same rule violation type as the aerospace pair
- Code-domain vocabulary (no aerospace terms remaining)

Use these mappings for common aerospace → code concepts:

| Aerospace Concept | Code-Domain Analogue |
|-------------------|---------------------|
| mechanic / operator | developer / engineer |
| aircraft / system / component | application / module / service |
| maintenance procedure | build, deploy, or test procedure |
| leak / damage / failure | bug / crash / exception |
| safety precaution / warning | security advisory / BREAKING |
| tool / equipment | dependency / SDK / CLI tool |
| manufacturer's instructions | API documentation / style guide |
| inspection / check | test / lint / audit |
| fluid / material / container | data / input / payload |
| door / hatch / panel | endpoint / port / interface |

**Step 7: Write the adapted rule file.**
Write `ste-code/adapted/a-secN-ruleY.Z.md` with this structure:

```
# Rule X.Y — [Original STE Rule Title]

> **Source:** Adapted from ASD-STE100 Issue 9, Rule X.Y

## Original Rule
[The complete rule text from master.md — all paragraphs, examples, and notes]

## STE-Code Adaptation
[The adapted rule text with code-domain vocabulary]
[Adapted sentences — same structure, code vocabulary]

### Examples
> **Non-STE:** [code-domain non-STE example]
> **STE:** [code-domain STE-Code example]
>
> *Adapted from spec pair: [aerospace non-STE] → [aerospace STE]*

[Repeat for each example pair]
```

**Step 8: Cite the source.**
Each adapted example must include a citation line that shows the original aerospace pair it adapts from. Use this format:

```
*Adapted from spec pair: "aerospace non-STE text" → "aerospace STE text"*
```

If you add an example that has no direct spec pair (an additional code-domain example to clarify a concept), mark it:

```
*Additional code-domain example — no direct spec pair*
```

### Phase 4C — Produce Final Artifacts

**Step 9: Generate the 6 artifacts from the adapted files.**
Read all 53 adapted rule files from `ste-code/adapted/`. Use their content to write:

1. `ste-code-self-reading-manual.txt` — combine all S0-S8 sections
2. `ste-code-distilled-system-prompt.txt` — extract 14 principles + synonym table
3. `ste-code-extraction-methodology.txt` — build 6-pass pipeline from adapted rules
4. `ste-code-example-turn.txt` — write a worked comment transformation
5. `ste-code-deployment-guide.txt` — write deployment instructions
6. `README.md` — write overview and quick start

### Phase 4D — Verify and Report

**Step 10: Run the quality gate checklist.** See the Quality Gate Checklist section below.

**Step 11: Update PROGRESS.md.** Mark Phase D complete only after verification passes.

## Worked Example: Rule 3.5 (Restrict the "-ing" Form)

This section shows the complete adaptation of one rule — from aerospace spec extraction through STE-Code output. Use this as a template for all 53 rules.

### Input: Original Rule from master.md (aerospace domain)

The original rule text in `ste-code/merged/master.md` includes these aerospace example pairs:

> **Non-STE:** When you are doing this procedure, obey all the safety precautions.
> **STE:** When you do this procedure, obey all the safety precautions.

> **Non-STE:** [fragment] inappropriate tools without observing the manufacturer's instructions, are in danger of coming into contact with these materials and thus suffering from skin irritation and breathing problems.
> **STE:** Before you use dangerous materials, obey these precautions:
>
> 1. Read the manufacturer's instructions.
> 2. Make sure that there is sufficient airflow in the work area.
> 3. Put on a face mask and protective clothing.
> 4. Get the correct tools to open the containers for these materials.
>
> If you do not obey these precautions, injury to your skin and your lungs can occur.

### Analogue Identification

- Para 1 (simple -ing): "are doing" → violate Rule 3.5's ban on -ing as verb. Code analogue: "are running" (build command), "are writing" (code).
- Para 2 (complex -ing): long fragment with multiple -ing forms, reworked into vertical list with consequences. Code analogue: complex sentence about developers writing code without style guide → reworked into vertical list of instructions with consequences.

### Output: Adapted Rule (code domain)

The adapted file `ste-code/adapted/a-sec3-rule3.5.md` transforms the aerospace examples:

> **Non-STE:** When you are running the build command, check the terminal for errors.
> **STE:** When you run the build command, check the terminal for errors.
>
> *Adapted from spec pair: "When you are doing this procedure, obey all the safety precautions." → "When you do this procedure, obey all the safety precautions."*

> **Non-STE:** Developers writing code without following the style guide can cause formatting conflicts and merge issues.
> **STE:** Obey the style guide when you write code. If you do not obey the style guide, formatting conflicts and merge issues can occur.
>
> *Adapted from spec pair: "[fragment] inappropriate tools without observing the manufacturer's instructions..." → "Before you use dangerous materials, obey these precautions: ... If you do not obey these precautions, injury to your skin and your lungs can occur."*

> **Non-STE:** The script is processing all the input files while logging the results to the console.
> **STE:** The script processes all the input files. Then it writes the results to the console.
>
> *Additional code-domain example — no direct spec pair*

### Traceability

Each adapted example contains a citation line that traces back to the exact aerospace example pair in the original spec. This preserves the chain of reasoning and allows an auditor to verify that the adaptation is grounded in source material (RAIL 4: Content Fidelity).

## Adaptation Rules

### Preservation Rationale

Each preservation decision has a specific reason. Do not preserve without understanding why.

| What to Preserve | Rationale |
|-----------------|-----------|
| All 53 rule numbers (same numbering, same 9-section organization) | Downstream artifacts (`self-reading-manual.txt`, `system-prompt.txt`, benchmark tests) reference rules by number. Changing numbers would break all cross-references. |
| 6-pass transformation pipeline structure | The pipeline is domain-agnostic — Pass 1 (lexical) through Pass 6 (consistency) applies identically to aerospace and code documentation. Only the vocabulary changes. |
| Dictionary architecture (APPROVED/UNAPPROVED tables) | The two-table structure (words allowed / words forbidden with alternatives) is a proven usability pattern. Readers scan the UNAPPROVED column first, then find the APPROVED alternative. Changing this structure would reduce scanability. |
| 19 Technical Code Noun categories (adapted from STE's 19) | The category count (19) is verified against ASD-STE100 Issue 9 pages 47-52. Each category has a clear code-domain analogue in `references/category-mapping.md`. No category is dropped or added. |
| 4 Technical Code Verb categories | Verbs in code documentation cluster into four families: development operations, data operations, application operations, communication operations. These map to STE's verb organization without loss. |
| Safety instruction format (WARNING/CAUTION → BREAKING/DEPRECATED) | The two-level risk format is structurally identical — only the risk domain changes. BREAKING replaces WARNING (risk of system failure / data loss / security breach), DEPRECATED replaces CAUTION (risk of unexpected behavior / performance degradation). |

### Replacement Rationale

Each replacement decision has a specific reason. Do not replace without understanding why.

| What to Replace | Rationale |
|----------------|-------------|
| All aerospace example pairs (STE/non-STE) → code documentation example pairs | The target domain is software documentation. Aerospace examples about mechanics, aircraft, leaks, and safety belts are not meaningful to a developer reading API docs. Every example must use vocabulary from the 19 STE-Code technical noun categories. |
| Technical noun categories → code-domain categories | STE's categories (vehicles, materials, facilities) map to code-domain categories (frameworks, dependencies, deployment targets) via `references/category-mapping.md`. The mapping preserves the 19-category count while changing every example. |
| Vocabulary → code-domain approved words | The canonical synonym table replaces STE's general-English synonyms with code-domain synonyms. "Use" replaces "utilize/leverage/employ." "Start" replaces "initiate/commence/bootstrap." These are the words developers actually use. |
| WARNING/CAUTION → BREAKING/DEPRECATED | STE's safety words warn about physical injury and equipment damage. STE-Code's signal words warn about API breakage and deprecated features. The two-level structure is identical; only the risk domain changes. |

### WHAT TO PRESERVE (unchanged structure)
- All 53 rules — same numbers, same 9-section organization
- 6-pass transformation pipeline
- Dictionary architecture (APPROVED/UNAPPROVED)
- 19 Technical Code Noun categories (adapted from STE's 19 — verified from Issue 9 spec pages 47-52)
- 4 Technical Code Verb categories
- Safety instruction format (WARNING/CAUTION → BREAKING/DEPRECATED)

### WHAT TO REPLACE (adapted for code domain)
- All STE/non-STE example pairs → code documentation examples
- Technical noun categories → code-domain categories (see references/category-mapping.md)
- Vocabulary → code-domain approved words
- Safety WARNING/CAUTION → BREAKING/DEPRECATED

## Edge Case Guidance

This section covers rules and examples that resist simple domain-substitution adaptation. When you encounter these cases, use the guidance below.

### EC1: Rule with No Obvious Code-Domain Analogue

**Scenario:** A rule concerns physical safety, mechanical assembly, or aerospace-specific equipment with no natural code equivalent.

**Guidance:** Map the *structure* of the rule, not its physical content.

- **Physical safety instruction (Rule 7.1)** — Map to API breaking changes or security vulnerabilities. The consequence structure is identical: condition → action → consequence. "If you touch the live wire" becomes "If you call this deprecated endpoint."
- **Mechanical assembly instruction (Rule 5.2)** — Map to software build or deploy steps. "Install the left bracket before the right bracket" becomes "Build the frontend before the backend."
- **Equipment inspection (Rule 5.4)** — Map to test/lint/audit procedures. "Examine the filter for damage" becomes "Run the linter on the changed files."

### EC2: Idiomatic Aerospace Example That Resists Adaptation

**Scenario:** An aerospace example uses a phrase that is highly domain-specific and has no clean code analogue.

**Guidance:** Preserve the *grammatical structure* and *violation type*. Replace the vocabulary.

- **"The landing gear must be retracted before takeoff"** → "The database must be migrated before deployment." Same structure (passive voice violation, Rule 3.6), different domain.
- **"Do not operate the engine without oil"** → "Do not run the server without authentication." Same structure (imperative prohibition, Rule 5.2), different risk domain.

### EC3: Rule Where Multiple Adaptations Are Possible

**Scenario:** A rule can be adapted to two different code-domain concepts, both valid.

**Guidance:** Pick the adaptation that is most common in everyday developer documentation. Prefer examples from README files, API docs, and commit messages over niche domains like embedded systems or GPU programming. The adaptation must feel natural to the widest developer audience.

If both adaptations are equally common, include both and mark the second as:

```
*Alternative code-domain example*
```

### EC4: Dictionary Word with No Code Analogue

**Scenario:** An approved STE word (example: "aileron," "fuselage") has no meaning in code documentation.

**Guidance:** Do not include the word in STE-Code. The STE-Code dictionary is a subset of the STE dictionary — words without code-domain meaning are omitted. Note the omission in the adapted rule file:

```
> **NOTE:** The original STE dictionary entry for "[word]" has no code-domain analogue and is omitted from the STE-Code dictionary.
```

### EC5: Rule That Spans Multiple Sections

**Scenario:** A rule references or depends on rules from other sections.

**Guidance:** Add a "See also" line at the end of the adapted rule file that cross-references the related sections.

```
> **See also:** Rule 5.3 — Imperative (Command) Form for Instructions; Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition
```

### EC6: Truncated or Corrupted Input

**Scenario:** The master.md file has a truncated rule — missing example pairs, partial sentences, or formatting errors.

**Guidance:** Follow RAIL 8 (Error Recovery):
1. Mark the adapted file as incomplete with a NOTE at the top
2. Adapt only the parts that are present and complete
3. Do not fabricate missing content
4. Report the issue in `.agents/feedback/exchange.md`

```
> **NOTE:** This adapted file is incomplete. The source rule in master.md has [describe the truncation]. [N example pairs] are missing.
```

## Category Mapping

See `references/category-mapping.md` for the full 19-category adaptation from STE's 19 categories.

## Quality Gate Checklist

Run this checklist after all 53 adapted rule files are written and the 6 artifacts are produced. Do not claim completion until every item passes.

### Adapted Files (53 files)

- [ ] All 53 adapted rule files exist in `ste-code/adapted/`
- [ ] Each file follows the naming convention `a-secN-ruleY.Z.md`
- [ ] Each file contains an "## Original Rule" section with text from master.md
- [ ] Each file contains an "## STE-Code Adaptation" section with code-domain text
- [ ] Every example has a citation line (`*Adapted from spec pair: ...*` or `*Additional code-domain example*`)
- [ ] No aerospace terms remain in the STE-Code sections (check: "aircraft," "mechanic," "landing gear," "fuselage," "aileron")
- [ ] All adapted examples use vocabulary from the 19 STE-Code technical noun categories
- [ ] BREAKING/DEPRECATED/NOTE format matches WARNING/CAUTION/NOTE structure
- [ ] File sizes: each adapted rule file is 1 KB to 8 KB (extreme outliers may indicate truncation or fabrication)

### Artifact Files (6 files)

- [ ] `ste-code-self-reading-manual.txt` exists, size 25-35 KB
- [ ] `ste-code-distilled-system-prompt.txt` exists, size 4-7 KB, ~1,200 tokens
- [ ] `ste-code-extraction-methodology.txt` exists, size 3-5 KB
- [ ] `ste-code-example-turn.txt` exists, size 2-4 KB
- [ ] `ste-code-deployment-guide.txt` exists, size 3-5 KB
- [ ] `README.md` exists, size 1.5-3.5 KB

### Cross-Reference Integrity

- [ ] All 53 rule numbers are present across all artifact files
- [ ] All 19 technical noun categories are listed in the self-reading manual
- [ ] All 14 core principles map to a rule number in the system prompt
- [ ] The synonym table has exactly the approved 12 prefer/avoid pairs
- [ ] No fabrication signals: no "22 categories," no "deepseek-pro," no modern tools in extraction sections

### Rail Compliance

- [ ] RAIL 1: Files are in `ste-code/adapted/` (Stage 4 directory) — not in `merged/` or `artifacts/`
- [ ] RAIL 2: All files follow `a-secN-ruleY.Z.md` convention
- [ ] RAIL 3: Verification pass completed before marking stage complete
- [ ] RAIL 4: Every adapted claim is grounded in master.md source text
- [ ] RAIL 5: Headings have blank lines, tables have separators, example pairs use blockquote format
- [ ] RAIL 6: Facts are correct (19 categories, 53 rules, poolside/laguna-s-2.1:free)
- [ ] RAIL 7: PROGRESS.md reflects actual status
- [ ] RAIL 8: Errors are fixed or reported, not hidden

## Verification

After producing each artifact:
- Verify all 53 rule numbers are present
- Verify word counts: short form ~1,200 tokens, long form ~7,000 tokens
- Verify all examples are code-domain (no aerospace examples remaining)
- Verify BREAKING/DEPRECATED/NOTE format matches WARNING/CAUTION/NOTE structure

## File Structure After Adaptation

```
ste-code/
├── merged/
│   └── master.md                    # Input: complete ASD-STE100 spec
├── adapted/
│   ├── a-sec1-rule1.1.md            # 53 adapted rule files
│   ├── a-sec1-rule1.2.md
│   ├── ... (49 files)
│   ├── a-sec9-rule9.4.md
│   ├── a-sec9-rule9.5.md
│   ├── a-gr-rule1.md                # 4 general rules
│   ├── a-gr-rule2.md
│   ├── a-gr-rule3.md
│   └── a-gr-rule4.md
├── artifacts/
│   ├── ste-code-self-reading-manual.txt
│   ├── ste-code-distilled-system-prompt.txt
│   ├── ste-code-extraction-methodology.txt
│   ├── ste-code-example-turn.txt
│   ├── ste-code-deployment-guide.txt
│   └── README.md
└── README.md                        # Project overview
```
