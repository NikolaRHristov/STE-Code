# SCE — Simplified Code English v2 Architecture

This directory implements the **4-stratum architecture** for STE-Code, designed for LLM composability, developer extensibility, and agentic pipeline integration.

## Benchmark Results

| | STE-Code | Plain Assistant | Improvement |
|---|----------|-----------------|-------------|
| Pass rate | 96.6% (57/59) | 11.9% (7/59) | +84.7% |
| Avg correctness | 0.919 | 0.471 | +0.448 |
| Tests | 59 (14 categories) | 59 | — |

## Strata

| Stratum | Directory | Type | Purpose |
|---------|-----------|------|---------|
| 1 — Static Core | `core/` | Immutable MD + JSON | Rules, categories, canonical synonym table |
| 2 — Variable Data | `data/` | Living JSON | Vocabulary, domain extensions |
| 3 — Computable Logic | `compute/` | JSON schemas + prompts | Rails, gate conditions, worker contracts |
| 4 — Readable Narratives | `narratives/` | Generated MD | System prompts (micro/full/agentic/developer), examples |

## Loading Strategy for LLMs

- **Minimal (~500 tokens):** `narratives/system-prompts/ste-code-micro.md`
- **Standard (~4,000 tokens):** `narratives/system-prompts/ste-code-full.md` (14 principles + synonym table + anti-patterns)
- **Agentic (~2,500 tokens):** `narratives/system-prompts/ste-code-agentic.md` + `compute/agentic/rails.json`
- **Developer (full):** All strata in order: core → data → compute → narratives

## Relationship to `ste-code/` and `.agents/`

| Directory | Purpose |
|-----------|---------|
| `ste-code/` | Pipeline outputs (extracted, refined, merged, adapted, artifacts) |
| `.agents/` | Agent definitions, skills, benchmark suite, rewrites |
| `SCE/` | Structured, composable STE-Code for programmatic and LLM use |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-07 | Initial 4-stratum architecture |
| 2.0.0 | 2026-07-30 | Canonical synonym table, updated P1-P14, benchmark results, anti-patterns aligned |
