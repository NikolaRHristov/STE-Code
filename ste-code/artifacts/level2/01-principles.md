# Level 2 — Core Principles (Section 1: Words)

Section 1 of STE-Code holds the fourteen word-level rules. Every word in code
documentation must pass one of three gates:

1. It is approved in the STE-Code controlled terminology.
2. It is a code-domain technical noun (Rule 1.5).
3. It is a code-domain technical verb (Rule 1.12).

There is no fourth category. Rule 1.6 forbids everything else.

| Rule | Statement |
|------|-----------|
| 1.1 | Use words that are approved in the controlled terminology, code-domain technical nouns, or code-domain technical verbs. |
| 1.2 | Use approved words only as the specified part of speech. |
| 1.3 | Use approved words only with their approved meanings. |
| 1.4 | Use only the approved forms of verbs and adjectives. |
| 1.5 | You can use words that you can include in a code-domain technical noun category. |
| 1.6 | Use a non-approved word only when it is a code-domain technical noun or part of one. |
| 1.7 | Do not use code-domain technical nouns as verbs. |
| 1.8 | Use code-domain technical nouns that are approved in your project, company, industry, or subject field. |
| 1.9 | When you must select a code-domain technical noun, use one which is short and easy to understand. |
| 1.10 | Do not use regional, slang, or jargon words as code-domain technical nouns. |
| 1.11 | Do not use different code-domain technical nouns for the same item. |
| 1.12 | You can use verbs that you can include in a code-domain technical verb category. |
| 1.13 | Do not use code-domain technical verbs as nouns. |
| 1.14 | Use American English spelling unless other official directives tell you differently. |

---

## Rule 1.1 — Use approved words, technical nouns, or technical verbs

In code documentation, use words that are approved in the project controlled
terminology, code-domain technical nouns, or code-domain technical verbs.

- A code-domain technical noun names a concept in software development
  (`UserAuthenticator`, connection pool, race condition).
- A code-domain technical verb names an operation or process in software
  development (serialize, compile, deploy).
- The controlled terminology also lists non-approved words with approved
  alternatives. Register project terms in the project glossary.

Common replacements:

| Do not write | Write |
|--------------|-------|
| execute, invoke (prose) | run, call |
| generate, construct | make |
| configure | set |
| retrieve, fetch | get |
| transmit | send |
| delete, purge | remove |
| validate, verify, ensure | check |
| utilize, leverage | use |
| initiate, bootstrap, commence | start |
| terminate | stop |
| unable to | cannot |
| invalid, malformed | not correct |
| prior to | before |
| at this time | now |
| persists | continues |

Examples:

> **Non-STE:** Execute the script to do the task.
>
> **STE:** Run the script to do the task.

> **Non-STE:** To begin utilizing the build toolchain, you must first generate the distributable artifact, then execute the compiled binary to bootstrap the local development service.
>
> **STE:** Use the build tool to make the binary. Run the binary to start the local service.

> **Non-STE:** `Error: Unable to establish connection to the database. Please verify your credentials and retry.`
>
> **STE:** `Error: Cannot connect to the database. Check your credentials and try again.`

Application by documentation type:

- **README** — approved imperative verbs in setup steps; approved adjectives in
  overview prose ("large" not "substantial", "usual" not "conventional").
- **API reference** — names stay as technical nouns; the prose around them uses
  approved words ("gives" not "resolves", "gives an error" not "rejects").
- **Docstrings and comments** — shortest approved word: "do" not "perform",
  "check" not "ensure", "make" not "construct".
- **Commit messages** — approved imperative verbs only: add, fix, remove,
  update, set, make, check, run. Not "implement" (use "add"), not "optimize"
  (use "make faster").
- **Error messages** — approved words only, no jargon or abbreviations that are
  not technical nouns.

---

## Rule 1.2 — Use approved words only as the specified part of speech

Each approved word has a specified part of speech in the controlled
terminology. Use the word only in that role.

- "Query" is an approved noun, not an approved verb.
- "Static" is an approved adjective, not an approved verb.
- Some words are approved in more than one role. "Call" is an approved verb
  (to call a function) and an approved noun (a function call). Position in the
  sentence shows which role applies.

When a word is not in the controlled terminology: find it in a standard
English dictionary, find the closest approved synonym, then use the approved
word or a different sentence construction. A replacement must not change the
meaning.

