# STE-Code — Simplified Technical English for Code Documentation

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Standard](https://img.shields.io/badge/standard-51%20rules%20%2B%204%20GR-brightgreen)](https://github.com/NikolaRHristov/STE-Code)
[![Spec](https://img.shields.io/badge/source-ASD--STE100%20Issue%209-lightgrey)](https://asd-ste100.org)
[![Benchmark](https://img.shields.io/badge/benchmark-96.6%25%20pass-success)](https://github.com/NikolaRHristov/STE-Code)

---

STE-Code is a documentation standard adapted from [ASD-STE100 Issue 9](https://asd-ste100.org) for code documentation. It gives you 51 writing rules, 4 grammar recommendations, a controlled vocabulary, and system prompt templates at five levels. The standard removes ambiguity, jargon, and hedging from README files, API documentation, docstrings, commit messages, and error messages.

---

## Adaptation Levels

Choose the level that fits your token budget:

| Level | File | Tokens | Best For |
|:-----:|------|:------:|----------|
| **1** | [`level1/system-prompt.txt`](ste-code/artifacts/level1/system-prompt.txt) | ~1.2K | Interactive sessions, tight token budgets |
| **2** | [`level2/system-prompt.txt`](ste-code/artifacts/level2/system-prompt.txt) | ~4.5K | Code review, PR feedback |
| **3** | [`level3/system-prompt.txt`](ste-code/artifacts/level3/system-prompt.txt) | ~8K | Full document rewriting |
| **4** | [`level4/system-prompt.txt`](ste-code/artifacts/level4/system-prompt.txt) | ~45K | Strict compliance checking |

Level 5 (the full specification) has 51 rule summaries at [`ste-code/artifacts/level5/`](ste-code/artifacts/level5/).

---

## How It Works

Copy a system prompt into your LLM. The model writes clear, unambiguous documentation.

```
You: Copy level1/system-prompt.txt into the system prompt field.
LLM: You are an STE-Code technical writer. Apply these rules...
You: Check this docstring.
     /** This function basically handles user stuff. */
LLM: /** Creates a user or updates the data of a user. */
```

The LLM applies the controlled vocabulary, the synonym table, and the sentence-length limits. It replaces jargon with approved words. It uses active voice and imperative mood.

---

## The Rules

The 51 rules cover nine sections:

| Section | Rules | Covers |
|---------|:-----:|--------|
| 1 — Words | 14 | Approved vocabulary, parts of speech, technical nouns and verbs |
| 2 — Noun Phrases | 2 | Article use, noun clusters |
| 3 — Verbs | 7 | Tense, voice, mood, verb forms |
| 4 — Sentences | 5 | Length, clarity, contractions, completeness |
| 5 — Procedures | 5 | Instructional writing, step structure |
| 6 — Descriptions | 5 | Descriptive writing, comparisons |
| 7 — Warnings | 3 | BREAKING, DEPRECATED, NOTE formatting |
| 8 — Punctuation | 6 | Commas, hyphens, parentheses, lists |
| 9 — Document Structure | 4 | Headings, lists, tables, organization |

Each rule has a code-domain adaptation with paradigm-specific guidance for object-oriented, functional, procedural, declarative, and systems programming. The full rules are in [`ste-code/adapted/`](ste-code/adapted/).

---

## Benchmark

STE-Code against a plain assistant on 59 documentation tests across 14 categories:

| | STE-Code | Plain Assistant | Improvement |
|---|:--------:|:---------------:|:-----------:|
| Pass rate | 96.6% | 11.9% | **+84.7%** |
| Average score | 0.919 | 0.471 | **+0.448** |

Top categories: comments, error messages, and config files.

---

## Repository

```
STE-Code/
├── README.md
├── ste-code/
│   ├── artifacts/
│   │   ├── level1/system-prompt.txt     ★ ~1.2K tokens
│   │   ├── level2/system-prompt.txt     ★ ~4.5K tokens
│   │   ├── level3/system-prompt.txt     ★ ~8K tokens
│   │   ├── level4/system-prompt.txt     ★ ~45K tokens
│   │   └── level5/                      ★ 51 rule summaries
│   ├── adapted/               The standard (57 adapted files)
│   ├── data/                  Structured JSON (vocabulary, synonyms)
│   ├── templates/             Additional system prompts
│   ├── merged/                master.md (full spec consolidation)
│   ├── refined/               Stage 2 — formatted extraction
│   └── extracted/             Stage 1 — raw extraction
├── spec/                      ASD-STE100 Issue 9 source (434 pages)
├── translations/              Translation scaffolding (9 locales)
└── .agents/                   Pipeline orchestration (agents, skills, config)
    ├── config/agents.yaml     Agent backend configuration
    └── tools/                 Assembly scripts (agent-agnostic)
```

---

## Agent-Agnostic Tools

All assembly scripts use the agent runner at `.agents/tools/agent-runner.py`. The default backend is Hermes. Add other agents in `.agents/config/agents.yaml`.

```bash
# Assemble prompts (default: Hermes)
python3 .agents/tools/assemble-level3.py
python3 .agents/tools/assemble-level2.py
python3 .agents/tools/assemble-level1.py

# Use a different agent
python3 .agents/tools/assemble-level1.py --agent claude

# List available agents
python3 .agents/tools/agent-runner.py --list
```

For full documentation, see [`.agents/AGENTS.md`](.agents/AGENTS.md).

---

## Pipeline

The standard was built from ASD-STE100 Issue 9 through a five-stage automated pipeline:

```
Extract → Refine → Merge → Adapt → Artifacts
(434pp)   (109f)    (1f)    (57f)    (5 levels)
```

Nine specialized agents orchestrated 109 parallel workers. The adaptation replaced aerospace terms with code-domain equivalents.

---

## Credits

STE-Code is an independent adaptation of **[ASD-STE100 Issue 9](https://asd-ste100.org)** (January 2025), published by the AeroSpace and Defence Industries Association of Europe (ASD), Brussels, Belgium.

> (c) ASD, 2025 — All rights reserved.

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
