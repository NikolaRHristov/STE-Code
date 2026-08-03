---
name: artifacts
description: > **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
category: authoring
capability: authoring-and-changing-the-standard
source: .agents/skills/artifacts
layout: ste-code-canonical-v1
---

# Artifact Generation Protocol - Stage 5

> **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
> Session isolation + STRICT_RULES (R1-R6) from `lib/pipeline_core.py` apply to
> THIS skill. One session = one operation = one read + one write. No re-editing
> own output.

Generate 6 final STE-Code artifact files from adapted content. Agent-agnostic.

## Prerequisites

- master.md exists and validated
- All 53 rules present, 19 categories enumerated
- Dictionary entries available
- Synonym and polysemy tables extracted

## 6 Artifacts

| #   | File                                   | Target        | Purpose                   |
| --- | -------------------------------------- | ------------- | ------------------------- |
| 1   | `ste-code-distilled-system-prompt.txt` | ~1,200 tokens | LLM system prompt         |
| 2   | `ste-code-self-reading-manual.txt`     | ~7,000 tokens | S0-S8 self-reading manual |
| 3   | `ste-code-extraction-methodology.txt`  | ~1,400 tokens | 6-pass pipeline protocol  |
| 4   | `ste-code-example-turn.txt`            | ~500 tokens   | Worked example            |
| 5   | `ste-code-deployment-guide.txt`        | ~1,800 tokens | Ollama, LM Studio, Python |
| 6   | `README.md`                            | ~500 tokens   | Project overview          |

## Input File Dependencies

Each artifact draws from a specific set of adapted source files. Use this map to
confirm that input files exist before you start generation.

| Artifact | Required Input Files                                                                                                                |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| 1        | `ste-code/adapted/a-sec1-rules.md`, `ste-code/adapted/a-sec2-rules.md`, `ste-code/adapted/a-categories.md`, master.md synonym table |
| 2        | All 11 adapted files (`a-sec1-rules.md` through `a-dictionary.md`), master.md sections S0-S8                                        |
| 3        | master.md (6-pass pipeline description), `.agents/skills/extraction/SKILL.md` (worker protocol)                                     |
| 4        | `ste-code/adapted/a-sec1-rules.md`, master.md synonym table, master.md anti-patterns                                                |
| 5        | `ste-code/artifacts/ste-code-distilled-system-prompt.txt` (for Modelfile reference), `ste-code/adapted/a-dictionary.md`             |
| 6        | All 5 generated artifact files (1-5), `.agents/benchmark/` (results), `.agents/AGENTS.md`                                           |

NOTE: Artifact 6 is generated last. You cannot write it until Artifacts 1-5 pass
all quality gates.

## Generation Order

Generate artifacts in this sequence. Each artifact feeds the next.

1. **Artifact 1** - system prompt (foundation; all other artifacts reference its
   vocabulary)
2. **Artifact 2** - self-reading manual (consumes all 11 adapted files)
3. **Artifact 3** - extraction methodology (references the 6-pass pipeline from
   master.md)
4. **Artifact 4** - worked example (uses Artifact 1 vocabulary to show a
   complete transformation)
5. **Artifact 5** - deployment guide (references Artifact 1 file path and
   structure)
6. **Artifact 6** - README (summary of all other artifacts)

Do not reorder. Artifact 4 depends on Artifact 1 for its approved vocabulary.
Artifact 5 depends on Artifact 1 for its Modelfile SYSTEM directive.

## Pre-Generation Checklist

Run these checks before you generate any artifact. Stop if any check fails.

- [ ] `ste-code/grouped/master.md` file size > 500KB
- [ ] `grep -c "^#### Rule" ste-code/grouped/master.md` returns exactly 53
- [ ] `grep -c "^### Category" ste-code/grouped/master.md` returns exactly 19
- [ ] `ls ste-code/adapted/a-*.md | wc -l` returns at least 11
- [ ] `grep -c "^### Rule" ste-code/adapted/a-sec1-rules.md` returns at least 14
      (Section 1 has 14 rules)
- [ ] `grep -c "APPROVED" ste-code/adapted/a-dictionary.md` returns > 800
- [ ] `ste-code/artifacts/` directory exists (make it if needed:
      `mkdir -p ste-code/artifacts`)

