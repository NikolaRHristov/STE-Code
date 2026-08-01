# Level 3 — Words, Part 2: Code-Domain Technical Nouns (Rules 1.5–1.9)

Scope: the technical-noun block of STE-Code Section 1. Five rules decide which
words outside the approved dictionary may appear in code documentation, how they
must be spelled, shaped, and used, and which part of speech they may take.

Reading order: 1.5 defines what a code-domain technical noun is → 1.6 is the gate
that admits unapproved words → 1.7 forbids using those nouns as verbs → 1.8 picks
the standard name among competing candidates → 1.9 keeps the chosen name short.

Vocabulary model in one line: every word in STE-Code documentation is either an
approved dictionary word (Rule 1.1) or a code-domain technical noun (Rule 1.5) or
a technical verb (Rule 1.12). There is no fourth category.

---

## Rule 1.5 — You can use words that you can include in a code-domain technical noun category

**Rule.** You can use words that you can include in a code-domain technical noun
category.

A code-domain technical noun names a specified concept in software development
and is applicable to a subject field. The controlled terminology does not list
them all — there are too many, and each project uses different ones. Record the
ones your project uses in the project glossary or terminology database.

Technical nouns are permitted in procedural and descriptive writing when they fit
one or more of the nineteen categories below.

### The nineteen categories

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
| 10 | Quoted text (unchangeable text) | `Cannot read properties of undefined`, `ENOENT: no such file or directory`, `Submit` button, `404 Not Found`, `connection refused` |
| 11 | Professional roles, teams, and organizations | administrator, backend developer, contributor, DevOps engineer, frontend developer, Google, maintainer, Microsoft, product owner, QA engineer, reviewer, scrum master, user |
| 12 | Official documents, API references, and standards | API reference, changelog, code of conduct, contributing guide, diagram, figure, Getting Started guide, HTTP specification, note, paragraph, README, release notes, RFC, section, table, warning |
| 13 | Runtime environments and operational conditions | development, environment variable, garbage collection, heap, hot reload, live reload, memory leak, production, sandbox, stack trace, staging, test, thread, timeout, virtual machine |
| 14 | Colors | black, blue, cyan, gray, green, magenta, orange, red, white, yellow |
| 15 | Defects, errors, and fault terminology | assertion failure, bug, crash, deadlock, defect, exception, hang, infinite loop, memory leak, null pointer, race condition, regression, stack overflow, timeout, type error |
| 16 | Computer science, information, and communication technology | AI, algorithm, authentication, authorization, blockchain, containerization, cryptography, database, encoding, encryption, firewall, hashing, internet, machine learning, metadata, neural network, protocol, query, sandbox, schema, token, virtualization |
| 17 | Legal and licensing terms | Apache 2.0, BSD license, compliance, copyright, GPL, license, MIT license, open source, proprietary, terms of service, third-party, trademark, warranty |
| 18 | Database and storage terminology | connection pool, cursor, foreign key, index, migration, NoSQL, ORM, PostgreSQL, primary key, query, Redis, relation, row, schema, seed, SQL, SQLite, stored procedure, table, transaction, view |
| 19 | Network and protocol terminology | DNS, endpoint, HTTP, HTTPS, IP address, localhost, middleware, packet, port, request, response, route, socket, SSH, TCP, TLS, UDP, URL, VPN, WebSocket |

Colors (category 14) are adjectives, but STE-Code classifies them as code-domain
technical nouns. Comparative and superlative color forms (blacker, the reddest)
are not permitted.

The listed terms are examples only. Rule 1.5 does not give a complete list.

### Category selection by documentation type

