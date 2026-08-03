# Pipeline run state

Empty by design. Every file that appears here is written by a running pipeline
stage and describes **this machine's run** — not the project.

```
.agents/state/
  <stage>-checkpoint.json    resume points: which units a stage finished
  <stage>-progress.md        human-readable status, regenerated from disk
  locks/                     advisory locks held while a stage writes
```

## Rules

**Never commit run state.** A checkpoint records what one operator's machine
completed. Committed, it makes the next clone skip work it never did.

**Never trust a checkpoint over disk.** A checkpoint marks a unit done even when
the stage fell back to a copy. Regenerate the progress table from the output
files and compare:

```bash
python3 .agents/tools/ --regen-progress < stage > / < stage > _batch.py
```

**Never write pipeline output here.** This directory holds bookkeeping only.
Stage output belongs in the output tree the stage owns.

## Reset

Deleting this directory's contents returns the pipeline to a clean state. Stages
recreate what they need on the next run:

```bash
rm -rf .agents/state/*
```
