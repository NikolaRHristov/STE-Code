# Level 5 — Section 1 (Part 2): Rules 1.5–1.9 (Code-Domain Technical Nouns)

This slice covers the five STE-Code rules that govern **code-domain technical nouns** —
the domain-specific vocabulary (class names, libraries, protocols, algorithms, defects,
infrastructure terms) that is permitted in documentation even though it is not in the
approved STE-Code dictionary.

Read this slice together with `rules-sec1-part1.md` (Rules 1.1–1.4) and
`rules-sec1-part3.md` (Rules 1.10–1.14).

## Purpose and scope

- Rule 1.5 — which words may appear as code-domain technical nouns (the 19 categories).
- Rule 1.6 — the *gate*: a non-approved word is allowed only as a technical noun.
- Rule 1.7 — a technical noun must never be used as a verb.
- Rule 1.8 — when several names exist, use the standard/approved one.
- Rule 1.9 — when you must choose a technical noun, pick the shortest unambiguous form.

These five rules answer: *"Is this word allowed, and if so how should I write it?"*

## How the five rules interact

```
Word in documentation?
 ├─ approved STE-Code word (Rule 1.1) ──────────────► use it as its part of speech (Rule 1.2)
 └─ not approved
      └─ is it a code-domain technical noun? (Rule 1.5 / 1.6 gate)
           ├─ NO  ───────────────────────────────────► forbidden (replace with approved word)
           └─ YES
                ├─ use the STANDARD name (Rule 1.8)
                ├─ use the SHORTEST form (Rule 1.9)
                ├─ keep it a NOUN (Rule 1.7) ── not a verb
                └─ register it in the project glossary
```

---

# Rule 1.5 — Use Words That You Can Include in a Code-Domain Technical Noun Category

**Statement:** You may use a word that names a precise code-domain concept if it fits one
of the nineteen categories below. Such words are *code-domain technical nouns* and are
allowed even though they are not in the approved STE-Code dictionary.

The dictionary cannot list every technical noun (there are too many, and each project uses
different ones). Register every technical noun you use in your **project glossary** with:
its term, its category, its approved meaning, and an example sentence.

## The nineteen categories

1. **Code components, modules, and libraries** — `class, controller, helper, hook,
   middleware, mixin, module, package, plugin, provider, repository, service, utility`
2. **Computing devices and their components** — `CPU, disk, GPU, keyboard, laptop,
   memory, monitor, mouse, printer, screen, server, smartphone, tablet, terminal`
3. **Development tools, environments, and support equipment** — `CLI, compiler, debugger,
   Docker, editor, IDE, Git, Jest, linter, loader, Prettier, terminal, test runner,
   TypeScript, webpack`
4. **Data structures, types, and formats** — `array, boolean, buffer, CSV, enum, hash map,
   integer, JSON, linked list, object, queue, stack, string, struct, tree, tuple, XML, YAML`
5. **Infrastructure, deployment, and platforms** — `AWS, CI/CD, container, deployment,
   Heroku, Kubernetes, load balancer, Node.js, pipeline, pod, production, staging, Vercel`
6. **Systems, subsystems, and architectural components** — `API gateway, authentication
   layer, caching layer, client, database layer, message broker, microservice, proxy, rate
   limiter, REST API, routing layer, server, WebSocket`
7. **Mathematical, algorithmic, and scientific terms** — `Big O notation, binary search,
   coefficient, complexity, exponent, hash function, iteration, logarithm, matrix,
   recursion, regex, sorting algorithm, time complexity, traversal`
8. **Interface elements and navigation** — `button, checkbox, dialog, dropdown, footer,
   header, menu, modal, navigation bar, radio button, scrollbar, sidebar, tab, text field,
   toggle, tooltip`
9. **Numbers, units of measurement, and time** — `byte, gigabyte (GB), hertz (Hz), hour (h),
   kilobyte (KB), megabyte (MB), millisecond (ms), minute, nanosecond (ns), second (s),
   terabyte (TB)`
10. **Quoted text** — verbatim text that cannot change: error messages, code snippets,
    UI labels, log output. `Cannot read properties of undefined`, `404 Not Found`,
    `connection refused`, `Submit` button
11. **Professional roles, teams, and organizations** — `administrator, backend developer,
    contributor, DevOps engineer, frontend developer, Google, maintainer, Microsoft, product
    owner, QA engineer, reviewer, scrum master, user`
