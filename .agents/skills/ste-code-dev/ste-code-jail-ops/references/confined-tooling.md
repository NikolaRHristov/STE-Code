# Confined-tooling fixes (verified under the bench jail)

## Symptom

`make test` / `selftest.py` under the `bench` policy went 158/180 — every one of
the 22 failures was a `compiles:` check. Under `dev` it was green (180/180).

## Root cause

The old `test_modules_compile()` did:

```python
subprocess.run([sys.executable, "-m", "py_compile", str(path)], ...)
```

Two failure modes inside the bench jail (which denies project-root writes and
pins the spawned child's cwd):

1. The **relative** `str(path)` does not resolve when the caller's cwd is not
   the bench dir (FileNotFoundError).
2. `py_compile` tries to write `__pycache__/*.pyc` next to the source — into a
   tree the bench jail denies.

## Fix (jail-proof, environment-independent)

Compile **in-process** to a `cfile` under a writable temp dir:

```python
cache_root = os.environ.get("PYTHONPYCACHEPREFIX") or tempfile.gettempdir()
cache_dir = Path(cache_root) / "ste-selftest-pyc"
cache_dir.mkdir(parents=True, exist_ok=True)
for path in sorted(BENCH.glob("*.py")):
    if path.name == "selftest.py":
        continue
    ok = True
    try:
        cfile = cache_dir / "{}.{}.pyc".format(path.stem, abs(hash(str(path))))
        py_compile.compile(str(path), cfile=str(cfile), doraise=True)
    except (py_compile.PyCompileError, SyntaxError, OSError):
        ok = False
    check(ok, "compiles: {}".format(path.name))
```

- Absolute path → no cwd dependency.
- `cfile` under `$PYTHONPYCACHEPREFIX` (or `/tmp`) → no project-root write.
- `doraise=True` → still catches real syntax errors via the full `compile()`
  pipeline (stronger than `ast.parse`, which misses `return`/`yield`/`continue`
  outside their valid scope).

After this, `selftest.py` passes **180/180 under the bench jail AND under dev**.

## Design rule

A "new looser/anonymous profile" does NOT fix this. `core/policy.py`:
`_STRICT_FALLBACK = "bench"` — an unmapped profile name falls through to the
strictest policy. Fix the _tooling_ (temp-dir bytecode, absolute paths), or run
_developer verification_ from the `dev` policy; keep the adversarial _run_ under
`bench`.
