---
name: ste-code-artifacts
description: "Generate the 6 STE-Code artifact files from the master extraction state, following the adaptation protocol."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [ste-code, artifacts, generation, system-prompt, manual]
---

# STE-Code Artifact Generation

## Overview

After merge and validation, produce the 6 STE-Code artifact files by adapting
the extracted spec data from `ste-code/merged/master.md`.

## Prerequisites

- [ ] GATE 2 complete: `ste-code/merged/master.md` exists and validated
- [ ] All 53 rules present in master.md
- [ ] All 19 categories enumerated
- [ ] Dictionary entries available
- [ ] Synonym and polysemy tables extracted

## Artifact 1: ste-code-distilled-system-prompt.txt

**Target**: ~1,200 tokens (~4,800 chars)
**Purpose**: System prompt constraining any LLM to STE-Code output

Must contain:
1. **IDENTITY block** (2-3 sentences) — "You are a STE-Code compliant technical writer..."
2. **14 CORE PRINCIPLES** (P1-P14) with exact STE rule source references
3. **CANONICAL SYNONYM TABLE** — adapted from master.md's synonym table
4. **APPROVED VOCABULARY POLICY** — adapted from master.md's dictionary architecture
5. **DOCUMENT INTERACTION PROTOCOL** — 10-step protocol for code documents
6. **OUTPUT FORMAT** — standardized sections
7. **ANTI-PATTERNS** — 10 rules for code domain

**Quality gates:**
- [ ] All 14 principles reference specific STE rules from master.md
- [ ] Synonym table uses actual canonical forms (not invented ones)
- [ ] Anti-patterns are code-specific (not copy-pasted from aerospace)
- [ ] ~4,800 chars total

## Artifact 2: ste-code-self-reading-manual.txt

**Target**: ~7,000 tokens (~28,000 chars)
**Purpose**: 8-section self-reading manual following SSRM v1.0 structure

Must contain:
- **S0**: How to use this manual (recursive loop: read S3→read document→read S4→extract→...)
- **S1**: Core STE-Code principles (14 principles with code-domain examples)
- **S2**: Knowledge base — all 53 rules adapted, 19 categories, polysemy, synonym, pipeline
- **S3**: Page-reading protocol (document state tracking, page classification for code docs)
- **S4**: Skill extraction framework (5 patterns for code documentation)
- **S5**: UML extraction (code UML: class diagrams, sequence diagrams, flowcharts)
- **S6**: Recursive questioning protocol (13 questions adapted for code documents)
- **S7**: Output format (per-turn + final consolidated)
- **S8**: Context window management (keep manual + state, discard raw pages)

**Quality gates:**
- [ ] All 8 sections present and numbered
- [ ] All 53 adapted rules have code-domain example pairs
- [ ] 19 categories listed with code examples
- [ ] Recursive loop diagram present in S0
- [ ] S6 contains exactly 13 questions

## Artifact 3: ste-code-extraction-methodology.txt

**Target**: ~1,400 tokens (~5,600 chars)
**Purpose**: Turn-by-turn protocol for processing code documents

Must contain:
- Turn 0: Initialization (read title, TOC, identify document type)
- Turns 1+: READ→TOKENIZE→LEXICAL CHECK→EXTRACT STRUCTURAL DATA→OPTIMIZE→OUTPUT→ADVANCE
- 5 structural extraction types adapted for code (classes, associations, procedures, conditions, safety)
- Final turn: Consolidation
- UML output format (Mermaid class + flowchart)
- State persistence between turns

## Artifact 4: ste-code-example-turn.txt

**Target**: ~500 tokens (~2,000 chars)
**Purpose**: Single worked example showing non-STE-Code input → STE-Code output

Must contain:
- Non-STE-Code INPUT (a real code comment, commit message, or README section)
- ## COMPLIANCE STATUS: N violations found
- ## STE-CODE OUTPUT: corrected text
- ## UML EXTRACTION: Mermaid diagrams
- ## OPTIMIZATIONS: table with before/after metrics

Example input format:
```
Non-STE-Code: "The function should be called with the user object and
the return value needs to be checked for null before proceeding."
```

## Artifact 5: ste-code-deployment-guide.txt

**Target**: ~1,800 tokens (~7,200 chars)
**Purpose**: Deployment instructions for Ollama, LM Studio, Python+llama.cpp

Must cover:
- Option A: Ollama Modelfile with baked-in system prompt
- Option B: LM Studio GUI steps
- Option C: Python + llama.cpp programmatic loop
- Option D: Full conversation export as additional context
- Token budget breakdown
- Expected output after processing

## Artifact 6: README.md

**Target**: ~500 tokens (~2,000 chars)
**Purpose**: Project overview and quick start

Must contain:
- What STE-Code is (2-3 sentences)
- File listing with sizes
- Quick start (3 steps)
- Architecture summary (preserve/replace)
- Design principles
- References to ASD-STE100 Issue 9

## Generation Protocol

Generate artifacts in order (1→6). For each artifact:

1. Read the relevant sections from master.md
2. Adapt using the preserve/replace rules
3. Write the artifact file
4. Run the quality gate checklist
5. If any gate fails, fix before moving to next artifact

## Anti-Fabrication Rules

- Every adapted rule MUST reference a specific rule_number from master.md
- Every synonym MUST trace to an entry in master.md's synonym table
- Every category MUST match one of the 19 from master.md
- Every example MUST be an adaptation of a real STE/non-STE pair from master.md
- No invented code terms without a master.md source

## Verification After All Artifacts

```bash
for f in ste-code/ste-code-*.txt; do
  chars=$(wc -c < "$f")
  echo "$(basename $f): $chars chars ~$((chars/4)) tokens"
done
```

Expected totals:
- System prompt: ~4,800 chars (~1,200 tokens)
- Manual: ~28,000 chars (~7,000 tokens)
- Methodology: ~5,600 chars (~1,400 tokens)
- Example: ~2,000 chars (~500 tokens)
- Deployment: ~7,200 chars (~1,800 tokens)
- README: ~2,000 chars (~500 tokens)
- **Total: ~49,600 chars (~12,400 tokens)**
