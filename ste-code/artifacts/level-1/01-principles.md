# Level -1 — Core Principles (Word Choice)

STE-Code is a controlled language for code documentation, adapted from
ASD-STE100 Simplified Technical English. This sub-document gives the 14 core
principles of Section 1 (words). They govern **which words you may use, in
which part of speech, and with which meaning**.

Scope of this slice: word choice only. Sentence, procedure, and description
rules live in later sections.

Three word sources are permitted, and only three:

1. Words approved in the STE-Code controlled terminology.
2. Code-domain technical nouns (names of real things in software).
3. Code-domain technical verbs (names of real operations in software).

Definitions used throughout:

- **Code-domain technical noun** — a noun term that refers to a specified
  concept in software development and is applicable to a subject field
  (for example `UserService`, `backup file`, API endpoint).
- **Code-domain technical verb** — a verb term that refers to a specified
  operation or process in software development (for example compile, lint,
  deploy, mock).
- **Controlled terminology** — the STE-Code word list (part 2). It replaces
  the STE dictionary.

## Quick index

| Rule | Principle |
|------|-----------|
| 1.1 | Use approved words, code-domain technical nouns, or code-domain technical verbs. |
| 1.2 | Use approved words only as the specified part of speech. |
| 1.3 | Use approved words only with their approved meanings. |
| 1.4 | Use only the approved forms of verbs and adjectives. |
| 1.5 | You may use words that fit a code-domain technical noun category. |
| 1.6 | Use an unapproved word only when it is (part of) a code-domain technical noun. |
| 1.7 | Do not use code-domain technical nouns as verbs. |
| 1.8 | Use the code-domain technical nouns approved in your project or field. |
| 1.9 | When you must choose a technical noun, choose a short and clear one. |
| 1.10 | Do not use regional, slang, or jargon words as technical nouns. |
| 1.11 | Do not use different technical nouns for the same item. |
| 1.12 | You may use verbs that fit a code-domain technical verb category. |
| 1.13 | Do not use code-domain technical verbs as nouns. |
| 1.14 | Use American English spelling unless official directives say otherwise. |

## The 14 principles

### Rule 1.1 — Use approved words, code-domain technical nouns, or technical verbs

Use words that are approved in the project controlled terminology, or that are
code-domain technical nouns, or that are code-domain technical verbs. Words
outside these three sources are not permitted.

The controlled terminology also lists words that are **not** approved, together
with approved alternatives. Your project glossary, API reference, and coding
standards are the normal home of your technical nouns and verbs.

- Approved verb: `use`.
- Code-domain technical noun: `cache`.
- Code-domain technical verb: `compile`.

### Rule 1.2 — Use approved words only as the specified part of speech

Each approved word carries one or more parts of speech. Use it only in those.

"Query" is an approved noun, but not an approved verb.

> **Do not write:** Query the database for all active users.
>
> **Write:** Do a query of the database for all active users.

Some words are approved as more than one part of speech; sentence position
shows the function. When an approved alternative has a *different* part of
speech, change the sentence construction — never force a word-for-word swap
that changes the meaning.

If a word you want is not in the controlled terminology:

1. Find the word in an English dictionary.
2. Find the best approved synonym.
3. Use that approved word, or rewrite the sentence with other approved words.

### Rule 1.3 — Use approved words only with their approved meanings

Each approved word has one specified meaning, often narrower than in standard
English. Do not borrow other senses.

- `follow` = "come after, go after" — use it for the sequence of steps.
- `obey` = "to do that which the procedures or instructions tell you".

Four-step check for every approved word you write:

1. Identify the part of speech in your sentence.
2. Look the word up in the controlled terminology for that part of speech.
3. Compare your intended meaning with the approved meaning.
4. If they differ, choose a different approved word or rewrite the sentence.

### Rule 1.4 — Use only the approved forms of verbs and adjectives

The controlled terminology gives each approved verb with its approved forms,
and each adjective with its comparative and superlative forms where they
apply.

`COMPILE (v), COMPILES, COMPILED, COMPILED`

| Infinitive / Imperative | Simple present | Simple past | Past participle (as adjective) |
|--------------------------|----------------|-------------|-------------------------------|
| (To) compile / Compile | Compile(s) | Compiled | Compiled |

Adjectives that form comparatives with "more" and "most" do not list those
forms, because "more" and "most" are themselves approved words.

### Rule 1.5 — You may use words that fit a code-domain technical noun category

A code-domain technical noun refers to a specified concept in software
development. The controlled terminology cannot list them all: each project and
subject field has its own. Take them from your project glossary, API
documentation, or terminology database.

STE-Code gives categories so that you can (a) select technical nouns for your
glossary and (b) use them correctly. A word qualifies as a code-domain
technical noun when it fits one or more of those categories — for example
computer science and information technology terms, database and storage
terminology, official documents and standards, numbers and units, quoted text,
professional roles, and environmental or operational conditions.

### Rule 1.6 — Use an unapproved word only when it is (part of) a technical noun

A word that is not approved may still be used when it fits a technical noun
category, or when it is part of a multi-word technical noun.

> **Do not write:** Make sure that the two handles at the base of the panel engage.
>
> **Write:** Make sure that the two handles at the bottom of the panel engage.

But `base` is permitted as a technical noun (mathematical and engineering
terms) — for example "base 16", "base class".

`backup` is not approved as a general word; its alternatives are "emergency
(n)" and "auxiliary (adj)". It **is** permitted as a code-domain technical
noun, and as part of the two-word technical noun `backup file`.