If master.md is present but a check fails, master.md is stale. Do not generate
artifacts from stale input. Re-run Stage 3 (Merge) and Stage 4 (Adaptation)
first. See `.agents/skills/continuation/SKILL.md` for the Stage 3-5 continuation
protocol.

## Artifact 1 Quality Gates

- All 14 principles reference specific STE rules
- Synonym table uses actual canonical forms
- Anti-patterns are code-specific
- ~4,800 chars total

### Artifact 1 Pass/Fail Criteria

| Check              | Pass                                                                   | Fail                                            |
| ------------------ | ---------------------------------------------------------------------- | ----------------------------------------------- |
| P1-P14 presence    | All 14 principles appear with rule numbers (e.g., "Rule 1.1")          | Any principle missing or lacks a rule reference |
| Synonym rows       | At least 12 rows with Prefer/Avoid columns                             | Fewer than 10 rows or columns mislabeled        |
| Anti-pattern count | At least 5 anti-patterns, all code-domain                              | Anti-patterns are aerospace or generic          |
| Character budget   | 4,300 - 5,300 chars                                                    | <4,000 or >5,800 chars                          |
| Vocabulary         | All words are from the STE-Code dictionary or are technical code nouns | Contains non-approved non-technical words       |

### Artifact 1 Worked Example (excerpt - first 30 lines of a passing artifact)

```
# STE-Code System Prompt - Level 1

You are STE-Code, a Simplified Technical English for Code documentation.
Your purpose: make technical documentation for software clear, consistent, and unambiguous.

## 14 Core Principles

P1. Use approved words from the STE-Code dictionary (Rule 1.1)
P2. Use words only as their specified part of speech (Rule 1.2)
P3. Use words only with their approved meanings (Rule 1.3)
P4. Use only approved verb forms and adjective forms (Rule 1.4)
P5. Technical code nouns (keywords, frameworks, tools) are allowed (Rule 1.5)
P6. Non-approved words only when they are technical code nouns (Rule 1.6)
P7. Do not use technical nouns as verbs (Rule 1.7)
P8. Use standard, well-known technical nouns (Rule 1.8)
P9. Prefer short, clear technical nouns (Rule 1.9)
P10. No slang, jargon, or regional terms (Rule 1.10)
P11. One term per concept - be consistent (Rule 1.11)
P12. Technical verbs (build, deploy, test, lint) are allowed (Rule 1.12)
P13. Do not use technical verbs as nouns (Rule 1.13)
P14. Use American English spelling (Rule 1.14)

## Canonical Synonym Table (code domain)
| Prefer | Avoid |
|--------|-------|
| use | utilize, leverage, employ |
...
```

This excerpt shows the expected format, vocabulary level, and rule-number
tracing. The full artifact continues with the synonym table, output format
rules, and anti-patterns.

## Artifact 2 Quality Gates

- All 8 sections (S0-S8) present, S9 optional
- All 53 adapted rules have code-domain example pairs
- 19 categories listed with code examples
- S6 contains exactly 13 questions

### Artifact 2 Pass/Fail Criteria

| Check            | Pass                                                                                 | Fail                                                    |
| ---------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| Section headers  | S0 through S8 each have an `## S` header; S9 is optional and allowed                 | Any of S0-S8 missing                                    |
| Rule count       | `grep -c "^### Rule" ste-code/artifacts/ste-code-self-reading-manual.txt` returns 53 | Returns < 53 (rules missing) or > 53 (fabricated rules) |
| Example pairs    | Every adapted rule has at least one STE/non-STE code example pair                    | Any rule section lacks a code example pair              |
| Category count   | `grep -c "^## Category"` returns exactly 19                                          | Returns any number other than 19                        |
| S6 questions     | Section S6 contains exactly 13 questions, numbered 1-13                              | Fewer than 13 or more than 13 questions                 |
| Character budget | 26,000 - 30,000 chars (~7,000 tokens)                                                | <24,000 or >32,000 chars                                |
| Rule references  | Every adapted rule cites its master.md rule number (e.g., "from Rule 3.2")           | Any adapted rule lacks a master.md source reference     |
| No aerospace     | Zero aerospace examples remain (no "aircraft", "flight", "wing")                     | Any aerospace term found in examples                    |

