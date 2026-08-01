# Level 1 — Core Principles (Words)

STE-Code Level 1 controls **which words you may use** in code documentation.
Every other level builds on it. This file is the LLM-facing form of Section 1
(Rules 1.1–1.14), plus ready-to-use document templates.

## Contract

Every word in code documentation must pass one of three gates:

1. It is **approved in the controlled terminology** (the STE-Code dictionary).
2. It is a **code-domain technical noun** (Rule 1.5 categories).
3. It is a **code-domain technical verb** (Rule 1.12).

If a word passes none of the three gates, it is forbidden. There is no fourth
category.

Scope: README files, API reference, docstrings, inline comments, commit
messages, error messages, test specifications, code review and PR feedback.

## Principle index (P1–P14)

| ID | Rule | Principle |
|----|------|-----------|
| P1 | 1.1 | Use words that are approved in the controlled terminology, code-domain technical nouns, or code-domain technical verbs. |
| P2 | 1.2 | Use approved words only as the specified part of speech. |
| P3 | 1.3 | Use approved words only with their approved meanings. |
| P4 | 1.4 | Use only the approved forms of verbs and adjectives. |
| P5 | 1.5 | You can use words that fit a code-domain technical noun category (19 categories). |
| P6 | 1.6 | Use a non-approved word only when it is a code-domain technical noun, or part of one. |
| P7 | 1.7 | Do not use words that are technical nouns as verbs. |
| P8 | 1.8 | Use technical nouns that are approved in your project, company, industry, or subject field. |
| P9 | 1.9 | When you must select a technical noun, use one which is short and easy to understand. |
| P10 | 1.10 | Do not use regional, slang, or jargon words as technical nouns. |
| P11 | 1.11 | Do not use different technical nouns for the same item. |
| P12 | 1.12 | You can use verbs that fit a technical verb category. |
| P13 | 1.13 | Do not use technical verbs as nouns. |
| P14 | 1.14 | Use American English spelling unless other official directives tell you differently. |

## P1 (Rule 1.1) — Approved words, technical nouns, technical verbs

In code documentation, use words that are approved in the project controlled
terminology, code-domain technical nouns, or code-domain technical verbs.

- A **code-domain technical noun** names a concept in software development
  (`UserAuthenticator`, `connection pool`, `stack trace`).
- A **code-domain technical verb** names an operation or process
  (`serialize`, `compile`, `deploy`).
- The controlled terminology also lists non-approved words with approved
  alternatives. Keep both lists in the project glossary.

Common substitutions:

| Do not write | Write |
|---|---|
| execute, invoke (prose) | run, call |
| generate, construct, instantiate | make |
| configure, assign | set |
| retrieve, fetch | get |
| transmit | send |
| delete, purge | remove |
| validate, verify, ensure | check |
| utilize, leverage, employ | use |
| initiate, commence, bootstrap | start |
| terminate | stop |
| unable to | cannot |
| invalid, malformed | not correct |
| maintain | keep |
| perform | do |
| optimize | make faster, make smaller |
| aggregate | collect |
| persists | continues |
| prior to | before |

Examples:

> **Non-STE:** To begin utilizing the build toolchain, you must first generate
> the distributable artifact, then execute the compiled binary to bootstrap the
> local development service.
>
> **STE:** Use the build tool to make the binary. Run the binary to start the
> local service.

> **Non-STE:** `Error: Unable to establish connection to the database. Please
> verify your credentials and retry.`
>
> **STE:** `Error: Cannot connect to the database. Check your credentials and
> try again.`

> **Non-STE:** `feat: implement JWT authentication middleware for API routes`
>
> **STE:** `feat: add JWT authentication middleware for API routes`

## P2 (Rule 1.2) — One part of speech per approved word

Each approved word has a specified part of speech. Use the word only as that
part of speech.

- "query" is an approved noun, not a verb → "Send a query to the database."
- "static" is an approved adjective, not a verb → "Make the variable static."
- Some words are approved as more than one part of speech ("call" is a verb and
  a noun). Sentence position shows which one you use.

