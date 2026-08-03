---
name: extraction
description: > **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
category: dev
capability: developing-and-changing-the-standard
source: /Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code/.agents/skills/extraction
layout: ste-code-canonical-v1
---

# Extraction Worker Orchestration

> **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
> Session isolation + STRICT_RULES (R1-R6) from `lib/pipeline_core.py` apply to
> THIS skill. One session = one operation = one read + one write. No re-editing
> own output.

Extract the 434-page ASD-STE100 Issue 9 spec using 109 parallel `hermes -z`
workers. Each worker processes exactly 4 pages. Coordinate the workers in 37
batches of 3. This skill is agent-agnostic. Any agent can use it.

## Design Rationale

### Why 4 Pages per Worker

A worker with fewer than 4 pages wastes launch overhead. A worker with more than
4 pages causes these problems:

- Truncation. The model output limit cuts content at ~4 pages of dense spec
  text.
- Quality degradation. The model skips details when the input is too large.
- Recovery cost. A failed 8-page worker needs 2 re-extractions. A failed 4-page
  worker needs only 1.

Four pages gives the best balance of throughput, quality, and fault isolation.

### Why Batches of 3

Three workers per batch gives these benefits:

- **Verification window.** You check 3 outputs after each batch. This catches
  failures early.
- **Resource safety.** Too many parallel `hermes -z` calls can exhaust API rate
  limits or local memory.
- **State checkpoint frequency.** A git commit after each batch (37 total) gives
  fine-grained rollback points.

### Why 109 Workers for 434 Pages

434 pages / 4 pages per worker = 108.5 workers. Round up to 109.

The last worker (W109) processes only 2 pages (pages 433-434). This is correct.
Do not redistribute pages to make all workers equal. Uneven last batches are
better than changing the page-per-worker rule.

### Total Time Estimate

| Phase                                  | Duration      |
| -------------------------------------- | ------------- |
| 1 batch (3 workers)                    | 30-60 seconds |
| 37 batches                             | 20-37 minutes |
| With re-extractions (10% failure rate) | 25-45 minutes |

## Worker Command Template

```bash
hermes -z "Read spec/issue-09-2025/page-dir/page-<<START>>.md through page-<<END>>.md. \
Extract ALL content exactly into ste-code/extracted/w<<NNN>>-p<<START>>-<<END>>.md.\
Do not summarize. Include every word, every table, every example.\
Output ONLY the markdown file." -m poolside/laguna-s-2.1:free --yolo
```

NOTE: Page files now use spec page identifiers (e.g., page-HI-1.md,
page-1-1-1.md) in the page-dir/ subdirectory, not sequential page-NNNN.md
numbering. Use spec/issue-09-2025/split_spec.py to regenerate page files from
the combined issue-09-2025.md.

## Launch Rules

- **ALWAYS PRESERVE** existing extracted files. Never `rm` or overwrite files in
  `ste-code/extracted/` that already exist. If a file already exists and passes
  quality checks, skip it. If it exists but fails, delete only that one file and
  re-extract.
- **Always** use `hermes -z` with the oneshot wrapper (via agent-runner)
- **Always** launch exactly 3 workers per batch. Do not launch more.
- **Always** verify output after each batch before you launch the next batch.
- **Never** use inline extraction. It defeats parallelization.
- **Never** exceed 4 pages per worker. This prevents truncation.
- **Always** save state. Use `git gcommit-hermes` after each batch.
- If running in a new session with existing extracted files from a previous run,
  **check what already exists** and skip already-extracted worker ranges. Resume
  from the first missing worker.

## Concurrent Session Handling

If multiple sessions launch `extract_batch.py`:

- Each checks existing files and skips already-completed workers
- Worker output files use deterministic names (`wNNN-pSTART-END.md`) — the same
  worker will produce the same filename
- If a file already exists and passes quality gates, the worker is skipped
  (marked "already extracted")
- **Never** clear the entire `ste-code/extracted/` directory — only delete
  individual files that fail verification

## Expected Output Format

A correct extraction file must follow this structure.

### File Header

```markdown
# Page NNN of 434
```

Every file starts with this exact line. The page number is the first page in the
worker range.

### Section Structure

