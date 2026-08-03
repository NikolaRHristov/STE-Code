# STE-Code Continuation Refinement Worker (Phase B1)

Continue refining a refined page from where a previous worker left off. You are
given ONE file to redo. Rewrite it so the content is complete, non-truncated,
and follows the refined markdown format used by the rest of ste-code/refined/.

## Target file

`{{target}}`

## What to do

1. Read the current content of the target file.
2. If it is truncated, orphaned continuation text, or missing its page header,
   rewrite the FULL page so it is complete and self-contained.
3. Preserve the canonical page header (`# Page N of 434` or `## Page <spec-id>`)
   and all marker conventions used elsewhere in ste-code/refined/ (e.g.
   `<!-- Start of picture text -->` ... `<!-- End of picture text -->`).
4. Do NOT change the meaning or drop any source content. Reflow only if needed.
5. Write the corrected file with your file-write tool, replacing the old
   content.

## Hard rules

- Output ONLY the rewritten file. No commentary outside it.
- No aerospace examples that are not also valid in the code domain.
- Keep sentences short and in active voice.
- Do not split the page mid-entry or mid-table.

When done, the file must start with a heading and contain no "continued…" or
"truncated" markers.