### Artifact 2 S6 Validation Script

```bash
# Count S6 questions
sed -n '/^## S6/,/^## S7/p' ste-code/artifacts/ste-code-self-reading-manual.txt | grep -c "^[0-9]"
# Must return exactly 13
```

## Artifact 3 Quality Gates

Artifact 3 describes the 6-pass extraction pipeline. It must be self-contained:
a reader with no prior knowledge can understand how extraction works.

### Artifact 3 Pass/Fail Criteria

| Check            | Pass                                                                               | Fail                               |
| ---------------- | ---------------------------------------------------------------------------------- | ---------------------------------- |
| Pass count       | Exactly 6 passes described, each with a name and purpose                           | Fewer than 6 or more than 6 passes |
| Pass naming      | Pass names match master.md: Read, Map, Filter, Adapt, Validate, Write              | Pass names are invented or renamed |
| Input/output     | Each pass describes its input and output format                                    | Any pass lacks I/O description     |
| Pipeline order   | Passes appear in correct sequence (Read → Map → Filter → Adapt → Validate → Write) | Passes are reordered               |
| Worker reference | Mentions the 109-worker extraction architecture                                    | No mention of workers              |
| Character budget | 5,000 - 6,200 chars (~1,400 tokens)                                                | <4,600 or >6,600 chars             |

## Artifact 4 Quality Gates

Artifact 4 is a worked example showing one complete STE-Code transformation. It
must demonstrate the standard in action on a real code-documentation sentence.

### Artifact 4 Pass/Fail Criteria

| Check                | Pass                                                                             | Fail                                           |
| -------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------- |
| Three stages visible | Shows input (non-compliant) → transformation steps → output (STE-Code compliant) | Missing any of the three stages                |
| Rule annotations     | At least 3 specific rule numbers are cited in the transformation steps           | Fewer than 3 rule citations                    |
| Code-domain content  | Example is about code documentation (API doc, README, commit message, etc.)      | Example is about aerospace or non-code domain  |
| Self-contained       | Reader can understand the example without reading external files                 | Example assumes knowledge from other artifacts |
| Character budget     | 1,800 - 2,200 chars (~500 tokens)                                                | <1,600 or >2,500 chars                         |

### Artifact 4 Worked Example (full passing example)

```
INPUT (non-compliant):
"Utilize the initialize() function in order to commence the server, it
should be able to handle multiple simultaneous connections effectively."

--- TRANSFORMATION ---

Step 1 - Synonym replacement (Rule 1.11, synonym table):
"utilize" → "use", "commence" → "start", "in order to" → "to"

Step 2 - Sentence splitting (Rule 4.1):
One sentence → two sentences. Break at the comma splice.

Step 3 - Remove filler (Rule 4.3):
"should be able to" → remove. State the fact directly.

Step 4 - Approve vocabulary (Rules 1.1, 1.2, 1.3):
"simultaneous" → "at the same time" (simultaneous is not approved)
"effectively" → remove (filler adverb, Rule 4.3)

--- OUTPUT (STE-Code compliant) ---

Use the initialize() function to start the server.
The server handles multiple connections at the same time.
```

This example demonstrates synonym replacement (Rule 1.11), sentence splitting
(Rule 4.1), filler removal (Rule 4.3), and vocabulary approval (Rules 1.1-1.3).
Four rule references in one short example.

## Artifact 5 Quality Gates

Artifact 5 covers three deployment targets: Ollama, LM Studio, and Python. Each
target must include working, copy-pasteable commands.

### Artifact 5 Pass/Fail Criteria

| Check             | Pass                                                                                            | Fail                                                 |
| ----------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| Ollama section    | Contains a complete Modelfile with FROM, SYSTEM, and PARAMETER directives                       | Modelfile is incomplete or has invalid directives    |
| LM Studio section | Contains preset configuration or import instructions                                            | LM Studio section is missing or empty                |
| Python section    | Contains a `pip install` command and a working Python code block that loads and uses the prompt | Python code block is missing or would not run        |
| File paths        | All artifact file paths in the guide match actual artifact output filenames                     | Paths are wrong or reference files that do not exist |
| Model reference   | Uses `poolside/laguna-s-2.1:free` (NOT deepseek-pro)                                            | Wrong model name                                     |
| Minimum versions  | States minimum versions for Ollama (≥0.1.0) and Python (≥3.10)                                  | No version requirements stated                       |
| Character budget  | 6,800 - 7,800 chars (~1,800 tokens)                                                             | <6,400 or >8,200 chars                               |

