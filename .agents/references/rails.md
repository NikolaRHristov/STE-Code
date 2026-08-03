# Process Rails — Error Prevention for All Orchestrators and Workers

> Each orchestrator and worker MUST validate against these rails before claiming
> any action complete. Rails are non-negotiable guardrails.

---

## Related Documents

Process rails are part of a three-layer quality system:

| Document                             | Scope                                                              | Audience          |
| ------------------------------------ | ------------------------------------------------------------------ | ----------------- |
| **`rails.md`** (this file)           | 8 process rails for all orchestrators and workers                  | All agents        |
| [`worker-rails.md`](worker-rails.md) | 10 output-format rails for extraction/refinement workers           | Stage 1–2 workers |
| [`worker-grid.md`](worker-grid.md)   | Worker launch architecture and batch map (109 workers, 37 batches) | Orchestrator      |

### Rail Overlap Map

Worker rails (W1-W10) inherit and refine the broader process rails. The table
below shows which worker rails extend which process rails:

| Process Rail                  | Extended By           | Relationship                                                                                   |
| ----------------------------- | --------------------- | ---------------------------------------------------------------------------------------------- |
| Rail 4 — Content Fidelity     | W3 — No Fabrication   | W3 adds extraction-specific signals (commentary detection, modern term scanning)               |
| Rail 5 — Formatting Standards | W2, W6, W7, W8        | W2 adds glued-heading detection. W6 adds PDF-interleaving detection. W7, W8 add spacing rules. |
| Rail 3 — Completion Integrity | W9 — Content Complete | W9 is the per-worker complement to Rail 3 batch-level checks                                   |
| Rail 2 — Naming Convention    | W10 — Naming Correct  | W10 enforces the stage-specific pattern from Rail 2                                            |

When a worker rail fails, check this document for broader recovery actions. See
Rail 8 — Error Recovery for systemic fixes.

---

## RAIL 1: Stage Isolation

**Rule**: A process in Stage N MUST NOT write to Stage N+1 or Stage N-1
directories.

| Stage         | Directory    | Allowed Actions                                        |
| ------------- | ------------ | ------------------------------------------------------ |
| 1 — Extract   | `extracted/` | Write `w*-p*.md`. Read `spec/issue-09-2025/`.          |
| 2 — Refine    | `refined/`   | Read `extracted/`, write `r*-p*.md`.                   |
| 3 — Merge     | `merged/`    | Read `refined/` (or `extracted/`), write to `merged/`. |
| 4 — Adapt     | `adapted/`   | Read `merged/`, write to `adapted/`.                   |
| 5 — Artifacts | `artifacts/` | Read `adapted/`, write `.txt` files.                   |

**Violation**: Writing adaptation files while extraction is in Stage 1.
**Violation**: Placing files in `ste-code/` root instead of a stage directory.
**Violation**: Reading from `extracted/` when `refined/` is available (Stage
3+).

### Quality Gate

| Check                        | Threshold                         | Method                                                               |
| ---------------------------- | --------------------------------- | -------------------------------------------------------------------- |
| Files in correct directory   | 0 files in wrong stage directory  | `find <stage-dir> -name "*.md"` — all files must match stage pattern |
| No cross-stage writes        | 0 cross-stage write operations    | Audit file creation timestamps against PROGRESS.md stage markers     |
| Stage N reads Stage N-1 only | 0 reads from Stage N-2 or earlier | Verify file read paths in worker logs                                |

---

## RAIL 2: Naming Convention

**Rule**: All worker output files MUST follow the exact naming pattern.

| Stage     | Pattern               | Example                                |
| --------- | --------------------- | -------------------------------------- |
| Extract   | `wNNN-pPPPP-PPPP.md`  | `w001-p1-4.md`                         |
| Refine    | `rNNN-pPPPP-PPPP.md`  | `r001-p1-4.md`                         |
| Adapt     | `a-secN-ruleY.Z.md`   | `a-sec1-rule1.1.md`                    |
| Artifacts | `ste-code-<name>.txt` | `ste-code-distilled-system-prompt.txt` |

