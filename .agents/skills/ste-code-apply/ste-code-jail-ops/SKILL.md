---
name: ste-code-jail-ops
description: Maintain the jail that confines the three STE-Code Hermes profiles. The jail
category: apply
capability: applying-the-standard-to-a-codebase
source: /Users/nikola/.hermes/profiles/dev-ste-code/skills/ste-code/ste-code-jail-ops
layout: ste-code-canonical-v1
---


# STE-Code Jail Ops

Maintain the jail that confines the three STE-Code Hermes profiles. The jail
source lives at `.agents/hermes/jail/` (single source); it is exposed as the
grouped plugin `ste-code-jail` (components: `jail-fs`, `jail-cmd`, `jail-net`,
`jail-exec-wrap`).

## When to use
- Adding or reworking a profile (`dev-ste-code`, `ste-code`, `benchmark-ste-code`).
- Closing a confinement gap — a way out of the jail an adversarial prompt found.
- Making a locked profile spawn sessions that stay confined (`benchmark-ste-code` → per-stage sessions).
- Stripping default Hermes skills so a profile loads only STE-Code skills.
- Verifying the jail after any policy/plugin change.

## The confinement model — 5 layers
| # | Layer | Enforced by | Classic gap |
|---|---|---|---|
| 1 | Session tool calls | `jail-fs` arg inspection | (solid) |
| 2 | Opaque subprocess (`python3 build.py`) | `jail-exec-wrap` → kernel sandbox (Seatbelt/bwrap) | **WAS OPEN**: bare `python3` escaped arg inspection |
| 3 | In-session re-read | policy cached at session start | warm-restart after an edit |
| 4 | Inside a tool call | `jail-cmd` basename deny-list | only ~30 cmds; widen as needed |
| 5 | LLM session launched from inside | `AGENT_SPAWN_COMMANDS` deny + force-confine | `hermes` binary **WAS allowed** → unjailed child |

Proven facts (see `references/confinement-layers.md`):
- `pre_tool_call` hooks receive the **same `args` dict** the executor later runs; mutating it in place rewrites the command. Verified, not assumed.
- Policy is derived from the **PROFILE NAME**, not `$HERMES_HOME`. A bench run launched from a dev shell inherited the dev profile dir → fixed by `profile_home()`.
- Profile **control surface** (`config.yaml`, `hooks/`, `plugins/`, `skills/`, `cron/`, `auth.json`) is denied even inside the writable profile, else a locked session rewrites its own cage then restarts unconfined.
- Force-confine spawns: `jail-exec-wrap` sets `STE_CODE_JAIL_POLICY` + `HERMES_PROFILE` on every child `terminal` call, so `benchmark-ste-code` may `delegate_task` while children stay `bench`.

## Profile single-source model
Profile content lives in `.agents/hermes/profiles/<name>/` and is **symlinked into `~/.hermes/profiles/<name>/` per-profile** (NOT the whole dir). See `references/profile-layout.md`.
- Product files (`config.yaml`, `SOUL.md`, `profile.yaml`, `skills/*`) = symlinks to repo.
- Runtime state (`.db`, `cache/`, `logs/`, `.env`) = local only; covered by `.gitignore` in the source.
- Installer `scripts/jail-install.sh --status` links sources; it **backs up** a live file before replacing it (`.bak`) so an in-flight session is not clobbered.

## Stripping default Hermes skills
During a profile session the TUI repins `SKILLS_DIR` (and `HERMES_HOME`) to
`profile_dir/skills`, so that dir is the **ONLY** skill source — `~/.hermes/skills/`
(the ~78 bundled defaults) is NOT scanned. Therefore "only STE-Code skills" =
make `profile_dir/skills/` contain only STE symlinks (into `.agents/skills/`).
- Verify at runtime (NOT static): `env -u HERMES_HOME HERMES_PROFILE=<p> HERMES_HOME=~/.hermes/profiles/<p> hermes skills list --enabled-only` — expect 0 builtin, only STE names.
- See `scripts/verify_profile_skills.py` for a read-only check.