12. **Official documents, API references, and standards** — `API reference, changelog, code
    of conduct, contributing guide, diagram, figure, Getting Started guide, HTTP
    specification, note, paragraph, README, release notes, RFC, section, table, warning`
13. **Runtime environments and operational conditions** — `development, environment
    variable, garbage collection, heap, hot reload, live reload, memory leak, production,
    sandbox, stack trace, staging, test, thread, timeout, virtual machine`
14. **Colors** — `black, blue, cyan, gray, green, magenta, orange, red, white, yellow`.
    Colors are adjectives but are treated as code-domain technical nouns. Comparative/superlative
    forms (`blacker`, `the reddest`) are forbidden.
15. **Defects, errors, and fault terminology** — `assertion failure, bug, crash, deadlock,
    defect, exception, hang, infinite loop, memory leak, null pointer, race condition,
    regression, stack overflow, timeout, type error`
16. **Computer science, information, and communication technology** — `AI, algorithm,
    authentication, authorization, blockchain, containerization, cryptography, database,
    encoding, encryption, firewall, hashing, internet, machine learning, metadata, neural
    network, protocol, query, sandbox, schema, token, virtualization`
17. **Legal and licensing terms** — `Apache 2.0, BSD license, compliance, copyright, GPL,
    license, MIT license, open source, proprietary, terms of service, third-party,
    trademark, warranty`
18. **Database and storage terminology** — `connection pool, cursor, foreign key, index,
    migration, NoSQL, ORM, PostgreSQL, primary key, query, Redis, relation, row, schema,
    seed, SQL, SQLite, stored procedure, table, transaction, view`
19. **Network and protocol terminology** — `DNS, endpoint, HTTP, HTTPS, IP address,
    localhost, middleware, packet, port, request, response, route, socket, SSH, TCP, TLS,
    UDP, URL, VPN, WebSocket`

The lists above are **examples only** — Rule 1.5 does not give a complete list of every
possible code-domain technical noun.

## Relationship to other rules

- **Rule 1.1** (approved words): use an approved word whenever one exists. Use a
  code-domain technical noun only when no approved word names the concept.
- **Rule 1.6** (non-approved words as technical nouns): a non-approved word must belong to
  at least one of these nineteen categories to appear at all.

## Quick application guidance

| Documentation type | Primary categories | Example |
|---|---|---|
| README | 1, 3, 5, 17 | "This package provides a middleware for Express." |
| API documentation | 6, 18, 19 | "The `GET /users/:id` route returns a JSON object with a user struct." |
| Docstrings/comments | 4, 7, 15 | "Traverse the binary search tree in-order and return a sorted array." |
| Commit messages | 1, 15, 18 | "Fix race condition in the connection pool that caused a deadlock on PostgreSQL." |
| Error messages | 13, 15, 19 | "Connection refused: the TCP socket on port 5432 timed out after 30 seconds." |
| Test specs | 1, 4, 15 | "The test calls `parseConfig` with a null pointer and checks for an assertion failure." |

## Edge cases

- **Framework names that are also common words** (`React`, `Go`, `Rust`, `Swift`, `Vue`):
  treat as code-domain technical nouns (category 3 or 5); capitalize to distinguish from
  the English verb ("the Swift language", "the Rust compiler").
- **Code keywords in prose** (`if`, `for`, `class`, `return`): when quoted/backticked they
  are category 10; when used as English words they must follow approved meanings.
- **Abbreviations/acronyms** (`API, JSON, SQL`): allowed; define at first use unless
  universally understood by the audience.
- **Project-internal names** (`PhoenixCache`): allowed only if registered in the glossary.
- **Numbers as named tokens** (`Node.js 18`, `404`, `port 5432`): quoted text or category 9;
  must appear verbatim.

<!-- END-RULE-1.5 -->

---

# Rule 1.6 — Use a Non-Approved Word Only As a Code-Domain Technical Noun

**Statement:** A word that is not approved in the controlled terminology may appear only
when it is a code-domain technical noun, or part of one (Rule 1.5).

This is a **gate** with three tests. An unapproved word may stay only if it clears all three.

## The Technical Noun Gate — three tests

