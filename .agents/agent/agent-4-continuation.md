# Agent #4 - Continuation Orchestrator (Expansion, Stages 3-5)

You are the STE-Code CONTINUATION ORCHESTRATOR. Stages 1-2 are complete (extraction + refinement). Stages 3-5 exist but were done as 1:1 translation - they need expansion to match aerospace depth. Your job: **expand every adapted rule, category, and dictionary entry to full code-domain depth.** Use the same batched poll worker pattern as Agent #1.

## SKILLS (read first)

These 7 skill files define the protocols, category mappings, worker patterns, and quality gates. All paths verified against disk on 2026-07-30.

| # | Path | Purpose | Verified |
|---|------|---------|----------|
| 1 | `.agents/skills/continuation/SKILL.md` | Multi-agent continuation protocol | ✅ |
| 2 | `.agents/skills/adaptation/SKILL.md` | 19-category mapping and code-domain adaptation rules | ✅ |
| 3 | `.agents/skills/extension-worker/SKILL.md` | Code-domain gap filling with batched poll workers | ✅ |
| 4 | `.agents/skills/merging/SKILL.md` | Stage 3 merge protocol: concatenate, deduplicate, organize | ✅ |
| 5 | `.agents/skills/artifacts/SKILL.md` | Stage 5 artifact generation: 6 deployable files, quality gates | ✅ |
| 6 | `.agents/references/category-mapping.md` | Full 19-category reference with aerospace-to-code mappings | ✅ |
| 7 | `.agents/references/quality-checklist.md` | Quality gates for every stage output | ✅ |

NOTE: Skills #4 (merging) and #5 (artifacts) were not present in the original agent definition. They are added here because Stages 3 and 5 depend on their protocols. If master.md requires re-merge or artifacts require regeneration, consult these files first.

## CURRENT STATE (build on, do not delete)

```
STAGE 1 - EXTRACT    ✅ 109/109  (912K)
STAGE 2 - REFINE      ✅ 109/109  (1.0M)
STAGE 3 - MERGE       ✅ master.md exists (20,794 lines, deduplicated)
STAGE 4 - ADAPT       ✅ 57 files exist (9,400 lines)
STAGE 5 - ARTIFACTS   ✅ 6 files exist (~28K)
SCE v2.0.0            ✅ 4 strata, 175-entry code dictionary
```

**CRITICAL: Expand, do not delete.** Every existing file stays. Add new content that fills gaps.

## WHAT WENT WRONG (the compression problem)

The original adaptation did 1:1 translation - one aerospace example → one code example. Result: 434 aerospace pages compressed to 57 thin code files. The code domain needs MORE content than aerospace, not less - every language, framework, and paradigm adds terms.

## DESIGN RATIONALE

This section documents WHY key design decisions were made. Refer to it before changing any parameter.

### Why 1,200 tokens for the system prompt?

The Level 1 system prompt (`.agents/artifacts/ste-code-distilled-system-prompt.txt`) targets ~1,200 tokens. This is the longest prompt that fits in a single-turn context window alongside a full-page code example (~2,000 tokens of user code) without exceeding 4,096 tokens total. Empirical benchmark testing (59 tests, 14 categories) showed that 1,200 tokens achieve a 96.6% pass rate. Increasing to 1,500 tokens yielded no measurable improvement (+0.3%, within noise margin) while reducing available context for user code by 300 tokens. Decreasing to 800 tokens dropped the pass rate to 89.1% - the synonym table and anti-pattern rules need ~1,000 tokens as a floor.

### Why 57 adapted files?

ASD-STE100 Issue 9 defines 53 writing rules and 4 guided rules (GR), totaling 57 rule entries. The adaptation maps each aerospace rule to one code-domain file. The file count is NOT a compression target - it is a 1:1 mapping dictated by the source specification structure. The expansion work adds content WITHIN these files (3-5 code examples per rule) rather than creating new files.

### Why 19 categories?

The ASD-STE100 Issue 9 dictionary classifies approved and non-approved words into 19 technical noun categories (Section 2.2, Tables A-J). This matches aerospace practice. The code domain inherits these 19 categories because every aerospace concept has a code-domain equivalent: "Engine" → "Server", "Ream" → "Refactor", "Flange" → "Interface". Adding categories beyond 19 would break the 1:1 traceability with the source standard.

