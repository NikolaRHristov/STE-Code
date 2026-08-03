# .agents — Agent-Agnostic Pipeline Skills

Role-based, self-contained skills for the STE-Code pipeline. Any agent can read
any prompt or skill and act in that role.

## Structure

```
.agents/
├── AGENTS.md                     ← Full project documentation
├── README.md                     ← This file
├── MASTER.md                     ← Launch protocol + terminology
├── config/                       ← Shared config: defaults.yaml (agent+runtime), agents.yaml
├── agent/                        ← Agent definitions (9 agents)
│   ├── agent-1-extractor.md
│   ├── agent-2-refiner.md
│   ├── agent-3-auditor.md
│   ├── agent-4-continuation.md
│   ├── agent-5-sce-populator.md
│   ├── agent-6-phi-sce.md        ← Paradigm-agnostic analysis agent
│   └── agent-7-level-worker.md   ← Parameterized level worker
├── benchmark/                    ← STE-Code benchmark suite
│   ├── SKILL.md                  ← Benchmark orchestrator prompt
│   ├── schema.json               ← JSON schema for tests/results
│   ├── orchestrator.py           ← STE-Code parallel runner
│   ├── orchestrator-control.py   ← Control group runner
│   ├── run-benchmark.sh          ← Shell runner (legacy)
│   ├── rescore.py                ← Re-scoring utility
│   ├── test-cases/               ← 14 category files, 59 tests
│   ├── results/                  ← STE-Code benchmark results
│   ├── results-control/          ← Control group results
│   └── examples/                 ← Generated code examples
├── prompts/                      ← Role-based agent prompts
│   ├── extractor.md
│   ├── refiner.md
│   ├── auditor.md
│   ├── continuator.md
│   ├── sce-populator.md
│   ├── adapt/                    ← Adaptation phase prompts
│   ├── enrich/                   ← Enrichment phase prompts
│   ├── refine/                   ← Refinement batch prompts
│   └── oss/                      ← Open-source doc prompts
├── skills/                       ← Capability skills
│   ├── extraction/SKILL.md
│   ├── refinement/SKILL.md
│   ├── auditing/SKILL.md
│   ├── grouping/SKILL.md
│   ├── adaptation/SKILL.md
│   ├── artifacts/SKILL.md
│   ├── benchmarking/SKILL.md
│   ├── validation/SKILL.md
│   ├── continuation/             ← Multi-file continuation orchestrator
│   ├── execution-auditor/        ← Hidden state-report auditor
│   ├── state-report/             ← State report format standard
│   └── extension-worker/         ← Extension worker skill
├── references/                   ← Shared reference data (shared across skills + agents)
│   ├── worker-grid.md
│   ├── section-types.md
│   ├── quality-checklist.md
│   ├── rails.md
│   ├── category-mapping.md
│   └── STE-CODE-IMPLEMENTATION.md
├── uml/                          ← Pipeline diagrams
├── state/                        ← Progress tracking
├── audit/                        ← Auditor reports
├── tools/                        ← Orchestration scripts (hermes agents, quality checks)
│   ├── lib/                      # Core infrastructure + shared helpers (ste_io, ste_config, ste_runtime, …)
│   ├── shared/                   # Shared utilities
│   ├── runners/                  # Pipeline phase runners (phase-a..f-run.py + templates/)
│   ├── extraction/               # Spec page extraction (extract_batch.py + test-worker.py)
│   ├── refinement/               # Refinement orchestration (refine_batch.py + gates)
│   ├── grouping/                 # Deterministic grouping (group_batch + verify)
│   ├── adaptation/               # STE→STE-Code adaptation (adapt_batch + verify-adaptation)
│   ├── extension/                # Gap-fill extensions (extend_batch + md_to_json + verify)
│   ├── continuation/             # B1 redo/continuation (continue_batch + verify-continuation)
│   ├── artifacts/                # Final artifact assembly (artifact_batch + verify-artifacts)
│   ├── maintenance/              # Content fixes and gap filling
│   ├── quality/                  # Quality auditing and verification
│   ├── benchmark/                # Benchmark execution
│   └── linkcheck/                # Link checker
└── feedback/                     ← Inter-agent communication
```

## Configuration (one source of truth)

All tunables live in config, never hardcoded in scripts. Each `tools/<unit>/`
owns a `config.yaml` declaring its footprint (inputs, outputs, layout, agent
overrides); `.agents/config/defaults.yaml` supplies shared `agent:` (model,
timeout, workers) and `runtime:` (retry_attempts, batch_divisor, encoding) knobs
merged underneath. Stages read `ste_config.load(__file__)` for footprint and
`ste_runtime.resolve(__file__)` for pre-flight knobs.

