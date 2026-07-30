---
name: ste-code-continuation
description: "Multi-agent continuation skill for Stages 3-5 (merge, adapt, artifacts) — usable by Agents #1, #2, or #3 from their own perspective to track and advance pipeline stages."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [ste-code, continuation, merge, adapt, artifacts, multi-agent]
    replaces: agent-4-continuation.md
---

# STE-Code Continuation Skill — Stages 3-5

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

### File Count Check

```bash
# Check which files exist and determine active stage
ls ste-code/enriched/w*-p*.md 2>/dev/null | wc -l  # enriched count
ls ste-code/refined/r*.md 2>/dev/null | wc -l        # refined count
ls ste-code/extracted/w*-p*.md 2>/dev/null | wc -l   # extracted count
ls ste-code/merged/master.md 2>/dev/null              # merge exists?
ls ste-code/adapted/*.md 2>/dev/null | wc -l         # adaptation count
ls ste-code/artifacts/*.txt 2>/dev/null | wc -l      # artifact count
```

### Timestamp Staleness Check

```bash
# Check if merged/master.md is newer than its source files
SOURCE_DIR="ste-code/extracted"
if [ -f ste-code/merged/master.md ]; then
  NEWEST_SRC=$(ls -t ste-code/$SOURCE_DIR/w*-p*.md 2>/dev/null | head -1)
  if [ -n "$NEWEST_SRC" ] && [ "$NEWEST_SRC" -nt ste-code/merged/master.md ]; then
    echo "STALE: master.md is older than source files → RE-MERGE"
  fi
fi

# Check if adapted/ files are newer than master.md
if [ -f ste-code/merged/master.md ]; then
  ADAPTED_NEWEST=$(ls -t ste-code/adapted/*.md 2>/dev/null | head -1)
  if [ -n "$ADAPTED_NEWEST" ] && [ ste-code/merged/master.md -nt "$ADAPTED_NEWEST" ]; then
    echo "STALE: adapted/ is older than master.md → RE-ADAPT"
  fi
fi
```

### File Size Truncation Check

```bash
# Merge: master.md must exceed 500KB (validated master)
MERGE_SIZE=$(wc -c < ste-code/merged/master.md 2>/dev/null || echo 0)
[ $MERGE_SIZE -lt 500000 ] && echo "TRUNCATED: master.md < 500KB → RE-MERGE"

# Adaptation: each adapted file must exceed 2KB
for f in ste-code/adapted/*.md; do
  SIZE=$(wc -c < "$f" 2>/dev/null || echo 0)
  [ $SIZE -lt 2000 ] && echo "TRUNCATED: $f < 2KB → RE-ADAPT worker"
done

# Artifacts: each artifact must be within 30% of target size
# Artifact 1 target: ~4,800 chars → min 3,360 chars
# Artifact 2 target: ~28,000 chars → min 19,600 chars
# Artifact 3 target: ~5,600 chars → min 3,920 chars
# Artifact 4 target: ~2,000 chars → min 1,400 chars
# Artifact 5 target: ~7,200 chars → min 5,040 chars
```

### Partial Stage Completion Detection

```bash
# Adaptation: 11 files expected (a-sec1 through a-sec11 + a-dictionary)
ADAPTED_COUNT=$(ls ste-code/adapted/*.md 2>/dev/null | wc -l)
case $ADAPTED_COUNT in
  0)  echo "Stage 4: NOT STARTED" ;;
  [1-9]|10) echo "Stage 4: PARTIAL ($ADAPTED_COUNT/11 files) — RESUME" ;;
  11) echo "Stage 4: COMPLETE — verify and proceed" ;;
esac

# Artifacts: 6 files expected (5 .txt + README.md)
ARTIFACT_COUNT=$(ls ste-code/artifacts/*.txt ste-code/artifacts/README.md 2>/dev/null | wc -l)
case $ARTIFACT_COUNT in
  0)  echo "Stage 5: NOT STARTED" ;;
  [1-5]) echo "Stage 5: PARTIAL ($ARTIFACT_COUNT/6 files) — RESUME" ;;
  6) echo "Stage 5: COMPLETE — verify and report" ;;
esac
```

