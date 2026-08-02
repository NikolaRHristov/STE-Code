# STE-Code Methodology & Operations Manual

> **Version:** 1.0 | **Date:** 2026-07-30
> **Purpose:** Complete reference for running, extending, and maintaining the STE-Code pipeline.

---

## 1. Canonical Worker Launching

### The ONLY Correct Pattern

```python
import os
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"

# Write prompt to temp file
tmp = PROJECT / ".agents" / "tmp" / "worker-<id>.txt"
tmp.write_text(prompt_text)

# Fork + exec — the ONLY reliable pattern
pid = os.fork()
if pid == 0:
    os.chdir(str(PROJECT))
    env = os.environ.copy()
    env["HERMES_REASONING_EFFORT"] = "medium"  # or "high"
    from ste_paths import venv_python
    from ste_runtime import resolve as _resolve_rt
    rt = _resolve_rt(__file__)
    os.execvpe(venv_python(), [venv_python(), rt.wrapper, str(tmp),
                "--model", CFG.model], env)
    os._exit(1)
```

### What NEVER to Use

| ❌ Anti-Pattern | Why It Fails |
|----------------|-------------|
| `hermes -z "$(cat file)"` in background | Opens TUI, doesn't process |
| `subprocess.Popen(["hermes", "-z", ...])` | Unreliable stdout capture |
| Custom Python subprocess wrappers calling `hermes -z` | Use oneshot wrapper instead |
| Single worker processing >10 files | Context limits, quality degradation |

### Reasoning Levels

| Level | Use When | Token Cost |
|-------|----------|:----------:|
| `high` | Complex adaptation, creative writing, multi-file assembly | 1.5x |
| `medium` | Fixing gaps, extracting data, simple transformations | 1.0x |
| `low` | Counting, verification, file checks | 0.7x |

---

## 2. Batch Orchestration

### The Pattern (from Phase A/B/C)

```python
# 1. Group work into batches of 3
batches = [items[i:i+3] for i in range(0, len(items), 3)]

# 2. For each batch, launch 3 workers in parallel (fork)
for batch in batches:
    workers = {}
    for item in batch:
        pid = launch_worker(item)  # fork + oneshot
        workers[item.id] = {"pid": pid, "start": time.time()}

    # 3. Wait for all 3
    while pending:
        time.sleep(5)
        for wid in list(pending):
            try:
                wpid, status = os.waitpid(workers[wid]["pid"], os.WNOHANG)
                if wpid != 0: pending.discard(wid)
            except (ChildProcessError, ProcessLookupError):
                pending.discard(wid)

    # 4. Verify output files exist
    for wid, wdata in workers.items():
        ok = output_file.exists() and output_file.stat().st_size > 500

    # 5. Save state, commit
    state["done"].append(wid)
    save_state(state)
```

### State Tracking

Every phase MUST have a state file (`.agents/state/PHASE-<LETTER>-PROGRESS.json`):

```json
{
  "done": ["worker-id-1", "worker-id-2"],
  "batches_done": [1, 2, 3],
  "updated": "2026-07-30T12:00:00Z"
}
```

### Idempotency (from idempotency-baseline.md)

| Tier | Check | When |
|:----:|-------|------|
| 1 | Output file exists + >500B | All workers |
| 2 | Structural validity (headings, entries) | Adaptation, expansion |
| 3 | Content fingerprint (SHA256) | Artifacts, merge |

---

## 3. File Organization

### Active Standard (`ste-code/`)

```
ste-code/
├── adapted/       ★ 51 deepened rules (200-600L each)
├── artifacts/     ★ Deployable outputs (6 files + 8 levels)
├── data/          ★ Structured JSON (vocabulary, synonyms)
├── templates/     ★ System prompts (4 templates + 3 levels)
└── _archive/      Pipeline history (extracted, refined, enriched, merged)
```

### Agent Orchestration (`.agents/`)

```
.agents/
├── agent/         Agent definitions (9 agents)
├── skills/        Capability skills
├── benchmark/     4-mode benchmark suite
├── tools/         Worker launchers, generators, checkers
├── state/         Progress tracking per phase
├── prompts/       Generated worker prompts
├── references/    Rails, grids, checklists, baselines
├── audit/         Audit reports (gitignored)
├── telemetry/     Worker telemetry JSON (gitignored)
├── tmp/           Temp prompt files (gitignored)
└── MASTER.md      Full launch protocol
```

---

## 4. Tool Inventory

### Canonical (use these)

| Tool | Purpose |
|------|---------|
| `hermes-oneshot-wrapper.py` | Launch a single worker (calls AIAgent directly) |
| `telemetry-worker.py` | Tracked worker with JSON telemetry |
| `phase-a-run.py` | Phase A orchestrator (maturity fixes) |
| `phase-b-run.py` | Phase B orchestrator (rule deepening) |
| `phase-c-run.py` | Phase C orchestrator (structured data) |
| `phase-d-run.py` | Phase D orchestrator (artifact regeneration) |
| `phase-f-run.py` | Phase F orchestrator (final audit) |
| `populate-level5.py` | Level 5 summary population |
| `assemble-level4.py` | Level 4 prompt assembly |
| `generate-max-prompt.py` | Level 5 MAX prompt generation |
| `fix-ste-run.py` | STE gap fixer (batched) |
| `check-tables.py` | Table integrity checker |
| `scan-fences.py` | Nested code fence detector |
| `dogfood-audit.py` | STE-Code compliance self-audit |

