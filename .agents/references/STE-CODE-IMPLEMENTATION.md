# STE-Code: Simplified Technical English for Code — Implementation Protocol

> **CRITICAL: Anti-Fabrication Rules — READ BEFORE ANY ACTION**
>
> 1. You MUST NOT write any output file until its prerequisite worker JSON exists on disk.
> 2. Every phase has a HARD GATE — a file-existence check. Do not proceed past a gate.
> 3. If a worker fails, re-launch it. Do not fabricate its data.
> 4. All STE-Code content MUST cross-reference a worker JSON entry. No spec data = no output.
> 5. Track progress in `.agents/state/PROGRESS.md` — update it after EVERY completed step.

---

## Version History

This document is a living protocol. Record all structural changes, field additions, and logic updates below.

| Version | Date | Author | Change | Rationale |
|---------|------|--------|--------|-----------|
| 1.0 | 2025-07-15 | Agent #1 (Extractor, proto) | Initial protocol — 5 gates, 9 workers, 6 artifacts | First working extraction pipeline |
| 1.1 | 2025-07-22 | Agent #2 (Refiner) | Added worker failure protocol (retry, split, sub-workers). Added JSON validation in verification step. | Workers were failing silently; needed recovery paths |
| 1.2 | 2025-07-28 | Agent #3 (Auditor) | Added anti-fabrication rules block at document top. Added spot-check validation in GATE 2. | Audit found fabricated rule text in 3 of 9 worker JSONs |
| 1.3 | 2025-07-29 | Agent #1 (Extractor) | Updated worker table to match 109-worker grid (granular-strategy.md). Documented 4pp sweet spot. | Original 9-worker split was too coarse; workers missed content |
| 1.4 | 2025-07-30 | Hermes (maturity audit) | Added cross-reference index, known limitations, measurable quality gates, schema evolution protocol, recovery protocols, environment dependencies, timing budget, decision consequences, and glossary. | Maturity audit identified 5 structural gaps. This release fills all 5 plus adds 7 proactive sections. |

### How to Update This Version Table

After any change to this document:

1. Add a new row to the version table.
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
| Worker Rails | `.agents/references/worker-rails.md` | 10 output-format rails injected into every worker prompt | Workers validate their own output before writing. Missing rails = corrupted JSON files. |
| Process Rails | `.agents/references/rails.md` | 8 process rails for all orchestrators and workers | Anti-fabrication rules (top of this document) derive from rail R4. |
| Quality Checklist | `.agents/references/quality-checklist.md` | Per-batch verification checklist run after each batch of 3 | GATE 1 batch validation references this. Skip it and malformed JSON passes through. |
| Category Mapping | `.agents/references/category-mapping.md` | 19 technical noun categories mapped from STE to STE-Code | GATE 3 adaptation needs these mappings. Incorrect mapping = incorrect output artifacts. |

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
| Worker JSONs | `ste-code/workers/w1.json` through `w9.json` | GATE 1 workers | GATE 1 |
| Master State | `ste-code/extracted/master.json` | GATE 2 merge script | GATE 2 |
| 6 Output Artifacts | `ste-code/artifacts/*.txt` + `ste-code/README.md` | GATE 4 artifact writers | GATE 4 |

---

## Protocol Scope

### What This Protocol Covers

- Extraction of the ASD-STE100 Issue 9 specification into structured JSON
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
ls spec/issue-09-2025/page-0001.md   # Must return the file
ls spec/issue-09-2025/page-0434.md   # Must return the file
ls spec/issue-07-2017/page-0001.md   # Must return the file
```

**Create output directories:**

```bash
mkdir -p ste-code/workers
mkdir -p ste-code/artifacts
```

**Initialize progress tracking:**

```bash
cat > .agents/state/PROGRESS.md << 'TRACKER'
# STE-Code Progress Tracker

## Workers
- [ ] W1: Front matter + Section 1 rules (pages 1-30) → workers/w1.json
- [ ] W2: Sections 2-3 rules (pages 31-60) → workers/w2.json
- [ ] W3: Sections 4-5 rules (pages 61-90) → workers/w3.json
- [ ] W4: Sections 6-7 rules (pages 91-120) → workers/w4.json
- [ ] W5: Sections 8-9 + GR rules (pages 121-180) → workers/w5.json
- [ ] W6: Dictionary A-F (pages 181-240) → workers/w6.json
- [ ] W7: Dictionary G-P (pages 241-300) → workers/w7.json
- [ ] W8: Dictionary Q-Z (pages 301-360) → workers/w8.json
- [ ] W9: Appendices + history (pages 361-434) → workers/w9.json

