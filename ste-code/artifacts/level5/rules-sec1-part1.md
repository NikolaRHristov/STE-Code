# Level 5 — Section 1 Rules, Part 1 (Words: 1.1–1.4, 1.10–1.14)

Level 5 is the full STE-Code standard. This sub-document is **Section 1, part 1**:
the nine word-level rules that decide *which words you may use, in what form, with
what meaning, and under which name*.

Rules in this part: **1.1, 1.2, 1.3, 1.4, 1.10, 1.11, 1.12, 1.13, 1.14**.
Rules 1.5–1.9 (technical-noun categories) are in Section 1, part 2.

Use this file when an LLM generates, rewrites, or reviews code documentation:
READMEs, API reference, docstrings and inline comments, commit messages, error
messages, and log output.

## How to apply this part

1. **Gate every word** (Rule 1.1): approved word, code-domain technical noun, or
   code-domain technical verb. Nothing else.
2. **Check the part of speech** (Rule 1.2) and the **meaning** (Rule 1.3).
3. **Check the form** (Rule 1.4): only the listed verb and adjective forms.
4. **Check the name** (Rules 1.10, 1.11): no slang or jargon; one name per item.
5. **Check verb use** (Rules 1.12, 1.13): technical verbs only where an approved
   verb is not sufficient, and never as nouns.
6. **Check the spelling** (Rule 1.14): American English, except in quoted text.

| Rule | Statement | One-line test |
|------|-----------|---------------|
| 1.1 | Use approved words, code-domain technical nouns, or code-domain technical verbs. | Does the word pass one of the three gates? |
| 1.2 | Use approved words only as the specified part of speech. | Is the word used as the part of speech it is approved for? |
| 1.3 | Use approved words only with their approved meanings. | Does the sentence use the one approved meaning? |
| 1.4 | Use only the approved forms of verbs and adjectives. | Is the form in the entry (no invented or `-ing` forms)? |
| 1.10 | Do not use regional, slang, or jargon words as code-domain technical nouns. | Would a developer from another community understand it? |
| 1.11 | Do not use different code-domain technical nouns for the same item. | Is this item called the same thing everywhere? |
| 1.12 | You can use verbs you can include in a code-domain technical verb category. | Is an approved verb sufficient instead? |
| 1.13 | Do not use code-domain technical verbs as nouns. | Is the action written as a verb, not as "do a X"? |
| 1.14 | Use American English spelling unless official directives tell you differently. | Is every unquoted word spelled American English? |

---

## Rule 1.1 — Use approved words, technical nouns, or technical verbs

In code documentation, use words that are:

- approved in the controlled terminology (part 2),
- code-domain technical nouns (Rule 1.5), or
- code-domain technical verbs (Rule 1.12).

A **code-domain technical noun** is a noun term for a specified concept in software
development, applicable to a subject field. A **code-domain technical verb** is a
verb term for a specified operation or process in software development.

The controlled terminology also lists words that are **not** approved, with the
approved alternative. Your project glossary or terminology database holds the
technical nouns and verbs; check it first, then this rule.

Rule 1.1 is the gatekeeping rule: every word in every sentence must pass one gate.
Names of tools, files, commands, classes, and endpoints are technical nouns and do
not need approval. The prose around them does.

### Core substitutions

| Do not write | Write |
|--------------|-------|
| execute | run |
| generate, construct | make |
| configure | set |
| retrieve, fetch | get |
| transmit | send |
| delete, purge | remove |
| validate, verify, ensure | check |
| utilize, leverage | use |
| bootstrap, initiate, commence | start |
| terminate | stop |
| perform | do |
| unable to | cannot |
| invalid, malformed | incorrect, not correct |
| duration | time |
| prior to | before |
| implement | add, make |
| optimize (prose) | make faster, make smaller |

### By documentation type

- **README** — procedural sections take approved imperative verbs; descriptive
  sections take approved adjectives and adverbs ("large" not "substantial",
  "usual" not "conventional", "correct" not "valid").
- **API reference** — names are technical nouns; return, parameter, and error prose
  uses approved verbs.
- **Docstrings and comments** — shortest approved word available. `NOTE:` and
  `WARNING:` are approved nouns; `FIXME:` is a code-domain technical noun.
- **Commit messages** — the smallest vocabulary of all: add, fix, remove, update,
  set, make, check, run. "refactor" is allowed as a technical verb (Rule 1.12).
- **Error messages** — read by end users; no jargon, no slang, no abbreviation
  that is not a technical noun.

### Examples

> **Non-STE:** Execute the script to do the task.
>
> **STE:** Run the script to do the task.

> **Non-STE:** To begin utilizing the build toolchain, you must first generate the
> distributable artifact, then execute the compiled binary to bootstrap the local
> development service.
>
> **STE:** Use the build tool to make the binary. Run the binary to start the local
> service.

