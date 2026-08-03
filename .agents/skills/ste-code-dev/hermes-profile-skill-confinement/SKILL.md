---
name: hermes-profile-skill-confinement
description:
    Confine a Hermes profile to a chosen skill set; block default bundled
    skills.
category: dev
capability: developing-the-standard
source: <home>/.hermes/profiles/dev-ste-code/skills/ste-code-dev/hermes-profile-skill-confinement
layout: ste-code-canonical-v1
---

# Confine a Hermes profile to a specific skill set

## When to use

A Hermes profile must load ONLY a chosen skill set and NO default bundled Hermes
skills (e.g. STE-Code authoring/benchmark/consumer profiles).

## Mechanism (verified in Hermes source)

- `hermes_cli/web_server.py:13352` repins at profile-session start:
  `SKILLS_DIR = profile_dir/"skills"` and `HERMES_HOME = profile_dir`.
- `agent/skill_commands.py` scans ONLY `SKILLS_DIR` (+ `skills.external_dirs`
  from config), NOT the global `~/.hermes/skills/`.
- So the profile `skills/` dir is the SOLE source while that profile is active.
  Make it hold only symlinks to your chosen skills and NO default skill can
  load.

## Procedure

1. Canonical source: `REPO/.agents/skills/<name>` (+ the consumer skill
   `ste-code-consumer/apply-standard`).
2. Per profile `skills/` dir:
    - KEEP state files: `.bundled_manifest`, `.usage.json`, `.usage.json.lock`,
      `.hub/`.
    - For each desired skill: symlink `skills/<name> -> <source>/<name>`.
    - REMOVE (MOVE to `/tmp/<backup>/<profile>/`, never delete) default real
      dirs (apple, creative, email, media, mlops, note-taking, productivity,
      research, smart-home, social-media, software-development).
    - Remove stale/wrong symlinks; create missing wanted symlinks.

## Pitfalls

- LIVE sessions regenerate `skills/` (e.g. `dev-ste-code/skills/ste-code/` came
  back with `ste-code-jail-ops`, `ste-code-repo-hygiene`). Re-strip only after
  the session goes quiet. If the user explicitly says to leave a regenerated
  real dir as-is (their active work), do NOT re-symlink it - it is legit STE
  work, just not yet single-sourced.
- Do NOT prune `~/.hermes/skills/` (global, shared). Confinement is per-profile.
- `github-release-maintenance`, `ste-code-continuation`, `ste-code-validate`,
  `adversarial-benchmark-harness`, `gated-batch-orchestration`, `link-checking`,
  `pipeline-output-attribution` are SUB-SKILLS inside parent STE skills
  (`github`, `continuation`, `validation`); `hermes skills list` flattens them.

## Verification (runtime, not static)

```
env -u HERMES_HOME HERMES_PROFILE=<p> HERMES_HOME=~/.hermes/profiles/<p> \
  hermes skills list --enabled-only
```

Confirm zero default skills, only intended STE skills. Static `ls` is NOT enough

- a live session can change what resolves.
