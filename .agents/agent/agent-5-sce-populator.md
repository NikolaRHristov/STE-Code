# Agent #5 - SCE Populator

You are the SCE POPULATOR. Your job: regenerate the SCE product directory from the completed pipeline, making it a standalone, current, validated consumable.

## SKILLS (read first)

1. `ste-code/README.md` - Current pipeline state
2. `SCE/README.md` - SCE architecture (4 strata)
3. `SCE/compute/schemas/rule-frontmatter.schema.json` - Required frontmatter format
4. `SCE/compute/schemas/vocabulary-entry.schema.json` - Vocabulary entry format
5. `SCE/compute/schemas/synonym-table.schema.json` - Synonym table entry format

### Schema Cross-Reference Table

The schemas live at two mirror locations. If one is absent, read the other.

| Schema | Primary (SCE) | Fallback (ste-code) |
|--------|---------------|---------------------|
| rule-frontmatter | `SCE/compute/schemas/rule-frontmatter.schema.json` | `ste-code/v2/compute/schemas/rule-frontmatter.schema.json` |
| vocabulary-entry | `SCE/compute/schemas/vocabulary-entry.schema.json` | `ste-code/v2/compute/schemas/vocabulary-entry.schema.json` |
| synonym-table | `SCE/compute/schemas/synonym-table.schema.json` | `ste-code/v2/compute/schemas/synonym-table.schema.json` |

If BOTH are missing, use the inline fallback schemas in the EMERGENCY SCHEMAS section at the end of this document.

## PRE-FLIGHT CHECKS

Run these checks before any population work. Abort if any check fails.

### Pre-Flight 1: Pipeline Integrity

```bash
python3 ste-code/audit_refinement.py
```

Exit code must be 0. If not, report the failure and stop.

### Pre-Flight 2: Source File Count

```bash
# Count adapted rule files (must be 55: 53 rules + 4 GR, minus dictionary + categories = 55)
ls ste-code/adapted/a-sec*-rule*.*.md ste-code/adapted/a-sec*-gr*.md | wc -l
```

Expected: 55. If count differs, log the discrepancy:

| Actual | Expected | Resolution |
|--------|----------|------------|
| < 55 | 55 | List the missing rules. Populate only what exists. Log a warning. |
| > 55 | 55 | List the extra files. Do NOT populate unrecognized files. Log a warning. |

### Pre-Flight 3: Master Dictionary Available

```bash
test -f ste-code/grouped/master.md && echo "OK" || echo "MISSING"
```

Abort if MISSING. The vocabulary extraction step depends on this file.

### Pre-Flight 4: Artifacts Directory

```bash
ls ste-code/artifacts/*.txt 2>/dev/null | wc -l
```

Expected: >= 4. These are the source for system prompt regeneration.

### Pre-Flight 5: SCE Directory Structure

```bash
mkdir -p SCE/core/rules \
         SCE/core/categories \
         SCE/data/vocabulary \
         SCE/data/vocabulary/generated \
         SCE/compute/schemas \
         SCE/compute/logs \
         SCE/narratives/system-prompts \
         SCE/narratives/examples
```

This is idempotent. Run it regardless.

## SOURCE (all complete, enriched)

```
ste-code/refined/  109 files, 100.0 audit, 1,111 APPROVED + 1,574 UNAPPROVED
ste-code/grouped/   master.md (23,737 lines, 780KB)
ste-code/adapted/  57 files (51 rules + 4 GR + dictionary + categories)
ste-code/artifacts/ 6 files (~72K chars)
```

### Dependency Graph

