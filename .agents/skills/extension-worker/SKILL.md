---
description: "Generate code-domain placeholder entries for STE-Code gaps using batched poll workers. Dictionary, categories, anti-patterns, domain extensions."
version: "2.0.0"
related: [".agents/agent/agent-8-extension-worker.md", "SCE/core/categories/synonym-table.json", "SCE/data/vocabulary/approved-verbs.json"]
---

# Extension Worker Orchestration — Agent-Agnostic

> **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
> Session isolation + STRICT_RULES (R1-R6) from `lib/pipeline_core.py` apply to THIS skill.
> One session = one operation = one read + one write. No re-editing own output.

Generate code-domain extensions to fill gaps between aerospace ASD-STE100 and the code documentation domain. Uses the same batched poll worker pattern as Agent #1 (Extractor).

## Gap Areas

| # | Area | Target Count | Current | Gap |
|---|------|:---:|:---:|:---:|
| 1 | Approved Verbs (with code examples) | 50 | 35 | 15 |
| 2 | Approved Adjectives (with code examples) | 25 | ~6 | 19 |
| 3 | Noun Category Examples (concrete) | 200 | ~114 | 86 |
| 4 | Verb Category Examples | 20 | 0 | 20 |
| 5 | Code Anti-Patterns | 15 | 5 | 10 |
| 6 | Domain Extensions | 50 | ~3 | 47 |

## How to run (markdown-first — replaces the old JSON-era flow)

> **IMPORTANT:** JSON generation was an RCE-artifact remnant. Workers now emit
> **MARKDOWN ONLY** (`ste-code/extensions/<area>.md`). JSON is derived
> deterministically by `.agents/tools/extension/md_to_json.py` (no LLM, no
> eval/exec). Do NOT ask workers to emit JSON.

```bash
# Run one gap area (or all six): verbs adjectives nouns verb-examples anti-patterns domains
python3 .agents/tools/runners/phase-e-run.py verbs
python3 .agents/tools/runners/phase-e-run.py            # all areas
python3 .agents/tools/runners/phase-e-run.py --resume   # skip passed areas
python3 .agents/tools/extension/verify_extensions.py    # Gate 1-6 after a run
```

- 3 workers per batch max (the orchestrator enforces this).
- Each area commits only after `verify_extensions.py` passes (Gate 1-6).
- Per-area git commit is automatic (crash-safe, like the other stages).
- Output: `ste-code/extensions/<area>.md` (+ derived `<area>.json`).

## Worker Prompt Template (now externalized)

The worker prompt is externalized to `.agents/tools/extension/templates/extend-area.md`
and rendered by `extend_batch.py` with the embedded SKILL section appended. Edit
the template to change wording; edit this SKILL to change behavior. The embedded
protocol below (Entry Schemas, Quality Gates) is the single source of truth.

## Worker Prompt Template

Every worker prompt must include these five sections in strict order. Write the full prompt to a temp file before launch.

### Section 1 — Task Directive

Specify the gap area, entry count, and exact output file path.

```
You are the STE-Code Extension Worker. Your task: generate [ENTRY_COUNT] entries
for the [GAP_AREA] gap area.

Output area: [GAP_AREA_NAME]
Maximum entries: [COUNT]
Output file: [EXACT_FILE_PATH]
Model: poolside/laguna-s-2.1:free

Each entry must follow the schema in Section 3 below.
```

### Section 2 — Output Schema Constraints

Include the relevant schema inline so the worker does not invent fields. Copy from the Entry Schemas section of this file.

```
OUTPUT SCHEMA (exact fields, no additions):

[PASTE RELEVANT SCHEMA FROM ENTRY SCHEMAS SECTION]

RULES:
- Output ONLY a valid JSON array. No markdown fences. No commentary.
- Every entry must include all required fields listed above.
- The "definition" field must have 10 or more words.
- Do not invent terms. Use only terms traceable to the STE-Code domain.
- If you cannot generate a valid entry, output an empty array [].
```

### Section 3 — Anti-Fabrication Rails

```
ANTI-FABRICATION RAILS:
- Do not use placeholder text (TODO, TBD, FIXME, ???, <placeholder>).
- Do not repeat the same definition across multiple entries.
- Every code_example_ste must use approved STE-Code vocabulary.
- Every code_example_non_ste must use avoided synonyms from the canonical synonym table.
- If a term is not in your knowledge, skip it. Do not invent a definition.
```

### Section 4 — Worker Rails (W1-W10)

Append the full W1-W10 checklist from `.agents/references/worker-rails.md`. The worker must self-check against these rails before writing output.

