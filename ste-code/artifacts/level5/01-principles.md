# Level 5 — Core Principles (Words: Rules 1.1–1.14)

Level 5 is the full STE-Code standard: every rule, the extension vocabulary, the
reference catalogue, and provenance. This sub-document is the **core principles**
slice — Section 1, which governs *words*. Every other section of STE-Code assumes
these fourteen rules already hold.

Use this file when you generate, review, or lint code documentation with an LLM.

## The three gates

A word is allowed in STE-Code prose only if it passes one of three gates:

1. The word is **approved in the controlled terminology** (STE-Code part 2), or
2. The word is a **code-domain technical noun** (Rule 1.5, 19 categories), or
3. The word is a **code-domain technical verb** (Rule 1.12, 4 categories).

A word that passes no gate must be replaced, or the sentence must be restructured
so that approved words carry the meaning.

## Definitions

- **Controlled terminology** — the STE-Code approved word list. Each entry gives
  one part of speech and one approved meaning, plus the approved verb and
  adjective forms.
- **Code-domain technical noun** — a noun term for a specified concept in
  software development, applicable to a subject field (Rule 1.5).
- **Code-domain technical verb** — a verb term for a specified operation or
  process in software development (Rule 1.12).
- **Project glossary** — the project, company, industry, or subject-field list of
  approved technical nouns and verbs. It is checked before the controlled
  terminology for domain names, and the repository is its source of truth.

## Rule index

| Rule | Statement |
|------|-----------|
| 1.1 | Use words that are approved, code-domain technical nouns, or code-domain technical verbs. |
| 1.2 | Use approved words only as the specified part of speech. |
| 1.3 | Use approved words only with their approved meanings. |
| 1.4 | Use only the approved forms of verbs and adjectives. |
| 1.5 | You can use words you can include in a code-domain technical noun category. |
| 1.6 | Use an unapproved word only when it is a code-domain technical noun or part of one. |
| 1.7 | Do not use code-domain technical nouns as verbs. |
| 1.8 | Use code-domain technical nouns approved in your project, company, industry, or subject field. |
| 1.9 | When you must select a code-domain technical noun, use one that is short and easy to understand. |
| 1.10 | Do not use regional, slang, or jargon words as code-domain technical nouns. |
| 1.11 | Do not use different code-domain technical nouns for the same item. |
| 1.12 | You can use verbs you can include in a code-domain technical verb category. |
| 1.13 | Do not use code-domain technical verbs as nouns. |
| 1.14 | Use American English spelling unless other official directives tell you differently. |

---

## Rule 1.1 — Use approved words, code-domain technical nouns, or code-domain technical verbs

In code documentation, use words that are:

- approved in the controlled terminology,
- code-domain technical nouns, or
- code-domain technical verbs.

The controlled terminology gives the words most frequently used in code
documentation. It also lists words that are **not** approved, with approved
alternatives. Your project glossary or terminology database holds the technical
nouns and technical verbs of your subject field; always check it first.

Worked vocabulary swaps:

| Do not write | Write | Why |
|---|---|---|
| execute the script | run the script | "run" is the approved verb for executing programs |
| generate the artifact | make the artifact | "make" is approved; "generate" is not |
| utilize / leverage the cache | use the cache | inflated verb |
| bootstrap / initiate the service | start the service | "start" is approved |
| configure the runtime | set the runtime behavior | "set" is approved |
| retrieve / fetch the record | get the record | "get" is approved |
| transmit the payload | send the data | "send" is approved |
| validate / verify the input | check the input | "check" is approved |
| unable to connect | cannot connect | "cannot" is approved |
| invalid / malformed data | incorrect data | "correct" is the approved adjective |

Technical terms stay: `UserAuthenticator` is a code-domain technical noun,
`serialize` is a code-domain technical verb, and both are permitted although
neither is in the controlled terminology.

Examples by documentation type:

> **Non-STE (README):** To begin utilizing the build toolchain, you must first
> generate the distributable artifact, then execute the compiled binary to
> bootstrap the local development service.
>
> **STE:** Use the build tool to make the binary. Run the binary to start the
> local service.