### Shell Wrappers

| Tool | Purpose |
|------|---------|
| `launch-worker.sh` | Venv detection + oneshot wrapper |
| `telemetry-worker.sh` | Convenience wrapper for telemetry |

---

## 5. Benchmark System

### 4-Mode Comparison

```bash
python3 .agents/benchmark/run.py --compare
```

| Mode | Prompt | Purpose |
|------|--------|---------|
| original | Plain LLM | Baseline |
| sloppy | Intentional sloppiness | Worst case |
| ste-code | Level 5 standard | Best case |
| ste-baseline | Original ASD-STE100 | Reference |

### Scoring

```
score = 0.4 + 0.6*(met/total_principles) - 0.3*(found/total_forbidden) + 0.1*(found/total_expected)
```

Pass threshold: 0.7.

---

## 6. Quality Rules

### Non-Negotiable

1. Every Non-STE example MUST have a complete STE correction
2. Use blank `>` separators between Non-STE and STE in blockquotes
3. Use 4-backtick fences (` ``` `) when showing 3-backtick syntax
4. Never delete existing content — only add
5. Commit after every batch, push every 3 batches
6. Batch size: 3. Never launch more at once

### Pre-Flight (save tokens)

```
Before doing any work:
1. Read the target file from disk
2. If output exists and is valid, SKIP
3. Report "SKIPPED: already complete"
```

---

## 7. Pipeline Stages

```
Stage 1: EXTRACT     109 workers → 434 spec pages → raw markdown     ✅ Complete
Stage 2: REFINE      109 workers → formatted markdown (100.0 audit)  ✅ Complete
Stage 3: MERGE       master.md (23,737 lines)                        ✅ Archived
Stage 4: ADAPT       57 adapted files (aerospace → code)             ✅ Complete
Stage 5: ARTIFACTS    6 deployable files                             ✅ Complete
Phase A: MATURITY    61 workers → agent/skill deepening              ✅ Complete
Phase B: DEEPENING   51 workers → rule expansion (55→432L avg)       ✅ Complete
Phase C: STRUCTURED   6 tasks → vocabulary JSON, templates           ✅ Complete
Phase D: REGEN        6 tasks → artifact regeneration                ✅ Complete
Phase E: TRANSLATE    Skeleton ready, 9 locales                      ⬜ Deferred
Phase F: AUDIT       21/22 checks passed                             ✅ Complete
Level 5: SUMMARIES  51/51 rule summaries populated                  ✅ Complete
Level 4: ASSEMBLY    Assembly script ready, pending execution        🔄 Ready
```

---

## 8. Common Pitfalls & Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Workers open TUI instead of processing | `hermes -z "$(cat file)"` in bg | Use oneshot wrapper with fork+exec |
| Workers delete content | Prompt too permissive | Add "PRESERVE ALL EXISTING CONTENT" + "Only ADD" |
| Empty STE after Non-STE | Phase B blockquote formatting split pairs | Mark with FIXME, fix in targeted batch |
| Level prompt mangled | Single worker processing too many files | Batch into groups of 4 |
| State file stale | Orchestrator crashed mid-batch | Remove current batch from `batches_done`, re-run |

---

## 10. Configuration & Shared Helpers

Every tunable lives in config, never hardcoded. Each `tools/<unit>/` owns a
`config.yaml` (its footprint: inputs, outputs, layout, agent overrides). The
shared `.agents/config/defaults.yaml` supplies `agent:` (model, timeout,
workers) and `runtime:` (retry_attempts, batch_divisor, encoding) knobs merged
underneath, so the unit always wins. Stages read `ste_config.load(__file__)`
for footprint and `ste_runtime.resolve(__file__)` for pre-flight knobs.

All file writes go through `ste_io` (confined to the repo by the jail policy);
the agent runtime path comes from `ste_paths` (`venv_python()`, `wrapper_path()`).
No script declares `VENV_PYTHON` / `WRAPPER` / `open(...,"w")` literals — those
are centralized in the helpers. See `tools/lib/README.md`.

## 9. Quick Reference

```bash
# Run a single worker (model injected from config via ste_config)
python3 .agents/tools/lib/hermes-oneshot-wrapper.py prompt.txt --model "$(python3 -c 'from ste_config import load; print(load(".agents/tools/refinement/refine_batch.py").model)')"

# Run Phase A (maturity fixes)
python3 .agents/tools/runners/phase-a-run.py

# Run Phase B (rule deepening)
python3 .agents/tools/runners/phase-b-run.py

# Run benchmark (all 4 modes)
python3 .agents/benchmark/run.py --compare

# Run final audit
python3 .agents/tools/runners/phase-f-run.py

# Populate Level 5 summaries
python3 .agents/tools/refinement/populate-level5.py

# Assemble Level 4 prompt
python3 .agents/tools/refinement/assemble-level4.py

# Check table integrity
python3 .agents/tools/quality/check-tables.py

# Scan for nested code fences
python3 .agents/tools/maintenance/scan-fences.py

# Self-audit STE-Code compliance
python3 .agents/tools/quality/dogfood-audit.py
```