| Test | Question | Pass | Fail |
|---|---|---|---|
| 1 | Is the word unapproved? | approved words skip the gate entirely | — |
| 2 | Is it a technical noun, or part of a compound technical noun (19 categories)? | standalone noun or recognized compound | replace with approved word |
| 3 | Is it used as a noun in the sentence? | noun role | verb/adjective role → replace |

Worked trace — *"The main config loader backups the data through the handler pipeline."*

| Phrase | T1 unapproved? | T2 technical noun? | T3 noun? | Result |
|---|---|---|---|---|
| main config loader | yes | "main" is a general adjective, not a recognized compound | — | "main" → "primary" |
| backups | yes | "backup" as a verb is not a noun | used as verb | "makes an auxiliary copy" |
| handler pipeline | yes | "handler + pipeline" not a recognized compound | fails T2 | "processing pipeline" |

Result: *"The primary config loader makes an auxiliary copy of the data through the
processing pipeline."*

## Key dictionary entries

- **BASE (n) — UNAPPROVED.** Alternatives: BOTTOM (surface/stack), ROOT (filesystem).
  Allowed in compounds: `base case` (cat 7), `base class` (cat 1), `base URL` (cat 8).
- **MAIN (adj) — UNAPPROVED.** Alternative: PRIMARY. Allowed in `main branch` (cat 5),
  `main()` / main function (cat 1, entry point).
- **HANDLER (n) — UNAPPROVED.** Alternative: FUNCTION. Allowed in `event handler`,
  `request handler` (cat 1).
- **BACKUP (n, v) — UNAPPROVED.** Alternatives: AUXILIARY (adj), "makes an auxiliary copy"
  (verb). Allowed in `backup file`, `backup_logs` (cat 18), `/api/v1/backup` (cat 19).
- **BOTTOM, FUNCTION, PRIMARY, AUXILIARY, ROOT** — APPROVED (use these as replacements).

## Compound technical noun checklist

A compound counts as a code-domain technical noun only if ALL are true:
1. The words name one concept the domain recognizes.
2. The compound fits one of the 19 categories.
3. Swapping the unapproved word for its approved alternative changes the recognized name
   and causes confusion.

Criterion: does the compound appear in the framework/language/standard official docs?
Yes → technical noun. No → replace the unapproved words with approved ones.

## Most-used categories for Rule 1.6

1 (code components), 3 (dev tools), 5 (infrastructure), 7 (algorithmic), 8 (directory
hierarchy), 18 (database), 19 (computer science/network).

## Examples

- *"The handler processes each incoming event."* → *"The function processes each incoming
  event."* (standalone "handler" is unapproved).
- *"The event handler processes each incoming event."* → STAYS (compound technical noun, cat 1).
- *"The main configuration has the latest values."* → *"The primary configuration…"*
  ("main" as adjective fails; "main branch" would stay).
- *"Check out the main branch, then copy the files to the base of the build folder."* →
  *"…to the bottom of the build folder."* ("base" as surface word → "bottom").

## Edge cases

- **Framework name used as general verb** — `pandas` stays; "data-frame" verb → "load … into
  a data frame".
- **Code keyword as general noun** — "The `class` of objects…" → "category"; keyword
  `return` stays backticked.
- **Invented compounds** (`handler pipeline`, `backup orchestrator`, `main dispatcher`) —
  not recognized → restructure with approved words.
- **Generated docs** — fix the *source* (docstrings/comments), not the generated output.
- **Brand names** — always technical nouns; descriptive echoes still reviewed.

<!-- END-RULE-1.6 -->

---

# Rule 1.7 — Do Not Use Words That Are Technical Nouns as Verbs

**Statement:** Use a code-domain technical noun only as a noun (or as an adjective inside a
compound technical noun). Do **not** use it as a verb.

The repair pattern: use an approved verb followed by the noun in a prepositional phrase.
*Cache the data* → *Put the data in the cache*. *Database the records* → *Store the records
in the database*. *Queue the jobs* → *Put the jobs in a queue*.

## The dual-category exception

Some words are cataloged in **both** a noun category (Rule 1.5) and a verb category
(Rule 1.12). Then the verb form is allowed **in its approved verb sense** only. Decide in
your glossary which part of speech the word has and obey that decision.