| Violating form | Error | Write instead |
|---|---|---|
| Query the database / Cache the result / Queue the job / Log the error | Technical noun used as verb | Send a query / Keep the result in the cache / Put the job in the queue / Write the error in the log |
| Docker the app / Git the change / Terraform the VPC | Tool name used as verb | Use Docker / Save with Git / Use Terraform |
| Secure the endpoint / Empty the buffer | Adjective used as verb | Make the endpoint secure / Make the buffer empty |
| Static the variable / Ready the worker | Adjective used as verb | Make the variable static / Make the worker ready |
| Utilize the cache / Leverage the library | Unapproved verb | Use the cache / Use the library |
| Orchestrate the services / Facilitate the sync | Unapproved verb | Control the services / Help the sync |

If a word is not in the controlled terminology: find it in a standard English
dictionary, find the best approved synonym, then use the approved word or a
different sentence construction.

## P3 (Rule 1.3) — Approved meanings only

Each approved word has one or more approved meanings, often more restricted
than standard English. Do not use an approved word with a meaning it does not
have in the controlled terminology.

Check procedure for each word:

1. Identify the part of speech as you wrote it.
2. Look up the approved meaning for that part of speech.
3. Ask whether your sentence uses exactly that meaning.
4. If not, replace the word or restructure the sentence.

> **Sentence:** The background worker runs every night.
> The approved meaning of the verb "run" is "execute a program or command."
> The writer means "operates on a schedule" — the meaning does not match.
> **Rewrite:** The background worker operates every night.

## P4 (Rule 1.4) — Approved verb and adjective forms only

The controlled terminology gives each approved verb with its approved forms,
and each approved adjective with its comparative and superlative forms.

| Infinitive/Imperative | Simple present | Simple past | Past participle |
|---|---|---|---|
| (To) Compile / Compile | Compile(s) | Compiled | Compiled |

`FAST (adj) (FASTER, FASTEST)` — base, comparative, superlative.
Adjectives that form the comparative with "more" and "most" have no listed
forms, because "more" and "most" are approved words.

Do not invent forms such as "compilating" or "compilates."

> **Non-STE:** The compiler is compilating the source files every time you save.
>
> **STE:** The compiler compiles the source files each time you save.

## P5 (Rule 1.5) — The 19 code-domain technical noun categories

You may use a word that is not in the controlled terminology when you can put
it in one or more of these categories. The examples are not a full list.

