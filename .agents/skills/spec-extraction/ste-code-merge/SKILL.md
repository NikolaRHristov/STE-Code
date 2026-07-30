---
name: ste-code-merge
description: "Merge 109 worker extraction files into a single master state document with deduplication and section organization."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [ste-code, merge, dedup, master-state, extraction]
---

# STE-Code Merge Phase

## Overview

> **RAILS**: Validate every action against `references/rails.md` — 8 immutable guardrails.

After all 109 workers complete extraction, merge their output into `ste-code/merged/master.md`.
This phase handles duplicate content (same spec text appearing across page boundaries),
organizes by section, and validates completeness.

> **RAILS**: Before any action, validate against `references/rails.md`.
> All 8 rails apply: stage isolation, naming, completion integrity, content fidelity,
> formatting standards, factual correctness, progress tracking, error recovery.

## Per-Rail Merge Mapping

Each of the 8 rails constrains specific merge decisions. Use this map to apply the correct rail at each step.

| Rail | Constraint on Merge | Enforcement Point |
|------|--------------------|--------------------|
| **Rail 1 — Stage Isolation** | Merge reads from `extracted/` (or `refined/`) and writes ONLY to `merged/`. Never write to `adapted/` or `artifacts/`. | Step 1 concatenation path check, Step 6 output directory check |
| **Rail 2 — Naming Convention** | Output files must be `master-raw.md` and `master.md` inside `ste-code/merged/`. No other filenames. | Step 6 file existence check |
| **Rail 3 — Completion Integrity** | Never claim merge complete until all 5 checks in Step 4 pass and all 10 spot-checks in Step 5 pass. | Step 4 validation, Step 5 spot-checks, Verification Gates |
| **Rail 4 — Content Fidelity** | Merge must NOT introduce commentary, summaries, or fabricated content. Every word in master.md must trace to a worker file, which traces to a spec page. Deduplication removes exact duplicates only — never rewrites content. | Step 2 dedup rules, Step 5 spot-check fidelity |
| **Rail 5 — Formatting Standards** | master.md must follow heading hierarchy, blank-line spacing, STE/Non-STE blockquote format, and table standards from `references/rails.md` Section 5. | Step 3 organization template, Step 4 format audit |
| **Rail 6 — Factual Correctness** | Verify immutable facts: 53 Rules + 4 GR, 19 categories, 434 pages, Model is `deepseek-v4-pro`. Never claim different counts. | Step 4 counts, Step 5 spot-checks |
| **Rail 7 — Progress Tracking** | Update PROGRESS.md only after merge verification passes. Mark merge as `[x]` only when master.md passes all checks. If merge fails mid-way, mark `[!]` and log the failure reason. | Post-merge PROGRESS.md update |
| **Rail 8 — Error Recovery** | When any check in Step 4 or Step 5 fails, use the Failure Recovery Protocol (Section "Recovery") to diagnose and fix. Never hide failures. | Recovery Protocol decision tree |

## When to Use

- After GATE 1 passes: all 109 worker files exist and have content
- Before GATE 3 adaptation begins

## Pre-Merge Resource Estimates

The merge operation processes 109 worker files into a 500KB+ master document.
Plan for these resource needs before you start.

| Resource | Estimate | Notes |
|----------|----------|-------|
| **Wall-clock time** | 15–30 minutes | 5 min concatenation + 10 min dedup scan + 5 min section organization + 5–10 min validation and spot-checks |
| **Disk space** | ~1.5 MB total | 109 worker files (~500KB) + master-raw.md (~520KB) + master.md (~500KB). Temporary master-raw.md is 520KB. |
| **Memory** | Minimal | All operations are sequential file reads. No in-memory map of the full document is required. |
| **Worker file count** | 109 | w001 through w109. Each covers pages 1–4 through 429–434 respectively. |
| **Expected output size** | >500KB | master.md must be at least 500KB. If smaller, content is missing. |

## Pre-Merge Validation Checklist

Before you start the merge, run these checks. Do not proceed if any check fails.

```bash
# 1. Count worker files — must be exactly 109
ls ste-code/extracted/w*.md | wc -l

# 2. Check each worker file is non-empty (>0 bytes)
find ste-code/extracted/ -name "w*.md" -size 0 | wc -l
# Expected: 0 (no empty files)

# 3. Verify worker file naming pattern (wNNN-pPPPP-PPPP.md)
ls ste-code/extracted/ | grep -v "^w[0-9][0-9][0-9]-p[0-9]*-[0-9]*\.md$" | wc -l
# Expected: 0 (all files follow pattern)

# 4. Check for missing page ranges (gaps)
for i in $(seq -w 1 109); do
  if [ ! -f "ste-code/extracted/w${i}-p"*".md" ]; then
    echo "MISSING: w${i}"
  fi
done
```