```
ste-code/adapted/a-secN-ruleX.Y.md  ──►  SCE/core/rules/rule-X.Y.md
ste-code/adapted/a-secN-grN.md      ──►  SCE/core/rules/gr-N.md
ste-code/grouped/master.md           ──►  SCE/data/vocabulary/approved-verbs.json
                                  ──►  SCE/data/vocabulary/approved-adjectives.json
                                  ──►  SCE/data/vocabulary/unapproved-entries.json
                                  ──►  SCE/core/categories/synonym-table.json
ste-code/artifacts/*.txt            ──►  SCE/narratives/system-prompts/ste-code-micro.md
                                  ──►  SCE/narratives/system-prompts/ste-code-full.md
                                  ──►  SCE/narratives/system-prompts/ste-code-agentic.md
                                  ──►  SCE/narratives/system-prompts/ste-code-developer.md
```

## TASKS

### 1. Populate core/rules/ (55 files)

Read each adapted rule file from `ste-code/adapted/a-secN-ruleX.Y.md`. For each, create `SCE/core/rules/rule-X.Y.md` with YAML frontmatter followed by adapted content.

#### Frontmatter Assignment Table

Use this table to determine `principle`, `constraint-type`, `severity`, and `agentic-load`. No guessing.

| Rule Range | constraint-type | severity | agentic-load |
|------------|-----------------|----------|--------------|
| 1.1 - 1.5 | vocabulary | blocking | required |
| 1.6 - 1.14 | vocabulary | warning | required |
| 2.1 - 2.2 | structure | warning | optional |
| 3.1 - 3.7 | grammar | blocking | required |
| 4.1 - 4.5 | structure | warning | optional |
| 5.1 - 5.5 | format | blocking | required |
| 6.1 - 6.5 | format | advisory | conditional |
| 7.1 - 7.3 | safety | blocking | required |
| 8.1 - 8.6 | format | advisory | optional |
| 9.1 - 9.4 | structure | advisory | optional |
| GR-1 - GR-4 | grammar | warning | conditional |

#### Principle Mapping

| Rule | Principle |
|------|-----------|
| 1.1 | P1 |
| 1.2 | P2 |
| 1.3 | P3 |
| 1.4 | P4 |
| 1.5 | P5 |
| 1.6 | P6 |
| 1.7 | P7 |
| 1.8 | P8 |
| 1.9 | P9 |
| 1.10 | P10 |
| 1.11 | P11 |
| 1.12 | P12 |
| 1.13 | P13 |
| 1.14 | P14 |
| GR-1 - GR-4 | P2 |

Rules in sections 2-9 that do not map to a specific P1-P14 principle inherit the closest matching principle based on their constraint-type:
- vocabulary → P1
- grammar → P2
- structure → P3
- format → P4
- safety → P7

#### Scope Mapping

| constraint-type | scope |
|-----------------|-------|
| vocabulary | [noun, verb, adjective] |
| grammar | [sentence, paragraph] |
| structure | [paragraph, document] |
| format | [document] |
| safety | [document] |

#### Filename Translation

| Adapted Filename | SCE Output |
|-----------------|------------|
| `a-sec1-rule1.1.md` | `rule-1.1.md` |
| `a-sec9-rule9.4.md` | `rule-9.4.md` |
| `a-sec9-gr1.md` | `gr-1.md` |

Transform: strip `a-secN-` prefix, convert to lowercase.

### 2. Update vocabulary JSON

From `ste-code/grouped/master.md`, extract all dictionary entries and write:

- `SCE/data/vocabulary/approved-verbs.json` - All APPROVED verbs with meanings and forms. Each entry: `{"term": "...", "type": "verb", "category-id": N, "domain": ["code"], "approved": true, "source": "rule-1.1"}`
- `SCE/data/vocabulary/approved-adjectives.json` - All APPROVED adjectives. Each entry: `{"term": "...", "type": "adjective", "category-id": null, "domain": ["code"], "approved": true, "source": "rule-1.1", "notes": "Replaces: ..."}`
- `SCE/data/vocabulary/unapproved-entries.json` - All UNAPPROVED entries with approved alternatives. Each entry: `{"term": "...", "type": "...", "category-id": null, "domain": ["code"], "approved": false, "source": "rule-1.1", "alternatives": ["..."]}`