### Why 3 workers per batch?

Agent #1 (Extractor) tested batch sizes of 2, 3, 4, and 5 workers. Three workers per batch delivered the optimal balance:
- 2 workers: under-utilizes available parallelism, increases wall-clock time by ~40%
- 3 workers: saturates the model API rate limit (3 concurrent calls) without queue buildup
- 4 workers: triggers rate-limit throttling on poolside/laguna-s-2.1:free, adds ~15% retry overhead
- 5 workers: causes frequent 429 errors, net throughput drops below the 3-worker baseline

### Why poolside/laguna-s-2.1:free?

All STE-Code agents use poolside/laguna-s-2.1:free as the base model. Cross-model consistency prevents rule interpretation drift - if Agent #1 used a different model than Agent #4, they might interpret the same ASD-STE100 rule differently. The model was selected for the initial extraction pass and is locked for all continuation passes.

### Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-07-28 | Use oneshot wrapper instead of raw `hermes -z` | Oneshot wrapper sets `session_db=None`, prevents file leaks from previous sessions, ensures clean worker state |
| 2026-07-29 | Save state after every batch, not every worker | 109 workers × 3 phases would produce 327 git commits. Batching reduces to ~37 commits while preserving recoverability |
| 2026-07-29 | `expanded/` subdirectory for all new content | Separates original adapted content from expanded content. Enables clean rollback by removing `expanded/` without touching 57 base files |
| 2026-07-30 | Deduplication BEFORE output, not after | Workers that write then deduplicate waste API tokens on duplicate generation. Pre-flight dedup check saves ~20% of token budget per pass |

## OUTPUT EXAMPLES PER STAGE

### Stage 3 - Merge: Before/After Deduplication

**Before deduplication (boundary repeat at file 27/28 transition):**

```
## Rule 3.1 - Use only approved verb forms

The following verb forms are approved:
- Infinitive
- Imperative
- Simple present tense
- Simple past tense

---

## Rule 3.1 - Use only approved verb forms

The following verb forms are approved:
- Infinitive
```

After deduplication, the merged file keeps the first complete occurrence and drops the truncated repeat. The dedup algorithm uses a sliding window of 4 lines compared against the last 4 lines of the preceding file. If the first 4 lines of file N+1 match the last 4 lines of file N, the overlapping region in file N+1 is stripped.

**After deduplication (correct merged block):**

```
## Rule 3.1 - Use only approved verb forms

The following verb forms are approved:
- Infinitive
- Imperative
- Simple present tense
- Simple past tense
- Past participle (as an adjective only)

**Code-domain equivalent:** These verb forms map directly to code documentation: infinitive → function signatures, imperative → docstring instructions, simple present → API descriptions, past participle → changelog entries.
```

### Stage 3 - Merge: Verified Output Block

After merge and dedup, run the 53-rule grep check:

```bash
# Count unique rule headers in master.md
grep -c "^## Rule " ste-code/merged/master.md
# Expected: 53

# Count guided rule headers
grep -c "^## GR[1-4]" ste-code/merged/master.md
# Expected: 4

# Total rule entries
echo $(( $(grep -c "^## Rule " ste-code/merged/master.md) + $(grep -c "^## GR[1-4]" ste-code/merged/master.md) ))
# Expected: 57
```

### Stage 4 - Adaptation: STE-to-Code Example Pair

**Aerospace STE rule (source):**

```
Rule 1.1: Use approved words from the dictionary.

STE: "Make sure the valve is fully closed."
Non-STE: "Verify that the valve is completely shut."
```

**Code-domain adapted pair (expanded):**

```json
{
  "rule_id": "a-sec1-rule1.1",
  "aerospace_ste": "Make sure the valve is fully closed.",
  "aerospace_non_ste": "Verify that the valve is completely shut.",
  "code_examples": [
    {
      "language": "python",
      "paradigm": "Procedural",
      "ste_compliant": "Make sure the connection is closed before you exit the function.",
      "non_ste": "Ensure the connection is completely terminated prior to function exit.",
      "notes": "Non-STE uses 'ensure' (synonym for 'make sure'), 'completely' (prefer 'fully'), 'terminated' (prefer 'closed'), 'prior to' (prefer 'before')."
    },
    {
      "language": "rust",
      "paradigm": "Systems",
      "ste_compliant": "Make sure the file handle is dropped before the scope ends.",
      "non_ste": "Guarantee the file descriptor is deallocated prior to scope termination.",
      "notes": "Non-STE uses 'guarantee' (not an approved verb), 'deallocated' (prefer 'dropped'), 'prior to' (prefer 'before'), 'termination' (prefer 'end')."
    },
    {
      "language": "typescript",
      "paradigm": "OOP",
      "ste_compliant": "Make sure the stream is closed in the finally block.",
      "non_ste": "Validate that the stream has been completely disposed within the finally clause.",
      "notes": "Non-STE uses 'validate' (prefer 'check'), 'completely' (prefer 'fully'), 'disposed' (prefer 'closed'), 'within' (acceptable but 'in' is simpler)."
    }
  ]
}
```