## Shared helpers (tools/lib/)

The single source for cross-cutting behaviour — no unit re-implements these:
`ste_io` (the only gated write path), `ste_config` (config resolution),
`ste_runtime` (pre-flight runtime knobs), `ste_checkpoint` (atomic resume),
`ste_paths` / `ste_time` / `ste_retry` / `ste_cli` (path, timestamp, retry,
argparse helpers). See `tools/lib/README.md`.

## Pipeline (standardized stages)

Every stage shares one discipline: **orchestrated workers** (background, <=3
concurrent, checkpoint, `--resume`, per-chunk git commit) **+ a deterministic
gate** that blocks bad output **+ externalized prompts** (`templates/*.md` via
`lib/templater.py`) **+ tests**. Workers emit **markdown only**; JSON (where
needed, e.g. extensions) is derived deterministically — never generated by a
worker (that was an RCE-artifact remnant).

| Stage       | Runner            | Orchestrator                     | Gate / Verify                 | Output                     |
| ----------- | ----------------- | -------------------------------- | ----------------------------- | -------------------------- |
| A Extract   | `phase-a-run.py`  | `extraction/extract_batch.py`    | `verify_output`               | `ste-code/extracted/`      |
| B Refine    | (agent)           | `refinement/refine_batch.py`     | SKILL gates                   | `ste-code/refined/`        |
| B1 Continue | `phase-b1-run.py` | `continuation/continue_batch.py` | `verify-continuation` (queue) | `ste-code/refined/` (redo) |
| C Group     | `phase-c-run.py`  | `grouping/group_batch.py`        | `verify-groups.py`            | `ste-code/grouped/`        |
| D Adapt     | `phase-d-run.py`  | `adaptation/adapt_batch.py`      | `verify-adaptation.py`        | `ste-code/adapted/`        |
| E Extend    | `phase-e-run.py`  | `extension/extend_batch.py`      | `verify-extensions.py`        | `ste-code/extensions/`     |
| F Artifacts | `phase-f-run.py`  | `artifacts/artifact_batch.py`    | `verify-artifacts.py`         | `ste-code/artifacts/`      |

Run order: **A -> B -> (B1 if needed) -> C -> D -> E -> F**. Each stage's runner
refuses to launch until its input directory is ready (grouping needs
`ste-code/refined/`; adaptation needs `ste-code/grouped/`).

## Quick Reference

| Task                      | Command                                                               |
| ------------------------- | --------------------------------------------------------------------- |
| Run STE-Code benchmark    | `python3 .agents/benchmark/orchestrator.py`                           |
| Re-score existing outputs | `python3 .agents/benchmark/rescore.py`                                |
| Group refined pages       | `python3 .agents/tools/runners/phase-c-run.py --verify`               |
| Adapt (STE->STE-Code)     | `python3 .agents/tools/runners/phase-d-run.py`                        |
| Extend (gap-fills)        | `python3 .agents/tools/runners/phase-e-run.py`                        |
| Assemble artifacts        | `python3 .agents/tools/runners/phase-f-run.py`                        |
| Continue/redo refined     | `python3 .agents/tools/runners/phase-b1-run.py --scan` then `--queue` |

## Adaptation Levels

| Level | Content                              | Size   | Tokens |
| ----- | ------------------------------------ | ------ | ------ |
| -2    | 14 core principles only              | 5 KB   | ~1.2K  |
| -1    | + synonym table                      | 26 KB  | ~5.9K  |
| 0     | + short dictionary excerpt           | 17 KB  | ~4.3K  |
| 1     | + doc templates                      | 58 KB  | ~14.5K |
| 2     | + section-specific grammar           | 75 KB  | ~18.5K |
| 3     | + complete dictionary + all 54 rules | 388 KB | ~95K   |
| 4     | + extensions + reference catalogue   | 462 KB | ~116K  |
| 5     | Full standard + provenance           | 539 KB | ~134K  |

Measured, not estimated. Regenerate with
`python3 .agents/tools/maintenance/measure_artifacts.py` (o200k_base tokenizer).

## Benchmark Results

**STE-Code: 96.6% pass rate (57/59)** vs Plain Assistant: 11.9% (7/59). +84.7%
improvement.

## See also

- `AGENTS.md` — agent backends, stage detail, skills inventory.
- `MASTER.md` — launch protocol.
- `tools/lib/README.md` — shared helper reference.
- `config/defaults.yaml` — shared defaults.
