---
name: refinement
description: Reformat extracted STE-Code docs to simplified-English standard.
category: authoring
capability: authoring-and-changing-the-standard
source: .agents/skills/refinement
layout: ste-code-canonical-v1
---

# Refinement Skill (STE-100 spec docs)

Reformat extracted STE-100 simplified-English documentation
(`ste-code/extracted/*.md`) into clean, standardized GitHub-Flavored Markdown
(`ste-code/refined/*.md`), preserving every word, table cell, and `<mark>`
annotation while collapsing per-page boilerplate.

## The 9 Rules (authoritative protocol)

1. **Keep dictionary tables as markdown tables.** Source arrives as 4-column
   grids
   (`Word (POS) | Approved meaning/ALTERNATIVES | STE EXAMPLE | Non-STE example`).
   Do NOT explode rows into `#### WORD (POS)` + bullet lists (that inflates ~3×
   and truncates). Emit the header + `|---|---|---|---|` separator once per
   page, preserve every cell, keep in-cell `<br>` line breaks, escape `|` as
   `\|`.
2. **STE / Non-STE examples use blockquotes.** Put each labeled example on its
   own `> **STE:**` / `> **Non-STE:**` line, WITH a quoted-blank `>` line
   BETWEEN them (see Pitfall 3). Never merge onto one line.
3. **Highlights / change-log / index pages stay compact.** A 2-column table
   (`| Word (POS) | Change |` or `| Subject | Rule |`) is ideal. Include every
   entry.
4. **Collapse ONLY repeated per-page stamps** into the single top metadata
   block: `**Page X-Y-Z**`, `**Issue 9 2025-01-15**`,
   `**ASD-STE100 Simplified Technical English**`, `**Part N - Dictionary**`,
   `**Subject-to-rule index**`, date stamps, repeated `**Highlights**`.
5. **Zero content loss.** Every dictionary row / `<mark>` annotation / last
   source entry survives. The LAST entry on the LAST source page must appear in
   your output.
6. **No mechanical edits / helper scripts.** Read the source, WRITE the refined
   file directly. Do NOT write/run `.py` / shell / `_gen_*.py` to transform
   output. Re-read your file with your eyes to confirm the self-check.
7. **Rule-7 boilerplate collapse.** Repeated running headers
   (`**Part N - Writing rules**`, `**Subject-to-rule index**`) count as
   boilerplate, not content - they're normalized out of the word-count gate.
8. **Mark text-coverage, not raw tag count.** Workers legitimately MERGE
   PDF-split `<mark>` fragments (a lone `<mark>Non-STE:</mark>` +
   `<mark>_sentence_</mark>`) into one clean span, preserving 100% of the marked
   words while reducing the raw tag count. Gate on surviving TEXT, not tag
   count.
9. **Batch-per-worker over per-file spawns.** One session refines 3 files
   sequentially (skill embedded once). ~23k tok = 9% of 250k context; each write
   stays a bounded generation (no truncation). Prefer launching batches of 3,
   not 109 single-file workers.

## Pitfall 3 (reversed): quoted-blank between blockquote lines

Consecutive `> ` lines WITHOUT a quoted-blank `>` between them soft-wrap into
one rendered paragraph on GitHub/VSCode. Insert a line containing only `>`
between `> **STE:**` and `> **Non-STE:**` to force separate paragraphs _within_
the same blockquote.

## What This Fixes (table)

| Symptom                              | Wrong                 | Right                    |
| ------------------------------------ | --------------------- | ------------------------ |
| Dictionary explodes to `####` blocks | inflate + truncate    | clean markdown table     |
| `<mark>` dropped on merge            | raw tag-count fails   | text-coverage passes     |
| Blockquote lines soft-wrap           | one line on GitHub    | quoted-blank separates   |
| Per-file foreground spawn            | 109 sleeps/poll loops | batch-of-3, no long wait |

## USER-DIRECTED WORKFLOW (embedded preferences)

- **Launch batches, not per-file workers.** The free model truncates long single
  generations; packing 3 files/worker sequential keeps each write bounded and
  safe. Drive workers as SEPARATE background processes (no for-loop, no
  refine_batch.py parent that reaps).
- **No long foreground sleeps.** Replace `sleep 300` + poll with `ps` +
  file-mtime checks, then READ the produced file - do not block the session
  waiting.
- **Poll + read instead of sleep.** After launching,
  `ps aux | grep [h]ermes-oneshot` + check refined mtimes; read a snippet to
  confirm real content (no phantom files).
- **`<mark>` text-coverage gate.** Skip column-header label fragments
  (`Column N: STE/Non-STE example`) - preserved as the real
  `| STE example | Non-STE example |` header, not content loss.
- **Dictionary → markdown table.** Keep 4-col grids; never explode to `####`
  headings.

## Support files (this skill)

- `references/mark-gate.md` - the `<mark>` merge false-positive case + fix.
- `references/blockquote-gfm.md` - the soft-wrap GFM bug + quoted-blank fix.
- `templates/worker-prompt.txt` - known-good batched worker prompt.
- `scripts/parity_gate.py` - `_word_count` + `_mark_text_coverage` checker.

## Self-check before you finish

1. Every dictionary table row / entry from the source appears in your output.
2. Every `<mark>` annotation is present (by text, not tag count).
3. The LAST entry on the LAST source page is present.
4. No example sentence is dropped or shortened.
