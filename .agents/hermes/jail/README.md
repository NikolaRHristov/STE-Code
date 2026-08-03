# STE-Code jail

Confines Hermes Agent sessions so a prompt — mistaken or hostile — cannot touch
the rest of the machine. Reads stay open; **writes, tool use, and network
egress** are governed by a policy chosen from the active profile.

Single source of truth: everything lives here in the repository. Profiles get
symlinks pointing back, so an edit here updates every profile at once and no
copy can drift.

## Why

Sessions launched from this project created directories _outside_ it — an empty
`.agents/prompts/<batch>/` tree one level up, and a stray sibling `.agents/`.
Root cause: pipeline scripts derived their project root by counting parent hops:

```python
PROJECT = Path(__file__).resolve().parent.parent.parent   # depth-encoded
```

The hop count silently encodes the script's depth. Move the file and the root
becomes an _ancestor_ of the repo, where `os.makedirs(exist_ok=True)` builds the
tree without complaint. Hermes only _warns_ about this
(`_path_resolution_warning` in `tools/file_tools.py`) — it never blocks.

## Layout

```
.agents/hermes/jail/
  core/              SINGLE SOURCE OF TRUTH
    policy.py          profile -> Policy; containment decisions
    analysis.py        extract write targets from tool arguments
    jail.yaml          shared defaults
  plugins/
    jail-fs/           filesystem writes
    jail-cmd/          tool and command use
    jail-net/          network egress
    ste-code-jail/     GROUP: assembles the three under one policy
  scripts/
    jail-lib.sh        shared shell library (mirrors core/policy.py)
    jail-exec.sh       kernel-enforced confinement
    jail-install.sh    symlink the jail into a profile
  tests/
    test_jail.py       adversarial suite, all policies
```

Granular by design: each plugin guards one concern and can be enabled alone to
debug a policy. Enable the **group** for normal use.

## Profiles and policies

| Profile              | Policy  | Writes                | Network | Purpose                              |
| -------------------- | ------- | --------------------- | ------- | ------------------------------------ |
| `dev-ste-code`       | `dev`   | repo + profile        | yes     | Author the methodology               |
| `ste-code`           | `user`  | user's own project    | **no**  | Ship: read standard, apply artifacts |
| `benchmark-ste-code` | `bench` | benchmark output only | **no**  | Run adversarial benchmarks           |

Policy resolution: `STE_CODE_JAIL_POLICY` → `policy:` in `jail.yaml` → profile
name → **fail closed to `bench`**. An unmapped profile is locked down, never
opened up.

Under `user` and `bench` the jail also blocks delegation, cron, and memory —
without that, an adversarial prompt could spawn a subagent and inherit a weaker
context.

## Two enforcement layers

**Layer 1 — argument inspection (the plugins).** A `pre_tool_call` hook that
resolves every path a call would write to and blocks when one lands outside the
policy. Fires _before_ approvals, so `--yolo` does not bypass it.

**Layer 2 — kernel confinement (`jail-exec.sh`).** Wraps a command in
`sandbox-exec` (macOS) or `bwrap` (Linux) so the OS refuses the write.

Layer 1 is honest about its ceiling: a shell command is not statically
analysable in general. `python3 build.py` may call `os.makedirs("../out")` and
no argument inspection can know. Layer 1 catches every mistake visible in the
arguments — the whole observed failure class — and layer 2 catches the rest.

```bash
# run a pipeline stage so even its subprocesses are confined
.agents/hermes/jail/scripts/jail-exec.sh python3 .agents/tools/runners/phase-a-run.py
```

## Install

```bash
cd .agents/hermes/jail/scripts
./jail-install.sh --all                   # link the group plugin into all profiles
./jail-install.sh ste-code                # one profile
./jail-install.sh dev-ste-code --granular # link the three components
./jail-install.sh --status                # verify links point at the single source
```

`--status` warns when a plugin is a real directory rather than a symlink,
because that copy will drift.

## Verify

```bash
python3 .agents/hermes/jail/tests/test_jail.py # all policies
python3 .agents/hermes/jail/tests/test_jail.py --policy bench -v
.agents/hermes/jail/scripts/jail-exec.sh --check # kernel layer
.agents/hermes/jail/scripts/jail-exec.sh --show  # resolved policy
make check                                       # includes the jail
```

Current: **108/108** — 35 allow cases (false-positive guard) and 83 escape
attempts blocked across three policies.

The escape suite is adversarial by construction. Its first run found **14
holes** in an implementation that passed a 16-case happy-path suite: relative
paths, `cd ..` then a bare relative `mkdir`, `$HOME` expansion, subshells,
`git -C`, heredocs, `tee`. Add a case whenever a new bypass is imagined; never
delete one.

## Configuration

`core/jail.yaml` holds shared defaults with no machine-specific paths. A profile
that needs an override drops its own `jail.yaml` into `$HERMES_HOME/`, which is
merged on top.

```yaml
enforce: true # false = dry run: log violations, block nothing
# policy: dev          # force a policy regardless of profile name
extra_write_roots: [] # keep SHORT — every entry is a hole
extra_deny_roots: []
# benchmark_output: /path   # where bench may write
# workspace: /path          # the user's own project under the user policy
```

## Threat model

**Stops:** accidental parent-directory writes from a wrong root variable; path
traversal and `~`/`$VAR` expansion; writes hidden in redirections, heredocs,
`sh -c`, and subshells; an adversarial benchmark prompt writing outside its
output tree, exfiltrating over the network, or escalating via
delegation/cron/memory.

**Does not stop:** a determined attacker with shell access who can reach an
interpreter _not_ wrapped by layer 2 — argument inspection is not a security
boundary on its own. Wrap untrusted execution in `jail-exec.sh`, where the
kernel makes the decision.

**Deliberately allows:** reading anything on the machine, under every policy.

## Maintenance

Never derive a path by counting parent hops. Use the marker walk in
`core.policy.resolve_project_root()`, or `repo_root()` from
`.agents/tools/lib/repo_root.py`. The jail itself follows this rule — an earlier
draft used `parent.parent.parent`, silently loaded zero components, and reported
every escape as blocked while blocking nothing. The test suite caught it; hop
counting is now banned throughout.
