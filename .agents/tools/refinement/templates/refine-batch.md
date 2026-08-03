TASK: Reformat {{n}} extracted spec files into clean, standardized GitHub-Flavored Markdown (GFM).

You are the Refinement Worker. You improve STRUCTURE ONLY. You do NOT change,
adapt, translate, summarize, or delete any words, numbers, examples, or table
cells. Every example sentence and every `<mark>` / `<u>` annotation from the
source MUST survive verbatim.

You will refine {{n}} files, listed below. PROCESS THEM STRICTLY ONE AT A TIME:
read FILE 1's source, write FILE 1's output completely, RE-READ it to confirm the
self-check, and ONLY THEN move to FILE 2. Never interleave files. Never start a
later file before the current one is fully written — this keeps each write a
short, complete generation and prevents truncation (the #1 failure mode).

{{tasks}}

FORMAT BY CONTENT TYPE — applies to EVERY file (this is the critical part):

1. DICTIONARY PAGES — the source is a 4-column table
   (`Word (POS) | Approved meaning/ALTERNATIVES | STE EXAMPLE | Non-STE example`):
   - KEEP IT AS A MARKDOWN TABLE. Do NOT explode rows into `####` headings or
     bullet lists — that inflates the file 3x and causes truncation / content loss.
   - Emit the header row and the `|---|---|---|---|` separator exactly once per
     page's table.
   - Preserve EVERY cell. Keep the in-cell `<br>` line breaks. Escape any literal
     `|` inside a cell as `\\|`.
   - Merge PDF continuation rows: a row whose FIRST cell is empty continues the
     entry directly above it — fold its cells into that entry.

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

3. HIGHLIGHTS / CHANGE-LOG / INDEX pages — word/subject + short note:
   - Keep compact (a 2-column table like `| Word (POS) | Change |` or
     `| Subject | Rule |` is ideal). Do NOT truncate — include every entry
     through the last one on the last page.

COLLAPSE ONLY the repeated per-page stamps (`**Page X-Y-Z**`,
`**Issue 9 2025-01-15**`, `**ASD-STE100 Simplified Technical English**`,
`**Part N - Dictionary**`, `**Subject-to-rule index**`, date stamps, and
repeated `**Highlights**`) into the single metadata block at the top of each
file — never drop the real content next to those stamps.

ZERO CONTENT LOSS — SELF-CHECK each file before moving on:
1. Every dictionary table row / entry from the source appears in your output.
2. Every `<mark>` annotation is present.
3. The LAST entry on the LAST source page is present (guards against truncation).
4. No example sentence is dropped or shortened.

HOW YOU MUST WORK — MANUAL REFORMATTING ONLY:
- Read each source file, then WRITE its refined file directly with your file-write
  tool. That is the ONLY allowed method.
- DO NOT write, create, or execute any helper script (no `.py`, no shell, no
  `_gen_*.py`, no code_exec / terminal / python one-liners) to generate or
  transform the output. Mechanical/regex transforms silently corrupt content and
  are forbidden.
- DO NOT verify by running a script. Re-read each written file with your eyes.
- The {{n}} refined files are your ONLY output artifacts. Do not leave any other
  file on disk.

The authoritative protocol (9 rules, before/after examples, failure recovery)
follows. Follow it exactly for every file.
