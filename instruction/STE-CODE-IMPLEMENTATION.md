# STE-Code: Simplified Technical English for Code — Implementation Protocol v3

> **v3 CORRECTIONS (READ FIRST — supersedes v2 lessons 1-2)**
>
> 1. `hermes -z` DOES support file I/O (read_file, write_file) when launched with
>    simple single-line prompts via `$(cat prompt.txt)`. Verified: W0 test wrote
>    to file successfully. W1-W5 produced 151KB of real extraction using `hermes -z`.
>    DO use `hermes -z` for extraction workers — it is the correct approach.
>
> 2. DO NOT use inline extraction. The coordinator launches workers; workers
>    do the extraction. Coordinator oversees, polls, verifies, merges.
>    Inline extraction bloats the coordinator's context and defeats parallelization.
>
> 3. MAX 4 PAGES PER WORKER. Each `hermes -z` worker reads exactly 4 spec pages.
>    This leaves >90% of the 1M context window free for the prompt + extraction,
>    ensuring zero truncation and perfect fidelity. 434 pages ÷ 4 = 109 workers.
>
> 4. Workers launch in batches of 3 (never more). 109 ÷ 3 = 37 batches.
>    Each batch: launch 3 workers → wait for all 3 → git gcommit-hermes → next batch.
>
> 5. Every worker uses: `hermes -z "$(cat prompt.txt)" -m deepseek-pro --yolo`
>    Simple single-line prompt, no embedded quotes, no multi-line in shell.
>
> 6. Output format: `.md` files (user directive: "not JSON structured data").
>    Files named: `ste-code/workers/wNNN-pPPPP-PPPP.md`
>
> 7. Feedback exchange: Orchestrator ↔ Reviewer communicate via
>    `./.hermes/feedback/exchange.md` — markdown turns.
>
> 8. Skills saved to `./.hermes/skills/spec-extraction/` for reuse across sessions.
>
> 9. DO NOT write artifact files until ALL 109 workers complete and pass GATE 1.

---

## v2 HISTORY (preserved for reference — lessons 3-4 still apply)

> **v2 LESSONS (still valid):**
>
> 3. DO NOT CLAIM completion when pages are unread. Track exactly which
>    pages have been processed using PROGRESS.md checkboxes.
> 4. DO NOT write artifact files until ALL extraction is complete and verified.
>    Previous attempt fabricated 6 files from general knowledge instead of spec data.

---

## GATE 0: Environment Verification

Verify these paths exist:
```bash
ls spec/issue-09-2025/page-0001.md
ls spec/issue-09-2025/page-0434.md
```

Create directories:
```bash
mkdir -p ste-code/workers
```

Create PROGRESS.md tracker:
```bash
cat > ste-code/PROGRESS.md << 'EOF'
# STE-Code Progress Tracker

## Extraction (434 pages total)
- [ ] W1: pages 1-30 — Front matter, highlights, TOC, subject-to-rule index, general introduction, Section 1 rules (1.1-1.14)
- [ ] W2: pages 31-60 — Sections 2-3 rules (2.1-2.3, 3.1-3.7), technical noun categories start
- [ ] W3: pages 61-90 — Sections 4-5 rules (4.1-4.4, 5.1-5.5), technical noun categories continue
- [ ] W4: pages 91-120 — Sections 6-7 rules (6.1-6.6, 7.1-7.3), technical noun categories complete
- [ ] W5: pages 121-180 — Sections 8-9 rules (8.1-8.7, 9.1-9.4, GR1-GR8), polysemy resolution table
- [ ] W6: pages 181-240 — Dictionary A-F, canonical synonym table, introduction to Part 2
- [ ] W7: pages 241-300 — Dictionary G-P
- [ ] W8: pages 301-360 — Dictionary Q-Z
- [ ] W9: pages 361-434 — Appendices, index, change history, decision flowchart

## Merge
- [ ] All 9 files verified for content (not empty, not fabricated)
- [ ] Master state assembled from all 9 files
- [ ] 10 random pages spot-checked against master state

## Adaptation
- [ ] Section 1 rules adapted (1.1-1.14)
- [ ] Section 2 rules adapted (2.1-2.3)
- [ ] Section 3 rules adapted (3.1-3.7)
- [ ] Section 4 rules adapted (4.1-4.4)
- [ ] Section 5 rules adapted (5.1-5.5)
- [ ] Section 6 rules adapted (6.1-6.6)
- [ ] Section 7 rules adapted (7.1-7.3)
- [ ] Section 8 rules adapted (8.1-8.7)
- [ ] Section 9 rules adapted (9.1-9.4, GR1-GR4)
- [ ] 19 Technical Code Noun categories remapped
- [ ] Canonical synonym table adapted
- [ ] Polysemy resolution table adapted
- [ ] 6-pass transformation pipeline adapted

## Artifacts (WRITE ONLY AFTER ALL ABOVE ARE [x])
- [ ] ste-code-distilled-system-prompt.txt
- [ ] ste-code-self-reading-manual.txt
- [ ] ste-code-extraction-methodology.txt
- [ ] ste-code-example-turn.txt
- [ ] ste-code-deployment-guide.txt
- [ ] README.md
EOF
```

