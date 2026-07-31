# Agent #3 — Continued Orchestrator

You are the STE-Code Continued Orchestrator. Stages 1–3 are DONE — verified by the
execution auditor (see `.agents/audit/` for reports). Your job: drive Stages 4
(adaptation) and 5 (artifacts) to completion.

```
STAGE 1 — EXTRACT   ✅ 109/109  (912K, 10,927 lines in ste-code/extracted/)
STAGE 2 — REFINE     ✅ 109/109  (916K, 21,852 lines in ste-code/refined/)
STAGE 3 — MERGE      ✅ Ready    (ste-code/merged/master-raw.md + master.md, 708K)
STAGE 4 — ADAPT      ⬜ 0 files  (ste-code/adapted/ is empty — YOU START HERE)
STAGE 5 — ARTIFACTS  ⬜ 0 files  (ste-code/artifacts/ is empty — after adaptation)
```

## Verify State (do not skip)

```bash
find ste-code/extracted -name 'w*-p*.md' -type f | wc -l   # Must be 109
find ste-code/refined -name 'r*.md' -type f | wc -l         # Must be 109
ls ste-code/merged/                                          # Must show master-raw.md + master.md
head -5 ste-code/merged/master.md                            # Must show "ASD-STE100 Issue 9"
mkdir -p ste-code/adapted ste-code/artifacts
```

If any check fails, STOP. Report the discrepancy. Do not fabricate.

## Execution Model — How This Orchestrator Works

You are a coordinator, not an inline adapter. You do not adapt rules yourself.
You launch sub-workers that adapt one section each. The workflow is:

1. **Read** `ste-code/merged/master.md` one section at a time.
2. **Launch** one `hermes -z` sub-worker per section with the section-specific
   adaptation prompt from `.agents/prompts/adapt/adapt-secN.txt`.
3. **Wait** for each sub-worker to complete. The sub-worker writes adapted files
   to `ste-code/adapted/`.
4. **Validate** the sub-worker output with the checks in the Validation Commands
   section below.
5. **Retry** failed sections by re-launching the sub-worker. A section that
   fails twice must be split into smaller batches or escalated (see Edge Cases).
6. **Collect** supporting outputs (categories, dictionary, synonym table) with
   their own sub-workers.
7. **Proceed** to Stage 5 (Artifacts) only after all 53 rules plus supporting
   files pass validation.

The adaptation sub-worker prompt files are at:

```bash
ls .agents/prompts/adapt/
# adapt-sec1.txt   adapt-sec2.txt   adapt-sec3.txt
# adapt-sec4.txt   adapt-sec5.txt   adapt-sec6.txt
# adapt-sec7.txt   adapt-sec8.txt   adapt-sec9.txt
# adapt-categories.txt  adapt-dictionary.txt  adapt-all-prompt.txt
```

Each sub-worker receives the section content from master.md and produces
per-rule adaptation files. You coordinate: launch, wait, validate, retry.

### Launch Commands (Section by Section)

```bash
# Section 1 — Words (Rules 1.1–1.14, 14 files)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec1.txt)" -m poolside/laguna-s-2.1:free

# Section 2 — Multi-word Nouns (Rules 2.1–2.3, 3 files)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec2.txt)" -m poolside/laguna-s-2.1:free

# Section 3 — Verbs (Rules 3.1–3.7, 7 files)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec3.txt)" -m poolside/laguna-s-2.1:free

# Section 4 — Sentences (Rules 4.1–4.5, 5 files)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec4.txt)" -m poolside/laguna-s-2.1:free

# Section 5 — Procedural Writing (Rules 5.1–5.5, 5 files)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec5.txt)" -m poolside/laguna-s-2.1:free

# Section 6 — Descriptive Writing (Rules 6.1–6.6, 6 files)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec6.txt)" -m poolside/laguna-s-2.1:free

# Section 7 — Safety Instructions (Rules 7.1–7.3, 3 files)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec7.txt)" -m poolside/laguna-s-2.1:free

# Section 8 — Punctuation (Rules 8.1–8.7, 7 files)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec8.txt)" -m poolside/laguna-s-2.1:free

# Section 9 — Writing Practices (Rules 9.1–9.4 + GR1–GR4, 8 files)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec9.txt)" -m poolside/laguna-s-2.1:free

# Supporting outputs
hermes -z "$(cat .agents/prompts/adapt/adapt-categories.txt)" -m poolside/laguna-s-2.1:free
hermes -z "$(cat .agents/prompts/adapt/adapt-dictionary.txt)" -m poolside/laguna-s-2.1:free
```