**Violation**: `w1-sec1-rules.md` (old style — must be `w001-p1-4.md`).
**Violation**: `coding-rules-part1-sec1.md` (wrong stage, wrong naming).

### Quality Gate

| Check                               | Threshold                                              | Method                                                            |
| ----------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------- |
| Filename matches stage pattern      | 100% of files match                                    | `ls <stage-dir>/` — every file must match the regex for its stage |
| Zero-width padding on worker number | 3 digits (e.g., `w001` not `w1`)                       | `grep -c '^w[0-9]{3}-'` must equal total worker file count        |
| Page range matches content          | Page numbers in filename match `# Page N of M` headers | Spot-check 5 random files                                         |

---

## RAIL 3: Completion Integrity

**Rule**: NEVER claim a batch, stage, or phase complete without verification.

**Before claiming "Batch N complete":**

- [ ] All 3 output files exist on disk
- [ ] Each file > 3KB (>30 lines)
- [ ] Last 3 lines end cleanly (no mid-word truncation)
- [ ] Update PROGRESS.md with [x]

**Before claiming "Stage complete":**

- [ ] All files for that stage exist (e.g., 109/109 for extraction)
- [ ] Coverage audit passes (all 434 pages accounted for)
- [ ] Spot-check 3 random files for content fidelity

**Violation**: PLAN.md claiming "CORE ARTIFACTS COMPLETE ✅" when 288 pages
unread. **Violation**: PROGRESS.md showing [x] for a batch whose files don't
exist.

### Quality Gate

| Check                  | Threshold                                                                     | Method                                                     |
| ---------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Files exist on disk    | 100% of expected files present                                                | `test -f <file>` for each file in batch                    |
| Minimum file size      | >3,072 bytes (>1,536 bytes for last batch)                                    | `stat -f%z <file>` or `wc -c < <file>`                     |
| Minimum line count     | >30 lines (>15 lines for last batch)                                          | `wc -l < <file>`                                           |
| No mid-word truncation | Last 3 lines end with sentence-ending punctuation or a complete word boundary | `tail -3 <file>` — no trailing partial words               |
| PROGRESS.md updated    | 1 update per batch, timestamped, after verification                           | Check PROGRESS.md modification time vs. file creation time |

NOTE: The 30-line threshold is a warning signal, not a hard block. Content-light
pages (tables, diagrams, front matter) may produce fewer than 30 lines
legitimately. See Known Limitations below for edge cases.

---

## RAIL 4: Content Fidelity

**Rule**: NEVER fabricate, summarize, or adapt content that isn't backed by
source data.

**Extraction workers**: Output EXACT spec text. Never:

- Add commentary ("This page describes...")
- Add modern terms not in the spec
- Summarize instead of extracting fully

**Refinement workers**: Reformat only. Never:

- Delete any word, number, or example
- Merge different examples into one
- Change rule numbers or section structure

**Adaptation workers**: Ground every claim. Never:

- Write an adapted rule without referencing the original rule from master.md
- Invent synonyms not in the original synonym table
- Claim a category count without verifying against master.md

**Fabrication detection signals** (if output contains any of these, it's
fabricated):

- Modern software terms in spec extraction: "React", "Docker", "npm",
  "async/await"
- Commentary language: "This page describes", "The key point is", "In summary"
- Missing spec boilerplate: no "ASD-STE100" header
- Wrong facts: "22 categories", "deepseek-pro normalizes to flash", "hermes -z
  doesn't support file I/O"

### Quality Gate