## Artifact 6 Quality Gates

Artifact 6 is the project README. It is the entry point for new users. Generate
it last, after Artifacts 1-5 all pass.

### Artifact 6 Pass/Fail Criteria

| Check                | Pass                                                                    | Fail                                               |
| -------------------- | ----------------------------------------------------------------------- | -------------------------------------------------- |
| One-sentence summary | First sentence states what STE-Code is and what it does                 | No clear summary sentence                          |
| Artifact listing     | Lists all 6 artifact files with one-line descriptions                   | Any artifact file missing from the list            |
| Quick start          | Gives a 3-step quick-start path (download prompt → load into LLM → use) | No quick-start section or steps are not actionable |
| Benchmark results    | Includes pass rate and improvement percentage from `.agents/benchmark/` | No benchmark results or fabricated numbers         |
| Model stated         | Names the model used: `poolside/laguna-s-2.1:free`                      | Wrong model name or omitted                        |
| Character budget     | 1,800 - 2,200 chars (~500 tokens)                                       | <1,600 or >2,500 chars                             |

## Anti-Fabrication

- Every adapted rule references master.md rule number
- Every synonym traces to master.md synonym table
- Every example adapts a real STE/non-STE pair
- 19 categories (NOT 22), poolside/laguna-s-2.1:free (NOT deepseek-pro)

## Token Budget Tracking

All 6 artifacts share a total budget of ~12,400 tokens (~49,600 chars). Track
consumption as you generate. If one artifact exceeds its budget, the next
artifact in sequence must tighten its budget to compensate.

| Artifact  | Budget (chars) | Tolerance |
| --------- | -------------- | --------- |
| 1         | 4,800          | ±500      |
| 2         | 28,000         | ±2,000    |
| 3         | 5,600          | ±600      |
| 4         | 2,000          | ±200      |
| 5         | 7,200          | ±600      |
| 6         | 2,000          | ±200      |
| **Total** | **49,600**     | -         |

If Artifact 2 consumes 30,000 chars (the upper bound), Artifact 3 must target
5,000 chars (the lower bound) to keep the total under 49,600. Always prefer
budget compliance over content padding.

## Verification

```bash
for f in ste-code/artifacts/ste-code-*.txt; do
	chars=$(wc -c < "$f")
	echo "$(basename $f): $chars chars ~$((chars / 4)) tokens"
done
```

Expected total: ~49,600 chars (~12,400 tokens)

### Full Verification Script

Run this script after all 6 artifacts are generated. It performs every pass/fail
check in one pass.

