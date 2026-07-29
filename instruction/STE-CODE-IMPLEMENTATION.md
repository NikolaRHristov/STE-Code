# STE-Code: Simplified Technical English for Code — Implementation Protocol v2

> **LESSONS FROM PREVIOUS ATTEMPT (READ FIRST)**
>
> 1. `hermes -z` oneshot mode DOES NOT support file I/O tools (read_file, write_file).
>    Workers launched this way cannot read spec pages or write output files.
>    DO NOT use `hermes -z` for extraction workers.
>
> 2. Instead, use INLINE BATCH EXTRACTION: read pages yourself and write
>    output files directly, batch by batch. This is the proven approach.
>
> 3. DO NOT CLAIM completion when pages are unread. Track exactly which
>    pages have been processed using PROGRESS.md checkboxes.
>
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
