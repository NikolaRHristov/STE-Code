---
name: ste-code-repo-hygiene
description:
    The STE-Code repo (`.agents/` toolchain + `ste-code/` artifacts) is shipped
    to
category: dev
capability: developing-and-changing-the-standard
source: <home>/.hermes/profiles/dev-ste-code/skills/ste-code/ste-code-repo-hygiene
layout: ste-code-canonical-v1
---

# STE-Code Repo Hygiene & Refactoring

The STE-Code repo (`.agents/` toolchain + `ste-code/` artifacts) is shipped to
third parties and edited across several concurrent Hermes sessions. These rules
keep it portable, reviewable, and free of local-environment leakage. They were
hardened after a multi-session DRY + config-centralisation refactor.

## 1. Directory structure (`.agents` holds ONLY parent categories)

- `.agents/` contains **parent-category directories only** (tools/, hermes/,
  benchmark/, config/, state/, tmp/, feedback/, vendor/). It must NOT hold
  direct children that interrupt work.
- **All temporary / research / delegate scratch goes in `.agents/tmp/`** — never
  invent a new top-level dir like `.agents/refactor/`. If a delegate writes
  scratch elsewhere, move it to `.agents/tmp/` and remove the stray dir before
  any commit.
- `.agents/tmp/` is gitignored → it ships nothing. Keep final reports there too,
  unless the user wants them promoted.
- Do NOT touch `ste-code/` unless explicitly told — it holds production
  artifacts.

## 2. Shippability / anonymization

- **No local absolute paths in tracked files.** Replace `<home>` →
  `/home/operator` and `<repo-root>` with marker-walk root detection.
  `git grep -n "<repo-root>\\|<home>" -- .` (excluding vendor) must be clean
  before shipping.
- **PII in tracked memory / profile files.** When `USER.md` / `MEMORY.md` are
  tracked in the repo (they are symlinked from
  `~/.hermes/profiles/<p>/memories/` into `.agents/hermes/memory/<p>/`),
  context-compaction auto-summaries routinely capture real identifiers — the
  operator's full name, the GitHub org, and repo names. These are
  version-controlled, so they leak on every clone. **Anonymize on sight:**
  `<person>`, `<github-org>`, `<repo-a/b/c>`, etc. Keep the workflow preferences
  (the durable, non-personal part) verbatim.
    - _Verification:_
      `grep -rniE "<person>|<github-org>|<real-org>|<real-repo>" .agents/hermes/memory/`
      must return CLEAN before committing memory files.
