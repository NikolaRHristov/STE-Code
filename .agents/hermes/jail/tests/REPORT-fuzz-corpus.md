# Fuzz corpus report - jail shell argument analyser

Generator: `.agents/hermes/jail/tests/fuzz_corpus_generator.py` (stdlib only).

Run: `python3 .agents/hermes/jail/tests/fuzz_corpus_generator.py 3000`

- Commands generated: 3000 (15-25 tokens each; wrappers, chaining, redirects,
  `cd ..` prefixes, `$HOME`/`${HOME}`, quoting, tricky `-o`/`--output`/`-C`).
- Crashes (analyser raised): **0** - exit 0.
- Targets extracted: 16153. Corpus: 2.6 MB, 3000 JSONL lines at
  `.agents/hermes/jail/tests/fuzz_corpus.jsonl`.
- Escaping targets (resolved outside the repo root): 9821, as expected for a
  path pool deliberately weighted to `../`, `/tmp`, and `~`.

Label distribution top: `terminal(redirect)` 3433, then per-verb labels
(`mkdir`, `wget`, `tee`, `curl`, `dd`, `chmod`), `terminal(flag)` 1013,
`terminal(-C)` 451, `terminal(--directory)` 438.

Surprising behaviour (no defect, documented ceilings):

- `-o` is correctly scoped: `ps -o pid=` yields no target, while `curl -o ../x`
  does. The scoping table in `_EXTRA_DIR_FLAGS` holds up.
- `-C` and `--directory` are universal, so a wrapper such as `env -C /tmp`
  produces a write target even though `env -C` only changes directory.
- `tar -tzf` correctly yields nothing; `tar -czf ../x.tgz` is caught.

No analyser modifications were made.