| # | Category | Examples |
|---|---|---|
| 1 | Code components, modules, and libraries | class, controller, helper, hook, middleware, mixin, module, package, plugin, provider, repository, service, utility |
| 2 | Computing devices and their components | CPU, disk, GPU, keyboard, laptop, memory, monitor, mouse, printer, screen, server, smartphone, tablet, terminal |
| 3 | Development tools, environments, and support equipment | CLI, compiler, debugger, Docker, editor, IDE, Git, Jest, linter, loader, Prettier, terminal, test runner, TypeScript, webpack |
| 4 | Data structures, types, and formats | array, boolean, buffer, CSV, enum, hash map, integer, JSON, linked list, object, queue, stack, string, struct, tree, tuple, XML, YAML |
| 5 | Infrastructure, deployment, and platforms | AWS, CI/CD, container, deployment, Heroku, Kubernetes, load balancer, Node.js, pipeline, pod, production, staging, Vercel |
| 6 | Systems, subsystems, and architectural components | API gateway, authentication layer, caching layer, client, database layer, message broker, microservice, proxy, rate limiter, REST API, routing layer, server, WebSocket |
| 7 | Mathematical, algorithmic, and scientific terms | Big O notation, binary search, coefficient, complexity, exponent, hash function, iteration, logarithm, matrix, recursion, regex, sorting algorithm, time complexity, traversal |
| 8 | Interface elements and navigation | button, checkbox, dialog, dropdown, footer, header, menu, modal, navigation bar, radio button, scrollbar, sidebar, tab, text field, toggle, tooltip |
| 9 | Numbers, units of measurement, and time | byte, gigabyte (GB), hertz (Hz), hour (h), kilobyte (KB), megabyte (MB), millisecond (ms), minute, nanosecond (ns), second (s), terabyte (TB) |
| 10 | Quoted text | `Cannot read properties of undefined`, `ENOENT: no such file or directory`, `Submit` button, `404 Not Found`, `connection refused` |
| 11 | Professional roles, teams, and organizations | administrator, backend developer, contributor, DevOps engineer, frontend developer, Google, maintainer, Microsoft, product owner, QA engineer, reviewer, scrum master, user |
| 12 | Official documents, API references, and standards | API reference, changelog, code of conduct, contributing guide, diagram, figure, Getting Started guide, HTTP specification, note, paragraph, README, release notes, RFC, section, table, warning |
| 13 | Runtime environments and operational conditions | development, environment variable, garbage collection, heap, hot reload, live reload, memory leak, production, sandbox, stack trace, staging, test, thread, timeout, virtual machine |
| 14 | Colors | black, blue, cyan, gray, green, magenta, orange, red, white, yellow |
| 15 | Defects, errors, and fault terminology | assertion failure, bug, crash, deadlock, defect, exception, hang, infinite loop, memory leak, null pointer, race condition, regression, stack overflow, timeout, type error |
| 16 | Computer science, information, and communication technology | AI, algorithm, authentication, authorization, blockchain, containerization, cryptography, database, encoding, encryption, firewall, hashing, internet, machine learning, metadata, neural network, protocol, query, sandbox, schema, token, virtualization |
| 17 | Legal and licensing terms | Apache 2.0, BSD license, compliance, copyright, GPL, license, MIT license, open source, proprietary, terms of service, third-party, trademark, warranty |
| 18 | Database and storage terminology | connection pool, cursor, foreign key, index, migration, NoSQL, ORM, PostgreSQL, primary key, query, Redis, relation, row, schema, seed, SQL, SQLite, stored procedure, table, transaction, view |
| 19 | Network and protocol terminology | DNS, endpoint, HTTP, HTTPS, IP address, localhost, middleware, packet, port, request, response, route, socket, SSH, TCP, TLS, UDP, URL, VPN, WebSocket |

Colors are adjectives, but STE-Code identifies them as code-domain technical
nouns. Comparative and superlative color forms (blacker, the reddest) are not
permitted.

### Glossary registration (required)

Before you use a code-domain technical noun, add it to the project glossary
with: the noun term, its category or categories, its approved meaning in the
project context, and one correct example sentence.

### Grammar notes

- **Articles.** Use "the" for a specific instance, "a"/"an" for an indefinite
  instance, no article for plural general references.
- **Modifiers.** A technical noun can modify another technical noun
  ("Redis cache server"). Both nouns must belong to a recognized category.
- **Possessive.** Use `'s` only with category 11 (roles, teams, organizations).
  Write "the configuration of the Docker container", not
  "the Docker container's configuration".
- **Plurals.** Add a lowercase "s" with no apostrophe: `APIs`, not `API's`.
- **Capitalization.** Proper nouns keep their original form (`TypeScript`).
  Common technical nouns are lowercase unless they start the sentence.

### Edge cases

1. **Framework names that are also common words** (React, Vue, Swift, Go, Rust,
   Next, Nest) are technical nouns in category 3 or 5. Capitalize them, or use
   the full term ("the Swift language"), so they are not read as approved words.
2. **Code keywords** (`if`, `for`, `return`, `class`, `async`) are quoted text
   (category 10) when they appear in documentation. Status codes and literals
   must be quoted too: "return `500 Internal Server Error`".
3. **Abbreviations and acronyms** (API, JSON, SQL, HTTP, TLS) are technical
   nouns in categories 16, 18, or 19. Define each one at first use unless the
   audience universally understands it.
4. **Generated code and generated documentation** are exempt, because a machine
   produces them. Human-written comments inside generated files are not exempt.
5. **Project-specific internal names** (`PhoenixCache`) are technical nouns
   only when they are in the project glossary. Without registration they are
   non-approved words and violate P6.
6. **Numbers as technical nouns.** Version numbers, HTTP status codes, and port
   numbers are category 9 nouns or quoted text and must appear verbatim
   ("port 5432", "`404 Not Found`"), not "the default db port".

## P6 (Rule 1.6) — Non-approved words only as technical nouns

Use a word that is not approved only when it is a code-domain technical noun or
part of one.