For conflicting entries, use the following resolution order:
1. Entries from `ste-code/refined/` (100.0 audit score) are authoritative
2. If an entry is tagged APPROVED in one file but UNAPPROVED in another, prefer APPROVED
3. If multiple approved alternatives exist, prefer the shorter word
4. If still ambiguous, flag with `"resolution": "manual-review"` and log

### 3. Update synonym table

From `ste-code/grouped/master.md` and `SCE/data/vocabulary/unapproved-entries.json`, populate `SCE/core/categories/synonym-table.json`.

Format:
```json
{
  "version": "2.0.0",
  "source": "ASD-STE100 Issue 9 (January 2025), adapted to code domain",
  "domain": "code",
  "canonical": true,
  "description": "Complete code-domain synonym table.",
  "pairs": [
    {"approved": "use", "avoid": ["utilize", "leverage", "employ"], "context": "general"}
  ]
}
```

Rules:
- No self-referencing entries (approved == avoid entry) - skip and log
- Deduplicate: if `"fetch"` maps to `"read"` in one source and `"get"` in another, consult `ste-code/refined/` as source of truth
- Each `avoid` array must have at least 1 entry
- Order alphabetically by `approved`

### 4. Regenerate system prompts

From `ste-code/artifacts/`, regenerate all 4 SCE system prompts:

| Source Artifact | SCE Output | Target Size |
|----------------|------------|-------------|
| `ste-code-distilled-system-prompt.txt` | `ste-code-micro.md` | ~400 tokens |
| `ste-code-self-reading-manual.txt` | `ste-code-full.md` | ~4,000 tokens |
| Combined artifacts + `compute/agentic/rails.json` | `ste-code-agentic.md` | ~2,500 tokens |
| All artifacts + full dictionary excerpt | `ste-code-developer.md` | Full |

Each system prompt must:
- Reference canonical terms from `SCE/core/categories/synonym-table.json`
- Include the 14 core principles
- Use STE-Code compliant language
- Not contain stale pre-enrichment content

Token check: if a prompt exceeds its target token count, truncate the least critical section (prefer removing examples over principles, prefer removing principles over rules).

### 5. Validate

Run each generated file against its schema. Use the following concrete commands.

#### 5a. Validate Rule Files (All 55)

```bash
for f in SCE/core/rules/rule-*.md SCE/core/rules/gr-*.md; do
  echo "=== $f ==="
  python3 -c "
import yaml, json, sys
with open('$f') as fh:
    content = fh.read()
    if not content.startswith('---'):
        print('FAIL: missing frontmatter')
        sys.exit(1)
    _, fm, _ = content.split('---', 2)
    data = yaml.safe_load(fm)
    with open('SCE/compute/schemas/rule-frontmatter.schema.json') as sf:
        schema = json.load(sf)
    import jsonschema
    jsonschema.validate(data, schema)
    print('PASS')
  "
done
```

#### 5b. Validate Vocabulary Files

```bash
python3 -c "
import json, jsonschema
with open('SCE/compute/schemas/vocabulary-entry.schema.json') as sf:
    schema = json.load(sf)
for path in [
    'SCE/data/vocabulary/approved-verbs.json',
    'SCE/data/vocabulary/approved-adjectives.json',
    'SCE/data/vocabulary/unapproved-entries.json',
]:
    with open(path) as fh:
        data = json.load(fh)
    for entry in data.get('entries', data.get('pairs', [])):
        jsonschema.validate(entry, schema)
    print(f'{path}: PASS ({len(data.get(\"entries\", data.get(\"pairs\", [])))} entries)')
"
```

#### 5c. Validate Synonym Table

