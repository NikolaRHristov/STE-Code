---
name: ste-code-skill-library
description: Reorganize the STE-Code Hermes skill library.
category: dev
capability: developing-and-changing-the-standard
source: .agents/skills/ste-code-dev/ste-code-skill-library
layout: ste-code-canonical-v1
---

# STE-Code Skill Library Maintenance

The STE-Code skill library lives in **`STE-Code/.agents/skills/`** and is the
single source for every STE-Code Hermes skill. Each profile
(`~/.hermes/profiles/<p>/skills/`) points at it via symlinks - during a profile
session the TUI repins `SKILLS_DIR` + `HERMES_HOME` to the profile dir, so **the
profile's `skills/` dir is the only skill source scanned** (the bundled
`~/.hermes/skills/` set is NOT consulted). Therefore: to change what a profile
loads, change `.agents/skills/` and the profile's symlinks.

## Trigger

- "reorganize the skills", "group skills by capability", "strip default Hermes
  skills", "which skills does profile X load", "consolidate these skills".
- Any task that moves/renames/rewrites skill directories or edits a profile's
  `skills/` layout.

## Workflow (do it manually - see rule below)

1. **Backup first.** Copy the current tree to `/tmp/ste-skills-backup` (or
   `.agents/tmp/`) before any destructive move:
   `cp -R STE-Code/.agents/skills /tmp/ste-skills-backup/skills`.
2. **Categorize semantically by USAGE, not by origin or literal tags.** Name a
   bucket for _when you reach for it_. The four canonical buckets (as settled
   after user corrections):
    - `ste-code-authoring` - skills that **WRITE / CHANGE the STE standard**
      (adaptation, extension-worker, refinement, translations, artifacts,
      auditing, continuation).
    - `ste-code-dev` - skills that **DEVELOP / OPERATE the agents + pipeline
      that produce it** (extraction, grouping, level-worker, execution-auditor,
      state-report, github-release-maintenance, ste-code-repo-hygiene).
    - `ste-code-benchmark` - running the adversarial benchmark.
    - `ste-code-dev` - developing the agents/tools that produced the standard
      (jail-ops, profile-confinement, agent-session-triage, poll-worker-launch).
      The split is **authoring the standard** vs **developing the agents that
      produced it** - they are NOT the same bucket; `authoring` ≠ `development`.
      Avoid narrow-action names - `release` was rejected as "too specific of an
      action"; GitHub / release ops go in `ste-code-dev`, not a `release`
      bucket. **Never use literal `-etc` suffixes** - they read as placeholders,
      not categories.
3. **Move files with terminal commands** (`mkdir -p`, `mv`, `cp -R`, `ln -s`,
   `rm -rf`), not Python scripts. See the rule below.
4. **Relink the profile.** Remove the old flat symlinks + redundant real dirs,
   then symlink each bucket dir into the profile's `skills/`:
   `ln -s STE-Code/.agents/skills/ste-code-authoring ~/.hermes/profiles/dev-ste-code/skills/ste-code-authoring`
   Hermes recurses into a symlinked bucket dir and loads each child `SKILL.md`;
   a bucket dir without its own `SKILL.md` is just a container - that's fine.
5. **Rewrite the moved `category` / `capability` / `source` frontmatter.** When
   a skill changes bucket, its YAML metadata goes stale. After the move, fix
   every `SKILL.md` in the bucket:
    - `category:` → the bucket name without the `ste-code-` prefix (`authoring`,
      `dev`, `benchmark`, `apply`).
    - `capability:` → a kebab phrase for the bucket (authoring =
      `authoring-and-changing-the-standard`; dev =
      `developing-and-changing-the-standard`; benchmark =
      `running-the-adversarial-benchmark`; apply =
      `applying-the-standard-to-a-codebase`).
    - `source:` → the new repo path (e.g. `.agents/skills/ste-code-dev/<slug>`),
      never a stale `~/.hermes/...` machine-local path. One
      `sed -i '' -e 's/^category: X$/category: Y/' ...` per field across
      `ste-code-<bucket>/*/SKILL.md` does it. (The `layout:` key stays
      `ste-code-canonical-v1`.)
6. **Run heavy reorgs as a background poll worker, not foreground.** Launch the
   move/copy as `terminal(background=true, notify_on_complete=true)` and keep
   working; poll with `process(action='poll')`. The user's standing directive:
   "recursively in a poll worker so that it doesn't interfere with your work" -
   never block on a long reorg.
7. **Verify (see references/verify.md).**

## MANDATORY RULES

### 1. File operations are manual, not scripted

Prefer terminal/CLI for moving, copying, renaming, and symlinking files (`mv`,
`cp`, `ln -s`, `rm`). **Do NOT write a Python helper script to do file
reorganization unless the user explicitly asks for one.** Hand-written scripts
for bulk file ops were rejected mid-session: "do it manually with copying files
and manually checking - don't write python scripts unless specifically asked."
Use Python/`execute_code` only for _inspection_ (reading, diffing, counting),
never as the mechanism that performs the move. (The `skill_manage` tool itself
is fine - that is not a hand-written script.)

