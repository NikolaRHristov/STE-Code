# Level 0 — Dictionary Excerpt (Approved / Unapproved)

This sub-document is the short dictionary excerpt that accompanies the fourteen
core principles in the Level 0 baseline of STE-Code. Together with
`01-principles.md`, it forms the complete deterministic base for code
documentation (API docs, commit messages, README sections, code comments).

The glossary is adapted from the ASD-STE100 Issue 9 dictionary (Part 2,
pages 149–434) and domain-adapted from aerospace to the code domain: aerospace
examples are replaced with code examples, while word alphabetization, the
STE/non-STE pair format, approved/unapproved status, and parts of speech are
preserved.

The full controlled terminology contains approximately 875 approved words and
1274 unapproved words. This Level 0 slice shows a short excerpt (the A entries)
plus the rules for reading any entry. Higher tiers bundle the complete
dictionary.

---

## How to Read This Dictionary

- **UPPERCASE words** are approved in STE-Code.
- **lowercase words** are not approved; use the listed STE alternatives instead.
- **(v)** = verb, **(n)** = noun, **(adj)** = adjective, **(adv)** = adverb,
  **(prep)** = preposition, **(conj)** = conjunction, **(pron)** = pronoun,
  **(art)** = article.
- **(TN)** = code-domain Technical Noun, **(TV)** = code-domain Technical Verb.
- Each entry shows the original rule text, a code-domain rewrite, and
  STE / non-STE code example pairs.
- An entry marked **UNNAPROVED** (lowercase) is forbidden; the entry lists the
  approved replacement(s) and example pairs that show the correction.

---

# A

## A (art) — APPROVED

Indefinite article. Use before a singular countable noun.

- Original: A FUEL PUMP IS INSTALLED IN ZONE 10.
- Code-domain: A CONFIG FILE IS INCLUDED IN THE ROOT DIRECTORY.

> STE: A config file is included in the root directory.
> Non-STE: Config files included in root directory.

---

## ABANDON (v) — UNNAPROVED

Not approved. Use **STOP (v)** or **TERMINATE (v)** instead.

- Original: GO (v), STOP (v). IF THERE IS A FIRE, IMMEDIATELY GO TO A SAFE AREA. / IF THE VALUES ARE INCORRECT, STOP THE TEST PROCEDURE.
- Code-domain: TERMINATE (v), STOP (v). IF THE BUILD FAILS, STOP THE DEPLOYMENT PIPELINE. / IF THE VALUES ARE INCORRECT, TERMINATE THE TEST RUN.

> STE: If the build fails, stop the deployment pipeline.
> Non-STE: If the build fails, abandon the deployment pipeline.

> STE: If the values are incorrect, terminate the test run.
> Non-STE: If the values are incorrect, abandon the test procedure.

---

## ABILITY (n) — UNNAPROVED

Not approved. Use **CAN (v)** instead.

- Original: CAN (v). ONE GENERATOR CAN SUPPLY POWER FOR ALL THE SYSTEMS.
- Code-domain: CAN (v). ONE CONFIGURATION CAN HANDLE REQUESTS FOR ALL THE ENDPOINTS.

> STE: One configuration can handle requests for all the endpoints.
> Non-STE: One configuration has the ability to handle requests for all the endpoints.

---

## Scope of This Slice

This excerpt covers the A entries only. The patterns it demonstrates — approved
articles, unapproved verbs replaced by approved verbs (ABANDON → STOP/TERMINATE),
and unapproved nouns replaced by modal verbs (ABILITY → CAN) — repeat across the
full A–Z dictionary bundled in higher STE-Code tiers.

For the gate that this glossary serves, see `01-principles.md` (the fourteen
core principles) and `02-synonyms.md`. A word is permitted in Level 0 only when
it is an approved word, a code-domain technical noun, or a code-domain technical
verb.
