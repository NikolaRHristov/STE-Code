# Rule 1.2 — Use Approved Words Only as the Specified Part of Speech

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.2

## Original Rule

**Rule 1.2** Use approved words from the dictionary only as the specified part of speech.

In the dictionary, each approved word has a specified part of speech. When you use an approved word, make sure that you use it only as the specified part of speech.

Examples:

"Test" is an approved noun, but not an approved verb.

> **STE:** Test B is an alternative to test A.

> **Non-STE:** Test the system for leaks.
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

### Examples

> **Non-STE:** Query the database for user records.
> **STE:** Send a query to the database for user records.

> *Adapted from spec pair: "Test the system for leaks" → "Do the leak test of the system." Just as "test" is only an approved noun in STE and cannot be used as a verb, "query" is only an approved noun in STE-Code. The STE version uses the approved verb "send" with the approved noun "query."*

> **Non-STE:** Static the variable to prevent modification.
> **STE:** Make the variable static to prevent modification.

> *Adapted from spec example: "dim" is an approved adjective but not a verb. Just as you cannot use "dim" as a verb in STE, you cannot use "static" as a verb in STE-Code. The STE version uses the approved verb "make" with the approved adjective "static."*

---

## Code-Domain Explanation

Rule 1.2 enforces part-of-speech discipline across all code documentation types. Every approved word carries a label in the controlled terminology — verb (v), noun (n), adjective (adj), adverb (adv), preposition (prep), conjunction (conj), pronoun (pron), or article (art). You must use each word only in the grammatical role that its label permits. This section explains how the rule applies to each documentation type.

### README Files

README files mix procedural instructions (setup, build, run) with descriptive overviews. Part-of-speech violations in README files often occur when a writer converts a noun into a verb for brevity.

The most common violation pattern is noun-as-verb: using a code-domain technical noun like "Docker," "Git," or "npm" as a verb. "Docker the application" is a Rule 1.2 violation because "Docker" is a technical noun, not a verb. The correct STE-Code construction uses an approved verb with the technical noun as its object: "Use Docker to run the application."

Another frequent pattern is adjective-as-verb: using a property name like "secure," "empty," or "silent" as a verb. "Secure the endpoint" is a Rule 1.2 violation because "secure" is an approved adjective, not an approved verb. The STE-Code construction uses "make" with the adjective: "Make the endpoint secure."

> **Non-STE:** Docker the app and deploy to production. If it fails, rollback.
> **STE:** Use Docker to make a container for the application. Deploy the container to production. If the deployment fails, roll back to the previous version.
> *(P2 applied: "Docker" is a noun, not a verb → "Use Docker." P2 applied: "rollback" as a verb → "roll back" using the approved verb "roll" with the adverb "back.")*

### API Documentation

API documentation describes function signatures, parameters, return types, and error conditions. The descriptive prose around parameter names and return values is where Rule 1.2 violations concentrate.

A common violation is using a code-domain technical noun like "cache," "map," or "filter" as a verb in the prose description. The parameter documentation may say "Caches the result for subsequent calls" where "cache" is a noun used as a verb. The STE-Code version uses an approved verb: "Keeps the result in the cache for later calls."

Status-code and error-condition descriptions also trigger Rule 1.2 when writers use adjectives as verbs: "Errors if the token is missing" uses "errors" as a verb. The correct form uses the approved noun "error" with an approved verb: "Gives an error if the token is not present."

> **Non-STE:** POST /api/users — Creates a user. Caches the profile. Errors on duplicate email.
> **STE:** POST /api/users — Makes a new user record. Keeps the profile in the cache. Gives an error on a duplicate email address.
> *(P2 applied: "Creates" → "Makes"; "Caches" → "Keeps in the cache"; "Errors" → "Gives an error.")*

### Docstrings and Inline Comments

Docstrings and inline comments have limited space. This constraint tempts writers to compress sentences by converting nouns into verbs. Rule 1.2 requires that the compression does not change the part of speech.