> **Non-STE (JSDoc):** Fetches a user record. The duration in milliseconds the
> client shall await a response prior to terminating the connection attempt.
>
> **STE:** Gets a user record. The time in milliseconds that the client waits
> for a response before it stops the connection.

> **Non-STE (CLI error):** Unable to establish connection to the database.
> Please verify your credentials and retry.
>
> **STE:** Cannot connect to the database. Check your credentials and try again.

Paradigm notes:

- **Object-oriented** — prose uses approved verbs (make, get, set, call, send,
  keep). Class, method, and pattern names stay as technical nouns.
- **Functional** — `map`, `fold`, `reduce`, `filter`, `compose`, and `curry` are
  code-domain technical verbs. "Pure function" is a compound technical noun.
- **Procedural** — each step starts with an approved imperative verb. "Allocate"
  is not approved (write "make a buffer"). "Free" and "dereference" are
  code-domain technical verbs.
- **Declarative** — SQL keywords and resource kind names are technical terms.
  "Provision" is not approved (use "make" or "set up"); "orchestrate" is not
  approved (use "control" or "manage").
- **Systems** — "own", "borrow", and "move" are Rust technical verbs. "Dangling
  pointer" and "undefined behavior" are compound technical nouns (category 15).

---

## Rule 1.2 — Use approved words only as the specified part of speech

Each entry in the controlled terminology carries one label: verb (v), noun (n),
adjective (adj), adverb (adv), preposition (prep), conjunction (conj), pronoun
(pron), or article (art). Use the word only in that grammatical role.

- "Query" is an approved **noun**, not a verb. Write "Send a query to the
  database", not "Query the database".
- "Static" is an approved **adjective**, not a verb. Write "Make the variable
  static", not "Static the variable".
- Some words carry more than one label. "Call" is an approved verb and an
  approved noun; the position in the sentence shows the function.

If the word you want is not in the controlled terminology:

1. Find the word in a standard English dictionary.
2. Find the best synonym that is approved in the STE-Code controlled terminology.
3. Use that approved word, or write a different sentence construction.

When you replace a word, make sure that the meaning does not change.

| Violating form | Part-of-speech error | Approved replacement |
|---|---|---|
| Query the database / Cache the result / Queue the job / Log the error | technical noun used as verb | Send a query / Keep the result in the cache / Put the job in the queue / Write the error in the log |
| Docker the app / Git the change / Kubectl the pod | tool name used as verb | Use Docker / Save with Git / Use `kubectl` |
| Secure the endpoint / Empty the buffer / Silent the log | adjective used as verb | Make the endpoint secure / Make the buffer empty / Make the log silent |
| Static the variable / Ready the worker / Live the connection | adjective used as verb | Make the variable static / Make the worker ready / Make the connection live |
| Utilize / Leverage / Employ the service | inflated verb | Use the service |
| Commence the build / Initiate the transfer / Terminate the process | inflated verb | Start the build / Start the transfer / Stop the process |
| Orchestrate the services / Facilitate the sync | unapproved verb | Control the services / Help the sync |

> **Non-STE:** Docker the app and deploy to production. If it fails, rollback.
>
> **STE:** Use Docker to make a container for the application. Deploy the
> container to production. If the deployment fails, roll back to the previous
> version.

---

## Rule 1.3 — Use approved words only with their approved meanings

Each approved word has one specified meaning, often narrower than the standard
English meaning. Do not use an approved word with any other meaning.

- The approved meaning of the verb **follow** is "come after, go after". Use it
  only for sequence: "Do the steps that follow."
- The approved meaning of the verb **obey** is "to do that which the procedures
  or instructions tell you". Use it for compliance: "Obey the instructions."

Four-step check for every approved word you write:

1. **Identify the part of speech** as you used it in the sentence.
2. **Look up the approved meaning** for that part of speech in the controlled
   terminology.
3. **Ask: does my sentence use exactly that meaning?** If not, the word fails —
   even when the word is approved and the sentence reads well.
4. **Replace or restructure** so the approved word carries its approved meaning.

Worked check:

> **Sentence:** The background worker runs every night.
> **Step 1:** "runs" is a verb.
> **Step 2:** Approved meaning of "run" = "execute a program or command".
> **Step 3:** The writer means "operates on a schedule". The meaning does not match.
> **Step 4:** Rewrite: "The background worker operates every night."

