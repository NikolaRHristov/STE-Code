# Level 0 — Core Principles

STE-Code Level 0 is the baseline. It collects the fourteen core principles that
govern controlled vocabulary in code documentation, plus a short dictionary
excerpt of code-domain technical terms. Everything below is faithful to the
STE-Code standard: no rules are invented, and every example stays inside the
code domain (no aerospace or other subject-field leakage).

The principles form a gate. Every word in every sentence of code documentation
must pass one of them: it is an approved word in the controlled terminology, a
code-domain technical noun, or a code-domain technical verb.

---

## The Fourteen Principles

**Rule 1.1 — Use words that are approved in the dictionary, technical nouns, or technical verbs.**
Use only vocabulary that is (a) listed in the controlled terminology, (b) a
code-domain technical noun such as `UserAuthenticator`, or (c) a code-domain
technical verb such as `serialize`. A sentence like
"Run the script to do the task" passes because `run` is an approved verb.

**Rule 1.2 — Use approved words only as the specified part of speech.**
A word approved as a noun must not be forced into verb service. Do not write
"Docker the app"; write "Use Docker to build the app." The technical noun
`query` stays a noun — use "Send a query to the database," not "Query the
database."

**Rule 1.3 — Use approved words only with their approved meanings.**
An approved verb keeps its controlled meaning. "The worker runs every night"
is correct only when you mean execute; if you mean manage, write "operates."

**Rule 1.4 — Use only the approved forms of verbs and adjectives.**
Use the approved inflection: `run / ran / run` for the verb, `large / larger /
largest` for the adjective — never unlisted variants.

**Rule 1.5 — You can use words that you can include in a code-domain technical noun category.**
Words outside the dictionary are allowed when they name a precise concept in one
of the nineteen code-domain categories — for example `Promise`, `User`, `ApiError`.

**Rule 1.6 — Use a word that is not approved in the dictionary, only when it is a code-domain technical noun or part of a code-domain technical noun.**
A non-approved word must be a registered code-domain technical noun (such as
`ValidationError`) or it is forbidden.

**Rule 1.7 — Do not use words that are technical nouns as verbs.**
"Cache the result" is wrong when `cache` is a noun; write "Keep the result in
the cache."

**Rule 1.8 — Use technical nouns that are approved in your project, company, industry, or subject field.**
Register project-specific nouns (`aws_instance`, `kubernetes_deployment`) in
your glossary and reuse them exactly.

**Rule 1.9 — When you must select a technical noun, use one which is short and easy to understand.**
Prefer `socket` over `realtime_notification_channel`; short nouns read faster.

**Rule 1.10 — Do not use regional, slang, or jargon words as technical nouns.**
"No worries" and "utilize" are not technical nouns; use `use` and `use` instead.

**Rule 超额1.11 — Do not use different technical nouns for the same item.**
One concept, one term. If your README says `auth middleware`, the API docs and
docstrings must say `auth middleware` — not `auth layer`.

**Rule 1.12 — You can use verbs that you can include in a technical verb category.**
Code-domain technical verbs (`map`, `filter`, `fold`, `reduce`, `compose`,
`curry`) are permitted even though they are not in the approved-word list.

**Rule 1.13 — Do not use technical verbs as nouns.**
"Refactor the module" is fine as a verb; do not write "The refactor of the
module" when `refactor` is a verb, not a noun.

**Rule 1.14 — Use American English spelling unless other official directives tell you differently.**
`color`, `center`, `initialize` — not `colour`, `centre`, `initialise`.

---

## Short Dictionary Excerpt (code-domain examples)

| Type | Example | Notes |
|------|---------|-------|
| Approved verb | `run`, `make`, `get`, `set`, `send` | General-purpose STE-Code verbs |
| Code-domain technical noun | `UserAuthenticator`, `Promise`, `aws_instance` | Registered in project glossary |
| Code-domain technical verb | `serialize`, `map`, `filter`, `refactor` | Permitted under Rule 1.12 |
| Adjective (approved) | `large`, `static`, `secure` | Use only as adjectives, never as verbs |

**Non-STE vs STE (canonical pair):**

> Non-STE: Query the database for user records.
> STE: Send a query to the database for user records.

> Non-STE: Docker the app and deploy to production.
> STE: Use Docker to make a container for the app. Deploy the container to production.

These fourteen principles, together with the dictionary excerpt, are the complete
Level 0 slice. They are the deterministic base from which higher tiers build.