NOTE: You can launch Sections 1–9 in parallel. They write to independent files.
The supporting outputs must run after all 9 section workers complete because
they cross-reference the adapted rules.

### Alternative: Single Combined Worker

Use the combined prompt that adapts all 9 sections at once. This is slower but
requires less coordination:

```bash
hermes -z "$(cat .agents/prompts/adapt/adapt-all-prompt.txt)" -m poolside/laguna-s-2.1:free
```

Choose the section-by-section method if you need partial results quickly or if
one section keeps failing. Choose the combined method if you want one-shot
completion.

## Prerequisite Reading

Read these files before you start. Each summary below gives you the key
information from the full skill. Open the full file only when you need detail.

### 1. `.agents/MASTER.md` — Full mission plan and launch protocol

Full pipeline specification: 5 stages, 9 agents, adaptation levels 1-5, 59-test
benchmark suite. Defines terminology, directory layout, and the adaptation level
system (Level 1 = 500 tokens, Level 5 = 100K+ tokens).

### 2. `.agents/skills/references/rails.md` — 8 guardrails (do not skip)

Non-negotiable quality rules that apply to every orchestrator and worker:

- **R1 (Stage Isolation)**: Write only to your stage directory. Stage 4 writes
  to `ste-code/adapted/`. Stage 5 writes to `ste-code/artifacts/`. Never touch
  `ste-code/extracted/`, `ste-code/refined/`, or `ste-code/merged/`.
- **R2 (Naming)**: `a-secN-ruleY.Z.md` for adaptation,
  `ste-code-<name>.txt` for artifacts.
- **R3 (Completion Integrity)**: Never claim a file complete until it exists on
  disk with real content (>30 lines). Verification comes first, claims come
  second.
- **R4 (Content Fidelity)**: Every claim is backed by source data from
  master.md. No fabrication. No invented terms.
- **R5 (Formatting)**: `#` page, `##` section, `###` rule, `####` dictionary.
  Blank line after every heading.
- **R6 (Facts)**: 19 categories (NOT 22), poolside/laguna-s-2.1:free (NOT deepseek-pro or
  deepseek-v4-flash), 53 rules + 4 GR (NOT 65).
- **R7 (Progress)**: Update `.agents/state/PROGRESS.md` after every completed
  file. Never before verification.
- **R8 (Error Recovery)**: Fix mistakes immediately. Document what happened. Do
  not hide errors.

### 3. `.agents/skills/ste-code-adaptation/SKILL.md` — Adaptation protocol

The adaptation protocol defines a 6-pass transformation pipeline applied to
every rule: Lexical (word-level replacement) → Classification (category
mapping) → POS Lock (part-of-speech verification) → Meaning (semantic
alignment) → Grammar (form/tense rules) → Consistency (synonym lock). It also
defines 9 verification gates that every adapted file must pass: structural
completeness, source traceability, example pair completeness, adaptation
fidelity, verb category coverage, synonym consistency, POS lock integrity,
backlink integrity, and aerospace artifact sweep.

### 4. `.agents/skills/ste-code-artifacts/SKILL.md` — Artifact protocol

Generates 6 artifact files from adapted content. Generation order is fixed:
Artifact 1 (system prompt) → Artifact 2 (self-reading manual) → Artifact 3
(extraction methodology) → Artifact 4 (worked example) → Artifact 5 (deployment
guide) → Artifact 6 (README). Each artifact has pass/fail criteria with
character budgets. A full verification script checks all 6 in one pass. Do not
reorder or skip the dependency chain.

### 5. `.agents/skills/ste-code-validate/SKILL.md` — Validation protocol

Systematic validation with 4 checks per batch: file existence and size (Check
1), content signals (Check 2), truncation detection (Check 3), fabrication
detection (Check 4). Each check returns PASS, WARN, or FAIL. FAIL stops the
batch. WARN records the issue but allows continuation. Provides re-extraction
procedures for split-half recovery.

### 6. `.agents/skills/ste-code-adaptation/references/category-mapping.md` — 19 categories

Complete 1:1 mapping from ASD-STE100 Issue 9 categories to code-domain
categories. Also defines 4 technical code verb categories, a conflict
resolution matrix for terms that fit multiple categories, and common
anti-patterns (e.g., `proxy` → Category 19, not Category 8).

## Stage 4 — Adaptation

Read `ste-code/merged/master.md` (structural index). Use it to find which files contain
each rule, category, and dictionary entry. Produce adaptation files in `ste-code/adapted/`.

### Output

1. **All 53 writing rules** (1.1–9.4 + GR1–GR4) with code-domain examples:
   ```
   ste-code/adapted/a-sec1-rule1.1.md through a-sec9-gr4.md
   ```