### 2. Never simplify or lose instructions when rewriting

When consolidating or reformatting a skill, **preserve the original instruction
body verbatim**. You may normalize layout and frontmatter, but every procedural
sentence, command, and example must survive. The user's standing rule: "do not
simplify or lose their instructions." A safe check: after the move, take 8+
non-empty content lines from the source `SKILL.md` and confirm each is a
substring of the new file. 0 missing = safe.

### 3. Preserve out-of-scope artifacts

Keep any profile-local real dirs that are NOT STE-Code (e.g. `delegation/`)
unless the user says otherwise. Only remove STE skills that are now duplicated
inside a bucket.

## Pitfalls

- **Stale `-etc` dirs:** a re-run can leave old output dirs (e.g.
  `ste-code-dev-etc`) that glob patterns miss. After a reorg,
  `ls -d .agents/skills/ste-code-*-etc` and remove stragglers before trusting
  the count.
- **Doubled sub-skill slugs:** sub-skills nested under a parent get a slug like
  `github-github-release-maintenance`. Use the **leaf folder name** as the slug,
  not the relative path, to avoid the parent prefix repeating.
- **`copy_assets` "File exists":** if re-copying into a dir that already has
  `references/`, `copytree` fails. Remove the dest subdir before copying (or use
  `dirs_exist_ok`). This is why manual `mv`/`cp -R` is safer than a re-run
  script.
- **Self-improvement patches target profile-local real dirs.** Skills like
  `ste-code-jail-ops` and `hermes-profile-skill-confinement` get auto-patched in
  `~/.hermes/profiles/dev-ste-code/skills/` - they are machine-local, not in the
  repo. Promote them into `.agents/skills/` if you want them tracked; otherwise
  they vanish if the profile is wiped.
- **Concurrent committer:** another Hermes session may sweep your uncommitted
  skill files into its own commit. Stage explicitly and verify with
  `git log --oneline -1 -- <file>` that your content landed.
- **Stale frontmatter after a move.** A moved/renamed skill keeps its old
  `category:` (wrong bucket), `capability:` (wrong phrase), and `source:` (a
  stale machine-local `~/.hermes/...` path). Always rewrite these after the move
  (step 5) - a renamed skill whose `source:` still points at the old path is a
  real finding from this session.
- **Idempotent re-runs leave ghosts.** A re-run that writes `ste-code-dev-etc`
  then later `ste-code-dev` leaves the `-etc` dir behind (glob cleanup only
  matched `-*` names). Before trusting the final count,
  `ls -d .agents/skills/ste-code-*-etc` and remove stragglers.

## Pitfalls

- **`skill_manage(action='create')` frontmatter is strict.** The `description:`
  field has a small budget (~60 chars), must be trigger-first, and must end with
  a period; YAML parsing FAILS if it contains `->` arrows, unescaped colons, or
  runs long (the `iterative-diff-research` create failed 3× before the
  description fit). Keep the description to one short sentence; put all detail
  in the SKILL.md body. If a create returns a YAML/char error, trim the
  description first.

## Pitfalls (skill hygiene - added after the dead-reference cleanup)

- **Verify a referenced doc actually exists before keeping a MANDATORY
  cross-reference.** Skills across all buckets carried
  `> **MANDATORY**: Read .agents/skills/OPERATING_PRINCIPLES.md before any work.`
  even though that file does not exist anywhere in the repo. A skill that points
  at a missing file trains the next session to fail open. Before adding a
  `MANDATORY`/doc reference, `search_files` for the target path; remove dangling
  references. When scrubbing, also fix `rule`/`Pitfalls` text that tells the
  reader to _preserve_ a file that does not exist.
- **Benchmark skills must describe GOAL + HOW-TO, not the environment they run
  in.** The `ste-code-benchmark/*` bucket executes _inside_ the confinement, but
  its skill text must stay at the level of "what to build/verify and the
  commands to run." Strip jail/Seatbelt/`STE_CODE_JAIL_POLICY`/`policy.py`/
  `_STRICT_FALLBACK`/`PYTHONPYCACHEPREFIX`/`dev`/`bench` profile names, and
  "sandbox reads the policy map" prose. Keep confinement/environment detail in
  `ste-code-dev/*` (jail-ops, profile-confinement), where it belongs - a
  benchmark skill that leaks the cage teaches the adversarial runner to reason
  about its own jail. (Harness _tooling_ may still be told to "compile
  in-process so it is environment-independent" - that is a portability rule, not
  a jail disclosure.)

## Verification

See `references/verify.md` for the exact commands:
`env HERMES_PROFILE=<p> HERMES_HOME=~/.hermes/profiles/<p> hermes skills list --enabled-only`
must list every expected skill under its bucket, and a body spot-diff must show
0 missing instruction lines. Also run `make check`.

## Overlap

`hermes-profile-skill-confinement` covers the _goal_ (a profile must load only
the chosen set, no default bundled skills). This skill covers the _mechanics_ of
reorganizing the library layout. They are complementary, not duplicates.
