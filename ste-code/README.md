# STE-Code: Simplified Technical English for Code

**Issue 1, July 2026**

STE-Code is the coding-domain adaptation of ASD-STE100 (Simplified Technical
English, Issue 9). It provides a controlled natural language for software
documentation, API design, commit messages, code reviews, README files, and
inline comments.

## What's Included

| File | Description | Size |
|------|-------------|------|
| `ste-code-distilled-system-prompt.txt` | Short-form system prompt for constraining any LLM | ~1,200 tokens |
| `ste-code-self-reading-manual.txt` | Long-form self-reading manual with all 53 rules, categories, pipeline, and protocols | ~7,000 tokens |
| `ste-code-extraction-methodology.txt` | Turn-by-turn protocol for processing code documents | ~1,400 tokens |
| `ste-code-example-turn.txt` | Worked example of transforming non-STE code comment to STE-Code | ~500 tokens |
| `ste-code-deployment-guide.txt` | Deployment instructions for Ollama, LM Studio, OpenAI, Claude, LangChain | — |
| `workers/` | Raw extraction data from the ASD-STE100 spec (9 worker JSON files) | — |
| `PLAN.md` | Generation plan and execution log | — |

## Quick Start

1. Copy `ste-code-distilled-system-prompt.txt` into your LLM's system prompt field.
2. Set temperature to 0.1–0.3.
3. Ask the LLM to document code, write commit messages, or review code.
4. The LLM will produce STE-Code compliant output.

## Architecture

STE-Code preserves the exact architecture of ASD-STE100:
- **Part 1**: 53 writing rules in 9 sections (adapted for code)
- **Part 2**: Controlled vocabulary (approved/unapproved words with alternatives)
- **6-pass transformation pipeline** for converting non-compliant text
- **19 Technical Code Noun categories** (adapted from STE's 22 categories)
- **4 Technical Code Verb categories**
- **Safety instruction format** (BREAKING / DEPRECATED / NOTE)

## Design Principles

1. **STE-Code is a proper subset of English** — just as STE is a proper subset.
2. **One word, one meaning** — no polysemy without explicit resolution.
3. **Short, clear statements** — 20 words max (procedural), 25 words max (descriptive).
4. **Active voice** — passive only when the agent is unknown.
5. **Consistent terminology** — one name per concept throughout a document.

## License

Public domain. Free use, reproduction, and adaptation for all purposes.
No warranty; use at your own risk.

## References

- ASD-STE100 Issue 9, January 2025 — the original specification
- ISO 1087:2019 — Terminology work and terminology science
