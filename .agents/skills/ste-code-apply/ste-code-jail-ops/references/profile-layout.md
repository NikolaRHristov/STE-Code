# Profile single-source layout

Every STE-Code profile is sourced from `.agents/hermes/profiles/<name>/` in the
repo and symlinked PER-PROFILE into `~/.hermes/profiles/<name>/`. Never symlink
the whole dir — runtime state must stay local.

## Layout per profile source (in repo)
```
.agents/hermes/profiles/<name>/
  config.yaml            -> symlinked out (product content)
  SOUL.md                -> symlinked out
  profile.yaml           -> symlinked out
  .gitignore             -> excludes state: *.db, cache/, logs/, .env, auth*
  skills/
    <ste-skill>          -> symlink into ../../skills/<ste-skill> (or repo)
  (benchmark-ste-code) .no-bundled-skills
```

## Live profile after install (`~/.hermes/profiles/<name>/`)
- `config.yaml`, `SOUL.md`, `profile.yaml`, `skills/*` = symlinks → repo
- `.env` = symlink → `~/.hermes/.env` (credentials, never in repo)
- `*.db`, `cache/`, `logs/`, `state.db*`, `sessions/`, `*.cache.json` = REAL (gitignored)

## Installer behaviour (`scripts/jail-install.sh`)
- `jail-install.sh <name>` links the source; if the live profile lacks a source
  dir it auto-creates the dir, but profiles with machine-local state
  (`dev-ste-code`) must be created by `hermes profile create` first.
- For each source entry: if a real file/dir already exists live, it is **backed
  up** to `<entry>.bak` (once) then replaced with the symlink — in-flight
  sessions are not clobbered.
- `--status` prints what is linked and whether the jail is enabled.

## Launch a profile correctly
```bash
env -u HERMES_HOME \
    HERMES_PROFILE=<name> \
    HERMES_HOME=~/.hermes/profiles/<name> \
    hermes --tui
```
`env -u HERMES_HOME` clears any stale value inherited from a parent shell
(this is exactly the leak that pointed a bench run at the dev profile).

## bench is special
- Writes confined to `.agents/benchmark/` (nested under repo → beats repo deny).
- May `delegate_task`/`cronjob` (force-confined to `bench` by jail-exec-wrap).
- `ste-code/` stays read-only — it runs, not develops, the standard.