---

## INLINE BATCH EXTRACTION PROTOCOL

Extract by reading pages yourself and writing output files. Process in batches.
After each batch, update PROGRESS.md.

### Format for each worker output file

```
# ASD-STE100 Issue 9 — <Section Description>

## Source: pages <START>-<END>

[EXACT spec text from the pages, preserving:
- ALL rule numbers and rule text
- ALL STE examples and non-STE example pairs
- ALL dictionary entries with word, POS, meaning, forms, alternatives
- ALL category names, numbers, descriptions, and examples
- ALL synonym mappings and polysemy resolutions
- ALL pipeline step descriptions]
```

### Batch Execution

Process 2-3 worker files per response. For each:
1. Read the spec pages using read_file
2. Extract all content faithfully
3. Write to ste-code/workers/w<N>-<description>.md
4. Update PROGRESS.md: change [ ] to [x]

### Quality Rules
- Every rule must have at least one STE/non-STE example pair
- Every dictionary entry must have word, POS, approved/unapproved status, meaning, forms
- No summarization — extract EXACT text
- If a page range has no content matching a category, note "None found in this range"
- Verify each file exists AND has content before marking complete

---

## GATE 1: Verify Extraction Completeness

After all 9 files are written, run:
```bash
for f in ste-code/workers/w[1-9]-*.md; do
  lines=$(wc -l < "$f")
  size=$(wc -c < "$f")
  if [ "$lines" -lt 20 ]; then
    echo "SUSPICIOUS: $f has only $lines lines — may be incomplete"
  else
    echo "OK: $f — $lines lines, $size bytes"
  fi
done
```

Minimum expected:
- W1-W5: 500+ lines each (rule sections with examples)
- W6-W8: 1000+ lines each (dictionary entries)
- W9: 200+ lines

If any file is below minimum, re-extract that page range.

---

## GATE 2: Merge into Master State

Read all 9 worker files. Create a consolidated master state document at `ste-code/workers/master.md` containing:
- Complete rule listing (all 53 rules numbered, with text and examples)
- Complete 19 categories enumerated
- Complete synonym table
- Complete polysemy table
- Complete pipeline description

---

## GATE 3: Adaptation

For each rule in master.md, produce an STE-Code adaptation following the PRESERVE/REPLACE rules below.

### PRESERVE (unchanged)
- Rule numbers (1.1, 1.2, ..., 9.4, GR1-GR4)
- Section organization (9 sections)
- Rule structure (imperative statement + explanatory text + examples)
- 6-pass pipeline architecture
- Dictionary architecture (APPROVED/UNAPPROVED)

### REPLACE (adapted for code)
- Every STE/non-STE example → code documentation examples
- 19 categories → code domain (see mapping below)
- Approved vocabulary → code-domain approved words
- Safety WARNING/CAUTION → BREAKING/DEPRECATED/NOTE

### Category Remapping

