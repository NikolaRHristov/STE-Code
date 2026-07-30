---
name: ste-code-adaptation
description: "Take extracted spec worker output and produce STE-Code artifacts (system prompt, self-reading manual, methodology)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [ste-code, adaptation, spec, system-prompt, documentation]
    related_skills: [ste-code-worker-orchestration]
---

# STE-Code Adaptation Phase

## Overview

> **RAILS**: Validate every action against `references/rails.md` — 8 immutable guardrails.

After 9 workers extract the full ASD-STE100 spec, the coordinator reads all worker output and produces STE-Code: the coding-domain adaptation preserving the exact architecture.


> **RAILS**: Before any action, validate against .
> All 8 rails apply: stage isolation, naming, completion integrity, content fidelity,
> formatting standards, factual correctness, progress tracking, error recovery.

## Input

All 9 worker `.md` files in `ste-code/extracted/`:
- `w1-sec1-rules.md` through `w9-appendices.md`

## Output Artifacts

| File | Size | Description |
|------|------|-------------|
| `ste-code-self-reading-manual.txt` | ~30KB | Long form — S0–S8, all 53 rules, 19 categories, pipeline |
| `ste-code-distilled-system-prompt.txt` | ~5.5KB | Short form — ~1,200 tokens, 14 principles, synonym table |
| `ste-code-extraction-methodology.txt` | ~4KB | 6-pass pipeline, turn-by-turn protocol |
| `ste-code-example-turn.txt` | ~3KB | Worked example: non-STE comment → STE-Code |
| `ste-code-deployment-guide.txt` | ~4KB | Ollama, LM Studio, OpenAI, Claude, LangChain |
| `README.md` | ~2.5KB | Overview, quick start |

## Adaptation Rules

### WHAT TO PRESERVE (unchanged structure)
- All 53 rules — same numbers, same 9-section organization
- 6-pass transformation pipeline
- Dictionary architecture (APPROVED/UNAPPROVED)
- 19 Technical Code Noun categories (adapted from STE's 19 — verified from Issue 9 spec pages 47-52)
- 4 Technical Code Verb categories
- Safety instruction format (WARNING/CAUTION → BREAKING/DEPRECATED)

### WHAT TO REPLACE (adapted for code domain)
- All STE/non-STE example pairs → code documentation examples
- Technical noun categories → code-domain categories (see references/category-mapping.md)
- Vocabulary → code-domain approved words
- Safety WARNING/CAUTION → BREAKING/DEPRECATED

## Category Mapping

See `references/category-mapping.md` for the full 19-category adaptation from STE's 19 categories.

## Verification

After producing each artifact:
- Verify all 53 rule numbers are present
- Verify word counts: short form ~1,200 tokens, long form ~7,000 tokens
- Verify all examples are code-domain (no aerospace examples remaining)
- Verify BREAKING/DEPRECATED/NOTE format matches WARNING/CAUTION/NOTE structure
