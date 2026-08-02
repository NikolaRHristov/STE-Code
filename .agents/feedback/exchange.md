# Inter-agent exchange

Working channel between the agents that run the pipeline. It carries
observations from a **live run**: what a stage actually did, where it
disagreed with the documentation, and what the next agent must know.

This file is **run state**. It is blank between runs and is not a place for
durable knowledge. A lesson that survives the run belongs in the skill or
reference that teaches it:

| Kind of finding | Where it belongs |
|---|---|
| How a stage should be operated | `.agents/skills/<stage>/SKILL.md` |
| A rule every agent must follow | `.agents/references/rails.md` |
| A one-off observation about this run | here |

## Format

Append one section per entry. Newest last, so the file reads in run order.

```markdown
## <stage> — <short title>

**Observed:** what happened, with the command or path that shows it.
**Expected:** what the documentation says should happen.
**Action:** what you changed, or what the next agent must do.
```

Name a file, a command, or a count in every entry. An entry that cannot be
checked against disk is an opinion, and the auditor discards it.

<!-- entries start below this line -->