NOTE: A worker prompt without the W1-W10 rails is incomplete. Do not launch it.

### Section 5 — Output Format Lock

```
OUTPUT FORMAT LOCK:
- Output begins with "[" and ends with "]".
- One JSON object per entry, separated by commas.
- No trailing commas.
- No newlines inside string values.
- All string values use double quotes, not single quotes.
```

### Prompt Construction Command

```bash
# Build a complete worker prompt from the template
cat > /tmp/ext-worker-prompt-N.txt << 'PROMPTEOF'
[ASSEMBLE SECTIONS 1-5 HERE]
PROMPTEOF
```

NOTE: Use a heredoc with a quoted delimiter (`'PROMPTEOF'`) to prevent shell variable expansion inside the prompt body.

## Actions

### `generate` — Fill SCE gap areas

Launches batched poll workers to generate entries for a specified gap area. Uses the same parallel launch pattern as the benchmark orchestrator.

```bash
# Launch extension workers for a specific gap area
# Configure area and batch size in the script before running
python3 .agents/benchmark/launch-extension-workers.py --area [AREA] --batch-size 3 --max-entries 20
```

Arguments:

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| `--area` | `verbs`, `adjectives`, `nouns`, `verb-examples`, `anti-patterns`, `domains` | (required) | Gap area to fill |
| `--batch-size` | 1-3 | 3 | Workers per batch |
| `--max-entries` | 5-20 | 20 | Entries per worker |
| `--output-dir` | (path) | auto | Override output directory |

The script:
1. Reads the prompt template from this file.
2. Generates 3 worker prompt files in `/tmp/ext-worker-prompt-{1,2,3}.txt`.
3. Launches all 3 workers in parallel via `hermes -z`.
4. Waits for all workers to complete (120-second timeout per worker).
5. Runs the Output Validation Pipeline on the batch output.
6. Commits valid output via `git gcommit-hermes`.

Output: `SCE/data/vocabulary/generated/`, `SCE/core/categories/generated/`, `SCE/compute/generated/`

### `enlarge` — Expand ste-code from refined content

```bash
python3 .agents/benchmark/enlarge-ste-code.py
```
Takes `ste-code/refined/` as input, generates code-domain enrichments in `ste-code/enriched-code/`.
Areas: code-examples (STE/non-STE pairs), dictionary-expand (code-domain terms), domain-adapt (category mappings).

### `audit` — Run quality validation on generated output

```bash
# Validate a single batch file
python3 .agents/tools/quality/check-rails.py SCE/data/vocabulary/generated/output-N.json

# Validate all generated files
python3 .agents/tools/quality/check-rails.py SCE/data/vocabulary/generated/*.json

# Check for duplicates across all batches
python3 .agents/tools/quality/detect-duplicates.py SCE/data/vocabulary/generated/
```

## Output Directories
- Verbs: `SCE/data/vocabulary/generated/`
- Adjectives: `SCE/data/vocabulary/generated/`
- Noun examples: `SCE/core/categories/generated/`
- Anti-patterns: `SCE/compute/generated/`
- Domain extensions: `SCE/data/vocabulary/generated/`

## Entry Schemas — Inline Summary (from Agent #8)

The full schemas live in `.agents/agent/agent-8-extension-worker.md`. This section summarizes the required fields for each gap area so the reader can validate output without opening a second file.

### Verb Entry

Required fields: `term`, `type`, `category-id`, `approved`, `replaces`, `definition`, `code_example_ste`, `code_example_non_ste`, `source`.

- `term` (string): The approved verb. Must match a verb from the STE-Code approved verb list or be a standard code-domain verb.
- `type` (string): Always `"verb"`.
- `category-id` (number): The noun category this verb applies to (1-19).
- `approved` (boolean): `true` for STE-Code approved verbs, `false` for rejected synonyms.
- `replaces` (array of strings): Avoided synonyms this verb replaces. Must reference entries from the canonical synonym table (14 Prefer/Avoid pairs).
- `definition` (string): 10+ words. Describes the verb's meaning in a code documentation context.
- `code_example_ste` (string): A procedural sentence using the verb in STE-Code compliant form.
- `code_example_non_ste` (string): The same instruction using avoided synonyms.
- `source` (string): Batch identifier, for example `"generated-batch-003"`.

### Adjective Entry

Required fields: `term`, `type`, `approved`, `definition`, `code_example_ste`, `code_example_non_ste`, `source`.

- `term` (string): The approved adjective.
- `type` (string): Always `"adjective"`.
- `approved` (boolean): `true` for approved adjectives.
- `definition` (string): 10+ words. Describes the adjective's technical meaning.
- `code_example_ste` (string): A sentence using the adjective in STE-Code compliant form.
- `code_example_non_ste` (string): The same sentence using an unapproved alternative.
- `source` (string): Batch identifier.

