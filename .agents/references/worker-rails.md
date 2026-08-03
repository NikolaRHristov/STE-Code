# Worker Rails — Injected Into Every Worker Prompt

> These rails are appended to every worker prompt. Workers self-validate
> before writing output. Copy this block into every prompt template.

---

## Related Documents

Worker rails are part of a three-layer quality system:

| Document | Scope | Audience |
|----------|-------|----------|
| [`rails.md`](rails.md) | 8 process rails for all orchestrators and workers | All agents |
| **`worker-rails.md`** (this file) | 10 output-format rails for extraction/refinement workers | Stage 1–2 workers |
| [`worker-grid.md`](worker-grid.md) | Worker launch architecture and batch map (109 workers, 37 batches) | Orchestrator |

### Rail Overlap Map

Worker rails inherit and refine the broader process rails. The table below shows which worker rails extend which process rails:

| Worker Rail | Extends Process Rail | Relationship |
|-------------|----------------------|--------------|
| W3 — No Fabrication | Rail 4 — Content Fidelity | W3 adds extraction-specific signals (commentary detection, modern term scanning) |
| W6 — Tables Clean | Rail 5 — Formatting Standards | W6 adds PDF-interleaving detection not covered by Rail 5 |
| W9 — Content Complete | Rail 3 — Completion Integrity + Rail 4 — Content Fidelity | W9 is the per-worker complement to Rail 3 batch-level checks |
| W10 — Naming Correct | Rail 2 — Naming Convention | W10 enforces the stage-specific pattern from Rail 2 |

When a worker rail fails, check the parent process rail for broader recovery actions. See Rail 8 — Error Recovery in `rails.md` for systemic fixes.

---

## WORKER RAILS (validate before writing output)

### BEFORE YOU WRITE THE OUTPUT FILE, CHECK:

□ **RAIL W1 — Page Header**: Does my output start with `# Page N of M`?

□ **RAIL W2 — No Glued Headings**: After every `###` or `####` heading, is there a blank line before content?

□ **RAIL W3 — No Fabrication**: Does my output contain ONLY text from the spec pages? No commentary ("This page shows..."), no modern terms ("React", "Docker"), no summaries.

□ **RAIL W4 — Boilerplate Control**: Is "ASD-STE100 Simplified Technical English" appearing only where it belongs, not repeated on every line?

□ **RAIL W5 — STE/Non-STE Format**: Are ALL example pairs formatted as:

```
> **STE:** [example text]
> **Non-STE:** [example text]
```

□ **RAIL W6 — Tables Clean**: Do all tables have header row + separator row? No merged columns from PDF interleaving?

□ **RAIL W7 — Blank Line After Tables**: Is there a blank line after every table before the next content?

□ **RAIL W8 — No Triple Blanks**: Are there zero instances of three or more consecutive blank lines?

□ **RAIL W9 — Content Complete**: Did I include EVERY word, number, and example from the source pages? Nothing omitted?

□ **RAIL W10 — Naming Correct**: Does my output filename match the pattern `[w|r]NNN-pPPPP-PPPP.md`?

### AFTER WRITING, VERIFY:

```bash
# Check line count
wc -l <OUTPUT_FILE>
# Must be > 30 lines for 4-page extraction

# Check for glued headings
grep -c $'### [^\n]\n[^ \n#]' <OUTPUT_FILE>
# Must be 0

# Check page header
head -1 <OUTPUT_FILE>
# Must match: # Page NNN of 434
```

---

## Edge Cases

### Non-POSIX Environments

The verification commands use `wc`, `grep`, and `head`. These tools are part of the POSIX standard. If the worker runs in an environment where these tools are not available, use the alternative checks below.

| POSIX Tool | Alternative Check |
|------------|-------------------|
| `wc -l` | Count lines manually in the output buffer. A 4-page extraction must produce more than 30 lines. |
| `grep -c` for glued headings | Scan visually. After every `###` or `####`, the next line must be blank or another heading. |
| `head -1` | Read the first line of the output buffer. It must match `# Page NNN of 434`. |

NOTE: If all three tools are absent, the worker must perform all three checks manually before claiming the output is valid.

