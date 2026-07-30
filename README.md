# STE-Code — Simplified Technical English for Code Documentation

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Pipeline](https://img.shields.io/badge/pipeline-5%20stages-brightgreen)](https://github.com/NikolaRHristov/STE-Code)
[![Version](https://img.shields.io/badge/version-1.0-blue)](https://github.com/NikolaRHristov/STE-Code)
[![Spec](https://img.shields.io/badge/source-ASD--STE100%20Issue%209-lightgrey)](https://asd-ste100.org)
[![Benchmark](https://img.shields.io/badge/benchmark-96.6%25%20pass-success)](https://github.com/NikolaRHristov/STE-Code)

---

## What is STE-Code?

STE-Code is a **documentation standard** adapted from the [ASD-STE100](https://asd-ste100.org) aerospace specification into the code domain. It provides **53 writing rules**, **19 technical noun categories**, **4 technical verb categories**, and a **controlled vocabulary** that eliminates ambiguity, jargon, and hedging from every type of code documentation.

The project ships as a set of **LLM system prompt templates** — drop them into any model with ≥4K context and it produces clear, unambiguous, machine-readable documentation for READMEs, API docs, docstrings, comments, commit messages, and error messages.

---

## Quick Example

**Before (non-compliant):**

```javascript
/**
 * This function basically handles all the user stuff like creating and updating.
 * You need to make sure you pass a valid token in the header otherwise it'll fail.
 * It does some validation but not everything so be careful with what you send.
 */
app.post('/api/users', async (req, res) => { ... });
```

**After (STE-Code compliant):**

```javascript
/**
 * Creates a new user or updates an existing user.
 * Include a valid bearer token in the Authorization header.
 * The endpoint validates the email and password fields.
 * Other fields are accepted but not validated.
 */
app.post('/api/users', async (req, res) => { ... });
```

| Metric | Before | After |
|--------|--------|-------|
| Word count | 54 | 38 |
| Ambiguous terms ("basically", "stuff", "everything") | 3 | 0 |
| Conditional hedging ("if...otherwise") | 2 | 0 |
| Unapproved vocabulary ("make sure", "be careful") | 2 | 0 |

---

## What You Get — The Artifacts

Six deployable templates in [`ste-code/artifacts/`](ste-code/artifacts/):

| File | Tokens | Use Case |
|------|:------:|----------|
| [`ste-code-distilled-system-prompt.txt`](ste-code/artifacts/ste-code-distilled-system-prompt.txt) | ~1,200 | **Primary template.** Drop into any LLM's system prompt field. Covers all 14 core principles + synonym table. Fits 4K+ context models. |
| [`ste-code-self-reading-manual.txt`](ste-code/artifacts/ste-code-self-reading-manual.txt) | ~7,000 | Full manual with all 53 rules, dictionary excerpt, and examples. For models with 16K+ context. |
| [`ste-code-extraction-methodology.txt`](ste-code/artifacts/ste-code-extraction-methodology.txt) | ~1,400 | How the standard was extracted from ASD-STE100. For transparency and reproducibility. |
| [`ste-code-example-turn.txt`](ste-code/artifacts/ste-code-example-turn.txt) | ~500 | Single example turn showing the before/after transformation. For onboarding and evaluation. |
| [`ste-code-deployment-guide.txt`](ste-code/artifacts/ste-code-deployment-guide.txt) | — | Deployment instructions for integrating STE-Code into documentation pipelines. |
| [`README.md`](ste-code/artifacts/README.md) | — | Artifact index and usage notes. |

### Usage

Copy the system prompt into any LLM:

```
System: [contents of ste-code-distilled-system-prompt.txt]
User:   Check this docstring for STE-Code compliance:
        [your documentation here]
```

Works with any model that supports system prompts: ChatGPT, Claude, Gemini, DeepSeek, Llama, Mistral, and local models via LM Studio, Ollama, or llama.cpp.

---

## How It's Made — 5-Stage Pipeline

The standard was extracted from ASD-STE100 Issue 9 (434 pages) through a 5-stage automated pipeline:

```
ASD-STE100 Issue 9 (434 pages)
        │
        ▼
┌───────────────────────────────────────┐
│ Stage 1: EXTRACTION                   │
│   109 parallel workers → 109 raw files│
│   Enrichment: metadata + structure    │
└────────────────┬──────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────┐
│ Stage 2: REFINEMENT                   │
│   Section-aware formatting            │
│   2,689 dictionary entries tagged     │
│   100.0/100 quality audit score       │
└────────────────┬──────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────┐
│ Stage 3: MERGE                        │
│   109 files → master.md (23,737 lines)│
│   Deduplication, cross-referencing    │
└────────────────┬──────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────┐
│ Stage 4: ADAPTATION                   │
│   Aerospace → Code domain             │
│   57 adapted files: 51 rules + 4 GR + │
│   dictionary + 19 categories          │
└────────────────┬──────────────────────┘
                 │
                 ▼
┌───────────────────────────────────────┐
│ Stage 5: ARTIFACTS                    │
│   6 deployable system prompt templates│
│   ~72,000 characters total            │
└───────────────────────────────────────┘
```

The pipeline is orchestrated by 9 specialized agents using 21 skills. See [`.agents/MASTER.md`](.agents/MASTER.md) for the full orchestration protocol.

---

## Benchmark Results

STE-Code system prompt vs plain assistant on 59 tests across 14 documentation categories:

| | STE-Code | Plain Assistant | Improvement |
|---|----------|-----------------|-------------|
| Pass rate | 96.6% (57/59) | 11.9% (7/59) | **+84.7%** |
| Avg correctness | 0.919 | 0.471 | **+0.448** |

Top 3 categories where STE-Code wins hardest: **comments** (+0.580), **error messages** (+0.560), **config files** (+0.520).

Run the benchmark:
```bash
python3 .agents/benchmark/orchestrator.py         # STE-Code
python3 .agents/benchmark/orchestrator-control.py  # Plain assistant (control)
```

---

## Repository Structure

```
Manual/
├── README.md                        ← You are here
├── LICENSE                          ← MIT License
├── ste-code/
│   ├── artifacts/                   ← ★ The 6 deployable templates
│   ├── adapted/                     ← 57 adapted rule files (51 rules + 4 GR + dictionary + categories)
│   ├── merged/                      ← master.md (23,737 lines)
│   ├── refined/                     ← Formatted extraction (109 files, 100.0 audit)
│   ├── extracted/                   ← Raw extraction (109 files)
│   ├── enriched/                    ← Enriched with metadata + structure
│   ├── data/                        ← Machine-readable vocabulary + synonyms (JSON)
│   └── templates/                   ← 4 STE-Code system prompt templates
├── spec/                            ← ASD-STE100 Issue 9 source pages
│   └── issue-09-2025/
├── .agents/                         ← Pipeline orchestration
│   ├── agent/                       ← 9 agent definitions
│   ├── skills/                      ← 21 capability skills
│   ├── benchmark/                   ← 59 tests, 14 categories, orchestrator
│   ├── prompts/                     ← Worker prompts (maturity fixes, expansion)
│   └── tools/                       ← Telemetry wrapper, batch launchers

```

---

## Credits & Attribution

STE-Code is an independent adaptation of **[ASD-STE100 Issue 9](https://asd-ste100.org)** (January 2025), published by the AeroSpace and Defence Industries Association of Europe (ASD), Brussels, Belgium.

> © ASD, 2025 — All rights reserved

STE-Code is **not endorsed, affiliated with, or sponsored by ASD**. It is an open-source re-interpretation of the STE methodology, adapted exclusively for code documentation and software development contexts.

**STE** is a European Union Trade Mark (No. 017966390).

For the authoritative standard, visit [www.asd-europe.org](https://www.asd-europe.org) and [asd-ste100.org](https://asd-ste100.org).

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for the full text.

---

## Citation

If you use STE-Code in academic work, please cite:

```bibtex
@misc{ste-code-2025,
  title        = {{STE-Code}: Simplified Technical English for Code Documentation},
  author       = {{Nikola Hristov}},
  year         = {2025},
  howpublished = {\\url{https://github.com/NikolaRHristov/STE-Code}},
  note         = {Adapted from ASD-STE100 Issue 9 (January 2025), ASD Europe, Brussels}
}
```