## Merge
- [ ] Master state merged from all 9 worker JSONs
- [ ] Spot-check: 10 random pages verified against master state

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

Each worker is a separate `hermes -z` session. All workers use `deepseek-v4-pro` (full reasoning capability).
Workers extract RAW spec text — they do NOT adapt or rewrite anything.

### Worker Assignments

| Worker | Pages | What to Extract | Output |
|--------|-------|-----------------|--------|
| W1 | 1–30 | Front matter, TOC, highlights, Section 1 rules (1.1–1.14) with ALL STE/non-STE example pairs, subject-to-rule index | `workers/w1.json` |
| W2 | 31–60 | Section 2-3 rules (2.1–2.3, 3.1–3.7) with ALL example pairs. Technical noun categories start | `workers/w2.json` |
| W3 | 61–90 | Section 4-5 rules (4.1–4.4, 5.1–5.5) with ALL example pairs. Technical noun categories continue | `workers/w3.json` |
| W4 | 91–120 | Section 6-7 rules (6.1–6.6, 7.1–7.3) with ALL example pairs. Technical noun categories complete | `workers/w4.json` |
| W5 | 121–180 | Section 8-9 rules (8.1–8.7, 9.1–9.4) + GR1–GR4 with ALL examples. Complete polysemy resolution table | `workers/w5.json` |
| W6 | 181–240 | Dictionary A–F: every entry with WORD, POS, approved meaning, approved forms, alternatives. Complete canonical synonym table | `workers/w6.json` |
| W7 | 241–300 | Dictionary G–P: every entry. All transformation examples with before/after text | `workers/w7.json` |
| W8 | 301–360 | Dictionary Q–Z: every entry. Remaining transformation examples | `workers/w8.json` |
| W9 | 361–434 | Appendices, change history (all issues 1-9), decision flowchart, index, 19 category enumeration | `workers/w9.json` |

### Worker JSON Schema

Every worker MUST output this exact JSON structure. No markdown wrapping.

```json
{
  "worker_id": "W1",
  "source_pages": "1-30",
  "pages_actually_read": 30,
  "extraction_timestamp": "ISO8601",
  "rules": [
    {
      "rule_number": "1.1",
      "section": "Words",
      "rule_text": "EXACT TEXT FROM SPEC",
      "ste_examples": ["EXACT STE EXAMPLE 1", "EXACT STE EXAMPLE 2"],
      "non_ste_examples": ["EXACT NON-STE EXAMPLE 1", "EXACT NON-STE EXAMPLE 2"],
      "explanatory_notes": "EXACT EXPLANATORY TEXT"
    }
  ],
  "categories": [
    {
      "category_number": 1,
      "category_name": "EXACT CATEGORY NAME",
      "description": "EXACT DESCRIPTION",
      "examples": ["example1", "example2"]
    }
  ],
  "dictionary_entries": [
    {
      "word": "WORD",
      "approved": true,
      "part_of_speech": "v",
      "approved_meaning": "EXACT MEANING",
      "approved_forms": ["FORM1", "FORM2"],
      "alternatives": []
    }
  ],
  "synonyms": [
    {
      "canonical": "CANONICAL FORM",
      "rejected": ["synonym1", "synonym2"],
      "concept": "WHAT THE CONCEPT IS"
    }
  ],
  "polysemy": [
    {
      "word": "WORD",
      "approved_meaning": "THE ONE APPROVED MEANING",
      "rejected_meanings": [
        {"sense": "rejected sense 1", "use_instead": "ALTERNATIVE WORD"},
        {"sense": "rejected sense 2", "use_instead": "ALTERNATIVE WORD"}
      ]
    }
  ],
  "pipeline_steps": [
    {
      "pass_number": 1,
      "name": "EXACT PASS NAME",
      "description": "EXACT DESCRIPTION",
      "actions": ["action 1", "action 2"]
    }
  ],
  "evolution_history": [
    {
      "issue": "Issue 1",
      "year": 1986,
      "key_changes": ["change 1", "change 2"]
    }
  ]
}
```

### Worker Prompt Template

For each worker, construct the prompt EXACTLY as follows (replace `<<PLACEHOLDERS>>`):