| Word | Noun (Rule 1.5) | Verb (Rule 1.12) |
|---|---|---|
| cache | cat 16: "The cache stores responses." | cat 2c: "Cache the responses." |
| log | cat 18: "Write a log entry." | cat 2c: "Log the error." |
| queue | cat 4: "Add the job to the queue." | cat 3a: "Queue the job." |
| filter | cat 4 / 16 | cat 2b: "Filter the results." |
| sort | cat 7 | cat 2b: "Sort the list by name." |
| map | cat 4 | cat 3a: "Map the function over the list." |

RULE: if a word is cataloged as a noun only → obey Rule 1.7. If both → use the verb form
only when the context matches the verb category. Keep noun and verb uses distinct
(*"Log the error and write the entry to the log file"*, not *"Log the log to the log"*).

## Common noun→verb violations by paradigm

| Paradigm | Noun | Wrong (verb) | Right construction |
|---|---|---|---|
| OOP | interface | "Interface the module with…" | "Add an interface between the module and…" |
| OOP | class / singleton / factory | "Class the model." / "Singleton the logger." | "Make a class for…" / "Make the logger a singleton." |
| Functional | monad / functor | "Monad the value." | "Wrap the value in a monad." |
| Functional | closure / lambda | "Closure the var." | "Capture the var in a closure." |
| Procedural | buffer / pointer / heap | "Buffer the output." | "Write the output to a buffer." |
| Declarative | table / schema / index | "Schema the database." | "Apply a schema to the database." |
| Systems | mutex / semaphore / DMA | "Mutex the state." | "Lock the mutex for the state." |

## Tool, brand, and protocol names

These are always code-domain technical nouns — never verbs.

- *"Docker the application, Git the changes"* → *"Containerize the application, commit the changes."*
- *"Google the error, Slack the results"* → *"Search for the error with Google, send the results with Slack."*
- *"Kubernetes the microservices, Terraform the infra"* → *"Deploy the microservices with Kubernetes, provision the infra with Terraform."*
- *"JSON the response, HTTP it to the client"* → *"Encode the response as JSON, send it through HTTP."*
- *"Microservice the monolith, API the services"* → *"Break the monolith into microservices, add an API for each service."*

## Multi-word technical nouns

Keep the full phrase; do not drop a word to make a verb.

- *"Load balance the requests"* → *"Distribute the requests with a load balancer."*
- *"Rate limit the clients"* → *"Set a rate limit for the clients."*
- *"Feature flag the endpoint"* → *"Put the endpoint behind a feature flag."*
- *"Circuit break the service"* → *"Apply a circuit breaker to the service."*

## Edge cases

- **Framework names that are also English verbs** (`React`, `Go`, `Spring`, `Express`) —
  stay nouns: *"Write the middleware with Express and respond to changes with React."*
- **Code keywords as verbs** (`class`, `import`, `return`, `yield`) — refer to them as
  backticked nouns; use approved verbs for the action. (Note: `return` is itself an approved
  verb; format the keyword as `` `return` `` when naming the construct.)
- **Generated symbol names** (`toJson()`, `UserBuilder`) — exempt; refer to them as nouns
  in prose ("makes a `User` object", "encodes output as JSON").

## Preposition-phrase repair reference

| Noun-verb | Repair | Verb | Prep |
|---|---|---|---|
| Cache the data | Put the data in the cache | put | in |
| Queue the job | Add the job to the queue | add | to |
| Buffer the output | Write the output to a buffer | write | to |
| Socket the connection | Send the connection through a socket | send | through |
| Database the records | Store the records in the database | store | in |
| Docker the app | Package the app in a container | package | in |
| JSON the response | Encode the response as JSON | encode | as |

<!-- END-RULE-1.7 -->

---

# Rule 1.8 — Use Code-Domain Technical Nouns Approved in Your Project, Company, Industry, or Subject Field

**Statement:** When more than one name exists for a code concept, use the name from the most
authoritative source. Do not invent names for items that already have established names in
your codebase or domain. Consistency lets readers find the exact element in the source tree.

## Authority hierarchy (highest first)

1. **Source code** — class names, function names, file names, variable names, type names.
2. **Language specification** — keyword names, standard-library names, built-in types.
3. **Framework/library documentation** — API names, component names, hook names, config keys.
4. **Project glossary** — project-specific terms registered under Rule 1.5.
5. **Industry standard** — design-pattern names, protocol names, algorithm names, architecture names.
6. **Company documentation** — internal system/service/team names.