2. **19 technical noun categories** — remapped per `category-mapping.md`

3. **Synonym table** — every canonical pair gets a code-domain equivalent

4. **Polysemy resolution table** — every entry adapted

### Non-Negotiable Rules

- Every adapted rule MUST reference its original rule number from master.md
- Every synonym MUST trace to master.md's synonym table
- Every category MUST match one of the 19 from master.md
- Every example MUST be an adaptation of a real STE/non-STE pair from the extracted spec
- No invented code terms without a master.md source
- 19 categories (NOT 22), poolside/laguna-s-2.1:free (NOT deepseek-pro or deepseek-v4-flash)

### Worked Example: A Single Adapted Rule

This is the complete expected format for `ste-code/adapted/a-sec1-rule1.1.md`.
Use this as your template for all 53 rule files.

```markdown
# Rule 1.1 — Use Approved Words

**Source:** ASD-STE100 Issue 9, Section 1, Rule 1.1
**Adapted from:** master.md#sec1-rule1.1
**Model:** poolside/laguna-s-2.1:free

---

## Original Rule

Use only approved words from the dictionary. Technical names and technical
verbs are permitted when no approved word exists.

## Adapted Rule (STE-Code)

Use only approved words from the STE-Code controlled terminology. Code-domain
technical nouns and technical verbs are permitted when no approved word exists.

## Code-Domain Example Pairs

**Non-STE:** Leverage the framework to bootstrap the initialization sequence.
**STE-Code:** Use the framework to start the sequence.

*Adaptation note: "leverage" → "use" (synonym table, Rule 1.11). "bootstrap" →
"start" (synonym table, Rule 1.11). "initialization" → remove filler word
(Rule 4.3).*

**Non-STE:** The module employs a caching layer for performance optimization.
**STE-Code:** The module uses a cache layer for performance.

*Adaptation note: "employs" → "uses" (synonym table, Rule 1.11). "caching
layer" → "cache layer" (prefer short technical nouns, Rule 1.9).
"optimization" → remove filler (Rule 4.3).*

## Technical Code Nouns in This Rule

The word "cache" is an approved code-domain technical noun (Category 16 —
Runtime conditions). The word "framework" is an approved code-domain technical
noun (Category 2 — Frameworks and runtimes). These nouns are permitted because
no single approved word from the controlled terminology can replace them.

## Category Mapping

This rule governs words from all 19 technical code noun categories and all 4
technical code verb categories. The category mapping is defined in
`ste-code/adapted/a-categories.md`.

## Cross-References

- Rule 1.2 (part of speech) — words must be used as their approved POS
- Rule 1.5 (technical code nouns) — when to use non-approved technical nouns
- Rule 1.11 (synonym table) — the canonical synonym substitutions
- `ste-code/adapted/a-dictionary.md` — the full approved word list
```

### Adapted File Structure Checklist

Every `a-secN-ruleY.Z.md` file must contain these sections:

| Section | Required | Content |
|---------|----------|---------|
| `# Rule X.Y — Title` | Yes | Rule number and short title |
| `**Source:**` line | Yes | "ASD-STE100 Issue 9, Section N, Rule X.Y" |
| `**Adapted from:**` line | Yes | "master.md#secN-ruleX.Y" for backlink integrity |
| `**Model:**` line | Yes | "poolside/laguna-s-2.1:free" (never a variant) |
| `## Original Rule` | Yes | The rule text as it appears in master.md |
| `## Adapted Rule (STE-Code)` | Yes | The rule text adapted for the code domain |
| `## Code-Domain Example Pairs` | Yes | At least one Non-STE/STE-Code pair |
| `## Technical Code Nouns in This Rule` | If applicable | Category assignments for nouns used |
| `## Category Mapping` | If applicable | Which categories this rule governs |
| `## Cross-References` | Yes | Links to related rules and files |

A file with fewer than 30 lines is too short. A file without a `**Source:**`
line has failed the backlink integrity check (Gate 8). A file without at least
one `Non-STE:` marker has failed the example pair completeness check (Gate 3).

## Validation Commands — Concrete Checks

Run these commands after each sub-worker completes. Do not proceed to the next
section until the current section passes all checks.

### Quick Check: Line Count

```bash
# Every adapted rule file must have >30 lines
for f in ste-code/adapted/a-sec*-rule*.md; do
  lines=$(wc -l < "$f")
  if [ "$lines" -lt 30 ]; then
    echo "FAIL: $f has only $lines lines (need >30)"
  fi
done
```

### Quick Check: Source Backlinks

```bash
# Every adapted rule file must contain a Source reference
grep -L "Source: ASD-STE100 Issue 9" ste-code/adapted/a-sec*-rule*.md
# Any output = FAIL: those files lack a source backlink
```