- "handler" is not approved; the alternative is "function (n)".

> **Non-STE:** The handler processes each incoming event.
>
> **STE:** The function processes each incoming event.

But "handler" is permitted inside a compound technical noun (category 1):

> **STE:** The event handler processes each incoming event.

- "main" is not approved; the approved adjective is "primary".

> **Non-STE:** The main configuration has the latest values.
>
> **STE:** The primary configuration has the latest values.

## P7 (Rule 1.7) — Do not use technical nouns as verbs

Use a code-domain technical noun only as a noun, or as a modifier inside
another technical noun. Restructure the sentence with an approved verb.

> **Non-STE:** Database the user records before the migration.
>
> **STE:** Store the user records in the database before the migration.

Same pattern: "cache the result" → "keep the result in the cache";
"host the service" → "run the service" or "make the service available".

## P8 (Rule 1.8) — Use the technical nouns your project already approves

If your project, company, industry, or subject field has an approved name for a
class, module, function, method, variable, component, or process, use that
name. Do not invent a description for something that already has a name in the
codebase.

> **STE:** The dashboard page has a `UserTable` component and a `FilterPanel`
> component.

The reader must be able to find the exact element in the source tree from the
name you used.

## P9 (Rule 1.9) — Short, clear technical nouns

When you must select a code-domain technical noun, use one that is short (not
more than three words) and easy to understand. If a code snippet, line number,
diagram, or API reference already identifies the item, use the shortest
unambiguous term. Add one or two adjectives only when the reader needs them.

> **Non-STE:** Call the asynchronous JavaScript XML HTTP request wrapper utility
> function (line 42) to get the serialized JSON payload from the remote
> application programming interface endpoint.
>
> **STE:** Call the `fetchUtility` function (line 42) to get the JSON data from
> the API endpoint.

## P10 (Rule 1.10) — No regional words, slang, or jargon

Some technical words are used only inside one community or one technology
ecosystem. Readers from a different background, a different stack, or a
different first language cannot understand them. Select well-known words.

| Do not write | Write |
|---|---|
| cruft | unnecessary code |
| snag the repo | clone the repository |
| fire up / spin up | start |
| kick off | start |
| crunch the data | process the data |
| wonky, funky | not correct, known defect |
| hack | workaround |
| repo, K8s, TS (in prose) | repository, Kubernetes, TypeScript |
| thing, stuff | the exact technical noun |

> **Non-STE:** `"""Remove all the cruft from the legacy module."""`
>
> **STE:** `"""Remove all the unnecessary code from the legacy module."""`

## P11 (Rule 1.11) — One technical noun per item

Do not use different code-domain technical nouns for the same item. The source
of truth for the name is the code: the class, function, module, table,
resource, environment variable, or configuration key as the repository defines
it.

> **Non-STE:**
> 1. Initialize the UserService class to start the session manager.
> 2. Call the authenticate method on the AccountManager to check a user.
> 3. The UserHandler gives a session token that you send in later requests.

The repository defines one class, `UserService`. Use that name in all three
sentences. When the reader sees three names, the reader cannot know whether
there is one class or three.

## P12 (Rule 1.12) — The 4 code-domain technical verb categories

A code-domain technical verb names an operation or process in software
development. You may use a technical verb when you can put it in one of these
four categories. The examples are not a full list.

