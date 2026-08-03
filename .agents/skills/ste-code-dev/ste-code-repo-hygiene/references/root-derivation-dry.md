# Root-derivation DRY migration

The refactor replaced hop-counted root derivation in 87 scripts:

```python
PROJECT = Path(__file__).resolve().parent.parent.parent.parent   # 4 hops — BAD
PROJECT = Path(__file__).resolve().parents[3]                    # also BAD
PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))  # BAD
```

with a depth-independent bootstrap that delegates to the tested helper
`.agents/tools/lib/repo_root.py`:

```python
# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
```

## Why this matters

Counting `.parent` hops encodes the file's depth in the tree. Move the script
one directory deeper/shallower and `PROJECT` silently points at an ancestor of
the repo; `os.makedirs` then scatters output outside the checkout. That is the
exact defect the jail exists to contain.

## Two mistakes made (and reverted) during the migration

1. **Inlining a 19-line helper into every file.** First attempt defined a
   `_repo_root_bootstrap()` function (marker-walk + import + try/except) inside
   each file. That trades one duplication for another and defeats the DRY goal.
   Fix: a 6-line bootstrap that delegates to the shared `repo_root()`.

2. **Import ordering `NameError`.** The bootstrap first emitted the marker-walk
   using `Path(__file__)`, then a separate `import sys` /
   `from pathlib import Path` line, then `sys.path.insert(...)`. Because the
   bootstrap used `sys` ABOVE its import, the module raised
   `NameError: name 'sys' is not defined` on import. Fix: make the bootstrap
   self-contained — `import sys as _sys` and `from pathlib import Path as _Path`
   _inside_ the bootstrap block, so ordering is impossible to get wrong.

## How the migration script works (re-run it with)

`scripts/migrate_root.py` — operate from the repo root:

```bash
python3 scripts/migrate_root.py                                   # dry run, lists every derivation
python3 scripts/migrate_root.py --apply                           # rewrite all three fragile forms
python3 scripts/migrate_root.py --only "benchmark/adversarial.py" # one file
```

It excludes `.agents/tools/lib/repo_root.py` itself and `.agents/hermes/jail/`
(owned by another live session), plus vendor/**pycache**/ste-code/tmp. It skips
files that already contain the `_STE_REPO_ROOT_BOOTSTRAP` marker.

## Proof the fix works (run after migrating)

```python
import importlib.util, pathlib
d = pathlib.Path(".agents/tmp/probe/a/b"); d.mkdir(parents=True)
import shutil; shutil.copy(".agents/benchmark/adversarial.py", d/"moved.py")
spec = importlib.util.spec_from_file_location("m", d/"moved.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
assert str(m.PROJECT).endswith("STE-Code")   # still correct despite the move
# the OLD form would have pointed at .agents/tmp/probe/a/b
```

## Verify after a bulk apply

```bash
python3 -m py_compile $(git diff --name-only | grep '\.py$')   # all compile
git ls-files --with-tree=<base_sha> | sort > /tmp/a; git ls-files | sort > /tmp/b
diff /tmp/a /tmp/b                              # expects ZERO adds/removes, edits only
```