### Decision Tree

1. Run all checks above (count, timestamp, size, partial).
2. Make the decision in this order:

```
FOR EACH STAGE (3→4→5) in sequence:
  If stage output exists AND passes size check AND passes timestamp check
    → SKIP stage (already complete)
  Else if stage output exists AND fails size/timestamp check
    → DELETE partial output, RE-RUN stage from start
  Else if partial output exists (some files but not all)
    → RESUME stage from first missing worker/artifact
  Else
    → RUN stage from start
```

- If merged/master.md missing, stale, or truncated → do Stage 3 (Merge)
- If adapted/ has fewer than 11 files or any file < 2KB → do Stage 4 (Adapt)
- If artifacts/ has fewer than 6 files or any file outside 30% of target → do Stage 5 (Artifacts)
- If all complete → verify and report

### Edge Case Matrix

| Condition | Action |
|-----------|--------|
| enriched/ has fewer files than extracted/ | Use extracted/ as source. Flag enrichment gap in exchange.md. |
| refined/ has stale timestamps (older than extracted/) | Use extracted/ as source. Flag refinement gap in exchange.md. |
| enriched/ has 50 files but extracted/ has 109 | Use extracted/ (complete set). Log enrichment incomplete in exchange.md. |
| master.md exists but fails rule count (< 53) | Delete master-raw.md and master.md. Re-merge from scratch. |
| master.md exists but fails category count (< 19) | Delete master-raw.md and master.md. Re-merge from scratch. |
| adapted/ has 5 of 11 files | Skip completed workers. Resume from first missing worker index. |
| adapted/ has 11 files but a007.md < 2KB | Re-launch only worker a007. Do not re-run completed workers. |
| artifacts/ has 3 of 6 files | Skip completed artifacts. Resume from artifact #4. |
| artifacts/ has 6 files but #2 is 3,000 chars (target ~28,000) | Regenerate only artifact #2. Flag truncation in exchange.md. |
| No source directory has 109 files | Report to exchange.md: "INCOMPLETE: Stages 1-2 not finished. Awaiting extraction/refinement." Do not proceed. |
| Two source directories available (e.g., extracted + refined) | Prefer refined (higher quality). Fall back to extracted if refined is incomplete. |

---

## Stage 3 — Merge

> **Deep detail in:** `.agents/skills/spec-extraction/ste-code-merge/SKILL.md`  
> This skill provides the dispatcher protocol. The merge skill provides the full deduplication patterns, section structure, and validation commands.

### Input Selection (agent-perspective)
Pick the best available source directory:

```bash
# Agent #1 perspective: prefer enriched, fall back to extracted
INPUT_DIR="ste-code/enriched"
[ $(ls ste-code/enriched/w*-p*.md 2>/dev/null | wc -l) -lt 109 ] && INPUT_DIR="ste-code/extracted"

# Agent #2 perspective: prefer refined, fall back to enriched, then extracted
INPUT_DIR="ste-code/refined"
[ $(ls ste-code/refined/r*.md 2>/dev/null | wc -l) -lt 109 ] && INPUT_DIR="ste-code/enriched"
[ $(ls ste-code/enriched/w*-p*.md 2>/dev/null | wc -l) -lt 109 ] && INPUT_DIR="ste-code/extracted"

# Agent #3 perspective: use extracted (verified by auditor)
INPUT_DIR="ste-code/extracted"
```

### Protocol

1. **Concatenate** all files in page order into `ste-code/merged/master-raw.md`:
   ```bash
   cat ste-code/$INPUT_DIR/w*-p*.md > ste-code/merged/master-raw.md
   ```

