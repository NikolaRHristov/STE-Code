# Rule 2.1 — Multi-word Nouns (Maximum Three Words)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 2.1

## Original Rule

Write multi-word nouns of no more than three words.

In English, you can use one or more words to describe or modify a noun. Technical texts can contain long groups of words that have the function of one part of speech in a sentence. Usually, these groups of words are made of nouns and/or adjectives and are the subject or the object in a sentence. Such groups of words are known as multi-word nouns.

General examples:

- Horizontal cylinder pivot bearing (a multi-word noun of 4 words)
- Stainless steel corrosion protection strips (a multi-word noun of 5 words)
- Actuator operating rod (a multi-word noun of 3 words)

Long multi-word nouns are not easy to understand because the words in the multi-word noun can connect to each other differently. The main noun, or head noun of the group, is usually the last word of the multi-word noun. When the connections between words are not clear, ambiguity occurs. As a result, short multi-word nouns are easier to understand.

- Runway light connection
  *(This example shows a short multi-word noun (3 words). The main noun is "connection.")*

- Runway light connection resistance calibration
  *(This example shows a long multi-word noun (5 words). The main noun is "calibration.")*

The long multi-word noun in the example does not tell the reader the relation between "runway" and "calibration." The reader must understand four modifiers before the main noun "calibration."

Long multi-word nouns can cause problems for non-native English readers because, in some languages, the main noun comes first in the multi-word noun. When a multi-word noun has more words, it is less clear.

To help your reader, keep multi-word nouns to a maximum of three words.

To keep multi-word nouns short, you can use prepositions (for example, "of," "on," "in," and "for") and explain the multi-word nouns.

Examples:

> **Non-STE:** Runway light connection resistance calibration. (5 words)
>
> **STE:** Calibration of the resistance of the runway light connection.
> *(1 word, 1 word, and 3 words)*

## STE-Code Adaptation

In code documentation, multi-word nouns frequently appear when describing system components, data structures, or configurations. Long chains of nouns and adjectives make documentation hard to parse, especially for non-native English readers.

General examples:

- API gateway request rate limiter (a multi-word noun of 4 words)
- GraphQL query response cache eviction strategy (a multi-word noun of 5 words)
- Database connection pool (a multi-word noun of 3 words)

Keep multi-word nouns to a maximum of three words. When a concept requires more than three words, break the multi-word noun into smaller units connected by prepositions such as "of," "for," "in," and "on." The main noun (head noun) should be the last word of each multi-word noun unit.

- Database connection pool
  *(This example shows a short multi-word noun (3 words). The main noun is "pool.")*

- Database connection pool timeout configuration
  *(This example shows a long multi-word noun (5 words). The main noun is "configuration.")*

The long multi-word noun does not tell the reader the relation between "database" and "configuration." The reader must understand four modifiers before the main noun "configuration."

This rule applies to documentation prose, not to code identifiers (variable names, function names, class names). Code identifiers follow the naming conventions of the programming language and are not multi-word nouns in the STE sense.

### Examples

> **Non-STE:** Database connection pool timeout configuration. (5 words)
>
> **STE:** Configuration of the timeout of the database connection pool.
> *(1 word, 1 word, and 3 words)*

> *Adapted from spec pair: "Runway light connection resistance calibration" / "Calibration of the resistance of the runway light connection."* Both break a long multi-word noun into smaller units connected by prepositions. The spec multi-word noun "runway light connection resistance calibration" (5 words) becomes three separate multi-word noun units. The code-domain multi-word noun "database connection pool timeout configuration" (5 words) follows the same pattern: "Configuration of the timeout of the database connection pool."

---

## Code-Domain Explanation

This rule applies to all forms of code documentation. The specific application varies by document type.

### README Files

README files introduce a project to new users. Long multi-word nouns in the opening paragraphs create a barrier to understanding. Keep the project description accessible by using short multi-word nouns.

> **Non-STE (README introduction):** The project implements a distributed event sourcing aggregate root snapshot storage strategy.
> **STE (README introduction):** The project implements a strategy for storage of snapshots of the aggregate roots in a distributed event sourcing system.

> **Principle applied:** P1, P5 — "event sourcing," "aggregate root," and "distributed" are approved technical nouns. The multi-word noun is restructured from 7 words into a chain of short units (1 word, 1 word, 1 word, and 3 words).

### API Documentation

API reference documentation describes parameters, return types, and behavior. Long multi-word nouns in parameter descriptions cause confusion about which noun modifies which.

