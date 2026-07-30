# ASD-STE100 Specification Archive

> Downloaded specification documents, academic papers, and presentations.
> Each page extracted to an individual advanced markdown file.

---

## PDF Sources

|| File | Pages | Content |
||------|-------|---------|
|| `issue-09-2025.pdf` | 434 | **Issue 9, January 2025** — International standard. Latest issue. |
|| `issue-07-2017.pdf` | 382 | **Issue 7, January 2017** — Rules reduced 65→53. Full rule revision. |
|| `presentation-ata-s1000d-2022.pdf` | 10 | Industry presentation — S1000D/ATA Forum, June 2022 |
|| `paper-ceur-vol3427.pdf` | 6 | Academic paper — CEUR Vol. 3427 |
|| `paper-ceur-vol3990.pdf` | 8 | Academic paper — CEUR Vol. 3990 |

---

## Extracted Markdown — One Page Per File

|| Directory | Pages | Output | Markdown Features |
||-----------|-------|--------|-------------------||
|| `issue-09-2025/page-dir/` | 426 | 737 KB (~184K tokens) | Headings, lists, tables, dictionary entries, STE examples |
|| `issue-07-2017/` | 382 | 606 KB (~151K tokens) | Headings, lists, tables, dictionary entries, STE examples |
|| `presentation-ata-s1000d-2022/` | 10 | 4 KB (~1K tokens) | Headings, lists, presentation slides |
|| `paper-ceur-vol3427/` | 6 | 22 KB (~5.5K tokens) | Academic paper structure |
|| `paper-ceur-vol3990/` | 8 | 22 KB (~5.6K tokens) | Academic paper structure |
|| **TOTAL** | **840** | **~1.37 MB (~341K tokens)** | |

### File naming

Each page: `page-<spec-page-id>.md` (using spec page identifiers)

```
issue-09-2025/
  issue-09-2025.md       ← Combined markdown (all pages in one file)
  page-dir/
    page-front-matter.md  ← Cover, copyright, highlights table
    page-HI-1.md          ← Highlights page HI-1
    page-HI-2.md          ← Highlights page HI-2
    ...
    page-HI-26.md         ← Highlights page HI-26
    page-TOC-1.md         ← Table of Contents page TOC-1
    page-TOC-2.md         ← Table of Contents page TOC-2
    page-SRI-1.md         ← Subject-to-Rule Index page SRI-1
    ...
    page-SRI-4.md         ← Subject-to-Rule Index page SRI-4
    page-i.md             ← General introduction page i
    ...
    page-viii.md          ← General introduction page viii
    page-1-0-2.md         ← Part 1 title page
    page-1-1-1.md         ← Section 1, Rule 1.1
    page-1-1-2.md         ← Section 1, Rule 1.2
    ...
    page-1-9-14.md        ← Section 9, GR-8
    page-2-0-1.md         ← Dictionary introduction
    ...
    page-2-1-A1.md        ← Dictionary A-1
    page-2-1-A2.md        ← Dictionary A-2
    ...
    page-2-1-Y2.md        ← Dictionary Y-2 (last page)
    MANIFEST.md           ← Page file manifest (all pages listed)
```

### Page ID Reference

| Page ID Prefix | Section | Description |
|---------------|---------|-------------|
| `HI-N` | Highlights | Issue 9 change highlights (26 pages) |
| `TOC-N` | Table of Contents | Document structure navigation (2 pages) |
| `SRI-N` | Subject-to-Rule Index | Subject-to-rule mapping (4 pages) |
| `i`–`viii` | General Introduction | Preamble, Q&A, reference docs (8 pages) |
| `1-X-Y` | Part 1 — Writing Rules | Sections 1-9, Rules 1.1–9.4 (131 pages) |
| `2-0-N` | Part 2 — Dictionary Intro | Dictionary introduction and instructions (21 pages) |
| `2-1-XN` | Part 2 — Dictionary | Word list A-Z (285 pages) |

---

## Extraction Scripts (atomic, granular)

|| Script | Purpose |
||--------|---------||
|| `issue-09-2025/split_spec.py` | Split combined markdown into individual page files |
|| `extract_page.py` | Single-page PDF→Markdown converter with heading detection, table formatting, dictionary entry parsing, list detection |
|| `extract_pdf.py` | Batch orchestrator — extracts all pages from one PDF |
|| `batch_extract_all.sh` | Master script — runs extraction for all PDFs in spec/ |

### Usage

```bash
# Split combined markdown into individual page files
python3 issue-09-2025/split_spec.py

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
- **`| **WORD (POS)** |`** — Approved dictionary entries (uppercase)
- **`| **word (POS) — UNNAPPROVED** |`** — Unapproved dictionary entries (lowercase)
- Indented continuation lines for list items

---

## Missing Issues

Issues 6 and 8 are not publicly available on known mirrors. The official website (asd-ste100.org) requires a request form.