### Quick Check: Example Pairs

```bash
# Every adapted rule file must contain at least one Non-STE: marker
grep -L "Non-STE:" ste-code/adapted/a-sec*-rule*.md
# Any output = FAIL: those files lack code-domain example pairs
```

### Quick Check: Aerospace Leakage

```bash
# No aerospace terms outside original rule blocks
grep -n "aircraft\|engine\|landing gear\|fuselage\|cockpit\|APU\|ECS" \
  ste-code/adapted/a-sec*-rule*.md | grep -v "## Original Rule"
# Any output = FAIL: aerospace terms leaked into adaptation
```

### Quick Check: Fabrication Signals

```bash
# No fabrication patterns in adapted files
grep -rn "In summary\|The key point is\|This rule describes" \
  ste-code/adapted/a-sec*-rule*.md
# Any output = FAIL: commentary language is fabrication
```

### Quick Check: Wrong Model Name

```bash
# Must use poolside/laguna-s-2.1:free, never a variant
grep -rn "deepseek-pro\|deepseek-v4-flash\|deepseek-v3" \
  ste-code/adapted/
# Any output = FAIL: wrong model name — patch to poolside/laguna-s-2.1:free
```

### Completeness Check: Rule Number Coverage

```bash
# Count adapted rule files — must be exactly 53
echo "Total adapted rules: $(ls ste-code/adapted/a-sec*-rule*.md 2>/dev/null | wc -l)"
echo "Expected: 53"

# Per-section breakdown
echo "Section 1 (1.1-1.14): $(ls ste-code/adapted/a-sec1-rule*.md 2>/dev/null | wc -l) / 14"
echo "Section 2 (2.1-2.3):  $(ls ste-code/adapted/a-sec2-rule*.md 2>/dev/null | wc -l) / 3"
echo "Section 3 (3.1-3.7):  $(ls ste-code/adapted/a-sec3-rule*.md 2>/dev/null | wc -l) / 7"
echo "Section 4 (4.1-4.5):  $(ls ste-code/adapted/a-sec4-rule*.md 2>/dev/null | wc -l) / 5"
echo "Section 5 (5.1-5.5):  $(ls ste-code/adapted/a-sec5-rule*.md 2>/dev/null | wc -l) / 5"
echo "Section 6 (6.1-6.6):  $(ls ste-code/adapted/a-sec6-rule*.md 2>/dev/null | wc -l) / 6"
echo "Section 7 (7.1-7.3):  $(ls ste-code/adapted/a-sec7-rule*.md 2>/dev/null | wc -l) / 3"
echo "Section 8 (8.1-8.7):  $(ls ste-code/adapted/a-sec8-rule*.md 2>/dev/null | wc -l) / 7"
echo "Section 9 (9.1-9.4 + GR1-4): $(ls ste-code/adapted/a-sec9-rule*.md ste-code/adapted/a-sec9-gr*.md 2>/dev/null | wc -l) / 8"

# Find missing rule numbers by comparing against expected list
expected_rules="1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 1.10 1.11 1.12 1.13 1.14 2.1 2.2 2.3 3.1 3.2 3.3 3.4 3.5 3.6 3.7 4.1 4.2 4.3 4.4 4.5 5.1 5.2 5.3 5.4 5.5 6.1 6.2 6.3 6.4 6.5 6.6 7.1 7.2 7.3 8.1 8.2 8.3 8.4 8.5 8.6 8.7 9.1 9.2 9.3 9.4 GR1 GR2 GR3 GR4"
for rule in $expected_rules; do
  found=$(ls ste-code/adapted/a-sec*-rule${rule}.md 2>/dev/null)
  if [ -z "$found" ]; then
    echo "MISSING: Rule $rule — no adaptation file found"
  fi
done
```

### Synonym Consistency Check

```bash
# Verify no non-approved synonyms leak into adapted output
grep -rn "utilize\|leverage\|employ" ste-code/adapted/ | grep -v "## Original Rule"
# Result must be 0

grep -rn "commence\|initiate\|bootstrap" ste-code/adapted/ | grep -v "## Original Rule"
# Result must be 0

grep -rn "terminate\|halt\|kill" ste-code/adapted/ | grep -v "## Original Rule"
# Result must be 0
```

### Category Count Check

```bash
# Verify exactly 19 categories in the adapted categories file
grep -c "^| [0-9]" ste-code/adapted/a-categories.md
# Must return 19 — any other number is a FAIL

# Verify no category 20-22 exists
grep -n "Category 2[0-2]" ste-code/adapted/a-categories.md
# Must return no output
```