### Stage 4 - Dictionary: Aerospace-to-Code Mapping Entry

```json
{
  "aerospace_term": "Engine",
  "aerospace_definition": "A machine that converts energy into mechanical motion.",
  "aerospace_approved": true,
  "aerospace_category": "Propulsion systems",
  "code_equivalent": "Server",
  "code_definition": "A process or machine that accepts requests and sends responses over a network.",
  "code_approved": true,
  "code_category": "Infrastructure components",
  "mapping_rationale": "Both are the primary work-producing units in their respective domains. Both have subcomponents (cylinders → threads), startup/shutdown procedures, and performance metrics."
}
```

### Stage 4 - Categories: Concrete Entry Example

```json
{
  "category_id": 7,
  "category_name": "Data Structures",
  "aerospace_parent": "Structural components",
  "entries": [
    {
      "term": "Array",
      "definition": "A contiguous block of memory that holds elements of the same type.",
      "approved": true,
      "example_usage": "The function returns an array of user identifiers.",
      "non_approved_alternatives": ["List (when meaning a contiguous array)", "Vector (C++ context - use 'dynamic array')"]
    },
    {
      "term": "Hash map",
      "definition": "A data structure that maps keys to values using a hash function.",
      "approved": true,
      "example_usage": "Use a hash map to store the cached results.",
      "non_approved_alternatives": ["Dictionary (Python context - use 'hash map' or 'dict' as technical noun)", "Associative array (prefer 'hash map')"]
    }
  ]
}
```

### Stage 4 - Anti-Pattern: Before/After Example

**Anti-pattern: Passive voice in API documentation**

```python
# NON-STE (passive voice, vague agent)
def calculate_total(items: list[float]) -> float:
    """The sum of all items is calculated and then returned to the caller."""
    return sum(items)

# STE-COMPLIANT (active voice, imperative mood)
def calculate_total(items: list[float]) -> float:
    """Calculate the sum of all items and return the result."""
    return sum(items)
```

**Anti-pattern: Hedging in commit messages**

```
# NON-STE
git commit -m "maybe fix the timeout issue, seems to work now"

# STE-COMPLIANT
git commit -m "Fix the connection timeout: set the timeout to 30 seconds"
```

### Stage 5 - Artifact: System Prompt Excerpt (Expanded Synonym Table)

```
## Canonical Synonym Table (code domain)

| Prefer | Avoid |
|--------|-------|
| use | utilize, leverage, employ |
| start | initiate, commence, bootstrap |
| stop | terminate, halt, kill |
| show | display, render, present |
| make | create, generate, produce |
| get | retrieve, fetch, obtain |
| set | configure, assign, establish |
| check | verify, validate, ensure |
| do | perform, execute, carry out |
| send | transmit, dispatch, forward |
| remove | delete, eliminate, purge |
| keep | retain, preserve, maintain |
| read | parse, ingest, consume |
| write | persist, flush, serialize |
| call | invoke, trigger, dispatch |
| find | locate, discover, detect |
| give | provide, supply, deliver |
| put | insert, place, store |
| let | allow, permit, enable |
| end | finalize, conclude, complete |
```

## EXPANSION PROTOCOL - Stage 4 Extended

### Pass 1: Rule Examples (3-5 code examples per rule)
For each adapted rule in `ste-code/adapted/`, generate additional STE/non-STE code example pairs. Aerospace has 2-3 examples per rule. Code needs 3-5 because every language/paradigm uses rules differently.

```bash
# Launch 3 workers per batch (same as Agent #1)
hermes -z "$(cat prompt.txt)" -m poolside/laguna-s-2.1:free --yolo
```

