# Contributing

The full contribution policy is in
[`CONTRIBUTING.md`](https://github.com/NikolaRHristov/STE-Code/blob/Current/CONTRIBUTING.md)
in the repository root. It is the one canonical file. Read it before you open a
pull request. This page summarizes how to run the pipeline on your machine.

| Section in `CONTRIBUTING.md` | Contents |
|------------------------------|----------|
| Before you start | `make check` and every other `make` target |
| Development setup | Prerequisites, backends, and the clone step |
| Ways to contribute | Synonyms, categories, rule changes, examples, bug reports |
| Where the content lives | Which directory holds what, and which directories are generated |
| Run the pipeline locally | Dry-run commands and the stage gates |
| Testing | The 8 rails, table integrity, and the link check |
| Documentation | The STE-Code writing rules this project applies to itself |
| Pull requests | Branch names, Conventional Commits, and the merge checklist |

---

## Ways to contribute

| Contribution | What to supply |
|--------------|----------------|
| New synonym | The unapproved term, the approved replacement, the domain, the reason it is ambiguous, and 3 real examples from public documentation |
| New category | The category name, 5 example nouns, a counterexample, and why the existing 22 categories do not cover it |
| Rule improvement | A before/after example pair, and a migration plan that keeps the output idempotent |
| Real-world example | The original text, your STE-Code rewrite, and a short metrics table |
| Domain example | A Non-STE / STE pair for a domain tag from `.agents/GAPS.md` |
| Bug report | The file, the line number, the expected behavior, and the actual behavior |

We do not accept speculative proposals. A new synonym needs a proven
counterexample from real documentation.

Domain example pairs use this format in the matching rule file in
`ste-code/adapted/`:

```markdown
> [DOMAIN: mobile]
> **Non-STE:** [real code documentation from the domain]
> **STE:** [the STE-Code compliant correction]
```

Put the domain tag in the commit message.

---

## Prerequisites

| Requirement | Needed for |
|-------------|------------|
| Python 3 | Every runner, every gate, and the deterministic stages |
| An agent backend | The stages that call a model |

The default backend is Hermes. Configure the backends in
`.agents/config/agents.yaml` and list them with:

```bash
python3 .agents/tools/lib/agent-runner.py --list
```

The extension and artifact runners call
`~/.hermes/hermes-agent/venv/bin/python3`. If Hermes is not at that path, start
`extend_batch.py` or `artifact_batch.py` directly with your own interpreter.

The model is read from the `STE_MODEL` environment variable. The default is
`tencent/hy3:free`.

---

## Run the pipeline locally

The deterministic stages are safe on a clean checkout. The model stages cost
tokens and rewrite tracked content, so run them only when you intend to
regenerate that layer.

```bash
# Merge — plan only, writes nothing
python3 .agents/tools/runners/phase-c-run.py --dry-run

# Merge — assemble and gate
python3 .agents/tools/runners/phase-c-run.py --verify

# Artifacts — plan only
python3 .agents/tools/runners/phase-f-run.py --dry-run
```

To run the whole downstream chain:

```bash
bash .agents/tools/runners/launch-downstream.sh
bash .agents/tools/runners/launch-downstream.sh --dry   # plan only
```

The script stops before the Merge stage when `ste-code/refined/` holds fewer
than 100 markdown files, because that means refinement is still running.

See the [pipeline overview](pipeline.md) for the stage table and the runner of
each stage.

---

## Run the gates before you push

Every stage has a deterministic gate. Run the gate for the layer you changed.
Exit code `0` means the gate passes.

```bash
python3 .agents/tools/grouping/verify-groups.py         # Merge
python3 .agents/tools/adaptation/verify-adaptation.py   # Adaptation
python3 .agents/tools/extension/verify_extensions.py    # Extensions
python3 .agents/tools/artifacts/verify-artifacts.py     # Artifacts
```

Quality checks that apply to any markdown layer:

```bash
python3 .agents/tools/quality/check-rails.py       # the 8 rails
python3 .agents/tools/quality/check-tables.py      # table integrity
python3 .agents/tools/quality/sweep-quality.py --batches 5
bash .agents/tools/linkcheck/run_linkcheck.sh      # lychee link check
```

The canonical repository gate is:

```bash
make check
```

---

## Build the documentation site

```bash
pip install mkdocs
mkdocs serve            # preview at http://127.0.0.1:8000
mkdocs build --strict   # writes ./site/, fails on a broken link or a warning
```

`mkdocs.yml` is in the repository root and the pages are in `docs/`. See
[`docs/README.md`](https://github.com/NikolaRHristov/STE-Code/blob/Current/docs/README.md)
for the site layout and how to add a page.

---

## Code of conduct

This project uses the
[Code of Conduct](https://github.com/NikolaRHristov/STE-Code/blob/Current/CODE_OF_CONDUCT.md)
in the repository root.