---

## Rule 1.4 — Use only the approved forms of verbs and adjectives

The controlled terminology gives each approved verb with its approved forms, and
each approved adjective in the base form with the comparative and superlative
forms where applicable.

Verb entry: `COMPILE (v), COMPILES, COMPILED, COMPILED`

| Infinitive / imperative | Simple present | Simple past | Past participle (as adjective) |
|---|---|---|---|
| (To) Compile / Compile | Compile(s) | Compiled | Compiled |

Forms that are not listed are not permitted: "compilating" and "compilates" are
both incorrect.

Adjective entry: `FAST (adj) (FASTER, FASTEST)` — base form *fast*, comparative
*faster*, superlative *fastest*. Adjectives that make their comparative and
superlative with "more" and "most" have no extra forms in the terminology,
because "more" and "most" are approved words.

Do not use the "-ing" form as a main verb in procedural writing unless the
controlled terminology lists it.

> **Non-STE:** The compiler is compilating the source files every time you save
> the document.
>
> **STE:** The compiler compiles the source files each time you save the document.

> **Non-STE:** This algorithm is more fast than the previous one.
>
> **STE:** This algorithm is faster than the previous one.

> **Non-STE:** After installing the dependencies, you can start compiling the
> project by running the build script.
>
> **STE:** After you install the dependencies, compile the project with the build
> script.

---

## Rule 1.5 — Code-domain technical noun categories

A code-domain technical noun is a noun term for a specified concept in software
development, applicable to a subject field. The controlled terminology cannot
list them all, because each project uses different ones; keep yours in the
project glossary or terminology database.

STE-Code gives the categories to help you select the technical nouns for your
project glossary and to use them correctly. You may use a code-domain technical
noun in procedural and descriptive writing when you can put it in one or more of
these **nineteen** categories. The words shown are examples only, not a complete
list.

| # | Category | Example terms |
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
| 10 | Quoted text (text you cannot change: error messages, code snippets, UI labels, log output) | `Cannot read properties of undefined`, `ENOENT: no such file or directory`, `Submit` button, `404 Not Found`, `connection refused` |
| 11 | Professional roles, teams, and organizations | administrator, backend developer, contributor, DevOps engineer, frontend developer, Google, maintainer, Microsoft, product owner, QA engineer, reviewer, scrum master, user |
| 12 | Official documents, API references, and standards | API reference, changelog, code of conduct, contributing guide, diagram, figure, Getting Started guide, HTTP specification, note, paragraph, README, release notes, RFC, section, table, warning |
| 13 | Runtime environments and operational conditions | development, environment variable, garbage collection, heap, hot reload, live reload, memory leak, production, sandbox, stack trace, staging, test, thread, timeout, virtual machine |
| 14 | Colors | black, blue, cyan, gray, green, magenta, orange, red, white, yellow |
| 15 | Defects, errors, and fault terminology | assertion failure, bug, crash, deadlock, defect, exception, hang, infinite loop, memory leak, null pointer, race condition, regression, stack overflow, timeout, type error |
| 16 | Computer science, information, and communication technology | AI, algorithm, authentication, authorization, blockchain, containerization, cryptography, database, encoding, encryption, firewall, hashing, internet, machine learning, metadata, neural network, protocol, query, sandbox, schema, token, virtualization |
| 17 | Legal and licensing terms | Apache 2.0, BSD license, compliance, copyright, GPL, license, MIT license, open source, proprietary, terms of service, third-party, trademark, warranty |
| 18 | Database and storage terminology | connection pool, cursor, foreign key, index, migration, NoSQL, ORM, PostgreSQL, primary key, query, Redis, relation, row, schema, seed, SQL, SQLite, stored procedure, table, transaction, view |
| 19 | Network and protocol terminology | DNS, endpoint, HTTP, HTTPS, IP address, localhost, middleware, packet, port, request, response, route, socket, SSH, TCP, TLS, UDP, URL, VPN, WebSocket |

Note on category 14: colors are adjectives, but STE-Code identifies them as
code-domain technical nouns. Comparative and superlative forms of colors (for
example "blacker", "the reddest") are not permitted.

---

## Rule 1.6 — Unapproved words are permitted only inside technical nouns

