# Level 4 — Section 1: Technical Noun Rules (Rules 1.5–1.9)

This sub-document is the LLM-optimized distillation of STE-Code Section 1 rules that
govern **technical nouns** — the words you may use outside the approved dictionary
because they name a precise code-domain concept. It covers Rules **1.5, 1.6, 1.7, 1.8,
and 1.9**.

Audience: people who use LLMs to generate code documentation and want the model to
obey STE-Code's technical-noun rules. Use this file as a constraint sheet: every
non-approved word in generated documentation must clear the gate described below.

Voice: plain, code-domain. No aerospace leakage. Examples use software terms only.

Cross-links (within the same level-4 artifact set):
- Rule 1.1 — Approved words (the dictionary you default to)
- Rule 1.2 — Part of speech
- Rule 1.3 — Approved meanings
- Rule 1.10 — No slang / jargon
- Rule 1.11 — One term per concept
- Rule 1.12 — Technical verbs allowed
- Rule 1.13 — Do not use technical verbs as nouns
- Rule 1.14 — American English spelling

---

# Rule 1.5 — You Can Use Code-Domain Technical Nouns

**Rule statement:** You may use a word that is not in the approved dictionary if it names
a precise software-development concept that fits one of the **19 code-domain categories**
below. Such a word is a *code-domain technical noun*. Use it only as a noun (or noun
modifier).

**Why it exists:** The approved dictionary cannot list every domain term (there are too
many, and every project uses different ones). Rule 1.5 is the gateway that lets
domain-specific vocabulary into STE-Code documentation without breaking the controlled
terminology.

**Requirements:**
- Register every code-domain technical noun you use in the **project glossary** (term,
  category, approved meaning, example sentence). Unregistered made-up names are not
  permitted (Rule 1.6 forbids them).
- Use an approved word whenever one exists. Use a technical noun only when no approved
  word names the concept.
- Categories are examples, not a closed list.

## The 19 code-domain categories (with example terms)

1. **Code components, modules, libraries** — class, controller, helper, hook, middleware,
   mixin, module, package, plugin, provider, repository, service, utility
2. **Computing devices and components** — CPU, disk, GPU, keyboard, laptop, memory,
   monitor, mouse, printer, screen, server, smartphone, tablet, terminal
3. **Development tools, environments, support equipment** — CLI, compiler, debugger,
   Docker, editor, IDE, Git, Jest, linter, loader, Prettier, terminal, test runner,
   TypeScript, webpack
4. **Data structures, types, formats** — array, boolean, buffer, CSV, enum, hash map,
   integer, JSON, linked list, object, queue, stack, string, struct, tree, tuple, XML, YAML
5. **Infrastructure, deployment, platforms** — AWS, CI/CD, container, deployment, Heroku,
   Kubernetes, load balancer, Node.js, pipeline, pod, production, staging, Vercel
6. **Systems, subsystems, architectural components** — API gateway, authentication layer,
   caching layer, client, database layer, message broker, microservice, proxy, rate
   limiter, REST API, routing layer, server, WebSocket
7. **Mathematical, algorithmic, scientific terms** — Big O notation, binary search,
   coefficient, complexity, exponent, hash function, iteration, logarithm, matrix,
   recursion, regex, sorting algorithm, time complexity, traversal
8. **Interface elements and navigation** — button, checkbox, dialog, dropdown, footer,
   header, menu, modal, navigation bar, radio button, scrollbar, sidebar, tab, text field,
   toggle, tooltip
9. **Numbers, units, time** — byte, GB, Hz, hour (h), KB, MB, ms, minute, ns, second (s), TB
10. **Quoted text** — texts you cannot change: error messages, code snippets, UI labels,
    log output. Example: `Cannot read properties of undefined`, `ENOENT: no such file`,
    `Submit` button, `404 Not Found`, `connection refused`