| Check                             | Threshold                                                | Method                                                                       |
| --------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Fabrication signal scan           | 0 banned terms found                                     | `grep -c -E 'React                                                           | Docker | npm | async/await | This page describes | The key point is | In summary' <file>` |
| Boilerplate present               | "ASD-STE100" appears at least once                       | `grep -c 'ASD-STE100' <file>` must be ≥1                                     |
| Source-backed claims (adaptation) | Every adapted rule references a source rule in master.md | Spot-check 5 random adapted files for `See Rule X.Y` or equivalent reference |

---

## RAIL 5: Formatting Standards

**Rule**: All markdown output MUST follow these rules.

### Headings

```
✅ # Page N of M          ← Every file starts with this
✅ ## Section Title        ← Major sections
✅ ### Rule X.Y            ← Rule headings
✅ #### WORD (POS)         ← Dictionary entries (refined format)

❌ ### ASD-STE100          ← Proper names are not headings
❌ ### Heading\nText       ← NEVER glue heading to text
```

### Spacing

```
✅ ### Heading            ← Heading
✅                        ← BLANK LINE (mandatory)
✅ Content starts here    ← Content

❌ ### Heading            ← Heading
❌ Content starts here    ← NO blank line = GLUED
```

### Tables

```
✅ | Header | Header |    ← Header row
✅ |--------|--------|    ← Separator row
✅ | Cell   | Cell   |    ← Data rows
✅                        ← BLANK LINE after table

❌ | Cell |\nNext text     ← No blank line after table
```

### STE/Non-STE Examples

```
✅ > **STE:** [example text]
✅ > **Non-STE:** [example text]

❌ STE: [text]             ← Must use blockquote + bold label
❌ Non-STE: [text] on same line as STE
```

### Dictionary Entries (refined format)

```
✅ #### WORD (POS) — APPROVED
✅ - **Meaning:** [text]
✅ - **Forms:** [form1, form2]
✅ - **STE:** [example]
✅ - **Non-STE:** [example]

❌ Word | Meaning merged in one column  ← Raw extraction format, not refined
```

### Quality Gate — Numeric Thresholds

| Check                         | Threshold                                                 | Method                                                                       |
| ----------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Glued headings                | ≤0 instances                                              | `grep -c $'### [^\\n]\\n[^ \\n#]' <file>` — must return 0                    |
| Blank line after tables       | 0 missing blank lines                                     | Visual scan: every table's last row must be followed by a blank line or EOF  |
| Triple (or more) blank lines  | ≤0 instances                                              | `grep -c $'\\n\\n\\n\\n' <file>` — must return 0                             |
| Blockquote STE/Non-STE format | 100% of example pairs use `> **STE:**` / `> **Non-STE:**` | `grep -c '^> \*\*STE:\*\*' <file>` — count must match expected example pairs |
| Page header on line 1         | 100% of files start with `# Page N of M`                  | `head -1 <file>` must match pattern                                          |
| Code fence nesting resolved   | 0 unterminated code fences                                | `grep -c '```' <file>` must be even                                          |

BREAKING: Glued headings can cause downstream parsers to merge unrelated
content. The threshold is zero — any glued heading is a failure.

---

## RAIL 6: Factual Correctness

**Rule**: These facts are immutable. Never claim otherwise.

| Fact                                                 | Wrong Claim (never make)              |
| ---------------------------------------------------- | ------------------------------------- |
| STE has 19 technical noun categories                 | "22 categories"                       |
|                                                      | Model is `poolside/laguna-s-2.1:free` | "deepseek-pro" or "deepseek-v4-flash" |
| `hermes -z` supports file I/O                        | "hermes -z does not support file I/O" |
| 53 writing rules + 4 GR rules                        | 65 rules (Issue 6 count)              |
| Output is `.md` files                                | "JSON structured data"                |
| Stage directories are `extracted/`, `refined/`, etc. | "workers/"                            |

### Meta-Instruction: Keeping Facts Current

This rail contains hardcoded facts that MAY DRIFT when project constants change.
The facts in this rail are derived from the following sources:

| Fact                          | Source File                                              | Update Trigger                             |
| ----------------------------- | -------------------------------------------------------- | ------------------------------------------ |
| 19 technical noun categories  | `ste-code/adapted/a-sec1-rule1.5.md`                     | A new category is added or removed         |
|                               | Model name `poolside/laguna-s-2.1:free`                  | `.agents/AGENTS.md` — Model field          | The model changes (update in AGENTS.md first, then here) |
| 53 writing rules + 4 GR rules | `ste-code/adapted/` — count of `a-secN-ruleY.Z.md` files | Rules are added, split, or merged          |
| Output format `.md`           | Pipeline specification                                   | A new output format is introduced          |
| Stage directory names         | `ste-code/` directory structure                          | Pipeline stages are renamed or reorganized |

**Update procedure**: When a project constant changes, update the source file
first. Then update this rail's fact table within the same commit. Do NOT let the
source file and this rail diverge.

**Drift check** (run monthly or after any pipeline reconfiguration):

```bash
# Check category count
grep -c "^## Category" ste-code/adapted/a-sec1-rule1.5.md
# Must equal 19. If not, update Rail 6.

# Check rule count
ls ste-code/adapted/a-sec*-rule*.*.md | wc -l
# Must equal 57 (53 writing rules + 4 GR rules). If not, update Rail 6.

# Check model name
grep "Model:" .agents/AGENTS.md
# Must match Rail 6 fact table. If not, update Rail 6.
```

---

## RAIL 7: Progress Tracking

**Rule**: PROGRESS.md must reflect reality. Never lie to the tracker.

- Update PROGRESS.md AFTER verification, never before.
- If a worker fails, mark it [!] not [x].
- If re-extracting, revert [x] to [ ] until verified again.
- Timestamp all updates.

### Quality Gate

| Check                                  | Threshold                                | Method                                                                      |
| -------------------------------------- | ---------------------------------------- | --------------------------------------------------------------------------- |
| PROGRESS.md updated after verification | Modification time > last file write time | `stat -f%m .agents/state/PROGRESS.md` vs. file timestamps                   |
| No [x] markers on missing files        | 0 mismatches between [x] and disk        | Cross-reference PROGRESS.md [x] entries with `test -f` on each output file  |
| Timestamps present                     | Every update line has a timestamp        | `grep -c '^\{20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]' .agents/state/PROGRESS.md` |

---

## RAIL 8: Error Recovery

**Rule**: When a mistake is detected, fix it. Do not hide it.

| Mistake                     | Recovery Action                                  |
| --------------------------- | ------------------------------------------------ |
| Truncated worker output     | Split page range in half, re-extract both        |
| Fabricated content detected | Delete file, re-extract from spec                |
| Wrong naming convention     | Rename file to correct pattern                   |
| Missing PROGRESS.md update  | Update immediately, note the correction          |
| Premature adaptation files  | Move to `_scratch/`, regenerate after extraction |
| Model reference wrong       | Patch to correct model name                      |

### Quality Gate

| Check                                | Threshold                                                  | Method                                                                  |
| ------------------------------------ | ---------------------------------------------------------- | ----------------------------------------------------------------------- |
| Recovery documented                  | Every error has an entry in `.agents/feedback/exchange.md` | Check exchange.md for error entries matching [!] markers in PROGRESS.md |
| No hidden errors                     | 0 unreported failures                                      | Cross-reference PROGRESS.md [!] count with exchange.md error entries    |
| Recovery successful after ≤3 retries | Recovered worker passes all gates                          | Re-run verification gates on recovered output                           |

---

## Known Limitations

### Glued Heading Detection

The `grep` pattern for glued heading detection has known limitations:

| Limitation                                      | Description                                                                                                                                                             | Impact                                                                  |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| False positive: heading followed by heading     | `### Rule 1.1` then `#### Sub-rule` — the pattern `[^ \n#]` already excludes lines starting with `#` but may not exclude all edge cases in non-GNU grep implementations | Low — visual confirmation resolves                                      |
| False positive: heading followed by code fence  | `### Heading` then ` ``` ` — a code fence is valid markdown after a heading without a blank line                                                                        | Medium — code fence containers should not trigger glued-heading failure |
| False positive: heading followed by blockquote  | `### Heading` then `> text` — blockquotes are structural containers and do not require a blank line                                                                     | Medium — blockquote containers should not trigger glued-heading failure |
| False negative: grep implementation differences | Some `grep` implementations (BSD grep on macOS, BusyBox grep) handle `$'...\n...'` differently than GNU grep                                                            | Low — may miss genuine glued headings; supplement with visual scan      |
| False negative: Unicode or non-ASCII headings   | Headings containing Unicode characters may not match the `[^ \n#]` character class as expected                                                                          | Very low — ASD-STE100 content is ASCII                                  |

**Mitigation**: Do not rely on `grep` alone for glued heading detection. The
automated check is a first pass. Always follow with a visual scan of 3 random
headings per file. If the worker environment lacks GNU grep, perform the check
manually.

### Line Count Threshold

The 30-line minimum threshold for a 4-page extraction is an empirical heuristic
with known edge cases:

| Edge Case                  | Affected Workers             | Legitimate Line Count | Handling                                                                                             |
| -------------------------- | ---------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------- |
| Last batch (2 pages)       | W109 (pages 433-434)         | 15–20 lines           | Threshold lowered to 15 lines for batch 37                                                           |
| Table-heavy pages          | W088-W099 (dictionary pages) | 20–30 lines           | Wide multi-column tables produce fewer markdown lines; check content completeness manually           |
| Front matter / index pages | W001 (pages 1-4)             | 10–25 lines           | Structural content inherently produces short output; verify page header and boilerplate presence     |
| Diagram-heavy pages        | Various                      | 15–25 lines           | Diagrams do not produce markdown text; verify that all text content from the source pages is present |

**Decision rule**: If line count is below 30 and the worker is NOT in batch 37,
add a comment at the top of the output file:
`<!-- Low line count: <N> lines. Reason: <reason>. Verified content-complete. -->`.
Do not pad the output to reach 30 lines.

### Fact Table Drift

The facts in Rail 6 are static strings that can drift when the project evolves.
The meta-instruction above provides a drift check procedure. However, note that
the drift check itself depends on the source files being correct — it cannot
detect if both the source file and Rail 6 are wrong in the same way. A human
review of Rail 6 facts is recommended after any major pipeline reconfiguration
or model change.

### Cross-Stage Verification Gaps

Rails 1-8 cover process-level correctness but do not cover:

- **Semantic correctness**: A file may pass all format and naming checks but
  contain logically wrong content (e.g., extracted text from the wrong
  specification issue). Spot-checks (Rail 3) mitigate this but do not eliminate
  it.
- **Inter-file consistency**: Two adapted files may both pass their individual
  checks but contradict each other (e.g., one file says 19 categories, another
  says 22). A cross-file audit is not part of the process rails — it is the
  Auditor agent's responsibility.
- **Pipeline state corruption**: PROGRESS.md may be correct but the actual state
  of files on disk may not match due to filesystem errors, git conflicts, or
  manual edits outside the pipeline. Run `git status` before each batch launch
  to detect unexpected changes.

---

## Relationship to Worker Rails

The `worker-rails.md` document defines 10 worker-level rails (W1-W10) that
specialize the process rails for extraction and refinement workers. The
relationship is hierarchical:

```
Process Rails (R1-R8) — all agents, all stages
├── Rail 1: Stage Isolation ────────────── (no worker-rail equivalent; orchestrator-only)
├── Rail 2: Naming Convention ─────────── extended by → W10 (Naming Correct)
├── Rail 3: Completion Integrity ──────── extended by → W9 (Content Complete)
├── Rail 4: Content Fidelity ──────────── extended by → W3 (No Fabrication)
├── Rail 5: Formatting Standards ──────── extended by → W2, W5, W6, W7, W8
├── Rail 6: Factual Correctness ──────── (no worker-rail equivalent; shared reference)
├── Rail 7: Progress Tracking ─────────── (no worker-rail equivalent; orchestrator-only)
└── Rail 8: Error Recovery ────────────── referenced by → worker recovery decision tree
```

Worker rails that have NO process-rail parent (W1, W4) are worker-specific
concerns:

- **W1 (Page Header)**: Specific to extraction workers that produce per-page
  output files.
- **W4 (Boilerplate Control)**: Specific to ASD-STE100 extraction where document
  headers can leak into every line.

### When to Use Which

| Situation                                            | Reference                                                                                                 |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Launching a batch of extraction workers              | `worker-grid.md` for batch map + `worker-rails.md` for W1-W10 checks                                      |
| Verifying a batch is complete                        | `rails.md` Rail 3 — Completion Integrity                                                                  |
| A worker output has glued headings                   | `worker-rails.md` Rail W2 for detection, `rails.md` Rail 5 for the formatting standard                    |
| A worker fabricated content                          | `worker-rails.md` Rail W3 for detection, `rails.md` Rail 4 for the fidelity standard, Rail 8 for recovery |
| An orchestrator script writes to the wrong directory | `rails.md` Rail 1 — Stage Isolation (no worker-rail equivalent)                                           |
| Three or more worker rails fail on the same file     | `worker-rails.md` multi-rail failure guidance + `rails.md` Rail 8 for systemic fix                        |

---

## Design Rationale

### Why 8 Process Rails?

The 8 process rails cover every category of systemic failure observed across
multiple pipeline runs:

1. **Structural failures** (R1, R2, R5): Files in wrong directories, wrong
   names, wrong formatting. These break automated processing.
2. **Integrity failures** (R3, R4, R6, R7): Claimed completion without
   verification, fabricated content, wrong facts, lying to the tracker. These
   corrupt downstream stages.
3. **Recovery failures** (R8): Mistakes hidden instead of fixed. These compound
   errors across stages.

Each rail was added after a real failure event, not pre-emptively. No rail
exists for a hypothetical failure mode.

### Why Rails Are Non-Negotiable

Rails are not guidelines. They are guardrails. A guideline can be skipped when
convenient. A rail cannot — violating a rail means the action is incomplete,
regardless of what the agent claims. This distinction is critical because
language models are prone to declaring success prematurely. Rails are the
objective check against subjective claims.

### Why Numeric Thresholds

Where possible, rails include numeric thresholds (0 glued headings, >3KB file
size, >30 lines). Numeric thresholds are:

- **Objective**: Two different auditors checking the same file will reach the
  same conclusion.
- **Automated**: Scripts can verify thresholds without human judgment.
- **Stable**: Thresholds do not change based on the auditor's mood, fatigue, or
  interpretation.

Non-numeric checks (spot-checks, visual scans) are reserved for semantic quality
dimensions that cannot be reduced to a number.

### Why This Document Is Separate from worker-rails.md

Process rails and worker rails serve different audiences at different
granularities:

- **Process rails**: Apply to ALL agents across ALL stages. An orchestrator, an
  auditor, and a refinement worker all validate against Rail 3 (Completion
  Integrity).
- **Worker rails**: Apply ONLY to Stage 1-2 workers. A merge worker does not
  need to check for page headers (W1) or boilerplate leaks (W4).