| Documentation type | Typical categories | Example |
|---|---|---|
| README | 1, 3, 5, 17 | "This package provides a middleware for Express." |
| API documentation | 4, 6, 18, 19 | "The `GET /users/:id` route returns a JSON object with a user struct." |
| Docstrings and comments | 4, 7, 15 | "Traverse the binary search tree in-order and return a sorted array." |
| Commit messages | 1, 15, 18 | "Fix race condition in the connection pool that caused a deadlock on PostgreSQL." |
| Error messages | 9, 13, 15, 19 | "Connection refused: the TCP socket on port 5432 timed out after 30 seconds." |
| Test specifications | 1, 4, 15 | "The test calls `parseConfig` with a null pointer and checks for an assertion failure." |

### Relation to the neighbouring rules

- Rule 1.1 requires approved words for common vocabulary. Rule 1.5 is the
  complement: it permits words outside the dictionary when they name a technical
  concept. Use an approved word whenever one exists.
- Rule 1.6 forbids every unapproved word that Rule 1.5 does not admit. Read the
  two rules as one gate.

### Glossary registration is mandatory

Before you use a code-domain technical noun, add it to the project glossary. Each
entry states: the noun term; its STE-Code category or categories; the approved
meaning in the project context; one correct example sentence. A project without a
glossary drifts into ambiguity and breaks Rule 1.11 (one term per concept).

### Paradigm notes

