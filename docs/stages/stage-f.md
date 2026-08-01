# Stage F — Artifacts

**Purpose:** consolidate the adapted rule corpus into the canonical deployable
deliverables. This stage is **deterministic**: it collects and packages, and no
model re-types the content.

| | |
|---|---|
| **Reads** | `ste-code/adapted/` |
| **Writes** | `ste-code/artifacts/ste-code-rules.md`, `ste-code/artifacts/ste-code-system-prompt.md` |
| **Type** | Pure Python, no LLM |
| **Runner** | `.agents/tools/runners/phase-f-run.py` |
| **Orchestrator** | `.agents/tools/artifacts/artifact_batch.py` |
| **Gate** | `.agents/tools/artifacts/verify-artifacts.py` |
| **Checkpoint** | `.agents/state/artifact-checkpoint.json` |

---

## Commands

```bash
# Assemble the artifacts
python3 .agents/tools/runners/phase-f-run.py

# Plan only, write nothing
python3 .agents/tools/runners/phase-f-run.py --dry-run

# Gate only
python3 .agents/tools/runners/phase-f-run.py --verify

# Direct assembler use
python3 .agents/tools/artifacts/artifact_batch.py
python3 .agents/tools/artifacts/artifact_batch.py --dry-run
python3 .agents/tools/artifacts/artifact_batch.py --verify

# Gate on its own
python3 .agents/tools/artifacts/verify-artifacts.py
```

`--agent` and `--model` are accepted and forwarded as informational no-ops. The
runner executes the Hermes virtual environment interpreter at
`~/.hermes/hermes-agent/venv/bin/python3`; to use a different interpreter, call
`artifact_batch.py` directly.

---

## What the assembler does

* Concatenates the adapted rule files in canonical order (`SECTION_ORDER` in
  `artifact_batch.py`): section 1 rules, then section 2, and so on to section 9
  followed by `GR1`–`GR4`.
* Wraps the corpus in an externalized header and footer template, so you can
  change the packaging without changing the Python.
* Verifies rule coverage.

The creative work already happened in Stage D. Stage F only collects, so there
is no truncation risk, and the output is reproducible byte for byte from the
same `adapted/` input.

---

## Level prompts

The five adaptation levels live under `ste-code/artifacts/level1` …
`ste-code/artifacts/level5`. They are assembled by the level scripts in
`.agents/tools/refinement/`, not by `artifact_batch.py`:

```bash
python3 .agents/tools/refinement/assemble-level4.py
python3 .agents/tools/refinement/assemble-level3.py
python3 .agents/tools/refinement/assemble-level2.py
python3 .agents/tools/refinement/assemble-level1.py

# Level 5 summaries
python3 .agents/tools/refinement/populate-level5.py
python3 .agents/tools/refinement/regenerate-level5.py
```

Every assembly script accepts `--agent <name>` to select a backend and
`--dry-run` to preview.

| Script | Input | Output |
|--------|-------|--------|
| `assemble-level1.py` | Level 2 | Level 1 (~1.2K tokens) |
| `assemble-level2.py` | Level 3 | Level 2 (~4.5K tokens) |
| `assemble-level3.py` | Level 5 rule summaries | Level 3 (~8K tokens) |
| `assemble-level4.py` | Level 5 rule summaries | Level 4 (~45K tokens) |
| `assemble-level4-parallel.py` | Level 5 rule summaries | Level 4, parallel build |

---

## Verification gate

`verify-artifacts.py` confirms that the assembled artifacts cover every adapted
rule and that the assembly did not drop or duplicate content. It is
deterministic — no model. Exit code `0` means the gate passes.

Related quality tools:

```bash
python3 .agents/tools/quality/sweep-quality.py --batches 5
python3 .agents/tools/quality/check-rails.py
python3 .agents/tools/quality/check-tables.py
```

---

## Benchmark the result

```bash
python3 .agents/benchmark/orchestrator.py           # STE-Code, 59 tests
python3 .agents/benchmark/orchestrator-control.py   # Plain assistant control group
```

---

## Back to the overview

See the [pipeline overview](../pipeline.md) for the full A→F flow.
