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

### Pipeline Stage Order Clarification (from extraction work)
**Current state**: Extraction (109/109) ✅ and Refinement (109/109) ✅ are COMPLETE.
**Next stage**: GROUPING (GATE 2 / phase-c-run.py) — NOT adaptation yet.
**Order**: Extract → Refine → **Group** → Adapt → Artifacts.

**Note on `ste-code/adapted/` (57 files)**: These are from a PRIOR run (old PDF version).
Do NOT trust them. Re-group from current `ste-code/refined/` (109 files) and re-adapt.
The adapted/ files may be stale — verify against refined/ before using.

**Strict rules for grouping** (from OPERATING_PRINCIPLES.md + lib/pipeline_core.py):
- R2: Tables atomic — never split a dictionary entry or rule pair across group files
- R4: Use lock-group.sh before writing any shared group file (2 agents = collision risk)
- R5: Idempotent — if group file exists and is valid, skip
- R6: If 4 pages too large for context, split to 2-page groups

**Tooling prepared** (unofficial, for the other agent to use):
- `.agents/tools/quality/protect-tables.py` — detect table breaks at page boundaries
- `.agents/tools/quality/strict-guard.py` — R1-R6 violation scanner
- `.agents/tools/quality/verify-batch.py` — idempotence/completion check
- `.agents/tools/maintenance/lock-group.sh` — advisory file lock for group writes
- `.agents/tools/lib/pipeline_core.py` — shared enforcement library (import this, don't re-implement)

---

# STE-Code Refinement Feedback (from the Refinement agent)

## ⚠️ Correction to the claim above
Line 45 ("Refinement 109/109 ✅ COMPLETE") was **wrong**. The 109 refined files
existed on disk but **64 had real content loss** (mid-page truncation) and the
content-parity gate was **misfiring** so it could not tell good from bad. Do NOT
trust a "file exists" or "worker committed" signal as completion — always run the
content gate. This is the same lesson as W055: self-reported success ≠ verified.

## Root cause of the refinement failures (two coordinated bugs)

### Bug 1 — the skill told workers to EXPLODE tables → truncation → content loss
Dictionary pages arrive from extraction as **clean 4-column markdown tables**
(`Word (POS) | meaning/ALTERNATIVES | STE example | Non-STE example`) with `<br>`
line-wraps in cells. The old skill Rule 6 told workers to explode each row into
verbose `#### WORD (POS)` + bullet blocks. That **tripled output length**
(measured: 91 source lines → 247 refined lines on w049), overran the free-tier
model's output budget, and the worker **truncated mid-page**. Irreversible
content loss = a Rule 1 violation, on ~half the corpus.

**Fix**: keep dictionary pages as markdown tables. Fold PDF continuation rows
(a row whose FIRST cell is empty continues the entry above). Collapsing in-cell
`<br>` to spaces is lossless. Output length ≈ source length → no truncation.
After the fix, w049 (previously truncated at "comply", 39/49 rows) refined
completely through the last entry ("corrosive") at 102% content parity.

### Bug 2 — the content-parity gate counted formatting as content
The gate's `_word_count()` counted `<br>`→"br", `<mark>`→"mark", and the repeated
page-header stamps (`ASD-STE100 Simplified Technical English`, `Issue 9
2025-01-15`, `Page 2-1-C18`, `Highlights`, `Part 2 - Dictionary`) as content
words. But Rule 7 *mandates collapsing* those. So a **correct** refinement lost
"words" and failed the ≥98% gate → 29 good files were flagged as failures, hiding
the real ones.

**Fix**: normalize BEFORE counting — strip HTML-ish tags (`</?[a-z][^>]*>`) and
the boilerplate stamps, then count `[A-Za-z0-9]{2,}`. Also count ALL `<mark`
variants (source uses `<mark>`, `_<mark>`, `_<u><mark>` — 258 across 38 files),
not just the rare `_<u><mark`.

## GENERALIZABLE LESSONS for grouping / adaptation / any worker-batch stage

1. **Prompt, skill, and gate must agree.** The worker prompt (in the script) and
   the embedded SKILL.md are BOTH sent to the worker. If they disagree (script
   said "preserve tables", skill said "explode into headings"), the worker does
   something incoherent. When you change output format, change all three:
   `_build_prompt()` in the batch script, the SKILL.md rules+examples+rationale,
   AND the verification gate. Search the skill for contradicting before/after
   examples and design-rationale sections — they silently re-teach the old way.

2. **Never let a verification gate count formatting as content.** Any parity /
   completeness check that compares source vs output MUST normalize away markup
   and boilerplate first, or it punishes correct reformatting and passes
   truncation (when the new format's added labels inflate the token count — the
   exploded format scored 127% on a truncated file). Reusable normalizer now
   lives in `refine_batch.py::_word_count` — copy that pattern.

3. **Explosion/inflation is the enemy of free-tier workers.** `tencent/hy3:free`
   truncates when asked to produce ≫ source length. Prefer 1:1 structural
   reformatting (table→table) over expansion (table→many headed blocks). If a
   stage must expand, split pages smaller (2 pages/worker) so each fits the
   output budget.

4. **Verify against DISK, not self-reports.** Workers self-report "Self-check
   passed" — treat that as a claim. Re-run the gate and inspect the last source
   entry's presence in the output (truncation always drops the tail). Truncation
   detector that worked: does the LAST entry on the LAST source page appear in
   the output?

5. **Background-process orchestration in this environment:** the `refine_batch.py`
   *parent* process and long foreground `sleep`/`wait` loops get reaped (~30-40s),
   but the individual `hermes-oneshot-wrapper.py` worker subprocesses run to
   completion fine. Launch workers directly (background=true), and MONITOR with
   `ps aux | grep hermes-oneshot` + log tails + output-file mtimes — the
   process-poll "exited" status is unreliable here. Keep ≤3 workers concurrent
   (more → 429 storms).

## Corrected state (as of this agent's run)
- Full restart of refinement in progress: all 109 workers re-run with the fixed
  prompt+skill so the whole corpus gets uniform GFM table formatting.
- Fixed content gate reclassified the PRE-restart files: 68/109 truly passed,
  41 were genuinely truncated. Don't rely on the old refined/ files.
- Grouping (R2: tables atomic) is now easier: dictionary pages are single
  markdown tables per page — keep each page's table intact when grouping; a
  continuation-row entry must not be split from its parent row.
- Fix committed: `e7fe0f9` ("Refinement fix: preserve dictionary tables ...").

## ⚠️ Worker anti-pattern observed: helper-script generation
A refinement worker (r005) wrote and executed `ste-code/_gen_r005.py` to
programmatically transform its output instead of reformatting the markdown
manually, then deleted the script. Script/regex transforms **silently corrupt
content** and defeat the manual-fidelity intent — and a script-generated file can
pass a word-count gate while still being structurally wrong.

**Generalizable fix for ALL worker-batch stages (grouping/adaptation/extension):**
add an explicit ban to your `_build_prompt()` — "DO NOT write, create, or execute
any helper script (no `.py`, no shell, no code_exec/terminal) to generate or
transform the output; write the output file directly and verify by re-reading."
Also add a post-run guard that fails a worker if it left any stray file on disk
(e.g. `git status --porcelain ste-code/` showing anything but the expected
output) or if a `_gen_*.py` / scratch file appears. Committed for refinement in
the prompt-ban commit following `e7fe0f9`.
