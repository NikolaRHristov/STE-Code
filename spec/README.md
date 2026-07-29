# ASD-STE100 Specification Archive

> Downloaded specification documents, academic papers, and presentations.
> Each page extracted to an individual advanced markdown file.

---

## PDF Sources

| File | Pages | Content |
|------|-------|---------|
| `issue-09-2025.pdf` | 434 | **Issue 9, January 2025** — International standard. Latest issue. |
| `issue-07-2017.pdf` | 382 | **Issue 7, January 2017** — Rules reduced 65→53. Full rule revision. |
| `presentation-ata-s1000d-2022.pdf` | 10 | Industry presentation — S1000D/ATA Forum, June 2022 |
| `paper-ceur-vol3427.pdf` | 6 | Academic paper — CEUR Vol. 3427 |
| `paper-ceur-vol3990.pdf` | 8 | Academic paper — CEUR Vol. 3990 |

---

## Extracted Markdown — One Page Per File

| Directory | Pages | Output | Markdown Features |
|-----------|-------|--------|-------------------|
| `issue-09-2025/` | 434 | 712 KB (~178K tokens) | Headings, lists, tables, dictionary entries, STE examples |
| `issue-07-2017/` | 382 | 606 KB (~151K tokens) | Headings, lists, tables, dictionary entries, STE examples |
| `presentation-ata-s1000d-2022/` | 10 | 4 KB (~1K tokens) | Headings, lists, presentation slides |
| `paper-ceur-vol3427/` | 6 | 22 KB (~5.5K tokens) | Academic paper structure |
| `paper-ceur-vol3990/` | 8 | 22 KB (~5.6K tokens) | Academic paper structure |
| **TOTAL** | **840** | **~1.37 MB (~341K tokens)** | |

### File naming

Each page: `page-NNNN.md` (zero-padded to 4 digits)
```
issue-09-2025/
  page-0001.md   ← Cover
  page-0002.md   ← Copyright
  page-0003.md   ← Table of Contents
  ...
  page-0050.md   ← Technical noun categories
  ...
  page-0201.md   ← Dictionary (C-entries)
  ...
  page-0434.md   ← Last page
```

---

## Extraction Scripts (atomic, granular)

| Script | Purpose |
|--------|---------|
| `extract_page.py` | Single-page PDF→Markdown converter with heading detection, table formatting, dictionary entry parsing, list detection |
| `extract_pdf.py` | Batch orchestrator — extracts all pages from one PDF |
| `batch_extract_all.sh` | Master script — runs extraction for all PDFs in spec/ |

### Usage

```bash
# Extract one page
python3 extract_page.py issue-09-2025.pdf 50 page-0050.md

# Extract all pages from one PDF
python3 extract_pdf.py issue-09-2025.pdf issue-09-2025/

# Extract everything
bash batch_extract_all.sh
```

---

## Markdown Format Features

- **`### HEADING`** — Section titles, all-caps key terms
- **`## Heading`** — Rule numbers, section names
- **`> STE:`** — STE-compliant example text
- **`| Table |`** — Tables from PDF (highlights, multi-column)
- **`| Word (POS) | Meaning |`** — Dictionary entries
- Indented continuation lines for list items

---

## Missing Issues

Issues 6 and 8 are not publicly available on known mirrors. The official website (asd-ste100.org) requires a request form.
