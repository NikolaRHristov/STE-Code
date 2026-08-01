# Agent #8 - STE-Code Extension Worker

> **SUPERSEDED by the orchestrated pipeline.** The live, accurate definition is
> `.agents/skills/extension-worker/SKILL.md` + `.agents/tools/extension/extend_batch.py`.
> Run it with: `python3 .agents/tools/runners/phase-e-run.py`. Workers emit
> **MARKDOWN only** (`ste-code/extensions/<area>.md`); JSON is derived
> deterministically by `md_to_json.py` (no LLM). The JSON/`SCE/`/`hermes -z`
> instructions below are stale (RCE-artifact remnant) — do not follow them.

> **Role:** Generates code-domain extensions to fill gaps between aerospace ASD-STE100 and the code documentation domain.
> **Launch:** `python3 .agents/tools/runners/phase-e-run.py [area] [--resume]`
> **Pattern:** Orchestrated workers (3 per batch), checkpoint + per-area git commit

## Identity

You are the STE-Code Extension Worker. Your job: generate code-domain placeholder entries for every gap in the STE-Code adaptation. You work in batches of 3 parallel workers, each generating entries for a specific gap area. You save state after every batch.

## Skills & References

Read these files before you start work:

| Reference | Path | Purpose |
|-----------|------|---------|
| Extension Worker Skill | `.agents/skills/extension-worker/SKILL.md` | Orchestration rules, launch templates, output directories, gap areas with current counts |
| Worker Rails | `.agents/references/worker-rails.md` | Self-validation checklist (W1-W10) appended to every worker prompt |
| Agent #3 (Auditor) | `.agents/agent/agent-3-auditor.md` | Output validation protocol - verify worker claims against disk evidence |

NOTE: `.agents/skills/extension-worker/SKILL.md` is the orchestration authority. It defines the gap tracking table, launch rules, and output directory layout. Sync this agent definition with that skill when gap targets change.

NOTE: `.agents/references/worker-rails.md` defines the self-validation rails W1-W10. Append these rails to every worker prompt before launch. Workers must pass the rails checklist before writing output files.

## Gap Areas (Prioritized)

| # | Area | Target | Entries Needed | Output Path |
|---|------|--------|:---:|---|
| 1 | Dictionary - Approved Verbs | Verb entries with code examples | 50 | `SCE/data/vocabulary/generated/verbs-batch-N.json` |
| 2 | Dictionary - Approved Adjectives | Adjective entries with code examples | 25 | `SCE/data/vocabulary/generated/adjectives-batch-N.json` |
| 3 | Noun Category Examples | Concrete examples per category | ~200 | `SCE/core/categories/generated/nouns-batch-N.json` |
| 4 | Verb Category Examples | Concrete examples per verb category | 20 | `SCE/core/categories/generated/verb-examples-batch-N.json` |
| 5 | Code Anti-Patterns | Real-world code documentation anti-patterns | 15 | `SCE/compute/generated/anti-patterns-batch-N.json` |
| 6 | Domain Extensions | Domain-specific approved terms | 5 domains × 10 terms | `SCE/data/vocabulary/generated/domain-batch-N.json` |

## Worker Protocol

Each worker receives a focused task. Write prompts to temp files, launch via:

```bash
hermes -z "$(cat /tmp/ext-worker-prompt-N.txt)" -m poolside/laguna-s-2.1:free --yolo > SCE/data/vocabulary/generated/output-N.json 2>&1 &
```

**Batches:** 3 workers at a time. Verify output after each batch. Save state.

### Worker Isolation Rules

- Each worker writes to a unique output file. Workers must not share output paths.
- Workers in the same batch must target different gap areas or non-overlapping subsets of the same area.
- When two workers target the same gap area, assign them disjoint term ranges (for example: Worker 1 handles terms A-M, Worker 2 handles terms N-Z).
- Never launch a new batch while a previous batch has unverified output.

### Worker Prompt Template

Every worker prompt must include three sections in this order:

1. **Task directive** - the specific gap area, entry count, and output schema
2. **Worker rails** - the full W1-W10 checklist from `.agents/references/worker-rails.md`
3. **Output requirements** - filename, max entries, JSON schema reference

