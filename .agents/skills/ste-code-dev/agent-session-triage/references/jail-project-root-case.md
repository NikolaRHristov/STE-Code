# Jail project-root case (worked example)

Companion to the `agent-session-triage` skill - a concrete, verified instance of
the "looping session reports it cannot locate the repo" class.

## Symptom

A dev session reports "the jail cannot locate the STE-Code repo" / "every write is
blocked as outside the allowed roots". The instinct is to hunt for a stale
installed copy of `policy.py` or a wrong `cfg` path. **In the instance that
produced this note, that instinct was wrong.**

## The false premise (proven false)

The dev policy derived its write roots from a project root discovered by walking
up from the process cwd to a `.git`/`Makefile` marker. The theory: a session
spawned with `cwd=~/.hermes` found no marker → `project_root=None` → the repo
dropped from the write roots.

Verify the premise before investigating it. Evaluating `load_context()` directly:

```
project_root: /Volumes/CORSAIR/.../STE-Code
policy: dev
write_roots: [repo, profile, profiles, /tmp, ...]
```

The anchored resolver (`resolve_project_root_anchored`) was already landing on the
repo. The premise was false; every downstream step (searching for duplicate
`policy.py`, diffing jail configs) was wasted.

## The real cause in the live stuck sessions

They were **benchmark** sessions whose `HERMES_HOME` had been inherited as
`benchmark-ste-code` (env leak from a parent dev shell). Under the `bench` policy
the STE-Code checkout is **read-only by design** - so "cannot write to the repo"
was *correct* behaviour, not a bug. The fix was to launch with the intended
profile (`HERMES_PROFILE` + `HERMES_HOME` set to the dev profile), not to change
any code.

## The read-only jail-context probe

Use this to confirm the resolved policy/roots of a live or fresh session without
guessing. It reads `core.policy.load_context()` exactly as the jail does - no
in-session caching, no cwd assumptions:

```bash
python3 .agents/skills/ste-code-dev/agent-session-triage/scripts/show_jail_context.py
```

Or inline:

```python
import os, sys
sys.path.insert(0, ".agents/hermes/jail")
import core.policy as p
ctx = p.load_context()
print(ctx.profile, ctx.policy.name, ctx.project_root)
for r in ctx.policy.write_roots: print("  write:", r)
for r in ctx.policy.deny_roots:  print("  deny: ", r)
```

A session that prints `policy=dev write_roots=6 network=allowed` and lists the
repo under `write:` is healthy. Anything else is an **environment** problem
(wrong `HERMES_HOME`/`HERMES_PROFILE`), resolved by relaunching with the correct
profile - never by editing `policy.py`.