11. **Professional roles, teams, orgs** — administrator, backend developer, contributor,
    DevOps engineer, frontend developer, Google, maintainer, Microsoft, product owner,
    QA engineer, reviewer, scrum master, user
12. **Official documents, API references, standards** — API reference, changelog, code of
    conduct, contributing guide, diagram, figure, Getting Started guide, HTTP spec, note,
    paragraph, README, release notes, RFC, section, table, warning
13. **Runtime environments and operational conditions** — development, environment
    variable, garbage collection, heap, hot reload, live reload, memory leak, production,
    sandbox, stack trace, staging, test, thread, timeout, virtual machine
14. **Colors** — black, blue, cyan, gray, green, magenta, orange, red, white, yellow.
    Colors are adjectives but count as technical nouns here. Comparative/superlative forms
    (blacker, reddest) are forbidden.
15. **Defects, errors, faults** — assertion failure, bug, crash, deadlock, defect,
    exception, hang, infinite loop, memory leak, null pointer, race condition, regression,
    stack overflow, timeout, type error
16. **Computer science, ICT** — AI, algorithm, authentication, authorization, blockchain,
    containerization, cryptography, database, encoding, encryption, firewall, hashing,
    internet, machine learning, metadata, neural network, protocol, query, sandbox,
    schema, token, virtualization
17. **Legal and licensing** — Apache 2.0, BSD license, compliance, copyright, GPL, license,
    MIT license, open source, proprietary, terms of service, third-party, trademark,
    warranty
18. **Database and storage** — connection pool, cursor, foreign key, index, migration,
    NoSQL, ORM, PostgreSQL, primary key, query, Redis, relation, row, schema, seed, SQL,
    SQLite, stored procedure, table, transaction, view
19. **Network and protocol** — DNS, endpoint, HTTP, HTTPS, IP address, localhost,
    middleware, packet, port, request, response, route, socket, SSH, TCP, TLS, UDP, URL,
    VPN, WebSocket

## Application by documentation type (which categories to reach for)

- **README:** categories 1 (components), 3 (tools), 5 (infra), 17 (legal).
- **API docs:** categories 6 (systems), 18 (database), 19 (network).
- **Docstrings / comments:** categories 4 (types), 7 (algorithms), 15 (defects).
- **Commit messages:** categories 1 (components), 15 (defects), 18 (database).
- **Error messages:** categories 13 (runtime), 15 (defects), 19 (network).
- **Test specs:** categories 1 (components), 4 (types), 15 (defects).

## Grammar notes for technical nouns

- **Articles:** "the" for a specific instance, "a/an" for indefinite, none for plural
  general reference.
- **As modifiers:** a technical noun may modify another to form a compound (e.g.
  `Redis cache server`). Both parts must fit a recognized category.