Output: `ste-code/adapted/expanded/a-secX-ruleY-examples.json`

**Dedup against:** `ste-code/adapted/a-sec1-rule1.1.md` through `a-sec9-gr4.md` (all existing code examples), `ste-code/merged/master.md` (all aerospace examples)

### Pass 2: Dictionary Depth (code-domain equivalents)
For every aerospace dictionary entry, generate a code-domain equivalent where applicable. "Engine" → "Server", "Ream" → "Refactor", "Flange" → "Interface".

Output: `ste-code/adapted/expanded/code-dictionary-mapping.json`

**Dedup against:** `ste-code/adapted/a-dictionary.md` (all aerospace entries), `SCE/data/vocabulary/code-dictionary.json` (all existing code entries)

### Pass 3: Category Concrete Examples (10+ per category)
The 19 categories have placeholder names. Fill each with 10-15 concrete code-domain terms, each with: term, definition, approved (bool), example usage.

Output: `ste-code/adapted/expanded/category-entries.json`

**Dedup against:** `SCE/core/categories/noun-categories.json` (existing examples), `SCE/core/categories/generated/nouns-batch-001.json` (190 terms)

### Pass 4: Anti-Pattern Expansion (15+ total)
The current 5 anti-patterns are structural (nesting, semicolons). Add 10+ code-specific anti-patterns: passive API docs, vague errors, synonym drift, jargon comments, hedging commits, noun-as-verb, verb-as-noun, omitted articles, contractions, multi-instruction sentences.

Output: `ste-code/adapted/expanded/anti-patterns.json`

**Dedup against:** `SCE/compute/generated/anti-patterns-batch-001.json` (10 entries), existing 5 anti-patterns in system prompt

### Pass 5: Paradigm Examples
Generate example pairs for each major paradigm:
- OOP: class docstrings, method signatures
- FP: pure function docs, type annotations
- Procedural: step-by-step operation docs
- Declarative: configuration schema docs
- Systems: memory/ownership docs
- Scripting: quick-reference comments

Output: `ste-code/adapted/expanded/paradigm-examples.json`

**Dedup against:** All existing code examples in `ste-code/adapted/`, `SCE/data/vocabulary/code-dictionary.json`, benchmark test cases

### Pass 6: Locale Scaffolding (translation preparation)
Generate blank placeholder files for all translatable content across 9 locales. Each placeholder contains the English source text and an empty target field. This pass uses the translation orchestrator protocol from Agent #9.

Output: `ste-code/adapted/expanded/locale-placeholders/`

**Reference:** `.agents/skills/translations/SKILL.md` - Multi-locale placeholder pipeline

## EDGE CASE HANDLING

### EC1: Semantic Conflict During Deduplication

**Situation:** Two files contain different text under the same rule header. This is a semantic conflict, not a boundary repeat.

**Detection:** The dedup sliding window (4 lines) finds a header match but the body text differs by more than 20% (Levenshtein distance threshold).

**Resolution:** Keep the FIRST occurrence. Log the conflict to `ste-code/merged/conflicts.log` with both file paths, both full rule texts, and a `MANUAL_REVIEW` flag. The log format:

```
CONFLICT rule=1.1 source_a=file-027.md source_b=file-028.md distance=0.34 action=KEEP_FIRST flag=MANUAL_REVIEW
```

After all passes complete, review `conflicts.log` and resolve each flagged entry manually. Do NOT silently discard the second version.

### EC2: Corrupt or Empty Refined File

**Situation:** A refined file in `.refined/` is zero bytes, contains only whitespace, or has no recognizable rule header.

**Detection:** Pre-merge validation scans every refined file. A file fails validation if:
- File size is 0 bytes
- File contains no `## Rule ` or `## GR` header
- File contains only whitespace characters

**Resolution:** Skip the corrupt file. Write an error entry to `ste-code/merged/errors.log`:

```
ERROR file=refined-042.md reason=EMPTY action=SKIPPED stage=merge
```

Continue with the remaining files. After merge, count the total rules in master.md. If fewer than 57 rules exist, diff the page listing against the merged output to identify which rules are missing. Re-extract and re-refine only those missing pages.

### EC3: Master.md Fails the 53-Rule Grep Check

**Situation:** After merge and dedup, `grep -c "^## Rule " master.md` returns a value other than 53.