### Noun Category Example

Required fields: `category-id`, `category`, `term`, `definition`, `approved`, `source`.

- `category-id` (number): Category number 1-19.
- `category` (string): Full category name from the STE-Code 19 noun categories.
- `term` (string): A concrete technical noun (class name, module name, data type).
- `definition` (string): 10+ words. Describes the noun in a code documentation context.
- `approved` (boolean): `true` for domain-appropriate technical nouns.
- `source` (string): Batch identifier.

### Verb Category Example

Required fields: `category-id`, `verb`, `context`, `example_ste`, `example_non_ste`, `source`.

- `category-id` (number): Category number 1-19.
- `verb` (string): The approved verb being exemplified.
- `context` (string): The documentation context (for example, "API reference", "README", "error message").
- `example_ste` (string): A procedural sentence using the verb in STE-Code form.
- `example_non_ste` (string): The same instruction using avoided synonyms.
- `source` (string): Batch identifier.

### Anti-Pattern

Required fields: `id`, `pattern`, `non_ste`, `ste`, `violates`, `severity`, `context`.

- `id` (string): Unique identifier, for example `"AP-007"`.
- `pattern` (string): Name of the anti-pattern.
- `non_ste` (string): Example of the bad documentation.
- `ste` (string): The STE-Code compliant rewrite.
- `violates` (array of strings): STE-Code principles violated. Must use valid principle numbers P1-P14.
- `severity` (string): One of `"blocking"`, `"error"`, `"warning"`, `"info"`. See Severity Levels below.
- `context` (string): Where this pattern appears (for example, "API documentation", "README files").

### Domain Extension

Required fields: `domain`, `term`, `definition`, `replaces`, `source`.

- `domain` (string): The code domain (for example, "containerization", "networking", "testing").
- `term` (string): The domain-specific approved term.
- `definition` (string): 10+ words. Describes the term in its domain context.
- `replaces` (array of strings): Non-approved alternatives this term replaces.
- `source` (string): Batch identifier.

### Anti-Pattern Severity Levels

| Severity | Meaning | Use When |
|----------|---------|----------|
| `blocking` | Documentation cannot pass compliance check | Passive voice in API descriptions, undefined technical terms, contradictory instructions |
| `error` | Understandable but violates a core rule | Jargon without definition, slang, regional spelling, unapproved verb forms, semicolons, contractions |
| `warning` | Rule-compliant but uses weak style | Long sentences (over 25 words), nested clauses, inconsistent terminology |
| `info` | Meets rules but could be clearer | Synonyms for approved terms, minor redundancy, verbose phrasing |

## Example Generated Entries

These examples show what a valid entry looks like for each gap area. Use them as reference when reviewing worker output. Every field is required unless marked optional.

### Area 1: Approved Verb

```json
{
  "term": "attach",
  "type": "verb",
  "category-id": 3,
  "approved": true,
  "replaces": ["mount", "connect to", "link with"],
  "definition": "Connect one software component or resource to another so they can exchange data or share state.",
  "code_example_ste": "Attach the debugger to the running process before you set a breakpoint.",
  "code_example_non_ste": "Hook up the debugger to the running process prior to configuring a breakpoint.",
  "source": "generated-batch-001"
}
```

### Area 1: Approved Verb (second example, showing rejected synonym)

```json
{
  "term": "leverage",
  "type": "verb",
  "category-id": 1,
  "approved": false,
  "replaces": [],
  "definition": "A rejected synonym. Use \"use\" instead. This term is jargon and violates STE-Code Rule P1.",
  "code_example_ste": "Use the cache layer to reduce database load.",
  "code_example_non_ste": "Leverage the cache layer to decrease database burden.",
  "source": "generated-batch-001"
}
```

### Area 2: Approved Adjective

```json
{
  "term": "idempotent",
  "type": "adjective",
  "approved": true,
  "definition": "Describes an operation that produces the same result when applied one or more times, with no additional side effects after the first application.",
  "code_example_ste": "Make the DELETE endpoint idempotent. A second request with the same identifier must not cause an error.",
  "code_example_non_ste": "Ensure the DELETE endpoint operates in an idempotent fashion such that duplicate invocations don't throw.",
  "source": "generated-batch-002"
}
```

### Area 3: Noun Category Example

```json
{
  "category-id": 6,
  "category": "Modules, Classes and Services",
  "term": "AuthenticationService",
  "definition": "A service class that verifies user credentials and issues access tokens for protected API endpoints.",
  "approved": true,
  "source": "generated-batch-004"
}
```

