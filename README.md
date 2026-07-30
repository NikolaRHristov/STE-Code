# STE-Code — Simplified Technical English for Code Documentation

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Standard](https://img.shields.io/badge/standard-51%20rules%20%2B%204%20GR-brightgreen)](https://github.com/NikolaRHristov/STE-Code)
[![Spec](https://img.shields.io/badge/source-ASD--STE100%20Issue%209-lightgrey)](https://asd-ste100.org)
[![Benchmark](https://img.shields.io/badge/benchmark-96.6%25%20pass-success)](https://github.com/NikolaRHristov/STE-Code)

---

STE-Code is a documentation standard adapted from [ASD-STE100 Issue 9](https://asd-ste100.org) for code documentation. It gives you 51 writing rules, 4 grammar rules, a controlled vocabulary, and LLM system prompt templates. The standard removes ambiguity, jargon, and hedging from READMEs, API docs, docstrings, commit messages, and error messages.

Drop a system prompt template into any LLM. The model produces clear, unambiguous documentation that follows the standard.

---

## What You Get

Six deployable system prompt templates in [`ste-code/artifacts/`](ste-code/artifacts/):

| File | Tokens | Use |
|------|:------:|-----|
| [`ste-code-distilled-system-prompt.txt`](ste-code/artifacts/ste-code-distilled-system-prompt.txt) | ~1,000 | Drop into any LLM. All 14 core principles, synonym table, anti-patterns. |
| [`ste-code-self-reading-manual.txt`](ste-code/artifacts/ste-code-self-reading-manual.txt) | ~12,000 | Full manual. All 51 rules, dictionary excerpt, examples. |
| [`ste-code-extraction-methodology.txt`](ste-code/artifacts/ste-code-extraction-methodology.txt) | ~4,000 | How the standard was built. Pipeline, adaptation, quality assurance. |
| [`ste-code-example-turn.txt`](ste-code/artifacts/ste-code-example-turn.txt) | ~1,400 | Before/after transformation. Compliance table. |
| [`ste-code-deployment-guide.txt`](ste-code/artifacts/ste-code-deployment-guide.txt) | ~4,000 | Integration with ChatGPT, Claude, Gemini, local models. CI/CD. |
| [`README.md`](ste-code/artifacts/README.md) | ~400 | Artifact index. |

Four additional templates for specific use cases in [`ste-code/templates/`](ste-code/templates/):

| File | Tokens | Use |
|------|:------:|-----|
| `ste-code-micro.md` | ~900 | Minimum. Context windows under 4K tokens. |
| `ste-code-full.md` | ~4,500 | Full standard summary. |
| `ste-code-agentic.md` | ~2,500 | Agent behavioral rules. |
| `ste-code-developer.md` | ~2,300 | Extension guide for new domains. |

Structured data for tooling in [`ste-code/data/`](ste-code/data/):

| File | Format | Contents |
|------|--------|----------|
| `vocabulary/approved-verbs.json` | JSON | All approved verbs with meanings and examples. |
| `vocabulary/approved-adjectives.json` | JSON | All approved adjectives. |
| `vocabulary/unapproved-entries.json` | JSON | Unapproved words with approved alternatives. |
| `vocabulary/code-dictionary.json` | JSON | Code-domain technical terms. |
| `vocabulary/domain-extensions.json` | JSON | 17 code-domain category extensions. |
| `synonym-table.json` | JSON | Complete synonym mapping. |

---

## How It Works

```
You:    [Copy system prompt into LLM]
LLM:    You are STE-Code...
You:    Check this docstring for compliance:
        /** This function basically handles user stuff. */
LLM:    /** Creates a new user or updates an existing user. */
```

The LLM applies all 51 rules, the controlled vocabulary, and the synonym table. It replaces jargon with approved words. It uses active voice and imperative mood. It writes short, clear sentences.

---

## The Rules

The 51 rules cover nine sections:

| Section | Rules | Covers |
|---------|:-----:|--------|
| 1 — Words | 14 | Approved vocabulary, parts of speech, technical nouns/verbs |
| 2 — Noun Phrases | 2 | Article use, noun clusters |
| 3 — Verbs | 7 | Tense, voice, mood, verb forms |
| 4 — Sentences | 5 | Length, clarity, contractions, completeness |
| 5 — Procedures | 5 | Instructional writing, step structure |
| 6 — Descriptions | 5 | Descriptive writing, comparisons |
| 7 — Warnings | 3 | BREAKING, DEPRECATED, NOTE formatting |
| 8 — Punctuation | 6 | Commas, hyphens, parentheses, lists |
| 9 — Document Structure | 4 | Headings, lists, tables, organization |

Each rule has a code-domain adaptation section. The adaptation covers README files, API documentation, docstrings, commit messages, error messages, and CLI help text. Each rule includes paradigm-specific guidance for object-oriented, functional, procedural, declarative, and systems programming.

The full rules are in [`ste-code/adapted/`](ste-code/adapted/). Each file is 200 to 600 lines with original rule text, code-domain examples, edge cases, and grammar notes.

---

## Benchmark

STE-Code system prompt against a plain assistant on 59 documentation tests across 14 categories:

| | STE-Code | Plain Assistant | Improvement |
|---|:--------:|:---------------:|:-----------:|
| Pass rate | 96.6% | 11.9% | **+84.7%** |
| Average score | 0.919 | 0.471 | **+0.448** |

The top categories where STE-Code wins hardest: comments, error messages, and config files.

---

## Repository

```
STE-Code/
├── README.md
├── ste-code/
│   ├── artifacts/          ★ Deployable system prompts (6 files)
│   ├── adapted/            ★ The standard (51 rules, dictionary, categories)
│   ├── data/               ★ Structured JSON (vocabulary, synonyms)
│   ├── templates/          ★ Additional system prompts (4 files)
│   ├── merged/               master.md (full spec consolidation)
│   ├── refined/              Stage 2 — formatted extraction
│   └── extracted/            Stage 1 — raw extraction
├── spec/                     ASD-STE100 Issue 9 source (434 pages)
├── translations/             Translation scaffolding (9 locales)
└── .agents/                  Pipeline orchestration (agents, skills, benchmark)
```

---

## Pipeline

The standard was built from ASD-STE100 Issue 9 through a five-stage automated pipeline:

```
Extract → Refine → Merge → Adapt → Artifacts
(434pp)   (109f)    (1f)    (57f)    (6f)
```

Nine specialized agents orchestrated 109 parallel workers to extract all 434 pages. The adaptation replaced aerospace terms with code-domain equivalents. Phase B later deepened each rule from ~55 lines to ~400 lines with paradigm-specific guidance and extended examples.

---

## Credits

STE-Code is an independent adaptation of **[ASD-STE100 Issue 9](https://asd-ste100.org)** (January 2025), published by the AeroSpace and Defence Industries Association of Europe (ASD), Brussels, Belgium.

> © ASD, 2025 — All rights reserved.

STE-Code is not endorsed by or affiliated with ASD. **STE** is a European Union Trade Mark (No. 017966390).

---

## License

MIT. See [LICENSE](LICENSE).

## Citation

```bibtex
@misc{ste-code-2025,
  title        = {{STE-Code}: Simplified Technical English for Code Documentation},
  author       = {{Nikola Hristov}},
  year         = {2025},
  howpublished = {\url{https://github.com/NikolaRHristov/STE-Code}},
  note         = {Adapted from ASD-STE100 Issue 9 (January 2025)}
}
```
