# Spec Page Section Types and Tailored Extraction Instructions

## Overview

Different sections of the ASD-STE100 spec require different extraction strategies.
This reference helps workers and the coordinator apply the right approach per page range.

## Section Type Classification

| Type | Pages | Content Signature | Extraction Priority |
|------|-------|-------------------|---------------------|
| **FRONT** | 1-12 | Large centered text, copyright blocks, change tables | Exact text, preserve ALL legal text |
| **TOC** | 13-16 | Multi-column page references | Extract structure, preserve page numbers |
| **INDEX** | 17-24 | Subject-to-rule mapping table | Extract ALL mappings as table |
| **INTRO** | 25-42 | Narrative prose, Q&A format | Full text, preserve ALL reference documents list |
| **RULES** | 43-128 | "Rule X.Y", STE/non-STE example pairs, explanatory text | ALL rules with ALL example pairs — highest priority |
| **CATEGORIES** | 47-66 | Numbered lists with descriptions, category tables | Full enumeration, preserve ALL examples |
| **DICT** | 129-360 | "Word (POS)" entries, APPROVED/UNAPPROVED, 4-column layout | EVERY entry — word, POS, meaning, forms, alternatives, examples |
| **APPENDIX** | 361-434 | Change history tables, flowcharts, index, forms | Full text, preserve issue evolution data |

## Per-Type Extraction Prompts

### FRONT Type (pages 1-12)

```
TASK: Preserve ALL front matter text exactly — title, copyright, EU trademark,
special usage rights, disclaimer of liability, issue date. The highlights table
shows Issue 9 changes — extract every row. DO NOT summarize legal text.
```

### RULES Type (pages 43-128)

```
TASK: For EVERY rule on these pages:
1. Extract the exact rule statement (bold text)
2. Extract ALL explanatory paragraphs
3. Extract ALL example pairs — mark STE examples and non-STE examples clearly
4. Preserve the "Rule X.Y" numbering
5. If a rule spans multiple pages, note the continuation

FORMAT:
### Rule X.Y
[Exact rule statement]
[Explanatory text]

**STE:** [example text]
**Non-STE:** [example text]
```

### CATEGORIES Type (pages 47-66)

```
TASK: Extract ALL technical noun categories:
1. Category number and exact name
2. Category description paragraph
3. ALL example words/phrases listed for that category
4. Any notes or help text associated with the category

FORMAT:
### Category N: [Exact Name]
[Description]
Examples: [comma-separated list]
Notes: [any]
```

### DICT Type (pages 129-360)

```
TASK: Extract EVERY dictionary entry. For each entry:
1. WORD (exact casing — UPPERCASE = approved, lowercase = unapproved)
2. Part of speech abbreviation
3. APPROVED or UNAPPROVED status
4. Approved meaning (for approved) OR approved alternatives (for unapproved)
5. Verb forms (if a verb)
6. STE example text
7. Non-STE example text

NOTE: The 4-column PDF layout causes text interleaving in extraction.
This is expected. Preserve ALL text even if columns appear merged.

FORMAT:
#### WORD (POS) — APPROVED
Meaning: [exact meaning]
Forms: [form1, form2, form3]
STE: [example]
Non-STE: [example]

#### word (POS) — UNAPPROVED
Alternatives: [word1 (POS), word2 (POS)]
STE: [example using alternative]
Non-STE: [example using unapproved word]
```

### APPENDIX Type (pages 361-434)

```
TASK: Extract ALL appendix content:
1. Decision flowchart text and structure
2. Change history table (Issues 1-9 with dates and key changes)
3. Index entries
4. Change form template
5. Reference documents list
6. Any remaining dictionary entries or reference material

FORMAT: Preserve original structure. Use ## headings for major sections.
```

## Page Range Reference (Quick Lookup)

| Start Page | End Page | Type | Workers |
|------------|----------|------|---------|
| 1 | 12 | FRONT | W001-W003 |
| 13 | 16 | TOC | W004 |
| 17 | 24 | INDEX | W005-W006 |
| 25 | 42 | INTRO | W007-W010 |
| 43 | 66 | RULES+CAT | W011-W016 |
| 67 | 94 | RULES | W017-W023 |
| 95 | 128 | RULES | W024-W032 |
| 129 | 240 | DICT A-F | W033-W060 |
| 241 | 300 | DICT G-P | W061-W075 |
| 301 | 360 | DICT Q-Z | W076-W090 |
| 361 | 434 | APPENDIX | W091-W109 |
