# STE-Code — Simplified Technical English for Code Documentation

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.1.0-blue)](https://github.com/NikolaRHristov/STE-Code/releases)
[![Standard](https://img.shields.io/badge/standard-54%20rules-brightgreen)](ste-code/final/rules/)
[![Source](https://img.shields.io/badge/source-ASD--STE100%20Issue%209-lightgrey)](https://asd-ste100.org)

[ASD-STE100](https://asd-ste100.org) is *Simplified Technical English*. It is a
controlled language from the aerospace industry. It gives writers a set of
writing rules and an approved dictionary. Aircraft maintenance manuals use it so
that no sentence has two meanings.

**STE-Code applies that idea to code documentation.** It gives you 54 writing
rules in 9 sections, 4 General Rules, a code-domain dictionary, and a synonym
table. Use it for comments, docstrings, error messages, commit messages, API
documentation, changelogs, and configuration files. The standard removes
ambiguity, jargon, and hedging.

You do not have to read the standard yourself. You load the level artifacts
into a large language model, and the model writes your project's technical
documentation to the standard for you.

---

## What you get

Each level is one plain-text file. Copy the file into the system-prompt field of
your model. A higher level is stricter and costs more context.

| Level | File to load | Size | Tokens | What it adds |
|:-----:|--------------|-----:|-------:|--------------|
| **-2** | [`ste-code/artifacts/level-2/system-prompt.txt`](ste-code/artifacts/level-2/system-prompt.txt) | 5 KB | ~1.2K | The 14 core principles |
| **-1** | [`ste-code/artifacts/level-1/system-prompt.txt`](ste-code/artifacts/level-1/system-prompt.txt) | 26 KB | ~5.9K | + the synonym table |
| **0** | [`ste-code/artifacts/level0/system-prompt.txt`](ste-code/artifacts/level0/system-prompt.txt) | 17 KB | ~4.3K | + a short dictionary excerpt |
| **1** | [`ste-code/artifacts/level1/system-prompt.txt`](ste-code/artifacts/level1/system-prompt.txt) | 58 KB | ~14.5K | + document templates |
| **2** | [`ste-code/artifacts/level2/system-prompt.txt`](ste-code/artifacts/level2/system-prompt.txt) | 75 KB | ~18.5K | + section grammar rules |
| **3** | [`ste-code/artifacts/level3/system-prompt.txt`](ste-code/artifacts/level3/system-prompt.txt) | 388 KB | ~94.7K | + the full dictionary and all 54 rules |
| **4** | [`ste-code/artifacts/level4/system-prompt.txt`](ste-code/artifacts/level4/system-prompt.txt) | 462 KB | ~116.0K | + extensions and the reference catalogue |
| **5** | [`ste-code/artifacts/level5/system-prompt.txt`](ste-code/artifacts/level5/system-prompt.txt) | 539 KB | ~133.8K | + provenance (the complete standard) |

Start at **level 1**. It fits an ordinary context window and it includes the
templates. Move to level 3 or higher only when you need full rule coverage.

Each level is a **directory of small sub-documents**, so an agent reads and
writes files of a few tens of KB and never one large file. `system-prompt.txt`
is those sub-documents joined together, and `_index.md` lists them.

Two more files sit at the top of `ste-code/artifacts/`:

| File | Purpose |
|------|---------|
| [`llms.txt`](ste-code/artifacts/llms.txt) | An [llms.txt](https://llmstxt.org)-style index of every level |
| [`llms-full.txt`](ste-code/artifacts/llms-full.txt) | Every distilled sub-document in one file |

Size is the size of `system-prompt.txt` on disk. Token counts use the
`o200k_base` tokenizer (GPT-4o, GPT-4.1, GPT-5, o-series). `cl100k_base`
(GPT-4, GPT-3.5-turbo) agrees to within 0.3%, and the Claude and Llama
tokenizers stay within a few percent for English prose. Regenerate the numbers
with:

```bash
python3 .agents/tools/maintenance/measure_artifacts.py
python3 .agents/tools/release/facts.py
```

---

## Use it

Load a level into any model that accepts a system prompt.

```bash
# Ollama, llama.cpp, or any CLI that takes a system-prompt file
ollama run llama3 --system "$(cat ste-code/artifacts/level1/system-prompt.txt)"
```

```python
# OpenAI-compatible API
from pathlib import Path
from openai import OpenAI

system = Path("ste-code/artifacts/level1/system-prompt.txt").read_text()
client = OpenAI()

reply = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": "Rewrite: /** Basically handles user stuff. */"},
    ],
)
print(reply.choices[0].message.content)
```

The model then applies the approved vocabulary, the synonym table, and the
sentence-length limits. It replaces jargon with approved words, it uses the
active voice and the imperative mood, and it keeps each sentence to one
instruction.

```
You:  Rewrite this docstring.
      /** This function basically handles user stuff. */

LLM:  /** Creates a user, or updates the data of a user. */
```

---

## The rules

The 54 rules are in [`ste-code/final/rules/`](ste-code/final/rules/), one file
per rule.

| Section | Rules | Covers |
|:-------:|:-----:|--------|
| 1 | 14 | Words: approved vocabulary, parts of speech, technical nouns and verbs |
| 2 | 3 | Noun phrases: articles, noun clusters |
| 3 | 7 | Verbs: tense, voice, mood, verb forms |
| 4 | 5 | Sentences: length, clarity, completeness |
| 5 | 5 | Procedures: instructional writing, step structure |
| 6 | 6 | Descriptions: descriptive writing, comparisons |
| 7 | 3 | Warnings: BREAKING, DEPRECATED, and NOTE formatting |
| 8 | 7 | Punctuation: commas, hyphens, parentheses, lists |
| 9 | 4 | Document structure: headings, lists, tables, organization |

Each rule carries a code-domain adaptation with guidance for the
object-oriented, functional, procedural, declarative, and systems paradigms.

`ste-code/final/` also holds the dictionary (`rules/a-dictionary.md`), the 22
technical-noun categories (`rules/a-categories.md`), six gap-fill extensions
(`extensions/`), the reference catalogue, and the provenance record. The four
General Rules (GR1–GR4) live in `ste-code/adapted/a-sec9-gr1..4.md`.

---

## How the standard was built

The pipeline reads the ASD-STE100 Issue 9 specification and writes the level
artifacts. It runs in five stages.

```
Extraction → Refinement → Merge → Adaptation → Artifacts
 extracted/    refined/    grouped/   adapted/   artifacts/
                                      final/
```

| Stage | Reads | Writes | Type |
|-------|-------|--------|------|
| Extraction | `spec/issue-09-2025/page-dir/` | `ste-code/extracted/` (109 files) | LLM workers |
| Refinement | `ste-code/extracted/` | `ste-code/refined/` (109 files) | LLM workers |
| Merge | `ste-code/refined/` | `ste-code/grouped/` (24 groups) | Deterministic |
| Adaptation | `ste-code/grouped/` | `ste-code/adapted/`, then `ste-code/final/` | LLM workers |
| Artifacts | `ste-code/final/` | `ste-code/artifacts/` (8 tiers) | Deterministic + LLM |

The Merge and Artifacts assembly stages are pure Python on purpose. Where the
task is reorganization and not writing, the pipeline moves bytes instead of
re-typing them, so content cannot be lost.

Read [docs/pipeline.md](docs/pipeline.md) for the runners, the gates, and how to
run a stage.

### The artifact build

The deliverables are produced by a hybrid design, so content is never lost and
never silently truncated:

1. **Scaffold (deterministic).** `levels_scaffold.py` reads `ste-code/final/`
   and emits, for each of the 8 tiers, a directory of bounded sub-documents
   under `ste-code/artifacts/_base/level<N>/`. Oversized rule sections are
   split. This layer is byte-reproducible and needs no model.
2. **Distill (LLM).** `distill_one.py` runs one session per sub-document. The
   worker rewrites its base sub-document into an optimized file at
   `ste-code/artifacts/level<N>/<subdoc>`, and writes in several `write_file`
   and `patch` calls. On any failure the deterministic base stays in place, so
   nothing is lost.
3. **Assemble (deterministic).** `artifact_batch.py` writes each tier's
   `_index.md` and `system-prompt.txt`, then the top-level `llms.txt`,
   `llms-full.txt`, and `VERSION`. No model, and no truncation.

```
final/  ──levels_scaffold.py──▶  _base/level<N>/  ──distill_one.py (LLM)──▶  level<N>/<subdoc>
   │                                                                                 │
   └────────────────────────artifact_batch.py───────────────▶ llms.txt + llms-full.txt
```

---

## Repository

| Path | Contents |
|------|----------|
| `ste-code/artifacts/` | The deliverable: 8 level directories, `llms.txt`, `llms-full.txt`, `VERSION` |
| `ste-code/final/` | The standard: 54 rules, dictionary, categories, extensions, catalogue, provenance |
| `ste-code/extensions/` | Gap-fill entries for the code domain: verbs, adjectives, nouns, anti-patterns, domains |
| `ste-code/` | All other pipeline layers, from `extracted/` to `enriched/` |
| `spec/` | ASD-STE100 Issue 9 source. The PDF has 434 pages; the split produces 426 page files |
| `docs/` | The MkDocs documentation site |
| `translations/` | Locale scaffolding for 10 locales |
| `.agents/` | Development only. The machinery that BUILDS `ste-code/`: pipeline runners, tools, skills, benchmark, and the write jail. It is not part of the deliverable and you never load it into a model |

---

## Verify a checkout

```bash
make check
```

The gate prints `RESULT: all policies passed`. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the other `make` targets.

Quality checks for any markdown layer:

```bash
python3 .agents/tools/quality/check-rails.py    # the 8 rails
python3 .agents/tools/quality/check-tables.py   # table integrity
bash .agents/tools/linkcheck/run_linkcheck.sh   # lychee link check
```

The link checker scans `ste-code/final/**/*.md` and
`ste-code/artifacts/**/*.md`. It ignores the intentional legacy `master.md#…`
backlinks and reports real breakage: stale internal paths and dead external
URLs. The configuration is `.agents/tools/linkcheck/lychee.toml`.

---

## Agent-agnostic tools

Every pipeline script uses the agent runner in `.agents/tools/lib/`. The default
backend is Hermes, and other backends are configured in
`.agents/config/agents.yaml`. Prompts are externalized to
`.agents/tools/prompts/*.md` and rendered by `templater.py` with double-brace
`{{token}}` syntax.

```bash
# List the configured agent backends
python3 .agents/tools/lib/agent-runner.py --list

# Assemble the consolidated artifacts (deterministic, from final/)
python3 .agents/tools/artifacts/artifact_batch.py
python3 .agents/tools/artifacts/verify-artifacts.py

# Build the deterministic boilerplate sub-documents
python3 .agents/tools/artifacts/levels_scaffold.py

# Distill one sub-document with a model (one worker, own process)
python3 .agents/tools/artifacts/distill_one.py level3 01-principles.md 3 "..."

# Run the whole downstream chain
bash .agents/tools/runners/launch-downstream.sh
```

The model is read from the `STE_MODEL` environment variable. The default is
`tencent/hy3:free`. Full documentation: the
[documentation site](docs/index.md) and [`.agents/AGENTS.md`](.agents/AGENTS.md).

---

## Benchmark

The benchmark suite is in [`.agents/benchmark/`](.agents/benchmark/). It holds
59 tests in 14 categories, and it scores a model with a level artifact against
the same model without one.

```bash
python3 .agents/benchmark/benchmark-levels.py --levels -2,-1,0,1,2,3,4,5
python3 .agents/benchmark/orchestrator-control.py   # plain-assistant baseline
```

Run output is not committed to this repository, so this README publishes no
score. Run the suite to get numbers for your own model.

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

## Credits and references

STE-Code stands on decades of controlled-language research, documentation
theory, and verification tooling.

### Primary standard

- **ASD-STE100 Simplified Technical English, Issue 9 (January 2025)** — the
  standard that STE-Code adapts to the code domain. It is owned by **ASD**
  (Aerospace, Security and Defence Industries Association of Europe) and
  maintained by the **Simplified Technical English Maintenance Group (STEMG)**.
  <https://www.asd-ste100.org/>

### Controlled natural language theory

- **Tobias Kuhn** — *A Survey and Classification of Controlled Natural
  Languages* (Computational Linguistics, 2014). The source of the PENS
  classification. <https://aclanthology.org/J14-1005.pdf>
- **Norbert E. Fuchs and Rolf Schwitter** (University of Zurich) — *Attempto
  Controlled English (ACE)* (1996). <https://attempto.ifi.uzh.ch/>

### Documentation and readability

- **John M. Carroll** — *Minimalism* (ACM SIGDOC). The basis for register
  stratification: users act first, and they read at the moment of need.

### Adjacent standards

- **Google Style Guides** — <https://google.github.io/styleguide/>
- **github/codeql-coding-standards** — machine-enforceable standards as
  executable queries. <https://github.com/github/codeql-coding-standards>

## Intellectual property

ASD-STE100 is a copyright and a trademark of ASD, Brussels. STE-Code adapts the
*principles and rule categories* of the standard to the software domain. It does
not reproduce the dictionary or the rule text of the standard. Get Issue 9
directly from ASD with the free official form:
<https://www.asd-ste100.org/>.