2. **Deduplicate** — scan for duplicate content at page boundaries:
   - Duplicate rule statements: keep first occurrence
   - Duplicate example pairs: keep first occurrence
   - Duplicate dictionary entries: keep from the page where the header appears
   - Page boundary overlap: merge adjacent pages, drop repeated lines

3. **Organize by section** into `ste-code/merged/master.md`:
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
   - `grep -c "^#### Rule" ste-code/merged/master.md` → must be 53
   - `grep -c "^### Category" ste-code/merged/master.md` → must be 19
   - File size > 500KB
   - 10 random spot-checks against source pages

### Output
- `ste-code/merged/master-raw.md` — concatenated raw (temporary)
- `ste-code/merged/master.md` — deduplicated, organized (permanent)

### Merge Failure Recovery

If merge validation fails:

1. **Save partial work.** Do not delete master-raw.md. It may contain usable content.
   ```bash
   cp ste-code/merged/master-raw.md ste-code/merged/master-raw-failed-$(date +%Y%m%d-%H%M%S).md
   ```

2. **Diagnose the failure:**
   ```bash
   # Check rule count
   grep -c "^#### Rule" ste-code/merged/master.md
   # Check for missing page ranges
   for i in $(seq 1 109); do
     N=$(printf "%03d" $i)
     [ -f "ste-code/$INPUT_DIR/w${N}-p*.md" ] || echo "MISSING: worker w${N}"
   done
   # Check for zero-byte files
   find ste-code/$INPUT_DIR -name "*.md" -size 0
   ```

3. **Map missing workers to the worker grid** in `references/worker-grid.md`.
   Log which workers produced output and which are missing.

4. **Resume from the first missing worker index:**
   - Launch a targeted extraction worker for the missing page range.
   - Append output to master-raw.md.
   - Re-run deduplication and organization.

5. **If re-merge fails twice:**
   Reduce scope. Split master-raw.md into halves (pages 1-217, 218-434).
   Merge each half independently. Combine results.

---

## Stage 4 — Adaptation

> **Deep detail in:** `.agents/skills/spec-extraction/ste-code-adaptation/SKILL.md`  
> This skill provides the worker orchestration protocol. The adaptation skill provides the full preserve/replace rules, category mapping, and verification criteria.

### Overview
Adapt the 53 writing rules + 19 categories + synonym/polysemy tables from master.md into code-domain equivalents. Write to `ste-code/adapted/`.

### Prerequisites
- [ ] GATE 2 complete: `ste-code/merged/master.md` exists and passes validation
- [ ] All 53 rules confirmed present in master.md
- [ ] All 19 categories enumerated
- [ ] Dictionary entries extracted

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

### Batch Breakdown (4 batches of 3 workers)

| Batch | Workers | Sections | Pages in master.md |
|-------|---------|----------|---------------------|
| **B1** | a001, a002, a003 | Sec 1-3 (Rules 1.1–3.7) | Rules 1.1–3.7 |
| **B2** | a004, a005, a006 | Sec 4-6 (Rules 4.1–6.6) | Rules 4.1–6.6 |
| **B3** | a007, a008, a009 | Sec 7-9 (Rules 7.1–GR4) | Rules 7.1–GR4 |
| **B4** | a010, a011 | Categories + Dictionary | Categories A-Z + Appendices |

### Full Orchestration Protocol

**Launch Rule:** Exactly 3 workers per batch. Never launch more than 3 at once.
Verify output after each batch before launching the next batch.

