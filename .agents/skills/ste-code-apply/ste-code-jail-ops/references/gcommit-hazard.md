# `git gcommit-hermes` hazard under a concurrent committer

`gcommit-hermes` is an alias for the `Save` binary
(`~/Developer/Maintain/Save/Target/release/Save`), not plain `git commit`. It
auto-generates a Conventional Commit message.

## Observed behavior (verified this session)

- It commits the **staged index** ("Executing 'git commit -F -'"), BUT it also
  **auto-stages untracked AND modified-but-unstaged files** before committing.
  A run with only `jail-install.sh` staged swept in an unrelated `refine_batch.py`
  that another agent had modified.
- On its internal failure path it runs **`git reset` and wipes the staged
  index** without committing. Multiple runs here lost my staged `jail-install.sh`.
- The repo has a **concurrent external committer** that auto-commits mid-session
  (often empty/auto messages), sweeping in-flight staged/untracked files into ITS
  commit. So `gcommit-hermes` output is also unreliable as proof of what was
  committed.

## Safe pattern when concurrency is active

1. `git reset -q HEAD .` to clear any foreign staging.
2. `git add <exact/path>` — only your file(s), never `.` or `-A`.
3. `git commit -m "feat(jail): <conventional message>"` directly (mirror the
   repo's existing Conventional Commit style; the `Save` binary only generates
   this text).
4. Immediately verify: `git status --short` (must be clean except the OTHER
   agent's live files) and `git log --oneline -1` (your SHA).
5. Re-run `make check` to confirm nothing regressed.

Reserve `gcommit-hermes` for quiet periods (no other agent modifying the tree),
or when you specifically want the auto-generated message and the tree holds only
your changes.
