# STE-Code — templates/

**Status: templating moved out of this folder.** The eleven hand-written
prompt files that used to live here (`ste-code-full.md`, `ste-code-compact.md`,
`ste-code-level-0.md`, `compliance-check.prompt.md`, …) were pre-trajectory
one-off prompts. Nothing in the codebase loaded them and they drifted from
`ste-code/final/`, so they are retired. Recover them from git history if needed:

```bash
git log --diff-filter=D --name-only -- ste-code/templates/
```

## What owns templating now

### 1. The `{{placeholder}}` template standard — `.agents/tools/lib/templater.py`

Every tool keeps its generated markdown / worker prompts in its **own**
`templates/*.md` next to the `.py`, and renders them through the shared loader:

```python
from templater import Templater, render_template

TPL  = Templater(__file__)                     # -> ./templates/ next to the tool
text = TPL.render("group_header", gid="001-front", page_start=1, ...)

# or one-shot against an explicit path:
text = render_template(Path("ste-code/templates/tier-system-prompt.md"),
                       subdoc_name="01-principles.md", subdoc_body="...")
```

Substitution is **double-brace `{{name}}`**, never `str.format()` — markdown is
full of literal `{}` (JSON, code fences) and `|` (tables), and `{{name}}` never
collides with them, so templates need zero escaping. Rendering is **strict**: an
unsupplied placeholder or an unused variable raises. Reference implementation of
the folder convention: `.agents/tools/grouping/templates/README.md`.

### 2. The trajectory system — `.agents/tools/trajectory/trajectory.py`

Phase T (optional, experimental) supersedes per-file prompt variants. It takes a
`ste-code/final/rules/*.md` document and distills it into K **parametrized
variants** — same rule, different mission (target consumer, use case, paradigm
emphasis, example density, vocabulary strictness, register, format). Its worker
prompt is externalized to `.agents/tools/prompts/trajectory-worker.md` and
rendered with the same templater.

Variants are written to `ste-code/parametarized/<doc>/v<k>.md` (created on first
run). Trajectory **never** writes to `final/`, `adapted/`, or `artifacts/`.

```bash
python3 .agents/tools/trajectory/trajectory.py --list-params   # show the grid
python3 .agents/tools/trajectory/trajectory.py --plan          # dry run
```

## Where the deployable prompt material lives

Not here — in **`ste-code/artifacts/`**, as 8 tier directories:

| Tier dir | Level | Tier dir | Level |
|---|---|---|---|
| `level-2/` | -2 (ultra-minimal) | `level2/` | 2 |
| `level-1/` | -1 | `level3/` | 3 |
| `level0/`  | 0  | `level4/` | 4 |
| `level1/`  | 1  | `level5/` | 5 (full standard) |

Each tier directory holds its distilled sub-documents (`0N-*.md` /
`rules-secN.md`), an `_index.md` listing them, and **`system-prompt.txt`** — the
whole tier concatenated into one file, ready to pass as a system prompt.
`ste-code/artifacts/llms.txt` (tier index) and `llms-full.txt` (everything in one
file) are the consolidated deliverables. Sizes, token counts and build details:
`ste-code/artifacts/README.md`.

### Regenerate

```bash
# deterministic re-assembly of every tier's _index.md + system-prompt.txt,
# plus llms.txt and llms-full.txt (no LLM, reproducible byte-for-byte)
python3 .agents/tools/artifacts/finalize_artifacts.py
```

### Consume

```bash
# benchmark all 8 tiers (default --levels -2,-1,0,1,2,3,4,5)
python3 .agents/benchmark/benchmark-levels.py
python3 .agents/benchmark/benchmark-levels.py --levels 0,1,2 --dry-run

# or feed one tier to any tool
cat ste-code/artifacts/level1/system-prompt.txt
```

## Files in this folder

| File | Purpose | Placeholders |
|---|---|---|
| `README.md` | this note | — |
| `tier-system-prompt.md` | the per-sub-document block format of a tier's `system-prompt.txt` | `subdoc_name`, `subdoc_body` |

`tier-system-prompt.md` documents, in renderable form, the exact block that
`finalize_artifacts.py::_write_tier_system_prompt` emits per sub-document.
Blocks are joined with `\n\n---\n\n` and one trailing newline is appended.
Rendering it over the sub-docs of all 8 tiers reproduces the on-disk
`system-prompt.txt` files byte-for-byte:

```python
from pathlib import Path
import sys; sys.path.insert(0, ".agents/tools/lib")
from templater import render_template

tpl  = Path("ste-code/templates/tier-system-prompt.md")
tier = Path("ste-code/artifacts/level1")
subs = sorted(p for p in tier.glob("*.md") if p.name != "_index.md")
out  = "\n\n---\n\n".join(
    render_template(tpl, subdoc_name=s.name,
                    subdoc_body=s.read_text(encoding="utf-8").strip())
    for s in subs) + "\n"
assert out == (tier / "system-prompt.txt").read_text(encoding="utf-8")
```

`finalize_artifacts.py` still holds that format inline; this template is the
externalized, verified copy it can adopt. Do not edit artifacts by hand — change
`ste-code/final/` and re-run the assembler.