## Verify after ANY change
- `make check` — the gate (178 checks + all 3 policies pass).
- `python3 .agents/hermes/jail/tests/test_jail.py` — adversarial suite (bench: 20 allow / 49 escape; user: 14/48; dev: 24/37).
- `hermes skills list --enabled-only` per profile — confirms the skill strip.
- Confirm a locked profile cannot defeat its own cage: under `STE_CODE_JAIL_POLICY=bench HERMES_PROFILE=benchmark-ste-code`, `jail-exec.sh /bin/sh -c 'rm -f "$HOME/.hermes/profiles/benchmark-ste-code/plugins/ste-code-jail"'` must return `Operation not permitted`; same for writing `config.yaml` or any file under `plugins/`. This proves the deny-path, not just the symlink.

## Pitfalls
- **Only the `dev` (parent) profile may (re)install the jail.** `jail-install.sh --all`/`install` writes into `<hermes>/profiles`, a root granted ONLY under `_build_dev`. A `bench`/`user` session has no profiles-root write access, and its `PROFILE_CONTROL_SUBDIRS` deny (config.yaml, hooks, plugins, skills) means it cannot even touch its own cage — so a confined session is structurally unable to install, relink, repair, or disable the jail. Treat `jail-install.sh` as a TRUSTED SETUP action run only by a parent (dev) session; never let a confined session run it. A confined session may run only read-only probes: `jail-install.sh --status` and `jail-exec.sh --check`/`--show` (they change nothing). After any dev-side (re)install, verify with `--status` + `jail-exec.sh --check` under `STE_CODE_JAIL_POLICY=bench`.
- **Concurrent-committer commit hazard.** `git gcommit-hermes` is the `Save`
  binary: it auto-stages untracked/modified files AND `git reset`s the index on
  failure, so it sweeps the OTHER agent's live work into your commit or silently
  drops yours. On a shared tree, stage only your exact files and `git commit -m`
  directly (mirror the repo's Conventional Commit style); reserve `gcommit-hermes`
  for quiet periods. See `references/gcommit-hazard.md`.
- **Do NOT re-split commits the concurrent committer already swept.** When another
  session's `gcommit-hermes` lands your staged work inside its own commit (e.g.
  `jail-install.sh` ending up in `2fbf541`), leave it. Rewriting history to
  re-attribute (`rebase` / `--amend` / `filter-repo`) risks clobbering that
  agent's in-flight files. Confirm your code is present with `git show <sha> --
  <file>` and move on. The user has explicitly said "don't split".
- Do NOT set `STE_CODE_JAIL_POLICY` from an inherited `$HERMES_HOME` alone — derive the profile dir from the profile NAME (`profile_home()`).
- Do NOT leave `execute_code` allowed under a wrapped policy — it runs in-process, cannot be kernel-confined. Block it; tell the user to use `terminal`.
- Do NOT wrap `dev` — authoring must build/install across the tree.
- A running session caches its policy at startup; verify a fix in a FRESH subprocess (`jail-install.sh --status` or a new `hermes` invocation), never in-session.
- The installer auto-creates a profile ONLY if it has a source dir; profiles with machine-local state (`dev-ste-code`) are created by `hermes profile create`.
- When stripping skills, MOVE default dirs to a backup outside the repo (e.g. `/tmp`); never delete — they may be needed.

## User preferences (this repo)
- Profiles: source in `.agents/hermes/profiles/`, symlinked per-profile into `~/.hermes/profiles/`. Never symlink the whole dir.
- Git-ignore runtime state for every profile.
- `benchmark-ste-code` may spawn adversarial sessions (`delegate_task`/`cronjob` are
  ALLOWED, force-confined via `jail-exec-wrap` setting `STE_CODE_JAIL_POLICY=bench`
  on every child) and rewrite the WHOLE `.agents/benchmark/` tree (harness,
  attacks, results) — not just `tests/`. `ste-code/` stays read-only via
  most-specific-match-wins in the write roots.
- Work in background + poll; never long foreground sleep/wait blockers.