```
You are a spec extraction worker. Extract ONLY — do not adapt, summarize, or rewrite.

READ these files sequentially:
  spec/issue-09-2025/page-<<START_PAGE>>.md through page-<<END_PAGE>>.md

EXTRACT: <<TASK_DESCRIPTION>>

OUTPUT: Write ONLY valid JSON to ste-code/extracted/w<<N>>.json
Use the schema below. Every field must contain EXACT text from the spec pages.
If a page has no content matching a key, use an empty array [].

{
  "worker_id": "W<<N>>",
  "source_pages": "<<START_PAGE>>-<<END_PAGE>>",
  "pages_actually_read": <<PAGE_COUNT>>,
  "rules": [ ... rule objects with EXACT rule_number, rule_text, ste_examples, non_ste_examples, explanatory_notes ... ],
  "categories": [ ... category objects ... ],
  "dictionary_entries": [ ... entry objects ... ],
  "synonyms": [ ... synonym objects ... ],
  "polysemy": [ ... polysemy objects ... ],
  "pipeline_steps": [ ... step objects ... ],
  "evolution_history": [ ... issue objects ... ]
}

RULES:
1. Extract EXACT text. Do not paraphrase. Do not summarize.
2. Include ALL example pairs — every STE example AND its non-STE counterpart.
3. For dictionary entries, include every field: word, approved boolean, POS, meaning, forms, alternatives.
4. If you cannot finish all pages, update "pages_actually_read" to the actual count.
5. Write ONLY the JSON. No markdown fences, no explanations, no preamble, no postscript.
6. Verify the JSON is valid before writing.
```

### Worker Launch Protocol (Batch of 3)

**DO NOT launch more than 3 workers at once.** After each batch, verify the JSON files exist and are valid before launching the next batch.

**Batch 1 — Launch:**
```bash
hermes -z --model deepseek-v4-pro "<W1_PROMPT>" &
hermes -z --model deepseek-v4-pro "<W2_PROMPT>" &
hermes -z --model deepseek-v4-pro "<W3_PROMPT>" &
```

**Batch 1 — Verify (after workers complete):**
```bash
# Check files exist
test -f ste-code/extracted/w1.json && echo "W1 OK" || echo "W1 MISSING — RE-LAUNCH"
test -f ste-code/extracted/w2.json && echo "W2 OK" || echo "W2 MISSING — RE-LAUNCH"
test -f ste-code/extracted/w3.json && echo "W3 OK" || echo "W3 MISSING — RE-LAUNCH"

# Validate JSON
python3 -c "import json; json.load(open('ste-code/extracted/w1.json')); print('W1 valid')"
python3 -c "import json; json.load(open('ste-code/extracted/w2.json')); print('W2 valid')"
python3 -c "import json; json.load(open('ste-code/extracted/w3.json')); print('W3 valid')"

# Check content quality: each file must have actual entries
python3 -c "
import json
for w in ['w1','w2','w3']:
    d = json.load(open(f'ste-code/extracted/{w}.json'))
    rules = len(d.get('rules',[]))
    cats = len(d.get('categories',[]))
    entries = len(d.get('dictionary_entries',[]))
    print(f'{w}: {rules} rules, {cats} categories, {entries} dict entries')
    if rules == 0 and cats == 0 and entries == 0:
        print(f'  WARNING: {w} has zero extracted content — RE-LAUNCH')
"
```

**Update PROGRESS.md** after each verified batch:
```bash
# In .agents/state/PROGRESS.md, change [ ] to [x] for W1, W2, W3
```

**Batch 2 — W4, W5, W6** (launch only after Batch 1 fully verified)
**Batch 3 — W7, W8, W9** (launch only after Batch 2 fully verified)

### Worker Failure Protocol

If ANY worker JSON is missing, has zero content, or fails JSON validation:
1. Mark it `[!] FAILED` in PROGRESS.md
2. Re-launch that specific worker with the SAME prompt
3. If it fails twice, reduce its page range by half and launch two sub-workers
4. Do NOT proceed past GATE 1 until all 9 worker files exist AND contain real content

---

### Quality Gates for Extraction (Measurable Thresholds)

> **CRITICAL:** Binary checks (file exists, JSON parses, non-empty arrays) are necessary but insufficient. Apply these quantitative thresholds to every worker JSON before accepting it.

#### QG1: Rule Completeness

