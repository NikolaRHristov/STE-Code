# STE-Code — Simplified Technical English for Code Documentation

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Pipeline](https://img.shields.io/badge/pipeline-5%20stages-brightgreen)](https://github.com/NikolaRHristov/Manual)
[![Version](https://img.shields.io/badge/version-1.0-blue)](https://github.com/NikolaRHristov/Manual)
[![Model](https://img.shields.io/badge/model-deepseek--v4--pro-orange)](https://deepseek.com)
[![Spec](https://img.shields.io/badge/source-ASD--STE100%20Issue%209-lightgrey)](https://asd-ste100.org)

---

## What is STE-Code?

STE-Code adapts the [ASD-STE100](https://asd-ste100.org) Simplified Technical English standard — originally developed for aerospace maintenance documentation — into the code documentation domain. It provides 53 writing rules, 19 technical noun categories, 4 technical verb categories, and a controlled vocabulary that eliminates ambiguity, jargon, and hedging from READMEs, API docs, comments, commit messages, and error messages. Every output is clear, unambiguous, and machine-readable.

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
| Conditional hedging ("if", "otherwise") | 2 | 0 |
| Unapproved vocabulary ("make sure", "be careful") | 2 | 0 |

---

## Pipeline Architecture

```
ASD-STE100 Issue 9 (434 pages)
        │
        ▼
┌─────────────────────────────────────────┐
│ Stage 1: EXTRACTION  (Agent #1)         │
│   109 workers → 109 raw markdown files  │
│   Enrichment pass: metadata + structure │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Stage 2: REFINEMENT  (Agent #2)         │
│   42 section-aware v2 workers           │
│   2,689 dictionary entries tagged       │
│   100.0/100 quality audit score         │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Stage 3: MERGE                          │
│   109 files → master.md (23,737 lines)  │
│   Deduplication, cross-referencing      │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Stage 4: ADAPTATION                     │
│   Aerospace → Code domain               │
│   57 adapted files (51 rules + 4 GR +   │
│   dictionary + 19 categories)           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Stage 5: ARTIFACTS                      │
│   6 deployable files, ~72,000 chars     │
│   System prompt, manual, methodology,   │
│   example turn, deployment guide, README│
└─────────────────────────────────────────┘
```

---

## Quick Start

### Option A — Ollama (one-liner)

```bash
ollama create ste-code -f Modelfile && ollama run ste-code
```

### Option B — Python snippet

```python
from llama_cpp import Llama

llm = Llama(model_path='models/deepseek-coder-6.7b.Q4_K_M.gguf', n_ctx=8192)
with open('ste-code/artifacts/ste-code-distilled-system-prompt.txt') as f:
    system_prompt = f.read()

doc = open('README.md').read()
response = llm.create_chat_completion(
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': f'Check for STE-Code compliance:\n\n{doc}'}
    ],
    temperature=0.3, max_tokens=4096
)
print(response['choices'][0]['message']['content'])
```

### Option C — Direct file usage (any LLM)

Drop [`ste-code-distilled-system-prompt.txt`](ste-code/artifacts/ste-code-distilled-system-prompt.txt) into any LLM's system prompt field (LM Studio, Ollama, ChatGPT, Claude). The prompt is ~1,200 tokens and fits models with ≥4K context.

---

## Repository Structure

```
Manual/
├── README.md                  ← You are here
├── LICENSE                    ← MIT License
├── spec/                      ← ASD-STE100 Issue 9 source pages
│   └── issue-09-2025/
├── ste-code/
│   ├── README.md              ← Pipeline overview
│   ├── extracted/             ← Stage 1: raw extraction (109 files)
│   ├── enriched/              ← Stage 1b: enriched extraction (109 files)
│   ├── refined/               ← Stage 2: v2 formatted (109 files, 100.0 audit)
│   ├── merged/                ← Stage 3: master.md (23,737 lines)
│   ├── adapted/               ← Stage 4: 57 adapted files
│   │   └── expanded/           ← Agent #4 expansion outputs
│   ├── artifacts/             ← Stage 5: 6 deployable files
│   └── audit_refinement.py    ← Automated quality scoring
├── SCE/                       ← Structured STE-Code v2.0 (4 strata, 175 entries)
├── .agents/                   ← Agent-agnostic: 9 agents, 21 skills, 59-test benchmark
│   ├── agent/                 ← Agent definitions (#1-9)
│   ├── skills/                ← 21 capability skills
│   ├── benchmark/              ← 59 tests, 14 categories, orchestrator
│   └── tools/                 ← Distributed worker tools (oneshot wrapper + launcher)
```

---

## Benchmark Results

STE-Code system prompt vs plain assistant on 59 tests across 14 categories:

| | STE-Code | Plain Assistant | Improvement |
|---|----------|-----------------|-------------|
| Pass rate | 96.6% (57/59) | 11.9% (7/59) | **+84.7%** |
| Avg correctness | 0.919 | 0.471 | **+0.448** |

---

## Credits & Attribution

STE-Code is an independent adaptation of **[ASD-STE100 Issue 9](https://asd-ste100.org)** (January 2025), published by the AeroSpace and Defence Industries Association of Europe (ASD), Brussels, Belgium.

The original specification's text is:

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
  howpublished = {\url{https://github.com/NikolaRHristov/Manual}},
  note         = {Adapted from ASD-STE100 Issue 9 (January 2025), ASD Europe, Brussels}
}
```

---

## Links

- **GitHub repository** — [github.com/NikolaRHristov/Manual](https://github.com/NikolaRHristov/Manual)
- **ASD-STE100 source** — [asd-ste100.org](https://asd-ste100.org)
- **ASD Europe** — [www.asd-europe.org](https://www.asd-europe.org)
- **Model** — [deepseek-v4-pro](https://deepseek.com)
