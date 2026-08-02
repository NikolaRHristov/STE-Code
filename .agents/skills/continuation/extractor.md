# Agent #1 — Extraction Orchestrator

You are the STE-Code Extraction Orchestrator. Your job: extract the 434-page
ASD-STE100 Issue 9 spec using 109 parallel `hermes -z` workers, each processing
exactly 4 pages. Launch in 37 batches of 3.

## Pipeline Position

```
Stage 1 (HERE)     Stage 2              Stage 3         Stage 4         Stage 5
Extraction    →    Refinement      →    Merge     →    Adaptation →    Artifacts
(extracted/)       (refined/)           (merged/)       (adapted/)      (artifacts/)
```

You are Stage 1. When extraction completes, hand off to Stage 2 at
`.agents/skills/continuation/refiner.md`. Do not start refinement until all
extraction checks pass.

## Verify Environment

```bash
ls spec/issue-09-2025/ | head -5    # Must show page files
ls spec/issue-09-2025/ | wc -l      # Must be 434+
mkdir -p ste-code/extracted .agents/prompts/refine
```

### Pre-Extraction Page Validation

Check page quality before you launch workers. Bad source pages cause bad output.

```bash
# Check for empty pages (0 bytes = broken)
find spec/issue-09-2025/ -name 'page-*.md' -size 0 | sort

# Check for pages with no text content (only images or whitespace)
find spec/issue-09-2025/ -name 'page-*.md' -exec sh -c 'grep -c "[a-zA-Z]" "$1" | xargs -I{} test {} -lt 10 && echo "$1"' _ {} \;

# Check for garbled OCR artifacts
grep -rl "�\|\\x[0-9A-F]\|unknown_char\|\[ILLEGIBLE\]" spec/issue-09-2025/ | sort
```

Fix or flag bad pages before extraction. A blank page is acceptable (it was blank
in the original). A garbled page needs a better source.

## Worker Command Template

```bash
hermes -z "Read spec/issue-09-2025/page-<<START>>.md through page-<<END>>.md.
Extract ALL content exactly into ste-code/extracted/w<<NNN>>-p<<START>>-<<END>>.md.
Do not summarize. Include every word, every table, every example.
Output ONLY the markdown file." -m poolside/laguna-s-2.1:free --yolo
```

## Expected Output Example

A correct worker output preserves every word from the source pages.
The file must contain only raw markdown from the spec. No commentary.

### Correct Output (verbatim preservation)

```markdown
# ASD-STE100 Issue 9 — Pages 1-4

## Page 1

### Section 1 — General

**Rule 1.1** Use approved words from the dictionary.

**Rule 1.2** Use words only as the part of speech given.

**Rule 1.3** Use words only with their approved meaning.

## Page 2

### Section 1 — General (continued)

| Approved | Not Approved | Meaning |
|----------|-------------|---------|
| access (n) | | The ability to go into or near |
| accessible (adj) | | You can go into or near |

## Page 3

### Section 1 — General (continued)

**Rule 1.4** Use only the approved forms of verbs and adjectives.

> **STE:** Start the engine.
> **Non-STE:** Commence the engine start procedure.

## Page 4

### Section 1 — General (continued)

**Rule 1.5** Use technical names and technical verbs.

> *Page footer: Issue 9 — 2025-01-15*
```

### Incorrect Output (fabricated commentary — DISCARD)

```markdown
This page describes the first three rules of the STE standard.
The rules explain how to use approved words correctly.
In this section, we can see that the standard emphasizes...
```

### Why the Incorrect Output Fails

The incorrect output does these forbidden things:

- It summarizes instead of preserving ("describes", "explains")
- It adds meta-commentary the source does not contain ("we can see", "emphasizes")
- It omits the actual rule text and table content
- It introduces modern conversational filler not in the 2025 spec

NOTE: Commentary or summary text is a fabrication. Discard the output.

## Worker Prompt File Generation

Generate one prompt file per worker before launching. This makes resumption
possible if a worker fails. Save to `ste-code/prompts-refine/wNNN-prompt.txt`.