| Paradigm | Lean on categories | Correct | Incorrect |
|---|---|---|---|
| Object-oriented (Java, C++, C#, Python) | 1, 4, 6, 16 | "The `UserRepository` class extends the `BaseRepository` abstract class and implements the `IAuditable` interface." | "The repo leverages the base to retrieve user data." (use "use"; use "repository") |
| Functional (Haskell, Elixir, Clojure, Rust) | 4, 7, 16 | "The function returns an `Option` monad. Use pattern matching to extract the value." | "The combinator stuff chains stuff together." (name the terms: parser combinator, function, pipeline) |
| Procedural (C, Go, Bash) | 4, 13, 19 | "The Go goroutine reads from the channel. The mutex prevents a race condition." | "The script fires off a subprocess to crunch the numbers." (use "starts", "process") |
| Declarative (SQL, Terraform, Kubernetes) | 5, 10, 12, 18 | "The `SELECT` statement uses an `INNER JOIN` on the `users` and `orders` tables." | "K8s spins up a bunch of pods inside the thing." (use "Kubernetes", "starts", "namespace") |
| Systems (Rust ownership, C memory) | 4, 13, 15, 16 | "The borrow checker prevents dangling pointers at compile time." | "Rust's thingy stops you from shooting yourself in the foot." (idiom forbidden by P10) |

```java
/**
 * The UserRepository class extends the BaseRepository abstract class
 * and implements the IAuditable interface.
 * Use the findById method to get a user struct from the database layer.
 */
public class UserRepository extends BaseRepository implements IAuditable {
    public User findById(Long id) { /* ... */ }
}
```

```rust
// The Rust compiler enforces the ownership rules.
// The borrow checker prevents dangling pointers at compile time.
fn parse_input(buffer: Vec<u8>) -> Result<String, Utf8Error> {
    let text = String::from_utf8(buffer)?;  // heap allocation (category 13)
    Ok(text)
}
```

### Edge cases

1. **Framework names that are also common words** (React, Vue, Swift, Go, Rust,
   Elm, Next, Nest). The framework name is a technical noun (category 3 or 5) and
   does not follow the dictionary meaning. Capitalize it, or use the full term
   ("the Swift language", "the Rust compiler"), so it cannot be read as the
   approved verb.
2. **Code keywords in documentation** (`if`, `for`, `return`, `class`, `async`).
   Inside backticks they are quoted text (category 10) and exempt. In prose they
   must follow the approved meaning. Write "If the request fails, return
   `500 Internal Server Error`." — not a bare `500`.
3. **Abbreviations and acronyms** (API, JSON, SQL, HTML, HTTP, TCP, DNS, URL) are
   technical nouns in categories 16, 18, or 19. Expand each at first use unless
   the audience universally knows it: "the application programming interface
   (API) uses Hypertext Transfer Protocol Secure (HTTPS)".
4. **Generated code and generated documentation** (OpenAPI specs, protobuf stubs,
   migration files, JSDoc or Sphinx output) are exempt, because a machine
   produces them. Every human-written comment or annotation inside them is not.
5. **Project-specific internal names** (`PhoenixCache`, "Hammerhead subsystem")
   are technical nouns under category 1 or 6 **only when registered in the
   project glossary**. Without registration they are unapproved words and break
   Rule 1.6.
6. **Numbers as technical nouns.** Fixed named values — version numbers
   (`Node.js 18`), status codes (`404`), port numbers (`port 5432`) — are
   category 9 nouns or quoted text and must appear verbatim. Do not write "the
   default db port" or "a not found error".

### Grammar of technical nouns

- **Articles.** Same as approved nouns: "the" for a specific instance, "a"/"an"
  for an indefinite one, no article for plural general reference — "Kubernetes
  pods run in a namespace."
- **As modifiers.** A technical noun may modify another to form a compound; both
  parts must belong to a recognized category. "The Redis cache server stores the
  session data." Not: "The thing layer processes the stuff queue."
- **Possessive.** Permitted only for category 11 (roles, organizations):
  "the user's session data". Use an "of" construction elsewhere: "the
  configuration of the Docker container" — not "the Docker container's
  configuration".
- **Plurals.** Standard English rules; acronyms add a lowercase "s" with no
  apostrophe. "two APIs and three SQL queries" — not "two API's".
- **Capitalization.** Proper-noun technical nouns keep published casing
  (`TypeScript`); common ones stay lowercase unless sentence-initial
  (controller, endpoint, middleware).

### Worked pair

> **Non-STE:** The developer used the thing to get data from the storage layer and put it on the screen.
>
> **STE:** The frontend developer used the API client to get data from the database and show it on the UI.

frontend developer (11), API client (16), database (18), UI (8). "Thing" names
nothing; "screen" is category 2 hardware, not the interface element.

> **Non-STE:** The endpoint leverages the middleware to authenticate the request and then kicks off a background job to crunch the data.
>
> **STE:** The endpoint uses the authentication middleware to check the request. The endpoint then starts a background job to process the data.

> **Non-STE:** First, snag the repo and then cd into it. After that, fire up the dev server.
>
> **STE:** First, clone the repository. Then, change to the repository directory. After that, start the development server.

> **Non-STE:** Bumped deps and fixed the wonky timeout thing that was breaking prod.
>
> **STE:** Update dependencies. Fix a timeout defect in the connection pool that caused a crash in production.

### Rule 1.5 cross-references

Rule 1.1 (approved words) · Rule 1.2 (part of speech) · Rule 1.3 (approved
meanings) · Rule 1.4 (verb and adjective forms) · Rule 1.6 (unapproved words) ·
Rule 1.7 (nouns not as verbs) · Rule 1.8 (standard names) · Rule 1.9 (short
names) · Rule 1.11 (one term per concept) · Rule 1.12 (technical verbs).

---

## Rule 1.6 — Use an unapproved word only when it is a code-domain technical noun, or part of one

**Rule.** Use a word that is not approved in the controlled terminology only when
it is a code-domain technical noun or part of a code-domain technical noun.

Some words are listed as unapproved. If such a word fits an applicable technical
noun category, it may be used in that noun sense — and only in that sense.

### The three-test gate

An unapproved word may stay only if it clears all three tests.

| Test | Question | Fails | Passes |
|---|---|---|---|
| 1 | Is the word unapproved? | "function" (approved — Rule 1.1 handles it) | "handler" enters the gate |
| 2 | Is it a technical noun, or inside a compound technical noun (Rule 1.5)? | "handler" alone; "main" alone | "event handler" (cat. 1); "main branch" (cat. 5) |
| 3 | Is it used as a noun in the sentence? | "This class handlers the request." | "The event handler processes the request." |

Failing any test means: replace with the approved alternative, or restructure.

### Compound checklist

A compound counts as a code-domain technical noun only when all three hold:

1. The words together name one concept that the domain recognizes.
2. The compound fits one of the nineteen categories.
3. Swapping the unapproved word for its approved alternative changes the
   recognized name and causes confusion.

Swap test: if the approved alternative still names the same concept, it is not a
technical noun — make the replacement. If the swap produces a name nobody in the
domain would recognize, the compound is a technical noun and the unapproved word
stays inside it.

Authority for "recognized": the project glossary, the framework or language
documentation, or an industry standard (RFC, W3C, POSIX).

### Core pairs

> **Non-STE:** The handler processes each incoming event.
>
> **STE:** The function processes each incoming event.
>
> **STE:** The event handler processes each incoming event. *("Event handler" is category 1.)*

> **Non-STE:** The main configuration has the latest values.
>
> **STE:** The primary configuration has the latest values.
>
> **STE:** Merge the feature branch into the main branch. *("Main branch" is the Git term, category 5; "primary branch" is not.)*

> **Non-STE:** Make sure that the two connectors at the base of the chassis engage.
>
> **STE:** Make sure that the two connectors at the bottom of the chassis engage.
>
> "Base" stays inside "base case" (cat. 7), "base class" (cat. 1), "base URL" (cat. 8).

### Descriptive adjective or technical noun?

| Permitted (technical noun) | Replace (descriptive) |
|---|---|
| "Check out the main branch before you merge." | "The main configuration has the latest values." → primary |
| "The base case returns the single-element array." | "The base configuration is loaded first." → primary |
| "The event handler processes each request." | "The handler processes each request." → function |

Criterion: does the compound appear in the official documentation of the
framework, language, or standard? If yes, technical noun. If no, prose — replace.

### Category overlap

The same unapproved word can pass in different categories when its meaning
changes: "base" in "base case" (7), "base class" (1), "base URL" (8); "cache" in
"cache layer" (6), "cache invalidation" (16), "query cache" (18). Each names a
specific concept — not a general adjective or verb.

### Worked trace

> **Non-STE:** The main config loader backups the data through the handler pipeline.
>
> **STE:** The primary config loader makes an auxiliary copy of the data through the processing pipeline.

| Word / phrase | Unapproved? | Technical noun? | Used as noun? | Result |
|---|---|---|---|---|
| main config loader | yes | "main" is a general adjective here | — | "main" → "primary" |
| backups | yes | verb sense is not a technical noun | no, verb | → "makes an auxiliary copy" |
| handler pipeline | yes | not a recognized compound | yes, but fails Test 2 | → "processing pipeline" |

### Applied by documentation type

**README.**

> **Non-STE:** The base setup leverages Express for the main API and MongoDB for the database backend. The handler backs up the data every night.
>
> **STE:** The primary setup uses Express for the main API and MongoDB for the database backend. The function makes an auxiliary copy of the data each night.

Package names (`Express`, `MongoDB`, `react-router`) are technical nouns
(cat. 3, 18). Keep a package-name compound whole — never split the unapproved
word out of `react-router`.

**API documentation.** Paths and field names stay; verbs must be approved.

```yaml
/api/v1/backup:
  summary: Makes an auxiliary copy of the database. Returns a backup ID.
  responses:
    '200':
      description: The auxiliary copy was made. The event handler processed the request.
```

**Docstrings and comments.**

```python
def serve(req):
    """Processes the request and returns a response."""
    # base case: the event handler returns null when req is empty
    if not req:
        return None
    return build(req)
```

"Handles" → "processes"; "base case" stays (cat. 7); "handler" → "event handler".
In Go: "the base URL is null and the event handler runs longer than the timeout"
— not "times out".

**Commit messages.** Conventional prefixes are technical nouns; the description
obeys the gate.

```
feat: add an event handler for the auxiliary-copy endpoint and the primary config loader
fix: run the backup script before the primary migration
chore: update the main config loader settings   # glossary names the file "main config"
```

**Error messages.**

```
Error: primary config file not found. The event handler for auxiliary copies will stop.
Build failed: the primary config loader ran longer than the timeout. The auxiliary-copy handler did not start.
```

### Paradigm notes

- **Object-oriented.** Class and pattern names stay: `BaseService`, `MainFactory`.
  Verbs must be approved: "handlers" → "processes", "backups" → "makes auxiliary
  copies", "factories" → "makes". A pattern name is never a verb: "This class
  uses the Singleton pattern for the connection used by all callers."
- **Functional.** Type and monad names stay (`ReaderT`). Use "base monad" only if
  the library's own docs use it; otherwise "underlying monad". "Base case" is a
  permitted compound (cat. 7).
- **Procedural.** `main` as the entry-point function name and the Go `main`
  package are technical nouns and stay; "main goroutine" as a general adjective
  becomes "primary goroutine". Make a bare "handler" explicit: "file handler".
- **Declarative.** Table names (`backup_logs`) and resource kinds (`ConfigMap`,
  `Deployment`) stay; "backups" → "keeps auxiliary copies"; "base settings" →
  "primary settings".
- **Systems.** `unsafe` block, `raw pointer`, `dangling pointer` are technical
  nouns. As a descriptive adjective, "unsafe" is not approved: write "This
  approach is not safe because the buffer is shared." "Base allocation" →
  "primary allocation"; bare "handler" → "drop handler".

### Rule 1.6 edge cases

1. **Framework name that is also an unapproved word.** `pandas`, `Express`,
   `webpack` are technical nouns when they name the tool, with published
   capitalization. As general verbs they are unapproved: "use pandas to load the
   CSV into a data frame, then use Express to send the results as JSON".
2. **Code keyword that is also a general word.** Inside backticks it is quoted
   text (cat. 10). In prose its role decides: "The category of objects that
   `return` a value must not block the primary thread." ("class" as a general
   noun → "category"; "main" → "primary".)