The ASD-STE100 Issue 9 specification defines exactly 53 writing rules (Sections 1-9 plus GR1-GR4). After GATE 2 merge, the master state MUST contain at least **95% of expected rules** (50 of 53). Rules may be split across workers. Count unique `rule_number` values in the merged dataset.

```bash
python3 -c "
import json, os
master = json.load(open('ste-code/extracted/master.json'))
rules = master.get('rules', [])
rule_nums = set(r.get('rule_number') for r in rules if r.get('rule_number'))
total = len(rule_nums)
print(f'Unique rules: {total} / 53 expected')
if total < 50:
    missing = set(f'{s}.{n}' for s in range(1,10) for n in range(1,15)) - rule_nums
    print(f'MISSING RULES: {sorted(missing)}')
    print(f'FAIL: {total}/53 is below the 95% threshold (50/53). Do not proceed.')
    exit(1)
else:
    print(f'PASS: {total}/53 meets the 95% threshold.')
"
```

#### QG2: Dictionary Entry Threshold

The complete dictionary contains approximately 875 approved words plus non-approved alternatives. After GATE 2 merge, the master state MUST contain at least **90% of expected entries** (788 of 875). Count unique `word` values in the `dictionary_entries` array.

```bash
python3 -c "
import json
master = json.load(open('ste-code/extracted/master.json'))
entries = master.get('dictionary_entries', [])
total = len(entries)
approved = sum(1 for e in entries if e.get('approved'))
rejected = sum(1 for e in entries if not e.get('approved'))
print(f'Dictionary entries: {total} total ({approved} approved, {rejected} non-approved)')
if total < 788:
    print(f'FAIL: {total}/875 is below the 90% threshold (788). Do not proceed.')
    exit(1)
print(f'PASS: {total} entries meets the 90% threshold.')
"
```

#### QG3: Category Completeness

The specification defines exactly 19 technical noun categories. After GATE 2 merge, the master state MUST contain **exactly 19 categories**. Fewer than 19 means data loss. More than 19 means duplication. Either is a failure.

```bash
python3 -c "
import json
master = json.load(open('ste-code/extracted/master.json'))
cats = master.get('categories', [])
total = len(cats)
print(f'Categories: {total}')
if total != 19:
    print(f'FAIL: Expected exactly 19 categories, found {total}. Do not proceed.')
    exit(1)
print('PASS: Exactly 19 categories.')
"
```

#### QG4: Example Pair Density

Each rule object MUST contain at least one STE example AND one non-STE example in its `ste_examples` and `non_ste_examples` arrays. Rules with zero examples in either array indicate incomplete extraction.

```bash
python3 -c "
import json
master = json.load(open('ste-code/extracted/master.json'))
rules = master.get('rules', [])
empty_ste = [r['rule_number'] for r in rules if not r.get('ste_examples')]
empty_non = [r['rule_number'] for r in rules if not r.get('non_ste_examples')]
print(f'Rules with zero STE examples: {len(empty_ste)} ({empty_ste})')
print(f'Rules with zero non-STE examples: {len(empty_non)} ({empty_non})')
if empty_ste or empty_non:
    print('FAIL: Rules with zero examples found. Re-extract those pages.')
    exit(1)
print('PASS: All rules have example pairs.')
"
```

#### QG5: Spot-Check Accuracy

Pick 10 random page numbers from 1-434. Read the original markdown page. Find the corresponding content in master.json. Compare character-by-character. If ANY mismatch is found (excluding whitespace normalization), the responsible worker must re-extract.

```bash
python3 -c "
import json, random, os
master = json.load(open('ste-code/extracted/master.json'))
# Pick 10 random pages
pages = sorted(random.sample(range(1, 435), 10))
errors = 0
for p in pages:
    print(f'Spot-check page {p:04d}: ', end='')
    path = f'spec/issue-09-2025/page-{p:04d}.md'
    if not os.path.exists(path):
        print(f'FILE MISSING (cannot verify)')
        errors += 1
    else:
        # Read a slice of the file for comparison
        text = open(path).read()[:500].strip()
        found = False
        for r in master.get('rules', []):
            if text[:50] in r.get('rule_text', '') or r.get('rule_text', '')[:50] in text:
                found = True
                break
        for e in master.get('dictionary_entries', []):
            if e.get('word', '').lower() in text.lower():
                found = True
                break
        if found:
            print('MATCH')
        else:
            print(f'NO MATCH — content from page {p} not found in master')
            errors += 1
if errors > 0:
    print(f'FAIL: {errors}/10 spot-checks failed. Re-extract affected pages.')
    exit(1)
print('PASS: All 10 spot-checks matched.')
"
```

