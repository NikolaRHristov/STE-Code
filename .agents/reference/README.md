# STE-Code Reference Library (vendor references for final agent tools & LLMs)

These are **external vendor/community references** used to inform the finalize
agent and downstream LLMs — they are NOT part of the STE-Code standard itself
and never feed into the adaptation pipeline as input. They live here (outside
`ste-code/final/`) per instruction: vendor reference files are kept separate from
the final deliverable.

## Layout
- `manifest.json` — index of every reference (slug, title, url, local_path, kind, fetched_at)
- `<slug>.md` / `<slug>.txt` — one file per reference, downloaded separately
- Entries with `kind: pointer` in the manifest are large corpora / topic
  directories stored as URL pointers only (not embedded, to avoid repo bloat)

## Categories covered
- Style guides with controlled word lists (Microsoft, Google)
- Coding & API glossary datasets (Kong, dwyl, jvalentino, GitHub, DevOps)
- Open-source controlled vocabulary (OpenSTE)
- English word corpora for vocabulary filtering (SCOWL, public-domain lists)
- Vale linter styles (machine-enforceable approved/avoided word lists)

## Fetched by
`.agents/tools/lib/fetch_references.py` (deterministic; re-run appends new
entries without clobbering existing ones).