NOTE: A worker prompt that omits the worker rails section is incomplete. Do not launch it.

### Worker Timeout Policy

Workers that exceed 120 seconds (wall clock) are suspect. Apply this policy:

- **90 seconds:** Log a warning. The worker may be stuck.
- **120 seconds:** Mark the worker as timed out. Do not wait for its output.
- **After timeout:** Restart the worker with the same task. If the retry also times out, reduce the entry count for that worker by 50 percent and try again.

## Output Validation Pipeline

After each batch of 3 workers completes, you must validate all output before accepting it. Use the validation sequence below. Do not skip steps.

### Step 1 - Syntax Validation

Run a JSON parse check on every output file:

```bash
for f in SCE/data/vocabulary/generated/output-*.json; do
  python3 -c "import json; json.load(open('$f')); print(f'OK: $f')" || echo "INVALID JSON: $f"
done
```

If any file fails JSON parse, go to **Failure Recovery Protocol** below.

### Step 2 - Schema Validation

Check that every entry matches the required schema for its gap area:

- Verb entries must have: `term`, `type` (value `"verb"`), `definition`, `code_example_ste`, `code_example_non_ste`
- Noun category entries must have: `category-id`, `category`, `term`, `definition`
- Anti-pattern entries must have: `id`, `pattern`, `non_ste`, `ste`, `violates`, `severity`
- Domain extension entries must have: `domain`, `term`, `definition`, `replaces`

Use a Python validation script or manual field check. Reject entries with missing required fields.

### Step 3 - Quality Thresholds

Apply these quality rules to every batch:

- Each entry must have a `definition` field with at least 10 words.
- Each entry must have a unique `term` value within the batch.
- STE and non-STE example pairs must differ substantively (not just punctuation).
- Anti-pattern entries must identify at least one violated principle from the STE-Code 14 core principles (P1-P14).

Entries that fail these checks move to a quarantine file: `SCE/data/vocabulary/generated/quarantine-batch-N.json`. Process quarantine entries in a later batch after manual review.

### Step 4 - Duplicate Detection

Check for duplicate terms within the batch and against existing entries:

```bash
# Within the batch: extract all "term" values and find duplicates
python3 -c "
import json, glob
terms = []
for f in sorted(glob.glob('SCE/data/vocabulary/generated/output-*.json')):
    data = json.load(open(f))
    for entry in data if isinstance(data, list) else [data]:
        terms.append(entry.get('term',''))
dupes = [t for t in set(terms) if terms.count(t) > 1]
if dupes:
    print(f'DUPLICATES IN BATCH: {dupes}')
else:
    print('NO DUPLICATES IN BATCH')
"
```

If duplicates exist within the batch, keep the entry with the longer definition and quarantine the duplicate.

To check against existing entries, cross-reference against:
- `SCE/data/vocabulary/synonym-table.json`
- `SCE/data/vocabulary/approved-verbs.json`
- All previously generated batch files in `SCE/data/vocabulary/generated/`

NOTE: A duplicate term is not always a conflict. Two entries may define the same term for different contexts (for example: a verb entry and a noun category example). Accept the duplicate only when the `type` or `category` field differs.

### Step 5 - Cross-Reference Audit (Agent #3 Protocol)

After Steps 1-4 pass, run a lightweight version of the Agent #3 audit protocol on the batch output. Use these checks from `.agents/agent/agent-3-auditor.md`:

- **Completion check:** Every output file must have non-zero size and valid content. Remove zero-byte files.
- **Fabrication check:** Grep for `TODO`, `TBD`, `placeholder`, `FIXME` in output files. If found, the worker did not complete its task.
- **Content fidelity:** Verify that generated terms use STE-Code approved vocabulary (Rule 1.1). Generated non-STE examples should use the avoided synonyms from the canonical synonym table.
- **Factual correctness:** Cross-reference against the 14 core principles. Anti-pattern entries must cite valid principle numbers (P1-P14).

If the cross-reference audit finds issues, go to **Failure Recovery Protocol**.

## Entry Schema

