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
**`status=completed` means the loop ended, not that the goal was met.** Under
API rate limits the subagent's final payload can be an HTTP 429 / 524 error
string while the wrapper still reports `status=completed`. Reading `completed`
as success silently ships empty work.

## Steps

1. **Verify the deliverable on disk before trusting the summary.** If the GOAL
   named an output path, `ls` it. Absent = goal not met, regardless of status.
2. **Grep the live transcript for the real outcome:**
   `grep -c "429\|rate limit\|524" <live>/task-N.log` — any hit = failure.
3. **Do NOT re-dispatch into the same rate limit.** Salvage what the delegate
   left and finish locally: it often wrote a scratch JSON (e.g. `_scan.json`
   with per-file metrics) to its scratch dir. Read it with **local Python** and
   rebuild the deliverable — deterministic, zero tokens. See
   `references/salvage-recipe.md`.
4. **Parallel research passes must be reconciled before implementing.** Two
   delegates on overlapping territory (helper boundaries vs config boundaries)
   produce one target architecture only after you read and merge both reports.
5. **Keep research delegates read-only:** one report file, no `git`, no tree
   edits.
6. **For any deliverable that takes >~5 min or a long research sweep, WRITE IT
   INCREMENTALLY AND EARLY — never in a single final `write_file`.** A delegate
   that does all its work then writes the whole result at the end will lose
   EVERYTHING if the final summary/transport call hits HTTP 524 (Cloudflare 120
   s proxy timeout) or 429. The 524 lands on the LAST turn — exactly the turn
   that writes the file. **Protocol (proven across repeated 15-min passes):**
    - First `write_file` = skeleton (range identity + headline stats + first 2–3
      verified claims). Land it BEFORE the sweep is done.
    - Then loop: `read_file` the current file -> `patch` (or rewrite) to append
      the next section -> repeat. Reason between writes (read source -> decide
      next chunk -> write only that chunk -> reassess). This is iterative, not a
      single dump.
    - Keep the final chat message SHORT (a one-line `DONE path=... lines=N`). Do
      the writing via tool calls, not the final turn.
    - If the delegate reports `status=completed` but the file is absent, the
      final-turn 524 ate the write — salvage by reading its live transcript
      (`grep` for the commands/output it ran) and rebuilding locally, OR
      re-dispatch with the incremental-write mandate. The prior pass's
      transcript still contains the verified facts.
    - The Composer (downstream delegate) inherits the same rule: land title +
      headline-stats + first chapter first, then append via `patch`. A run that
      followed this survived two 524s with the file intact; a run that didn't
      lost its whole 15-minute output.

## Pitfalls

- **Scope drift: a delegate that narrates instead of doing the task is a lie
  too.** `status=completed` + real on-disk deliverables is NOT the only failure
  shape. The other is the delegate quietly re-scoping itself from _executor_ to
  _reporter_: it diagnoses, explains, and pastes "fresh verification evidence"
  while leaving the actual engineering (the fix, the edit, the verification
  command) undone. It reports `completed` truthfully — it did finish narrating —
  but the GOAL (the change) was never made. Signals: the final summary is long
  and analytical, contains words like "if we…", "the right approach is…", "would
  fix", or "I recommend…" with NO corresponding `write_file`/`patch` to a
  deliverable path; or it asks "should I implement?" after being told to.
  Antidote: before trusting a delegate's sign-off, check that the DELIVERABLE
  (the file edit / command run) actually exists and matches the goal — not just
  that a polished report was returned. When the user says the delegate "is just
  explaining a run" instead of doing it, that IS the failure; finish the
  engineering in the parent session and do not let the delegate's narrative
  stand in for the work. (This is distinct from the `status=completed` + 5xx
  case — here the loop genuinely ended and the summary is honest; only the _task
  scope_ was silently dropped.)
- `status=completed` + HTTP 429/524 in transcript = gave up, not finished —
  **with one exception.** A 429 can land at the _tail_ of the transcript: the
  summary-transport call failing _after_ the delegate already wrote its
  deliverables. In that case `status=completed` + a 429 + a real on-disk
  deliverable = a completed task. Do NOT discard the work. The 429 alone is not
  proof of failure; it is a reason to verify on disk (which you must do anyway).
  Only treat 429 as failure when the deliverable is genuinely absent — confirm
  with `ls`/reads before re-launching.
- The jail may reject `python3 - <<'EOF>` heredocs as a write to `/` (false
  positive). Write the salvage script to `.agents/tmp/` and run it instead.
- **Concrete on-disk verification battery (don't just trust `status`).** After a
  delegate returns, run an independent check on the named deliverable before
  declaring success: (a) `read_file` the output path — read the actual content,
  don't rely on `grep` alone; (b) `grep -n "<false-phrase>" <file>` to prove the
  bad text is gone; (c) `git check-ignore -v <path>` whenever the claim involves
  what the repo ships. Observed this session: a delegate reported
  `status=completed` with an HTTP 429 on its final transport call, yet its
  `patch` writes HAD landed — the battery confirmed the edits were real, so the
  429 tail was the "completed + 429 + real deliverable" non-failure case (see
  pitfall #1), not a discard. The battery is what lets you tell the two apart.
- A delegate that says "done?" or pastes an error as a result has not verified
  anything. Trust the file, not the chat.

## References

- `references/salvage-recipe.md` — local rebuild from a delegate's `_scan.json`.
