# Scratch

Empty by design. Throwaway probes, one-off scripts, and captured output go here
so they never land in a source directory.

Everything here is ignored by git and is safe to delete at any moment. Write
nothing here that another stage reads.

```bash
rm -rf .agents/tmp/*
```

A probe that proves something worth keeping does not stay a probe: move the
check into the committed self-test (`make check`) so it runs again on its own. A
finding worth keeping goes into the skill or reference that teaches it, not into
a file here.