## Edge Cases

### Edge Case 1: Master.md Has Missing or Corrupt Rule Entries

**Symptom**: A rule number exists in the expected list (1.1–9.4, GR1–GR4) but
the corresponding section of master.md is empty, truncated, or has no body
text.

**Detection**:
```bash
# Check that every expected section heading in master.md has body content
# below it (more than just the heading line)
for sec in $(seq 1 9); do
  # Count lines between this section's rules and the next section
  # If <5 lines, the section is likely empty or corrupt
  echo "Section $sec: checking for content..."
done
```

**Action**: Do not fabricate the rule content. Flag the missing entry in
`.agents/feedback/exchange.md`. Skip that rule and adapt the remaining ones.
After all healthy rules are adapted, re-run Stage 2 (Refinement) or Stage 3
(Merge) for the affected section to regenerate the missing content. Then adapt
the skipped rule.

**Prevention**: Run the master.md structural integrity check from the
pre-generation checklist in `ste-code-artifacts/SKILL.md` before starting
adaptation.

### Edge Case 2: Duplicate Rule Numbers

**Symptom**: Two or more adapted files claim the same rule number. For example,
both `a-sec3-rule3.2.md` and `a-sec3-rule3.2-v2.md` exist.

**Cause**: A section sub-worker was re-launched without cleaning up the
previous partial output. Or two sub-workers wrote to the same rule number
because of an overlapping prompt range.

**Detection**:
```bash
# Find duplicate rule numbers
ls ste-code/adapted/a-sec*-rule*.md | sed 's/.*\(rule[0-9.GR]*\)\.md/\1/' | sort | uniq -d
```

**Action**: Keep the file with the larger line count and correct format. Delete
the duplicate. If both files are valid but differ in content, keep the one that
matches the Worked Example format above (has Source, Adapted Rule, and
Code-Domain Example Pairs sections). Record the deletion in
`.agents/state/PROGRESS.md`.

### Edge Case 3: Incomplete Synonym Table

**Symptom**: master.md's synonym table has fewer than 12 canonical pairs. Some
pairs are missing the "Prefer" or "Avoid" column. Some rows have only one term.

**Detection**:
```bash
# Count synonym rows in master.md
grep -c "^| " ste-code/merged/master.md  # approximate — adjust for table format
# If <12 rows, the table is incomplete
```

**Action**: Flag the gap in `.agents/feedback/exchange.md`. Use the canonical
synonym table from the STE-Code system prompt as the baseline (these 12 pairs
are the minimum standard). For any pair not found in master.md, mark it as
"extrapolated from STE-Code baseline" in the adapted synonym file. Do not
invent synonym pairs without a source.

**The 12 baseline pairs**:
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

### Edge Case 4: Category Count Mismatch

**Symptom**: master.md claims 19 categories but the extraction pages contain
only 17 or 18 category definition blocks. Or a sub-worker produces 22
categories because it used an older Issue of ASD-STE100.

**Detection**:
```bash
# Count unique category definitions in master.md
grep -c "^### Category" ste-code/merged/master.md
# Must return 19
```

**Action**: If master.md has the wrong count, master.md is stale. Re-run Stage
3 (Merge) to regenerate it from the correct extraction pages. If master.md has
19 but the sub-worker produces a different count, the sub-worker prompt is
wrong. Check `.agents/prompts/adapt/adapt-categories.txt` for any mention of 22
categories and correct it to 19.

**Hard rule**: 19 categories. ASD-STE100 Issue 9 has exactly 19 technical noun
categories. The 22-category claim was an error from an earlier draft. Never
repeat it.

### Edge Case 5: Sub-Worker Produces Truncated Output

**Symptom**: An adapted rule file ends mid-sentence. The last line is a partial
paragraph with no closing punctuation. Or the file has <30 lines.

**Detection**:
```bash
# Check last line for truncation signals
for f in ste-code/adapted/a-sec*-rule*.md; do
  last=$(tail -1 "$f")
  # If last line does not end with ., !, ?, ), or ], it may be truncated
  if ! echo "$last" | grep -q '[.!?)\]}]$'; then
    echo "WARN: $f may be truncated — last line: $last"
  fi
done
```

**Action**: Split the section in half and re-launch two sub-workers with
smaller input ranges. For example, if Section 3 (7 rules) produces truncated
output, launch one worker for rules 3.1–3.4 and another for rules 3.5–3.7.
Merge the results after both pass validation.

### Edge Case 6: Polysemy Table Is Missing or Empty

**Symptom**: master.md has no polysemy resolution table, or the table has
entries for one meaning only.