Keeping them separate prevents worker-specific details from cluttering the
process-level rules, and prevents process-level rules from being overlooked
because they are buried in worker-specific documentation.

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────────────────┐
│                    PROCESS RAIL CARD                             │
├──────┬───────────────────────────────────────────────────────────┤
│  R1  │ Stage Isolation — write only to current stage directory   │
│  R2  │ Naming Convention — exact pattern per stage               │
│  R3  │ Completion Integrity — verify before claiming complete    │
│  R4  │ Content Fidelity — no fabrication, no commentary          │
│  R5  │ Formatting Standards — blank lines, tables, STE format    │
│  R6  │ Factual Correctness — 19 categories, poolside/laguna-s-2.1:free, 53  │
│  R7  │ Progress Tracking — PROGRESS.md reflects reality          │
│  R8  │ Error Recovery — fix mistakes, do not hide them           │
├──────┼───────────────────────────────────────────────────────────┤
│ GATE │ R1: 0 cross-stage writes                                  │
│      │ R2: 100% filenames match pattern                          │
│      │ R3: >3KB, >30 lines, clean truncation, [x] in PROGRESS.md │
│      │ R4: 0 banned terms, ASD-STE100 header present             │
│      │ R5: 0 glued headings, 0 triple blanks, 0 missing blanks   │
│      │ R6: Facts match source files (run drift check monthly)    │
│      │ R7: Timestamps, no [x] orphans, update after verify       │
│      │ R8: Every [!] has exchange.md entry, ≤3 retries           │
├──────┼───────────────────────────────────────────────────────────┤
│ SELF │ □ Did I write to the correct stage directory?             │
│CHECK │ □ Does my file follow the naming convention?              │
│      │ □ Did I verify before claiming complete?                  │
│      │ □ Is my content backed by source data (not fabricated)?   │
│      │ □ Are my headings separated from text by blank lines?     │
│      │ □ Are my facts correct (19 categories, poolside/laguna-s-2.1:free)?  │
│      │ □ Did I update PROGRESS.md with the real status?          │
├──────┼───────────────────────────────────────────────────────────┤
│ REFS │ worker-rails.md — 10 worker output rails (W1-W10)         │
│      │ worker-grid.md — batch map, launch architecture           │
│      │ exchange.md — inter-agent error reports                   │
└──────┴───────────────────────────────────────────────────────────┘
```

---

## Self-Check Checklist (run after every action)

```
□ Did I write to the correct stage directory?           [Rail 1]
□ Does my file follow the naming convention?             [Rail 2]
□ Did I verify before claiming complete?                 [Rail 3]
□ Is my content backed by source data (not fabricated)?  [Rail 4]
□ Are my headings separated from text by blank lines?    [Rail 5]
□ Are my facts correct (19 categories, poolside/laguna-s-2.1:free, 53 rules)?  [Rail 6]
□ Did I update PROGRESS.md with the real status?         [Rail 7]
□ If I found a mistake, did I fix it (not hide it)?      [Rail 8]
```

---

## Version History

| Version | Date       | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2025-07-15 | Initial release. 8 process rails created from defect analysis of the first pipeline run. Rails 1-8 defined.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 1.1     | 2025-07-22 | Added Rail 6 (Factual Correctness) with static fact table. Added Quick Self-Check section.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 1.2     | 2025-07-28 | Added Rail 7 (Progress Tracking) and Rail 8 (Error Recovery).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| 1.3     | 2025-07-30 | Added Related Documents section with cross-references to `worker-rails.md` and `worker-grid.md`. Added Rail Overlap Map showing which worker rails extend which process rails. Added Quality Gate subsections to Rails 1-8 with numeric thresholds. Added Known Limitations section (glued heading detection edge cases, line count threshold edge cases, fact table drift risk, cross-stage verification gaps). Added Relationship to Worker Rails section documenting the hierarchical relationship. Added Design Rationale section (why 8 rails, why non-negotiable, why numeric thresholds, why separate from worker-rails.md). Added meta-instruction to Rail 6 for keeping facts current with source files and a drift check procedure. Upgraded Quick Self-Check to a Quick Reference Card with gate thresholds and reference pointers. Added this Version History section. |