```bash
#!/bin/bash
PASS=0
FAIL=0
ARTIFACTS="ste-code/artifacts"

echo "Full Artifact Verification"
echo

# --- Artifact 1 ---
echo "--- Artifact 1: System Prompt ---"
f="$ARTIFACTS/ste-code-distilled-system-prompt.txt"
[ -f "$f" ] || {
	echo "FAIL: file missing"
	FAIL=$((FAIL + 1))
}
principles=$(grep -c "^P[0-9]" "$f" 2> /dev/null || echo 0)
[ "$principles" -ge 14 ] && echo "PASS: $principles principles" && PASS=$((PASS + 1)) || {
	echo "FAIL: only $principles principles (need 14)"
	FAIL=$((FAIL + 1))
}
synonyms=$(grep -c "^| " "$f" 2> /dev/null || echo 0)
[ "$synonyms" -ge 10 ] && echo "PASS: $synonyms synonym rows" && PASS=$((PASS + 1)) || {
	echo "FAIL: only $synonyms synonym rows (need >=10)"
	FAIL=$((FAIL + 1))
}
echo

# --- Artifact 2 ---
echo "--- Artifact 2: Self-Reading Manual ---"
f="$ARTIFACTS/ste-code-self-reading-manual.txt"
[ -f "$f" ] || {
	echo "FAIL: file missing"
	FAIL=$((FAIL + 1))
}
for s in S0 S1 S2 S3 S4 S5 S6 S7 S8; do
	grep -q "^## $s" "$f" 2> /dev/null && echo "PASS: $s section present" && PASS=$((PASS + 1)) || {
		echo "FAIL: $s section missing"
		FAIL=$((FAIL + 1))
	}
done
questions=$(sed -n '/^## S6/,/^## S7/p' "$f" 2> /dev/null | grep -c "^[0-9]")
[ "$questions" -eq 13 ] && echo "PASS: S6 has exactly 13 questions" && PASS=$((PASS + 1)) || {
	echo "FAIL: S6 has $questions questions (need 13)"
	FAIL=$((FAIL + 1))
}
rules=$(grep -c "^### Rule" "$f" 2> /dev/null || echo 0)
[ "$rules" -eq 53 ] && echo "PASS: $rules adapted rules" && PASS=$((PASS + 1)) || {
	echo "FAIL: $rules rules (need 53)"
	FAIL=$((FAIL + 1))
}
categories=$(grep -c "^## Category" "$f" 2> /dev/null || echo 0)
[ "$categories" -eq 19 ] && echo "PASS: $categories categories" && PASS=$((PASS + 1)) || {
	echo "FAIL: $categories categories (need 19)"
	FAIL=$((FAIL + 1))
}
echo

# --- Artifact 3 ---
echo "--- Artifact 3: Extraction Methodology ---"
f="$ARTIFACTS/ste-code-extraction-methodology.txt"
[ -f "$f" ] || {
	echo "FAIL: file missing"
	FAIL=$((FAIL + 1))
}
for pass in "Read" "Map" "Filter" "Adapt" "Validate" "Write"; do
	grep -qi "$pass" "$f" 2> /dev/null && echo "PASS: '$pass' pass described" && PASS=$((PASS + 1)) || {
		echo "FAIL: '$pass' pass missing"
		FAIL=$((FAIL + 1))
	}
done
grep -q "109" "$f" 2> /dev/null && echo "PASS: worker count (109) mentioned" && PASS=$((PASS + 1)) || {
	echo "FAIL: worker count (109) not mentioned"
	FAIL=$((FAIL + 1))
}
echo

# --- Artifact 4 ---
echo "--- Artifact 4: Worked Example ---"
f="$ARTIFACTS/ste-code-example-turn.txt"
[ -f "$f" ] || {
	echo "FAIL: file missing"
	FAIL=$((FAIL + 1))
}
grep -qi "INPUT" "$f" 2> /dev/null && echo "PASS: INPUT section" && PASS=$((PASS + 1)) || {
	echo "FAIL: no INPUT section"
	FAIL=$((FAIL + 1))
}
grep -qi "OUTPUT" "$f" 2> /dev/null && echo "PASS: OUTPUT section" && PASS=$((PASS + 1)) || {
	echo "FAIL: no OUTPUT section"
	FAIL=$((FAIL + 1))
}
rule_cites=$(grep -oc "Rule [0-9]" "$f" 2> /dev/null || echo 0)
[ "$rule_cites" -ge 3 ] && echo "PASS: $rule_cites rule citations" && PASS=$((PASS + 1)) || {
	echo "FAIL: only $rule_cites rule citations (need >=3)"
	FAIL=$((FAIL + 1))
}
echo

# --- Artifact 5 ---
echo "--- Artifact 5: Deployment Guide ---"
f="$ARTIFACTS/ste-code-deployment-guide.txt"
[ -f "$f" ] || {
	echo "FAIL: file missing"
	FAIL=$((FAIL + 1))
}
grep -qi "Ollama\|Modelfile" "$f" 2> /dev/null && echo "PASS: Ollama/Modelfile section" && PASS=$((PASS + 1)) || {
	echo "FAIL: no Ollama section"
	FAIL=$((FAIL + 1))
}
grep -qi "LM Studio" "$f" 2> /dev/null && echo "PASS: LM Studio section" && PASS=$((PASS + 1)) || {
	echo "FAIL: no LM Studio section"
	FAIL=$((FAIL + 1))
}
grep -qi "pip install\|from openai\|import" "$f" 2> /dev/null && echo "PASS: Python section" && PASS=$((PASS + 1)) || {
	echo "FAIL: no Python section"
	FAIL=$((FAIL + 1))
}
grep -q "poolside/laguna-s-2.1:free" "$f" 2> /dev/null && echo "PASS: correct model name" && PASS=$((PASS + 1)) || {
	echo "FAIL: wrong or missing model name (must be poolside/laguna-s-2.1:free)"
	FAIL=$((FAIL + 1))
}
echo

# --- Artifact 6 ---
echo "--- Artifact 6: README ---"
f="$ARTIFACTS/README.md"
[ -f "$f" ] || {
	echo "FAIL: file missing"
	FAIL=$((FAIL + 1))
}
grep -q "STE-Code" "$f" 2> /dev/null && echo "PASS: project name present" && PASS=$((PASS + 1)) || {
	echo "FAIL: project name missing"
	FAIL=$((FAIL + 1))
}
grep -qi "quick.start\|getting started" "$f" 2> /dev/null && echo "PASS: quick-start section" && PASS=$((PASS + 1)) || {
	echo "FAIL: no quick-start section"
	FAIL=$((FAIL + 1))
}
grep -q "poolside/laguna-s-2.1:free" "$f" 2> /dev/null && echo "PASS: correct model name" && PASS=$((PASS + 1)) || {
	echo "FAIL: wrong or missing model name"
	FAIL=$((FAIL + 1))
}
echo

echo "Summary: $PASS passed, $FAIL failed"
```

