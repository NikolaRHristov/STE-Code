# STE-Code Documentation

STE-Code is a documentation standard adapted from
[ASD-STE100 Issue 9 (January 2025)](https://asd-ste100.org) for code
documentation. It gives you writing rules, four General Rules (GR1–GR4), a
controlled vocabulary, and system-prompt templates at five levels.

The standard removes ambiguity, jargon, and hedging from README files, API
documentation, docstrings, commit messages, and error messages.

---

## Start here

| Page | Contents |
|------|----------|
| [Pipeline](pipeline.md) | The six-stage A→F build, with reads and writes per stage |
| [Stage A — Extraction](stages/stage-a.md) | Spec pages → `ste-code/extracted/` |
| [Stage B — Refinement](stages/stage-b.md) | Extracted pages → `ste-code/refined/` |
| [Stage C — Grouping](stages/stage-c.md) | Refined pages → `ste-code/grouped/` (24 groups) |
| [Stage D — Adaptation](stages/stage-d.md) | Grouped spec → `ste-code/adapted/` (code domain) |
| [Stage E — Extension](stages/stage-e.md) | Gap-fill entries → `ste-code/extensions/` |
| [Stage F — Artifacts](stages/stage-f.md) | Adapted rules → `ste-code/artifacts/` |
| [Contributing](contributing.md) | Local pipeline run and contribution rules |

---

## Adaptation levels

Each level is a directory of sub-documents, with a concatenated
`system-prompt.txt` for one-file use. Choose the level that fits your token
budget.

| Level | Directory | Size | Tokens | Best for |
|:-----:|-----------|:----:|:------:|----------|
| **-2** | [`level-2/`](https://github.com/NikolaRHristov/STE-Code/tree/Current/ste-code/artifacts/level-2) | 5 KB | ~1.2K | Ultra-minimal: the 14 core principles |
| **-1** | [`level-1/`](https://github.com/NikolaRHristov/STE-Code/tree/Current/ste-code/artifacts/level-1) | 26 KB | ~5.9K | Core principles + synonym table |
| **0** | [`level0/`](https://github.com/NikolaRHristov/STE-Code/tree/Current/ste-code/artifacts/level0) | 17 KB | ~4.3K | Baseline: + short dictionary excerpt |
| **1** | [`level1/`](https://github.com/NikolaRHristov/STE-Code/tree/Current/ste-code/artifacts/level1) | 58 KB | ~14.5K | Interactive sessions, tight token budgets |
| **2** | [`level2/`](https://github.com/NikolaRHristov/STE-Code/tree/Current/ste-code/artifacts/level2) | 75 KB | ~18.5K | Code review, PR feedback |
| **3** | [`level3/`](https://github.com/NikolaRHristov/STE-Code/tree/Current/ste-code/artifacts/level3) | 388 KB | ~95K | Full document rewriting |
| **4** | [`level4/`](https://github.com/NikolaRHristov/STE-Code/tree/Current/ste-code/artifacts/level4) | 462 KB | ~116K | Strict compliance checking |
| **5** | [`level5/`](https://github.com/NikolaRHristov/STE-Code/tree/Current/ste-code/artifacts/level5) | 539 KB | ~134K | Specification-grade documentation |

Sizes are measured sums of each tier's sub-documents. Token counts use the
`o200k_base` tokenizer (GPT-4o, GPT-4.1, GPT-5, o-series); `cl100k_base`
(GPT-4, GPT-3.5-turbo) agrees to within 0.3%. Run
`python3 .agents/tools/maintenance/measure_artifacts.py` to regenerate them.

To use a level, copy its `system-prompt.txt` into the system-prompt field of
your model. The model then applies the controlled vocabulary, the synonym table,
and the sentence-length limits.

---

## Benchmark

STE-Code against a plain assistant on 59 documentation tests in 14 categories:

| | STE-Code | Plain assistant | Improvement |
|---|:--------:|:---------------:|:-----------:|
| Pass rate | 96.6% | 11.9% | **+84.7%** |
| Average score | 0.919 | 0.471 | **+0.448** |

The benchmark suite is in
[`.agents/benchmark/`](https://github.com/NikolaRHristov/STE-Code/tree/Current/.agents/benchmark).

---

## Repository layout (short form)

| Path | Contents |
|------|----------|
| `ste-code/` | All pipeline layers, from `extracted/` to `artifacts/` |
| `spec/` | ASD-STE100 Issue 9 source, split into 434 page files |
| `.agents/` | Pipeline orchestration: runners, tools, skills, agents, benchmark |
| `docs/` | This documentation site |
| `translations/` | Locale scaffolding (bg, de, es, fr, it, ja, pl, pt-BR, uk, zh-CN) |

The full tree is in the
[repository README](https://github.com/NikolaRHristov/STE-Code#repository).

---

## License and attribution

STE-Code is MIT licensed. ASD-STE100 is a copyright and trademark of ASD,
Brussels. STE-Code adapts the *principles and rule categories* of the standard
to the software domain. It does not reproduce the dictionary or the rule text of
the standard. To get the authoritative aerospace standard, use the official
form at <https://www.asd-ste100.org/>.
