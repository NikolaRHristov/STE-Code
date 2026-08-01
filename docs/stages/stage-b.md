# Stage B — Refinement

**Purpose:** reformat the raw extraction into clean, standardized markdown —
structured dictionary tables and rule pages — with no content loss.

| | |
|---|---|
| **Reads** | `ste-code/extracted/*.md` (109 files) |
| **Writes** | `ste-code/refined/rNNN-pA-B.md` (109 files) |
| **Type** | LLM workers, 37 batches launched in parallel |
| **Runners** | `.agents/tools/runners/phase-b-run.py`, `.agents/tools/runners/phase-b1-run.py` |
| **Orchestrators** | `.agents/tools/refinement/refine_batch.py`, `.agents/tools/continuation/continue_batch.py` |

---

## Commands

```bash
# Single refinement worker (batch number is optional, default 1)
python3 .agents/tools/runners/phase-b-run.py
python3 .agents/tools/runners/phase-b-run.py 12
python3 .agents/tools/runners/phase-b-run.py --agent claude

# Full batch orchestration (37 batches)
python3 .agents/tools/refinement/refine_batch.py
python3 .agents/tools/refinement/refine_batch.py 1 37
python3 .agents/tools/refinement/refine_batch.py --resume
STE_MODEL=tencent/hy3:free python3 .agents/tools/refinement/refine_batch.py
```

Each batch runs as its own background process, so many workers process files at
the same time.

---

## Stage B1 — continuation and redo

Stage B1 re-processes specific refined pages that failed or came back
incomplete. It writes into `ste-code/refined/`, which the refinement agent also
owns, so it needs an explicit queue and must not run while refinement is
active.

```bash
# Scan for incomplete pages (runs verify_continuation.py)
python3 .agents/tools/runners/phase-b1-run.py --scan

# Re-process the pages in an explicit queue file
python3 .agents/tools/runners/phase-b1-run.py --queue Q.json
python3 .agents/tools/runners/phase-b1-run.py --queue Q.json --resume
```

With no arguments, `phase-b1-run.py` prints its usage, because a queue is
mandatory. The queue file is produced by
`.agents/tools/continuation/verify_continuation.py`.

---

## Key tools

| Tool | Purpose |
|------|---------|
| `.agents/tools/refinement/refine_batch.py` | Parallel batch orchestrator |
| `.agents/tools/refinement/generate_refine_prompts.py` | Builds refinement worker prompts |
| `.agents/tools/continuation/continue_batch.py` | Re-processes queued pages with a checkpoint and per-item commit |
| `.agents/tools/continuation/verify_continuation.py` | Finds incomplete pages and writes the queue |
| `.agents/tools/quality/check-tables.py` | Table integrity check |
| `.agents/tools/quality/check-rails.py` | 8-rail quality compliance check |
| `.agents/tools/runners/templates/phase-b-worker.md` | Externalized worker prompt |

---

## Verification gate

* Each batch is measured against the extracted source with a normalized word
  count, so formatting changes do not count as content changes.
* A batch is committed to git only after the gate passes.
* `verify_continuation.py` finds pages that are still short or malformed, and
  Stage B1 re-processes them.

---

## Next stage

[Stage C — Grouping](stage-c.md) reads `ste-code/refined/`.