```markdown
# Page 129 of 434

## Section Title From Spec

Content paragraph. Preserve all text exactly.

### Subsection

More content. Do not add commentary. Do not summarize.

#### DICT ENTRY (POS) - APPROVED

- **Meaning:** exact approved meaning from spec
- **Forms:** form1, form2, form3
- **STE:** approved example sentence
- **Non-STE:** non-approved example sentence
```

### What Good Output Looks Like

This is a correct extraction from the DICT section (pages 129-132, worker W033):

```markdown
# Page 129 of 434

## Dictionary - A

#### ABILITY (n) - APPROVED

- **Meaning:** The quality of being able to do something
- **STE:** Make sure that the component has the ability to move freely.
- **Non-STE:** Ascertain that the unit possesses the capability of free
  movement.

#### ABLE (adj) - APPROVED

- **Meaning:** Having the power, skill, or means to do something
- **STE:** The technician must be able to remove the panel.
- **Non-STE:** It shall be possible for the technician to accomplish panel
  removal.

#### ABOVE (prep) - APPROVED

- **Meaning:** In or to a higher position than
- **STE:** Install the bracket above the valve.
- **Non-STE:** The bracket shall be positioned superjacent to the valve
  assembly.

#### ABSORB (v) - APPROVED

- **Meaning:** To take in a liquid or gas
- **Forms:** absorbs, absorbed, absorbing
- **STE:** The filter absorbs unwanted particles.
- **Non-STE:** The filtration mechanism entraps and retains undesirable
  particulate matter.
```

### What Corrupted Output Looks Like

These examples show common failure modes. If you see any of these patterns, the
extraction failed.

#### Truncation (mid-word cut)

```markdown
#### ACCESS (n) - APPROVED

- **Meaning:** The right or opportunity to use or benefit from something
- **STE:** You must have access to the contr
```

The last word is cut. The file ends in the middle of a sentence. This is the
most common failure.

#### Fabrication (invented content)

```markdown
# Page 129 of 434

This page describes the ASD-STE100 dictionary section. The key point is that
approved words must be used in technical documentation. In summary, this section
lists approximately 900 approved words organized alphabetically.

TODO: Add remaining dictionary entries for letters A through C. TBD: Verify word
count against master index.
```

Signals of fabrication: commentary language, "TODO", "TBD", modern software
terms, summaries instead of raw extraction.

#### Glued Headings (missing blank line)

```markdown
#### ABOVE (prep) - APPROVED

- **Meaning:** In or to a higher position than

#### ABSORB (v) - APPROVED

- **Meaning:** To take in a liquid or gas
```

Headings have no blank line between entries. The content runs together. This
fails the formatting rail (RAIL 5).

#### Wrong Section Type Extraction

```markdown
# Page 43 of 434

### Rule 1.1

Use approved words from the dictionary.

Wait, actually let me check the spec again. The rule says...
```

The worker is thinking aloud instead of extracting. It adds meta-commentary.
This is fabrication.

#### Missing Spec Boilerplate

```markdown
# Page 1 of 434

## Front Matter

Some text about the standard.
```

No "ASD-STE100" header. No copyright text. No issue number. The worker
summarized the front matter instead of extracting it.

## Edge Cases

### Multi-Page Tables

Some spec tables span 2 or more pages. For example, the change history table in
Appendix A crosses pages 363-366.

**Detection.** A page ends with a table row that has no closing context. The
next page starts with a continuation of that table.

**Handling.** The worker must:

1. Extract the table start on the first page.
2. Note the continuation: `<!-- TABLE CONTINUES ON NEXT PAGE -->`
3. Extract the remainder on the next page.
4. The merge stage (Stage 3) joins the table parts.

**Worker prompt addition for table boundary pages:**

```
If a table starts on this page but does not finish, add this marker at the cut point:
<!-- TABLE CONTINUES ON NEXT PAGE -->
Do not invent table rows to close the table.
```

### Pages with Images or Diagrams

Some spec pages contain flowcharts, decision trees, or structural diagrams. For
example, page 361 has the word approval flowchart.

**Handling.** The worker must:

1. Describe the diagram structure in text. Use `[DIAGRAM: description]` markers.
2. Extract all text labels from the diagram.
3. Preserve the decision logic as a numbered list.

**Format for diagram pages:**

```markdown
[DIAGRAM: Word approval decision flowchart]

The flowchart has these decision points:

1. Is the word in the dictionary? → YES: go to step 2. NO: go to step 5.
2. Is the word approved? → YES: use the word. NO: go to step 3. ...
```