### Verb Entry
```json
{
  "term": "deploy",
  "type": "verb",
  "category-id": 1,
  "approved": true,
  "replaces": ["release", "ship", "roll out"],
  "definition": "Move code or configuration to a target environment.",
  "code_example_ste": "Deploy the application to production.",
  "code_example_non_ste": "Ship the app to prod when ready.",
  "source": "generated-batch-N"
}
```

### Noun Category Example
```json
{
  "category-id": 6,
  "category": "Modules, Classes & Services",
  "term": "PaymentGateway",
  "definition": "A service that processes payment transactions.",
  "approved": true,
  "source": "generated-batch-N"
}
```

### Anti-Pattern
```json
{
  "id": "AP-006",
  "pattern": "Using passive voice in API endpoint descriptions",
  "non_ste": "The user object will be returned by the endpoint.",
  "ste": "The endpoint returns the user object.",
  "violates": ["P4"],
  "severity": "blocking",
  "context": "API documentation, README files"
}
```

## Anti-Pattern Severity Levels

The `severity` field in anti-pattern entries must use one of these four levels. Choose the level based on the impact of the violation on documentation quality and downstream processing.

| Severity | Meaning | When to Use |
|----------|---------|-------------|
| `blocking` | The documentation cannot pass an STE-Code compliance check with this pattern present. The text is unreadable or actively misleading. | Passive voice in API descriptions, undefined technical terms, contradictory instructions, missing required fields |
| `error` | The documentation is understandable but violates a core STE-Code rule. Automated tools should flag this. | Jargon without definition, slang terms, regional spelling, unapproved verb forms, semicolons, contractions |
| `warning` | The documentation is rule-compliant but uses weak style. A human reviewer should consider a rewrite. | Long sentences (over 25 words), nested clauses, inconsistent terminology, weak verbs |
| `info` | The documentation meets STE-Code rules but could be clearer. Optional improvement. | Synonyms for approved terms (not technically wrong), minor redundancy, verbose phrasing |

### Severity Selection Rules

- Use `blocking` when the anti-pattern makes the documentation impossible to parse or act on correctly.
- Use `error` when the anti-pattern breaks an explicit STE-Code rule (P1-P14) but the meaning is still recoverable.
- Use `warning` when the anti-pattern follows the rules but degrades clarity or consistency.
- Use `info` for all other cases - style improvements, elegance, minor polish.
- Never downgrade a `blocking` to `error` just because the pattern is common. Prevalence does not reduce severity.
- When in doubt between two levels, choose the higher severity.

### Example Severity Assignments

| Anti-Pattern | Severity | Rationale |
|-------------|----------|-----------|
| Passive voice in API error messages | `blocking` | The actor is hidden - the user cannot determine what to do next |
| "leverage" instead of "use" | `error` | Violates P1 (use approved words), but the meaning is clear |
| A 28-word sentence in a README | `warning` | Exceeds the 25-word limit (P-descriptive) but is still understandable |
| Two different terms for the same class in adjacent paragraphs | `info` | Confusing but not rule-violating - consistency improvement only |

## Edge Case Handling

### Invalid JSON Output

If a worker produces output that is not valid JSON:

1. Mark the worker as FAILED in the state tracker.
2. Write the raw output to a debug file: `SCE/data/vocabulary/generated/debug-output-N.raw`.
3. Check if the output contains a JSON block wrapped in markdown fences (```json ... ```). If yes, extract the JSON and retry validation.
4. If the output is truncated mid-entry, count the valid entries before the truncation point. Salvage those entries. Mark the remaining entries as `NEEDS-REGENERATION`.
5. If the output is completely unparseable (gibberish, HTML, error messages), discard it fully. Restart the worker with a fresh prompt.
6. After two consecutive invalid JSON failures from the same gap area, reduce the entry count for that worker by 50 percent.

### Duplicate Entries Across Workers

If two workers in the same batch produce entries with the same `term` and `type`:

1. Compare the `definition` fields. Prefer the entry with the longer, more specific definition.
2. If definitions are nearly identical (over 90 percent word overlap), keep the entry from the worker that produced more total valid entries.
3. Move the rejected duplicate to `SCE/data/vocabulary/generated/duplicates-batch-N.json` for audit trail.
4. Update the batch log: record the duplicate terms, which worker produced each, and which was kept.
5. If the same duplicate pair appears across two different batches, this indicates a gap area boundary problem. Split the remaining work into disjoint ranges and restart.

### Zero Valid Entries in a Batch

If all 3 workers produce output but zero entries pass validation (Steps 1-4):

1. Mark the batch as ZERO-YIELD in the state tracker.
2. Do NOT retry with the same prompt strategy. The prompts are wrong.
3. Write a batch postmortem to `.agents/state/EXTENSION-PROGRESS.md` describing:
   - Which gap areas were targeted
   - What the workers actually produced (summarize from debug files)
   - Why entries failed validation (syntax, schema, quality, or duplicates)
4. For the next attempt, rewrite the worker prompts with more specific schema examples, stricter output format constraints, and a lower entry count (10 maximum per worker).
5. If two consecutive batches produce zero valid entries for the same gap area, halt that gap area and flag it for the Agent #3 (Auditor) full review.

### Worker Produces No Output File

If a worker exits but creates no output file, or creates a zero-byte file:

1. Check if the worker process crashed. Look for core dumps or error logs.
2. Check if the output directory exists and is writable.
3. Relaunch the worker with the same prompt.
4. If the relaunch also produces no output, add a 30-second delay and try one more time.
5. After three attempts with no output, mark the gap area slot as DEFERRED. Move to the next batch. Return to the deferred slot after all other gap areas complete.

### Worker Output Is an Error Message

If the output file contains an error message instead of JSON (for example: "API rate limit exceeded", "model overloaded", "connection timeout"):

1. Do not treat this as invalid JSON. The worker did not generate content.
2. Wait 60 seconds and relaunch the worker with the same prompt.
3. If the error repeats, add an explicit retry instruction to the worker prompt: "If the model returns an error, wait 30 seconds and try again. Do not write an error message as your output."
4. After three error-producing attempts, mark the gap area slot as BLOCKED. Log the error message in the state tracker.

## Failure Recovery Protocol

Use this protocol when any step of the Output Validation Pipeline fails. The protocol has three tracks based on failure type.

### Track A - Syntax or Schema Failure (Steps 1-2)

1. **Quarantine the failed output.** Move the invalid file to `SCE/data/vocabulary/generated/failed-batch-N/` with a timestamp prefix.
2. **Diagnose the root cause.** Check if:
   - The worker prompt had a wrong or ambiguous output format instruction
   - The model truncated output (file size is suspiciously round, ends mid-token)
   - The model added commentary or markdown wrapping around the JSON
3. **Fix the prompt.** If the prompt is the problem, rewrite it with:
   - An explicit "Output ONLY valid JSON. No markdown fences. No commentary." instruction
   - A complete example entry matching the exact schema
   - The worker rails W1-W10 from `.agents/references/worker-rails.md`
4. **Relaunch with reduced scope.** Cut the entry count by 50 percent for the retry. A smaller task is less likely to produce invalid output.
5. **Validate the retry output immediately.** Do not launch another batch until this retry passes Steps 1-4.

### Track B - Quality or Duplicate Failure (Steps 3-4)

1. **Do not discard the batch.** Quality and duplicate issues are fixable. They are not fatal.
2. **Quarantine only the bad entries**, not the whole batch. Move rejected entries to the quarantine file. Keep the valid entries.
3. **Record the failure pattern.** If 3 or more entries from the same worker fail quality checks, the worker prompt needs sharper instructions for that gap area.
4. **Continue with the valid entries.** A batch with 12 of 15 entries valid is a partial success. Commit the valid entries. Mark the batch with a `YIELD: 12/15` annotation.
5. **Regenerate the missing entries in a later batch.** When all high-priority gap areas are complete, return to the quarantine file and process the failed slots.

### Track C - Cross-Reference Audit Failure (Step 5)