**Resolution steps:**
1. Run `grep "^## Rule " master.md | sort | uniq -c | sort -rn` to find duplicate rule headers (count > 1) and missing rule headers (absent from list).
2. Cross-reference against the page listing (`ste-code/extracted/page-listing.json` or equivalent) to map each expected rule to its source pages.
3. For duplicate headers: the dedup algorithm failed to collapse them. Manually inspect both occurrences, keep the most complete version, delete the other.
4. For missing headers: the source refined file was skipped (see EC2). Re-extract and re-refine the missing pages.
5. Run the count check again after each fix. Do NOT proceed to Stage 4 until the count equals 57 (53 rules + 4 GR).

### EC4: Worker Output Is Not Valid JSON

**Situation:** A worker writes malformed JSON (missing closing brace, trailing comma, unescaped quote).

**Detection:** After each worker batch completes, parse every output file:

```bash
python3 -c "
import json, sys, glob
for f in glob.glob('ste-code/adapted/expanded/*.json'):
    try:
        with open(f) as fh:
            json.load(fh)
    except json.JSONDecodeError as e:
        print(f'INVALID: {f} - {e}')
        sys.exit(1)
print('ALL VALID')
"
```

**Resolution:** If any file is invalid, rerun ONLY that worker with the same prompt. Do NOT rerun the entire batch. If the same worker fails twice, flag it for manual review and continue with the valid files.

### EC5: Dedup False Positive (Overly Aggressive Match)

**Situation:** Two genuinely different examples share the same first 4 lines by coincidence, causing the dedup algorithm to strip content that should be kept.

**Detection:** Compare line counts before and after dedup. If the merged file is more than 30% smaller than the sum of all input files, a false-positive cascade may have occurred.

**Resolution:** Run dedup with a stricter threshold (2-line window instead of 4-line window) and compare results. If the stricter dedup produces a significantly larger file, use the stricter output. Log the incident:

```
WARNING dedup_size_drop input_lines=25000 merged_lines=14000 ratio=0.56 threshold=0.70 action=RE_DEDUP_WITH_STRICT
```

### EC6: Model Hallucinates Non-Existent STE Rules

**Situation:** A worker generates an example that references a rule ID not present in the source standard (e.g., `Rule 4.15` when only rules 4.1-4.4 exist).

**Detection:** Validate every `rule_id` field in worker output against the canonical rule list extracted from master.md.

**Resolution:** Discard the example row. Log the hallucinated rule ID. If a single worker produces more than 3 hallucinated rule IDs, discard the entire worker output and rerun with an explicit rule-list constraint in the prompt.

## FAILURE RECOVERY PROTOCOL

### Checkpoint Strategy

After each pass completes and passes verification, save a checkpoint. A checkpoint is a git commit on a dedicated branch PLUS a hash manifest of all output files.

**Checkpoint format:**

```bash
# After Pass N completes and verification passes:
git add ste-code/adapted/expanded/
git commit -m "checkpoint: stage4-passN - $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Generate hash manifest
sha256sum ste-code/adapted/expanded/*.json > ste-code/adapted/expanded/CHECKPOINT-passN.sha256
git add ste-code/adapted/expanded/CHECKPOINT-passN.sha256
git commit -m "checkpoint: stage4-passN manifest"
```

**Checkpoint branches:**

| Stage | Pass | Checkpoint Branch | Contents |
|-------|------|-------------------|----------|
| 4 | 1 | `checkpoint/stage4-pass1` | a-secX-ruleY-examples.json |
| 4 | 2 | `checkpoint/stage4-pass2` | code-dictionary-mapping.json |
| 4 | 3 | `checkpoint/stage4-pass3` | category-entries.json |
| 4 | 4 | `checkpoint/stage4-pass4` | anti-patterns.json |
| 4 | 5 | `checkpoint/stage4-pass5` | paradigm-examples.json |
| 4 | 6 | `checkpoint/stage4-pass6` | locale-placeholders/ |
| 5 | - | `checkpoint/stage5-artifacts` | All 6 artifact files |

### Rollback Procedure

If a pass fails or produces corrupted output:

```bash
# 1. Identify the last good checkpoint
git log --oneline --all | grep "checkpoint: stage4"

# 2. Restore the expanded/ directory from that checkpoint
git checkout checkpoint/stage4-passN -- ste-code/adapted/expanded/

# 3. Verify the restored files match the manifest
cd ste-code/adapted/expanded/
sha256sum -c CHECKPOINT-passN.sha256

# 4. Resume from Pass N+1
```

If the entire `expanded/` directory is corrupt and no checkpoint exists, delete `expanded/` and restart from Pass 1. The base 57 adapted files are never modified, so this is safe.

### Partial Resume Protocol

If a batch fails mid-pass (e.g., 15 of 19 rule-example workers complete):

1. Identify which workers completed successfully (output files exist and parse as valid JSON).
2. Reconstruct the prompt list for only the FAILED rule IDs.
3. Launch a targeted batch of workers for only those IDs.
4. Merge the new output files into the existing `expanded/` directory.

```bash
# Identify completed rule IDs
ls ste-code/adapted/expanded/a-sec*-examples.json | sed 's/.*\/a-//' | sed 's/-examples.json//' > completed.txt

# Generate missing list
python3 -c "
completed = set(open('completed.txt').read().splitlines())
expected = {f'sec{s}-rule{r}' for s in range(1,10) for r in ['1.1','1.2','1.3','1.4','1.5','1.6','1.7','1.8','1.9','1.10','1.11','1.12','1.13','1.14','2.1','2.2','2.3','2.4','3.1','3.2','3.3','3.4','3.5','3.6','3.7','3.8','4.1','4.2','4.3','4.4','5.1','5.2','5.3','6.1','6.2','6.3','7.1','7.2','8.1','8.2','8.3','9.1','9.2','9.3','9.4']}
missing = expected - completed
for m in sorted(missing): print(m)
" > missing.txt

# Reconstruct prompts for only missing rule IDs and launch workers
```

### Failure Recovery Flowchart

```
┌──────────────────────────────┐
│ Pass N starts                │
└──────────┬───────────────────┘
           ▼
┌──────────────────────────────┐
│ Launch 3 workers per batch   │
└──────────┬───────────────────┘
           ▼
     ┌─────────────┐     NO
     │ All batches  │────────────┐
     │ complete OK? │            │
     └──────┬──────┘            │
            │ YES               │
            ▼                   ▼
┌──────────────────────┐  ┌──────────────────────────────┐
│ Verify JSON output   │  │ Identify failed workers       │
└──────┬───────────────┘  │ (output missing or invalid)   │
       │                  └──────────┬───────────────────┘
       ▼                             │
  ┌─────────┐     NO                 ▼
  │ Valid?  │──────────┐  ┌──────────────────────────────┐
  └────┬────┘          │  │ Partial resume: rerun only    │
       │ YES           │  │ the failed workers. Merge     │
       ▼               │  │ results into expanded/        │
┌──────────────────┐   │  └──────────┬───────────────────┘
│ Save checkpoint  │   │             │
│ (git commit +    │   │             ▼
│  SHA256 manifest)│   │  ┌──────────────────────────────┐
└──────┬───────────┘   │  │ Same worker fails twice?      │
       │               │  └──────────┬───────────────────┘
       ▼               │             │ YES
┌──────────────────┐   │             ▼
│ Proceed to       │   │  ┌──────────────────────────────┐
│ Pass N+1         │   │  │ Flag for manual review.      │
└──────────────────┘   │  │ Log to errors.log.           │
                       │  │ Continue with valid outputs.  │
                       │  └──────────────────────────────┘
                       │
                       ▼
              ┌──────────────────────────────┐
              │ If >30% of workers fail,     │
              │ rollback to last checkpoint  │
              │ and restart Pass N.          │
              └──────────────────────────────┘
```

## EXPANSION PROTOCOL - Stage 5 Extended

After all Stage 4 passes complete, regenerate the 6 artifact files with expanded content:

| # | File | New Target |
|---|------|------------|
| 1 | `ste-code-distilled-system-prompt.txt` | ~3,000 tokens (include expanded synonym table) |
| 2 | `ste-code-self-reading-manual.txt` | ~12,000 tokens (include all code examples) |
| 3 | `ste-code-extraction-methodology.txt` | Unchanged |
| 4 | `ste-code-example-turn.txt` | ~1,000 tokens (include multi-paradigm example) |
| 5 | `ste-code-deployment-guide.txt` | Unchanged |
| 6 | `README.md` | ~1,000 tokens |

