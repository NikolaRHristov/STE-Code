---
name: ste-code-merge
description: "Merge 109 worker extraction files into a single master state document with deduplication and section organization."
version: 1.0.0
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


> **RAILS**: Before any action, validate against .
> All 8 rails apply: stage isolation, naming, completion integrity, content fidelity,
> formatting standards, factual correctness, progress tracking, error recovery.

## When to Use

- After GATE 1 passes: all 109 worker files exist and have content
- Before GATE 3 adaptation begins

## Merge Protocol

### Step 1: Concatenate by Page Range

Workers output in order (w001 covers pages 1-4, w109 covers 433-434).
Simple concatenation in page order preserves document flow:

```bash
cat ste-code/extracted/w*.md > ste-code/merged/master-raw.md
```

### Step 2: Deduplicate

Workers on adjacent page ranges may capture the same content at boundaries.
Use these patterns to identify duplicates:

- **Rule statements**: "Rule X.Y" followed by identical text → keep first occurrence
- **Example pairs**: Non-STE/STE pairs that are identical → keep first occurrence
- **Category listings**: Same category with same examples → keep from the page where the category header appears
- **Dictionary entries**: Same WORD (POS) with identical meaning → keep first occurrence

Manual dedup is preferred over scripted — the coordinator should scan for patterns:

```bash
# Find duplicate rule headers
grep -n "^### Rule" ste-code/extracted/master-raw.md | sort -t: -k2 | uniq -d -f1
```

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

Run these checks on master.md:

```bash
# Count rules (should be 53 + 4 GR)
grep -c "^#### Rule" ste-code/extracted/master.md

# Count categories (should be 19)
grep -c "^### Category" ste-code/extracted/master.md

# Count dictionary entries (should be ~875 approved + ~1400 unapproved)
grep -c "^#### " ste-code/extracted/master.md | head -1

# Verify page coverage (should span 1-434)
head -5 ste-code/extracted/master.md
tail -5 ste-code/extracted/master.md
```

### Step 5: Spot-Check Fidelity

Pick 10 random page numbers. For each:
1. Read the original spec page (`spec/issue-09-2025/page-NNNN.md`)
2. Find the corresponding content in master.md
3. Verify text matches EXACTLY — no paraphrasing, no omission

If any mismatch found, flag the worker responsible and re-extract those pages.

## Output

- `ste-code/merged/master-raw.md` — concatenated raw extraction (temporary)
- `ste-code/merged/master.md` — deduplicated, organized master state (permanent)

## Verification Gates

After merge:
- [ ] master.md exists and is >500KB
- [ ] 53 rules present and numbered correctly
- [ ] 19 categories enumerated
- [ ] Dictionary entries cover A-Z
- [ ] 10 random spot-checks pass
- [ ] No duplicate rule headers