3. **A compound that looks technical but is not recognized.** "The handler
   pipeline integrates with the backup orchestrator via the main dispatcher"
   contains three invented compounds → "The processing pipeline integrates with
   the auxiliary-copy service through the primary dispatcher."
4. **Auto-generated documentation.** Apply the gate to the source docstring or
   annotation, not the generated output: `/// <summary>Processes the
   auxiliary-copy operation for the primary controller.</summary>`
5. **Project and brand names.** `Homebrew` stays (cat. 3 or 11); the descriptive
   prose around it is still reviewed: "Use Homebrew to install the primary
   packages. Then use `webpack` to make the primary bundle."

### Terminology referenced by Rule 1.6

| Term | Status | Approved alternative | Permitted inside |
|---|---|---|---|
| BASE (n) | unapproved | BOTTOM (n) for a surface or stack position; ROOT (n) for a filesystem root | base case (7), base class (1), base URL (8) |
| MAIN (adj) | unapproved | PRIMARY (adj) | main branch (5), main function / `main()` (1) |
| HANDLER (n) | unapproved | FUNCTION (n) | event handler, request handler, file handler (1) |
| BACKUP (n, v) | unapproved | AUXILIARY (adj); "makes an auxiliary copy" for the verb | backup file, `backup_logs` (18), `/api/v1/backup` (19) |
| BOTTOM (n, adj) | approved | — | — |
| FUNCTION (n) | approved | — | — |
| PRIMARY (adj) | approved | — | — |
| AUXILIARY (adj) | approved | — | — |
| ROOT (n) | technical noun | top-level directory (5 or 13) | — |

Categories most used by this rule: 1 (event handler, base class, main function),
3 (Express, pandas, webpack), 5 (main branch, ConfigMap), 7 (base case), 8 (base
URL, Git root), 18 (backup file, config file), 19 (backup as a resource name).

### Rule 1.6 cross-references

Rule 1.1 · Rule 1.2 · Rule 1.5 · Rule 1.7 · Rule 1.8 · Rule 1.9 · Rule 1.11 ·
Rule 1.12.

---
