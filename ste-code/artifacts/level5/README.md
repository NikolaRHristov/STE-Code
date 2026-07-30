# Level 5 — Full Specification (51 Rule Summaries)

Organized by ASD-STE100 section. Each rule has its own directory with a summary file.

## Structure

```
level5/
├── sec1/   (14 rules — Words)
│   └── a-sec1-rule1.1/summary.md  through  a-sec1-rule1.14/summary.md
├── sec2/   (2 rules — Noun Phrases)
├── sec3/   (7 rules — Verbs)
├── sec4/   (5 rules — Sentences)
├── sec5/   (5 rules — Procedures)
├── sec6/   (5 rules — Descriptions)
├── sec7/   (3 rules — Warnings)
├── sec8/   (6 rules — Punctuation)
├── sec9/   (4 rules — Document Structure)
└── README.md
```

Total: 51 rule summaries in 51 directories across 9 sections.

## Each Summary Contains

- Rule number and title
- What the rule requires
- One Non-STE and STE example pair

## Usage

Level 5 summaries are the input for Level 3 and Level 4 assembly. They are also the reference for specification-grade documentation.

```bash
# Assemble from Level 5 summaries
python3 .agents/tools/assemble-level3.py   # → Level 3 (~8K tokens)
python3 .agents/tools/assemble-level4.py   # → Level 4 (~45K tokens)
```

Source rules: `ste-code/adapted/a-secN-ruleY.Z.md`