In Python docstrings, the word "param" is a code-domain technical noun (short for "parameter"). "Param the input" is a Rule 1.2 violation. The correct form uses an approved verb: "Set the input parameter."

In inline comments, abbreviations like "init" (for "initialization") are code-domain technical nouns. "Init the connection" is a violation. The correct form uses an approved verb: "Start the connection" or "Make the connection ready."

> **Non-STE:** # init the pool, then cache the results, finally error if null
> **STE:** # Start the connection pool. Keep the results in the cache. Give an error when the value is null.
> *(P2 applied: "init" as a verb → "Start"; "cache" as a verb → "Keep in the cache"; "error" as a verb → "Give an error.")*

### Commit Messages

Commit messages follow a conventional format with a type prefix and a short description. The type prefix (feat, fix, chore, docs, test, refactor) is not governed by Rule 1.2 — these are code-domain technical nouns. The description after the colon is where Rule 1.2 applies.

The description must use approved verbs in their approved imperative form. "Cache user sessions" is a Rule 1.2 violation because "cache" is a noun. "Add cache for user sessions" uses the approved verb "add."

When a commit message describes a refactor, the word "refactor" is a code-domain technical verb (permitted under Rule 1.12). But if the change is simple, prefer an approved verb: "fix" instead of "refactor to correct."

> **Non-STE:** fix: cache the query results to speed up the dashboard
> **STE:** fix: add a cache for query results to make the dashboard faster
> *(P2 applied: "cache" as a verb → "add a cache." "Speed up" is a phrasal verb using "speed" as a verb — restructured to "make faster" using the approved adjective.)*

### Error Messages

Error messages are displayed to end users and logged for developers. Rule 1.2 ensures that error messages use nouns and verbs correctly so that non-native English speakers understand the message.

The word "fail" is an approved verb in the controlled terminology. "The connection failed" is correct. "The connection had a fail" uses "fail" as a noun, which is a Rule 1.2 violation. Use the approved noun "failure" instead, or restructure the sentence.

The word "timeout" is a code-domain technical noun. "The request timed out" uses "timed out" as a verb phrase derived from the noun. This is a Rule 1.2 violation. The STE-Code version uses an approved verb: "The request did not complete within the timeout period."

> **Non-STE:** Error: Connection timeout. The server timed out after 30s.
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

> **Non-STE:** The `UserService` singletons the connection pool and factories the query builders.
> **STE:** The `UserService` class uses a singleton pattern for the connection pool. It makes query builders with a factory method.
> *(P2 applied: "singletons" as a verb → "uses a singleton pattern"; "factories" as a verb → "makes with a factory method.")*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional programming documentation uses terms like "map," "filter," "fold," "reduce," and "compose" as code-domain technical verbs. These are permitted under Rule 1.12 and are not governed by Rule 1.2 when used in their technical sense. But when these words appear in descriptive prose with a non-technical meaning, Rule 1.2 applies.

The word "map" is a code-domain technical verb meaning "transform each element of a collection by applying a function." When used in this technical sense, Rule 1.2 does not constrain it (Rule 1.12 takes priority). But when "map" is used as a noun in the general English sense ("a map of the system"), it is an approved noun in some contexts and an unapproved noun in others — check the controlled terminology.

The word "apply" has two valid uses: (1) as an approved general English verb meaning "put something on something" and (2) as a code-domain technical verb meaning "give arguments to a function." Both uses are valid under different rules, and Rule 1.2 does not conflict because "apply" is approved as a verb in the controlled terminology.

> **Non-STE:** Map the values through the transformer, then pipe the result into the reducer.
> **STE:** Apply the `map` function to change each value. Then apply the `pipe` function to send the result into the `reduce` function.
> *(P2 applied: "pipe" as a verb → "apply the `pipe` function." "Map" remains valid as a technical verb. "Reducer" restructured to "`reduce` function" for clarity.)*

