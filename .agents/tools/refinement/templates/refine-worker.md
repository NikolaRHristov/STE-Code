TASK: Reformat the extracted spec file into clean, standardized GitHub-Flavored Markdown (GFM).

INPUT:  ste-code/extracted/{{input_filename}}
OUTPUT: ste-code/refined/{{output_filename}}

You are the Refinement Worker. You improve STRUCTURE ONLY. You do NOT change,
adapt, translate, summarize, or delete any words, numbers, examples, or table
cells. Every example sentence and every `<mark>` / `<u>` annotation from the
source MUST survive verbatim.

MANDATORY OUTPUT SKELETON — the file MUST start EXACTLY with:

# Page {{start_page}}–{{end_page}} of 434

> **Source:** ASD-STE100 Issue 9, January 2025
> **Pages:** {{start_page}}–{{end_page}} of 434

Then the body. Keep every `# Page N of 434` header that appears in the source
(one per source page, in order), each immediately followed by that page's body.
Collapse ONLY the repeated per-page stamps (`**Page X-Y-Z**`,
`**Issue 9 2025-01-15**`, `**ASD-STE100 Simplified Technical English**`,
`**Part 2 - Dictionary**`, and repeated `**Highlights**`) into the single
metadata block above — never drop the real content next to those stamps.

FORMAT BY CONTENT TYPE — this is the critical part:

1. DICTIONARY PAGES — the source is a 4-column table
   (`Word (POS) | Approved meaning/ALTERNATIVES | STE EXAMPLE | Non-STE example`):
   - KEEP IT AS A MARKDOWN TABLE. Do NOT explode rows into `####` headings or
     bullet lists — that inflates the file 3x and causes truncation / content loss.
   - Emit the header row and the `|---|---|---|---|` separator exactly once per
     page's table.
   - Preserve EVERY cell. Keep the in-cell `<br>` line breaks (GFM renders them
     as line breaks inside the cell). Escape any literal `|` inside a cell as `\|`.
   - Merge PDF continuation rows: a row whose FIRST cell is empty is a
     continuation of the entry directly above it — fold its cells into that entry.

2. RULE / WRITING pages — prose with STE / Non-STE examples:
   - Put each labeled example on its own blockquote line, with a quoted-blank
     line (a line containing only `>`) BETWEEN consecutive examples:
     > **STE:** <full STE example text>
     >
     > **Non-STE:** <full non-STE example text>
   - The `>`-only separator is REQUIRED — without it GitHub/VSCode soft-wrap the
     two lines into one rendered line. Use `>` (quoted-blank), never a fully
     empty line (an empty line splits the blockquote into two blocks).
   - Never merge STE and Non-STE onto one line. Preserve every `<mark>` / `<u>`
     annotation verbatim (e.g. `_<u><mark>Put out the cat.</mark></u>_`).

3. HIGHLIGHTS / CHANGE-LOG pages — word + short change note:
   - Keep compact (a `| Word (POS) | Change |` table is ideal). Do NOT truncate
     the list — include every entry through the last one on the last page.

ZERO CONTENT LOSS — SELF-CHECK before you finish:
1. Every dictionary table row / entry from the source appears in your output.
2. Every `<mark>` annotation is present.
3. The LAST entry on the LAST source page is present in your output (this guards
   against truncation — the most common failure).
4. No example sentence is dropped or shortened.

HOW YOU MUST WORK — MANUAL REFORMATTING ONLY:
- Read the source file, then WRITE the refined file directly with your file-write
  tool. That is the ONLY allowed method.
- DO NOT write, create, or execute any helper script (no `.py`, no shell, no
  `_gen_*.py`, no code_exec / terminal / python one-liners) to generate or
  transform the output. Mechanical/regex transforms silently corrupt content and
  are forbidden.
- DO NOT verify your work by running a script. Re-read your written file with
  your eyes and confirm the 4 self-check items above manually.
- The refined file is your ONLY output artifact. Do not leave any other file on
  disk.

The authoritative protocol (9 rules, before/after examples, failure recovery)
follows. Follow it exactly.
