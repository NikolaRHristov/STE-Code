# Recovery Required: r007-p25-28.md Missing

> **Severity:** CRIT-4 (from audit-20260729-211611.md)
> **Status:** ❌ UNRESOLVED — file not on disk as of 2026-07-30
> **Affects:** Refinement batch 3 (pages 25–28)

---

## What Happened

Refinement batch 3 executed partially:
- r007-p25-28.md — **MISSING** (never written to disk)
- r008-p29-32.md — ✅ present (3,826 bytes, 104 lines)
- r009-p33-36.md — ✅ present (6,791 bytes, 104 lines)

r007 was either never executed or its output was lost. The prompt file
`prompts-refine/r007-prompt.txt` exists (1,300 bytes), so recovery is
straightforward.

---

## Recovery Instructions (for any agent)

1. **Locate the source files:**
   ```
   ste-code/extracted/w007-p25-28.md     ← extraction input
   ste-code/prompts-refine/r007-prompt.txt  ← refinement prompt
   ```

2. **Execute refinement:**
   Run `r007-prompt.txt` against `w007-p25-28.md` using the same
   refinement process used for r001–r006 and r008–r009.

3. **Write output:**
   ```
   ste-code/refined/r007-p25-28.md
   ```

4. **Verify with existing tooling:**
   ```bash
   bash ste-code/verify-batch.sh refined r r007
   ```
   Must pass: ≥ 30 lines, no fabrication signals, clean ending.

5. **Update REFINE-PROGRESS.md:**
   Batch 3 can only be marked ✅ once r007 is confirmed present and verified.

6. **Delete this file** once r007-p25-28.md is confirmed on disk and
   verified. Or keep as a closed incident record — agent’s choice.

---

## Impact if Not Recovered

- GATE 1 cannot pass (missing file in coverage range p1–96)
- `refined-master.md` concatenation will have a gap at pages 25–28
- Batch 3 will remain partially marked in REFINE-PROGRESS.md

---

*Flagged by Perplexity AI external audit — 2026-07-30 00:40 EEST*
*Source: CRIT-4, audit-20260729-211611.md*