| Violating form | Error | Write |
|----------------|-------|-------|
| Query the database / Cache the result / Queue the job / Log the error / Index the record | Technical noun used as verb | Send a query / Keep the result in the cache / Put the job in the queue / Write the error in the log / Use the index to find the record |
| Docker the app / Git the change / Kubectl the pod / Terraform the VPC | Tool name used as verb | Use Docker / Save with Git / Use `kubectl` / Use Terraform |
| Secure the endpoint / Empty the buffer / Silent the log | Adjective used as verb | Make the endpoint secure / Make the buffer empty / Make the log silent |
| Static the variable / Ready the worker / Live the connection | Adjective used as verb | Make the variable static / Make the worker ready / Make the connection live |
| Utilize the cache / Leverage the library / Employ the service | Unapproved verb | Use the cache / Use the library / Use the service |
| Commence the build / Initiate the transfer / Terminate the process | Unapproved verb | Start the build / Start the transfer / Stop the process |
| Orchestrate the services / Facilitate the sync | Unapproved verb | Control the services / Help the sync |

"Clear" is approved as both a verb and an adjective, so "Clear the flag" is
permitted. The make + adjective pattern applies to true adjectives such as
"secure" and "empty".

---

## Rule 1.3 — Use approved words only with their approved meanings

Each approved word has a specified meaning that is often narrower than its
standard English meaning. Do not use the word with any other meaning.

- The approved meaning of "follow" is "come after, go after".
- The approved meaning of "obey" is "to do that which the procedures or
  instructions tell you".

Check procedure (run every content word through it):

1. Identify the part of speech as you wrote it.
2. Look up the approved meaning for that part of speech in the dictionary.
3. Ask whether your sentence uses exactly that meaning. If not, the word fails
   even though it is approved and the sentence reads well.
4. Replace the word, or rewrite the sentence so the word carries its approved
   meaning.

Worked check:

> **Sentence:** The background worker runs every night.
> **Step 1:** "runs" is a verb.
> **Step 2:** Approved meaning of the verb "run" = "execute a program or command".
> **Step 3:** The writer means "operates on a schedule". No match.
> **Step 4:** "The background worker operates every night."

---

## Rule 1.4 — Use only the approved forms of verbs and adjectives

The controlled terminology gives each approved verb with its approved forms,
and each approved adjective in base form with its comparative and superlative
forms where applicable.

| Infinitive/Imperative | Simple present | Simple past | Past participle (as adjective) |
|-----------------------|----------------|-------------|--------------------------------|
| (To) Compile / Compile | Compile(s) | Compiled | Compiled |

Adjective: FAST (adj) (FASTER, FASTEST). Base "fast", comparative "faster",
superlative "fastest". Adjectives that form comparatives with "more" and "most"
have no listed forms, because "more" and "most" are approved words.

Do not invent forms.

> **Non-STE:** The compiler is compilating the source files every time you save the document, and it compilates them even when no change occurs in the code.
>
> **STE:** The compiler compiles the source files each time you save the document, and it compiles them even when no change occurs in the code.

---

## Rule 1.5 — Code-domain technical noun categories

You can use a word that is not in the controlled terminology when you can put
it in one or more of these nineteen categories. Register each such noun in the
project glossary with its category, its approved meaning in the project, and an
example sentence.

| # | Category | Examples |
|---|----------|----------|
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
nouns. Comparative and superlative forms of colors (blacker, the reddest) are
not permitted. The listed nouns are examples only, not a full list.

### Grammar notes for technical nouns

- **Articles.** Use "the" for a specific instance, "a" or "an" for an
  indefinite instance, and no article for a plural general reference:
  "Kubernetes pods run in a namespace."
- **Modifiers.** A technical noun can modify another technical noun. Both parts
  must belong to a recognized category: "The Redis cache server stores the
  session data."
- **Possessive form.** Permitted only for category 11 (roles, teams,
  organizations). Write "The user's session data" but "The configuration of the
  Docker container", not "The Docker container's configuration".
- **Plurals.** Standard English rules. Acronyms add a lowercase "s" without an
  apostrophe: "two APIs and three SQL queries", not "two API's".
- **Capitalization.** Proper nouns keep their original capitalization
  (TypeScript, PostgreSQL). Common technical nouns are lowercase unless they
  start a sentence (controller, endpoint, middleware).

### Edge cases