#### Quality Gate Summary

| Gate | Threshold | Fails If | Recovery |
|------|-----------|----------|----------|
| QG1: Rule Completeness | ≥ 50 of 53 rules (95%) | Fewer than 50 unique rule numbers | Identify missing rules, re-launch workers for those page ranges |
| QG2: Dictionary Entries | ≥ 788 of 875 entries (90%) | Fewer than 788 unique dictionary words | Identify which letter ranges are under-extracted, re-launch W6/W7/W8 |
| QG3: Categories | Exactly 19 | Fewer or more than 19 | Re-extract W2-W4 (categories span these workers) |
| QG4: Example Density | 100% of rules have ≥1 STE + ≥1 non-STE example | Any rule has empty example arrays | Re-launch the worker responsible for that rule's page range |
| QG5: Spot-Check Accuracy | 10 of 10 random pages match master | Any page has zero matches in master | Flag the specific worker, re-extract with halved page range |

**Do not proceed past GATE 2 until all five quality gates pass.**

---

## GATE 2: Merge and Validate

**HARD GATE: All 9 worker JSON files must exist, be valid JSON, and contain non-empty extraction data.**
```bash
python3 -c "
import json, os
total_rules = 0
total_entries = 0
for i in range(1,10):
    path = f'ste-code/extracted/w{i}.json'
    if not os.path.exists(path):
        print(f'MISSING: {path} — CANNOT PROCEED')
        exit(1)
    d = json.load(open(path))
    rules = len(d.get('rules',[]))
    entries = len(d.get('dictionary_entries',[]))
    total_rules += rules
    total_entries += entries
    print(f'W{i}: {rules} rules, {entries} dict entries — OK')
print(f'TOTAL: {total_rules} rules, {total_entries} dict entries')
if total_rules < 50:
    print(f'WARNING: Only {total_rules} rules — expected ~53. Some may be missing.')
if total_entries < 500:
    print(f'WARNING: Only {total_entries} dict entries — expected ~875+.')
"
```

**If the gate fails, do not proceed. Fix missing workers first.**

### Merge into Master State

Read all 9 worker JSONs. Merge into `ste-code/extracted/master.json`:
- Deduplicate rules by rule_number
- Sort rules by section (1.1, 1.2, ..., 9.4, GR1-GR4)
- Merge categories (should total exactly 19)
- Merge dictionary entries, deduplicating by word
- Merge synonyms and polysemy entries

### Spot-Check Validation

Pick 10 random page numbers from 1-434. For each:
1. Read the original markdown page directly
2. Find the rule/dictionary entry in your master state
3. Verify the text matches EXACTLY

If ANY mismatch found, flag the worker responsible and re-extract those pages.

---

## GATE 3: Adaptation (Phase 2 from Original)

**HARD GATE: `ste-code/extracted/master.json` must exist and contain verified data.**

Only NOW do you begin adaptation. For each rule in the master state:

### Adaptation Protocol (PER RULE)

1. Read the rule's exact text from master.json
2. Read the STE and non-STE example pairs
3. Think: "What is the coding-domain equivalent of this constraint?"
4. Write the adapted rule text preserving the original structure
5. Write code-domain example pairs (non-STE-Code → STE-Code)
6. Cross-reference: note which original rule number this maps to

### Category Remapping (ALL 19)

For each of the 19 categories, produce a table entry:

| Original Category | STE-Code Category | Rationale |
|-------------------|-------------------|-----------|
| Exact name from master.json | Code-domain equivalent | 1-sentence justification |

### Synonym Table Adaptation

Take every canonical synonym pair from master.json. For each:
- Keep the original canonical form if it works for code domain
- OR adapt it to a code-domain equivalent
- Document the mapping

---

## GATE 4: Output Artifacts

**HARD GATE: All adaptation checkboxes in PROGRESS.md must be checked `[x]`.**

Only NOW write the output files. Each file MUST reference specific data from master.json.

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
|| STE-Code | NOT | Original STE Mapping |
||...|...|...|

## APPROVED VOCABULARY POLICY
[Adapted from master.json vocabulary architecture]

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
Each section must reference data from master.json.

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

