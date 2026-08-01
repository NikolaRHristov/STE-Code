# Level 1 — Technical Noun Categories (Rule 1.5)

This is the Rule 1.5 slice of STE-Code Level 1: the **code-domain technical noun
categories** — the "approved-word / synonym table" that lets you use precise
domain terms outside the approved-word dictionary.

Level 1 controls *which words you may use*. Every other level builds on it. This
file is the LLM-facing form of Rule 1.5 (one of the three word-gates in Section 1).
It is faithful to the standard: the nineteen categories and their example terms
are taken from the authoritative Rule 1.5 adaptation, not invented. All examples
stay inside the code domain.

## Rule 1.5 — what it permits

**Rule 1.5** You can use words that you can include in a code-domain technical
noun category.

A code-domain technical noun is a noun term that refers to a specified concept in
software development and is applicable to a subject field. The controlled
terminology does not include all code-domain technical nouns because there are
too many, and each project or subject field uses different technical nouns. You
can find many of these in your project glossary or terminology database.

STE-Code gives you a list of nineteen categories, with examples, to help you:
- Select code-domain technical nouns to put in your project glossary.
- Use code-domain technical nouns correctly.

You can use code-domain technical nouns in procedural and descriptive writing if
you can include them in one or more of these nineteen categories.

Rule 1.5 is the **gateway for all domain-specific vocabulary**. Without it, every
project noun (`repository`, `middleware`, `race condition`) would be forbidden and
documentation would be unusable. With it, a non-approved word is allowed *only*
when it names a precise concept in one of the nineteen categories below.

## The three-word gate (Rules 1.1, 1.5, 1.6)

Use an approved word whenever one exists. Use a code-domain technical noun only
when no approved word names the concept. These three rules form a gate with no
fourth category:

| Gate | Rule | Allows |
|------|------|--------|
| Approved word | 1.1 | A word listed in the controlled terminology (the dictionary). |
| Technical noun | 1.5 | A non-approved word that fits at least one of the 19 categories below **and** is registered in your glossary. |
| Technical verb | 1.12 | A verb in the technical-verb category (for example `build`, `deploy`, `test`, `lint`, `compile`, `debug`). |

Any word that passes **none** of these three gates is forbidden by Rule 1.6.

> Non-STE: The developer used the thing to get data from the storage layer and put it on the screen.
> STE: The frontend developer used the API client to get data from the database and show it on the UI.
> (`frontend developer` = category 11, `API client` = category 16, `database` = category 18, `UI` = category 8 — each names a precise concept; "thing", "storage layer", "screen" do not.)

## Glossary registration (required)

Before you use a code-domain technical noun in documentation, add it to the
project glossary or terminology database. The glossary entry must specify:
- The noun term.
- The STE-Code category (or categories) it belongs to.
- The approved meaning in the project context.
- An example sentence that uses the noun correctly.

A project without a glossary risks ambiguity: the same noun may mean different
things to different readers, which also violates Rule 1.11 (one term per concept).
Project-specific internal names (for example `PhoenixCache`, `Hammerhead subsystem`)
are permitted only after glossary registration; without it they are non-approved
words and violate Rule 1.6.

---

## The 19 code-domain technical noun categories

The terms under each category are **examples only** — Rule 1.5 does not give a
full list. A word belongs in a category if it names a precise software concept.
Register every project-specific noun in your glossary before using it. When a term
is a literal identifier, API name, or exact string from code (a class name,
function name, environment variable, or error message), show it in backticks —
for example `UserRepository`, `NODE_ENV`, `"404 Not Found"`.

### 1. Code components, modules, and libraries
Software parts, packages, and reusable units of code.
`class`, `controller`, `helper`, `hook`, `middleware`, `mixin`, `module`, `package`, `plugin`, `provider`, `repository`, `service`, `utility`

### 2. Computing devices and their components
Hardware, devices, and physical computing resources.
`CPU`, `disk`, `GPU`, `keyboard`, `laptop`, `memory`, `monitor`, `mouse`, `printer`, `screen`, `server`, `smartphone`, `tablet`, `terminal`

### 3. Development tools, environments, and support equipment
Development tools, IDEs, build systems, and testing frameworks.
`CLI`, `compiler`, `debugger`, `Docker`, `editor`, `IDE`, `Git`, `Jest`, `linter`, `loader`, `Prettier`, `terminal`, `test runner`, `TypeScript`, `webpack`

### 4. Data structures, types, and formats
Data representation, storage structures, and file formats.
`array`, `boolean`, `buffer`, `CSV`, `enum`, `hash map`, `integer`, `JSON`, `linked list`, `object`, `queue`, `stack`, `string`, `struct`, `tree`, `tuple`, `XML`, `YAML`

