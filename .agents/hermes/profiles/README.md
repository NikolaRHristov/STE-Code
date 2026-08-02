# Hermes profiles

Profile sources for this repository. Each subdirectory is the **single source**
for one Hermes profile: `~/.hermes/profiles/<name>` holds symlinks that point
back here, so editing a file in this tree changes the live profile and no copy
can drift.

Install with `.agents/hermes/jail/scripts/jail-install.sh`.

## Profiles

| Profile | Policy | Source | Purpose |
|---------|--------|--------|---------|
| `dev-ste-code` | `dev` | not in this tree | Author the methodology. Writes across the repository and the Hermes profile. This is the profile the pipeline runs from |
| `ste-code` | `user` | `profiles/ste-code/` | The consumer view. Read the standard and the artifacts, then write documentation in **your own** repository. The STE-Code checkout is read-only |
| `benchmark-ste-code` | `bench` | not in this tree | Adversarial benchmark runs. Writes confined to the benchmark output tree |

`dev-ste-code` is not tracked here: it holds machine-local authoring state
(session database, caches, credentials) that must not enter the repository.
Only profiles whose content is part of the product live in this tree.

## Why the profile lives in the repository

A profile that is copied into `~/.hermes` drifts: fix a skill in the repository
and the live profile keeps the old text. Every profile file that belongs to the
product is therefore stored here and symlinked out.

The rule the installer applies:

| Content | Where it lives | Why |
|---------|----------------|-----|
| `config.yaml`, `SOUL.md`, `skills/` | this tree, symlinked out | Product content. Reviewable, versioned, shared |
| `.env`, `auth.json` | `~/.hermes`, symlinked in | Credentials. Never in the repository |
| `logs/`, `cache/`, `state.db` | `~/.hermes` only | Machine-local runtime state |

## The `ste-code` profile

`ste-code` is **not** the old development profile. That profile was renamed to
`dev-ste-code`. `ste-code` is a new, separate profile that models how an
ordinary Hermes user works with this repository:

- Read the standard, the rules, and the level artifacts.
- Apply them to documentation in a **different** repository.
- Never write into the STE-Code checkout.

The `user` jail policy enforces exactly that. See
`.agents/hermes/jail/core/policy.py`.

## Install

```bash
# link every profile that has a source in this tree
bash .agents/hermes/jail/scripts/jail-install.sh --all

# one profile
bash .agents/hermes/jail/scripts/jail-install.sh ste-code

# check what is linked, and whether the jail is actually enabled
bash .agents/hermes/jail/scripts/jail-install.sh --status
```

## Launch a session in a profile

Set both variables. `HERMES_PROFILE` is the source of truth for the jail
policy; `HERMES_HOME` is what Hermes itself reads. Clear any inherited value
first, because a stale `HERMES_HOME` from a parent shell otherwise wins:

```bash
env -u HERMES_HOME \
    HERMES_PROFILE=ste-code \
    HERMES_HOME=~/.hermes/profiles/ste-code \
    hermes --tui
```
