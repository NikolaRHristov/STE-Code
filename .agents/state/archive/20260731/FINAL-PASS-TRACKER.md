# STE-Code Final Pass — Single-Session Orchestration

> **Launch from one session. Track every worker. Self-audit every phase.**
> Model: `poolside/laguna-s-2.1:free` | Reasoning: `high` | Batch: 3 | Telemetry: `.agents/tools/shared/telemetry-worker.py`

---

## Orchestration Loop

```
PER BATCH (3 workers):
  1. Pick next 3 workers from tracker below
  2. Launch: python3 .agents/tools/shared/telemetry-worker.py <id> <prompt> --output <file> (bg + notify)
  3. Wait for all 3 → verify telemetry shows PASS
  4. Flip [ ] → [x] in tracker
  5. git add -A && git gcommit-hermes "phase:<letter> batch:<N>"
  6. Push every 3 batches. Never launch >3. Never skip verify.
```

---

## What's Done

| Item | Status |
|------|:------:|
| Maturity audit (21 files, ~85 scored) | ✅ |
| Agent #3 rewritten (74→416L, L2→L4+) | ✅ |
| Agent #4 cross-refs fixed (5 broken paths) | ✅ |
| worker-prompts.md v2→v3 migration | ✅ |
| 10 md-fixes applied (audit/SCE formatting) | ✅ |
| Expansion B1 batches 1-4 (20 examples) | ✅ |
| Telemetry wrapper built + tested | ✅ |
| Reasoning set to `high` permanently | ✅ |
| Agent #9 — Translation Orchestrator | ✅ |
| Repo: description, topics, homepage, remote | ✅ |
| Agent #4 self-audit: found scoring bugs, worker issues, handoff gaps | 🔴 In progress |

---

## Remaining Phases

### Phase A0: Missing Maturity Fixes (2 inline fixes)

| ID | File | Gap |
|:--:|------|-----|
| A0-W1 | `.agents/agent/agent-5-sce-populator.md` | 2 broken schema refs → point to `ste-code/v2/compute/schemas/` |
| A0-W2 | `.agents/agent/agent-6-phi-sce.md` | Zero cross-references → add 5 pipeline links + worked example |

### Phase A: Maturity Fixes (61 workers, 21 batches)
**Prompts:** `.agents/prompts/maturity-fixes/fix-NNN-*.txt` (already generated)
**Note:** Already run once — most will self-skip. Only unapplied fixes execute.
```
[A01-A21: fix-001 through fix-061]
```

### Phase B1: Expansion — Rule Examples (51 remaining, 17 batches)
**Prompts:** `.agents/prompts/expansion-pass1/pass1-batch-NNN.txt`
**Done:** batches 001-004 [x]
```bash
python3 .agents/tools/shared/telemetry-worker.py b1-NNN \
  .agents/prompts/expansion-pass1/pass1-batch-NNN.txt \
  --output ste-code/adapted/expanded/pass1-batch-NNN.json
```
```
[B1-05 through B1-19: pass1-005 through pass1-055]
```

### Phase B2: Dictionary Depth (30 workers, 10 batches)
**Needs:** prompt generation script — split 5,943-line dictionary into 30 batches.
```
[B2-01 through B2-10: dict-001 through dict-030]
```

### Phase B3: Category Entries (9 workers, 3 batches)
```
[B3-01 through B3-03: cat-001 through cat-009]
```

### Phase B4: Anti-Patterns + Paradigms (6 workers, 2 batches)
```
[B4-01: ap-001, ap-002, ap-003]  [B4-02: para-001, para-002, para-003]
```

### Phase C: SCE Population (18 workers, 6 batches)
**Pre-flight:** Copy schemas from v2 if missing.
```bash
mkdir -p SCE/compute/schemas
cp ste-code/v2/compute/schemas/*.json SCE/compute/schemas/
```
```
[C01-C03: rules-sec1 through rules-sec9]
[C04: vocab-verbs, vocab-adj, vocab-unapproved]
[C05: synonym-table, prompt-micro, prompt-full]
[C06: prompt-agentic, prompt-developer, sce-validate]
```

### Phase D: Artifact Regeneration (6 workers, 2 batches)
```
[D01: distilled-prompt, self-reading-manual, methodology]
[D02: example-turn, deployment-guide, readme]
```

### Phase E: Translations (30 workers, 10 batches)
**Runs parallel with C+D.** Discovery-based — workers explore source dirs, create blank placeholders.
```
[E01-E10: 10 discovery targets × 3 locale workers each]
```

### Phase F: Final Audit (10 workers, 4 batches)
```
[F01: counts-1, counts-2, zerobyte]
[F02: rail-1, rail-2, rail-3]
[F03: consistency-1, consistency-2]
[F04: benchmark-rerun-1, benchmark-rerun-2]
```

---

## Self-Audit Per Phase

After each phase completes, launch a review worker at reasoning:high:
```
Quality review: audit all output from Phase <letter>. Check for:
- Scoring/validation bugs
- Missing edge cases
- Duplicate or conflicting entries
- Broken cross-references
- Handoff accuracy
Be specific. List every finding.
```
Fix findings before advancing to next phase.

---

## Summary

| Phase | Workers | Batches | Status |
|-------|:------:|:------:|:------:|
| A0 | 2 | 1 inline | ✅ |
| A | 61 | 21 | ⬜ (prompts ready) |
| B1 | 51 | 17 | 🟢 4/55 done |
| B2 | 30 | 10 | ⬜ (needs prompts) |
| B3 | 9 | 3 | ⬜ |
| B4 | 6 | 2 | ⬜ |
| C | 18 | 6 | ⬜ |
| D | 6 | 2 | ⬜ |
| E | 30 | 10 | ⬜ (parallel) |
| F | 10 | 4 | ⬜ |
| **Total** | **223** | **76** | **4/223 done** |

**Tracker:** Copy to `.agents/state/FINAL-PASS-TRACKER.md` — flip [ ] → [x] per batch.
