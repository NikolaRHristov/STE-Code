# STE-Code 📘

[ASD-STE100](https://asd-ste100.org) is _Simplified Technical English_, a
controlled language from the aerospace industry. It is a set of writing rules
and an approved dictionary. Aircraft maintenance manuals use it so that no
sentence has two meanings.

**STE-Code applies that idea to code documentation.** It gives you 54 writing
rules in 9 sections, 4 General Rules (GR1–GR4), a code-domain dictionary, and a
synonym table. Use it for comments, docstrings, error messages, commit messages,
API documentation, changelogs, and configuration files. The standard removes
ambiguity, jargon, and hedging.

You do not have to read the standard. Load one file into a large language model,
and the model writes to the standard for you.

---

## Load a level 📦

Each level is one plain-text file. Copy it into the system-prompt field of your
model. A higher level is stricter and costs more context.

| Level  | File                                           |   Size |  Tokens | What it adds                             |
| :----: | ---------------------------------------------- | -----: | ------: | ---------------------------------------- |
| **-2** | `ste-code/artifacts/level-2/system-prompt.txt` |   5 KB |   ~1.2K | The 14 core principles                   |
| **-1** | `ste-code/artifacts/level-1/system-prompt.txt` |  26 KB |   ~5.9K | + the synonym table                      |
| **0**  | `ste-code/artifacts/level0/system-prompt.txt`  |  17 KB |   ~4.3K | + a short dictionary excerpt             |
| **1**  | `ste-code/artifacts/level1/system-prompt.txt`  |  58 KB |  ~14.5K | + document templates                     |
| **2**  | `ste-code/artifacts/level2/system-prompt.txt`  |  75 KB |  ~18.5K | + section grammar rules                  |
| **3**  | `ste-code/artifacts/level3/system-prompt.txt`  | 388 KB |  ~94.7K | + the full dictionary and all 54 rules   |
| **4**  | `ste-code/artifacts/level4/system-prompt.txt`  | 462 KB | ~116.0K | + extensions and the reference catalogue |
| **5**  | `ste-code/artifacts/level5/system-prompt.txt`  | 539 KB | ~133.8K | + provenance (the complete standard)     |

> [!TIP]
>
> **Start at level 1.** It fits an ordinary context window and it includes the
> templates. Move to level 3 or higher only when you need full rule coverage.

**`Terminal`**

```bash
ollama run llama3 --system "$(cat ste-code/artifacts/level1/system-prompt.txt)"
```

The model then applies the controlled vocabulary, the synonym table, and the
sentence-length limits.

Each level directory also holds the same content as separate markdown
sub-documents plus an `_index.md`, so an agent can read one part instead of the
whole file. `ste-code/artifacts/llms.txt` indexes every level, and
`ste-code/artifacts/llms-full.txt` holds every sub-document in one file.

Size is the size of `system-prompt.txt` on disk. Token counts use the
`o200k_base` tokenizer (GPT-4o, GPT-4.1, GPT-5, o-series); `cl100k_base` (GPT-4,
GPT-3.5-turbo) agrees to within 0.3%. Regenerate the numbers with
`python3 .agents/tools/maintenance/measure_artifacts.py`.

---

## Pages 📄

| Page                            | Contents                                                        |
| ------------------------------- | --------------------------------------------------------------- |
| [Pipeline](pipeline.md)         | The five stages that build the standard, with runners and gates |
| [Contributing](contributing.md) | How to run the pipeline locally and how to propose a change     |
| [Roadmap](roadmap/ROADMAP.md)   | Planned work on the linguistic layer                            |

---

## The standard 📏

The 54 rules are in `ste-code/final/rules/`, one file per rule.

| Section | Rules | Covers                                                                 |
| :-----: | :---: | ---------------------------------------------------------------------- |
|    1    |  14   | Words: approved vocabulary, parts of speech, technical nouns and verbs |
|    2    |   3   | Noun phrases: articles, noun clusters                                  |
|    3    |   7   | Verbs: tense, voice, mood, verb forms                                  |
|    4    |   5   | Sentences: length, clarity, completeness                               |
|    5    |   5   | Procedures: instructional writing, step structure                      |
|    6    |   6   | Descriptions: descriptive writing, comparisons                         |
|    7    |   3   | Warnings: BREAKING, DEPRECATED, and NOTE formatting                    |
|    8    |   7   | Punctuation: commas, hyphens, parentheses, lists                       |
|    9    |   4   | Document structure: headings, lists, tables, organization              |

Each rule carries a code-domain adaptation with guidance for the
object-oriented, functional, procedural, declarative, and systems paradigms.

`ste-code/final/` also holds the dictionary, the 22 technical-noun categories,
six gap-fill extensions, the reference catalogue, and the provenance record. The
four General Rules live in `ste-code/adapted/a-sec9-gr1..4.md`.

---

## Repository layout 🗂️

| Path                   | Contents                                                                            |
| ---------------------- | ----------------------------------------------------------------------------------- |
| `ste-code/artifacts/`  | The deliverable: 8 tier directories, `llms.txt`, `llms-full.txt`, `VERSION`         |
| `ste-code/final/`      | The standard                                                                        |
| `ste-code/extracted/`  | Stage 1 output: 109 raw page-group files                                            |
| `ste-code/refined/`    | Stage 2 output: 109 formatted page-group files                                      |
| `ste-code/grouped/`    | Stage 3 output: 24 semantic groups                                                  |
| `ste-code/adapted/`    | Stage 4 output: 60 code-domain rule files                                           |
| `ste-code/extensions/` | Gap-fill entries: verbs, adjectives, nouns, anti-patterns, domains                  |
| `spec/`                | ASD-STE100 Issue 9 source. The PDF has 434 pages; the split produces 426 page files |
| `docs/`                | This documentation site                                                             |
| `translations/`        | Locale scaffolding for 10 locales (bg, de, es, fr, it, ja, pl, pt-BR, uk, zh-CN)    |
| `.agents/`             | Pipeline orchestration: runners, tools, skills, benchmark. Development only         |

The full tree is in the
[repository README](https://github.com/NikolaRHristov/STE-Code#repository).

---

## Benchmark 📊

`.agents/benchmark/` holds 59 tests in 14 categories. It scores a model with a
level artifact against the same model without one.

**`Terminal`**

```bash
python3 .agents/benchmark/benchmark-levels.py --levels -2,-1,0,1,2,3,4,5
python3 .agents/benchmark/orchestrator-control.py # plain-assistant baseline
```

> [!NOTE]
>
> **Run output is not committed**, so this site publishes no score. Run the
> suite to get numbers for your own model.

---

## License and attribution ⚖️

STE-Code is MIT licensed. ASD-STE100 is a copyright and a trademark of ASD,
Brussels. STE-Code adapts the _principles and rule categories_ of the standard
to the software domain. It does not reproduce the dictionary or the rule text of
the standard. Get the authoritative aerospace standard with the free official
form at <https://www.asd-ste100.org/>.
