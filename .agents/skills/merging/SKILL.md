---
description: "Merge 109 worker extraction files into a single master state document with deduplication and section organization."
version: "1.0.0"
related: [".agents/references/rails.md"]
---

# Merge Protocol — Stage 3 (Full Protocol)

Concatenate, deduplicate, and organize 109 worker files into a single master document. Agent-agnostic.

## When to Use
- After GATE 1 passes: all 109 worker files exist and have content
- Before adaptation begins

## Step 1: Concatenate by Page Range

Workers output in order (w001 covers 1-4, w109 covers 433-434):
```bash
cat ste-code/extracted/w*.md > ste-code/merged/master-raw.md
```

## Step 2: Deduplicate

Workers on adjacent page ranges may capture same content at boundaries:
- **Rule statements**: "Rule X.Y" with identical text → keep first occurrence
- **Example pairs**: Identical STE/non-STE pairs → keep first occurrence
- **Category listings**: Same category with same examples → keep from header page
- **Dictionary entries**: Same WORD (POS) with identical meaning → keep first

## Step 3: Organize by Section

Restructure into clean master.md:
```
# ASD-STE100 Issue 9 — Master Extraction

## Front Matter
- Title, copyright, disclaimer, highlights, TOC, index, introduction

## Part 1 — Writing Rules
### Section 1 — Words (Rules 1.1-1.14)
### Section 2 — Multi-word Nouns (Rules 2.1-2.3)
### Section 3 — Verbs (Rules 3.1-3.7)
### Section 4 — Sentences (Rules 4.1-4.4)
### Section 5 — Procedural Writing (Rules 5.1-5.5)
### Section 6 — Descriptive Writing (Rules 6.1-6.6)
### Section 7 — Safety Instructions (Rules 7.1-7.3)
### Section 8 — Punctuation (Rules 8.1-8.7)
### Section 9 — Writing Practices (Rules 9.1-9.4 + GR1-GR4)

### Technical Noun Categories (19 categories with descriptions)

## Part 2 — Dictionary
### A-Z entries with WORD (POS), APPROVED/UNAPPROVED, meaning, forms, examples

## Appendices
### Change History, Flowchart, Index, Change Form, Reference Documents
```

## Step 4: Validate Completeness

```bash
grep -c "^#### Rule" master.md     # Must be 53
grep -c "^### Category" master.md  # Must be 19
grep -c "^#### " master.md         # Dictionary entries: ~875 approved + ~1400 unapproved
head -5 master.md                  # Verify starts at page 1
tail -5 master.md                  # Verify ends at page 434
```

## Step 5: Spot-Check Fidelity

Pick 10 random page numbers. For each:
1. Read original spec page
2. Find corresponding content in master.md
3. Verify text matches EXACTLY — no paraphrasing, no omission

Flag any mismatched worker and re-extract those pages.

## Output
- `ste-code/merged/master-raw.md` — concatenated raw (temporary)
- `ste-code/merged/master.md` — deduplicated, organized (permanent)

## Verification Gates
- [ ] master.md exists and >500KB
- [ ] 53 rules present and numbered correctly
- [ ] 19 categories enumerated
- [ ] Dictionary entries cover A-Z
- [ ] 10 random spot-checks pass
- [ ] No duplicate rule headers

References: `.agents/references/rails.md`
