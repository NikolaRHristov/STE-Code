# GATE 1: Verification Runbook

> **Prerequisite:** All 109 extraction workers complete (109/109 ✅ confirmed)
> **Tooling:** `ste-code/verify-batch.sh` (already committed)
> **Output:** GATE 1 checks in `PROGRESS.md` all marked `[x]`
> **Estimated time:** ~5 minutes for all 109 workers

---

## Before You Start

1. Ensure `r007-p25-28.md` is recovered (see `audit/r007-recovery-needed.md`)
2. `cd` to repo root
3. Confirm `extracted/` has 109 files:
   ```bash
   ls ste-code/extracted/*.md | wc -l
   # Expected: 109 (may show 114 if legacy w1-w5 files present — that’s OK)
   ```

---

## Run Verification — All 109 Workers

Run in 37 batches of 3 (matching extraction batches). Worker IDs match
`wNNN` filenames in `ste-code/extracted/`.

```bash
# Batch 1
bash ste-code/verify-batch.sh extracted w w001 w002 w003

# Batch 2
bash ste-code/verify-batch.sh extracted w w004 w005 w006

# Batch 3
bash ste-code/verify-batch.sh extracted w w007 w008 w009

# Batch 4
bash ste-code/verify-batch.sh extracted w w010 w011 w012

# Batch 5
bash ste-code/verify-batch.sh extracted w w013 w014 w015

# Batch 6
bash ste-code/verify-batch.sh extracted w w016 w017 w018

# Batch 7
bash ste-code/verify-batch.sh extracted w w019 w020 w021

# Batch 8
bash ste-code/verify-batch.sh extracted w w022 w023 w024

# Batch 9
bash ste-code/verify-batch.sh extracted w w025 w026 w027

# Batch 10
bash ste-code/verify-batch.sh extracted w w028 w029 w030

# Batch 11
bash ste-code/verify-batch.sh extracted w w031 w032 w033

# Batch 12
bash ste-code/verify-batch.sh extracted w w034 w035 w036

# Batch 13
bash ste-code/verify-batch.sh extracted w w037 w038 w039

# Batch 14
bash ste-code/verify-batch.sh extracted w w040 w041 w042

# Batch 15
bash ste-code/verify-batch.sh extracted w w043 w044 w045

# Batch 16
bash ste-code/verify-batch.sh extracted w w046 w047 w048

# Batch 17
bash ste-code/verify-batch.sh extracted w w049 w050 w051

# Batch 18
bash ste-code/verify-batch.sh extracted w w052 w053 w054

# Batch 19
bash ste-code/verify-batch.sh extracted w w055 w056 w057

# Batch 20
bash ste-code/verify-batch.sh extracted w w058 w059 w060

# Batch 21
bash ste-code/verify-batch.sh extracted w w061 w062 w063

# Batch 22
bash ste-code/verify-batch.sh extracted w w064 w065 w066

# Batch 23
bash ste-code/verify-batch.sh extracted w w067 w068 w069

# Batch 24
bash ste-code/verify-batch.sh extracted w w070 w071 w072

# Batch 25
bash ste-code/verify-batch.sh extracted w w073 w074 w075

# Batch 26
bash ste-code/verify-batch.sh extracted w w076 w077 w078

# Batch 27
bash ste-code/verify-batch.sh extracted w w079 w080 w081

# Batch 28
bash ste-code/verify-batch.sh extracted w w082 w083 w084

# Batch 29
bash ste-code/verify-batch.sh extracted w w085 w086 w087

# Batch 30
bash ste-code/verify-batch.sh extracted w w088 w089 w090

# Batch 31
bash ste-code/verify-batch.sh extracted w w091 w092 w093

# Batch 32
bash ste-code/verify-batch.sh extracted w w094 w095 w096

# Batch 33
bash ste-code/verify-batch.sh extracted w w097 w098 w099

# Batch 34
bash ste-code/verify-batch.sh extracted w w100 w101 w102

# Batch 35
bash ste-code/verify-batch.sh extracted w w103 w104 w105

# Batch 36
bash ste-code/verify-batch.sh extracted w w106 w107 w108

# Batch 37 (2 workers only)
bash ste-code/verify-batch.sh extracted w w109
```

### Or Run All at Once

```bash
for i in $(seq -w 1 109); do
  worker="w$(printf '%03d' $i)"
  FILE=$(ls ste-code/extracted/${worker}-p*.md 2>/dev/null | head -1)
  if [ -z "$FILE" ]; then
    echo "🔴 $worker: NOT FOUND"
  else
    LINES=$(wc -l < "$FILE" | tr -d ' ')
    echo "✅ $worker: $LINES lines"
  fi
done
```

---

## Pass / Fail Thresholds

| Signal | Threshold | Action |
|---|---|---|
| File not found | Any | 🔴 BLOCK — re-extract before proceeding |
| Lines < 15 | Any | 🔴 BLOCK — empty or truncated, re-extract |
| Lines 15–29 | ≥ 1 file | 🟡 WARN — check if page is content-light (cover, blank, appendix header) |
| Lines ≥ 30 | All 109 | ✅ PASS |
| Fabrication signal | Any | 🔴 BLOCK — re-extract that worker |
| Last line mid-word | Any | 🟡 WARN — check surrounding pages for context bleed |
| Missing page header | ≤ 5 files | 🟡 ACCEPTABLE (cover/TOC pages may lack `# Page N of 434`) |

---

## Known Issues to Watch For

**Legacy files (w1–w5):** Five coarse legacy extraction files co-exist in `extracted/`
alongside the 109 v3 workers. The `verify-batch.sh` script only runs against
`wNNN` filenames (three-digit IDs) so legacy files are skipped automatically.
They are not authoritative; `master-raw.md` was built from v3 workers.

**Workers w067–w069:** The primary audit (2026-07-29 21:16) flagged these as
possibly uncommitted. Confirm they are present and have correct content.

---

## When All 109 Pass

Update `PROGRESS.md` GATE 1 section:

```markdown
## GATE 1: Verify ✓
- [x] All extraction files have content > 30 lines
- [x] No truncated files (last 3 lines end cleanly)
- [x] No fabrication signals in spot-checks
- [x] Execution audit passed with 0 critical discrepancies
```

Then `git gcommit-hermes` with message:
```
docs(gate1): GATE 1 passed — all 109 extraction workers verified
```

---

## Notes

- `check-rails.py` in `ste-code/` may provide additional validation — review its flags before declaring GATE 1 complete
- GATE 1 is a prerequisite for GATE 3 (Adaptation) — do not begin rule adaptation until GATE 1 is confirmed
- This runbook covers extraction verification only; refinement verification (r001–r109) follows the same pattern with `refined` as the directory argument

---

*Runbook authored by Perplexity AI external audit — 2026-07-30 00:40 EEST*
*Based on existing tooling: verify-batch.sh (c1b77373)*