- **Framework names that are common words** (React, Vue, Swift, Go, Rust, Elm,
  Next, Nest) are technical nouns in category 3 or 5. Capitalize them or use
  the full term ("the Swift language", "the Go compiler") to remove ambiguity.
- **Code keywords** (`if`, `else`, `for`, `return`, `class`, `async`) are
  quoted text (category 10) in documentation. Write "The `if` statement checks
  the condition." Return `500 Internal Server Error`, not a bare 500.
- **Abbreviations and acronyms** (API, JSON, SQL, HTTP, TLS) are permitted in
  categories 16, 18, or 19. Define each one at first use unless the audience
  universally understands it.
- **Generated code and generated documentation** are exempt, because a machine
  produced them. Human-written comments inside generated files are not exempt.
- **Project-specific internal names** (`PhoenixCache`) are technical nouns only
  after glossary registration. Without registration they are non-approved words
  and violate Rule 1.6.
- **Numbers as technical nouns.** Version numbers, status codes, and port
  numbers are category 9 nouns or quoted text and must appear verbatim: "runs
  on port 5432 and returns `404 Not Found`".

---

## Rule 1.6 — Non-approved words only as technical nouns

A word that the controlled terminology does not approve is permitted only when
it is a code-domain technical noun or part of one.

> **Non-STE:** The handler processes each incoming event.
>
> **STE:** The function processes each incoming event.
>
> **STE:** The event handler processes each incoming event.

"Event handler" is a code-domain technical noun (category 1), so "handler" is
permitted inside it.

> **Non-STE:** The main configuration has the latest values.
>
> **STE:** The primary configuration has the latest values.
>
> **STE:** Merge the feature branch into the main branch.

"Main branch" is the approved Git technical noun (category 5). Do not replace
"main" with "primary" there, because "primary branch" is not the approved term.

---

## Rule 1.7 — Do not use technical nouns as verbs

Use a code-domain technical noun only as a noun, or as a modifier inside
another technical noun. Restructure the sentence so the word keeps its noun
role.

> **Non-STE:** Database the user records before the migration.
>
> **STE:** Store the user records in the database before the migration.

> **Non-STE:** Cache the API responses to improve performance.
>
> **STE:** Store the API responses in the cache to improve performance.

---

## Rule 1.8 — Use technical nouns approved in your project or field

If your project, company, industry, or subject field has an approved name for a
class, module, function, method, variable, component, or process, use that
name. Do not invent a new name for an item that already has one. The source of
truth is the codebase.

> **STE:** The dashboard page has a `UserTable` component and a `FilterPanel` component.

> **Non-STE:** The account controller manages login and user profile operations.
>
> **STE:** The `AccountController` manages authentication and user profile operations.

---

## Rule 1.9 — Select short technical nouns

When your project has no approved technical noun, select one that is short (not
more than three words) and easy to understand. Do not use a long descriptive
phrase when the context — a code snippet, a line number, a diagram, or an API
reference — already identifies the item. Add one or two adjectives only when
clarification is necessary.

> **Non-STE:** Call the asynchronous JavaScript XML HTTP request wrapper utility function (line 42) to get the serialized JSON payload from the remote application programming interface endpoint.
>
> **STE:** Call the `fetchUtility` function (line 42) to get the JSON data from the API endpoint.

---

## Rule 1.10 — No regional, slang, or jargon words

Some technical words are used only inside a confined community or a single
language ecosystem. Readers from other backgrounds, junior developers, and
non-native English speakers cannot understand them. Select well-known words.

> **Non-STE:** `"""Remove all the cruft from the legacy module."""`
>
> **STE:** `"""Remove all the unnecessary code from the legacy module."""`

Other examples: "snag the repo" → "clone the repository"; "fire up the dev
server" → "start the development server"; "K8s spins up pods" → "Kubernetes
starts pods"; "a funky TS bug" → "a known TypeScript defect".

---

## Rule 1.11 — One technical noun per item

Do not use different technical nouns for the same item in different parts of a
document. A changed name forces the reader to decide whether you refer to one
item or to several.

> **Non-STE:**
> 1. Initialize the UserService class to start the session manager.
> 2. Call the authenticate method on the AccountManager to verify a user.
> 3. The UserHandler returns a session token that you send in later requests.
>
> **STE:** Use `UserService` in all three sentences, because the repository
> defines one class with that name.

---

## Rule 1.12 — Code-domain technical verb categories

