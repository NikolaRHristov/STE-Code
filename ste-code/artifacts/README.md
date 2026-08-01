# STE-Code Artifacts

Ready-to-use, LLM-friendly packaging of the STE-Code standard (ASD-STE100
Issue 9, January 2025, adapted to software documentation). The canonical
source is [`../final/`](../final/) — this directory holds the **deployable
deliverables**, built by the hybrid Phase F pipeline (deterministic base +
LLM distillation).

> Adapted from ASD-STE100 Issue 9 (January 2025), ASD Europe. (c) ASD, 2025.
> STE is an EU Trade Mark. Independent adaptation.

## Layout

Each adaptation **level is a directory of small sub-documents** (so an LLM reads
and writes files of a few hundred KB at most, never one 1.8 MB monster):

| Level | Directory | Approx. size | Purpose |
|:-----:|-----------|:------------:|---------|
| **-2** | [`level-2/`](level-2/) | ~5 KB | Ultra-minimal: the 14 core principles only |
| **-1** | [`level-1/`](level-1/) | ~12 KB | Minimal: core principles + synonym table |
| **0** | [`level0/`](level0/) | ~25 KB | Baseline: + short dictionary excerpt |
| **1** | [`level1/`](level1/) | ~35 KB | + doc templates (code review / PR feedback) |
| **2** | [`level2/`](level2/) | ~45 KB | + section-specific grammar rules |
| **3** | [`level3/`](level3/) | ~1.8 MB | + complete dictionary + all 54 rules |
| **4** | [`level4/`](level4/) | ~1.8 MB | + extensions + reference catalogue |
| **5** | [`level5/`](level5/) | ~1.8 MB | Full standard (all rules + extensions + catalogue + provenance) |

Supporting files:

| File | Purpose |
|------|---------|
| `_base/` | Deterministic boilerplate sub-docs per tier (the layer the LLM distills from). Byte-reproducible; no LLM. |
| `llms.txt` | `llms.txt`-style index of every tier and its sub-documents (for agentic retrieval). |
| `llms-full.txt` | Concatenation of every distilled sub-document — the single-file full corpus. |
| `VERSION` | Artifact version (bumped on each regeneration). |
| `README.md` | This file. |

> The previous flat `ste-code-rules.md` / `ste-code-system-prompt.md` consolidated
> files are **no longer produced**; `llms-full.txt` is the consolidated artifact.

## How it was built (Phase F, hybrid)

1. **Deterministic level separation** — `levels_scaffold.py` reads `../final/`
   and emits bounded sub-documents per tier into `_base/`. Oversized rule
   sections are split (`rules-secN-part{i}.md`) so no sub-doc exceeds ~450 KB.
2. **LLM distillation** — `distill_one.py` runs one Hermes session per
   sub-document, reading its base and rewriting it into an LLM-optimized file
   at `level<N>/<subdoc>` (multiple `write_file` / `patch` calls). On failure it
   falls back to the base, so nothing is lost. Each worker commits its sub-doc
   turn-by-turn.
3. **Index assembly** — `llms.txt` (index) and `llms-full.txt` (concatenation)
   are written deterministically after all sub-docs are distilled.

## Quick start

1. Pick a level directory that fits your token budget.
2. Load its `_index.md` (or `llms.txt`) so the LLM knows the sub-doc layout.
3. Point the LLM at the relevant sub-document(s) when it needs a rule, the
   dictionary, or an example. For a single-file load, use `llms-full.txt`.

## Tooling

All scripts are agent-agnostic, in `.agents/tools/artifacts/`:

```bash
python3 .agents/tools/artifacts/levels_scaffold.py     # rebuild _base/ boilerplate
python3 .agents/tools/artifacts/distill_one.py <tier> <subdoc> <label> <desc>   # distill one sub-doc
python3 .agents/tools/artifacts/artifact_batch.py      # assemble consolidated artifacts
python3 .agents/tools/artifacts/verify-artifacts.py    # coverage gate (54/54 from final/)
```

The worker prompt lives at `.agents/tools/prompts/synthesize-artifacts-worker.md`
and is rendered with `templater.py` (double-brace `{{token}}` syntax).
