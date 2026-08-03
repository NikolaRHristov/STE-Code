# Profile and jail architecture

How this project isolates agent sessions. Nothing here is specific to one
machine or one operator: clone the repository anywhere, create the profiles,
and the same guarantees hold.

The rules are enforced in code, not by convention. `.agents/hermes/jail/`
holds the implementation; this document explains the shape and the reasoning.

---

## 1. The repository is the source

Agent configuration — skills, jail plugins, policies — lives **in the
repository**. A profile under the agent's home directory holds symlinks that
point back here.

```
<repo>/.agents/skills/<skill>/         real directory, version controlled
<repo>/.agents/hermes/jail/            real directory, version controlled
        │
        │  symlink
        ▼
<agent-home>/profiles/<profile>/skills/<skill>
<agent-home>/profiles/<profile>/plugins/<plugin>
```

The direction matters, and only one direction is correct.

| | Result |
|---|---|
| Profile → repository (**correct**) | One source. An edit reaches every profile at once. Review and history come free. |
| Repository → profile (**wrong**) | The repository ships a link to a path that exists on one machine. Every clone gets a dangling symlink. |

Nothing in the checkout points outward into the agent's home directory.
Verify at any time — the command prints nothing when correct:

```bash
find . -path ./.git -prune -o -type l -print | xargs -r -n1 readlink | grep '\.hermes'
```

Because the profile side is a link, a fresh machine needs no copying: create
the profile, run the installer, and it is wired to the same source.

---

## 2. One profile per role

A single profile cannot serve three purposes. Authoring the standard needs
write access that running an adversarial benchmark must never have. The
project therefore separates them, and the **profile name selects the policy**.

| Profile | Policy | May write to | Network | Purpose |
|---|---|---|---|---|
| `dev-<project>` | `dev` | the repository, its own profile, sibling profiles | yes | Author the methodology |
| `<project>` | `user` | the user's own project only | no | Ship: read the standard, apply it |
| `benchmark-<project>` | `bench` | the benchmark output tree only | no | Run adversarial prompts |

Reads are unrestricted under every policy. Confinement targets **writes,
dangerous commands, and network egress** — the operations that can leave a
mark or leak.

Resolution order, highest first:

1. the `<PROJECT>_JAIL_POLICY` environment variable — an explicit one-off
2. `policy:` in the profile's own `jail.yaml`
3. the profile name, mapped in `core/policy.py`
4. **fail closed** to the most restrictive policy

Step 4 is the important one. An unmapped or misspelled profile is locked
down, never opened up. A typo costs a blocked write, not an escape.

### Why the granularity

Each policy grants the minimum its role needs.

`dev` includes the sibling profiles directory because provisioning the other
profiles is part of authoring — but it stops at `profiles/`, deliberately
excluding the parent that holds the shared credential file. No authoring task
writes API keys.

`bench` denies the repository *and its parent*, permitting only the output
tree. It also denies the profile's own control surface: without that, an
adversarial prompt could rewrite `config.yaml` to disable the jail, then
start a fresh session with no confinement at all. It blocks delegation, cron,
and memory for the same reason — each is a way to spawn a context that
inherits weaker rules.

---

## 3. Two enforcement layers

**Layer 1 — argument inspection.** A `pre_tool_call` hook resolves every path
a tool call would write to and blocks the call when one lands outside the
policy. It runs *before* approvals, so a session started with approvals
disabled cannot wave a violation through.

**Layer 2 — kernel confinement.** `jail-exec.sh` wraps a command in the
platform's sandbox (`sandbox-exec` on macOS, `bwrap` on Linux) so the
operating system refuses the write.

Layer 1 is honest about its ceiling. A shell command is not statically
analysable in general: `python3 build.py` may call `os.makedirs("../out")`
and no argument inspection can see it. Layer 1 catches every mistake visible
in the arguments; layer 2 catches the rest. Run anything untrusted or
generated through layer 2:

```bash
.agents/hermes/jail/scripts/jail-exec.sh python3 <script>
```

---

## 4. Output is confined and granular

Every run writes inside the tree its policy allows, one directory per run.
Nothing is written beside the source it was generated from.

```
.agents/benchmark/tests/<run-name>/run-<timestamp>/    benchmark output
.agents/state/                                          resume points, progress
.agents/tmp/                                            scratch, disposable
```

Runners take a **bare name**, not a path; it resolves to a subdirectory of
the one output root. An absolute path outside that root is rejected by the
runner, and under the `bench` policy the kernel refuses it as well.

These directories are ignored by git except for a `README.md` that documents
the reset. The structure is committed, the contents never are — a checkpoint
records what one machine did, and committing it makes the next clone skip
work it never performed.

