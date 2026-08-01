# Release audit prompt

Paste this into an LLM (or run it through `hermes -z`) when the deterministic
scan is clean but you want a judgement call on wording, or when `sync.py`
reports an **ambiguous** count it refuses to guess.

The tools decide *numbers*. The LLM decides *meaning*. Never let the model
invent a count — it only ever chooses between candidates the tools measured.

---

## Prompt: resolve an ambiguous count

```
You are auditing release claims for STE-Code, a controlled-language
documentation standard adapted from ASD-STE100.

Measured facts (authoritative, from disk — do not contradict these):
{paste the output of: python3 .agents/tools/release/facts.py}

A claim scanner flagged this line because its number matches none of the
measured facts for that claim:

  File:     {file}:{line}
  Claim:    {claim-id}
  Found:    {found}
  Expected: one of {candidates}
  Line:     {the full line}

Decide exactly one of:

  A. STALE  — the line means the same quantity as the fact and the number is
              simply out of date. Reply: STALE <value>
  B. OTHER  — the line means a genuinely different quantity that happens to
              collide with the pattern. Reply: OTHER <one-sentence reason>
  C. QUOTE  — the line deliberately quotes a historical mistake or an example
              from the standard's own content. Reply: QUOTE <reason>

Reply with the verdict line only. No preamble.
```

Apply the verdict:

| Verdict | Action |
|---------|--------|
| `STALE 22` | `python3 .agents/tools/release/sync.py --pick <claim-id>=22` |
| `OTHER …` | append `<!-- release-scan:ignore -->` to that line |
| `QUOTE …` | append `<!-- release-scan:ignore -->` to that line |

---

## Prompt: review generated release notes

```
You are reviewing release notes for STE-Code before publication.

Notes:
{paste: python3 .agents/tools/release/changelog.py --notes <version>}

Measured facts:
{paste: python3 .agents/tools/release/facts.py}

Check only these, and report findings as a short list:

1. Any stated number that contradicts the measured facts.
2. Any entry that describes internal pipeline bookkeeping rather than a
   user-visible change (candidate for the NOISE filter in changelog.py).
3. Any entry whose subject line is too vague to tell a reader what changed.
4. Missing breaking-change callouts: an entry that clearly changes an
   interface, path, or output format but is not listed under Breaking.

If everything is sound, reply exactly: NOTES OK
```

A finding of type 2 means the pattern belongs in `changelog.py`'s `NOISE`
regex — fix the filter, not the notes, so the next release inherits it.

---

## Prompt: post-release documentation sweep

Run after `--execute`, once the scan is green. Catches prose the scanner
cannot see, because it reads meaning rather than digits.

```
You are checking STE-Code documentation for claims that are stale in ways a
regex cannot detect.

Measured facts:
{paste: python3 .agents/tools/release/facts.py}

Documents:
{paste README.md, docs/index.md, ste-code/README.md}

Find statements that are now wrong or misleading, such as:
  - a pipeline described with the wrong number of stages or wrong stage names
  - a file path that no longer exists
  - a described capability that the facts contradict
  - a tier table whose "best for" advice conflicts with its measured size
  - language implying work is pending that the facts show is complete

For each, output: <file> | <quoted phrase> | <why it is wrong> | <fix>
If nothing is wrong, reply exactly: DOCS OK
```

---

## Running these through Hermes

```bash
python3 .agents/tools/release/facts.py > .agents/tmp/facts.txt
python3 .agents/tools/release/scan.py --json > .agents/tmp/drift.json

hermes -z "$(cat .agents/tools/release/prompts/audit.md)
FACTS:
$(cat .agents/tmp/facts.txt)
DRIFT:
$(cat .agents/tmp/drift.json)"
```

Keep scratch files in `.agents/tmp/` and delete them afterwards — they are
never part of a release.