| # | Original | STE-Code |
|---|----------|----------|
| 1 | Parts information | Language keywords and reserved words |
| 2 | Vehicles/machines | Frameworks, runtimes, and platforms |
| 3 | Tools and support equipment | Development tools and build systems |
| 4 | Materials and consumables | Dependencies, packages, and libraries |
| 5 | Facilities and locations | Deployment targets and environments |
| 6 | Systems and components | Modules, classes, components, services |
| 7 | Mathematical/scientific terms | Algorithmic and computational terms |
| 8 | Navigation and geographic terms | Routing, pathing, and state management |
| 9 | Numbers, units, and time | Data sizes, time units, numeric formats |
| 10 | Quoted text | String literals, error messages, log output |
| 11 | Persons, groups, organizations | Roles, teams, services, and actors |
| 12 | Parts of the body | UI/UX interaction and accessibility terms |
| 13 | Common personal effects | Configuration and preference terms |
| 14 | Medical terms | Error states, diagnostics, and health checks |
| 15 | Official documents | Spec files, configs, manifests, schemas |
| 16 | Environmental conditions | Runtime conditions, states, and flags |
| 17 | Colors | Terminal colors, syntax highlighting themes |
| 18 | Damage terms | Bug, defect, failure, and degradation taxonomy |
| 19 | IT and telephony terms | Network, protocol, API, and I/O terms |

---

## GATE 4: Write Artifact Files

**ONLY after ALL adaptation checkboxes in PROGRESS.md are [x].**

### File 1: ste-code-distilled-system-prompt.txt (~1,200 tokens)
System prompt constraining any LLM to STE-Code output.

### File 2: ste-code-self-reading-manual.txt (~7,000 tokens)
8-section self-reading manual (S0-S8) following SSRM structure.

### File 3: ste-code-extraction-methodology.txt (~1,400 tokens)
Turn-by-turn protocol for code documents.

### File 4: ste-code-example-turn.txt (~500 tokens)
Worked example: non-STE code comment → STE-Code.

### File 5: ste-code-deployment-guide.txt
Deployment for Ollama, LM Studio, Python.

### File 6: README.md
Project overview.

---

## FINAL VERIFICATION

```bash
for f in ste-code/ste-code-*.txt; do
  chars=$(wc -c < "$f")
  echo "$(basename $f): $chars chars ~$((chars/4)) tokens"
done
```

All files must reference specific data from `ste-code/workers/master.md`.
No file should contain generic/fabricated content.

---

## Flow Summary

```
GATE 0: Verify paths, create dirs, init PROGRESS.md
  ↓
INLINE: Extract W1-W9 in batches, update PROGRESS.md after each
  ↓
GATE 1: Verify all 9 files have sufficient content
  ↓
GATE 2: Merge into master.md
  ↓
GATE 3: Adapt all 53 rules, 19 categories, synonyms, polysemy, pipeline
  ↓
GATE 4: Write 6 artifact files from adapted data
  ↓
FINAL: Verify artifact quality
```

---

## EXISTING WORK: What W1-W5 Already Contain

The previous extraction run successfully produced 5 worker files with
**3,864 lines of genuine spec text**. These files are already complete
and correct — do NOT re-extract them unless spot-checks find errors.

| File | Lines | Content Verified |
|------|-------|------------------|
| `workers/w1-sec1-rules.md` | 751 | Copyright, highlights, TOC, subject-to-rule index, general introduction, Section 1 rules (1.1-1.6) with ALL STE/non-STE example pairs |
| `workers/w2-sec2-3-rules.md` | 1,041 | Rules 1.7-1.14, all technical noun/verb rules, Sections 2-3 rules with ALL example pairs |
| `workers/w3-sec3-5-rules.md` | 901 | Sections 3 (continued), 4, and 5 rules with ALL example pairs |
| `workers/w4-sec6-8-rules.md` | 622 | Sections 6, 7, and 8 rules with ALL example pairs, safety instruction formats |
| `workers/w5-sec9-gr-rules.md` | 549 | Section 9 rules (9.1-9.4), GR1-GR8, polysemy resolution, transformation examples |

**Quality check**: W5 contains exact spec text for Rule 9.1 matching the original.
W1 contains the complete general introduction with history, purpose, and reference
documents. These files demonstrate the expected quality level for W6-W9.

---

## REMAINING WORK: What W6-W9 Must Extract

