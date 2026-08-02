---
name: delegation-verification
description: "Delegate completed status lies; verify output on disk."
version: "1.0.0"
category: dev
capability: developing-and-changing-the-standard
source: .agents/skills/ste-code-dev/delegation-verification
layout: ste-code-canonical-v1
---

# Delegation Verification

`delegate_task` returns a summary with a `status` field. The trap:
**`status=completed` means the loop ended, not that the goal was met.** Under API
rate limits the subagent's final payload can be an HTTP 429 / 524 error string
while the wrapper still reports `status=completed`. Reading `completed` as success
silently ships empty work.

## Steps

1. **Verify the deliverable on disk before trusting the summary.** If the GOAL
   named an output path, `ls` it. Absent = goal not met, regardless of status.
2. **Grep the live transcript for the real outcome:**
   `grep -c "429\|rate limit\|524" <live>/task-N.log` — any hit = failure.
3. **Do NOT re-dispatch into the same rate limit.** Salvage what the delegate left
   and finish locally: it often wrote a scratch JSON (e.g. `_scan.json` with
   per-file metrics) to its scratch dir. Read it with **local Python** and rebuild
   the deliverable — deterministic, zero tokens. See `references/salvage-recipe.md`.
4. **Parallel research passes must be reconciled before implementing.** Two
   delegates on overlapping territory (helper boundaries vs config boundaries)
   produce one target architecture only after you read and merge both reports.
5. **Keep research delegates read-only:** one report file, no `git`, no tree edits.

## Pitfalls

- `status=completed` + HTTP 429/524 in transcript = gave up, not finished.
- The jail may reject `python3 - <<'EOF>` heredocs as a write to `/` (false
  positive). Write the salvage script to `.agents/tmp/` and run it instead.
- A delegate that says "done?" or pastes an error as a result has not verified
  anything. Trust the file, not the chat.

## References

- `references/salvage-recipe.md` — local rebuild from a delegate's `_scan.json`.