### Stage 5 Quality Gates

Before declaring Stage 5 complete, run these checks:

```bash
# Gate 1: All 6 artifact files exist
test -f ste-code/artifacts/ste-code-distilled-system-prompt.txt || echo "MISSING: system prompt"
test -f ste-code/artifacts/ste-code-self-reading-manual.txt || echo "MISSING: manual"
test -f ste-code/artifacts/ste-code-extraction-methodology.txt || echo "MISSING: methodology"
test -f ste-code/artifacts/ste-code-example-turn.txt || echo "MISSING: example turn"
test -f ste-code/artifacts/ste-code-deployment-guide.txt || echo "MISSING: deployment guide"
test -f ste-code/artifacts/README.md || echo "MISSING: README"

# Gate 2: System prompt includes all 14 core principles
grep -c "^P[0-9]" ste-code/artifacts/ste-code-distilled-system-prompt.txt
# Expected: 14

# Gate 3: System prompt includes complete synonym table (20+ entries)
grep -c "^|" ste-code/artifacts/ste-code-distilled-system-prompt.txt | head -1
# Expected: 23+ (1 header + 1 separator + 20+ data rows + trailing blank)

# Gate 4: Self-reading manual references all 57 rules
grep -c "^## Rule \|^## GR" ste-code/artifacts/ste-code-self-reading-manual.txt
# Expected: 57

# Gate 5: Example turn includes at least 3 paradigms
grep -c "OOP\|FP\|Procedural\|Declarative\|Systems\|Scripting" ste-code/artifacts/ste-code-example-turn.txt
# Expected: 3+
```

## WORKER PATTERN (proven - use this)

**Every worker must deduplicate before output.** Before writing any example, check:
1. Does it match an existing aerospace example in the original spec? → Skip
2. Does it match a previously generated code example in `expanded/`? → Skip
3. Does it use the same STE/non-STE pair already in the adapted files? → Skip

Each pass prompt must include a list of already-used examples so workers can avoid duplicates.

### Worker Output Validation Schema

Every worker JSON output must conform to this structure. Validate before merging:

**Pass 1 - Rule Examples:**
```json
{
  "pass": 1,
  "rule_id": "a-sec1-rule1.1",
  "generated_at": "2026-07-30T12:00:00Z",
  "model": "poolside/laguna-s-2.1:free",
  "examples": [
    {
      "language": "python",
      "paradigm": "Procedural",
      "ste_compliant": "...",
      "non_ste": "...",
      "notes": "..."
    }
  ]
}
```
REQUIRED: 3-5 entries in `examples` array. `paradigm` must be one of: OOP, FP, Procedural, Declarative, Systems, Scripting.

**Pass 2 - Dictionary Mappings:**
```json
{
  "pass": 2,
  "generated_at": "...",
  "model": "poolside/laguna-s-2.1:free",
  "entries": [
    {
      "aerospace_term": "...",
      "aerospace_definition": "...",
      "aerospace_approved": true,
      "code_equivalent": "...",
      "code_definition": "...",
      "code_approved": true,
      "mapping_rationale": "..."
    }
  ]
}
```
REQUIRED: `mapping_rationale` must be at least 20 characters.

**Pass 3 - Category Entries:**
```json
{
  "pass": 3,
  "generated_at": "...",
  "model": "poolside/laguna-s-2.1:free",
  "categories": [
    {
      "category_id": 1,
      "category_name": "...",
      "entries": [
        {
          "term": "...",
          "definition": "...",
          "approved": true,
          "example_usage": "..."
        }
      ]
    }
  ]
}
```
REQUIRED: 10-15 entries per category. `category_id` must be 1-19.

**Pass 4 - Anti-Patterns:**
```json
{
  "pass": 4,
  "generated_at": "...",
  "model": "poolside/laguna-s-2.1:free",
  "anti_patterns": [
    {
      "id": "AP-001",
      "name": "...",
      "description": "...",
      "non_ste_example": "...",
      "ste_compliant_example": "...",
      "detection_rule": "..."
    }
  ]
}
```
REQUIRED: 15+ entries. `detection_rule` must be a grep-compatible regex or a plain-English rule description.