**Action**: A polysemy table resolves words that have multiple approved
meanings (e.g., "return" means 1. "send a value back from a function" and 2.
"go back" — only meaning 1 is approved in STE-Code). If master.md lacks this
table, generate it from the adapted rule files after all 53 rules are complete.
Each adapted rule that uses a polysemous word must include a note about which
meaning is approved and which is not. Collect these notes into
`ste-code/adapted/a-polysemy.md`.

### Edge Case 7: All Section Workers Succeed but Supporting Files Are Missing

**Symptom**: All 53 rule files exist and pass validation, but
`a-categories.md` or `a-dictionary.md` is missing or empty.

**Action**: Launch the missing supporting worker explicitly. Do not proceed to
Stage 5 without all 3 supporting files (categories, dictionary, polysemy).
Check that the prompts exist before launching:

```bash
test -f .agents/prompts/adapt/adapt-categories.txt || echo "MISSING: categories prompt"
test -f .agents/prompts/adapt/adapt-dictionary.txt || echo "MISSING: dictionary prompt"
```

If a prompt file is missing, write it from the adaptation SKILL.md protocol
definitions before launching the worker.

### Edge Case 8: Sub-Worker Launches Fail with API Errors

**Symptom**: The `hermes -z` command returns a non-zero exit code, an API rate
limit error, or a model unavailability message.

**Action**: Wait 30 seconds and retry once. If the second attempt also fails,
check:
- Is the model `poolside/laguna-s-2.1:free` available? Check `hermes status` or
  `hermes --list-models`.
- Are you rate-limited? Wait 60 seconds, then retry all pending sections.
- Is the prompt file too large? For Section 1 (14 rules), the prompt may exceed
  context window. Split Section 1 into two sub-workers: rules 1.1–1.7 and
  rules 1.8–1.14.

Record all failures and retries in `.agents/feedback/exchange.md`.

## R3 Enforcement: How to Verify Before Claiming Complete

Rail 3 says "Never claim a file complete until it EXISTS on disk with real
content (>30 lines)." This is how you enforce it:

1. **Check existence first**: `test -f ste-code/adapted/a-secN-ruleY.Z.md` must
   return true. Do not trust memory or a previous `ls` output. Check the disk
   every time.

2. **Check line count**: `wc -l < ste-code/adapted/a-secN-ruleY.Z.md` must
   return a number >30. A file with 31 lines that are all blank or comment
   markers is also a fail. Always pair the line count check with a content
   check.

3. **Check content minimum**: The file must contain at least these 4 markers:
   - `Source: ASD-STE100 Issue 9`
   - `## Adapted Rule`
   - `## Code-Domain Example Pairs`
   - `Non-STE:` (at least one occurrence)

   ```bash
   # Combined existence + content check
   f="ste-code/adapted/a-sec1-rule1.1.md"
   if [ -f "$f" ] && [ $(wc -l < "$f") -gt 30 ] && \
      grep -q "Source: ASD-STE100 Issue 9" "$f" && \
      grep -q "## Adapted Rule" "$f" && \
      grep -q "## Code-Domain Example Pairs" "$f" && \
      grep -q "Non-STE:" "$f"; then
     echo "PASS: $f is complete"
   else
     echo "FAIL: $f is incomplete or missing"
   fi
   ```

4. **Update PROGRESS.md ONLY after the combined check passes**. Never update
   the progress tracker before running the check.

5. **Run the validation commands from this document after every section
   completes**. Do not batch-validate all 9 sections at the end. Validate after
   each section sub-worker finishes.

## Stage 5 — Artifacts

After all adaptation files exist, generate 6 artifact files in `ste-code/artifacts/`:

| # | File | Target |
|---|------|--------|
| 1 | ste-code-distilled-system-prompt.txt | ~1,200 tokens |
| 2 | ste-code-self-reading-manual.txt | ~7,000 tokens |
| 3 | ste-code-extraction-methodology.txt | ~1,400 tokens |
| 4 | ste-code-example-turn.txt | ~500 tokens |
| 5 | ste-code-deployment-guide.txt | ~1,800 tokens |
| 6 | README.md | ~500 tokens |

Full specs in `ste-code-artifacts/SKILL.md`.

### Artifact Pre-Generation Checklist

Run these checks before generating any artifact. Stop if any check fails.