> **Non-STE (API parameter):** `timeout` — The database connection pool acquisition timeout duration in milliseconds.
> **STE (API parameter):** `timeout` — The duration of the timeout for acquisition of the database connection pool, in milliseconds.

> **Principle applied:** P11 — the consistent use of "acquisition" instead of its synonyms ("fetch," "retrieval") keeps the documentation predictable.

### Docstrings and Inline Comments

Docstrings are read by developers who need fast understanding. Short multi-word nouns help them scan the documentation quickly.

> **Non-STE (Python docstring):** Handles the Redis cache key expiration event notification dispatch.
> **STE (Python docstring):** Handles dispatch of the notification of the event of expiration of the Redis cache key.

> **Principle applied:** P4 — "handles" and "dispatch" are approved verb and noun forms. The long multi-word noun is broken with "of" prepositions.

### Commit Messages

Commit messages must be scannable in a git log. Multi-word nouns longer than three words make the subject line too dense.

> **Non-STE (commit subject):** fix: user authentication token refresh race condition handling
> **STE (commit subject):** fix: handling of the race condition in the refresh of the user authentication token

> **Principle applied:** P9 — the shorter, clearer structure uses "of" and "in" to show the relations between the nouns.

### Error Messages

Error messages appear in logs and terminal output. The reader must understand the error immediately. Long multi-word nouns delay comprehension.

> **Non-STE (error message):** ERROR: Payment gateway transaction rollback failure recovery attempt limit exceeded.
> **STE (error message):** ERROR: The limit of attempts for recovery from failure of the rollback of a transaction in the payment gateway is exceeded.

> **Principle applied:** P2, P3 — "recovery" is used only as a noun. "Failure" is used only with its approved meaning.

### Configuration Files and Environment Variables

Configuration documentation must be unambiguous. When a multi-word noun names a setting, the description must show the exact relation between the parts.

> **Non-STE (env var description):** `CACHE_TTL` — Redis cluster node connection pool maximum idle time seconds.
> **STE (env var description):** `CACHE_TTL` — The maximum idle time, in seconds, for the connection pool of the node of the Redis cluster.

> **Principle applied:** P1 — "maximum" and "idle" are approved words from the STE-Code dictionary. The unit ("seconds") is placed after the value it modifies.

---

## Paradigm-Specific Guidance

Different programming paradigms produce different types of multi-word nouns. The strategy for breaking them is the same, but the patterns vary.

### Object-Oriented Programming (Java, C++, C#, Python Classes)

OOP documentation frequently chains class names, design pattern names, and architectural layer names. These chains often exceed three words.

> **Non-STE:** The AbstractFactoryMethodPatternImplementationRegistryBuilder constructs the registry.
>
> **STE:** The builder for the registry of the implementation of the abstract factory method pattern constructs the registry.

Design pattern names such as "abstract factory method pattern" are official technical nouns. Write them in full the first time. After explanation, use a shorter form (see Rule 2.2).

> **Non-STE:** Inject the UserRepositoryInterfaceDependencyInjectionContainerBinding.
>
> **STE:** Inject the binding of the container for dependency injection of the interface of the user repository.

"UserRepositoryInterface" and "DependencyInjectionContainer" are class names in code. In documentation prose, break them into their semantic parts with prepositions.

### Functional Programming (Haskell, Elixir, Clojure, Rust)

Functional documentation describes monadic chains, transformer stacks, and pure function compositions. These create deeply nested noun modifiers.

> **Non-STE:** The monadic error handling pipeline transformer composition chain evaluates the input.
>
> **STE:** The chain of composition of the transformer of the pipeline for monadic error handling evaluates the input.

> **Principle applied:** P7 — "chain" is used as a noun, not as a verb ("to chain"). The technical nouns "monadic," "pipeline," "transformer," and "composition" are preserved.

> **Non-STE:** Apply the higher order function currying partial application optimization.
>
> **STE:** Apply the optimization of the partial application of the currying of the higher-order function.

### Procedural Programming (C, Go, Bash)

Procedural code documents sequences of operations, memory management, and system calls. Multi-word nouns describe buffers, handlers, and procedures.

> **Non-STE:** The file descriptor read buffer allocation failure handler signals the caller.
>
> **STE:** The handler for failure of allocation of the read buffer of the file descriptor signals the caller.