A word that the controlled terminology marks as not approved fails when you use
it as a general noun or adjective, and passes when it is part of a recognized
code-domain technical noun.

**"Handler"** — not approved; the alternative is "function (n)".

> **Non-STE:** The handler processes each incoming event.
>
> **STE:** The function processes each incoming event.
>
> **STE:** The event handler processes each incoming event. ("Event handler" is a
> code-domain technical noun, category 1.)

**"Main"** — not approved as a general adjective; the alternative is
"primary (adj)".

> **Non-STE:** The main configuration has the latest values.
>
> **STE:** The primary configuration has the latest values.
>
> **STE:** Merge the feature branch into the main branch. ("Main branch" is a
> code-domain technical noun, category 5. Do not write "primary branch".)

**"Base"** — not approved for a surface location; the alternative is "bottom
(n)". "Base" stays inside the technical nouns "base case" (category 7) and "base
class" (category 1).

> **Non-STE:** Copy the files to the base of the build folder.
>
> **STE:** Copy the files to the bottom of the build folder.

---

## Rule 1.7 — Do not use code-domain technical nouns as verbs

Use a code-domain technical noun only as a noun, or as an adjective inside a
different technical noun. Restructure the sentence with an approved verb.

> **Non-STE:** Database the user records before the migration.
>
> **STE:** Store the user records in the database before the migration.

> **Non-STE:** Cache the API responses to improve performance.
>
> **STE:** Store the API responses in the cache to improve performance.

A word can be a technical noun **and** a technical verb when it fits a category
in Rule 1.5 and a category in Rule 1.12. Your project glossary decides:

> **STE (noun):** Write a log entry for each failed request.
>
> **STE (verb):** Log each failed request.

> **See also:** Rule 1.5, Rule 1.12, Rule 1.13.

---

## Rule 1.8 — Use the technical nouns approved in your project or field

If your project, company, industry, or subject field already has an approved
name for a class, module, function, method, variable, component, or process, use
that name. These names live in your project glossary, API documentation, coding
standards, or company documentation. Do not invent your own names for items that
already have established names. The source of truth is the repository.

> **STE:** The dashboard page has a `UserTable` component and a `FilterPanel`
> component.

> **Non-STE:** The account controller manages login and user profile operations.
>
> **STE:** The `AccountController` manages authentication and user profile
> operations.

---

## Rule 1.9 — Select short, easy technical nouns

When no approved technical noun exists in your project, company, industry, or
subject field, select one that is short (not more than three words) and easy to
understand. Do not write a long descriptive phrase when a shorter term is
enough. When the context identifies the item — a code snippet, a line number, a
diagram, an API reference — use the shortest unambiguous term. Add one or two
adjectives only when clarification is necessary.

```javascript
// client.js — line 42
async function fetchUtility(url) {
  const response = await fetch(url);
  return response.json();
}
```

> **Non-STE:** Call the asynchronous JavaScript XML HTTP request wrapper utility
> function (line 42) to get the serialized JSON payload from the remote
> application programming interface endpoint.
>
> **STE:** Call the `fetchUtility` function (line 42) to get the JSON data from
> the API endpoint.

---

## Rule 1.10 — No regional, slang, or jargon words as technical nouns

Some technical words are used only inside confined communities or single
technology ecosystems. They are not easy to understand for readers from a
different background or stack. Code documentation is read by junior developers,
developers from other language communities, and non-native English speakers: a
word that one subculture finds clear can be opaque to every other reader. Always
select well-known words.

| Do not write | Write |
|---|---|
| Remove all the cruft from the legacy module. | Remove all the unnecessary code from the legacy module. |
| The function monkeys with the input data before validation. | The function changes the input data before validation. |
| Bikeshedding delayed the API design by two weeks. | Unnecessary discussion about small details delayed the API design by two weeks. |
| I spent the morning yak shaving before I could write the test. | I spent the morning completing unrelated prerequisite tasks before I could write the test. |
| Replace the foo and bar placeholders with real values. | Replace the example and placeholder values with real values. |

---

## Rule 1.11 — One technical noun per item

Do not use a different code-domain technical noun in another part of your
documentation for the same item. Changing the name of one item between sections
forces the reader to decide whether you mean the same item or a different one.
The source of truth for the name is the code: the class, function, module,
table, resource, environment variable, or configuration key as it is defined in
the repository.