```bash
# Batch 1: Sections 1-3 (Rules 1.1 through 3.7)
hermes -z "Read ste-code/merged/master.md. Focus on Section 1 (Rules 1.1-1.14), Section 2 (Rules 2.1-2.3), Section 3 (Rules 3.1-3.7). Adapt every rule, category, and example from aerospace to code documentation domain. PRESERVE: rule numbers, section structure, STE/non-STE pair format. REPLACE: aerospace examples → code examples (API docs, commit messages, README sections). For each rule: write original rule text, then code-domain rewrite, then STE/non-STE code example pairs. Write to ste-code/adapted/a-sec1-rules.md. Output ONLY the adaptation file." -m deepseek-v4-pro --yolo &
hermes -z "Read ste-code/merged/master.md. Focus on Section 2 (Rules 2.1-2.3). Adapt every rule, category, and example from aerospace to code documentation domain. PRESERVE: rule numbers, section structure, STE/non-STE pair format. REPLACE: aerospace examples → code examples (API docs, commit messages, README sections). For each rule: write original rule text, then code-domain rewrite, then STE/non-STE code example pairs. Write to ste-code/adapted/a-sec2-rules.md. Output ONLY the adaptation file." -m deepseek-v4-pro --yolo &
hermes -z "Read ste-code/merged/master.md. Focus on Section 3 (Rules 3.1-3.7). Adapt every rule, category, and example from aerospace to code documentation domain. PRESERVE: rule numbers, section structure, STE/non-STE pair format. REPLACE: aerospace examples → code examples (API docs, commit messages, README sections). For each rule: write original rule text, then code-domain rewrite, then STE/non-STE code example pairs. Write to ste-code/adapted/a-sec3-rules.md. Output ONLY the adaptation file." -m deepseek-v4-pro --yolo &
wait
```

**After Batch 1, verify before launching Batch 2:**
```bash
# Verify all 3 files exist and have content
for f in a-sec1-rules.md a-sec2-rules.md a-sec3-rules.md; do
  SIZE=$(wc -c < ste-code/adapted/$f 2>/dev/null || echo 0)
  echo "$f: $SIZE bytes"
  [ $SIZE -lt 2000 ] && echo "WARNING: $f too small — may be truncated"
done
# Confirm rule count from Section 1-3 output
grep -c "^#### Rule" ste-code/adapted/a-sec1-rules.md ste-code/adapted/a-sec2-rules.md ste-code/adapted/a-sec3-rules.md
# Expected: 14 + 3 + 7 = 24 rules across sections 1-3
```

```bash
# Batch 2: Sections 4-6 (Rules 4.1 through 6.6)
hermes -z "Read ste-code/merged/master.md. Focus on Section 4 (Rules 4.1-4.4). Adapt every rule... Write to ste-code/adapted/a-sec4-rules.md." -m deepseek-v4-pro --yolo &
hermes -z "Read ste-code/merged/master.md. Focus on Section 5 (Rules 5.1-5.5). Adapt every rule... Write to ste-code/adapted/a-sec5-rules.md." -m deepseek-v4-pro --yolo &
hermes -z "Read ste-code/merged/master.md. Focus on Section 6 (Rules 6.1-6.6). Adapt every rule... Write to ste-code/adapted/a-sec6-rules.md." -m deepseek-v4-pro --yolo &
wait

# Batch 3: Sections 7-9 (Rules 7.1 through GR4)
hermes -z "Read ste-code/merged/master.md. Focus on Section 7 (Rules 7.1-7.3). Adapt every rule... Write to ste-code/adapted/a-sec7-rules.md." -m deepseek-v4-pro --yolo &
hermes -z "Read ste-code/merged/master.md. Focus on Section 8 (Rules 8.1-8.7). Adapt every rule... Write to ste-code/adapted/a-sec8-rules.md." -m deepseek-v4-pro --yolo &
hermes -z "Read ste-code/merged/master.md. Focus on Section 9 (Rules 9.1-9.4 + GR1-GR4). Adapt every rule... Write to ste-code/adapted/a-sec9-rules.md." -m deepseek-v4-pro --yolo &
wait

# Batch 4: Categories + Dictionary
hermes -z "Read ste-code/merged/master.md. Focus on the 19 technical noun categories and 4 technical verb categories. Adapt all category names, descriptions, and examples from aerospace to code domain. Map per references/category-mapping.md. Write to ste-code/adapted/a-categories.md." -m deepseek-v4-pro --yolo &
hermes -z "Read ste-code/merged/master.md. Focus on Part 2 — Dictionary (pages 129-360) and Appendices (pages 361-434). Adapt every dictionary entry and appendix section from aerospace to code domain. PRESERVE: APPROVED/UNAPPROVED structure, part-of-speech tags, alternative word mappings. REPLACE: aerospace examples → code documentation examples. Write to ste-code/adapted/a-dictionary.md." -m deepseek-v4-pro --yolo &
wait
```

