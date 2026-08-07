# Pipeline ⚙️

The pipeline reads the ASD-STE100 Issue 9 specification and writes the STE-Code
level artifacts. It runs in five stages. Each stage has a runner in
`.agents/tools/runners/`, an orchestrator module in `.agents/tools/<domain>/`,
and a deterministic gate that blocks the commit when the stage output is bad.

**`Pipeline`**

```text
Extraction → Refinement → Merge → Adaptation → Artifacts
 extracted/    refined/    grouped/   adapted/   artifacts/
  (109 f)      (109 f)     (24 f)      (60 f)     (8 tiers)
                                       final/
```

Every stage writes into its own directory under `ste-code/`. A stage never edits
the output of an earlier stage, so you can re-run one stage without losing the
rest.

---

## Stages 🧩

|  #  | Stage      | Reads                          | Writes                                                   | Type                  | Runner                                               | Gate                                           |
| :-: | ---------- | ------------------------------ | -------------------------------------------------------- | --------------------- | ---------------------------------------------------- | ---------------------------------------------- |
|  1  | Extraction | `spec/issue-09-2025/page-dir/` | `ste-code/extracted/` — 109 page-group files             | LLM workers           | `phase-a-run.py`, `phase-a-gen.py`                   | Output size and page headers, 2 retries        |
|  2  | Refinement | `ste-code/extracted/`          | `ste-code/refined/` — 109 formatted files                | LLM workers           | `phase-b-run.py`, `phase-b1-run.py`                  | Per-batch content parity                       |
|  3  | Merge      | `ste-code/refined/`            | `ste-code/grouped/` — 24 groups plus `GROUPING-NOTES.md` | Deterministic         | `phase-c-run.py`                                     | `verify-groups.py`                             |
|  4  | Adaptation | `ste-code/grouped/`            | `ste-code/adapted/`, then `ste-code/final/`              | LLM workers           | `phase-d-run.py`, `phase-e-run.py`, `phase-g-run.py` | `verify-adaptation.py`, `verify_extensions.py` |
|  5  | Artifacts  | `ste-code/final/`              | `ste-code/artifacts/` — 8 tiers                          | Deterministic and LLM | `phase-f-run.py`                                     | `verify-artifacts.py`                          |

All runners are in `.agents/tools/runners/`.

### 1. Extraction ⛏️

Workers read the specification pages and write markdown. Each worker takes four
pages. The source PDF has 434 pages, and the split produces 426 page files,
because the front matter and the blank versos merge.

### 2. Refinement ✨

Workers reformat the raw extraction into clean markdown: dictionary tables and
rule pages. No content is removed.

### 3. Merge 🔗

Python concatenates and splits the 109 refined files into 24 semantic groups. No
model runs in this stage. Reorganization moves bytes; it does not re-type them,
so content cannot be lost.

### 4. Adaptation 🔄

Workers rewrite the aerospace specification into the code domain. Rule numbers
and structure stay the same. The examples change from aircraft maintenance to
code documentation. This stage produces:

| Output                 | Contents                                                                                                         |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `ste-code/adapted/`    | 60 markdown files: 54 rules, 4 General Rules, the dictionary, the categories                                     |
| `ste-code/extensions/` | Gap-fill entries for the code domain: verbs, adjectives, nouns, anti-patterns, domains                           |
| `ste-code/final/`      | The consolidated standard: 54 rule files, dictionary, 22 categories, extensions, reference catalogue, provenance |

Workers emit markdown only. Any JSON is derived from that markdown by a separate
deterministic step, so a model never hand-writes structured data.

`ste-code/final/` is the source of truth for stage 5.

### 5. Artifacts 📦

Stage 5 packages `ste-code/final/` into the deliverable at
`ste-code/artifacts/`. It works in three steps:

1. **Scaffold (deterministic).** `levels_scaffold.py` reads `ste-code/final/`
   and writes one directory of bounded sub-documents per tier into
   `ste-code/artifacts/_base/level<N>/`. Oversized rule sections are split. This
   step is byte-reproducible and needs no model.
2. **Distill (LLM).** `distill_one.py` runs one session per sub-document. It
   rewrites the scaffold into an optimized file at
   `ste-code/artifacts/level<N>/<subdoc>`, in several `write_file` and `patch`
   calls. If a session fails, the deterministic scaffold stays in place, so
   nothing is lost.
3. **Assemble (deterministic).** `artifact_batch.py` writes each tier's
   `_index.md` and `system-prompt.txt`, then the top-level `llms.txt`,
   `llms-full.txt`, and `VERSION`.

`system-prompt.txt` is the tier's sub-documents joined together. It is the file
you load into a model.

---

## Which stages use a model 🤖

|    Stage     | Type              | Reason                                                                                                        |
| :----------: | ----------------- | ------------------------------------------------------------------------------------------------------------- |
| 1 Extraction | LLM workers       | Reads spec page text and writes markdown                                                                      |
| 2 Refinement | LLM workers       | Reformats extracted text into the refinement rules                                                            |
|   3 Merge    | **Deterministic** | Grouping only moves bytes, so content cannot be lost                                                          |
| 4 Adaptation | LLM workers       | Genuine rewriting: aerospace examples become code-domain examples                                             |
| 5 Artifacts  | **Hybrid**        | Deterministic scaffold and assembly, with an LLM distillation pass that falls back to the scaffold on failure |