> **Non-STE:**
> 1. Initialize the UserService class to start the session manager.
> 2. Call the authenticate method on the AccountManager to verify a user.
> 3. The UserHandler returns a session token that you send in later requests.
>
> **STE:**
> 1. Initialize the UserService class to start the session manager.
> 2. Call the authenticate method on the UserService to verify a user.
> 3. The UserService returns a session token that you send in later requests.

> **Non-STE:** "/api/login path", "authentication route", "login endpoint" —
> three names for one endpoint.
>
> **STE:** Use "/api/login endpoint" in every sentence, because the OpenAPI file
> defines the path as `/api/login`.

---

## Rule 1.12 — Code-domain technical verb categories

A code-domain technical verb is a verb term that refers to a specified operation
or process in software development and is applicable to a subject field. The
controlled terminology does not include them all; keep yours in the project
glossary or terminology database.

Code-domain technical verbs must obey the same rules as other approved verbs.
Use them in procedural and descriptive texts when you can put them in one or more
of these four categories (examples only, not a complete list):

1. **Development processes**
   - a) Write and modify code: compile, concatenate, import, inject, instantiate,
     lint, minify, marshal, optimize, polyfill, refactor, resolve, shim, stub,
     substitute, tokenize, transpile, trace, vectorize
   - b) Test and verify code: assert, benchmark, debug, fuzz, instrument, mock,
     profile, snapshot, spy, stub, unit-test
   - c) Build and package: bundle, deploy, package, publish, release, tag, version
   - d) Manage dependencies: hoist, install, link, lock, pin, update, upgrade

2. **Computer processes and applications**
   - a) Input and output: click, copy, cut, digitize, enter, paste, press, print,
     scan, swipe, tap, type
   - b) UI and application operations: clear, close, delete, deselect, disable,
     drag, enable, encrypt, erase, filter, hide, highlight, invalidate, maximize,
     minimize, navigate, open, save, scroll, select, show, sort, store, submit,
     toggle, validate, zoom in, zoom out
   - c) System operations: abort, authenticate, authorize, boot, cache,
     communicate, configure, debug, deserialize, download, format, hydrate,
     initialize, install, load, log, manage, mount, process, reboot, render,
     retry, serialize, spawn, synchronize, throttle, update, upgrade, upload

3. **Instructions and information for applicable subject fields**
   - a) Algorithmic, mathematical, data: aggregate, bisect, compute, concatenate,
     convert, count, decode, encode, escape, filter, hash, index, map, merge,
     normalize, parse, pipeline, precompute, recalculate, reduce, tokenize,
     transform, validate, verify
   - b) Database and storage: backup, compact, flush, index, migrate, persist,
     query, replicate, restore, roll back, seed, shard, upsert, vacuum,
     write-ahead
   - c) Network and communication: broadcast, connect, disconnect, establish,
     forward, handshake, intercept, listen, poll, proxy, reject, resolve, route,
     send, stream, timeout, tunnel, unsubscribe, webhook
   - d) Security and authentication: authenticate, authorize, decrypt, decode,
     encode, encrypt, hash, revoke, salt, sanitize, sign, validate, verify

4. **Legal and licensing terms** — only for legal and regulatory texts:
   acknowledge, assign, comply with, conform to, disclose, enforce, explain,
   grant, inform, license, modify, notify, permit, regulate, sign, supersede,
   waive

If there is an approved verb in the controlled terminology that accurately gives
the instruction or information, use the approved verb. Do not use a code-domain
technical verb if you can write the same sentence with approved words.

> **Non-STE:** If you detect a null pointer exception in the parser, fix it before
> the response returns to the client.
>
> **STE:** If you find a null pointer exception in the parser, fix it before the
> response returns to the client.

> **STE:** Read the API key from the configuration file. ("Enter" is a
> code-domain technical verb, category 2 a.)

> **Non-STE:** Run the database migration to version 3, then verify the row
> counts before you open the service.
>
> **STE:** Run the migration of the database schema to version 3, then check the
> row counts before you open the service. (Prefer approved "run" + technical noun
> "migration" over the technical verb "migrate" when precision is not lost.)