### Adaptation Prompt Template

For each worker, generate a prompt using this template:

```
Read ste-code/merged/master.md. Focus on <<SECTION>>. 
Adapt every rule, category, and example from aerospace to code documentation domain.
PRESERVE: rule numbers, section structure, STE/non-STE pair format.
REPLACE: aerospace examples → code examples (API docs, commit messages, README sections).
For each rule: write original rule text, then code-domain rewrite, then STE/non-STE code example pairs.
Write to ste-code/adapted/<<OUTPUT_FILE>>. Output ONLY the adaptation file.
```

### Worker Retry Protocol

If any adaptation worker fails (timeout, truncated output, missing file):

1. **First failure:** Retry the same worker with the same prompt.
   ```bash
   hermes -z "$(cat .agents/prompts/adapt/a005-prompt.txt)" -m deepseek-v4-pro --yolo
   ```

2. **Second failure (same worker):** Reduce scope. Split the section into two sub-workers.
   Example for worker a005 (Rules 5.1–5.5, 5 rules):
   ```bash
   # Sub-worker A: Rules 5.1-5.3
   hermes -z "Read ste-code/merged/master.md. Focus on Section 5 (Rules 5.1-5.3 only). Adapt... Write to ste-code/adapted/a-sec5-rules-part1.md." -m deepseek-v4-pro --yolo &
   # Sub-worker B: Rules 5.4-5.5
   hermes -z "Read ste-code/merged/master.md. Focus on Section 5 (Rules 5.4-5.5 only). Adapt... Write to ste-code/adapted/a-sec5-rules-part2.md." -m deepseek-v4-pro --yolo &
   wait
   # Combine results
   cat ste-code/adapted/a-sec5-rules-part1.md ste-code/adapted/a-sec5-rules-part2.md > ste-code/adapted/a-sec5-rules.md
   ```