- **Possessive ('s):** allowed only for category 11 (roles, orgs). Use "of" or
  noun-modifier for others: "the configuration of the Docker container", NOT "the Docker
  container's configuration".
- **Pluralization:** standard rules; acronyms take a lowercase "s" without apostrophe:
  "two APIs", "three SQL queries" (never "API's").
- **Capitalization:** proper nouns (language, company, product names) keep original case;
  common technical nouns are lowercase unless sentence-initial.

## Minimal examples

> Non-STE: The developer used the thing to get data from the storage layer and put it on the screen.
> STE: The frontend developer used the API client to get data from the database and show it on the UI.

> Non-STE: The endpoint leverages the middleware to authenticate the request and then kicks off a background job to crunch the data.
> STE: The endpoint uses the authentication middleware to check the request. The endpoint then starts a background job to process the data.

---

# Rule 1.6 — Use a Non-Approved Word Only as a Code-Domain Technical Noun

**Rule statement:** A word that is not approved in the controlled terminology may appear
only when it is a code-domain technical noun or part of a compound code-domain technical
noun. If it is neither approved (Rule 1.1) nor a technical noun (Rule 1.5), it is
forbidden.

**Why it exists:** Together with Rule 1.5, this forms a gate. An unapproved word must
belong to one of the 19 categories to be legal. Rule 1.5 defines *what qualifies*;
Rule 1.6 enforces *that only qualifying words pass*.

## The three-test decision gate

An unapproved word may stay ONLY if it clears all three tests. Fail any one → replace
with the approved alternative or restructure.

**Test 1 — Is the word unapproved?** Approved words skip this gate. Only unapproved
words enter. (e.g. "function" is approved → not tested; "handler" is unapproved → tested.)

**Test 2 — Is it a technical noun, or part of a compound technical noun?** It must be a
standalone noun in the 19 categories, or embedded in a compound that fits a category.
- "handler" alone → fails (not a recognized technical noun).
- "event handler" → passes (design-pattern term, category 1).
- "main" alone → fails (general adjective).
- "main branch" → passes (Git term, category 5).

**Test 3 — Is it used as a noun in the sentence?** Even a word that passes Test 2 must
function as a noun. If it is a verb/adjective/adverb, it fails (enforced by Rule 1.7).
- "The event handler processes the request." → noun → passes.
- "This class handlers the request." → "handlers" is a verb → fails. Use "processes" or
  "The request handler processes the request."

## Worked trace

> Non-STE: The main config loader backups the data through the handler pipeline.
> STE: The primary config loader makes an auxiliary copy of the data through the processing pipeline.

| Phrase | T1 unapproved? | T2 technical noun? | T3 noun use? | Result |
|---|---|---|---|---|
| main config loader | yes | "main" is a general adjective | — | "main" → "primary" |
| backups | yes | "backup" as verb is not a noun | verb | "makes an auxiliary copy" |
| handler pipeline | yes | not a recognized compound | noun but fails T2 | "processing pipeline" |

## Compound technical noun checklist

A compound counts as a technical noun only if ALL are true:
1. The words combine to name one concept the domain recognizes.
2. The compound fits one of the 19 categories.
3. Replacing the unapproved word with its approved alternative changes the recognized
   name and causes confusion.

Swap test: if you can replace the unapproved word with its approved alternative and the
term still names the same concept, it is NOT a technical noun → make the replacement. If
the swap produces a name no one in the domain would recognize, the compound IS a
technical noun and the unapproved word is permitted inside it.

## Distinction: technical noun vs. descriptive adjective

Criterion: does the compound appear in the official docs of the framework, language, or
standard? If yes → technical noun (permitted). If no → descriptive prose (replace).

- ✅ "Check out the main branch before you merge." (Git convention)
- ❌ "The main configuration has the latest values." → "primary configuration"
- ✅ "The base case returns the single-element array." (algorithmic term)
- ❌ "The base configuration is loaded first." → "primary configuration"
- ✅ "The event handler processes each request." (design-pattern term)
- ❌ "The handler processes each request." → "function"

## Dictionary reference (controlled-terminology entries)

- **BASE (n) — UNAPPROVED.** Alternatives: BOTTOM (surface/stack), ROOT (filesystem top).
  Permitted in compounds: "base case" (cat 7), "base class" (cat 1), "base URL" (cat 8).
- **MAIN (adj) — UNAPPROVED.** Alternative: PRIMARY. Permitted in "main branch" (cat 5)
  and "main function"/`main()` (cat 1, entry-point).
- **HANDLER (n) — UNAPPROVED.** Alternative: FUNCTION. Permitted in "event handler",
  "request handler" (cat 1).
- **BACKUP (n, v) — UNAPPROVED.** Alternatives: AUXILIARY (adj), "makes an auxiliary copy"
  (verb). Permitted in "backup file", `backup_logs` (cat 18), `/api/v1/backup` (cat 19).
- **BOTTOM (n), FUNCTION (n), PRIMARY (adj), AUXILIARY (adj), ROOT (n) — APPROVED.**

## Minimal examples

> Non-STE: The base setup leverages Express for the main API and MongoDB for the database backend. The handler backs up the data every night.
> STE: The primary setup uses Express for the main API and MongoDB for the database backend. The function makes an auxiliary copy of the data each night.

> Non-STE: POST /api/v1/backup — Authenticates the user and backups the records.
> STE: POST /api/v1/backup — Checks the user and makes an auxiliary copy of the records.

---

# Rule 1.7 — Do Not Use Code-Domain Technical Nouns as Verbs

**Rule statement:** Use a code-domain technical noun only as a noun (or as an adjective
inside another technical noun). Do NOT use it as a verb.

**Why it exists:** Verbing a noun loses its precise technical meaning. "Database" is a
specific storage system with ACID properties, schemas, queries. "To database" is unclear
— does it mean store, index, query, or replicate? The reader must guess.

**Core repair pattern:** replace the noun-verb with an approved verb + the noun in a
prepositional phrase. The preposition depends on the relationship:

| Noun-verb (wrong) | STE repair | Verb | Prep |
|---|---|---|---|
| Cache the data | Put the data in the cache | put | in |
| Queue the job | Add the job to the queue | add | to |
| Buffer the output | Write the output to a buffer | write | to |
| Socket the connection | Send the connection through a socket | send | through |
| Database the records | Store the records in the database | store | in |
| Docker the app | Package the app in a container | package | in |
| Git the changes | Commit the changes | commit | (none) |
| JSON the response | Encode the response as JSON | encode | as |

**Double-category exception:** some words are cataloged as BOTH a technical noun (Rule
1.5) and a technical verb (Rule 1.12). You may use them as verbs only in their approved
verb sense, and only if your project glossary lists the verb form. If the glossary lists
the word as a noun only, obey Rule 1.7.

| Word | Noun (Rule 1.5) | Verb (Rule 1.12) |
|---|---|---|
| cache | "The cache stores responses." (cat 16) | "Cache the responses." (cat 2c) |
| log | "Write a log entry." (cat 18) | "Log the error." (cat 2c) |
| queue | "Add the job to the queue." (cat 4) | "Queue the job for processing." (cat 3a) |
| filter | "Apply a filter." (cat 4/16) | "Filter the results." (cat 2b) |
| sort | "Use a merge sort." (cat 7) | "Sort the list by name." (cat 2b) |
| map | "Use a hash map." (cat 4) | "Map the function over the list." (cat 3a) |

RULE: decide the part of speech in your glossary. Do not mix noun and verb uses of the
same word in one paragraph without clear context. When the verb form implies the noun
(e.g. "Filter the results and sort the list"), do not also restate the noun.

## Paradigm-specific noun/verb tables (use the right construction)

**OOP:** interface → "Add an interface between …"; class → "Make a class for …";
subclass → "Make a subclass of …"; singleton → "Make the logger a singleton";
factory → "Use a factory to make …"; observer → "Add an observer for …";
dependency → "Inject the service as a dependency into …".

**Functional:** monad → "Wrap … in a monad"; functor → "Map the function over the
functor"; combinator → "Combine the parsers with a combinator"; closure → "Capture … in a
closure"; thunk → "Wrap … in a thunk"; lambda → "Write the function as a lambda".

**Procedural:** buffer → "Write … to a buffer"; pointer → "Get a pointer to …";
malloc → "Allocate … with `malloc`"; struct → "Put … in a struct"; heap → "Allocate … on
the heap"; stack → "Put … on the stack".

**Declarative:** table → "Store … in a table"; schema → "Apply a schema to …";
index → "Make an index on …"; YAML → "Write … in YAML"; pod → "Put … in a pod";
secret → "Store … as a secret".

**Systems:** mutex → "Lock the mutex before …"; semaphore → "Use a semaphore to control
access to …"; register → "Write to the register at …"; interrupt → "Send an interrupt to
…"; DMA → "Transfer … with DMA"; MMU → "Map … through the MMU".

## Edge cases

- **Brand / tool / framework names as verbs:** never. "Docker the app" → "Containerize the
  app"; "Google the error" → "Search for the error with Google"; "Kubernetes the
  services" → "Deploy the services with Kubernetes".
- **Framework names that are also English verbs:** keep as nouns. "Express the middleware"
  → "Write the middleware with Express"; "React to state changes" → "Respond to the state
  changes with React".
- **Code keywords used as verbs:** `class`, `import`, `return`, `yield` are nouns when you
  refer to them; quote them, use approved verbs: "make a `class`", "add the `import`
  statements".
- **Generated symbol names** (e.g. `toJson()`, `UserBuilder`): exempt from the rule, but
  refer to them as nouns in prose. Do not verb them.
- **Multi-word technical nouns:** keep the full phrase; do not drop a word to make a verb.
  "Load balance the requests" → "Distribute the requests with a load balancer";
  "feature flag the endpoint" → "Put the endpoint behind a feature flag";
  "circuit break the service" → "Apply a circuit breaker to the service".

## Minimal examples

> Non-STE: You must Docker the application, then Git the changes, and finally Webpack the bundle.
> STE: You must containerize the application, then commit the changes, and then bundle the code with Webpack.

> Non-STE: Cache the API responses to improve performance.
> STE: Store the API responses in the cache to improve performance.

---

# Rule 1.8 — Use the Standard, Approved Code-Domain Technical Noun

**Rule statement:** When more than one name exists for the same concept, use the name
that is approved in your project, company, industry, or subject field. Do not invent your
own name for an item that already has an established name. (Rule 1.5 tells you *whether* a
word is a technical noun; Rule 1.8 tells you *which* one to pick.)

**Why it exists:** Documentation must be traceable to the codebase. A reader who searches
for "user retrieval endpoint" will not find `GET /users/:id`. Use the exact approved name
so readers can locate the element in the source tree.

## Authority hierarchy for name selection

When several names compete, pick the most authoritative:

1. **Source code** — class/function/file/variable/type names (e.g. `UserRepository`).
2. **Language specification** — keyword, std-lib, built-in type names (e.g. `malloc`,
   `struct`, `pointer`, `Option`).
3. **Framework/library docs** — API, component, hook, config-key names (e.g. `useEffect`,
   `DATABASE_URL`).
4. **Project glossary** — project-specific terms registered under Rule 1.5.
5. **Industry standard** — design-pattern, protocol, algorithm, architecture names
   (e.g. Observer pattern, HTTPS, binary search).
6. **Company documentation** — internal system/service/team names.

Conflict rule: when source code differs from industry standard (e.g. class `DataStore`
but industry "Repository"), use the codebase name for the code element and the industry
name for the conceptual explanation — never mix levels for the same concept in one doc.

## Paradigm-specific: avoid → use

- **OOP:** "user manager" → `UserRepository`; "maker pattern" → Factory pattern; "wiring"
  → Dependency injection; "display pattern" → MVC; "data layer" → `IRepository<T>`.
- **Functional:** "maybe-type" → `Option`/`Maybe`; "IO box" → `IO` monad; "chaining" →
  Function composition; "destructuring" → Pattern matching; "frozen data" → Immutable
  data; "callback function" → Higher-order function.
- **Procedural:** "heap allocation" → `malloc`; "record/compound type" → `struct`;
  "memory reference" → `pointer`; "light thread" → `goroutine` (Go); "console/screen" →
  `stdout`; "shell vars" → Environment variables.
- **Declarative:** "compute instance" → `aws_instance`; "pod config" → `Pod`/`PodSpec`;
  "data fetch" → `SELECT` statement; "all-or-nothing unit" → `TRANSACTION`; "export block"
  → `output`; "project space" → `Namespace`.
- **Systems:** "move operation" → `move` semantics; "reference pass" → `borrow`; "free
  store" → `heap`; "call stack" → `stack`; "thread lock" → `Mutex`; "ISR function" → `ISR`.

## Grammar / formatting notes

- **As a modifier:** the approved noun stays the modifier. "The `UserRepository` interface"
  (correct) vs. "the user storage interface" (wrong).
- **Capitalization:** keep the source form. `userService` and `findById` (not
  `UserService`/`FindById`).
- **Definite article:** use "the" for a specific entity ("The `UserController` handles the
  request"); omit it for the general concept ("`UserController` is a common pattern").
- **In code vs prose:** the name is identical; only formatting (code block / inline code)
  changes.

## Edge cases

- **Codebase uses a non-standard name:** use the codebase name (`DataStore`) and mention
  the industry name in parentheses for comprehension: "The `DataStore` class (a Repository
  pattern implementation) …".
- **Two competing standards** (callback/handler/listener; hash map/dictionary/associative
  array): pick one per Rule 1.11, register it, prefer the language-ecosystem term (Java
  "map", Python "dictionary").
- **Acronyms:** use the approved acronym; define at first use unless the audience knows
  it. After definition, use only the acronym (do not alternate full form/acronym).
- **Framework renames a concept** (Django "view" vs others "component"/"controller"): in
  framework-specific docs use the framework's name; in general docs use the common term and
  note the variant.
- **Name changes during refactor:** use the target name; show the old name only as
  quoted, DEPRECATED text.
- **Package name varies by registry** (`python-dotenv` on PyPI vs `dotenv` on npm): in
  ecosystem docs use that registry's name; give the registry-qualified install command.

## Minimal examples

> Non-STE: The account controller manages login and user profile operations.
> STE: The `AccountController` manages authentication and user profile operations.

> Non-STE: The service uses secure web communication to send data between the client and the server.
> STE: The service uses HTTPS to send data between the client and the server.

---

# Rule 1.9 — Select a Short, Easy-to-Understand Technical Noun

**Rule statement:** When you must choose a code-domain technical noun and no approved name
exists, select one that is short (not more than three words) and easy to understand. Do
not use long descriptive phrases when a shorter term is sufficient.

**Why it exists:** Long noun phrases raise cognitive load — the reader parses a chain of
modifiers before reaching the head noun. Context permits brevity: the code, an API spec, a
diagram, or a preceding definition already identifies the item, so the short term is
enough.

**Context sources that permit the short form:**
- Code references (line number, function/class/file name)
- Diagrams / figures that label components
- A preceding definition ("the authentication service, called AuthService")
- An API spec that fully describes a type
- A following code snippet

When no context source is available, add one or two **disambiguating** adjectives only.
Remove "noise adjectives" (e.g. "the secure HTTPS protocol" — HTTPS is secure by
definition; "the configurable settings object" — all settings are configurable).

## Three-word limit — rationale and exceptions

The limit reflects working-memory capacity. Exceptions (keep the longer term; do not
invent a shorter one the community does not use):
1. **Established technical terms** — "abstract syntax tree", "single sign-on provider",
   "continuous integration pipeline".
2. **Framework/tool proper nouns** — "GitHub Actions workflow", "Amazon Web Services
   Lambda". Use given; abbreviate only if the abbreviation is itself a recognized noun
   (e.g. "AWS Lambda").
3. **Fully qualified type names** — `com.example.module.SubComponent`; use the short name
   after first reference.
4. **Shortening causes ambiguity** — keep the longer phrase.

## Long phrase → short form reference

| Long phrase | Short STE form | Context that permits it |
|---|---|---|
| asynchronous JavaScript XML HTTP request wrapper utility function | fetch utility | line number + snippet |
| serialized JSON payload from the remote API endpoint | JSON data from the API endpoint | field name + type |
| user account profile information data transfer object | `UserProfileDTO` | parameter already named |
| relational database management system server instance | database | port + "primary" |
| multi-platform containerized microservice orchestration layer | Kubernetes cluster | diagram / README title |
| dependency injection inversion of control container | DI container | preceding definition of DI |
| mutual exclusion lock primitive with timeout-bounded acquisition | mutex | class name in code |
| configuration, settings, and options parameters object | `Config` object | object is named `Config` |
| dynamically allocated resizable contiguous memory region utility | dynamic array | type is declared |
| horizontal pod autoscaling controller with CPU threshold | `HorizontalPodAutoscaler` resource | YAML `kind` field |

## Abbreviations and acronyms

- **Universal** (use on first reference, expansion optional): API, JSON, SQL, HTML, HTTP,
  URL, DNS, TCP, TLS, CPU, RAM, SSD.
- **Domain-specific** (expand on first use for a general audience): JWT, CORS, ORM, SPA,
  SSR.
- **Project-specific** (expand on first use in every doc): only after definition.

Do NOT invent abbreviations to satisfy this rule ("TransSec" for "Transport Layer
Security" fails Rule 1.8 — use the recognized short form "TLS").

## Edge cases

- **Short term less well-known than long** (e.g. "AST"): expand on first use — "abstract
  syntax tree (AST)" — then use "AST". If the audience knows it (compiler docs), use it
  directly. Ease test: would a 1-year-experience developer in this domain understand it?
- **Framework name is also a short word** (React, Go, Rust): use "the React framework" /
  "the Go language" on first use to disambiguate; bare name is fine afterward. Do not
  invent abbreviations.
- **Codebase uses long names internally** (`AbstractUserAuthenticationProviderFactoryBean`):
  Rule 1.8 wins for the name itself — use it as given. Rule 1.9 applies to surrounding
  prose: "the factory bean". Do not rename in code or references.
- **Shortening creates a homonym** ("pool" = thread/connection/object): keep the
  two-word form ("connection pool", "thread pool") unless the doc discusses exactly one
  kind throughout.
- **Generated docs** (JSDoc/Sphinx/godoc): the auto-generated portion is exempt, but any
  human-written `@description` / docstring summary must obey the rule.

## Minimal examples

> Non-STE: Remove the four stainless steel pan head machine screws (10) that attach the metallic machined flange (15) to the front housing cover (20).
> STE: Remove the four screws (10) that attach the flange (15) to the cover (20).

> Non-STE: The request body must contain a JSON object with a required string field named "emailAddress" that must match the standard internet electronic mail address format as defined by RFC 5322 …
> STE: The request body is a JSON object with these fields: `emailAddress` (string, required) — a valid email address; `displayName` (string, optional, max 100 characters); `subscribeToNewsletter` (boolean, optional, default: `false`).

---

# Quick reference — the five rules at a glance

| Rule | One-line constraint | Key mechanism |
|---|---|---|
| 1.5 | You may use a non-dictionary word if it names a code concept in 1 of 19 categories. | 19 categories; glossary registration required. |
| 1.6 | A non-approved word is legal only as a technical noun (or inside one). | 3-test gate: unapproved? → noun category? → used as noun? |
| 1.7 | Do not use a technical noun as a verb. | Approved verb + noun in prepositional phrase; double-category exception. |
| 1.8 | When names compete, use the approved/standard one. | Authority hierarchy (source code > spec > framework > glossary > industry > company). |
| 1.9 | Pick the short, clear form; context permits brevity. | ≤3 words; expand acronyms on first use; no invented abbreviations. |

**The only two kinds of words in STE-Code documentation:** approved STE-Code words (Rule
1.1) for common vocabulary, and code-domain technical nouns (Rule 1.5) for domain-specific
concepts. There is no third category. Rule 1.6 forbids everything else; Rules 1.7–1.9
govern how you use the technical nouns you keep.