> **Non-STE (JSDoc):** Fetches a user record. `@param timeout` — The duration the
> client shall await a response prior to terminating the connection attempt.
>
> **STE (JSDoc):** Gets a user record. `@param timeout` — The time that the client
> waits for a response before it stops the connection.

> **Non-STE (Python):** `"""Performs validation on the input data to ensure it
> conforms to the expected schema."""`
>
> **STE (Python):** `"""Checks the input data against the schema. Gives True when
> the data is correct and False when the data is not correct."""`

> **Non-STE (commit):** `feat: implement JWT authentication middleware`
>
> **STE (commit):** `feat: add JWT authentication middleware`

> **Non-STE (CLI):** `Error: Unable to establish connection to the database. Please
> verify your credentials and retry.`
>
> **STE (CLI):** `Error: Cannot connect to the database. Check your credentials and
> try again.`

### Paradigm notes

- **Object-oriented** — class, method, interface, and pattern names are technical
  nouns (Rules 1.5, 1.6). In prose: make (not instantiate), get (not retrieve), set
  (not assign), call, send, keep (not maintain), "is a" / "has a".
- **Functional** — pure, immutable, monad, closure, higher-order function are
  technical nouns. map, fold, reduce, filter, compose, curry are technical verbs
  (Rule 1.12). "Apply" and "pure" carry both an approved sense and a functional
  sense; both are valid.
- **Procedural** — one approved imperative verb per step.
- **Declarative and systems** — keyword names are technical nouns; the surrounding
  instruction uses approved verbs.

### Edge cases

- A framework name that is also a common word (Rails, Spring, Django, Flask) is a
  technical noun when capitalized as a proper noun.
- Code keywords (`goto`, `break`, `continue`, `finally`) keep their code meaning;
  do not use them colloquially.
- Generated documentation (OpenAPI output, JSDoc stubs, godoc) may not follow the
  rule; human-written prose inside it must.
- A technical verb used inside a compound term is part of a technical noun.
- Loanwords and non-English words are not approved unless they are technical nouns.

---

## Rule 1.2 — Use approved words only as the specified part of speech

Each entry in the controlled terminology gives one part of speech. Use the word
only as that part of speech.

- "Query" is an approved **noun**, not a verb. Write "Send a query to the
  database", not "Query the database".
- "Static" is an approved **adjective**, not a verb. Write "Make the variable
  static", not "Static the variable".
- Some words are approved as more than one part of speech. "Call" is an approved
  verb and an approved noun; position in the sentence shows which.

When you replace a word, check that the replacement does not change the meaning.
If it does, restructure the sentence.

If a word is not in the controlled terminology:

1. Find the word in a standard English dictionary.
2. Find the best synonym that is approved in the controlled terminology.
3. Use that approved word, or build a different sentence from approved words.

### Part-of-speech violation table

| Violating form (do not use) | Error | Approved replacement |
|-----------------------------|-------|----------------------|
| Query the database / Cache the result / Queue the job / Log the error / Index the record | Technical noun used as verb | Send a query / Keep the result in the cache / Put the job in the queue / Write the error in the log / Use the index to find the record |
| Docker the app / Git the change / Kubectl the pod / Terraform the VPC | Tool name used as verb | Use Docker / Save with Git / Use `kubectl` / Use Terraform |
| Secure the endpoint / Empty the buffer / Silent the log | Adjective used as verb | Make the endpoint secure / Make the buffer empty / Make the log silent |
| Static the variable / Ready the worker / Live the connection | Adjective used as verb | Make the variable static / Make the worker ready / Make the connection live |
| Utilize the cache / Leverage the library / Employ the service | Unapproved verb (inflated) | Use the cache / Use the library / Use the service |
| Commence the build / Initiate the transfer / Terminate the process | Unapproved verb (inflated) | Start the build / Start the transfer / Stop the process |
| Orchestrate the services / Facilitate the sync | Unapproved verb | Control the services / Help the sync |

"Clear" is approved as both verb and adjective, so "Clear the flag" is allowed.
The **make + adjective** pattern applies to true adjectives such as "secure" and
"empty".

### Examples

> **Non-STE:** Query the database for user records.
>
> **STE:** Send a query to the database for user records.

> **Non-STE (comment):** `# Static the cache size so the value does not change.`
>
> **STE (comment):** `# Make the cache size static so the value does not change.`

> **Non-STE (comment):** `# Terraform the VPC, then Kubectl the pods into the cluster.`
>
> **STE (comment):** `# Use Terraform to make the VPC. Use kubectl to apply the pod configuration to the cluster.`

---

## Rule 1.3 — Use approved words only with their approved meanings

