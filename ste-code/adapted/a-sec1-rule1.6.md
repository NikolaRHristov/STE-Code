# Rule 1.6 — Use a Word That Is Not Approved in the Dictionary, Only When It Is a Technical Noun or Part of a Technical Noun

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.6

## Original Rule

**Rule 1.6** Use a word that is not approved in the dictionary, only when it is a technical noun or part of a technical noun.

The dictionary includes some words that you cannot use because they are not approved. But if you can put these words in an applicable category of technical nouns, you can use them as technical nouns in some contexts.

Examples:

The word "base" is not approved in the dictionary and its alternative is "bottom (n)."

> **Non-STE:** Make sure that the two spigots at the base of the unit engage.

("Base" is not permitted when it is related to a surface.)

> **STE:** Make sure that the two spigots at the bottom of the unit engage.

But you can use "base" as a technical noun.

("Base" is a technical noun, category 7, mathematical, scientific, engineering terms, and formulas.)

The same word "base" can go into different categories of technical nouns. This condition occurs when you use the word "base" with different meanings in different contexts.

("Base" is a technical noun, category 5, facilities, infrastructure, and logistic procedures.)

"Backup" is not approved in the dictionary and its alternatives are "emergency (n)" and "auxiliary (adj)." But you can use "backup" as a technical noun.

("Backup" is a technical noun, category 19, computer science, information and communication technology.)

"Backup" is a one-word technical noun. But you can also write "backup file," a two-word technical noun.

("Backup file" is a technical noun, category 19, computer science, information and communication technology.)

"Main" is a word that is not approved, and its alternative is "primary (adj)."

("Main part" is not a technical noun, and it is correct to replace "main" with "primary.")

But you can use "main" as part of a technical noun.

("Main landing gear" is a technical noun. It is incorrect to replace "main" with "primary" here, because "primary landing gear" is not the technical noun that is approved in your company, industry, or subject field.)

If a word is not in the dictionary, you can use it if it is part of a technical noun. In the example that follows, "angular" and "position" are approved but "relative" is not in the dictionary.

(You can use "relative" as part of a technical noun, category 7, mathematical, scientific, engineering terms, and formulas.)

## STE-Code Adaptation

**Rule 1.6** Use a word that is not approved in the controlled terminology, only when it is a code-domain technical noun or part of a code-domain technical noun.

The controlled terminology includes some words that you cannot use because they are not approved. But if you can put these words in an applicable category of code-domain technical nouns, you can use them as code-domain technical nouns in some contexts.

"Handler" is not approved in the controlled terminology and its alternative is "function (n)." This adapts the spec example where "base" is not approved and its alternative is "bottom." Just as you must use "bottom" instead of "base" when referring to a surface, you must use "function" instead of "handler" when referring to a general processing function.

> **Non-STE:** The handler processes each incoming event.
>
> **STE:** The function processes each incoming event.

> *Adapted from spec pair: "Make sure that the two spigots at the base of the unit engage" / "Make sure that the two spigots at the bottom of the unit engage."* Just as "base" (unapproved) must be replaced with "bottom" (approved) when referring to a surface, "handler" (unapproved) must be replaced with "function" (approved) when referring to a general processing function.

But you can use "handler" as part of a code-domain technical noun. This is the same principle as the spec example where "base" can be used as a technical noun in certain categories.

> **STE:** The event handler processes each incoming event.

> *Adapted from spec pair: "base" can be used as a technical noun in categories 7 and 5.* Just as "base" transitions from unapproved word to technical noun when part of a recognized compound term, "handler" transitions from unapproved word to code-domain technical noun when part of "event handler."

("Event handler" is a code-domain technical noun, category 1, code components, modules, and libraries.)

"Main" is not approved in the controlled terminology and its alternative is "primary (adj)." This adapts the spec example directly: "main" is the same word with the same alternative in both STE and STE-Code.

> **Non-STE:** The main branch of the repository has the latest code.
>
> **STE:** The primary branch of the repository has the latest code.

> *Adapted from spec pair: "main" is not approved and its alternative is "primary (adj)."* The same word "main" with the same alternative "primary" appears in both STE and STE-Code. When "main" is used as a general adjective, it must be replaced with "primary."

But you can use "main" as part of a code-domain technical noun. This adapts the spec example where "main landing gear" is a technical noun.

> **STE:** Merge the feature branch into the main branch.

> *Adapted from spec pair: "Main landing gear" is a technical noun and it is incorrect to replace "main" with "primary."* Just as "primary landing gear" is not the approved technical name, "primary branch" is not the approved code-domain technical noun. The official term "main branch" must be used.

("Main branch" is a code-domain technical noun, category 5, infrastructure, deployment, and platforms. It is incorrect to replace "main" with "primary" here, because "primary branch" is not the technical noun that is approved in your project, industry, or subject field. This is the same principle as the spec example: "primary landing gear" is not the approved technical noun.)

### Examples

> **Non-STE:** Make sure that the two connectors at the base of the chassis engage.
>
> **STE:** Make sure that the two connectors at the bottom of the chassis engage.

This adapts the spec pair directly: "base" → "bottom" when referring to a physical surface. Just as in the aerospace example, "base" is not permitted when it refers to a surface location. The STE version uses the approved alternative "bottom."

> **Non-STE:** The auxiliary function handles the error recovery.
>
> **STE:** The auxiliary function processes the error recovery.

This adapts the spec example where "backup" is not approved and its alternatives include "auxiliary (adj)." In the spec, "backup" can be a technical noun in computer science (category 19). In STE-Code, "handler" is not approved as a general verb, but "handler" as part of a code-domain technical noun is permitted, just as "backup" is permitted as a technical noun.