### Procedural (C, Go, Bash)

Procedural documentation uses direct imperative verbs. Rule 1.2 reinforces this by requiring that each imperative verb is an approved verb in the controlled terminology — not a noun or adjective forced into verb service.

In C documentation, the word "malloc" is a code-domain technical noun (the name of the standard library function). "Malloc a buffer" is a Rule 1.2 violation because "malloc" is a noun used as a verb. Use "Allocate a buffer with `malloc`" or, when applying Rule 1.1 strictly, "Make a buffer with `malloc`."

In Go documentation, "goroutine" is a code-domain technical noun. "Goroutine the task" is a violation. Use "Run the task in a goroutine."

In Bash documentation, commands are code-domain technical nouns (category 3, dev tools). "Grep the file" is a Rule 1.2 violation if "grep" is treated as a verb. Use "Use `grep` to find the text in the file."

> **Non-STE:** Malloc a struct, memset it to zero, then free it when done.
> **STE:** Make a struct with `malloc`. Set all bytes to zero with `memset`. Free the struct when the operation is complete.
> *(P2 applied: "Malloc" as a verb → "Make with `malloc`"; "memset" as a verb → "Set with `memset`." The function names remain code-domain technical nouns. "Free" is a code-domain technical verb and is permitted.)*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes state and configuration rather than procedures. Rule 1.2 applies to the prose that explains what a configuration does, even though the configuration itself is declarative.

SQL keywords (SELECT, INSERT, UPDATE, DELETE) are code-domain technical verbs. When they appear inside code blocks, they are quoted text and Rule 1.2 does not apply. When they appear in prose, they are technical terms and must be marked with backticks. But the prose around them must use approved parts of speech.

"SELECT from the table" is incorrect in prose because "SELECT" is a technical verb used as a general verb and it is not marked as code. The correct prose is "Use `SELECT` to get data from the table."

In Terraform documentation, resource names like "aws_instance" are code-domain technical nouns. "Terraform the infrastructure" is a Rule 1.2 violation — "Terraform" is a technical noun, not a verb. Use "Use Terraform to make the infrastructure."

> **Non-STE:** Terraform the VPC, then Kubectl the pods into the cluster.
> **STE:** Use Terraform to make the VPC. Use `kubectl` to apply the pod configuration to the cluster.
> *(P2 applied: "Terraform" as a verb → "Use Terraform"; "Kubectl" as a verb → "Use `kubectl`.")*

### Systems (Rust Ownership, C Memory Management)

Systems documentation explains ownership, lifetimes, memory layout, and concurrency. These concepts have dense technical vocabularies. Rule 1.2 requires that the framing prose around these technical terms respects part-of-speech boundaries.

In Rust documentation, "borrow," "own," and "move" are code-domain technical verbs and are permitted under Rule 1.12. "Drop" is a code-domain technical noun (the `Drop` trait). "Drop the value" is a Rule 1.2 violation if "Drop" is used as a verb without backtick marking. Use "The value runs its `Drop` implementation" or "The value is dropped" (where "dropped" is the past participle of the technical verb "drop").

"Unsafe" is an approved adjective in the controlled terminology (meaning "not safe"). In Rust, "unsafe" is also a keyword and a code-domain technical noun (an `unsafe` block). When used as a keyword, mark it with backticks. When used as a descriptive adjective, it follows Rule 1.2 as an adjective.

> **Non-STE:** The function unsafes the pointer access and drops the guard afterwards.
> **STE:** The function uses `unsafe` for the pointer access. It runs the `Drop` implementation for the guard afterwards.
> *(P2 applied: "unsafes" as a verb → "uses `unsafe`"; "drops" as a verb without marking → "runs the `Drop` implementation.")*

---

## Extended Examples

Each example pair below shows a real code documentation scenario, the STE-Code compliant rewrite, which principle was applied, and an explanation of the fix.