3. **Third failure (same worker):** Flag in exchange.md for manual review. Do not loop.
   ```markdown
   ## Agent #N → Reviewer — Adaptation Worker a005 FAILED
   Worker a005 (Rules 5.1-5.5) failed after 3 attempts.
   Sub-workers for 5.1-5.3 and 5.4-5.5 also failed.
   Manual adaptation required.
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

### Adaptation Checkpoint

After each batch completes, save state:
```bash
git add ste-code/adapted/ && git gcommit-hermes "Stage 4 Batch N: workers a00X-a00Y complete"
```

If the adaptation process is interrupted, resume from the first missing batch:
```bash
# Check which files exist
ls -la ste-code/adapted/
# Find first missing worker index. If a005.md is missing but a001-a004 exist:
# Resume from Batch 2 (a004, a005, a006).
```

---

## Stage 5 — Artifacts

> **Deep detail in:** `.agents/skills/spec-extraction/ste-code-artifacts/SKILL.md`  
> This skill provides the dispatcher protocol. The artifacts skill provides the full per-artifact content requirements, quality gates, and verification commands.

Generate 6 artifact files in `ste-code/artifacts/`:

| # | File | Target | Key Requirements |
|---|------|--------|-----------------|
| 1 | ste-code-distilled-system-prompt.txt | ~1,200 tokens | 14 core principles (P1-P14), synonym table, approved vocabulary policy, 10 anti-patterns, ~4,800 chars |
| 2 | ste-code-self-reading-manual.txt | ~7,000 tokens | 8 sections (S0-S8), all 53 adapted rules, 19 categories, recursive loop diagram, 13 questions in S6, ~28,000 chars |
| 3 | ste-code-extraction-methodology.txt | ~1,400 tokens | 6-pass pipeline, turn-by-turn protocol, 5 extraction types, Mermaid UML output, ~5,600 chars |
| 4 | ste-code-example-turn.txt | ~500 tokens | Non-STE input → STE-Code output, compliance status, Mermaid diagrams, optimization metrics, ~2,000 chars |
| 5 | ste-code-deployment-guide.txt | ~1,800 tokens | 4 deployment options (Ollama, LM Studio, Python+llama.cpp, export), token budget breakdown, ~7,200 chars |
| 6 | README.md | ~500 tokens | What STE-Code is, file listing, quick start (3 steps), architecture summary, design principles, ~2,000 chars |

### Per-Artifact Quality Gates

**Artifact 1 — System Prompt:**
- [ ] All 14 principles reference specific STE rules from master.md
- [ ] Synonym table uses actual canonical forms from master.md (not invented)
- [ ] Anti-patterns are code-specific (not copy-pasted from aerospace)
- [ ] Total ~4,800 chars (~1,200 tokens, within 30% tolerance)
- [ ] Contains IDENTITY, 14 PRINCIPLES, SYNONYM TABLE, VOCABULARY POLICY, OUTPUT FORMAT, ANTI-PATTERNS sections

**Artifact 2 — Self-Reading Manual:**
- [ ] All 8 sections (S0-S8) present and numbered
- [ ] All 53 adapted rules have code-domain example pairs
- [ ] 19 categories listed with code examples
- [ ] Recursive loop diagram present in S0
- [ ] S6 contains exactly 13 questions
- [ ] Total ~28,000 chars (~7,000 tokens, within 30% tolerance)

**Artifact 3 — Extraction Methodology:**
- [ ] Turn 0 initialization protocol present
- [ ] Turns 1+ protocol: READ→TOKENIZE→LEXICAL CHECK→EXTRACT→OPTIMIZE→OUTPUT→ADVANCE
- [ ] 5 structural extraction types adapted for code
- [ ] Final turn consolidation protocol present
- [ ] Mermaid class + flowchart output format described
- [ ] State persistence between turns documented
- [ ] Total ~5,600 chars (~1,400 tokens, within 30% tolerance)

**Artifact 4 — Example Turn:**
- [ ] Non-STE-Code INPUT block present
- [ ] COMPLIANCE STATUS with N violations count
- [ ] STE-CODE OUTPUT block present
- [ ] UML EXTRACTION with Mermaid diagrams
- [ ] OPTIMIZATIONS table with before/after metrics
- [ ] Total ~2,000 chars (~500 tokens, within 30% tolerance)

**Artifact 5 — Deployment Guide:**
- [ ] Option A: Ollama Modelfile instructions
- [ ] Option B: LM Studio GUI steps
- [ ] Option C: Python + llama.cpp programmatic loop
- [ ] Option D: Full conversation export as context
- [ ] Token budget breakdown table
- [ ] Expected output after processing described
- [ ] Total ~7,200 chars (~1,800 tokens, within 30% tolerance)

**Artifact 6 — README.md:**
- [ ] What STE-Code is (2-3 sentences)
- [ ] File listing with sizes
- [ ] Quick start (3 steps)
- [ ] Architecture summary (preserve/replace)
- [ ] Design principles
- [ ] References to ASD-STE100 Issue 9
- [ ] Total ~2,000 chars (~500 tokens, within 30% tolerance)

### Generation Protocol
1. Read relevant sections from master.md + adapted files
2. Apply preserve/replace rules
3. Write artifact file
4. Run quality gate checklist (all checkboxes above)
5. Fix failures before next artifact
6. After each artifact, verify size within 30% of target:
   ```bash
   TARGET=4800; ACTUAL=$(wc -c < ste-code/artifacts/ste-code-distilled-system-prompt.txt)
   MIN=$(($TARGET * 70 / 100)); MAX=$(($TARGET * 130 / 100))
   [ $ACTUAL -ge $MIN ] && [ $ACTUAL -le $MAX ] || echo "SIZE FAIL: $ACTUAL chars (target $TARGET ±30%)"
   ```

### Anti-Fabrication Rules
- Every adapted rule MUST reference a specific rule_number from master.md
- Every synonym MUST trace to master.md's synonym table
- Every category MUST match one of the 19 from master.md
- Every example MUST be an adaptation of a real STE/non-STE pair
- No invented code terms without a master.md source

### Artifact Checkpoint

After each artifact completes, save state:
```bash
git add ste-code/artifacts/ && git gcommit-hermes "Stage 5: Artifact #N complete (ste-code-...)"
```

If interrupted, resume from the first missing artifact:
```bash
# Check which artifacts exist
for f in ste-code-distilled-system-prompt.txt ste-code-self-reading-manual.txt \
         ste-code-extraction-methodology.txt ste-code-example-turn.txt \
         ste-code-deployment-guide.txt README.md; do
  [ -f "ste-code/artifacts/$f" ] && echo "EXISTS: $f" || echo "MISSING: $f"
