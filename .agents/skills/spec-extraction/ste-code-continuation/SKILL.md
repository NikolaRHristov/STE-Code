---
name: ste-code-continuation
description: "Multi-agent continuation skill for Stages 3-5 (merge, adapt, artifacts) — usable by Agents #1, #2, or #3 from their own perspective to track and advance pipeline stages."
version: 1.0.0
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

```bash
# Check which files exist and determine active stage
ls ste-code/enriched/w*-p*.md 2>/dev/null | wc -l  # enriched count
ls ste-code/refined/r*.md 2>/dev/null | wc -l        # refined count
ls ste-code/extracted/w*-p*.md 2>/dev/null | wc -l   # extracted count
ls ste-code/merged/master.md 2>/dev/null              # merge exists?
ls ste-code/adapted/*.md 2>/dev/null | wc -l         # adaptation count
ls ste-code/artifacts/*.txt 2>/dev/null | wc -l      # artifact count
```

**Decision tree:**
- If merged/master.md missing or stale → do Stage 3 (Merge)
- If adapted/ has <10 files → do Stage 4 (Adapt)
- If artifacts/ has <6 files or files < target size → do Stage 5 (Artifacts)
- If all complete → verify and report

---

## Stage 3 — Merge

### Input Selection (agent-perspective)
Pick the best available source directory:

```bash
# Agent #1 perspective: prefer enriched, fall back to extracted
INPUT_DIR="ste-code/enriched"
[ $(ls ste-code/enriched/w*-p*.md 2>/dev/null | wc -l) -lt 109 ] && INPUT_DIR="ste-code/extracted"
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

### Adaptation Prompt Template
```
Read ste-code/merged/master.md. Focus on <<SECTION>>. 
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

### Generation Protocol
1. Read relevant sections from master.md + adapted files
2. Apply preserve/replace rules
3. Write artifact file
4. Run quality gate checklist
5. Fix failures before next artifact

### Anti-Fabrication Rules
- Every adapted rule MUST reference a specific rule_number from master.md
- Every synonym MUST trace to master.md's synonym table
- Every category MUST match one of the 19 from master.md
- Every example MUST be an adaptation of a real STE/non-STE pair
- No invented code terms without a master.md source

---

## Progress Tracking

Update `.agents/state/PROGRESS.md` after every completed stage. Signal in `.agents/feedback/exchange.md` with agent perspective tag:

```markdown
## Agent #N → Reviewer — Stage X Complete
[status, metrics, next stage]
```

## Immutable Facts
- 19 technical noun categories (NOT 22)
- 53 writing rules + 4 GR rules (NOT 65)
- Model: deepseek-v4-pro (NOT deepseek-pro or v4-flash)
- 434 pages in ASD-STE100 Issue 9