| # | Category | Sub-group | Examples |
|---|---|---|---|
| 1 | Development processes | Write and modify code | compile, concatenate, import, inject, instantiate, lint, minify, marshal, optimize, polyfill, refactor, resolve, shim, stub, substitute, tokenize, transpile, trace, vectorize |
| 1 | Development processes | Test and verify code | assert, benchmark, debug, fuzz, instrument, mock, profile, snapshot, spy, stub, unit-test |
| 1 | Development processes | Build and package | bundle, deploy, package, publish, release, tag, version |
| 1 | Development processes | Manage dependencies | hoist, install, link, lock, pin, update, upgrade |
| 2 | Computer processes and applications | Input and output | click, copy, cut, digitize, enter, paste, press, print, scan, swipe, tap, type |
| 2 | Computer processes and applications | User interface and application operations | clear, close, delete, deselect, disable, drag, drag and drop, enable, encrypt, erase, filter, hide, highlight, invalidate, maximize, minimize, navigate, open, save, scroll, select, show, sort, store, submit, toggle, validate, zoom in, zoom out |
| 2 | Computer processes and applications | System operations | abort, authenticate, authorize, boot, cache, communicate, configure, debug, deserialize, download, format, hydrate, initialize, install, load, log, manage, mount, process, reboot, render, retry, serialize, spawn, synchronize, throttle, update, upgrade, upload |
| 3 | Applicable subject fields | Algorithmic, mathematical, and data | aggregate, bisect, compute, concatenate, convert, count, decode, encode, escape, filter, hash, index, map, merge, normalize, parse, pipeline, precompute, recalculate, reduce, tokenize, transform, validate, verify |
| 3 | Applicable subject fields | Database and storage | backup, compact, flush, index, migrate, persist, query, replicate, restore, roll back, seed, shard, upsert, vacuum, write-ahead |
| 3 | Applicable subject fields | Network and communication | broadcast, connect, disconnect, establish, forward, handshake, intercept, listen, poll, proxy, reject, resolve, route, send, stream, timeout, tunnel, unsubscribe, webhook |
| 3 | Applicable subject fields | Security and authentication | authenticate, authorize, decrypt, decode, encode, encrypt, hash, revoke, salt, sanitize, sign, validate, verify |
| 4 | Legal and licensing terms | Legal and regulatory texts only | acknowledge, assign, comply with, conform to, disclose, enforce, explain, grant, inform, license, modify, notify, permit, regulate, sign, supersede, waive |

Constraints:

- If an approved verb gives the instruction or the information accurately, use
  the approved verb. Do not use a technical verb when approved words are enough.
- Use only technical verbs that are correct in your context. Do not use general
  or unclear technical verbs.
- Where possible, use an approved verb together with a code-domain technical
  noun instead of a technical verb.
- Technical verbs obey the same rules as other approved verbs (section 3).

## P13 (Rule 1.13) — Do not use technical verbs as nouns

Use a code-domain technical verb only as a verb. When you need a noun, use an
approved noun or a code-domain technical noun with the same meaning.

| Do not write | Write |
|---|---|
| Do a build of the project | Build the project |
| The function does a parse of the input string | The function parses the input string |
| Does a compile of the source files | Compiles the source files |
| `// A retry of the connection` | `// Retry the connection` |
| Addition of login endpoint | Add login endpoint |
| Compile of module 'auth' failed | Failed to compile module 'auth' |

Some words belong to a verb category (P12) and a noun category (P5) at the same
time. When the API returns a named artifact (a `Build` object, a `Deployment`
resource), the noun form is a technical noun, not a misused verb.

## P14 (Rule 1.14) — American English spelling

Use the spelling given in the controlled terminology (American English). Use a
different spelling only when a project specification, style guide, contract, or
other official directive requires it.

| Do not write | Write |
|---|---|
| colour | color |
| fibre | fiber |
| initialise | initialize |
| serialise | serialize |
| behaviour | behavior |
| centre | center |

Do not change the spelling inside quoted text. If an error message, a comment,
or a user interface shows British English spelling, keep it verbatim:

> **STE:** The terminal shows the message `Colour profile not recognised`.

## Application by documentation type

| Document type | What P1–P14 constrain most |
|---|---|
| README | Imperative verbs in setup steps; adjectives and adverbs in the overview. Tool, file, and command names are technical nouns. |
| API reference | Prose around parameters, return values, and error conditions. Function, type, and endpoint names are technical nouns (P5). |
| Docstrings and inline comments | The shortest approved verb. `NOTE:`, `WARNING:` are approved nouns; `FIXME:` is a technical noun. |
| Commit messages | The smallest approved vocabulary, imperative form: add, fix, remove, update, set, make, check, run. |
| Error messages | Approved words only, so non-native readers understand. "cannot", not "unable to"; "not correct", not "invalid". |
| Test specifications | Name the component under test and the condition with technical nouns from categories 1, 4, and 15. |
| Code review and PR feedback | Approved verbs in every request for change; one technical noun per item (P11); no jargon (P10). |