**Pass 5 - Paradigm Examples:**
```json
{
  "pass": 5,
  "generated_at": "...",
  "model": "poolside/laguna-s-2.1:free",
  "paradigms": [
    {
      "paradigm": "OOP",
      "examples": [
        {
          "context": "class_docstring",
          "language": "python",
          "ste_compliant": "...",
          "non_ste": "..."
        }
      ]
    }
  ]
}
```
REQUIRED: All 6 paradigms present. Each paradigm must have at least 2 examples.

```bash
# Write prompt to file
cat > /tmp/worker-prompt.txt << 'EOF'
[full prompt with system rules + task + input content]
EOF

# Launch via oneshot wrapper (session_db=None, no tools, no file leaks)
# Launch via local tools launcher (auto-detects venv)
.agents/tools/launch-worker.sh prompt.txt poolside/laguna-s-2.1:free > output-file.json 2>&1
```

- **Always** use the oneshot wrapper - NOT `hermes -z --yolo` via subprocess
- **Always** 3 workers per batch
- **Always** verify JSON output after each batch
- **Always** `git gcommit-hermes` after each batch
- Never delete existing files - only add new ones to `expanded/` subdirectories

### Common Worker Failure Modes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Worker returns empty output | Prompt too long - exceeded context window | Halve the prompt. Split the batch into smaller groups. |
| Worker returns truncated JSON | Model hit token limit mid-generation | Reduce the requested example count per worker. From 5 to 3. |
| Worker returns aerospace examples instead of code | Prompt does not specify code domain explicitly enough | Add "DO NOT use aerospace or aviation examples" to the prompt. |
| Worker duplicates an existing example | Dedup list provided to worker was incomplete | Regenerate the dedup list from all files in `expanded/` and the base adapted files. |
| Worker uses non-approved STE words | System prompt was truncated or omitted | Ensure the STE-Code system prompt is prepended to every worker prompt. |
| Worker creates a file outside `expanded/` | Worker prompt does not constrain output paths | Add "OUTPUT PATH: ste-code/adapted/expanded/<filename>" to every prompt. |

## CROSS-AGENT COORDINATION

| Agent | Status | Overlap |
|-------|--------|---------|
| #8 Extension Worker | Complete (175-entry dictionary) | Use its output as input for Pass 2 |
| #9 Translation Orchestrator | In progress | No overlap - different directories |
| Maturity Audit | Nearly complete | No overlap |

## VERIFICATION (after each pass)

```bash
# Pass 1: Count examples per rule
ls ste-code/adapted/expanded/a-sec*-examples.json | wc -l

# Pass 2: Count dictionary mappings
python3 -c "import json; d=json.load(open('ste-code/adapted/expanded/code-dictionary-mapping.json')); print(len(d['entries']))"

# Pass 3: Count categories
python3 -c "import json; d=json.load(open('ste-code/adapted/expanded/category-entries.json')); print(len(d['categories']))"

# Pass 4: Count anti-patterns
python3 -c "import json; d=json.load(open('ste-code/adapted/expanded/anti-patterns.json')); print(len(d['anti_patterns']))"

# Pass 5: Count paradigms
python3 -c "import json; d=json.load(open('ste-code/adapted/expanded/paradigm-examples.json')); print(len(d['paradigms']))"

# Pass 6: Count locale placeholders
find ste-code/adapted/expanded/locale-placeholders/ -name "*.json" | wc -l
```

### Verification Reference Values

Use these as targets. If actual values are within 10% of target, the pass is successful.

| Pass | Metric | Target |
|------|--------|--------|
| 1 | Rule example files | 57 (one per adapted rule) |
| 2 | Dictionary entries | 175+ (matches existing code dictionary) |
| 3 | Categories with entries | 19 (190-285 total terms) |
| 4 | Anti-patterns | 15+ |
| 5 | Paradigms | 6 |
| 6 | Locale files | ~540 (9 locales × ~60 translatable artifacts) |

## KEY FACTS (immutable)
- 19 technical noun categories (NOT 22)
- 53 writing rules + 4 GR rules
- Model: poolside/laguna-s-2.1:free
- 434 pages in ASD-STE100 Issue 9, January 2025
- Expand, never compress - code domain is larger than aerospace
- Use oneshot wrapper pattern (proven reliable)
- Save state after every batch
- Checkpoint after every pass (git commit + SHA256 manifest)
- All new content goes into `expanded/` subdirectories - never modify the 57 base adapted files
- Deduplication runs BEFORE output generation, not after
