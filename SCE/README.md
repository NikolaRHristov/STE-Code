# SCE — Simplified Code English v2 Architecture

This directory implements the **4-stratum architecture** for STE-Code, designed for LLM composability, developer extensibility, and agentic pipeline integration.

## Strata

| Stratum | Directory | Type | Purpose |
|---------|-----------|------|---------|
| 1 — Static Core | `core/` | Immutable MD + JSON | Rules, categories, constraints |
| 2 — Variable Data | `data/` | Living JSON/CSV | Vocabulary, synonyms, extensions |
| 3 — Computable Logic | `compute/` | JSON schemas + prompts | Checklists, rubrics, validators |
| 4 — Readable Narratives | `narratives/` | Generated MD | System prompts, guides, examples |

## Loading Strategy for LLMs

- **Minimal (1,600 tokens):** Load `narratives/system-prompts/ste-code-micro.md` only
- **Standard (~4,000 tokens):** Load `narratives/system-prompts/ste-code-full.md`
- **Agentic (~2,500 tokens):** Load `narratives/system-prompts/ste-code-agentic.md` + `compute/agentic/rails.json`
- **Developer (full):** Load all strata in order: core → data → compute → narratives

## Relationship to `ste-code/`

`ste-code/` contains the pipeline outputs (extracted, refined, merged, adapted, artifacts).
`SCE/` contains the structured, composable version of the same knowledge for programmatic and LLM use.
