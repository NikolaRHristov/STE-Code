# STE-Code Agent Tools

## Purpose

`.agents/tools/` holds every orchestration script in the STE-Code pipeline, grouped
into one directory per pipeline unit. A unit owns its scripts, its `config.yaml`
footprint, its `templates/` prompt text and its verification gate. Pipeline
operators read this file to find the right entrypoint; contributors read it to learn
where a new script belongs.

## Footprint

`.agents/tools/` has no `config.yaml` of its own. Each unit declares its complete
footprint in `<unit>/config.yaml`, and the loader `lib/ste_config.py` resolves it
against the shared `.agents/config/defaults.yaml`.

- Reads: `.agents/config/defaults.yaml`, `.agents/config/agents.yaml`,
  `<unit>/config.yaml`, `<unit>/templates/*.md`, `.agents/skills/*/SKILL.md`.
- Writes: the `outputs:` paths declared by the unit that runs, plus `.agents/state`
  for checkpoints. Every write passes through `lib/ste_io.py`, which confines the
  target to the repo root.

## Usage

    python3 .agents/tools/<unit>/<script>.py [--dry-run] [--resume]

Pipeline phases run through the runners:

    python3 .agents/tools/runners/phase-a-run.py     # A  extraction
    python3 .agents/tools/runners/phase-b-run.py     # B  refinement
    python3 .agents/tools/runners/phase-b1-run.py --queue Q.json
    python3 .agents/tools/runners/phase-c-run.py     # C  grouping
    python3 .agents/tools/runners/phase-d-run.py     # D  adaptation
    python3 .agents/tools/runners/phase-e-run.py     # E  extension
    python3 .agents/tools/runners/phase-f-run.py     # F  artifacts
    python3 .agents/tools/runners/phase-g-run.py     # G  finalize
    .agents/tools/runners/launch-downstream.sh       # C -> D -> E -> F

## Behaviour

- Each unit directory pairs a batch orchestrator with a deterministic verify gate
  (`verify-*.py` / `verify_*.py`); the gate decides whether a stage counts as done.
- Orchestrators resolve settings from `config.yaml` through `ste_config.load()`,
  never from literals in the script body.
- Worker prompt text lives in `<unit>/templates/*.md` and is rendered by
  `lib/templater.py`; scripts hold control flow only.
- Sub-agents do not inherit the profile's skills, so `lib/skill_prompt.py` embeds the
  governing `SKILL.md` into the worker prompt.
- Long stages checkpoint through `lib/ste_checkpoint.py` and resume with `--resume`.
- Retries and backoff come from `lib/ste_retry.py` driven by the `runtime:` keys.

## Directory map

| Directory | Role |
|---|---|
| `lib/` | Shared infrastructure: config, IO, paths, retry, templater, checkpoint |
| `shared/` | Agent launchers and telemetry wrappers |
| `runners/` | Phase runners A-G plus `launch-downstream.sh` |
| `extraction/` | Stage A — spec page extraction |
| `refinement/` | Stage B — page refinement and level assembly |
| `continuation/` | Stage B1 — redo queue for incomplete refined pages |
| `grouping/` | Stage C — deterministic grouping, no model call |
| `adaptation/` | Stage D — STE to STE-Code adaptation |
| `extension/` | Stage E — gap-fill extensions |
| `artifacts/` | Stage F — artifact assembly and distillation |
| `finalize/` | Stage G — final enrichment and assembly |
| `maintenance/` | Content fixes, gap filling, artifact measurement |
| `quality/` | Rails, tables, grounding and sweep auditing |
| `benchmark/` | Lightweight benchmark runner |
| `linkcheck/` | Lychee link checking and reports |
| `release/` | Release facts, changelog, scan and sync |
| `trajectory/` | Trajectory worker orchestration |
| `prompts/` | Cross-unit worker prompts loaded by absolute path |

Top-level scripts: `audit_overlap.py`, `audit_overlap_strict.py`, `git-sync.py`.

## Configuration

- `agent.model`, `agent.name`, `agent.timeout_s`, `agent.workers_per_batch`,
  `agent.retries`, `agent.backoff_s` — declared in `.agents/config/defaults.yaml`
  and overridable per unit in `<unit>/config.yaml`. The unit always wins.
- `runtime.retry_attempts`, `runtime.backoff_base_s`, `runtime.batch_divisor`,
  `runtime.encoding` — pre-flight knobs read by `lib/ste_runtime.py`.
- `inputs:`, `outputs:`, `layout:`, `format:`, `thresholds:` — unit-local, declared
  only in `<unit>/config.yaml`.
- Knobs live only in config. A model name, path or threshold hardcoded in a `.py`
  is a defect.
- The interpreter path comes from `ste_paths.venv_python()` and the oneshot wrapper
  from `ste_paths.wrapper_path()`; neither is written as a literal.
- `.env.example` documents legacy `STE_*` environment overrides that a few
  orchestrators still honour. Prefer `config.yaml`; the env vars are a fallback.

## Failure modes

- **HTTP 429** — the free tier rejects more than three concurrent workers. Keep
  `agent.workers_per_batch` at 3; `ste_retry` backs off and retries
  `runtime.retry_attempts` times before the batch fails.
- **Timeout** — a worker exceeding `agent.timeout_s` is killed and retried. The
  oneshot wrapper self-terminates when the API stops responding.
- **Partial writes** — `ste_io.write_text` confines every write to the repo root and
  refuses paths outside it. A stage killed mid-batch leaves completed items on disk;
  rerun with `--resume` to continue from the checkpoint in `.agents/state`.
- **Gate failure** — a verify script exiting non-zero means the stage did not
  produce valid output. Do not advance to the next phase.
- **Concurrent writers** — B1 writes into `ste-code/refined/`, which refinement also
  owns. Run B1 only with an explicit `--queue` and never alongside refinement.
- **Commit sweeps** — a repo-wide commit made while another session is working can
  pick up unrelated files. Stage explicit paths rather than committing everything.

## See also

- [lib/PROMPTS.md](lib/PROMPTS.md) — canonical prompt organization system
- [TEMPLATES.md](TEMPLATES.md) — pointer to the same system
- [../config/defaults.yaml](../config/defaults.yaml) — shared agent defaults
- [../AGENTS.md](../AGENTS.md) — pipeline overview and agent roles