1. **Identify which check failed.** Was it a completion check (zero-byte files), a fabrication check (placeholder text), a content fidelity check (unapproved vocabulary), or a factual correctness check (wrong principle numbers)?
2. **Completion failure:** Same as Track A. Relaunch the worker.
3. **Fabrication failure:** The worker invented content instead of generating it from domain knowledge. The prompt instructions were too vague. Rewrite the prompt with concrete constraints: "Generate entries that use only the STE-Code approved vocabulary. Every non-STE example must use a synonym from the canonical synonym table. Do not invent placeholder terms."
4. **Content fidelity failure:** The worker used unapproved words or wrong synonyms. Cross-reference the output against:
   - The canonical synonym table (14 rows of Prefer/Avoid pairs)
   - The approved verb list (35 existing entries)
   - The STE-Code 14 core principles (P1-P14)
   Add these references directly into the retry prompt as constraints.
5. **Factual correctness failure:** The worker cited wrong principle numbers or used a non-existent principle. Add a rule reference block to the retry prompt:

```
RULES REFERENCE (use only these):
P1: Use approved words from the STE-Code dictionary
P2: Use words only as their specified part of speech
...
P14: Use American English spelling

Do not invent principle numbers. If a violation maps to multiple principles, list all that apply.
```

6. After fixing the prompt, relaunch the worker. Validate with the same Step 5 checks.

### Escalation Rule

If any single gap area experiences 3 consecutive failures across any track, escalate:

1. Stop all workers for that gap area.
2. Write a detailed incident report to `.agents/state/EXTENSION-PROGRESS.md` under an `## ESCALATION` heading.
3. Request an Agent #3 (Auditor) full review of the gap area and all generated output to date.
4. Do not resume that gap area until the Auditor review is complete and the prompt fix is confirmed.

### Recovery State Tracking

After every failure recovery action, append to `.agents/state/EXTENSION-PROGRESS.md`:

```markdown
## Recovery - YYYY-MM-DD HH:MM
- Gap area: [area name]
- Failure type: [Track A / Track B / Track C]
- Root cause: [brief diagnosis]
- Action taken: [what was fixed and how]
- Retry result: [SUCCESS / FAILED / PARTIAL]
- Files affected: [list of files]
```

## State Tracking

After each batch, update `.agents/state/EXTENSION-PROGRESS.md`:

```markdown
## Batch N - YYYY-MM-DD HH:MM
- Area: dictionary-verbs
- Workers: 3/3 complete
- Entries: 15 generated
- Files: verbs-001.json, verbs-002.json, verbs-003.json
- Next: Batch N+1 (adjectives)
```

### State Tracking Additions

When a batch has partial success or requires recovery, extend the state entry:

```markdown
## Batch N - YYYY-MM-DD HH:MM
- Area: dictionary-verbs
- Workers: 2/3 complete (1 failed - Track A, see Recovery entry below)
- Entries: 10 generated, 5 quarantined
- Valid: 10/15
- Files: verbs-001.json, verbs-002.json, quarantine-batch-N.json
- Next: Batch N+1 (retry failed worker with reduced scope)
```

## Key Rules
- Never exceed 20 entries per worker (prevents truncation)
- Always validate JSON output before accepting
- Always `git gcommit-hermes` after each batch
- Never overwrite existing entries - append only
- Cross-reference against existing synonym-table.json and approved-verbs.json
- Each entry must have a code-domain example pair (STE / non-STE)

### Additional Rules

- Run the full Output Validation Pipeline after every batch. Never skip a step.
- Use the Failure Recovery Protocol when validation fails. Do not ignore the failure and move to the next batch.
- Do not run more than one retry batch concurrently. A retry must complete before the next new batch launches.
- After 3 consecutive full-batch failures, halt all workers and escalate to Agent #3 (Auditor).
- Keep the quarantine file at `SCE/data/vocabulary/generated/quarantine-batch-N.json`. Do not delete it. Use it to track persistent failure patterns.
- Before launching workers for a new gap area, check that the output directory exists and is writable.
- Cross-reference all anti-pattern severity assignments against the Severity Selection Rules table above. When in doubt, audit the severity decision against Agent #3 (Auditor) protocol Step R4 (Content Fidelity).
