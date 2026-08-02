# Delegate hits HTTP 429 — salvage and finish locally

## Symptom

A `delegate_task` batch returns with each task `status=completed`, but the task
summary text is an HTTP 429 payload and the deliverable file was never written:

```
API call failed after 3 retries: HTTP 429: Hold up for a bit, you've exceeded
the rate limit on your API key.
```

`completed` means the loop ended, NOT that the goal was met. Re-launching more
delegates just hits the same limit.

## What to do instead (zero API calls)

1. **Confirm nothing was produced.** `ls` the delegate's scratch path / the
   report path it was told to write. If the file is absent, the delegate did
   nothing useful.

2. **Adopt the delegate's raw scan data if it exists.** Even a killed delegate
   often leaves intermediate artifacts. During the real refactor, the dead
   delegate had written `.agents/tmp/refactor/_scan.json` — a per-file dump of
   LOC, docstrings, imports, and 20 duplication counters. That was the expensive
   part; the analysis on top of it needs no model.

3. **Finish the work with deterministic local Python.** Static scans, `grep`
   sweeps, regex substitution, and report generation are pure computation.
   - Inventory + duplication ranking: `execute_code` over the file tree.
   - Config surface: regex over `os.environ.get("STE_MODEL", "...")`,
     `Path(__file__).resolve().parent…`, glob patterns, argparse defaults.
   - Reports: `write_file` the markdown; verify with `python3` not a model.

4. **Report honestly.** State that the delegate failed on rate limits and that
   you completed the analysis locally from its salvaged data.

## Why this pattern matters here

The STE-Code repo runs several concurrent Hermes sessions on one Nous key.
HTTP 429 is common and transient. A delegate that dies on it leaves `completed`
but empty — trusting that flag loses the work. The salvage path recovers it
without burning more quota.