# Verify all files reference master.json data
python3 -c "
import json
master = json.load(open('ste-code/extracted/master.json'))
print(f'Master state: {len(master[\"rules\"])} rules, {len(master[\"dictionary_entries\"])} entries')
print(f'Categories: {len(master[\"categories\"])}')
print('All artifact files must exist in ste-code/artifacts/')
"
```

---

## Phase Flow Summary (with Hard Gates)

```
GATE 0:  Verify spec files exist, create directories, init PROGRESS.md
  ↓ (gate passes: all files confirmed)
GATE 1:  Launch 9 workers in 3 batches, verify JSON output
  ↓ (gate passes: 9 valid JSON files with real content)
GATE 2:  Merge into master.json, spot-check 10 random pages
  ↓ (gate passes: master.json valid, spot-checks pass)
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

**Detection:** A worker JSON that passes validation but contains jumbled rule text (characters from wrong sections, truncated sentences) likely hit a malformed page.

**Mitigation:** Before launching workers, run a syntax check on all 434 pages:

```bash
python3 -c "
import os, re
for i in range(1, 435):
    path = f'spec/issue-09-2025/page-{i:04d}.md'
    if not os.path.exists(path):
        print(f'MISSING: {path}')
        continue
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

If more than 5 pages are malformed, halt extraction and fix the spec source first.

### Limitation 2: Spec Page Count Mismatch

**Problem:** The protocol assumes exactly 434 pages in `spec/issue-09-2025/`. If the directory contains fewer pages (a partial extraction, a truncated download, a version mismatch), workers will read to the end of available files and report `pages_actually_read` lower than assigned.

**Detection:** The GATE 0 file check confirms page-0001.md and page-0434.md exist. But intermediate gaps are not checked. After GATE 1, a worker may report `pages_actually_read: 18` when assigned 30 pages.

**Mitigation:** Run a gap check after GATE 0:

```bash
python3 -c "
import os
gaps = []
for i in range(1, 435):
    path = f'spec/issue-09-2025/page-{i:04d}.md'
    if not os.path.exists(path):
        gaps.append(i)
if gaps:
    print(f'GAPS: Missing {len(gaps)} pages: {gaps[:20]}...')
    print('Extraction may be incomplete. Fill gaps or reduce worker ranges.')
else:
    print('All 434 pages present.')