The Merge stage and the assembly step of Artifacts are pure Python on purpose. A
free-tier model that is asked to re-emit a 650 KB corpus truncates mid-stream,
and that is silent content loss. Where the task is reorganization and not
writing, the pipeline moves bytes instead of re-typing them.

---

## Output layers 🗃️

Everything the pipeline writes is under `ste-code/`.

| Directory      | Stage | Contents                                                                                                                                              |
| -------------- | :---: | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `extracted/`   |   1   | 109 raw page-group files (`wNNN-pA-B.md`), 4 spec pages each                                                                                          |
| `refined/`     |   2   | 109 formatted page-group files (`rNNN-pA-B.md`)                                                                                                       |
| `grouped/`     |   3   | 24 group files plus `GROUPING-NOTES.md`                                                                                                               |
| `adapted/`     |   4   | 60 markdown files of code-domain rules                                                                                                                |
| `extensions/`  |   4   | Gap-fill entries, markdown plus derived JSON                                                                                                          |
| `final/`       |   4   | **The standard**: 54 rule files (`a-secN-ruleX.Y.md`), `a-categories.md`, `a-dictionary.md`, `extensions/`, `reference-catalogue.md`, `provenance.md` |
| `artifacts/`   |   5   | `_base/` (deterministic scaffold), `level-2/`…`level5/` (distilled sub-documents), `llms.txt`, `llms-full.txt`, `VERSION`                             |
| `enriched/`    |   —   | 109 enrichment-pass files                                                                                                                             |
| `data/`        |   —   | Synonym table and vocabulary JSON                                                                                                                     |
| `templates/`   |   —   | Prompt templates for each STE-Code register                                                                                                           |
| `linguistics/` |   —   | Research notes, decision tree, generation contract, reference linter                                                                                  |
| `audit/`       |   —   | Audit reports                                                                                                                                         |

The consolidation into `final/` is grounded in the vendor research under
`.agents/vendor/`. That directory holds cloned public reference corpora. It is
git-ignored and it is never committed.

---

## Run a stage 🏃

The deterministic stages are safe on a clean checkout. The model stages cost
tokens and rewrite tracked content, so run them only when you intend to
regenerate that layer.

**`Terminal`**

```bash
# Merge — plan only, writes nothing
python3 .agents/tools/runners/phase-c-run.py --dry-run

# Merge — assemble and gate
python3 .agents/tools/runners/phase-c-run.py --verify

# Artifacts — plan only
python3 .agents/tools/runners/phase-f-run.py --dry-run

# The whole downstream chain
bash .agents/tools/runners/launch-downstream.sh
bash .agents/tools/runners/launch-downstream.sh --dry
```

Each stage refuses to start when its input is not ready, so an early abort is a
hard stop and not a silent failure. `launch-downstream.sh` stops before the
Merge stage when `ste-code/refined/` holds fewer than 100 markdown files,
because that means refinement is still running.

The model comes from the `STE_MODEL` environment variable. The default is
`tencent/hy3:free`.

**`Terminal`**

```bash
STE_MODEL=tencent/hy3:free bash .agents/tools/runners/launch-downstream.sh
```

---

## Gates 🚪

Each stage has a deterministic verifier. Exit code `0` means the gate passes.

**`Terminal`**

```bash
python3 .agents/tools/grouping/verify-groups.py       # Merge
python3 .agents/tools/adaptation/verify-adaptation.py # Adaptation
python3 .agents/tools/extension/verify_extensions.py  # Extensions
python3 .agents/tools/artifacts/verify-artifacts.py   # Artifacts
```

Quality checks that apply to any markdown layer:

**`Terminal`**

```bash
python3 .agents/tools/quality/check-rails.py  # the 8 rails
python3 .agents/tools/quality/check-tables.py # table integrity
bash .agents/tools/linkcheck/run_linkcheck.sh # lychee link check
```

---

## Checkpoints and resume 💾

Every orchestrated stage writes a checkpoint into `.agents/state/` after each
work item, and commits the item when the gate passes. If the session stops,
restart the stage with `--resume` to skip the completed items.

|    Stage     | Checkpoint                                                                                  |
| :----------: | ------------------------------------------------------------------------------------------- |
| 1 Extraction | `.agents/state/extraction-checkpoint.json`                                                  |
| 2 Refinement | `.agents/state/refine-checkpoint.json`                                                      |
|   3 Merge    | `.agents/state/grouping-checkpoint.json`                                                    |
| 4 Adaptation | `.agents/state/adapt-checkpoint.json`, `extend-checkpoint.json`, `finalize-checkpoint.json` |
| 5 Artifacts  | `.agents/state/artifact-checkpoint.json`, `artifact-llm-checkpoint.json`                    |

---

## Prerequisites ✅

| Requirement      | Needed for                                                        |
| ---------------- | ----------------------------------------------------------------- |
| Python 3         | Every runner, and the deterministic stages                        |
| An agent backend | The stages that call a model (1, 2, 4, and the distill step of 5) |

The default backend is Hermes. Configure backends in
`.agents/config/agents.yaml` and list them with:

**`Terminal`**

```bash
python3 .agents/tools/lib/agent-runner.py --list
```

The extension and artifact runners call
`~/.hermes/hermes-agent/venv/bin/python3`. If Hermes is not at that path, start
`extend_batch.py` or `artifact_batch.py` directly with your own interpreter.
