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
[Copyright, highlights, TOC]

## Part 1 — Writing Rules
### Section 1 — Words (Rules 1.1-1.14)
#### Rule 1.1
[Full text + examples]
...

### Section 2 — Multi-word Nouns (Rules 2.1-2.3)
...

[through Section 9 + GR1-GR4]

### Technical Noun Categories (19)
[Full enumeration with descriptions and examples]

## Part 2 — Dictionary
### Introduction
### Dictionary A-Z
#### A entries
...

## Appendices
### Change History (Issues 1-9)
### Decision Flowchart
### Index
### Reference Documents
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
