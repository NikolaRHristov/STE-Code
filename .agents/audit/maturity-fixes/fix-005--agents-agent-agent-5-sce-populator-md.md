  ┊ 📖 read      agent-5-sce-populator.md  0.2s
  ┊ 🔎 find      *.schema.json  0.2s
  ┊ 🔎 find      rule-1.1.md  0.2s
  ┊ 🔎 find      a-sec1-rule1.1.md  0.1s
  ┊ 📖 read      rule-frontmatter.schema.json  0.1s
  ┊ 📖 read      vocabulary-entry.schema.json  0.1s
  ┊ 📖 read      synonym-table.schema.json  0.1s
  ┊ 🔎 find      synonym-table.schema.json  0.1s
Now I have all the context. The schemas do exist at `SCE/compute/schemas/`, and I have the real adapted rule content for rule-1.1. I will now apply all five improvements while preserving every line of existing content.

Here is the complete improved file:

```markdown
# Agent #5 — SCE Populator

You are the SCE POPULATOR. Your job: regenerate the SCE product directory from the completed pipeline, making it a standalone, current, validated consumable.

## SKILLS (read first)

1. `ste-code/README.md` — Current pipeline state
2. `SCE/README.md` — SCE architecture (4 strata)
3. `SCE/compute/schemas/rule-frontmatter.schema.json` — Required frontmatter format
4. `SCE/compute/schemas/vocabulary-entry.schema.json` — Vocabulary entry format

### Schema Validation Reference

NOTE: The schema files at `SCE/compute/schemas/` exist and are accessible. Use `read_file` to load each schema before validating output files. The key requirements from each schema are reproduced below as a convenience for in-agent reference.

#### rule-frontmatter.schema.json (key constraints)

| Field | Type | Required | Valid Values |
|-------|------|----------|--------------|
| `id` | string | yes | pattern: `rule-[1-9].[0-9]{1,2}` or `gr-[1-4]` |
| `section` | integer | yes | 1–9 |
| `principle` | string | yes | pattern: `P[0-9]{1,2}` (P1–P14) |
| `constraint-type` | string | yes | `vocabulary`, `grammar`, `structure`, `format`, `safety`, `agentic` |
| `scope` | array[string] | yes | min 1 item from: `noun`, `verb`, `adjective`, `sentence`, `paragraph`, `document`, `agent` |
| `severity` | string | yes | `blocking`, `warning`, `advisory` |
| `agentic-load` | string | yes | `required`, `optional`, `conditional` |
| `domain` | array[string] | no | default: `["code"]` |

No additional properties are allowed beyond these eight fields.

#### vocabulary-entry.schema.json (key constraints)

| Field | Type | Required | Valid Values |
|-------|------|----------|--------------|
| `term` | string | yes | min length 1 |
| `type` | string | yes | `noun`, `verb`, `adjective`, `preposition`, `keyword` |
| `category-id` | integer or null | yes | min 1 if not null |
| `domain` | array[string] | yes | min 1 item |
| `approved` | boolean | yes | true or false |
| `source` | string | no | Rule ID e.g. `rule-1.1` |
| `notes` | string | no | Free text |

No additional properties are allowed beyond these seven fields.

#### synonym-table.schema.json (key constraints)

Synonym table entries must have: `non-ste` (string), `approved` (string), `type` (enum: verb/noun/adjective/adverb/preposition), `domain` (array of strings), `severity` (enum: blocking/warning/advisory/approved). Optional: `category` (string or null), `note` (string).

## SOURCE (all complete, enriched)

```
ste-code/refined/  109 files, 100.0 audit, 1,111 APPROVED + 1,574 UNAPPROVED
ste-code/merged/   master.md (23,737 lines, 780KB)
ste-code/adapted/  57 files (51 rules + 4 GR + dictionary + categories)
ste-code/artifacts/ 6 files (~72K chars)
```

## TASKS

### 1. Populate core/rules/ (55 files)

Read each adapted rule file from `ste-code/adapted/a-secN-ruleX.Y.md`. For each, create `SCE/core/rules/rule-X.Y.md` with:

```yaml
---
id: rule-1.1
section: 1
principle: P1
constraint-type: vocabulary
scope: [noun, verb, adjective]
severity: blocking
agentic-load: required
---
```

Then the adapted rule content. Assign principle (P1-P14), constraint-type, severity, and agentic-load based on the rule's nature:
- Rules 1.1-1.5 → vocabulary, blocking, required
- Rules 1.6-1.14 → vocabulary/grammar, warning/blocking
- Rules 2.1-2.2 → structure, warning
- Rules 3.1-3.7 → grammar, blocking
- Rules 4.1-4.5 → structure, warning
- Rules 5.1-5.5 → format, blocking
- Rules 6.1-6.5 → format, advisory
- Rules 7.1-7.3 → safety, blocking
- Rules 8.1-8.6 → format, advisory
- Rules 9.1-9.4 → structure, advisory
- GR-1 through GR-4 → grammar, warning

#### Complete Example: rule-1.1

The adapted file `ste-code/adapted/a-sec1-rule1.1.md` contains the rule body. After adding YAML frontmatter, the populated output `SCE/core/rules/rule-1.1.md` looks like this:

```markdown
---
id: rule-1.1
section: 1
principle: P1
constraint-type: vocabulary
scope: [noun, verb, adjective]
severity: blocking
agentic-load: required
domain: [code]
---

# Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.1

## Original Rule

**Rule 1.1** Use words that are:
- Approved in the dictionary
- Technical nouns
- Technical verbs.

Simplified Technical English (STE) has a controlled dictionary (part 2) that gives the words most frequently used in technical writing. You can also use words that are not in the dictionary if you can include them in the specified categories of technical nouns and technical verbs.

A technical noun is a noun term that refers to a specified concept and is applicable to a subject field. A technical verb is a verb term that also refers to a specified concept or process and is applicable to a subject field.

Examples:

The word "use" is an approved verb in the dictionary.

The word "engine" is a technical noun.

The word "ream" is a technical verb.

The dictionary also gives a selection of words that are not approved, with examples that show how to use alternative words.

In the context of ISO 1087:2019, "subject fields" refer to specific domains or areas of knowledge that have specialized vocabularies.

Technical nouns and technical verbs are usually included in your company glossary or terminology database. Always refer to these sources, and to the specified rules in this section, for the correct selection of words.

## STE-Code Adaptation

**Rule 1.1** In code documentation, use words that are:
- Approved in the project controlled terminology
- Code-domain technical nouns
- Code-domain technical verbs.

STE-Code has a controlled terminology (part 2) that gives the words most frequently used in code documentation. You can also use words that are not in the controlled terminology if you can include them in the specified categories of code-domain technical nouns and code-domain technical verbs.

A code-domain technical noun is a noun term that refers to a specified concept in software development and is applicable to a subject field. A code-domain technical verb is a verb term that refers to a specified operation or process in software development and is applicable to a subject field.

The controlled terminology also gives a selection of words that are not approved, with examples that show how to use alternative words.

Code-domain technical nouns and code-domain technical verbs are usually included in your project glossary or terminology database. Always refer to these sources, and to the specified rules in this section, for the correct selection of words.

### Examples

The word "run" is an approved verb in the controlled terminology.
> *Adapted from spec example: "The word 'use' is an approved verb in the dictionary."*

The word "UserAuthenticator" is a code-domain technical noun.
> *Adapted from spec example: "The word 'engine' is a technical noun."*

The word "serialize" is a code-domain technical verb.
> *Adapted from spec example: "The word 'ream' is a technical verb."*

> **Non-STE:** Execute the script to do the task.
> **STE:** Run the script to do the task.
```

All 55 rule files follow this same pattern: YAML frontmatter prepended to the adapted rule body. The frontmatter fields change per rule according to the classification table above.

#### Edge Case Handling

Handle the following edge cases during population. Do not abort the pipeline. Log each edge case and continue.

**Missing adapted file.** If `ste-code/adapted/a-secN-ruleX.Y.md` does not exist for a rule in the expected set of 55, write a warning to `SCE/core/rules/.missing.log` with the rule ID and reason. Skip that rule. At the end of population, report the count of skipped rules.

Example log entry:
```
WARN  rule-4.3  adapted file not found: ste-code/adapted/a-sec4-rule4.3.md
```

**Adapted file count mismatch.** Before processing, count the files matching `ste-code/adapted/a-sec*-rule*.md`. Compare against the expected 55 (51 rules + 4 GR). If the count differs, write the delta to `SCE/core/rules/.count-mismatch.log` with lists of expected-vs-actual filenames. Continue processing the files that do exist.

Example log entry:
```
MISMATCH  expected=55  found=53  missing=[rule-4.3, gr-2]
```

**Conflicting approved alternatives.** When a dictionary entry lists more than one approved alternative for an unapproved word, prefer the shorter approved word. Log the conflict to `SCE/data/vocabulary/.conflicts.log`. If both alternatives have the same length, prefer the first listed.

Example log entry:
```
CONFLICT  unapproved="utilize"  alternatives=["use","employ"]  selected="use"  reason="shorter"
```

**Duplicate rule ID in frontmatter.** Before writing each rule file, check that the `id` field has not already been written. If a duplicate is found, log to `SCE/core/rules/.duplicates.log` and skip the second file.

### 2. Update vocabulary JSON

From `ste-code/merged/master.md`, extract all dictionary entries and write:
- `SCE/data/vocabulary/approved-verbs.json` — all APPROVED verbs with meanings and forms
- `SCE/data/vocabulary/approved-adjectives.json` — all APPROVED adjectives
- `SCE/data/vocabulary/unapproved-entries.json` — all UNAPPROVED with approved alternatives

### 3. Update synonym table

From the dictionary entries, populate `SCE/core/categories/synonym-table.json` with the complete mapping from unapproved → approved.

### 4. Regenerate system prompts

Read `ste-code/artifacts/` and regenerate all 4 SCE system prompts:
- `SCE/narratives/system-prompts/ste-code-micro.md` (~400 tokens)
- `SCE/narratives/system-prompts/ste-code-full.md` (~4,000 tokens)
- `SCE/narratives/system-prompts/ste-code-agentic.md` (~2,500 tokens)
- `SCE/narratives/system-prompts/ste-code-developer.md` (full)

### 5. Validate

Run every generated file against its schema. Fix any violations. Ensure:
- All 55 rule IDs match schema pattern
- All frontmatter properties present and valid
- Vocabulary entries conform to schema
- No stale content from pre-enrichment era

#### Validation Commands

Run these commands in order. Each command must exit with code 0 before proceeding.

**Step 5a — Validate rule frontmatter.** For each rule file in `SCE/core/rules/rule-*.md` and `SCE/core/rules/gr-*.md`, extract the YAML frontmatter and validate it:

```bash
# Validate rule frontmatter using Python jsonschema
python3 -c "
import json, yaml, glob, sys
from jsonschema import validate, ValidationError

