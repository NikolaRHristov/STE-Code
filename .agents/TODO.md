# TODO — jail rollout

Handover between `dev-ste-code` sessions. Everything below is verified state,
not intention. Commands run from the repository root.

Architecture and reasoning: [`docs/architecture-profiles-and-jail.md`](../docs/architecture-profiles-and-jail.md).

---

## Done

| | Evidence |
|---|---|
| `dev` / `user` / `bench` policies, name-derived, fail closed | `.agents/hermes/jail/core/policy.py` |
| Argument inspection blocks before approvals | `make check` → 178/178 |
| Kernel layer | `jail-exec.sh --check` → ok |
| Live-session harness with canary-file evidence | `scripts/live-jail-test.sh --all` |
| Profiles hold symlinks back to this repository | `jail-install.sh --status` |
| Installer links **and enables** the plugin | `--status` reports enablement |

Profiles now on disk: `dev-ste-code` (authoring, live) and
`benchmark-ste-code` (blank, `bench` policy). The `ste-code` consumer profile
has been removed — recreate it from clean when the product ships:

```bash
hermes profile create ste-code --no-skills
.agents/hermes/jail/scripts/jail-install.sh ste-code
```

---

## 1. Retire the v1 plugin

Two generations exist:

```
.agents/hermes/plugins/ste-code-jail/    v1 — superseded, no profile links it
.agents/hermes/jail/                     v2 — single source of truth
```

v2 is what both profiles link to and what the `Makefile` tests. v1 is dead
weight, but **confirm no session is working from it before deleting** — the
directory name is close enough to v2's that a careless removal reads as an
attack on the live jail.

```bash
git rm -r .agents/hermes/plugins/ste-code-jail
make check          # must stay green
```

---

## 2. Migrate pipeline scripts off hop counting

The jail is a backstop; this is the actual fix. **79** path derivations under
`.agents/tools/` still compute the root by counting parent hops:

```python
PROJECT = Path(__file__).resolve().parent.parent.parent   # fragile
```

They are all *currently* correct, which is what makes them dangerous — the
bug appears only when a file moves. Replace with the marker walk:

```python
from lib.repo_root import repo_root, ensure_inside_repo
PROJECT = repo_root(__file__)
ensure_inside_repo(target)        # raises before a bad makedirs
```

`.agents/tools/lib/repo_root.py` exists and is tested. Mechanical, but it
touches many files — give it its own commit.

Recount before starting:

```bash
grep -rl "parent\.parent\.parent\|parents\[[0-9]\]" .agents/tools --include=*.py | wc -l
```

---

## 3. Wrap pipeline stages in the kernel jail

Argument inspection cannot see inside `python3 build.py`. No runner is
wrapped yet:

```bash
grep -rln "jail-exec" .agents/tools/runners/ .agents/benchmark/*.py   # currently empty
```

Benchmark runners are the priority — they execute adversarially generated
prompts by design.

```bash
.agents/hermes/jail/scripts/jail-exec.sh python3 .agents/benchmark/orchestrator.py
```

---

## Rules that produced this work

**Never derive a path by counting parent hops.** The jail's own first draft
broke this rule, loaded zero components, and reported every escape as blocked
while blocking nothing. The test suite caught it.

**Never delete a case from the escape suite.** Add one whenever a new bypass
is imagined. The first adversarial run found 14 holes in an implementation
that had passed a happy-path suite.

**A test that cannot fail proves nothing.** The live harness once scored a
vacuous pass on every case because the platform shipped no `timeout` binary:
the agent never launched, no canary appeared, and "no file" was read as
success.

**A running session caches its policy at start.** After editing
`core/policy.py`, your own session still enforces the old rules. Verify in a
fresh process; do not read a stale refusal as a failed fix.