"
```

### Limitation 3: Context Window Constraints

**Problem:** This protocol was designed for `deepseek-v4-pro` with a 1M token context window. If the target model changes (a smaller model, a different provider), the 30-page worker ranges may exceed the context window. The worker will truncate input silently mid-page, producing incomplete extraction.

**Detection:** Compare `pages_actually_read` against the assigned range for each worker. A discrepancy of more than 2 pages is suspicious.

**Mitigation:** If the model has a smaller context window, use the 4-page-per-worker strategy defined in `.agents/references/granular-strategy.md` (109 workers instead of 9). The 9-worker layout in this protocol is the "coarse" version for models with large context windows.

### Limitation 4: Model Unavailability

**Problem:** If `deepseek-v4-pro` is unavailable (API outage, rate limit, credential expiry), all 9 workers will fail simultaneously. There is no fallback model specified in this protocol.

**Detection:** Batch 1 workers all fail with HTTP 429 or 503 errors. No JSON files are written.

**Mitigation:**
1. Check provider status.
2. Wait for the rate limit window to reset.
3. If the outage persists beyond 30 minutes, switch to an alternative model with comparable context window. Update all `--model` flags in the launch commands.
4. Document the model switch in the version history table.

### Limitation 5: Inter-Worker Boundary Errors

**Problem:** W1 covers pages 1-30 and W2 covers pages 31-60. A rule that starts on page 30 and continues on page 31 may be partially extracted by W1 (truncated) and partially by W2 (missing the beginning). The merge step sees two incomplete fragments that do not deduplicate cleanly.

**Detection:** After GATE 2 merge, check for rules with truncated `rule_text` (ends with "..." or a mid-sentence fragment) or rules appearing in two workers with different `rule_number` values but overlapping content.

**Mitigation:** Overlap worker page ranges by 1 page. W1: pages 1-30, W2: pages 30-60, W3: pages 60-90, etc. The 1-page overlap ensures boundary rules appear in both workers. In the merge step, deduplicate by comparing the first 100 characters of `rule_text`.

### Limitation 6: Dictionary Entry Drift Across Issues

**Problem:** The protocol references ASD-STE100 Issue 9 (January 2025) and also checks for `spec/issue-07-2017/page-0001.md` in GATE 0. If Issue 7 has different dictionary entries than Issue 9, workers may inadvertently mix data from two versions.

**Detection:** Compare `evolution_history` arrays in W9 (which should document changes from Issue 1 through 9) against the actual dictionary entries in W6-W8. If W6 contains a word that W9 claims was removed in Issue 5, there is a cross-issue contamination.

**Mitigation:** Use Issue 9 as the authoritative source. The Issue 7 file check in GATE 0 exists for reference only. Workers MUST extract from `spec/issue-09-2025/` and MUST NOT read from `spec/issue-07-2017/` unless the task description explicitly requires historical comparison.

### Limitation 7: Concurrent Write Collisions

**Problem:** If two instances of this protocol run simultaneously (two separate `hermes` sessions both following this document), they will write to the same `ste-code/workers/` and `ste-code/extracted/` directories. One session may overwrite the other's worker output.

**Detection:** Worker JSON files change unexpectedly between verification and merge. The `extraction_timestamp` field in worker JSON does not match the expected launch time.

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
3. If the model is available but all prompts return empty JSON, the prompt template may contain an error. Check for unescaped characters, mismatched quotes, or schema validation failures in the worker prompt.
4. Re-launch the batch after fixing the root cause.

### Recovery Path: Merge Failure (master.json is invalid)

1. Check which worker JSON file introduced the corruption. Validate each file individually.
2. Re-extract the corrupted worker.
3. Re-run the merge.
4. If corruption persists, manually merge the valid worker JSONs and flag the corrupted worker's page range for re-extraction from the raw spec pages.

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

### When to Evolve the Worker JSON Schema

The worker JSON schema may need new fields when:

1. A new section of the spec is discovered that does not fit into existing arrays (`rules`, `categories`, `dictionary_entries`, `synonyms`, `polysemy`, `pipeline_steps`, `evolution_history`).
2. A downstream artifact needs structured data not captured by the current schema (for example, a `cross_references` field linking each rule to the dictionary words it governs).
3. A quality gate requires a new quantitative metric that the current schema does not support (for example, `example_count` per rule, or `page_number` per dictionary entry for traceability).

### Protocol for Adding a Field

1. **Document the need.** Add a row to the version history table explaining what field is needed and why.
2. **Add the field to the schema in this document.** Update the JSON schema block in GATE 1.
3. **Update the worker prompt template.** Add the new field to the prompt template in GATE 1 so workers know to populate it.
4. **Add a quality gate for the new field** in the Quality Gates section (QG6, QG7, etc.).
5. **Mark the change as a BREAKING change** if existing worker JSON files will fail validation against the new schema. If the field is optional (workers can leave it as `[]`), it is backward-compatible.
6. **Re-extract affected pages** if the new field requires data that old worker JSONs do not contain.

### Protocol for Renaming a Field

1. Do NOT rename fields. Add a new field and mark the old one as DEPRECATED in the schema comments.
2. During GATE 2 merge, read from the new field if present, fall back to the old field if absent.
3. After all 9 workers use the new field (proven by running the full pipeline at least once), remove the DEPRECATED field from the schema.

### Protocol for Removing a Field

1. Mark the field as DEPRECATED in the schema for one full pipeline run.
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
| Model: deepseek-v4-pro | — | API availability check | GATE 1 (all workers) |
| Bash | 3.2+ | `bash --version` | GATE 0 (init scripts) |
| Disk space | 500 MB free | `df -h .` | GATE 1 (worker JSON storage) |
| Spec files | ASD-STE100 Issue 9, 434 pages | `ls spec/issue-09-2025/page-0001.md` | GATE 0 |

### Pre-Flight Environment Check

Run this before GATE 0 to verify all dependencies:

```bash
echo "=== Environment Check ==="
python3 --version || { echo "FAIL: Python 3 not found"; exit 1; }
echo "Python: OK"

hermes --version 2>/dev/null || { echo "WARN: hermes not in PATH (check ~/.hermes/bin)"; }
echo "Hermes: OK"

df -h . | tail -1 | awk '{print "Disk: " $4 " free"}'

test -f spec/issue-09-2025/page-0001.md && echo "Spec: OK" || { echo "FAIL: Spec files missing"; exit 1; }

