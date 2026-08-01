# Contributing

The full contribution policy is in
[`CONTRIBUTING.md`](https://github.com/NikolaRHristov/STE-Code/blob/Current/CONTRIBUTING.md)
in the repository root. Read it before you open a pull request. This page
summarizes how to run the pipeline on your machine.

---

## Ways to contribute

| Contribution | What to supply |
|--------------|----------------|
| New synonym | The unapproved term, the approved replacement, the domain, the justification, and at least 3 real-world examples |
| New category | The category name, at least 5 example nouns, a counterexample, and why the existing categories do not cover it |
| Rule improvement | A before/after example pair and a migration plan that keeps the output idempotent |
| Real-world example | The original text, your STE-Code rewrite, and a short metrics table |
| Pipeline bug | The file, the line number, the expected behavior, and the actual behavior |
| Domain examples | Non-STE / STE example pairs for a domain tag from `.agents/GAPS.md` |

Domain example pairs use this format in `ste-code/adapted/a-secN-ruleX.Y.md`:

```markdown
> [DOMAIN: mobile]
> **Non-STE:** [realistic code documentation from the domain]
> **STE:** [STE-Code compliant correction]
```

Put the domain tag in the commit message.

---

## Prerequisites

* Python 3.
* An agent backend for the stages that use a model (A, B, D, E). The default
  backend is Hermes. Backends are configured in `.agents/config/agents.yaml`.

```bash
# List the configured agent backends
python3 .agents/tools/lib/agent-runner.py --list
```

* The Stage E and Stage F runners execute
  `~/.hermes/hermes-agent/venv/bin/python3`. If you do not have Hermes at that
  path, call `extend_batch.py` and `artifact_batch.py` directly with your own
  interpreter.
* The model is read from `STE_MODEL` (default `tencent/hy3:free`).

---

## Run the pipeline locally

The deterministic stages (C and F) are safe to run on a clean checkout. The
model stages (A, B, D, E) cost tokens and rewrite tracked content, so run them
only when you intend to regenerate that layer.

```bash
# Stage C — grouping: plan only, writes nothing
python3 .agents/tools/runners/phase-c-run.py --dry-run

# Stage C — assemble and gate
python3 .agents/tools/runners/phase-c-run.py --verify

# Stage F — assemble the deliverables, plan only
python3 .agents/tools/runners/phase-f-run.py --dry-run
```

To run the whole downstream chain C→D→E→F:

```bash
bash .agents/tools/runners/launch-downstream.sh
bash .agents/tools/runners/launch-downstream.sh --dry   # grouping dry-run only
```

The script stops before Stage C when `ste-code/refined/` has fewer than 100
markdown files.

See the [pipeline overview](pipeline.md) and the stage pages
([A](stages/stage-a.md), [B](stages/stage-b.md), [C](stages/stage-c.md),
[D](stages/stage-d.md), [E](stages/stage-e.md), [F](stages/stage-f.md)) for the
command reference of each stage.

---

## Run the gates before you push

Every stage has a deterministic gate. Run the gate for the layer you changed:

```bash
python3 .agents/tools/grouping/verify-groups.py         # Stage C
python3 .agents/tools/adaptation/verify-adaptation.py   # Stage D
python3 .agents/tools/extension/verify_extensions.py    # Stage E
python3 .agents/tools/artifacts/verify-artifacts.py     # Stage F
```

Quality checks that apply to any markdown layer:

```bash
python3 .agents/tools/quality/check-rails.py
python3 .agents/tools/quality/check-tables.py
python3 .agents/tools/quality/sweep-quality.py --batches 5
```

Exit code `0` means the gate passes.

---

## Build the documentation site

```bash
pip install mkdocs
mkdocs serve     # preview at http://127.0.0.1:8000
mkdocs build --strict
```

`mkdocs.yml` is in the repository root and the pages are in `docs/`. See
[`docs/README.md`](https://github.com/NikolaRHristov/STE-Code/blob/Current/docs/README.md)
for details.

---

## Code of conduct

This project uses the
[Code of Conduct](https://github.com/NikolaRHristov/STE-Code/blob/Current/CODE_OF_CONDUCT.md)
in the repository root.