### 5. Infrastructure, deployment, and platforms
Hosting, deployment, containerization, and runtime platforms.
`AWS`, `CI/CD`, `container`, `deployment`, `Heroku`, `Kubernetes`, `load balancer`, `Node.js`, `pipeline`, `pod`, `production`, `staging`, `Vercel`

### 6. Systems, subsystems, and architectural components
System design, architecture patterns, and their parts.
`API gateway`, `authentication layer`, `caching layer`, `client`, `database layer`, `message broker`, `microservice`, `proxy`, `rate limiter`, `REST API`, `routing layer`, `server`, `WebSocket`

### 7. Mathematical, algorithmic, and scientific terms
Algorithms, computational concepts, and mathematical formulas.
`Big O notation`, `binary search`, `coefficient`, `complexity`, `exponent`, `hash function`, `iteration`, `logarithm`, `matrix`, `recursion`, `regex`, `sorting algorithm`, `time complexity`, `traversal`

### 8. Interface elements and navigation
UI components, navigation controls, and layout elements.
`button`, `checkbox`, `dialog`, `dropdown`, `footer`, `header`, `menu`, `modal`, `navigation bar`, `radio button`, `scrollbar`, `sidebar`, `tab`, `text field`, `toggle`, `tooltip`

### 9. Numbers, units of measurement, and time
Quantitative data, measurements, and time-related information.
`byte`, `gigabyte (GB)`, `hertz (Hz)`, `hour (h)`, `kilobyte (KB)`, `megabyte (MB)`, `millisecond (ms)`, `minute`, `nanosecond (ns)`, `second (s)`, `terabyte (TB)`

### 10. Quoted text
Texts you cannot change in code documentation — error messages, code snippets, UI labels, log output.
`Cannot read properties of undefined`, `ENOENT: no such file or directory`, `Submit` button, `404 Not Found`, `connection refused`

### 11. Professional roles, teams, and organizations
Roles, individuals, organizations, and teams related to software development.
`administrator`, `backend developer`, `contributor`, `DevOps engineer`, `frontend developer`, `Google`, `maintainer`, `Microsoft`, `product owner`, `QA engineer`, `reviewer`, `scrum master`, `user`

### 12. Official documents, API references, and standards
Documentation types, standards, specifications, and their structural parts.
`API reference`, `changelog`, `code of conduct`, `contributing guide`, `diagram`, `figure`, `Getting Started guide`, `HTTP specification`, `note`, `paragraph`, `README`, `release notes`, `RFC`, `section`, `table`, `warning`

### 13. Runtime environments and operational conditions
Execution contexts, environment variables, and operating parameters.
`development`, `environment variable`, `garbage collection`, `heap`, `hot reload`, `live reload`, `memory leak`, `production`, `sandbox`, `stack trace`, `staging`, `test`, `thread`, `timeout`, `virtual machine`

### 14. Colors
Colors that identify color-related properties in code (CSS, terminal output, syntax highlighting).
`black`, `blue`, `cyan`, `gray`, `green`, `magenta`, `orange`, `red`, `white`, `yellow`
Colors are adjectives, but STE-Code identifies them as code-domain technical nouns. Comparative and superlative forms (for example, `blacker`, `the reddest`) are not permitted.

### 15. Defects, errors, and fault terminology
Types of software defects, errors, and malfunctions.
`assertion failure`, `bug`, `crash`, `deadlock`, `defect`, `exception`, `hang`, `infinite loop`, `memory leak`, `null pointer`, `race condition`, `regression`, `stack overflow`, `timeout`, `type error`

### 16. Computer science, information, and communication technology
Concepts, technologies, and architectures in computing and communication.
`AI`, `algorithm`, `authentication`, `authorization`, `blockchain`, `containerization`, `cryptography`, `database`, `encoding`, `encryption`, `firewall`, `hashing`, `internet`, `machine learning`, `metadata`, `neural network`, `protocol`, `query`, `sandbox`, `schema`, `token`, `virtualization`

### 17. Legal and licensing terms
Software licenses, legal documents, and compliance terminology.
`Apache 2.0`, `BSD license`, `compliance`, `copyright`, `GPL`, `license`, `MIT license`, `open source`, `proprietary`, `terms of service`, `third-party`, `trademark`, `warranty`

### 18. Database and storage terminology
Database concepts, storage systems, and data persistence.
`connection pool`, `cursor`, `foreign key`, `index`, `migration`, `NoSQL`, `ORM`, `PostgreSQL`, `primary key`, `query`, `Redis`, `relation`, `row`, `schema`, `seed`, `SQL`, `SQLite`, `stored procedure`, `table`, `transaction`, `view`