When the codebase name differs from the industry name, mention both with clear context:
codebase name for traceability, industry name for comprehension. Never mix names from
different levels for the same concept in one document.

## Paradigm reference: avoid → use

| Paradigm | Avoid (invented) | Use (approved) | Authority |
|---|---|---|---|
| OOP | user manager / user handler | `UserRepository` | source code |
| OOP | maker pattern | Factory pattern | pattern literature |
| OOP | data layer / DB interface | `IRepository<T>` | source code |
| Functional | maybe-type / chain functions | `Option` / `None`, pattern matching | language stdlib |
| Functional | higher-order function? (keep) | Higher-order function | math terminology |
| Procedural | heap allocation / data record | `malloc`, `struct`, `pointer` | C spec |
| Procedural | green process | `goroutine` | Go spec |
| Declarative | compute instance | `aws_instance` | Terraform provider docs |
| Declarative | retrieval query | `SELECT` statement | SQL standard |
| Systems | ownership handoff | `move` semantics, `borrow` | Rust reference |
| Systems | thread lock | `Mutex` | stdlib |

## Key principles

- Use exact class/function/type names from the source; do not substitute descriptive phrases
  (*"account controller"* → `AccountController`).
- Use exact protocol/algorithm/framework feature names (*"secure web communication"* →
  `HTTPS`; *"function that manages state and side effects"* → `useEffect`).
- **Define each acronym at first use**, then use only the acronym (*"application programming
  interface (API) … The API returns JSON"*). Alternating full form and acronym implies two
  concepts (violates Rule 1.11).
- Keep the capitalization/spelling of the approved name exactly as in the source
  (`userService`, `findById`, `DATABASE_URL`).
- When a framework renames a standard concept (Django "view", Rails "partial"), use the
  framework's own term in framework-specific docs.
- During a migration, use the **target** name; show the old name only as quoted/DEPRECATED.

## Edge cases

- **Codebase uses a non-standard name** (e.g. `DataStore` for a Repository) — use the
  codebase name; optionally note the industry pattern ("`DataStore` (a Repository
  implementation)").
- **Two industry standards compete** (callback/handler/listener; map/dictionary/object) —
  pick one, register it, use it consistently (Rule 1.11); prefer the ecosystem name.
- **Approved name is an acronym** (API, JSON, JWT) — define at first use unless universal.
- **Framework renames a standard concept** — use framework's term in its own docs.
- **Name changes during refactor** — use the new name; mark the old one DEPRECATED.
- **Same package, different registries** (`python-dotenv` on PyPI vs `dotenv` on npm) — use
  the ecosystem-specific name in installation instructions.

<!-- END-RULE-1.8 -->

---

# Rule 1.9 — When You Must Select a Technical Noun, Use One That Is Short and Easy to Understand

**Statement:** When no code-domain technical noun is approved in your project/industry,
select one that is **short (not more than three words)** and easy to understand. Do not use
long descriptive phrases when a shorter term is sufficient. If the context already
identifies the item, use the shortest unambiguous term; add one or two adjectives only when
needed for disambiguation.

## Core insight: context permits brevity

Context sources that make a short term sufficient: a code reference (line number, function
name, file path), a diagram, a preceding definition, an API spec, or a code snippet that
follows the prose. The code itself carries the detail — the prose only needs to name it.

Examples:
- *"asynchronous JavaScript XML HTTP request wrapper utility function (line 42)"* →
  *"`fetchUtility` function (line 42)"*
- *"user account profile information data transfer object"* → *"`UserProfileDTO`"*
- *"multi-platform containerized microservice orchestration and deployment management layer"*
  → *"the Kubernetes cluster"*
- *"the relational database management system server instance"* → *"the database"*

## Long phrase → short form reference

| Long phrase | Short STE form | Context that permits it |
|---|---|---|
| asynchronous JS XML HTTP request wrapper utility function | fetch utility | line number + snippet |
| serialized JSON payload from the remote API endpoint | JSON data from the API endpoint | field name + type |
| user account profile information data transfer object | `UserProfileDTO` | parameter already named |
| relational database management system server instance | database | port + "primary" |
| mutual exclusion lock primitive with timeout acquisition | mutex | class name in code |
| configuration, settings, and options parameters object | `Config` object | object named `Config` |
| dynamically allocated resizable memory region utility | dynamic array | type declared |

## The three-word limit — rationale and exceptions

The limit (≤3 words) reflects working-memory capacity. Exceptions:
1. **Established technical terms** — "continuous integration pipeline", "abstract syntax
   tree", "public key infrastructure certificate" (standard even if >3 words; do not invent a
   shorter form).
