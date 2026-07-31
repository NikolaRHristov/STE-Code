# STE-Code: Simplified Technical English for Code — Implementation Protocol

> **CRITICAL: Anti-Fabrication Rules — READ BEFORE ANY ACTION**
>
> 1. You MUST NOT write any output file until its prerequisite data exists on disk.
> 2. Every phase has a HARD GATE — a file-existence check. Do not proceed past a gate.
> 3. If a worker fails, re-launch it. Do not fabricate its data.
> 4. All STE-Code content MUST cross-reference a source page. No spec data = no output.
> 5. Track progress in `.agents/state/PROGRESS.md` — update it after EVERY completed step.

---

## Version History

| Version | Date | Author | Change | Rationale |
|---------|------|--------|--------|-----------|
| 1.0 | 2025-07-15 | Agent #1 (Extractor, proto) | Initial protocol — 5 gates, 9 workers, 6 artifacts | First working extraction pipeline |
| 1.1 | 2025-07-22 | Agent #2 (Refiner) | Added worker failure protocol (retry, split, sub-workers). Added JSON validation in verification step. | Workers were failing silently; needed recovery paths |
| 1.2 | 2025-07-28 | Agent #3 (Auditor) | Added anti-fabrication rules block at document top. Added spot-check validation in GATE 2. | Audit found fabricated rule text in 3 of 9 worker JSONs |
| 1.3 | 2025-07-29 | Agent #1 (Extractor) | Updated worker table to match 109-worker grid (granular-strategy.md). Documented 4pp sweet spot. | Original 9-worker split was too coarse; workers missed content |
| 1.4 | 2025-07-30 | Hermes (maturity audit) | Added cross-reference index, known limitations, measurable quality gates, schema evolution protocol, recovery protocols, environment dependencies, timing budget, decision consequences, and glossary. | Maturity audit identified 5 structural gaps. This release fills all 5 plus adds 7 proactive sections. |
| 1.5 | 2026-07-31 | Hermes (operator) | Updated GATE 0 to use page-dir/ naming. Updated GATE 1 to use 109-worker markdown pipeline. Updated model references to poolside/laguna-s-2.1:free. Removed JSON-based worker schema in favor of markdown extraction. | Page files now use spec page identifiers in page-dir/. Model is poolside/laguna-s-2.1:free, not poolside/laguna-s-2.1:free. Workers output .md files, not .json files. |

### How to Update This Version Table

After any change to this document:

1. Add a new row to the version history table.
2. Use the current date in `YYYY-MM-DD` format.
3. State the author as your agent role or `Hermes (operator)`.
4. Describe the change in one sentence.
5. Explain why the change was needed.
6. Do NOT delete any existing rows. The full history stays visible.

---

## Cross-Reference Index

This protocol does not exist in isolation. The table below lists every document that this protocol depends on, extends, or drives. Read these documents before you start execution.

### Documents This Protocol DEPENDS ON (must exist and be correct)

| Reference | Path | What It Provides | Why This Protocol Needs It |
|-----------|------|------------------|----------------------------|
| Granular Strategy | `.agents/references/granular-strategy.md` | Page-split rationale: why 4pp per worker, why 109 workers, why 37 batches | GATE 1 worker assignments assume this split. If the strategy changes, worker counts break. |
| Section Types | `.agents/references/section-types.md` | Content signature per page range, tailored extraction prompts, edge case rules | Workers need content-aware extraction. Generic extraction misses rule/dictionary boundary markers. |
| Worker Grid | `.agents/references/worker-grid.md` | Full 109-worker launch architecture, batch map, worker-to-page mapping | GATE 1 launch protocol uses this grid. Without it, workers hit the wrong pages. |
| Worker Rails | `.agents/references/worker-rails.md` | 10 output-format rails injected into every worker prompt | Workers validate their own output before writing. Missing rails = corrupted output files. |
| Process Rails | `.agents/references/rails.md` | 8 process rails for all orchestrators and workers | Anti-fabrication rules (top of this document) derive from rail R4. |
| Quality Checklist | `.agents/references/quality-checklist.md` | Per-batch verification checklist run after each batch of 3 | GATE 1 batch validation references this. Skip it and malformed output passes through. |
| Category Mapping | `.agents/references/category-mapping.md` | 19 technical noun categories mapped from STE to STE-Code | GATE 3 adaptation needs these mappings. Incorrect mapping = incorrect output artifacts. |
| Page Files | `spec/issue-09-2025/page-dir/page-*.md` | 426 individual spec page files split from combined markdown | GATE 0 verifies these exist. Workers read these in GATE 1. |

### Documents That EXTEND This Protocol (read only when relevant)