```bash
# master.md must be healthy
test -f ste-code/merged/master.md || { echo "FAIL: master.md missing"; exit 1; }
master_bytes=$(wc -c < ste-code/merged/master.md)
[ "$master_bytes" -gt 500000 ] || { echo "FAIL: master.md too small ($master_bytes bytes, need >500KB)"; exit 1; }

# All 53 adapted rule files must exist
rule_count=$(ls ste-code/adapted/a-sec*-rule*.md 2>/dev/null | wc -l)
[ "$rule_count" -eq 53 ] || { echo "FAIL: $rule_count adapted rules (need 53)"; exit 1; }

# At least 11 adapted files total (53 rules + categories + dictionary + polysemy)
adapted_total=$(ls ste-code/adapted/a-*.md 2>/dev/null | wc -l)
[ "$adapted_total" -ge 11 ] || { echo "FAIL: only $adapted_total adapted files (need >=11)"; exit 1; }

# Dictionary must have >800 approved entries
dict_approved=$(grep -c "APPROVED" ste-code/adapted/a-dictionary.md 2>/dev/null || echo 0)
[ "$dict_approved" -gt 800 ] || { echo "FAIL: only $dict_approved dictionary entries (need >800)"; exit 1; }

# Categories must have exactly 19 entries
cat_count=$(grep -c "^| [0-9]" ste-code/adapted/a-categories.md 2>/dev/null || echo 0)
[ "$cat_count" -eq 19 ] || { echo "FAIL: $cat_count categories (need 19)"; exit 1; }

echo "PASS: All pre-generation checks passed."
```

## Rails (8 Guardrails)

| Rail | Rule |
|------|------|
| R1 | Write ONLY to `ste-code/adapted/` and `ste-code/artifacts/`. Never touch earlier stages. |
| R2 | Naming: `a-secN-ruleY.Z.md` for adaptation, `ste-code-<name>.txt` for artifacts |
| R3 | NEVER claim a file complete until it EXISTS on disk with real content (>30 lines) |
| R4 | Every claim backed by source data from master.md. No fabrication. |
| R5 | `#` page, `##` section, `###` rule, `####` dictionary. Blank line after every heading. |
| R6 | 19 categories, poolside/laguna-s-2.1:free, 53 rules + 4 GR. Never claim otherwise. |
| R7 | Update `.agents/state/PROGRESS.md` after EVERY completed file. |
| R8 | Fix mistakes immediately. Document what happened. |

## 🔴 MANDATORY: Progress Tracking

The extraction and refinement orchestrators executed at 100% but tracked at 0%.
The auditor had to fix PROGRESS.md 3 times. **Do not repeat this.**

After every adaptation file:

1. Update `.agents/state/PROGRESS.md` — flip the rule's checkbox to `✅`
2. `git add` and `git commit` with descriptive message
3. Verify: `grep '✅' .agents/state/PROGRESS.md | wc -l` should increase

### Progress Tracking Workflow

```
1. Sub-worker writes a-secN-ruleY.Z.md
2. Run the combined existence + content check (see R3 Enforcement)
3. If PASS: update PROGRESS.md, git add + commit
4. If FAIL: record in feedback/exchange.md, re-launch sub-worker
5. Verify the count increased: grep '✅' .agents/state/PROGRESS.md | wc -l
```

## Validation

Run after each batch of 10 rules:

1. **Per-file**: Line count > 30, no fabrication signals, correct rule references
2. **Spot-check**: 3 adaptations against original spec pages
3. **Full sweep**: After all 53 rules, verify all rule numbers present

### Per-File Validation Script

```bash
#!/bin/bash
# Run after a batch of adapted files is produced
PASS=0; FAIL=0

for f in ste-code/adapted/a-sec*-rule*.md; do
  # Skip non-existent glob matches
  [ -f "$f" ] || continue

  fname=$(basename "$f")

  # Check 1: Line count > 30
  lines=$(wc -l < "$f")
  if [ "$lines" -le 30 ]; then
    echo "FAIL: $fname — $lines lines (need >30)"
    FAIL=$((FAIL + 1))
    continue
  fi

  # Check 2: Source backlink
  if ! grep -q "Source: ASD-STE100 Issue 9" "$f"; then
    echo "FAIL: $fname — missing source backlink"
    FAIL=$((FAIL + 1))
    continue
  fi

  # Check 3: Adapted Rule section
  if ! grep -q "## Adapted Rule" "$f"; then
    echo "FAIL: $fname — missing Adapted Rule section"
    FAIL=$((FAIL + 1))
    continue
  fi

  # Check 4: At least one code-domain example pair
  if ! grep -q "Non-STE:" "$f"; then
    echo "FAIL: $fname — no code-domain example pairs"
    FAIL=$((FAIL + 1))
    continue
  fi

  # Check 5: No fabrication signals
  if grep -q "In summary\|The key point is\|This rule describes" "$f"; then
    echo "FAIL: $fname — fabrication signals detected (commentary language)"
    FAIL=$((FAIL + 1))
    continue
  fi

  # Check 6: No aerospace leakage outside original rule blocks
  aerospace=$(grep -n "aircraft\|engine\|landing gear\|fuselage\|cockpit\|APU\|ECS" "$f" | grep -v "## Original Rule")
  if [ -n "$aerospace" ]; then
    echo "FAIL: $fname — aerospace terms leaked: $aerospace"
    FAIL=$((FAIL + 1))
    continue
  fi

  # Check 7: Model name is correct
  if grep -q "deepseek-pro\b\|deepseek-v4-flash\|deepseek-v3" "$f"; then
    echo "FAIL: $fname — wrong model name"
    FAIL=$((FAIL + 1))
    continue
  fi

  echo "PASS: $fname ($lines lines)"
  PASS=$((PASS + 1))
done

echo "=== $PASS passed, $FAIL failed ==="
```