done
# Resume from first MISSING artifact
```

---

## Failure Recovery & Resume Protocol

### Stage 3 — Merge Recovery

| Failure | Recovery Action |
|---------|-----------------|
| master-raw.md is 0 bytes | Check source directory. Re-run concatenation. If source files are missing, flag in exchange.md. |
| master.md fails rule count (< 53) | Save partial master-raw.md. Run `grep "^#### Rule" ste-code/merged/master.md`. Identify missing rules from master-raw.md. Re-run dedup with corrected boundaries. |
| master.md fails category count (< 19) | Check master-raw.md for category headers. If missing, source files are incomplete. Flag in exchange.md. |
| master.md < 500KB | Concatenation may have missed files. Check `ls ste-code/$INPUT_DIR/ | wc -l`. If < 109, some workers did not complete. Flag in exchange.md. Resume from first missing worker. |
| master.md fails spot-checks | Page boundary dedup may have cut content. Manually audit the 10 failed spot-checks. Adjust dedup boundaries. |

### Stage 4 — Adaptation Recovery

| Failure | Recovery Action |
|---------|-----------------|
| a001-a003 (Batch 1) all fail | Check master.md is valid. If valid, the adaptation prompt may be too aggressive. Reduce scope: adapt 2 rules per worker instead of full section. |
| Single worker times out (e.g., a005) | Retry with same prompt. If fail again, split into sub-workers (see retry protocol above). If fail a third time, flag in exchange.md. |
| Partial batch (2 of 3 workers complete) | Retry only the failed worker. Do not re-run completed workers. |
| Adapted file < 2KB (truncated) | Worker output was cut off. Re-launch with the same prompt. If same result, the section may have sparse content — verify against master.md manually. |
| Adapted file has aerospace examples | Worker did not follow the REPLACE directive. Re-launch with stronger instruction: "Replace ALL aerospace examples. Zero aerospace examples allowed." |

### Stage 5 — Artifact Recovery

| Failure | Recovery Action |
|---------|-----------------|
| Artifact size outside 30% tolerance | Regenerate that artifact only. If too small, expand content. If too large, trim. |
| Artifact missing required section | Regenerate with explicit section checklist in prompt. |
| Artifact has fabricated content | Flag in exchange.md. Regenerate with anti-fabrication rules repeated in prompt. |
| Multiple artifacts fail quality gates | Halt. Check master.md and adapted/ files for source quality. The input may be corrupt. |

### General Checkpoint Protocol

**Before each stage, save state:**
```bash
git add -A && git gcommit-hermes "CHECKPOINT: before Stage N (resume point)"
```

**After each stage completes and validates, save state:**
```bash
git add -A && git gcommit-hermes "Stage N COMPLETE: [metrics, file counts, sizes]"
```

**To resume after interruption:**
1. `git log --oneline -5` — find last checkpoint or stage completion
2. Run Stage Detection (count, timestamp, size, partial) to find resume point
3. Execute the first incomplete stage
4. Do not re-run completed stages unless they fail timestamp or size checks

**State save/restore markers:**
```bash
# Save stage completion marker
echo "STAGE_3_COMPLETE=true" > ste-code/.stage-state
echo "STAGE_3_TIMESTAMP=$(date -Iseconds)" >> ste-code/.stage-state
echo "STAGE_3_SOURCE_DIR=$INPUT_DIR" >> ste-code/.stage-state