Dual-category note: a word may be both a technical verb (Rule 1.12) and a
technical noun (Rule 1.5). For example `deploy` is a technical verb (category 1
c) and a technical noun (category 5); `serialize` is a technical verb and also a
method name (technical noun). Let your project glossary decide the role.

---

## Rule 1.13 — Do not use code-domain technical verbs as nouns

Use code-domain technical verbs only as verbs, not as nouns. If you need a noun,
find an approved noun or a code-domain technical noun with the equivalent meaning.

The most common violation is the **light verb construction**: a weak verb (do,
make, perform, execute, run) paired with a nominalized technical verb.

| Do not write | Write |
|---|---|
| Make a commit of your changes | Commit your changes |
| Do a compile of the source files | Compile the source files |
| Execute a rollback of the migration | Roll back the migration |
| The import of the module takes ten seconds | The import operation for the module takes ten seconds |
| The merge of the feature branch caused a conflict | The merge operation of the feature branch caused a conflict |

Dual-category exception: when a word fits both a technical verb category (Rule
1.12) and a technical noun category (Rule 1.5), you may use it as a noun.

| Word | Technical Verb | Technical Noun |
|------|---------------|---------------|
| build | 1 c) Build and package | 3) Development tools |
| deploy | 1 c) Build and package | 5) Infrastructure, deployment, and platforms |
| test | 1 b) Test and verify code | 3) Development tools |
| commit | 2 c) System operations | 4) Data structures |
| merge | 1 c) Build and package | 4) Data structures |
| release | 1 c) Build and package | 5) Infrastructure, deployment, and platforms |
| patch | 1 a) Write and modify code | 4) Data structures |
| log | 2 c) System operations | 13) Runtime environments |
| import | 1 a) Write and modify code | 4) Data structures |

Article test: if you can put "a / an / the" before the word and the sentence
stays grammatical, the word is acting as a noun. If it is not a dual-category
word, the usage violates Rule 1.13. "The build failed" is correct (dual-category);
"the compile failed" is wrong (compile is only a technical verb).

Quoted tool output (Rule 1.5 category 10) is exempt: a compiler message that says
"compile error" is text you did not write and must not be changed.

> **See also:** Rule 1.5, Rule 1.7, Rule 1.12.

---

## Rule 1.14 — Use American English spelling unless other official directives tell you differently

Use the spelling specified in the STE-Code controlled terminology (American
English). Use a different spelling only if other project specifications, style
guides, contracts, or official directives apply.

If quoted text has British English spelling — an error message, a code comment, a
user interface label, terminal output — do not change it. Keep the quoted text as
it is (Rule 8.6). The surrounding prose must use American English spelling.

Common British → American pairs:

| British | American | Context |
|---------|----------|---------|
| colour | color | UI, terminal, theming |
| behaviour | behavior | feature descriptions, bug reports |
| organise | organize | restructuring, refactoring |
| analyse | analyze | profiling, data processing |
| licence (noun) | license | software license, license key |
| defence | defense | security fixes |
| centre | center | layout, positioning |
| initialise | initialize | object initialization |
| serialise | serialize | object serialization |
| optimise | optimize | performance optimization |
| parametrise | parameterize | parameterized types |
| cancelled | canceled | canceled operations |
| customise | customize | custom behavior |
| minimise | minimize | rollout minimization |
| synchronise | synchronize | state sync |
| traveller | traveler | traveler pattern |

> **Non-STE:** The log file shows the colour of each output line. Initialise the
> variable before you use it in the loop.
>
> **STE:** The log file shows the color of each output line. Initialize the
> variable before you use it in the loop.

> **STE:** The terminal shows the message `Colour profile not recognised`.
> (Quoted terminal output keeps its British spelling; the prose around it uses
> American English.)

> **See also:** Rule 8.6 — Use Quoted Texts Correctly.

---

## Extension adjectives for Section 1

These adjectives are approved extensions to the controlled terminology, added for
the code domain. Use them as the specified part of speech (Rule 1.2).