## Template — code review comment

```markdown
**File:** `<path>:<line>`
**Type:** defect | question | suggestion
**Principle:** P<n> (Rule 1.<n>)

**What I see:** <one sentence, approved verb, present tense>

**Why it is a problem:** <one or two sentences; name the defect with a
category 15 technical noun where one applies>

**What to do:** <imperative sentence that starts with an approved verb:
add, remove, change, set, make, check, move, rename, split>
```

Filled example:

```markdown
**File:** `src/auth/UserService.ts:42`
**Type:** defect
**Principle:** P11 (Rule 1.11)

**What I see:** The docstring calls this class `AccountManager`. The file
defines the class `UserService`.

**Why it is a problem:** Two names for one class. The reader cannot know
whether there is one class or two.

**What to do:** Change the docstring to use `UserService` in all sentences.
```

Rules for review comments:

- Start each request for change with an approved imperative verb.
- Use one sentence for one point. Do not join two points with "and".
- Name the file and the line. Do not write "this thing" or "the stuff above".
- Do not use slang ("nit", "wonky", "hacky", "LGTM") in the body of the
  comment. Write "small point", "not correct", "workaround", "I approve".
- Do not use a technical noun as a verb (P7) or a technical verb as a noun
  (P13) in your own feedback.

## Template — pull request description

```markdown
# <Imperative summary line, one approved verb first, 72 characters or less>

## What this change does

<One paragraph. Each sentence has one clause. Use approved verbs and
code-domain technical nouns. Name every component with the name the
repository uses.>

## Why

<The defect, the request, or the requirement. Name the defect with a
category 15 technical noun: race condition, memory leak, regression,
timeout, type error.>

## How to check it

1. <Imperative step, approved verb first.>
2. <Imperative step, approved verb first.>
3. <The result the reviewer must see.>

## Risk

<What can break. Name the affected component and environment
(development, staging, production).>

## Related

- Issue: #<n>
- Documents changed: <README | API reference | changelog | none>
```

Filled example:

```markdown
# Fix the timeout defect in the connection pool

## What this change does

The `ConnectionPool` class now closes each idle connection after 30 seconds.
The class writes one line in the log for each connection that it closes.

## Why

The pool kept idle connections open. The database refused new connections
after 100 idle connections. This caused a crash in production.

## How to check it

1. Start the service in the development environment.
2. Send 120 requests to the `/orders` endpoint.
3. Check the log. The log must show `closed idle connection` for each
   connection that the pool closes.

## Risk

A short timeout can close a connection that a slow query still uses. Set
`POOL_IDLE_TIMEOUT` to a larger value if the staging tests show this defect.

## Related

- Issue: #482
- Documents changed: changelog
```

## Template — PR review summary

```markdown
**Decision:** approve | request changes | comment

**Summary:** <One sentence. What the change does, in approved words.>

**Blocking points**
1. `<path>:<line>` — <imperative sentence>
2. `<path>:<line>` — <imperative sentence>

**Non-blocking points**
1. `<path>:<line>` — <imperative sentence>

**Checked:** <what you ran or read: tests, linter, documentation>
```

## Level 1 compliance checklist

Run this list on every document before you publish it.

1. Each word is an approved word, a code-domain technical noun, or a
   code-domain technical verb. (P1)
2. Each approved word is used as its specified part of speech. (P2)
3. Each approved word carries only its approved meaning. (P3)
4. Each verb and adjective uses an approved form. (P4)
5. Each non-approved word fits one of the 19 noun categories, or is part of a
   compound that does. (P5, P6)
6. No technical noun is used as a verb. (P7)
7. Each component uses the name the project glossary and the repository give
   it. (P8)
8. Each technical noun is short (three words or less) and clear. (P9)
9. No regional word, slang word, or jargon word appears. (P10)
10. One item has exactly one name in the whole document. (P11)
11. Each technical verb fits one of the four verb categories, and no approved
    verb could do the same work. (P12)
12. No technical verb is used as a noun. (P13)
13. All spelling is American English, except inside quoted text. (P14)
14. Every technical noun and technical verb you introduced is registered in the
    project glossary.


