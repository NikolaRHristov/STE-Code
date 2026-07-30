# Refinement Protocol — 9 Rules (Full Protocol)

Reformat extracted spec files into clean, standardized markdown. Zero content loss — format only. Agent-agnostic.

## When to Use
- After extraction phase complete (all 109 raw files exist)
- When extracted tables show PDF 4-column interleaving artifacts
- When heading hierarchy is inconsistent
- When STE/non-STE examples are not clearly delineated
- Before adaptation phase (clean input = better adaptation)

## What This Fixes

| Problem in Raw Extraction | Refined Output |
|---------------------------|----------------|
| STE examples merged with non-STE in dictionary tables | `**STE:**` / `**Non-STE:**` line separation |
| 4-column PDF interleaving in dictionary entries | Clean 2-column layout |
| `###` used for proper names ("ASD-STE100") | `**bold**` for names, `###` only for real headings |
| Page headers repeated | Collapsed to once per section |
| Rule examples inconsistent | Standardized blockquote format |
| Page footers ("Issue 9", "2025-01-15") | Single page metadata line |
| Missing or inconsistent code blocks | Fenced with language identifier |
| Tables without headers | Headers added where detectable |
| Lists with inconsistent indentation | Standardized 2-space indent |

## 9 Refinement Rules (NON-NEGOTIABLE)

### Rule 1: ZERO CONTENT LOSS
Every word, number, example, table cell from the original extraction MUST appear in the refined output. Format only — never delete.

### Rule 2: STANDARDIZED HEADINGS
```
# Page N of M          ← Every file starts with this
## Section Title        ← Major sections (Section 1, Part 2, etc.)
### Rule X.Y            ← Rule headings
#### WORD (POS)         ← Dictionary entries
```

### Rule 3: TABLE FORMATTING
Clean markdown with header row + separator row:
```
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
```
Align columns. Escape pipe chars with `\|`. Merge split cells.

### Rule 4: STE/NON-STE EXAMPLE FORMAT
```
> **STE:** [The STE-compliant example text, fully written]
> **Non-STE:** [The non-compliant example text, fully written]
```
Separated by blank line. Never merge STE/non-STE into same line.

### Rule 5: CODE BLOCKS
Fenced with language identifier. Never bare ```.

### Rule 6: DICTIONARY ENTRY FORMAT
```
#### WORD (POS) — APPROVED
- **Meaning:** [exact approved meaning]
- **Forms:** [form1, form2, form3]
- **STE:** [example]
- **Non-STE:** [example]

#### word (POS) — UNAPPROVED
- **Alternatives:** [alternative1 (POS), alternative2 (POS)]
- **STE:** [example using alternative]
- **Non-STE:** [example using unapproved word]
```

### Rule 7: PAGE METADATA
```
# Page NNN of 434

> **Source:** ASD-STE100 Issue 9, January 2025
> **Pages:** NN–MM of 434
```
Remove repetitive "ASD-STE100 Simplified Technical English" headers from body.

### Rule 8: LIST STANDARDIZATION
- Numbered: `1. `, `2. ` (not `1)` or `1-`)
- Bullets: `- ` (not `* ` or `• `)
- Nested: 2-space indent

### Rule 9: CONSISTENT SPACING
- `### Heading` → blank line → content
- Content end → blank line → next heading
- Table end → blank line → next content
- Exactly one blank line between sections (never two, never zero)
- No trailing whitespace
- No triple blank lines

## Worker Setup

109 workers, 4 pages each. Batches of 3. Output: `ste-code/refined/rNNN-pPPPP-PPPP.md`

### Launch Protocol
```bash
hermes -z "$(cat prompt.txt)" -m deepseek-v4-pro --yolo &
```
Use ONLY deepseek-v4-pro. 3 workers per batch.

## Verification (Per Batch)
1. Output line count >= input line count
2. All page numbers from input appear in output
3. No "ASD-STE100 Simplified Technical English" repeated as headings
4. All STE/non-STE pairs use `> **STE:**` format
5. All tables have header rows

## 🔴 MANDATORY: Progress Tracking
Update REFINE-PROGRESS.md after EVERY batch. Flip batch status to ✅. Update counter. Git commit. The auditor cross-references this against disk.

References: `.agents/references/rails.md`, `.agents/references/quality-checklist.md`