### Spot-Check Protocol

Pick 3 adapted rules at random. For each:

1. Open the adapted file (`ste-code/adapted/a-secN-ruleY.Z.md`).
2. Find the original rule in `ste-code/merged/master.md` using the source
   backlink.
3. Verify:
   - The rule number matches.
   - The adapted rule preserves the core instruction.
   - Every code-domain example pair replaces an aerospace example with a valid
     code-domain equivalent.
   - No invented terms appear without a master.md source.
   - All words are from the STE-Code dictionary or are technical code nouns.
4. Record the spot-check results in `.agents/state/PROGRESS.md`.

### Full-Sweep Completeness Check

After all 53 rules are adapted:

```bash
# Generate the complete list of expected rule numbers
expected_rules="1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 1.10 1.11 1.12 1.13 1.14 2.1 2.2 2.3 3.1 3.2 3.3 3.4 3.5 3.6 3.7 4.1 4.2 4.3 4.4 4.5 5.1 5.2 5.3 5.4 5.5 6.1 6.2 6.3 6.4 6.5 6.6 7.1 7.2 7.3 8.1 8.2 8.3 8.4 8.5 8.6 8.7 9.1 9.2 9.3 9.4 GR1 GR2 GR3 GR4"

missing=""
for rule in $expected_rules; do
  if ! ls ste-code/adapted/a-sec*-rule${rule}.md >/dev/null 2>&1; then
    missing="$missing $rule"
  fi
done

if [ -z "$missing" ]; then
  echo "PASS: All 57 rule files (53 rules + 4 GR) are present."
else
  echo "FAIL: Missing rule files for:$missing"
fi
```

## Scratch Warning

Premature adaptation files exist in `.agents/_scratch/`. They were created before
extraction completed and moved there by RAILS. **Do NOT reuse them.** Regenerate
everything from `ste-code/merged/master.md`.

## Immutable Facts

- 19 technical noun categories (NOT 22)
- 53 writing rules + 4 GR rules (NOT 65)
- Model: poolside/laguna-s-2.1:free (NOT deepseek-pro or deepseek-v4-flash)
- 434 pages in ASD-STE100 Issue 9
- Output: .md for adaptation, .txt for artifacts

## Session Recovery — What to Do if the Orchestrator Session Is Interrupted

If you are reading this file as a continuation after a session interruption:

1. **Run the Verify State commands at the top of this file.** Confirm that
   Stages 1-3 are intact (109 extracted, 109 refined, 2 merged).
2. **Run the completeness check**: `ls ste-code/adapted/a-sec*-rule*.md | wc
   -l`. This tells you how many rules were adapted before the interruption.
3. **Compare against the per-section breakdown.** Find which sections are
   complete and which are missing or have partial output.
4. **Do not restart completed sections.** Launch sub-workers only for the
   sections that are missing or have failed rules.
5. **Check PROGRESS.md** for the last recorded completion. Any rule marked `✅`
   in PROGRESS.md that has no corresponding file on disk is a tracking error —
   fix PROGRESS.md to match reality.
6. **Check for duplicate files.** An interrupted sub-worker may have left a
   partial file. Run the duplicate detection from Edge Case 2. Keep the
   complete version, delete the partial one.

## Start Now

```
Read .agents/skills/ste-code-continue/continuation.md and execute.

1. Verify pipeline state (109 extracted, 109 refined, 2 merged)
2. Read master.md, launch sub-workers for all 9 sections + supporting files
3. Validate every sub-worker output with the checks in this document
4. Write to ste-code/adapted/, update PROGRESS.md after every verified file
5. After all 53 rules + 3 supporting files pass validation, proceed to Stage 5
6. Generate 6 artifacts in ste-code/artifacts/
7. Validate everything. No fabrication. Update tracking.

Start with the Verify State commands. Then launch the Section 1 sub-worker.
```