| Adjective | Definition | STE example |
|-----------|------------|-------------|
| idempotent | Describes an operation that produces the same result when applied more than once, with no extra side effects after the first run. | Make the retry handler idempotent so a second call with the same input does not duplicate the record. |
| immutable | Describes a data structure or value that cannot be changed after it is created, which prevents accidental shared-state bugs. | Keep the request context immutable so concurrent threads cannot overwrite each other's values during a single operation. |
| atomic | Describes an operation that completes fully or not at all, with no partial result visible to other processes. | Wrap the balance update in an atomic transaction so the debit and credit always succeed or fail together. |
| thread-safe | Describes code that functions correctly when accessed by multiple threads at the same time without external locking. | Mark the singleton constructor thread-safe so two threads can call it on first use without creating two instances. |
| asynchronous | Describes a call or task that starts and returns before its work finishes, so the caller can do other work meanwhile. | Make the file upload asynchronous so the user interface stays responsive while the transfer runs in the background. |
| concurrent | Describes tasks that make progress within the same time period, interleaved by the scheduler rather than strictly sequentially. | Run the test suites in concurrent processes so the full check finishes in a fraction of the time. |

The full extension inventory (nouns, verbs, and adjectives) is in
`ste-code/artifacts/level5/06-extensions.md`.

---

## Reference catalogue

These external references inform the STE-Code controlled vocabulary. They are
**not** part of the standard; they are kept in `.agents/reference/` outside
`final/`. They are listed here as a catalogue only.

| Reference | Type | Source |
|---|---|---|
| Microsoft Writing Style Guide | page | https://learn.microsoft.com/en-us/style-guide/welcome/ |
| MicrosoftDocs/microsoft-style-guide (GitHub source) | page | https://github.com/MicrosoftDocs/microsoft-style-guide |
| Google Style Guides | page | https://google.github.io/styleguide/ |
| Kong/apiglossary | page | https://github.com/Kong/apiglossary |
| dwyl/technical-glossary | raw | https://raw.githubusercontent.com/dwyl/technical-glossary/main/README.md |
| jvalentino/glossary | page | https://github.com/jvalentino/glossary |
| GitHub Official Glossary | page | https://docs.github.com/en/get-started/learning-about-github/github-glossary |
| DevOps Style Guide Glossary | page | https://tydukes.github.io/coding-style-guide/glossary/ |
| ryanwi software-terms.dic | raw | https://gist.githubusercontent.com/ryanwi/6135845/raw/software-terms.dic |
| OpenSTE.org | pointer | https://openste.org/ |
| en-wl/wordlist (SCOWL) | page | https://github.com/en-wl/wordlist |
| MichaelWehar 5000-more-common | raw | https://raw.githubusercontent.com/MichaelWehar/Public-Domain-Word-Lists/master/5000-more-common.txt |
| dwyl/english-words | pointer | https://github.com/dwyl/english-words |

The full catalogue, with local mirror paths, is in
`ste-code/artifacts/level5/07-catalogue.md`.

---

## Provenance

Section 1 of STE-Code is adapted from ASD-STE100 Issue 9, Part 1, Section 1
(Words). The adaptation is semantic, not a word swap: each rule keeps its intent
and structure, and the examples and categories are re-expressed for software
documentation. Two structural changes apply to this section:

- The 22 technical noun categories of the source specification become **19**
  code-domain categories (Rule 1.5).
- The technical verb categories become **4** code-domain categories (Rule 1.12).

Per-rule source mapping and the original rule text are in
`ste-code/final/rules/a-sec1-rule1.*.md`, and the tier-wide provenance record is
in `ste-code/artifacts/level5/08-provenance.md`.

---

## Section 1 checklist for LLM generation and review

For each word in the prose you generate:

1. Is the word approved in the controlled terminology? If yes, check the part of
   speech (1.2), the meaning (1.3), and the form (1.4).
2. If it is not approved, is it a code-domain technical noun in one of the 19
   categories (1.5, 1.6)? Use it only as a noun (1.7).
3. If it is not a noun, is it a code-domain technical verb in one of the 4
   categories (1.12)? Use it only as a verb (1.13), and prefer an approved verb
   when one carries the same meaning.
4. Prefer the name already used in the repository or project glossary (1.8), keep
   it short (1.9), avoid slang and jargon (1.10), and use the same name for the
   same item everywhere (1.11).
5. Spell in American English (1.14), but never change quoted text.

If a word passes no gate, replace it or rewrite the sentence.