---

## Code-Domain Explanation

Rule 1.6 establishes the boundary between words the writer must replace and words the writer may keep. Every word in code documentation falls into one of three categories: (a) approved words from the controlled terminology, (b) unapproved words that are code-domain technical nouns, and (c) unapproved words that are neither approved nor technical nouns. Category (c) words must be replaced or removed. Category (b) words may stay — but only when they function as nouns or as parts of compound technical nouns. This section explains how the rule applies to each documentation type.

### README Files

README files describe projects, their setup, their usage, and their architecture. They mix general descriptive prose with tool names, framework names, and package names. Rule 1.6 permits the tool names to stay as technical nouns. The surrounding descriptive prose must use only approved words.

The most common violation pattern in README files is using an unapproved word in the descriptive prose when a code-domain technical noun would have been more precise — or when the writer should have used the approved alternative. For example, a README that says "The base configuration uses Express" uses "base" as a general adjective when "primary" is the approved alternative. But "Express" is a code-domain technical noun (category 3, dev tools) and is permitted.

When a README refers to a project name, a library name, or a tool name that contains an unapproved word, the entire compound term is a technical noun. "React Router" contains "router" (unapproved), but "React Router" is a package name — a code-domain technical noun (category 3). The compound is permitted as a whole. You must not extract the unapproved word and treat it separately.

> **Non-STE:** The base setup leverages Express for the main API and MongoDB for the database backend.
>
> **STE:** The primary setup uses Express for the main API and MongoDB for the database backend.
> *(P6 applied: "base" → "primary" when used as a general adjective. "leverages" → "uses" per P1 synonym table. "Express," "main API," "MongoDB," and "database backend" are code-domain technical nouns and remain unchanged.)*

### API Documentation

API documentation describes endpoints, parameters, request bodies, response shapes, and authentication schemes. Technical nouns dominate this documentation type: endpoint paths, HTTP method names, header names, parameter names, and response field names are all code-domain technical nouns.

Rule 1.6 interacts with API documentation in a specific way: the names of API resources and the names of their properties are technical nouns. But the prose that describes what each resource does must use approved words. When an API resource name contains an unapproved word (for example, an endpoint named `/api/v1/backup`), the full resource name is a technical noun and is permitted. The description of that resource must use the approved alternative: "Use this endpoint to make an auxiliary copy of the data," not "Use this endpoint to backup the data."

Authentication scheme names like "OAuth2," "JWT," and "API key" are technical nouns (category 16, computer science). Their descriptions must follow the rule. "The API key authenticates the request" uses "authenticates" — check the controlled terminology. If "authenticate" is not approved, use the approved alternative.

> **Non-STE:** POST /api/v1/backup — Backups the database and returns a backup ID.
>
> **STE:** POST /api/v1/backup — Makes an auxiliary copy of the database. Returns a backup ID.
> *(P6 applied: "Backups" as a verb → "Makes an auxiliary copy." The endpoint path `/api/v1/backup` and the field name "backup ID" are code-domain technical nouns and remain unchanged. "Backup ID" is a compound technical noun, category 18, database and storage terminology.)*

### Docstrings and Inline Comments

Docstrings and inline comments explain function behavior, parameter meanings, and algorithmic choices. They have limited space, which creates pressure to use short words instead of full approved phrases. Rule 1.6 requires that the short words be code-domain technical nouns — not unapproved general vocabulary.

A Python docstring that says "Handles the request and returns a response" violates Rule 1.6 because "handles" is an unapproved word used as a general verb. The approved alternative is "processes" (from the synonym table) or the construction "The request handler processes the request," where "request handler" is a code-domain technical noun.

Inline comments that refer to variable names, class names, or function names treat those names as quoted text (category 10). The comment itself must use approved words. A comment that says "// base case: handler returns null" uses "base" (unapproved) when "primary" is the alternative. But "base case" is itself a code-domain technical noun (category 7, algorithmic terms) — the recursive base case of a function. When "base case" is the established term for the termination condition of a recursive function, Rule 1.6 permits it.

> **Non-STE:** # Handles the edge case where the base URL is null and the handler times out.
>
> **STE:** # Processes the edge case where the base URL is null and the event handler runs longer than the timeout.
> *(P6 applied: "Handles" as a verb → "Processes." "base URL" is a compound technical noun — "base" is permitted here as part of the term. "handler" alone → "event handler" as a technical noun. "times out" → "runs longer than the timeout" replaces an unapproved phrasal verb with approved words.)*

### Commit Messages

Commit messages use conventional prefixes (feat, fix, chore, docs, test, refactor) that are code-domain technical nouns. The description after the colon must follow Rule 1.6.

A commit message like "fix: backup the config before the main migration" uses "backup" as a verb and "main" as a general adjective. Both are violations. The STE-Code version uses approved alternatives: "fix: make an auxiliary copy of the config before the primary migration."

But if "backup" is part of a recognized technical noun — for example, "backup script" — the compound is permitted: "fix: run the backup script before the primary migration." The distinction is whether the unapproved word stands alone in a general role or is embedded in a code-domain technical noun.

> **Non-STE:** feat: add handler for the backup endpoint and the main config loader
>
> **STE:** feat: add an event handler for the auxiliary-copy endpoint and the primary config loader
> *(P6 applied: "handler" alone → "event handler" (TN). "backup" as standalone adjective → "auxiliary" (approved). "backup endpoint" → "auxiliary-copy endpoint" because "backup" is not part of a recognized technical noun here. "main config loader" → "primary config loader" because "main" is a general adjective, not part of a recognized compound. If "main config" were a named configuration file in the project, then "main config" would be a technical noun and "main" would be permitted.)*

