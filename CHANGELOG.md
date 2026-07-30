# Changelog

All notable changes to STE-Code will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Pre-built Modelfiles for DeepSeek-Coder, Qwen-Coder, CodeLlama, and Codestral
- GitHub Action for CI-based documentation compliance checks
- VS Code Extension for real-time STE-Code linting
- Expanded synonym table with 50 additional code-domain synonyms
- Language-specific rule subsets for JavaScript, Python, Rust, Go, and Java

---

### [1.0.0] — 2026-07-30 — Initial Release

### Added
- 5-stage extraction pipeline — Extract, Refine, Merge, Adapt, Artifacts — processing 434 pages of ASD-STE100 Issue 9
- 109 parallel workers for page extraction from the full specification PDF
- 9 refinement rules producing clean, standardized markdown output
- 55 adaptation files covering all 53 writing rules plus 4 General Rules (GR1–GR4)
- 19 technical noun categories and 4 technical verb categories adapted for code documentation
- 6 deployable artifacts:
  - Distilled system prompt (~1,200 tokens, 14 STE-Code principles) for drop-in LLM deployment
  - Self-reading manual (S0–S9) with all 53 adapted rules, categories, and synonym tables
  - Extraction methodology documenting the 6-pass transformation pipeline
  - Example turn with 3 worked before/after transformations and Mermaid diagrams
  - Deployment guide covering 7 deployment options and a 14-model compatibility matrix
  - Project README with real-world examples, comparison metrics, roadmap, and contribution guidelines

### Infrastructure
- Hermes agent orchestration with a 3-agent pipeline (extraction, refinement, adaptation)
- Rails compliance system (R1–R8) enforcing output quality across all processing stages
- Execution auditor providing disk-verified claims for every pipeline stage
- Git-based state tracking via PROGRESS.md with per-worker completion markers

### Attribution
- Adapted from ASD-STE100 Issue 9 (January 2025)
- © ASD, 2025 — All rights reserved (original specification)
- Model: deepseek-v4-pro

---

[1.0.0]: https://github.com/NikolaRHristov/Manual/releases/tag/v1.0.0
