# SESSION ISOLATION PRINCIPLE — STE-Code Pipeline

## Core Rule
**Every transformation step happens in its OWN isolated session. One session = one
operation = one read + one write. Never carry content across sessions for
re-editing.**

## Why
Language models "freelance" when they hold content across multiple operations:
- They omit lines they judge "redundant"
- They "improve" wording (violates R1 verbatim rule)
- They compress tables they think are "repetitive"
- They drop `<br>` tags, reformat cells, merge rows
- They add commentary they think is "helpful"

The fix is structural: **don't let the model hold the content longer than one pass.**

## Pipeline Stage Isolation

| Stage | Session | Input | Output | Model may NOT |
|-------|---------|--------|--------|---------------|
| Extract | 1 per worker (W001-W109) | 4 raw page files | 1 extracted .md | re-read its own output, edit it |
| Verify | automatic (strict-guard) | extracted .md | pass/fail | modify content |
| Refine | 1 per 4-page chunk | extracted .md | refined .md | merge with other chunks |
| Merge | 1 session | all refined | master.md | re-edit extracted |
| Adapt | 1 per rule file | 1 spec section | 1 adapted file | rewrite other rules |
| Artifact | 1 per artifact | adapted files | 1 artifact | combine unrelated rules |

## Hard Constraints
1. A session that extracts MUST NOT also refine. Separate sessions.
2. A session that refines MUST NOT read its own refined output back and "fix" it.
3. Re-runs are idempotent (R5): if output exists and is valid, SKIP. Never re-touch.
4. Each session writes exactly ONE file. No cross-file edits within one session.
5. Context window too small for the job? Split the job (R6) — don't truncate.

## Implementation
- `extract_batch.py` launches 1 hermes process per worker (already isolated)
- `verify-batch.py` runs as a SEPARATE process after extraction (not inside it)
- `strict-guard.py` is a SEPARATE process that only reads and reports
- Grouping/adaptation workers acquire `lock-group.sh` so 2 sessions can't write
  the same file — but each session still writes only its own assigned slice

## Anti-Pattern (forbidden)
```
# WRONG: one session does extract → refine → adapt → artifact
agent.run("read pages, extract, refine, adapt, generate artifact")
# The model will "helpfully" summarize the dictionary to save tokens.
```

## Correct Pattern
```
# RIGHT: 4 separate sessions, each one job
session1 = extract(W057)          # reads 4 pages, writes w057.md, exits
verify(w057.md)                   # separate process, read-only check
session2 = refine(r057)           # reads w057.md, writes r057.md, exits
session3 = adapt(a-secX)          # reads 1 rule from spec, writes 1 file, exits
```