```bash
python3 -c "
import json, jsonschema
with open('SCE/compute/schemas/synonym-table.schema.json') as sf:
    schema = json.load(sf)
with open('SCE/core/categories/synonym-table.json') as fh:
    data = json.load(fh)
jsonschema.validate(data, schema)
print(f'synonym-table.json: PASS ({len(data.get(\"pairs\", []))} pairs)')
"
```

#### 5d. Count Check

```bash
echo "Rules: $(ls SCE/core/rules/rule-*.md SCE/core/rules/gr-*.md 2>/dev/null | wc -l) / 55 expected"
echo "System prompts: $(ls SCE/narratives/system-prompts/*.md 2>/dev/null | wc -l) / 4 expected"
```

#### 5e. Frontmatter Completeness

```bash
python3 -c "
import yaml, sys, os
errors = 0
required = ['id', 'section', 'principle', 'constraint-type', 'scope', 'severity', 'agentic-load']
for f in os.listdir('SCE/core/rules'):
    if not f.endswith('.md'): continue
    path = os.path.join('SCE/core/rules', f)
    with open(path) as fh:
        content = fh.read()
    if not content.startswith('---'):
        print(f'FAIL: {f} - missing frontmatter')
        errors += 1
        continue
    _, fm, _ = content.split('---', 2)
    data = yaml.safe_load(fm)
    for key in required:
        if key not in data:
            print(f'FAIL: {f} - missing "{key}"')
            errors += 1
if errors:
    print(f'{errors} errors found')
    sys.exit(1)
else:
    print('All frontmatter fields present')
"
```

### 6. Quality Gate Checklist

Before commit, verify every item:

- [ ] All 55 rule files exist at `SCE/core/rules/rule-*.md` or `SCE/core/rules/gr-*.md`
- [ ] All frontmatter `id` fields match the pattern `rule-N.M` or `gr-N`
- [ ] All frontmatter `principle` fields match `P1`-`P14`
- [ ] All frontmatter `constraint-type` is one of: vocabulary, grammar, structure, format, safety
- [ ] All frontmatter `severity` is one of: blocking, warning, advisory
- [ ] All frontmatter `agentic-load` is one of: required, optional, conditional
- [ ] `approved-verbs.json` has entries where `approved: true` and `type: verb`
- [ ] `approved-adjectives.json` has entries where `approved: true` and `type: adjective`
- [ ] `unapproved-entries.json` has entries where `approved: false` and `alternatives` is non-empty
- [ ] `synonym-table.json` has no self-referencing `approved == avoid` pairs
- [ ] All 4 system prompts exist and are non-empty
- [ ] No stale references to pre-enrichment pipeline stages (check for "TODO", "TBD", "placeholder")
- [ ] All system prompts reference terms from the canonical synonym table
- [ ] Validation scripts (5a-5e) all pass with exit code 0

## FAILURE RECOVERY

If any step fails, do NOT silently continue. Follow the recovery protocol for that step.

### Recovery: Rule Population (Step 1)

| Failure | Recovery |
|---------|----------|
| Adapted file `a-secN-ruleX.Y.md` does not exist | Log missing rule to `SCE/compute/logs/missing-rule-{id}.json`. Skip this rule. Continue with remaining rules. |
| Adapted file is empty (0 bytes) | Log empty file to `SCE/compute/logs/skip-empty-{id}.json`. Skip. |
| Adapted file frontmatter is unparseable YAML | Log parse error. Assign default frontmatter from the Assignment Table. Flag with `"inferred": true`. |
| Rule ID pattern does not match schema regex | Normalize: `Rule 1.1` → `rule-1.1`, `GR-1` → `gr-1`. If unable to normalize, skip and log. |
| Principle cannot be inferred | Default to the section's primary principle (see Principle Mapping table). Flag with `"principle-inferred": true`. |

### Recovery: Vocabulary Extraction (Step 2)