### Example 1 — README: Build and Run Instructions

> **Non-STE:** Clone the repo, then npm install to dependency the project. Webpack the bundle and express the server on port 3000.
> **STE:** Clone the repository. Run `npm install` to get the dependencies. Use `webpack` to make the bundle. Start the Express server on port 3000.

> **Principles applied:** P2 (use approved part of speech: "dependency" is a noun → "get the dependencies"; "Webpack" is a noun → "Use `webpack`"; "express" is a noun → "Start the Express server").
> **Explanation:** Three separate part-of-speech violations in one instruction block. "Dependency" is an approved noun in the controlled terminology — it cannot be used as a verb meaning "install dependencies." "Webpack" is a code-domain technical noun (a build tool name) — it cannot be used as a verb meaning "build with webpack." "Express" is a code-domain technical noun (a framework name) — it cannot be used as a verb meaning "serve with Express." The STE version introduces approved verbs ("run," "get," "use," "make," "start") to carry the action while keeping the technical nouns in their correct grammatical role.

### Example 2 — API Docstring: JSDoc for an Express Route Handler

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

> **Non-STE:** refactor: interface the user repository and factory the database connection
> **STE:** refactor: add an interface to the user repository and use a factory for the database connection

> **Principles applied:** P2 (use approved part of speech: "interface" is a noun → "add an interface"; "factory" is a noun → "use a factory"); P1 (use approved words: "add" and "use" are approved verbs).
> **Explanation:** "Interface" is a code-domain technical noun (an OOP contract type) — it cannot be used as a verb meaning "to add an interface to." "Factory" is a code-domain technical noun (a design pattern name) — it cannot be used as a verb meaning "to create with a factory." The STE version introduces the approved verbs "add" and "use" to carry the actions. The trade-off is a longer commit message, but the meaning is unambiguous to all readers regardless of native language.

### Example 4 — Error Message: Database Connection Failure

> **Non-STE:** FATAL: Could not database the connection. The pool is empty. Retry the operation or contact your admin.
> **STE:** FATAL: Could not connect to the database. The connection pool has no available connections. Try the operation again or speak to your administrator.

> **Principles applied:** P2 (use approved part of speech: "database" is a noun → "connect to the database"; "empty" used without a verb → "has no available connections"); P1 (use approved words: "retry" → "try again"; "contact" → "speak to"; "admin" → "administrator").
> **Explanation:** "Database" is a code-domain technical noun (category 9, data stores) — it cannot be used as a verb meaning "to connect to a database." The STE version uses the approved verb "connect" with the technical noun "database." "Empty" is an approved adjective — the sentence "The pool is empty" is grammatically correct but ambiguous (does "empty" mean zero connections, or zero available connections?). The STE version makes the state explicit: "has no available connections."

### Example 5 — Python Docstring: Class Constructor

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

---

## Edge Cases

The following scenarios show where the boundary between approved parts of speech and code-domain usage requires careful judgment.

### Edge Case 1: Word Approved as Both Noun and Verb — Ambiguity in Context

**Scenario:** A word like "commit" is approved as both a noun and a verb in the controlled terminology. The sentence "Make a commit" uses "commit" as a noun (correct). The sentence "Commit the changes" uses "commit" as a verb (also correct). But the sentence "The commit committed the commit" uses the word three times with ambiguous roles and is difficult to parse.

**Guidance:** When a word is approved as more than one part of speech, the context must make the role clear. If the same word appears multiple times in one sentence with different roles, restructure the sentence to use different approved words. For "commit," use "commit" as the verb and "change set" as the noun when both roles must appear in the same sentence.

> **Non-STE:** The commit committed the files to the commit history.
> **STE:** The `git commit` command added the files to the change history.
> *(P11 applied: one term per concept — use "change history" instead of "commit history" to avoid the double "commit.")*

