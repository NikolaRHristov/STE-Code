# Pipeline

STE-Code is built from the ASD-STE100 Issue 9 specification by a **six-stage
pipeline (A→F)**. Each stage has one runner in `.agents/tools/runners/`, one
orchestrator module in `.agents/tools/<domain>/`, and a deterministic
verification gate that blocks the commit when the stage output is bad.

```text
A Extraction → B Refinement → C Grouping → D Adaptation → E Extension → Finalize → F Artifacts → Linkcheck
   spec/          extracted/     refined/      grouped/       adapted/      final/      artifacts/   (lychee)
      ↓               ↓             ↓             ↓              ↓           ↓            ↓
  extracted/       refined/      grouped/      adapted/     extensions/    final/     artifacts/  reports
   (109 f)         (109 f)       (24 f)        (54+ f)        (6 areas)   (54 rules)  (deliverables)
```

Stage **Finalize** consolidates the adapted corpus + extensions into the single
canonical standard at `ste-code/final/` (54 rules, dictionary, categories,
extensions, catalogue, provenance). Stage **F (Artifacts)** packages `final/`
into deployables. The **Linkcheck** stage (lychee, in `.agents/tools/linkcheck/`)
validates links across `final/` and `artifacts/`.

---

## Stage table

| Stage | Runner | Reads | Writes | Gate |
|:-----:|--------|-------|--------|------|
| [A](stages/stage-a.md) | `phase-a-run.py`, `phase-a-gen.py` | `spec/issue-09-2025/page-dir/` (434 pages) | `ste-code/extracted/` | output size + page headers, 2 retries |
| [B](stages/stage-b.md) | `phase-b-run.py`, `phase-b1-run.py` | `ste-code/extracted/` | `ste-code/refined/` | per-batch content parity; `verify_continuation.py` |
| [C](stages/stage-c.md) | `phase-c-run.py` | `ste-code/refined/` | `ste-code/grouped/` | `verify-groups.py` |
| [D](stages/stage-d.md) | `phase-d-run.py` | `ste-code/grouped/` | `ste-code/adapted/` | `verify-adaptation.py` |
| [E](stages/stage-e.md) | `phase-e-run.py` | gap areas + adapted corpus | `ste-code/extensions/` | `verify_extensions.py` |
| [F](stages/stage-f.md) | `phase-f-run.py`, `artifact_batch.py`, `distill_one.py` | `ste-code/final/` | `ste-code/artifacts/` | `verify-artifacts.py` |

---

## Which stages use an LLM

| Stage | Type | Reason |
|:-----:|------|--------|
| A | LLM workers | Reads spec page images/text and writes markdown |
| B | LLM workers | Reformats extracted text into the 9 refinement rules |
| C | **Deterministic** | Grouping only moves bytes (concatenate + split), so content cannot be lost |
| D | LLM workers | Genuine rewriting: aerospace examples become code-domain examples |
| E | LLM workers | Generates new code-domain entries; JSON is derived deterministically |
| F | **Hybrid** | Deterministic assembly (`artifact_batch.py`) concatenates `final/` with no truncation; an LLM pass (`distill_one.py`) distills each sub-document into `level<N>/`. The LLM writes in multiple `write_file`/`patch` calls; on failure it falls back to the deterministic base. |
| Finalize | Deterministic + deep enrichment | Consolidates `adapted/` + extensions into `final/` (54 rules), grounded in `.agents/vendor/` research. |
| Linkcheck | Deterministic | lychee scans `final/` + `artifacts/` for broken links. |

Stage C and Stage F are pure Python on purpose. A free-tier model that is asked
to re-emit a 600 KB corpus truncates mid-stream, which is silent content loss.
Where the task is reorganization, not writing, the pipeline moves bytes instead
of re-typing them.

---

## Run the downstream stages

`launch-downstream.sh` runs C→D→E→F in order. Each stage refuses to start when
its input is not ready, so an early abort is a hard stop and not a silent
failure.

```bash
# Full downstream run: C → D → E → F
bash .agents/tools/runners/launch-downstream.sh

# Grouping dry-run only (writes nothing)
bash .agents/tools/runners/launch-downstream.sh --dry
```

The script stops before Stage C when `ste-code/refined/` has fewer than 100
markdown files, because that means the refiner is still running.

The model is read from the `STE_MODEL` environment variable
(default: `tencent/hy3:free`).

```bash
STE_MODEL=tencent/hy3:free bash .agents/tools/runners/launch-downstream.sh
```

---

## Output layers

All pipeline output is under `ste-code/`.

| Directory | Stage | Contents |
|-----------|:-----:|----------|
| `extracted/` | A | 109 raw page-group files (`wNNN-pA-B.md`), 4 spec pages each |
| `refined/` | B | 109 formatted page-group files (`rNNN-pA-B.md`) |
| `grouped/` | C | 24 semantic group files plus `GROUPING-NOTES.md` |
| `final/` | Finalize | **THE STANDARD** — 54 rule files (`a-secN-ruleX.Y.md`), `a-categories.md`, `a-dictionary.md`, `extensions/`, `reference-catalogue.md`, `provenance.md`, `README.md` |
| `artifacts/` | F | `_base/` (deterministic boilerplate sub-docs), `level-2/`…`level5/` (LLM-distilled sub-docs), `ste-code-rules.md`, `ste-code-system-prompt.md`, `llms.txt`, `llms-full.txt` |
| `enriched/` | — | Enrichment pass output (109 files) |
| `data/` | — | `synonym-table.json` and the vocabulary data |
| `merged/` | — | `master-raw.md` consolidation |
| `templates/` | — | Prompt templates for each STE-Code register |
| `linguistics/` | — | Research notes, decision tree, generation contract |
| `audit/` | — | Audit reports |
| `_archive/` | — | Superseded output from earlier pipeline versions |

---

## Checkpoints and resume

Every orchestrated stage writes a checkpoint to `.agents/state/` after each
work item and commits the item to git when the gate passes. If the session
stops, restart the stage with `--resume` to skip the completed items.

| Stage | Checkpoint |
|:-----:|------------|
| A | `.agents/state/extraction-checkpoint.json` |
| D | `.agents/state/adapt-checkpoint.json` |
| E | `.agents/state/extend-checkpoint.json` |
| F | `.agents/state/artifact-checkpoint.json` |

---

## Prerequisites

* Python 3 for the deterministic stages (C, F) and for all runners.
* An agent backend for the LLM stages (A, B, D, E). The default backend is
  Hermes. Configure the backends in `.agents/config/agents.yaml`, and list them
  with `python3 .agents/tools/lib/agent-runner.py --list`.
* The Phase E and Phase F runners execute the Hermes virtual environment
  interpreter at `~/.hermes/hermes-agent/venv/bin/python3`. Install Hermes at
  that path, or start the orchestrator modules directly
  (`extend_batch.py`, `artifact_batch.py`) with your own interpreter.
