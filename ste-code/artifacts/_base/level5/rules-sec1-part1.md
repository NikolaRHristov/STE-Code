<!-- a-sec1-rule1.1.md -->

# Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.1](ste-code/grouped/), Rule 1.1

## Original Rule

**Rule 1.1** Use words that are:
- Approved in the dictionary
- Technical nouns
- Technical verbs.

Simplified Technical English (STE) has a controlled dictionary (part 2) that gives the words most frequently used in technical writing. You can also use words that are not in the dictionary if you can include them in the specified categories of technical nouns and technical verbs.

A technical noun is a noun term that refers to a specified concept and is applicable to a subject field. A technical verb is a verb term that also refers to a specified concept or process and is applicable to a subject field.

Examples:

The word "use" is an approved verb in the dictionary.

The word "engine" is a technical noun.

The word "ream" is a technical verb.

The dictionary also gives a selection of words that are not approved, with examples that show how to use alternative words.

In the context of ISO 1087:2019, "subject fields" refer to specific domains or areas of knowledge that have specialized vocabularies.

Technical nouns and technical verbs are usually included in your company glossary or terminology database. Always refer to these sources, and to the specified rules in this section, for the correct selection of words.

## STE-Code Adaptation

**Rule 1.1** In code documentation, use words that are:
- Approved in the project controlled terminology
- Code-domain technical nouns
- Code-domain technical verbs.

STE-Code has a controlled terminology (part 2) that gives the words most frequently used in code documentation. You can also use words that are not in the controlled terminology if you can include them in the specified categories of code-domain technical nouns and code-domain technical verbs.

A code-domain technical noun is a noun term that refers to a specified concept in software development and is applicable to a subject field. A code-domain technical verb is a verb term that refers to a specified operation or process in software development and is applicable to a subject field.

The controlled terminology also gives a selection of words that are not approved, with examples that show how to use alternative words.

Code-domain technical nouns and code-domain technical verbs are usually included in your project glossary or terminology database. Always refer to these sources, and to the specified rules in this section, for the correct selection of words.

### Examples

> *Adapted from spec pair:* Non-STE: "Execute the script to do the task."  |  STE: "Run the script to do the task."  (Derived from ASD-STE100 Rule 1.1, which restricts vocabulary to the dictionary; STE-Code restricts vocabulary to the controlled terminology. The spec's three illustrative sentences map as: "use" (approved verb) → "run" (approved verb for executing programs); "engine" (technical noun) → "UserAuthenticator" (code-domain technical noun); "ream" (technical verb) → "serialize" (code-domain technical verb).)

The word "run" is an approved verb in the controlled terminology. This is the code-domain adaptation of the spec example where "use" is an approved verb: just as "use" is the approved general-purpose verb in STE, "run" is the approved general-purpose verb for executing programs in STE-Code.
> *Adapted from spec example: "The word 'use' is an approved verb in the dictionary."*

The word "UserAuthenticator" is a code-domain technical noun. This adapts the spec example where "engine" is a technical noun: just as "engine" belongs to the aerospace subject field, "UserAuthenticator" belongs to the software subject field.
> *Adapted from spec example: "The word 'engine' is a technical noun."*

The word "serialize" is a code-domain technical verb. This adapts the spec example where "ream" is a technical verb: just as "ream" describes a manufacturing process, "serialize" describes a data transformation process.
> *Adapted from spec example: "The word 'ream' is a technical verb."*

> **Non-STE:** Execute the script to do the task.
>
> **STE:** Run the script to do the task.

> *Adapted from spec concept: the STE dictionary lists non-approved words with approved alternatives. Just as the spec restricts vocabulary to the dictionary, STE-Code restricts vocabulary to the controlled terminology.*

---

## Code-Domain Explanation

Rule 1.1 is the gatekeeping rule of STE-Code. Every word in every sentence of code documentation must pass one of three gates: it is an approved word in the controlled terminology, it is a code-domain technical noun, or it is a code-domain technical verb. This section explains how the rule applies to each type of code documentation.

### README Files

README files are the public face of a project. They use a mix of procedural writing (setup instructions, getting started guides) and descriptive writing (project overviews, architecture summaries, design philosophy). Rule 1.1 constrains both types.

Procedural sections tell the reader how to do something. Each imperative verb must come from the approved verb list. For example, use "run" instead of "execute," use "make" instead of "generate," and use "set" instead of "configure." Noun phrases for tools, files, and commands are code-domain technical nouns and do not require approval in the controlled terminology.

Descriptive sections explain what the project does or how it works. Here, Rule 1.1 constrains adjectives and adverbs to their approved meanings. For example, use "large" instead of "substantial," use "usual" instead of "conventional," and use "correct" instead of "valid" when describing data.

Example — README setup section:

> **Non-STE:**
>
> ## Getting Started
>
> To begin utilizing the build toolchain, you must first generate the distributable artifact via `npm run build`. Then, execute the compiled binary to bootstrap the local development service. You should utilize the available environment variables to configure the runtime behavior of the application before you initiate the server.
> ```bash
> # Generate the artifact, then execute the binary to bootstrap the service
> npm run build && node dist/server.js
> ```
>
> **STE:**
>
> ## Getting Started
>
> Use the build tool to make the binary. Run the binary to start the local service. Use the environment variables to set the runtime behavior of the application before you start the server.
> ```bash
> # Make the binary, then run it to start the service
> npm run build && node dist/server.js
> ```
>
> *(P1 applied: "utilizing" → "use"; "generate" → "make"; "execute" → "run"; "bootstrap" → "start"; "utilize" → "use"; "configure" → "set"; "initiate" → "start")*

### API Documentation

API documentation describes functions, methods, endpoints, and their inputs and outputs. The technical nouns (function names, parameter names, type names, endpoint paths) are code-domain technical nouns covered by Rule 1.5. The descriptive prose that surrounds them must use approved words.

Return value descriptions, parameter explanations, and error condition notes must follow Rule 1.1. Use "get" instead of "retrieve" or "fetch." Use "send" instead of "transmit." Use "remove" instead of "delete" or "purge." Use "check" instead of "validate" or "verify."

Example — JSDoc parameter description:

> **Non-STE:**
> ```js
> /**
>  * Fetches a user record from the remote API.
>  *
>  * @param {number} timeout — The duration in milliseconds the client shall await
>  * a response prior to terminating the connection attempt.
>  * @returns {Promise<User>} A promise that resolves with the user object,
>  * or rejects if the request fails.
>  */
> async function fetchUser(id, timeout) { /* ... */ }
> ```
>
> **STE:**
> ```js
> /**
>  * Gets a user record from the remote API.
>  *
>  * @param {number} timeout — The time in milliseconds that the client waits for
>  * a response before it stops the connection.
>  * @returns {Promise<User>} A promise that gives the user object, or gives an
>  * error if the request does not complete.
>  */
> async function getUser(id, timeout) { /* ... */ }
> ```
>
> *(P1 applied: "duration" → "time"; "shall await" → "waits"; "prior to" → "before"; "terminating" → "stops"; "resolves" → "gives"; "rejects" → "gives an error")*

### Docstrings and Inline Comments

Docstrings and inline comments are written for developers who read the source code. They must be concise and unambiguous. Rule 1.1 prevents the use of casual or imprecise vocabulary that could confuse readers from different language backgrounds.

For docstrings, prefer approved verbs: "do" instead of "perform," "check" instead of "ensure," "make" instead of "construct." For inline comments, use the shortest approved word available: "NOTE:" (approved noun) for important information, "WARNING:" (approved noun) for cautionary notes, and "FIXME:" as a code-domain technical noun for known issues.

Example — Python docstring:

> **Non-STE:**
> ```python
> def validate_config(config):
>     """Performs validation on the input data to ensure it conforms to the
>     expected schema. Returns a boolean indicating whether the data is valid."""
>     schema = load_schema()
>     return schema.is_valid(config)
> ```
>
> **STE:**
> ```python
> def check_config(config):
>     """Checks the input data against the schema. Gives `True` when the data is
>     correct and `False` when the data is not correct."""
>     schema = load_schema()
>     return schema.is_correct(config)
> ```
>
> *(P1 applied: "perform" → "do"; "validation" restructured to "check"; "ensure" → "when"; "conforms to" → "against"; "indicating whether" restructured)*

### Commit Messages

Commit messages are the most constrained form of code documentation. They have a conventional format (type: description) and a character limit. Rule 1.1 forces commit messages to use the smallest possible approved vocabulary.

Use approved imperative verbs: "add," "fix," "remove," "update," "set," "make," "check," "run." These are all approved in the controlled terminology. Do not use "implement" (not approved; use "make" or "add"), "refactor" (code-domain technical verb, acceptable per Rule 1.12), or "optimize" (not approved; use "make faster" or "make smaller").

Example — conventional commit:

> **Non-STE:**
> ```
> feat: implement JWT authentication middleware for API routes
> perf: optimize database query performance in user listing endpoint
> ```
>
> **STE:**
> ```
> feat: add JWT authentication middleware for API routes
> perf: make the database query faster in the user listing endpoint
> ```
>
> *(P1 applied: "implement" → "add"; "optimize" → "make faster"; "performance" removed as redundant)*

### Error Messages

Error messages are read by end users and developers. They must use approved words to be clear to non-native English speakers. Do not use jargon, slang, or domain-specific abbreviations unless they are code-domain technical nouns.

Use "cannot" (approved) instead of "unable to" (not approved). Use "incorrect" (approved adjective) instead of "invalid" or "malformed." Use "N/A" only when it is a code-domain technical noun for a missing value.

Example — CLI error message:

> **Non-STE:**
> ```text
> $ mycli sync --db production
> Error: Unable to establish connection to the database. Please verify your
> credentials and retry.
> ```
>
> **STE:**
> ```text
> $ mycli sync --db production
> Error: Cannot connect to the database. Check your credentials and try again.
> ```
>
> *(P1 applied: "unable to" → "cannot"; "establish connection" → "connect"; "verify" → "check"; "retry" → "try again")*

---

## Paradigm-Specific Guidance

Rule 1.1 applies to all code documentation regardless of programming paradigm. But each paradigm has its own vocabulary of technical nouns and verbs, and the boundary between approved words and technical terms shifts depending on the paradigm.

### Object-Oriented (Java, C++, C#, Python Classes)

Object-oriented documentation uses class names, method names, interface names, and design pattern names as code-domain technical nouns. These are exempt from the approved-word requirement under Rule 1.5 and Rule 1.6. But the prose that describes what these classes do must use approved words.

**Approved word patterns for OOP documentation:**

- Use "make" instead of "instantiate" or "construct" when describing object creation in prose. (Note: "constructor" is a code-domain technical noun and is permitted.)
- Use "get" instead of "retrieve" or "fetch" for accessor descriptions.
- Use "set" instead of "assign" for mutator descriptions.
- Use "call" (approved verb) for invoking methods.
- Use "send" for passing messages between objects.
- Use "keep" instead of "maintain" for state retention.
- Use "is a" and "has a" for inheritance and composition relationships (both are approved constructions).

Example — class documentation:

> **Non-STE:**
> ```java
> /**
>  * The UserRepository class is responsible for persisting and retrieving User
>  * entities from the database. It leverages an ORM to abstract away the
>  * underlying SQL queries and encapsulates all data-access logic.
>  */
> public class UserRepository {
>     public User findById(Long id) { /* ... */ }
> }
> ```
>
> **STE:**
> ```java
> /**
>  * The UserRepository class keeps User records in the database and gets User
>  * records from the database. It uses an ORM to hide the SQL queries and holds
>  * all data-access logic.
>  */
> public class UserRepository {
>     public User getById(Long id) { /* ... */ }
> }
> ```
>
> *(P1 applied: "persisting" → "keeps"; "retrieving" → "gets"; "leverages" → "uses"; "abstract away" → "hide"; "encapsulates" → "holds")*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional documentation uses terms like "pure function," "immutable," "monad," "closure," and "higher-order function" as code-domain technical nouns. These are permitted under Rule 1.5 and Rule 1.6. The functional paradigm reuses some approved words with special meanings — for example, "apply" is an approved verb in STE but in functional programming it also refers to the act of giving arguments to a function.

**Guidance points for functional documentation:**

- "Apply" as a verb meaning "put something on something" is approved. The functional-programming sense of "apply a function to arguments" is a code-domain technical verb and is permitted under Rule 1.12. Both uses are valid under Rule 1.1.
- "Map" as a noun (the `map` data structure or the `map` higher-order function) is a code-domain technical noun. "Map" as a verb (to transform each element of a collection) is a code-domain technical verb. Both are permitted.
- "Fold," "reduce," "filter," "compose," and "curry" are code-domain technical verbs. They are not in the approved word list but are permitted under Rule 1.12.
- "Pure" as an adjective meaning "not mixed with anything" is approved. The functional-programming sense of "pure function" (no side effects) is a compound code-domain technical noun. Both uses are valid.

Example — module documentation:

> **Non-STE:**
> ```haskell
> -- This module furnishes a collection of pure utility functions for
> -- transforming and combining data structures in a declarative fashion.
> module Data.Utils where
>   transform :: [a] -> [b]
>   transform = map pureFn
> ```
>
> **STE:**
> ```haskell
> -- This module gives a set of pure utility functions for changing and joining
> -- data structures.
> module Data.Utils where
>   change :: [a] -> [b]
>   change = map pureFn
> ```
>
> *(P1 applied: "furnishes" → "gives"; "collection" → "set"; "transforming" → "changing"; "combining" → "joining"; clause "in a declarative fashion" removed as unnecessary)*

### Procedural (C, Go, Bash)

Procedural documentation tends to be direct and imperative. Rule 1.1 reinforces this natural tendency by requiring approved imperative verbs. Procedural code is often documented with step-by-step instructions, which must use one approved verb per step.

**Guidance points for procedural documentation:**

- Each step in a procedure must start with an approved imperative verb: "do," "make," "check," "set," "get," "run," "start," "stop," "send," "remove," "keep."
- "Allocate" is not an approved verb. Use "make" or "get" instead (for example, "make a buffer" instead of "allocate a buffer").
- "Deallocate" is not an approved verb. Use "free" (a code-domain technical verb, permitted under Rule 1.12) or restructure the sentence.
- "Dereference" is a code-domain technical verb and is permitted under Rule 1.12.
- Pointer terminology ("pointer," "address," "reference," "dereference") are all code-domain technical nouns.

Example — C function documentation:

> **Non-STE:**
> ```c
> /* Allocate a buffer of the specified size on the heap. The caller is
>  * responsible for deallocating the buffer when it is no longer needed. */
> char *make_buffer(size_t size) {
>     return malloc(size);
> }
> ```
>
> **STE:**
> ```c
> /* Make a buffer of the given size on the heap. The caller must free the
>  * buffer when the buffer is no longer necessary. */
> char *make_buffer(size_t size) {
>     return malloc(size);
> }
> ```
>
> *(P1 applied: "allocate" → "make"; "specified" → "given"; "is responsible for deallocating" → "must free"; "needed" → "necessary")*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes configuration, state, and desired outcomes rather than procedures. Rule 1.1 still applies to the prose that explains what a configuration does, but declarative documents contain a higher proportion of code-domain technical nouns (resource names, property names, keywords).

**Guidance points for declarative documentation:**

- SQL keywords (SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER) are code-domain technical verbs and are permitted under Rule 1.12. When these words appear in code blocks, they are quoted text (Rule 1.5, category 10). When they appear in prose, they are technical terms and must be marked as such.
- Terraform resource type names (for example, `aws_instance`, `kubernetes_deployment`) are code-domain technical nouns from category 5 (infrastructure, deployment, and platforms).
- Kubernetes kind names (Pod, Service, Deployment, ConfigMap) are code-domain technical nouns from the same category.
- "Provision" is not an approved verb. Use "make" or "set up" instead.
- "Orchestrate" is not an approved verb. Use "control" or "manage" (code-domain technical verb) instead.
- "Declare" and "describe" are approved verbs in the controlled terminology. They are also used in declarative programming with similar meanings, which makes them especially well-suited for declarative documentation.

Example — Terraform module documentation:

> **Non-STE:**
> ```hcl
> # This module provisions an auto-scaling group with a launch template. It
> # orchestrates the deployment of EC2 instances across multiple availability
> # zones to ensure high availability.
> resource "aws_autoscaling_group" "web" {
>   desired_capacity = 3
> }
> ```
>
> **STE:**
> ```hcl
> # This module makes an auto-scaling group with a launch template. It controls
> # the deployment of EC2 instances across many availability zones to give high
> # availability.
> resource "aws_autoscaling_group" "web" {
>   desired_capacity = 3
> }
> ```
>
> *(P1 applied: "provisions" → "makes"; "orchestrates" → "controls"; "multiple" → "many"; "ensure" → "give")*

### Systems (Rust Ownership, C Memory Management)

Systems documentation explains ownership, lifetimes, memory layout, and concurrency. These concepts have dense technical vocabularies. Rule 1.1 requires that the framing prose around these technical terms uses approved words, even when the technical terms themselves are domain-specific.

**Guidance points for systems documentation:**

- "Own," "borrow," and "move" are code-domain technical verbs in Rust and are permitted under Rule 1.12. Their standard English meanings are different from their Rust meanings, but this is acceptable because they are technical terms.
- "Allocate" and "deallocate" are not approved verbs. Use the code-domain technical verbs "allocate" (when describing memory operations precisely) or restructure to use "make" and "free" in general prose.
- "Dangle" (as in "dangling pointer") is not an approved word. Use "dangling pointer" as a compound code-domain technical noun (category 15, defects and errors).
- "Undefined behavior" is a compound code-domain technical noun (category 15).

Example — Rust documentation:

> **Non-STE:**
> ```rust
> /// The borrow checker ensures that references do not outlive the data they
> /// refer to, preventing dangling pointers and use-after-free bugs at compile
> /// time.
> fn process(data: &str) { /* ... */ }
> ```
>
> **STE:**
> ```rust
> /// The borrow checker makes sure that references do not live longer than the
> /// data they point to. This prevents dangling pointers and use-after-free
> /// defects at compile time.
> fn process(data: &str) { /* ... */ }
> ```
>
> *(P1 applied: "ensures" → "makes sure"; "outlive" → "live longer than"; "bugs" → "defects")*

---

## Extended Examples

Each example pair below shows a real code documentation scenario, the STE-Code compliant rewrite, which principle was applied, and an explanation of the fix.

### Example 1 — API Reference: Return Value Description

> **Non-STE:**
> ```ts
> /**
>  * Fetches the current user's order history.
>  * Returns a promise that resolves to an array of User objects, or rejects
>  * with an ApiError if the request fails.
>  */
> function getOrderHistory(): Promise<User[]> { /* ... */ }
> ```
>
> **STE:**
> ```ts
> /**
>  * Gets the current user's order history.
>  * Gives a Promise that completes with a list of User objects. If the request
>  * does not complete, the Promise gives an ApiError.
>  */
> function getOrderHistory(): Promise<User[]> { /* ... */ }
> ```
>
> **Principle applied:** P1 (use approved words: "resolve" → "complete," "reject" → "gives an error")
> **Explanation:** "Resolve" and "reject" are Promise-specific technical verbs. In prose, they are replaced with the approved verb "complete" and the approved construction "gives an error." The technical nouns `Promise`, `User`, and `ApiError` are code-domain technical nouns and remain unchanged. The structure is split into two sentences to keep each sentence under 25 words (descriptive limit).

### Example 2 — README: Feature Description

> **Non-STE:**
>
> ## Features
>
> The application leverages machine learning algorithms to analyze user behavior patterns and generate personalized recommendations in real time. It utilizes a distributed event pipeline to aggregate telemetry across microservices.
>
> **STE:**
>
> ## Features
>
> The application uses machine learning to examine user behavior and make personal recommendations immediately. It uses a distributed event pipeline to collect telemetry across microservices.
>
> **Principle applied:** P1 (use approved words: "leverage" → "use," "analyze" → "examine," "generate" → "make," "personalized" → "personal," "utilizes" → "uses," "aggregate" → "collect"); P9 (prefer short technical nouns: "algorithms" removed as redundant next to "machine learning"); P8 (use standard technical nouns: "real time" → "immediately")
> **Explanation:** "Leverage" is a banned word under P1. "Analyze" is not in the approved verb list; "examine" is approved and has the same meaning in this context. "Patterns" and "algorithms" add no information that "machine learning" does not already carry. "Real time" is replaced with "immediately," an approved adverb. The sentence structure is simplified to one clause.

### Example 3 — Docstring: Function Purpose

> **Non-STE:**
> ```js
> /**
>  * Validates the provided configuration object against the schema
>  * and populates default values for any missing fields.
>  *
>  * @param {Object} config - The configuration object to validate.
>  * @returns {Object} The validated and populated configuration.
>  * @throws {ValidationError} If the configuration is invalid.
>  */
> function processConfig(config) { /* ... */ }
> ```
>
> **STE:**
> ```js
> /**
>  * Checks the given configuration object against the schema
>  * and adds default values for all missing fields.
>  *
>  * @param {Object} config - The configuration object to check.
>  * @returns {Object} The checked configuration with defaults.
>  * @throws {ValidationError} If the configuration is not correct.
>  */
> function checkConfig(config) { /* ... */ }
> ```
>
> **Principle applied:** P1 (use approved words: "validate" → "check," "provided" → "given," "populate" → "add," "any" → "all," "invalid" → "not correct"); P6 (non-approved word used as technical noun: "ValidationError" is a code-domain technical noun)
> **Explanation:** "Validate" is not an approved verb; "check" is the approved alternative with the same meaning. "Populate" is replaced with "add," which is simpler and approved. "Invalid" is not an approved adjective; "not correct" uses the approved adjective "correct" with the approved negation "not." The technical noun `ValidationError` is a code-domain technical noun and remains unchanged.

### Example 4 — Error Message: User-Facing

> **Non-STE:**
> ```text
> $ upload backup.tar.gz
> Unable to process your request at this time. Please verify your input and
> try again. If the problem persists, contact support.
> ```
>
> **STE:**
> ```text
> $ upload backup.tar.gz
> Cannot process your request now. Check your input and try again. If the
> problem continues, speak to support.
> ```
>
> **Principle applied:** P1 (use approved words: "unable to" → "cannot," "at this time" → "now," "verify" → "check," "persists" → "continues," "contact" → "speak to")
> **Explanation:** "Unable to" is not approved; "cannot" is the approved modal verb. "Verify" is not an approved verb in this context; "check" is approved. "Persist" is not approved; "continue" is approved. "Contact" as a verb is not approved; "speak to" uses the approved verb "speak."

### Example 5 — Commit Message: Bug Fix

> **Non-STE:**
> ```
> fix: rectify race condition in connection pool that caused intermittent
>       failures under load
> ```
>
> **STE:**
> ```
> fix: correct race condition in connection pool that caused failures under load
> ```
>
> **Principle applied:** P1 (use approved words: "rectify" → "correct"); P9 (prefer short terms: "intermittent" removed as unnecessary — the fix implies it was intermittent)
> **Explanation:** "Rectify" is not an approved verb; "correct" is approved (as both adjective and verb). "Intermittent" is not needed in a commit message because the fix itself implies the problem was intermittent. "Race condition" and "connection pool" are code-domain technical nouns and remain unchanged.

### Example 6 — Configuration File Comment

> **Non-STE:**
> ```yaml
> # This parameter dictates the maximum quantity of concurrent connections
> # the server shall entertain before commencing to reject additional requests.
> max_connections: 100
> ```
>
> **STE:**
> ```yaml
> # This parameter sets the largest number of connections that the server
> # accepts at the same time. When the server has this many connections,
> # it refuses new requests.
> max_connections: 100
> ```
>
> **Principle applied:** P1 (use approved words: "dictates" → "sets," "quantity" → "number," "concurrent" → "at the same time," "shall entertain" → "accepts," "commencing" → removed, "reject" → "refuses," "additional" → "new"); P9 (prefer short terms); anti-pattern: no semicolons, no "-ing" as main verb in procedure
> **Explanation:** This example shows many violations at once. "Dictate" is replaced with "set." "Shall entertain" is a double violation — "shall" is not approved in descriptive writing and "entertain" is not the approved meaning. The entire sentence is restructured into two shorter sentences that use approved verbs ("sets," "accepts," "refuses") and approved constructions.

---

## Edge Cases

The following scenarios show where the boundary between approved words, technical nouns, and technical verbs requires careful judgment.

### Edge Case 1: Framework Name That Is Also an Unapproved Word

**Scenario:** A popular framework uses a name that is not an approved word in the STE-Code controlled terminology. For example, "Express" (the Node.js web framework) or "FastAPI" (the Python framework).

**Guidance:** Framework names are code-domain technical nouns (category 3, development tools and environments) and are permitted under Rule 1.5. The fact that "express" as a verb is not approved does not affect the use of "Express" as a proper noun. Always write the framework name with its correct capitalization and treat it as a technical noun.

> **Non-STE:**
> ```js
> // Express your API using Express's routing capabilities.
> const app = express();
> ```
>
> **STE:**
> ```js
> // Use Express routing to make your API endpoints.
> const app = express();
> ```
>
> In the first sentence, "Express" as a verb (meaning "to show or state") conflicts with the framework name. The second sentence uses "Express" only as a technical noun and uses the approved verb "use" for the action.

### Edge Case 2: Code Keyword That Conflicts with the Rule

**Scenario:** A programming language keyword is identical to an unapproved word. For example, `yield` is a keyword in Python and JavaScript but "yield" is not an approved verb in STE-Code (its approved alternative is "give").

**Guidance:** When the keyword appears in a code block, it is quoted text (Rule 1.5, category 10) and does not need to follow Rule 1.1. When the keyword appears in prose documentation, treat it as a code-domain technical noun (use backticks: `` `yield` ``). If you must describe what `yield` does, use the approved verb "give" in the prose and mark the keyword with backticks.

> **Non-STE:**
> ```python
> def counter():
>     """The yield keyword yields control back to the caller."""
>     yield 1
> ```
>
> **STE:**
> ```python
> def counter():
>     """The `yield` keyword gives control back to the caller."""
>     yield 1
> ```
>
> `` `yield` `` is a code-domain technical noun. "Gives" is the approved verb that replaces the unapproved "yields" in the prose.

### Edge Case 3: Generated Code Documentation

**Scenario:** Auto-generated API documentation (for example, from OpenAPI specs, JSDoc, or Sphinx) produces text that does not follow Rule 1.1.

**Guidance:** Rule 1.1 applies to documentation that a human writes or reviews. Generated documentation is exempt when the generation tool does not support STE-Code. But when you write the source annotations that feed the generator (docstrings, JSDoc comments, OpenAPI descriptions), those source texts must follow Rule 1.1. The generated output inherits the quality of the source text.

**Recommendation:** Write STE-Code compliant source annotations. The generated documentation will be cleaner even if the generator adds non-STE boilerplate. For critical public-facing API docs, post-process the generated output to replace non-approved words.

> **Non-STE:** (source annotation)
> ```yaml
> # components.schemas.User.description:
> # The object encapsulating the validated credentials of the authenticated
> # principal subsequent to a successful login operation.
> ```
>
> **STE:** (source annotation)
> ```yaml
> # components.schemas.User.description:
> # The object that holds the checked credentials of the user after a
> # successful login.
> ```

### Edge Case 4: Technical Verb Used as a Noun in a Compound Term

**Scenario:** A code-domain technical verb like "build" appears as a noun in a compound term like "build system" or "build pipeline."

**Guidance:** Rule 1.13 states that you must not use technical verbs as nouns. But when a technical verb is part of a compound code-domain technical noun, the compound as a whole is a noun. "Build system" is a code-domain technical noun (category 3, development tools). The word "build" inside the compound is not functioning as a standalone noun — it is part of a recognized technical term. This is permitted under Rule 1.5 and Rule 1.6.

> **Non-STE:**
> ```text
> The build took 45 minutes to complete.
> ```
>
> **STE:**
> ```text
> The build procedure took 45 minutes.
> ```
>
> "Build" used alone as a noun violates Rule 1.13. Adding "procedure" makes it a compound technical noun that is acceptable. Alternatively, restructure: "The system built in 45 minutes."

### Edge Case 5: Non-English Words and Loanwords

**Scenario:** Code documentation sometimes includes non-English words that have become standard in the domain (for example, "rendezvous" in networking, "de facto" in standards discussions, "naïve" in algorithm names like "naïve Bayes").

**Guidance:** These words are code-domain technical nouns when they name a specific algorithm, protocol, or pattern. "Rendezvous" as part of "rendezvous protocol" is a technical noun. "Naïve Bayes" is a technical noun. When used outside of a technical term, replace with an approved English word. "De facto" in prose should be replaced with "usual" or "primary."

> **Non-STE:**
> ```text
> This is the de facto standard for serialization in the ecosystem.
> ```
>
> **STE:**
> ```text
> This is the usual standard for serialization in the ecosystem.
> ```
>
> "De facto" is not an approved phrase. "Usual" is the approved adjective.

---

## Cross-References

This rule is the entry point to Section 1 (Words) of the STE-Code specification. The rules that follow refine and extend Rule 1.1:

| Rule | Title | Relationship to Rule 1.1 |
|------|-------|---------------------------|
| **Rule 1.2** | Use Approved Words Only as the Specified Part of Speech | Constrains approved words to their dictionary-listed part of speech. You must know a word is approved (Rule 1.1) before you can apply the part-of-speech constraint (Rule 1.2). |
| **Rule 1.3** | Use Approved Words Only with Their Approved Meanings | Constrains approved words to their dictionary-listed meanings. A word that passes Rule 1.1 must also be used with its correct meaning per Rule 1.3. |
| **Rule 1.4** | Use Only the Approved Verb Forms and Adjective Forms | Limits morphological variants of approved words. If a word passes Rule 1.1, you must use only its approved inflected forms per Rule 1.4. |
| **Rule 1.5** | You Can Use Words That You Can Include in a Technical Noun Category | Defines the technical noun exception to Rule 1.1. Rule 1.5 gives the 19 categories that make a word a technical noun. |
| **Rule 1.6** | Use a Non-Approved Word Only When It Is a Technical Noun | Refines the technical noun exception. A word that would fail Rule 1.1 can still be used if Rule 1.6 applies. |
| **Rule 1.7** | Do Not Use Technical Nouns as Verbs | Prevents a word that passed Rule 1.1 as a technical noun from being used as a verb. |
| **Rule 1.8** | Use Standard, Well-Known Technical Nouns | Adds a quality constraint: a technical noun that passes Rule 1.1 must also be a standard term per Rule 1.8. |
| **Rule 1.9** | Prefer Short, Clear Technical Nouns | Adds a brevity constraint: when more than one technical noun passes Rule 1.1, prefer the shorter one per Rule 1.9. |
| **Rule 1.10** | No Slang, Jargon, or Regional Terms | Prohibits colloquial vocabulary that might otherwise pass Rule 1.1. |
| **Rule 1.11** | One Term Per Concept | Requires consistency: once you choose an approved word for a concept per Rule 1.1, do not use a different word for the same concept. |
| **Rule 1.12** | Technical Verbs Are Allowed | Defines the technical verb exception to Rule 1.1. Code-domain technical verbs are permitted even when they are not in the approved word list. |
| **Rule 1.13** | Do Not Use Technical Verbs as Nouns | Prevents a word that passed Rule 1.1 as a technical verb from being used as a noun. |
| **Rule 1.14** | Use American English Spelling | Applies a spelling constraint to all words that pass Rule 1.1. |

**Dictionary reference:** See `a-dictionary.md` for the full STE-Code controlled terminology, including all approved words with their parts of speech and meanings, and all unapproved words with their approved alternatives.

**Categories reference:** See `a-categories.md` for the 19 code-domain technical noun categories defined under Rule 1.5.

---

## Grammar Notes

### The Three-Gate Model

Rule 1.1 establishes a three-gate model for vocabulary selection in code documentation. Every word in a sentence must pass through one of three gates:

1. **Gate 1 — Approved Word:** The word is listed as APPROVED in the STE-Code controlled terminology. It must be used with its specified part of speech (Rule 1.2) and its approved meaning (Rule 1.3). This is the default gate for all general-purpose vocabulary.

2. **Gate 2 — Code-Domain Technical Noun:** The word is not in the controlled terminology (or is listed as UNAPPROVED) but fits into one of the 19 code-domain technical noun categories (Rule 1.5). It names a specific concept, component, tool, or entity in the software domain. A word that passes through Gate 2 must not be used as a verb (Rule 1.7).

3. **Gate 3 — Code-Domain Technical Verb:** The word is not in the controlled terminology but refers to a specified technical operation or process in software development. It describes domain-specific actions that have no simple approved-word alternative. A word that passes through Gate 3 must not be used as a noun (Rule 1.13).

A word that cannot pass through any of the three gates must be replaced with an approved alternative or the sentence must be restructured.

### Part-of-Speech Primacy

The three-gate model depends on the part-of-speech classification system in the controlled terminology. Each approved word entry specifies its part of speech: verb (v), noun (n), adjective (adj), adverb (adv), preposition (prep), conjunction (conj), pronoun (pron), or article (art). Some words are approved as more than one part of speech.

The part-of-speech classification determines which gate a word can use. If a word is approved only as a noun, it passes through Gate 1 only when used as a noun. If it is used as a verb, it cannot pass through Gate 1 and must either pass through Gate 3 (as a technical verb) or be replaced. This interaction between Rule 1.1 and Rule 1.2 is the most frequent source of STE-Code violations.

### Morphological Constraints

Rule 1.1 permits a word, but Rule 1.4 constrains its morphological forms. An approved verb like "run" has approved forms: "run," "runs," "ran," "running." But "ran" is only approved as the past tense — do not use it as a past participle ("has ran" is not correct; use "has run"). An approved adjective like "clear" can be used in the comparative ("clearer") and superlative ("clearest") forms, but only when the dictionary entry for "clear" lists those forms as approved.

When a word passes through Gate 2 or Gate 3 (technical nouns and verbs), the morphological constraints of Rule 1.4 do not apply in the same way. Technical terms follow the conventions of their subject field. But when a technical term has a standard English morphological pattern, prefer the pattern that is consistent with Rule 1.4.

### Domain Boundary Awareness

The most difficult judgment in applying Rule 1.1 is deciding whether a word is a code-domain technical term (Gate 2 or Gate 3) or general-purpose vocabulary (Gate 1). The test is: would a software developer from a different language background recognize this word as a standard technical term in the domain? If yes, it is likely a technical noun or verb. If the word is a synonym that a writer chose for variety or style, it must pass through Gate 1.

When in doubt, consult the project glossary. If the word appears in the project glossary as a defined term, it is a technical noun or verb. If it does not appear in the glossary and there is an approved alternative in the controlled terminology, use the approved alternative.

### Cross-Domain Technical Terms

Some words are technical terms in both the general STE dictionary and the software domain, but with different meanings. For example, "terminal" is a technical noun in aerospace (the end of a connection point) and in software (a command-line interface or a computer endpoint). Both uses pass through Gate 2. The context determines which meaning applies. When the context is ambiguous, add a modifier to make the meaning clear: "terminal window" or "terminal connector."

### Historical Note: ASD-STE100 Precedent

In ASD-STE100 Issue 9, Rule 1.1 is the foundation of the entire specification. It introduces the dictionary (Part 2 of the spec) and the concept of controlled vocabulary. The aerospace specification emphasizes that the dictionary is not a complete vocabulary — it is a selection of the most frequently used words, and technical terms fill the gaps. STE-Code follows the same philosophy: the controlled terminology gives the most frequently used words in code documentation, and the 19 categories of code-domain technical nouns (plus the code-domain technical verb provision) fill the gaps.

The original ASD-STE100 uses the term "dictionary." STE-Code uses "controlled terminology" to avoid confusion with programming language data structures (Python `dict`, JavaScript `Map`, etc.). Both serve the same function: a curated list of approved words with their parts of speech, meanings, and usage examples.

---

> **See also:** Rule 1.2 — Use Approved Words Only as the Specified Part of Speech
> **See also:** Rule 1.3 — Use Approved Words Only with Their Approved Meanings
> **See also:** Rule 1.4 — Use Only the Approved Verb Forms and Adjective Forms
> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category
> **See also:** Rule 1.6 — Use a Non-Approved Word Only When It Is a Technical Noun
> **See also:** Rule 1.7 — Do Not Use Technical Nouns as Verbs
> **See also:** Rule 1.8 — Use Standard, Well-Known Technical Nouns
> **See also:** Rule 1.9 — Prefer Short, Clear Technical Nouns
> **See also:** Rule 1.10 — No Slang, Jargon, or Regional Terms
> **See also:** Rule 1.11 — One Term Per Concept
> **See also:** Rule 1.12 — Technical Verbs Are Allowed
> **See also:** Rule 1.13 — Do Not Use Technical Verbs as Nouns
> **See also:** Rule 1.14 — Use American English Spelling

---

<!-- a-sec1-rule1.10.md -->

# Rule 1.10 — Do Not Use Regional, Slang, or Jargon Words as Technical Nouns

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.10](ste-code/grouped/), Rule 1.10

## Original Rule

**Rule 1.10** Do not use regional, slang, or jargon words as technical nouns.

There can be technical words that only persons in confined regions or geographical areas use. These words are not easy to understand for persons who are from a different region or area. When you select technical nouns, always use well-known words.

This rule is also applicable to technical slang or jargon words. If only a small number of persons understand a word, it will cause confusion and non-effective communication.

Examples:

"Skid road" is a term used in some regions of North America and Canada, Northern Europe, and New Zealand. Its meaning is not immediately clear to the reader.

> **STE:** During logging operations, attach a cable to the heavy machinery to hold the logs in their position.

"Gear" is technical jargon that refers to tools and equipment, and its meaning is not immediately clear to the reader.

> **STE:** During logging operations, attach a cable to the heavy machinery to hold the logs in their position.

## STE-Code Adaptation

**Rule 1.10** Do not use regional, slang, or jargon words as code-domain technical nouns.

There can be technical words that only persons in confined communities or specific programming language ecosystems use. These words are not easy to understand for persons who are from a different background or use a different technology stack. When you select code-domain technical nouns, always use well-known words.

This rule is also applicable to technical slang or jargon words. If only a small number of persons understand a word, it will cause confusion and non-effective communication. Code documentation is read by developers with diverse backgrounds, including junior developers, developers from different language communities, and non-native English speakers. A word that one subculture finds clear can be opaque to every other reader.

### Examples

> *Adapted from spec pair:* Non-STE: "Skid road" is a regional term used only in some regions of North America, Canada, Northern Europe, and New Zealand; "gear" is technical jargon that refers to tools and equipment. | STE: During logging operations, attach a cable to the heavy machinery to hold the logs in their position.

**Example A — Hacker jargon as a noun (cruft → unnecessary code).**

A docstring in a module-cleanup utility:

```python
# Non-STE docstring
def cleanup(legacy_module):
    """Remove all the cruft from the legacy module."""
    dead_code = find_unreachable_functions(legacy_module)
    legacy_module.delete(dead_code)


# STE docstring
def cleanup(legacy_module):
    """Remove all the unnecessary code from the legacy module."""
    dead_code = find_unreachable_functions(legacy_module)
    legacy_module.delete(dead_code)
```

> **Non-STE:** Remove all the cruft from the legacy module.
>
> **STE:** Remove all the unnecessary code from the legacy module.

> *Adapted from spec example: "Gear" is technical jargon for "tools and equipment" — its meaning is not immediately clear to the reader. Just as "gear" is unclear to readers outside a specific community, "cruft" is hacker jargon that means "poorly designed or unnecessary code." Its meaning is not immediately clear to readers who are not familiar with the jargon. The STE version uses the approved words "unnecessary code," just as the spec example replaces "gear" with the clearer phrase "tools and equipment."*

**Example B — Slang verb as if it were a technical action (monkeys with → changes).**

A function comment in a data-validation module:

```javascript
// Non-STE
// The normalize() function monkeys with the input data before validation.
function normalize(rawInput) {
  rawInput = coerceTypes(rawInput); // "monkeys with" the input
  return validate(rawInput);
}

// STE
// The normalize() function changes the input data before validation.
function normalize(rawInput) {
  rawInput = coerceTypes(rawInput); // changes the input
  return validate(rawInput);
}
```

> **Non-STE:** The function monkeys with the input data before validation.
>
> **STE:** The function changes the input data before validation.

> *Adapted from spec example: "Skid road" is a regional term not understood by readers from other areas. Just as "skid road" is a forestry term used only in specific regions, "monkey with" is slang used only in certain developer communities. Its meaning ("to tamper with or change in an uncontrolled way") is not clear to non-native English readers or developers from other backgrounds. The STE version uses the approved verb "change."*

**Example C — Concept jargon in a planning document (bikeshedding → unnecessary discussion about small details).**

A team's design-decision log:

```markdown
## API Design Decisions — 2026-07

Non-STE:
> Bikeshedding delayed the API design by two weeks.

STE:
> Unnecessary discussion about small details delayed the API design by two weeks.
```

> **Non-STE:** Bikeshedding delayed the API design by two weeks.
>
> **STE:** Unnecessary discussion about small details delayed the API design by two weeks.

> *Principle: P10. "Bikeshedding" is jargon from Parkinson's Law of Triviality. It means "spending disproportionate time on trivial details." Only developers familiar with the history of this term understand it. The STE version uses the approved adjective "unnecessary" with the noun "discussion."*

**Example D — Metaphor jargon in a task note (yak shaving → completing unrelated prerequisite tasks).**

A developer's work log:

```text
Non-STE:
I spent the morning yak shaving before I could write the test.

STE:
I spent the morning completing unrelated prerequisite tasks before I could write the test.
```

> **Non-STE:** I spent the morning yak shaving before I could write the test.
>
> **STE:** I spent the morning completing unrelated prerequisite tasks before I could write the test.

> *Principle: P10. "Yak shaving" is hacker jargon that describes a chain of small, seemingly unrelated tasks that must be completed before the main task. Its meaning is opaque to any reader not familiar with the Ren and Stimpy reference. The STE version describes the actual activity without metaphor.*

**Example E — Metasyntactic placeholders in user-facing docs (foo and bar → example and placeholder values).**

An integration guide:

```markdown
# Connect your service

Non-STE:
Replace the foo and bar placeholders with real values.

STE:
Replace the example and placeholder values with real values.
```

> **Non-STE:** Replace the foo and bar placeholders with real values.
>
> **STE:** Replace the example and placeholder values with real values.

> *Principle: P10. "Foo" and "bar" are metasyntactic variables from early hacker culture. While widely used in code examples, they have no semantic meaning and confuse readers who are not familiar with the convention. Use "example" or "placeholder" to make the purpose clear.*

**Example F — Science-fiction jargon as a verb (grok → understand).**

A README onboarding section:

```markdown
## Before you change the auth module

Non-STE:
Take time to grok the authentication module before making changes.

STE:
Take time to understand the authentication module before making changes.
```

> **Non-STE:** Take time to grok the authentication module before making changes.
>
> **STE:** Take time to understand the authentication module before making changes.

> *Principle: P1, P10. "Grok" is a term from Robert Heinlein's 1961 novel "Stranger in a Strange Land." It entered hacker vocabulary through early computing culture. It means "to understand deeply and intuitively." The approved verb "understand" is clear to all readers.*

### Code-Domain Explanation

This rule applies differently across documentation types. The audience and purpose of each type determine the acceptable vocabulary.

**README files:** README documents are the entry point for new users and contributors. They must use words that are clear to developers who have no prior context with the project. Avoid community-specific slang, inside jokes, and regional expressions. A README is read by a global audience. Example of a README line that fails the rule: "This library lets you pwn the DOM." Use instead: "This library lets you control the DOM."

**API documentation:** API documentation is reference material consumed by integrators who may not share the language ecosystem of the API author. Use standard terms from the STE-Code dictionary. Do not use framework-specific nicknames. Do not use slang verbs like "hit the endpoint" when "send a request to the endpoint" is clearer. Example: write "Send a request to the /v1/users endpoint" not "Hit the /v1/users endpoint."

**Docstrings and inline comments:** Docstrings are embedded in source code and read by maintainers. While the audience is more technical, the same rules apply. A docstring written today may be read by a developer five years from now who does not know the slang of the current era. Avoid temporal jargon like "modern," "old-school," or "legacy" without clear definition. Example: write "written in 2018" not "legacy code."

**Commit messages:** Commit messages form the permanent history of a project. They are read during code reviews, blame annotations, and release notes. Slang in commit messages creates ambiguity during forensic debugging. Write commit messages as if they will be read by a developer who joined the team yesterday. Example: write "Remove the deprecated configuration parser" not "Yeet the deprecated config parser."

**Error messages:** Error messages are user-facing communication. They must be understood by operators, integrators, and end users who may not be developers. Slang or jargon in error messages causes support tickets and frustration. Error messages must use approved words and complete sentences. Example: write "The upload failed at 50 percent. Check your network connection and try again." not "The upload went pear-shaped halfway through."

**CLI help text and man pages:** Command-line tools often use terse, idiomatic language. Avoid regional idioms like "tweak the knobs" or "twiddle the bits." Use the approved verbs "change" and "set" instead. Example: write "Set the timeout value with --timeout" not "Twiddle the timeout knob with --timeout."

### Paradigm-Specific Guidance

Different programming paradigms develop their own community vocabularies. These terms become jargon when used outside the community.

**Object-Oriented (Java, C++, C#, Python classes):** The OO community uses terms like "POJO" (Plain Old Java Object), "DTO" (Data Transfer Object), and "bean." These are acceptable as technical code nouns under Rule 1.5 because they name specific patterns. However, avoid slang derived from these terms: "POJO-ify," "bean-ize," or "DTO-ification." Use full descriptions: "convert to a plain object" instead of "POJO-ify the response."

```java
// Non-STE: POJO-ify the response before you return it.
// STE: Convert the response to a plain object before you return it.
public Response toPlainObject(Response response) {
    return new PlainResponse(response.getId(), response.getName());
}
```

**Functional (Haskell, Elixir, Clojure, Rust):** The FP community has a dense vocabulary of mathematical and category-theory terms. "Monad," "functor," and "applicative" are technical code nouns allowed under Rule 1.5. However, avoid informal FP slang: "point-free style" is jargon; use "tacit programming" or describe the technique. "Eta-reduce" is jargon; use "simplify the function" or describe the specific transformation.

```haskell
-- Non-STE: Eta-reduce this helper to make it slicker.
-- STE: Simplify the helper function by removing the redundant argument.
f x = g x   -- simplify to: f = g
```

**Procedural (C, Go, Bash):** Procedural communities use hardware-derived slang. "Bang on the bits," "twiddle the register," and "massage the buffer" are all informal. Use "change," "write to," and "adjust" instead. The C community uses "pointer gymnastics" to describe complex pointer arithmetic; use "pointer arithmetic" or describe the specific operation.

```c
/* Non-STE: Massage the buffer before you ship it to the socket. */
/* STE: Adjust the buffer contents before you write them to the socket. */
void prepare_buffer(char *buffer, size_t len) {
    memset(buffer, 0, len);
}
```

**Declarative (SQL, Terraform, Kubernetes YAML):** Declarative communities use operations slang. "Blast radius," "scream test," and "cattle not pets" are infrastructure jargon. These terms are not clear to developers from other backgrounds. Use "scope of impact," "verification by controlled outage," and "disposable resources" instead.

```hcl
# Non-STE: Keep these nodes as cattle, not pets.
# STE: Treat these nodes as disposable resources that you can replace at any time.
resource "aws_instance" "web" {
  count = 3
  # disposable resources: terminate and recreate without data loss
}
```

**Systems (Rust ownership docs, C memory docs):** Systems programming has precise technical vocabulary: "undefined behavior," "data race," "use-after-free." These are technical code nouns under Rule 1.5. However, informal extensions like "UB" (abbreviation for undefined behavior) or "UAF" (use-after-free) are jargon. Spell out the full term on first use.

```rust
// Non-STE: This cast can trigger UB if the layout differs.
// STE: This cast can trigger undefined behavior if the memory layout differs.
unsafe fn cast_bytes<T>(bytes: &[u8]) -> &T {
    &*(bytes.as_ptr() as *const T)
}
```

### Extended Examples

Each example below shows a common code-documentation scenario where slang or jargon causes confusion. The STE version provides a clear alternative.

**Example 1: Hacker Jargon in Code Review Comments**

A reviewer comment on a pull request:

```text
Non-STE:
This regex is a dumpster fire. Nuke it from orbit.

STE:
This regular expression is too complex and unreliable. Remove it and write a new one.
```

> **Non-STE:** This regex is a dumpster fire. Nuke it from orbit.
>
> **STE:** This regular expression is too complex and unreliable. Remove it and write a new one.

> *Principle: P10, P6. "Dumpster fire" is American slang for a complete failure. "Nuke it from orbit" is a movie reference (Aliens, 1986). Neither phrase is clear to a global audience. The STE version states the problem and the required action in approved words.*

**Example 2: Gaming Slang in Performance Documentation**

A changelog entry:

```markdown
## Performance

Non-STE:
The garbage collector is totally nerfed in v2.4.

STE:
The garbage collector has decreased performance in version 2.4.
```

> **Non-STE:** The garbage collector is totally nerfed in v2.4.
>
> **STE:** The garbage collector has decreased performance in version 2.4.

> *Principle: P10. "Nerfed" comes from online gaming culture. It means "made weaker or less effective." A developer who does not play online games does not understand this word. The STE version uses "decreased performance," which is clear to all readers.*

**Example 3: Cultural Metaphor in Architecture Docs**

An architecture decision record:

```markdown
## ADR-014: Decompose the monolith

Non-STE:
The monolith is our Gordian knot. We need a strangle pattern.

STE:
The monolithic application has many tightly connected parts. Use a gradual replacement pattern.
```

> **Non-STE:** The monolith is our Gordian knot. We need a strangle pattern.
>
> **STE:** The monolithic application has many tightly connected parts. Use a gradual replacement pattern.

> *Principle: P10. "Gordian knot" is a reference to Greek mythology. "Strangle pattern" (short for "strangler fig pattern") is a metaphor from botany. Both assume cultural and domain knowledge. The STE version describes the architecture without metaphor.*

**Example 4: Community Nickname in API Docs**

An API reference page:

```markdown
# Endpoints

Non-STE:
The v2 endpoint is the shiny new hotness.

STE:
The version 2 endpoint is the current interface. Use it for all new integrations.
```

> **Non-STE:** The v2 endpoint is the shiny new hotness.
>
> **STE:** The version 2 endpoint is the current interface. Use it for all new integrations.

> *Principle: P10, P1. "Shiny new hotness" is informal English with no technical meaning. It does not tell the reader what to do or why version 2 matters. The STE version uses approved words and gives a clear instruction.*

**Example 5: Regional Idiom in Error Messages**

A service log line:

```text
Non-STE:
The upload went pear-shaped halfway through.

STE:
The upload failed at 50 percent. Check your network connection and try again.
```

> **Non-STE:** The upload went pear-shaped halfway through.
>
> **STE:** The upload failed at 50 percent. Check your network connection and try again.

> *Principle: P10. "Went pear-shaped" is a British idiom meaning "went wrong." American and Asian readers may not know this expression. The STE version states the failure point precisely and gives a recovery action.*

**Example 6: Slang Verb in Commit Messages**

A git commit:

```text
Non-STE:
Yeet the deprecated config parser.

STE:
Remove the deprecated configuration parser.
```

> **Non-STE:** Yeet the deprecated config parser.
>
> **STE:** Remove the deprecated configuration parser.

> *Principle: P10. "Yeet" is recent internet slang meaning "to discard forcefully." Its meaning is unknown to most professional developers and will age poorly. The approved verb "remove" is timeless and clear.*

### Edge Cases

The boundary between jargon and technical vocabulary is not always clear. These scenarios require judgment.

**Edge Case 1: Framework name that is also an unapproved word.** Some frameworks have names that are common English words: Rails, Spring, Django, Flask. When used as a proper noun (Ruby on Rails), these are technical code nouns under Rule 1.5. When used as a common noun ("the rails of the pipeline"), they become ambiguous. Always capitalize framework names to distinguish them from common nouns.

**Edge Case 2: Code keyword that conflicts with the rule.** Keywords like `goto`, `break`, `continue`, and `finally` have specific meanings in code. Do not use them as informal descriptions. "The function breaks before the loop" is ambiguous: "break" could mean "malfunctions" or "executes a break statement." Use "the function exits before the loop" for the colloquial meaning, and "the function executes a break statement" for the keyword meaning.

**Edge Case 3: Relaxed application for generated code.** Automatically generated documentation (Swagger/OpenAPI output, JSDoc stubs, godoc) may include auto-generated text that does not follow this rule. This is acceptable because generated documentation reflects the source code, not human-authored prose. However, any human-written descriptions within generated docs must follow this rule.

**Edge Case 4: Community-standard abbreviations.** Some abbreviations are so widely used that they transcend jargon status: "API," "JSON," "SQL," "HTML." These are technical code nouns under Rule 1.5. However, less universal abbreviations like "AFAICT" (as far as I can tell), "IIRC" (if I recall correctly), and "IMHO" (in my humble opinion) remain jargon. Spell out these phrases or omit them.

**Edge Case 5: When the jargon is the documented concept.** If you are documenting a tool named with a jargon term (for example, a build tool called "Gradle" or a linter called "ESLint"), the name itself is a technical code noun. Use the tool name as given. The rule applies to the prose around the name, not the name itself. Write "Run ESLint to check your code" not "Run ESLint to lint your junk."

### Cross-References

This rule interacts with several other STE-Code rules. Apply them together for maximum clarity.

- **Rule 1.1 (Use approved words):** Rule 1.1 provides the dictionary of approved words. When this rule requires you to replace slang or jargon, consult Rule 1.1 for the approved replacement.

- **Rule 1.5 (Technical code nouns are allowed):** Rule 1.5 defines the boundary between acceptable technical nouns and prohibited jargon. A term used by a specific framework or language is a technical code noun. A term used only by a subculture within that community is jargon.

- **Rule 1.6 (Non-approved words only as technical nouns):** Rule 1.6 reinforces that non-approved words are permitted only when they are technical code nouns. Slang and jargon are not technical code nouns and are not permitted even under Rule 1.6.

- **Rule 1.11 (One term per concept):** Rule 1.11 requires consistency. When you replace a jargon term with an approved word, use the same approved word every time. Do not use "remove" in one location and "delete" in another for the same concept.

- **Rule 1.12 (Technical verbs are allowed):** Rule 1.12 permits technical verbs like "build," "deploy," "test," and "lint." These are not slang. However, informal extensions like "buildify," "deploy-ify," or "test-athon" are slang and are not permitted.

- **Rule 1.13 (Do not use technical verbs as nouns):** Slang often converts verbs to nouns ("the build" becomes "the buildage") or nouns to verbs ("to architect"). Rule 1.13 prevents this pattern, which also helps enforce Rule 1.10.

- **Rule 1.14 (Use American English spelling):** Regional terms are prohibited by this rule. Regional spellings are also prohibited. When a term exists in both American and British English, use the American spelling: "color" not "colour," "initialize" not "initialise."

### Grammar Notes: Slang and Jargon in Code Documentation

The original ASD-STE100 spec identifies three categories of problematic words: regional terms, slang, and jargon. Each has distinct grammatical patterns that cause confusion in code documentation.

**Regional Terms:** These are words used only in specific geographical areas. In code documentation, regional terms also include vocabulary from specific technology ecosystems. A term common in the Ruby community ("gem," "rake task") may be unknown to a Python developer. The grammatical danger is that the reader may think they understand the word (its surface meaning) while missing its technical meaning entirely.

**Slang:** Slang words often originate as metaphors. "Spaghetti code," "brittle tests," and "flaky behavior" are all slang metaphors. The grammatical pattern is adjective + noun where the adjective has a non-literal meaning. These metaphors are culture-bound. "Spaghetti" as a metaphor for tangled code assumes familiarity with Italian cuisine. Replace slang metaphors with literal descriptions: "code with complex control flow," "tests that fail intermittently," "behavior that is not consistent."

**Jargon:** Jargon differs from technical vocabulary. Technical vocabulary ("polymorphism," "memoization," "serialization") has a precise, agreed-upon meaning. Jargon ("grok," "cruft," "bikeshedding") has a fuzzy, community-dependent meaning. The grammatical test is: can the term be found in a standard dictionary of computing with the same definition? If not, it is likely jargon.

**Abbreviations as Jargon:** Initialisms like "DRY" (Don't Repeat Yourself), "KISS" (Keep It Simple, Stupid), and "YAGNI" (You Aren't Gonna Need It) are jargon abbreviations. While they encode useful principles, the abbreviations themselves are not transparent. Spell out the principle on first use and use the abbreviation sparingly afterward. Better: state the principle directly without the abbreviation. "Remove duplicate code" is clearer than "Apply DRY."

**Temporal Jargon:** Words like "modern," "legacy," "cutting-edge," and "state-of-the-art" are temporal slang. They have no fixed meaning because time passes. Code described as "modern" in 2020 will not be "modern" in 2030. Describe the specific characteristic: "uses async/await syntax" instead of "uses modern patterns." Describe the specific age: "written in 2018" instead of "legacy code."

### Practical Application: Documentation Review Checklist

Use this checklist when reviewing code documentation for Rule 1.10 compliance:

1. Read the text aloud. Would a developer from a different country understand every word?
2. Identify all metaphors and idioms. Replace them with literal descriptions.
3. Identify all abbreviations. Expand them on first use.
4. Check for community-specific nicknames. Replace them with standard terms.
5. Check for temporal words ("modern," "legacy," "old"). Replace them with specific dates or characteristics.
6. Verify that every noun and verb appears in the STE-Code dictionary (Rule 1.1) or is a justified technical code noun (Rule 1.5).
7. Confirm that slang verbs are not used as technical actions. "Hit," "nuke," "yeet," "tweak," and "twiddle" are not approved verbs.

NOTE: This checklist is a guide. Professional judgment is always necessary when deciding if a term is jargon or a necessary technical noun.

> **See also:** Rule 1.1 — Use Approved Words
> **See also:** Rule 1.5 — Use Approved Technical Nouns for Your Subject Field
> **See also:** Rule 1.6 — Use Non-Approved Words Only as Technical Nouns
> **See also:** Rule 1.11 — Use One Term for One Concept
> **See also:** Rule 1.12 — Use Approved Technical Verbs
> **See also:** Rule 1.13 — Do Not Use Technical Verbs as Nouns
> **See also:** Rule 1.14 — Use English (American) Spelling

---

<!-- a-sec1-rule1.11.md -->

# Rule 1.11 — Do Not Use Different Technical Nouns for the Same Item

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.11](ste-code/grouped/), Rule 1.11

## Original Rule

**Rule 1.11** Do not use different technical nouns for the same item.

When you select a technical noun, do not use a different technical noun in other parts of your text to refer to the same item.

Example:

> **Non-STE:**
> 1. Make sure that the servo control unit is in the open position.
> 2. Do the operational test of the actuator.
> 3. Disconnect the control unit from the test rig.

> **STE:**
> 1. Make sure that the actuator is in the open position.
> 2. Do the operational test of the actuator.
> 3. Disconnect the actuator from the test rig.

In the non-STE example, "servo control unit," "actuator," and "control unit" refer to the same item. Use the technical noun that is approved in your company, industry, or subject field. If, as in the example, the technical noun is "actuator," then always use this technical noun in your text.

## STE-Code Adaptation

**Rule 1.11** Do not use different code-domain technical nouns for the same item.

When you select a code-domain technical noun, do not use a different code-domain technical noun in other parts of your documentation to refer to the same item. Use the code-domain technical noun that is approved in your project, company, industry, or subject field consistently throughout your text.

Changing the name of the same item in different sections of the documentation causes confusion. The reader must determine whether you refer to the same item or to a different item. Always use the same code-domain technical noun for the same item. The source of truth for the noun is the code itself: the class, function, module, table, resource, environment variable, or configuration key as it is defined and used in the repository.

### Examples

> *Adapted from spec pair:* Non-STE: "servo control unit", "actuator", "control unit" (three names for one component)  |  STE: "actuator" (one consistent technical noun for the component)

> **Non-STE:**
> 1. Initialize the UserService class to start the session manager.
> 2. Call the authenticate method on the AccountManager to verify a user.
> 3. The UserHandler returns a session token that you send in later requests.

```typescript
// src/auth/UserService.ts  — the single source of truth for the name
export class UserService {
  authenticate(credentials: Credentials): SessionToken {
    // ...
  }
}
```

> *Adapted from spec pair: "servo control unit," "actuator," and "control unit" → "actuator" (consistent technical noun). In the spec, three different names refer to the same component. In the non-STE example, "UserService," "AccountManager," and "UserHandler" refer to the same class. The reader cannot tell whether they are the same class or three classes. The repository defines one class named `UserService`. The STE version uses that approved code-domain technical noun in all three sentences.*

> **STE:**
> 1. Initialize the UserService class to start the session manager.
> 2. Call the authenticate method on the UserService to verify a user.
> 3. The UserService returns a session token that you send in later requests.

```typescript
// src/auth/UserService.ts  — the only class that handles authentication
export class UserService {
  authenticate(credentials: Credentials): SessionToken {
    // ...
  }
}
```

> **Non-STE:**
> 1. Send a request to the /api/login path to get a token.
> 2. The authentication route returns a JSON Web Token that you store in the browser.
> 3. Include the token from the login endpoint in all later requests.

```yaml
# openapi.yaml
paths:
  /api/login:
    post:
      summary: Authenticate a user and return a token
      responses:
        '200':
          description: Returns a JSON Web Token
```

> *Adapted from spec pair: "servo control unit," "actuator," and "control unit" → "actuator" (consistent technical noun). In the spec, three names refer to one item. In the non-STE example, "/api/login path," "authentication route," and "login endpoint" are three names for the same API endpoint. The OpenAPI file defines the path as `/api/login`. The STE version uses that single approved code-domain technical noun consistently.*

> **STE:**
> 1. Send a request to the /api/login endpoint to get a token.
> 2. The /api/login endpoint returns a JSON Web Token that you store in the browser.
> 3. Include the token from the /api/login endpoint in all later requests.

```yaml
# openapi.yaml
paths:
  /api/login:
    post:
      summary: Authenticate a user and return a token
      responses:
        '200':
          description: Returns a JSON Web Token
```

---

## Code-Domain Explanation

Rule 1.11 is one of the most frequently violated rules in software documentation. Code projects accumulate names from many sources: class names in source code, route patterns in HTTP APIs, file paths on disk, configuration keys, database table names, and colloquial names that developers use in conversation. When documentation mixes these names, the reader cannot know whether each name refers to the same item or to different items.

This rule applies to five primary code documentation types:

### README Files

README files introduce the project to new developers. If the README calls the same component by three different names, the reader will think the project has three separate components. A README must use exactly one code-domain technical noun for each component, service, module, or endpoint that it describes. The project's entry file, the main class name, or the documented public API name is the source of truth for this noun.

### API Documentation

API documentation (OpenAPI, JSDoc, Sphinx, Javadoc) describes endpoints, parameters, and response objects. Each endpoint has one URL path. Each parameter has one field name. Each response object has one schema name. The API documentation must use the URL path, the field name, and the schema name consistently. Do not substitute a colloquial name for the actual path. Do not describe the same parameter as "user ID" in one sentence and "account identifier" in the next sentence.

### Docstrings and Inline Comments

Docstrings describe a single function, method, class, or module. The name of the entity is given by the code itself. The docstring must use that name consistently. Do not refer to the function by a shorthand nickname in the docstring body. Do not describe the same argument by different names in different parts of the docstring. Inline comments must use the same name that the surrounding code uses.

### Commit Messages

Commit messages are short and refer to components by their file paths, class names, or function names. A commit message about `src/auth/UserService.ts` must use "UserService" or "src/auth/UserService.ts" consistently. Do not call it "the auth module" in the subject line and "the login handler" in the body. A reviewer who reads the commit later must know exactly which component changed.

### Error Messages and Log Output

Error messages and log output are read during debugging. If the error message uses a different name than the code, the developer must manually map the error message to the source. Always use the canonical code-domain technical noun in error messages. The log line `ERROR [PaymentProcessor] transaction failed` must use "PaymentProcessor" if that is the class name, not "billing engine" or "payment handler."

---

## Paradigm-Specific Guidance

### Object-Oriented (Java, C++, C#, Python)

In object-oriented documentation, the canonical technical noun is the class name. The class name is defined once in the source code. All documentation that refers to that class must use the exact class name.

**Rule:** Choose the class name as the code-domain technical noun. Use it in all method descriptions, architecture diagrams, sequence diagrams, and README sections.

**Common violations in OO documentation:**
- Calling the class `PaymentProcessor` in one section and "the payment module" in another
- Using a shortened nickname like "PP" or "the processor" in inline comments
- Describing an interface by its implementation class name

**Guidance for interfaces and abstract classes:**
When a component implements an interface, choose one canonical noun. If the documentation is about the interface contract, use the interface name. If the documentation is about the specific implementation, use the implementation class name. Document this choice at the start of the section.

### Functional (Haskell, Elixir, Clojure, Rust)

In functional documentation, the canonical technical noun is the module name or the top-level function name. Functional code often uses type aliases and generic type parameters. The documentation must settle on one name per concept.

**Rule:** Choose the module-qualified function name (for example, `Auth.authenticate`) or the type alias name as the code-domain technical noun. Use it consistently.

**Common violations in functional documentation:**
- Calling a function `validate_input` in the module doc and `check_params` in the function docstring
- Using different type alias names for the same data structure in different documentation sections
- Describing a data type by its structural shape instead of its named alias (for example, calling `UserRecord` a "map of string to user field" in one place and "the user dictionary" in another)

**Guidance for type aliases:**
When a type alias (`type User = { name: String, age: Int }`) names a concept, use the alias name. Do not describe the same concept by its structural expansion.

### Procedural (C, Go, Bash)

In procedural documentation, the canonical technical noun is the function name, the struct name, or the file path. Procedural code often has fewer naming layers than OO code, making the rule simpler but also easier to violate through informal nicknames.

**Rule:** Choose the function name or the struct name as given in the source header file or the module file. Use it in all documentation.

**Common violations in procedural documentation:**
- Calling a function `parse_config_file` in the header comment and "the config parser" in the README
- Using the file path as a name in one section and the exported function name in another
- Describing a C struct by its typedef alias in one file and its tag name in another

**Guidance for C structs with multiple names:**
A C struct can have a tag name (`struct user_record`), a typedef alias (`user_record_t`), and a variable instance name. Choose the typedef alias as the canonical noun. Use it in all documentation. Do not switch between the tag name and the typedef alias.

### Declarative (SQL, Terraform, Kubernetes YAML)

In declarative documentation, the canonical technical noun is the resource name or the table name. Declarative configuration files define resources by name. Documentation about those resources must use the defined name.

**Rule:** Choose the resource name from the configuration file or the table name from the schema as the code-domain technical noun. Use it in all documentation.

**Common violations in declarative documentation:**
- Calling a Terraform resource `aws_instance.web_server` in one section and "the EC2 instance" or "the web VM" in another
- Referring to a SQL table as `users` in the schema comment and "the user table," "the accounts table," or "the user_relation" in query documentation
- Describing a Kubernetes Deployment by its metadata name, its label selector, and its Pod template interchangeably

**Guidance for generated resource names:**
Some declarative tools generate resource names dynamically (for example, Terraform `count.index` or Helm release names). When the name is not static, choose the most specific static part of the name as the canonical noun. Document this choice.

### Systems (Rust Ownership Docs, C Memory Docs)

In systems documentation (ownership, lifetimes, memory layout), the canonical technical noun is the concept name as defined by the language specification or the standard library documentation. Systems concepts are abstract and do not have a single source file to point to. The documentation must define the term once and use it consistently.

**Rule:** Choose the name from the language specification or the standard library documentation. Define it in a glossary section. Use it in all documentation.

**Common violations in systems documentation:**
- Calling the same concept "the borrow checker" in one section and "the ownership system" in another
- Describing a memory region as "the heap allocation," "the arena," and "the buffer pool" interchangeably
- Using "lifetime parameter," "lifetime annotation," and "borrow annotation" for the same Rust syntax element

**Guidance for abstract concepts:**
When the concept does not map to a single code identifier, create a glossary entry in the project documentation. Use the glossary entry as the canonical code-domain technical noun. Cross-reference the glossary in each documentation section.

---

## Extended Examples

### Example 1: Database Table

> **Non-STE:**
> 1. The user_accounts table stores authentication data for each user.
> 2. Query the accounts relation to find active sessions that have not expired.
> 3. The user table has a foreign key to the roles table that limits access.

```sql
-- migrations/0001_init.sql
CREATE TABLE user_accounts (
  id      UUID PRIMARY KEY,
  email   TEXT NOT NULL UNIQUE,
  role_id UUID REFERENCES roles(id)
);
```

> **STE:**
> 1. The user_accounts table stores authentication data for each user.
> 2. Query the user_accounts table to find active sessions that have not expired.
> 3. The user_accounts table has a foreign key to the roles table that limits access.

```sql
-- migrations/0001_init.sql
CREATE TABLE user_accounts (
  id      UUID PRIMARY KEY,
  email   TEXT NOT NULL UNIQUE,
  role_id UUID REFERENCES roles(id)
);
```

> *Principle applied: P11 (One term per concept). Three names — "user_accounts table," "accounts relation," and "user table" — refer to the same database table. The schema defines the table as `user_accounts`. The reader cannot know whether "user table" is a shortened name for "user_accounts" or a different table. The STE version uses the schema-defined name "user_accounts" in all three sentences. If the canonical noun includes the "table" qualifier, use it consistently or drop it consistently — do not mix.*

### Example 2: Configuration Key

> **Non-STE:**
> 1. Set the database_connection_timeout value in your config to 5 seconds.
> 2. The DB timeout parameter controls how long the driver waits for a connection.
> 3. Increase the connection deadline if you see timeout errors in the logs.

```yaml
# config/database.yaml
database_connection_timeout: 5s
```

> **STE:**
> 1. Set the database_connection_timeout value in your configuration file to 5 seconds.
> 2. The database_connection_timeout parameter controls how long the driver waits for a connection.
> 3. Increase the database_connection_timeout value if you see timeout errors in the logs.

```yaml
# config/database.yaml
database_connection_timeout: 5s
```

> *Principle applied: P11 (One term per concept) and P1 (Use approved words from the dictionary). Four names — "database_connection_timeout," "DB timeout," "connection deadline," and "database_connection_timeout" — refer to the same configuration key. The first and fourth sentences use the correct name, but the middle sentences drift into informal synonyms. The STE version uses the configuration file key name in all three sentences. "DB" is an unapproved abbreviation (Rule 1.5); "deadline" has a different approved meaning than "timeout."*

### Example 3: CLI Command

> **Non-STE:**
> 1. Run the project-builder tool to compile your source files into artifacts.
> 2. The build system outputs the compiled artifacts to the dist/ directory.
> 3. Use the compiler's --watch flag to recompile when you change a file.

```text
$ project-builder --help
Usage: project-builder [options]
  --watch     Recompile when source files change
  --out <dir> Output directory for artifacts (default: dist)
```

> **STE:**
> 1. Run the project-builder tool to compile your source files into artifacts.
> 2. The project-builder tool outputs the compiled artifacts to the dist/ directory.
> 3. Use the project-builder tool's --watch flag to recompile when you change a file.

```text
$ project-builder --help
Usage: project-builder [options]
  --watch     Recompile when source files change
  --out <dir> Output directory for artifacts (default: dist)
```

> *Principle applied: P11 (One term per concept). Three names — "project-builder tool," "build system," and "compiler" — refer to the same CLI tool. The binary is named `project-builder`. The reader may think the project has three separate tools. The STE version uses the binary name "project-builder" in all three sentences. If the tool has other legitimate subsystem names (for example, a separate compiler), those must be introduced explicitly as distinct items.*

### Example 4: Error Type

> **Non-STE:**
> 1. The function throws a ValidationFailure when the input is invalid.
> 2. Catch the InputError to show a user-friendly message in the form.
> 3. The validation exception includes a list of field errors to display.

```python
# src/validation.py
class ValidationError(ValueError):
    def __init__(self, field_errors: list[str]) -> None:
        self.field_errors = field_errors

def validate(payload: dict) -> None:
    if not payload.get("email"):
        raise ValidationError(["email is required"])
```

> **STE:**
> 1. The function throws a ValidationError when the input is invalid.
> 2. Catch the ValidationError to show a user-friendly message in the form.
> 3. The ValidationError includes a list of field errors to display.

```python
# src/validation.py
class ValidationError(ValueError):
    def __init__(self, field_errors: list[str]) -> None:
        self.field_errors = field_errors

def validate(payload: dict) -> None:
    if not payload.get("email"):
        raise ValidationError(["email is required"])
```

> *Principle applied: P11 (One term per concept) and P8 (Use standard, well-known technical nouns). Three names — "ValidationFailure," "InputError," and "validation exception" — refer to the same error type. The source code defines the class as `ValidationError`. The reader cannot know whether "InputError" is a parent class of "ValidationFailure" or the same class. The STE version uses the class name "ValidationError" in all three sentences. If the class name is "ValidationError" in the source code, the documentation must match.*

### Example 5: Environment Variable

> **Non-STE:**
> 1. Set the API_KEY environment variable before you start the server.
> 2. The service reads its auth token from the environment at startup.
> 3. If the secret key is not set, the process exits with code 1.

```bash
# .env
API_KEY=sk_live_4eC39HqLyjWDarjtT1zdp7dc
```

> **STE:**
> 1. Set the API_KEY environment variable before you start the server.
> 2. The service reads the API_KEY environment variable at startup.
> 3. If the API_KEY environment variable is not set, the process exits with code 1.

```bash
# .env
API_KEY=sk_live_4eC39HqLyjWDarjtT1zdp7dc
```

> *Principle applied: P11 (One term per concept) and P4 (Use only approved verb and adjective forms). Three names — "API_KEY environment variable," "auth token," and "secret key" — refer to the same environment variable. The shell file defines the variable as `API_KEY`. The reader cannot know whether "auth token" is the same concept as "API_KEY" or a separate configuration value. The STE version uses the exact environment variable name "API_KEY" in all three sentences. The approved verb "start" replaces "starting" (Rule 1.4, no -ing forms as main verbs).*

### Example 6: Git Branch

> **Non-STE:**
> 1. Create a feature branch from the mainline to hold your changes.
> 2. Push your topic branch to the remote repository for review.
> 3. Merge the development line back into master after the tests pass.

```bash
$ git branch
  main
* feature/login-rate-limit
```

> **STE:**
> 1. Create a feature branch from the main branch to hold your changes.
> 2. Push your feature branch to the remote repository for review.
> 3. Merge the feature branch back into the main branch after the tests pass.

```bash
$ git branch
  main
* feature/login-rate-limit
```

> *Principle applied: P11 (One term per concept) and P14 (Use American English spelling). The names "mainline," "master," and "main branch" refer to the same branch. "Topic branch," "development line," and "feature branch" refer to the same branch. The STE version uses the Git convention names "main branch" and "feature branch" in all three sentences. Some projects use "master" as the canonical branch name — if so, use "master branch" consistently. The project's Git configuration determines the canonical noun.*

---

## Edge Cases

### Edge Case 1: Framework Names That Are Also Unapproved Words

Some software frameworks and libraries have names that are also words in the STE-Code controlled terminology. For example, a framework named "Act" (conflicts with the approved verb "act"), a library named "Before" (conflicts with the approved preposition "before"), or a tool named "Make" (conflicts with the approved verb "make").

**Resolution:** Framework and library names are code-domain technical nouns under Rule 1.5. They are exempt from the dictionary restriction. Use the framework name as the code-domain technical noun, exactly as it appears in the framework's own documentation. Do not rename the framework to avoid the conflict. Capitalize the framework name when the framework's own documentation does so.

**Guidance:** When both the approved word and the framework name appear in the same sentence, use capitalization and context to disambiguate. For example: "Use the Make build tool to make the project." The capital "Make" signals the technical noun; the lowercase "make" signals the approved verb. If capitalization alone is insufficient, add a qualifier: "Use the Make tool to make the project."

### Edge Case 2: Code Keywords That Conflict with the Canonical Noun

A code keyword (for example, `class`, `type`, `def`, `fn`, `let`, `async`, `await`) can sometimes be part of the concept name that the documentation needs to describe. The documentation must distinguish between the keyword as syntax and the concept name.

**Resolution:** Use a code-formatted span (backticks in Markdown, `<code>` in HTML) for the keyword when it appears as syntax. Use the prose form without code formatting for the concept name. For example: "The `async` keyword marks a function as asynchronous. An async function returns a Promise."

**Guidance:** When the concept name includes the keyword (for example, "async function" is the canonical name in JavaScript documentation), use the same compound noun consistently. Do not shorten it to "async" in some sentences and "async function" in others. The full compound noun is the code-domain technical noun.

### Edge Case 3: Multiple Canonical Names for the Same Item in Different Contexts

Some items have multiple legitimate names in different contexts. A Docker container image might be named `myapp:latest` in the Dockerfile, `myapp-image` in the CI pipeline configuration, and "the application container" in the architecture documentation. All three names refer to the same item but serve different audiences.

**Resolution:** Choose one canonical name per documentation document or per section. If you must use different names in different documents, declare the mapping at the start of each document. For example, a section header: "Container Image (myapp:latest)". After this declaration, use "myapp:latest" consistently in that section.

**Guidance:** This edge case is common in multi-repository projects and microservice architectures. The name that the build system uses may differ from the name that the deployment system uses, and both may differ from the name that the monitoring system uses. Do not force one name across all documentation. Force one name within each document or section, and document the cross-reference.

### Edge Case 4: Generated Code and Auto-Generated Documentation

Generated code (from protobuf, OpenAPI codegen, GraphQL codegen, ORM tools) produces class names, method names, and type names automatically. These names may not follow the project's naming conventions. The generated names may also change when the generator version changes.

**Resolution:** Use the generated names as code-domain technical nouns when documenting the generated code itself. Do not rename generated symbols. When documenting the hand-written code that uses the generated code, use the hand-written names as the canonical nouns and mention the generated names only in cross-references.

**Guidance:** If the generated name is long or awkward, you may define a shorter alias in the documentation, provided that you declare the alias explicitly at first use. For example: "The generated class `com.example.api.v1.UserServiceGrpc.UserServiceImplBase` (referred to as `UserServiceImplBase` in this document) provides the base implementation." After this declaration, use the alias consistently.

### Edge Case 5: Renaming During Refactoring

During a refactoring, a component changes its name. Documentation written before the refactoring uses the old name. Documentation written after the refactoring uses the new name. During the transition period, both names exist.

**Resolution:** After a rename is complete and committed, update all documentation to use the new name. Do not keep the old name in documentation with a "formerly known as" note, unless the old name is part of a public API that has not yet been deprecated. Use the DEPRECATED marker (per the STE-Code output format conventions) when the old name still appears in public-facing documentation.

**Guidance:** A git log or changelog records the rename history. Documentation does not need to preserve the old name for historical purposes. If the rename affects a public API, add a deprecation notice that maps the old name to the new name, and remove the old name from all other documentation.

---

## Cross-References

### Related Rules in Section 1

- **Rule 1.1** (Use words that are approved in the dictionary, technical nouns, or technical verbs): Rule 1.11 assumes that the chosen code-domain technical noun is itself approved under Rule 1.1. A consistent noun that violates the dictionary is still a violation.
- **Rule 1.3** (Use approved words only with their approved meanings): The canonical code-domain technical noun must be used with its approved meaning. Do not use the canonical noun to mean something else, even if you use it consistently.
- **Rule 1.5** (Technical code nouns are allowed): Rule 1.11 applies to code-domain technical nouns. Rule 1.5 defines what qualifies as a code-domain technical noun. Together, these rules say: code-domain technical nouns are allowed, and once you choose one, use it consistently.
- **Rule 1.6** (Non-approved words only when they are technical code nouns): If the code-domain technical noun is not in the controlled terminology, it is only permitted if it qualifies as a code-domain technical noun under Rule 1.6. Rule 1.11 does not override the dictionary restriction.
- **Rule 1.8** (Use standard, well-known technical nouns): The canonical noun chosen under Rule 1.11 should be the standard, well-known name for the item. Rule 1.8 helps select the correct canonical noun. Rule 1.11 enforces consistency once the noun is chosen.
- **Rule 1.9** (Prefer short, clear technical nouns): When choosing the canonical noun under Rule 1.11, prefer the shorter, clearer option among legitimate alternatives. Rule 1.9 guides the selection. Rule 1.11 governs the usage.
- **Rule 1.10** (No slang, jargon, or regional terms): The canonical noun must not be slang or jargon. Rule 1.10 disqualifies inappropriate candidates. Rule 1.11 applies to the noun that survives the Rule 1.10 filter.

### Related Rules in Section 3 (Verbs)

- **Rule 3.1** (Use only the approved verb forms): When the canonical noun is used as the subject or object of a sentence, the verb must obey Rule 3.1. A consistent noun with an unapproved verb form is still a violation.
- **Rule 3.6** (Use the active voice): A sentence that uses the canonical noun consistently but in passive voice violates Rule 3.6 if active voice is possible. Rule 1.11 governs noun choice; Rule 3.6 governs sentence structure.

### STE-Code Dictionary

- **Entry: TECHNICAL NOUN (TN):** The dictionary defines the category "technical noun" and gives examples. Rule 1.11 applies to all terms that qualify as code-domain technical nouns under this category. Refer to the dictionary entry for the full definition and scope.
- **Entry: NAME (n):** The approved noun "name" is the general term for identifiers. When you cannot use the specific code-domain technical noun (for example, when describing the naming process itself), use "name." Do not use "identifier," "label," "tag," or "handle" as synonyms for "name" — these are reserved for their specific approved meanings.

---

## Grammar Notes

### Definite Article Consistency

When a code-domain technical noun is used with the definite article "the," the article signals that the noun is specific and known to the reader. If you switch to a different noun for the same item, the reader expects "the" to introduce a different, also-known item. The reader then searches for the new item and finds nothing. This is a grammatical cause of the confusion that Rule 1.11 prevents.

In English, the first mention of an item can use the indefinite article "a" or "an":
> "A UserService handles authentication."

Subsequent mentions use the definite article "the":
> "The UserService returns a session token."

If the second sentence says "The AccountManager returns a session token," the reader interprets "the AccountManager" as a previously introduced item. The reader searches the preceding text for the first mention of "an AccountManager" and does not find it. This breaks the discourse coherence.

**Rule 1.11 is a semantic rule, but it has a direct grammatical consequence:** the article system of English depends on consistent noun choice to maintain reference chains. When you change the noun, you break the reference chain that the articles establish.

### Anaphora and Pronoun Reference

Pronouns (it, they, them, its, their) refer back to the most recent noun phrase that matches in number and gender. If the documentation alternates between "UserService" (singular) and "authentication modules" (plural), a pronoun like "it" becomes ambiguous. The reader does not know whether "it" refers to the service or to the modules.

**Example of pronoun ambiguity caused by noun inconsistency:**

> **Non-STE:**
> The UserService processes login requests. The authentication modules validate credentials. It returns a token on success.

The pronoun "it" could refer to "UserService" (singular) or the nearest plural "authentication modules" (treated as a singular system). The reader must guess. The STE version eliminates this ambiguity by using one noun consistently:

> **STE:**
> The UserService processes login requests. The UserService validates credentials. The UserService returns a token on success.

### Compound Nouns and Head Nouns

A compound noun is a sequence of nouns that together name one concept (for example, "user authentication service"). The last noun in the sequence is the head noun. The head noun carries the core meaning. The preceding nouns modify the head noun.

When documentation alternates between the full compound noun and a shortened form that changes the head noun, the reader may think the shortened form refers to a different concept.

**Example of head-noun drift:**

> **Non-STE:**
> 1. The user authentication service handles login.
> 2. The authentication system validates tokens.
> 3. The user service manages profiles.

Three different head nouns — "service," "system," and "service" — appear. The reader cannot know whether the second and third sentences describe the same component or different components. The STE version uses one compound noun with one head noun:

> **STE:**
> 1. The user authentication service handles login.
> 2. The user authentication service validates tokens.
> 3. The user authentication service manages profiles.

If the project genuinely has three separate components (an authentication service, an authentication system, and a user service), the documentation must introduce each one explicitly and explain their relationships. Rule 1.11 does not prevent projects from having multiple components. It prevents one component from having multiple names.

### Parallel Structure in Lists

Lists of steps, features, or components rely on parallel grammatical structure for readability. When each item in a list names a different component, each item must use the same grammatical form (for example, all capitalized class names, or all lowercase noun phrases). If one item uses a different naming pattern, the reader cannot tell whether the difference is meaningful or accidental.

**Example of broken parallelism:**

> **Non-STE:**
> The project has these components:
> - UserService (handles authentication)
> - The payment module (processes transactions)
> - notification_system (sends emails)

Three different naming conventions — PascalCase, sentence case with article, and snake_case — appear in one list. The STE version normalizes the naming:

> **STE:**
> The project has these components:
> - UserService (handles authentication)
> - PaymentService (processes transactions)
> - NotificationService (sends emails)

The normalization enforces Rule 1.11 at the list level. Each item uses the code-domain technical noun that matches the source code naming convention for the project.

---

> **See also:** Rule 1.1 — Use words that are approved in the dictionary, technical nouns, or technical verbs
> **See also:** Rule 1.3 — Use approved words only with their approved meanings
> **See also:** Rule 1.5 — Technical code nouns are allowed
> **See also:** Rule 1.6 — Non-approved words only when they are technical code nouns
> **See also:** Rule 1.8 — Use standard, well-known technical nouns
> **See also:** Rule 1.9 — Prefer short, clear technical nouns
> **See also:** Rule 1.10 — No slang, jargon, or regional terms
> **See also:** Rule 3.1 — Use only the approved verb forms
> **See also:** Rule 3.6 — Use the active voice

---

<!-- a-sec1-rule1.12.md -->

# Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.12](ste-code/grouped/), Rule 1.12

## Original Rule

**Rule 1.12** You can use verbs that you can include in a technical verb category.

A technical verb is a verb term that refers to a specified concept or process and is applicable to a subject field.

The dictionary does not include technical verbs because there are too many, and each subject field uses different technical verbs for their texts.

You can find many of these technical verbs in your company glossary or terminology database.

STE gives you a list of categories, with examples, to help you:
- Select technical verbs to put in your company glossary or terminology database.
- Use technical verbs correctly.

Technical verbs must obey the same rules as other approved verbs in STE. Refer to section 3.

You can use technical verbs in procedural and descriptive texts if you can include them in one or more of these four categories.

[The original specification lists 4 main categories with subcategories: 1) Manufacturing processes (a-f subcategories); 2) Computer processes and applications (a-c subcategories); 3) Instructions and information for applicable subject fields (a-f subcategories); 4) Law and regulations.]

The technical verbs in their related categories are only examples. Rule 1.12 does not give a full list of all possible technical verbs.

If there is an approved verb in the dictionary that accurately gives the instruction or the information, use the approved verb. Do not use a technical verb if it is possible to write the same sentence with the words (verbs and other related words) that are approved in the dictionary.

Examples:

> **Non-STE:** If you detect broken wires, repair them.

("Detect" is not approved and cannot be a technical verb in this context.)

> **STE:** If you find broken wires, repair them.

But you can write:

("Detect" is the correct technical verb in this context.)

If you must use technical verbs, use only technical verbs that are correct in your context. Do not use technical verbs that are general or not clear.

Do not use a technical verb if it is not necessary. If it is possible, use a verb that is approved in the dictionary and an applicable technical noun.

"Clamp" is a technical noun, category 1, official parts information. Do not use "clamp" as a technical verb.

"Grease" is a technical noun, category 4, materials, consumables, and unwanted material. Do not use "grease" as a technical verb.

"Wire" is a technical noun, category 1, official parts information. Do not use "wire" as a technical verb.

The dictionary includes some words that, although not approved, can be technical verbs if you can put them in the specified categories.

> **STE:** Enter your password.

("Enter" is a technical verb, category 2 a), computer processes and applications, input and output processes.)

## STE-Code Adaptation

**Rule 1.12** You can use verbs that you can include in a code-domain technical verb category.

A code-domain technical verb is a verb term that refers to a specified operation or process in software development and is applicable to a subject field.

The controlled terminology does not include all code-domain technical verbs because there are too many, and each project or subject field uses different technical verbs.

You can find many of these code-domain technical verbs in your project glossary or terminology database.

STE-Code gives you a list of categories, with examples, to help you:
- Select code-domain technical verbs to put in your project glossary or terminology database.
- Use code-domain technical verbs correctly.

Code-domain technical verbs must obey the same rules as other approved verbs in STE-Code. Refer to section 3.

You can use code-domain technical verbs in procedural and descriptive texts if you can include them in one or more of these four categories.

1. **Development processes**
   Terms that give instructions and information to:
   a) Write and modify code:
      compile, concatenate, import, inject, instantiate, lint, minify, marshal, optimize, polyfill, refactor, resolve, shim, stub, substitute, tokenize, transpile, trace, vectorize
   b) Test and verify code:
      assert, benchmark, debug, fuzz, instrument, mock, profile, snapshot, spy, stub, unit-test
   c) Build and package:
      bundle, deploy, package, publish, release, tag, version
   d) Manage dependencies:
      hoist, install, link, lock, pin, update, upgrade

2. **Computer processes and applications**
   Terms that give instructions and information for:
   a) Input and output processes:
      click, copy, cut, digitize, enter, paste, press, print, scan, swipe, tap, type
   b) User interface and application operations:
      clear, close, delete, deselect, disable, drag, drag and drop, enable, encrypt, erase, filter, hide, highlight, invalidate, maximize, minimize, navigate, open, save, scroll, select, show, sort, store, submit, toggle, validate, zoom in, zoom out
   c) System operations:
      abort, authenticate, authorize, boot, cache, communicate, configure, debug, deserialize, download, format, hydrate, initialize, install, load, log, manage, mount, process, reboot, render, retry, serialize, spawn, synchronize, throttle, update, upgrade, upload

3. **Instructions and information for applicable subject fields**
   Terms that give instructions and information in these contexts:
   a) Algorithmic, mathematical, and data:
      aggregate, bisect, compute, concatenate, convert, count, decode, encode, escape, filter, hash, index, map, merge, normalize, parse, pipeline, precompute, recalculate, reduce, tokenize, transform, validate, verify
   b) Database and storage:
      backup, compact, flush, index, migrate, persist, query, replicate, restore, roll back, seed, shard, upsert, vacuum, write-ahead
   c) Network and communication:
      broadcast, connect, disconnect, establish, forward, handshake, intercept, listen, poll, proxy, reject, resolve, route, send, stream, timeout, tunnel, unsubscribe, webhook
   d) Security and authentication:
      authenticate, authorize, decrypt, decode, encode, encrypt, hash, revoke, salt, sanitize, sign, validate, verify

4. **Legal and licensing terms**
   Terms that give instructions and information only for legal and regulatory texts. For example, licenses, terms of service, contributor agreements, and compliance documents.
   acknowledge, assign, comply with, conform to, disclose, enforce, explain, grant, inform, license, modify, notify, permit, regulate, sign, supersede, waive

The code-domain technical verbs in their related categories are only examples. Rule 1.12 does not give a full list of all possible code-domain technical verbs.

If there is an approved verb in the controlled terminology that accurately gives the instruction or the information, use the approved verb. Do not use a code-domain technical verb if it is possible to write the same sentence with the words (verbs and other related words) that are approved in the controlled terminology.

This adapts the spec principle: just as you must prefer the approved verb "find" over the technical verb "detect" when the context does not require the technical term, you must prefer approved verbs over code-domain technical verbs when the approved verb is sufficient.

If you must use code-domain technical verbs, use only code-domain technical verbs that are correct in your context. Do not use code-domain technical verbs that are general or not clear.

Do not use a code-domain technical verb if it is not necessary. If it is possible, use a verb that is approved in the controlled terminology and an applicable code-domain technical noun.

### Examples

> *Adapted from spec pair:* Non-STE: "If you detect broken wires, repair them."  |  STE: "If you find broken wires, repair them."

> **Non-STE:**
> ```python
> # api/handler.py
> def handle_request(req):
>     # If you detect a null pointer exception in the parser, fix it
>     # before the response returns to the client.
>     try:
>         result = parse(req.body)
>     except NullPointerError as exc:
>         log(exc)
> ```
>
> **STE:**
> ```python
> # api/handler.py
> def handle_request(req):
>     # If you find a null pointer exception in the parser, fix it
>     # before the response returns to the client.
>     try:
>         result = parse(req.body)
>     except NullPointerError as exc:
>         log(exc)
> ```
>
> *Adapted from spec pair: "If you detect broken wires, repair them" → "If you find broken wires, repair them." In the spec, "detect" is not approved and cannot be a technical verb in the general maintenance context — the approved verb "find" must be used. The same principle applies in STE-Code: when describing a general debugging scenario, "detect" is not approved and "find" must be used.*

> **STE:**
> ```python
> # security/ids.py
> def inspect(event):
>     # The intrusion detection system detects unauthorized access attempts
>     # and forwards them to the alert queue.
>     if event.is_unauthorized():
>         alert_queue.put(event)
> ```
>
> *Adapted from spec concept: "detect" becomes permissible as a technical verb in the correct context. In the spec, "detect" can be a technical verb in category 3 c), civil and military operations. In STE-Code, "detect" is a code-domain technical verb (category 3 c), network and communication) when used in a security context where it is the established technical term. The logging statement shows a full IDS handler that uses "detect" precisely.*

> **STE:**
> ```bash
> # scripts/setup.sh
> read -r -p "Enter your API key in the configuration file: " API_KEY
> echo "API_KEY=$API_KEY" >> config/env.cfg
> echo "Save the file and restart the service."
> ```
>
> *Adapted from spec example: "Enter your password" — "Enter" is a technical verb, category 2 a), computer processes and applications, input and output processes. Just as "enter" is a technical verb in the spec, "enter" is a code-domain technical verb in category 2 a) in STE-Code. The word "enter" is not approved in the controlled terminology as a general verb, but it is permitted because it fits the code-domain technical verb category — exactly as the spec permits it.*

> **Non-STE:**
> ```markdown
> ## Operations runbook
> 1. Migrate the database schema to version 3 and then verify the row
>    counts before you open the service to traffic.
> ```
>
> **STE:**
> ```markdown
> ## Operations runbook
> 1. Run the migration of the database schema to version 3 and then check
>    the row counts before you open the service to traffic.
> ```
>
> *Adapted from spec principle: prefer an approved verb with a technical noun over a technical verb when possible. In the spec, you must not use "clamp," "grease," or "wire" as technical verbs when you can use an approved verb with the technical noun. Similarly, "migrate" is a code-domain technical verb (category 3 b), database and storage), but the approved verb "run" with the code-domain technical noun "migration" is a valid alternative. The STE version uses the approved verb "run."*

---

## Code-Domain Explanation

This rule controls which verbs you can use in code documentation. Rule 1.12 applies differently to each documentation type because each type has a different audience and purpose.

### README Files

README files give a high-level description of a project. The audience includes both new users and experienced developers. README files must use approved verbs as the main verb of each sentence. Use code-domain technical verbs only when an approved verb cannot give the same meaning with the same precision.

> **Non-STE:**
> ```markdown
> ## Quick start
> To bootstrap the project, execute `npm install` in the root directory and
> then initiate the development server with `npm run dev` before you open
> http://localhost:3000 in your browser.
> ```
>
> **STE:**
> ```markdown
> ## Quick start
> To start the project, run `npm install` in the root directory and then
> start the development server with `npm run dev` before you open
> http://localhost:3000 in your browser.
> ```
>
> *Principles applied: P12 (canonical synonym table). "Bootstrap" and "initiate" are not approved; "start" is the approved verb. The instruction is a general project setup step, not a technical operation that needs a code-domain technical verb.*

> **Non-STE:**
> ```markdown
> ## Build
> The continuous integration pipeline compiles TypeScript, minifies
> JavaScript, and deploys the build artifacts to the CDN every time you
> push a commit to the main branch.
> ```
>
> **STE:**
> ```markdown
> ## Build
> The continuous integration pipeline compiles TypeScript, minifies
> JavaScript, and deploys the build artifacts to the CDN every time you
> push a commit to the main branch.
> ```
>
> *Principles applied: P12, Rule 1.12 categories 1 a) and 1 c). "Compile," "minify," and "deploy" are all code-domain technical verbs in their correct categories. The sentence describes specific build operations. No approved verb can replace them without losing precision.*

### API Reference Documentation

API documentation describes function signatures, parameters, return values, and side effects. API docs have the most tolerance for code-domain technical verbs because the verbs often match the method names in the code. The principle of one term per concept (Rule 1.11) is important here: if the method is named `serialize()`, the documentation must also use "serialize" to keep consistency.

> **Non-STE:**
> ```markdown
> ### `serialize()`
> This method performs serialization of the object into a byte stream and
> returns the encoded result to the caller.
> ```
>
> **STE:**
> ```markdown
> ### `serialize()`
> This method serializes the object to a byte stream and returns the
> encoded result to the caller.
> ```
>
> *Principles applied: P7, P13. The first version uses the technical noun "serialization" where the technical verb "serializes" is more direct and matches the method name. Do not use a technical verb as a noun or a technical noun as a verb.*

### Docstrings and Inline Comments

Docstrings must be short. Use approved verbs for general operations. Use code-domain technical verbs when the operation is specific to the code domain and an approved verb would make the text longer or less clear.

> **Non-STE:**
> ```python
> def load_user(uid):
>     # Utilize the cache to retrieve the user object, then verify its
>     # validity before returning the response to the router.
>     cached = cache.get(uid)
> ```
>
> **STE:**
> ```python
> def load_user(uid):
>     # Get the user object from the cache, then check that it is valid
>     # before you return the response to the router.
>     cached = cache.get(uid)
> ```
>
> *Principles applied: P1 (approved words only). "Utilize," "retrieve," and "verify" are not approved. "Get," "check," and "return" are approved. The comment describes a general flow, not a specific technical operation.*

### Commit Messages

Commit messages must use the imperative mood. Use approved verbs as the main verb. Code-domain technical verbs can appear as the main verb when the commit describes a specific technical operation that only that verb can name.

> **Non-STE:**
> ```
> Implemented user authentication and authorization for the admin panel
> and added the login route.
> ```
>
> **STE:**
> ```
> Add user authentication and authorization for the admin panel and add
> the login route.
> ```
>
> *Principles applied: P4 (approved verb forms), imperative mood. "Add" is an approved verb. The past tense "Implemented" violates the imperative mood rule for commit messages.*

> **STE:**
> ```
> Refactor the token parser to use a recursive descent algorithm and
> remove the regex fallback.
> ```
>
> *Principles applied: P12, Rule 1.12 category 1 a). "Refactor" is a code-domain technical verb. It names a specific code operation that "change" or "modify" does not capture with the same precision.*

### Error Messages

Error messages must be clear to all users, not only developers. Use approved verbs in error messages that end users see. Use code-domain technical verbs in error messages that only developers see, such as stack traces, debug logs, and internal error codes.

> **Non-STE:** (end-user error dialog)
> ```
> The system failed to instantiate the configuration module due to a
> deserialization failure in the startup sequence.
> ```
>
> **STE:** (end-user error dialog)
> ```
> Could not load the configuration file because its format is not correct.
> Check the file and try again.
> ```
>
> *Principles applied: P6, P10. "Instantiate" and "deserialization" are code-domain technical terms that an end user does not understand. Use approved verbs and plain language for end-user messages.*

> **STE:** (developer error log)
> ```
> Failed to deserialize config.yaml: unexpected token at line 42,
> column 7. Run the schema validator to see the full error report.
> ```
>
> *Principles applied: P12, Rule 1.12 category 2 c). "Deserialize" is a code-domain technical verb for a developer audience. The developer needs the precise technical term to debug the problem.*

---

## Paradigm-Specific Guidance

### Object-Oriented Programming (Java, C++, C#, Python classes)

Object-oriented documentation uses a specific set of code-domain technical verbs that describe class relationships and object lifecycles. These verbs are all in category 1 a) (write and modify code).

| Code-Domain Technical Verb | Meaning | Example |
|---|---|---|
| instantiate | Make an instance of a class | "Instantiate the `UserService` class with the default constructor in the test setup." |
| inherit | Get behavior from a parent class | "The `AdminController` inherits from `BaseController` and reuses its request filter." |
| override | Replace a parent method | "Override the `validate()` method to add custom checks for the email field." |
| extend | Add to a base class or interface | "Extend the `AbstractParser` to make a JSON parser that reads the response body." |
| implement | Give a body to an interface method | "Implement the `Serializable` interface so the object can be written to the cache." |
| encapsulate | Hide internal state | "Encapsulate the connection pool behind a getter method to control access." |
| delegate | Forward a method call to another object | "Delegate the logging to the injected `Logger` instance instead of calling `print` directly." |
| inject | Supply a dependency from outside | "Inject the `Database` dependency through the constructor of the repository class." |

NOTE: Do not use these verbs when an approved verb is sufficient. For example, do not say "The class encapsulates the data" when you can say "The class holds the data."

> **Non-STE:**
> ```java
> // The Session class encapsulates the user record and the token, then
> // exposes them through getter methods.
> public class Session {
>     private User user;
>     private String token;
> }
> ```
>
> **STE:**
> ```java
> // The Session class holds the user record and the token, then gives
> // them through getter methods.
> public class Session {
>     private User user;
>     private String token;
> }
> ```

### Functional Programming (Haskell, Elixir, Clojure, Rust iterators)

Functional programming documentation uses verbs that describe transformations of immutable data. These verbs are in category 3 a) (algorithmic, mathematical, and data).

| Code-Domain Technical Verb | Meaning | Example |
|---|---|---|
| compose | Combine functions into a pipeline | "Compose the `parse` and `validate` functions into a single handler." |
| curry | Change a multi-argument function to a chain of single-argument functions | "Curry the `add` function for partial application in the reducer." |
| map | Apply a function to each element | "Map the `toUpperCase` function over the list of labels." |
| reduce | Combine elements with a binary operation | "Reduce the list with the `sum` function to get the total count." |
| fold | Combine elements with an initial value | "Fold the collection from the left with a seed value of 0 to compute the average." |
| recurse | Call a function from within itself | "Recurse on the tail of the list until the base case returns an empty list." |
| memoize | Cache function results | "Memoize the `fibonacci` function to prevent recomputation on repeated calls." |
| lift | Move a function into a monadic context | "Lift the pure function into the `IO` monad so it can read the config file." |

NOTE: "Map" and "reduce" are code-domain technical verbs in category 3 a). Do not confuse them with the approved verb "map" (to show a relationship) or "reduce" (to make smaller). The context must make the meaning clear.

### Procedural Programming (C, Go, Bash)

Procedural documentation uses verbs that describe memory management, control flow, and system-level operations. These verbs are in categories 2 c) and 3 a).

| Code-Domain Technical Verb | Meaning | Example |
|---|---|---|
| allocate | Get a block of memory | "Allocate a buffer of 1024 bytes on the heap before you read the socket." |
| deallocate | Release a block of memory | "Deallocate the buffer before the function returns to prevent a memory leak." |
| dereference | Get the value at a pointer address | "Dereference the pointer to get the struct value from the response." |
| flush | Write buffered data to output | "Flush the output buffer after each write so the client receives the data." |
| signal | Send a signal to a process | "Signal the worker process to stop when the shutdown hook fires." |

> **Non-STE:**
> ```c
> /* You must free the memory that you malloced earlier in the function
>    before you return. */
> free(buf);
> ```
>
> **STE:**
> ```c
> /* You must deallocate the memory that you allocated earlier in the
>    function before you return. */
> free(buf);
> ```
>
> *Principles applied: P11 (one term per concept). "Free" and "malloc" are C standard library function names. In documentation, use the code-domain technical verbs "allocate" and "deallocate" (category 2 c) for consistency across languages. The function names "malloc" and "free" are technical code nouns (Rule 1.5).*

### Declarative Programming (SQL, Terraform, Kubernetes YAML)

Declarative documentation uses verbs that describe the desired state of a system. The documentation describes what the configuration does, not how the system makes it happen.

| Code-Domain Technical Verb | Meaning | Example |
|---|---|---|
| provision | Make infrastructure available | "This resource provisions an AWS EC2 instance with the `web` tag." |
| converge | Bring actual state to desired state | "The controller converges the cluster to the declared configuration on every reconcile loop." |
| reconcile | Compare actual state to desired state | "The operator reconciles the custom resource every 30 seconds and reports drift." |
| apply | Put a configuration into effect | "Apply the Terraform plan to provision the resources in the `staging` workspace." |
| destroy | Remove provisioned infrastructure | "Destroy the stack to remove all resources and free the allocated IP addresses." |

> **Non-STE:**
> ```hcl
> # Terraform will make an S3 bucket for you when you execute
> # `terraform apply` in the root module.
> resource "aws_s3_bucket" "assets" {
>   bucket = "my-assets"
> }
> ```
>
> **STE:**
> ```hcl
> # Terraform provisions an S3 bucket when you apply the configuration
> # in the root module.
> resource "aws_s3_bucket" "assets" {
>   bucket = "my-assets"
> }
> ```
>
> *Principles applied: P12, Rule 1.12 category 3 a) and 2 c). "Provision" is a code-domain technical verb (category 3 a), algorithmic and data, or category 2 c), system operations). "Apply" is a code-domain technical verb (category 2 c). The approved verb "make" is not precise enough.*

### Systems Programming (Rust ownership, C memory, embedded)

Systems documentation uses verbs that describe ownership, borrowing, and lifetime management. These verbs are in category 2 c) and category 3 a).

| Code-Domain Technical Verb | Meaning | Example |
|---|---|---|
| borrow | Get a reference without taking ownership | "Borrow the vector immutably for the duration of the loop to read each item." |
| own | Hold exclusive control of a value | "The `String` struct owns its heap-allocated buffer and frees it on drop." |
| drop | Run the destructor and release resources | "The value drops when it goes out of scope at the end of the function." |
| move | Transfer ownership to another binding | "Move the value into the closure so the spawned thread can use it." |
| pin | Prevent a value from moving in memory | "Pin the future to the heap before you poll it in the runtime." |
| acquire | Get exclusive access to a lock | "Acquire the mutex before you access the shared state in the worker thread." |
| release | Give up exclusive access to a lock | "Release the lock when the critical section is complete to unblock the next worker." |

> **Non-STE:**
> ```rust
> // You need to clone the string to avoid a borrow checker violation when
> // you return the slice.
> let s = self.data.clone();
> ```
>
> **STE:**
> ```rust
> // You must clone the string to prevent a borrow conflict when you
> // return the slice.
> let s = self.data.clone();
> ```
>
> *Principles applied: P10, P12. "Violation" is a legal term (category 4), not a systems programming term. "Conflict" or "error" is more correct for a compiler message.*

---

## Extended Examples

### Example Group A: General Verb vs. Code-Domain Technical Verb

> **Non-STE:**
> ```bash
> # deploy.sh
> # The script initiates a connection to the database and then commences
> # the data migration process before it starts the health check.
> ```
>
> **STE:**
> ```bash
> # deploy.sh
> # The script connects to the database and then migrates the data before
> # it starts the health check.
> ```
>
> *Principles applied: P12 (canonical synonym table + Rule 1.12). "Connect" and "migrate" are code-domain technical verbs (categories 3 c and 3 b). "Initiates" and "commences" are not approved and are not technical verbs in any category. The STE version uses the code-domain technical verbs directly, which is more concise and precise.*

### Example Group B: Technical Noun Used Incorrectly as a Verb

> **Non-STE:**
> ```yaml
> # ci.yml
> # You must docker the application before you ship it to the registry
> # with the release tag.
> ```
>
> **STE:**
> ```yaml
> # ci.yml
> # You must containerize the application before you ship it to the
> # registry with the release tag.
> ```
>
> *Principles applied: P7 (do not use technical nouns as verbs), P8 (use standard technical nouns). "Docker" is a brand name and a technical code noun (Rule 1.5). It is not a verb. "Containerize" is a code-domain technical verb (category 1 c), build and package). If "containerize" is not acceptable in your project glossary, use "package the application in a container" — the approved verb "package" with the technical noun "container."*

> **Non-STE:**
> ```markdown
> ## Contributor guide
> Git the changes and then push them to the remote before you open the
> pull request.
> ```
>
> **STE:**
> ```markdown
> ## Contributor guide
> Commit the changes and then push them to the remote before you open the
> pull request.
> ```
>
> *Principles applied: P7. "Git" is a tool name and a technical code noun. It is not a verb. "Commit" is a code-domain technical verb (category 2 b), user interface and application operations, when used in the version-control context).*

### Example Group C: When an Approved Verb Is Sufficient

> **Non-STE:**
> ```markdown
> ## Test plan
> Execute the test suite to verify that the API endpoint returns the
> correct status code and the response body is valid.
> ```
>
> **STE:**
> ```markdown
> ## Test plan
> Run the test suite to check that the API endpoint returns the correct
> status code and the response body is valid.
> ```
>
> *Principles applied: P1, P12 (canonical synonym table). "Execute" and "verify" are not approved. "Run" and "check" are approved. The operations are general testing steps. No code-domain technical verb category is needed. Use the approved verbs.*

### Example Group D: When Only the Code-Domain Technical Verb Works

> **Non-STE:**
> ```python
> def convert(text):
>     # The convert() function takes a string and turns it into a number,
>     # then does an operation on each item of the list and gives back a
>     # new list.
>     ...
> ```
>
> **STE:**
> ```python
> def convert(text):
>     # The convert() function parses a string to an integer, then maps
>     # the transformation over the list and returns a new list.
>     ...
> ```
>
> *Principles applied: P12, Rule 1.12 categories 3 a) and 3 a). "Parse" and "map" are code-domain technical verbs. "Turns it into" and "does an operation on each item" are imprecise and wordy. The code-domain technical verbs are necessary for precision.*

### Example Group E: API Documentation — Method Name Consistency

> **Non-STE:**
> ```yaml
> # openapi.yaml
> post:
>   description: >
>     This endpoint performs the creation of a new user record in the
>     database and returns the identifier of the created resource.
> ```
>
> **STE:**
> ```yaml
> # openapi.yaml
> post:
>   description: >
>     This endpoint makes a new user in the database and returns the
>     identifier of the new resource.
> ```
>
> *Principles applied: P13 (do not use technical verbs as nouns), P1 (approved words). "Performs the creation" uses the technical noun "creation" instead of the approved verb "makes." Do not use the nominalized form of a verb when the verb form is available and approved.*

> **Non-STE:**
> ```python
> def serialize(self) -> bytes:
>     """Returns the serialization of this object as a byte string for
>     transport."""
> ```
>
> **STE:**
> ```python
> def serialize(self) -> bytes:
>     """Serializes this object and returns the result as a byte string
>     for transport."""
> ```
>
> *Principles applied: P13. The method is named "serialize" (a code-domain technical verb). The documentation must use the same verb form to keep one term per concept (Rule 1.11). Do not switch to the noun "serialization."*

### Example Group F: Commit Message — Imperative Mood with Technical Verbs

> **Non-STE:**
> ```
> Deployed the new authentication middleware and configured the rate
> limiter for the public API.
> ```
>
> **STE:**
> ```
> Deploy the new authentication middleware and set the rate limiter for
> the public API.
> ```
>
> *Principles applied: P4 (imperative mood for commit messages), P12 (canonical synonym table). "Deploy" is a code-domain technical verb (category 1 c). "Set" is an approved verb. "Configured" uses the wrong mood (past indicative instead of imperative) and "configure" is a code-domain technical verb that can be replaced by "set" in this context.*

---

## Edge Cases

### Edge Case 1: Framework or Tool Name That Is Also a General Verb

Some framework names are also common English verbs. For example, "Express" (the Node.js framework) is also a general verb meaning "to show" or "to state." "Go" (the programming language) is also a general verb. "C" (the language) sounds like "see."

RULE: When a framework or tool name is also a general verb, always use the framework name as a technical code noun (Rule 1.5). Add a qualifier if the context does not make the meaning clear.

> **Non-STE:**
> ```javascript
> // Express the route handler as a middleware function so the request
> // passes through the logger first.
> app.use(logger);
> ```
>
> **STE:**
> ```javascript
> // Write the route handler as an Express middleware function so the
> // request passes through the logger first.
> app.use(logger);
> ```
>
> *Principles applied: P6, Rule 1.5. "Express" as a verb meaning "to state" is not approved. As a proper noun, "Express" is a technical code noun. The STE version makes the meaning clear by adding the framework name as a qualifier.*

### Edge Case 2: Code Keyword That Conflicts with an Approved Verb

Some programming language keywords are the same as approved STE-Code verbs. For example, `return` (keyword) vs. "return" (approved verb meaning "to give back"). `import` (keyword) vs. "import" (code-domain technical verb, category 1 a). `class` (keyword) vs. "class" (technical code noun).

RULE: When a code keyword and an approved verb have the same spelling, use context to make the meaning clear. In inline code formatting, the keyword appears in monospace. In prose, the approved verb or technical verb appears in normal text.

> **Non-STE:**
> ```javascript
> // The function returns a promise that you must await to get the result
> // from the network call.
> async function fetchUser() { /* ... */ }
> ```
>
> **STE:**
> ```javascript
> // The function returns a `Promise` that you must `await` to get the
> // result from the network call.
> async function fetchUser() { /* ... */ }
> ```
>
> *Principles applied: P6, Rule 1.5. "Returns" is an approved verb. "Promise" and "await" are JavaScript keywords and technical code nouns. Use monospace formatting for keywords to distinguish them from approved verbs.*

> **Non-STE:**
> ```python
> # Import the module at the top of the file, then return the configured
> # instance to the caller.
> ```
>
> **STE:**
> ```python
> # Import the module at the top of the file. Then return the set
> # instance to the caller.
> ```
>
> *Principles applied: P12, Rule 1.12 category 1 a). "Import" is a code-domain technical verb. "Return" is an approved verb. "Configured" is a code-domain technical verb that can be replaced by the approved verb "set" in this context.*

### Edge Case 3: Generated Code and Automated Documentation

Generated code and auto-generated documentation do not always obey STE-Code rules. Generated code comes from tools (compilers, code generators, OpenAPI spec generators, protobuf compilers). You cannot control the word choices in generated output.

RULE: Rule 1.12 applies to documentation that a human writes. Generated code and auto-generated documentation are exempt, but you must write any surrounding explanation in STE-Code. When you refer to a generated symbol name, treat it as a technical code noun (Rule 1.5).

> **Non-STE:**
> ```markdown
> ## Integration note
> The generated client library exposes a `serializeToJson()` method that
> leverages the native JSON encoder to build the payload.
> ```
>
> **STE:**
> ```markdown
> ## Integration note
> The generated client library has a `serializeToJson()` method that
> uses the native JSON encoder to build the payload.
> ```
>
> *Principles applied: P1, P12. "Exposes" and "leverages" are not approved. "Has" and "uses" are approved. The method name `serializeToJson()` is a technical code noun — do not change it even though "serialize" is a code-domain technical verb. The method name is generated and fixed.*

### Edge Case 4: CLI Command Names as Verbs

Command-line interface (CLI) commands often use technical verbs as their names. For example, `git commit`, `docker build`, `kubectl apply`, `npm install`. When you document CLI commands, the command name is a technical code noun. The verb that describes the action can be an approved verb.

> **Non-STE:**
> ```markdown
> ## Operations guide
> Execute `docker build` to containerize the application, then execute
> `docker push` to upload the image to the registry.
> ```
>
> **STE:**
> ```markdown
> ## Operations guide
> Run `docker build` to containerize the application, then run
> `docker push` to upload the image to the registry.
> ```
>
> *Principles applied: P1, P12. "Execute" is not approved. "Run" is approved. The commands `docker build` and `docker push` are technical code nouns. "Containerize" and "upload" are code-domain technical verbs (categories 1 c and 2 c).*

### Edge Case 5: Multi-Word Technical Verbs

Some code-domain technical verbs have more than one word. For example, "roll back" (category 3 b), "drag and drop" (category 2 b), "zoom in" and "zoom out" (category 2 b), "write-ahead" (category 3 b). These multi-word verbs are permitted as single lexical units. Do not split them or substitute a different verb.

RULE: Keep the multi-word technical verb as one unit. Do not insert words between its parts. Use the full form every time you refer to the operation.

> **Non-STE:**
> ```markdown
> ## Migration runbook
> You must roll the database migration back if the validation of the
> schema fails during the upgrade.
> ```
>
> **STE:**
> ```markdown
> ## Migration runbook
> You must roll back the database migration if the check of the schema
> fails during the upgrade.
> ```
>
> *Principles applied: P11 (one term per concept), P1 (approved words). "Roll back" is a single code-domain technical verb (category 3 b). Do not split it with an object. "Validation" is a technical noun form; use the approved verb "check" instead. In English, phrasal verbs can be split ("roll it back"), but STE-Code does not permit splitting of multi-word technical verbs to prevent ambiguity.*

---

## Cross-References

This rule connects to several other STE-Code rules. Read these rules together to make sure that your documentation obeys all of them.

| Related Rule | Relationship to Rule 1.12 |
|---|---|
| **Rule 1.1** — Use approved words from the dictionary | You must try approved words before you use a code-domain technical verb. If an approved verb gives the same meaning, you must use the approved verb. |
| **Rule 1.2** — Use words only as their specified part of speech | A word that is approved as a noun cannot be a code-domain technical verb. Check the controlled terminology before you use a word as a verb. |
| **Rule 1.5** — Technical code nouns are allowed | Tool names, framework names, and CLI commands are technical code nouns (not verbs). Do not use them as code-domain technical verbs. |
| **Rule 1.7** — Do not use technical nouns as verbs | This is the inverse of Rule 1.12. Rule 1.7 prevents you from using "Docker" as a verb. Rule 1.12 permits "containerize" as a code-domain technical verb. |
| **Rule 1.11** — One term per concept | When you choose a code-domain technical verb, use it the same way everywhere. Do not use "serialize" in one file and "marshal" in another for the same concept. |
| **Rule 1.13** — Do not use technical verbs as nouns | If a word is a code-domain technical verb, do not use its nominalized form. Prefer "serialize" (verb) over "serialization" (noun) when the sentence calls for a verb. Use the approved verb with the technical noun when the sentence calls for a noun. |
| **Section 3** — Verb rules (tense, mood, voice) | Code-domain technical verbs must obey the same tense, mood, and voice rules as approved verbs. Use the imperative mood for procedures. Use the active voice. Do not use the "-ing" form as the main verb. |

---

## Grammar Notes

### Code-Domain Technical Verbs and the Imperative Mood

Procedural documentation (instructions, setup guides, API usage examples) must use the imperative mood. Code-domain technical verbs in the imperative mood follow the same rules as approved verbs.

> **STE:** Compile the source files before you run the tests.
> *"Compile" is a code-domain technical verb (category 1 a) in the imperative mood.*

> **STE:** Deploy the application to the staging environment.
> *"Deploy" is a code-domain technical verb (category 1 c) in the imperative mood.*

Do not use the "-ing" form of a code-domain technical verb as the main verb of a procedural sentence.

> **Non-STE:** The runbook step reads: "Compiling the source files and then deploying to staging before you run the smoke tests."
>
> **STE:** The runbook step reads: "Compile the source files. Then deploy the application to staging before you run the smoke tests."
>
> *Principles applied: P4 (approved verb forms). The "-ing" form is not an approved verb form for procedures. Use the imperative form.*

### Code-Domain Technical Verbs in Descriptive Texts

Descriptive documentation (architecture overviews, design documents, project descriptions) uses the indicative mood. Code-domain technical verbs in the indicative mood follow standard subject-verb agreement.

> **STE:** The build system compiles TypeScript, minifies JavaScript, and deploys static assets.
> *All three verbs ("compiles," "minifies," "deploys") are code-domain technical verbs in the third-person singular indicative form.*

> **STE:** The database engine indexes the new columns during the migration.
> *"Indexes" is a code-domain technical verb (category 3 b) in the indicative mood.*

### Prefer the Active Voice

Use the active voice for code-domain technical verbs. The passive voice is permitted in descriptive texts when the agent is not important, but the active voice is always clearer.

> **Non-STE:** The design document says: "The configuration file is parsed by the bootstrap module during initialization and the result is cached."
>
> **STE:** The design document says: "The bootstrap module parses the configuration file when it starts and caches the result."
>
> *Principles applied: active voice, P12 (canonical synonym table). "Parses" is a code-domain technical verb (category 3 a). "Starts" is an approved verb. The passive construction "is parsed by" is wordier and less direct than the active "parses."*

### Code-Domain Technical Verbs and the Infinitive

When a code-domain technical verb follows another verb, use the full infinitive form ("to" + verb). Do not drop the "to."

> **Non-STE:** The usage note reads: "You need serialize the object before you send it to the client in the response."
>
> **STE:** The usage note reads: "You must serialize the object before you send it to the client in the response."
>
> *Principles applied: P4 (approved verb forms), grammar. "Need" is not approved; use "must." The full infinitive "to serialize" is required after some constructions, but "must" takes the bare infinitive ("must serialize"), which is correct.*

### Tense Restrictions for Code-Domain Technical Verbs

Code-domain technical verbs obey the same tense restrictions as approved verbs. Use only the tenses that STE-Code permits:

- Imperative (for procedures): "Compile the source files."
- Simple present (for descriptive texts): "The compiler optimizes the output."
- Simple past (for reporting completed actions): "The test suite found three failures."
- Simple future (for results and outcomes): "The deployment will complete in five minutes."

Do not use the present perfect, past perfect, or continuous tenses with code-domain technical verbs.

> **Non-STE:** The status report reads: "The system has been indexing the database for ten minutes and the query latency keeps increasing."
>
> **STE:** The status report reads: "The system indexes the database. The index operation started ten minutes ago and the query latency keeps increasing."
>
> *Principles applied: P4, tense restrictions. The present perfect continuous "has been indexing" is not permitted. Use the simple present with a time reference in a separate sentence.*

---

## See also

> **See also:** Rule 1.1 — Use approved words from the dictionary
> **See also:** Rule 1.2 — Use words only as their specified part of speech
> **See also:** Rule 1.5 — Technical code nouns are allowed
> **See also:** Rule 1.7 — Do not use technical nouns as verbs
> **See also:** Rule 1.11 — One term per concept
> **See also:** Rule 1.13 — Do not use technical verbs as nouns
> **See also:** Section 3 — Verb rules (tense, mood, voice)

---

<!-- a-sec1-rule1.13.md -->

# Rule 1.13 — Do Not Use Technical Verbs as Nouns

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.13](ste-code/grouped/), Rule 1.13

## Original Rule

**Rule 1.13** Do not use technical verbs as nouns.

In English, words that look the same do not always have the same function in a sentence. Use technical verbs only as verbs, not as nouns.

Example:

> **STE:** Enter your password.

("Enter" is a technical verb, category 2 a), computer processes and applications, input and output processes.)

Words that can be technical verbs and technical nouns

In some contexts, the same word can be a technical verb and a technical noun. This condition occurs when you can put this word in a technical verb category (rule 1.12) and in a technical noun category (rule 1.5).

> **STE:** There are two methods to plate the ring nut (2).

("Plate" is a technical verb, category 1 c), manufacturing processes, attach material.)

## STE-Code Adaptation

**Rule 1.13** Do not use code-domain technical verbs as nouns.

> **See also:** Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category
> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category
> **See also:** Rule 1.7 — Do Not Use Technical Nouns as Verbs

In English, words that look the same do not always have the same function in a sentence. Use code-domain technical verbs only as verbs, not as nouns. If you need to use a word as a noun, find an approved noun or a code-domain technical noun that has the equivalent meaning.

This adapts the spec principle: just as you cannot use "enter" as a noun in STE (you must use it only as a verb, as in "Enter your password"), you cannot use code-domain technical verbs as nouns in STE-Code.

In some contexts, the same word can be a code-domain technical verb and a code-domain technical noun. This condition occurs when you can put this word in a code-domain technical verb category (rule 1.12) and in a code-domain technical noun category (rule 1.5). This adapts the spec example where "plate" can be a technical verb (a manufacturing process) — the spec explicitly acknowledges that some words can belong to both category systems.

### Code-Domain Explanation

This rule applies across all forms of code documentation. Each documentation type has different risk patterns for verb-as-noun misuse.

**README files** — README files frequently describe project workflows in noun-heavy prose. A common error is nominalizing build and deployment verbs: "Do a build of the project" instead of "Build the project." README files must use imperative verb forms for setup instructions.

**API documentation** — API reference docs describe operations that return results. Do not nominalize the operation: "The function does a parse of the input string" must become "The function parses the input string." However, when the API returns a named artifact (for example, a `Build` object, a `Deployment` resource), the noun form is a technical noun (rule 1.5), not a misused verb.

**Docstrings and inline comments** — Docstrings describe what a function or method does. Use the verb form: "Compiles the source files" not "Does a compile of the source files." Comments that explain why a line exists must use verb forms for actions: "// Retry the connection" not "// A retry of the connection."

**Commit messages** — Commit messages describe what the commit does. The conventional commit format uses the imperative: "Add login endpoint" not "Addition of login endpoint." The commit subject line is a command — it tells the codebase what to do. Using a verb as a noun in a commit message hides the action.

**Error messages** — Error messages must describe what failed and what to do. Use verb forms: "Failed to compile module 'auth'" not "Compile of module 'auth' failed." The reader needs to know the action that did not complete.

**Log output** — Log lines describe events. Use verb forms for actions: "Deploy started for release v2.1.0" not "Start of deploy for release v2.1.0." Log aggregation tools parse action verbs more reliably than nominalized forms.

### Paradigm-Specific Guidance

The verb-as-noun risk varies by programming paradigm because each paradigm has a different set of common technical verbs.

**Object-Oriented (Java, C++, C#, Python classes)**

OOP documentation frequently nominalizes instantiation and lifecycle verbs. Common violations:

- "Create an instantiate of the class" → "Instantiate the class"
- "Do an initialize of the service" → "Initialize the service"
- "Call the dispose method" → "The dispose method" can be correct if "dispose" is a method name (technical noun, rule 1.5). The instruction must say "Call the dispose method," not "Do a dispose."

OOP design patterns use noun-heavy language naturally (Factory, Builder, Observer). These pattern names are code-domain technical nouns (rule 1.5), not verbs used as nouns. Distinguish carefully: "Use the Builder to construct the object" (Builder = technical noun, construct = approved verb) versus "Do a build of the object" (build = misused verb).

**Functional (Haskell, Elixir, Clojure, Rust)**

Functional programming documentation often nominalizes transformation verbs. Common violations:

- "Do a map over the list" → "Map over the list" or "Apply the map function to the list"
- "Do a filter of the collection" → "Filter the collection"
- "Do a reduce on the array" → "Reduce the array"

When a function name is also a verb (map, filter, reduce, fold, compose, curry), use the word as a verb in instructions and as a function name (technical noun) in type signatures. In type signatures, "map" is a function reference (technical noun, rule 1.5). In instructions, "map" is a verb (technical verb, rule 1.12).

**Procedural (C, Go, Bash)**

Procedural code documentation frequently nominalizes memory and I/O verbs. Common violations:

- "Do an allocate of memory" → "Allocate memory"
- "Do a read from the file descriptor" → "Read from the file descriptor"
- "Do a write to the buffer" → "Write to the buffer"
- "Make a copy of the struct" → "Copy the struct"

C and Go use short, action-oriented function names (malloc, read, write, copy, send, recv). In documentation, use these as verbs: "malloc allocates memory on the heap" not "malloc does an allocation."

**Declarative (SQL, Terraform, Kubernetes YAML)**

Declarative documentation describes desired state. The configuration file declares what must exist, but the documentation that explains how to write the configuration uses imperative verbs. Common violations:

- "Do an apply of the manifest" → "Apply the manifest"
- "Do a plan of the infrastructure" → "Plan the infrastructure" or "Run `terraform plan`"
- "Do a select from the table" → "Select from the table" or "Run a SELECT query"

In SQL documentation, SELECT, INSERT, UPDATE, and DELETE are keyword names (technical nouns, rule 1.5). The instruction "Select all rows from the users table" uses "select" as a verb (technical verb, rule 1.12). Both uses are correct because the word fits both category systems.

**Systems (Rust ownership, C memory)**

Systems documentation describes resource management and safety guarantees. Common violations:

- "The drop of the guard happens at end of scope" → "The guard drops at end of scope"
- "The borrow of the reference prevents mutation" → "The reference borrow prevents mutation" or "The borrow prevents mutation" (borrow as technical noun, rule 1.5, when referring to the Rust borrow concept)
- "Do a clone of the Arc" → "Clone the Arc"

Rust documentation has an approved exception: the borrow checker is a named system component (technical noun, rule 1.5). "The borrow" as a concept name is correct. But "do a borrow" as an instruction is wrong — use "Borrow the value."

### Examples

> *Adapted from spec pair:* Non-STE: nominalized technical verb — for example, "Do an enter of the password" (enter used as a noun) | STE: "Enter your password." (enter used only as a verb, ASD-STE100 Rule 1.13). The spec's parallel dual-category case is "plate": "There are two methods to plate the ring nut (2)" — plate used as a technical verb, while the same word can also fit a technical noun category.

> **Non-STE:** The `build` job does a compile of the source files, then it starts the unit tests.
>
> **STE:** The `build` job compiles the source files, then it starts the unit tests.

```
# Non-STE — README.md (Build section)
Run `npm run build`. The script does a compile of the source files
and then starts the dev server.

# STE — README.md (Build section)
Run `npm run build`. The script compiles the source files
and then starts the dev server.
```

> *Adapted from spec example: "Enter your password" — "enter" must be used only as a verb. Just as you cannot use "enter" as a noun in STE, you cannot use "compile" as a noun in STE-Code. "Compile" is a code-domain technical verb (category 1 a), development processes, write and modify code). The non-STE version uses "compile" as a noun, which is not permitted. The STE version uses "compile" correctly as a verb.*

> **Non-STE:** The merge of the feature branch caused a conflict in the `auth` module and blocked the release.
>
> **STE:** The merge operation of the feature branch caused a conflict in the `auth` module and blocked the release.

```
# Non-STE — CHANGELOG.md
- The merge of the feature branch caused a conflict in the auth module.

# STE — CHANGELOG.md
- The merge operation of the feature branch caused a conflict in the auth module.
```

> *Adapted from spec principle: technical verbs must be used only as verbs. "Merge" is a code-domain technical verb (category 1 c), development processes, build and package). The non-STE example uses "merge" as a noun. The STE version uses "merge" as an adjective that is part of the code-domain technical noun "merge operation."*

> **STE:** Run the deploy script before you switch the load balancer to the new version.
>
> **STE:** The deploy completed successfully and all health checks passed.

("Deploy" is a code-domain technical verb, category 1 c), development processes, build and package.)

```
# STE — runbook.md
Run the deploy script before you switch the load balancer to the new version.
The deploy completed successfully and all health checks passed.
```

> *Adapted from spec example: "There are two methods to plate the ring nut (2)" — "plate" can be both a technical verb and a technical noun. Just as "plate" in the spec can be a technical verb (category 1 c), attach material) and also a technical noun (a different context), "deploy" can be both a code-domain technical verb (category 1 c), build and package) and a code-domain technical noun (category 5, infrastructure, deployment, and platforms). In the second example, "deploy" refers to a deployment event or process as a noun — it fits into a code-domain technical noun category in the same way "plate" fits into a technical noun category in the spec.*

> **Non-STE:** If the error rate stays above five percent, execute a rollback of the migration.
>
> **STE:** If the error rate stays above five percent, roll back the migration.

```
# Non-STE — incident-runbook.md
If the error rate stays above five percent, execute a rollback of the migration.

# STE — incident-runbook.md
If the error rate stays above five percent, roll back the migration.
```

> *Principle applied: P13 — Do not use technical verbs as nouns. "Rollback" is a code-domain technical verb (category 3 b), database and storage). The non-STE version nominalizes "rollback" with a light verb "Execute." The STE version uses "roll back" as the main verb of the sentence — the approved verb "roll" plus the particle "back." If the project uses "rollback" as a compound noun (category 18, database and storage), the STE version "Run the rollback of the migration" is also correct because "rollback" then fits a technical noun category.*

> **Non-STE:** The import of the module takes approximately ten seconds on a cold cache.
>
> **STE:** The import operation for the module takes approximately ten seconds on a cold cache.

```
# Non-STE — src/loader.ts
/**
 * The import of the module takes approximately ten seconds on a cold cache.
 */

# STE — src/loader.ts
/**
 * The import operation for the module takes approximately ten seconds on a cold cache.
 */
```

> *Principle applied: P13 — Do not use technical verbs as nouns, P1 — Use approved words from the STE-Code dictionary. "Import" is a code-domain technical verb (category 1 a), development processes, write and modify code). In the non-STE version, "import" is used as a noun. The STE version replaces it with the approved noun "operation" modified by "import" as an adjective. An alternative STE version "Importing the module takes approximately ten seconds" uses the gerund form — gerunds are permitted in descriptive text when they describe an ongoing process, but avoid them as main verbs in procedural sentences (refer to Section 3 grammar rules).*

> **Non-STE:** Make a commit of your changes before you switch branches.
>
> **STE:** Commit your changes before you switch branches.

```
# Non-STE — CONTRIBUTING.md
Make a commit of your changes before you switch branches.

# STE — CONTRIBUTING.md
Commit your changes before you switch branches.
```

> *Principle applied: P13 — Do not use technical verbs as nouns, P4 — Use only approved verb forms. "Commit" is a code-domain technical verb (category 2 c), system operations). The non-STE version wraps "commit" in a light verb construction "Make a commit." The STE version uses "commit" directly as the main imperative verb. In Git documentation, "a commit" as a noun (referring to a snapshot object) is correct because it is a code-domain technical noun (category 4, data structures) — this is the dual-category exception from rule 1.5 and rule 1.12.*

### Edge Cases

**Framework names that are verbs**

Some frameworks and tools have names that are also verbs. For example, React, Build (a build tool), Make (a build system), Log (a logging library), Split (an A/B testing tool). When the word refers to the tool or framework, it is a code-domain technical noun (rule 1.5) and can be used as a noun:

> **STE:** Install React in your project.
> **STE:** Make uses a Makefile to define build targets.

When the same word describes an action, it is a verb and must be used as a verb:

> **STE:** The component reacts to state changes.
> **STE:** The tool makes an executable from the source files.

Always capitalize framework names when they are proper nouns to distinguish them from the verb form.

**Git subcommands used as nouns**

Git documentation frequently uses subcommand names as both verbs and nouns. The subcommand name is a technical noun (it names a Git operation). The instruction to perform the operation uses the verb form:

> **STE:** Run `git rebase` to integrate the changes. (rebase = technical noun, a Git subcommand)
> **STE:** Rebase your branch onto main. (rebase = technical verb)

Both forms are correct if the word fits both category systems (rule 1.12 and rule 1.5). The dual use is the same pattern as the spec's "plate" example.

**Log and CLI tool output**

Generated output from tools, compilers, and linters is quoted text (technical noun category 10, rule 1.5). You cannot change the grammar of generated output. If a compiler emits "Build failed: compile error in module auth," the message contains "compile" as a noun. This is quoted text and does not violate rule 1.13 because you did not write the message.

When you summarize the tool output in your own documentation, apply rule 1.13:

> **STE:** The compiler could not compile module "auth."
> **Non-STE:** The compiler reported a compile error in module "auth."

The non-STE version uses "compile" as a noun ("a compile error"). The STE version uses "compile" as a verb ("could not compile"). If "compile error" is an established term in your project glossary, it can be a compound technical noun (rule 1.5).

**Docker and Kubernetes resource names**

Container orchestration tools use resource names that are verb-derived nouns. For example, a Kubernetes "Deployment" resource, a Docker "Build" stage. These are code-domain technical nouns (rule 1.5, category 5 — infrastructure, deployment, and platforms) because they name specific API resources. Use them as nouns:

> **STE:** The Deployment has three replicas.
> **STE:** The Build stage runs before the test stage.

When you describe the action, use the verb form:

> **STE:** Deploy the application to the cluster.
> **STE:** Build the Docker image from the Dockerfile.

**The "-ing" gerund as a noun substitute**

Technical writers sometimes use gerunds (-ing forms) as nouns to avoid the verb-as-noun violation: "The compiling of the source files takes ten seconds." While this avoids using "compile" as a noun, gerunds as sentence subjects can make text less direct. Prefer the verb form with a dummy subject or the imperative:

> **STE:** Compiling the source files takes ten seconds. (descriptive — correct but less direct)
> **STE:** It takes ten seconds to compile the source files. (preferred for descriptive text)

In procedural text, use the imperative verb directly:

> **STE:** Compile the source files. (procedural — preferred)

### Cross-References

This rule works with a network of related rules. Violations of rule 1.13 often trace to a misunderstanding of the category distinction.

| Rule | Relationship |
|------|-------------|
| **Rule 1.12** — You Can Use Verbs That You Can Include in a Technical Verb Category | Rule 1.12 defines which verbs are "technical verbs." Rule 1.13 constrains how you can use them. A word that does not fit a technical verb category under rule 1.12 cannot be misused as a noun because it is not a technical verb at all — use an approved verb instead. |
| **Rule 1.5** — You Can Use Words That You Can Include in a Technical Noun Category | Rule 1.5 defines which nouns are "technical nouns." When a word fits both a technical verb category (rule 1.12) and a technical noun category (rule 1.5), rule 1.13 permits dual use — just as the spec permits "plate" as both verb and noun. |
| **Rule 1.7** — Do Not Use Technical Nouns as Verbs | Rule 1.7 is the inverse of rule 1.13. Where rule 1.13 prevents verb→noun conversion, rule 1.7 prevents noun→verb conversion. Both rules enforce the principle that a word's category determines its grammatical role. |
| **Rule 1.4** — Use Only Approved Verb Forms and Adjective Forms | Rule 1.4 restricts which verb forms are permitted. When a technical verb is nominalized into a noun (violating rule 1.13), the noun form is often an unapproved derivation. Fixing the violation restores the approved verb form. |
| **Rule 1.10** — No Slang, Jargon, or Regional Terms | Nominalized technical verbs often become project-specific jargon ("a deploy," "a lint," "a hotfix"). If the noun form is not in a technical noun category (rule 1.5), the usage is jargon and violates both rule 1.13 and rule 1.10. |
| **STE-Code Dictionary** — Approved Words and Technical Verb/Noun Lists | The controlled terminology defines approved verbs and their approved parts of speech. When a verb is not approved, you cannot use it as a noun either. The dictionary entries for BUILD, CHECK, DO, GET, MAKE, RUN, SET, SHOW, START, STOP, and USE are particularly relevant to rule 1.13 violations. |

### Grammar Notes

**The light verb construction anti-pattern**

The most common violation of rule 1.13 is the light verb construction: a semantically weak verb (do, make, perform, execute, run, carry out) paired with a nominalized technical verb. For example:

- "Make a commit" instead of "Commit"
- "Do a compile" instead of "Compile"
- "Execute a deploy" instead of "Deploy"
- "Run a build" instead of "Build"

In English grammar, light verb constructions are grammatically correct but stylistically weak. In STE-Code, they are violations because the technical verb is used as a noun (the object of the light verb). The fix is always to use the technical verb as the main verb of the sentence.

When the light verb adds necessary semantic information, the construction can be correct if the object is a genuine code-domain technical noun (rule 1.5), not a nominalized verb:

> **STE:** Run the test suite. ("test suite" is a technical noun, category 3)
> **STE:** Do a quick check of the configuration. ("check" is an approved noun in the controlled terminology)

**Distinguishing technical verb from technical noun by category membership**

The only reliable test for whether a word can be used as a noun is the category test from rule 1.5. Ask:

1. Can this word fit into one of the 19 code-domain technical noun categories?
2. If yes, the word is a technical noun and can be used as a noun.
3. If no, the word cannot be used as a noun — even if it is common in your team's speech.

For example, "deploy" fits category 5 (infrastructure, deployment, and platforms) as a noun. "Compile" does not fit any technical noun category naturally — it is only a technical verb (category 1 a). Therefore, "the deploy" is correct and "the compile" is wrong.

**The dual-category exception: formal justification**

The ASD-STE100 spec explicitly permits dual-category words. The spec's example is "plate," which is both a technical verb (category 1 c, manufacturing processes) and a technical noun (category 1, official parts information). The spec does not require you to choose one category and forbid the other — it permits both when the context justifies the category assignment.

In STE-Code, common dual-category words include:

| Word | Technical Verb Category (Rule 1.12) | Technical Noun Category (Rule 1.5) |
|------|--------------------------------------|-------------------------------------|
| build | Category 1 c) Build and package | Category 3) Development tools |
| deploy | Category 1 c) Build and package | Category 5) Infrastructure, deployment, and platforms |
| test | Category 1 b) Test and verify code | Category 3) Development tools |
| commit | Category 2 c) System operations | Category 4) Data structures |
| merge | Category 1 c) Build and package | Category 4) Data structures |
| release | Category 1 c) Build and package | Category 5) Infrastructure, deployment, and platforms |
| patch | Category 1 a) Write and modify code | Category 4) Data structures |
| log | Category 2 c) System operations | Category 13) Runtime environments |
| import | Category 1 a) Write and modify code | Category 4) Data structures |

For each word, the noun use must refer to a concrete artifact or event that fits the noun category. "The build failed" is correct because "build" names a build artifact or process (category 3). "Do a build" is wrong because the instruction should use the verb form — the word is neither category here; it is a misused verb in a light verb construction.

**Regression test: the article test**

A simple test for verb-as-noun violations: if you can put an article (a, an, the) before the word and the sentence remains grammatical, the word is functioning as a noun. If it is a code-domain technical verb functioning as a noun, check the dual-category table above. If the word is not in the dual-category table, the usage violates rule 1.13.

Test application:

- "The compile failed" — "compile" with article → noun use → "compile" is not a dual-category word → VIOLATION
- "The build failed" — "build" with article → noun use → "build" is a dual-category word (category 3) → CORRECT
- "The import failed" — "import" with article → noun use → "import" is a dual-category word (category 4) → CORRECT
- "The lint found errors" — "lint" with article → noun use → "lint" is not a dual-category word → VIOLATION. Write "The linter found errors" (linter = technical noun, category 3).

> **See also:** Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category
> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category
> **See also:** Rule 1.7 — Do Not Use Technical Nouns as Verbs
> **See also:** Rule 1.4 — Use Only Approved Verb Forms and Adjective Forms
> **See also:** Rule 1.10 — No Slang, Jargon, or Regional Terms

---

<!-- a-sec1-rule1.14.md -->

# Rule 1.14 — Use American English Spelling Unless Other Official Directives Tell You Differently

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.14](ste-code/grouped/), Rule 1.14

## Original Rule

**Rule 1.14** Use American English spelling unless other official directives tell you differently.

Use the spelling specified in the STE dictionary (American English spelling). Use a different spelling only if other technical publication specifications, style guides, contracts, or other official directives are applicable.

Examples:

("Fiber" is American English spelling.)

("Color" is American English spelling.)

If there is quoted text that has British English spelling, for example on a computer screen, do not change the spelling. Keep the quoted text as it is. Refer to Rule 8.6 which tells you how to use quoted texts correctly.

## STE-Code Adaptation

**Rule 1.14** Use American English spelling unless other official directives tell you differently.

> **See also:** Rule 8.6 — Use Quoted Texts Correctly

Use the spelling specified in the STE-Code controlled terminology (American English spelling). Use a different spelling only if other project specifications, style guides, contracts, or other official directives are applicable.

This adapts the spec directly: the same rule applies to code documentation as it does to aerospace documentation. American English spelling is the default in both STE and STE-Code.

If there is quoted text that has British English spelling, for example in an error message, a code comment, or on a user interface, do not change the spelling. Keep the quoted text as it is. Refer to Rule 8.6 which tells you how to use quoted texts correctly.

### Examples

> *Adapted from spec pair:* Non-STE: "Fibre is British English spelling."  |  STE: "Fiber is American English spelling."

> *Adapted from spec pair:* Non-STE: "Colour is British English spelling."  |  STE: "Color is American English spelling."

> **Non-STE:** The log file shows the colour of each output line.
>
> **STE:** The log file shows the color of each output line.

> *Adapted from spec example: "Color" is American English spelling, and the spec explicitly lists it as an example. The non-STE version uses the British English spelling "colour," which is not permitted. The STE version uses the American English spelling "color."*

> **Non-STE:** Initialise the variable before you use it in the loop.
>
> **STE:** Initialize the variable before you use it in the loop.

> *Adapted from spec example: "Fiber" is American English spelling. Just as the spec requires American English spelling for all technical documentation, STE-Code requires it for code documentation. "Initialize" is American English spelling. The non-STE version uses the British English spelling "initialise," which is not permitted.*

> **STE:** The terminal shows the message `Colour profile not recognised`.
>
> *Adapted from spec concept: if a computer screen displays text with British English spelling, you must not change the spelling of the quoted text. In STE-Code, if a terminal output or error message contains British English spelling ("Colour," "recognised"), you must keep the quoted text exactly as it is. The surrounding documentation text must use American English spelling. This is the same principle as the spec example where British spelling in quoted computer screen text is preserved.*

---

## Code-Domain Explanation

Rule 1.14 is a surface-level constraint that applies to every word in every type of code documentation. Unlike rules that govern vocabulary selection (Rule 1.1) or part of speech (Rule 1.2), Rule 1.14 governs the spelling of words that are already selected. It is the final orthographic check before documentation is complete.

The rule has consequences beyond cosmetic consistency. British English spellings can cause confusion in technical contexts where spelling differences create ambiguity. For example, "meter" (American) is a measuring device; "metre" (British) is a unit of length. In code documentation, "meter" always refers to a measurement component, and "metre" would be an error.

### README Files

README files are the first document a new contributor reads. Inconsistent spelling between American and British English signals a lack of editorial control. README files must use American English spelling throughout, including in headings, bullet points, code comments within README code blocks, and link text.

Common README violations involve the -ise/-ize suffix pair. Words that end in "-ise" in British English end in "-ize" in American English: "initialise" becomes "initialize," "organise" becomes "organize," "recognise" becomes "recognize." The -yse/-yze pair follows the same pattern: "analyse" becomes "analyze," "paralyse" becomes "paralyze."

Example — README installation section:

> **Non-STE:** Organise your environment variables in a `.env` file. The application analyses this file at startup.
>
> **STE:** Organize your environment variables in a `.env` file. The application analyzes this file at startup.
> *(P14 applied: "organise" → "organize"; "analyse" → "analyze")*

Example — full README installation block:

````
# Non-STE

## Installation

1. Clonse the repository with `git clone https://github.com/acme/widget-api.git`.
2. Organise your environment variables in a `.env` file. The application analyses
   this file at startup to load the database connection string.
3. Run `npm install`, then `npm run build` to compile the TypeScript sources.

## Usage

The CLI tool centres the output and colour-codes each log level.

# STE

## Installation

1. Clone the repository with `git clone https://github.com/acme/widget-api.git`.
2. Organize your environment variables in a `.env` file. The application analyzes
   this file at startup to load the database connection string.
3. Run `npm install`, then `npm run build` to build the TypeScript sources.

## Usage

The CLI tool centers the output and color-codes each log level.

> *(P14 applied: "Clonse" → "Clone" [general error, not a dialect pair]; "Organise" → "Organize"; "analyses" → "analyzes"; "centres" → "centers"; "colour-codes" → "color-codes")*
````

### API Documentation

API documentation is often generated from source code annotations. When the source annotations use British English spelling and a generation tool produces the final output, both the source and the output must follow Rule 1.14. This is especially important for public APIs, where British English spellings in parameter descriptions or return value documentation can confuse non-native English speakers who learned American English spelling conventions.

Parameter names and endpoint paths are code-domain technical nouns (Rule 1.5, category 10). If a parameter name contains a British English spelling, you must not change it in the code. But the prose description of that parameter must use American English spelling.

Example — OpenAPI description:

> **Non-STE:** `colour_scheme` — The colour scheme to apply to the dashboard. Accepted values: "light", "dark".
>
> **STE:** `colour_scheme` — The color scheme to use for the dashboard. Accepted values: "light", "dark".
> *(P14 applied: "colour" → "color" in prose; parameter name `colour_scheme` preserved as quoted text)*

Example — full JSDoc block for a REST endpoint handler:

````
/**
 * Non-STE
 *
 * @route GET /api/v1/reports
 * @summary Generate a usage report for the selected organisation.
 * @param {string} colour_filter - The colour to filter the chart by.
 *        Accepts any valid CSS colour value such as "#ff0000".
 * @returns {Report} report - The generated report object. Serialises the
 *          data set and returns the summarised totals.
 */
async function getReport(req, res) { /* ... */ }

/**
 * STE
 *
 * @route GET /api/v1/reports
 * @summary Make a usage report for the selected organization.
 * @param {string} colour_filter - The color to filter the chart by.
 *        Accepts any valid CSS color value such as "#ff0000".
 * @returns {Report} report - The generated report object. Serializes the
 *          data set and gives the summarized totals.
 */
async function getReport(req, res) { /* ... */ }

> *(P14 applied: "organisation" → "organization"; "colour" → "color" in prose; "Serialises" → "Serializes"; "returns" → "gives" [P1]; "summarised" → "summarized"; parameter name colour_filter preserved as quoted text)*
````

### Docstrings and Inline Comments

Docstrings and inline comments are the documentation closest to the source code. They are read by developers who work in many different spelling environments. American English spelling in docstrings gives a consistent reading experience regardless of the developer's native language.

British English spellings in docstrings often come from developers whose locale defaults to British English. Common violations include "behaviour" (British) instead of "behavior" (American), "centre" instead of "center," and "defence" instead of "defense."

Example — Python docstring:

> **Non-STE:** """Centre the text in the terminal window. Returns the centred string."""
>
> **STE:** """Center the text in the terminal window. Gives the centered string."""
> *(P14 applied: "centre" → "center"; "centred" → "centered"; P1 also applied: "returns" → "gives")*

Example — full Python module with docstrings and inline comments:

````
# Non-STE

def normalise_signal(samples):
    """Normalise the input signal and serialise the result to a buffer.
    Returns the centred and optimised sample set."""
    # Centre the data around zero, then optimise for peak detection.
    buffer = serialise(samples)
    return buffer


# STE

def normalize_signal(samples):
    """Normalize the input signal and serialize the result to a buffer.
    Gives the centered and optimized sample set."""
    # Center the data around zero, then optimize for peak detection.
    buffer = serialize(samples)
    return buffer

> *(P14 applied: "normalise" → "normalize"; "serialise" → "serialize"; "Returns" → "Gives" [P1]; "centred" → "centered"; "optimised" → "optimized"; "Centre" → "Center"; "optimise" → "optimize")*
````

### Commit Messages

Commit messages are short and indexable. British English spellings in commit messages create friction during search: a developer who searches for "color" will not find commits that say "colour." Consistent American English spelling makes commit history searchable across teams with different language backgrounds.

Common commit message violations:

| British | American | Context |
|---------|----------|---------|
| colour | color | UI, terminal, theming |
| behaviour | behavior | feature descriptions, bug reports |
| organise | organize | restructuring, refactoring |
| recognise | recognize | pattern matching, parsing |
| analyse | analyze | profiling, data processing |
| defence | defense | security fixes |

Example — commit message:

> **Non-STE:** fix: correct colour parsing behaviour in the analytics module
>
> **STE:** fix: correct color parsing behavior in the analytics module
> *(P14 applied: "colour" → "color"; "behaviour" → "behavior")*

Example — full commit body:

````
# Non-STE
feat(auth): parametrise the token refresh logic

We reorganise the session store and recognise expired tokens earlier.
This optimises the reconnect path for clients that travel through
proxy servers.

# STE
feat(auth): parameterize the token refresh logic

We reorganize the session store and recognize expired tokens earlier.
This optimizes the reconnect path for clients that travel through
proxy servers.

> *(P14 applied: "parametrise" → "parameterize"; "reorganise" → "reorganize"; "recognise" → "recognize"; "optimises" → "optimizes"; "travel" → "travel" [single-l, American])*
````

### Error Messages

Error messages that the development team writes are documentation. They must use American English spelling. Error messages from third-party libraries, language runtimes, or operating systems are quoted text (Rule 1.5, category 10). If a third-party error message uses British English spelling, you must not change it.

When you write error messages for your own software, apply Rule 1.14 consistently. An error message that says "colour" in one place and "color" in another is a quality defect.

Example — application error message:

> **Non-STE:** Error: The licence key is not recognised. Please contact your administrator.
>
> **STE:** Error: The license key is not recognized. Speak to your administrator.
> *(P14 applied: "licence" (noun) → "license"; "recognised" → "recognized"; P1 applied: "contact" → "speak to")*

Example — full error-handling module:

````
# Non-STE (application-authored messages)
raise ConfigError("The licence key is not recognised. Please contact your administrator.")
logger.error("The connection was cancelled by the server. The programme will retry.")

# STE (application-authored messages)
raise ConfigError("The license key is not recognized. Speak to your administrator.")
logger.error("The connection was canceled by the server. The program will retry.")

# Third-party / runtime messages are quoted text — preserve exactly
try:
    os.stat("/etc/app/colour_profiles.cfg")
except OSError as exc:
    # Non-STE and STE both keep the operating system's wording unchanged:
    log_foreign_error(exc)  # OSError: [Errno 2] No such file or directory:
                           # '/etc/app/colour_profiles.cfg'

> *(P14 applied to prose: "licence" → "license"; "recognised" → "recognized"; "contact" → "speak to" [P1]; "cancelled" → "canceled"; "programme" → "program". The OSError string is quoted text, so its British spelling is preserved.)*
````

---

## Paradigm-Specific Guidance

Rule 1.14 applies uniformly to all paradigms because spelling is language-level, not paradigm-level. But each paradigm has its own vocabulary of common British English violations that appear in documentation because of historical spelling patterns in the paradigm's community.

### Object-Oriented (Java, C++, C#, Python Classes)

Object-oriented documentation uses many words that end in -or/-our and -ize/-ise. The OOP community has historically been split between American and British spelling conventions. Some Java standard library methods and C# framework APIs use British English spellings in their names (for example, `java.awt.Color` uses American spelling, but some older Java libraries use British spelling). This creates documentation challenges.

**Common OOP documentation spelling violations:**

| British | American | OOP Context |
|---------|----------|-------------|
| behaviour | behavior | class behavior, method behavior, object behavior |
| colour | color | UI component color, syntax highlighting color |
| initialise | initialize | object initialization, lazy initialization |
| serialise | serialize | object serialization, data serialization |
| optimise | optimize | performance optimization, query optimization |
| parametrise | parameterize | parameterized types, parameterized tests |
| customise | customize | custom behavior, custom implementation |

Example — Java class documentation:

> **Non-STE:** The `CacheManager` class is responsible for the initialisation and serialisation of cached objects. It optimises memory usage through customisable eviction behaviour.
>
> **STE:** The `CacheManager` class is responsible for the initialization and serialization of cached objects. It optimizes memory usage through customizable eviction behavior.
> *(P14 applied: "initialisation" → "initialization"; "serialisation" → "serialization"; "optimises" → "optimizes"; "customisable" → "customizable"; "behaviour" → "behavior")*

Example — full C# XML documentation:

````
/// Non-STE
/// <summary>
/// Initialises the repository and serialises the cached entities.
/// The method optimises throughput and customises the eviction behaviour.
/// </summary>
public void Bootstrap() { /* ... */ }

/// STE
/// <summary>
/// Initializes the repository and serializes the cached entities.
/// The method optimizes throughput and customizes the eviction behavior.
/// </summary>
public void Bootstrap() { /* ... */ }

> *(P14 applied: "Initialises" → "Initializes"; "serialises" → "serializes"; "optimises" → "optimizes"; "customises" → "customizes"; "behaviour" → "behavior")*
````

### Functional (Haskell, Elixir, Clojure, Rust)

Functional programming documentation has fewer spelling violations than OOP documentation because the functional community adopted American English spelling conventions early. But Elixir, which has a strong European user base, is an exception. Elixir documentation and library names sometimes use British English spellings (for example, "behaviour" is the name of a language construct in Elixir, and it uses British spelling).

**Guidance points for functional documentation:**

- The word "behaviour" is used in British English spelling as a language keyword in Elixir. When referring to the Elixir `@behaviour` module attribute, use the British spelling because it is quoted text (the actual code uses that spelling). But when describing the concept in prose, use the American English spelling "behavior."
- Haskell documentation uses "centre" in some older texts. Modern Haskell documentation should use "center."
- Clojure documentation follows American English spelling conventions.
- Rust documentation follows American English spelling conventions.

Example — Elixir module documentation:

> **Non-STE:** This module defines a custom behaviour for plug initialisation. Modules that implement this behaviour must provide an `init/1` callback.
>
> **STE:** This module defines a custom `@behaviour` for plug initialization. Modules that implement this `@behaviour` must give an `init/1` callback.
> *(P14 applied: "initialisation" → "initialization"; `@behaviour` preserved as code keyword; P1 applied: "provide" → "give")*

Example — full Elixir doc:

````
# Non-STE
defmodule Storage do
  @moduledoc """
  Defines a custom behaviour for plug initialisation.
  Modules that implement this behaviour must provide an `init/1` callback
  and a `handle_event/2` callback that analyses each request.
  """
end

# STE
defmodule Storage do
  @moduledoc """
  Defines a custom @behaviour for plug initialization.
  Modules that implement this @behaviour must give an `init/1` callback
  and a `handle_event/2` callback that analyzes each request.
  """
end

> *(P14 applied: "initialisation" → "initialization"; "analyses" → "analyzes"; "@behaviour" preserved as code keyword; "provide" → "give" [P1])*
````

### Procedural (C, Go, Bash)

Procedural documentation has the fewest British English spelling violations because the procedural community is predominantly American. But specialized domains within procedural programming — especially embedded systems, networking, and telecommunications — have historically used British English because of their European origins.

**Common procedural documentation spelling violations:**

| British | American | Procedural Context |
|---------|----------|-------------------|
| licence | license | software license, license key |
| defence | defense | defense programming, defense in depth |
| cancelled | canceled | canceled operations, canceled signals |
| traveller | traveler | traveler pattern in process management |

Example — C library documentation:

> **Non-STE:** The licence key must be validated before the defence mechanisms are initialised.
>
> **STE:** The license key must be checked before the defense mechanisms are initialized.
> *(P14 applied: "licence" → "license"; "defence" → "defense"; "initialised" → "initialized"; P1 applied: "validated" → "checked")*

Example — full Go doc comment:

````
// Non-STE
// OpenStore validates the licence key and arms the defence mechanisms
// before the connection is initialised. A cancelled context stops the
// traveller goroutine that polls the upstream host.
func OpenStore(ctx context.Context) (*Store, error) { /* ... */ }

// STE
// OpenStore checks the license key and arms the defense mechanisms
// before the connection is initialized. A canceled context stops the
// traveler goroutine that polls the upstream host.
func OpenStore(ctx context.Context) (*Store, error) { /* ... */ }

> *(P14 applied: "validates" → "checks" [P1]; "licence" → "license"; "defence" → "defense"; "initialised" → "initialized"; "cancelled" → "canceled"; "traveller" → "traveler")*
````

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation often includes British English spellings because many declarative tools (Terraform, Kubernetes, Ansible) are developed by international teams with European contributors. But the official documentation for these tools uses American English spelling, and STE-Code documentation must follow the same convention.

**Guidance points for declarative documentation:**

- Kubernetes documentation uses American English spelling ("behavior," "color," "organize").
- Terraform documentation uses American English spelling. HashiCorp is an American company.
- SQL keywords do not have spelling variants (SELECT, INSERT, UPDATE are the same in all English locales). But SQL comments and documentation strings do.
- YAML is a data serialization format. Documentation about YAML must use American English spelling.

Example — Terraform module documentation:

> **Non-STE:** This module centralises the organisation of network policies. It also synchronises security groups across regions.
>
> **STE:** This module centralizes the organization of network policies. It also synchronizes security groups across regions.
> *(P14 applied: "centralises" → "centralizes"; "organisation" → "organization"; "synchronises" → "synchronizes")*

Example — full Kubernetes manifest comment block:

````
# Non-STE
# This Deployment centralises the organisation of network policies.
# The controller synchronises security groups across regions and
# optimises the rollout to minimise downtime during a config change.
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway

# STE
# This Deployment centralizes the organization of network policies.
# The controller synchronizes security groups across regions and
# optimizes the rollout to minimize downtime during a config change.
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway

> *(P14 applied: "centralises" → "centralizes"; "organisation" → "organization"; "synchronises" → "synchronizes"; "optimises" → "optimizes"; "minimises" → "minimizes")*
````

### Systems (Rust Ownership, C Memory Management)

Systems documentation has a vocabulary of spelling-sensitive words related to memory and hardware. Words like "defense," "license," "meter," and "analog" have American English spellings that differ from their British English equivalents. Using the wrong spelling can create ambiguity in technical contexts.

**Common systems documentation spelling violations:**

| British | American | Systems Context |
|---------|----------|----------------|
| analogue | analog | analog signal, analog input |
| metre | meter | memory meter, CPU meter |
| defence | defense | memory defense, defense in depth |
| cancelled | canceled | canceled memory allocation |
| traveller | traveler | traveler pattern in garbage collection |

Example — Rust systems documentation:

> **Non-STE:** The memory metre shows the current heap usage. The defence mechanisms prevent double-free errors and cancelled allocations from corrupting the heap.
>
> **STE:** The memory meter shows the current heap usage. The defense mechanisms prevent double-free errors and canceled allocations from corrupting the heap.
> *(P14 applied: "metre" → "meter"; "defence" → "defense"; "cancelled" → "canceled")*

Example — full C memory-pool comment:

````
/* Non-STE */
/* The memory metre samples heap usage every second. The defence layer
   blocks double-free errors, and the allocator frees cancelled
   allocations before the traveller sweep runs. */

/* STE */
/* The memory meter samples heap usage every second. The defense layer
   blocks double-free errors, and the allocator frees canceled
   allocations before the traveler sweep runs. */

> *(P14 applied: "metre" → "meter"; "defence" → "defense"; "cancelled" → "canceled"; "traveller" → "traveler")*
````

---

## Extended Examples

Each example pair below shows a real code documentation scenario with a British English spelling violation, the STE-Code compliant rewrite, which principle was applied, and an explanation of the fix.

### Example 1 — API Reference: Parameter Description

> **Non-STE:** @param {string} colour — The colour of the notification badge. Accepts any valid CSS colour value.
>
> **STE:** @param {string} color — The color of the notification badge. Accepts any valid CSS color value.
>
> **Principle applied:** P14 (use American English spelling: "colour" → "color")
> **Explanation:** Both occurrences of "colour" in the parameter documentation use British English spelling. The American English spelling "color" is required. Note that CSS property names (for example, `background-color`) use American English spelling natively, so the documentation is now also consistent with the API it documents.

### Example 2 — README: Architecture Overview

> **Non-STE:** The service-oriented architecture centralises request handling through a single API gateway. This organisation minimises latency and maximises throughput.
>
> **STE:** The service-oriented architecture centralizes request handling through a single API gateway. This organization minimizes latency and maximizes throughput.
>
> **Principle applied:** P14 (use American English spelling: "centralises" → "centralizes"; "organisation" → "organization"; "minimises" → "minimizes"; "maximises" → "maximizes")
> **Explanation:** Four words in two sentences use the British English -ise suffix. The American English -ize suffix is required for all four. This example shows how a single paragraph can accumulate many spelling violations when a British English locale is used. The -ise/-ize pattern is the most frequent source of Rule 1.14 violations in code documentation.

### Example 3 — Docstring: Function Behavior Description

> **Non-STE:** /** Analyses the input data and recognises patterns. Returns an object modelling the recognised patterns. */
>
> **STE:** /** Analyzes the input data and recognizes patterns. Gives an object that models the recognized patterns. */
>
> **Principle applied:** P14 (use American English spelling: "analyses" (verb) → "analyzes"; "recognises" → "recognizes"; "recognised" → "recognized"); P1 (use approved words: "returns" → "gives")
> **Explanation:** Three words use the British English -yse/-ise suffixes. The American English -yze/-ize suffixes are required. "Modelling" is also a British English spelling variant (American: "modeling"), but the rewrite avoids it by restructuring the sentence. The docstring now uses American English spelling throughout.

### Example 4 — Commit Message: Configuration Change

> **Non-STE:** chore: standardise ESLint configuration across all packages and synchronise with the monorepo
>
> **STE:** chore: standardize ESLint configuration across all packages and synchronize with the monorepo
>
> **Principle applied:** P14 (use American English spelling: "standardise" → "standardize"; "synchronise" → "synchronize")
> **Explanation:** Two verbs in a commit message use the British English -ise suffix. The American English -ize suffix is required. Commit messages with British English spelling break search consistency across a team.

### Example 5 — Error Message: User-Facing Validation

> **Non-STE:** Validation error: The programme cannot recognise the file format. The file may have been cancelled during transfer.
>
> **STE:** Validation error: The program cannot recognize the file format. The file may have been canceled during transfer.
>
> **Principle applied:** P14 (use American English spelling: "programme" → "program"; "recognise" → "recognize"; "cancelled" → "canceled")
> **Explanation:** Three British English spelling variants in a user-facing error message. "Programme" (British) refers to a television or radio broadcast in American English; "program" is the American English spelling for a computer program. "Cancelled" uses the British English double-L convention; the American English single-L "canceled" is required.

### Example 6 — Configuration File Comment

> **Non-STE:** # The log level controls the verbosity of output. Set to "debug" to
> # analyse the full request/response lifecycle, including serialisation
> # behaviour and connection pool utilisation.
> **STE:** # The log level controls the verbosity of output. Set to "debug" to
> # analyze the full request/response lifecycle, including serialization
> # behavior and connection pool usage.
>
> **Principle applied:** P14 (use American English spelling: "analyse" → "analyze"; "serialisation" → "serialization"; "behaviour" → "behavior"; "utilisation" → "usage"); P1 (use approved words: "utilisation" is not approved; "usage" is the approved noun form of "use")
> **Explanation:** Four British English spelling violations in a three-line configuration comment. Three are -yse/-ise suffix violations. The fourth is "behaviour," which uses the -our ending. "Utilisation" is both a British English spelling (American: "utilization") and an unapproved word under P1. The rewrite uses "usage," which is the approved noun form.

---

## Edge Cases

The following scenarios show where the rigid application of Rule 1.14 requires careful judgment because of conflicts with code-domain technical terms, framework conventions, or other official directives.

### Edge Case 1: Framework or Library Name That Uses British English Spelling

**Scenario:** A widely used framework or library has a name that uses British English spelling. Examples include:

- Elixir's `Behaviour` module (the language keyword uses British spelling)
- Python's `argparse` module historically accepted British English spellings in some parameter names
- Some npm packages use British English spelling in their package names (for example, `colours`, `centre-align`)
- The `centre` attribute in some older HTML/CSS specifications

**Guidance:** Framework names, library names, and package names are code-domain technical nouns (Rule 1.5, categories 3 and 1). You must write them with their official spelling, even when that spelling uses British English. The framework author chose the spelling, and changing it would create confusion.

When you write prose about a framework that uses British English spelling in its name, the prose must use American English spelling:

> **Non-STE:** The `ColourPicker` component uses the `colour` library for colour space conversions.
>
> **STE:** The `ColourPicker` component uses the `colour` library for color space conversions.
> *(Framework names preserved; prose uses American English spelling)*

This creates a visual inconsistency, but it is the correct approach. The inconsistency signals to the reader that the British English words are technical names, not prose vocabulary.

### Edge Case 2: Code Keyword That Uses British English Spelling

**Scenario:** A programming language keyword or standard library function uses British English spelling. Examples include:

- Elixir: `@behaviour`, `defexception` (exception names may use British spelling)
- Python: `os.error` and older standard library error messages may use British English
- C++: Some older Boost libraries use British English spelling in function names
- CSS: Some older CSS properties used British English spelling (for example, `colour` was proposed but never adopted; `centre` was used in some early drafts)

**Guidance:** When the British English spelling is part of the code (a keyword, a function name, a class name), it is code-domain technical text. Preserve it exactly as it appears in the code. The surrounding documentation prose must use American English spelling.

> **Non-STE:** The `@behaviour` callback initialises the module's state.
>
> **STE:** The `@behaviour` callback initializes the module state.
> *(P14 applied: "initialises" → "initializes"; `@behaviour` preserved as code keyword)*

Extreme case: when a language keyword and a documentation word are adjacent and use different spelling conventions:

> **STE:** The `@behaviour` defines the behavior of the module.
> *(Both spellings coexist: `@behaviour` is a code keyword, "behavior" is prose)*

This is visually awkward but technically correct. Avoid the awkwardness by restructuring when possible:

> **STE:** The module behavior is set by the `@behaviour` callback.
> *(Separation reduces the visual clash)*

### Edge Case 3: Generated Documentation from British English Tools

**Scenario:** Documentation generation tools (Sphinx, JSDoc, Doxygen, godoc) may produce output that contains British English spellings. This happens when the tool uses British English default templates or when the tool was developed by a team in a British English locale.

**Guidance:** Rule 1.14 applies to documentation that a human writes or reviews. When a generation tool adds British English boilerplate (for example, "Generated by Sphinx. Copyright © 2024. All rights reserved.") you cannot control it without customizing the tool's templates.

The following approach is recommended:

1. For public-facing API documentation, customize the generation tool's templates to use American English spelling.
2. For internal documentation, accept the generated boilerplate as-is unless it causes confusion.
3. Write all source annotations (docstrings, comments, descriptions) in American English spelling. The generated output will inherit the correct spelling for the content you control.

> **STE (acceptable for internal docs):** *Generated by Sphinx. All rights reserved. Licence: MIT.*
> *(The boilerplate "Licence" is from the tool's British English template. It is acceptable for internal documentation.)*

> **STE (preferred for public docs):** *Generated by Sphinx. All rights reserved. License: MIT.*
> *(The template was customized to use American English spelling. This is preferred for public documentation.)*

### Edge Case 4: Internationalization (i18n) and Localization (l10n) Strings

**Scenario:** A software application has internationalization (i18n) strings that must support both American English and British English locales. The American English locale file must use American English spelling. The British English locale file must use British English spelling.

**Guidance:** Localization files are quoted text when referenced in documentation. The documentation prose around them must use American English spelling. The content of the files must be preserved as-is.

> **STE:** The `en-GB.json` locale file contains `"colour": "Colour"`. The `en-US.json` locale file contains `"color": "Color"`.
> *(Both locale strings are preserved as-is. The documentation prose uses American English spelling: "contains," "file.")*

When you write the American English locale file for your application, Rule 1.14 applies to that file as documentation. The British English locale file is written for British English users and falls under the "official directive" exception to Rule 1.14: the locale specification requires British English spelling.

### Edge Case 5: Official Directive to Use British English

**Scenario:** A project has an official style guide or contributing guide that requires British English spelling. For example, a project sponsored by a British organization or a project in a British English locale (for example, UK government software) may mandate British English spelling.

**Guidance:** Rule 1.14 states "unless other official directives tell you differently." An official project style guide that mandates British English spelling is an official directive. In this case, you must use British English spelling throughout the project's documentation.

> **NOTE:** When a project uses British English spelling by official directive, it is not using STE-Code. STE-Code requires American English spelling. But the STE-Code specification acknowledges that official directives override the default. This is the same exception mechanism that the original ASD-STE100 provides.

> **Recommendation:** If the project has no official directive, use American English spelling. If the project has an official directive for British English spelling, document this exception in the project's CONTRIBUTING.md file and apply British English spelling consistently throughout.

---

## Cross-References

Rule 1.14 is the final orthographic constraint in Section 1 (Words). It interacts with several other rules:

| Rule | Title | Relationship to Rule 1.14 |
|------|-------|---------------------------|
| **Rule 1.1** | Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs | Rule 1.14 constrains the spelling of words that pass Rule 1.1. You must first select the correct word (Rule 1.1) and then spell it with American English (Rule 1.14). |
| **Rule 1.5** | You Can Use Words That You Can Include in a Technical Noun Category | Technical nouns that use British English spelling in their official names must be preserved. Rule 1.14 makes an exception for quoted text and proper names. |
| **Rule 1.6** | Use a Non-Approved Word Only When It Is a Technical Noun | Non-approved words used as technical nouns may carry British English spelling from their source. Rule 1.14 requires American English spelling for prose but preserves quoted text spelling. |
| **Rule 1.8** | Use Standard, Well-Known Technical Nouns | Standard technical nouns have a canonical spelling. Rule 1.8 and Rule 1.14 both require using the standard form: Rule 1.8 requires using the well-known term, and Rule 1.14 requires the American English spelling of it. |
| **Rule 1.10** | No Slang, Jargon, or Regional Terms | British English spellings can be a form of regional variation. Rule 1.10 prohibits regional terms, and Rule 1.14 extends this prohibition to regional spellings. |
| **Rule 1.11** | One Term Per Concept — Be Consistent | Consistent spelling is part of consistent terminology. If you use "color" in one section and "colour" in another, you violate both Rule 1.11 (inconsistent terminology) and Rule 1.14 (non-American spelling). |
| **Rule 8.6** | Use Quoted Texts Correctly | Rule 8.6 governs how to present quoted text in documentation. Rule 1.14 requires that quoted text with British English spelling must not be changed — it must be preserved as-is. Rule 8.6 gives the formatting and presentation rules for such quoted text. |

**Dictionary reference:** See `a-dictionary.md` for the full STE-Code controlled terminology. All approved words in the dictionary use American English spelling. If a word's approved spelling differs from a British English variant you are used to, the dictionary is the authority.

**Categories reference:** See `a-categories.md` for the 19 code-domain technical noun categories. Category 10 (Quoted Text) is the primary exception mechanism for British English spellings in code documentation.

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category
> **See also:** Rule 1.11 — One Term Per Concept — Be Consistent
> **See also:** Rule 8.6 — Use Quoted Texts Correctly

---

## Grammar Notes

### The Spelling Classification Model

Rule 1.14 divides all words in code documentation into three spelling classes:

1. **Prose Words — American English Only:** Every word in the descriptive and procedural prose of code documentation must use American English spelling. This includes headings, sentences, bullet points, table content, and figure captions. There are no exceptions for prose words.

2. **Quoted Text — Preserved As-Is:** Words that appear as quoted text (Rule 1.5, category 10) must be preserved with their original spelling. This includes error messages from third-party libraries, terminal output, UI labels, file paths, and code keywords. When quoted text uses British English spelling, you must not change it.

3. **Code-Domain Technical Nouns — Official Spelling:** Technical nouns (Rule 1.5, all categories) must use their official spelling. When the official spelling uses British English (for example, the `colour` npm package, the `@behaviour` Elixir keyword), you must preserve that spelling. The surrounding prose must use American English spelling.

### The -ize/-ise Suffix Rule

The most frequent Rule 1.14 violation in code documentation is the -ize/-ise suffix pair. The rule is:

- Use -ize (American English): initialize, serialize, optimize, organize, recognize, synchronize, standardize, parameterize, customize, authorize, characterize, prioritize, minimize, maximize, centralize, visualize, analyze, paralyze.

- Do not use -ise (British English): initialise, serialise, optimise, organise, recognise, synchronise, standardise, parametrise, customise, authorise, characterise, prioritise, minimise, maximise, centralise, visualise, analyse, paralyse.

There are no exceptions to this rule in STE-Code prose. The -ise suffix is never permitted in documentation prose.

**NOTE:** The word "size" (meaning dimensions) uses -ize in both American and British English. "Size" is not a -ize suffix verb — it is a standalone noun. The verb "size" (to measure or adjust the size) also uses -ize in both dialects. These words are not affected by the -ize/-ise rule.

### The -or/-our Suffix Rule

The second most frequent Rule 1.14 violation is the -or/-our suffix pair in nouns:

- Use -or (American English): color, behavior, flavor, humor, labor, neighbor, rumor, harbor, honor, vapor, rigor.

- Do not use -our (British English): colour, behaviour, flavour, humour, labour, neighbour, rumour, harbour, honour, vapour, rigour.

**Exception:** The word "contour" uses -our in both American and British English. It is not an -or/-our alternation word.

### The -er/-re Suffix Rule

The -er/-re alternation affects a small set of words:

- Use -er (American English): center, theater, liter, meter (measuring device), fiber, caliber.

- Do not use -re (British English): centre, theatre, litre, metre (unit of length), fibre, calibre.

**NOTE:** "Meter" and "metre" have different meanings in American English. "Meter" is a measuring device (a parking meter, a voltage meter). "Metre" is not an American English word. For the unit of length, American English also uses "meter" (a two-meter cable). In code documentation, "meter" always refers to a measuring or monitoring component (a memory meter, a CPU meter). "Metre" should not appear in American English code documentation.

### The -l/-ll Doubling Rule

British English doubles the final "l" before -ed, -ing, -er, -or suffixes in words where American English uses a single "l":

- Use single -l (American English): canceled, canceling, traveler, traveling, modeled, modeling, labeled, labeling, fueled, fueling, signaled, signaling.

- Do not use double -ll (British English): cancelled, cancelling, traveller, travelling, modelled, modelling, labelled, labelling, fuelled, fuelling, signalled, signalling.

**Exception:** Words where the stress falls on the final syllable always double the consonant in both dialects: "compelled," "compelling," "rebelled," "rebelling." These are not Rule 1.14 violations.

### Words with Different Spelling in Both Dialects

Some words have completely different spellings in American and British English beyond suffix patterns:

| British | American | Code Documentation Context |
|---------|----------|---------------------------|
| programme | program | computer program, program file |
| licence (noun) | license (noun and verb) | license key, license agreement |
| defence | defense | defense programming, defense in depth |
| offence | offense | offense-detection rules, security offense |
| pretence | pretense | rarely used in code documentation |
| practise (verb) | practice (verb and noun) | best practice, practice exercise |
| analyse | analyze | analyze data, code analysis |
| paralyse | paralyze | rarely used in code documentation |
| catalogue | catalog | service catalog, API catalog |
| dialogue | dialog | dialog box, dialog window |
| analogue | analog | analog signal, analog input |
| judgement | judgment | rarely used in code documentation |
| manoeuvre | maneuver | rarely used in code documentation |
| plough | plow | rarely used in code documentation |

### Words with the Same Spelling in Both Dialects

Some words that are sometimes mistakenly hyper-corrected to American English actually have the same spelling in both dialects:

- "Address" (not "adress")
- "All" (not "al")
- "Committee" (not "comittee")
- "Disappoint" (not "dissapoint")
- "Necessary" (not "neccessary")
- "Occurrence" (not "occurrance")
- "Parallel" (not "paralel")
- "Recommend" (not "reccomend")

These are not Rule 1.14 issues — they are general spelling errors that would violate any English spelling standard.

### The Quoted Text Exception: Grammar of Preservation

Rule 1.14 states that quoted text with British English spelling must be preserved. This creates a specific grammatical context: quoted text is orthographically isolated from the surrounding prose. The prose uses American English spelling. The quoted text uses its original spelling. The boundary is marked by quotation marks, backticks, code blocks, or other formatting conventions (Rule 8.6).

When a quoted British English word appears adjacent to an American English prose word, the reader sees two different spelling conventions in the same sentence. This is intentional: it signals that one word is a technical reference and the other is documentation prose.

> **STE:** The `Colour` class manages color profiles for the application.
> *(`` `Colour` `` is a code reference; "color" is prose)*

This visual distinction is a feature, not a defect. It helps the reader distinguish between technical names and explanatory prose.

### Historical Note: ASD-STE100 Precedent

In ASD-STE100 Issue 9, Rule 1.14 is a short but important rule. The original specification recognizes that aerospace documentation is international and that American English spelling is the international standard for technical English. The rule provides the spelling standard for the entire STE dictionary.

The original specification gives two examples: "Fiber" (American) and "Color" (American). These examples were chosen because they are frequent words in aerospace documentation and have well-known British English variants ("fibre," "colour"). STE-Code extends this principle to code documentation, where the frequency of -ize/-ise, -or/-our, and -er/-re alternations is high because of the domain's vocabulary.

The original specification acknowledges that official directives can override Rule 1.14. This exception mechanism is preserved in STE-Code. When a project has an official style guide that requires British English spelling, that guide is an official directive and Rule 1.14 does not apply. The project is then outside the scope of STE-Code for spelling, though all other STE-Code rules still apply.

### Practical Enforcement

Rule 1.14 is the easiest STE-Code rule to enforce with automated tools. Spelling checkers can flag British English spellings automatically. The following approach is recommended for enforcing Rule 1.14 in a project:

1. Configure the project's spell checker to use American English (en-US).
2. Add a pre-commit hook that runs a spell check on all documentation files.
3. Use a CI/CD pipeline step that rejects documentation with British English spellings.
4. Maintain a project-specific dictionary of approved technical nouns with British English spellings (for example, `colour` as an npm package name) so the spell checker does not flag them.
5. Require code review for documentation changes, with Rule 1.14 as a review checklist item.

Automated enforcement prevents the most common Rule 1.14 violations before they enter the project's documentation. Human review is still necessary for the edge cases (framework names, code keywords, quoted text).

---

<!-- a-sec1-rule1.2.md -->

# Rule 1.2 — Use Approved Words Only as the Specified Part of Speech

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.2](ste-code/grouped/), Rule 1.2

## Original Rule

**Rule 1.2** Use approved words from the dictionary only as the specified part of speech.

In the dictionary, each approved word has a specified part of speech. When you use an approved word, make sure that you use it only as the specified part of speech.

Examples:

"Test" is an approved noun, but not an approved verb.

> **STE:** Test B is an alternative to test A.

> **Non-STE:** Test the system for leaks.
>
> **STE:** Do the leak test of the system.

or

> **STE:** Do a test for leaks in the system.

"Dim" is an approved adjective, but not an approved verb.

Some words are approved as more than one part of speech. For example, "clean" is an approved verb and an approved adjective. The position of the word in the sentence shows its function (and its meaning) because verbs and adjectives have different positions.

"Acceptable" is an adjective that is not approved. The dictionary gives three approved alternatives that have the same part of speech. You can use one of these alternatives to replace the word "acceptable" in the sentence with a word-for-word replacement.

"Operable" is an adjective that is not approved. The dictionary gives an approved alternative that has a different part of speech: "operate" as a verb. Thus, you must use a different sentence construction.

When you replace a word, always make sure that the approved alternative you select does not change the meaning of the sentence. If the meaning changes, select a different word or use a different sentence construction.

Each word in the dictionary has its part of speech in parentheses, abbreviated as specified in the introduction to the dictionary.

If a word that you want to use is not in the dictionary:
1. Find that word in an English dictionary.
2. Find which is the best synonym that is approved in the STE dictionary.
3. Use the approved STE word or find a different sentence construction with other approved words.

## STE-Code Adaptation

**Rule 1.2** Use approved words from the controlled terminology only as the specified part of speech.

In the controlled terminology, each approved word has a specified part of speech. When you use an approved word, make sure that you use it only as the specified part of speech.

"Query" is an approved noun, but not an approved verb. This adapts the spec example where "test" is an approved noun but not an approved verb: just as you cannot write "test the system" in STE, you cannot write "query the database" in STE-Code.

"Static" is an approved adjective, but not an approved verb. This adapts the spec example where "dim" is an approved adjective but not an approved verb: just as you cannot use "dim" as a verb in STE, you cannot use "static" as a verb in STE-Code.

Some words are approved as more than one part of speech. For example, "call" is an approved verb and an approved noun. This adapts the spec example where "clean" is an approved verb and an approved adjective: just as the position of "clean" in the sentence shows whether it is a verb or an adjective, the position of "call" shows whether it is a verb (to call a function) or a noun (a function call).

When you replace a word, always make sure that the approved alternative you select does not change the meaning of the sentence. If the meaning changes, select a different word or use a different sentence construction.

If a word that you want to use is not in the controlled terminology:
1. Find that word in a standard English dictionary.
2. Find which is the best synonym that is approved in the STE-Code controlled terminology.
3. Use the approved STE-Code word or find a different sentence construction with other approved words.

### Preferred Approved Verbs (Borrowed Vocabulary)

When you must replace a noun or adjective used as a verb, choose the shortest approved verb that keeps the meaning. The Microsoft Writing Style Guide and the Google Developer Documentation Style Guide both recommend plain, common verbs and warn against inflated words such as "utilize," "leverage," "commence," "terminate," and "initiate." STE-Code follows the same advice: prefer "use" over "utilize" or "leverage," "start" over "commence" or "initiate," and "stop" over "terminate."

The table below maps the most common noun-as-verb and adjective-as-verb violations in code documentation to the approved STE-Code verb (or construction) you should use instead.

| Violating form (do not use) | Part of speech error | Approved STE-Code replacement |
|-----------------------------|----------------------|-------------------------------|
| Query the database / Cache the result / Queue the job / Log the error / Index the record | Technical noun used as verb | Send a query / Keep the result in the cache / Put the job in the queue / Write the error in the log / Use the index to find the record |
| Docker the app / Git the change / Kubectl the pod / Terraform the VPC | Tool name used as verb | Use Docker / Save with Git / Use `kubectl` / Use Terraform |
| Secure the endpoint / Empty the buffer / Silent the log / Clear the flag* | Adjective used as verb | Make the endpoint secure / Make the buffer empty / Make the log silent / Clear the flag |
| Static the variable / Ready the worker / Live the connection | Adjective used as verb | Make the variable static / Make the worker ready / Make the connection live |
| Utilize the cache / Leverage the library / Employ the service | Unapproved verb (inflate) | Use the cache / Use the library / Use the service |
| Commence the build / Initiate the transfer / Terminate the process | Unapproved verb (inflate) | Start the build / Start the transfer / Stop the process |
| Orchestrate the services / Facilitate the sync | Unapproved verb | Control the services / Help the sync |

\* "Clear" is approved as both verb and adjective, so "Clear the flag" is allowed; the table lists it only to show the make + adjective pattern applies to true adjectives such as "secure" and "empty."

---

> *Adapted from spec pair:* Non-STE: "Test the system for leaks." | STE: "Do the leak test of the system."

The two adapted spec pairs below are the canonical starters for Rule 1.2. Each one is shown first as a single corrected sentence pair, then as a full, runnable code documentation context so you can see the part-of-speech fix in a realistic situation.

**Pair A — "query" (approved noun, not verb), adapted from "test" (approved noun, not verb).**

> **Non-STE:** Query the database for user records.

> **STE:** Send a query to the database for user records.

> *Adapted from spec pair: "Test the system for leaks" → "Do the leak test of the system." Just as "test" is only an approved noun in STE and cannot be used as a verb, "query" is only an approved noun in STE-Code. The STE version uses the approved verb "send" with the approved noun "query."*

Full data-access module, before:

```python
def get_users(db):
    # Query the database for user records that are active.
    rows = db.execute("SELECT * FROM users WHERE active = 1")
    return rows
```

Full data-access module, after:

```python
def get_users(db):
    # Send a query to the database for the user records that are active.
    rows = db.execute("SELECT * FROM users WHERE active = 1")
    return rows
```

**Pair B — "static" (approved adjective, not verb), adapted from "dim" (approved adjective, not verb).**

> **Non-STE:** Static the variable to prevent modification.

> **STE:** Make the variable static to prevent modification.

> *Adapted from spec pair: "dim" is an approved adjective but not a verb. Just as you cannot use "dim" as a verb in STE, you cannot use "static" as a verb in STE-Code. The STE version uses the approved verb "make" with the approved adjective "static."*

Full configuration constant, before:

```go
// Static the cache size so the value does not change at run time.
const cacheSize = 256
```

Full configuration constant, after:

```go
// Make the cache size static so the value does not change at run time.
const cacheSize = 256
```

---

## Code-Domain Explanation

Rule 1.2 enforces part-of-speech discipline across all code documentation types. Every approved word carries a label in the controlled terminology — verb (v), noun (n), adjective (adj), adverb (adv), preposition (prep), conjunction (conj), pronoun (pron), or article (art). You must use each word only in the grammatical role that its label permits. This section explains how the rule applies to each documentation type.

### README Files

README files mix procedural instructions (setup, build, run) with descriptive overviews. Part-of-speech violations in README files often occur when a writer converts a noun into a verb for brevity.

The most common violation pattern is noun-as-verb: using a code-domain technical noun like "Docker," "Git," or "npm" as a verb. "Docker the application" is a Rule 1.2 violation because "Docker" is a technical noun, not a verb. The correct STE-Code construction uses an approved verb with the technical noun as its object: "Use Docker to run the application."

Another frequent pattern is adjective-as-verb: using a property name like "secure," "empty," or "silent" as a verb. "Secure the endpoint" is a Rule 1.2 violation because "secure" is an approved adjective, not an approved verb. The STE-Code construction uses "make" with the adjective: "Make the endpoint secure."

Full README section, before:

```markdown
## Quick Start

1. Docker the app and deploy to production. If it fails, rollback.
2. Git your changes to the `main` branch after you green the build.
```

Full README section, after:

```markdown
## Quick Start

1. Use Docker to make a container for the application. Deploy the container to
   production. If the deployment fails, roll back to the previous version.
2. Save your changes with Git on the `main` branch after you make the build pass.
```

> **Non-STE:** Docker the app and deploy to production. If it fails, rollback.
>
> **STE:** Use Docker to make a container for the application. Deploy the container to production. If the deployment fails, roll back to the previous version.
> *(P2 applied: "Docker" is a noun, not a verb → "Use Docker." P2 applied: "rollback" as a verb → "roll back" using the approved verb "roll" with the adverb "back.")*

### API Documentation

API documentation describes function signatures, parameters, return types, and error conditions. The descriptive prose around parameter names and return values is where Rule 1.2 violations concentrate.

A common violation is using a code-domain technical noun like "cache," "map," or "filter" as a verb in the prose description. The parameter documentation may say "Caches the result for subsequent calls" where "cache" is a noun used as a verb. The STE-Code version uses an approved verb: "Keeps the result in the cache for later calls."

Status-code and error-condition descriptions also trigger Rule 1.2 when writers use adjectives as verbs: "Errors if the token is missing" uses "errors" as a verb. The correct form uses the approved noun "error" with an approved verb: "Gives an error if the token is not present."

Full route handler documentation, before:

```javascript
/**
 * POST /api/users
 * Creates a user. Caches the profile. Errors on duplicate email.
 * @param {UserInput} body - The user to create.
 * @returns {User} The created user record.
 */
app.post('/api/users', (req, res) => { /* ... */ });
```

Full route handler documentation, after:

```javascript
/**
 * POST /api/users
 * Makes a new user record. Keeps the profile in the cache.
 * Gives an error on a duplicate email address.
 * @param {UserInput} body - The user to make.
 * @returns {User} The user record that the function made.
 */
app.post('/api/users', (req, res) => { /* ... */ });
```

> **Non-STE:** POST /api/users — Creates a user. Caches the profile. Errors on duplicate email.
>
> **STE:** POST /api/users — Makes a new user record. Keeps the profile in the cache. Gives an error on a duplicate email address.
> *(P2 applied: "Creates" → "Makes"; "Caches" → "Keeps in the cache"; "Errors" → "Gives an error.")*

### Docstrings and Inline Comments

Docstrings and inline comments have limited space. This constraint tempts writers to compress sentences by converting nouns into verbs. Rule 1.2 requires that the compression does not change the part of speech.

In Python docstrings, the word "param" is a code-domain technical noun (short for "parameter"). "Param the input" is a Rule 1.2 violation. The correct form uses an approved verb: "Set the input parameter."

In inline comments, abbreviations like "init" (for "initialization") are code-domain technical nouns. "Init the connection" is a violation. The correct form uses an approved verb: "Start the connection" or "Make the connection ready."

Full Python module, before:

```python
def load_config(path):
    # init the pool, then cache the results, finally error if null
    pool = ConnectionPool(path)
    results = pool.query()
    if results is None:
        raise ValueError("no data")
    return results
```

Full Python module, after:

```python
def load_config(path):
    # Start the connection pool. Keep the results in the cache.
    # Give an error when the value is null.
    pool = ConnectionPool(path)
    results = pool.query()
    if results is None:
        raise ValueError("no data")
    return results
```

> **Non-STE:** # init the pool, then cache the results, finally error if null
>
> **STE:** # Start the connection pool. Keep the results in the cache. Give an error when the value is null.
> *(P2 applied: "init" as a verb → "Start"; "cache" as a verb → "Keep in the cache"; "error" as a verb → "Give an error.")*

### Commit Messages

Commit messages follow a conventional format with a type prefix and a short description. The type prefix (feat, fix, chore, docs, test, refactor) is not governed by Rule 1.2 — these are code-domain technical nouns. The description after the colon is where Rule 1.2 applies.

The description must use approved verbs in their approved imperative form. "Cache user sessions" is a Rule 1.2 violation because "cache" is a noun. "Add cache for user sessions" uses the approved verb "add."

When a commit message describes a refactor, the word "refactor" is a code-domain technical verb (permitted under Rule 1.12). But if the change is simple, prefer an approved verb: "fix" instead of "refactor to correct."

Full git history view, before:

```
$ git log --oneline -3
f3a1c9d fix: cache the query results to speed up the dashboard
b7e204a feat: socket the realtime notifications
a1c5580 chore: dependency the project before release
```

Full git history view, after:

```
$ git log --oneline -3
f3a1c9d fix: add a cache for query results to make the dashboard faster
b7e204a feat: use a socket for the realtime notifications
a1c5580 chore: get the dependencies before the release
```

> **Non-STE:** fix: cache the query results to speed up the dashboard
>
> **STE:** fix: add a cache for query results to make the dashboard faster
> *(P2 applied: "cache" as a verb → "add a cache." "Speed up" is a phrasal verb using "speed" as a verb — restructured to "make faster" using the approved adjective.)*

### Error Messages

Error messages are displayed to end users and logged for developers. Rule 1.2 ensures that error messages use nouns and verbs correctly so that non-native English speakers understand the message.

The word "fail" is an approved verb in the controlled terminology. "The connection failed" is correct. "The connection had a fail" uses "fail" as a noun, which is a Rule 1.2 violation. Use the approved noun "failure" instead, or restructure the sentence.

The word "timeout" is a code-domain technical noun. "The request timed out" uses "timed out" as a verb phrase derived from the noun. This is a Rule 1.2 violation. The STE-Code version uses an approved verb: "The request did not complete within the timeout period."

Full HTTP response body, before:

```json
{
  "error": "Connection timeout. The server timed out after 30s. Retry the operation."
}
```

Full HTTP response body, after:

```json
{
  "error": "Connection did not complete. The server did not answer within the 30-second timeout. Try the operation again."
}
```

> **Non-STE:** Error: Connection timeout. The server timed out after 30s.
>
> **STE:** Error: Connection did not complete. The server did not answer within the 30-second timeout.
> *(P2 applied: "timed out" as a verb → "did not answer within the timeout.")*

---

## Paradigm-Specific Guidance

Rule 1.2 applies to all code documentation regardless of programming paradigm. But each paradigm has its own vocabulary of technical nouns and verbs, and the boundary between approved words and part-of-speech violations shifts depending on the paradigm conventions.

### Object-Oriented (Java, C++, C#, Python Classes)

Object-oriented documentation uses class names, method names, and design pattern names as code-domain technical nouns. These are exempt from the approved-word requirement under Rule 1.5. But the prose that surrounds these technical nouns must still obey part-of-speech constraints.

The most common Rule 1.2 violation in OOP documentation is using class names as verbs. "Factory the object" is a violation — "Factory" is a technical noun (a design pattern name), not a verb. Use an approved verb: "Make the object with a factory."

Similarly, "Singleton the instance" is a violation. Use "Make the instance a singleton" or "Get the singleton instance."

Inheritance descriptions also trigger Rule 1.2 when writers use the base class name as a verb: "The Admin class Users the base class" is a violation. Use "The Admin class extends the User base class" or "The Admin class gets properties from the User base class."

Full class documentation, before:

```java
/**
 * The UserService singletons the connection pool and factories the
 * query builders. The Admin class Users the base class for auth.
 */
public class UserService {
    public void configure() { /* ... */ }
}
```

Full class documentation, after:

```java
/**
 * The UserService class uses a singleton pattern for the connection pool.
 * It makes query builders with a factory method.
 * The Admin class extends the User base class for authentication.
 */
public class UserService {
    public void configure() { /* ... */ }
}
```

> **Non-STE:** The `UserService` singletons the connection pool and factories the query builders.
>
> **STE:** The `UserService` class uses a singleton pattern for the connection pool. It makes query builders with a factory method.
> *(P2 applied: "singletons" as a verb → "uses a singleton pattern"; "factories" as a verb → "makes with a factory method.")*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional programming documentation uses terms like "map," "filter," "fold," "reduce," and "compose" as code-domain technical verbs. These are permitted under Rule 1.12 and are not governed by Rule 1.2 when used in their technical sense. But when these words appear in descriptive prose with a non-technical meaning, Rule 1.2 applies.

The word "map" is a code-domain technical verb meaning "transform each element of a collection by applying a function." When used in this technical sense, Rule 1.2 does not constrain it (Rule 1.12 takes priority). But when "map" is used as a noun in the general English sense ("a map of the system"), it is an approved noun in some contexts and an unapproved noun in others — check the controlled terminology.

The word "apply" has two valid uses: (1) as an approved general English verb meaning "put something on something" and (2) as a code-domain technical verb meaning "give arguments to a function." Both uses are valid under different rules, and Rule 1.2 does not conflict because "apply" is approved as a verb in the controlled terminology.

Full module documentation, before:

```haskell
-- Map the values through the transformer, then pipe the result
-- into the reducer so the report prints clean.
transform :: [Int] -> [Int]
transform xs = map (+1) xs
```

Full module documentation, after:

```haskell
-- Apply the `map` function to change each value. Then apply the
-- `pipe` function to send the result into the `reduce` function
-- so the report prints in a clean way.
transform :: [Int] -> [Int]
transform xs = map (+1) xs
```

> **Non-STE:** Map the values through the transformer, then pipe the result into the reducer.
>
> **STE:** Apply the `map` function to change each value. Then apply the `pipe` function to send the result into the `reduce` function.
> *(P2 applied: "pipe" as a verb → "apply the `pipe` function." "Map" remains valid as a technical verb. "Reducer" restructured to "`reduce` function" for clarity.)*

### Procedural (C, Go, Bash)

Procedural documentation uses direct imperative verbs. Rule 1.2 reinforces this by requiring that each imperative verb is an approved verb in the controlled terminology — not a noun or adjective forced into verb service.

In C documentation, the word "malloc" is a code-domain technical noun (the name of the standard library function). "Malloc a buffer" is a Rule 1.2 violation because "malloc" is a noun used as a verb. Use "Allocate a buffer with `malloc`" or, when applying Rule 1.1 strictly, "Make a buffer with `malloc`."

In Go documentation, "goroutine" is a code-domain technical noun. "Goroutine the task" is a violation. Use "Run the task in a goroutine."

In Bash documentation, commands are code-domain technical nouns (category 3, dev tools). "Grep the file" is a Rule 1.2 violation if "grep" is treated as a verb. Use "Use `grep` to find the text in the file."

Full C function, before:

```c
/* Malloc a struct, memset it to zero, then free it when done. */
void *make_record() {
    record_t *r = malloc(sizeof(record_t));
    memset(r, 0, sizeof(record_t));
    return r;
}
```

Full C function, after:

```c
/* Make a struct with `malloc`. Set all bytes to zero with `memset`.
   Free the struct when the operation is complete. */
void *make_record() {
    record_t *r = malloc(sizeof(record_t));
    memset(r, 0, sizeof(record_t));
    return r;
}
```

> **Non-STE:** Malloc a struct, memset it to zero, then free it when done.
>
> **STE:** Make a struct with `malloc`. Set all bytes to zero with `memset`. Free the struct when the operation is complete.
> *(P2 applied: "Malloc" as a verb → "Make with `malloc`"; "memset" as a verb → "Set with `memset`." The function names remain code-domain technical nouns. "Free" is a code-domain technical verb and is permitted.)*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes state and configuration rather than procedures. Rule 1.2 applies to the prose that explains what a configuration does, even though the configuration itself is declarative.

SQL keywords (SELECT, INSERT, UPDATE, DELETE) are code-domain technical verbs. When they appear inside code blocks, they are quoted text and Rule 1.2 does not apply. When they appear in prose, they are technical terms and must be marked with backticks. But the prose around them must use approved parts of speech.

"SELECT from the table" is incorrect in prose because "SELECT" is a technical verb used as a general verb and it is not marked as code. The correct prose is "Use `SELECT` to get data from the table."

In Terraform documentation, resource names like "aws_instance" are code-domain technical nouns. "Terraform the infrastructure" is a Rule 1.2 violation — "Terraform" is a technical noun, not a verb. Use "Use Terraform to make the infrastructure."

Full deploy script documentation, before:

```bash
# Terraform the VPC, then Kubectl the pods into the cluster.
terraform apply -target=module.vpc
kubectl apply -f pods.yaml
```

Full deploy script documentation, after:

```bash
# Use Terraform to make the VPC. Use `kubectl` to apply the
# pod configuration to the cluster.
terraform apply -target=module.vpc
kubectl apply -f pods.yaml
```

> **Non-STE:** Terraform the VPC, then Kubectl the pods into the cluster.
>
> **STE:** Use Terraform to make the VPC. Use `kubectl` to apply the pod configuration to the cluster.
> *(P2 applied: "Terraform" as a verb → "Use Terraform"; "Kubectl" as a verb → "Use `kubectl`.")*

### Systems (Rust Ownership, C Memory Management)

Systems documentation explains ownership, lifetimes, memory layout, and concurrency. These concepts have dense technical vocabularies. Rule 1.2 requires that the framing prose around these technical terms respects part-of-speech boundaries.

In Rust documentation, "borrow," "own," and "move" are code-domain technical verbs and are permitted under Rule 1.12. "Drop" is a code-domain technical noun (the `Drop` trait). "Drop the value" is a Rule 1.2 violation if "Drop" is used as a verb without backtick marking. Use "The value runs its `Drop` implementation" or "The value is dropped" (where "dropped" is the past participle of the technical verb "drop").

"Unsafe" is an approved adjective in the controlled terminology (meaning "not safe"). In Rust, "unsafe" is also a keyword and a code-domain technical noun (an `unsafe` block). When used as a keyword, mark it with backticks. When used as a descriptive adjective, it follows Rule 1.2 as an adjective.

Full Rust function documentation, before:

```rust
/// The function unsafes the pointer access and drops the guard afterwards.
fn release(ptr: *mut u8, guard: Guard) {
    unsafe { *ptr = 0; }
    drop(guard);
}
```

Full Rust function documentation, after:

```rust
/// The function uses `unsafe` for the pointer access. It runs the
/// `Drop` implementation for the guard afterwards.
fn release(ptr: *mut u8, guard: Guard) {
    unsafe { *ptr = 0; }
    drop(guard);
}
```

> **Non-STE:** The function unsafes the pointer access and drops the guard afterwards.
>
> **STE:** The function uses `unsafe` for the pointer access. It runs the `Drop` implementation for the guard afterwards.
> *(P2 applied: "unsafes" as a verb → "uses `unsafe`"; "drops" as a verb without marking → "runs the `Drop` implementation.")*

---

## Extended Examples

Each example pair below shows a real code documentation scenario, the STE-Code compliant rewrite, which principle was applied, and an explanation of the fix.

> *Adapted from spec pair:* Non-STE: "Test the system for leaks." | STE: "Do the leak test of the system."

### Example 1 — README: Build and Run Instructions

Full README snippet, before:

```markdown
# Getting Started

Clone the repo, then npm install to dependency the project.
Webpack the bundle and express the server on port 3000.
```

Full README snippet, after:

```markdown
# Getting Started

Clone the repository. Run `npm install` to get the dependencies.
Use `webpack` to make the bundle. Start the Express server on port 3000.
```

> **Non-STE:** Clone the repo, then npm install to dependency the project. Webpack the bundle and express the server on port 3000.
>
> **STE:** Clone the repository. Run `npm install` to get the dependencies. Use `webpack` to make the bundle. Start the Express server on port 3000.

> **Principles applied:** P2 (use approved part of speech: "dependency" is a noun → "get the dependencies"; "Webpack" is a noun → "Use `webpack`"; "express" is a noun → "Start the Express server").
> **Explanation:** Three separate part-of-speech violations in one instruction block. "Dependency" is an approved noun in the controlled terminology — it cannot be used as a verb meaning "install dependencies." "Webpack" is a code-domain technical noun (a build tool name) — it cannot be used as a verb meaning "build with webpack." "Express" is a code-domain technical noun (a framework name) — it cannot be used as a verb meaning "serve with Express." The STE version introduces approved verbs ("run," "get," "use," "make," "start") to carry the action while keeping the technical nouns in their correct grammatical role.

### Example 2 — API Docstring: JSDoc for an Express Route Handler

Full JSDoc block, before:

```javascript
/**
 * GET /api/products/:id
 * @param {string} id - The product ID to query from the DB.
 * @returns {Product} The matched product object.
 * @throws {NotFoundError} Errors if the ID doesn't match any product.
 */
function getProduct(req, res) { /* ... */ }
```

Full JSDoc block, after:

```javascript
/**
 * GET /api/products/:id
 * @param {string} id - The product ID. The handler sends a query to
 *   the database with this ID.
 * @returns {Product} The product object that matches the ID.
 * @throws {NotFoundError} Gives this error when no product matches the ID.
 */
function getProduct(req, res) { /* ... */ }
```

> **Non-STE:** /**
>  * GET /api/products/:id
>  * @param {string} id - The product ID to query from the DB.
>  * @returns {Product} The matched product object.
>  * @throws {NotFoundError} Errors if the ID doesn't match any product.
>  */
> **STE:** /**
>  * GET /api/products/:id
>  * @param {string} id - The product ID. The handler sends a query to the database with this ID.
>  * @returns {Product} The product object that matches the ID.
>  * @throws {NotFoundError} Gives this error when no product matches the ID.
>  */

> **Principles applied:** P2 (use approved part of speech: "query" is a noun → "sends a query"; "errors" as a verb → "Gives this error"); P13 (do not use technical verbs as nouns: "matched" is fine as an adjective here since "match" is approved as both verb and noun).
> **Explanation:** "Query" is a code-domain technical noun (database request) — it cannot be used as a verb meaning "to request data from the database." The STE version uses the approved verb "send" with the technical noun "query." "Errors" used as a verb is a Rule 1.2 violation — "error" is an approved noun, not a verb. The correct construction uses the verb "give" with the noun phrase "this error." Note that `NotFoundError` is a code-domain technical noun (category 14, error states) and remains unchanged.

### Example 3 — Commit Message: Repository Pattern Refactor

Full commit log, before:

```
$ git log --oneline -1
c0ffee1 refactor: interface the user repository and factory the database connection
```

Full commit log, after:

```
$ git log --oneline -1
c0ffee1 refactor: add an interface to the user repository and use a factory for the database connection
```

> **Non-STE:** refactor: interface the user repository and factory the database connection
>
> **STE:** refactor: add an interface to the user repository and use a factory for the database connection

> **Principles applied:** P2 (use approved part of speech: "interface" is a noun → "add an interface"; "factory" is a noun → "use a factory"); P1 (use approved words: "add" and "use" are approved verbs).
> **Explanation:** "Interface" is a code-domain technical noun (an OOP contract type) — it cannot be used as a verb meaning "to add an interface to." "Factory" is a code-domain technical noun (a design pattern name) — it cannot be used as a verb meaning "to create with a factory." The STE version introduces the approved verbs "add" and "use" to carry the actions. The trade-off is a longer commit message, but the meaning is unambiguous to all readers regardless of native language.

### Example 4 — Error Message: Database Connection Failure

Full application log output, before:

```
FATAL: Could not database the connection. The pool is empty.
Retry the operation or contact your admin.
```

Full application log output, after:

```
FATAL: Could not connect to the database. The connection pool has no
available connections. Try the operation again or speak to your
administrator.
```

> **Non-STE:** FATAL: Could not database the connection. The pool is empty. Retry the operation or contact your admin.
>
> **STE:** FATAL: Could not connect to the database. The connection pool has no available connections. Try the operation again or speak to your administrator.

> **Principles applied:** P2 (use approved part of speech: "database" is a noun → "connect to the database"; "empty" used without a verb → "has no available connections"); P1 (use approved words: "retry" → "try again"; "contact" → "speak to"; "admin" → "administrator").
> **Explanation:** "Database" is a code-domain technical noun (category 9, data stores) — it cannot be used as a verb meaning "to connect to a database." The STE version uses the approved verb "connect" with the technical noun "database." "Empty" is an approved adjective — the sentence "The pool is empty" is grammatically correct but ambiguous (does "empty" mean zero connections, or zero available connections?). The STE version makes the state explicit: "has no available connections."

### Example 5 — Python Docstring: Class Constructor

Full Python class, before:

```python
class CacheManager:
    def __init__(self, config: dict) -> None:
        """
        Constructs a new CacheManager instance.

        Configs the Redis client with the provided settings.
        Defaults the TTL to 3600 seconds when no TTL is specified.
        """
        self.client = redis.Redis(**config)
        self.ttl = 3600
```

Full Python class, after:

```python
class CacheManager:
    def __init__(self, config: dict) -> None:
        """
        Makes a new CacheManager instance.

        Sets the Redis client configuration from the given settings.
        Uses a TTL of 3600 seconds when no TTL is given.
        """
        self.client = redis.Redis(**config)
        self.ttl = 3600
```

> **Non-STE:** def __init__(self, config: dict) -> None:
>     """
>     Constructs a new CacheManager instance.
>
>     Configs the Redis client with the provided settings.
>     Defaults the TTL to 3600 seconds when no TTL is specified.
>     """
> **STE:** def __init__(self, config: dict) -> None:
>     """
>     Makes a new CacheManager instance.
>
>     Sets the Redis client configuration from the given settings.
>     Uses a TTL of 3600 seconds when no TTL is given.
>     """

> **Principles applied:** P2 (use approved part of speech: "Configs" as a verb → "Sets the configuration"; "Defaults" as a verb → "Uses a default"); P1 (use approved words: "Constructs" → "Makes"; "provided" → "given"; "specified" → "given").
> **Explanation:** "Config" is a code-domain technical noun (short for "configuration") — it cannot be used as a verb meaning "to set the configuration of." "Default" is an approved noun meaning "a preset value" — it cannot be used as a verb meaning "to set to the default value." The STE version uses approved verbs ("set," "use") to carry the actions while keeping the nouns ("configuration," "TTL") in their correct roles. The word "Constructs" is replaced with "Makes" per the canonical synonym table (P1).

### Example 6 — Configuration File Comment: YAML with Docker Compose

Full compose file, before:

```yaml
# This compose file orchestrates three services:
# - The API server, which endpoints the HTTP traffic
# - The worker, which queues the background jobs
# - The database, which stores the persistent data
services:
  api:
    image: api:1.0
  worker:
    image: worker:1.0
  db:
    image: postgres:16
```

Full compose file, after:

```yaml
# This compose file controls three services:
# - The API server, which handles HTTP traffic at its endpoints
# - The worker, which puts background jobs in the queue
# - The database, which keeps the persistent data
services:
  api:
    image: api:1.0
  worker:
    image: worker:1.0
  db:
    image: postgres:16
```

> **Non-STE:** # This compose file orchestrates three services:
> # - The API server, which endpoints the HTTP traffic
> # - The worker, which queues the background jobs
> # - The database, which stores the persistent data
> **STE:** # This compose file controls three services:
> # - The API server, which handles HTTP traffic at its endpoints
> # - The worker, which puts background jobs in the queue
> # - The database, which keeps the persistent data

> **Principles applied:** P2 (use approved part of speech: "endpoints" as a verb → "handles at its endpoints"; "queues" as a verb → "puts in the queue"); P1 (use approved words: "orchestrates" → "controls"; "stores" → "keeps").
> **Explanation:** "Endpoint" is a code-domain technical noun (category 8, routing and state) — it cannot be used as a verb meaning "to handle HTTP requests at endpoints." "Queue" is a code-domain technical noun (category 6, modules and services) — it cannot be used as a verb meaning "to put messages into a queue." Both are corrected by introducing approved verbs ("handles," "puts") and keeping the technical nouns in prepositional phrases. The word "orchestrates" is corrected per P1 to "controls."

### Example 7 — Unit Test: Name and Assertion Message

A unit test file mixes code and human-readable descriptions. The test name (a sentence) and the assertion message are prose, so Rule 1.2 applies to them even though the code itself is exempt.

Full test module, before:

```python
def test_cache_eviction():
    cache = Cache(max_size=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)  # should garbage the oldest entry
    assert cache.size() == 2
    assert not cache.contains("a")
```

Full test module, after:

```python
def test_cache_eviction():
    cache = Cache(max_size=2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)  # should remove the oldest entry
    assert cache.size() == 2
    assert not cache.contains("a")
```

> **Non-STE:** # should garbage the oldest entry
>
> **STE:** # should remove the oldest entry

> **Principles applied:** P2 (use approved part of speech: "garbage" is a noun → "remove"); P1 (use approved words: "remove" is an approved verb).
> **Explanation:** "Garbage" is a code-domain technical noun (waste data) — it cannot be used as a verb meaning "to delete." The comment is prose that explains the assertion, so Rule 1.2 applies. The STE version uses the approved verb "remove." The test function name `test_cache_eviction` stays unchanged because it is a code identifier (Rule 1.5, category 10).

### Example 8 — CI/CD Pipeline: Step Descriptions

Pipeline configuration files (YAML) contain step names and echo messages that are prose. Rule 1.2 applies to those strings even though the YAML keys and shell commands are exempt.

Full workflow file, before:

```yaml
name: build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Docker the image
        run: docker build -t app:1.0 .
      - name: Artifact the binary
        run: mv app dist/app
```

Full workflow file, after:

```yaml
name: build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Use Docker to make the image
        run: docker build -t app:1.0 .
      - name: Put the binary in the artifact
        run: mv app dist/app
```

> **Non-STE:** - name: Docker the image / - name: Artifact the binary
>
> **STE:** - name: Use Docker to make the image / - name: Put the binary in the artifact

> **Principles applied:** P2 (use approved part of speech: "Docker" is a noun → "Use Docker"; "Artifact" is a noun → "Put in the artifact"); P1 (use approved words: "make" and "put" are approved verbs).
> **Explanation:** The `name:` fields are prose that a human reads in the CI log, so Rule 1.2 applies. "Docker" is a code-domain technical noun (a tool name) — it cannot be used as a verb. "Artifact" is a code-domain technical noun (category 13, build output) — it cannot be used as a verb. The `run:` shell commands stay unchanged because they are code (Rule 1.5, category 10).

---

## Edge Cases

The following scenarios show where the boundary between approved parts of speech and code-domain usage requires careful judgment.

### Edge Case 1: Word Approved as Both Noun and Verb — Ambiguity in Context

**Scenario:** A word like "commit" is approved as both a noun and a verb in the controlled terminology. The sentence "Make a commit" uses "commit" as a noun (correct). The sentence "Commit the changes" uses "commit" as a verb (also correct). But the sentence "The commit committed the commit" uses the word three times with ambiguous roles and is difficult to parse.

**Guidance:** When a word is approved as more than one part of speech, the context must make the role clear. If the same word appears multiple times in one sentence with different roles, restructure the sentence to use different approved words. For "commit," use "commit" as the verb and "change set" as the noun when both roles must appear in the same sentence.

Full changelog entry, before:

```
## 2026-08-01
The commit committed the files to the commit history and passed CI.
```

Full changelog entry, after:

```
## 2026-08-01
The `git commit` command added the files to the change history and passed CI.
```

> **Non-STE:** The commit committed the files to the commit history.
>
> **STE:** The `git commit` command added the files to the change history.
> *(P11 applied: one term per concept — use "change history" instead of "commit history" to avoid the double "commit.")*

### Edge Case 2: Framework CLI Command Used as a Verb

**Scenario:** Many frameworks provide CLI commands that developers use as verbs in documentation. For example, "Docker compose up," "npm install," "kubectl apply." The CLI command itself contains a verb ("up," "install," "apply"), but the tool name ("Docker," "npm," "kubectl") is used as if it were a verb.

**Guidance:** The tool name is a code-domain technical noun. When writing prose documentation, always introduce an approved verb before the tool name: "Use Docker to start the containers" instead of "Docker the containers." When quoting a CLI command literally inside a code block, the command is quoted text (Rule 1.5, category 10) and Rule 1.2 does not apply. The distinction is between prose (must follow Rule 1.2) and code blocks (exempt).

Full deploy runbook, before:

```
1. Build the image.
2. Kubectl the deployment into the cluster.
3. Check the pods.
```

Full deploy runbook, after:

```
1. Build the image.
2. Use `kubectl apply` to send the deployment to the cluster.
3. Check the pods.
```

> **Non-STE:** Kubectl the deployment into the cluster.
>
> **STE:** Use `kubectl apply` to send the deployment to the cluster.
> *(P2 applied: "Kubectl" as a verb → "Use `kubectl apply`." The CLI command `kubectl apply` is a compound technical noun.)*

### Edge Case 3: Adjective Used as a Verb in a Standard Industry Phrase

**Scenario:** Some adjective-as-verb constructions are so common in the software industry that they function as de facto technical verbs. For example, "to green the build" (make the CI pipeline pass), "to yellow the test" (mark a test as flaky), "to red the deployment" (to cause a deployment failure).

**Guidance:** These are jargon (violation of Rule 1.10) and part-of-speech violations (Rule 1.2). They are not permitted in STE-Code regardless of how common they are. Use approved constructions: "Make the build pass," "Mark the test as flaky," "Cause the deployment to fail." Color-based status terminology is especially problematic for accessibility and translation — avoid it entirely.

Full team chat note, before:

```
We need to green the CI before we can ship. The flaky test is yellowed.
```

Full team chat note, after:

```
We must make the CI pipeline pass before we can deploy. The flaky test
is marked as flaky.
```

> **Non-STE:** We need to green the CI before we can ship.
>
> **STE:** We must make the CI pipeline pass before we can deploy.
> *(P2 applied: "green" as a verb → "make pass"; P10 applied: "ship" is slang → "deploy.")*

### Edge Case 4: Language-Keyword Noun Used as a Verb in Prose

**Scenario:** A programming language keyword like `import`, `export`, `return`, or `yield` is a code-domain technical noun when marked with backticks. But writers often use these keywords as verbs in prose without backticks: "Import the module," "Export the function," "Return the value."

**Guidance:** When used as a verb in prose without backticks, the word must be an approved verb in the controlled terminology. "Return" is approved as a verb (meaning "send a value back from a function") — "Return the value" is correct. "Import" is not an approved verb in the controlled terminology — "Import the module" is a Rule 1.2 violation. Use "Add the module with `import`" or "Use `import` to add the module." "Export" is not an approved verb — use "Make the function available with `export`."

Full module header comment, before:

```javascript
// Import the helper, export the main function, and return the result.
import { helper } from './helper.js';
export function main() { return helper(); }
```

Full module header comment, after:

```javascript
// Use `import` to add the helper. Use `export` to make the main
// function available. Return the result.
import { helper } from './helper.js';
export function main() { return helper(); }
```

> **Non-STE:** Import the helper, export the main function, and return the result.
>
> **STE:** Use `import` to add the helper. Use `export` to make the main function available. Return the result.
> *(P2 applied: "Import" as a verb without backticks → "Use `import`"; "Export" as a verb without backticks → "Use `export`." "Return" is an approved verb and remains unchanged.)*

### Edge Case 5: Past Participle of a Noun-Derived Technical Verb

**Scenario:** Some code-domain technical verbs are derived from nouns and have irregular past participles. For example, "input" (technical verb) → "input" or "inputted" (past participle). "Output" → "output" or "outputted." "Broadcast" → "broadcast" or "broadcasted."

**Guidance:** Rule 1.2 applies to the base form of the word. When a code-domain technical verb is permitted under Rule 1.12, its inflected forms (past, past participle, present participle) follow the conventions of the programming language or domain, not the approved verb forms of Rule 1.4. But when the verb is an approved word in the controlled terminology, Rule 1.4 applies and only the approved inflected forms are permitted.

For "input" and "output" — these are code-domain technical verbs. Their past participles follow domain convention. For approved verbs like "run" (ran, running) or "set" (set, setting), only the forms listed in the controlled terminology are permitted.

Full data pipeline log, before:

```
The user inputted the data and the system outputted the report at 09:00.
```

Full data pipeline log, after:

```
The user gave the data as input. The system wrote the report as output
at 09:00.
```

> **Non-STE:** The user inputted the data and the system outputted the report.
>
> **STE:** The user gave the data as input. The system wrote the report as output.
> *(P2 applied: "inputted" and "outputted" are rare and awkward forms. The STE version uses the approved nouns "input" and "output" with approved verbs "gave" and "wrote.")*

---

## Cross-References

This rule is part of Section 1 (Words) of the STE-Code specification. It interacts with every other rule in Section 1.

| Rule | Title | Relationship to Rule 1.2 |
|------|-------|---------------------------|
| **Rule 1.1** | Use Approved Words from the Dictionary, Technical Nouns, or Technical Verbs | Rule 1.1 determines which words are approved. Rule 1.2 then constrains how those approved words may be used — only as their specified part of speech. A word that passes Rule 1.1 as an approved noun must still pass Rule 1.2: it cannot be used as a verb. |
| **Rule 1.3** | Use Approved Words Only with Their Approved Meanings | Rule 1.2 constrains part of speech. Rule 1.3 constrains meaning within that part of speech. A word approved as both a noun and a verb (Rule 1.2 permits both roles) must still be used with the approved meaning for each role (Rule 1.3). |
| **Rule 1.4** | Use Only the Approved Verb Forms and Adjective Forms | Rule 1.2 determines the valid part of speech. Rule 1.4 determines which morphological forms of that part of speech are permitted. For example, Rule 1.2 confirms that "run" is an approved verb; Rule 1.4 confirms that "ran" and "running" are approved forms but "runned" is not. |
| **Rule 1.5** | You Can Use Words That You Can Include in a Technical Noun Category | Technical nouns are exempt from the approved-word requirement of Rule 1.1. But Rule 1.2 still constrains them: a technical noun must not be used as a verb. |
| **Rule 1.7** | Do Not Use Technical Nouns as Verbs | Rule 1.7 is a direct consequence of Rule 1.2 applied to technical nouns. A word that passes Rule 1.5 as a technical noun is still a noun — Rule 1.7 forbids using it as a verb. |
| **Rule 1.12** | Technical Verbs Are Allowed | When a word is a code-domain technical verb, Rule 1.12 overrides the part-of-speech constraint of Rule 1.2 for that specific word in that specific context. Rule 1.2 still applies to all other words in the sentence. |
| **Rule 1.13** | Do Not Use Technical Verbs as Nouns | Rule 1.13 is the inverse of Rule 1.7 and a consequence of Rule 1.2 applied to technical verbs. A word permitted as a technical verb under Rule 1.12 must not be used as a noun. |

**Dictionary reference:** See `a-dictionary.md` for the full STE-Code controlled terminology. Each approved word entry includes its part of speech in parentheses — verb (v), noun (n), adjective (adj), adverb (adv), preposition (prep), conjunction (conj), pronoun (pron), article (art). Before you use any approved word, check its part of speech in the dictionary. Unapproved words are listed with their approved alternatives and the part of speech of each alternative.

**Key dictionary entries referenced in this rule:**

- **TEST (n):** Approved noun. Permitted in phrases like "do a test" and "run the tests." TEST (v) is listed as UNAPPROVED and also as a technical verb (TV) under Rule 1.12.
- **QUERY (n):** Technical noun (TN). A request to a database. Not approved as a verb. Use "send a query" or "run a query."
- **CALL (v):** Listed as UNAPPROVED for general English meanings. Permitted as a technical verb (TV) under Rule 1.12 when meaning "invoke a function." Also approved as a noun in the controlled terminology.
- **CLEAN (v), CLEAN (adj):** Both approved. Position in the sentence determines the part of speech: "Clean the files" (verb) vs. "The files are clean" (adjective).
- **STATIC (adj):** Approved adjective in the controlled terminology. Not approved as a verb. Use "make static" for the verb sense.

**Categories reference:** See `a-categories.md` for the 19 code-domain technical noun categories defined under Rule 1.5. Technical nouns from these categories are exempt from Rule 1.2's part-of-speech constraint only when they remain nouns — they must not be used as verbs.

---

## Grammar Notes

### The Part-of-Speech Gate Model

Rule 1.2 functions as a grammatical gate that every approved word must pass. The gate has two checks:

1. **Is the word in the controlled terminology as an approved word?** If the word is not in the controlled terminology, it must pass through a different gate (Rule 1.5 for technical nouns, Rule 1.12 for technical verbs). If it is in the controlled terminology but listed as UNAPPROVED, it cannot pass through this gate.
2. **Is the word used as its specified part of speech?** If the word is approved as a noun but the sentence uses it as a verb, it fails this check. The word must be replaced or the sentence must be restructured.

A word passes through the gate only when both checks succeed. This gate model is stricter than the three-gate model of Rule 1.1 because Rule 1.2 adds the grammatical role constraint on top of the vocabulary constraint.

### Grammatical Role Identification

To apply Rule 1.2 correctly, you must identify the grammatical role of each approved word in the sentence. The role is determined by the word's position and function in the sentence, not by the writer's intention.

**Verbs** carry the action of the sentence. In English, the verb typically follows the subject: "The function [verb] the data." In imperative sentences, the verb is the first word: "[Verb] the data."

**Nouns** name entities, concepts, or objects. They typically appear as the subject, the object of a verb, or the object of a preposition: "The [noun] processes the [noun]."

**Adjectives** modify nouns. They typically appear before the noun they modify or after a linking verb: "The [adjective] function" or "The function is [adjective]."

**Adverbs** modify verbs, adjectives, or other adverbs. They typically appear after the verb or before the adjective: "The function runs [adverb]" or "The function is [adverb] [adjective]."

When a word can play more than one role (like "commit" which is both a noun and a verb), the sentence structure determines which role is active. If the role is ambiguous, restructure the sentence to make the role clear.

### The Noun-as-Verb Pattern — Most Common Violation

The most frequent Rule 1.2 violation in code documentation is the noun-as-verb pattern. A code-domain technical noun — often a tool name, framework name, or data structure name — is used as a verb for brevity.

The pattern: `[TechnicalNoun] the [object]`

Examples:
- "Git the changes"
- "Docker the app"
- "Cache the results"
- "Queue the jobs"
- "Index the records"
- "Log the errors"

The STE-Code fix follows one of three patterns:

1. **Prepositional phrase:** Use an approved verb with the noun in a prepositional phrase.
   - "Git the changes" → "Save the changes with Git"
   - "Cache the results" → "Keep the results in the cache"

2. **Infinitive construction:** Use an approved verb with an infinitive that contains the noun.
   - "Queue the jobs" → "Use the queue to hold the jobs"
   - "Index the records" → "Use the index to find the records"

3. **Make + adjective construction:** When the noun has a corresponding approved adjective.
   - "Secure the endpoint" → "Make the endpoint secure"
   - "Empty the buffer" → "Make the buffer empty"

Choose the pattern that produces the shortest, clearest sentence while keeping all words in their approved parts of speech.

### The Adjective-as-Verb Pattern — Second Most Common Violation

The second most frequent Rule 1.2 violation is using an approved adjective as a verb. This often occurs with property-setting descriptions.

The pattern: `[Adjective] the [object]`

Examples:
- "Clear the cache"
- "Secure the connection"
- "Empty the queue"
- "Warm the cache"
- "Silent the logs"

Note: Some of these words are approved as both adjectives and verbs. "Clear" is approved as both an adjective and a verb — "Clear the cache" is correct. "Secure" is approved as an adjective but not as a verb — "Secure the connection" is a violation. "Empty" is approved as an adjective — "Empty the queue" is a violation.

The STE-Code fix uses the pattern: **Make + adjective**

- "Secure the connection" → "Make the connection secure"
- "Empty the queue" → "Make the queue empty"

When the word is approved as both adjective and verb (like "clear"), either form is correct, but the imperative verb form is preferred for procedures: "Clear the cache" is better than "Make the cache clear" because it is shorter and uses a single approved verb.

### Interaction with Rule 1.12 — Technical Verb Override

Rule 1.12 permits code-domain technical verbs even when they are not in the approved word list. This creates an important exception to Rule 1.2: when a word is a code-domain technical verb, Rule 1.12 overrides Rule 1.2 for that specific word in that specific context.

For example, "serialize" is not in the approved word list. Rule 1.2 would normally reject "serialize" as a verb. But "serialize" is a code-domain technical verb (data transformation operation) and is permitted under Rule 1.12. The override applies only to the verb use of "serialize" — if "serialize" were used as a noun ("The serialize failed"), Rule 1.13 would reject it.

The override does not apply to all uses of the word. "Test" is an approved noun but not an approved verb in the basic controlled terminology. As a technical verb (meaning "execute test cases"), "test" is permitted under Rule 1.12 in sentences like "Test the module." But this is a domain-specific technical use. If the writer means "examine generally," the approved verb "check" should be used instead: "Check the output" not "Test the output" (unless "test" refers specifically to running test cases).

### Past Participle and Present Participle Forms

Rule 1.2 constrains the base part of speech. Rule 1.4 constrains the inflected forms. Together, they prevent the use of unapproved participle forms.

An approved verb like "run" has the approved forms: run, runs, ran, running. "Running" as a present participle is approved when used as part of a verb phrase: "The server is running." "Running" as a gerund (a noun form) is not approved: "The running of the server" is a violation. Use the approved noun form instead: "The operation of the server."

An approved adjective like "correct" has the approved forms: correct, more correct, most correct. "Correcting" as a present participle derived from the adjective is not approved: "The correcting process" is a violation. Use the adjective directly: "The correction process" or restructure: "The process that makes the data correct."

When a code-domain technical verb is used under Rule 1.12, its participle forms follow domain convention. "Serializing" is acceptable in "The serializing step" because "serialize" is a technical verb. But when an approved general-purpose verb can express the same meaning, prefer the approved verb: "The step that serializes the data" is clearer than "The serializing step."

### Historical Note: ASD-STE100 Precedent

In ASD-STE100 Issue 9, Rule 1.2 is presented as a grammatical discipline rule that operates on the foundation of Rule 1.1. The aerospace specification devotes considerable attention to the part-of-speech labels in the dictionary and to the grammatical justification for restricting each word to its labeled role. The examples ("test" as noun, "dim" as adjective, "clean" as verb and adjective) are carefully chosen to illustrate the three most common violation patterns: noun-as-verb, adjective-as-verb, and the special case of words approved as multiple parts of speech.

The aerospace specification emphasizes that part-of-speech discipline is not an arbitrary constraint — it is a safety measure. When a word changes its grammatical role, its meaning can shift in ways that non-native readers do not expect. "Test the system" (using "test" as a verb) is grammatically correct English but violates STE because "test" is only approved as a noun. The aerospace justification is that non-native readers may not recognize that "test" as a verb carries the same meaning as "test" as a noun.

STE-Code adopts the same justification for code documentation. When a writer uses "Docker" as a verb, a non-native reader must infer that "Docker" means "use the Docker tool to containerize." When a writer uses "cache" as a verb, the reader must infer that "cache" means "store in the cache." These inferences are easy for native English speakers but create ambiguity for the global developer audience. Rule 1.2 removes the inference by requiring that each word stays in its approved grammatical role.

The ASD-STE100 Issue 9 also notes that Rule 1.2 interacts with Rule 1.12 (Technical Verbs). In the aerospace domain, a technical verb like "ream" is permitted even though it is not in the approved word list. STE-Code follows the same pattern: "serialize," "memoize," "normalize," and other code-domain technical verbs are permitted under Rule 1.12 even though they are not in the general approved word list. The key distinction is that the technical verb exception applies only to domain-specific operations that have no simple approved-word alternative.

---

## See also

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** Rule 1.3 — Use Approved Words Only with Their Approved Meanings
> **See also:** Rule 1.4 — Use Only the Approved Verb Forms and Adjective Forms
> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category
> **See also:** Rule 1.7 — Do Not Use Technical Nouns as Verbs
> **See also:** Rule 1.10 — Do Not Use Jargon, Slang, or Clipped Forms
> **See also:** Rule 1.12 — Technical Verbs Are Allowed
> **See also:** Rule 1.13 — Do Not Use Technical Verbs as Nouns

---

<!-- a-sec1-rule1.3.md -->

# Rule 1.3 — Use Approved Words Only with Their Approved Meanings

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.3](ste-code/grouped/), Rule 1.3

## Original Rule

**Rule 1.3** Use approved words only with their approved meanings.

Each approved word in the dictionary has a specified approved meaning. Some of these words can have more restricted meanings compared with their meanings in standard English. Always use the approved words only with their approved meanings.

Examples:

The approved meaning of the verb "follow" is "come after, go after."

> **STE:** Do the procedures that follow:

You cannot use the verb "follow" with other meanings that are not approved.

In this sentence, always use "obey" with the approved meaning "to do that which the procedures or instructions tell you."

## STE-Code Adaptation

**Rule 1.3** Use approved words only with their approved meanings.

Each approved word in the controlled terminology has a specified approved meaning. Some of these words can have more restricted meanings compared with their meanings in standard English. Always use the approved words only with their approved meanings.

The approved meaning of the verb "follow" is "come after, go after." You can use "follow" to describe the sequence of steps in a procedure. This is the same approved meaning as in the spec — the verb "follow" carries over directly from STE to STE-Code because procedural writing occurs in both domains.

The approved meaning of the verb "obey" is "to do that which the procedures or instructions tell you." You can use "obey" to tell the reader to comply with instructions. This is the same approved meaning as in the spec and carries over directly to STE-Code.

When an approved word has only one approved meaning in the controlled terminology, do not use it with any other meaning from standard English. If you need to express a different meaning, find an alternative approved word or use a different sentence construction.

### Decision Procedure: How to Check a Word Against Rule 1.3

Before you publish any code documentation, run every approved verb, noun, adjective, or adverb you used through this four-step check. The check is cheap and catches the most common class of documentation defect: a sentence that looks correct and uses an approved word, but assigns that word a meaning it does not have.

1. **Identify the part of speech in your sentence.** Is the word a verb, noun, adjective, or adverb in the way you wrote it? Write it down. (This step belongs to Rule 1.2, but Rule 1.3 depends on it — the part of speech selects the meaning.)
2. **Look up the approved meaning for that part of speech** in `a-dictionary.md`. Each entry lists the approved meaning(s) and, for polysemous words, the meaning tied to each part of speech.
3. **Ask the only question that matters: does my sentence use the word with exactly that meaning?** If yes, the word passes. If no — even if the word is approved and the sentence reads smoothly — the word fails Rule 1.3.
4. **Replace or restructure.** If the word fails, either swap it for an approved word whose meaning fits the context (for example, "operate" instead of "run" when you mean "function on a platform") or rewrite the sentence so the original approved word carries its approved meaning.

Worked check — a README line:

> **Sentence:** The background worker runs every night.
> **Step 1:** "runs" is a verb.
> **Step 2:** The approved meaning of the verb "run" is "execute a program or command."
> **Step 3:** The writer means "operates" or "executes on a schedule," not "executes a program." The meaning does not match.
> **Step 4:** Rewrite: "The background worker operates every night." (Approved meaning of "operate" = "function or work in a specified way" — match.)

This procedure is the difference between a document that is merely grammatical and a document that is unambiguous. A reader who sees "the job runs" assumes execution; if you meant "the job continues," the documentation is wrong even though "run" is an approved verb.

### Examples

> *Adapted from spec pair:* Non-STE: "Follow the instructions to complete the task." | STE: "Obey the instructions to complete the task." *(ASD-STE100 Issue 9, Rule 1.3: approved meaning of "follow" = "come after, go after"; approved meaning of "obey" = "to do that which the procedures or instructions tell you")*

> **Non-STE:**

```markdown
## Install

Follow the configuration steps to set up the server. After you follow
the steps, the service starts and listens on port 8080.
```

> **STE:**

```markdown
## Install

Obey the configuration instructions to set up the server. After you do
the steps that follow, the service starts and listens on port 8080.
```

> *Adapted from spec concept: "follow" (approved meaning: "come after, go after") is misused to mean "act in accordance with." In the spec, you must use "obey" when you mean "comply with instructions." The same distinction applies in STE-Code: use "follow" only for sequence ("Do the steps that follow") and use "obey" for compliance ("Obey the instructions").*

> **Non-STE:**

```python
def logout(user):
    """The function will return you to the login screen."""
    session.end(user)
    redirect("/login")
```

> **STE:**

```python
def logout(user):
    """The function will go back to the login screen."""
    session.end(user)
    redirect("/login")
```

> *Adapted from spec concept: each approved word has a specified approved meaning that limits its use. In STE-Code, the approved meaning of "return" is "to send a value back from a function to its caller." Using "return" to mean "go back" is not an approved meaning. The STE version uses the approved phrase "go back."*

---

## Code-Domain Explanation

Rule 1.3 governs semantic precision in code documentation. An approved word is not a blank check — it carries exactly the meaning assigned to it in the controlled terminology. This rule prevents the most common class of documentation bugs: using the right word with the wrong meaning. A reader who sees "run" assumes "execute a program." If the writer meant "manage" or "operate," the documentation is misleading even though "run" is an approved verb. This section explains how Rule 1.3 applies to each documentation type.

### Quick Reference: Most-Misused Approved Words

The table below collects the approved words most often used with the wrong meaning across all documentation types, with their single approved meaning and the approved word to use instead when you mean something different. Use it as a first-pass audit of your own writing before applying the per-type guidance that follows.

| Approved word | Approved meaning (use it only this way) | Wrong meaning to avoid | Approved alternative |
|---------------|------------------------------------------|------------------------|----------------------|
| **run** | execute a program or command | operate, manage, continue | operate, manage, continue |
| **return** | send a value back from a function to its caller | go back to a state or location | go back |
| **call** | invoke a function, method, or subroutine | name something, shout | name, refer to as |
| **get** | fetch or retrieve data from a source | become, understand, receive passively | become, understand, receive |
| **set** | put a value into a variable or configuration | become solid, prepare | become solid, prepare |
| **make** | bring into existence by building or assembling | force, earn | cause, earn |
| **send** | transmit data to a destination | cause to go (a person) | cause to go |
| **raise** | cause an exception or error to occur | increase, lift | increase, lift |
| **catch** | handle or intercept an exception | capture a moving object, become trapped | capture, become trapped |
| **pass** | give data as an argument to a function | go past, succeed, transfer possession | go past, succeed, give |
| **check** | examine something to determine correctness or state | stop, restrain, leave in safekeeping | stop, leave |
| **break** | exit a loop or switch statement immediately | divide into parts, damage, interrupt | split, damage, interrupt |
| **continue** | skip to the next iteration of a loop | keep doing something without interruption | keep |
| **fail** | an operation did not complete successfully | not pass a test | not pass |
| **move** | transfer ownership of a value (Rust) | change physical position | go, change position |
| **borrow** | take a reference without taking ownership | take something temporarily | take temporarily |

### README Files

README files use a small set of approved verbs with precise approved meanings. The most frequent violations occur when a writer uses an approved verb in a general-English sense that differs from its controlled-terminology meaning.

**High-risk approved words in README files:**

- **run** — Approved meaning: "execute a program or command." Do not use "run" to mean "manage" (run a team), "operate" (run a machine), or "continue" (run indefinitely). Use "manage," "operate," or "continue" — all are approved verbs with different approved meanings.
- **call** — Approved meaning: "invoke a function, method, or subroutine." Do not use "call" to mean "name" (call it X) or "shout." Use "name" or "refer to as."
- **set** — Approved meaning: "put a value into a variable or configuration." Do not use "set" to mean "become solid" (the concrete sets) or "prepare" (set the table). Use "become solid" or "prepare" — "prepare" is an approved verb.
- **make** — Approved meaning: "bring into existence by building or assembling." Do not use "make" to mean "force" (make someone do something) or "earn" (make money). Use "cause" or "earn."

Example — README project description:

> **Non-STE:**

```markdown
# PipeRunner

This tool runs your CI pipeline. It runs on any platform and runs 24/7
without supervision. Run it in your terminal to start a build.
```

> **STE:**

```markdown
# PipeRunner

This tool executes your CI pipeline. It operates on any platform and
operates continuously without supervision. Execute it in your terminal
to start a build.
```

> *(P3 applied: first "runs" = execute (approved meaning, correct); second "runs" = operates (wrong approved meaning, replaced with "operates"); third "runs" = operates (wrong approved meaning, replaced))*

### API Documentation

API documentation describes functions, methods, endpoints, parameters, and return values. The approved verbs that appear in API documentation have meanings that are specific to the software domain. Using them with their general-English meanings creates ambiguity.

**High-risk approved words in API documentation:**

- **return** — Approved meaning: "send a value back from a function to its caller." Do not use "return" to mean "go back to a previous state or location." Use "go back."
- **get** — Approved meaning: "fetch or retrieve data from a source." Do not use "get" to mean "become" (get ready), "understand" (get it), or "receive passively" (get a gift). Use "become," "understand," or "receive."
- **send** — Approved meaning: "transmit data to a destination." Do not use "send" to mean "cause to go" (send someone home). Use "cause to go" or a different construction.
- **post** — Approved meaning (for HTTP APIs): "submit data to create a resource" (code-domain technical verb, Rule 1.12). Do not use "post" in prose to mean "publish" outside the HTTP context. Use "publish" or "put."
- **put** — Approved meaning: "place data at a location to store or update." Do not use "put" to mean "express in words" (put it simply). Use "say" or "write."

Example — API endpoint description:

> **Non-STE:**

```markdown
## GET /users

Returns a list of users. It gets the data from the cache first. If the
cache misses, it gets the data from the database.
```

> **STE:**

```markdown
## GET /users

Gives a list of users. It gets the data from the cache first. If the
cache does not have the data, it gets the data from the database.
```

> *(P3 applied: "returns" → "gives" — the endpoint gives data to the client, the function returns a value; "misses" → "does not have" — "miss" is not an approved verb in this context)*

### Docstrings and Inline Comments

Docstrings and inline comments explain what code does. The most common Rule 1.3 violation in docstrings is using an approved verb in a sense that belongs to a different approved meaning or to no approved meaning at all.

**High-risk approved words in docstrings:**

- **raise** — Approved meaning: "cause an exception or error to occur." Do not use "raise" to mean "increase" (raise the limit) or "lift" (raise the window). Use "increase" or "lift" — both are approved verbs.
- **catch** — Approved meaning: "handle or intercept an exception." Do not use "catch" to mean "capture a moving object" (catch a ball) or "become trapped" (catch on fire). Use "capture" or "become trapped."
- **pass** — Approved meaning: "give data as an argument to a function or method." Do not use "pass" to mean "go past" (pass the building), "succeed" (pass the test), or "transfer possession" (pass the salt). Use "go past," "succeed," or "give."
- **check** — Approved meaning: "examine something to determine correctness or state." Do not use "check" to mean "stop or restrain" (check your anger) or "leave in safekeeping" (check your bags). Use "stop" or "leave."

Example — Python docstring:

> **Non-STE:**

```python
def apply_multiplier(value, rate):
    """Raises the value by 10% and passes it through the pipeline.
    Checks the result before returning."""
    scaled = value * (1 + rate)
    processed = pipeline.run(scaled)
    assert processed is not None
    return processed
```

> **STE:**

```python
def apply_multiplier(value, rate):
    """Increases the value by 10% and sends it through the pipeline.
    Examines the result before it goes back."""
    scaled = value * (1 + rate)
    processed = pipeline.run(scaled)
    assert processed is not None
    return processed
```

> *(P3 applied: "raises" → "increases" — "raise" means "cause an exception," not "increase"; "passes" → "sends" — "pass" means "give as argument," not "send through"; "checks" → "examines" — "check" is approved but "examines" is more precise; "returning" → "goes back" — "return" means "send a value back," not "go back")*

### Commit Messages

Commit messages use a constrained vocabulary where each approved verb has exactly one approved meaning. The restricted format (type: description) leaves no room for semantic ambiguity. Every verb in a commit message must be used with its single approved meaning.

**Commit-message-specific approved meanings:**

- **add** — Approved meaning: "include new code, files, or features that did not exist before." Not "perform arithmetic addition."
- **fix** — Approved meaning: "correct a defect or unintended behavior." Not "attach firmly" or "repair physical damage."
- **remove** — Approved meaning: "delete code, files, or features so they no longer exist in the codebase." Not "move to a different location."
- **update** — Approved meaning: "change existing code or configuration to a newer version or state." Not "give someone the latest information" in a conversational sense.
- **set** — Approved meaning: "configure a value, flag, or option." Not "harden" or "solidify."

Example — commit message:

> **Non-STE:**

```bash
$ git commit -m "fix: set the timeout to stop connections from running forever"
```

> **STE:**

```bash
$ git commit -m "fix: set the timeout to stop connections that do not complete"
```

> *(P3 applied: "running" → "that do not complete" — "run" means "execute," not "continue indefinitely")*

### Error Messages

Error messages appear at runtime and must be understood quickly by users and developers under stress. Rule 1.3 violations in error messages cause confusion because the reader interprets the approved word with its approved meaning, but the writer intended a different meaning.

**High-risk approved words in error messages:**

- **fail** — Approved meaning: "an operation that did not complete successfully." Do not use "fail" to mean "not pass a test or examination." Use "not pass."
- **timeout** — Approved meaning: "a time limit was exceeded" (code-domain technical noun). Do not use "timeout" to mean "a break or pause." Use "pause" (approved noun).
- **refuse** — Approved meaning: "decline to accept or process." Do not use "refuse" to mean "garbage" (the noun sense). Use "waste" or "garbage."
- **deny** — Approved meaning: "reject a request for access." Do not use "deny" to mean "declare something to be untrue." Use "say something is not true."

Example — error message:

> **Non-STE:**

```python
raise ConnectionError(
    "Connection failed: the server refused to negotiate the handshake. "
    "The operation timed out after 30s."
)
```

> **STE:**

```python
raise ConnectionError(
    "Connection did not complete: the server refused the handshake. "
    "The operation stopped after 30 seconds."
)
```

> *(P3 applied: "failed" → "did not complete" — "fail" means "did not complete successfully"; "negotiate" → removed — "negotiate" is not approved in this sense; "timed out" → "stopped after 30 seconds" — "timeout" is a noun, and the approved meaning is "time limit exceeded," but restructured to avoid the noun-as-verb issue)*

### Tests and Test Documentation

Test code and its documentation describe expected and observed behavior. The approved verbs in tests carry meanings that are specific to the testing domain, and general-English drift is common. "Pass" and "fail" are the two highest-risk words.

**High-risk approved words in test documentation:**

- **pass** — Approved meaning: "a procedure to check correctness was successful" (noun sense of the test outcome) or, as a verb, "give data as an argument to a function" (Rule 1.3, docstrings table). In test reporting, "the test passes" uses "pass" to mean "the test reaches its expected result." Do not use "pass" to mean "go past" (pass the building) or "succeed at a non-test task." When you mean "succeed," use "succeed."
- **fail** — Approved meaning: "an operation did not complete successfully" (or, in test reporting, "the test did not reach its expected result"). Do not use "fail" to mean "not pass an examination." Use "not pass."
- **assert** — Approved meaning: "state that a condition is true, or cause an error when it is not" (code-domain technical verb, Rule 1.12). Do not use "assert" in prose to mean "claim" or "insist" (assert your opinion). Use "state" or "claim."
- **mock** — Approved meaning: "replace a real component with a test double that records or simulates its behavior" (code-domain technical verb). Do not use "mock" in prose to mean "ridicule." Use "make fun of."

Example — pytest documentation:

> **Non-STE:**

```python
def test_retry_policy():
    """Verifies the client retries three times before it gives up.
    The test fails if the backoff does not pass the threshold."""
    result = client.with_retries(3).call()
    assert result.attempts == 3
```

> **STE:**

```python
def test_retry_policy():
    """Checks that the client retries three times before it stops.
    The test does not complete if the backoff does not reach the threshold."""
    result = client.with_retries(3).call()
    assert result.attempts == 3
```

> *(P3 applied: "verifies" → "checks" — "verify" is not an approved verb, "check" is (approved meaning: examine for correctness); "gives up" → "stops" — "give up" is not an approved phrase in this sense, "stop" is approved; "fails" → "does not complete" — "fail" means "did not complete successfully"; "pass" → "reach" — "pass" as a verb means "give as argument," not "exceed a threshold")*

### Changelogs and Release Notes

Changelogs describe what changed between versions. They combine the constrained vocabulary of commit messages with the descriptive freedom of prose, which makes Rule 1.3 violations easy to miss. Each verb that names a change must carry its approved meaning.

**High-risk approved words in changelogs:**

- **add** — Approved meaning: "include new code, files, or features that did not exist before." Do not use "add" to mean "perform arithmetic addition" or "increase an amount." Use "increase."
- **remove** — Approved meaning: "delete code, files, or features so they no longer exist in the codebase." Do not use "remove" to mean "move to a different location." Use "move."
- **update** — Approved meaning: "change existing code or configuration to a newer version or state." Do not use "update" to mean "give someone the latest information" in a conversational sense. Use "tell."
- **fix** — Approved meaning: "correct a defect or unintended behavior." Do not use "fix" to mean "attach firmly." Use "attach."
- **support** — Approved meaning: "provide compatibility with or the ability to handle a feature, protocol, or input" (code-domain technical verb, Rule 1.12). Do not use "support" to mean "hold up physically" or "endorse." Use "hold" or "endorse."

Example — changelog entry:

> **Non-STE:**

```markdown
## 2.4.0

- Added support for OAuth2 and removed the legacy XML exporter.
- Fixed the connection pool that was dropping requests under load.
```

> **STE:**

```markdown
## 2.4.0

- Added compatibility with OAuth2 and removed the legacy XML exporter.
- Corrected the connection pool that was losing requests under load.
```

> *(P3 applied: "support" → "compatibility" — "support" as a noun phrasing "added support for" drifts from its approved meaning ("provide the ability to handle"); "fixed" → "corrected" — "fix" means "correct a defect," and "corrected" states the approved meaning directly; "dropping" → "losing" — "drop" as a verb means "remove permanently" in declarative contexts, not "lose intermittently," so "lose" is the precise approved alternative)*

---

## Paradigm-Specific Guidance

Rule 1.3 applies to all code documentation regardless of paradigm. But each paradigm loads approved words with paradigm-specific approved meanings. A word that is unremarkable in one paradigm may have a highly constrained approved meaning in another. This section gives guidance for each paradigm.

### Object-Oriented (Java, C++, C#, Python Classes)

Object-oriented documentation uses a set of approved words that have narrow, paradigm-specific meanings. These meanings are more restricted than the words' general-English senses and must not drift.

**Words with paradigm-specific approved meanings in OOP documentation:**

| Word | Approved Meaning (OOP) | Unapproved Meaning (do not use) |
|------|------------------------|--------------------------------|
| **class** | A blueprint for creating objects (code-domain technical noun, Rule 1.5) | A group of students, a category of service (use "category" or "type") |
| **object** | An instance of a class (code-domain technical noun) | A physical thing, a goal or purpose (use "thing" or "goal") |
| **method** | A function defined inside a class (code-domain technical noun) | A way of doing something, a procedure (use "procedure" or "technique") |
| **interface** | A contract or specification of behavior (code-domain technical noun) | A boundary between surfaces, a user interface (use "boundary" or "UI") |
| **abstract** | A class or method declared without complete implementation (code-domain technical noun/adjective) | A summary of a document (use "summary") |
| **extend** | Create a subclass from a parent class (approved verb, inheritance sense) | Make something longer or larger in physical space (use "make longer" or "increase") |
| **override** | Replace an inherited method with a new implementation (approved verb) | Use authority to reject a decision (use "reject" or "overrule") |
| **call** | Invoke a method or function (approved verb) | Name something, shout (use "name" or "shout") |

Example — class hierarchy documentation:

> **Non-STE:**

```java
// AdminUser extends User and overrides the authenticate method.
// It calls the parent method before running its own checks.
public class AdminUser extends User {
    @Override
    boolean authenticate(Credentials c) {
        boolean ok = super.authenticate(c);
        return runChecks(c) && ok;
    }
}
```

> **STE:**

```java
// AdminUser extends User and overrides the authenticate method.
// It calls the parent method before it does its own checks.
public class AdminUser extends User {
    @Override
    boolean authenticate(Credentials c) {
        boolean ok = super.authenticate(c);
        return doChecks(c) && ok;
    }
}
```

> *(P3 applied: "running" → "does" — "run" means "execute a program," not "perform checks"; the OOP-specific uses of "extends," "overrides," and "calls" all use their approved OOP meanings correctly)*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional documentation uses approved words with meanings that are often more mathematically precise than their general-English senses. The controlled terminology preserves these distinctions.

**Words with paradigm-specific approved meanings in functional documentation:**

| Word | Approved Meaning (Functional) | Unapproved Meaning (do not use) |
|------|------------------------------|--------------------------------|
| **pure** | Having no side effects (adjective, referring to functions) | Not mixed with anything, morally clean (use "clean" or "not mixed") |
| **apply** | Call a function with arguments (approved verb, code-domain sense) | Put something on a surface (use "put on") |
| **map** | Transform each element of a collection using a function (code-domain technical verb) | A geographical chart (use "chart"), to plan a route (use "plan") |
| **reduce** | Combine elements of a collection into a single value (code-domain technical verb) | Make something smaller in size (use "make smaller" or "decrease") |
| **filter** | Select elements from a collection based on a predicate (code-domain technical verb) | A device for removing impurities (use "strainer" or "purifier") |
| **fold** | Reduce a collection using an accumulator (code-domain technical verb) | Bend something over itself (use "bend") |
| **compose** | Combine two or more functions into one (code-domain technical verb) | Create a piece of music, write a letter (use "write") |
| **curry** | Transform a multi-argument function into a chain of single-argument functions (code-domain technical verb) | A spice, to prepare food with spices (use "spice") |

Example — module documentation:

> **Non-STE:**

```haskell
-- This module composes pure functions that map, filter, and reduce
-- collections without mutating state.
transform :: [Int] -> [Int]
transform = map (*2) . filter (>0) . reduce (+)
```

> **STE:**

```haskell
-- This module composes pure functions that map, filter, and reduce
-- collections without changing state.
transform :: [Int] -> [Int]
transform = map (*2) . filter (>0) . reduce (+)
```

> *(P3 applied: "mutating" → "changing" — "mutate" is a code-domain technical verb with a specific approved meaning ("change state destructively"), and here it is used in its general English sense; "changing" is the approved alternative)*

### Procedural (C, Go, Bash)

Procedural documentation uses a lean set of approved verbs, each with exactly one approved meaning. The procedural paradigm borrows little vocabulary from other domains, so Rule 1.3 violations tend to involve general-English meanings intruding on approved technical meanings.

**Words with paradigm-specific approved meanings in procedural documentation:**

| Word | Approved Meaning (Procedural) | Unapproved Meaning (do not use) |
|------|------------------------------|--------------------------------|
| **return** | Send a value back from a function to its caller | Go back to a previous location or state (use "go back") |
| **call** | Invoke a function or subroutine | Name something, shout (use "name") |
| **pass** | Give data as an argument to a function | Go past, succeed, transfer (use "go past," "succeed," "give") |
| **break** | Exit a loop or switch statement immediately | Damage something, interrupt (use "damage" or "interrupt") |
| **continue** | Skip to the next iteration of a loop | Keep doing something without interruption (use "keep") |
| **goto** | Jump to a labeled statement (code-domain technical noun) | Move toward a destination (use "go to" — two words) |
| **declare** | Specify a variable with its type (but not allocate it) | State something formally, announce (use "state" or "announce") |
| **allocate** | Reserve memory for use (code-domain technical verb) | Distribute resources among recipients (use "distribute") |

Example — C function documentation:

> **Non-STE:**

```c
/* Loops over the requests. The function allocates a buffer, passes it
   to the handler, and breaks if the handler returns an error. */
void process_requests(request_t *reqs, int n) {
    for (int i = 0; i < n; i++) {
        buffer_t *buf = allocate(1024);
        int err = handler(buf);
        if (err) break;
    }
}
```

> **STE:**

```c
/* Loops over the requests. The function allocates a buffer, gives it
   to the handler, and stops if the handler gives an error. */
void process_requests(request_t *reqs, int n) {
    for (int i = 0; i < n; i++) {
        buffer_t *buf = allocate(1024);
        int err = handler(buf);
        if (err) return;
    }
}
```

> *(P3 applied: "passes" → "gives" — "pass" means "give as argument," not "hand over"; "breaks" → "stops" — "break" means "exit a loop," not "stop executing"; "returns" → "gives" — "return" means "send a value back from a function," and "gives" is clearer in this context)*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state. The approved words in declarative contexts often double as keywords in the declarative language. When they appear in documentation prose, they must be used with their controlled-terminology meanings, not their general-English meanings or their keyword behavior.

**Words with paradigm-specific approved meanings in declarative documentation:**

| Word | Approved Meaning (Declarative) | Unapproved Meaning (do not use) |
|------|-------------------------------|--------------------------------|
| **select** | Retrieve rows from a database table | Choose from a set of options (use "choose") |
| **join** | Combine rows from two or more tables | Connect things physically, become a member (use "connect" or "become a member") |
| **create** | Make a new resource, table, or object | Invent something new, cause a situation (use "invent" or "cause") |
| **drop** | Remove a table, database, or resource permanently | Let something fall, stop doing something (use "let fall" or "stop") |
| **apply** | Execute a configuration plan (Terraform) | Put something on a surface, request a job (use "put on" or "request") |
| **describe** | Show the current state of a resource (Kubernetes) | Give a verbal account of something (use "tell about") |
| **declare** | Specify desired state in a manifest | State formally (use "state") |
| **provision** | Set up infrastructure resources (code-domain technical verb) | Supply with necessities (use "supply") |

Example — Terraform documentation:

> **Non-STE:**

```hcl
# Apply the configuration to provision the resources.
# The plan will create three instances and join them to the load balancer.
resource "aws_instance" "web" {
  count = 3
}
```

> **STE:**

```hcl
# Apply the configuration to make the resources.
# The plan will create three instances and connect them to the load balancer.
resource "aws_instance" "web" {
  count = 3
}
```

> *(P3 applied: "provision" → "make" — "provision" as a general verb is not approved; "join" → "connect" — "join" as a SQL keyword means "combine rows," and in prose it should use "connect" for the general sense)*

### Systems (Rust Ownership, C Memory Management)

Systems documentation uses approved words that have been given highly specific meanings in the context of ownership, borrowing, lifetimes, and memory. These meanings often diverge significantly from general English.

**Words with paradigm-specific approved meanings in systems documentation:**

| Word | Approved Meaning (Systems) | Unapproved Meaning (do not use) |
|------|---------------------------|--------------------------------|
| **move** | Transfer ownership of a value (Rust) | Change physical position (use "go," "travel," or "change position") |
| **borrow** | Take a reference to a value without taking ownership | Take something temporarily with intent to return (use "take temporarily") |
| **own** | Hold ownership of a value (Rust) | Possess something, admit to something (use "have" or "admit") |
| **drop** | Run the destructor and deallocate memory (Rust) | Let something fall (use "let fall") |
| **copy** | Duplicate data using bitwise or `Clone` semantics | Make a duplicate of anything (use "make a copy") |
| **clone** | Explicitly create a deep copy (Rust) | Create a genetic copy of an organism (use "copy" or "duplicate") |
| **free** | Deallocate memory that was previously allocated | Release from confinement, without cost (use "release" or "no cost") |
| **dangling** | Referring to memory that has been deallocated (code-domain technical adjective) | Hanging loosely (use "hanging") |

Example — Rust ownership documentation:

> **Non-STE:**

```rust
// When you move a value, the original owner can no longer use it.
// You can borrow a reference to read the value without taking ownership.
fn process(data: String) {
    let original = data;          // move: ownership transfers here
    let r = &original;            // borrow: shared reference, no ownership
    println!("{}", r.len());
}
```

> **STE:**

```rust
// When you move a value, the first owner can no longer use it.
// You can borrow a reference to read the value without taking ownership.
fn process(data: String) {
    let first_owner = data;       // move: ownership transfers here
    let r = &first_owner;         // borrow: shared reference, no ownership
    println!("{}", r.len());
}
```

> *(P3 applied: "original" → "first" — "original" is an approved adjective meaning "existing from the beginning," but "first" is more precise; the systems-specific uses of "move," "borrow," "own," and "reference" all use their approved systems meanings correctly)*

---

## Extended Examples

Each example pair below shows a real code documentation scenario, the STE-Code compliant rewrite, which principle was applied, and an explanation of the fix.

### Example 1 — API Reference: Return Value Description

> **Non-STE:**

```python
def get_current_user(token: str) -> "User | None":
    """Returns the authenticated user object.

    If authentication fails, returns null and logs the error.
    """
    user = auth.verify(token)
    if user is None:
        logger.log("authentication failed for token")
        return None
    return user
```

> **STE:**

```python
def get_current_user(token: str) -> "User | None":
    """Gives the authenticated `User` object.

    If authentication does not complete, gives `null` and writes the
    error to the log.
    """
    user = auth.verify(token)
    if user is None:
        logger.write("authentication failed for token")
        return None
    return user
```

> **Principle applied:** P3 (use approved words only with their approved meanings: "returns" → "gives" — the function gives a value to the caller; "fails" → "does not complete" — "fail" means "did not complete successfully," used correctly but restructured for clarity); P1 (use approved words: "logs" → "writes to the log")
> **Explanation:** The verb "return" has the approved meaning "send a value back from a function to its caller." But in API documentation, the endpoint "gives" data to the client. The distinction is between intra-process return and inter-process delivery. "Logs" as a verb is not approved — use the approved verb "write" with the approved noun "log."

### Example 2 — README: Project Feature Description

> **Non-STE:**

```markdown
# Transfuse

This library runs on Node.js and runs in the browser. It runs your
transformations in parallel to maximize throughput.
```

> **STE:**

```markdown
# Transfuse

This library operates on Node.js and operates in the browser. It runs
your transformations together to increase throughput.
```

> **Principle applied:** P3 (use approved words only with their approved meanings: first two "runs" → "operates" — "run" means "execute a program," not "function on a platform"; third "runs" → "runs" — correct, it executes the transformations); P1 ("maximize" → "increase" — "maximize" is not approved)
> **Explanation:** "Run" has exactly one approved meaning in STE-Code: "execute a program or command." When the writer says "runs on Node.js," the intended meaning is "operates on" or "functions on." The third use ("runs your transformations") uses the correct approved meaning. This example shows that the same word in the same paragraph can be both correct and incorrect depending on the intended meaning.

### Example 3 — Docstring: Exception Handling

> **Non-STE:**

```python
def load_config(path: str) -> dict:
    """This method raises an error when the input is empty. Catch the
    error and return a default value to prevent the application from
    crashing."""
    if not path:
        raise ValueError("path is empty")
    try:
        data = read(path)
    except ParseError as exc:
        return DEFAULT_CONFIG
    return data
```

> **STE:**

```python
def load_config(path: str) -> dict:
    """This method raises an error when the input is empty. Catch the
    error and give a default value to prevent the application from
    stopping."""
    if not path:
        raise ValueError("path is empty")
    try:
        data = read(path)
    except ParseError as exc:
        return DEFAULT_CONFIG
    return data
```

> **Principle applied:** P3 (use approved words only with their approved meanings: "return" → "give" — "return" means "send a value back from a function," but the prose describes what to do with the caught error, not a function return; "crashing" → "stopping" — "crash" is a code-domain technical noun meaning "abnormal program termination," and "stopping" is more precise here); P1 ("prevent" → "prevent" — correct, "prevent" is approved)
> **Explanation:** "Raise" and "catch" use their approved exception-handling meanings correctly. But "return" is used to mean "provide as a substitute," which is not the approved meaning. "Give" is the approved replacement. "Crash" is a code-domain technical noun, but using it as a verb ("crashing") violates Rule 1.7. Restructure to use "stop."

### Example 4 — CLI Error Message

> **Non-STE:**

```text
$ fetcher sync --remote api.example.com
Error: Could not connect to the server. The connection timed out.
Check your network and try running the command again.
```

> **STE:**

```text
$ fetcher sync --remote api.example.com
Error: Cannot connect to the server. The connection stopped after
30 seconds. Check your network and try the command again.
```

> **Principle applied:** P3 (use approved words only with their approved meanings: "timed out" → "stopped after 30 seconds" — "timeout" is an approved noun meaning "time limit exceeded," but using it as a verb violates Rule 1.13); P1 ("could not" → "cannot" — "cannot" is the approved modal; "running" → removed — redundant next to "try")
> **Explanation:** "Time out" as a verb phrase uses the noun "timeout" in an unapproved verb construction. The rewrite uses the approved verb "stop" with the time specification. "Try running" uses "run" in its approved meaning ("execute"), but the "-ing" form as a main verb violates the anti-pattern rule. "Try the command again" is simpler and compliant.

### Example 5 — Commit Message: Refactoring

> **Non-STE:**

```bash
$ git commit -m "refactor: break the UserService into smaller classes to improve testability"
```

> **STE:**

```bash
$ git commit -m "refactor: split the UserService into smaller classes to make testing easier"
```

> **Principle applied:** P3 (use approved words only with their approved meanings: "break" → "split" — "break" means "exit a loop," not "divide into parts"); P1 ("improve testability" → "make testing easier" — "improve" is an approved verb but "testability" is not an approved noun)
> **Explanation:** "Break" has the approved meaning "exit a loop or switch statement immediately." Using "break" to mean "divide" is a violation. "Split" is an approved verb. "Testability" is not an approved noun — restructure to "make testing easier" using the approved verb "make," the approved noun "testing" (code-domain technical noun), and the approved adjective "easier."

### Example 6 — Configuration File Documentation

> **Non-STE:**

```ini
# Set this flag to "true" to enable debug mode. When enabled, the server
# will dump verbose logs to stdout. Setting this flag impacts performance
# significantly, so do not enable it in production.
[server]
debug = true
```

> **STE:**

```ini
# Set this flag to `true` to turn on debug mode. When debug mode is on,
# the server writes detailed logs to stdout. This setting decreases
# performance. Do not turn on debug mode in production.
[server]
debug = true
```

> **Principle applied:** P3 (use approved words only with their approved meanings: "enable" → "turn on" — "enable" is an approved verb meaning "make something possible," but "turn on" is the correct phrase for activating a feature; "dump" → "writes" — "dump" is a code-domain technical noun, not a verb; "impacts" → "decreases" — "impact" as a verb meaning "affect" is not approved; "significantly" → removed — unnecessary adverb); P1 ("verbose" → "detailed" — approved adjective; "setting" → "setting" — approved noun, correct)
> **Explanation:** "Enable" has the approved meaning "make something possible." But for toggling a boolean flag to `true`, "turn on" is the correct phrase. "Dump" is a code-domain technical noun ("core dump," "memory dump"), not a verb. "Impacts" as a verb meaning "affects" is not approved — "decreases" is more precise and approved. The sentence is split to keep each under 20 words (procedural limit).

### Example 7 — Test Suite: Timeout Assertion

> **Non-STE:**

```python
def test_upload_deadline():
    """The upload should break if the network hangs. The test passes
    only when the request returns before the deadline."""
    with timeout(5):
        upload(sample_file)
    assert completed
```

> **STE:**

```python
def test_upload_deadline():
    """The upload should stop if the network does not respond. The test
    reaches its result only when the request goes back before the deadline."""
    with timeout(5):
        upload(sample_file)
    assert completed
```

> **Principle applied:** P3 (use approved words only with their approved meanings: "break" → "stop" — "break" means "exit a loop," not "abort an operation"; "hangs" → "does not respond" — "hang" is a code-domain technical noun for an unresponsive process, not a verb; "passes" → "reaches its result" — "pass" as a verb means "give as argument," not "succeed"; "returns" → "goes back" — "return" means "send a value back from a function," not "complete"); P1 ("should" → "should" — approved modal, kept)
> **Explanation:** "Break" is the hardest word in this example: its only approved meaning is "exit a loop or switch statement." Aborting an upload on a stalled network is not a loop exit, so "stop" is the approved replacement. "Pass" again shows the verb/noun split — as a verb it means "give as argument," so a passing test must be described with "reaches its result" or "completes." "Return" for "complete before a deadline" is the classic intra-process return vs. completion drift; the approved phrase is "goes back" only when a value literally comes back, otherwise "completes."

### Example 8 — README: Command Invocation vs. Naming

> **Non-STE:**

```markdown
## Usage

Call the CLI `shipit` to deploy your app. We call this workflow the
"Blue-Green" workflow. The tool runs on any host and returns a status code.
```

> **STE:**

```markdown
## Usage

Call the CLI `shipit` to deploy your app. We name this workflow the
"Blue-Green" workflow. The tool operates on any host and gives a status code.
```

> **Principle applied:** P3 (use approved words only with their approved meanings: first "call" → "call" — correct, "invoke" meaning; second "call" → "name" — "call" meaning "name" is not approved; "runs" → "operates" — "run" means "execute a program," not "function on a host"; "returns" → "gives" — "return" means "send a value back from a function," not "produce a result"); P2 (part of speech: "call" as verb (invoke) vs. "call" meaning name — the second use violates Rule 1.2 as well)
> **Explanation:** This example shows the same word, "call," used twice in one paragraph with two different intended meanings. The first is the approved verb meaning "invoke." The second, "we call this workflow," means "name," which is not an approved meaning for either the verb or noun form of "call" — it fails both Rule 1.2 (part of speech drift) and Rule 1.3 (meaning drift). "Name" is the approved replacement. "Runs on any host" again drifts to "operates," and "returns a status code" drifts to "gives a status code" because a CLI does not send a value back from a function; it produces output.

---

## Edge Cases

The following scenarios show where the boundary of an approved meaning requires careful judgment in code documentation.

### Edge Case 1: Framework Name That Shares a Spelling with an Approved Word

**Scenario:** A framework or library has a name that spells the same as an approved word. For example, "Express" (the Node.js web framework) shares its spelling with the verb "express" (approved meaning: "show or state clearly"). A writer might write: "Express your API using Express."

**Guidance:** Framework names are code-domain technical nouns (Rule 1.5, category 3) and are exempt from Rule 1.3 meaning restrictions. The approved word "express" (verb, "show or state clearly") and the technical noun "Express" (proper noun, the framework) are different words that happen to share spelling. Always capitalize the framework name to distinguish it. Do not use the framework name as a verb.

> **Non-STE:**

```javascript
// Express your API using Express.
const app = express();
app.get("/health", (req, res) => res.send("ok"));
```

> **STE:**

```javascript
// Use Express to make your API.
const app = express();
app.get("/health", (req, res) => res.send("ok"));
```

> In the non-STE version, "Express" appears twice with two different meanings: first as a verb (approved meaning: "show or state"), second as a proper noun (framework name). The STE version avoids the verb use entirely.

**When the framework name is a verb:** Some frameworks have names that are verbs in general English (for example, "React," "Build," "Run"). Treat the framework name as a code-domain technical noun regardless of its general-English part of speech. "I built the project with Build" is confusing but technically compliant because "Build" (capitalized) is a technical noun. Prefer restructured sentences: "I used Build to make the project."

### Edge Case 2: Code Keyword Whose Behavior Conflicts with Its Approved Meaning

**Scenario:** A programming language keyword has behavior that does not match the approved meaning of the same word in the controlled terminology. For example, `static` in C means "a variable with a lifetime equal to the program's lifetime." But "static" is an approved adjective meaning "not moving or changing." The keyword behavior and the approved meaning overlap but are not identical.

**Guidance:** When the keyword appears in a code block (backtick-quoted), it is quoted text (Rule 1.5, category 10) and is exempt from Rule 1.3. When you document what the keyword does, use the approved meaning in your prose and let the code block carry the language-specific semantics. The reader sees the keyword in context and understands its behavior from the code, not from your adjective choice.

> **Non-STE:**

```c
/* The static variable keeps its value between function calls. It is
   static. */
static int counter = 0;
```

> **STE:**

```c
/* The `static` variable keeps its value between function calls. The
   variable does not change between calls. */
static int counter = 0;
```

> The non-STE version uses "static" twice: first as a quoted keyword (exempt), second as an adjective in prose. The prose adjective "static" carries the approved meaning "not moving." The rewrite avoids the adjective and uses a clause that describes the behavior precisely.

### Edge Case 3: Word Approved with More Than One Meaning

**Scenario:** Some approved words have more than one approved meaning in the controlled terminology. For example, "call" is approved as a verb meaning "invoke a function" and also as a noun meaning "a function invocation." Both meanings are approved. The writer must choose the meaning that matches the part of speech used.

**Guidance:** When a word has multiple approved meanings, all of them are valid under Rule 1.3. The part of speech disambiguates. "Call the function" uses the verb meaning (invoke). "The function call" uses the noun meaning (invocation). Do not use "call" to mean "name" ("we call this X") — this is not an approved meaning for either the verb or noun form.

> **Non-STE:**

```python
# Call the function getUser. We call this pattern the Repository Pattern.
def get_user(uid):
    return store.read(uid)
```

> **STE:**

```python
# Call the function getUser. We name this pattern the Repository Pattern.
def get_user(uid):
    return store.read(uid)
```

> "Call" in the first sentence uses the approved verb meaning "invoke." "Call" in the second sentence means "name," which is not an approved meaning. "Name" is the approved replacement.

**Other words with multiple approved meanings:**

| Word | Approved Meaning 1 | Approved Meaning 2 | Unapproved Meaning |
|------|-------------------|-------------------|-------------------|
| **set** | (v) put a value into a variable | (n) a collection of unique elements | (v) become solid |
| **run** | (v) execute a program | (n) a single execution | (v) manage or operate |
| **file** | (n) a named collection of data on a disk | (v) to store data in a file | (n) a tool for smoothing surfaces |
| **test** | (n) a procedure to check correctness | (v) to run tests against code | (n) an examination in school |

### Edge Case 4: Approved Word Whose Meaning Drifts Across Documentation Types

**Scenario:** The same approved word means slightly different things in different documentation types. "Return" in a docstring means "send a value from a function to its caller." "Return" in a README means "go back to a previous step." The first meaning is approved; the second is not. But the writer may not notice the shift.

**Guidance:** Use the approved meaning consistently across all documentation types. If the approved meaning does not fit the context, use a different approved word. Do not stretch an approved meaning to cover a different concept just because the word is approved and familiar.

> **Non-STE:**

```markdown
## Install

1. Run the installer.
2. If the installation fails, return to step 2 and check your
   configuration.
```

> **STE (README):**

```markdown
## Install

1. Run the installer.
2. If the installation does not complete, go back to step 2 and check
   your configuration.
```

> "Return" has the approved meaning "send a value from a function to its caller." The README context uses "return" to mean "go back," which is not approved. "Go back" is the approved phrase.

### Edge Case 5: Domain Borrowing — When a Word's Approved Meaning in One Domain Conflicts with Another

**Scenario:** "Probe" is an approved noun in aerospace STE meaning "a device for testing or measuring." In software, "probe" is a code-domain technical noun meaning "a monitoring or diagnostic tool inserted into running code" (for example, a "liveness probe" in Kubernetes, an "observability probe"). The aerospace meaning and the software meaning are related but not identical.

**Guidance:** When a word is both an approved word in the controlled terminology and a code-domain technical noun, use the more specific meaning for the context. In software documentation, the code-domain technical noun meaning takes priority. If the context is ambiguous, add a modifier: "Kubernetes liveness probe" or "measurement probe." This follows the same principle as Rule 1.8 (use standard, well-known technical nouns).

> **Non-STE:**

```yaml
# The probe checks if the container is alive.
livenessProbe:
  httpGet:
    path: /health
    port: 8080
```

> **STE:**

```yaml
# The liveness probe checks if the container is alive.
livenessProbe:
  httpGet:
    path: /health
    port: 8080
```

> "Liveness probe" is a compound code-domain technical noun. Adding the modifier "liveness" disambiguates between the general approved noun "probe" and the domain-specific technical noun.

### Edge Case 6: Homograph Drift — When a Word's Approved Meaning and a Code-Domain Technical Verb Share a Spelling

**Scenario:** A general-English word is approved with one meaning, but the same spelling is also used as a code-domain technical verb with a different, more specific meaning. For example, "serve" is an approved verb meaning "give food or attend to a customer," but in web documentation "serve" is also used as a code-domain technical verb meaning "respond to a request from a client" (a web server serves a response). A writer may use the approved general meaning when the technical meaning is intended, or vice versa, and the reader cannot tell which.

**Guidance:** When the context is a running program responding to requests, treat "serve" as the code-domain technical verb (permitted under Rule 1.12) and do not apply the general approved meaning. When the context is genuinely about attending to a user or providing a resource in a non-network sense, use the approved general meaning or restructure. The disambiguator is the subject: a `server` (code-domain technical noun) serves requests; a person serves a customer.

> **Non-STE:**

```python
# The middleware serves the cached page to the user and then returns.
def handle(req):
    page = cache.get(req.path)
    return respond(page)
```

> **STE:**

```python
# The middleware gives the cached page to the user and then goes back.
def handle(req):
    page = cache.get(req.path)
    return respond(page)
```

> "Serve" here is used in the code-domain technical sense ("respond to a request"), which is permitted under Rule 1.12. But the sentence also says "returns," which means "send a value back from a function." The middleware does not send a value back to itself — it responds to the client and the function goes back. The rewrite uses "gives" for the delivery and "goes back" for the function exit, removing the ambiguous "serve" and the misused "returns." When in doubt, prefer the explicit approved verbs "give" and "go back" over the homographic "serve" and "return."

---

## Cross-References

Rule 1.3 is the semantic constraint on the approved vocabulary. It works with the other rules in Section 1 to build a complete system of vocabulary control.

| Rule | Title | Relationship to Rule 1.3 |
|------|-------|---------------------------|
| **Rule 1.1** | Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs | Rule 1.1 tells you which words you may use. Rule 1.3 tells you what those words mean. A word that passes Rule 1.1 must then pass Rule 1.3 — it must be used with its approved meaning. |
| **Rule 1.2** | Use Approved Words Only as the Specified Part of Speech | Rule 1.2 constrains the grammatical role of an approved word. When an approved word has more than one approved meaning, the part of speech selects the meaning. "Call" as a verb means "invoke." "Call" as a noun means "an invocation." Rule 1.2 and Rule 1.3 are applied together. |
| **Rule 1.4** | Use Only the Approved Verb Forms and Adjective Forms | Rule 1.4 constrains the morphological forms of approved words. Even when a word is used with its approved meaning (Rule 1.3), only the approved inflected forms are permitted. "Run," "runs," "ran," and "running" are all approved verb forms of "run." But "runned" is not — even though the meaning is the same. |
| **Rule 1.7** | Do Not Use Technical Nouns as Verbs | When a code-domain technical noun has an approved meaning as a noun, using it as a verb violates Rule 1.7 even if the meaning is clear. For example, "docker" is a technical noun. "Dockerize the application" uses it as a verb — not permitted. |
| **Rule 1.11** | One Term Per Concept — Be Consistent | Rule 1.11 requires that you use the same approved word for the same concept throughout a document. Rule 1.3 ensures that when you use that word, you use it with the correct meaning. Together, these rules enforce consistency of both vocabulary and semantics. |
| **Rule 1.13** | Do Not Use Technical Verbs as Nouns | When a code-domain technical verb has an approved meaning as a verb, using it as a noun violates Rule 1.13. For example, "deploy" is a technical verb. "The deploy failed" uses it as a noun — not permitted. Use "deployment." |

**Dictionary reference:** See `a-dictionary.md` for the full STE-Code controlled terminology. Each entry includes the approved word, its part(s) of speech, and its approved meaning(s). When you are unsure whether a word is being used with its approved meaning, consult the dictionary entry. The dictionary also lists unapproved words with their approved alternatives, organized by meaning category.

**Categories reference:** See `a-categories.md` for the 22 code-domain technical noun categories defined under Rule 1.5. When a domain-specific meaning is needed and no approved word carries that meaning, a code-domain technical noun from the appropriate category can fill the gap.

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** Rule 1.2 — Use Approved Words Only as the Specified Part of Speech
> **See also:** Rule 1.4 — Use Only the Approved Verb Forms and Adjective Forms
> **See also:** Rule 1.7 — Do Not Use Technical Nouns as Verbs
> **See also:** Rule 1.11 — One Term Per Concept — Be Consistent
> **See also:** Rule 1.13 — Do Not Use Technical Verbs as Nouns

---

## Grammar Notes

### Semantic Narrowing: The Core Mechanism of Rule 1.3

Rule 1.3 enforces semantic narrowing — the principle that an approved word has a meaning that is more restricted and more precise than its general-English meaning. This is the linguistic mechanism that makes STE-Code unambiguous.

In general English, the verb "run" has over 20 distinct meanings (execute, manage, operate, flow, extend, compete, publish, and more). In STE-Code, "run" has exactly one approved meaning: "execute a program or command." This semantic narrowing eliminates 19+ possible interpretations. The reader cannot misunderstand because there is only one possible meaning.

For example, a function named `run_pipeline()` is unambiguous: it executes the pipeline. A sentence "the job runs" means the job executes. The reader never needs to ask "does the writer mean manage, operate, or execute?" because "run" carries only one meaning in the controlled terminology.

### Polysemy Control

Many approved words are polysemous — they have multiple related meanings. Rule 1.3 selects exactly one meaning as the approved meaning and forbids the others. This is polysemy control.

Example: The verb "set" in general English can mean "put something in a specified place," "adjust a device," "establish a rule," "become solid," "cause to start," and more. In STE-Code, "set" has the approved meaning "put a value into a variable or configuration." All other meanings are forbidden.

Polysemy control is especially important in code documentation because many verbs that describe software operations also describe physical actions. "Run a program" vs. "run a marathon." "Call a function" vs. "call your mother." "Return a value" vs. "return home." The approved meaning is always the software-domain meaning. When the writer needs the physical meaning, they must use a different approved word.

### Context-Dependent Meaning Resolution

When an approved word has more than one approved meaning (Edge Case 3 above), the correct meaning is resolved by context. The part of speech (Rule 1.2) is the primary resolver. If the word is used as a verb, select the verb meaning. If it is used as a noun, select the noun meaning.

The documentation type is the secondary resolver. In a docstring, "call" means "invoke." In an error message, "call" means "invocation." The context makes the distinction clear even though both meanings are approved.

When context cannot resolve the ambiguity, restructure the sentence. Add a modifier, use a different approved word, or split the sentence into two simpler sentences. Never rely on the reader to guess which approved meaning applies.

### Meaning and Part of Speech: The Intersection of Rule 1.2 and Rule 1.3

Rule 1.2 (part of speech) and Rule 1.3 (meaning) are applied in sequence. First, verify that the word is used with its approved part of speech (Rule 1.2). Second, verify that the approved part of speech carries the approved meaning (Rule 1.3).

A word can pass Rule 1.2 but fail Rule 1.3. For example:

> **Non-STE:** The server runs on port 8080.

"Runs" is a verb (passes Rule 1.2 — "run" is approved as a verb). But the intended meaning is "operates on a given port," not "executes." The approved meaning of the verb "run" is "execute a program or command." This sentence fails Rule 1.3.

> **STE:** The server operates on port 8080.

"Operates" is a verb (passes Rule 1.2). The approved meaning of "operate" is "to function or work in a specified way." This sentence passes Rule 1.3.

### The "Approved Meaning" as a Semantic Constraint (Not a Syntactic One)

Rule 1.3 constrains semantics, not syntax. It does not restrict sentence structure, word order, or grammatical construction. It only restricts what a word is allowed to mean. This distinction is important because writers sometimes confuse "I cannot use this word" (Rule 1.1 violation) with "I am using this word incorrectly" (Rule 1.3 violation).

A word that appears in a sentence with correct syntax, correct part of speech, and correct morphological form can still violate Rule 1.3 if the intended meaning does not match the approved meaning. This is the hardest class of violations to detect because the sentence looks correct on the surface.

### Historical Note: ASD-STE100 Precedent

In ASD-STE100 Issue 9, Rule 1.3 is one of the most actively enforced rules in aerospace technical writing. The original specification gives the example of "follow" (approved meaning: "come after, go after") vs. "obey" (approved meaning: "do that which the procedures or instructions tell you"). This distinction has safety implications in aerospace: a maintenance procedure that says "follow the steps" does not communicate the same obligation as "obey the steps."

STE-Code adapts the same severity to code documentation. A docstring that says "the function returns you to the login screen" suggests that the function navigates the user somewhere. The correct documentation is "the function gives the login screen back to the caller" (if it does) or "the function sends the user to the login screen" (if it redirects). The difference between "returns" (sends a value back) and "redirects" (sends the user somewhere else) is the difference between correct and incorrect documentation.

The original ASD-STE100 uses a dictionary (Part 2) to define approved meanings. STE-Code uses a controlled terminology (also Part 2, in `a-dictionary.md`) to do the same. Each entry specifies the approved word, its part of speech, its approved meaning, and (for unapproved words) approved alternatives. The dictionary is the single source of truth for approved meanings. When a meaning dispute arises, the dictionary resolves it.

---

<!-- a-sec1-rule1.4.md -->

# Rule 1.4 — Use Only the Approved Forms of Verbs and Adjectives

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.4](ste-code/grouped/), Rule 1.4

## Original Rule

**Rule 1.4** Use only the approved forms of verbs and adjectives.

The dictionary gives each approved verb together with its approved forms. The dictionary also gives the approved adjectives in their base form, together with their comparative and superlative forms in parentheses where applicable.

Example — Verbs:

| REMOVE (v) |           |
|-------------|-----------|
| REMOVES,    |           |
| REMOVED,    |           |
| REMOVED     |           |

This word tells you that you can use the approved verb "remove" as follows:

| Infinitive/Imperative forms | Simple present tense | Simple past tense | Past participle form (as an adjective) |
|-----------------------------|----------------------|-------------------|----------------------------------------|
| (To) Remove/Remove          | Remove(s)            | Removed           | Removed                                |

The past participle form of the verb is usually the same as the simple past tense. Thus, the dictionary gives it two times.

Example — Adjectives:

SLOW (adj) (SLOWER, SLOWEST)

This word tells you that you can use the approved adjective "slow" as follows:

Base form: Slow
Comparative form: Slower
Superlative form: Slowest

Adjectives that make their comparative and superlative forms with "more" and "most" do not have these forms in the dictionary. This is because "more" and "most" are approved words.

## STE-Code Adaptation

**Rule 1.4** Use only the approved forms of verbs and adjectives.

The controlled terminology gives each approved verb together with its approved forms. The controlled terminology also gives the approved adjectives in their base form, together with their comparative and superlative forms in parentheses where applicable.

Example — Verbs:

COMPILE (v), COMPILES, COMPILED, COMPILED

This adapts the spec verb "remove." Just as the dictionary gives the approved forms of "remove" (removes, removed, removed), the controlled terminology gives the approved forms of "compile" (compiles, compiled, compiled).

| Infinitive/Imperative forms | Simple present tense | Simple past tense | Past participle form (as an adjective) |
|-----------------------------|----------------------|-------------------|----------------------------------------|
| (To) Compile/Compile        | Compile(s)           | Compiled          | Compiled                               |

You cannot use verb forms that are not approved. For example, you cannot use "compilating" or "compilates" because these are not approved forms of "compile."

Example — Adjectives:

FAST (adj) (FASTER, FASTEST)

This adapts the spec adjective "slow." Just as the dictionary gives the comparative and superlative forms of "slow" (slower, slowest), the controlled terminology gives the forms of "fast" (faster, fastest).

Base form: Fast
Comparative form: Faster
Superlative form: Fastest

Adjectives that make their comparative and superlative forms with "more" and "most" do not have these forms in the controlled terminology. This is because "more" and "most" are approved words.

### Examples

> *Adapted from spec pair:* Non-STE: The operator is removing the panel.  |  STE: The operator removes the panel.
> *Adapted from spec pair:* Non-STE: This procedure is slower than the previous procedure.  |  STE: This procedure is slower than the previous procedure.

> **Non-STE:** The compiler is compilating the source files every time you save the document, and it compilates them even when no change occurs in the code.
>
> **STE:** The compiler compiles the source files each time you save the document, and it compiles them even when no change occurs in the code.

> *Adapted from spec concept: only approved verb forms are permitted. Just as you cannot invent verb forms for "remove" beyond removes/removed/removed in STE, you cannot use "compilating" in STE-Code. The only approved simple present form of "compile" is "compiles."*

> **Non-STE:** This algorithm is more fast than the previous one, so it completes the sort in less time and uses fewer resources from the machine.
>
> **STE:** This algorithm is faster than the previous one, so it completes the sort in less time and uses fewer resources from the machine.

> *Adapted from spec example: "slow" (adj) (SLOWER, SLOWEST). Just as "slow" has the approved comparative form "slower" and you cannot use "more slow," "fast" has the approved comparative form "faster" and you cannot use "more fast." The approved comparative and superlative forms from the controlled terminology must be used.*

---

## Code-Domain Explanation

Rule 1.4 constrains the morphological forms of every approved verb and adjective in code documentation. It applies differently to each documentation type because each type uses different verb forms by convention. This section explains those differences.

### README Files

README files use the imperative mood for procedural sections (setup instructions, getting started guides) and the simple present tense for descriptive sections (project overviews, feature summaries).

For procedural sections, the imperative mood uses the base form of the verb, which is always the first approved form in the controlled terminology entry. For example, COMPILE (v), COMPILES, COMPILED, COMPILED — the first COMPILE is the imperative form. Use "Compile the source files" not "Compiling the source files" or "Compilate the source files."

For descriptive sections, the simple present tense uses the base form or the third-person singular form depending on the subject. "The compiler compiles the source files" uses the approved form COMPILES. "The compilers compile the source files" uses the approved form COMPILE.

Do not use the "-ing" form as a main verb in procedural writing. This is an anti-pattern. The "-ing" form appears in the approved verb entry only when the controlled terminology explicitly lists it. The verb COMPILE has no "-ing" form listed, so do not use "compiling" as a main verb in a procedure.

Example — README procedural section:

> **Non-STE:** After installing the dependencies, you can start compiling the project by running the build script. The compiler will be generating the output in the dist directory while you are editing the configuration file.
>
> **STE:** After you install the dependencies, compile the project with the build script. The compiler makes the output in the dist directory while you edit the configuration file.
> *(P4 applied: "compiling" → "compile"; "will be generating" → "makes"; "are editing" → "edit")*

### API Documentation

API documentation uses the simple present tense for return value descriptions and the imperative mood for usage examples. The simple present tense in API docs conventionally uses the third-person singular form because the subject is the function or method name.

The verb "give" is the approved alternative to "return" in descriptive prose. Its approved forms are GIVE (v), GIVES, GAVE, GIVEN. For API return value descriptions, use "Gives" (third-person singular) or "Give" (base form for plural subjects or imperative mood in usage examples). Do not use "giving" or "gived."

The past participle form (GIVEN) serves as an adjective for describing state. "The given input" is correct. But do not use the past participle form where the simple present is required. "The function given a result" is not correct; use "The function gives a result."

Example — API return value description:

> **Non-STE:** This method is returning a sorted list of users. It is accepting an optional filter parameter and is throwing an error when the query is failing.
>
> **STE:** This method gives a sorted list of users. It accepts an optional filter parameter and gives an error when the query fails.
> *(P4 applied: "is returning" → "gives"; "is accepting" → "accepts"; "is throwing" → "gives"; "is failing" → "fails")*

### Docstrings and Inline Comments

Docstrings use the imperative mood (base form) for the first line and the simple present tense for additional description. The imperative mood uses the infinitive form without "to."

When a docstring describes what a function does, use the third-person singular form if the implied subject is the function. When it gives instructions, use the imperative form. Do not mix forms within the same docstring for the same type of content.

Example — Python docstring:

> **Non-STE:** Checked the input data and returning a boolean. Raises ValueError if the data is invalidating the schema, and it is logging every call to the console during the run.
>
> **STE:** Check the input data and give a boolean. Raise ValueError when the data is not correct, and log every call to the console during the run.
> *(P4 applied: "Checked" → "Check" (imperative); "returning" → "give"; "invalidating" → "not correct"; "is logging" → "log")*

### Commit Messages

Commit messages use the imperative mood exclusively in the subject line. The imperative mood uses the base form of the verb. Use "add," "fix," "remove," "update," "set," "make," "check," "run" — all base forms of approved verbs.

Do not use the past tense in commit message subject lines. "Added" is not correct for a commit subject. Do not use the "-ing" form. "Adding" is not correct. This is similar to the STE-Code procedural writing constraint: the imperative mood is the standard for instructions.

Example — commit message:

> **Non-STE:** Fixed memory leak in connection pool and adding timeout configuration to the worker process
>
> **STE:** Fix memory leak in connection pool and add timeout configuration to the worker process
> *(P4 applied: "Fixed" → "Fix"; "adding" → "add")*

### Error Messages

Error messages use descriptive language. The simple present tense and the past participle as an adjective are the most common verb forms. Use "cannot" (approved modal) with the base form. Use "is" with the past participle as an adjective to describe state.

Do not use continuous forms ("is running," "is starting") in error messages unless the controlled terminology explicitly approves the "-ing" form. Prefer simple constructions: "The server cannot start" instead of "The server is not starting."

Example — error message:

> **Non-STE:** Connection failed: the database is not running. Please verify your configuration and retrying the migration script before you reboot the service.
>
> **STE:** Connection failed: the database does not run. Check your configuration and try the migration script again before you restart the service.
> *(P4 applied: "is not running" → "does not run"; "verify" → "check"; "retrying" → "try again"; "reboot" → "restart")*

---

## Paradigm-Specific Guidance

Rule 1.4 applies to all code documentation regardless of programming paradigm. But each paradigm has its own conventions for verb forms and adjective use in documentation. This section gives guidance for each paradigm.

### Object-Oriented (Java, C++, C#, Python Classes)

Object-oriented documentation uses the simple present tense to describe class behavior and the passive voice with the past participle to describe state. The approved verb forms must match these patterns.

When you describe what a class does, use the third-person singular form of approved verbs. "The `UserService` class gets user data from the database." Do not use "The `UserService` class is getting user data."

When you describe the state of an object or the result of an operation, use the past participle as an adjective. "The compiled class file" is correct because COMPILED is an approved form. "The instantiated object" is not correct because "instantiate" is not an approved verb and "instantiated" is not an approved form. Use "the made object" or restructure.

**Approved form patterns for OOP documentation:**

| Approved Verb | Imperative (use in procedures) | 3rd Person (use in class descriptions) | Past Participle (use as adjective) | Non-Approved Form (do not use) |
|---------------|-------------------------------|----------------------------------------|-------------------------------------|-------------------------------|
| MAKE          | Make                          | Makes                                  | Made                                | Making, Maked, Maketh          |
| GET           | Get                           | Gets                                   | Got (past only, not as adjective)   | Getting, Getted                |
| SET           | Set                           | Sets                                   | Set                                 | Setting, Setted                |
| CALL          | Call                          | Calls                                  | Called                              | Calling, Called (past only)    |
| SEND          | Send                          | Sends                                  | Sent                                | Sending, Sended                |
| KEEP          | Keep                          | Keeps                                  | Kept                                | Keeping, Keeped                |
| CHECK         | Check                         | Checks                                 | Checked                             | Checking, Checkt               |
| DO            | Do                            | Does                                   | Done                                | Doing, Doed, Doned             |

Example — class documentation:

> **Non-STE:** The `CacheManager` is responsible for maintaining cached data and invalidating entries when they become stale. It's leveraging a TTL-based eviction policy and it is spawning background threads to flush the buffer.
>
> **STE:** The `CacheManager` class keeps cached data and removes old entries. It uses a TTL-based eviction policy and starts background threads to flush the buffer.
> *(P4 applied: "maintaining" → "keeps"; "invalidating" → "removes"; "is leveraging" → "uses"; "is spawning" → "starts")*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional documentation uses the simple present tense to describe pure functions and their transformations. The emphasis is on what a function does, not how it does it. Use the third-person singular form of approved verbs.

Functional programming has many technical verbs that describe transformations: "map," "filter," "reduce," "fold," "compose," "curry." These are code-domain technical verbs (permitted under Rule 1.12) and their forms follow standard English morphology. "Map" as a verb: map, maps, mapped, mapped. "Filter": filter, filters, filtered, filtered. These technical verbs do not need to be in the controlled terminology as long as they follow standard morphological patterns.

**Guidance points for functional documentation:**

- Use "give" instead of "return" when describing what a function produces. Approved forms: give, gives, gave, given.
- Use "do" instead of "perform" or "execute" for function operations. Approved forms: do, does, did, done.
- Use "change" instead of "transform" for data modifications. Approved forms: change, changes, changed, changed.
- Technical verbs like "fold," "reduce," and "compose" follow standard English morphology. Their forms are predictable and do not violate Rule 
1.4.
- The comparative form of adjectives matters for performance comparisons. Use "faster," "slower," "larger," "smaller" (all approved forms). Do not use "more performant," "more efficient" (non-approved adjectives, restructure the sentence).

Example — module documentation:

> **Non-STE:** This module provides functions for transforming lists. The `sortBy` function is ordering elements using a comparator. The `groupBy` function is grouping elements by a key function and is memoizing the result for reuse.
>
> **STE:** This module gives functions that change lists. The `sortBy` function orders elements with a comparator. The `groupBy` function groups elements by a key function and saves the result for reuse.
> *(P4 applied: "is ordering" → "orders"; "is grouping" → "groups"; P1 applied: "provides" → "gives"; "transforming" → "change"; "is memoizing" → "saves")*

### Procedural (C, Go, Bash)

Procedural documentation uses the imperative mood heavily for step-by-step instructions. Each step must start with an approved imperative verb in its base form. The "-ing" form is never used as a main verb in procedural writing.

Procedural code often deals with memory, pointers, and system resources. The technical verbs for these operations ("allocate," "free," "dereference," "cast," "link") follow standard English morphology. "Allocate" is a code-domain technical verb with forms: allocate, allocates, allocated, allocated. "Free" in the memory-management sense is a code-domain technical verb with forms: free, frees, freed, freed.

**Guidance points for procedural documentation:**

- Each step uses the base form of the verb. "Make a buffer of 256 bytes." Not "Making a buffer."
- The simple past tense describes what a previous step did. "You made the buffer. Now fill the buffer with data."
- The past participle as an adjective describes the state of a resource. "The freed memory" or "the allocated buffer" (technical verbs, forms follow standard English).
- "Deallocate" is not a standard English word (it is "de-allocate"). Use "free" instead. Forms: free, frees, freed, freed.
- "Input" as a verb is a code-domain technical verb. Its past tense follows the irregular pattern: input, inputs, input (or inputted, inputted). Prefer "input" as the past tense to match the base form.

Example — C function documentation:

> **Non-STE:** Allocating a buffer on the heap. The caller is deallocating the buffer when it's no longer needed. The function is returning a pointer to the allocated memory and is logging the address to the trace file.
>
> **STE:** Make a buffer on the heap. The caller frees the buffer when the buffer is no longer necessary. The function gives a pointer to the allocated memory and logs the address to the trace file.
> *(P4 applied: "Allocating" → "Make" (imperative); "is deallocating" → "frees"; "is returning" → "gives"; "is logging" → "logs")*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes configuration, desired state, and resource definitions. It uses the simple present tense predominantly for describing what a configuration does. Procedural sections within declarative docs (for example, "How to apply this configuration") use the imperative mood.

Declarative tools introduce many technical verbs that describe infrastructure operations: "provision," "orchestrate," "deploy," "apply." These are code-domain technical verbs. Their forms follow standard English: provision, provisions, provisioned, provisioned; orchestrate, orchestrates, orchestrated, orchestrated; deploy, deploys, deployed, deployed; apply, applies, applied, applied.

**Guidance points for declarative documentation:**

- "Provision" is a code-domain technical verb when used in infrastructure contexts. Its approved forms follow standard English. But when the context is general, prefer the approved verb "make."
- "Orchestrate" has the same guidance: a technical verb in infrastructure context, but prefer "control" or "manage" in general prose.
- "Deploy" has forms: deploy, deploys, deployed, deployed. The past participle "deployed" also serves as an adjective: "the deployed service."
- The comparative form of adjectives appears in configuration comparisons. Use "larger," "smaller," "faster" (approved). Do not use "more scalable" (not an approved adjective, restructure: "can scale to more users").
- Kubernetes status fields often use past participles as adjectives: "Running," "Failed," "Succeeded." These are quoted text when they appear as status values (category 10, Rule 1.5). Do not use them as main verbs in prose.

Example — Terraform module documentation:

> **Non-STE:** This module is provisioning an EC2 instance and configuring security groups. After applying, the instance will be running and accessible, and the load balancer is routing traffic to the new host.
>
> **STE:** This module makes an EC2 instance and sets the security groups. After you apply the configuration, the instance runs and you can connect, and the load balancer routes traffic to the new host.
> *(P4 applied: "is provisioning" → "makes"; "configuring" → "sets"; "will be running" → "runs"; "is routing" → "routes")*

### Systems (Rust Ownership, C Memory Management)

Systems documentation explains ownership, lifetimes, memory layout, and concurrency. These concepts use technical verbs that describe precise operations on memory and resources. The technical verbs "own," "borrow," "move," "drop," "copy," and "clone" are code-domain technical verbs in Rust.

These technical verbs follow standard English morphology but some are irregular. "Run" is irregular: run, runs, ran, run. "Begin" is irregular: begin, begins, began, begun. "Give" is irregular: give, gives, gave, given. When a technical verb is irregular, its forms must still follow the standard irregular pattern.

**Guidance points for systems documentation:**

- "Own" is a code-domain technical verb in Rust with forms: own, owns, owned, owned. The past participle "owned" is also an adjective: "owned data."
- "Borrow" is a code-domain technical verb with forms: borrow, borrows, borrowed, borrowed. "Borrowed" as an adjective: "borrowed reference."
- "Move" has forms: move, moves, moved, moved. The past participle "moved" as an adjective: "moved value."
- "Drop" has forms: drop, drops, dropped, dropped. The "-ing" form "dropping" is not used as a main verb in procedural writing. It may appear in technical terms: "a dropping scope."
- "Undefined behavior" is a compound code-domain technical noun. When describing what the compiler or runtime does, use simple present tense: "The program stops" not "The program is stopping."

Example — Rust documentation:

> **Non-STE:** The borrow checker is ensuring that references aren't outliving the data they refer to. When a value is moved, the original binding is becoming invalid. The compiler is preventing use-after-move errors and is emitting a warning.
>
> **STE:** The borrow checker makes sure that references do not live longer than the data they point to. When you move a value, the original binding becomes not valid. The compiler prevents use-after-move errors and gives a warning.
> *(P4 applied: "is ensuring" → "makes sure"; "aren't outliving" → "do not live longer than"; "is becoming" → "becomes"; "is preventing" → "prevents"; "is emitting" → "gives")*

---

## Extended Examples

Each example pair below shows a real code documentation scenario, the STE-Code compliant rewrite, which principle was applied, and an explanation of the fix.

### Example 1 — README: Build Instructions

> **Non-STE:** After cloning the repository, you can start building the project by executing the build script. The compiler will be transpiling TypeScript files and outputting JavaScript bundles in the dist directory while the test runner is watching for changes in the source tree.
>
> **STE:** After you clone the repository, build the project with the build script. The compiler transpiles TypeScript files and makes JavaScript bundles in the dist directory while the test runner watches for changes in the source tree.

> **Principle applied:** P4 (use only approved verb forms: "start building" → "build"; "will be transpiling" → "transpiles"; "outputting" → "makes"; "is watching" → "watches"); P1 (use approved words: "executing" → "with")
> **Explanation:** The "-ing" form "building" is not an approved form of "build" in the controlled terminology. The imperative mood uses the base form "build." "Will be transpiling" uses the future continuous, which is not an approved verb form — replace with simple present "transpiles." "Outputting" is not a standard form of "output" as a verb; restructure with the approved verb "makes." "Is watching" uses the continuous form; replace with simple present "watches." The word "transpile" is a code-domain technical verb and its forms follow standard English: transpile, transpiles, transpiled, transpiled.

### Example 2 — API Reference: Method Description

> **Non-STE:** The `authenticate` method is verifying user credentials and is returning a JWT token upon success. It is throwing an `AuthenticationError` if the credentials are invalidating the check, and it is logging the attempt to the audit table during the call.
>
> **STE:** The `authenticate` method checks user credentials and gives a JWT token when the check succeeds. It gives an `AuthenticationError` when the credentials are not correct, and it logs the attempt to the audit table during the call.

> **Principle applied:** P4 (use only approved verb forms: "is verifying" → "checks"; "is returning" → "gives"; "is throwing" → "gives"; "are invalidating" → "are not correct"; "is logging" → "logs")
> **Explanation:** The continuous form with "-ing" is not an approved main-verb form in the controlled terminology. Replace "is verifying" with the simple present "checks." Replace "is returning" with "gives" (the approved alternative to "return," which is not an approved verb for documentation). "Is throwing" should not use the continuous form; restructure with "gives" and the error type. "Invalidating" as a main verb is replaced with the approved adjective "correct" negated with "not." "Is logging" uses the continuous form; replace with simple present "logs." The technical noun `AuthenticationError` is a code-domain technical noun and remains unchanged.

### Example 3 — Docstring: Function Purpose

> **Non-STE:** /**
>  * Processed the input array and returning a new array with duplicated elements removed.
>  * The function is iterating over each element and checking if it was seen before.
>  * It is caching the result in a local map to avoid recomputation on the next call.
>  *
>  * @param {Array} items - The array to deduplicate.
>  * @returns {Array} A new array containing unique elements.
>  */
> **STE:** /**
>  * Remove duplicate elements from the input array and give a new array.
>  * The function iterates over each element and checks if the element is in the seen set.
>  * It saves the result in a local map to avoid recomputation on the next call.
>  *
>  * @param {Array} items - The array to deduplicate.
>  * @returns {Array} A new array with unique elements.
>  */

> **Principle applied:** P4 (use only approved verb forms: "Processed" → "Remove" (imperative); "returning" → "give"; "is iterating" → "iterates"; "was seen" → "is"; "is caching" → "saves"); P1 (use approved words: "duplicated" → "duplicate"; "containing" → "with")
> **Explanation:** The first line of a docstring uses the imperative mood. "Processed" is past tense — use the imperative "Remove." "Returning" uses the "-ing" form — use the base form "give" (approved alternative to "return"). "Is iterating" uses the continuous form — use simple present "iterates." "Was seen" uses passive past — use simple present "is." "Is caching" uses the continuous form; replace with simple present "saves" (the approved alternative to "cache" as a verb is acceptable, but "save" is in the controlled terminology). "Containing" is replaced with "with," which is shorter and approved.

### Example 4 — Commit Message: Feature Addition

> **Non-STE:** feat: adding user authentication middleware and updated the login endpoint, also fixing the cookie parser bug
>
> **STE:** feat: add user authentication middleware and update the login endpoint, also fix the cookie parser bug

> **Principle applied:** P4 (use only approved verb forms: "adding" → "add"; "updated" → "update"; "fixing" → "fix")
> **Explanation:** Commit message subject lines use the imperative mood (base form). "Adding" is the "-ing" form, "updated" is the past tense, and "fixing" is the "-ing" form. All three must be changed to the imperative form: "add," "update," and "fix." All three are approved verbs in the controlled terminology. Their imperative forms are identical to the base form. This example shows three violations in one commit message — mixed forms are a common error.

### Example 5 — Configuration File Comment

> **Non-STE:** # This setting determines the maximum number of threads the server
> # will be utilizing. Higher values are resulting in better throughput but
> # are also increasing memory usage, and the scheduler is dynamically
> # rebalancing the queue when the load is spiking.
> **STE:** # This setting controls the largest number of threads that the server
> # uses. Larger values give higher throughput but
> # also use more memory, and the scheduler rebalances the queue when the load is high.

> **Principle applied:** P4 (use only approved verb forms: "will be utilizing" → "uses"; "are resulting" → "give"; "are increasing" → "use"; "is dynamically rebalancing" → "rebalances"; "is spiking" → "is high"); P1 (use approved words: "determines" → "controls"; "maximum" → "largest"; "throughput" is a technical noun — permitted under Rule 1.5)
> **Explanation:** "Will be utilizing" uses the future continuous — a form not approved in the controlled terminology. Replace with simple present "uses." "Are resulting" and "are increasing" use continuous forms — replace with simple present "give" and "use." "Is dynamically rebalancing" uses the continuous form; replace with simple present "rebalances" (technical verb, follows standard morphology). "Is spiking" uses continuous; replace with the approved adjective "high" to describe load. The comment uses the adjective "larger" (approved comparative of "large") to describe the thread count. "Throughput," "scheduler," "queue," and "load" are code-domain technical nouns and remain unchanged.

### Example 6 — Error Message: Database Connection

> **Non-STE:** Connection timeout: the database server wasn't responding within the allocated timeframe. Please check your network configuration and try reconnecting the client before you shutdown the application.
>
> **STE:** Connection timeout: the database server did not respond in the given time. Check your network configuration and try to connect the client again before you stop the application.

> **Principle applied:** P4 (use only approved verb forms: "wasn't responding" → "did not respond"; "reconnecting" → "to connect again"; "shutdown" → "stop"); P1 (use approved words: "within" → "in"; "allocated timeframe" → "given time"; "check" is approved; "network" and "configuration" are technical nouns)
> **Explanation:** "Wasn't responding" uses the past continuous — an unapproved form. Replace with simple past "did not respond." "Allocated" is the past participle of the technical verb "allocate" — but "allocated timeframe" is not a clear phrase. Replace with "given time" using the approved past participle "given." "Reconnecting" is the "-ing" form used as a main verb — replace with "to connect again" using the approved infinitive construction. "Shutdown" is a noun used as a verb here; use the approved verb "stop." "Timeout," "database," "network," and "configuration" are all code-domain technical nouns and remain unchanged.

### Example 7 — Test Specification: Behavior Description

> **Non-STE:** When the user submits an invalid token, the gateway is rejecting the request and is returning a 401 status. The test is asserting that the response body contains an error code, and it is verifying that no session is being created in the store.
>
> **STE:** When the user submits an invalid token, the gateway rejects the request and gives a 401 status. The test checks that the response body contains an error code, and it checks that no session is made in the store.

> **Principle applied:** P4 (use only approved verb forms: "is rejecting" → "rejects"; "is returning" → "gives"; "is asserting" → "checks"; "is verifying" → "checks"; "is being created" → "is made")
> **Explanation:** The continuous forms "is rejecting," "is returning," "is asserting," and "is verifying" are all unapproved main-verb forms. Replace each with the simple present: "rejects," "gives," "checks," "checks." The passive continuous "is being created" uses an unapproved "-ing" form; replace with the approved past participle "made" ("the session is made"). The technical noun "gateway," "token," "status," "session," and "store" remain unchanged.

### Example 8 — Inline Comment: Loop Logic

> **Non-STE:** // Iterating through the list and accumulating the sum until the limit is reached, then outputting the result to the log file and breaking from the loop when the value exceeds the threshold.
>
> **STE:** // Iterate through the list and add the sum until you reach the limit, then write the result to the log file and stop the loop when the value is larger than the threshold.

> **Principle applied:** P4 (use only approved verb forms: "Iterating" → "Iterate" (imperative); "accumulating" → "add"; "outputting" → "write"; "breaking" → "stop"; "exceeds" → "is larger than"); P1 (use approved words: "threshold" is a technical noun — permitted; "limit" is permitted)
> **Explanation:** Inline comments that describe a procedure use the imperative mood, so the base form "Iterate" replaces the "-ing" form "Iterating." "Accumulating" is replaced with the approved verb "add." "Outputting" is replaced with "write" (the approved alternative to "output" as a verb is acceptable, but "write" is in the controlled terminology). "Breaking" is replaced with the approved verb "stop." "Exceeds" is replaced with the approved comparative construction "is larger than" to avoid the technical verb "exceed." The technical nouns "list," "sum," "limit," "log file," "loop," and "threshold" remain unchanged.

---

## Runnable Documentation Artifacts

The pairs above isolate single sentences. In real repositories, Rule 1.4 applies to whole files that mix narrative prose, code fences, and metadata. The two full artifacts below show a complete document written the wrong way and the same document rewritten to STE-Code. Each artifact is a file you can save and open as-is. Read the **STE** version as the template.

### Artifact A — `README.md` (project setup and feature summary)

**Non-STE:**

```markdown
# cachekit

cachekit is a library that is handling in-memory caching. It's leveraging
a TTL-based eviction policy and is automatically invalidating entries when
they become stale.

## Getting Started

After cloning the repo, you can start installing the dependencies and then
begin building the package by executing `npm run build`. The compiler will be
generating the bundles in the `dist/` directory while you are editing the
config file.

## Features

* The manager is responsible for maintaining cached data and is providing a
  thread-safe read path.
* We are supporting async loading, and the prefetch worker is continuously
  polling the source for changes.
* This release is more fast than the previous one and gives better throughput.
```

**STE:**

```markdown
# cachekit

cachekit is a library that handles in-memory caching. It uses a TTL-based
eviction policy and removes old entries when they become stale.

## Getting Started

Clone the repo, install the dependencies, then build the package with
`npm run build`. The compiler makes the bundles in the `dist/` directory
while you edit the config file.

## Features

* The manager keeps cached data and gives a thread-safe read path.
* cachekit supports async loading, and the prefetch worker checks the source
  for changes.
* This release is faster than the previous one and gives higher throughput.
```

> **Principle applied:** P4 (procedural sections use the imperative: "Clone," "install," "build"; "-ing" main verbs become simple present: "is handling" → "handles," "is leveraging" → "uses," "is automatically invalidating" → "removes," "will be generating" → "makes," "are editing" → "edit," "is responsible for maintaining" → "keeps," "is providing" → "gives," "are supporting" → "supports," "is continuously polling" → "checks," "is more fast" → "is faster"); P1 ("executing" → "with," "better" → "higher" — approved comparative of "high").

### Artifact B — `user_service.py` (module docstring, API doc, inline comments, and error path)

**Non-STE:**

```python
"""The UserService class is managing user records and is returning a
profile object upon lookup. It is throwing a NotFoundError when the id is
not matching any row, and it is logging every access for the audit trail.
"""

class UserService:
    def get_profile(self, user_id: str) -> Profile:
        """Was fetching the profile for the given id and returning it.
        Is raising NotFoundError if the record is not existing.
        """
        if not self.store.contains(user_id):
            # The lookup is failing, so we are bubbling up the error
            raise NotFoundError("no such user")
        record = self.store.read(user_id)
        # Is serializing the record and is writing it to the cache
        self.cache.put(user_id, record)
        return record
```

**STE:**

```python
"""The UserService class keeps user records and gives a profile object
upon lookup. It gives a NotFoundError when the id does not match any row,
and it logs every access for the audit trail.
"""

class UserService:
    def get_profile(self, user_id: str) -> Profile:
        """Get the profile for the given id and give it.
        Raise NotFoundError when the record is not in the store.
        """
        if not self.store.contains(user_id):
            # The lookup fails, so we give the error
            raise NotFoundError("no such user")
        record = self.store.read(user_id)
        # Save the record and put it in the cache
        self.cache.put(user_id, record)
        return record
```

> **Principle applied:** P4 (module docstring: "is managing" → "keeps," "is returning" → "gives," "is throwing" → "gives," "is logging" → "logs"; method docstring: "Was fetching" → "Get" (imperative), "is raising" → "Raise," "is not existing" → "is not in the store"; inline comments: "is failing" → "fails," "are bubbling up" → "give," "Is serializing … is writing" → "Save … put"); P1 ("bubbling up" → "give," "serializing" → "save"). Note that `NotFoundError`, `Profile`, `UserService`, `store`, `cache`, `record`, and `user_id` are code-domain technical nouns and remain unchanged.

---

## Edge Cases

The following scenarios show where the boundary between approved forms and technical usage requires careful judgment.

### Edge Case 1: The "-ing" Form as a Gerund or Noun

**Scenario:** The "-ing" form of a verb functions as a noun (gerund) rather than as a main verb. For example, "logging" (from "log"), "caching" (from "cache"), "routing" (from "route"), "debugging" (from "debug").

**Guidance:** When the "-ing" form is a code-domain technical noun, it is permitted under Rule 1.5 and Rule 1.6. "Logging" as a noun ("the logging module") is a code-domain technical noun. "Logging" as a main verb ("the system is logging events") is not permitted because the "-ing" form is not an approved form of the verb "log." The distinction depends on grammatical function: noun use is permitted, main-verb use is not.

> **Non-STE:** The system is logging errors to the console. The logging module is handling all output, but it is buffering the messages before it flushes them.
>
> **STE:** The system logs errors to the console. The logging module handles all output, but it saves the messages before it flushes them.
>
> In the first sentence, "is logging" uses "-ing" as a main verb — not permitted. Replace with "logs." In the second sentence, "logging" is a noun modifier — permitted. "Is handling" and "is buffering" use "-ing" forms as main verbs; replace with "handles" and "saves."

### Edge Case 2: Irregular Technical Verbs with Unusual Past Forms

**Scenario:** Some code-domain technical verbs have irregular past forms that differ from the standard pattern. For example, "input" (input/inputted), "output" (output/outputted), "broadcast" (broadcast/broadcasted), "cast" (cast/casted), "set" (set/setted), "read" (read/read).

**Guidance:** Follow the most widely accepted form in the software domain. For "input" and "output," both "input" and "inputted" appear in technical writing but "input" as the past tense is more common and follows the irregular pattern (like "set" → "set" and "cut" → "cut"). For "broadcast," "broadcast" as the past tense is standard. For "cast" (type casting), "cast" as the past tense is standard. For "set," "set" is the only correct past form — "setted" is never correct.

> **Non-STE:** The user inputted the data and the system outputted the result. The value was setted correctly and the cast was casted to the wrong type.
>
> **STE:** The user input the data and the system output the result. The value was set correctly and the cast was cast to the wrong type.

### Edge Case 3: Framework Names That Look Like Verb Forms

**Scenario:** A framework or library name uses a word that looks like an unapproved verb form. For example, "Running" (a state machine library), "Streaming" (a data processing library), "Binding" (a data binding library), "React" (a UI library whose name is a verb).

**Guidance:** Framework and library names are code-domain technical nouns (category 3, development tools) and are permitted as proper nouns under Rule 1.5. The fact that "running" is not an approved verb form does not affect the use of "Running" as a proper noun. Always write the framework name with its correct capitalization. When you describe what the framework does, use approved verb forms in the prose.

> **Non-STE:** React is rendering the component tree and updating the DOM efficiently. Streaming is processing the events in real time while the buffer is filling.
>
> **STE:** React renders the component tree and updates the DOM quickly. Streaming processes the events in real time while the buffer fills.
>
> "React" and "Streaming" as proper nouns are unchanged. "Is rendering" uses the "-ing" form — replaced with "renders" (technical verb, follows standard morphology). "Updating" uses the "-ing" form — replaced with "updates." "Is processing" uses the "-ing" form — replaced with "processes." "Is filling" uses the "-ing" form — replaced with "fills." "Efficiently" is not an approved adverb — use "quickly" (approved).

### Edge Case 4: Past Participle as Adjective vs. Passive Voice

**Scenario:** The past participle form serves two grammatical functions: as an adjective describing state ("the compiled code") and as part of the passive voice ("the code was compiled"). Both uses are permitted but the distinction matters for clarity.

**Guidance:** Use the past participle as an adjective when you describe the state of something. Use the active voice with an approved verb when you describe who or what performs an action. The passive voice with a past participle is grammatically correct but the active voice is clearer. Prefer active voice.

> **Non-STE:** The source files were compiled by the build system and the compiled output was deployed to the server, but the deployed service was failing to start.
>
> **STE:** The build system compiled the source files and deployed the compiled output to the server, but the deployed service did not start.
>
> Both sentences use approved forms ("compiled" and "deployed" are approved past participle forms). The STE version uses the active voice, which is clearer and uses fewer words. "Was failing" uses an unapproved continuous form; replace with "did not start."

### Edge Case 5: Adjectives with Irregular Comparative and Superlative Forms

**Scenario:** Some adjectives have irregular comparative and superlative forms that do not follow the "-er"/"-est" pattern or the "more"/"most" pattern. For example, "good" (better, best), "bad" (worse, worst), "far" (farther/further, farthest/furthest).

**Guidance:** These irregular adjectives are in the controlled terminology with their approved comparative and superlative forms. "Good" is not an approved adjective in the controlled terminology — it is listed as UNAPPROVED with the approved alternative "correct" or "satisfactory." When the controlled terminology gives an irregular comparative, use that form.

In the code domain, "good" and "bad" are rarely used in technical documentation. Prefer more precise adjectives: "correct," "incorrect," "fast," "slow," "large," "small." These have regular comparative forms ("faster," "slower," "larger," "smaller") and avoid the irregular-comparative problem entirely.

> **Non-STE:** This algorithm gives good results but the other algorithm gives better results. The worst case is bad, and the memory use is more large than we expected.
>
> **STE:** This algorithm gives correct results. The other algorithm gives more correct results for large inputs. The slowest case takes 10 seconds, and the memory use is larger than we expected.
>
> "Good" and "bad" are replaced with more precise, approved adjectives. "Better" (comparative of "good") is replaced with "more correct" (using the approved "more" + base form pattern). "Worst" (superlative of "bad") is replaced with "slowest" (approved superlative of "slow"). "More large" is ungrammatical; use "larger" (approved comparative of "large").

---

## Cross-References

This rule is the fourth rule in Section 1 (Words) of the STE-Code specification. It constrains the morphological forms of words that pass through the vocabulary gates of earlier rules.

| Rule | Title | Relationship to Rule 1.4 |
|------|-------|---------------------------|
| **Rule 1.1** | Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs | Establishes which words are available. Rule 1.4 then constrains which forms of those words you can use. A word must pass Rule 1.1 before Rule 1.4 applies. |
| **Rule 1.2** | Use Approved Words Only as the Specified Part of Speech | Constrains the grammatical function of approved words. Rule 1.4 constrains the morphological form. Together they define the complete shape of each approved word: its part of speech (Rule 1.2) and its inflected forms (Rule 1.4). |
| **Rule 1.3** | Use Approved Words Only with Their Approved Meanings | Constrains the semantic range of approved words. Rule 1.4 constrains the morphological range. The same base word with its approved meaning (Rule 1.3) must appear only in its approved forms (Rule 1.4). |
| **Rule 1.5** | You Can Use Words That You Can Include in a Technical Noun Category | Defines the technical noun exception. Technical nouns from the 19 categories do not need to appear in the controlled terminology, so their forms are not constrained by Rule 1.4 in the same way. But standard English morphology still applies. |
| **Rule 1.7** | Do Not Use Technical Nouns as Verbs | A technical noun that passes Rule 1.5 must not be inflected as a verb. This interacts with Rule 1.4 because adding verb inflections to a technical noun creates unapproved verb forms. |
| **Rule 1.12** | Technical Verbs Are Allowed | Defines the technical verb exception. Code-domain technical verbs are permitted even when not in the controlled terminology. Their inflected forms must follow standard English morphology, and Rule 1.4 constrains non-technical verb forms in the same sentence. |
| **Rule 1.13** | Do Not Use Technical Verbs as Nouns | A technical verb that passes Rule 1.12 must not be used as a noun. But the past participle form of a technical verb can function as an adjective ("the deployed service"). This is a form-level distinction that Rule 1.4 governs. |

**Dictionary reference:** See `a-dictionary.md` for the full STE-Code controlled terminology. Each verb entry lists its approved forms. Each adjective entry lists its base form and, where applicable, its comparative and superlative forms in parentheses. Verbs and adjectives that are not approved are listed with their approved alternatives, which include the approved forms.

**Categories reference:** See `a-categories.md` for the 19 code-domain technical noun categories defined under Rule 1.5. These categories determine which words are exempt from the controlled terminology and therefore from the full constraint of Rule 1.4.

---

## Grammar Notes

### The Four-Form Model for Verbs

Rule 1.4 establishes a four-form model for every approved verb in the controlled terminology. Each verb entry gives exactly four forms, and only these four forms are permitted:

1. **Form 1 — Infinitive/Imperative:** This is the base form. It is used for the infinitive ("to compile"), the imperative mood ("Compile the files"), and the simple present tense with plural subjects ("the compilers compile the files"). This form is always listed first in the controlled terminology.

2. **Form 2 — Simple Present Third-Person Singular:** This is the base form with the "-s" suffix for most verbs ("compiles"). It is used only when the subject is third-person singular ("the compiler compiles the files"). For verbs with irregular third-person forms (for example, "have" → "has," "do" → "does"), the controlled terminology gives the irregular form.

3. **Form 3 — Simple Past Tense:** This form is used for completed actions in the past. For regular verbs, it is the base form with the "-ed" suffix ("compiled"). For irregular verbs, the controlled terminology gives the irregular form ("give" → "gave," "run" → "ran," "set" → "set").

4. **Form 4 — Past Participle:** This form serves as an adjective and as part of the passive voice. For regular verbs, it is identical to the simple past tense ("compiled"). For irregular verbs, it may differ from the simple past ("give" → "given" vs. "gave," "run" → "run" vs. "ran"). The controlled terminology lists Form 4 explicitly even when it is identical to Form 3, because the double listing tells the writer that both the past-tense use and the adjective use are approved.

Forms that are NOT in the four-form model include: the "-ing" form (present participle/gerund), the future tense with "will," the conditional with "would," and any non-standard inflection (for example, "compilating" or "compilates"). These forms are never used in STE-Code prose.

### The Three-Form Model for Adjectives

Rule 1.4 establishes a three-form model for adjectives that form comparatives and superlatives with the "-er"/"-est" suffix:

1. **Base Form:** The simple adjective ("fast," "slow," "large," "small," "clear").

2. **Comparative Form:** The base form with "-er" ("faster," "slower," "larger," "smaller," "clearer"). Use this form to compare two items.

3. **Superlative Form:** The base form with "-est" ("fastest," "slowest," "largest," "smallest," "clearest"). Use this form to identify the extreme among three or more items.

Adjectives that form comparatives and superlatives with "more" and "most" (for example, "correct" → "more correct," "most correct") do not have comparative and superlative forms in the controlled terminology. This is because "more" and "most" are approved words, and the writer can combine them with any approved adjective. The controlled terminology only lists the comparative and superlative forms for adjectives that use the "-er"/"-est" suffix, because those forms are not predictable from "more" + base.

### The "-ing" Restriction: Rationale

The "-ing" form is the most frequent violation of Rule 1.4 in code documentation. The original ASD-STE100 specification excludes the "-ing" form from the approved verb forms because it creates ambiguity. The "-ing" form can function as:

- A main verb in the continuous aspect ("the server is running")
- A gerund (noun) ("the running of the server")
- A participial adjective ("the running server")

In STE-Code, the "-ing" form is permitted only when it is a code-domain technical noun (for example, "logging," "caching," "routing," "debugging") or when it is part of a compound technical term. It is not permitted as a main verb in any sentence.

The continuous aspect ("is running," "is compiling," "is checking") adds no information that the simple present does not carry. "The server runs" and "the server is running" describe the same state. The simple present is shorter and clearer.

### Morphological Constraints on Technical Nouns and Verbs

When a word is a code-domain technical noun (passing through Gate 2 of Rule 1.1) or a code-domain technical verb (passing through Gate 3), the morphological constraints of Rule 1.4 apply differently:

- **Technical nouns** have no verb forms, so Rule 1.4's verb-form constraints do not apply. But when a technical noun is used as part of a compound, the compound follows standard English morphology. For example, "pod" (Kubernetes) → "pods" (plural) is standard.

- **Technical verbs** follow standard English morphology. The controlled terminology does not list their forms because they are not approved words, but their forms must be predictable from standard English rules. A technical verb like "deploy" has the predictable forms: deploy, deploys, deployed, deployed. A technical verb like "run" (in the build/execute sense — distinct from the approved verb "run") has the irregular forms: run, runs, ran, run.

When a technical verb has an irregular pattern, the writer must know the pattern and apply it correctly. The controlled terminology cannot list all technical verbs with all their forms. This is a practical limitation of Rule 1.4 — the rule is strictest for approved words and looser for technical terms, relying on the writer's knowledge of standard English morphology for technical verbs.

### Cross-Linguistic Considerations

Code documentation is read by developers from many language backgrounds. The morphological constraints of Rule 1.4 reduce the number of verb forms a reader must recognize. A reader who knows the base form of "compile" can recognize "compiles" and "compiled" without needing to know that "compilating" is not a word. The four-form model limits the surface forms to exactly four per verb, which is easier for non-native readers to learn.

For adjectives, the three-form model (or the "more"/"most" pattern) limits the surface forms to at most three per adjective. The writer never invents a new form, and the reader never encounters an unexpected form.

### Historical Note: ASD-STE100 Precedent

In ASD-STE100 Issue 9, Rule 1.4 is a short rule (half a page) that simply tells the writer to consult the dictionary for approved verb and adjective forms. The aerospace specification relies on the dictionary (Part 2) to carry the full list of approved forms. The rule text itself is minimal.

STE-Code follows the same pattern: Rule 1.4 tells the writer to consult the controlled terminology. But code documentation has a larger vocabulary of technical verbs and adjectives, and the boundary between approved forms and technical forms is more complex. This deepened version of Rule 1.4 adds guidance for that boundary, drawing on the same morphological principles as the original specification but extending them to the code domain.

The original specification uses the term "dictionary" for the controlled vocabulary list. STE-Code uses "controlled terminology" for the same reason given in Rule 1.1: to avoid confusion with programming language data structures. Both serve the same function — a curated list of words with their approved forms.

---

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** Rule 1.2 — Use Approved Words Only as the Specified Part of Speech
> **See also:** Rule 1.3 — Use Approved Words Only with Their Approved Meanings
> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category
> **See also:** Rule 1.7 — Do Not Use Technical Nouns as Verbs
> **See also:** Rule 1.12 — Technical Verbs Are Allowed
> **See also:** Rule 1.13 — Do Not Use Technical Verbs as Nouns