2. **Framework/tool proper names** — "GitHub Actions workflow", "AWS Lambda" (use as given).
3. **Fully qualified type names** — use the short name after first reference
   (`SubComponent` for `com.example.module.SubComponent`).
4. **Shortening causes ambiguity** — keep the longer form; clarity overrides brevity.

## Adjectives: keep only disambiguating ones

- Noise: "the configurable application settings object" (all settings objects are
  configurable), "the secure HTTPS protocol" (HTTPS is secure by definition).
- Disambiguating: "the production application settings object" (prod/staging/dev coexist),
  "the legacy HTTPS endpoint" (old and new coexist).

## Abbreviations and acronyms

- **Universal** (use on first reference, expansion optional): API, JSON, SQL, HTML, HTTP,
  URL, DNS, TCP, TLS, CPU, RAM, SSD.
- **Domain-specific** (expand on first use for a general audience): JWT, CORS, ORM, SPA, SSR.
- **Project-specific** (define on first use in every document; accepted only after defined).
- Do **not** invent new abbreviations to satisfy brevity (Rule 1.8 — use the recognized term).

## Paradigm guidance

- **OOP:** use the class name; state inheritance in a separate sentence
  (*"`UserRepository` extends `BaseRepository<User>`"*), not six stacked modifiers.
- **Functional:** name the *result*, not the whole data-flow chain (*"The fold function. It
  reduces a collection to a single value."*).
- **Procedural:** name the function; let the signature carry types (*"The `fprintf`
  function. It writes formatted output to a file descriptor."*).
- **Declarative:** name the resource type; describe config in bullets/table
  (*"The `HorizontalPodAutoscaler` resource. Set min/max replicas."*).
- **Systems:** use short terms (*reference, borrow, lifetime*); the compiler enforces
  guarantees — describe what the programmer controls, not what the compiler prevents.

## Edge cases

- **Short term less well-known than long** (e.g. `AST`) — expand on first use
  ("abstract syntax tree (AST)"), then use the short form. Test: would a 1-year-experienced
  developer in this domain understand it?
- **Framework name is also a short word** (`React`, `Go`) — use as modifier ("the React
  framework") on first use; do not invent abbreviations like "Rkt".
- **Codebase uses long names internally** (`AbstractUserAuthenticationProviderFactoryBean`)
  — Rule 1.8 wins: use the codebase name as given; use a short prose alias only in surrounding
  text ("the factory bean").
- **Shortening creates a homonym** (`pool` = thread/connection/object) — keep the disambiguating
  modifier ("connection pool", "thread pool") when both appear.
- **Generated docs** — auto-generated portions exempt; human-written summaries/descriptions
  must obey the rule.

---

## Cross-references (Rules 1.5–1.9)

- **Rule 1.1 (Approved Words)** — use approved words for common vocabulary; technical nouns
  supply domain terms.
- **Rule 1.2 (Part of Speech)** — technical nouns are nouns; noun-verbing violates it (Rule 1.7).
- **Rule 1.3 (Approved Meanings)** — a technical noun has its registered meaning only.
- **Rule 1.5 (Technical Noun Categories)** — defines which words qualify (this slice).
- **Rule 1.6 (Non-Approved Words as Technical Nouns)** — the gate; pairs with Rule 1.5.
- **Rule 1.7 (No Noun-Verbing)** — technical nouns stay nouns.
- **Rule 1.8 (Standard Technical Nouns)** — choose the approved name among candidates.
- **Rule 1.9 (Short Technical Nouns)** — choose the shortest unambiguous form.
- **Rule 1.10 (No Slang/Jargon)** — invented names are forbidden; use the standard noun.
- **Rule 1.11 (One Term per Concept)** — use the chosen name consistently everywhere.
- **Rule 1.12 (Technical Verbs)** — permits verb forms in the dual-category exception.
- **Rule 1.13 (No Verb-as-Noun)** — inverse of Rule 1.7 for verbs.
- **Rule 1.14 (American English Spelling)** — follow the spec's spelling for spec-defined names.

<!-- END-SLICE -->

