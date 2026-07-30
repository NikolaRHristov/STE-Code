# Level 5 — Full Standard (Directory Structure)

Organized by ASD-STE100 section. Each rule has its own directory for section-specific content.

## Structure

```
level5/
├── sec1/   (14 rules — Words)
├── sec2/   (2 rules — Noun Phrases)
├── sec3/   (7 rules — Verbs)
├── sec4/   (5 rules — Sentences)
├── sec5/   (5 rules — Procedures)
├── sec6/   (5 rules — Descriptions)
├── sec7/   (3 rules — Warnings)
├── sec8/   (6 rules — Punctuation)
├── sec9/   (4 rules — Document Structure)
├── gr/     (4 grammar rules)
├── dictionary/  (Approved/unapproved vocabulary)
└── templates/   (System prompt templates per level)
```

## Usage

Each rule directory can contain:
- `summary.md` — Rule summary for LLM context
- `examples.md` — Non-STE/STE example pairs
- `paradigm.md` — Paradigm-specific guidance
- `edge-cases.md` — Edge cases and exceptions

Source rules: `ste-code/adapted/a-secN-ruleX.Y.md`