> **Principle applied:** P12 — "handler," "buffer," and "allocation" are approved technical verbs used as nouns here (which is correct — Rule 1.13 applies when technical verbs are used as nouns incorrectly).

> **Non-STE:** Execute the memory arena deallocation safety check routine.
>
> **STE:** Execute the routine for the safety check of the deallocation of the memory arena.

### Declarative Programming (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes resource specifications, policy definitions, and query structures.

> **Non-STE:** The Kubernetes pod resource limit specification defines the maximum memory.
>
> **STE:** The specification of the resource limit of the Kubernetes pod defines the maximum memory.

> **Principle applied:** P5 — "Kubernetes" and "pod" are technical code nouns. "Resource limit" is a three-word multi-word noun that stays within the limit.

> **Non-STE:** The Terraform module output variable dependency graph resolution algorithm runs before apply.
>
> **STE:** The algorithm for resolution of the graph of dependency of the output variable of the Terraform module runs before the apply step.

### Systems Programming (Rust Ownership, C Memory)

Systems documentation describes ownership models, lifetime annotations, and memory layouts. These concepts naturally stack many modifiers.

> **Non-STE:** The heap allocated reference counted thread safe pointer dereference operation returns the value.
>
> **STE:** The operation of dereference of the pointer that is heap-allocated, reference-counted, and thread-safe returns the value.

> **Principle applied:** P1, P4 — hyphens in "heap-allocated," "reference-counted," and "thread-safe" create adjective compounds. Each hyphenated compound counts as one word.

> **Non-STE:** The stack frame return address overflow protection mechanism prevents attacks.
>
> **STE:** The mechanism for protection against overflow of the return address of the stack frame prevents attacks.

---

## Extended Examples

Each pair shows a real code-documentation scenario, the STE-Code fix, and the principle applied.

### Example 1 — Configuration Documentation

> **Non-STE:** Set the load balancer health check interval threshold multiplier to 2.
>
> **STE:** Set the multiplier of the threshold of the interval of the health check of the load balancer to 2.

**Principle applied:** P1, P11 — "health check" and "load balancer" are canonical terms. The preposition "of" shows the ownership chain: multiplier → threshold → interval → health check → load balancer.

**Explanation:** The non-STE version chains 6 nouns before the reader reaches the head noun "multiplier." The STE version restructures with prepositions so each unit is at most 3 words.

### Example 2 — Commit Message

> **Non-STE:** feat: add GraphQL query response cache eviction strategy configuration
>
> **STE:** feat: add configuration of the strategy for eviction of the cache of the GraphQL query response

**Principle applied:** P9, P5 — "GraphQL" is a technical code noun. The shorter, clearer form uses prepositions to show the relations.

**Explanation:** The non-STE version (6 words) forces the reader to parse five modifiers before reaching "configuration." The STE version breaks this into: "configuration" (1), "strategy for eviction" (2), "cache of the GraphQL query response" (4, which becomes "cache of the response" after Rule 2.2 shortening on second use).

### Example 3 — Error Message

> **Non-STE:** ERROR: Authentication token validation failure recovery procedure initialization failed.
>
> **STE:** ERROR: Initialization of the procedure for recovery from failure of the validation of the authentication token failed.

**Principle applied:** P2, P3 — "recovery" (noun, approved), "validation" (noun, approved), "authentication" (noun, approved). No word is used as an incorrect part of speech.

**Explanation:** The non-STE version has 7 words in one multi-word noun. The reader cannot quickly identify which word is the subject of "failed." The STE version establishes "initialization" as the subject immediately.

### Example 4 — API Documentation (Return Value)

> **Non-STE:** Returns the user profile image upload progress percentage completion status.
>
> **STE:** Returns the status of completion of the percentage of progress of the upload of the user profile image.

**Principle applied:** P1 — "completion," "percentage," "progress," "upload," "image," and "status" are all approved nouns from the STE-Code dictionary.

**Explanation:** The non-STE version (6 words) makes the reader work backward from "status" to understand what kind of status. The STE version places the head noun "status" first.

### Example 5 — README Architecture Section

> **Non-STE:** The system uses a microservice inter-service communication message broker routing table.
>
> **STE:** The system uses a table for routing of messages in the broker for communication between the microservices.

**Principle applied:** P8, P9 — "microservice," "broker," and "routing" are standard, well-known technical nouns. The shorter, clearer prepositions replace the noun chain.

**Explanation:** The non-STE version (6 words) has ambiguous attachment: does "routing" modify "table" or "broker"? The STE version makes it explicit: routing → messages → broker → communication → microservices.