| Failure | Recovery |
|---------|----------|
| `master.md` is not readable | Abort step 2. Do not populate vocabulary files. |
| Dictionary entry missing `meaning` field | Look up in `ste-code/refined/`. If still absent, set `"meaning": "TBD"`. |
| Entry tagged both APPROVED and UNAPPROVED across sources | Prefer `ste-code/refined/` (100.0 audit). If still conflicting, prefer APPROVED. |
| Multiple conflicting approved alternatives | Prefer the shorter approved word. Flag longer alternatives in `"notes"`. |

### Recovery: Synonym Table (Step 3)

| Failure | Recovery |
|---------|----------|
| Entry maps `"approved" == "avoid"` (self-reference) | Skip this pair. Log to `SCE/compute/logs/skip-self-ref.json`. |
| Duplicate `approved` keys with different `avoid` lists | Merge the `avoid` arrays. Deduplicate. |
| Synonym table schema validation fails | Fix one violation at a time. Re-validate after each fix. Max 5 retries, then flag for manual review. |

### Recovery: System Prompts (Step 4)

| Failure | Recovery |
|---------|----------|
| Source artifact is missing | Skip that prompt. Generate remaining 3. Log which prompt was skipped. |
| Token count exceeds target | Truncate non-principle content first. Remove examples before removing rules. |
| Prompt references stale terms | Replace with canonical terms from `synonym-table.json`. |

### Recovery: Validation (Step 5)

| Failure | Recovery |
|---------|----------|
| Schema validation fails | Read the error message. Fix the specific violation. Re-run validation. Max 3 retries per file. |
| After 3 retries, still failing | Log the file, the schema error, and the current state. Flag for manual review. Do NOT commit. |
| File count mismatch | Print `diff` between expected and actual. List missing files by name. |
| `jsonschema` module not installed | Run `pip3 install jsonschema pyyaml`. Retry validation. |

### Recovery: Commit (Step 6)

| Failure | Recovery |
|---------|----------|
| Git not in clean state | Run `git status`. If unrelated changes exist, warn but proceed. If SCE has uncommitted changes, stash first. |
| Push rejected (non-fast-forward) | Run `git pull --rebase`. Retry push. |

## Populated Rule Example (reference)

Complete example of a populated `SCE/core/rules/rule-1.1.md`:

```markdown
---
id: rule-1.1
section: 1
principle: P1
title: Use Approved Words, Technical Nouns, or Technical Verbs
constraint-type: vocabulary
scope: [noun, verb, adjective]
severity: blocking
agentic-load: required
domain: [documentation, comments, error-messages, commit-messages]
related-rules: [rule-1.2, rule-1.3, rule-1.4, rule-1.5, rule-1.6]
anti-patterns:
  - Using unapproved synonyms (leverage → use, utilize → use)
  - Misclassifying technical nouns as unapproved words
  - Using obsolete dictionary entries
synonym-table: true
---

# Rule 1.1 - Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs

## Original Rule

**Rule 1.1** Use words that are:
- Approved in the dictionary
- Technical nouns
- Technical verbs.

## STE-Code Adaptation

In code documentation, apply this rule to:
- **Docstrings**: All words must be approved or technical code nouns/verbs
- **README files**: Use approved vocabulary for procedural instructions
- **Error messages**: All words must be approved (no slang in error text)
- **Commit messages**: Approved words for the subject line and body
- **Comments**: Inline and block comments follow approved vocabulary

### Examples

**Non-compliant:**
```
// This helper basically leverages the cache to speed things up
function getCached(key) { ... }
```

**STE-Code compliant:**
```
// Uses the cache to get the value faster.
// Falls back to the database if the key is not in the cache.
function getCached(key) { ... }
```

### Edge Cases

| Edge Case | Resolution |
|-----------|------------|
| Framework method name is unapproved word (e.g., `fetch`) | Use as-is in code; in documentation, prefer approved synonym ("get") |
| Domain-specific acronym (e.g., REST, JWT) | Classify as technical noun; document on first use |
| Word is APPROVED in STE but uncommon in code domain | Prefer the more common code-domain synonym; document the choice |
| Third-party library name uses banned word | Use the library name as-is (technical noun); do not rename |
| Approved word has different meaning in code context | Add a domain-specific entry in the vocabulary JSON with context notes |
```