### Edge Case 2: Framework CLI Command Used as a Verb

**Scenario:** Many frameworks provide CLI commands that developers use as verbs in documentation. For example, "Docker compose up," "npm install," "kubectl apply." The CLI command itself contains a verb ("up," "install," "apply"), but the tool name ("Docker," "npm," "kubectl") is used as if it were a verb.

**Guidance:** The tool name is a code-domain technical noun. When writing prose documentation, always introduce an approved verb before the tool name: "Use Docker to start the containers" instead of "Docker the containers." When quoting a CLI command literally inside a code block, the command is quoted text (Rule 1.5, category 10) and Rule 1.2 does not apply. The distinction is between prose (must follow Rule 1.2) and code blocks (exempt).

> **Non-STE:** Kubectl the deployment into the cluster.
> **STE:** Use `kubectl apply` to send the deployment to the cluster.
> *(P2 applied: "Kubectl" as a verb → "Use `kubectl apply`." The CLI command `kubectl apply` is a compound technical noun.)*

### Edge Case 3: Adjective Used as a Verb in a Standard Industry Phrase

**Scenario:** Some adjective-as-verb constructions are so common in the software industry that they function as de facto technical verbs. For example, "to green the build" (make the CI pipeline pass), "to yellow the test" (mark a test as flaky), "to red the deployment" (to cause a deployment failure).

**Guidance:** These are jargon (violation of Rule 1.10) and part-of-speech violations (Rule 1.2). They are not permitted in STE-Code regardless of how common they are. Use approved constructions: "Make the build pass," "Mark the test as flaky," "Cause the deployment to fail." Color-based status terminology is especially problematic for accessibility and translation — avoid it entirely.

> **Non-STE:** We need to green the CI before we can ship.
> **STE:** We must make the CI pipeline pass before we can deploy.
> *(P2 applied: "green" as a verb → "make pass"; P10 applied: "ship" is slang → "deploy.")*

### Edge Case 4: Language-Keyword Noun Used as a Verb in Prose

**Scenario:** A programming language keyword like `import`, `export`, `return`, or `yield` is a code-domain technical noun when marked with backticks. But writers often use these keywords as verbs in prose without backticks: "Import the module," "Export the function," "Return the value."

**Guidance:** When used as a verb in prose without backticks, the word must be an approved verb in the controlled terminology. "Return" is approved as a verb (meaning "send a value back from a function") — "Return the value" is correct. "Import" is not an approved verb in the controlled terminology — "Import the module" is a Rule 1.2 violation. Use "Add the module with `import`" or "Use `import` to add the module." "Export" is not an approved verb — use "Make the function available with `export`."

> **Non-STE:** Import the helper, export the main function, and return the result.
> **STE:** Use `import` to add the helper. Use `export` to make the main function available. Return the result.
> *(P2 applied: "Import" as a verb without backticks → "Use `import`"; "Export" as a verb without backticks → "Use `export`." "Return" is an approved verb and remains unchanged.)*

### Edge Case 5: Past Participle of a Noun-Derived Technical Verb

**Scenario:** Some code-domain technical verbs are derived from nouns and have irregular past participles. For example, "input" (technical verb) → "input" or "inputted" (past participle). "Output" → "output" or "outputted." "Broadcast" → "broadcast" or "broadcasted."

**Guidance:** Rule 1.2 applies to the base form of the word. When a code-domain technical verb is permitted under Rule 1.12, its inflected forms (past, past participle, present participle) follow the conventions of the programming language or domain, not the approved verb forms of Rule 1.4. But when the verb is an approved word in the controlled terminology, Rule 1.4 applies and only the approved inflected forms are permitted.

For "input" and "output" — these are code-domain technical verbs. Their past participles follow domain convention. For approved verbs like "run" (ran, running) or "set" (set, setting), only the forms listed in the controlled terminology are permitted.

> **Non-STE:** The user inputted the data and the system outputted the report.
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
