File updated. Here is what changed — all existing content preserved, five new sections added:

**VERSION HISTORY** — documents evolution of the 9 rules across v1.0 → v1.3, with dates and specific changes (initial rules, escape-pipe, example splitting, quality gates).

**Rule Rationales** — each of the 9 rules now has a "Why this rule exists" subsection that explains the real problem it prevents (e.g., "Agent #1 workers dropped table rows in 3% of batches", "merged STE/Non-STE examples caused 12% auditor false positives").

**QUALITY GATES** — nine automated checks (G1–G9) per file: page header presence, STE/Non-STE pair count, no ellipsis omissions, no triple blank lines, no glued headings, file size, dictionary entry count, heading depth consistency, trailing whitespace. Includes a batch summary gate and a self-improvement mechanism: if the same gate fails on three consecutive batches, stop and propose a rule update via the feedback channel.

**EDGE CASE HANDLING** — nine-row table covering corrupted table cells, missing headings, pure-table pages, mixed languages, deeply nested lists, split dictionary entries, pages with no headings, near-empty pages, and conflicting heading levels. Each row specifies detection criteria and the exact action (preserve, flag with `<!-- NEEDS-HUMAN -->`, infer, or flatten).

**PERFORMANCE** — estimated 37 minutes for a full pass, ~2M tokens total, with notes that dictionary pages (400-434) take 40% longer due to structured entries. Includes optimization guidance (background launches, atomic batch commits, 3-minute hung-worker threshold).

The WHEN COMPLETE section also gained step 4: run `check-refined-all.py` across all 109 files after the full pass.
