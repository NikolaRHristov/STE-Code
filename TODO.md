# TODO — finish the jail rollout

Read this **fully** before touching anything. Written by the session that
built the jail, for the `dev-ste-code` session that continues the work.

Everything below is verified state, not intention. Commands are runnable as
written from the repository root.

---

## 0. Where things stand

`dev-ste-code` is a **copy** of `ste-code`, not a rename. Both profiles exist
and are byte-identical apart from three repointed LSP symlinks.

| | files | dirs | links | size |
|---|---|---|---|---|
| `ste-code` | 10018 | 1480 | 34 | 553M |
| `dev-ste-code` | 10018 | 1480 | 34 | 553M |

Backup before any of this:
`.agents/tmp/backups/ste-code-profile-prerename.tar.gz` (136M, verified).

Copy was chosen over rename so the session that built this could keep running
while you restart into the new profile. **Nothing has been deleted.**

Jail state:

```
dev-ste-code        ✓ ste-code-jail -> single source     policy: dev
ste-code            ✗ no jail plugin linked              policy: user
benchmark-ste-code    NOT CREATED                        policy: bench
```

Verified working: `108/108` test cases, kernel layer green on all three
policies, and a live `--yolo` session in `dev-ste-code` was refused a write to
`/Users/nikola/Documents/`.

---

## 1. Confirm the new profile before trusting it

```bash
hermes profile list                     # dev-ste-code present
.agents/hermes/jail/scripts/jail-install.sh --status
python3 .agents/hermes/jail/tests/test_jail.py
.agents/hermes/jail/scripts/jail-exec.sh --check
make check
```

Expect `108/108`, `jail-exec: ok`, and `make check` green.

Sanity-check that the copy carried your data across — sessions, memories,
skills, cron:

```bash
ls ~/.hermes/profiles/dev-ste-code/{sessions,memories,skills,cron} | head
```

---

## 2. Create `benchmark-ste-code`

Not yet created. It must NOT be a clone of the dev profile — benchmarks run
adversarial prompts and should start from a clean, minimal profile.

```bash
hermes profile create benchmark-ste-code --no-skills
.agents/hermes/jail/scripts/jail-install.sh benchmark-ste-code
.agents/hermes/jail/scripts/jail-install.sh --status
```

Then verify the policy resolves to `bench` and writes land only in the
benchmark output tree:

```bash
HERMES_HOME=~/.hermes/profiles/benchmark-ste-code \
  python3 -c "import sys; sys.path.insert(0,'.agents/hermes/jail'); \
  from core.policy import load_context; c=load_context(force=True); \
  print(c.profile, c.policy.name, c.policy.allow_network)"
# expect: benchmark-ste-code bench False
```

---

## 3. Lock down `ste-code` (the shipped product) — DO THIS LAST

`ste-code` is currently the **unjailed** profile you are running from. Once
you have restarted into `dev-ste-code` and confirmed it works, link the jail
into `ste-code` so the product profile is locked down:

```bash
.agents/hermes/jail/scripts/jail-install.sh ste-code
```

After this, `ste-code` cannot write into the STE-Code checkout at all — that
is the point. It reads the standard and artifacts and applies them to the
user's *own* project.

**Do not do this while a session you care about is running in `ste-code`.**

---

## 4. Decide: keep or remove the old `ste-code` copy

Once `dev-ste-code` is proven, you have two options. Both are safe; pick one
deliberately.

- **Keep both** (recommended): `ste-code` becomes the genuine user-facing
  product profile, locked down per §3. No deletion, and it doubles as a live
  test of the `user` policy.
- **Reclaim 553M**: only if you decide `ste-code` should be recreated fresh
  from a clean profile rather than inheriting dev history — a user profile
  arguably should not carry your sessions and memories. If so, export
  anything wanted, then recreate:
  ```bash
  hermes profile export ste-code    # if you want an archive first
  hermes profile delete ste-code
  hermes profile create ste-code --no-skills
  .agents/hermes/jail/scripts/jail-install.sh ste-code
  ```

**Recommendation: recreate it.** The shipped user profile should not contain
this project's development history — it is the product, and it currently
holds 10,018 files of authoring state that a downloader has no business
receiving.

---

## 5. Retire the v1 plugin

The old single-policy plugin still exists at:

```
.agents/hermes/plugins/ste-code-jail/       # v1, superseded
.agents/hermes/jail/                        # v2, single source of truth
```

v1 is no longer linked into any profile (the symlink was removed). Once v2 is
running in all three profiles, delete v1 and repoint the Makefile:

```bash
git rm -r .agents/hermes/plugins/ste-code-jail
```

Then in `Makefile`, change the `jail` target from
`$(JAIL)/selftest.py` to `.agents/hermes/jail/tests/test_jail.py`.

Do not delete v1 before v2 is proven in all three profiles.

---

## 6. Migrate pipeline scripts off hop counting

The jail is a backstop; this is the actual fix. 88 `PROJECT` derivations in
`.agents/tools/` compute the repo root by counting parent hops:

```python
PROJECT = Path(__file__).resolve().parent.parent.parent   # fragile
```

They are all *currently* correct, which is what makes this dangerous — the bug
only appears when a file moves. Replace with the marker walk:

```python
from lib.repo_root import repo_root, ensure_inside_repo
PROJECT = repo_root(__file__)
ensure_inside_repo(target)        # raises before a bad makedirs
```

`.agents/tools/lib/repo_root.py` exists and is tested. This is mechanical but
touches many files — do it as its own commit.

---

## 7. Wrap pipeline stages in the kernel jail

Argument inspection cannot see inside `python3 build.py`. Any stage that runs
untrusted or generated code should go through layer 2:

```bash
.agents/hermes/jail/scripts/jail-exec.sh python3 .agents/tools/runners/phase-a-run.py
```

Benchmark runners are the priority — they execute adversarially generated
prompts by design.

---

## Known issue — please check

Two directories catalogued at the start of the jail work are no longer on
disk:

```
NikolaRHristov/.agents/prompts/maturity-fixes
NikolaRHristov/STE-code-small/
```

You asked that the stray directories not be deleted. `expansion-pass1`
survives; those two do not. I did not delete them intentionally and cannot
prove what did — 12 Hermes processes were running concurrently, and my only
`rmdir` calls targeted `.jail-exec-selfcheck-$$` paths. Both were empty
scaffolding, so no content should be lost, but please confirm you did not
need them. If you did, they are in a Time Machine snapshot or can be
regenerated by the phase-A prompt generators.

---

## Reference

- `.agents/hermes/jail/README.md` — architecture, threat model, configuration
- `.agents/hermes/jail/core/policy.py` — the three policies, in one place
- `.agents/hermes/jail/tests/test_jail.py` — add a case for every new bypass
  you imagine; never delete one

Rule that produced the original bug, and worth keeping: **never derive a path
by counting parent hops.** The jail itself broke this rule in an early draft,
silently loaded zero components, and reported every escape as blocked while
blocking nothing. The test suite caught it.
