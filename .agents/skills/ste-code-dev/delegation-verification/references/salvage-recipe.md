# Salvage recipe: rebuild a delegate's report from its scratch, zero API calls

Used when two research delegates died on HTTP 429 (every tool call failed) but
left a scratch JSON behind. The delegate's `status=completed` was a lie — it
wrote no report. The expensive part (scanning 138 files) was already in the
JSON.

## Symptom

- `delegate_task` returns `status=completed` but the named report file does not
  exist.
- `grep -c "429\|rate limit\|524" <live>/task-N.log` > 0.

## Steps

1. Find the delegate scratch dir (cache/delegation/live/<id>/). The agent may
   have written `_scan.json`, `_dup.py`, `_bodies.py` before dying.
2. Inspect the JSON shape with local Python — no network:
    ```python
    import json
    d = json.load(open("<scratch>/_scan.json"))
    print(type(d), list(d.keys()))   # usually {'files': {...}, 'counts': {...}}
    ```
3. Build the report from `counts` (the duplication metrics) and `files`
   (per-file LOC / imports). A focused read of ~10 representative files fills in
   the prose. Write the report to `.agents/tmp/refactor/`, NOT a new top-level
   dir.
4. Run the report-generator as a file under `.agents/tmp/` (the jail rejects
   `python3 - <<'EOF>` heredocs as a write to `/`). Example:
    ```bash
    python3 .agents/tmp/refactor/_report.py
    ```
5. Delete the scratch scripts; keep the two report .md files (gitignored).

## The actual figures salvaged (STE-Code, 138 files)

- 98 files derived their own PROJECT; 83 by hop counting; 1 used repo_root.py.
- 57 files with sys.path bootstrap; 56 bare write_text; 55 re-did mkdir; 51
  hermes invocations; 41 argparse blocks; 25 hand-rolled retry loops.
- Config surface: `tencent/hy3:free` x25, `poolside/laguna-s-2.1:free` x19,
  `utf-8` x67, 97 distinct path constants over 176 sites, 183 argparse defaults
  that are config in disguise.

## Do NOT re-dispatch

Re-running the delegate re-hits the same rate limit. Local analysis of the
salvaged JSON is deterministic and free.