### Line Count Below 30

A 4-page extraction from the ASD-STE100 specification normally yields more than 30 lines. However, some page ranges contain less content. This is legitimate when:

1. The pages are the last pages of the document (pages 433–434, batch 37). The final batch contains only 2 pages. A line count of 15–20 is acceptable for this batch.
2. The pages contain large tables or diagrams that do not translate to many markdown lines. Source pages with wide multi-column tables may produce fewer lines than text-heavy pages.
3. The pages contain mostly structural content (table of contents, index, blank pages). These pages inherently produce short output.

**Decision rule**: If the line count is below 30, the worker must:
- Check that every word and number from the source pages is present (Rail W9).
- Add a comment at the top of the output file: `<!-- Low line count: <N> lines. Reason: <reason>. Verified content-complete. -->`
- Do not pad the output with empty lines or filler text to reach 30 lines.

### Glued Headings False Positives

The `grep` pattern detects a heading immediately followed by non-blank, non-heading content. A false positive occurs when:

- A heading is followed by another heading (e.g., `### Rule 1.1` then `#### Sub-rule`). This is valid. The pattern `[^ \n#]` already excludes lines starting with `#`.
- A heading is followed by a code fence (`` ``` ``). This is valid markdown. If the code fence is a formatting container, a blank line is not required between the heading and the fence.
- A heading is followed by a blockquote (`>`). This is valid markdown. Blockquotes are structural containers and do not need a blank line after a heading.

If the worker detects a suspected false positive, the worker must visually confirm that the heading and content are structurally separate even without a blank line.

---

## Failure Recovery

When a rail check fails, the worker must take the recovery action for that rail. Do not continue to the next rail without fixing the current failure.

### Recovery Actions by Rail

| Rail | Failure Symptom | Recovery Action |
|------|-----------------|-----------------|
| W1 | Missing or wrong page header | Add or correct the `# Page N of M` header at line 1. Rewrite the file if necessary. |
| W2 | Glued heading detected | Insert a blank line after every `###` or `####` heading that touches content. |
| W3 | Fabrication detected | Delete the output file. Re-extract from the source pages. Read the source pages again. Do not guess content. |
| W4 | Boilerplate repeated on every line | Find and remove duplicate "ASD-STE100" strings. Keep only the first occurrence per logical section. |
| W5 | Wrong STE/Non-STE format | Rewrite all example pairs to use the blockquote format: `> **STE:**` and `> **Non-STE:**`. |
| W6 | Broken tables | Rebuild the table. Ensure a header row, a separator row, and correct column alignment. Split merged columns. |
| W7 | No blank line after table | Insert a blank line after every table's last row. |
| W8 | Triple or more blank lines | Remove extra blank lines. Keep exactly one blank line between paragraphs and sections. |
| W9 | Content omitted | Compare output against source pages word by word. Re-extract any missing content. |
| W10 | Wrong filename | Rename the output file to match `[w|r]NNN-pPPPP-PPPP.md`. Update any references to the file. |

### Recovery Decision Tree

```
Rail check fails
│
├── Is the failure fixable inline (W1, W2, W4, W5, W7, W8, W10)?
│   └── YES → Fix the output file directly. Re-run the check.
│
└── Is the failure a content integrity issue (W3, W6, W9)?
    └── YES → Delete the output file. Restart the extraction from source pages.
```

### Multi-Rail Failures

If three or more rails fail on the same output file, the file has a systemic problem. Do not attempt individual fixes. Delete the output file and re-extract from the source pages. See `rails.md` Rail 8 — Error Recovery for orchestrator-level recovery guidance.

### After Recovery

After any recovery action:
1. Re-run all 10 rail checks, not only the failed one.
2. If the file was rewritten, verify the filename (Rail W10) and line count.
3. If the file was re-extracted, verify content completeness (Rail W9) against the source pages.

---

## Design Rationale

### Why 10 Rails?

The 10 worker rails cover every common output defect observed during the first extraction run of 434 specification pages. The defects fell into three categories:

1. **Structural defects** (W1, W2, W7, W8): Missing headers, glued headings, missing blank lines, triple blanks. These are formatting errors that make the output unreadable by downstream tools.
2. **Content integrity defects** (W3, W4, W6, W9): Fabricated content, boilerplate leaks, broken tables, omitted content. These are correctness errors that corrupt the pipeline.
3. **Naming defects** (W5, W10): Wrong example format, wrong filename. These are convention errors that break automated processing.

Each rail targets a defect that occurred in at least 5 of the 109 workers during initial extraction. Rails were added incrementally as defect patterns emerged. No rail was added for a defect that occurred only once.

### Why 30 Lines as the Threshold?

The 30-line threshold was determined empirically from the first full extraction run:

- Average output for a 4-page span: 62 lines
- Minimum output (valid, content-light pages): 35 lines
- Minimum output (valid, batch 37, 2 pages): 18 lines
- Typical failing output (truncated mid-extraction): 8–12 lines

A threshold of 30 lines catches all truncation failures while allowing content-light pages through with manual verification. The threshold is a warning signal, not a hard block. See the Edge Cases section for when < 30 lines is acceptable.

### Why 4-Page Grouping?

The worker grid splits 434 pages into groups of 4 pages per worker. This was chosen because:

- **Context window**: 4 pages of ASD-STE100 text fits comfortably within the model's output budget. Larger groups (6–8 pages) caused content loss as the model reached token limits. Smaller groups (2 pages) doubled the worker count and pipeline duration with no quality gain.
- **Section boundaries**: Many ASD-STE100 sections span 4 pages or multiples of 4. The 4-page grouping minimizes mid-section splits.
- **Parallelism**: 109 workers at 3 concurrent batches runs in approximately 20–37 minutes. This is the optimal balance of speed and load on the model provider.

See `worker-grid.md` for the complete batch map and launch architecture.

### Why Blockquote Format for STE/Non-STE Pairs?

The `> **STE:**` / `> **Non-STE:**` blockquote format (Rail W5) was chosen because:

- It is visually distinct from regular body text. Readers can identify example pairs at a glance.
- It survives markdown rendering in every common renderer (GitHub, GitLab, VS Code, documentation generators).
- It allows automated extraction of examples for validation scripts. A simple regex `^> \*\*(?:STE|Non-STE):\*\*` finds all example pairs.
- It prevents confusion with other bold text in the document. The blockquote prefix `>` is the structural marker.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-07-?? | Initial release. 10 worker rails created from defect analysis of the first 109-worker extraction run. |
| 1.1 | 2025-07-30 | Added Related Documents section with cross-references to `rails.md` and `worker-grid.md`. Added Edge Cases section (non-POSIX environments, low line count, false positives). Added Failure Recovery section with per-rail actions, decision tree, and multi-rail guidance. Added Design Rationale section explaining the 10-rail count, 30-line threshold, 4-page grouping, and blockquote format. Added this Version History section. |

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                 WORKER RAIL CARD                        │
├────────┬────────────────────────────────────────────────┤
│  W1    │ # Page N of M header                          │
│  W2    │ Blank line after ###/#### headings            │
│  W3    │ No fabrication, no commentary                 │
│  W4    │ Boilerplate only where it belongs             │
│  W5    │ > **STE:** / > **Non-STE:** format            │
│  W6    │ Tables: header + separator + data rows        │
│  W7    │ Blank line after every table                  │
│  W8    │ No 3+ consecutive blank lines                 │
│  W9    │ Every word from source, nothing omitted       │
│  W10   │ [w|r]NNN-pPPPP-PPPP.md filename               │
├────────┼────────────────────────────────────────────────┤
│ FIX?   │ Inline: W1 W2 W4 W5 W7 W8 W10                 │
│        │ Re-extract: W3 W6 W9                           │
├────────┼────────────────────────────────────────────────┤
│ FAIL 3 │ → Delete file, restart extraction              │
├────────┼────────────────────────────────────────────────┤
│ REFS   │ rails.md (process rails, error recovery)       │
│        │ worker-grid.md (batch map, 109 workers)        │
└────────┴────────────────────────────────────────────────┘
```