### 19. Network and protocol terminology
Networking concepts, protocols, and communication.
`DNS`, `endpoint`, `HTTP`, `HTTPS`, `IP address`, `localhost`, `middleware`, `packet`, `port`, `request`, `response`, `route`, `socket`, `SSH`, `TCP`, `TLS`, `UDP`, `URL`, `VPN`, `WebSocket`

---

## Apply the categories by document type

Use the categories named here as your first-choice technical nouns for each kind
of documentation. Use an approved verb everywhere an approved word fits.

- **README files** — categories 1 (code components), 3 (development tools), 5 (infrastructure), 17 (legal). Example: "This package provides a `middleware` for `Express`." (`package` c1, `middleware` c1, `Express` c5.)
- **API documentation** — categories 6 (systems), 18 (database), 19 (network). Example: "The `GET /users/:id` route returns a `JSON` object with a user `struct`." (`route` c19, `JSON` c4, `struct` c4.)
- **Docstrings and inline comments** — categories 4 (data types), 7 (algorithms), 15 (defects). Example: "Traverse the binary search tree in-order and return a sorted `array`."
- **Commit messages** — categories 1 (code components), 15 (defects), 18 (database). Example: "Fix a `timeout` defect in the `connection pool` that caused a `deadlock` on `PostgreSQL`."
- **Error messages** — categories 13 (runtime), 15 (defects), 19 (network). Example: "Connection refused: the `TCP` `socket` on `port 5432` timed out after 30 seconds."
- **Test specifications** — categories 1 (code components), 4 (data types), 15 (defects). Example: "The test calls the `parseConfig` function with a `null pointer` and checks that it returns an `assertion failure`."

## Paradigm-specific guidance

Use the categories shown as your first-choice technical nouns for each paradigm.

