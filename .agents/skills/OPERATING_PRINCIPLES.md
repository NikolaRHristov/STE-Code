# STE-Code Pipeline — Global Operating Principles

These principles apply to **every** skill, script, and agent session in this
repo. They are non-negotiable. Violation = pipeline corruption.

---

## 1. SESSION ISOLATION (most important)

**One session = one operation = one read + one write. Never carry content across
sessions for re-editing.**

A model that holds content across multiple operations will:

- Omit lines it judges "redundant"
- "Improve" wording (violates verbatim rule R1)
- Compress tables it thinks are "repetitive"
- Drop `<br>` tags, reformat cells, merge rows
- Add commentary it thinks is "helpful"

**Structural fix:** don't let the model hold content longer than one pass.

### Per-stage isolation

| Stage    | Session scope    | Input           | Output          | Forbidden           |
| -------- | ---------------- | --------------- | --------------- | ------------------- |
| Extract  | 1 per worker     | 4 raw pages     | 1 extracted .md | re-read own output  |
| Verify   | separate process | extracted .md   | pass/fail       | modify content      |
| Refine   | 1 per chunk      | 1 extracted .md | 1 refined .md   | merge other chunks  |
| Merge    | 1 session        | all refined     | master.md       | re-edit extracted   |
| Adapt    | 1 per rule       | 1 spec section  | 1 adapted file  | rewrite other rules |
| Artifact | 1 per artifact   | adapted files   | 1 artifact      | combine unrelated   |

### Hard constraints

1. A session that extracts MUST NOT also refine. Separate sessions.
2. A session that refines MUST NOT read its own refined output back and "fix"
   it.
3. Re-runs are idempotent (R5): if output exists and is valid, SKIP.
4. Each session writes exactly ONE file. No cross-file edits within one session.
5. Context too small? Split the job (R6) — don't truncate.

---

## 2. STRICT CONTENT PRESERVATION (R1-R6)

Imported from `lib/pipeline_core.py` → `STRICT_RULES`:

- **R1 Verbatim** — byte-faithful to source, no cleanup/reformat
- **R2 Table atomicity** — rows never split/merged/reordered
- **R3 No freelance** — no commentary/examples/headers beyond required markers
- **R4 Single-file write** — never touch another worker's file; shared appends
  use locks
- **R5 Idempotence** — re-runs produce identical output; skip if valid
- **R6 Context safety** — request smaller range rather than truncate

All scripts MUST import `lib/pipeline_core.py` and use its checks. Do not
re-implement enforcement logic per-script.

---

## 3. SHARED LIBRARY (single source of truth)

`lib/pipeline_core.py` contains ALL enforcement logic:

- `STRICT_RULES` — injected into every worker prompt
- `find_table_breaks()` — R2 detection
- `detect_freelance()` — R3 detection
- `load_checkpoint()` / `save_checkpoint()` / `is_worker_done()` — R5
- `acquire_lock()` / `release_lock()` / `check_lock()` — R4 collision prevention
- `verify_extracted_file()` — unified R1-R6 check
- `would_truncate()` — R6 detection

Backup: this file is committed to git. Any script needing enforcement imports
it.

---

## 4. PAIR PHILOSOPHY (skill + script)

Each pipeline stage has a matching pair:

- **SKILL.md** — human/agent-readable instructions (what to do)
- **script** — executable enforcement (how to verify, what to run)

The script is the authority. The SKILL describes intent. Neither re-implements
the other's logic; both defer to `lib/pipeline_core.py`.

---

## 5. ANTI-PATTERNS (forbidden)

```python
# WRONG: one session does extract → refine → adapt → artifact
agent.run("read pages, extract, refine, adapt, generate artifact")
# The model will "helpfully" summarize the dictionary to save tokens.
```

```bash
# WRONG: two agents write the same group file without locking
agent_A: write group-005-dict-A-C.md
agent_B: write group-005-dict-A-C.md # race → lost writes
```

```python
# WRONG: re-reading own output to "improve" it
out = extract(w)
refine(out)  # model freelances here
```

---

## 6. CORRECT PATTERN

```python
# RIGHT: 4 separate sessions, each one job
session1 = extract(W057)        # reads 4 pages, writes w057.md, exits
verify(w057.md)                 # separate process, read-only check
session2 = refine(r057)         # reads w057.md, writes r057.md, exits
session3 = adapt(a-secX)        # reads 1 rule from spec, writes 1 file
```

All enforcement via `lib/pipeline_core.py`. All locks via `lock-group.sh`. All
verification via `verify-batch.py` / `strict-guard.py` / `protect-tables.py`.