### Error Messages

Error messages appear in logs, on screens, and in terminal output. They must be clear to developers and to non-technical users. Rule 1.6 ensures that unapproved words in error messages are technical nouns, not fuzzy general vocabulary.

An error message like "Backup failed: handler timed out" contains two violations: "backup" as a standalone word (not part of a technical noun) and "handler" as a standalone word. The STE-Code version uses approved alternatives: "Auxiliary copy failed: the event handler ran longer than the timeout period."

Error codes and error type names like `ENOENT`, `ETIMEDOUT`, `NullPointerException` are technical nouns (category 15, defects and errors). They are permitted regardless of their component words. But the prose that accompanies them must use approved words.

> **Non-STE:** Error: base config file not found. The backup handler will exit.
>
> **STE:** Error: primary config file not found. The event handler for auxiliary copies will stop.
> *(P6 applied: "base" → "primary"; "backup handler" → "event handler for auxiliary copies." The words "config file" and "event handler" are code-domain technical nouns. "Auxiliary copies" uses the approved adjective "auxiliary.")*

---

## Paradigm-Specific Guidance

Rule 1.6 applies to all code documentation regardless of programming paradigm. But each paradigm has different conventions for what counts as a technical noun. This section provides paradigm-specific thresholds and examples.

### Object-Oriented (Java, C++, C#, Python Classes)

Object-oriented documentation is rich with class names, interface names, design pattern names, and method names. These are all code-domain technical nouns (category 1, code components). They are permitted even when they contain unapproved words.

A class named `BackupManager` contains the unapproved word "backup." But `BackupManager` is a class name — a code-domain technical noun. Rule 1.6 permits it. The documentation for `BackupManager` must still use approved words: "The BackupManager class makes auxiliary copies of the database" not "The BackupManager class backups the database."

Design pattern names like "Singleton," "Factory," "Observer," and "Strategy" are technical nouns (category 7, algorithmic and scientific terms). When a docstring says "This class uses the Singleton pattern," the word "Singleton" is permitted as a technical noun. But "This class singletons the connection" is a Rule 1.7 violation — do not use the technical noun as a verb.

Inheritance hierarchy descriptions also intersect with Rule 1.6. A class named `BaseController` contains "base" (unapproved). As a class name, it is a technical noun and is permitted. But the prose description must use approved alternatives: "The BaseController class is the primary controller for all pages."

> **Non-STE:** The `BaseService` class handlers requests and backups data. It factories new instances via the `MainFactory`.
>
> **STE:** The `BaseService` class processes requests and makes auxiliary copies of data. It makes new instances with the `MainFactory` class.
> *(P6 applied: "handlers" as a verb → "processes"; "backups" as a verb → "makes auxiliary copies." `BaseService` and `MainFactory` are class names — code-domain technical nouns — and remain unchanged. "factories" as a verb → "makes.")*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional programming documentation uses function names, type names, monad names, and combinator names as code-domain technical nouns. Names like `Maybe`, `Either`, `Result`, `Option`, and `Future` are type names and are permitted.

The word "base" appears in functional documentation in contexts like "base case" (the termination condition of recursion) and "base functor." Both "base case" and "base functor" are code-domain technical nouns (category 7). Rule 1.6 permits them even though "base" alone is unapproved.

