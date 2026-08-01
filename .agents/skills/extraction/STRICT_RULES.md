# STRICT CONTENT PRESERVATION RULES

These rules are MANDATORY for every extraction, grouping, and adaptation worker.
Violation of any rule = the output is rejected and the worker must re-run.

---

## R1 — VERBATIM ORIGINAL
Output MUST be byte-faithful to the source page files. No summarization, no
"cleanup", no reformatting. Preserve exactly:
- All table structures (`|` columns, separator rows)
- All `<br>` tags inside table cells
- All `**bold**` markup
- All page numbering, headers, footers as they appear

## R2 — TABLE INTEGRITY (ATOMIC)
A table row is ONE atomic unit. Rules:
- NEVER split a row across files or pages
- NEVER merge two separate tables into one
- NEVER reorder, add, or remove columns
- If a table spans a page boundary: emit the row completely, then add
  `<!-- TABLE CONTINUES ON NEXT PAGE -->` before the next `# Page N` header

## R3 — NO FREELANCE CONTENT
Workers do NOT add: commentary, examples, section headers, footers, "helpful"
notes, or meta-text. The output is EXACTLY:
1. `# Page N of 434` marker
2. `**Page X**` page-id line
3. The verbatim extracted content
Nothing else. No "Here is the extraction", no "I have read", no summaries.

## R4 — SINGLE-FILE WRITE
A worker writes exactly ONE output file. It never touches another worker's file.
If appending to a shared group file: acquire lock-group.sh FIRST. Direct writes
to shared files by two workers = data loss.

## R5 — RE-BATCH IDEMPOTENCE
Re-running a worker MUST produce identical output. If the target file exists and
passes verify-batch.py, the worker SKIPS. No "improvements", no re-formatting of
existing valid files. This prevents context drift across sessions.

## R6 — CONTEXT WINDOW SAFETY
If 4 pages exceed the model's safe context window, the worker MUST request a
smaller range (2 pages) rather than truncate. Truncation = hard fail. Partial
output is NEVER written to disk.

---

## Enforcement
- `strict-guard.py check <file>` — verify a single file is clean
- `strict-guard.py scan <dir>` — scan all files in a directory
- `protect-tables.py --dir <dir>` — detect table breaks at page boundaries
- `verify-batch.py --all` — confirm all 109 workers complete + idempotent
- `lock-group.sh acquire <file> <agent>` — claim exclusive write on a group file

Run strict-guard.py and protect-tables.py AFTER every batch. Any violation
blocks the stage gate.
