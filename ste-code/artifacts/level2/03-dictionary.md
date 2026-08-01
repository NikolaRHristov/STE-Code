# Level 2 — Adapted Dictionary (A–Z excerpt)

A code-domain adaptation of the ASD-STE100 Issue 9 dictionary (Part 2, pp. 149–434),
reshaped for use by an LLM that generates or reviews code documentation.

This slice teaches the STE approval model for words: which words are approved,
which are not, and how to rewrite unapproved words into approved ones. It uses
code-domain examples only (API docs, commit messages, README sections, code comments).

Use this slice when you:
- Write or review API documentation and reference pages
- Draft commit messages and pull-request descriptions
- Author README sections and module/package overviews
- Write inline code comments and docstrings

Scope note: this Level 2 slice shows the entry format with a few canonical examples
(letter **A**). The complete approved (~875) and unapproved (~1274) word lists are
bundled at higher STE-Code tiers (3/4/5). Do not invent words beyond what the
dictionary lists; for unknown words, prefer an approved verb or a technical noun.

---

## How to read an entry

- **UPPERCASE words** are approved in STE-Code — you may use them.
- **lowercase words** are unapproved — replace them with the listed alternative.
  Unapproved status is also marked with the tag **UNNAPROVED** on the entry.
- Each entry carries a part-of-speech tag:
  `(v)` verb · `(n)` noun · `(adj)` adjective · `(adv)` adverb ·
  `(prep)` preposition · `(conj)` conjunction · `(pron)` pronoun · `(art)` article
- Code-domain technical tags:
  `(TN)` = code-domain Technical Noun (e.g. *config*, *endpoint*, *pipeline*)
  `(TV)` = code-domain Technical Verb (e.g. *deploy*, *build*, *parse*)
- Every entry shows three things:
  1. the original ASD-STE100 rule text,
  2. the same idea rewritten for code documentation,
  3. one or more STE / non-STE code-example pairs demonstrating the approved form.

### LLM guidance

When generating or reviewing code documentation, prefer UPPERCASE-approved words
and the verbs listed as alternatives for unapproved words (e.g. use `STOP`/`TERMINATE`
instead of `abandon`, `CAN` instead of `ability to`). Keep the approved form as
the short, direct sentence; the non-STE form is the longer, indirect phrasing to avoid.

---

# A

## A (art) — APPROVED
Function word: indefinite article. Use before a singular countable noun.
- **Original:** A FUEL PUMP IS INSTALLED IN ZONE 10.
- **Code-domain:** A CONFIG FILE IS INCLUDED IN THE ROOT DIRECTORY.
- **STE:** A config file is included in the root directory.
- **Non-STE:** Config files included in root directory.

## ABANDON (v) — UNNAPROVED
Not approved. Replace with `STOP` (v) or `TERMINATE` (v).
- **Original:** GO (v), STOP (v). IF THERE IS A FIRE, IMMEDIATELY GO TO A SAFE AREA. / IF THE VALUES ARE INCORRECT, STOP THE TEST PROCEDURE.
- **Code-domain:** TERMINATE (v), STOP (v). IF THE BUILD FAILS, STOP THE DEPLOYMENT PIPELINE. / IF THE VALUES ARE INCORRECT, TERMINATE THE TEST RUN.
- **STE:** If the build fails, stop the deployment pipeline.
- **Non-STE:** If the build fails, abandon the deployment pipeline.
- **STE:** If the values are incorrect, terminate the test run.
- **Non-STE:** If the values are incorrect, abandon the test procedure.

## ABILITY (n) — UNNAPROVED
Not approved. Replace with `CAN` (v).
- **Original:** CAN (v). ONE GENERATOR CAN SUPPLY POWER FOR ALL THE SYSTEMS.
- **Code-domain:** CAN (v). ONE CONFIGURATION CAN HANDLE REQUESTS FOR ALL THE ENDPOINTS.
- **STE:** One configuration can handle requests for all the endpoints.
- **Non-STE:** One configuration has the ability to handle requests for all the endpoints.

---

## Quick substitutions (from this excerpt)

| Unapproved (avoid) | Approved replacement | Example (STE) |
| --- | --- | --- |
| abandon (v) | STOP (v), TERMINATE (v) | If the build fails, stop the deployment pipeline. |
| ability (n) (as "has the ability to") | CAN (v) | One configuration can handle all the endpoints. |

When you see an unapproved word in source text, swap it for the approved verb and
keep the sentence short and direct. Approved articles such as **A** stay as-is.

---

## Scope of this slice

This excerpt covers the A entries only. The patterns it demonstrates — approved
articles, unapproved verbs replaced by approved verbs (ABANDON → STOP/TERMINATE),
and unapproved nouns replaced by modal verbs (ABILITY → CAN) — repeat across the
full A–Z dictionary bundled in higher STE-Code tiers (3/4/5).

The Level 2 dictionary couples with `01-principles.md`, `02-synonyms.md`,
`04-templates.md`, and `05-grammar.md`. A word is permitted in Level 2 only when
it is an approved word, a code-domain technical noun `(TN)`, or a code-domain
technical verb `(TV)`.