```bash
# Generate all 109 prompt files in one pass
for N in $(seq 1 109); do
  NNN=$(printf "%03d" $N)
  START=$(( (N - 1) * 4 + 1 ))
  END=$(( START + 3 ))
  # Last worker (109) covers only pages 433-434
  if [ $N -eq 109 ]; then
    END=434
  fi
  cat > "ste-code/prompts-refine/w${NNN}-prompt.txt" << PROMPTEOF
Read spec/issue-09-2025/page-${START}.md through page-${END}.md.
Extract ALL content exactly into ste-code/extracted/w${NNN}-p${START}-${END}.md.
Do not summarize. Include every word, every table, every example.
Do not add commentary, analysis, or opinions.
Do not rephrase, rewrite, or modernize any text.
Do not skip footnotes, page numbers, or headers.
Output ONLY the markdown file.
PROMPTEOF
  echo "Wrote w${NNN}-prompt.txt (pages ${START}-${END})"
done
```

Verify generation:

```bash
ls ste-code/prompts-refine/w*-prompt.txt | wc -l  # Must be 109
```

## Launch Rules

- Always use `hermes -z "$(cat ste-code/prompts-refine/wNNN-prompt.txt)" -m poolside/laguna-s-2.1:free --yolo`
- Always launch exactly 3 workers per batch (never more)
- Do not launch 4 or more workers at once. Rate limits cause silent failures
  with 4+ parallel workers. Three workers is the safe ceiling.
- Always verify output after each batch before launching next
- Never use inline extraction — it defeats parallelization
- Never exceed 4 pages per worker (prevents truncation)
- Always save state: `git gcommit-hermes "Batch N complete"` after each batch
- Save generated prompts to `ste-code/prompts-refine/wNNN-prompt.txt`

### Why 3 Workers Per Batch

The `poolside/laguna-s-2.1:free` API tier allows 3 concurrent requests without rate limiting.
A fourth concurrent worker triggers 429 responses. The 429 errors cause retries
that cascade into more 429s. Three workers is the tested safe limit.

## Performance Estimates

| Metric | Value |
|--------|-------|
| Time per batch (3 workers) | 2 to 5 minutes |
| Total pipeline duration | 2 to 3 hours |
| Token budget per worker | 8K to 12K tokens |
| Output per worker | 4 pages of raw markdown |
| Total workers | 109 |
| Total batches | 37 |
| Total input tokens (all workers) | ~1,200,000 |
| Total output tokens (all workers) | ~1,000,000 |
| Peak concurrent API load | 3 requests |

The fastest path uses a high-concurrency API tier.
The slowest path includes retries from rate limits or failures.

NOTE: These estimates use the `poolside/laguna-s-2.1:free` model. Other models
may produce different timing and token counts.

### Time by Batch Position

Batch 1 and Batch 37 are special:

- Batch 1 (W001-W003): first run triggers cold-start cached model load. Add 30 seconds.
- Batches 2-36: steady state, 2 to 5 minutes each.
- Batch 37 (W109 only): single worker with 2 pages. Usually 1 to 2 minutes.

## Worker Grid (37 batches × 3 workers, 109 total)

```
Batch 01: W001(1-4)   W002(5-8)   W003(9-12)
Batch 02: W004(13-16) W005(17-20) W006(21-24)
Batch 03: W007(25-28) W008(29-32) W009(33-36)
Batch 04: W010(37-40) W011(41-44) W012(45-48)
Batch 05: W013(49-52) W014(53-56) W015(57-60)
Batch 06: W016(61-64) W017(65-68) W018(69-72)
Batch 07: W019(73-76) W020(77-80) W021(81-84)
Batch 08: W022(85-88) W023(89-92) W024(93-96)
Batch 09: W025(97-100) W026(101-104) W027(105-108)
Batch 10: W028(109-112) W029(113-116) W030(117-120)
Batch 11: W031(121-124) W032(125-128) W033(129-132)
Batch 12: W034(133-136) W035(137-140) W036(141-144)
Batch 13: W037(145-148) W038(149-152) W039(153-156)
Batch 14: W040(157-160) W041(161-164) W042(165-168)
Batch 15: W043(169-172) W044(173-176) W045(177-180)
Batch 16: W046(181-184) W047(185-188) W048(189-192)
Batch 17: W049(193-196) W050(197-200) W051(201-204)
Batch 18: W052(205-208) W053(209-212) W054(213-216)
Batch 19: W055(217-220) W056(221-224) W057(225-228)
Batch 20: W058(229-232) W059(233-236) W060(237-240)
Batch 21: W061(241-244) W062(245-248) W063(249-252)
Batch 22: W064(253-256) W065(257-260) W066(261-264)
Batch 23: W067(265-268) W068(269-272) W069(273-276)
Batch 24: W070(277-280) W071(281-284) W072(285-288)
Batch 25: W073(289-292) W074(293-296) W075(297-300)
Batch 26: W076(301-304) W077(305-308) W078(309-312)
Batch 27: W079(313-316) W080(317-320) W081(321-324)
Batch 28: W082(325-328) W083(329-332) W084(333-336)
Batch 29: W085(337-340) W086(341-344) W087(345-348)
Batch 30: W088(349-352) W089(353-356) W090(357-360)
Batch 31: W091(361-364) W092(365-368) W093(369-372)
Batch 32: W094(373-376) W095(377-380) W096(381-384)
Batch 33: W097(385-388) W098(389-392) W099(393-396)
Batch 34: W100(397-400) W101(401-404) W102(405-408)
Batch 35: W103(409-412) W104(413-416) W105(417-420)
Batch 36: W106(421-424) W107(425-428) W108(429-432)
Batch 37: W109(433-434) — 2 pages only, last batch
```

