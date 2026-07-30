# STE-Code Documentation

Simplified Technical English for Code — extract, adapt, and enforce ASD-STE100
rules for software documentation. 9-agent pipeline, 59-test benchmark suite
(96.6% pass rate), multi-language translation scaffolding.

STE-Code adapts the aerospace standard ASD-STE100 (Issue 9, January 2025) into
a rule system for code documentation: docstrings, comments, README files, commit
messages, API documentation, error messages, and system prompts.

## Index

### Getting Started
- [Installing STE-Code](install/README.md) — setup, prerequisites, first run
- [Quick Start](install/quickstart.md) — 5-minute guide to using STE-Code
- [Concepts](concepts/README.md) — 14 core principles, synonym table, anti-patterns, paradigm adaptation

### Pipeline
- [Pipeline Overview](pipeline/README.md) — 5-stage extraction → refinement → merge → adaptation → artifacts
- [Workers](pipeline/workers.md) — Batch-of-3 polling, self-healing, telemetry, oneshot wrapper
- [Orchestration](pipeline/orchestration.md) — Single-session protocol, launch loop, progress tracking
- [Telemetry](pipeline/telemetry.md) — Worker metrics, timing, output validation, self-healing scans

### Agents
- [Agent Catalog](agents/README.md) — All 9 agents, roles, launch commands
- [Agent #1 — Extractor](agents/agent-1-extractor.md) — 109 parallel workers, 434 pages, 37 batches
- [Agent #2 — Refiner](agents/agent-2-refiner.md) — 9 refinement rules, zero content loss
- [Agent #3 — Auditor](agents/agent-3-auditor.md) — 8-rail verification, fabrication detection, escalation
- [Agent #4 — Continuator](agents/agent-4-continuator.md) — 5-pass expansion, merge→adapt→artifacts
- [Agent #5 — SCE Populator](agents/agent-5-sce-populator.md) — Rules, vocabulary, synonyms, system prompts
- [Agent #6 — STE-Code Analysis](agents/agent-6-analysis.md) — Paradigm-agnostic documentation agent
- [Agent #7 — Level Worker](agents/agent-7-level-worker.md) — Parameterized, 5 adaptation levels
- [Agent #8 — Extension Worker](agents/agent-8-extension-worker.md) — Code-domain gap fillers
- [Agent #9 — Translation Orchestrator](agents/agent-9-translations.md) — 9 locales, discovery-based

### Reference
- [Rule Reference](reference/rules.md) — All 53 writing rules + 4 GR rules adapted for code
- [Dictionary](reference/dictionary.md) — 875+ approved words with code-domain meanings
- [Synonym Table](reference/synonyms.md) — Canonical approved → avoid pairs
- [Category Mapping](reference/categories.md) — 19 code-domain noun categories
- [Anti-Patterns](reference/anti-patterns.md) — 30 code documentation anti-patterns
- [Schemas](reference/schemas.md) — JSON schemas for rules, vocabulary, worker contracts
- [Rails](reference/rails.md) — 8 behavioral guardrails for pipeline agents

### Benchmark
- [Benchmark Suite](benchmark/README.md) — 59 tests, 14 categories, 96.6% pass rate
- [Running Benchmarks](benchmark/running.md) — Orchestrator, control group, scoring
- [Results](benchmark/results.md) — Aggregate + per-category breakdown

### Translations
- [Translation Pipeline](translations/README.md) — 9 locales, discovery-based, blank placeholders
- [Adding a Locale](translations/adding-locale.md) — How to add a new target language
- [Translation Grid](translations/grid.md) — Per-locale worker assignments

### Examples
- [Before/After](examples/before-after.md) — STE/non-STE code documentation pairs
- [System Prompt Usage](examples/system-prompt.md) — Using STE-Code as a system prompt
- [Commit Message](examples/commit-message.md) — STE-Code compliant commit messages

### Contributing
- [Extending the Dictionary](contributing/dictionary.md) — Adding new approved terms
- [Adding Rules](contributing/rules.md) — Proposing and adapting new writing rules
- [Agent Development](contributing/agents.md) — Building new pipeline agents
- [Maturity Model](contributing/maturity.md) — 7-level file maturity scale (−2 to 5)

## Key Facts

| Fact | Value |
|------|-------|
| Source standard | ASD-STE100 Issue 9, January 2025 |
| Adapted rules | 53 writing rules + 4 grammar rules |
| Dictionary | 875+ approved, 1,400+ unapproved terms |
| Categories | 19 code-domain noun categories |
| Pipeline stages | 5 (Extract → Refine → Merge → Adapt → Artifacts) |
| Agents | 9 specialized orchestrators |
| Benchmark | 59 tests, 14 categories, 96.6% pass rate |
| Model | deepseek-v4-pro (reasoning: high) |
| Worker pattern | Batch of 3, notify_on_complete, self-healing |
| Locales | 9 target languages (zh-CN, ja, ko, es, fr, de, pt-BR, ru, ar) |