### Area 3: Noun Category Example (second example, different category)

```json
{
  "category-id": 9,
  "category": "Data Types and Structures",
  "term": "Result<T, E>",
  "definition": "A generic sum type that represents either a successful value of type T or an error value of type E, used for explicit error handling without exceptions.",
  "approved": true,
  "source": "generated-batch-004"
}
```

### Area 4: Verb Category Example

```json
{
  "category-id": 1,
  "verb": "initialize",
  "context": "API reference — class constructor documentation",
  "example_ste": "The constructor initializes the connection pool with the specified maximum size.",
  "example_non_ste": "The constructor bootstraps and wires up the connection pool leveraging the supplied max ceiling.",
  "source": "generated-batch-005"
}
```

### Area 5: Code Anti-Pattern

```json
{
  "id": "AP-007",
  "pattern": "Using future tense in procedural instructions",
  "non_ste": "The system will send a confirmation email after the registration process completes successfully.",
  "ste": "The system sends a confirmation email after registration completes.",
  "violates": ["P2", "P4"],
  "severity": "error",
  "context": "User-facing documentation, onboarding guides, API tutorials"
}
```

### Area 5: Code Anti-Pattern (second example, blocking severity)

```json
{
  "id": "AP-008",
  "pattern": "Undefined acronym in error message",
  "non_ste": "Error: DAG execution failed at T2.",
  "ste": "Error: The scheduled workflow (DAG) failed at step T2. Open the Airflow dashboard to see the step log.",
  "violates": ["P1", "P8"],
  "severity": "blocking",
  "context": "CLI error messages, log output, alert notifications"
}
```

### Area 6: Domain Extension

```json
{
  "domain": "containerization",
  "term": "orchestrator",
  "definition": "A control plane component that schedules and manages the lifecycle of containerized workloads across a cluster of machines.",
  "replaces": ["scheduler", "cluster manager", "container manager"],
  "source": "generated-batch-006"
}
```

## Quality Gates Checklist

After every batch, run these checks before accepting output. All gates must pass. Do not skip gates.

### Gate 1 — JSON Syntax

Every output file must parse as valid JSON.

```bash
python3 -c "import json; json.load(open('OUTPUT_FILE')); print('PASS: valid JSON')"
```

If a file fails to parse, extract JSON from markdown fences if present. If still invalid, move the file to the quarantine directory and rerun the worker with a corrected prompt.

### Gate 2 — Required Fields Present

Every entry must include all fields listed in the Entry Schemas section for its type. Missing fields are a hard fail.

```bash
# Check verb entries for required fields
python3 -c "
import json
data = json.load(open('OUTPUT_FILE'))
required = ['term','type','definition','code_example_ste','code_example_non_ste','source']
for i, entry in enumerate(data):
    missing = [f for f in required if f not in entry]
    if missing:
        print(f'Entry {i}: MISSING {missing}')
"
```

### Gate 3 — Definition Length

Every entry must have a `definition` field with 10 or more words.

```bash
python3 -c "
import json
data = json.load(open('OUTPUT_FILE'))
for i, entry in enumerate(data):
    words = entry.get('definition','').split()
    if len(words) < 10:
        print(f'Entry {i} ({entry.get(\"term\",\"?\")}): definition too short ({len(words)} words)')
"
```

### Gate 4 — No Fabricated Content

Grep output files for fabrication markers. Any match fails the gate.

```bash
grep -in 'TODO\|TBD\|FIXME\|placeholder\|<PLACEHOLDER>\|???\|to be determined' OUTPUT_FILE
```

If matches exist, the worker did not complete its task. Quarantine the file and rerun.

### Gate 5 — Unique Terms Within Batch

No two entries in the same batch may share the same `term` and `type` pair.

```bash
python3 -c "
import json
data = json.load(open('OUTPUT_FILE'))
keys = [(e.get('term',''), e.get('type','')) for e in data]
dupes = [k for k in set(keys) if keys.count(k) > 1]
if dupes:
    print(f'DUPLICATES: {dupes}')
else:
    print('PASS: no duplicates')
"
```

### Gate 6 — STE / Non-STE Pair Quality

For verb and adjective entries, the STE and non-STE example pair must differ substantively — not just by punctuation or word order. At least one avoided synonym from the canonical synonym table must appear in the non-STE example.