**If any check fails**: Stop. Go to the Failure Recovery Protocol. Do not concatenate partial or corrupt input.

## Merge Protocol

### Step 1: Concatenate by Page Range

Workers output in order (w001 covers pages 1-4, w109 covers 433-434).
Simple concatenation in page order preserves document flow:

```bash
cat ste-code/extracted/w*.md > ste-code/merged/master-raw.md
```

**Immediately after concatenation**, run a sanity check on master-raw.md:

```bash
# Check file size (must be >500KB for 434-page spec)
wc -c ste-code/merged/master-raw.md

# Check line count (must be >10,000 lines for full spec)
wc -l ste-code/merged/master-raw.md

# Check first and last 3 lines — first should be Page 1, last should be Page 434
head -3 ste-code/merged/master-raw.md
tail -3 ste-code/merged/master-raw.md
```

**If master-raw.md is <500KB or <10,000 lines**: Concatenation failed. Check which workers are missing or truncated. Use the gap detection script from the Pre-Merge Validation Checklist.

### Step 2: Deduplicate

Workers on adjacent page ranges may capture the same content at boundaries.
Use this concrete dedup procedure instead of ad-hoc scanning.

#### 2.1 Identify Duplicate Candidates

Run these detection commands on master-raw.md:

```bash
# Find duplicate rule headers (same rule number appearing more than once)
grep -n "^### Rule" ste-code/merged/master-raw.md | \
  awk -F: '{print $2}' | sort | uniq -d

# Find duplicate category headers
grep -n "^### Category" ste-code/merged/master-raw.md | \
  awk -F: '{print $2}' | sort | uniq -d

# Find duplicate dictionary entry headers (same WORD appearing more than once)
grep -n "^#### [A-Z]" ste-code/merged/master-raw.md | \
  awk -F: '{print $2}' | sed 's/ (.*//' | sort | uniq -d
```

#### 2.2 Dedup Rules (Exact Procedure)

For each pair of duplicate content blocks found, apply these rules in order:

1. **Rule statements**: Two occurrences of "Rule X.Y" with identical text. Keep the first occurrence. Remove the second occurrence and its surrounding content block. The first worker (lower page range) has the complete context.

   ```
   BEFORE:
   Line 456: ### Rule 1.1 — Use words that are approved...
   Line 457: Some explanatory text here.
   ...
   Line 489: ### Rule 1.1 — Use words that are approved...   ← DUPLICATE
   Line 490: Some explanatory text here.                     ← DUPLICATE

   AFTER:
   Line 456: ### Rule 1.1 — Use words that are approved...
   Line 457: Some explanatory text here.
   ...
   Line 489: [DELETED — duplicate of Line 456, removed by dedup]
   ```

2. **Example pairs**: Non-STE/STE pairs that are identical across workers. Keep the first occurrence. These happen when a page break cuts an example in half and both workers capture the full example.

   ```
   BEFORE (w050 end):
   > **STE:** Clean the filter with a dry cloth.
   > **Non-STE:** Utilize a dry rag to cleanse the filtration device.

   BEFORE (w051 start):
   > **STE:** Clean the filter with a dry cloth.    ← DUPLICATE
   > **Non-STE:** Utilize a dry rag to cleanse...   ← DUPLICATE

   AFTER (in merged):
   > **STE:** Clean the filter with a dry cloth.
   > **Non-STE:** Utilize a dry rag to cleanse the filtration device.
   [Second occurrence removed]
   ```

3. **Category listings**: Same category with same examples. Keep from the page where the category header first appears. The header is the anchor — content after it belongs to that worker.

4. **Dictionary entries**: Same WORD (POS) with identical meaning. Keep first occurrence. Dictionary entries are atomic — no entry depends on surrounding page context.

#### 2.3 Edge Cases During Dedup

These boundary conditions need special handling.

**Case A — Conflicting boundary content**: Two workers disagree on what appears at a page boundary.

```
w050 (pages 197-200), last content:  Rule 3.5 example ending "...the engine stopped."
w051 (pages 201-204), first content: Rule 3.5 example ending "...the engine was stopped."
```