### Empty or Near-Empty Appendix Pages

Pages 433-434 may be nearly empty. They contain only a change form template or
blank space.

**Handling.** Extract what exists. Do not pad with invented content. A 1KB file
for a nearly empty page is correct.

**Quality check override for empty pages:**

For workers W108-W109 (pages 429-434), lower the size threshold to 500 bytes.
These pages have less content.

### Non-English Characters

The ASD-STE100 spec includes some non-English characters:

- French accents in reference document titles (e.g., "Système International")
- German umlauts in manufacturer names
- Greek letters in technical symbols (e.g., µ for micro)

**Handling.** Preserve all non-English characters exactly. Use UTF-8 encoding.
Do not transliterate or strip them.

### Section Boundaries Inside a Worker Range

A 4-page range may cross a section boundary. For example, W016 covers pages
61-64. Page 66 ends the CATEGORIES section. Page 67 starts the RULES section
(continuation).

**Handling.** The worker must use the correct extraction prompt for each section
type within its range. See `.agents/references/section-types.md` for the
per-type prompts.

Refer to the page range reference in `section-types.md` to know which section
types fall in each worker range.

## Expected Keywords (Quality Check 4)

Quality check 4 says "Expected keywords present." The expected keywords depend
on the section type of the worker pages. Use this table.

| Section Type | Pages   | Expected Keywords (must find at least 3)                                               |
| ------------ | ------- | -------------------------------------------------------------------------------------- |
| FRONT        | 1-12    | "ASD-STE100", "Issue 9", "Copyright", "EU trademark", "Disclaimer", "Highlights"       |
| TOC          | 13-16   | "Table of Contents", "Rule", "Section", "Dictionary", "Appendix"                       |
| INDEX        | 17-24   | "Index", "Rule", "Page", subject-area terms                                            |
| INTRO        | 25-42   | "How to use", "Writing rules", "Dictionary", "Technical names", "Approved"             |
| RULES        | 43-128  | "Rule", "STE:", "Non-STE:", rule number pattern like "1.1"                             |
| CATEGORIES   | 47-66   | "Category", "Technical name", "Examples:", numbered list                               |
| DICT         | 129-360 | "APPROVED", "UNAPPROVED", "Meaning:", "STE:", "Non-STE:", part-of-speech abbreviations |
| APPENDIX     | 361-434 | "Appendix", "Issue", "Change", "Flowchart", "Index", "Form"                            |

**Check procedure for each batch:**

1. Identify the section types in this batch from the page range reference.
2. Check each output file for at least 3 keywords from its type row.
3. If fewer than 3 keywords match, the extraction may be fabricated or badly
   truncated.
4. Mark the file for re-extraction.

## Quality Checks (Per Batch)

1. All 3 output files exist in `ste-code/extracted/`
2. Each file > 3KB (>30 lines). Exception: Appendix pages 429-434 allow >500
   bytes.
3. Last 3 lines end cleanly. No mid-word truncation.
4. Expected keywords present. Use the keyword table above.
5. No fabrication signals. Reject these patterns:
    - Commentary: "This page describes", "The key point is", "In summary"
    - Placeholders: "TODO", "TBD", "FIXME", "Insert content here"
    - Modern software terms (fabrication in spec context): "React", "Docker",
      "npm", "async/await", "API endpoint", "microservices"
    - Meta-commentary: "Let me check", "I will now extract", "Wait, actually"
6. PROGRESS.md updated with `[x]` for completed workers

If any check fails, re-extract with the worker page range split in half.

## Failure Recovery Procedures

### Recovery for a Truncated Worker

If worker W042 (pages 165-168) produces truncated output:

1. Delete the bad file: `rm ste-code/extracted/w042-p165-168.md`
2. Split the range: W042a (pages 165-166) and W042b (pages 167-168)
3. Launch both sub-workers. Use the same command template.
4. After both complete, concatenate the outputs:
    ```bash
    cat ste-code/extracted/w042a-p165-166.md \
    	ste-code/extracted/w042b-p167-168.md \
    	> ste-code/extracted/w042-p165-168.md
    ```
5. Remove the sub-worker files.
6. Run quality checks on the concatenated file.
7. Mark PROGRESS.md `[x]` only after all checks pass.

