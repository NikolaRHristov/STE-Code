# Worker Prompts — ASD-STE100 Issue 9 Extraction

These are the exact prompts used to extract the 434-page ASD-STE100 Issue 9 specification.
Each prompt is written to `ste-code/extracted/wN-prompt.txt` and launched via:
```bash
hermes -z "$(cat ste-code/extracted/wN-prompt.txt)" -m deepseek-v4-pro --yolo
```

---

## W1: Pages 1–30 — Front Matter, TOC, Section 1 Rules

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0001.md through page-0030.md

TASK: Read every page and extract ALL content into ste-code/extracted/w1-sec1-rules.md

INCLUDE:
- Front matter (title, copyright, highlights)
- Table of Contents
- Subject-to-rule index
- General introduction
- Section 1 summary and Rules 1.1-1.6 FULL text with ALL example pairs

FORMAT: Markdown with ## headings. ALL example pairs as tables. Exact text. Output ONLY markdown.
```

---

## W2: Pages 31–66 — Categories, Sections 1–3

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0031.md through page-0066.md

TASK: Read every page and extract ALL content into ste-code/extracted/w2-sec2-3-rules.md

INCLUDE:
- Rules 1.7-1.14 FULL text with ALL example pairs
- ALL 19 technical noun categories with descriptions and examples
- ALL 4 technical verb categories with subcategories and examples
- Section 2 summary and Rules 2.1-2.2 FULL text
- Section 3 summary and Rules 3.1-3.2 FULL text

FORMAT: Markdown with ## headings. ALL examples as tables. Exact text. Output ONLY markdown.
```

---

## W3: Pages 67–94 — Sections 3–5 Rules

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0067.md through page-0094.md

TASK: Read every page and extract ALL content into ste-code/extracted/w3-sec3-5-rules.md

INCLUDE:
- Rules 3.3-3.7 FULL text with ALL example pairs
- Section 4 summary and Rules 4.1-4.5 FULL text
- Section 5 summary and Rules 5.1-5.5 FULL text

FORMAT: Markdown with ## headings. ALL examples as tables. Exact text. Output ONLY markdown.
```

---

## W4: Pages 95–114 — Sections 6–8 Rules

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0095.md through page-0114.md

TASK: Read every page and extract ALL content into ste-code/extracted/w4-sec6-8-rules.md

INCLUDE:
- Section 6: Rules 6.1-6.6 with ALL examples (descriptive writing, key words, paragraphs)
- Section 7: Rules 7.1-7.3 with ALL safety instruction examples (WARNING/CAUTION)
- Section 8: Rules 8.1-8.7 with ALL punctuation and word count examples

FORMAT: Markdown with ## headings. ALL examples as blockquotes. Exact text. Output ONLY markdown.
```

---

## W5: Pages 115–128 — Section 9 + General Recommendations

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0115.md through page-0128.md

TASK: Read every page and extract ALL content into ste-code/extracted/w5-sec9-gr-rules.md

INCLUDE:
- Section 9: Rules 9.1-9.4 FULL text with ALL example pairs
- GR-1 through GR-8: FULL text of each General Recommendation with ALL examples
- Word-for-word replacement and different sentence construction patterns

FORMAT: Markdown with ## headings. ALL examples as blockquotes. Exact text. Output ONLY markdown.
```

---

## W6: Pages 129–240 — Dictionary A–F

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0129.md through page-0240.md

TASK: Read every page and extract ALL content into ste-code/extracted/w6-dict-a-f.md

INCLUDE:
- Part 2 Dictionary title and full introduction
- EVERY dictionary entry A through F — do not skip any
- For each: word, POS, APPROVED/UNAPPROVED, meaning or alternatives, verb forms, STE example, non-STE example
- List of approved verbs, recurring errors

FORMAT: Markdown. ## for letters. ### for entries. Blockquotes for examples. Exact text. Output ONLY markdown.
```

---

## W7: Pages 241–300 — Dictionary G–P

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0241.md through page-0300.md

TASK: Read every page and extract ALL content into ste-code/extracted/w7-dict-g-p.md

INCLUDE: EVERY dictionary entry G through P. Do not skip any.
For each: word, POS, APPROVED/UNAPPROVED, meaning/alternatives, verb forms, examples.

FORMAT: Markdown. ## for letters. ### for entries. Exact text. Output ONLY markdown.
```

---

## W8: Pages 301–360 — Dictionary Q–Z

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0301.md through page-0360.md

TASK: Read every page and extract ALL content into ste-code/extracted/w8-dict-q-z.md

INCLUDE: EVERY dictionary entry Q through Z. Do not skip any.
For each: word, POS, APPROVED/UNAPPROVED, meaning/alternatives, verb forms, examples.

FORMAT: Markdown. ## for letters. ### for entries. Exact text. Output ONLY markdown.
```

---

## W9: Pages 361–434 — Appendices

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0361.md through page-0434.md

TASK: Read every page and extract ALL content into ste-code/extracted/w9-appendices.md

INCLUDE: All appendices, index, issue evolution data, change form, reference documents.

FORMAT: Markdown with ## headings. Exact text. Output ONLY markdown.
```
