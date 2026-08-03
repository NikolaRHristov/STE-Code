---
name: ste-code-profile-wiring
description: >-
    Wire profiles to a single-source via two-level symlinks.
---

# STE-Code profile single-source wiring

## When to use

- Adding a new `link-<thing>.sh` that makes a repo directory the single source
  of truth for every STE profile (skills, memory, hooks, or a future thing).
- Auditing or repairing the existing linkers in `.agents/hermes/`:
  `link-skills.sh`, `link-memory.sh`, `link-hooks.sh`.
- The user says "do it like we did skills" / "link-X like hooks/memory" / a
  profile is loading local `~/.hermes/` content instead of the repo.

## The convention (verified pattern)

Three linkers live in `.agents/hermes/`:

- `link-skills.sh` — skill buckets (per-profile _selected_ subsets).
- `link-memory.sh` — `USER.md` / `MEMORY.md` per profile.
- `link-hooks.sh` — a flat hook dir _shared_ by all profiles.

All three use the SAME two-level relative symlink chain:

```
REPO single source                  e.g. .agents/hermes/hooks/      (real files, tracked)
   ^  .agents/hermes/profiles/<p>/<thing>   (level-1 pointer, tracked symlink)
          ^  ~/.hermes/profiles/<p>/<thing> (level-2, live profile — what Hermes loads)
```

- Level-1 target is a **relative** symlink (relocatable repo).
- Level-2 points at the level-1 pointer (also relative).
- The global agent dir `~/.hermes/hermes-agent/hooks` is a SEPARATE symlink
  **→** the same canonical; it is NOT the source. If you find local `~/.hermes/`
  files leaking into a profile, the fix is to **LINK the profile dir**, not to
  unlink the global (see Pitfalls #5).

`install.sh` runs all three linkers (`--all`); the `Makefile` exposes
`skills-link`/`skills-check`, `memory-link`/`memory-check`,
`hooks-link`/`hooks-check` for each.

## Steps to add a new linker (e.g. `link-foo.sh`)

1. Copy the skeleton in `templates/link-SKELETON.sh`. Replace every `<thing>`.
2. `SOURCE="$REPO/hermes/foo"` — a real, tracked dir holding the content.
3. `link_dir dest src` — **refuse to replace a NON-EMPTY real dir** (only
   replace EMPTY real dirs); otherwise
   `ln -sfn "$(relpath "$dest" "$src")" "$dest"`.
4. `install_profile` links level-1 (profile repo dir → SOURCE) then level-2
   (live profile → level-1). See Pitfall #2 for the dry-run-safe ordering.
5. Wire `install.sh` (add the third `bash link-foo.sh --all $DRY` / `--status`
   line) and the `Makefile` (`FOO_LINK` var + `foo-link` / `foo-check` targets).
6. Add a `!foo` exception to **every** profile `.gitignore`
   (`.agents/hermes/profiles/<p>/.gitignore`) so the pointer symlink is TRACKED
   — the bare `foo/` entry ignores it. Also add a `# NOTE:` line.

## Pitfalls (verified this session — 2026-08-03)

1. **Status glob must match the dir itself.** A `case "$rt" in "$SOURCE"/*)`
   only matches children of the source, not the source dir when a symlink points
   AT it. Use `"$SOURCE" | "$SOURCE"/*`, or `show_status` reports a false
   `WRONG TARGET` even though the link is correct.

2. **Dry-run "source missing" for level-2.** Level-2's source is the level-1
   pointer, which the run creates. In `--dry-run` (no writes) level-1 doesn't
   exist yet, so `link_dir "$l2" "$l1"` fails with "source missing." Fix:
   `if [ -e "$l1" ]; then link_dir "$l2" "$l1"; else link_dir "$l2" "$SOURCE"; fi`
   — compute level-2 against the canonical when the pointer isn't present.

3. **`git check-ignore` lies for symlink-to-dir.**
   `git check-ignore .agents/hermes/profiles/<p>/foo` still reports "ignored"
   even with a `!foo` negation, because the dir-style pattern matches the
   symlink and negation-on-symlink ordering is finicky. Don't trust it. Verify
   the pointer is tracked with `git ls-files --cached -s <path>` → mode `120000`
   (symlink), and `git status --short` shows `A`. Confirm NO real files leaked
   with `git ls-files --cached | grep 'profiles/.*/foo/' | grep -v '/foo$'`
   (expect empty).

4. **Empty real dirs are safe to replace; non-empty are not.** Hermes may create
   an empty `hooks/` at runtime. `link_dir` should `rmdir` an empty real dir but
   REFUSE (skip) a non-empty one so authored runtime content is never clobbered.

5. **The premise can be inverted — check inodes first.** Before "unlinking"
   anything, check inodes: `stat -f '%i'` on the canonical file vs the profile
   copy. If they share an inode, the profile already reads the repo through a
   link — no unlink needed. In this session the user assumed hooks were linked
   repo→global; actually the global was a symlink **→** the repo, and the
   profiles were simply _unlinked_ (empty real dirs). The fix was to LINK the
   profiles, not unlink the global.

## Verification (run after any linker change)

- `bash link-foo.sh --status` → every profile `ok`, global agent `ok`, zero
  `WRONG` / `absent`.
- `bash link-foo.sh --all` again → idempotent (`= ` unchanged).
- `make check` still green (the linkers are not gated by it, but confirm no
  regression in the surrounding tree).
- `git ls-files --cached -s .agents/hermes/profiles/<p>/foo` shows `120000`.

## Relationship to other skills

- `ste-code-repo-hygiene` — formatting / link-checking / release-notes hygiene
  (a different concern; this skill is about _how the files get wired in_).
- `hermes-profile-skill-confinement` — _which_ skills a profile loads; this
  skill is about _how the files get there_.

## Promotion note

New skills created via `skill_manage` land in the live profile dir
(`~/.hermes/profiles/dev-ste-code/skills/`). To enter the single-source
distribution, also place it under `.agents/skills/<bucket>/` and let
`link-skills.sh` symlink it — otherwise it is a real dir, not a symlink, and
drifts from the repo.

## Support files

- `references/link-SKELETON.sh` — copy this, replace every `<thing>`, and wire
  it into `install.sh` + `Makefile` to add a new profile linker. Embeds all five
  pitfalls from above.