### Recovery for Fabricated Content

If a worker output contains fabrication signals:

1. Delete the file immediately. Do not try to salvage it.
2. Check the worker prompt. Was the command template followed exactly?
3. Re-launch with a stronger prompt. Add this line:
    ```
    CRITICAL: Output ONLY the raw spec text. Do not add commentary.
    Do not summarize. Do not use the words "describes" or "key point".
    ```
4. If the second attempt also fabricates, split the range in half and try both
   halves.

### Recovery for a Silent Worker Failure

If a worker produces no output file:

1. Check if the `hermes -z` process is still running. Use
   `process action='list'`.
2. If running, wait 120 seconds. Some workers take longer for dense pages.
3. If still no output after 120 seconds, kill the process.
4. Re-launch with the same page range.
5. If it fails again, split the range in half.

### Batch Recovery Checklist

For any batch that fails quality checks:

- [ ] Identify which of the 3 workers failed.
- [ ] Determine the failure mode (truncation, fabrication, missing file, wrong
      format).
- [ ] Apply the matching recovery procedure.
- [ ] Run quality checks on the recovered output.
- [ ] Update PROGRESS.md. Mark failed workers `[!]` until recovery succeeds.
- [ ] Git commit only after all 3 workers in the batch pass checks.

## Batch Lifecycle

Each batch follows this exact sequence.

```
LAUNCH → MONITOR → VERIFY → COMMIT → NEXT

1. LAUNCH: Start 3 hermes -z workers in background.
2. MONITOR: Wait for all 3 to finish. Check exit codes.
3. VERIFY: Run all 6 quality checks on each output file.
4. COMMIT: git gcommit-hermes "Batch N complete - W###, W###, W###"
5. NEXT: Proceed to batch N+1 or report completion.
```

Do not skip a step. Do not reorder the steps. Do not commit before verification.

## Progress Tracking Format

PROGRESS.md must use this format for each batch:

```markdown
## Batch 01 - Pages 1-12

- [x] W001 (1-4) - FRONT - 4.2KB, 87 lines - 2025-07-30 14:22 UTC
- [x] W002 (5-8) - FRONT - 3.9KB, 72 lines - 2025-07-30 14:23 UTC
- [x] W003 (9-12) - FRONT - 4.1KB, 79 lines - 2025-07-30 14:23 UTC
```

Status markers:

- `[ ]` - Not started
- `[~]` - In progress (workers launched, not yet verified)
- `[x]` - Complete (all quality checks passed)
- `[!]` - Failed (needs re-extraction)

## Quick Verification Script

Use this one-liner to check a batch before committing:

```bash
BATCH=01
for W in $(seq $(((BATCH - 1) * 3 + 1)) $((BATCH * 3))); do
	F=$(printf "ste-code/extracted/w%03d-p*.md" $W)
	if [ -f $F ]; then
		echo "OK $W: $(wc -c < $F) bytes, $(wc -l < $F) lines"
	else
		echo "MISSING $W"
	fi
done
```

Replace `BATCH=01` with the current batch number. This script checks file
existence, byte count, and line count for all 3 workers in the batch.

## Troubleshooting

| Symptom                                         | Probable Cause                           | Action                                                                     |
| ----------------------------------------------- | ---------------------------------------- | -------------------------------------------------------------------------- |
| All 3 workers produce empty files               | Prompt file missing or wrong path        | Check `prompt.txt` exists. Verify the page file paths.                     |
| Worker output is a conversation, not extraction | Prompt too weak or missing `--yolo`      | Add `--yolo` flag. Strengthen prompt with "Output ONLY the markdown file." |
| Output has wrong formatting (no headings)       | Worker misunderstood the task            | Add format example to the worker prompt.                                   |
| Batch takes >120 seconds                        | Dense dictionary pages or API congestion | Wait. Do not kill. DICT pages (129-360) are the densest.                   |
| Consecutive batches fail with same error        | Systematic issue with prompt or model    | Stop. Debug the prompt. Do not burn through all 37 batches.                |
| File size is correct but content is duplicated  | Worker read pages twice                  | Re-extract. Add "Read each page ONCE" to the prompt.                       |

## Worker Grid: `.agents/references/worker-grid.md`

## Section types: `.agents/references/section-types.md`

## Process Rails: `.agents/references/rails.md`