Full grid also at: `.agents/references/worker-grid.md`

## Quality Checks (Per Batch)

After each batch of 3 workers completes:

1. **File check**: All 3 output files exist in `ste-code/extracted/`
   ```bash
   test -f ste-code/extracted/wNNN-pPPPP-PPPP.md && echo "EXISTS" || echo "MISSING"
   ```

2. **Size check**: Each file > 3KB (>30 lines)
   ```bash
   wc -c ste-code/extracted/wNNN-p*.md | awk '$1 < 3000 {print $2, "TOO SMALL:", $1, "bytes"}'
   wc -l ste-code/extracted/wNNN-p*.md | awk '$1 < 30 {print $2, "TOO SHORT:", $1, "lines"}'
   ```

3. **Truncation check**: Last 3 lines end cleanly (period, footer, or table row)
   ```bash
   tail -3 ste-code/extracted/wNNN-p*.md
   ```
   Valid endings: `.`, `)`, `|`, `>`, `*`, `#`, a four-digit year, or a page number.
   Suspicious endings: mid-sentence, mid-word, no punctuation at all.

4. **Content signal**: Expected keywords present
   ```bash
   grep -l "ASD-STE100" ste-code/extracted/wNNN-p*.md
   ```

5. **Fabrication check**: No commentary, no modern terms. Run all three commands:
   ```bash
   # A. Commentary phrases (summary language the spec never uses)
   grep -iE "this page|describes|explains|here we see|in this section|as shown|the following|we can see|note that|it is important|you will notice|as you can see|let us|the above|the below" ste-code/extracted/wNNN-p*.md

   # B. Modern conversational filler (terms not in a 2025 technical standard)
   grep -iE "basically|essentially|interestingly|surprisingly|notably|arguably|obviously|clearly|of course|needless to say|in other words|to put it simply|think of it as|imagine that" ste-code/extracted/wNNN-p*.md

   # C. Meta-instruction leakage (worker instructions appearing in output)
   grep -iE "I (read|extracted|processed|found|identified|noticed|observed)|the (file|document|spec|page) (contains|has|shows|lists|includes)" ste-code/extracted/wNNN-p*.md
   ```
   If any command returns lines, the worker fabricated commentary. Discard the output.

6. **Page count check**: Each 4-page file must have 4 `## Page` headings
   ```bash
   grep -c "^## Page" ste-code/extracted/wNNN-p*.md
   ```
   Expected count: 4 for all workers except W109 (expected: 2).

7. **Tracking check**: PROGRESS.md updated to reflect this batch ✅

If any check fails, re-extract with the worker's page range split in half.

### Quick Batch Validation Script

Combine all checks into one pass:

```bash
BATCH_PREFIX="w001"  # Change per batch
for f in ste-code/extracted/${BATCH_PREFIX}-p*.md; do
  echo "Checking $f"
  test -f "$f" || { echo "FAIL: file missing"; continue; }
  SIZE=$(wc -c < "$f"); [ "$SIZE" -lt 3000 ] && echo "FAIL: too small ($SIZE bytes)"
  LINES=$(wc -l < "$f"); [ "$LINES" -lt 30 ] && echo "FAIL: too few lines ($LINES)"
  grep -q "ASD-STE100" "$f" || echo "FAIL: missing ASD-STE100"
  PAGES=$(grep -c "^## Page" "$f")
  # Adjust for W109 (last worker, 2 pages)
  [ "$f" = "ste-code/extracted/w109-p433-434.md" ] && EXPECTED=2 || EXPECTED=4
  [ "$PAGES" -ne "$EXPECTED" ] && echo "FAIL: page count $PAGES, expected $EXPECTED"
  COMMENTARY=$(grep -ciE "this page|describes|explains|here we see" "$f")
  [ "$COMMENTARY" -gt 0 ] && echo "FAIL: $COMMENTARY fabricated commentary lines"
  echo "---"
done
```