An approved word carries exactly one approved meaning. Using the right word with
the wrong meaning is the most common class of documentation error.

### Procedure

1. Identify the part of speech of the word.
2. Read the approved meaning in the controlled terminology.
3. Compare it to the meaning you intend.
4. If they do not match, use a different approved word or restructure.

### Most-misused approved words

| Approved word | Approved meaning (only this) | Wrong meaning to avoid | Use instead |
|---------------|------------------------------|------------------------|-------------|
| run | execute a program or command | operate, manage, continue | operate, manage, continue |
| return | send a value back from a function to its caller | go back to a state or location | go back |
| call | invoke a function, method, or subroutine | name something | name, refer to as |
| get | fetch or retrieve data from a source | become, understand | become, understand, receive |
| set | put a value into a variable or configuration | become solid, prepare | become solid, prepare |
| make | bring into existence by building or assembling | force, earn | cause, earn |
| send | transmit data to a destination | cause a person to go | cause to go |
| raise | cause an exception or error to occur | increase, lift | increase, lift |
| catch | handle or intercept an exception | capture, become trapped | capture, become trapped |
| pass | give data as an argument to a function | go past, succeed | go past, succeed, give |
| check | examine something to determine correctness or state | stop, restrain | stop, leave |
| break | exit a loop or switch statement immediately | divide, damage, interrupt | split, damage, interrupt |
| continue | skip to the next iteration of a loop | keep doing without interruption | keep |
| fail | an operation did not complete successfully | not pass a test | not pass |
| move | transfer ownership of a value (Rust) | change physical position | go, change position |
| borrow | take a reference without taking ownership | take temporarily | take temporarily |
| follow | come after, go after | act in accordance with | obey |

### Examples

> **Non-STE:** Follow the configuration steps to set up the server.
>
> **STE:** Obey the configuration instructions to set up the server. Then do the
> steps that follow.

> **Non-STE (docstring):** `"""The function will return you to the login screen."""`
>
> **STE (docstring):** `"""The function will go back to the login screen."""`

> **Non-STE:** The background worker runs every night.
>
> **STE:** The background worker operates every night.
> *(The writer means "operates on a schedule", not "executes a program".)*

> **Non-STE (comment):** `# We call this pattern the Repository Pattern.`
>
> **STE (comment):** `# We name this pattern the Repository Pattern.`

> **Non-STE (comment):** `# The middleware serves the cached page and then returns.`
>
> **STE (comment):** `# The middleware gives the cached page to the user and then goes back.`

---

## Rule 1.4 — Use only the approved forms of verbs and adjectives

The controlled terminology gives each approved verb with its approved forms, and
each approved adjective with its comparative and superlative forms where they
apply.

**Verbs** — `COMPILE (v), COMPILES, COMPILED, COMPILED`

| Infinitive / imperative | Simple present | Simple past | Past participle (as adjective) |
|-------------------------|----------------|-------------|--------------------------------|
| (To) Compile / Compile | Compile(s) | Compiled | Compiled |

Forms that are not listed are not allowed: "compilating" and "compilates" are not
forms of "compile".

**Adjectives** — `FAST (adj) (FASTER, FASTEST)`

Base: fast · Comparative: faster · Superlative: fastest.
Adjectives that form the comparative with "more" and "most" have no listed forms,
because "more" and "most" are approved words.

### Form rules by documentation type

- **README** — imperative (base form) for procedures; simple present for
  description. Do not use the `-ing` form as a main verb.
- **API reference** — simple present, third person singular, because the subject is
  the function: "gives", "accepts", "fails". `GIVE (v), GIVES, GAVE, GIVEN`. The
  past participle is an adjective ("the given input"), not a main verb.
- **Docstrings** — imperative for the first line, simple present for the rest. Do
  not mix forms for the same kind of content.
- **Commit messages** — imperative base form only. Not "Added", not "Adding".
- **Error messages and logs** — simple present or simple past of listed forms only.

### Examples

> **Non-STE:** The compiler is compilating the source files every time you save.
>
> **STE:** The compiler compiles the source files each time you save.

> **Non-STE:** This algorithm is more fast than the previous one.
>
> **STE:** This algorithm is faster than the previous one.

> **Non-STE (README):** After installing the dependencies, you can start compiling
> the project by running the build script.
>
> **STE (README):** After you install the dependencies, compile the project with the
> build script.

> **Non-STE (API):** This method is returning a sorted list of users. It is
> accepting an optional filter parameter and is throwing an error when the query is
> failing.
>
> **STE (API):** This method gives a sorted list of users. It accepts an optional
> filter parameter and gives an error when the query fails.

> **Non-STE (commit):** `Fixed memory leak in connection pool and adding timeout configuration`
>
> **STE (commit):** `Fix memory leak in connection pool and add timeout configuration`
