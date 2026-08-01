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
├── CONTRIBUTING.md            Contribution policy
├── CODE_OF_CONDUCT.md
├── CITATION.cff
├── LICENSE                    MIT
├── mkdocs.yml                 Documentation site config
├── docs/                      Documentation site (MkDocs → GitHub Pages)
│   ├── index.md               Home
│   ├── pipeline.md            Six-stage A→F overview
│   ├── stages/                stage-a.md … stage-f.md
│   ├── contributing.md
│   └── roadmap/               Roadmap, grounding report, state reconciliation
├── spec/                      ASD-STE100 Issue 9 source (434 pages)
│   └── issue-09-2025/page-dir/   Page files + MANIFEST.md
├── ste-code/
│   ├── artifacts/             Stage F — deliverables + level prompts
│   │   ├── level1/system-prompt.txt     ★ ~1.2K tokens
│   │   ├── level2/system-prompt.txt     ★ ~4.5K tokens
│   │   ├── level3/system-prompt.txt     ★ ~8K tokens
│   │   ├── level4/                      ★ rules + dictionary (~45K tokens)
│   │   └── level5/                      ★ full rule summaries
│   ├── extracted/             Stage A — raw page extraction (109 files)
│   ├── refined/               Stage B — formatted pages (109 files)
│   ├── grouped/               Stage C — 24 semantic groups
│   ├── adapted/               Stage D — the standard, adapted to code
│   ├── extensions/            Stage E — gap-fill entries (markdown + derived JSON)
│   ├── enriched/              Enrichment pass output
│   ├── data/                  Structured JSON (vocabulary, synonym table)
│   ├── merged/                master-raw.md consolidation
│   ├── templates/             Additional system prompts
│   ├── linguistics/           Research notes, decision tree, contracts
│   ├── audit/                 Audit reports
│   └── _archive/              Superseded pipeline output
├── translations/              Locale scaffolding (10 locales)
└── .agents/                   Pipeline orchestration (agents, skills, config)
    ├── config/agents.yaml     Agent backend configuration
    ├── benchmark/             59-test benchmark suite
    └── tools/
        ├── runners/           phase-a … phase-f runners + launch-downstream.sh
        ├── extraction/  refinement/  grouping/
        ├── adaptation/  extension/   artifacts/
        ├── quality/  maintenance/  continuation/  benchmark/
        └── lib/               Agent runner and shared infrastructure
```

---

## Agent-Agnostic Tools

All pipeline scripts use the agent runner at `.agents/tools/lib/agent-runner.py`. The default backend is Hermes. Add other agents in `.agents/config/agents.yaml`. The model is read from `STE_MODEL` (default `tencent/hy3:free`).

```bash
# List available agent backends
python3 .agents/tools/lib/agent-runner.py --list

# Run one pipeline stage (see the stage table below)
python3 .agents/tools/runners/phase-c-run.py --verify     # deterministic
python3 .agents/tools/runners/phase-d-run.py --resume     # LLM workers

# Run the downstream chain C→D→E→F
bash .agents/tools/runners/launch-downstream.sh

# Assemble the level prompts (all accept --agent <name> and --dry-run)
python3 .agents/tools/refinement/assemble-level3.py
python3 .agents/tools/refinement/assemble-level2.py
python3 .agents/tools/refinement/assemble-level1.py

# Quality sweep and benchmark
python3 .agents/tools/quality/sweep-quality.py --batches 5
python3 .agents/benchmark/orchestrator.py
```

Full documentation: the [documentation site](docs/index.md) and [`.agents/AGENTS.md`](.agents/AGENTS.md).

---

## Pipeline

The standard was built from ASD-STE100 Issue 9 by a six-stage pipeline (A→F). Every stage has a runner in `.agents/tools/runners/` and a deterministic verification gate.

```
A Extract → B Refine → C Group → D Adapt → E Extend → F Artifacts
 (434 pp)    (109 f)    (24 f)    (58+ f)   (6 areas)   (deliverables)
