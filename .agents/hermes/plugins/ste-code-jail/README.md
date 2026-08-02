# ste-code-jail

A Hermes Agent plugin that confines every filesystem **write** to the project
repository. Reads are untouched.

## Why

Agent sessions launched from this project were creating directories *outside*
the repository:

```
<parent>/.agents/prompts/expansion-pass1/     # empty, one level above the repo
<parent>/.agents/prompts/maturity-fixes/      # empty, one level above the repo
<parent>/STE-code-small/.agents/              # a sibling directory
```

**Root cause.** Pipeline scripts derive their project root by counting parent
directory hops from `__file__`:

```python
PROJECT = Path(__file__).resolve().parent.parent.parent   # 3 hops
```

The hop count silently encodes how deep the script sits in the tree. Move the
script one directory in either direction and `PROJECT` points at an *ancestor*
of the repository. `os.makedirs(..., exist_ok=True)` then cheerfully creates
the missing tree, and the run scatters output across the machine.

Hermes itself only **warns** about this (`_path_resolution_warning` in
`tools/file_tools.py`) — it never blocks. This plugin blocks.

## What it does

Registers a `pre_tool_call` hook that returns
`{"action": "block", "message": ...}` when a tool's **write target** resolves
outside the allowed roots.

| Tool | Write targets checked |
|---|---|
| `write_file` | `path` |
| `patch` | `path` (replace mode); every `*** Add/Update/Delete File:` header (V4A mode) |
| `skill_manage` | `file_path`, resolved under the profile skills directory |
| `terminal` | `workdir`, plus absolute path tokens in `command` — only when the command contains a write verb (`mkdir`, `>`, `tee`, `cp`, `mv`, `rm`, `sed -i`, ...) |

Guarantees:

- **Reads are never restricted.** `read_file`, `search_files`, and read-only
  shell commands reach anywhere on the machine, as before.
- **Symlinks cannot widen the jail.** Containment is checked on the fully
  resolved `realpath`, so a symlink pointing outward is still blocked.
- **`..` traversal is normalised** before the check.
- **Applies under `--yolo`.** Blocking happens before the approval layer, so
  bypassing approvals does not bypass the jail.

## Portability

No machine-specific paths appear anywhere in this plugin. The project root is
discovered at load time by walking up from the plugin directory until an
ancestor contains a repository marker (`.git`, `Makefile` — configurable).
Clone the repo anywhere, on any machine, and the jail anchors itself.

## Install

```bash
# 1. Link the plugin into the Hermes profile that runs this project
ln -sfn "$PWD/.agents/hermes/plugins/ste-code-jail" \
        "${HERMES_HOME:-$HOME/.hermes}/plugins/ste-code-jail"

# 2. Enable it (no --allow-tool-override needed; this is a hook, not an override)
hermes plugins enable ste-code-jail

# 3. Verify
hermes plugins list | grep ste-code-jail     # -> enabled
python3 .agents/hermes/plugins/ste-code-jail/selftest.py
```

The plugin takes effect on the **next** session.

## Configuration

`jail.yaml`, next to the plugin:

| Key | Default | Meaning |
|---|---|---|
| `enforce` | `true` | `false` = dry run: log violations, block nothing |
| `root_markers` | `.git`, `Makefile` | Files identifying the project root |
| `extra_roots` | `[]` | Additional writable roots. Keep short — each is a hole |
| `allow_hermes_home` | `true` | Permit writes under `$HERMES_HOME` (session state, skills, logs) |
| `allow_temp` | `true` | Permit writes under `/tmp`, `$TMPDIR`, `/var/folders` |
| `deny` | `.git`, this plugin dir | Paths inside a root that are still refused |

## Verify

```bash
python3 .agents/hermes/plugins/ste-code-jail/selftest.py   # 16 cases
make check                                                  # includes the jail gate
```

The self-test needs no Hermes runtime — it calls the hook directly, so it runs
in CI. It covers the exact real-world escape (a write into the repo's parent),
`..` traversal, `~` expansion, denied `.git`, V4A patch headers, `mkdir` and
shell redirects outside the repo, terminal `workdir` escape, and four
must-still-be-allowed read cases.

## Companion fix

The jail is the backstop. The root cause is fixed at the source by
`.agents/tools/lib/repo_root.py`, which replaces hop counting:

```python
from repo_root import repo_root, ensure_inside_repo

PROJECT = repo_root(__file__)                 # depth-independent
out = ensure_inside_repo(PROJECT / ".agents" / "prompts" / batch)
out.mkdir(parents=True, exist_ok=True)        # raises instead of escaping
```

Use both: `repo_root()` so paths are right, the jail so a mistake cannot
escape the repository.
