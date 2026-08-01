# Stage A — Extraction

**Purpose:** read the 434 pages of the ASD-STE100 Issue 9 specification and
write them into markdown page-group files.

| | |
|---|---|
| **Reads** | `spec/issue-09-2025/page-dir/` and its `MANIFEST.md` |
| **Writes** | `ste-code/extracted/wNNN-pA-B.md` (109 files) |
| **Type** | LLM workers (4 spec pages per worker) |
| **Runner** | `.agents/tools/runners/phase-a-run.py` |
| **Orchestrator** | `.agents/tools/extraction/extract_batch.py` |
| **Checkpoint** | `.agents/state/extraction-checkpoint.json` |

---

## Commands

```bash
# Single extraction worker through the agent runner
python3 .agents/tools/runners/phase-a-run.py
python3 .agents/tools/runners/phase-a-run.py --agent claude

# Pre-generate enhanced Phase A prompts for a batch range
# (writes .agents/tmp/phase-a-<worker-id>.txt)
python3 .agents/tools/runners/phase-a-gen.py 1 10

# Full batch orchestration (109 workers, 4 pages each)
python3 .agents/tools/extraction/extract_batch.py
python3 .agents/tools/extraction/extract_batch.py 1 5
python3 .agents/tools/extraction/extract_batch.py --resume
```

---

## What the orchestrator does

1. Reads `MANIFEST.md` to map position → (page id, filename).
2. Builds a prompt per worker that names the spec page files to read and the
   combined markdown file to write.
3. Runs the worker through `run_agent()` →
   `.agents/tools/lib/hermes-oneshot-wrapper.py` (no TUI).
4. Verifies the output on disk (size and page headers).
5. Retries up to 2 times when the output file is missing or the worker timed
   out.
6. Commits each passed batch to git.
7. Updates `PROGRESS.md`.
8. Writes the checkpoint after each worker, so `--resume` skips completed work.

Signal handlers for `SIGTERM` and `SIGINT` save the checkpoint before exit.

---

## Key tools

| Tool | Purpose |
|------|---------|
| `.agents/tools/extraction/extract_batch.py` | Batch orchestrator (109 workers) |
| `.agents/tools/extraction/strip-commentary.py` | Removes worker commentary from output |
| `.agents/tools/extraction/test-worker.py` | Single-worker smoke test |
| `.agents/tools/runners/templates/phase-a-worker.md` | Externalized worker prompt |
| `.agents/tools/runners/templates/phase-a-creative-block.md` | Externalized creative-license block |
| `.agents/tools/runners/templates/phase-a-execution-block.md` | Externalized execution block |

Prompt text lives in `templates/`, so you can edit a prompt without changing
the Python.

---

## Verification gate

Extraction is gated inside the orchestrator, not by a separate verifier:

* the output file must exist and be large enough,
* the page headers must be present,
* a failed worker is retried up to 2 times before the batch fails,
* only a passed batch is committed.

Pages per worker are configurable with the `STE_PAGES_PER_WORKER` environment
variable (default `4`).

---

## Next stage

[Stage B — Refinement](stage-b.md) reads `ste-code/extracted/`.