## Failure Recovery

If an artifact fails a quality gate, do not continue to the next artifact. Fix
the failure first. Use this table to diagnose and recover.

| Artifact                        | Common Failure                        | Root Cause                                                 | Recovery Action                                                                                                                                                                                                                      |
| ------------------------------- | ------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1 - P count < 14                | Missing principle                     | Adapted Section 1 file incomplete                          | Re-read `ste-code/adapted/a-sec1-rules.md`. Check that Rules 1.1-1.14 are all present. If fewer than 14 rules, the adaptation stage is incomplete. Run Stage 4 again for Section 1.                                                  |
| 1 - Synonym rows < 10           | Synonym table too short               | master.md synonym extraction missed rows                   | Re-read master.md synonym table. Cross-check against `ste-code/adapted/a-sec1-rules.md` synonym section.                                                                                                                             |
| 1 - Wrong model in text         | Fabricated model name                 | Agent invented "deepseek-pro" or similar                   | Search the artifact for "deepseek". Replace any variant other than `poolside/laguna-s-2.1:free`.                                                                                                                                     |
| 2 - Missing section (S0-S8)     | Adapted file for that section missing | Adaptation worker failed or produced truncated output      | Find the adapted file for the missing section (e.g., `a-sec6-rules.md` for S6). If the file is missing or <100 lines, re-run the adaptation worker for that section. See Stage 4 protocol in `.agents/skills/continuation/SKILL.md`. |
| 2 - S6 question count ≠ 13      | Questions miscounted or fabricated    | Agent added invented questions or dropped real ones        | Re-read master.md Section 6. Extract exactly the 13 questions listed there. Do not add, remove, or reword questions.                                                                                                                 |
| 2 - Rule count ≠ 53             | Rules missing or fabricated           | Adapted files are incomplete or agent invented extra rules | Count rules per adapted file: `grep -c "^### Rule" ste-code/adapted/a-sec*.md`. Sum must be 53. If not, find which section is off and regenerate that adapted file.                                                                  |
| 2 - Aerospace examples          | Adaptation incomplete                 | Adapted file still has aerospace examples                  | `grep -i "aircraft\|flight\|wing\|landing\|engine" ste-code/artifacts/ste-code-self-reading-manual.txt`. Find the offending section, re-read the corresponding adapted file, and regenerate the artifact section.                    |
| 3 - Missing pass name           | 6-pass names not read correctly       | Agent read master.md pass description incorrectly          | Re-read the 6-pass pipeline section in master.md. Write the 6 pass names exactly as they appear: Read, Map, Filter, Adapt, Validate, Write.                                                                                          |
| 4 - Fewer than 3 rule citations | Example too simple                    | Agent wrote a transformation without rule annotations      | Add a Step line for each transformation action. Each Step must cite at least one rule number. Aim for 4-5 rule citations in a 5-step transformation.                                                                                 |
| 5 - Missing deployment target   | Section skipped                       | Agent omitted Ollama, LM Studio, or Python                 | Check that all three targets have dedicated sections. If one is missing, read that target's documentation from master.md or adapted files and add the section.                                                                       |
| 6 - README generated too early  | Artifacts 1-5 not complete            | Agent wrote README before generating all other artifacts   | Delete the README. Finish Artifacts 1-5 first. Verify all 5 pass. Then generate Artifact 6.                                                                                                                                          |

