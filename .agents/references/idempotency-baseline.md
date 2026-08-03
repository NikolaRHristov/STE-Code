# Worker Idempotency Baseline

> **Version:** 1.0 | **Date:** 2026-07-30 **Purpose:** Every worker must check
> before regenerating. No wasted tokens.

## Rule

**A worker SHALL NOT regenerate output that already exists and is valid.**

## Three Tiers

### Tier 1 — File Existence (minimum)

Check if output file exists and is above minimum size threshold. Skip if yes.

```
if output_file.exists() and output_file.size > 500:
    skip("Output already exists")
```

**Applies to:** All extraction, refinement, maturity-fix workers.

### Tier 2 — Structural Validity

Check file existence + parse structural elements (headings, table rows,
dictionary entries). Skip if counts match expected minimums.

```
if output_file.exists():
    content = read(output_file)
    if count_headings(content) >= expected_min_headings:
        skip("Output valid")
```

**Applies to:** Adaptation, expansion, SCE population workers.

### Tier 3 — Content Fingerprint

Check file existence + hash content fingerprint. Skip if fingerprint matches
last-known-good. Re-run only if source inputs changed.

```
if output_file.exists():
    current_hash = sha256(output_file)
    if current_hash == state["last_hash"]:
        skip("Content unchanged")
```

**Applies to:** Artifact generation, merge workers.

## Implementation Pattern

Every worker prompt MUST include:

```
## PRE-FLIGHT CHECK

Before writing any output:
1. Check if the target file exists
2. If it exists, verify it has valid content (not empty, not truncated)
3. If valid, SKIP this worker — report "SKIPPED: output already valid"
4. Only regenerate if output is MISSING, EMPTY, or INVALID

This saves tokens. Do NOT regenerate valid existing content.
```

## Orchestrator State Tracking

Every orchestrator MUST:

1. Load `{phase}-state.json` before launching workers
2. Skip workers whose IDs are in `state["done"]`
3. After each worker completes, append to `state["done"]`
4. Save state after each batch

## Granular Commit Protocol

After each batch completes:

1. `git add <batch-target-dir>/`
2. `git commit -m "phase:<letter> batch:<N> — <files-summary>"`
3. Push every 3 batches

Do NOT commit all files at once. Commit per directory category.