Returning to a clean state is therefore a delete:

```bash
rm -rf .agents/state/* .agents/tmp/* .agents/benchmark/tests/*
```

---

## 5. Setting it up

```bash
# 1. create the profiles — the benchmark profile starts minimal and clean,
#    it must not inherit an authoring profile's history
<agent> profile create dev-<project>
<agent> profile create <project>            --no-skills
<agent> profile create benchmark-<project>  --no-skills

# 2. link the jail from the repository into each profile
.agents/hermes/jail/scripts/jail-install.sh --all

# 3. confirm every link points at the single source
.agents/hermes/jail/scripts/jail-install.sh --status

# 4. wire skills AND persistent memory to the repository single source
.agents/hermes/install.sh            # link skills + memory for all profiles
.agents/hermes/install.sh --status   # verify both are linked
```

Skills and persistent memory (USER.md / MEMORY.md) each have their own linker
— `link-skills.sh` and `link-memory.sh` — under `.agents/hermes/`. Both follow
the same single-source convention: the live profile holds a relative symlink to
a version-controlled file in the repository, so an edit propagates to every
profile and survives a profile wipe. `install.sh` runs both in one idempotent
step. `make install` / `make install-check` wrap the same.

The installer links the plugin **and** enables it in the profile's config. A
plugin that is present but not enabled looks correctly installed and enforces
nothing — a live test once escaped all four of its cases while the status
check reported the link was fine. `--status` now reports enablement, not just
the link, and warns when a plugin is a real directory rather than a symlink,
because such a copy will silently drift from the source.

---

## 6. Verifying

```bash
make check                                        # everything below, in CI
python3 .agents/hermes/jail/tests/test_jail.py    # argument inspection
.agents/hermes/jail/scripts/jail-exec.sh --check  # kernel layer
.agents/hermes/jail/scripts/live-jail-test.sh --all   # real sessions
```

The three differ in what they can prove, and the difference is the point:

- The **unit suite** runs every known escape against every policy.
- The **kernel check** proves the sandbox is available and configured.
- The **live test** launches a real agent session, asks it to write outside
  its policy, and then checks the filesystem. The agent's prose is
  irrelevant; only the absence of the file is evidence.

Two traps are worth knowing. A running session **caches its policy at
start** — after editing `core/policy.py`, your own session still enforces the
old rules. Verify in a fresh process, and do not read a stale refusal as a
failed fix. And the live harness once scored a vacuous pass on every case
because the platform shipped no `timeout` binary: the agent never launched,
no file appeared, and "no file" was read as success. A test that cannot fail
proves nothing.

The escape suite is adversarial by construction. Its first run found 14 holes
in an implementation that had passed a happy-path suite: relative paths,
`cd ..` followed by a bare relative `mkdir`, `$HOME` expansion, subshells,
`git -C`, heredocs, `tee`. **Add a case whenever a new bypass is imagined;
never delete one.**

---

## 7. Configuration

`core/jail.yaml` holds shared defaults and contains no machine-specific
paths. A profile that needs an override drops its own `jail.yaml` into its
profile directory, which is merged on top.

```yaml
enforce: true          # false = dry run: log violations, block nothing
# policy: dev          # force a policy regardless of profile name
extra_write_roots: []  # keep SHORT — every entry is a hole
extra_deny_roots: []
```

The project root is found by walking up to a repository marker (`.git`,
`Makefile`), so a clone works from any location.

**Never derive a path by counting parent hops.**

```python
PROJECT = Path(__file__).resolve().parent.parent.parent   # fragile
```

The hop count silently encodes the file's depth. Move the file and the root
becomes an *ancestor* of the repository, where `os.makedirs(exist_ok=True)`
builds the stray tree without complaint. This is the bug the jail was written
to contain, and the jail's own first draft repeated it — it loaded zero
components and reported every escape as blocked while blocking nothing. Use
the marker walk in `core.policy.resolve_project_root()`.

---

## Threat model

**Stops:** accidental writes above the project root from a wrong root
variable; path traversal and `~` or `$VAR` expansion; writes hidden in
redirections, heredocs, `sh -c`, and subshells; an adversarial prompt writing
outside its output tree, exfiltrating over the network, or escalating through
delegation, cron, or memory.

**Does not stop:** an attacker with shell access who reaches an interpreter
not wrapped by layer 2. Argument inspection is not a security boundary on its
own.

**Deliberately allows:** reading anything on the machine, under every policy.

---

## Reference

- `.agents/hermes/jail/README.md` — implementation detail and layout
- `.agents/hermes/jail/core/policy.py` — the policies, in one place
- `.agents/hermes/jail/tests/test_jail.py` — the escape suite