### General Recovery Protocol

When any artifact fails verification:

1. Identify the failing check from the pass/fail criteria table.
2. Find the root cause in the Failure Recovery table.
3. Apply the recovery action. Do not change more than one artifact at a time.
4. Re-run verification on the fixed artifact only.
5. If the fix changes artifact content that later artifacts depend on, re-verify
   the dependent artifacts.

If a recovery action does not fix the failure after two attempts, stop. Write
the failure to `.agents/feedback/exchange.md` with the artifact name, failing
check, actions tried, and current state. A human reviewer must resolve the
deadlock.

## Edge Cases

### master.md Is Present but Stale

If master.md exists but fails any Pre-Generation Checklist item:

- **Symptom**: file size < 500KB, rule count < 53, category count ≠ 19.
- **Cause**: Stage 3 (Merge) or Stage 4 (Adaptation) ran partially or not at
  all.
- **Action**: Do not generate artifacts. Re-run Stage 3 to rebuild master.md
  from the freshest source directory (enriched, refined, or extracted). Then
  re-run Stage 4. Verify master.md passes all checklist items before starting
  artifact generation.
- **Cross-reference**: `.agents/skills/continuation/SKILL.md` Stage Detection
  section tells you how to pick the best input source.

### Dictionary Entries Are Incomplete

If `ste-code/adapted/a-dictionary.md` has fewer than 800 approved entries:

- **Symptom**: `grep -c "APPROVED" ste-code/adapted/a-dictionary.md` returns
  < 800.
- **Cause**: The dictionary adaptation worker (a011) failed or produced
  truncated output.
- **Impact**: Artifacts 1, 2, and 5 reference the dictionary. Gaps cause false
  "word not approved" errors and missing synonym entries.
- **Action**: Re-run adaptation worker a011. See Stage 4 protocol in
  `.agents/skills/continuation/SKILL.md`. Wait for the worker to complete.
  Verify entry count > 800 before resuming artifact generation.

### Adapted Files Are Truncated

If any adapted file ends mid-sentence or is <50 lines:

- **Symptom**: `tail -1 ste-code/adapted/a-secN-rules.md` shows a partial
  sentence.
- **Cause**: The adaptation worker context window filled up before it finished
  writing.
- **Action**: Re-run the specific adaptation worker. Give it a smaller input
  range (split the section in half if it is large). Merge the results.
- **Prevention**: Always run the truncation check from validation skill after
  Stage 4 completes. See `.agents/skills/validation/SKILL.md` Check 3 for
  truncation detection patterns.

### Artifacts Directory Missing or Empty

If `ste-code/artifacts/` does not exist or has no files:

- **Action**: `mkdir -p ste-code/artifacts`. Start generation from Artifact 1.

### Disk Space Low

If disk space drops below 100MB during generation:

- **Symptom**: `df -h .` shows <100MB available.
- **Action**: Remove temporary files from earlier stages
  (`ste-code/grouped/master-raw.md`, old worker output in `ste-code/extracted/`
  that passed validation). Do not delete adapted files or master.md. If still
  low, stop and report.

### Regeneration After Partial Run

If 3 of 6 artifacts were generated before a crash or interruption:

- **Check**: Run verification on the 3 existing artifacts. Do not blindly
  regenerate them.
- **If they pass**: Continue from Artifact 4. Do not regenerate Artifacts 1-3.
- **If any fails**: Regenerate that artifact and all artifacts that depend on it
  (later in sequence). Example: Artifact 2 fails → regenerate Artifacts 2, 3, 4,
  5, 6.

### Model or Provider Change

If the generation model changes from `poolside/laguna-s-2.1:free` to another
model:

- All artifacts must use the new model name.
- Update the Anti-Fabrication section to list the new model name.
- Run all verifications again. A model change can produce slightly different
  output even with identical prompts.