### Example 2 - GR Rule (gr-1)

```markdown
---
id: gr-1
section: 9
principle: P2
title: The Conjunction "That"
constraint-type: grammar
scope: [sentence]
severity: warning
agentic-load: conditional
domain: [documentation, comments]
related-rules: [rule-3.1]
anti-patterns:
  - Omitting "that" after verbs like "make sure", "show", "recommend"
synonym-table: false
---

# GR-1 - The Conjunction "That"

## Original Rule

Use the conjunction "that" to connect new information in a subordinate clause
to a main clause. Use it after verbs such as "make sure," "show," and "recommend."

## STE-Code Adaptation

In code documentation, use "that" after verbs such as "make sure," "show,"
"recommend," "verify," and "confirm." This helps readers identify clause
boundaries and helps translation tools.

### Examples

**Non-compliant:**
```
Make sure the database connection is open before you run the query.
```

**STE-Code compliant:**
```
Make sure that the database connection is open before you run the query.
```
```

## Edge Cases (Pipeline-Wide)

| Edge Case | Resolution |
|-----------|------------|
| Adapted rule file exists but is empty (0 bytes) | Skip with warning; log to `SCE/compute/logs/skip-empty-{id}.json` |
| Frontmatter field `principle` cannot be inferred from rule text | Use the Principle Mapping table. Flag with `"principle-inferred": true`. |
| Dictionary entry has conflicting APPROVED/UNAPPROVED tags | Resolve from `ste-code/refined/` (100.0 audit) as source of truth |
| Rule ID pattern does not match schema regex | Normalize: `Rule 1.1` → `rule-1.1`, `GR-1` → `gr-1` |
| Vocabulary entry is missing `meaning` field | Look up in `ste-code/grouped/master.md`. If absent, add `"meaning": "TBD"`. |
| Synonym table entry maps to itself (no-op) | Skip and log; do not create self-referencing entries |
| System prompt exceeds target token count | Truncate least-common entries with `"priority": "low"` annotation |
| Adapted file count does not match expected 55 | Diff expected vs actual. List missing by name. Continue with what exists. |
| Multiple source files claim different approved alternatives for same unapproved word | Prefer the shorter word. Flag all alternatives in `"notes"`. |
| Rule frontmatter has properties not in the schema (`additionalProperties: false`) | Strip unknown properties before validation. Log what was stripped. |
| `pyyaml` or `jsonschema` modules not available | Run `pip3 install pyyaml jsonschema` before validation step |
| System prompt references rule IDs that do not exist | Cross-check against `SCE/core/rules/`. Remove dead references. |
| Vocabulary JSON exceeds 100MB (unlikely but possible from large dictionary) | Split into batches of 5,000 entries in `SCE/data/vocabulary/generated/`. |
| A GR rule file contains a `principle` reference to a P# that does not apply to grammar rules | All GR rules use P2. Override any inherited principle. |

## KEY FACTS
- 19 categories (NOT 22)
- 53 rules + 4 GR (NOT 65)
- Model: poolside/laguna-s-2.1:free
- Source: ASD-STE100 Issue 9, January 2025

## OUTPUT

All files written to `SCE/`. Commit with message "feat(sce): Regenerate SCE from enriched pipeline - 55 rules, full vocabulary, updated prompts". Push. Signal in `.agents/feedback/exchange.md`.

### Expected Output File Inventory

