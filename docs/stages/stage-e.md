# Stage E — Extension

**Purpose:** fill the documented gaps between the aerospace standard and the
code-documentation domain with new entries: approved verbs, adjectives, noun
and verb category examples, code anti-patterns, and domain extensions.

| | |
|---|---|
| **Reads** | The gap areas and the adapted corpus |
| **Writes** | `ste-code/extensions/<area>.md` plus the derived `<area>.json` |
| **Type** | LLM workers that emit markdown only; JSON is derived deterministically |
| **Runner** | `.agents/tools/runners/phase-e-run.py` |
| **Orchestrator** | `.agents/tools/extension/extend_batch.py` |
| **Gate** | `.agents/tools/extension/verify_extensions.py` |
| **Checkpoint** | `.agents/state/extend-checkpoint.json` |

`ste-code/extensions/` is created by the first Stage E run.

---

## Commands

```bash
# All six gap areas
python3 .agents/tools/runners/phase-e-run.py

# One area
python3 .agents/tools/runners/phase-e-run.py verbs

# Skip the areas that already passed
python3 .agents/tools/runners/phase-e-run.py --resume

# Gate only
python3 .agents/tools/runners/phase-e-run.py --verify

# Direct orchestrator use
python3 .agents/tools/extension/extend_batch.py verbs
python3 .agents/tools/extension/extend_batch.py --dry-run
STE_MODEL=tencent/hy3:free python3 .agents/tools/extension/extend_batch.py

# Derive JSON from markdown
python3 .agents/tools/extension/md_to_json.py ste-code/extensions/verbs.md
python3 .agents/tools/extension/md_to_json.py ste-code/extensions/

# Gate on its own
python3 .agents/tools/extension/verify_extensions.py
```

`--agent` and `--model` are accepted as informational no-ops. The runner
executes the Hermes virtual environment interpreter at
`~/.hermes/hermes-agent/venv/bin/python3`; to use a different interpreter, call
`extend_batch.py` directly.

---

## Gap areas

| Area | Output file | Target entries |
|------|-------------|:--------------:|
| `verbs` | `verbs.md` | 15 |
| `adjectives` | `adjectives.md` | 19 |
| `nouns` | `nouns.md` | 86 |
| `verb-examples` | `verb-examples.md` | 20 |
| `anti-patterns` | `anti-patterns.md` | 10 |
| `domains` | `domains.md` | 47 |

---

## Markdown first, JSON derived

Workers emit markdown only. `md_to_json.py` is the one place JSON is produced
for this stage: it parses each `### <title>` block of `- **field**: value`
lines and writes `<name>.json` next to the markdown. There is no `eval`, no
`exec`, and no model in the JSON path, so direct JSON generation cannot
introduce a remote-code-execution surface.

The markdown file is the source of truth. The JSON file is a derived artifact.

---

## Verification gate

`verify_extensions.py` runs the six deterministic gates from the
extension-worker skill on every `ste-code/extensions/<area>.md` file, and
confirms that the derived JSON matches:

1. Markdown is present and parses into at least one entry, and the derived
   JSON is valid.
2. The required fields are present for each entry type.
3. Every definition has at least 10 words.
4. There are no fabrication markers (`TODO`, `TBD`, `FIXME`, `placeholder`,
   `???`).
5. Entry titles are unique in each file.
6. STE / non-STE pairs are correct — for verbs and adjectives, the non-STE side
   contains a synonym that STE-Code avoids.

An area is committed to git only after its gate passes. Exit code `0` means all
gates pass.

---

## Next stage

[Stage F — Artifacts](stage-f.md) assembles the deliverables.