```

| Stage | Runner | Reads | Writes | Gate |
|:-----:|--------|-------|--------|------|
| **A** Extraction | `phase-a-run.py`, `phase-a-gen.py` | `spec/issue-09-2025/page-dir/` | `ste-code/extracted/` | size + page headers, 2 retries |
| **B** Refinement | `phase-b-run.py`, `phase-b1-run.py` | `ste-code/extracted/` | `ste-code/refined/` | per-batch parity, `verify_continuation.py` |
| **C** Grouping | `phase-c-run.py` | `ste-code/refined/` | `ste-code/grouped/` | `verify-groups.py` |
| **D** Adaptation | `phase-d-run.py` | `ste-code/grouped/` | `ste-code/adapted/` | `verify-adaptation.py` |
| **E** Extension | `phase-e-run.py` | gap areas | `ste-code/extensions/` | `verify_extensions.py` |
| **F** Artifacts | `phase-f-run.py` | `ste-code/adapted/` | `ste-code/artifacts/` | `verify-artifacts.py` |

Stages A, B, D, and E use LLM workers. Stages C and F are pure Python: grouping and assembly only move bytes, so content cannot be lost.

```bash
# Run the downstream chain C→D→E→F
bash .agents/tools/runners/launch-downstream.sh

# Grouping dry-run only (writes nothing)
bash .agents/tools/runners/launch-downstream.sh --dry
```

Stage details: [docs/pipeline.md](docs/pipeline.md) and [docs/stages/](docs/stages/).

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

## Credits & References

STE-Code stands on decades of controlled-language research, documentation
theory, and verification tooling.

### Primary Standard

- **ASD-STE100 Simplified Technical English, Issue 9 (January 2025)** —
  the foundational standard STE-Code adapts to the code domain. Owned by
  **ASD — Aerospace, Security and Defence Industries Association of Europe**,
  Brussels; maintained by the **Simplified Technical English Maintenance
  Group (STEMG)**. Copyright and trademark of ASD.
  <https://www.asd-ste100.org/>

- **AECMA / AIA Simplified English lineage** — STE's origin: developed in the
  late 1970s–1980s by the **European Association of Aerospace Industries
  (AECMA, now ASD)** with the **Aerospace Industries Association of America
  (AIA)**, at the request of the **Association of European Airlines (AEA)**.
  Working group founded 30 June 1983, Amsterdam; first Guide release 1986;
  became ASD-STE100 specification in 2005 and an international standard in
  2025. Historical basis for STE-Code's core principle: enforceability
  determines survival (Caterpillar Fundamental English, unenforced, died 1982).

### Controlled Natural Language Theory

- **Tobias Kuhn** — *A Survey and Classification of Controlled Natural
  Languages* (Computational Linguistics, 2014; 636+ citations). Source of
  the PENS classification (Precision, Expressiveness, Naturalness,
  Simplicity) used to profile STE-Code rules.
  <https://aclanthology.org/J14-1005.pdf>

- **Norbert E. Fuchs & Rolf Schwitter** (University of Zurich) — *Attempto
  Controlled English (ACE)* (1996). Precedent for machine-processable
  controlled English and explicit quoting conventions for the use–mention
  distinction.
  <https://attempto.ifi.uzh.ch/>

- **Rimay CNL research** — *On systematically building a controlled natural
  language for functional requirements* (PubMed). Source of the coverage
  methodology (88% of 460 real statements expressible).
  <https://pubmed.ncbi.nlm.nih.gov/34776756/>

### Documentation & Readability Research

- **John M. Carroll** — *Minimalism* tradition in technical documentation
  (ACM SIGDOC). Learning-theoretic basis for register stratification: users
  act first and read at the moment of need.
  <https://dl.acm.org/doi/10.1145/296336.296362>

### Verification & Executable Documentation Tooling

- **asciidoctest** (PyPI) — *Verifiable, stateful, and interactive
  documentation with AsciiDoc*. Reference implementation for code-block
  verification.
  <https://libraries.io/pypi/asciidoctest>

### Adjacent Standards & Catalogues

- **Google Style Guides** — precedent for public, per-language style standards.
  <https://google.github.io/styleguide/>
- **Kristories/awesome-guidelines** — community catalogue of coding standards.
  <https://github.com/Kristories/awesome-guidelines>
- **github/codeql-coding-standards** — precedent for machine-enforceable
  standards as executable queries.
  <https://github.com/github/codeql-coding-standards>

### Intellectual-Property Note

ASD-STE100 is a copyright and trademark of ASD, Brussels. STE-Code adapts
its *principles and rule categories* to the software domain; it does not
reproduce the standard's dictionary or rule text. Users requiring the
authoritative aerospace standard should obtain Issue 9 directly from ASD
(free of charge via the official form): <https://www.asd-ste100.org/>.