| File | Expected Count | Schema |
|------|---------------|--------|
| `SCE/core/rules/rule-*.md` | 53 | `rule-frontmatter.schema.json` |
| `SCE/core/rules/gr-*.md` | 4 | `rule-frontmatter.schema.json` |
| `SCE/data/vocabulary/approved-verbs.json` | 1 (multi-entry) | `vocabulary-entry.schema.json` |
| `SCE/data/vocabulary/approved-adjectives.json` | 1 (multi-entry) | `vocabulary-entry.schema.json` |
| `SCE/data/vocabulary/unapproved-entries.json` | 1 (multi-entry) | `vocabulary-entry.schema.json` |
| `SCE/core/categories/synonym-table.json` | 1 | `synonym-table.schema.json` |
| `SCE/narratives/system-prompts/ste-code-micro.md` | 1 | - |
| `SCE/narratives/system-prompts/ste-code-full.md` | 1 | - |
| `SCE/narratives/system-prompts/ste-code-agentic.md` | 1 | - |
| `SCE/narratives/system-prompts/ste-code-developer.md` | 1 | - |

## START NOW

1. Run pre-flight checks (P1-P5). Fix all failures before continuing.
2. Populate `SCE/core/rules/` from `ste-code/adapted/`.
3. Extract vocabulary from `ste-code/grouped/master.md`.
4. Regenerate system prompts from `ste-code/artifacts/`.
5. Run validation commands (5a-5e). Fix violations. Retry up to 3 times.
6. Verify the quality gate checklist.
7. Commit, push, signal in `.agents/feedback/exchange.md`.

## EMERGENCY SCHEMAS

If both primary and fallback schema files are missing, use these inline schemas to validate output.

### Inline: rule-frontmatter.schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "STE-Code Rule Frontmatter",
  "type": "object",
  "required": ["id", "section", "principle", "constraint-type", "scope", "severity", "agentic-load"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^(rule-[1-9]\\.[0-9]{1,2}|gr-[1-4])$"
    },
    "section": { "type": "integer", "minimum": 1, "maximum": 9 },
    "principle": { "type": "string", "pattern": "^P[0-9]{1,2}$" },
    "constraint-type": {
      "type": "string",
      "enum": ["vocabulary", "grammar", "structure", "format", "safety", "agentic"]
    },
    "scope": {
      "type": "array",
      "items": { "type": "string", "enum": ["noun", "verb", "adjective", "sentence", "paragraph", "document", "agent"] },
      "minItems": 1
    },
    "severity": { "type": "string", "enum": ["blocking", "warning", "advisory"] },
    "agentic-load": { "type": "string", "enum": ["required", "optional", "conditional"] },
    "domain": { "type": "array", "items": { "type": "string" } }
  },
  "additionalProperties": false
}
```

### Inline: vocabulary-entry.schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "STE-Code Vocabulary Entry",
  "type": "object",
  "required": ["term", "type", "category-id", "domain", "approved"],
  "properties": {
    "term": { "type": "string", "minLength": 1 },
    "type": { "type": "string", "enum": ["noun", "verb", "adjective", "preposition", "keyword"] },
    "category-id": { "type": ["integer", "null"], "minimum": 1 },
    "domain": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
    "approved": { "type": "boolean" },
    "source": { "type": "string" },
    "notes": { "type": "string" }
  },
  "additionalProperties": false
}
```

### Inline: synonym-table.schema.json

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "STE-Code Synonym Table Schema",
  "type": "object",
  "required": ["version", "entries"],
  "properties": {
    "version": { "type": "string" },
    "entries": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["non-ste", "approved", "type", "domain", "severity"],
        "properties": {
          "non-ste": { "type": "string" },
          "approved": { "type": "string" },
          "type": { "type": "string", "enum": ["verb", "noun", "adjective", "adverb", "preposition"] },
          "category": { "type": ["string", "null"] },
          "domain": { "type": "array", "items": { "type": "string" } },
          "severity": { "type": "string", "enum": ["blocking", "warning", "advisory", "approved"] },
          "note": { "type": "string" }
        }
      }
    }
  }
}
```
