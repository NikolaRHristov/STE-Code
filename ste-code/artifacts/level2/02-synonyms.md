# Level 2 — Technical Noun Categories: Grammar Rules (Rule 1.5)

This is the Rule 1.5 slice of STE-Code Level 2: the **grammar rules for
using code-domain technical nouns**. Level 1 gave you the nineteen categories
and the three-word gate (Rules 1.1 / 1.5 / 1.6). Level 2 adds the
section-specific grammar that governs how a technical noun is written once you
have decided it is allowed.

All content below is faithful to the authoritative Rule 1.5 adaptation
(`final/rules/a-sec1-rule1.5.md`). Every example stays inside the code domain.
The rule numbers and categories are not invented.

## Rule 1.5 — recap (before the grammar)

**Rule 1.5** You can use words that you can include in a code-domain technical
noun category.

A code-domain technical noun is a noun term that refers to a specified concept
in software development and is applicable to a subject field. The controlled
terminology does not include all code-domain technical nouns because there are
too many, and each project or subject field uses different technical nouns.
You can find many of these in your project glossary or terminology database.

The nineteen categories (Level 1) are the gate: a non-approved word is
permitted only when it names a precise concept in one of them **and** is
registered in your glossary. Level 2 now covers how to write that noun
correctly — articles, compounds, possessive, plural, and capitalization.

## Grammar rule 1 — Articles with technical nouns

Technical nouns follow the same article rules as approved nouns:

- Use **"the"** for a specific instance.
- Use **"a" / "an"** for an indefinite instance.
- Use **no article** for plural general references.

Acceptable:
- The `UserController` handles a request. The controller returns a response.
- Kubernetes pods run in a namespace.

(`UserController` is a specific code component; `request` and `response` are
network terms; `pods` is a plural general reference.)

## Grammar rule 2 — Technical nouns as modifiers (compound phrases)

A technical noun can modify another noun to form a compound technical noun
phrase. When two technical nouns form a compound, the first functions as a
modifier and the second as the head noun. **Both must belong to a recognized
category.**

Acceptable:
- The Redis cache server stores the session data.
  (`Redis` (database) modifies `cache server` (systems); `session data` is a
  compound where `session` (runtime) modifies `data` (data structure).)
- The PostgreSQL connection pool uses a round-robin scheduler.
  (`PostgreSQL` (database) modifies `connection pool` (database);
  `round-robin` (algorithmic) modifies `scheduler` (systems).)

Not acceptable:
- The thing layer processes the stuff queue.
  (Neither "thing" nor "stuff" is a recognized technical noun.)

## Grammar rule 3 — The possessive form

The possessive (`'s`) is permitted **only** for category 11 — professional
roles, individuals, groups, organizations, and teams. Do **not** use the
possessive with any other category of technical noun. Use "of" constructions or
noun-as-modifier constructions instead.

Acceptable:
- The user's session data is encrypted. (Category 11 permits possessive.)
- The configuration of the Docker container is stored in a YAML file.
  (Category 5 — use "of".)

Not acceptable:
- The Docker container's configuration is stored in a YAML file.
  (Category 5 does not permit possessive — use "of".)

## Grammar rule 4 — Pluralization

Technical nouns follow standard English pluralization. Acronyms and
initialisms form plurals by adding a lowercase **"s" without an apostrophe**.

Acceptable:
- The system uses two APIs and three SQL queries.
  (`APIs` is the plural of `API` (network); `queries` is the plural of
  `query` (database).)

Not acceptable:
- The system uses two API's and three SQL's.
  (The apostrophe incorrectly suggests possession. Use `APIs` and
  `SQL queries`.)

## Grammar rule 5 — Capitalization

Code-domain technical nouns that are **proper nouns** (programming language
names, company names, product names) keep their original capitalization.
**Common** technical nouns (for example `controller`, `endpoint`,
`middleware`) use lowercase unless they are the first word of a sentence.

Acceptable:
- The TypeScript compiler checks the types. The controller handles the request.
  (`TypeScript` is a proper noun (development tool); `controller` is a common
  technical noun (code component).)

Not acceptable:
- The typescript compiler checks the Types. The Controller handles the request.
  (`typescript` should be `TypeScript`; `Types` and `Controller` should be
  lowercase — not first word, not proper nouns.)

## Grammar-sensitive edge cases

These cases change how the grammar rules above apply.

### Framework names that are also common words

Some frameworks use common English words as names (`React`, `Vue`, `Swift`,
`Go`, `Rust`, `Elm`, `Next`, `Nest`). The framework name is a code-domain
technical noun (category 3 or 5) and does not follow the approved meaning of
the common word.

