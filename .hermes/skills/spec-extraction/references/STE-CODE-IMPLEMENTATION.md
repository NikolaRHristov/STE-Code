# STE-Code: Simplified Technical English for Code — Implementation Protocol

> **CRITICAL: Anti-Fabrication Rules — READ BEFORE ANY ACTION**
>
> 1. You MUST NOT write any output file until its prerequisite worker JSON exists on disk.
> 2. Every phase has a HARD GATE — a file-existence check. Do not proceed past a gate.
> 3. If a worker fails, re-launch it. Do not fabricate its data.
> 4. All STE-Code content MUST cross-reference a worker JSON entry. No spec data = no output.
> 5. Track progress in `ste-code/PROGRESS.md` — update it after EVERY completed step.

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
cat > ste-code/PROGRESS.md << 'TRACKER'
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

**DO NOT proceed past GATE 0 until `ste-code/PROGRESS.md` exists and all spec paths are confirmed readable.**

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
# In ste-code/PROGRESS.md, change [ ] to [x] for W1, W2, W3
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
| STE-Code | NOT | Original STE Mapping |
|...|...|...|

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