```bash
python3 -c "
import json
synonym_map = {
    'use': ['utilize','leverage','employ'],
    'start': ['initiate','commence','bootstrap'],
    'stop': ['terminate','halt','kill'],
    'show': ['display','render','present'],
    'make': ['create','generate','produce'],
    'get': ['retrieve','fetch','obtain'],
    'set': ['configure','assign','establish'],
    'check': ['verify','validate','ensure'],
    'do': ['perform','execute','carry out'],
    'send': ['transmit','dispatch','forward'],
    'remove': ['delete','eliminate','purge'],
    'keep': ['retain','preserve','maintain']
}
data = json.load(open('OUTPUT_FILE'))
for i, e in enumerate(data):
    ste = e.get('code_example_ste','')
    non = e.get('code_example_non_ste','')
    if ste == non:
        print(f'Entry {i}: STE and non-STE are identical')
    elif ste.lower().strip('.') == non.lower().strip('.'):
        print(f'Entry {i}: STE and non-STE differ only by punctuation')
"
```

### Gate 7 — Valid Principle Numbers (Anti-Patterns)

Every anti-pattern entry must cite valid STE-Code principle numbers (P1-P14).

```bash
python3 -c "
import json
data = json.load(open('OUTPUT_FILE'))
valid = set(f'P{i}' for i in range(1,15))
for i, e in enumerate(data):
    if 'violates' in e:
        invalid = [v for v in e['violates'] if v not in valid]
        if invalid:
            print(f'Entry {i}: INVALID principles {invalid}')
"
```

### Gate 8 — Cross-Reference Traceability

Every approved term must be traceable to one of:
- An existing entry in `SCE/data/vocabulary/approved-verbs.json`
- An entry in `SCE/core/categories/synonym-table.json`
- A recognized code-domain technical noun (Rule 1.5 / 1.6 / 1.8)

A term with no traceable source is suspect. Flag it for manual review.

### Gate 9 — Batch Size Compliance

No batch file may contain more than 20 entries from a single worker. Reject oversized output.

```bash
python3 -c "
import json
data = json.load(open('OUTPUT_FILE'))
if len(data) > 20:
    print(f'FAIL: {len(data)} entries exceeds the 20-entry limit')
else:
    print(f'PASS: {len(data)} entries')
"
```

### Gate 10 — No Cross-Batch Duplicates

Check new entries against all previously generated batch files for duplicate `term` + `type` pairs.

```bash
python3 .agents/tools/quality/detect-duplicates.py SCE/data/vocabulary/generated/
```

A duplicate is acceptable only when the `type` or `category` field differs between the two entries. Same `term` + same `type` = reject and quarantine the newer entry.

## Output Validation Pipeline Summary

The full validation protocol is defined in Agent #8 (`.agents/agent/agent-8-extension-worker.md`). This summary provides a quick reference for the operator.

### Pipeline Steps

1. **Syntax Validation** — Parse every output file as JSON. Reject unparseable files.
2. **Schema Validation** — Check that every entry has all required fields for its gap area.
3. **Quality Thresholds** — Definition length (10+ words), unique terms, substantive STE/non-STE pairs.
4. **Duplicate Detection** — Check within the batch and against all previous batches.
5. **Cross-Reference Audit** — Lightweight Agent #3 audit: completion check, fabrication check, content fidelity, factual correctness.

### Failure Recovery Tracks

| Track | Failure Type | Action |
|-------|-------------|--------|
| **Track A** | Syntax or Schema (Steps 1-2) | Quarantine file, diagnose root cause, fix prompt, relaunch with 50% reduced scope |
| **Track B** | Quality or Duplicates (Steps 3-4) | Quarantine only bad entries, keep valid entries, regenerate missing slots later |
| **Track C** | Cross-Reference Audit (Step 5) | Identify failing check, rewrite prompt with concrete constraints, relaunch |

### Escalation Rule

If a gap area experiences 3 consecutive failures across any track:
1. Stop all workers for that gap area.
2. Write an incident report to `.agents/state/EXTENSION-PROGRESS.md` under `## ESCALATION`.
3. Request an Agent #3 (Auditor) full review.
4. Do not resume until the Auditor confirms the prompt fix.

### Worker Timeout Policy

| Time | Action |
|------|--------|
| 90 seconds | Log a warning. The worker may be stuck. |
| 120 seconds | Mark as timed out. Do not wait. |
| After timeout | Restart with same task. If retry also times out, reduce entry count by 50%. |

## State

Progress tracked in `.agents/state/EXTENSION-PROGRESS.md`. Update after every batch using this format:

```markdown
## Batch N - YYYY-MM-DD HH:MM
- Area: [area-name]
- Workers: [N]/3 complete ([failure detail if any])
- Entries: [total] generated, [quarantined] quarantined
- Valid: [valid]/[total]
- Files: [list of output files]
- Next: Batch N+1 ([next area])
```