Acceptable:
- Use the React framework to build the user interface. (`React` is a
  development tool, not the verb "react".)
- The Go compiler builds the binary. (`Go` is a development tool, not the
  verb "go".)

When a sentence is ambiguous without capitalization (for example "use swift to
process the data"), always capitalize the framework name or use the full term
("the Swift language", "the Rust compiler") to distinguish it from an approved
word.

### Code keywords inside documentation

Code keywords (`if`, `else`, `for`, `while`, `return`, `class`, `def`, `fn`,
`let`, `const`, `var`, `async`, `await`) are **quoted text (category 10)** when
they appear in documentation. They do not need to be technical nouns. When you
use them as English words in a sentence, they must follow approved meanings.

Acceptable:
- The `if` statement checks the condition. (`if` is quoted text; the
  surrounding sentence uses approved words.)

Not acceptable:
- If the request fails, return a 500. (`500` is an HTTP status code — quoted
  text or a category 9 noun. Write `404 Not Found` or `500`.)

Acceptable:
- If the request fails, return `500 Internal Server Error`. (Status code is
  quoted text, category 10.)

### Abbreviations and acronyms

Code-domain technical nouns often appear as abbreviations or acronyms (`API`,
`JSON`, `SQL`, `HTML`, `CSS`, `HTTP`, `TCP`, `TLS`, `DNS`, `URL`). These are
permissible under Rule 1.5 (categories 16, 18, or 19). However, you must define
each abbreviation at its first use in a document, unless it is universally
understood by the target audience.

Acceptable (first use):
- The application programming interface (API) uses Hypertext Transfer Protocol
  Secure (HTTPS).

Acceptable (subsequent use):
- The API returns a JSON response over HTTPS.

Not acceptable:
- The API leverages HTTPS to transmit the payload. (Non-approved "leverage" →
  use "use"; non-approved "transmit" → use "send"; non-approved "payload" →
  use "data" or define as a technical noun.)

### Numbers as technical nouns

Quantitative values that name a configuration, version, status, or port are
code-domain technical nouns in category 9 when the value is a fixed, named
token rather than a measured quantity. Version numbers (`Node.js 18`), HTTP
status codes (`404`), and port numbers (`port 5432`) are quoted text or
category 9 nouns and must appear verbatim.

Acceptable:
- The service runs on port 5432 and returns `404 Not Found` when the row is
  absent. (`port 5432` is a category 9 noun; `404 Not Found` is quoted text.)

Not acceptable:
- The service runs on the default db port and gives a not found error.
  (Imprecise — use "port 5432" and "`404 Not Found`".)

## Cross-references

- **Rule 1.1 (Approved Words):** the dictionary for all common vocabulary;
  Rule 1.5 is the exception for domain-specific nouns.
- **Rule 1.2 (Part of Speech):** a technical noun is used only as a noun or
  noun modifier — never as a verb.
- **Rule 1.3 (Approved Meanings):** a technical noun carries the meaning
  registered in your glossary; do not reuse it with another meaning.
- **Rule 1.6 (Non-Approved Words):** forbids every non-approved word that is
  not a code-domain technical noun. Read Rules 1.5 and 1.6 together.
- **Rule 1.7 (Technical Nouns as Verbs):** a code-domain technical noun cannot
  be used as a verb (for example "host" is a noun; use "make available" or
  "run" as the verb).
- **Rule 1.8 (Standard Technical Nouns):** use well-known terms; do not invent
  a new term when a standard one exists.
- **Rule 1.9 (Short Technical Nouns):** prefer short, clear technical nouns
  over long, obscure ones.
- **Rule 1.11 (One Term per Concept):** each technical noun refers to exactly
  one concept in your project.
- **Rule 1.12 (Technical Verbs):** technical verbs (`build`, `deploy`, `test`,
  `lint`, `compile`, `debug`) are permitted but are a separate category from
  technical nouns.

## Summary

Level 2 adds the grammar layer on top of Level 1's nineteen categories. A
code-domain technical noun is written with correct articles, may modify other
nouns to form compound phrases, takes the possessive only when it is a
category-11 role/org term, pluralizes without an apostrophe, and keeps
proper-noun capitalization. Framework names that double as common words,
quoted code keywords, abbreviations, and fixed numeric tokens each have their
own handling. Together with Rules 1.1 and 1.6, these rules leave documentation
with only two kinds of words: approved STE-Code words for common vocabulary,
and code-domain technical nouns for domain-specific concepts — and the grammar
rules above govern how the second kind is written.
