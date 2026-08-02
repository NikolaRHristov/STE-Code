---
name: continuation
description: > **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
category: authoring
capability: authoring-and-changing-the-standard
source: /Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code/.agents/skills/continuation
layout: ste-code-canonical-v1
---


# STE-Code Continuation Skill — Stages 3-5

> **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
> Session isolation + STRICT_RULES (R1-R6) from `lib/pipeline_core.py` apply to THIS skill.
> One session = one operation = one read + one write. No re-editing own output.

## Overview

This skill is used by ANY agent (#1, #2, or #3) to continue pipeline work beyond their primary phase. Each agent applies this skill from its own perspective, using its own output as input to the next stage.

**Pipeline reference:**
```
STAGE 1 — EXTRACT   Agent #1 domain
STAGE 2 — REFINE     Agent #2 domain
STAGE 3 — MERGE      ← THIS SKILL (any agent)
STAGE 4 — ADAPT      ← THIS SKILL (any agent)
STAGE 5 — ARTIFACTS  ← THIS SKILL (any agent)
```

## Agent Perspective Mapping

Each agent uses different input sources depending on who invokes this skill:

| Agent | Stage 3 Input | Stage 4-5 Input |
|-------|-------------|-----------------|
| #1 (Extractor) | `ste-code/enriched/` (enriched extraction) | Merged master.md |
| #2 (Refiner) | `ste-code/refined/` (refined extraction) | Merged master.md |
| #3 (Auditor) | `ste-code/extracted/` (verified extraction) | Merged master.md |

**Rule:** Use the freshest, highest-quality source available. When Agent #1 invokes this skill, prefer enriched files if they exist, fall back to extracted.

## Stage Detection (always run first)

```bash
# Check which files exist and determine active stage
ls ste-code/enriched/w*-p*.md 2>/dev/null | wc -l  # enriched count
ls ste-code/refined/r*.md 2>/dev/null | wc -l        # refined count
ls ste-code/extracted/w*-p*.md 2>/dev/null | wc -l   # extracted count
ls ste-code/grouped/master.md 2>/dev/null              # merge exists?
ls ste-code/adapted/*.md 2>/dev/null | wc -l         # adaptation count
ls ste-code/artifacts/*.txt 2>/dev/null | wc -l      # artifact count
```

### Timestamp-Based Staleness Detection

File counts are not enough. A file that exists can be stale. Use timestamps to detect stale output:

```bash
# Check if master.md is older than any source file (stale)
if [ -f ste-code/grouped/master.md ]; then
  newest_source=$(find ste-code/enriched ste-code/refined ste-code/extracted -name "*.md" -newer ste-code/grouped/master.md 2>/dev/null | wc -l)
  if [ "$newest_source" -gt 0 ]; then
    echo "STALE: master.md is older than $newest_source source files. Re-merge required."
  fi
fi

# Check if adapted files are older than master.md (stale)
if [ -f ste-code/grouped/master.md ] && [ "$(ls ste-code/adapted/*.md 2>/dev/null | wc -l)" -gt 0 ]; then
  stale_count=$(find ste-code/adapted -name "*.md" ! -newer ste-code/grouped/master.md 2>/dev/null | wc -l)
  if [ "$stale_count" -gt 0 ]; then
    echo "STALE: $stale_count adapted files are older than master.md. Re-adaptation required."
  fi
fi
```

**Decision tree:**
- If merged/master.md missing or stale → do Stage 3 (Merge)
- If adapted/ has <10 files → do Stage 4 (Adapt)
- If artifacts/ has <6 files or files < target size → do Stage 5 (Artifacts)
- If all complete → verify and report

### Input Freshness by Agent

Each agent must also check its own input freshness:

| Agent | Freshness Check |
|-------|----------------|
| #1 (Extractor) | Compare `ste-code/enriched/` file timestamps to `ste-code/extracted/` timestamps. If enriched files exist and are newer than extracted, use enriched. |
| #2 (Refiner) | Compare `ste-code/refined/` file timestamps to `ste-code/enriched/` and `ste-code/extracted/`. Use the freshest directory. |
| #3 (Auditor) | Compare `ste-code/extracted/` timestamps to `ste-code/refined/`. If refined is newer, flag it — an auditor cannot use unverified refined output. |

---

## Stage 3 — Merge

### Input Selection (agent-perspective)
Pick the best available source directory:

```bash
# Agent #1 perspective: prefer enriched, fall back to extracted
INPUT_DIR="ste-code/enriched"
[ $(ls ste-code/enriched/w*-p*.md 2>/dev/null | wc -l) -lt 109 ] && INPUT_DIR="ste-code/extracted"

# Agent #2 perspective: prefer refined, fall back to extracted
INPUT_DIR="ste-code/refined"
[ $(ls ste-code/refined/r*.md 2>/dev/null | wc -l) -lt 109 ] && INPUT_DIR="ste-code/extracted"

# Agent #3 perspective: extracted only (auditor verified)
INPUT_DIR="ste-code/extracted"
```

### Edge Case: Incomplete Source Directories

If no source directory has the full 109 files:

| Scenario | Detection | Action |
|----------|-----------|--------|
| enriched/ has 108 files, not 109 | `ls ste-code/enriched/w*-p*.md \| wc -l` returns 108 | Use enriched/ for the 108 that exist. For the missing page range, use extracted/. Merge both sources. |
| refined/ has 105 files | `ls ste-code/refined/r*.md \| wc -l` returns 105 | Same pattern: use refined/ for present files, fill gaps from extracted/. |
| extracted/ has fewer than 109 files | Extraction is incomplete | Stop. Do not merge. Run Stage 1 (Extraction) to complete the missing workers first. |
| enriched/ and extracted/ both exist but extracted/ is newer | Timestamp comparison shows extracted has later files | Prefer extracted/ — it was rerun after enrichment. Enriched files are stale. |

### Edge Case: Zero-Byte master.md

If `ste-code/grouped/master.md` exists but has 0 bytes:

```bash
if [ -f ste-code/grouped/master.md ] && [ ! -s ste-code/grouped/master.md ]; then
  echo "CORRUPT: master.md is zero bytes. Remove and re-merge."
  rm ste-code/grouped/master.md
fi
```

**Cause:** A previous merge started but failed before writing content. The file was created (touch) but never populated.

**Action:** Remove the zero-byte file. Rerun Stage 3 from concatenation.

### Protocol

1. **Concatenate** all files in page order into `ste-code/grouped/master-raw.md`:
   ```bash
   cat ste-code/$INPUT_DIR/w*-p*.md > ste-code/grouped/master-raw.md
   ```

2. **Deduplicate** — scan for duplicate content at page boundaries.
   See the Deduplication Operations section below for operational commands.

3. **Organize by section** into `ste-code/grouped/master.md`:
   ```
   ## Front Matter (pages 1-42)
   ## Part 1 — Writing Rules (pages 43-128)
     ### Section 1 — Words (Rules 1.1-1.14)
     ### Section 2 — Noun Clusters (Rules 2.1-2.3)
     ### Section 3 — Verbs (Rules 3.1-3.7)
     ### Section 4 — Sentences (Rules 4.1-4.4)
     ### Section 5 — Procedures (Rules 5.1-5.5)
     ### Section 6 — Descriptive (Rules 6.1-6.6)
     ### Section 7 — Safety (Rules 7.1-7.3)
     ### Section 8 — Punctuation (Rules 8.1-8.7)
     ### Section 9 — Practices (Rules 9.1-9.4 + GR1-GR4)
     ### Technical Noun Categories (19)
   ## Part 2 — Dictionary (pages 129-360)
   ## Appendices (pages 361-434)
   ```

4. **Validate:**
   - `grep -c "^#### Rule" ste-code/grouped/master.md` → must be 53
   - `grep -c "^### Category" ste-code/grouped/master.md` → must be 19
   - File size > 500KB
   - 10 random spot-checks against source pages

### Output
- `ste-code/grouped/master-raw.md` — concatenated raw (temporary)
- `ste-code/grouped/master.md` — deduplicated, organized (permanent)

### Deduplication Operations (Operationalized)

Do not describe deduplication. Run these operational commands. The commands detect and remove duplicate rule statements, example pairs, category listings, and dictionary entries.

#### Find Duplicate Rule Headers

```bash
# List rule headers that appear more than once
grep "^#### Rule" ste-code/grouped/master-raw.md | sort | uniq -d

# Count occurrences of each rule header
grep "^#### Rule" ste-code/grouped/master-raw.md | sort | uniq -c | sort -rn
```

#### Find Duplicate Dictionary Entries

```bash
# Extract all dictionary entry headers (WORD (POS) - APPROVED/UNAPPROVED)
grep "^#### [A-Z]" ste-code/grouped/master-raw.md | sort | uniq -d

# Count entries that appear more than once
grep "^#### [A-Z]" ste-code/grouped/master-raw.md | sort | uniq -c | sort -rn | head -20
```

#### Find Duplicate Category Listings

```bash
# Category headers that appear more than once
grep "^### Category" ste-code/grouped/master-raw.md | sort | uniq -d
```

#### Automated Deduplication Script

Save this script as `ste-code/grouped/deduplicate.sh`. It performs a conservative first-pass deduplication:

```bash
#!/bin/bash
# deduplicate.sh — remove exact duplicate blocks from master-raw.md
# Writes deduplicated output to master-dedup.md

INPUT="ste-code/grouped/master-raw.md"
OUTPUT="ste-code/grouped/master-dedup.md"
TEMP=$(mktemp)

echo "Deduplication Report"

# Step 1: Find duplicate rule headers
echo "--- Rule duplicates ---"
dup_rules=$(grep "^#### Rule" "$INPUT" | sort | uniq -d)
if [ -z "$dup_rules" ]; then
  echo "No duplicate rule headers found."
else
  echo "$dup_rules"
  echo "Count: $(echo "$dup_rules" | wc -l) duplicate rule headers"
fi

# Step 2: Find duplicate category headers
echo "--- Category duplicates ---"
dup_cats=$(grep "^### Category" "$INPUT" | sort | uniq -d)
if [ -z "$dup_cats" ]; then
  echo "No duplicate category headers found."
else
  echo "$dup_cats"
  echo "Count: $(echo "$dup_cats" | wc -l) duplicate category headers"
fi

# Step 3: Find duplicate dictionary entry headers
echo "--- Dictionary duplicates ---"
dup_dict=$(grep "^#### [A-Z]" "$INPUT" | sort | uniq -d)
if [ -z "$dup_dict" ]; then
  echo "No duplicate dictionary entry headers found."
else
  echo "$dup_dict" | head -20
  count=$(echo "$dup_dict" | wc -l)
  echo "Count: $count duplicate dictionary entry headers"
fi

# Step 4: Mark all duplicate header locations with line numbers
echo "--- Duplicate locations ---"
grep -n "^#### Rule" "$INPUT" | sort -t: -k2 | uniq -d -f 1 2>/dev/null || true
grep -n "^### Category" "$INPUT" | sort -t: -k2 | uniq -d -f 1 2>/dev/null || true

echo "Deduplication complete"
echo "Review duplicates above. Keep first occurrence of each."
echo "Output: $OUTPUT"

rm -f "$TEMP"
```

#### Manual Deduplication Rules

After the script finds duplicates, apply these rules:

- **Duplicate rule statements**: keep first occurrence. Note the line numbers of later occurrences. Remove them.
- **Duplicate example pairs**: keep first occurrence. An example pair is duplicate when both the STE and non-STE lines are identical.
- **Duplicate dictionary entries**: keep from the page where the WORD header first appears. If the same entry has different formatting in different workers, keep the version that matches RAIL 5 format from `.agents/references/rails.md`.
- **Page boundary overlap**: merge adjacent pages. Drop repeated lines at the boundary. A boundary overlap is detected when the last 3 lines of worker N match the first 3 lines of worker N+1.

---

### Worked Example: Merge Output Structure

This is an excerpt from a correctly merged `master.md` showing the section structure:

```
# ASD-STE100 Issue 9 — Master Extraction

## Front Matter (pages 1-42)

[Title page, copyright notice, table of contents, introduction]

---

## Part 1 — Writing Rules (pages 43-128)

### Section 1 — Words (Rules 1.1-1.14)

#### Rule 1.1
Use approved words from the STE dictionary.

Only words that appear in the dictionary are approved. Use approved words
when they are available. Technical names and technical verbs are the
only exceptions.

> **STE:** Use the approved words from the dictionary.
> **Non-STE:** Utilize the sanctioned terminology from the lexicon.

#### Rule 1.2
Use words only as their specified part of speech.

Each approved word has a specified part of speech (POS). Use the word
only as that POS. For example, use "test" only as a noun, not as a verb.

> **STE:** Do a test of the system.
> **Non-STE:** Test the system.

#### Rule 1.3
Use words only with their approved meanings.

...

### Section 2 — Noun Clusters (Rules 2.1-2.3)

...

### Technical Noun Categories

### Category 1 — Official parts information
...

### Category 19 — Terminal colors and themes
...

---

## Part 2 — Dictionary (pages 129-360)

#### ABOVE (prep) — APPROVED
- **Meaning:** In or to a higher position
- **Forms:** above
- **STE:** The indicator light is above the switch.
- **Non-STE:** The indicator light is on top of the switch.

#### ACCESS (n) — APPROVED
- **Meaning:** The right to go into or near
- **Forms:** access, accesses, accessed, accessing
- **STE:** Get access to the control panel.
- **Non-STE:** You can access the control panel.

...

---

## Appendices (pages 361-434)

[Change history, flowchart, index, change form, reference documents]
```

This example shows:
- Correct section hierarchy (## Part → ### Section → #### Rule)
- Rule numbers in ascending order within each section
- Exactly 19 category entries under Part 1
- Dictionary entries with WORD (POS), APPROVED/UNAPPROVED, meaning, forms, and example pairs
- Em dashes (—) used as section separators, not hyphens

---

### Merge Failure Recovery

If the merge validation fails (wrong rule count, wrong category count, wrong file size):

| Failure | Root Cause | Recovery Action |
|---------|------------|-----------------|
| `grep -c "^#### Rule"` returns < 53 | One or more rules were not extracted or were lost in deduplication | Check which rules are missing: `for s in 1 2 3 4 5 6 7 8 9; do for r in $(seq 1 14); do grep -q "^#### Rule $s.$r" ste-code/grouped/master.md || echo "MISSING: Rule $s.$r"; done; done`. Re-extract the pages that contain missing rules. |
| `grep -c "^#### Rule"` returns > 53 | Deduplication failed — duplicate rule headers remain | Run the deduplication script again. Check output: `grep "^#### Rule" ste-code/grouped/master.md \| sort \| uniq -d`. Remove all but the first occurrence of each duplicate. |
| `grep -c "^### Category"` returns < 19 | Categories were split across page boundaries and not merged | Find which categories are missing. Check the original spec pages 43-128 for the category listing. Re-extract the category section if needed. |
| File size < 500KB | Concatenation missed files or a worker produced empty output | Run: `find ste-code/$INPUT_DIR -name "*.md" -size 0`. Re-extract any zero-byte files. Re-concatenate. |
| Spot-check mismatch (content does not match source) | Worker paraphrased or fabricated content | Identify the worker that produced the incorrect content. Re-extract those pages. The worker file naming convention maps page ranges: worker wNNN covers pages (NNN-1)*4+1 to min(NNN*4, 434). |
| master-raw.md contains binary content or encoding errors | Worker output contains non-UTF-8 characters | Run: `file ste-code/grouped/master-raw.md`. If it says "data" instead of "UTF-8 text", find the offending worker: `for f in ste-code/$INPUT_DIR/*.md; do file "$f" \| grep -v "UTF-8" && echo "BAD: $f"; done`. Re-extract those workers. |

**General merge recovery protocol:**

1. Do not delete master-raw.md. It is the concatenated source. Fix problems there.
2. After fixing, re-run deduplication and organization.
3. Re-run validation after every fix.
4. If the same validation check fails three times, stop. Write the failure to `.agents/feedback/exchange.md`. Include the specific check, the expected value, the actual value, and the actions you attempted.

---

## Stage 4 — Adaptation

### Overview
Adapt the 53 writing rules + 19 categories + synonym/polysemy tables from master.md into code-domain equivalents. Write to `ste-code/adapted/`.

### Adaptation Workers

Launch in batches of 3, same pattern as extraction/refinement. Generate prompts for adaptation workers using the section breakdown:

| Worker | Section | Rules | Output |
|--------|---------|-------|--------|
| a001 | Sec 1 — Words | 1.1–1.14 | a-sec1-rules.md |
| a002 | Sec 2 — Noun Clusters | 2.1–2.3 | a-sec2-rules.md |
| a003 | Sec 3 — Verbs | 3.1–3.7 | a-sec3-rules.md |
| a004 | Sec 4 — Sentences | 4.1–4.4 | a-sec4-rules.md |
| a005 | Sec 5 — Procedures | 5.1–5.5 | a-sec5-rules.md |
| a006 | Sec 6 — Descriptive | 6.1–6.6 | a-sec6-rules.md |
| a007 | Sec 7 — Safety | 7.1–7.3 | a-sec7-rules.md |
| a008 | Sec 8 — Punctuation | 8.1–8.7 | a-sec8-rules.md |
| a009 | Sec 9 — Practices | 9.1–9.4 + GR1-GR4 | a-sec9-rules.md |
| a010 | Categories | 19 categories | a-categories.md |
| a011 | Dictionary + Appendices | A-Z + change history | a-dictionary.md |

### Launch Command for Adaptation Workers

Use the same `hermes` command pattern as extraction workers. Each worker reads master.md and adapts one section:

```bash
# Launch adaptation workers in background with notification
hermes -z "Read ste-code/grouped/master.md. Focus on Section 1 — Words (Rules 1.1-1.14). Adapt every rule from aerospace to code documentation domain. PRESERVE rule numbers and section structure. REPLACE aerospace examples with code examples (API docs, commit messages, README sections). For each rule: write original rule text, then code-domain rewrite, then STE/non-STE code example pairs. Output ONLY the adaptation. Write to ste-code/adapted/a-sec1-rules.md." -m poolside/laguna-s-2.1:free &

hermes -z "Read ste-code/grouped/master.md. Focus on Section 2 — Noun Clusters (Rules 2.1-2.3). Adapt every rule from aerospace to code documentation domain. ..." -m poolside/laguna-s-2.1:free &

# Continue for all 11 workers (a001 through a011)
```

NOTE: Launch in batches of 3 to avoid resource contention. Wait for each batch to complete before launching the next batch.

### Adaptation Prompt Template
```
Read ste-code/grouped/master.md. Focus on <<SECTION>>. 
Adapt every rule, category, and example from aerospace to code documentation domain.
PRESERVE: rule numbers, section structure, STE/non-STE pair format.
REPLACE: aerospace examples → code examples (API docs, commit messages, README sections).
For each rule: write original rule text, then code-domain rewrite, then STE/non-STE code example pairs.
Write to ste-code/adapted/<<OUTPUT_FILE>>. Output ONLY the adaptation file.
```

### Preserve/Replace Rules

**PRESERVE (unchanged):**
- All 53 rule numbers and 9-section organization
- 6-pass transformation pipeline
- Dictionary architecture: APPROVED (UPPERCASE) vs UNAPPROVED (lowercase)
- 19 Technical Code Noun categories (adapted from STE's 19)
- Safety instruction format (WARNING/CAUTION → BREAKING/DEPRECATED)

**REPLACE (adapt for code domain):**
- Aerospace examples → code documentation examples
- Technical noun categories → code-domain categories (keywords, frameworks, dependencies, etc.)
- Vocabulary → code-domain approved words
- Safety WARNING/CAUTION → BREAKING/DEPRECATED/NOTE

### Validation
- All 53 rule numbers present in adapted files
- Every adapted rule references original rule number from master.md
- All examples are code-domain (no aerospace examples)
- 19 categories mapped per category-mapping.md

---

### Worked Example: Adapted Rule Transformation

This is a complete before/after example showing how Rule 4.1 (Sentence Length) transforms from aerospace to code domain:

**ORIGINAL (from master.md):**

```
#### Rule 4.1
Keep sentences short. Write a maximum of 20 words in each procedural
sentence. Write a maximum of 25 words in each descriptive sentence.

> **STE:** Remove the four bolts from the access panel.
> **Non-STE:** The mechanic should proceed to take out all four of the
>   bolts that hold the access panel in place before he goes any further.
```

**ADAPTED (written to ste-code/adapted/a-sec4-rules.md):**

```
### Rule 4.1 — Sentence Length (Adapted from Rule 4.1, master.md)

Keep sentences short. Write a maximum of 20 words in each procedural
sentence. Write a maximum of 25 words in each descriptive sentence.

**Code-domain adaptation:**
The length limits are identical. In code documentation, procedural
sentences appear in setup guides, API instructions, and deployment
steps. Descriptive sentences appear in README overviews, architecture
documents, and code comments.

> **Non-STE:** In order to get started with this application, you will
>   need to first install all of the required dependencies that are
>   listed in the package.json file and then after that is completed
>   you can proceed to run the development server.
>
> **STE:** Install the dependencies from package.json. Then start the
>   development server.

> **Non-STE:** The authentication middleware, which is responsible for
>   validating tokens that are sent with each HTTP request, will reject
>   any request where the token has expired or is otherwise invalid.
>
> **STE:** The authentication middleware validates tokens in each HTTP
>   request. It rejects requests with expired or invalid tokens.
```

**Key transformation points:**
- Rule number and core instruction are preserved exactly
- Aerospace example (bolts, access panel) becomes code-domain (dependencies, dev server)
- The sentence-length limits (20/25 words) apply identically in both domains
- Each adaptation includes a Non-STE/STE pair showing the transformation
- The adapted rule cites its source: "Adapted from Rule 4.1, master.md"

---

### Worked Example: WARNING/CAUTION → BREAKING/DEPRECATED/NOTE

```
### Rule 7.1 — Safety Signal Mapping (Adapted from Rule 7.1, master.md)

Safety signals in aerospace map to code-domain signals as follows:

| STE Signal | Code-Domain Signal | When to Use |
|------------|-------------------|-------------|
| WARNING (injury or death) | BREAKING | Irreversible data loss, auth bypass, security vulnerability |
| CAUTION (equipment damage) | DEPRECATED | API removal, config format change, behavior change with migration path |
| NOTE (important info) | NOTE | Constraints, preconditions, non-obvious behavior |

> **Original WARNING:** DO NOT TOUCH THE HOT EXHAUST. IT CAN BURN YOU.
> **STE-Code BREAKING:** This migration drops the `legacy_users` table.
>   All user data in that table will be deleted. Make a full database
>   backup before you run this migration.

> **Original CAUTION:** MAKE SURE THAT THE LOCKWIRE IS TIGHT. A LOOSE
>   LOCKWIRE CAN CAUSE DAMAGE TO THE ENGINE.
> **STE-Code DEPRECATED:** The `v1/auth` endpoint will be removed in
>   version 4.0. Use `v2/oauth` instead. See the migration guide at
>   docs/migration/v1-to-v2.md.

> **Original NOTE:** This procedure is for the left engine only.
> **STE-Code NOTE:** This configuration applies only to the production
>   environment. Staging and development environments use different
>   rate-limit values.
```

---

### Adaptation Failure Recovery

Adaptation failures occur when a worker produces incorrect, incomplete, or domain-wrong output.

| Failure | Detection | Recovery Action |
|---------|-----------|-----------------|
| Aerospace examples in adapted output | `grep -i "aircraft\|flight\|wing\|landing\|engine\|cockpit\|fuselage" ste-code/adapted/a-sec*-rules.md \| grep -v "## Original Rule"` | The adaptation worker did not replace aerospace examples. Re-launch the worker for that section with a stricter prompt that explicitly bans aerospace terms. See the prompt template below. |
| Adapted rule missing source reference | `grep -L "Adapted from.*master.md" ste-code/adapted/a-sec*-rule*.md` | The worker produced a rule without tracing it to master.md. Re-launch the worker with instruction: "Every adapted rule MUST include 'Adapted from Rule X.Y, master.md'." |
| Code-domain example uses non-approved words | Manual spot-check finds "utilize," "leverage," "commence" in adapted examples | The worker did not apply the synonym table. Re-read the synonym table from master.md. Re-launch the worker with the synonym table appended to the prompt. |
| Adapted dictionary entry has wrong part of speech | Cross-check 10 random entries from a-dictionary.md against master.md | The POS lock in Pass 3 was skipped. Re-launch the dictionary worker (a011) with explicit instruction: "Preserve the part of speech tag from the STE dictionary exactly. Do not change (n) to (v) or vice versa." |
| Category mismatch (wrong code-domain mapping) | Compare category names in a-categories.md against the canonical 19 from `.agents/references/category-mapping.md` | Re-launch the categories worker (a010) with the canonical mapping table appended. Instruct it to use exactly these 19 categories and no others. |

#### Stricter Re-Launch Prompt for Aerospace Contamination

When an adaptation worker produces aerospace examples, re-launch with this prompt:

```
CRITICAL: Your previous output contained aerospace examples. This is a failure.

Read ste-code/grouped/master.md. Focus on <<SECTION>>.
Adapt every rule to the code documentation domain.

FORBIDDEN terms (do NOT use in any example):
aircraft, engine, landing gear, fuselage, cockpit, APU, ECS, wing, flap, throttle,
hydraulic, pneumatic, avionics, ATA chapter, airworthiness, airframe

REQUIRED terms (use in examples):
function, module, endpoint, API, deployment, dependency, configuration, repository,
commit, pull request, build, test, lint, database, query, cache, server, client

PRESERVE: rule numbers, section structure, STE/non-STE pair format.
For each rule: write original rule text, code-domain rewrite, code-domain example pairs.
Every adapted rule MUST include "Adapted from Rule X.Y, master.md".
Write to ste-code/adapted/<<OUTPUT_FILE>>. Output ONLY the adaptation file.
```

---

## Stage 5 — Artifacts

Generate 6 artifact files in `ste-code/artifacts/`:

| # | File | Target |
|---|------|--------|
| 1 | ste-code-distilled-system-prompt.txt | ~1,200 tokens |
| 2 | ste-code-self-reading-manual.txt | ~7,000 tokens |
| 3 | ste-code-extraction-methodology.txt | ~1,400 tokens |
| 4 | ste-code-example-turn.txt | ~500 tokens |
| 5 | ste-code-deployment-guide.txt | ~1,800 tokens |
| 6 | README.md | ~500 tokens |

### Artifact Quality Gates (Cross-Reference)

The full quality gate checklist with pass/fail criteria, verification scripts, and failure recovery for all 6 artifacts lives in `.agents/skills/artifacts/SKILL.md`. This section covers only the Stage 5 generation protocol. For detailed quality gates, see:

| Resource | Path | Content |
|----------|------|---------|
| Quality gate checklist | `.agents/skills/artifacts/SKILL.md` § Pre-Generation Checklist | 7 checks before generation starts |
| Artifact 1 pass/fail | `.agents/skills/artifacts/SKILL.md` § Artifact 1 Quality Gates | 5 criteria with character budget |
| Artifact 2 pass/fail | `.agents/skills/artifacts/SKILL.md` § Artifact 2 Quality Gates | 8 criteria including S6 question count |
| Artifact 3 pass/fail | `.agents/skills/artifacts/SKILL.md` § Artifact 3 Quality Gates | 5 criteria with 6-pass naming |
| Artifact 4 pass/fail | `.agents/skills/artifacts/SKILL.md` § Artifact 4 Quality Gates | 5 criteria with worked example |
| Artifact 5 pass/fail | `.agents/skills/artifacts/SKILL.md` § Artifact 5 Quality Gates | 7 criteria with deployment targets |
| Artifact 6 pass/fail | `.agents/skills/artifacts/SKILL.md` § Artifact 6 Quality Gates | 5 criteria with benchmark results |
| Failure recovery | `.agents/skills/artifacts/SKILL.md` § Failure Recovery | 8 common failures with root causes and recovery actions |
| Edge cases | `.agents/skills/artifacts/SKILL.md` § Edge Cases | 7 edge cases (stale master, incomplete dictionary, truncated adapted files, disk space, partial regen, model change) |
| Verification script | `.agents/skills/artifacts/SKILL.md` § Full Verification Script | Single bash script that runs all pass/fail checks |
| Integration test | `.agents/skills/artifacts/SKILL.md` § Post-Generation Integration Test | 5 cross-artifact consistency checks |

### Generation Protocol
1. Read relevant sections from master.md + adapted files
2. Apply preserve/replace rules
3. Write artifact file
4. Run quality gate checklist (see `.agents/skills/artifacts/SKILL.md`)
5. Fix failures before next artifact

### Anti-Fabrication Rules
- Every adapted rule MUST reference a specific rule_number from master.md
- Every synonym MUST trace to master.md's synonym table
- Every category MUST match one of the 19 from master.md
- Every example MUST be an adaptation of a real STE/non-STE pair
- No invented code terms without a master.md source

---

### Worked Example: Artifact 1 Excerpt (System Prompt)

This is the first 30 lines of a passing Artifact 1. It shows the expected format:

```
# STE-Code System Prompt — Level 1

You are STE-Code, a Simplified Technical English for Code documentation.
Your purpose: make technical documentation for software clear, consistent,
and unambiguous.

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
P11. One term per concept — be consistent (Rule 1.11)
P12. Technical verbs (build, deploy, test, lint) are allowed (Rule 1.12)
P13. Do not use technical verbs as nouns (Rule 1.13)
P14. Use American English spelling (Rule 1.14)

## Canonical Synonym Table (code domain)
| Prefer | Avoid |
|--------|-------|
| use | utilize, leverage, employ |
| start | initiate, commence, bootstrap |
| stop | terminate, halt, kill |
...
```

The full artifact continues with the output format rules and anti-patterns. See `.agents/skills/artifacts/SKILL.md` § Artifact 1 Worked Example for the complete reference.

---

### Worked Example: Artifact 4 (Worked Example Turn)

This is a full passing Artifact 4. It demonstrates one complete STE-Code transformation on a real code-documentation sentence:

```
INPUT (non-compliant):
"Utilize the initialize() function in order to commence the server, it
should be able to handle multiple simultaneous connections effectively."

--- TRANSFORMATION ---

Step 1 — Synonym replacement (Rule 1.11, synonym table):
"utilize" → "use", "commence" → "start", "in order to" → "to"

Step 2 — Sentence splitting (Rule 4.1):
One sentence → two sentences. Break at the comma splice.

Step 3 — Remove filler (Rule 4.3):
"should be able to" → remove. State the fact directly.

Step 4 — Approve vocabulary (Rules 1.1, 1.2, 1.3):
"simultaneous" → "at the same time" (simultaneous is not approved)
"effectively" → remove (filler adverb, Rule 4.3)

--- OUTPUT (STE-Code compliant) ---

Use the initialize() function to start the server.
The server handles multiple connections at the same time.
```

This example demonstrates synonym replacement, sentence splitting, filler removal, and vocabulary approval in 4 steps with 4 rule citations.

---

### Artifact Generation Failure Recovery

If artifact generation fails, diagnose and recover using the quality gate tables in `.agents/skills/artifacts/SKILL.md`. This is a summary of the most common failures:

| Failure | Root Cause | Recovery Action |
|---------|------------|-----------------|
| Artifact 1 has fewer than 14 principles | Adapted Section 1 file is incomplete | Re-read `ste-code/adapted/a-sec1-rules.md`. Check that Rules 1.1-1.14 are all present. If not, re-run adaptation for Section 1. |
| Artifact 2 has wrong rule count (not 53) | Adapted files are incomplete or duplicated | Count rules per adapted file: `grep -c "^### Rule" ste-code/adapted/a-sec*.md`. Sum must be 53. Regenerate any file with wrong count. |
| Artifact 2 has fewer than 13 questions in S6 | Questions were dropped during adaptation | Re-read master.md Section 6. Extract exactly the 13 questions. Do not add or remove questions. |
| Artifact 4 has fewer than 3 rule citations | Transformation is too simple | Add a Step line for each transformation action. Each Step must cite at least one rule number. |
| Artifact 5 is missing a deployment target | Worker skipped a section | Check that Ollama, LM Studio, and Python each have a dedicated section. Add any missing section. |
| Aerospace terms found in any artifact | `grep -i "aircraft\|flight\|wing\|engine" ste-code/artifacts/*.txt` returns results | The adapted source files still have aerospace content. Go back to Stage 4 and fix the adaptation before regenerating artifacts. |
| Artifact 6 mentions wrong model name | Agent invented "deepseek-pro" or similar | Search artifacts for "deepseek". Replace any variant with `poolside/laguna-s-2.1:free`. |

---

## Progress Tracking

Update `.agents/state/PROGRESS.md` after every completed stage. Signal in `.agents/feedback/exchange.md` with agent perspective tag:

```markdown
## Agent #N → Reviewer — Stage X Complete
[status, metrics, next stage]
```

---

## Cross-References

This skill orchestrates Stages 3-5. Other skills provide input, validation, and detailed protocols.

| Skill | Path | How It Relates |
|-------|------|---------------|
| **Extraction** | `.agents/skills/extraction/SKILL.md` | Produces the 109 worker files that feed Stage 3. If extracted/ is incomplete, re-run Stage 1. |
| **Refinement** | `.agents/skills/refinement/SKILL.md` | Produces refined files in refined/. Used by Agent #2 as Stage 3 input. |
| **Merging** | `.agents/skills/grouping/SKILL.md` | Full merge protocol with 7 edge cases and 6 validation steps. This skill's Stage 3 section is the abbreviated version. For the complete protocol, see grouping SKILL.md. |
| **Adaptation** | `.agents/skills/adaptation/SKILL.md` | Full adaptation protocol with 9 verification gates, 5 worked examples, and 5 edge cases. This skill's Stage 4 section is the abbreviated version. |
| **Artifacts** | `.agents/skills/artifacts/SKILL.md` | Full artifact generation protocol with quality gates for all 6 artifacts, verification script, failure recovery, edge cases, and integration tests. This skill's Stage 5 section references it. |
| **Validation** | `.agents/skills/validation/SKILL.md` | Per-batch quality checks, truncation detection, fabrication detection. Apply these checks after each stage. |
| **Auditing** | `.agents/skills/auditing/SKILL.md` | 8-rail verification against fabrication. Run after Stage 5 on Artifacts 1, 2, and 5. |

---

## Post-Stage Verification Checklist

After completing any stage (3, 4, or 5), run this cross-check before declaring the stage complete:

### After Stage 3 (Merge)
- [ ] master.md exists and is > 500KB
- [ ] `grep -c "^#### Rule" ste-code/grouped/master.md` returns 53
- [ ] `grep -c "^### Category" ste-code/grouped/master.md` returns 19
- [ ] No duplicate rule headers: `grep "^#### Rule" ste-code/grouped/master.md | sort | uniq -d` returns empty
- [ ] All letters A-Z have dictionary entries
- [ ] master-raw.md is preserved (do not delete it — Stage 4 workers may need it for context)
- [ ] Spot-check 10 pages: content matches source

### After Stage 4 (Adaptation)
- [ ] At least 11 adapted files in `ste-code/adapted/`
- [ ] All 53 rules adapted: `grep -c "^### Rule" ste-code/adapted/a-sec*-rules.md | awk -F: '{s+=$2} END {print s}'` returns 53
- [ ] Zero aerospace terms survive outside original rule blocks: `grep -rn "aircraft\|engine\|landing gear\|cockpit" ste-code/adapted/ | grep -v "## Original Rule" | wc -l` returns 0
- [ ] All adapted rules cite source: `grep -L "Adapted from.*master.md" ste-code/adapted/a-sec*-rules.md` returns empty
- [ ] `grep -c "APPROVED" ste-code/adapted/a-dictionary.md` returns > 800
- [ ] No adapted file is truncated: `for f in ste-code/adapted/a-*.md; do tail -1 "$f" | grep -q "[.!?]$" || echo "TRUNCATED: $f"; done` returns empty

### After Stage 5 (Artifacts)
- [ ] All 6 artifact files exist
- [ ] Model name is correct everywhere: `grep -rh "deepseek" ste-code/artifacts/ | sort -u` returns only `poolside/laguna-s-2.1:free`
- [ ] Full verification script from `.agents/skills/artifacts/SKILL.md` passes all checks
- [ ] Integration test from `.agents/skills/artifacts/SKILL.md` passes all 5 consistency checks
- [ ] PROGRESS.md updated with final artifact counts and timestamps

---

## Edge Cases (Cross-Stage)

These edge cases span multiple stages. Stage-specific edge cases live in their respective skill files.

### Edge Case: enriched/ Has 108 Files Instead of 109

**Detection:** `ls ste-code/enriched/w*-p*.md | wc -l` returns 108.

**Cause:** One enrichment worker failed or was not launched.

**Action:**
1. Find the missing page range: compare file lists between enriched/ and extracted/.
   ```bash
   diff <(ls ste-code/enriched/w*-p*.md | sed 's/w.*-p//' | sed 's/\.md//' | sort -n) \
        <(ls ste-code/extracted/w*-p*.md | sed 's/w.*-p//' | sed 's/\.md//' | sort -n)
   ```
2. Use the corresponding extracted/ file for the missing pages.
3. Merge enriched/ (108 files) + the 1 extracted/ file for the gap.
4. Note the gap in PROGRESS.md.

### Edge Case: refined/ and extracted/ Both Exist but One Is Stale

**Detection:** Timestamp comparison shows one directory has significantly older files.

**Action:**
1. Use the directory with newer files as the primary source.
2. If the newer directory has fewer files, fill gaps from the older directory.
3. Record the decision in exchange.md: which source was used, why, and what gaps were filled.

### Edge Case: master.md Exists but Has 0 Bytes

See Stage 3 Edge Case above for the full recovery procedure.

### Edge Case: Two Agents Try to Run the Same Stage Simultaneously

**Detection:** Two exchange.md entries claim Stage 3 (or 4, or 5) is in progress.

**Action:**
1. The agent that started first owns the stage. The later agent must stop.
2. The later agent writes to exchange.md: "Stage X already in progress by Agent #N. Yielding."
3. The later agent polls PROGRESS.md every 60 seconds until the stage completes.
4. If PROGRESS.md does not update within 10 minutes, the first agent has stalled. The later agent may take over. Write the takeover to exchange.md.

### Edge Case: master.md Passes Validation but Adapted Files Are Stale

**Detection:** master.md has a newer timestamp than adapted files.

**Cause:** master.md was regenerated after adaptation completed. The adapted files still reference the old master.md content.

**Action:**
1. Check if the rule count in master.md changed. If not, the adaptation may still be valid.
2. Spot-check 5 adapted rules against the new master.md. If they match, the timestamps are misleading (file touch, not content change).
3. If adapted rules are genuinely stale, re-run Stage 4 from the new master.md.

---

## Immutable Facts
- 19 technical noun categories (NOT 22)
- 53 writing rules + 4 GR rules (NOT 65)
- Model: poolside/laguna-s-2.1:free (NOT deepseek-pro or v4-flash)
- 434 pages in ASD-STE100 Issue 9
- 109 extraction workers (pages 1-434, 4 pages each)
- 11 adaptation workers (9 sections + categories + dictionary)
- 6 final artifacts (system prompt, manual, methodology, example, deployment guide, README)