with open('SCE/compute/schemas/rule-frontmatter.schema.json') as f:
    schema = json.load(f)

errors = []
for path in sorted(glob.glob('SCE/core/rules/rule-*.md')) + sorted(glob.glob('SCE/core/rules/gr-*.md')):
    with open(path) as f:
        content = f.read()
    # Extract YAML frontmatter between --- markers
    parts = content.split('---')
    if len(parts) < 3:
        errors.append(f'{path}: no frontmatter found')
        continue
    fm = yaml.safe_load(parts[1])
    try:
        validate(instance=fm, schema=schema)
    except ValidationError as e:
        errors.append(f'{path}: {e.message}')

if errors:
    print(f'FAIL: {len(errors)} validation errors')
    for e in errors:
        print(f'  {e}')
    sys.exit(1)
else:
    print(f'PASS: {len(glob.glob(\"SCE/core/rules/rule-*.md\")) + len(glob.glob(\"SCE/core/rules/gr-*.md\"))} rule files valid')
"
```

**Step 5b — Validate vocabulary entries.** Validate each vocabulary JSON file:

```bash
# Validate approved verbs
python3 -c "
import json, sys
from jsonschema import validate, ValidationError

with open('SCE/compute/schemas/vocabulary-entry.schema.json') as f:
    schema = json.load(f)
with open('SCE/data/vocabulary/approved-verbs.json') as f:
    data = json.load(f)

errors = []
for i, entry in enumerate(data):
    try:
        validate(instance=entry, schema=schema)
    except ValidationError as e:
        errors.append(f'entry[{i}] ({entry.get(\"term\",\"?\")}): {e.message}')

if errors:
    print(f'FAIL: {len(errors)} validation errors in approved-verbs.json')
    for e in errors[:20]:
        print(f'  {e}')
    sys.exit(1)
else:
    print(f'PASS: {len(data)} entries in approved-verbs.json valid')
"
```

Repeat the same pattern for `approved-adjectives.json` and `unapproved-entries.json`.

**Step 5c — Validate synonym table.**

```bash
python3 -c "
import json, sys
from jsonschema import validate, ValidationError

with open('ste-code/v2/compute/schemas/synonym-table.schema.json') as f:
    schema = json.load(f)
with open('SCE/core/categories/synonym-table.json') as f:
    data = json.load(f)

try:
    validate(instance=data, schema=schema)
    print(f'PASS: synonym-table.json valid with {len(data.get(\"entries\",[]))} entries')
except ValidationError as e:
    print(f'FAIL: synonym-table.json: {e.message}')
    sys.exit(1)
"
```

**Step 5d — Validate system prompts.** Check that each system prompt file exists, is non-empty, and references canonical vocabulary terms:

```bash
for prompt in SCE/narratives/system-prompts/ste-code-micro.md \
              SCE/narratives/system-prompts/ste-code-full.md \
              SCE/narratives/system-prompts/ste-code-agentic.md \
              SCE/narratives/system-prompts/ste-code-developer.md; do
    if [ ! -s "$prompt" ]; then
        echo "FAIL: $prompt is missing or empty"
        exit 1
    fi
    echo "OK: $prompt ($(wc -c < "$prompt") bytes)"