**Resolution**: Check the original spec page 200 (last page of w050) and page 201 (first page of w051). Use the content from the page where the example begins. If the example spans both pages, prefer the worker that captured the start of the example (w050 in this case) — it has the complete sentence context.

**Case B — Dictionary entry with conflicting POS tags**:

```
w012: #### START (v) — APPROVED
w013: #### START (n) — APPROVED
```

**Resolution**: Both are valid. ASD-STE100 allows the same word as both a verb and a noun with different meanings. Keep both entries with their distinct POS tags. Do not merge them.

**Case C — Missing worker in the middle of a page range**:

```
w050 exists, w051 is missing, w052 exists
Pages 197-200 and 205-208 are covered. Pages 201-204 have no coverage.
```

**Resolution**: Do NOT merge. The gap produces a broken document. Go to the Failure Recovery Protocol — "Missing Worker File" path.

**Case D — Worker with empty output**:

```
w063 exists, file size is 0 bytes
```

**Resolution**: This is equivalent to a missing worker. The pages that w063 was assigned are unextracted. Go to the Failure Recovery Protocol — "Empty Worker Output" path.

### Step 3: Organize by Section

Restructure master-raw.md into a clean master.md:

```
# ASD-STE100 Issue 9 — Master Extraction

## Front Matter
- Title page with ASD-STE100 Simplified Technical English header
- Copyright notices and special usage rights
- Disclaimer of liability
- Highlights of changes from Issue 8 to Issue 9
- Table of Contents with all section page references
- Subject-to-Rule Index with all linguistic concept mappings
- General Introduction covering history, purpose, vocabulary policy, reference documents

## Part 1 — Writing Rules
### Section 1 — Words (Rules 1.1-1.14)
#### Rule 1.1 — Use words that are approved in the dictionary, technical nouns, or technical verbs
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 1.2 — Use approved words from the dictionary only as the specified part of speech
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 1.3 — Use approved words only with their approved meanings
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 1.4 — Use only the approved forms of verbs and adjectives
[Full rule text with all explanatory paragraphs and verb/adjective form tables]
#### Rule 1.5 — You can use words that you can include in a technical noun category
[Full rule text with all 19 category enumerations, descriptions, and examples]
#### Rule 1.6 — Use a word not approved in the dictionary only when it is a technical noun or part of a technical noun
[Full rule text with all explanatory paragraphs and examples]
#### Rule 1.7 — Do not use words that are technical nouns as verbs
[Full rule text with all explanatory paragraphs and examples]
#### Rule 1.8 — Use technical nouns that are approved in your company, industry, or subject field
[Full rule text with all explanatory paragraphs and examples]
#### Rule 1.9 — When you must select a technical noun, use one which is short and easy to understand
[Full rule text with all explanatory paragraphs and examples]
#### Rule 1.10 — Do not use regional, slang, or jargon words as technical nouns
[Full rule text with all explanatory paragraphs and examples]
#### Rule 1.11 — Do not use different technical nouns for the same item
[Full rule text with all explanatory paragraphs and examples]
#### Rule 1.12 — You can use verbs that you can include in a technical verb category
[Full rule text with all explanatory paragraphs and examples]
#### Rule 1.13 — Do not use technical verbs as nouns
[Full rule text with all explanatory paragraphs and examples]
#### Rule 1.14 — Use American English spelling
[Full rule text with all explanatory paragraphs and examples]

### Section 2 — Multi-word Nouns (Rules 2.1-2.3)
#### Rule 2.1 — Maximum three words in a noun cluster
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 2.2 — Use prepositions to break long clusters
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 2.3 — No noun clusters as verbs
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]

### Section 3 — Verbs (Rules 3.1-3.7)
#### Rule 3.1 — Use approved verb forms only
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 3.2 — Use the imperative for instructions
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 3.3 — Use only approved tenses
[Full rule text with all explanatory paragraphs, tense table, and STE/non-STE example pairs]
#### Rule 3.4 — Keep to one verb form per sentence
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 3.5 — Restrict the -ing form
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 3.6 — Active voice mandatory in procedures
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 3.7 — Passive voice restricted to descriptive writing
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]

### Section 4 — Sentences (Rules 4.1-4.4)
#### Rule 4.1 — Sentence length limits (20 words procedural, 25 words descriptive)
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 4.2 — No word omission
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 4.3 — Vertical lists with consistent format
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 4.4 — Connecting words mandatory
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]

### Section 5 — Procedural Writing (Rules 5.1-5.5)
#### Rule 5.1 — One instruction per sentence
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 5.2 — Numbered steps
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 5.3 — Notes and cautions before related step
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 5.4 — Conditional "If [condition], [action]"
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 5.5 — Standardized cross-reference language
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]

### Section 6 — Descriptive Writing (Rules 6.1-6.6)
#### Rule 6.1 — Maximum 6 sentences per paragraph
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 6.2 — One topic per paragraph
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 6.3 — Key phrases as signposts
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 6.4 — Logical flow with connecting words
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 6.5 — Simple sentence structure
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 6.6 — No imperative in descriptive text
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]

### Section 7 — Safety Instructions (Rules 7.1-7.3)
#### Rule 7.1 — Two-part format: command + consequence
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 7.2 — Place before related step
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 7.3 — Approved safety vocabulary only
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]

### Section 8 — Punctuation and Word Counts (Rules 8.1-8.7)
#### Rule 8.1 — No semicolons
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 8.2 — Word count enforcement
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 8.3 — Period as sole sentence terminator
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 8.4 — Colons only for introducing lists
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 8.5 — Hyphens for approved compounds only
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 8.6 — Abbreviations defined on first use
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 8.7 — No unnecessary punctuation
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]

### Section 9 — Writing Practices (Rules 9.1-9.4 + General Rules GR1-GR4)
#### Rule 9.1 — No word-for-word replacement without meaning check
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 9.2 — Words used in approved sense only
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 9.3 — Instructions in correct order
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### Rule 9.4 — Consistent style throughout
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### GR1 — "That" restricted to demonstrative/relative pronoun
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### GR2 — "With" restricted to "together with" or "having"
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### GR3 — Pronouns must have unambiguous antecedent
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]
#### GR4 — "This" must be followed by a noun
[Full rule text with all explanatory paragraphs and STE/non-STE example pairs]

### Technical Noun Categories (19 categories)
#### Category 1: Names in official parts information
[Full description and all example words]
#### Category 2: Names of vehicles/machines and locations on them
[Full description and all example words]
#### Category 3: Names of tools and support equipment
[Full description and all example words]
#### Category 4: Names of materials, consumables, and unwanted material
[Full description and all example words]
#### Category 5: Names of facilities, infrastructure, and locations
[Full description and all example words]
#### Category 6: Names of systems, components, circuits, and functions
[Full description and all example words]
#### Category 7: Mathematical, scientific, and engineering terms
[Full description and all example words]
#### Category 8: Navigation and geographic terms
[Full description and all example words]
#### Category 9: Numbers, units of measurement, and time
[Full description and all example words]
#### Category 10: Quoted text (placards, labels, signs, markings)
[Full description and all example words]
#### Category 11: Names of persons, groups, or organizations
[Full description and all example words]
#### Category 12: Parts of the body
[Full description and all example words]
#### Category 13: Common personal effects
[Full description and all example words]
#### Category 14: Medical terms
[Full description and all example words]
#### Category 15: Names of official documents and documentation parts
[Full description and all example words]
#### Category 16: Environmental and operational conditions
[Full description and all example words]
#### Category 17: Colors
[Full description and all example words]
#### Category 18: Damage terms
[Full description and all example words]
#### Category 19: Information technology and telephony terms
[Full description and all example words]

## Part 2 — Dictionary
### Dictionary Introduction
- Explanation of approved (UPPERCASE) vs unapproved (lowercase) words
- Part of speech abbreviations
- Verb type definitions (regular, irregular, auxiliary, modal)
- How to select words flowchart
- List of approved verbs
- List of recurring errors

### Dictionary A
#### Each entry with WORD (POS), APPROVED/UNAPPROVED, meaning, forms, STE example, Non-STE example

### Dictionary B
#### Each entry with WORD (POS), APPROVED/UNAPPROVED, meaning, forms, STE example, Non-STE example

### Dictionary C
#### Each entry with WORD (POS), APPROVED/UNAPPROVED, meaning, forms, STE example, Non-STE example

[Continue through D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z — every letter, every entry, no omissions]

## Appendices
### Change History (Issues 1 through 9)
Full timeline from 1986 to 2025 with all issue dates, designations, and key changes

### Decision Flowchart
Text and structure of the word approval flowchart added in Issue 8

### Index
Complete subject index with all cross-references

### Change Form
Template and instructions for submitting changes to the STEMG

### Reference Documents
Complete list of ISO standards, dictionaries, and style guides referenced
```