# Read stage completion marker on resume
source ste-code/.stage-state 2>/dev/null
```

---

## Progress Tracking

Update `.agents/state/PROGRESS.md` after every completed stage. Signal in `.agents/feedback/exchange.md` with agent perspective tag:

```markdown
## Agent #N → Reviewer — Stage X Complete
[status, metrics, next stage]
```

### Post-Stage Exchange Format

```markdown
## Agent #N → Reviewer — Stage 3 Complete (Merge)
- Source directory: ste-code/extracted (109 files)
- master.md size: 523,488 bytes
- Rule count: 53/53
- Category count: 19/19
- Spot-checks: 10/10 passed
- Next: Stage 4 (Adaptation), Batch 1 (a001-a003)
```

```markdown
## Agent #N → Reviewer — Stage 4 Complete (Adaptation)
- Workers: 11/11 complete
- Adapted file total: 9,400 lines across 11 files
- Rule count across files: 53/53
- Category mapping: 19/19 per category-mapping.md
- Aerospace examples remaining: 0
- Next: Stage 5 (Artifacts), starting with Artifact 1
```

```markdown
## Agent #N → Reviewer — Stage 5 Complete (Artifacts)
- Artifacts: 6/6 complete
- Total size: 49,600 chars (~12,400 tokens)
- Quality gates: all passed
- Pipeline complete. Awaiting review.
```

---

## Cross-References to Companion Skills

This file acts as the **dispatcher** for Stages 3-5. For deep detail on each stage, refer to the dedicated skill files:

| Stage | Companion Skill | Provides |
|-------|-----------------|----------|
| **3 — Merge** | `.agents/skills/spec-extraction/ste-code-merge/SKILL.md` | Full dedup patterns, section structure template (all 53 rules enumerated), validation commands, page boundary detection |
| **4 — Adaptation** | `.agents/skills/spec-extraction/ste-code-adaptation/SKILL.md` | Complete preserve/replace rules, category mapping reference, verification checklist, output artifact sizing |
| **5 — Artifacts** | `.agents/skills/spec-extraction/ste-code-artifacts/SKILL.md` | Per-artifact content requirements (all 6 artifacts), quality gate checklists (detailed per-artifact), anti-fabrication rules, post-generation verification script |
| **Worker Pattern** | `.agents/skills/spec-extraction/ste-code-workers/SKILL.md` | Batch-of-3 launch protocol, progress tracking format, per-batch quality checks |
| **Refinement Pattern** | `.agents/skills/spec-extraction/ste-code-refine/SKILL.md` | Second-pass worker swarm, 9 formatting rules, launch protocol with prompt template |
| **Implementation** | `.agents/references/STE-CODE-IMPLEMENTATION.md` | Full pipeline spec, worker grid, gate definitions, retry logic |

When a stage in this file references a protocol, the companion skill provides the complete, executable detail. Use this file to determine *which* stage to run and *how* to dispatch; use companion skills for *exactly what* to do inside each stage.

---

## Immutable Facts
- 19 technical noun categories (NOT 22)
- 53 writing rules + 4 GR rules (NOT 65)
- Model: deepseek-v4-pro (NOT deepseek-pro or v4-flash)
- 434 pages in ASD-STE100 Issue 9
