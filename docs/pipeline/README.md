# Pipeline

The STE-Code pipeline transforms the ASD-STE100 aerospace specification into
code-domain documentation rules through 5 stages.

## Architecture

```
ASD-STE100 Issue 9 (434 pages)
        │
        ▼
Stage 1: EXTRACTION   →  ste-code/extracted/  (109 files, 912K)
        │                  109 parallel workers, 4 pages each
        ▼
Stage 2: REFINEMENT    →  ste-code/refined/    (109 files, 1.0M)
        │                  9 formatting rules, zero content loss
        ▼
Stage 3: MERGE         →  ste-code/merged/     (master.md, 20,794 lines)
        │                  Concatenate, deduplicate, organize
        ▼
Stage 4: ADAPTATION    →  ste-code/adapted/    (57 files, 604K)
        │                  53 rules + 4 GR adapted for code domain
        ▼
Stage 5: ARTIFACTS     →  ste-code/artifacts/  (6 files, 28K)
                           System prompts, manuals, deployment guides
        │
        ▼
      SCE/              →  Product directory (29 files)
                           Rules, vocabulary, synonyms, schemas
```

## Workers

Every stage uses the same worker pattern:

```bash
python3 .agents/tools/telemetry-worker.py <worker-id> <prompt-file> --output <output-file>
```

**Rules:**
- Batch size: 3 workers maximum
- Launch: `background=true`, `notify_on_complete=true`
- Model: `deepseek-v4-pro` with `reasoning: high`
- Verify output after every batch before committing
- Track progress in `FINAL-PASS-TRACKER.md`

## Worker Lifecycle

```
WRITE prompt → LAUNCH 3 workers (bg + notify) → WAIT for all 3
  → VERIFY: file exists, size > 0, valid content
  → COMMIT: git gcommit-hermes
  → UPDATE tracker: flip [ ] → [x]
  → NEXT batch
```

## Self-Healing

Every worker validates its output before writing:
1. Check if output already exists with valid content → SKIP
2. Validate JSON schema if applicable
3. Check for blacklisted terms (aerospace leakage)
4. Verify cross-references exist on disk
5. Write `RECOVERY-NEEDED/<id>.md` on failure

## Telemetry

Every worker leaves a telemetry record at `.agents/telemetry/<worker-id>-<timestamp>.json`:

```json
{
  "worker_id": "b1-004",
  "duration_seconds": 77.0,
  "exit_code": 0,
  "output_size_bytes": 3918,
  "output_valid_json": true,
  "output_entry_count": 5,
  "self_healing": {
    "aerospace_terms_found": 0,
    "status": "PASS"
  }
}
```

## Self-Audit

After each pipeline stage completes, launch a review worker:
```
Quality review: audit all output from Stage <N>. Check for scoring bugs,
missing edge cases, duplicate entries, broken cross-references, handoff
accuracy. Be specific. List every finding.
```
Fix all findings before advancing to the next stage.