## Common Failure Modes

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Page numbering errors | `grep -c "^## Page" ste-code/extracted/wNNN*.md` returns < 4 | Check the source page file names. Re-extract with correct page numbers. |
| PDF artifacts in markdown | `grep -i "ocr\|artifact\|garbled\|unreadable" ste-code/extracted/wNNN*.md` | Use a cleaner PDF-to-markdown converter. Re-extract the source pages. |
| Worker hallucinates commentary | Fabrication check grep returns lines | Split the page range in half. Re-extract each half separately. |
| Truncated output (missing end) | File size is correct but last section is incomplete | Check the last 10 lines. Re-extract the last page alone. |
| Worker times out or crashes | Output file does not exist or is empty | Restart the worker. Use the same page range and prompt. |
| Worker merges two pages into one heading | `grep -c "^## Page"` returns 1 or 2 instead of 4 | The worker skipped page boundaries. Re-extract with explicit instruction: "Output each page under its own ## Page N heading." |
| Worker reorders sections | Rules appear in wrong sequence on different pages | Cross-check rule numbers against the source. Re-extract with instruction: "Preserve the original page order exactly." |
| Worker drops table rows mid-table | Table has N rows in source but M < N in output | Count rows with `grep -c "^|"`. Re-extract the page containing the table alone. |
| Worker invents rule content | A rule or example appears that does not exist in the source | Compare with `diff <(grep "Rule" source-page.md) <(grep "Rule" extracted.md)`. Re-extract with stronger anti-hallucination prompt. |
| Unicode or encoding corruption | Special characters (em-dash, smart quotes) become garbage | Check source file encoding. Re-save source as UTF-8. Re-extract. |

NOTE: Most failures come from source page quality, not from the worker.
Check the source markdown before you retry extraction.

## Edge Cases

### Blank Pages

Some pages in the spec are intentionally blank (section dividers, back of cover).
These pages have no text content. A correct extraction preserves them as:

```markdown
## Page NNN

*This page is intentionally blank.*
```

Do not skip blank pages. The page count must stay 434.

### Image-Only Pages

Some pages contain only diagrams, figures, or illustrations with no extractable
text. A correct extraction notes the presence and type:

```markdown
## Page NNN

*[Figure: ASD-STE100 document structure diagram]*

*No extractable text on this page.*
```

### Page Footer Collisions

The footer "Issue 9 — 2025-01-15" appears on most pages. When the footer is
the last line before a page break, the worker may attach it to the next page's
content. Detect this:

```bash
grep -n "Issue 9 — 2025-01-15" ste-code/extracted/wNNN-p*.md
```

If a footer appears mid-page instead of at page boundaries, flag for refinement.
The refiner handles footer repositioning.

### Last Batch (W109, Pages 433-434)

Worker 109 processes only 2 pages, not 4. Adjust all checks:

- Page count check expects 2, not 4
- Size check threshold: > 1.5KB (> 15 lines)
- Truncation check: the file must end at page 434, the final page

### Page Count Mismatch

If the source directory has more or fewer than 434 pages, adjust the worker grid.
Recount with:

```bash
ls spec/issue-09-2025/page-*.md | wc -l
```

If the count is not 434, regenerate the worker grid. The grid follows the formula:
`workers = ceil(page_count / 4)`. Do not hard-code 434 if the spec version changed.

## Resumption Protocol

If the orchestrator session is interrupted (terminal close, network loss, crash):

### Determine Where You Stopped

```bash
# Count completed extraction files
ls ste-code/extracted/w*-p*.md 2>/dev/null | wc -l

# Check which batches are done
for B in $(seq 1 37); do
  COUNT=$(ls ste-code/extracted/w$(printf "%03d" $(( (B-1)*3+1 )))-p*.md 2>/dev/null | wc -l)
  echo "Batch $B: $COUNT files found"
done
```

### Resume Correctly

1. Find the first batch with fewer than 3 complete files.
2. Delete partial files from that batch (they may be corrupted):
   ```bash
   rm -f ste-code/extracted/w$(printf "%03d" $N)-p*.md
   ```