### Step 4: Validate Completeness

Run these checks on master.md. All counts must match exactly.

```bash
# Count rules — must be exactly 57 (53 Rules + 4 GR)
grep -c "^#### Rule" ste-code/merged/master.md
# Expected: 53
grep -c "^#### GR[0-9]" ste-code/merged/master.md
# Expected: 4
# Combined: 57

# Count categories — must be exactly 19
grep -c "^#### Category" ste-code/merged/master.md
# Expected: 19

# Count dictionary letter sections — must be 26 (A-Z)
grep -c "^### Dictionary [A-Z]" ste-code/merged/master.md
# Expected: 26

# Verify page coverage — must span 1-434
head -5 ste-code/merged/master.md | grep -q "1" && echo "Start: OK"
tail -5 ste-code/merged/master.md | grep -q "434" && echo "End: OK"

# File size check — must be >500KB
SIZE=$(wc -c < ste-code/merged/master.md)
if [ "$SIZE" -gt 512000 ]; then echo "Size: OK ($SIZE bytes)"; else echo "Size: FAIL ($SIZE bytes < 512000)"; fi
```

**If any count is wrong**: Go to the Failure Recovery Protocol — "Wrong Rule/Entry Count" path.

### Step 5: Spot-Check Fidelity

Pick 10 random page numbers from 1 to 434. For each page:

1. Read the original spec page (`spec/issue-09-2025/page-NNNN.md`)
2. Find the corresponding content in master.md
3. Verify text matches EXACTLY — no paraphrasing, no omission, no added commentary

Use this procedure for each spot-check:

```bash
# Generate 10 random page numbers (1-434)
for i in $(seq 1 10); do echo $(( RANDOM % 434 + 1 )); done | sort -n

# For each page N, extract the first 3 sentences from spec and from master.md
PAGE=N  # Replace with actual page number
echo "=== SPEC PAGE $PAGE ==="
head -20 "spec/issue-09-2025/page-${PAGE}.md" | head -3

echo "=== MASTER (searching for page $PAGE content) ==="
grep -A 5 "Page ${PAGE}" ste-code/merged/master.md | head -6
```

If any mismatch is found, flag the worker responsible and re-extract those pages using the Failure Recovery Protocol.

**Spot-check pass criteria**: All 10 spot-checks must show exact text matches. If even 1 fails, the merge is incomplete. Do not proceed to GATE 3.

### Step 6: Finalize Output

```bash
# Clean up temporary raw file (optional — keep for debugging if needed)
# rm ste-code/merged/master-raw.md

# Verify final output files
ls -lh ste-code/merged/master.md
```

## Output

- `ste-code/merged/master-raw.md` — concatenated raw extraction (temporary, 520KB)
- `ste-code/merged/master.md` — deduplicated, organized master state (permanent, >500KB)

## Failure Recovery Protocol

When any check in the merge protocol fails, use this decision tree to diagnose and fix.

### Recovery Decision Tree