Monad transformer names like `ReaderT`, `StateT`, and `ExceptT` are technical nouns. Their documentation must use approved vocabulary: "The `ReaderT` transformer adds a read-only environment to the primary monad" not "The `ReaderT` transformer adds a read-only environment to the base monad" (unless "base monad" is the established term in the library's own vocabulary — then it is a technical noun and permitted).

> **Non-STE:** The `ReaderT` transformer wraps the base monad. It handlers the environment and backups the state.
>
> **STE:** The `ReaderT` transformer wraps the underlying monad. It supplies the environment to each function and makes an auxiliary copy of the state.
> *(P6 applied: "handlers" → "supplies"; "backups" → "makes an auxiliary copy." "base monad" → "underlying monad" when "base monad" is not the established library term. If the library documentation consistently uses "base monad," the term is a technical noun and is permitted.)*

### Procedural (C, Go, Bash)

Procedural documentation uses function names, struct names, macro names, and command names as technical nouns. Rule 1.6 permits these names but requires the surrounding prose to use approved words.

In C documentation, `main()` is a function name — a code-domain technical noun. Rule 1.6 permits it. But the prose that describes `main()` must use approved alternatives: "The `main` function is the primary entry point of the program," not "The `main` function is the main entry point" (where the second "main" is a general adjective, not the function name).

In Go documentation, package names like `main`, `http`, `json`, and `sql` are technical nouns. When the documentation says "The `main` package," the word "main" is part of a technical noun (the package name). When the documentation says "the main goroutine," the word "main" is a general adjective and must become "primary" — unless the project's convention treats "main goroutine" as a technical noun.

> **Non-STE:** The `main` function calls the `backup` routine and then the `handler` for each file.
>
> **STE:** The `main` function calls the backup routine and then the file handler for each file.
> *(P6 applied: `main` is a function name — permitted. "backup routine" and "file handler" are code-domain technical nouns — permitted. The version already follows the rule. The only change: `handler` for each file → "file handler" to make the technical noun explicit.)*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes state, resources, and configurations. Resource names, table names, column names, and property names are all code-domain technical nouns.

SQL table names like `backup_logs` and column names like `main_status` are technical nouns (category 18, database terminology). They are permitted. The documentation that describes them must use approved vocabulary: "The `backup_logs` table keeps auxiliary copy records" not "The `backup_logs` table backups the records."

Kubernetes resource names like `Deployment`, `Service`, `ConfigMap`, and `Ingress` are technical nouns (category 5, infrastructure). YAML keys that name these resources are permitted. The inline comments in a Kubernetes manifest must follow Rule 1.6: "# The primary container image for the deployment" not "# The main container image for the deployment."

> **Non-STE:** # This ConfigMap holds the base settings. The handler deployment backups the data.
>
> **STE:** # This ConfigMap holds the primary settings. The handler Deployment makes auxiliary copies of the data.
> *(P6 applied: "base" → "primary"; "backups" → "makes auxiliary copies." "ConfigMap" and "handler Deployment" are code-domain technical nouns and remain unchanged. "handler" is part of the Deployment name — if the Deployment is literally named "handler," it is a technical noun.)*

### Systems (Rust Ownership, C Memory Management)

Systems documentation explains ownership, lifetimes, borrowing, and memory layout. These concepts produce dense technical vocabularies where the boundary between general word and technical noun is subtle.

In Rust, "unsafe" is a keyword and a code-domain technical noun (the `unsafe` block). Rule 1.6 permits `unsafe` when it refers to the Rust construct. But when the documentation says "This approach is unsafe," it uses "unsafe" as a descriptive adjective — and "unsafe" is not an approved adjective in the controlled terminology. Use "This approach is not safe" (using the approved adjective "safe" with negation).

The Rust concept of "raw pointer" is a code-domain technical noun (category 6, architectural components). "Raw" is unapproved in the controlled terminology. But "raw pointer" as a compound is permitted under Rule 1.6. Similarly, "dangling pointer" is a compound technical noun and "dangling" is permitted within it.

> **Non-STE:** The `main` function uses an unsafe block to access the raw pointer. The handler drops the base allocation.
>
> **STE:** The `main` function uses an `unsafe` block to access the raw pointer. The drop handler frees the primary allocation.
> *(P6 applied: `main` function name → permitted; `unsafe` block → permitted as a Rust keyword (TN); "raw pointer" → permitted as a compound TN (category 6); "handler" → "drop handler" to form an explicit TN; "base allocation" → "primary allocation" because "base" is a general adjective here.)*

---

## Extended Examples

Each example pair below shows a real code documentation scenario, the STE-Code compliant rewrite, which principles were applied, and an explanation of the fix.

### Example 1 — README: Project Architecture Overview

> **Non-STE:** The base repository hosts three main services. Each service handlers its own data and backups to a central store.
>
> **STE:** The primary repository hosts three services. Each service processes its own data and makes auxiliary copies to a central data store.

> **Principles applied:** P6 (use unapproved words only as technical nouns: "base" → "primary" since it is a general adjective; "handlers" → "processes" since "handler" is unapproved as a verb; "backups" → "makes auxiliary copies" since "backup" is unapproved as a verb). P1 (use approved words: "leverages" → "uses" per synonym table; "repository" and "service" are code-domain technical nouns under Rule 1.5).
> **Explanation:** Three violations in a single paragraph. "Base" is a general adjective modifying "repository" — not part of the compound technical noun "base repository" (which could be permitted if the project had a literal component named "base repository"). "Handlers" is used as a verb — replace with "processes." "Backups" is used as a verb — replace with "makes auxiliary copies." Note that "services" is an approved word and "data store" is a code-domain technical noun (category 18).

### Example 2 — API Docstring: JSDoc for a Backup Endpoint

> **Non-STE:** /**
>  * POST /api/backup
>  * Backups the main database. Handlers errors and returns a backup ID.
>  * @returns {string} The backup ID for the auxiliary database copy.
>  */
> **STE:** /**
>  * POST /api/backup
>  * Makes an auxiliary copy of the primary database. Processes errors and returns a backup ID.
>  * @returns {string} The backup ID for the auxiliary database copy.
>  */

> **Principles applied:** P6 (unapproved words as technical nouns: "backups" as verb → "makes an auxiliary copy"; "Handlers" as verb → "Processes"). P1 ("main" as adjective → "primary"). The endpoint path `/api/backup` and the field name "backup ID" are code-domain technical nouns (category 18) and remain unchanged.
> **Explanation:** The JSDoc block describes a backup endpoint. The path `/api/backup` contains "backup" as part of a resource name — that is a technical noun and is permitted. The field name "backup ID" is a compound technical noun and is permitted. But the prose verbs "Backups" and "Handlers" are unapproved as verbs. They must be replaced with approved constructions. The word "main" as a modifier for "database" is a general adjective and must become "primary." The phrase "auxiliary database copy" in the `@returns` tag already uses the approved word "auxiliary" — no change needed.

### Example 3 — Commit Message: Multi-Service Architecture Change

> **Non-STE:** feat: add backup handler for the main API service and the base worker pool
>
> **STE:** feat: add an auxiliary-copy handler for the primary API service and the primary worker pool

> **Principles applied:** P6 (use unapproved words only as technical nouns: "backup handler" as standalone → component words are individually unapproved; when "handler" is part of the compound "auxiliary-copy handler" it becomes a TN). P1 ("main" → "primary"; "base" → "primary"). The scope "API service" and "worker pool" are code-domain technical nouns (category 1, category 6).
> **Explanation:** The commit message describes adding a handler for backup operations. "backup" as a standalone adjective for "handler" is not a recognized compound technical noun in most projects — but "backup handler" could be permitted if the project's glossary defines it as a technical noun. Here, "backup" is replaced with the approved adjective "auxiliary" in the compound "auxiliary-copy handler." "main" → "primary"; "base" → "primary" because both are general adjectives here. If the project has a component literally named "BaseWorkerPool," that would be a class name (TN) and "base" would be permitted within it.

### Example 4 — Error Message: CI Pipeline Failure

> **Non-STE:** Build failed: the main config loader timed out. The backup handler did not start.
>
> **STE:** Build failed: the primary config loader ran longer than the timeout. The auxiliary-copy handler did not start.

> **Principles applied:** P6 (unapproved words as technical nouns: "timed out" → "ran longer than the timeout" — "timeout" is a TN (category 13), but "timed out" uses it as a phrasal verb). P1 ("main" → "primary"). "backup handler" → "auxiliary-copy handler" — "handler" becomes part of a technical noun compound. "config loader" is a code-domain technical noun (category 1) and remains unchanged.
> **Explanation:** CI pipeline error messages are displayed to developers in logs and dashboards. "timed out" is a common phrasal verb derived from the technical noun "timeout." Rule 1.6 requires converting it to an approved construction: "ran longer than the timeout." "main" → "primary." For "backup handler," the compound "auxiliary-copy handler" uses approved words to describe the function while keeping "handler" as part of the technical noun. If the project's glossary defines "backup handler" as an approved technical noun (a specific service name), then the original form is permitted.

### Example 5 — Python Docstring: Recursive Algorithm

> **Non-STE:** def merge_sort(arr: list) -> list:
>     """
>     Sorts the input array. The base case is a single element.
>     The recursive case handlers the split and merge steps.
>     """
> **STE:** def merge_sort(arr: list) -> list:
>     """
>     Sorts the input array. The base case is a single element.
>     The recursive case processes the split step and the merge step.
>     """

> **Principles applied:** P6 (unapproved words as technical nouns: "base case" is a code-domain technical noun [category 7, algorithmic terms] and is permitted). "Handlers" as a verb → "Processes" (using the approved verb from the synonym table). P1 ("split and merge steps" → "split step and the merge step" for clarity with repeated noun).
> **Explanation:** "base case" is the established term in computer science for the termination condition of a recursive function. It is a code-domain technical noun (category 7) and Rule 1.6 permits it even though "base" alone is unapproved. This is the canonical example of the "part of a technical noun" provision. "Handlers," however, is used as a general verb and is not part of a technical noun — it is replaced with "processes." The change from "split and merge steps" to "the split step and the merge step" follows P3 (one term per concept, clear reference).

### Example 6 — Configuration File Comment: Docker Compose

> **Non-STE:** # This compose file defines the base services:
> # - The main API (handlers HTTP requests)
> # - The backup worker (backups the database nightly)
> # - The cache handler (keeps hot data in memory)
> **STE:** # This compose file defines the primary services:
> # - The main API service (processes HTTP requests)
> # - The auxiliary-copy worker (copies the database each night)
> # - The cache handler (keeps hot data in memory)

> **Principles applied:** P6 (unapproved words as technical nouns: "base" → "primary"; "main" → "primary" [but "main API" could be a named service — see explanation]; "backups" → "copies"). P1 ("handlers" → "processes"). "cache handler" is a code-domain technical noun (category 1) and remains unchanged. "backup worker" → "auxiliary-copy worker" replaces the unapproved adjective with an approved one.
> **Explanation:** Docker Compose comments explain service roles. "base" → "primary." "main API" is an interesting case: if "main API" is the literal service name in the Compose file (the image or container name), it is a technical noun and "main" is permitted. If it is a descriptive label, "primary API" is correct. "handlers" → "processes." "backups" → "copies" (the approved verb). "backup worker" → "auxiliary-copy worker" because "backup" as a standalone adjective is unapproved. "cache handler" is permitted: "cache" is a technical noun (category 16) and the compound "cache handler" is a recognized code-domain technical noun. "hot data" is an industry term with "hot" used as a technical adjective in "hot data" — as a compound technical noun (category 18), it is permitted.

---

## Edge Cases

The following scenarios show where the boundary between unapproved word and permissible technical noun requires careful judgment.

### Edge Case 1: Framework Name That Is Also an Unapproved Word

**Scenario:** A framework, library, or tool has a name that is identical to an unapproved word in the controlled terminology. For example, "Express" (the Node.js framework) is the same word as "express" (an unapproved verb meaning "to state or convey"). "Cargo" (the Rust build tool) is the same word as "cargo" (an unapproved noun meaning "goods carried by a vehicle"). "Pandas" (the Python library) is the same word as "pandas" (an unapproved noun — an animal name, category 22 in the original STE spec).

**Guidance:** When the word is used to refer to the framework, library, or tool by its proper name, it is a code-domain technical noun (category 3, dev tools). Capitalize it according to the tool's official capitalization ("Express," not "express") to signal that it is a proper noun. When the word is used with its general English meaning, it is unapproved and must be replaced. Context is the deciding factor.

> **Non-STE:** Use pandas to data-frame the CSV. Then express the results as JSON.
>
> **STE:** Use `pandas` to load the CSV file into a data frame. Then use Express to send the results as JSON.
> *(P6 applied: "pandas" as library name → TN permitted. "data-frame" as verb → restructured. "express" as general verb → replaced. "Express" as framework name → TN permitted.)*

### Edge Case 2: Code Keyword That Is Also an Unapproved General Word

**Scenario:** A programming language keyword is the same word as an unapproved general English word. For example, `class` (Python/Java keyword) is the same as "class" (an unapproved noun meaning "category" or "group" — the approved alternatives are "type" or "category"). `return` (keyword) is the same as "return" (approved verb meaning "go back" or "send back"). `while` (keyword) is the same as "while" (an unapproved noun meaning "a period of time" — the approved alternative is "during").

**Guidance:** When the word appears as a keyword inside a code block (backtick-quoted), it is quoted text and is not governed by Rule 1.6. When the word appears in prose, its role determines the rule. If the prose is describing the keyword itself — "The `class` keyword defines a new type" — the keyword is a code-domain technical noun (category 10, quoted text) and is permitted. If the prose uses the word with its general English meaning — "A class of functions" — it is unapproved and must be replaced ("A category of functions").

> **Non-STE:** The class of objects that return a value from the function must not block the main thread.
>
> **STE:** The category of objects that `return` a value from the function must not block the primary thread.
> *(P6 applied: "class" as general noun → "category"; `return` as keyword → backtick-quoted TN; "main" → "primary.")*

### Edge Case 3: Word That Appears to Be a Technical Noun But Is Not

**Scenario:** A writer creates a compound term that looks like a code-domain technical noun but is not recognized in the project glossary, the industry, or any STE-Code category. For example, "handler pipeline," "backup orchestrator," "main dispatcher." These compounds use unapproved words ("handler," "backup," "main") and claim technical-noun status, but no standard reference confirms them as technical nouns.

**Guidance:** For a compound to qualify as a code-domain technical noun under Rule 1.6, it must be recognized in at least one of these sources: (a) the project glossary, (b) the official documentation of the framework or library, (c) an industry-standard reference (RFC, W3C spec, etc.), or (d) one of the 19 STE-Code categories with clear category alignment. If none of these sources recognize the compound, it is not a technical noun. The unapproved words within it must be replaced or the compound must be restructured using approved words.

> **Non-STE:** The handler pipeline integrates with the backup orchestrator via the main dispatcher.
>
> **STE:** The processing pipeline integrates with the auxiliary-copy service through the primary dispatcher.
> *(P6 applied: "handler pipeline" → "processing pipeline" [not a recognized TN]; "backup orchestrator" → "auxiliary-copy service" [not a recognized TN]; "main dispatcher" → "primary dispatcher" [not a recognized TN]. All three compounds were restructured using approved words because none were recognized technical nouns.)*

### Edge Case 4: Relaxation for Auto-Generated Documentation

**Scenario:** Auto-generated API documentation (Swagger/OpenAPI, JSDoc output, Javadoc, Sphinx) may contain descriptive text that is produced from source-code comments, method summaries, or parameter descriptions. These are generated programmatically and may contain unapproved words that the generation tool cannot automatically fix.

**Guidance:** When documentation is generated automatically from source code, apply Rule 1.6 to the source (the docstrings, comments, and annotations) — not to the generated output. The generated output inherits the compliance status of its source. If the source docstring follows Rule 1.6, the generated documentation follows it automatically. If the generation tool adds its own boilerplate text (for example, "HTTP handler for the /api/backup endpoint"), that text is quoted text from the tool and is permitted under category 10.

> **Non-STE source:** /// <summary>Handlers the backup operation for the main controller.</summary>
> **STE source:** /// <summary>Processes the auxiliary-copy operation for the primary controller.</summary>
> *(P6 applied at the source level. The generated documentation will reflect the compliant source.)*

### Edge Case 5: Open-Source Project Names and Brand Names

**Scenario:** An open-source project has a name that contains an unapproved word — for example, "Basecamp," "webpack," "Homebrew." The project name is a proper noun and a code-domain technical noun. Documentation that refers to the project by its proper name uses the name as a technical noun. But when a descriptive phrase echoes the project name without being the project name itself, Rule 1.6 applies to the descriptive phrase.

**Guidance:** The project name is always a technical noun (category 3 or category 11). References to the project must use the exact, official capitalization. Descriptive phrases that are not the project name — for example, "the base setup" when "Base" is the project name — are subject to normal Rule 1.6 review. The fact that a word appears in a project name does not make every use of that word a technical noun.

> **Non-STE:** Use Homebrew to install the base packages. Then webpack the main bundle.
>
> **STE:** Use Homebrew to install the primary packages. Then use `webpack` to make the primary bundle.
> *(P6 applied: "Homebrew" is a project name → TN permitted. "base" as general adjective → "primary." "webpack" as a verb → "use `webpack` to make." "main" as general adjective → "primary.")*

---

## Cross-References

This rule is part of Section 1 (Words) of the STE-Code specification. It is the central exemption rule — the gate through which unapproved words pass when they function as technical nouns. It interacts with nearly every other rule in Section 1.

| Rule | Title | Relationship to Rule 1.6 |
|------|-------|---------------------------|
| **Rule 1.1** | Use Approved Words from the Dictionary, Technical Nouns, or Technical Verbs | Rule 1.1 establishes the three permitted word sources: approved words, technical nouns, and technical verbs. Rule 1.6 provides the detailed test for when an unapproved word can be used as a technical noun. A word that fails the Rule 1.6 test cannot be used under Rule 1.1 — the only remaining path is Rule 1.12 (technical verbs). |
| **Rule 1.2** | Use Approved Words Only as the Specified Part of Speech | Rule 1.2 constrains how approved words may be used (only as their specified part of speech). Rule 1.6 provides the exemption for unapproved words that function as nouns. When a word is permitted under Rule 1.6, it is used as a noun — which is consistent with Rule 1.2's requirement that words match their part of speech. |
| **Rule 1.5** | You Can Use Words That You Can Include in a Technical Noun Category | Rule 1.5 defines the 19 categories of code-domain technical nouns. Rule 1.6 operationalizes Rule 1.5: it tells you that you CAN use unapproved words IF they fit into one of those 19 categories. Rule 1.5 is the list of categories; Rule 1.6 is the permission to use them. Every example in Rule 1.6 references a specific category number. |
| **Rule 1.7** | Do Not Use Technical Nouns as Verbs | Rule 1.7 is the natural consequence of Rule 1.6. If a word is permitted as a technical noun under Rule 1.6, it must remain a noun. Rule 1.7 forbids using that same word as a verb. The two rules together enforce noun-only usage for all unapproved words that pass through the Rule 1.6 gate. |
| **Rule 1.8** | Use Standard, Well-Known Technical Nouns | Rule 1.6 permits unapproved words as technical nouns. Rule 1.8 adds a quality constraint: the technical noun must be standard and well-known. An obscure, project-specific compound that no external reference confirms is unlikely to pass both Rule 1.6 (is it a technical noun?) and Rule 1.8 (is it standard?). |
| **Rule 1.9** | Prefer Short, Clear Technical Nouns | Rule 1.9 adds a brevity constraint. When Rule 1.6 permits a compound technical noun, Rule 1.9 asks whether a shorter, clearer alternative exists. "Auxiliary-copy handler" (four words, clear) is better than "backup data duplication request processing component" (six words, obscure). |
| **Rule 1.11** | One Term Per Concept — Be Consistent | Rule 1.11 requires consistency. Once a technical noun is established under Rule 1.6, use that same term every time. Do not alternate between "auxiliary-copy handler" and "backup handler" and "replication processor." Pick one term that passes Rule 1.6 and use it consistently. |
| **Rule 1.12** | Technical Verbs Are Allowed | Rule 1.12 provides the verb counterpart to Rule 1.6's noun exemption. A word that cannot pass through Rule 1.6 because it fails the "is it a technical noun?" test may still be usable under Rule 1.12 if it is a code-domain technical verb. "Serialize," "memoize," and "normalize" are technical verbs, not technical nouns — they pass through Rule 1.12 instead. |

**Dictionary reference:** See `a-dictionary.md` for the full STE-Code controlled terminology. Each entry lists the approved or unapproved status of the word. When an unapproved word might be usable as a technical noun, the entry may include a "(TN)" marker to indicate that the word is permitted in technical-noun contexts. Words without the "(TN)" marker that are listed as UNAPPROVED cannot be used — even as technical nouns — unless they appear as part of a recognized compound technical noun from the 19 categories.

**Key dictionary entries referenced in this rule:**

- **BASE (n) — UNAPPROVED:** Listed as unapproved. Approved alternatives are FOUNDATION (n) for conceptual base and ROOT (n) for positional base. "Base" is permitted as part of compound code-domain technical nouns like "base case" (category 7) and "base class" (category 1).
- **MAIN (adj) — UNAPPROVED:** Listed as unapproved. Approved alternative is PRIMARY (adj). "Main" is permitted as part of compound code-domain technical nouns like "main branch" (category 5) and "main function" (category 1, when referring to the `main()` entry point).
- **BOTTOM (n), BOTTOM (adj):** Approved in the controlled terminology. The approved alternative for "base" when referring to a physical surface location. Used in contexts like "the bottom of the stack" and "at the bottom of the file."
- **FUNCTION (n):** Approved noun in the controlled terminology meaning "a named block of code that does a task." The approved alternative for an unapproved standalone use of "handler." Used in contexts like "The function processes the input."
- **PRIMARY (adj):** Approved adjective in the controlled terminology. The approved alternative for "main" when used as a general adjective. Used in contexts like "the primary configuration" and "the primary branch" (when not referring to the named Git branch).
- **AUXILIARY (adj):** Approved adjective in the controlled terminology meaning "additional, secondary, or backup." One of the approved alternatives for "backup." Used in contexts like "an auxiliary copy" and "the auxiliary power supply."
- **ROOT (n) — (TN):** Listed as a code-domain technical noun meaning "the top-level directory in a file system." Permitted as a technical noun (category 5 or category 13, depending on context). The approved alternative for "base" in positional contexts like "the root of the project."

**Categories reference:** See `a-categories.md` for the 19 code-domain technical noun categories defined under Rule 1.5. The categories most frequently invoked by Rule 1.6 are: Category 1 (code components, modules, and libraries), Category 3 (development tools, environments, and support equipment), Category 5 (infrastructure, deployment, and platforms), Category 7 (mathematical, algorithmic, and scientific terms), Category 16 (computer science, information, and communication technology), and Category 18 (database and storage terminology).

---

## Grammar Notes

### The Technical Noun Gate Model

Rule 1.6 functions as a gate — the exemption gate — that unapproved words must pass to be usable in code documentation. The gate applies three tests:

1. **Is the word unapproved in the controlled terminology?** If the word is approved, it passes through a different gate (Rule 1.1 and Rule 1.2). Rule 1.6 does not apply to approved words. Only unapproved words enter this gate.

2. **Is the word a technical noun, or is it part of a compound technical noun?** The unapproved word must be either (a) a standalone technical noun that fits one of the 19 categories, or (b) embedded within a compound technical noun that itself fits one of the 19 categories. If neither condition is met, the word fails the gate.

3. **Is the word used as a noun in the sentence?** Even if the word passes test 2, it must be used as a noun (or as part of a noun phrase) in the sentence. If the word is used as a verb, adjective, adverb, or any other part of speech, it fails this test — regardless of its technical-noun status. This third test is enforced by Rule 1.7.

A word that passes all three tests is permitted. A word that fails any test must be replaced with an approved alternative or the sentence must be restructured.

### Compound Technical Noun Formation

Rule 1.6 distinguishes between a standalone unapproved word and the same word embedded in a compound technical noun. The distinction is not always obvious. A compound technical noun forms when:

- Two or more words combine to name a single concept that is recognized in the domain.
- The compound as a whole fits into one of the 19 categories.
- Breaking the compound into its parts and replacing individual words with approved alternatives would change the recognized name and cause confusion.

Examples of valid compound technical nouns containing unapproved words:

| Compound TN | Contains Unapproved Word | Category | Reason Permitted |
|---|---|---|---|
| base case | "base" | Category 7 (algorithmic terms) | Recognized term for recursive termination condition |
| main branch | "main" | Category 5 (infrastructure) | Recognized Git term for the primary development branch |
| event handler | "handler" | Category 1 (code components) | Recognized design pattern term |
| backup file | "backup" | Category 18 (database/storage) | Recognized file type designation |
| cache handler | "handler" | Category 1 (code components) | Compound where "cache" (TN) + "handler" (TN part) = recognized component name |

Examples of compounds that are NOT valid technical nouns:

| Compound | Reason Rejected | STE-Code Fix |
|---|---|---|
| base configuration | "base" is a general adjective, not part of a recognized compound | primary configuration |
| main setting | "main" is a general adjective | primary setting |
| handler pipeline | "handler" + "pipeline" is not a recognized compound | processing pipeline |
| backup operation | "backup" is not a recognized compound with "operation" | auxiliary-copy operation |

The test: if you can replace the unapproved word with its approved alternative and the compound still refers to the same recognized concept, it is NOT a technical noun — you must make the replacement. If the replacement creates a term that no one in the domain would recognize, the compound IS a technical noun and the unapproved word is permitted within it.

### The "Part of a Technical Noun" Provision

The ASD-STE100 specification includes the provision that an unapproved word can be used when it is "part of a technical noun." This provision creates the distinction between:

- "Main" as an unapproved adjective (must be "primary") — "the main configuration"
- "Main" as part of the technical noun "main landing gear" (permitted) — "the main landing gear"

STE-Code extends this provision to code documentation with the same logic:

- "Main" as an unapproved adjective (must be "primary") — "the main configuration"
- "Main" as part of the technical noun "main branch" (permitted) — "the main branch"
- "Main" as part of the technical noun "main function" (permitted when referring to `main()`) — "the main function"

The provision does NOT grant blanket permission to use unapproved words. It grants permission only when the unapproved word is structurally inside a recognized technical noun. The test: remove the technical noun context. If the unapproved word is still there and still unapproved, the rule is violated.

### Category Overlap — Same Word, Different Categories

The ASD-STE100 specification notes that the same word can go into different categories of technical nouns when used with different meanings. STE-Code preserves this principle.

For example, "cache" is a code-domain technical noun in:
- Category 6 (architectural components) — "The caching layer sits between the application and the database"
- Category 16 (computer science) — "Cache invalidation is a hard problem"
- Category 18 (database and storage) — "The query cache stores recent results"

The same word "base" is a code-domain technical noun in:
- Category 5 (infrastructure) — "The base image for the Docker container"
- Category 7 (algorithmic) — "The base case of the recursion"
- Category 16 (computer science) — "The base address of the memory region"

In each case, Rule 1.6 permits the word because it functions as a technical noun in that specific category. The word is not being used as a general adjective or verb — it names a specific concept within the domain.

### Distinguishing Technical Nouns from Descriptive Adjectives

The most difficult judgment in Rule 1.6 is distinguishing a technical noun (permitted) from a descriptive adjective (must be replaced). Consider these sentence pairs:

1a. "The main branch has the latest code." — "main branch" is a Git convention, a technical noun. Permitted.
1b. "The main configuration has the latest values." — "main" is a descriptive adjective. Must become "primary."

2a. "The base case returns the single-element array." — "base case" is an algorithmic term. Permitted.
2b. "The base configuration is loaded first." — "base" is a descriptive adjective. Must become "primary."

3a. "The event handler processes each request." — "event handler" is a design pattern term. Permitted.
3b. "The handler processes each request." — "handler" alone is not a recognized technical noun. Must become "function."

The distinction criterion: does the compound term appear in the official documentation of the framework, language, or standard? If yes, it is a technical noun. If no, it is descriptive prose and the unapproved words must be replaced.

### Historical Note: ASD-STE100 Precedent

In ASD-STE100 Issue 9, Rule 1.6 is one of the most pragmatically significant rules in Section 1. It acknowledges that no controlled dictionary can contain every word an aerospace technician needs. The specification therefore creates the technical-noun exemption: unapproved words are permitted when they are the established names of parts, systems, procedures, or concepts in a specific subject field.

The aerospace specification devotes considerable attention to the category system (22 categories) and to the distinction between a word used as a general English word and the same word used as a technical noun. The examples — "base" as a surface position (must be "bottom") vs. "base" as a mathematical term (permitted), "backup" as a general adjective (must be "auxiliary" or "emergency") vs. "backup" as a computer science term (permitted) — are carefully chosen to illustrate the boundary.

STE-Code adopts the same architecture for code documentation. The 19 code-domain categories replace the 22 aerospace categories. The principle is identical: unapproved words are permitted when they name recognized concepts in the software development domain. The only adaptation is the domain vocabulary — aerospace terms become code terms, but the logical structure of the rule remains unchanged.

The ASD-STE100 specification also notes that Rule 1.6 interacts deeply with Rule 1.5 (categories), Rule 1.7 (no noun-as-verb), and Rule 1.8 (standard terms). STE-Code preserves these interactions. A writer who understands Rule 1.6 has the key to using domain vocabulary correctly: every unapproved word must either be replaced with an approved alternative, or justified as a code-domain technical noun with a clear category assignment.