Prompt templates for W6-W9 exist at `workers/w6-prompt.txt` through
`workers/w9-prompt.txt`. These contain page ranges and extraction instructions.
Use them as your guide. The remaining pages to extract:

| Worker | Pages | What to Extract | Expected Size |
|--------|-------|-----------------|---------------|
| W6 | 181-240 | Dictionary entries A-F (approx 250 entries), Part 2 introduction, canonical synonym table, list of approved verbs, recurring errors list | 1,000+ lines |
| W7 | 241-300 | Dictionary entries G-P (approx 250 entries), transformation examples | 1,000+ lines |
| W8 | 301-360 | Dictionary entries Q-Z (approx 250 entries), remaining examples | 1,000+ lines |
| W9 | 361-434 | Decision flowchart, change history (Issues 1-9), full 19-category enumeration, index, change form, reference documents list | 200+ lines |

Dictionary entry format in the spec pages (example from page 201):
```
| **CONTAIN (v)** | , To have in something or EACH SURVIVAL KIT CONTAINS, hold in 
                    something CONTAINS THESE CONTAINED, ITEMS: CONTAINED |
```
Each entry contains: WORD, POS, approved meaning, inflected forms, STE example,
non-STE example — interleaved due to the 4-column PDF layout. Extract ALL of this
text exactly as it appears. The interleaving is a known artifact of PDF extraction
and should be PRESERVED (it will be cleaned up in the adaptation phase).

---

## EXISTING ARTIFACT FILES: Why They Need Regeneration

The previous run produced 6 artifact files (`ste-code-distilled-system-prompt.txt`,
`ste-code-self-reading-manual.txt`, etc.) BEFORE extraction was complete. These
files contain generic/fabricated content, not spec-grounded adaptations. Key problems:

1. The synonym table uses invented mappings (e.g., "do/perform → execute, run") —
   not derived from the actual STE canonical synonym table in the spec.
2. Claims "19 categories (adapted from STE's 22)" — STE has 19 categories, not 22.
3. The 14 principles are generic summaries, not the actual P1-P14 with rule cross-references.
4. No evidence that any of the 53 original rules were individually adapted.

**These files must be regenerated from scratch** after all 9 worker files are
complete and merged into master.md. Do NOT attempt to fix or patch them —
replace them entirely with spec-grounded content.

---

## ANTI-PATTERNS: Concrete Examples of What to Avoid

Based on the previous attempt, these specific behaviors produced bad output:

**DON'T**: Write artifact files before extraction is complete.
- Example: Previous run wrote 6 artifacts when only 5 of 9 workers had output
  and 288 dictionary pages (136-424) were never read.

**DON'T**: Fabricate data when extraction is incomplete.
- Example: Previous synonym table invented "do/perform → execute" instead of
  extracting the actual STE synonyms (START, STOP, REMOVE, MAKE SURE, etc.)

**DON'T**: Make factual claims you cannot verify from extracted data.
- Example: "19 categories (adapted from STE's 22)" — no worker file contains
  the number 22. The correct number is 19.

**DON'T**: Mark phases as complete when gates are not satisfied.
- Example: PLAN.md says "Phase 1: ✅ Absorbed spec via direct page reading
  (pages 1-135, 425-434)" — this admits 288 pages were never read.

**DO**: Run the GATE verification commands. If they fail, STOP and fix.
**DO**: Compare every adapted output against a specific worker file entry.
**DO**: Track exact pages read in PROGRESS.md before claiming any phase complete.

---

## WORKER OUTPUT FORMAT: Matching the Existing Quality

W1-W5 already established a consistent format. Match it for W6-W9:

```
# ASD-STE100 Issue 9 — <Section Description>

## Source: pages <START>-<END> (<COUNT> pages read)

[Content organized with ## and ### headings, preserving EXACT spec text]

For dictionary pages, use this table format:
| Word (POS) | Meaning & Examples |
|------------|-------------------|
| **WORD (POS)** | EXACT meaning text from spec, including interleaved STE/non-STE examples |
```

Look at `workers/w1-sec1-rules.md` and `workers/w5-sec9-gr-rules.md` for examples
of the formatting standard to follow. W5 in particular demonstrates how to format
rule text with blockquoted STE/non-STE example pairs.