### Example 6 — Inline Code Comment

> **Non-STE:** // Trigger the CI/CD pipeline artifact retention policy enforcement job.
>
> **STE:** // Trigger the job for enforcement of the policy for retention of the artifacts of the CI/CD pipeline.

**Principle applied:** P1, P7 — "enforcement" is a noun (not used as a verb). "CI/CD" is a technical code noun.

**Explanation:** The non-STE version asks the reader to parse "CI/CD pipeline artifact retention policy enforcement job" as one 7-word unit. The STE version lets the reader process "trigger the job" immediately, then understand what the job does.

---

## Edge Cases

### Edge Case 1 — Framework Names That Contain "Unapproved" Words

Some framework names contain words that are not approved in STE-Code. The framework name is a technical code noun and is allowed under Rule 1.5 and Rule 1.6.

> **Non-STE framework name:** Express.js middleware stack configuration
> **STE:** Configuration of the stack of middleware for Express.js

"Express" is not an approved STE word (its approved meaning is "to move quickly," not a web framework). However, "Express.js" as a framework name is a technical code noun and is allowed. The multi-word noun rule still applies: break "Express.js middleware stack configuration" (4 words) into smaller units.

> **Non-STE framework name:** Spring Boot auto-configuration bean post-processor registry
> **STE:** Registry of the post-processor of the bean for auto-configuration in Spring Boot

"Spring" and "Boot" are not approved STE words individually, but "Spring Boot" is a framework name (technical code noun, Rule 1.5). "Bean" is a technical code noun in the Spring context. Apply the multi-word noun rule to the surrounding documentation prose.

### Edge Case 2 — Code Keywords That Conflict With the Rule

Some code keywords (reserved words in programming languages) appear in documentation prose. These keywords are technical code nouns and are not subject to the multi-word noun limit when used as code identifiers. However, the surrounding prose must still follow the rule.

> **Non-STE:** The `finally` block cleanup resource deallocation handler runs after the try-catch.
>
> **STE:** The handler for deallocation of the resource of the cleanup of the `finally` block runs after the try-catch statement.

The keyword `finally` is a reserved word in Java, Python, and JavaScript. It appears in backticks to indicate code. The multi-word noun rule applies to the prose around it, not to the keyword itself.

> **Non-STE:** The `yield` keyword generator state preservation mechanism differs in Python and JavaScript.
>
> **STE:** The mechanism for preservation of the state of the generator of the `yield` keyword is different in Python and in JavaScript.

### Edge Case 3 — Relaxation for Auto-Generated Documentation

Auto-generated documentation (JSDoc output, Sphinx autodoc, Swagger/OpenAPI generated docs) may contain multi-word nouns derived from code identifiers. These are acceptable in generated output because they reflect the source code directly. However, any manually written descriptions within the docstrings that feed the generator must follow the rule.

> **Acceptable in generated docs:** `getUserProfileImageUploadProgressPercentageCompletionStatus()`
> *(This is a function name from source code, generated verbatim. Not subject to the rule.)*

> **Must be corrected in the source docstring:**
> **Non-STE (docstring):** Gets the user profile image upload progress percentage completion status.
> **STE (docstring):** Gets the status of completion of the percentage of progress of the upload of the user profile image.

### Edge Case 4 — Compound Terms With Slashes

Technical terms that include slashes (read/write, input/output, create/read/update/delete) count as one word for the purpose of this rule. The slash binds the words into a single semantic unit.

> **Non-STE:** The read/write lock timeout configuration parameter controls contention.
>
> **STE:** The parameter for configuration of the timeout of the read/write lock controls contention.

"read/write" counts as one word. "Read/write lock" is a 2-word multi-word noun. "Read/write lock timeout configuration parameter" is 4 words and must be broken.

### Edge Case 5 — When Breaking Creates More Words but Improves Clarity

The goal of this rule is clarity, not minimal word count. A broken multi-word noun with prepositions will always have more total words than the original noun chain. This is acceptable because clarity is the primary goal.

> **Non-STE (8 total words):** The API gateway request rate limiter configuration is complex.
> **STE (14 total words):** The configuration of the limiter of the rate of the requests to the API gateway is complex.

The STE version uses more total words (14 vs. 8) but each multi-word noun unit is at most 3 words. The reader can process each unit independently.

---

## Cross-References

