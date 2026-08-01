# STE-Code — Artifacts

STE-Code is a controlled-language variation of ASD-STE100 for software
documentation. This `artifacts/` directory holds the **deployable,
LLM-distilled form** of the standard, laid out as small sub-documents so that
neither the LLM writer nor the LLM reader ever has to touch one enormous file.

## Layout — hybrid sub-doc tiers

The standard is sliced into **8 tiers**, each a directory of focused
sub-documents plus an `_index.md`:

| Tier | Level | Contents | Size on disk | Tokens |
|------|-------|----------|-------------:|-------:|
| `level-2/` | -2 | 14 core principles only (ultra-minimal) | 5 KB | ~1.2K |
| `level-1/` | -1 | core principles + synonym table | 26 KB | ~5.9K |
| `level0/`  | 0  | + short dictionary excerpt | 17 KB | ~4.3K |
| `level1/`  | 1  | + doc templates (code review / PR feedback) | 58 KB | ~14.5K |
| `level2/`  | 2  | + section-specific grammar rules | 75 KB | ~18.5K |
| `level3/`  | 3  | + complete dictionary excerpt + all rules | 388 KB | ~95K |
| `level4/`  | 4  | + extensions + reference catalogue | 462 KB | ~116K |
| `level5/`  | 5  | full standard (all rules + extensions + catalogue + provenance) | 539 KB | ~134K |

Size on disk is the measured sum of a tier's sub-documents; `_index.md` and
`system-prompt.txt` are excluded, because `system-prompt.txt` repeats the same
sub-documents. Token counts use the `o200k_base` tokenizer (GPT-4o, GPT-4.1,
GPT-5, o-series); `cl100k_base` (GPT-4, GPT-3.5-turbo) agrees to within 0.3%,
and Claude and Llama tokenizers stay within a few percent for English prose.
Regenerate these figures with:

```bash
python3 .agents/tools/maintenance/measure_artifacts.py             # summary table
python3 .agents/tools/maintenance/measure_artifacts.py --per-file  # sub-doc rows
python3 .agents/tools/maintenance/measure_artifacts.py --json      # machine readable
```

**Distillation status.** Two sub-documents are still byte-identical to their
`_base/` scaffold, which means the distiller fell back for them:

| Sub-document | Now | Projected after distillation |
|--------------|:---:|------------------------------|
| `level3/03-dictionary.md` | 2.5 KB (scaffold) | ~4.7 KB; tier stays near ~95K tokens |
| `level5/rules-sec7.md` | 123 KB (scaffold) | ~24 KB; tier drops to ~110K tokens |

Each projection uses the ratio that the same sub-document already reached in the
other tiers, so rule sections project downward and dictionary sections upward.

Each tier directory contains:
- `0N-*.md` / `rules-secN.md` — the distilled sub-documents
- `_index.md` — a human-readable list of the tier's sub-documents
- `system-prompt.txt` — **the whole tier concatenated into one file**, ready to
  pass as a `--system-prompt-file` to a benchmark or application

Concatenation is deterministic and reproducible; `system-prompt.txt` is just
the sub-docs joined by `---`.

## Consolidated single-file artifacts

| File | Purpose |
|------|---------|
| `llms.txt` | llms.txt-standard index — lists every tier + the full file |
| `llms-full.txt` | the entire distilled standard in one file (the canonical consolidated artifact) |

`llms-full.txt` replaces the retired `ste-code-rules.md` /
`ste-code-system-prompt.md`; it is regenerated from `final/` by the assembler
and is the single-file deliverable to embed.

## Boilerplate

| Path | Purpose |
|------|---------|
| `_base/` | deterministic per-tier base sub-docs (pre-LLM scaffold) |
| `VERSION` | semantic version, bumped by the assembler |

## How it is built

1. **Deterministic scaffold** — `levels_scaffold.py` emits `_base/<tier>/` sub-docs.
2. **LLM distill** — `synthesize_artifacts.py` distills each base sub-doc into
   `ste-code/artifacts/<tier>/` (one small session per sub-doc).
3. **Finalize assembly** — `finalize_artifacts.py` writes every tier's
   `_index.md` + `system-prompt.txt` and the top-level `llms.txt` /
   `llms-full.txt`.

Source of truth is `ste-code/final/` (the enriched standard produced by
Phases D+G). Nothing here is hand-edited; re-run the assembler to regenerate.

## Using a tier

```bash
# Feed a whole tier to an LLM (benchmark or app):
python3 .agents/benchmark/benchmark-levels.py --levels 0,1,2,3,4,5

# Or point any tool at one tier file:
cat ste-code/artifacts/level1/system-prompt.txt
```
