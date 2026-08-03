# Project-root resolution (worked STE-Code case)

The jail must resolve the STE-Code repo (its write root) **independent of the
process working directory**. This note records the verified behaviour and the
two real failure modes, so a future session does not re-derive the wrong theory.

## The invariant

`core/policy.py:resolve_project_root_anchored()` is the live path. It anchors to
`policy.py`'s own location:

```
parents[0] = core/
parents[1] = jail/
parents[2] = hermes/
parents[3] = .agents/
parents[4] = <repo>        # the STE-Code checkout
```

If `<repo>/.git` or `<repo>/Makefile` exists, it returns that path. Only if the
core is imported from _outside_ a checkout (unit tests) does it fall back to a
`cwd` walk via `resolve_project_root(os.getcwd())`.

`load_context()` calls it first:

```python
project_root = (
    cfg.get("project_root")
    or resolve_project_root_anchored()      # cwd-independent
    or resolve_project_root(os.getcwd(), ...)  # fallback only
)
```

## Verified behaviour

With `HERMES_HOME=~/.hermes/profiles/dev-ste-code` and
`HERMES_PROFILE=dev-ste-code`, a direct evaluation returns:

```
profile: dev-ste-code
policy: dev
write_roots:
  <repo>                                    (the STE-Code checkout)
  <user-home>/.hermes/profiles/dev-ste-code
  <user-home>/.hermes/profiles            (dev may provision siblings)
  /private/tmp
  /private/var/folders/...
deny_roots:
  <repo-parent>                            (repo PARENT)
  <repo>/.git
```

So the dev profile correctly lists the repo as a write root **whatever the cwd
of the session** - including a `hermes -z` child spawned with `cwd=~/.hermes`.

## Failure mode A - wrong profile via inherited env (NOT a code bug)

A session pointed at the _wrong_ profile behaves identically to a session
hitting a _code_ bug. The two stuck benchmark sessions reported "cannot write to
the repo" while **already carrying the anchored fix**: their `HERMES_HOME` was
inherited as `benchmark-ste-code`, so they resolved to the `bench` policy, under
which the repo is read-only _by design_. Fix = launch with the intended profile:

```bash
env -u HERMES_HOME \
	HERMES_PROFILE=dev-ste-code \
	HERMES_HOME=~/.hermes/profiles/dev-ste-code \
	hermes --tui
```

A healthy dev session logs: `profile=dev ... write_roots=6 network=allowed`.

## Failure mode B - stale bytecode (transient)

A process started _before_ an edit holds the old module in memory; plugins
import once at registration and `load_context()` caches the result in
`_context_cache`. Re-reading the file changes nothing for a live process. A
restart clears it. Always verify a fix in a FRESH subprocess
(`jail-install.sh --status` or a new `hermes` invocation), never in-session.

## Why this is the right design (not a hack)

Counting parent hops (`parent.parent.parent`) silently encodes the file's depth
in the tree; moving the file repoints the root to an ancestor of the repo where
`makedirs` builds a stray tree without complaint. The marker walk is the rule
everywhere in this jail and pipeline (`repo_root()` in
`.agents/tools/lib/repo_root.py`).
