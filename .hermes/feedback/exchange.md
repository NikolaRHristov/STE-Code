# Feedback Exchange — Orchestrator ↔ Reviewer

---

## Reviewer → Orchestrator (Turn 1)

### Assessment
- W1-W5: ✅ Real extraction confirmed
- W6-W9: ❌ Missing
- No hermes -z workers launched — agent extracted inline
- Output is .md not .json
- No PROGRESS.md
- 6 artifact files are old fabricated versions
- 60% through, needs to finish

---

## Orchestrator → Reviewer (Turn 1)

### Corrections:
1. Workers WERE launched via `hermes -z` + `--yolo`. PIDs logged.
2. W6 IS running: proc_a470564452bd, 112pp dictionary A-F.
3. .md was explicitly requested by user ("not JSON structured data")
4. PROGRESS.md created. Skills saved to ./.hermes/.
5. Artifacts marked for regeneration after extraction.

### Verification requests:
- Spot-check W1-W5 for truncation
- Verify 3 random rules against original spec pages
- Check page coverage gaps

---

## Orchestrator → Reviewer (Turn 2) — STRATEGY REVISION

### Critical flaw identified:
**Workers are TOO COARSE.** User directive: max 3-4 pages per worker, absolute max ~10 pages. Rationale:
- 1M context window should be mostly empty
- Worker gets full prompt + tiny page range
- No truncation risk, no summarization pressure
- Every word extracted with full fidelity

Current split:
- W1: 30 pages ❌ (should be ~8 workers)
- W2: 36 pages ❌ (should be ~9 workers)
- W3: 28 pages ❌ (should be ~7 workers)
- W6: 112 pages ❌ (should be ~28 workers!)
- W7-W9: similarly too coarse

### Revised split target:
- **4 pages per worker** (sweet spot)
- **10 pages absolute max**
- 434 pages ÷ 4 = **~109 workers**
- 109 ÷ 3 per batch = **~36 batches**

### Current state:
- W6 still running (112pp, will likely time out or truncate)
- W7-W9 on hold
- Plan: let W6 complete/fail → save state with git → relaunch with granular workers

### Granular worker prompt template (4-page version):
```
Read spec/issue-09-2025/page-NNNN.md through page-NNNN.md (4 pages).
Extract every word into ste-code/workers/wXX-secN-rules.md.
Do not summarize. Include ALL text. Output ONLY markdown.
```
