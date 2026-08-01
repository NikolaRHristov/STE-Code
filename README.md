# STE-Code — Simplified Technical English for Code Documentation

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Standard](https://img.shields.io/badge/standard-54%20rules-brightgreen)](https://github.com/NikolaRHristov/STE-Code)
[![Source](https://img.shields.io/badge/source-ASD--STE100%20Issue%209-lightgrey)](https://asd-ste100.org)
[![Benchmark](https://img.shields.io/badge/benchmark-96.6%25%20pass-success)](https://github.com/NikolaRHristov/STE-Code)

STE-Code is a documentation standard adapted from
[ASD-STE100 Issue 9](https://asd-ste100.org) for **code documentation**. It gives
you 54 writing rules (across 9 sections), a controlled vocabulary, a synonym
table, and system-prompt material packaged at **eight** levels of strictness
(`-2` → `5`). The standard removes ambiguity, jargon, and hedging from READMEs,
API docs, docstrings, commit messages, and error messages.

---

## Adaptation levels

Each level is a **directory of small sub-documents** (so an LLM reads/writes
files of a few tens of KB at most, never one 1.8 MB monster). Pick the level
that fits your token budget:

| Level | Directory | Size on disk | Tokens | Best for |
|:-----:|-----------|:------------:|:------:|----------|
| **-2** | [`ste-code/artifacts/level-2/`](ste-code/artifacts/level-2/) | 5 KB | ~1.2K | Ultra-minimal: the 14 core principles only |
| **-1** | [`ste-code/artifacts/level-1/`](ste-code/artifacts/level-1/) | 26 KB | ~5.9K | Minimal: core principles + synonym table |
| **0** | [`ste-code/artifacts/level0/`](ste-code/artifacts/level0/) | 17 KB | ~4.3K | Baseline: + short dictionary excerpt |
| **1** | [`ste-code/artifacts/level1/`](ste-code/artifacts/level1/) | 58 KB | ~14.5K | + doc templates (code review / PR feedback) |
| **2** | [`ste-code/artifacts/level2/`](ste-code/artifacts/level2/) | 75 KB | ~18.5K | + section-specific grammar rules |
| **3** | [`ste-code/artifacts/level3/`](ste-code/artifacts/level3/) | 388 KB | ~95K | + complete dictionary + all 54 rules |
| **4** | [`ste-code/artifacts/level4/`](ste-code/artifacts/level4/) | 462 KB | ~116K | + extensions + reference catalogue |
| **5** | [`ste-code/artifacts/level5/`](ste-code/artifacts/level5/) | 539 KB | ~134K | Full standard (all rules + extensions + catalogue + provenance) |

Sizes are the measured sum of each tier's sub-documents. Token counts come from
the `o200k_base` tokenizer (GPT-4o / GPT-4.1 / GPT-5 / o-series); `cl100k_base`
(GPT-4, GPT-3.5-turbo) lands within 0.3% of the same figures, and Claude and
Llama tokenizers stay within a few percent for English prose. Regenerate the
table with:

```bash
python3 .agents/tools/maintenance/measure_artifacts.py
```

Two sub-documents are still base boilerplate rather than distilled output
(`level3/03-dictionary.md`, `level5/rules-sec7.md`). When Phase F distills them,
level 3 moves to ~95K tokens and level 5 drops to ~110K tokens.

Two **consolidated** deliverables are also produced for tooling that wants one
file:

* [`ste-code/artifacts/ste-code-rules.md`](ste-code/artifacts/ste-code-rules.md) — the full corpus, assembled deterministically.
* [`ste-code/artifacts/ste-code-system-prompt.md`](ste-code/artifacts/ste-code-system-prompt.md) — the same standard shaped as an LLM system prompt.

And an `llms.txt` / `llms-full.txt` pair (in the spirit of the
[llms.txt](https://llmstxt.org) convention) indexes every sub-document for
agentic retrieval.

---

## How it works

Copy a level's system prompt (or load its `llms.txt`) into your LLM. The model
writes clear, unambiguous documentation.

```
You:  Load ste-code/artifacts/level1/ and its _index.md, or ste-code-rules.md.
LLM:  You are an STE-Code technical writer. Apply these rules...
You:  Check this docstring.
      /** This function basically handles user stuff. */
LLM:  /** Creates a user or updates the data of a user. */
```

The LLM applies the controlled vocabulary, the synonym table, and the
sentence-length limits. It replaces jargon with approved words, uses active
voice and the imperative mood, and keeps each sentence to one instruction.

---

## The rules

The 54 rules cover nine sections:

| Section | Rules | Covers |
|---------|:-----:|--------|
| 1 — Words | 14 | Approved vocabulary, parts of speech, technical nouns and verbs |
| 2 — Noun Phrases | 2 | Article use, noun clusters |
| 3 — Verbs | 7 | Tense, voice, mood, verb forms |
| 4 — Sentences | 5 | Length, clarity, contractions, completeness |
| 5 — Procedures | 5 | Instructional writing, step structure |
| 6 — Descriptions | 5 | Descriptive writing, comparisons |
| 7 — Warnings | 3 | BREAKING / DEPRECATED / NOTE formatting |
| 8 — Punctuation | 6 | Commas, hyphens, parentheses, lists |
| 9 — Document Structure | 7 | Headings, lists, tables, organization |

Each rule carries a code-domain adaptation with paradigm-specific guidance for
object-oriented, functional, procedural, declarative, and systems programming.
The canonical source is [`ste-code/final/`](ste-code/final/) — every rule, the
dictionary, the synonym categories, the six gap-fill extensions, the reference
catalogue, and the provenance record.

---

## Benchmark

STE-Code vs. a plain assistant on 59 documentation tests across 14 categories:

| | STE-Code | Plain Assistant | Improvement |
|---|:--------:|:---------------:|:-----------:|
| Pass rate | 96.6% | 11.9% | **+84.7%** |
| Average score | 0.919 | 0.471 | **+0.448** |

Top categories: comments, error messages, and config files.

---

## Repository

```
STE-Code/
├── README.md                  This file
├── LICENSE                    MIT
├── mkdocs.yml                 Documentation site config (MkDocs → GitHub Pages)
├── docs/                      Documentation site (MkDocs)
│   ├── index.md               Home
│   ├── pipeline.md            Pipeline overview (A→F + Finalize + Artifacts)
│   ├── stages/                stage-a.md … stage-f.md
│   ├── contributing.md
│   └── roadmap/               Roadmap, grounding report, state reconciliation
├── ste-code/
│   ├── final/                 ★ THE STANDARD (source of truth, 54 rules)
│   │   ├── rules/             a-secN-ruleX.Y.md (54), a-categories.md, a-dictionary.md
│   │   ├── extensions/        six gap-fill areas (markdown + derived JSON)
│   │   ├── README.md          Standard overview
│   │   ├── provenance.md      Build/provenance record
│   │   └── reference-catalogue.md
│   ├── artifacts/             ★ DEPLOYABLE DELIVERABLES (Phase F)
│   │   ├── _base/             Deterministic boilerplate sub-docs per tier
│   │   ├── level-2/ … level5/ LLM-distilled sub-docs per tier
│   │   ├── ste-code-rules.md  Consolidated full corpus
│   │   ├── ste-code-system-prompt.md
│   │   ├── llms.txt           Index of every sub-document
│   │   └── llms-full.txt      Concatenation of every sub-document
│   ├── extracted/  refined/  grouped/  adapted/   (intermediate pipeline stages)
│   ├── extensions/  enriched/  data/  templates/  linguistics/  audit/
│   └── _archive/              Superseded pipeline output
├── spec/                      ASD-STE100 Issue 9 source (434 pages)
├── translations/              Locale scaffolding
└── .agents/                   Pipeline orchestration (agents, skills, tools)
    ├── tools/
    │   ├── extraction/ refinement/ grouping/ adaptation/ extension/
    │   ├── finalize/    artifacts/   trajectory/   linkcheck/
    │   ├── quality/  maintenance/  continuation/  benchmark/
    │   ├── lib/         shared/       prompts/      runners/
    │   └── TEMPLATES.md
    ├── vendor/                 Vendor research (git-ignored, not committed)
    └── tmp/                    Runtime scratch (git-ignored)
```

---

## Hybrid artifact build (Phase F)

The deployable artifacts are produced by a **hybrid** design so content is never
lost and never silently truncated:

1. **Deterministic level separation** — `levels_scaffold.py` reads `ste-code/final/`
   and emits, for each of the 8 tiers, a directory of **bounded sub-documents**
   (`ste-code/artifacts/_base/level<N>/…`). Oversized rule sections are split so
   no base sub-doc exceeds 400 KB. This is the boilerplate layer; it is
   byte-reproducible and needs no LLM.
2. **LLM distillation pass** — `distill_one.py` runs one Hermes session per
   sub-document. The worker reads its base sub-doc (plus `ste-code/final/` for
   anything outside it) and rewrites it into an LLM-optimized file at
   `ste-code/artifacts/level<N>/<subdoc>`, writing in multiple `write_file` /
   `patch` calls. On any failure it falls back to the deterministic base, so
   nothing is lost. Each worker commits its sub-doc turn-by-turn. Distillation
   takes the 1.85 MB base tier down to 388–539 KB; the largest distilled
   sub-document is 123 KB.
3. **Deterministic assembler** — `artifact_batch.py` concatenates `ste-code/final/`
   into `ste-code-rules.md` and `ste-code-system-prompt.md` (full rule coverage,
   version-stamped). No LLM, no truncation.
4. **Index assembly** — a final pass writes `llms.txt` (an `llms.txt`-style index
   of every tier/sub-doc) and `llms-full.txt` (the concatenation).

```
final/  ──levels_scaffold.py──▶  _base/level<N>/   ──distill_one.py (LLM)──▶  level<N>/<subdoc>
   │                                                                                  │
   └──────────────────artifact_batch.py────────────────▶ ste-code-rules.md ─────────┘
                                                                                    │
                                                          llms.txt + llms-full.txt ◀──┘
```

---

## Link checking

A lychee-based link checker lives in `.agents/tools/linkcheck/` (config
`lychee.toml`, runner `run_linkcheck.sh`). It scans `ste-code/final/**/*.md` and
`ste-code/artifacts/**/*.md`, ignoring intentional legacy `master.md#…`
backlinks and surfacing **real** broken links (stale internal paths, dead
external URLs). Run it with `bash .agents/tools/linkcheck/run_linkcheck.sh`.

---

## Pipeline (how the standard was built)

The standard was built from ASD-STE100 Issue 9 by a six-stage pipeline
**A→F**, terminating in a Finalize stage that consolidates everything into
`ste-code/final/`, followed by the Artifacts stage that packages `final/` into
deployables.

```
A Extract → B Refine → C Group → D Adapt → E Extend → Finalize → F Artifacts → Linkcheck
 (434 pp)    (109 f)    (24 f)    (54+ f)   (6 areas)   (final/)     (artifacts/)   (lychee)
```

| Stage | Reads | Writes | Type |
|:------:|-------|--------|------|
| **A** Extraction | `spec/issue-09-2025/page-dir/` | `ste-code/extracted/` | LLM workers |
| **B** Refinement | `ste-code/extracted/` | `ste-code/refined/` | LLM workers |
| **C** Grouping | `ste-code/refined/` | `ste-code/grouped/` | Deterministic |
| **D** Adaptation | `ste-code/grouped/` | `ste-code/adapted/` | LLM workers |
| **E** Extension | gap areas | `ste-code/extensions/` | LLM workers |
| **Finalize** | `ste-code/adapted/` + extensions | `ste-code/final/` (54 rules) | Deterministic + deep enrichment |
| **F** Artifacts | `ste-code/final/` | `ste-code/artifacts/` | Hybrid (deterministic + LLM) |
| **Linkcheck** | `ste-code/final/`, `ste-code/artifacts/` | reports | Deterministic (lychee) |

Stages C, Finalize, F (assembly), and Linkcheck are deterministic or
byte-moving, so content cannot be lost. Stages A, B, D, E use LLM workers.

Run the downstream chain:

```bash
bash .agents/tools/runners/launch-downstream.sh   # C→D→E→Finalize→F
```

The model is read from `STE_MODEL` (default `tencent/hy3:free`).

---

## Agent-agnostic tools

All pipeline scripts use the agent runner at `.agents/tools/lib/`. The default
backend is Hermes; other backends can be configured. Prompts are externalized to
`.agents/tools/prompts/*.md` and rendered with `templater.py` (double-brace
`{{token}}` syntax).

```bash
# Assemble the consolidated artifacts (deterministic, from final/)
python3 .agents/tools/artifacts/artifact_batch.py
python3 .agents/tools/artifacts/verify-artifacts.py

# Build the deterministic boilerplate sub-docs
python3 .agents/tools/artifacts/levels_scaffold.py

# Distill ONE sub-document with the LLM (one worker, own process)
python3 .agents/tools/artifacts/distill_one.py level3 01-principles.md 3 "..."

# Link check
bash .agents/tools/linkcheck/run_linkcheck.sh
```

Full documentation: the [documentation site](docs/index.md) and
[`.agents/AGENTS.md`](.agents/AGENTS.md).

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

## Credits & references

STE-Code stands on decades of controlled-language research, documentation
theory, and verification tooling.

### Primary standard
- **ASD-STE100 Simplified Technical English, Issue 9 (January 2025)** — the
  foundational standard STE-Code adapts to the code domain, owned by **ASD**
  (Aerospace, Security and Defence Industries Association of Europe),
  maintained by the **Simplified Technical English Maintenance Group (STEMG)**.
  <https://www.asd-ste100.org/>

### Controlled natural language theory
- **Tobias Kuhn** — *A Survey and Classification of Controlled Natural
  Languages* (Computational Linguistics, 2014). Source of the PENS classification.
  <https://aclanthology.org/J14-1005.pdf>
- **Norbert E. Fuchs & Rolf Schwitter** (University of Zurich) — *Attempto
  Controlled English (ACE)* (1996). <https://attempto.ifi.uzh.ch/>

### Documentation & readability
- **John M. Carroll** — *Minimalism* (ACM SIGDOC). Basis for register
  stratification: users act first and read at the moment of need.

### Adjacent standards
- **Google Style Guides** — <https://google.github.io/styleguide/>
- **github/codeql-coding-standards** — machine-enforceable standards as
  executable queries. <https://github.com/github/codeql-coding-standards>

### IP note
ASD-STE100 is a copyright and trademark of ASD, Brussels. STE-Code adapts its
*principles and rule categories* to the software domain; it does not reproduce
the standard's dictionary or rule text. Obtain Issue 9 directly from ASD
(free via the official form): <https://www.asd-ste100.org/>.