- **Rule 1.5 — Technical Code Nouns:** Defines which code-domain terms (keywords, frameworks, tools) are allowed as technical nouns. These nouns are the building blocks that form multi-word nouns.
- **Rule 1.6 — Non-Approved Words as Technical Code Nouns:** Explains when non-approved words are allowed because they are technical code nouns. This rule interacts with 2.1 when a multi-word noun contains both approved and technical nouns.
- **Rule 1.7 — Do Not Use Technical Nouns as Verbs:** Multi-word nouns often contain technical nouns. Ensure these nouns are not used as verbs in the surrounding sentence.
- **Rule 1.8 — Use Approved Technical Nouns:** When breaking a long multi-word noun, use the approved form of each technical noun from your company or industry documentation.
- **Rule 1.9 — Prefer Short, Clear Technical Nouns:** Within a multi-word noun, prefer the shorter approved technical noun when synonyms exist.
- **Rule 1.11 — One Term per Concept:** Within a document, use the same multi-word noun structure consistently. Do not write "configuration of the timeout" in one section and "timeout configuration" in another.
- **Rule 1.14 — American English Spelling:** All words within multi-word nouns must use American English spelling ("authorization," not "authorisation").
- **Rule 2.2 — Long Technical Nouns (Shorter Forms and Hyphens):** When a multi-word noun is a long technical noun that cannot be broken, use Rule 2.2 methods (shorter forms, hyphens).
- **STE-Code Dictionary (a-dictionary.md):** Consult the dictionary for the approved status and part of speech of each word used in a multi-word noun.

---

## Grammar Notes

### Attributive Nouns in English

In English, nouns can function attributively — that is, a noun placed before another noun modifies it. The sequence "database connection pool" uses "database" and "connection" as attributive nouns that modify the head noun "pool."

This grammatical feature is productive: it allows writers to create arbitrarily long chains. However, each added attributive noun increases the cognitive load on the reader. Research in technical communication shows that comprehension drops sharply after three attributive nouns.

### Head Noun Position Across Languages

In English, the head noun of a multi-word noun is the last word. In many other languages (Romance languages, Semitic languages, many Asian languages), the head noun comes first and modifiers follow. A reader whose native language places the head noun first must mentally reorder the entire English multi-word noun from the end. The longer the chain, the harder the reordering.

### Syntactic Ambiguity in Noun Chains

Each pair of adjacent nouns in a chain has an implied relationship. The reader must infer this relationship from context. In "API gateway request rate limiter," the relationships include:

- The gateway is FOR the API.
- The requests go TO the gateway.
- The rate is OF the requests.
- The limiter acts ON the rate.

When the chain exceeds three words, the number of possible interpretations grows combinatorially. Using prepositions makes each relationship explicit.

### Code Documentation Grammar vs. Code Grammar

Code identifiers (variable names, function names, class names) follow the grammar of the programming language, not the grammar of English prose. A function named `getDatabaseConnectionPoolTimeout()` is grammatically correct in code. A documentation sentence that says "Gets the database connection pool timeout" is not grammatically correct in STE-Code prose.

This rule governs documentation prose only. Never apply it to code identifiers inside backticks.

### Preposition Selection

When breaking a multi-word noun, the choice of preposition matters. Use:

- **"of"** for possession, composition, or attribution: "timeout of the pool"
- **"for"** for purpose or destination: "limiter for the requests"
- **"in"** for location or context: "connection in the pool"
- **"on"** for attachment or dependence: "threshold on the interval"
- **"from"** for source or origin: "recovery from the failure"
- **"to"** for direction or target: "requests to the gateway"

If you are not sure which preposition to use, "of" is the safest default for ownership and composition chains.

### Counting Rules

When counting the words in a multi-word noun for compliance with this rule:

1. **Hyphenated compounds count as one word.** "read/write" counts as one word. "higher-order" counts as one word.
2. **Articles (a, an, the) are not part of the multi-word noun.** They are part of the surrounding sentence. Do not count them.
3. **Prepositions that break the chain are not part of the multi-word noun.** In "configuration of the timeout," the multi-word noun is "configuration" (1 word) and "the timeout" (2 words in "timeout" — the article "the" is not counted). Each preposition-separated group is an independent multi-word noun unit.
4. **Code identifiers in backticks count as one word.** The identifier `` `getUserProfile` `` counts as one word regardless of its internal structure.
5. **Slash-joined terms count as one word.** "read/write," "input/output," "create/read/update/delete" each count as one word.