The same word can belong to different categories when it carries different
meanings in different contexts. Do not replace a word that is part of an
established technical noun: the replacement is no longer the approved term.

### Rule 1.7 — Do not use code-domain technical nouns as verbs

Use a technical noun only as a noun, or as an adjective inside another
technical noun. Rewrite the sentence instead of verbing it.

> **Do not write:** Database the results after the job finishes.
>
> **Write:** Write the results to the database after the job finishes.

In some contexts the same word is both a technical noun (rule 1.5) and a
technical verb (rule 1.12). That is permitted only when the word genuinely
fits both category systems.

> **See also:** Rule 1.5, Rule 1.12.

### Rule 1.8 — Use the code-domain technical nouns approved in your project or field

If your project, company, industry, or subject field already has an approved
name for a class, module, function, method, variable, component, or process,
use that name. These names live in your project glossary, API documentation,
coding standards, and — above all — in the source tree.

Do not invent your own name for something that already has one. The reader must
be able to search the repository for the word you wrote.

> **Do not write:** The account controller manages login and user profile operations.
>
> **Write:** The `AccountController` manages authentication and user profile operations.

### Rule 1.9 — Choose a short and clear technical noun

When no approved technical noun exists, select one that is short (not more than
three words) and easy to understand. Do not write a long descriptive phrase
where a short term is unambiguous. A line number, a code snippet, or an API
reference identifies the item, in the same way that an index number and an
illustration do in printed procedures. Add one or two adjectives only when the
reader needs them.

> **Do not write:** Call the asynchronous JavaScript XML HTTP request wrapper utility function (line 42) to get the serialized JSON payload from the remote application programming interface endpoint.
>
> **Write:** Call the `fetchUtility` function (line 42) to get the JSON data from the API endpoint.

### Rule 1.10 — Do not use regional, slang, or jargon words as technical nouns

Some words are used only inside one community or one technology ecosystem.
Readers from a different background, a different stack, or a different first
language will not understand them. Choose well-known words.

> **Do not write:** Remove all the cruft from the legacy module.
>
> **Write:** Remove all the unnecessary code from the legacy module.

### Rule 1.11 — Do not use different technical nouns for the same item

One item, one name, everywhere in the documentation. When the name changes
between sections, the reader cannot tell whether you mean one item or several.
The source of truth is the code: the class, function, module, table, resource,
environment variable, or configuration key as it is defined in the repository.

> **Do not write:**
>
> 1. Initialize the `UserService` class to start the session manager.
> 2. Call the authenticate method on the `AccountManager` to verify a user.
> 3. The `UserHandler` returns a session token.

> **Write:**
>
> 1. Initialize the `UserService` class to start the session manager.
> 2. Call the authenticate method on the `UserService` to verify a user.
> 3. The `UserService` returns a session token.

### Rule 1.12 — You may use verbs that fit a code-domain technical verb category

A code-domain technical verb refers to a specified operation or process in
software development. The controlled terminology cannot list them all. Take
them from your project glossary or terminology database, and obey the same verb
rules that apply to every other approved verb.

A verb qualifies when it fits one or more of these four categories:

| # | Category | Examples |
|---|----------|----------|
| 1a | Write and modify code | compile, concatenate, import, inject, instantiate, lint, minify, marshal, optimize, polyfill, refactor, resolve, shim, stub, substitute, tokenize, transpile, trace, vectorize |
| 1b | Test and verify code | assert, benchmark, debug, fuzz, instrument, mock, profile, snapshot, spy, stub, unit-test |
| 1c | Build and package | bundle, deploy, package, publish, release, tag, version |
| 1d | Manage dependencies | hoist, install, link, lock, pin, update, upgrade |
| 2a | Input and output processes | click, copy, cut, digitize, enter, paste, press, print, scan, swipe, tap, type |

### Rule 1.13 — Do not use code-domain technical verbs as nouns

Use technical verbs only as verbs. When you need a noun, find an approved noun
or a code-domain technical noun with the equivalent meaning.

> **Do not write:** Do a build of the project. The function does a parse of the input string.
>
> **Write:** Build the project. The function parses the input string.

When the API returns a named artifact — a `Build` object, a `Deployment`
resource — that noun is a code-domain technical noun (rule 1.5), not a misused
verb. A word may belong to both category systems, as `stub` does.

> **See also:** Rule 1.5, Rule 1.7, Rule 1.12.

### Rule 1.14 — Use American English spelling

Use the spelling given in the STE-Code controlled terminology, which is
American English. Use a different spelling only when a project specification,
style guide, contract, or other official directive requires it.

> **Do not write:** Initialise the variable before you use it in the loop.
>
> **Write:** Initialize the variable before you use it in the loop.

> **Do not write:** The log file shows the colour of each output line.
>
> **Write:** The log file shows the color of each output line.

Do not change the spelling inside quoted text — an error message, a code
comment, a user interface string. Keep it exactly as it appears:

> **Write:** The terminal shows the message `Colour profile not recognised`.

> **See also:** Rule 8.6 — Use quoted texts correctly.

## Application order (for generators)

1. Is the word approved? If yes, check part of speech (1.2), meaning (1.3), and
   form (1.4).
2. If not approved: is it a code-domain technical noun (1.5, 1.6) or technical
   verb (1.12)? Prefer the term already approved in the project (1.8), short
   and clear (1.9), free of jargon (1.10), and used consistently (1.11).
3. Never cross word classes: nouns are not verbs (1.7), verbs are not nouns
   (1.13).
4. Spell it in American English (1.14), except inside quoted text.