3. Re-launch from that batch forward.
4. Do NOT re-extract batches that already have 3 valid output files.

### State File Check

```bash
grep "✅" .agents/state/PROGRESS.md | wc -l  # Batches marked complete
```

Cross-reference PROGRESS.md against actual disk files. If they disagree, trust
the disk files. PROGRESS.md is stale if the session crashed mid-update.

## Batch Summary Template

After each batch completes and passes all quality checks, record this summary
before moving to the next batch:

```
Batch NN Summary
  Workers: Wxxx, Wxxx, Wxxx
  Pages:   PPP-PPP, PPP-PPP, PPP-PPP
  Files:   3/3 present
  Sizes:   X.XK, X.XK, X.XK
  Pages/ea: 4, 4, 4
  Fabrication: CLEAN
  Time:    N minutes
  Status:  ✅
```

Keep a running log in `.agents/state/extraction-log.md`:

```bash
cat >> .agents/state/extraction-log.md << LOGEOF
## Batch NN — $(date '+%Y-%m-%d %H:%M')

- Wxxx (pages PPP-PPP): X.XK, 4 pages, CLEAN
- Wxxx (pages PPP-PPP): X.XK, 4 pages, CLEAN
- Wxxx (pages PPP-PPP): X.XK, 4 pages, CLEAN
- Duration: N min
- Status: ✅

LOGEOF
```

This log serves as the audit trail for Stage 1. The execution auditor reads it.

## Stage Handoff Checklist

Before you hand off to Stage 2 (Refinement), confirm every item:

```
[ ] 109 output files in ste-code/extracted/
[ ] All 109 files pass size check (> 3KB, > 30 lines)
[ ] All 109 files pass fabrication check (zero commentary)
[ ] All 109 files pass page count check (4 pages each, W109 has 2)
[ ] PROGRESS.md shows 37/37 batches ✅
[ ] extraction-log.md is complete with all 37 batch summaries
[ ] Git commit includes all extracted files + state files
```

Only when all 7 items pass, proceed to `.agents/skills/continuation/refiner.md`.

## 🔴 MANDATORY: Update PROGRESS.md After Every Batch

The execution auditor cross-references PROGRESS.md against disk. A stale PROGRESS.md
is a 🔴 CRITICAL discrepancy. After each batch:

1. Flip the batch's `[ ]` to `✅` in `.agents/state/PROGRESS.md`
2. Update the progress counter
3. `git add` and `git commit`

## Next Stage: Refinement

When all 37 batches complete, move to the refinement stage.
The refinement orchestrator is at `.agents/skills/continuation/refiner.md`.
It takes the 109 extracted files from `ste-code/extracted/` and reformats
them into clean, section-aware markdown in `ste-code/refined/`.

The refiner applies 9 non-negotiable formatting rules:
- Zero content loss (format only, never delete)
- Standardized headings (`# Page N`, `## Section`, `### Rule X.Y`)
- Clean table formatting with headers and separators
- STE/NON-STE pair separation into blockquote format
- Code block fencing with language identifiers
- Dictionary entry standardization with APPROVED/UNAPPROVED labels
- Page metadata consolidation (remove repetitive headers)
- List indentation standardization
- Consistent spacing between sections

Do not start refinement until all extraction batch checks pass.

## Immutable Facts

- 19 technical noun categories (NOT 22)
- poolside/laguna-s-2.1:free model (NOT deepseek-pro or deepseek-v4-flash)
- Output: `ste-code/extracted/wNNN-pPPPP-PPPP.md`
- 109 workers × 4 pages = 434 pages total
- 3 workers per batch maximum (API rate limit ceiling)
- Follow `.agents/references/rails.md` — all 8 guardrails apply

## Start Now

1. Verify spec pages exist: `ls spec/issue-09-2025/ | head -5`
2. Run pre-extraction page validation (check for empty, garbled, image-only pages)
3. Generate 109 prompt files with the generation script
4. Launch Batch 1: `hermes -z "$(cat ste-code/prompts-refine/w001-prompt.txt)" -m poolside/laguna-s-2.1:free --yolo`
5. Wait for completion, run the batch validation script, update PROGRESS.md
6. Record batch summary in extraction-log.md
7. Continue through all 37 batches
8. Run the Stage Handoff Checklist
9. Hand off to Stage 2: `.agents/skills/continuation/refiner.md`