- Record the model change in `.agents/feedback/exchange.md`.

## Cross-References

This skill is Stage 5 of the 5-stage pipeline. Other skills provide input and
validation for this stage.

| Skill            | Path                                   | How It Relates to Artifact Generation                                                                                                                           |
| ---------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Continuation** | `.agents/skills/continuation/SKILL.md` | Stage 5 generation protocol (lines 171-196). Use this when resuming partial artifact generation or when any agent invokes Stage 5 from a different perspective. |
| **Validation**   | `.agents/skills/validation/SKILL.md`   | Truncation detection patterns (Check 3) and fabrication detection (Check 4). Apply these checks to adapted files before using them as artifact input.           |
| **Adaptation**   | `.agents/skills/adaptation/SKILL.md`   | Produces the 11 adapted files that are the input to artifact generation. If adapted files are missing or incomplete, run Stage 4 first.                         |
| **Auditing**     | `.agents/skills/auditing/SKILL.md`     | 8-rail verification against fabrication. Run an audit pass on Artifacts 1, 2, and 5 (the largest artifacts) after generation.                                   |
| **Benchmarking** | `.agents/skills/benchmarking/SKILL.md` | 59-test benchmark results. Artifact 6 (README) must include the benchmark pass rate and improvement percentage.                                                 |

## Post-Generation Integration Test

After all 6 artifacts pass individual verification, run this integration test to
confirm cross-artifact consistency.

1. **Model name consistency**:
   `grep -rh "deepseek" ste-code/artifacts/ | sort -u` - must return exactly one
   line: `poolside/laguna-s-2.1:free`.
2. **Rule number cross-reference**: Every rule number in Artifact 1 must appear
   in Artifact 2. Every rule number in Artifact 2 must appear in adapted files.
3. **Synonym table consistency**: Every synonym pair in Artifact 1 must match
   the same pair in Artifact 2. No pair may appear with reversed columns.
4. **Artifact 5 file paths**: Every file path in Artifact 5 (the deployment
   guide) must resolve to a real file in `ste-code/artifacts/`. Run
   `grep -oP 'ste-code/artifacts/[^ )]+' ste-code/artifacts/ste-code-deployment-guide.txt | while read f; do [ -f "$f" ] || echo "MISSING: $f"; done`.
5. **Artifact 6 completeness**: Artifact 6 must list all 5 other artifact
   filenames. Run
   `for a in ste-code-distilled-system-prompt.txt ste-code-self-reading-manual.txt ste-code-extraction-methodology.txt ste-code-example-turn.txt ste-code-deployment-guide.txt; do grep -q "$a" ste-code/artifacts/README.md || echo "MISSING from README: $a"; done`.

If any integration test fails, fix the artifact that is inconsistent. Re-run the
integration test.

## Common Failure Signatures

Learn these patterns. They signal systematic problems that affect more than one
artifact.

| Pattern                                         | Signature                                                            | Systemic Fix                                                                                                                                        |
| ----------------------------------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Wrong model name**                            | "deepseek-pro" or "v4-flash" appears in multiple artifacts           | The Anti-Fabrication section was not checked during generation. Search all artifacts, replace all model name variants.                              |
| **22 categories instead of 19**                 | Category count is 22 in multiple artifacts                           | Agent hallucinated extra categories. Re-read master.md for the correct 19. Regenerate any artifact with wrong count.                                |
| **Aerospace terminology**                       | "aircraft", "flight", "wing" in adapted examples                     | Adaptation stage is incomplete. The adapted files still have aerospace examples. Re-run Stage 4 before regenerating artifacts.                      |
| **Missing rule references**                     | Adapted rules lack "Rule X.Y" citations in Artifact 2                | The adaptation worker did not include rule number references. Fix the adapted files first, then regenerate Artifact 2.                              |
| **Budget overrun**                              | Total chars > 55,000 across all artifacts                            | Agent added too much content. Identify the largest artifact. Trim filler text and redundant examples. Target the budget upper bound.                |
| **Artifact 6 mentions wrong benchmark results** | Pass rate or improvement percentage is not from `.agents/benchmark/` | Agent fabricated benchmark numbers. Read the actual results from `.agents/benchmark/` output or from the benchmark SKILL.md. Use real numbers only. |