- **Object-oriented (Java, C++, C#, Python classes)** — categories 1 (code components), 4 (data types), 6 (systems). Class, method, interface, and design-pattern names are technical nouns. Acceptable: "The `UserRepository` class extends the `BaseRepository` abstract class and implements the `IAuditable` interface." Do not write "The repo leverages the base to retrieve user data." (`leverage` is not approved; `repo` is a non-standard abbreviation — use `repository`.)
- **Functional (Haskell, Elixir, Clojure, Rust)** — categories 7 (algorithms), 4 (data types), 16 (computer science). Terms such as `monad`, `functor`, `closure`, `currying`, `pattern matching`, `recursion`, `immutability` are technical nouns. Acceptable: "The function returns an `Option` monad. Use pattern matching to extract the value." Do not write "The combinator stuff chains stuff together to make new stuff."
- **Procedural (C, Go, Bash)** — categories 4 (data types), 13 (runtime), 19 (network). Terms such as `pointer`, `struct`, `mutex`, `goroutine`, `channel`, `file descriptor`, `signal` are technical nouns. Acceptable: "The C function accepts a `pointer` to a `FILE` struct and returns an integer status code." Do not write "The script fires off a subprocess to crunch the numbers." (`fires off` → `starts`; `crunch` → `process`.)
- **Declarative (SQL, Terraform, Kubernetes YAML)** — categories 18 (database), 5 (infrastructure), 12 (official documents). `SELECT`, `JOIN`, resource, module, provider, pod, deployment, namespace are technical nouns; SQL keywords and YAML keys are quoted text (category 10) when referenced verbatim. Acceptable: "The `SELECT` statement uses an `INNER JOIN` on the `users` and `orders` tables." Do not write "K8s spins up a bunch of pods inside the thing." (`K8s` → `Kubernetes`; `spins up` → `starts`; `thing` → `namespace`.)
- **Systems programming (Rust ownership, C memory management)** — categories 13 (runtime), 4 (data types), 15 (defects). `ownership`, `borrow`, `lifetime`, `stack`, `heap`, `allocation`, `undefined behavior`, `segmentation fault` are technical nouns. Acceptable: "The Rust compiler enforces the ownership rules. The borrow checker prevents dangling pointers at compile time." Do not write "Rust's thingy stops you from shooting yourself in the foot with memory stuff."

---

## Edge cases

- **Framework names that are also common words** (`React`, `Vue`, `Swift`, `Go`, `Rust`, `Elm`, `Next`, `Nest`). When a framework name is also an approved word, the framework name is a code-domain technical noun (category 3 or 5) and does not follow the approved meaning. Always capitalize it to disambiguate: "Use the `React` framework to build the user interface" (not the verb *react*); "The `Go` compiler builds the binary" (not the verb *go*).
- **Code keywords in documentation.** Keywords (`if`, `else`, `for`, `while`, `return`, `class`, `def`, `fn`, `let`, `const`, `var`, `async`, `await`) are quoted text (category 10) when they appear in documentation. Use backticks. When you use them as English words in a sentence, they must follow approved meanings. Write: "If the request fails, return `500 Internal Server Error`." (not "return a 500" — `500` is quoted text or a category-9 noun and must appear verbatim).
- **Abbreviations and acronyms** (`API`, `JSON`, `SQL`, `HTML`, `CSS`, `HTTP`, `TCP`, `TLS`, `DNS`, `URL`). Permissible as technical nouns in categories 16, 18, or 19. Define each at first use unless universally understood: "The application programming interface (API) uses Hypertext Transfer Protocol Secure (HTTPS)." Then "The API returns a JSON response over HTTPS." Do not write "The API leverages HTTPS to transmit the payload" (`leverage`/`transmit`/`payload` are not approved — use `use`/`send`/`data` or define `payload` as a technical noun).
- **Generated code and auto-generated docs.** OpenAPI specs, protobuf stubs, migration files, JSDoc/Sphinx output are not required to follow STE-Code (a machine produces them). Any human-written comment, description, or annotation inside generated files must follow STE-Code. Write `// Workaround: clear the Redis cache when the heap reaches the limit.` Do not write `// this hack works around a funky TS bug` (`hack` → `workaround`; `funky` → `known defect`; `TS` → `TypeScript`).
- **Project-specific internal names.** Permitted under category 1 or 6 only after glossary registration. "The `PhoenixCache` layer stores frequently accessed data in memory." is acceptable *with* a glossary entry; without it, Rule 1.6 forbids the name.
- **Numbers as technical nouns.** A version (`Node.js 18`), HTTP status (`404`), or port (`port 5432`) is a category-9 noun or quoted text (category 10) when it is a fixed, named token, not a measured quantity. Write: "The service runs on `port 5432` and returns `404 Not Found` when the row is absent." Do not write "the default db port" or "a not found error."

## Grammar notes

- **Articles.** Use `the` for a specific instance, `a`/`an` for an indefinite instance, and no article for plural general references. "The `UserController` handles a request. The controller returns a response." / "Kubernetes pods run in a namespace."
- **Technical nouns as modifiers.** A technical noun can modify another noun to form a compound, if both belong to a recognized category. "The `Redis` cache server stores the session data." (`Redis` c18 modifies `cache server` c6; `session data` = `session` c13 + `data` c4.) Do not write "The thing layer processes the stuff queue."
- **Possessive form.** Permit `'s` only with category-11 nouns (roles, organizations). "The user's session data is encrypted." Use "of" or noun-as-modifier for all other categories: "The configuration of the `Docker` container is stored in a YAML file." Do not write "The `Docker` container's configuration…".
- **Pluralization.** Standard English rules. Acronyms take a lowercase `s` without an apostrophe. "The system uses two APIs and three SQL queries." Do not write "two API's and three SQL's".
- **Capitalization.** Proper-noun technical nouns (language names, company names, product names) keep their capitalization; common technical nouns use lowercase unless sentence-initial. "The `TypeScript` compiler checks the types. The controller handles the request." Do not write "the typescript compiler" or "The Controller".

## Cross-references

- **Rule 1.1 (Approved Words):** the dictionary of approved common-vocabulary words. Rule 1.5 is the exception that lets you use non-approved words as technical nouns.
- **Rule 1.2 (Part of Speech):** use a technical noun only as a noun or noun modifier; never as a verb.
- **Rule 1.3 (Approved Meanings):** use each technical noun only with the meaning registered in your glossary.
- **Rule 1.4 (Verb and Adjective Forms):** a word that is a technical noun may still have an approved verb form — use the verb form for actions and the noun form for naming concepts.
- **Rule 1.6 (Non-Approved Words):** forbids every non-approved word that is not a code-domain technical noun. Read Rules 1.5 and 1.6 together.
- **Rule 1.7 (Technical Nouns as Verbs):** a technical noun cannot be used as a verb (for example `host` is a noun; use `make available` or `run`).
- **Rule 1.8 (Standard Technical Nouns):** use widely accepted terms; do not invent one when a standard exists.
- **Rule 1.9 (Short Technical Nouns):** prefer short, clear technical nouns.
- **Rule 1.11 (One Term per Concept):** each technical noun refers to exactly one concept in your project.
- **Rule 1.12 (Technical Verbs):** `build`, `deploy`, `test`, `lint`, `compile`, `debug` and similar are permitted technical verbs — they are not technical nouns; do not confuse the two.

## Summary

Rule 1.5 is the gateway for all domain-specific vocabulary. It permits a word
outside the approved dictionary *only* when that word names a precise concept in
one of the nineteen code-domain categories above and is registered in your project
glossary. Follow it together with Rules 1.1 and 1.6: documentation then uses exactly
two kinds of words — approved STE-Code words for common vocabulary, and code-domain
technical nouns (plus technical verbs) for domain-specific concepts. There is no
third category.