echo "=== All checks passed ==="
```

---

## Timing Budget Estimates

Total pipeline wall-clock time under ideal conditions: **approximately 52 minutes.**

| Phase | Task | Est. Time | Parallelism | Notes |
|-------|------|-----------|-------------|-------|
| GATE 0 | Environment setup | 30 sec | Serial | File checks + directory creation |
| GATE 1 | Batch 1 (W1-W3) | 8-12 min | 3 parallel workers | Each worker reads 30 pages, extracts JSON |
| GATE 1 | Batch 1 verification | 1 min | Serial | JSON validation + quality checks |
| GATE 1 | Batch 2 (W4-W6) | 8-12 min | 3 parallel workers | Same page ranges |
| GATE 1 | Batch 2 verification | 1 min | Serial | JSON validation |
| GATE 1 | Batch 3 (W7-W9) | 8-12 min | 3 parallel workers | Final batch |
| GATE 1 | Batch 3 verification | 1 min | Serial | JSON validation |
| GATE 2 | Merge + spot-check | 3-5 min | Serial | Read 9 files, merge, validate 10 pages |
| GATE 2 | Quality gate scripts | 2 min | Serial | QG1-QG5 automated checks |
| GATE 3 | Rule adaptation (53 rules) | 5-8 min | Serial | One agent adapts all rules sequentially |
| GATE 3 | Category + synonym remapping | 2 min | Serial | Table generation |
| GATE 4 | Write 6 artifacts | 3-5 min | Serial | File writes + final verification |
| **Total** | | **~42-62 min** | | Variance depends on model response time |

NOTE: These estimates assume the model API is responsive and no worker failures occur. Add 10-15 minutes per failed worker that requires re-launch. A full batch failure (model outage) adds 30+ minutes.

---

## Decision Consequences

### If You Skip GATE 0

- PROGRESS.md does not exist. You cannot track which workers have completed.
- Output directories are missing. Worker JSONs fail to write with "No such file or directory."
- Spec files are not verified. Workers may run against missing pages and produce empty JSONs silently.

### If You Skip GATE 1 Verification

- Malformed JSON passes to GATE 2. The merge script crashes.
- Zero-content worker JSONs are accepted. The master state is incomplete.
- The pipeline appears to succeed but produces artifacts with missing data.

### If You Skip GATE 2 Quality Gates

- The master state has 42 rules instead of 53. Artifacts are incomplete.
- The master state has 600 dictionary entries instead of 875. Approved word lists are incorrect.
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
| **Worker** | A single `hermes -z` session that reads a range of spec pages and writes a JSON output file. Workers are stateless. They do not communicate with each other. |
| **Batch** | A group of up to 3 workers launched simultaneously. Batches are serialized: Batch 2 does not start until Batch 1 is verified. |
| **Gate** | A hard checkpoint in the pipeline. Progress past a gate is impossible until its conditions are met. Gates enforce sequential execution and prevent data fabrication. |
| **Master State** | The merged, deduplicated JSON file (`master.json`) that combines all 9 worker outputs into a single authoritative data structure. All adaptation and artifact generation reads from master state. |
| **Adaptation** | The process of transforming aerospace-domain STE rules into code-domain STE-Code rules. This is NOT summarization. Every adapted rule preserves the original structure and intent. |
| **Artifact** | One of 6 output files written in GATE 4. Artifacts are deployable documents (system prompts, manuals, guides) that can be used independently of this pipeline. |
| **Quality Gate** | A quantitative threshold that must be met before proceeding. Unlike binary gates (file exists), quality gates measure completeness (95% of rules present, 90% of dictionary entries). |
| **Fabrication** | Writing data into an output file that does not come from a worker JSON or the original spec. The anti-fabrication rules at the top of this document prohibit this under all circumstances. |
| **Spot-Check** | Reading a random spec page directly and comparing its content against the merged master state. A single mismatch is a failure. |
| **PROGRESS.md** | The state-tracking file at `.agents/state/PROGRESS.md`. Every completed step in the pipeline updates this file. It is the single source of truth for pipeline progress. |

---

## Document Metadata

- **Protocol version:** 1.4
- **Last updated:** 2025-07-30
- **Applies to:** ASD-STE100 Issue 9 (January 2025)
- **Target model:** deepseek-v4-pro
- **Framework:** Hermes Agent v0.19.0+
- **Total spec pages:** 434
- **Expected output:** 6 artifacts in `ste-code/artifacts/`
- **Estimated total runtime:** 42-62 minutes (ideal conditions)
