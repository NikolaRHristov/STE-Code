# Stage F — Artifacts (hybrid)

**Purpose:** package the canonical standard at `ste-code/final/` into the
deployable, LLM-friendly artifacts under `ste-code/artifacts/`.

Stage F is **hybrid**: a deterministic layer guarantees completeness and
reproducibility, and an LLM layer distills each slice into an
LLM-optimized form (in the spirit of `llms.txt` / `llms-full.txt`).

| | |
|---|---|
| **Reads** | `ste-code/final/` (54 rules, dictionary, categories, extensions, catalogue, provenance) |
| **Writes** | `ste-code/artifacts/_base/`, `ste-code/artifacts/level-2/`…`level5/`, `ste-code-rules.md`, `ste-code-system-prompt.md`, `llms.txt`, `llms-full.txt` |
| **Type** | Hybrid: deterministic assembly + LLM distillation |
| **Tools** | `.agents/tools/artifacts/levels_scaffold.py`, `distill_one.py`, `artifact_batch.py`, `verify-artifacts.py` |
| **Gate** | `.agents/tools/artifacts/verify-artifacts.py` |

---

## The four steps

### 1. Deterministic level separation — `levels_scaffold.py`
Reads `ste-code/final/` and emits, for each of the 8 tiers, a directory of
**bounded sub-documents** under `ste-code/artifacts/_base/level<N>/`. Oversized
rule sections are split (`rules-secN-part{i}.md`) so no base sub-doc exceeds
400 KB. This is the boilerplate layer — byte-reproducible, no LLM, no
truncation. Each full tier scaffold is about 1.85 MB before distillation.

```bash
python3 .agents/tools/artifacts/levels_scaffold.py            # write all 8 tier dirs
python3 .agents/tools/artifacts/levels_scaffold.py --dry-run
```

### 2. LLM distillation — `distill_one.py`
One Hermes session per sub-document. The worker reads its base sub-doc (and
`ste-code/final/` for anything outside it), then rewrites it into an
LLM-optimized file at `ste-code/artifacts/level<N>/<subdoc>`. It writes in
multiple `write_file` / `patch` calls (never one giant call, to avoid
truncation). On any failure it falls back to the deterministic base, so nothing
is lost. Each worker commits its sub-doc turn-by-turn with a batch number.

```bash
# one sub-doc, as its own background process
python3 .agents/tools/artifacts/distill_one.py level3 01-principles.md 3 \
    "+ complete dictionary excerpt + all rules"
```

The worker prompt lives at
`.agents/tools/prompts/synthesize-artifacts-worker.md` and is rendered with
`templater.py` (double-brace `{{token}}` syntax).

### 3. Deterministic assembler — `artifact_batch.py`
Concatenates `ste-code/final/` into two consolidated deliverables:

* `ste-code/artifacts/ste-code-rules.md` — the full corpus.
* `ste-code/artifacts/ste-code-system-prompt.md` — the same standard shaped as
  an LLM system prompt, with the "write in multiple calls" guidance.

Full rule coverage is verified against `final/` (54/54). No LLM, no truncation.

```bash
python3 .agents/tools/artifacts/artifact_batch.py
python3 .agents/tools/artifacts/artifact_batch.py --dry-run
```

### 4. Index assembly — `llms.txt` / `llms-full.txt`
A final deterministic pass writes:

* `ste-code/artifacts/llms.txt` — an `llms.txt`-style index of every tier and
  its sub-documents (for agentic retrieval).
* `ste-code/artifacts/llms-full.txt` — the concatenation of every distilled
  sub-document.

Each tier directory also gets a `_index.md` listing its sub-docs.

---

## Verification gate

`verify-artifacts.py` confirms that the assembled artifacts cover every rule in
`ste-code/final/` and that nothing was dropped or duplicated. Deterministic — no
model. Exit code `0` means the gate passes.

```bash
python3 .agents/tools/artifacts/verify-artifacts.py
```

Related quality tooling (applies to `final/`):

```bash
bash .agents/tools/linkcheck/run_linkcheck.sh   # lychee link check
```

---

## Back to the overview

See the [pipeline overview](../pipeline.md) for the full A→F + Finalize +
Linkcheck flow.