```
CHECK FAILED
│
├─→ Concatenation failed (master-raw.md <500KB or <10,000 lines)
│   │
│   ├─→ Missing worker files detected
│   │   ACTION: Identify missing worker numbers (gaps in sequence w001-w109).
│   │   Launch re-extraction for ONLY the missing page ranges.
│   │   Each worker covers 4 pages: wNNN covers pages (NNN-1)*4+1 to NNN*4.
│   │   Re-run concatenation after all missing workers are regenerated.
│   │
│   ├─→ Files exist but are empty (0 bytes)
│   │   ACTION: Same as missing worker — the pages are unextracted.
│   │   Delete the empty file, re-extract the page range from spec.
│   │
│   └─→ Files exist but are truncated (last line ends mid-sentence)
│       ACTION: Identify the truncated worker. Split its page range in half.
│       Example: w050 (pages 197-200) truncated → re-extract as
│       w050a (pages 197-198) and w050b (pages 199-200).
│       Replace the truncated file with both halves, then re-concatenate.
│
├─→ Wrong rule count (grep -c "^#### Rule" ≠ 53)
│   │
│   ACTION: Diff the found rules against the expected set.
│   Expected rule numbers: 1.1-1.14, 2.1-2.3, 3.1-3.7, 4.1-4.4,
│   5.1-5.5, 6.1-6.6, 7.1-7.3, 8.1-8.7, 9.1-9.4, GR1-GR4.
│   │
│   ├─→ Count < 53: Missing rules.
│   │   Identify which rule numbers are absent. Map each missing rule
│   │   to its spec page range. Re-extract those pages.
│   │
│   └─→ Count > 53: Extra rule headers (dedup failure).
│       Re-run Step 2 dedup with the duplicate detection commands.
│       Check for rules that appear more than once.
│
├─→ Wrong category count (grep -c "^#### Category" ≠ 19)
│   │
│   ACTION: If count < 19, identify missing category numbers.
│   Categories 1-19 map to Rule 1.5 (pages ~7-10 in the spec).
│   If count > 19, re-run dedup on category headers.
│
├─→ Wrong dictionary letter count (grep -c "^### Dictionary [A-Z]" ≠ 26)
│   │
│   ACTION: Missing a letter section means an entire dictionary letter
│   was dropped during concatenation or dedup. Check master-raw.md
│   for that letter's section. If it exists in raw but not in master,
│   the dedup step incorrectly removed the section header.
│
├─→ Spot-check mismatch (content in master.md ≠ content in spec page)
│   │
│   ACTION: Identify the page number that failed. Map it to its worker.
│   Worker wNNN covers pages (NNN-1)*4+1 to NNN*4.
│   Check if the worker's output has the correct content.
│   │
│   ├─→ Worker output is wrong → re-extract that page range.
│   └─→ Worker output is correct but master.md is wrong →
│       The dedup or organization step corrupted content.
│       Rebuild master.md from master-raw.md, re-running Steps 2-3.
│
└─→ File size <500KB but all counts pass
    │
    ACTION: Content is structurally complete but text is missing.
    Likely cause: dictionary entries or example pairs dropped during dedup.
    Compare line counts between master-raw.md and master.md.
    If master.md is >5% smaller than master-raw.md, dedup was too aggressive.
    Re-run dedup with manual review of each duplicate candidate.
```

### Recovery Command Quick Reference

```bash
# Map worker number to page range
# wNNN → pages (NNN-1)*4+1 through NNN*4
echo "Worker w050 covers pages $((50*4-3)) through $((50*4))"
# Output: Worker w050 covers pages 197 through 200

# Find which worker covers a specific page
# Page P → worker wNNN where NNN = ceil(P/4)
PAGE=200
WORKER=$(printf "%03d" $(( (PAGE + 3) / 4 )))
echo "Page $PAGE is covered by worker w$WORKER"

# Re-extract a single page range
# Example: re-extract pages 197-200 (worker w050)
# Launch the extraction worker with those page parameters

# Diff found rules vs expected rules
grep -oP "^#### Rule \d+\.\d+" ste-code/merged/master.md | sort -t. -k1,1n -k2,2n | uniq > /tmp/found_rules.txt
# Compare with expected set manually
```

## Verification Gates

After merge, all gates must pass before GATE 3 adaptation can begin:

- [ ] master.md exists and is >500KB
- [ ] 53 rules present and numbered correctly (1.1-1.14, 2.1-2.3, 3.1-3.7, 4.1-4.4, 5.1-5.5, 6.1-6.6, 7.1-7.3, 8.1-8.7, 9.1-9.4)
- [ ] 4 General Rules present (GR1-GR4)
- [ ] 19 categories enumerated
- [ ] Dictionary entries cover all 26 letters A-Z
- [ ] 10 random spot-checks pass with exact text matches
- [ ] No duplicate rule headers, category headers, or dictionary entry headers
- [ ] Page coverage spans 1-434 without gaps
- [ ] All 8 rails verified (see Per-Rail Merge Mapping)
- [ ] PROGRESS.md updated with [x] for merge stage

## Incremental Merge for Partial Results

If not all 109 workers are complete but you need to validate partial progress,
use this incremental merge procedure.

1. Concatenate only the complete workers: `cat ste-code/extracted/w[0-9]*.md > ste-code/merged/master-partial.md`
2. Run Step 2 dedup on the partial file.
3. Run Step 4 validation on the partial file — note expected counts will be lower.
4. Mark the merge as `[!]` in PROGRESS.md with a note: "Partial merge — N/109 workers complete."
5. When remaining workers finish, re-run the full merge from Step 1.

**NOTE**: Incremental merge is for progress tracking only. Do not pass GATE 3 with a partial merge.
