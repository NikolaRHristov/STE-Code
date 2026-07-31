# STE-Code Extraction Feedback

## Project-Specific Adaptations of Global Rules

### Parallelism: 2 Chains of Sequential Batches
**Global rule**: Max 2-way concurrent LLM API calls.
**Local adaptation**: Launch batches in **2 parallel chains** (not 3), each chain running batches sequentially:
- Chain A: `for b in 11 12 13 14; do python3 .agents/tools/extraction/extract_batch.py $b 1; done`
- Chain B: `for b in 15 16 17 18; do python3 .agents/tools/extraction/extract_batch.py $b 1; done`

This gives ~109s per worker completion with <5% failure rate, vs 5-way parallel which caused >50% failure rate with 3-5x slower workers.

### Git Commit Fix
**Problem**: `.gitignore` line 49 has `ste-code/extracted/` which ignores all extracted files.
**Fix applied**: Changed to `!ste-code/extracted/` (negation rule).
**Manual commit command**: `git add -A ste-code/extracted/*.md && git commit -m "..."`

### Progress Tracking
- **37 total batches** (109 workers, 4 pages each)
- **Batches 01-10 complete** (30 workers, 120 pages extracted) — committed as individual batch commits
- **Batches 11-22 currently running** via 2 parallel chains
- **434 pages total** (426 mapped + 8 front matter pages in MANIFEST)

### Key Commands
```bash
# Run 2 parallel chains (each batch sequentially within chain)
for b in 11 12 13 14; do python3 .agents/tools/extraction/extract_batch.py $b 1 2>&1; done &
for b in 15 16 17 18; do python3 .agents/tools/extraction/extract_batch.py $b 1 2>&1; done &

# Verify batch quality
bash .agents/tools/quality/verify-batch.sh extracted w w031 w032 w033

# Manual commit (when extract_batch auto-commit fails)
git add -A ste-code/extracted/*.md && git commit -m "W031-W035: Commit extracted worker files"
```

### extract_batch.py Behavior Notes
- Workers within a batch are **sequential** (3 workers per batch, run one at a time)
- Batch-level is the parallelism point (run multiple extract_batch.py processes)
- Script auto-skips workers whose output files already exist and pass verification
- `git add` + `git commit` inside the script fails on gitignored files (fixed by .gitignore negation)
- W055 had 3/3 retries fail due to "commentary" detection ("here is" in last 10 lines)