A code-domain technical verb names an operation or process in software
development. You can use a verb that is not in the controlled terminology when
you can put it in one of these four categories.

| # | Category | Examples |
|---|----------|----------|
| 1a | Development processes — write and modify code | compile, concatenate, import, inject, instantiate, lint, minify, marshal, optimize, polyfill, refactor, resolve, shim, stub, substitute, tokenize, transpile, trace, vectorize |
| 1b | Development processes — test and verify code | assert, benchmark, debug, fuzz, instrument, mock, profile, snapshot, spy, stub, unit-test |
| 1c | Development processes — build and package | bundle, deploy, package, publish, release, tag, version |
| 1d | Development processes — manage dependencies | hoist, install, link, lock, pin, update, upgrade |
| 2a | Computer processes — input and output | click, copy, cut, digitize, enter, paste, press, print, scan, swipe, tap, type |
| 2b | Computer processes — user interface and application operations | clear, close, delete, deselect, disable, drag, drag and drop, enable, encrypt, erase, filter, hide, highlight, invalidate, maximize, minimize, navigate, open, save, scroll, select, show, sort, store, submit, toggle, validate, zoom in, zoom out |
| 2c | Computer processes — system operations | abort, authenticate, authorize, boot, cache, communicate, configure, debug, deserialize, download, format, hydrate, initialize, install, load, log, manage, mount, process, reboot, render, retry, serialize, spawn, synchronize, throttle, update, upgrade, upload |
| 3a | Subject fields — algorithmic, mathematical, and data | aggregate, bisect, compute, concatenate, convert, count, decode, encode, escape, filter, hash, index, map, merge, normalize, parse, pipeline, precompute, recalculate, reduce, tokenize, transform, validate, verify |
| 3b | Subject fields — database and storage | backup, compact, flush, index, migrate, persist, query, replicate, restore, roll back, seed, shard, upsert, vacuum, write-ahead |
| 3c | Subject fields — network and communication | broadcast, connect, disconnect, establish, forward, handshake, intercept, listen, poll, proxy, reject, resolve, route, send, stream, timeout, tunnel, unsubscribe, webhook |
| 3d | Subject fields — security and authentication | authenticate, authorize, decrypt, decode, encode, encrypt, hash, revoke, salt, sanitize, sign, validate, verify |
| 4 | Legal and licensing texts | acknowledge, assign, comply with, conform to, disclose, enforce, explain, grant, inform, license, modify, notify, permit, regulate, sign, supersede, waive |

Code-domain technical verbs obey the same rules as approved verbs. The lists
are examples only.

Priority: if an approved verb gives the instruction or the information
accurately, use the approved verb. Use a technical verb only when no approved
verb is sufficient, and only when the technical verb is exact in your context.
Where possible, write the sentence with an approved verb plus a code-domain
technical noun.

> **Non-STE:** If you detect broken wires, repair them.
>
> **STE:** If you find broken wires, repair them.

---

## Rule 1.13 — Do not use technical verbs as nouns

Use a code-domain technical verb only as a verb. When you need a noun, use an
approved noun or a code-domain technical noun with the same meaning. A word can
belong to both systems when it fits a verb category (Rule 1.12) and a noun
category (Rule 1.5).

| Do not write | Write |
|--------------|-------|
| Do a build of the project | Build the project |
| The function does a parse of the input string | The function parses the input string |
| Does a compile of the source files | Compiles the source files |
| `// A retry of the connection` | `// Retry the connection` |
| Addition of login endpoint | Add login endpoint |
| Compile of module 'auth' failed | Failed to compile module 'auth' |
| Start of deploy for release v2.1.0 | Deploy started for release v2.1.0 |

When an API returns a named artifact (a `Build` object, a `Deployment`
resource), the noun form is a technical noun under Rule 1.5, not a misused
verb.

---

## Rule 1.14 — Use American English spelling

Use the spelling given in the STE-Code controlled terminology, which is
American English. Use a different spelling only when a project specification,
style guide, contract, or other official directive says so.

Do not change the spelling of quoted text — an error message, a code comment,
or a user interface label — even when it uses British English. See Rule 8.6.

> **Non-STE:** The log file shows the colour of each output line.
>
> **STE:** The log file shows the color of each output line.

> **Non-STE:** Initialise the variable before you use it in the loop.
>
> **STE:** Initialize the variable before you use it in the loop.