| Reference | Path | What It Provides | When to Read It |
|-----------|------|------------------|-----------------|
| Agent #1 (Extractor) | `.agents/agent/agent-1-extractor.md` | Full extraction orchestration role with worker launch, retry, and verification | When you are the Extraction Orchestrator running GATE 1 |
| Agent #2 (Refiner) | `.agents/agent/agent-2-refiner.md` | Refinement role that reformats extracted text into clean markdown | When GATE 1 completes and refinement starts |
| Agent #3 (Auditor) | `.agents/agent/agent-3-auditor.md` | Ground-truth verification of claims against disk evidence | When you need to verify any claim in this pipeline |
| Agent #4 (Continuator) | `.agents/agent/agent-4-continuation.md` | Multi-agent continuation for stages 3-5 from any agent perspective | When a session ends mid-phase and a new agent must resume |
| Agent #5 (SCE Populator) | `.agents/agent/agent-5-sce-populator.md` | STE-Code dictionary entry generation | When dictionary entries need creation or expansion |
| Agent #6 (STE-Code Analysis) | `.agents/agent/agent-6-phi-sce.md` | Paradigm-agnostic STE-Code compliant documentation generator | When you need to produce STE-Code output from arbitrary inputs |
| Agent #7 (Level Worker) | `.agents/agent/agent-7-level-worker.md` | Parameterized worker for levels 1-5 rewrite/test/benchmark actions | When you run level-based operations |
| Agent #8 (Extension Worker) | `.agents/agent/agent-8-extension-worker.md` | Code-domain gap filler generation via batched poll workers | When you need dictionary/category/anti-pattern extensions |
| Agent #9 (Translations) | `.agents/agent/agent-9-translations.md` | Multi-locale placeholder pipeline across 9 locales, ~540 files | When you need to scaffold translation infrastructure |
| Translation Grid | `.agents/references/translation-grid.md` | Discovery-based translation target tracking across 10 source directories | When you plan what artifacts need locale scaffolding |

### Documents This Protocol DRIVES (created by following this protocol)

| Artifact | Path | Created By | Gate |
|----------|------|-----------|------|
| Progress Tracker | `.agents/state/PROGRESS.md` | GATE 0 init script | GATE 0 |
| 109 Extraction Files | `ste-code/extracted/wNNN-pPPPP-PPPP.md` | GATE 1 workers | GATE 1 |
| Master State | `ste-code/merged/master.md` | GATE 2 merge script | GATE 2 |
| 6 Output Artifacts | `ste-code/artifacts/*.txt` + `ste-code/README.md` | GATE 4 artifact writers | GATE 4 |

---

## Protocol Scope

### What This Protocol Covers

- Extraction of the ASD-STE100 Issue 9 specification into markdown files
- Merging and validation of extracted data
- Adaptation of STE rules for the code documentation domain
- Generation of 6 deployable output artifacts

### What This Protocol Does NOT Cover