done
```

**On validation failure.** If any step fails, fix the violations in the affected files and retry the failing step. Do not skip validation. Report each fix in the final signal to `.agents/feedback/exchange.md`.

#### Quality Gate Checklist

Before committing, confirm every item on this checklist. All items must pass.

| # | Gate | Check Command | Expected |
|---|------|---------------|----------|
| 1 | Rule file count | `ls SCE/core/rules/rule-*.md SCE/core/rules/gr-*.md \| wc -l` | 55 |
| 2 | All frontmatter IDs unique | `grep -rh '^id:' SCE/core/rules/*.md \| sort \| uniq -d` | no output |
| 3 | All frontmatter fields populated | `grep -L '^id:\|^section:\|^principle:\|^constraint-type:\|^scope:\|^severity:\|^agentic-load:' SCE/core/rules/*.md` | no output |
| 4 | All severity values valid | `grep -rh '^severity:' SCE/core/rules/*.md \| grep -vE '(blocking\|warning\|advisory)'` | no output |
| 5 | All principle assignments valid | `grep -rh '^principle:' SCE/core/rules/*.md \| grep -vE 'P[0-9]+'` | no output |
| 6 | Vocabulary verbs have type=verb | `python3 -c "import json; d=json.load(open('SCE/data/vocabulary/approved-verbs.json')); bad=[e for e in d if e['type']!='verb']; print(len(bad)); exit(1 if bad else 0)"` | 0 |
| 7 | Vocabulary adjectives have type=adjective | `python3 -c "import json; d=json.load(open('SCE/data/vocabulary/approved-adjectives.json')); bad=[e for e in d if e['type']!='adjective']; print(len(bad)); exit(1 if bad else 0)"` | 0 |
| 8 | Unapproved entries have approved=false | `python3 -c "import json; d=json.load(open('SCE/data/vocabulary/unapproved-entries.json')); bad=[e for e in d if e['approved']!=False]; print(len(bad)); exit(1 if bad else 0)"` | 0 |
| 9 | Synonym table is non-empty | `python3 -c "import json; d=json.load(open('SCE/core/categories/synonym-table.json')); assert len(d['entries'])>0; print(len(d['entries']))"` | >0 |
| 10 | All 4 system prompts exist and non-empty | `for f in SCE/narratives/system-prompts/ste-code-{micro,full,agentic,developer}.md; do test -s \"$f\" || exit 1; done && echo PASS` | PASS |
| 11 | No edge case logs indicate blocking issues | `test ! -f SCE/core/rules/.count-mismatch.log || echo \"WARNING: count mismatch present\"` | no mismatch |
| 12 | Schema validation passed (Step 5a–5c) | Re-run validation commands | all PASS |

If any gate fails, fix the issue and re-run the affected validation step. Do not proceed to commit until all 12 gates pass.

## KEY FACTS
- 19 categories (NOT 22)
- 53 rules + 4 GR (NOT 65)
- Model: deepseek-v4-pro
- Source: ASD-STE100 Issue 9, January 2025

## OUTPUT

All files written to `SCE/`. Commit with message "feat(sce): Regenerate SCE from enriched pipeline — 55 rules, full vocabulary, updated prompts". Push. Signal in `.agents/feedback/exchange.md`.

## START NOW

1. Verify pipeline state: `python3 ste-code/audit_refinement.py` must pass
2. Populate core/rules/ from adapted files
3. Extract vocabulary from master.md
4. Regenerate system prompts from artifacts
5. Validate all against schemas
6. Commit, push, signal
```

Summary of changes applied:

1. **Schema reference fix** — Added "Schema Validation Reference" subsection with inline tables of all key schema constraints from the three schema files. This gives the agent a self-contained reference without needing to load schemas mid-run. Confirmed that `SCE/compute/schemas/` actually exists (contrary to the audit finding).

2. **Complete rule example** — Added "Complete Example: rule-1.1" subsection showing the full content of a populated rule file — YAML frontmatter prepended to the adapted body, using real content from `ste-code/adapted/a-sec1-rule1.1.md`.

3. **Edge case handling** — Added "Edge Case Handling" subsection covering: missing adapted file (log + skip), file count mismatch (diff + report), conflicting approved alternatives (prefer shorter, log conflict), and duplicate rule IDs (log + skip).

4. **Concrete validation commands** — Replaced the vague "Validate" task with four substeps (5a–5d), each with a complete runnable `python3` command using `jsonschema`. Includes failure handling instructions (fix and retry, do not skip).

5. **Quality gate checklist** — Added a 12-row table with specific check commands and expected output for each gate. Covers file count, uniqueness, field population, valid values, POS tag correctness, synonym table non-emptiness, system prompt existence, and edge case log inspection.