- **Audit for false "ships" claims.** `.agents/tmp/*` is gitignored → it ships
  NOTHING (see §1). A doc that says the repo "ships" content from a gitignored
  path is self-contradictory and false. Observed in the wild: a skill claimed
  the repo "ships a family of release notes under `.agents/tmp/remote-notes/`"
  while the repo's own hygiene rule states `.agents/tmp/` ships nothing.
    - _Audit:_ grep `ships|repo ships|the repo ships` across `**/*.md`; for each
      hit, confirm it is NOT a claim about THIS repo's shipped contents reaching
      a gitignored path (verify with `git check-ignore -v <path>`). Cautionary
      anti-pattern tables (e.g. "Repository → profile (wrong): the repo ships a
      dangling symlink") and illustrative Non-STE→STE example sentences are
      ACCURATE — leave them. Only correct claims that assert committed/shipped
      content living under a gitignored path.
- Repo is the source of truth; Hermes profiles symlink INTO it. Never put a
  repo→`~/.hermes` symlink in the tree.

## 3. DRY project-root derivation (NEVER count parent hops)

`<repo>/.agents/tools/lib/repo_root.py` already provides `repo_root(__file__)`
plus `ensure_inside_repo()` / `inside_repo()` guards. **98/138 scripts
previously derived the root themselves (83 by
`Path(__file__).resolve().parent.parent…`); exactly 1 used the helper.** A
script that counts `.parent` hops silently points PROJECT at an ancestor of the
repo when the file moves, and `os.makedirs` scatters output outside the checkout
— the exact bug class the jail exists to catch.

Replacement bootstrap (depth-independent, self-contained — see
`scripts/migrate_root.py`):

```python
# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
```

**PITFALLS (both hit and reverted during the real migration):**

- Do NOT inline a 19-line `_repo_root_bootstrap()` function into every file.
  That trades one duplication for another and defeats the purpose. The bootstrap
  above is 6 lines and delegates to the shared helper.
- Do NOT insert `import sys` / `from pathlib import Path` separately and then
  use `_sys`/`_Path` above the import — `NameError` at runtime. Use the
  self-contained `import sys as _sys` / `from pathlib import Path as _Path`
  aliases _inside_ the bootstrap so ordering is impossible to get wrong.
- Proof the fix works: copy a migrated file two levels deeper and assert
  `PROJECT` still resolves to the repo; the old form would point at the deeper
  dir.

## 4. Per-purpose configuration (NOT a global config)

Each unit owns `config.yaml` in its directory declaring its COMPLETE footprint:
inputs, outputs, layout/naming patterns, separators, thresholds, and agent
settings. A single file reveals everything the unit reads/writes/formats. The
loader `<repo>/.agents/tools/lib/ste_config.py` (see
`references/per-purpose-config.md`) implements:

- **Shared defaults without a global config:** `.agents/config/defaults.yaml`
  may carry ONLY the `agent:` section. The loader _rejects_ any other top-level
  key (`ConfigError`). This is the structural guarantee that shared defaults
  never silently become the global config.
- **Resolution order (lowest→highest):** defaults.yaml → unit config.yaml → env
  overrides (`STE_MODEL`, `STE_AGENT`, `STE_TIMEOUT`, opt-in) → explicit call
  args. A unit always wins over the shared default.
- **Path safety:** `CFG.path(...)` resolves relative to the repo root and runs
  `ensure_inside_repo()`, so a typo cannot send a write outside the checkout.
- **Models differ per stage** — refinement/assembly workers use
  `poolside/laguna-s-2.1:free`; extraction/adapt/extend/finalize use
  `tencent/hy3:free`. Declare the real model in each unit's `agent.model`; do
  not assume the default.

## 5. When a delegate hits rate limits (HTTP 429)

Delegates return `status=completed` while their summary is an HTTP 429 payload
and they wrote ZERO deliverables. **`completed` means the loop ended, not the
goal was met.** Do NOT re-launch delegates into the same limit.

**Fallback (deterministic, zero API calls):**

1. `ls` the delegate's scratch / `git ls-files` to confirm nothing was produced.
2. If the delegate emitted raw scan data (e.g. a JSON of file→LOC/imports),
   adopt it and finish the analysis with local Python — static scans and regex
   sweeps need no model.
3. Build the actual deliverable yourself with `execute_code` / terminal scripts.

## 6. Verification discipline

- After editing, **re-run the gate fresh** and read its real output. Do not
  reuse a prior turn's "passed" text — it can predate a later fix and be stale
  (this happened: a "passed" self-test actually had a stale assertion that a
  later poolside-override broke).
- For the refactor gate: `make check` may fail on ANOTHER session's in-flight
  edits (e.g. a half-written `test_jail.py`). Verify your own work with
  `make lint` + `python3 .agents/benchmark/selftest.py` (178/178) + the unit's
  own self-test, and state clearly what you could and could not gate.
- Prove no functionality lost: spot-import migrated modules, assert resolved
  values equal the pre-change literals, and `git ls-files` diff baseline SHA.

## 7. Commit discipline (granular, no polling)

- Commit with `git gcommit-hermes` (see `hermes-commit-workflow`). It commits
  staged files only and sweeps the whole working tree, so **stage each logical
  batch and run per batch** — split by area (benchmark / runners / per-stage),
  do NOT over-commit one giant squashed diff.
- **Kill all background processes** (delegate procs, poll loops, cron-style
  watchers) before starting; never poll/wait-block on them — keep the session
  moving and inspect via `ps`/`ls`/`log` + mtime.
- Leave another session's in-flight files alone; `git restore --staged` if a
  sweep captures them.

### THE SWEEP HAZARD (hit twice, had to fix)

`git gcommit-hermes` re-stages its OWN selection from the **whole working tree**
and commits that — it does NOT honor an index you pre-populated. When another
Hermes session is concurrently authoring and has uncommitted edits (e.g.
`.agents/hermes/jail/` while the jail session is live), those edits get **swept
into your commit under your message**. This happened twice: the sibling
session's `jail-install.sh` and profile-scaffolding landed inside commits whose
message described unrelated helper work.

**Hard rule — when `git status` shows another session's in-flight edits, do NOT
use `git gcommit-hermes`.** Use plain `git commit`:

```bash
git add <exactly-one-file>
git diff --cached --name-only      # confirm ONLY your file is staged
git commit -m "scope(subdir): short reason"
```

**If you already committed and the sweep happened (recovery, no amend):**

```bash
git reset --soft HEAD~1
git restore --staged <other-session-file>   # unstage their work
git diff --cached --name-only                # must show only your file
git commit -m "scope(subdir): short reason"  # re-commit cleanly
```

- **NEVER `git commit --amend`** — it rewrites shared history another session
  may be reading; the reset+recommit path above reaches the same result without
  rewriting the published SHA.
- One file per commit when another session is live. Each commit is verified to
  stage exactly one path before running it.

## 8. Dependency manifests (`requirements.txt`)

When this repo needs a `requirements.txt` (repo root), mirror the user's other
repos — `<repo>/Land/requirements.txt` and
`<repo>/Repository/requirements.txt`:

- **Banner-style `=== section ===` comments**, not a bare pip list.
- **Separate blocks:** `Python` (real PyPI packages pinned `pkg>=x.y.z`, or "No
  external packages required." + which stdlib modules + minimum Python version),
  `System tools` (external binaries the Makefile/scripts shell out to, with
  `macOS: brew install …` / `Linux: apt install …` hints), and
  `Node.js / pnpm ecosystem` (only if a `package.json` exists).
- **Evidence-based — never list from docs.** Only list deps actually `import`ed
  or invoked in the repo. Remote-research specs that _mention_ packages
  (openpyxl, scipy, opentelemetry, redis, …) are NOT dependencies unless code
  imports them. Scan with `grep -rhoE "^\s*(import|from) [a-zA-Z0-9_]+" .agents`
  and cross-check each module against the Python stdlib; keep only the
  third-party hits. Optional imports inside `try/except ImportError` still count
  if the code uses them.
- A repo release that _adds_ `requirements.txt` is repository-only — do not bump
  `STANDARD-*` for it (see `github-release-maintenance`).
- **Independently verify the manifest before shipping.** Do NOT trust a
  delegate's import-scan alone — tool-presence checks (`command -v`,
  `shutil.which`) and subprocess/shell invocations are often wrapped
  differently, and a bare grep for `import` can both miss real deps and
  over-count (`node` matches as an AST variable name; `curl` only appears inside
  jail test fixtures as a string to refuse). Cross-check each listed tool with
  `grep -rI` for actual invocations + install routes
  (`brew/apt/dnf/cargo/npm install …`), and confirm the `NOT required` calls
  really are only strings/tests. Count occurrences per tool to gauge
  significance.
- **Repo ships a `.venv` — do not `pip install` into system Python.** The
  checked-in `.venv` is CPython 3.14.6, and `python3` on macOS (3.9.6) is
  externally managed, so `python3 -m pip install` fails or harms system state.
  Install optional PyPI packages into the repo `.venv`
  (`source .venv/bin/activate && pip install …`). All required third-party
  packages were already verified importable in that venv.

## References

- `references/per-purpose-config.md` — ste_config.py API, defaults.yaml guard,
  how to add a unit config.
- `references/root-derivation-dry.md` — migration script recipe + the two
  reverted mistakes.
- `references/delegate-429-fallback.md` — salvage-and-finish-locally pattern
  with a real example.
- `scripts/migrate_root.py` — known-good, re-runnable root-derivation migrator.