- Refinement of extracted text (handled by Agent #2 after GATE 1 completes)
- Live deployment of artifacts to production systems
- Continuous maintenance of artifacts after initial generation
- Translation of artifacts into other languages (see Agent #9 and translation-grid.md)
- Benchmark execution (see `.agents/benchmark/`)
- UML diagram generation (see `.agents/uml/`)
- Inter-agent communication protocol (see `.agents/feedback/`)

---

## GATE 0: Environment Setup

**Before any extraction, verify these paths exist and are readable:**

```bash
# Verify page-dir exists with page files
ls spec/issue-09-2025/page-dir/page-front-matter.md  # Must return the file
ls spec/issue-09-2025/page-dir/page-HI-1.md          # Must return the file
ls spec/issue-09-2025/page-dir/page-2-1-Y2.md        # Must return the file
ls spec/issue-09-2025/page-dir/MANIFEST.md           # Must return the file

# Verify combined markdown exists
test -f spec/issue-09-2025/issue-09-2025.md && echo "Combined markdown: OK"

# If page-dir is missing, regenerate it:
# python3 spec/issue-09-2025/split_spec.py
```

**Create output directories:**

```bash
mkdir -p ste-code/extracted
mkdir -p ste-code/refined
mkdir -p ste-code/merged
mkdir -p ste-code/adapted
mkdir -p ste-code/artifacts
```

**Initialize progress tracking:**

```bash
cat > .agents/state/PROGRESS.md << 'TRACKER'
# STE-Code Progress Tracker — 109-Worker Grid

## GATE 0: Environment ✓
- [x] Page files exist in spec/issue-09-2025/page-dir/ (426 files + MANIFEST.md)
- [x] Output directories created (extracted/, refined/, merged/, adapted/, artifacts/)
- [x] State saved via git gcommit-hermes

## Extraction — 4 pages per worker, 109 workers total (434 pages)
Output directory: `ste-code/extracted/wNNN-pPPPP-PPPP.md`

| Batch | Workers | Pages | Status |
|-------|---------|-------|--------|
| 1 | W001(1-4), W002(5-8), W003(9-12) | 1-12 | [ ] |
| 2 | W004(13-16), W005(17-20), W006(21-24) | 13-24 | [ ] |
| 3 | W007(25-28), W008(29-32), W009(33-36) | 25-36 | [ ] |
| 4 | W010(37-40), W011(41-44), W012(45-48) | 37-48 | [ ] |
| 5 | W013(49-52), W014(53-56), W015(57-60) | 49-60 | [ ] |
| 6 | W016(61-64), W017(65-68), W018(69-72) | 61-72 | [ ] |
| 7 | W019(73-76), W020(77-80), W021(81-84) | 73-84 | [ ] |
| 8 | W022(85-88), W023(89-92), W024(93-96) | 85-96 | [ ] |
| 9 | W025(97-100), W026(101-104), W027(105-108) | 97-108 | [ ] |
| 10 | W028(109-112), W029(113-116), W030(117-120) | 109-120 | [ ] |
| 11 | W031(121-124), W032(125-128), W033(129-132) | 121-132 | [ ] |
| 12 | W034(133-136), W035(137-140), W036(141-144) | 133-144 | [ ] |
| 13 | W037(145-148), W038(149-152), W039(153-156) | 145-156 | [ ] |
| 14 | W040(157-160), W041(161-164), W042(165-168) | 157-168 | [ ] |
| 15 | W043(169-172), W044(173-176), W045(177-180) | 169-180 | [ ] |
| 16 | W046(181-184), W047(185-188), W048(189-192) | 181-192 | [ ] |
| 17 | W049(193-196), W050(197-200), W051(201-204) | 193-204 | [ ] |
| 18 | W052(205-208), W053(209-212), W054(213-216) | 205-216 | [ ] |
| 19 | W055(217-220), W056(221-224), W057(225-228) | 217-228 | [ ] |
| 20 | W058(229-232), W059(233-236), W060(237-240) | 229-240 | [ ] |
| 21 | W061(241-244), W062(245-248), W063(249-252) | 241-252 | [ ] |
| 22 | W064(253-256), W065(257-260), W066(261-264) | 253-264 | [ ] |
| 23 | W067(265-268), W068(269-272), W069(273-276) | 265-276 | [ ] |
| 24 | W070(277-280), W071(281-284), W072(285-288) | 277-288 | [ ] |
| 25 | W073(289-292), W074(293-296), W075(297-300) | 289-300 | [ ] |
| 26 | W076(301-304), W077(305-308), W078(309-312) | 301-312 | [ ] |
| 27 | W079(313-316), W080(317-320), W081(321-324) | 313-324 | [ ] |
| 28 | W082(325-328), W083(329-332), W084(333-336) | 325-336 | [ ] |
| 29 | W085(337-340), W086(341-344), W087(345-348) | 337-348 | [ ] |
| 30 | W088(349-352), W089(353-356), W090(357-360) | 349-360 | [ ] |
| 31 | W091(361-364), W092(365-368), W093(369-372) | 361-372 | [ ] |
| 32 | W094(373-376), W095(377-380), W096(381-384) | 373-384 | [ ] |
| 33 | W097(385-388), W098(389-392), W099(393-396) | 385-396 | [ ] |
| 34 | W100(397-400), W101(401-404), W102(405-408) | 397-408 | [ ] |
| 35 | W103(409-412), W104(413-416), W105(417-420) | 409-420 | [ ] |
| 36 | W106(421-424), W107(425-428), W108(429-432) | 421-432 | [ ] |
| 37 | W109(433-434) — 2 pages only | 433-434 | [ ] |

## Merge
- [ ] Master state merged from all 109 worker outputs
- [ ] Spot-check: 10 random pages verified against source

## Adaptation (performed AFTER merge is complete)
- [ ] Section 1 Rules (1.1-1.14) adapted for code
- [ ] Section 2 Rules (2.1-2.3) adapted for code
- [ ] Section 3 Rules (3.1-3.7) adapted for code
- [ ] Section 4 Rules (4.1-4.4) adapted for code
- [ ] Section 5 Rules (5.1-5.5) adapted for code
- [ ] Section 6 Rules (6.1-6.6) adapted for code
- [ ] Section 7 Rules (7.1-7.3) adapted for code
- [ ] Section 8 Rules (8.1-8.7) adapted for code
- [ ] Section 9 Rules (9.1-9.4 + GR1-GR4) adapted for code
- [ ] 19 Technical Code Noun categories remapped
- [ ] Canonical synonym table adapted
- [ ] Polysemy resolution table adapted
- [ ] 6-pass pipeline adapted

## Output Artifacts (written AFTER all adaptation checkboxes above are checked)
- [ ] ste-code-distilled-system-prompt.txt (short form)
- [ ] ste-code-self-reading-manual.txt (long form)
- [ ] ste-code-extraction-methodology.txt
- [ ] ste-code-example-turn.txt
- [ ] ste-code-deployment-guide.txt
- [ ] README.md
TRACKER

echo "GATE 0 PASSED: Environment ready"
```

**DO NOT proceed past GATE 0 until `.agents/state/PROGRESS.md` exists and all spec paths are confirmed readable.**

---

## GATE 1: Worker Extraction

### Worker Specification

Each worker is a separate `hermes -z` session. All workers use `poolside/laguna-s-2.1:free` (the available model in this environment).
Workers extract RAW spec text — they do NOT adapt or rewrite anything.

**Pipeline configuration:** 109 workers, 4 pages per worker, 37 batches of 3 workers.
See `.agents/references/worker-grid.md` for the full batch map and `.agents/references/worker-rails.md` for output format rails.

### Worker Assignments

Workers are launched in 37 batches of 3, each reading 4 pages from `spec/issue-09-2025/page-dir/`.
The full worker-to-page mapping is in `.agents/references/worker-grid.md`. Key ranges:

| Batch | Workers | Pages | Section Type |
|-------|---------|-------|--------------|
| 1 | W001(1-4), W002(5-8), W003(9-12) | 1-12 | FRONT |
| 2 | W004(13-16), W005(17-20), W006(21-24) | 13-24 | TOC + INDEX |
| 3 | W007(25-28), W008(29-32), W009(33-36) | 25-36 | INTRO |
| 4-5 | W010-W015 | 37-60 | RULES + CATEGORIES |
| 6-10 | W016-W030 | 61-120 | RULES |
| 11-12 | W031-W036 | 121-144 | RULES + DICT start |
| 13-30 | W037-W090 | 145-360 | DICT (A-F, G-P, Q-Z) |
| 31-37 | W091-W109 | 361-434 | APPENDIX |

### Worker Output Format

Each worker outputs a markdown file: `ste-code/extracted/wNNN-pPPPP-PPPP.md`

File structure:
```markdown
# Page N of 434

## Section Title From Spec

Content paragraph. Preserve all text exactly.

### Subsection

More content. Do not add commentary. Do not summarize.

#### WORD (POS) — APPROVED

- **Meaning:** exact approved meaning from spec
- **Forms:** form1, form2, form3
- **STE:** approved example sentence
- **Non-STE:** non-approved example sentence
```

### Worker Launch Protocol (Batch of 3)

**DO NOT launch more than 3 workers at once.** After each batch, verify the output files exist and pass quality checks before launching the next batch.

**Batch 1 — Launch:**
```bash
hermes -z "Read spec/issue-09-2025/page-dir/page-front-matter.md through page-1-1-4.md. Extract ALL content exactly into ste-code/extracted/w001-p1-4.md. Do not summarize. Include every word, every table, every example. Output ONLY the markdown file." -m poolside/laguna-s-2.1:free --yolo &
hermes -z "Read spec/issue-09-2025/page-dir/page-1-1-5.md through page-1-1-8.md. Extract ALL content exactly into ste-code/extracted/w002-p5-8.md. Do not summarize. Include every word, every table, every example. Output ONLY the markdown file." -m poolside/laguna-s-2.1:free --yolo &
hermes -z "Read spec/issue-09-2025/page-dir/page-1-1-9.md through page-1-1-12.md. Extract ALL content exactly into ste-code/extracted/w003-p9-12.md. Do not summarize. Include every word, every table, every example. Output ONLY the markdown file." -m poolside/laguna-s-2.1:free --yolo &
```

**Batch 1 — Verify (after workers complete):**
```bash
# Check files exist
test -f ste-code/extracted/w001-p1-4.md && echo "W001 OK" || echo "W001 MISSING — RE-LAUNCH"
test -f ste-code/extracted/w002-p5-8.md && echo "W002 OK" || echo "W002 MISSING — RE-LAUNCH"
test -f ste-code/extracted/w003-p9-12.md && echo "W003 OK" || echo "W003 MISSING — RE-LAUNCH"

# Check file sizes (FRONT section threshold: > 2 KB)
for f in ste-code/extracted/w001-p1-4.md ste-code/extracted/w002-p5-8.md ste-code/extracted/w003-p9-12.md; do
  if [ -f "$f" ]; then
    size=$(wc -c < "$f")
    lines=$(wc -l < "$f")
    echo "$f: $size bytes, $lines lines"
  fi
done

# Check for fabrication signals
grep -r -c 'React\|Docker\|npm\|async/await\|This page describes\|In summary' ste-code/extracted/w001-p1-4.md ste-code/extracted/w002-p5-8.md ste-code/extracted/w003-p9-12.md || echo "No fabrication signals found"
```

**Update PROGRESS.md** after each verified batch:
```bash
# In .agents/state/PROGRESS.md, change [ ] to [x] for W001, W002, W003
```

### Worker Failure Protocol

If ANY worker output file is missing, has zero content, or fails quality checks:
1. Mark it `[!] FAILED` in PROGRESS.md
2. Re-launch that specific worker with the SAME prompt
3. If it fails twice, split its page range in half and launch two sub-workers
4. Do NOT proceed past GATE 1 until all 3 workers in the batch pass checks

---

### Quality Gates for Extraction (Measurable Thresholds)

> **CRITICAL:** Binary checks (file exists, non-empty) are necessary but insufficient. Apply these quantitative thresholds to every worker output before accepting it.

#### QG1: File Existence & Size

| Check | Threshold | Method |
|-------|-----------|--------|
| Output file exists | File present on disk | `test -f <file>` |
| File size > 2 KB (FRONT/TOC) | 2,048 bytes minimum | `wc -c < <file>` |
| File size > 3 KB (INDEX/INTRO) | 3,072 bytes minimum | `wc -c < <file>` |
| File size > 5 KB (RULES) | 5,120 bytes minimum | `wc -c < <file>` |
| File size > 8 KB (DICT) | 8,192 bytes minimum | `wc -c < <file>` |
| File size > 1.5 KB (last batch only) | 1,536 bytes minimum for W109 | `wc -c < <file>` |

#### QG2: Truncation Detection

| Check | Method | Action on Failure |
|-------|--------|-------------------|
| Last 3 lines end cleanly | `tail -3 <file>` — no mid-word breaks | Split page range in half, retry both |
| No mid-sentence endings | Last line ends with punctuation or page footer | Re-extract |
| Page header present | `head -1 <file>` matches `# Page N of M` or `**Page <ID>**` | Re-extract with explicit header instruction |

#### QG3: Fabrication Detection

| Check | Method | Action on Failure |
|-------|--------|-------------------|
| No modern software terms | `grep -c -E 'React|Docker|npm|async/await|This page describes|In summary|The key point is' <file>` | CRITICAL: delete file, re-extract from spec |
| No commentary language | `grep -c -E 'This page describes|The key point is|In summary|Essentially|Let me check|Wait, actually' <file>` | Delete file, re-extract |

#### QG4: Content Signals

Use the expected content signals table from `.agents/references/quality-checklist.md` to verify each worker's output matches its section type.

#### QG5: Spot-Check Accuracy

Pick 10 random page numbers from 1-434. Read the original markdown page from `spec/issue-09-2025/page-dir/`. Find the corresponding content in the worker output. Compare character-by-character. If ANY mismatch is found (excluding whitespace normalization), the responsible worker must re-extract.

```bash
python3 -c "
import os, random
# Pick 10 random pages from the MANIFEST
manifest = open('spec/issue-09-2025/page-dir/MANIFEST.md').read()
# Extract page IDs from manifest
import re
page_ids = re.findall(r'\| \d+ \| (.+?) \|', manifest)
sample = random.sample(page_ids, min(10, len(page_ids)))
for pid in sample:
    print(f'Spot-check page ID: {pid}')
    path = f'spec/issue-09-2025/page-dir/page-{pid}.md'
    if not os.path.exists(path):
        print(f'  FILE MISSING (cannot verify)')
    else:
        text = open(path).read()[:500].strip()
        print(f'  Source: {text[:100]}...')
        # Check if this content appears in any extracted file
        found = False
        for ef in os.listdir('ste-code/extracted/'):
            content = open(f'ste-code/extracted/{ef}').read()
            if text[:50] in content:
                found = True
                print(f'  Found in: {ef}')
                break
        if not found:
            print(f'  NO MATCH — content from page {pid} not found in any extracted file')
"
```

#### Quality Gate Summary

| Gate | Threshold | Fails If | Recovery |
|------|-----------|----------|----------|
| QG1: File Existence & Size | File exists, size > per-type threshold | File missing or below threshold | Re-launch worker. If persists, split page range. |
| QG2: Truncation | Last 3 lines end cleanly | Mid-word or mid-sentence ending | Split page range in half, re-extract both |
| QG3: Fabrication | 0 banned terms found | Any banned term in output | Delete file, re-extract from spec |
| QG4: Content Signals | 3 of 3 sampled lines match section type | Fewer than 3 matches | Expand sample to 8 lines. If still < 3, re-extract. |
| QG5: Spot-Check | 10 of 10 random pages match | Any page has zero matches in extracted output | Flag the specific worker, re-extract with halved page range |

**Do not proceed past GATE 1 until all quality gates pass for all 3 workers in the batch.**

---

## GATE 2: Merge and Validate

**HARD GATE: All 109 extraction files must exist in `ste-code/extracted/` and pass quality checks.**

```bash
python3 -c "
import os
expected = 109
actual = len([f for f in os.listdir('ste-code/extracted/') if f.startswith('w') and f.endswith('.md')])
print(f'Extraction files: {actual}/{expected}')
if actual < expected:
    missing = expected - actual
    print(f'FAIL: {missing} files missing. Do not proceed.')
    exit(1)
print('PASS: All 109 extraction files present.')
"
```

### Merge into Master State

Concatenate all 109 refined files into `ste-code/merged/master.md`:
- Deduplicate content at page boundaries
- Sort by spec page order (use MANIFEST.md for ordering)
- Preserve all content verbatim — no summarization

### Spot-Check Validation

Pick 10 random page numbers from 1-434. For each:
1. Read the original markdown page from `spec/issue-09-2025/page-dir/`
2. Find the corresponding content in `ste-code/merged/master.md`
3. Verify the text matches EXACTLY

If ANY mismatch found, flag the worker responsible and re-extract those pages.

---

## GATE 3: Adaptation (Phase 2 from Original)

**HARD GATE: `ste-code/merged/master.md` must exist and contain verified data.**

Only NOW do you begin adaptation. For each rule in the master state:

### Adaptation Protocol (PER RULE)

1. Read the rule's exact text from master.md
2. Read the STE and non-STE example pairs
3. Think: "What is the coding-domain equivalent of this constraint?"
4. Write the adapted rule text preserving the original structure
5. Write code-domain example pairs (non-STE-Code → STE-Code)
6. Cross-reference: note which original rule number this maps to

### Category Remapping (ALL 19)

For each of the 19 categories, produce a table entry:

| Original Category | STE-Code Category | Rationale |
|-------------------|-------------------|-----------|
| Exact name from master.md | Code-domain equivalent | 1-sentence justification |

### Synonym Table Adaptation

Take every canonical synonym pair from the controlled terminology. For each:
- Keep the original canonical form if it works for code domain
- OR adapt it to a code-domain equivalent
- Document the mapping

---

## GATE 4: Output Artifacts

**HARD GATE: All adaptation checkboxes in PROGRESS.md must be checked `[x]`.**

Only NOW write the output files. Each file MUST reference specific data from master.md.

### File 1: ste-code-distilled-system-prompt.txt

Write to `ste-code/artifacts/ste-code-distilled-system-prompt.txt`

Structure:
```
# STE-Code Distilled System Prompt
# Derived from ASD-STE100 Issue 9 (January 2025)
# Adapted for code documentation, Issue 1, July 2026

## IDENTITY
[1 paragraph — STE-Code agent identity]

## 14 CORE PRINCIPLES (P1-P14)
P1. [Adapted from Rules 1.2, 1.3, 9.2 — original text: "EXACT QUOTE FROM MASTER"]
P2. [Adapted from Rules 1.3, 9.4 — original text: "..."]
... through P14

## CANONICAL SYNONYM TABLE
||| STE-Code | NOT | Original STE Mapping |||
|||...|...|...|

## APPROVED VOCABULARY POLICY
[Adapted from master.md vocabulary architecture]

## DOCUMENT INTERACTION PROTOCOL
[10-step protocol adapted for code documents]

## OUTPUT FORMAT
## COMPLIANCE STATUS / ## TECHNICAL OUTPUT / ## UML EXTRACTION / ## OPTIMIZATIONS

## ANTI-PATTERNS
[10 rules, adapted from original]
```

### File 2: ste-code-self-reading-manual.txt

Write to `ste-code/artifacts/ste-code-self-reading-manual.txt`

8 sections (S0-S8) following the exact structure of the original SSRM.
Each section must reference data from master.md.

### File 3: ste-code-extraction-methodology.txt

Write to `ste-code/artifacts/ste-code-extraction-methodology.txt`

Turn-by-turn protocol adapted for code documents.

### File 4: ste-code-example-turn.txt

Write to `ste-code/artifacts/ste-code-example-turn.txt`

Single worked example with before/after transformation.

### File 5: ste-code-deployment-guide.txt

Write to `ste-code/artifacts/ste-code-deployment-guide.txt`

Deployment for Ollama, LM Studio, Python.

### File 6: README.md

Write to `ste-code/README.md`

Summary of the project.

---

## Final Verification

After all 6 files are written, run:

```bash
# Count tokens (approximate: chars/4)
for f in ste-code/artifacts/*.txt; do
  chars=$(wc -c < "$f")
  echo "$(basename $f): $chars chars ~$((chars/4)) tokens"
done

# Verify all files reference master.md data
python3 -c "
import os
master_size = os.path.getsize('ste-code/merged/master.md')
print(f'Master state: {master_size:,} chars')
print('All artifact files must exist in ste-code/artifacts/')
for f in os.listdir('ste-code/artifacts/'):
    if f.endswith('.txt') or f.endswith('.md'):
        size = os.path.getsize(f'ste-code/artifacts/{f}')
        print(f'  {f}: {size:,} chars')
"
```

---

## Phase Flow Summary (with Hard Gates)

```
GATE 0:  Verify spec files exist in page-dir/, create directories, init PROGRESS.md
  ↓ (gate passes: all files confirmed)
GATE 1:  Launch 109 workers in 37 batches of 3, verify output files
  ↓ (gate passes: 109 valid .md files with real content)
GATE 2:  Merge into master.md, spot-check 10 random pages
  ↓ (gate passes: master.md valid, spot-checks pass)
GATE 3:  Adapt all 53 rules, 19 categories, synonyms, polysemy pipeline
  ↓ (gate passes: all PROGRESS.md checkboxes checked)
GATE 4:  Write 6 artifact files to ste-code/artifacts/
  ↓ (gate passes: all files exist, token budgets met)
  DONE
```

---

## Known Limitations and Edge Cases

### Limitation 1: Malformed Markdown in Spec Pages

**Problem:** If a spec page contains broken markdown (unclosed code fences, mismatched headers, corrupted tables), the worker may misparse the page and produce garbled extraction.

**Detection:** A worker output that passes format checks but contains jumbled text (characters from wrong sections, truncated sentences) likely hit a malformed page.

**Mitigation:** Before launching workers, run a syntax check on all page files:

```bash
python3 -c "
import os
page_dir = 'spec/issue-09-2025/page-dir'
for f in sorted(os.listdir(page_dir)):
    if not f.endswith('.md'):
        continue
    path = os.path.join(page_dir, f)
    text = open(path).read()
    # Check for unclosed code fences
    fences = text.count('\`\`\`')
    if fences % 2 != 0:
        print(f'UNCLOSED FENCE: {path} ({fences} backtick groups)')
    # Check for empty content
    if len(text.strip()) < 10:
        print(f'NEARLY EMPTY: {path}')
"
```

### Limitation 2: Spec Page Count Mismatch

**Problem:** The protocol assumes 426 page files in `spec/issue-09-2025/page-dir/`. If the directory contains fewer pages (a partial split, a truncated download), workers will read missing files and produce incomplete output.

**Detection:** The GATE 0 file check confirms key page files exist. Run a gap check after GATE 0:

```bash
python3 -c "
import os
manifest = 'spec/issue-09-2025/page-dir/MANIFEST.md'
if not os.path.exists(manifest):
    print('FAIL: MANIFEST.md missing')
    exit(1)
lines = open(manifest).readlines()
page_count = sum(1 for l in lines if l.strip().startswith('|') and 'page-' in l)
print(f'Manifest page entries: {page_count}')
if page_count < 426:
    print(f'WARNING: Expected 426 pages, found {page_count}')
else:
    print('All pages present.')
"
```

### Limitation 3: Context Window Constraints

**Problem:** This protocol uses `poolside/laguna-s-2.1:free`. If the target model changes (a smaller model, a different provider), the 4-page-per-worker ranges may exceed the context window. The worker will truncate input silently mid-page, producing incomplete extraction.

**Detection:** Compare output file size against the per-type thresholds in QG1. A file significantly below threshold suggests truncation.

**Mitigation:** If the model has a smaller context window, reduce pages per worker to 2 and double the worker count. The 4-page grouping is optimized for the current model.

### Limitation 4: Model Unavailability

**Problem:** If `poolside/laguna-s-2.1:free` is unavailable (API outage, rate limit, credential expiry), all 3 workers in a batch will fail simultaneously. There is no fallback model specified in this protocol.

**Detection:** Batch workers all fail with HTTP 429 or 503 errors. No output files are written.

**Mitigation:**
1. Check provider status.
2. Wait for the rate limit window to reset.
3. If the outage persists beyond 30 minutes, switch to an alternative model. Update all model flags in the launch commands.
4. Document the model switch in the version history table.

### Limitation 5: Inter-Worker Boundary Errors

**Problem:** W033 covers pages 129-132 and W034 covers pages 133-136. A rule that starts on page 132 and continues on page 133 may be partially extracted by W033 (truncated) and partially by W034 (missing the beginning). The merge step sees two incomplete fragments.

**Detection:** After GATE 2 merge, check for rules with truncated text (ends with "..." or a mid-sentence fragment) or rules appearing in two workers with overlapping content.

**Mitigation:** Workers at section boundaries add the note `[CONTINUED on next worker]` or `[CONTINUED from previous worker]` at the split point. The refiner joins them. See `.agents/references/section-types.md` Edge Case Resolution for details.

### Limitation 6: Spec Page Reference Drift

**Problem:** This protocol references ASD-STE100 Issue 9 (January 2025). If the spec source changes (new issue, updated PDF), the page file contents may not match what the protocol expects.

**Mitigation:** Use `spec/issue-09-2025/` as the authoritative source. Workers MUST extract from `spec/issue-09-2025/page-dir/` only. Do not read from other spec directories unless the task description explicitly requires historical comparison.

### Limitation 7: Concurrent Write Collisions

**Problem:** If two instances of this protocol run simultaneously (two separate `hermes` sessions both following this document), they will write to the same `ste-code/extracted/` directory. One session may overwrite the other's output.

**Detection:** Worker output files change unexpectedly between verification and merge.

**Mitigation:** Before starting GATE 0, check for an existing lock file:

```bash
test -f .agents/state/PIPELINE_RUNNING && echo "ANOTHER PIPELINE IS ACTIVE" || echo "CLEAR"
```

Create the lock file at GATE 0 start. Remove it at GATE 4 completion or on any hard failure.

---

## Recovery Protocols

### Recovery Path: Single Worker Failure

1. Mark the worker `[!] FAILED` in PROGRESS.md.
2. Re-launch the same worker with the same prompt.
3. If it passes on the second attempt, mark it `[x]` and continue.
4. If it fails again, split its page range in half and launch two sub-workers.

### Recovery Path: Full Batch Failure (3 workers all fail)

1. Check network connectivity and model API status.
2. If the model is unavailable, switch to an alternative model (see Limitation 4).
3. If the model is available but all prompts return empty, the prompt template may contain an error. Check for unescaped characters, mismatched quotes, or format issues.
4. Re-launch the batch after fixing the root cause.

### Recovery Path: Merge Failure (master.md is invalid)

1. Check which worker output file introduced the corruption. Validate each file individually.
2. Re-extract the corrupted worker.
3. Re-run the merge.
4. If corruption persists, manually merge the valid worker outputs and flag the corrupted worker's page range for re-extraction from the raw spec pages.

### Recovery Path: Adaptation Failure (cannot map a rule to code domain)

1. Some STE rules have no direct code-domain equivalent (for example, rules about physical safety warnings). Document these as "no adaptation — retained as reference" in the adaptation output.
2. Do NOT force an adaptation. A missing adaptation is better than a fabricated one.
3. Note the unadapted rules in PROGRESS.md with a `[~] SKIPPED` marker and the reason.

### Recovery Path: Artifact Write Failure (disk full, permissions)

1. Check available disk space: `df -h ste-code/artifacts/`
2. Check write permissions: `touch ste-code/artifacts/.write_test`
3. If disk is full, clean up temporary files or expand the volume.
4. If permissions are wrong, fix them and re-run GATE 4.

### Recovery Path: Lock File Stuck (previous pipeline crashed)

1. If `.agents/state/PIPELINE_RUNNING` exists but no pipeline is active, remove it manually.
2. Check PROGRESS.md to understand where the previous run stopped.
3. Resume from the next incomplete gate.

---

## Schema Evolution Protocol

### When to Evolve the Worker Output Schema

The worker output format may need new fields when:

1. A new section of the spec is discovered that does not fit into the current extraction format.
2. A downstream artifact needs structured data not captured by the current markdown output.
3. A quality gate requires a new quantitative metric that the current format does not support.

### Protocol for Adding a Field

1. **Document the need.** Add a row to the version history table explaining what field is needed and why.
2. **Update the worker prompt template.** Add the new field instructions to the GATE 1 prompt section.
3. **Add a quality gate for the new field** in the Quality Gates section (QG6, QG7, etc.).
4. **Re-extract affected pages** if the new field requires data that old worker outputs do not contain.

### Protocol for Renaming a Field

1. Do NOT rename fields. Add a new field and mark the old one as DEPRECATED in the schema comments.
2. During GATE 2 merge, read from the new field if present, fall back to the old field if absent.
3. After all 109 workers use the new field, remove the DEPRECATED field from the schema.

### Protocol for Removing a Field

1. Mark the field as DEPRECATED for one full pipeline run.
2. Verify that no downstream code (merge scripts, quality gates, artifact writers) references the deprecated field.
3. Remove the field from the schema. Document the removal in the version history.

### Self-Modification Authority Model

This document can be modified by:
- **Agent #3 (Auditor):** When audit discovers a structural gap, protocol error, or fabrication risk.
- **Any orchestration agent (#1, #2, #4):** When a pipeline run reveals an operational gap not covered by existing protocol.
- **Hermes operator:** When directed by the user to update the protocol.

Before any modification:
1. Read the full document.
2. Understand the version history.
3. Add a new version row.
4. Update the cross-reference index if new dependencies are introduced or existing references change paths.
5. Run all existing quality gate scripts to confirm they still work with the modified schema.

---

## Environment Dependencies

| Dependency | Minimum Version | Check Command | Gate Where Used |
|------------|----------------|---------------|-----------------|
| Python 3 | 3.9+ | `python3 --version` | GATE 0, 1, 2, 4 |
| Hermes Agent | 0.19.0+ | `hermes --version` | GATE 1 (worker launch) |
| Model: poolside/laguna-s-2.1:free | — | API availability check | GATE 1 (all workers) |
| Bash | 3.2+ | `bash --version` | GATE 0 (init scripts) |
| Disk space | 500 MB free | `df -h .` | GATE 1 (output file storage) |
| Spec files | ASD-STE100 Issue 9, 426 page files | `ls spec/issue-09-2025/page-dir/page-HI-1.md` | GATE 0 |

### Pre-Flight Environment Check

Run this before GATE 0 to verify all dependencies:

```bash
echo "=== Environment Check ==="
python3 --version || { echo "FAIL: Python 3 not found"; exit 1; }
echo "Python: OK"

hermes --version 2>/dev/null || { echo "WARN: hermes not in PATH (check ~/.hermes/bin)"; }
echo "Hermes: OK"

df -h . | tail -1 | awk '{print "Disk: " $4 " free"}'

test -f spec/issue-09-2025/page-dir/page-HI-1.md && echo "Spec: OK" || { echo "FAIL: Spec files missing"; exit 1; }

echo "=== All checks passed ==="
```

---

## Timing Budget Estimates

Total pipeline wall-clock time under ideal conditions: **approximately 37-74 minutes.**

| Phase | Task | Est. Time | Parallelism | Notes |
|-------|------|-----------|-------------|-------|
| GATE 0 | Environment setup | 30 sec | Serial | File checks + directory creation |
| GATE 1 | Each batch (3 workers) | 10-20 min | 3 parallel workers | Each worker reads 4 pages |
| GATE 1 | 37 batches | 20-37 min | 3 parallel per batch | Serialized batches |
| GATE 1 | Verification per batch | 1 min | Serial | File existence + quality checks |
| GATE 2 | Merge + spot-check | 3-5 min | Serial | Read 109 files, merge, validate 10 pages |
| GATE 2 | Quality gate scripts | 2 min | Serial | QG1-QG5 automated checks |
| GATE 3 | Rule adaptation (53 rules) | 5-8 min | Serial | One agent adapts all rules sequentially |
| GATE 3 | Category + synonym remapping | 2 min | Serial | Table generation |
| GATE 4 | Write 6 artifacts | 3-5 min | Serial | File writes + final verification |
| **Total** | | **~40-75 min** | | Variance depends on model response time |

NOTE: These estimates assume the model API is responsive and no worker failures occur. Add 10-15 minutes per failed worker that requires re-launch. A full batch failure (model outage) adds 30+ minutes.

---

## Decision Consequences

### If You Skip GATE 0

- PROGRESS.md does not exist. You cannot track which workers have completed.
- Output directories are missing. Worker output files fail to write with "No such file or directory."
- Spec files are not verified. Workers may run against missing pages and produce empty output silently.

### If You Skip GATE 1 Verification

- Malformed output files pass to GATE 2. The merge produces garbage.
- Zero-content worker files are accepted. The master state is incomplete.
- The pipeline appears to succeed but produces artifacts with missing data.

### If You Skip GATE 2 Quality Gates

- The master state has missing rules. Artifacts are incomplete.
- The master state has missing dictionary entries. Approved word lists are incorrect.
- Spot-check failures go undetected. Fabricated rule text enters the output artifacts.

### If You Skip GATE 3 Adaptation Verification

- Rules are not adapted for code domain. The output artifacts use aerospace terminology for code concepts.
- Category remapping is incomplete. The 19 technical noun categories have no code-domain equivalents.
- PROGRESS.md checkboxes are unchecked. GATE 4 cannot verify readiness.

### If You Fabricate Data to Pass a Gate

- The anti-fabrication rules at the top of this document are violated.
- The output artifacts contain text that does not appear in the ASD-STE100 specification.
- Any downstream system that relies on these artifacts (system prompts, benchmarks, translations) produces incorrect output.
- The fabrication is detectable: spot-check validation in GATE 2 compares artifact text against raw spec pages. Any mismatch is flagged.

---

## Glossary

| Term | Definition |
|------|-----------|
| **ASD-STE100** | The international specification for Simplified Technical English, maintained by the Aerospace and Defence Industries Association of Europe. |
| **Issue 9** | The January 2025 release of ASD-STE100, containing 53 writing rules, approximately 875 dictionary entries, 19 technical noun categories, and a 6-pass writing pipeline. |
| **Worker** | A single `hermes -z` session that reads a range of spec page files and writes a markdown output file. Workers are stateless. They do not communicate with each other. |
| **Batch** | A group of up to 3 workers launched simultaneously. Batches are serialized: Batch 2 does not start until Batch 1 is verified. |
| **Gate** | A hard checkpoint in the pipeline. Progress past a gate is impossible until its conditions are met. Gates enforce sequential execution and prevent data fabrication. |
| **Master State** | The merged markdown file (`ste-code/merged/master.md`) that combines all 109 worker outputs into a single authoritative document. All adaptation and artifact generation reads from master state. |
| **Adaptation** | The process of transforming aerospace-domain STE rules into code-domain STE-Code rules. This is NOT summarization. Every adapted rule preserves the original structure and intent. |
| **Artifact** | One of 6 output files written in GATE 4. Artifacts are deployable documents (system prompts, manuals, guides) that can be used independently of this pipeline. |
| **Quality Gate** | A quantitative threshold that must be met before proceeding. Unlike binary gates (file exists), quality gates measure completeness (file size, content signals, fabrication detection). |
| **Fabrication** | Writing data into an output file that does not come from a worker output or the original spec. The anti-fabrication rules at the top of this document prohibit this under all circumstances. |
| **Spot-Check** | Reading a random spec page directly and comparing its content against the merged master state. A single mismatch is a failure. |
| **PROGRESS.md** | The state-tracking file at `.agents/state/PROGRESS.md`. Every completed step in the pipeline updates this file. It is the single source of truth for pipeline progress. |

---

## Document Metadata

- **Protocol version:** 1.5
- **Last updated:** 2026-07-31
- **Applies to:** ASD-STE100 Issue 9 (January 2025)
- **Target model:** poolside/laguna-s-2.1:free
- **Framework:** Hermes Agent
- **Total spec pages:** 434 (426 page files in page-dir/)
- **Expected output:** 6 artifacts in `ste-code/artifacts/`
- **Estimated total runtime:** 40-75 minutes (ideal conditions)
