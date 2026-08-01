# Rule 1.9 — When You Must Select a Technical Noun, Use One Which Is Short and Easy to Understand

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.9](ste-code/grouped/), Rule 1.9

## Original Rule

**Rule 1.9** When you must select a technical noun, use one which is short and easy to understand.

When there is no technical noun that is approved in your company, industry, or subject field, select one that is short (not more than three words) and easy to understand.

Example:

> **Non-STE:** Remove the four stainless steel pan head machine screws (10) that attach the metallic machined flange (15) to the front housing cover (20).
>
> **STE:** Remove the four screws (10) that attach the flange (15) to the cover (20).

In this example, it is sufficient to use the words "screws," "flange," and "cover." This is because these parts have index numbers, and the related illustration clearly identifies them. Differently, add one or two adjectives to the noun to help your reader understand.

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** Rule 1.10 — Do Not Use Regional, Slang, or Jargon Words as Technical Nouns
> **See also:** Rule 1.11 — Do Not Use Different Technical Nouns for the Same Item
> **See also:** Rule 1.13 — Do Not Use Technical Verbs as Nouns
> **See also:** Rule 1.14 — Use American English Spelling Unless Other Official Directives Tell You Differently
> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category

## STE-Code Adaptation

**Rule 1.9** When you must select a code-domain technical noun, use one which is short and easy to understand.

When there is no code-domain technical noun that is approved in your project, company, industry, or subject field, select one that is short (not more than three words) and easy to understand.

Do not use long descriptive phrases when a shorter term is sufficient. If the context clearly identifies the item (for example, a code snippet, a diagram, or an API reference), use the shortest term that is unambiguous. If additional clarification is necessary, add one or two adjectives to the noun to help your reader understand.


> *Adapted from spec pair:* Non-STE: Test the system for leaks.  |  STE: Do the leak test of the system.
### Examples

> **Non-STE:** Call the asynchronous JavaScript XML HTTP request wrapper utility function (line 42) to get the serialized JSON payload from the remote application programming interface endpoint.
>
> **STE:** Call the fetch utility (line 42) to get the JSON data from the API endpoint.

This adapts the spec pair: "Remove the four stainless steel pan head machine screws (10) that attach the metallic machined flange (15) to the front housing cover (20)" becomes "Remove the four screws (10) that attach the flange (15) to the cover (20)." In the spec, the long descriptive phrase "stainless steel pan head machine screws" is reduced to "screws" because the index number (10) and the illustration identify the part. In STE-Code, the long phrase "asynchronous JavaScript XML HTTP request wrapper utility function" is reduced to "fetch utility" because the line number (42) and the code snippet identify the function. "JSON payload" becomes "JSON data" and "remote application programming interface endpoint" becomes "API endpoint" — both follow the spec principle of using the shortest unambiguous term.

## Code-Domain Explanation

Rule 1.9 addresses a common failure in code documentation: the use of excessively long noun phrases when a short term would be clearer. Documentation writers often believe that more words equal more precision. The opposite is usually true. Long noun phrases increase cognitive load. The reader must parse a chain of modifiers before reaching the head noun. Short terms reduce this load.

The rule is not an absolute command to use only one-word nouns. It is a directive to use the shortest term that is unambiguous in context. When the context already identifies the item — through a code reference, a line number, a diagram, or a preceding definition — the short term is sufficient. When the context does not identify the item, the rule permits adding one or two adjectives.

The three-word limit is a guideline, not a hard constraint. Exceptions exist for established technical terms that require more than three words (for example, "abstract syntax tree," "single page application," "continuous integration pipeline"). These multi-word terms are acceptable under Rule 1.5 (code-domain technical nouns) when they name a precise concept that cannot be shortened without losing meaning.

### Application by Documentation Type

**README files.** README documents introduce a project. They must convey the project's purpose, installation, and usage quickly. Long noun phrases in a README discourage readers. A README that says "the multi-platform containerized microservice orchestration and deployment management layer" loses the reader. Write "the Kubernetes cluster" instead. The shorter term is more specific and more recognizable.

**API documentation.** API docs describe endpoints, parameters, and return types. Each endpoint, parameter, and type already has a name. Do not repeat the name with a long descriptive phrase. An API doc that says "the user account profile information data transfer object parameter" is redundant when the parameter is named `UserProfileDTO`. Write "the `UserProfileDTO` parameter" and let the type definition provide the details.

**Docstrings and inline comments.** Docstrings appear directly above the code they describe. The code itself provides the ultimate context. A docstring that describes a function named `validateEmailAddress` does not need to say "this function validates an electronic mail address string against a regular expression pattern that implements the RFC 5322 specification for internet message format addresses." Write "Validate an email address against RFC 5322." The function signature, the regex pattern, and the RFC reference are all visible in the code.

**Commit messages.** Commit messages are constrained by convention to a short subject line (50-72 characters) and an optional body. Long noun phrases in the subject line force wrapping or truncation. A commit message subject that says "Refactor the asynchronous task processing and scheduling subsystem initialization sequence" exceeds typical length limits. Write "Refactor the task scheduler initialization." The body can provide additional detail.

**Error messages.** Error messages appear in logs, terminals, and alert systems. They are often truncated by display tools. Long noun phrases in error messages waste the reader's time and increase the chance that critical information is cut off. An error message that says "The remote procedure call connection handshake negotiation to the primary database cluster node failed" should be "Connection to the primary database node failed." The short version tells the reader what failed and which component is affected.

**CLI help text and man pages.** Command-line help text has limited horizontal space (typically 80 columns). Long noun phrases cause line wrapping that makes help text unreadable. Use the shortest term that identifies the concept. A flag description that says "Specifies the maximum number of concurrent parallel worker thread processes" should be "Maximum number of worker threads."

### The Context Principle

The core insight of Rule 1.9 is that context permits brevity. The original ASD-STE100 example demonstrates this: index numbers and illustrations provide context, so short nouns ("screws," "flange," "cover") are sufficient. In code documentation, equivalent context sources include:

- **Code references:** A line number, a function name, a class name, or a file path identifies the item unambiguously. Use the short term plus the reference.
- **Diagrams and figures:** An architecture diagram that labels components with short names makes long descriptions unnecessary in the accompanying text.
- **Preceding definitions:** If you define a term at first use ("the authentication service, called AuthService"), use the short name for all subsequent references.
- **API specifications:** An OpenAPI spec or a protobuf definition that fully describes a type makes long descriptions in prose redundant. Reference the type by name.
- **Code snippets:** When a code snippet follows the prose, the snippet provides full context. The prose only needs to introduce the snippet, not duplicate its content.

When none of these context sources are available, add one or two adjectives to the noun. The adjectives must be necessary for disambiguation. Do not add adjectives that describe properties already visible in the context.

### The Three-Word Limit: Rationale and Exceptions

The three-word limit is derived from the original ASD-STE100 specification, which states that a technical noun must be "short (not more than three words)." The limit reflects cognitive research: readers can hold approximately three to four chunks of information in working memory. A noun phrase of more than three words exceeds this capacity and forces the reader to re-read.

Exceptions to the three-word limit:

1. **Established technical terms.** Terms such as "continuous integration pipeline" (3 words), "single sign-on provider" (3 words), and "abstract syntax tree" (3 words) are at the limit. Terms such as "public key infrastructure certificate" (4 words) exceed the limit but are standard in the security domain. Use the established term even if it exceeds three words. Do not invent a shorter form that the community does not use.

2. **Framework and tool names.** Names such as "GitHub Actions workflow," "Amazon Web Services Lambda," and "Google Cloud Platform" exceed three words but are proper nouns. Use them as given. Do not abbreviate unless the abbreviation is a recognized technical noun (for example, "AWS Lambda").

3. **Fully qualified type names.** In strongly typed languages, fully qualified names can be long (for example, `com.example.project.module.SubComponent`). Use the short name (`SubComponent`) after the first reference, or use the language's import/alias mechanism to refer to the type.

4. **When shortening causes ambiguity.** If shortening a four-word phrase to three words creates ambiguity between two different concepts, keep the four-word phrase. Clarity overrides brevity.

## Paradigm-Specific Guidance

### Object-Oriented Paradigm (Java, C++, C#, Python classes)

Object-oriented documentation often describes class hierarchies with long inheritance chains. Writers describe a class as "the abstract base repository implementation class that extends the generic type-parameterized CRUD repository interface." This phrase buries the class name under six modifiers.

**Practice:** Use the class name. The reader can inspect the class definition for its inheritance chain, type parameters, and implemented interfaces. Write "the `UserRepository` class." If the inheritance is relevant to the discussion, state it in a separate sentence: "`UserRepository` extends `BaseRepository<User>`."

**Before:** The concrete factory method implementation class instantiates the appropriate data access object implementation based on the runtime configuration profile.
**After:** The `DaoFactory` class creates the correct DAO implementation for the active configuration profile.

**Before:** The dependency injection inversion of control container manages the lifecycle of the singleton-scoped service provider instances.
**After:** The DI container manages the lifecycle of singleton services.

In the second example, "DI" is a recognized abbreviation (category 16, Rule 1.5). "IoC" is removed because "DI container" already implies the concept. "Singleton-scoped service provider instances" becomes "singleton services" — the scope and role are clear from the context of DI documentation.

### Functional Paradigm (Haskell, Elixir, Clojure, Rust)

Functional programming documentation often describes transformations with long noun phrases that trace the entire data-flow chain. A writer describes a value as "the result of applying the partially applied curried function composition pipeline to the input list after mapping and filtering." The phrase describes the entire computation instead of naming the result.

**Practice:** Name the result. Use a short noun phrase that identifies what the value represents, not how it was computed. The computation is visible in the code.

**Before:** The monomorphized iterator adapter chain with lazy evaluation semantics produces a collection of transformed elements.
**After:** The iterator produces a transformed collection.

**Before:** The higher-order function that takes a binary operation and an initial accumulator value and returns a function that reduces a foldable data structure to a single value.
**After:** The fold function. It reduces a collection to a single value.

In the second example, "fold" is a standard algorithmic term (category 7). The long description duplicates what every functional programmer already knows. Use the standard term.

**Before:** The discriminated union algebraic data type with exhaustive pattern matching guarantees.
**After:** The enum type. Pattern matching covers all variants.

"Enum" is a data type term (category 4). "Discriminated union" and "algebraic data type" are synonyms in this context. Choose one and use it consistently (Rule 1.11). Do not use both in the same noun phrase.

### Procedural Paradigm (C, Go, Bash)

Procedural documentation often describes functions with long noun phrases that list every parameter, return value, and side effect. A C function description says "the function that accepts a pointer to a null-terminated character array and an unsigned integer representing the maximum buffer size and returns an integer status code indicating success or failure." This phrase describes the entire function signature.

**Practice:** Name the function. Describe its purpose in a short sentence. Let the function signature carry the type information.

**Before:** The variadic formatted output to file descriptor function with thread-safe internal buffering.
**After:** The `fprintf` function. It writes formatted output to a file descriptor.

**Before:** The dynamically allocated resizable contiguous memory region management utility.
**After:** The dynamic array. It grows as you add elements.

In the second example, "dynamic array" is a standard data structure term (category 4). The long phrase "dynamically allocated resizable contiguous memory region management utility" describes implementation details that are not needed for understanding the concept.

**Before:** The mutual exclusion lock primitive with timeout-bounded acquisition and deadlock detection.
**After:** The mutex. It has a timeout and deadlock detection.

"Mutex" is a computer science term (category 16). The additional features (timeout, deadlock detection) are described in a separate sentence, not embedded in the noun phrase.

### Declarative Paradigm (SQL, Terraform, Kubernetes YAML)

Declarative documentation often describes resources with long noun phrases that enumerate every attribute. A Terraform doc says "the Amazon Web Services Elastic Compute Cloud virtual machine instance resource with attached elastic block store volume and security group configuration." This phrase embeds the entire resource configuration.

**Practice:** Name the resource type. Describe the configuration in bullet points or a table. The declarative code itself is the ultimate reference.

**Before:** The Kubernetes horizontal pod autoscaling controller with CPU utilization metric threshold and minimum and maximum replica count bounds.
**After:** The `HorizontalPodAutoscaler` resource. It scales pods based on CPU utilization. Set the minimum and maximum replica counts.

**Before:** The Structured Query Language parameterized query with multiple table joins, aggregate functions, grouping clauses, and sorted result set.
**After:** The parameterized query. It joins the `users` and `orders` tables and groups results by region.

In the second example, the long phrase describes the SQL structure. The short description states what the query does. The SQL code itself shows the joins, aggregates, and sorting.

### Systems Programming (Rust ownership, C memory management)

Systems documentation often describes memory operations with long noun phrases that explain every safety guarantee. A Rust doc says "the compile-time checked reference that enforces the borrowing rules and prevents simultaneous mutable and immutable access to the same memory location." This phrase explains what the borrow checker does, not what the reference is.

**Practice:** Use the short term ("reference," "borrow," "lifetime"). The Rust compiler enforces the guarantees. Documentation describes what the programmer controls, not what the compiler prevents.

**Before:** The affine type system linear resource ownership tracking mechanism that prevents use-after-move errors at compile time.
**After:** The ownership system. It prevents use-after-move errors.

**Before:** The dynamically sized slice reference type with bounds checking that prevents out-of-bounds memory access at runtime.
**After:** The slice reference. Bounds checks prevent out-of-bounds access.

In both examples, the safety mechanism (ownership, bounds checking) is described in a separate sentence. The noun phrase names the concept. The explanation follows.

## Extended Examples

### Example Group 1: README Project Description

> **Non-STE:** This is a high-performance, event-driven, non-blocking I/O model JavaScript runtime environment built on Chrome's V8 JavaScript engine that uses an asynchronous, single-threaded event loop architecture for building scalable network applications.
>
> **STE:** Node.js is a JavaScript runtime. It uses an event-driven, non-blocking I/O model. Use it to build scalable network applications.

- **Principle applied:** P9 (use short technical nouns: "Node.js" is 2 words, "JavaScript runtime" is 2 words)
- **Explanation:** The non-STE version is a 42-word noun phrase that embeds architecture details, the engine name, and the use case. The STE version names the technology in two words, then explains the architecture and use case in separate sentences. The reader can absorb each piece of information independently. This follows the spec principle: "screws" (one word) replaces "stainless steel pan head machine screws" (six words). The context — the README title, the installation section, the code examples — makes the short term sufficient.

### Example Group 2: API Documentation Parameter Description

> **Non-STE:** The request body must contain a JSON object with a required string field named "emailAddress" that must match the standard internet electronic mail address format as defined by RFC 5322, an optional string field named "displayName" with a maximum length of 100 Unicode characters, and a required boolean field named "subscribeToNewsletter" that defaults to false if not provided.
>
> **STE:** The request body is a JSON object with these fields:
> - `emailAddress` (string, required) — a valid email address
> - `displayName` (string, optional, max 100 characters)
> - `subscribeToNewsletter` (boolean, optional, default: `false`)

- **Principle applied:** P9 (use short technical nouns: each field name is a one-word or two-word noun)
- **Explanation:** The non-STE version is a single 86-word sentence that embeds field names, types, constraints, defaults, and a reference to an RFC. The STE version uses a bulleted list. Each field is described with its name, type, and constraint. The RFC reference is removed because the field name "emailAddress" and the constraint "a valid email address" are sufficient for the API documentation. The API consumer can look up RFC 5322 if they need the full specification. This follows the spec principle: the field name is like the index number (10) in the original example — it identifies the item unambiguously, so a short description is sufficient.

### Example Group 3: Docstring for a Function

> **Non-STE:** This public static factory method constructs and returns a newly created, fully initialized, thread-safe instance of the UserService class with all of its required collaborator dependencies injected and its internal state properly configured for the current runtime environment.
>
> **STE:** Create and return a new `UserService` instance with the given dependencies.

- **Principle applied:** P9 (use short technical nouns: "UserService instance" is 2 words, "dependencies" is 1 word)
- **Explanation:** The non-STE version is a 40-word noun phrase that describes the method's visibility ("public"), its nature ("static factory"), its return behavior ("newly created"), its thread safety, its initialization state, and its configuration. The STE version states the action ("create and return") and the result ("a new UserService instance"). The code signature shows visibility, static modifier, and parameter types. The class documentation describes thread safety. The docstring does not need to repeat information that the code already conveys. This follows the spec principle: the function signature is like the illustration in the original example — it provides context that makes a long description unnecessary.

### Example Group 4: Commit Message Subject Line

> **Non-STE:** Refactor the authentication and authorization middleware layer to extract the JSON Web Token validation and user permission role resolution logic into separate composable utility functions.
>
> **STE:** Refactor auth middleware: extract JWT validation and role resolution into separate utilities.

- **Principle applied:** P9 (use short technical nouns: "auth middleware" is 2 words, "JWT validation" is 2 words, "role resolution" is 2 words)
- **Explanation:** The non-STE version is a 28-word subject line that exceeds typical commit message length limits (50-72 characters recommended). The STE version is 13 words with a clear structure: action (refactor), target (auth middleware), colon, detail (extract X and Y into Z). "Authentication and authorization" becomes "auth" — the abbreviation is recognized in the codebase. "JSON Web Token" becomes "JWT" — the acronym is an approved technical noun (category 19). "User permission role resolution logic" becomes "role resolution" — the context (auth middleware) makes "user permission" redundant. This follows the spec principle: just as "stainless steel pan head machine screws" becomes "screws," the commit message uses the shortest term that the project context makes unambiguous.

### Example Group 5: Error Message

> **Non-STE:** The operation to establish a connection to the primary relational database management system server instance located at the network address 192.168.1.100 on the default Transmission Control Protocol port number 5432 has failed due to a network timeout condition after waiting for the configured connection timeout duration of 30 seconds.
>
> **STE:** Connection to the primary database at 192.168.1.100:5432 timed out after 30 seconds.

- **Principle applied:** P9 (use short technical nouns: "primary database" is 2 words, "timed out" is a technical verb per P12)
- **Explanation:** The non-STE version is a 55-word sentence that embeds the database type ("relational database management system"), the server role ("primary"), the protocol ("Transmission Control Protocol"), the default port ("5432"), the failure type ("network timeout condition"), and the duration. The STE version is a 13-word sentence that conveys the same information: what failed (connection), where (192.168.1.100:5432), what happened (timed out), and when (after 30 seconds). The protocol is implied by the port number and the term "database." The database type is implied by "primary" (which implies a replica set, specific to certain databases). The error message reader needs to know what to fix, not what every acronym expands to. This follows the spec principle: the short term is sufficient because the context (a database connection error) identifies the components.

### Example Group 6: CLI Help Text

> **Non-STE:** Specifies the maximum permitted quantity of simultaneously executing concurrent parallel worker subprocess threads that the application is permitted to spawn and manage for the purpose of processing items from the background job queue.
>
> **STE:** Maximum number of worker threads for the job queue.

- **Principle applied:** P9 (use short technical nouns: "worker threads" is 2 words, "job queue" is 2 words)
- **Explanation:** The non-STE version is a 36-word description for a single flag. It uses synonyms piled together ("simultaneously executing concurrent parallel") and redundant permissions language ("permitted to spawn and manage"). The STE version is 9 words. "Maximum" implies the flag sets an upper bound. "Worker threads" names the resource. "Job queue" names the target. The reader does not need to be told that threads are "subprocess threads" or that they "process items" from a queue — these are inherent to the concepts of "worker threads" and "job queue." This follows the spec principle: reduce to the shortest term that is unambiguous in the program's context.

## Edge Cases

### Edge Case 1: When the Short Term Is Less Well-Known Than the Long Term

Some short technical nouns are obscure. A documentation writer might use "AST" (2 words when expanded: "abstract syntax tree") because it is short, but a junior developer may not know the acronym. The rule says to use the term that is "easy to understand," not just short.

**Resolution:** Use the expanded form at first use: "abstract syntax tree (AST)." Use "AST" for all subsequent references. If the audience is expected to know the acronym (for example, in a compiler documentation context), use "AST" directly. The ease-of-understanding test is: would a developer with one year of experience in this domain understand the term? If yes, the short term is acceptable. If no, expand on first use.

### Edge Case 2: When a Framework Name Is Also a Short Word

Frameworks with short, common-word names (React, Vue, Go, Rust, Next, Nest, Swift, Elm) create ambiguity. In a sentence such as "Use React to react to user input," the word "React" appears twice with different meanings. The short word is ambiguous.

**Resolution:** Use the framework name as a modifier: "the React framework" or "the Go language." This adds one word and resolves the ambiguity. After the first use, the bare name is acceptable if the context is clear. Do not create a new abbreviation to avoid the ambiguity — "Rkt" for "React" is not a standard term and violates Rule 1.8 (use standard technical nouns).

### Edge Case 3: When the Codebase Uses Long Names Internally

Some codebases use long, descriptive class names and function names by convention (for example, Java enterprise applications with names like `AbstractUserAuthenticationProviderFactoryBean`). Rule 1.9 says to use short terms, but the codebase name is the approved technical noun (Rule 1.8). The rules appear to conflict.

**Resolution:** Rule 1.8 takes precedence for names that are defined in the codebase. Use the codebase name as given. Rule 1.9 applies to the prose that surrounds the name. You can refer to "the factory bean" (short) in prose after introducing the full name: "The `AbstractUserAuthenticationProviderFactoryBean` (the factory bean) creates authentication providers." Do not rename the class in the code or in references — only in the surrounding prose.

### Edge Case 4: When Shortening Creates a Homonym

In some domains, a short term can refer to two different concepts. For example, "cache" can mean a hardware CPU cache or a software in-memory cache. "Pool" can mean a thread pool, a connection pool, or an object pool. If shortening "database connection pool" to "pool" could cause confusion with "thread pool" in the same document, the short term is not unambiguous.

**Resolution:** Keep the disambiguating modifier. "Connection pool" and "thread pool" are both two-word phrases (within the three-word limit). The one-word form "pool" is acceptable only when the document discusses exactly one kind of pool throughout. If the document discusses both, always use the two-word form. Context determines sufficiency.

### Edge Case 5: Generated Documentation and Automated Summaries

Tools such as JSDoc, Sphinx, and godoc generate documentation from source code. These tools often produce verbose output that includes the full type signature, all parameters, and all return values in a single block. The generated text may violate the three-word limit for noun phrases because it mechanically reproduces the code structure.

**Resolution:** Generated documentation is exempt from Rule 1.9 for the auto-generated portions (same principle as Edge Case 4 in Rule 1.5). However, any human-written summary, description, or comment within the generated documentation must follow Rule 1.9. When writing a JSDoc `@description` tag or a Python docstring summary line, apply the rule: use the shortest term that is unambiguous.

## Cross-References

- **Rule 1.1 (Approved Words):** When you shorten a noun phrase, replace non-approved words with approved words from the dictionary. For example, "leverage the authentication mechanism" becomes "use the auth service" — "leverage" is replaced with "use" (Rule 1.1), and "authentication mechanism" is shortened to "auth service" (Rule 1.9). The two rules work together.

- **Rule 1.5 (Technical Code Nouns):** Rule 1.5 defines which terms are permissible as code-domain technical nouns. Rule 1.9 applies after Rule 1.5: once you have identified a permissible technical noun, select the shortest form of it. "Application programming interface" is a technical noun under category 19; Rule 1.9 says to use "API."

- **Rule 1.6 (Non-Approved Words as Technical Nouns):** Rule 1.6 forbids non-approved words except as technical nouns. Rule 1.9 applies to the technical nouns that Rule 1.6 permits. A technical noun that passes Rule 1.6 must also pass Rule 1.9: it must be short and easy to understand.

- **Rule 1.8 (Standard Technical Nouns):** Rule 1.8 requires you to use the technical noun that is approved in your project or industry. Rule 1.9 says to use the shortest form of that approved noun. When the industry standard is a long form ("Transport Layer Security"), use the standard short form if one exists ("TLS"). Do not invent a non-standard short form ("TransSec").

- **Rule 1.10 (No Slang or Jargon):** Rule 1.10 forbids slang and jargon as technical nouns. Rule 1.9 reinforces this: a short slang term ("repo" for "repository") may seem to satisfy the shortness requirement, but it fails the "easy to understand" test for readers outside the community. Use the standard short form ("repository") or a recognized abbreviation.

- **Rule 1.11 (One Term per Concept):** Rule 1.11 requires consistency. When you shorten a technical noun under Rule 1.9, use the same shortened form everywhere in the document. Do not use "auth service" in one paragraph and "authentication module" in the next for the same component. Choose one short form and apply it consistently.

- **Rule 1.13 (Do Not Use Technical Verbs as Nouns):** Rule 1.13 forbids using verbs as nouns. A common violation occurs when writers shorten a noun phrase by converting a verb to a noun: "the deploy" instead of "the deployment process." Rule 1.9 does not permit this. The short form must be a noun, not a verb used as a noun.

- **Rule 1.14 (American English Spelling):** When a short form has both American and British spellings, use the American spelling. "Initialize" (American) not "initialise" (British). "Color" not "colour." This applies to all forms: full nouns, shortened nouns, and adjectives.

## Grammar Notes

### The Structure of Long Noun Phrases in Code Documentation

The original ASD-STE100 specification identifies the "noun cluster" as the primary source of long noun phrases. A noun cluster is a sequence of nouns and adjectives that all modify the final head noun. In code documentation, noun clusters follow predictable patterns:

**Pattern 1: Stacked Modifiers.** Writers stack multiple modifiers before the head noun: "the asynchronous event-driven non-blocking I/O JavaScript runtime environment." Each modifier adds a property. The reader must hold all modifiers in memory until reaching the head noun "environment."

**Correction:** Move modifiers into a separate clause or sentence. "The JavaScript runtime uses an asynchronous, event-driven, non-blocking I/O model."

**Pattern 2: Embedded Type Information.** Writers embed type information into the noun phrase: "the `Promise<Array<User>>` typed asynchronous function return value." The type is already visible in the code signature.

**Correction:** Name the concept, not the type. "The function returns a promise that resolves to an array of users."

**Pattern 3: Embedded Implementation Details.** Writers embed how something works into what it is called: "the Redis-backed distributed rate-limiting token bucket algorithm implementation." The implementation detail (Redis-backed, token bucket algorithm) is supplementary.

**Correction:** Separate the name from the implementation. "The rate limiter uses a token bucket algorithm backed by Redis."

**Pattern 4: Synonym Chains.** Writers use multiple synonyms to ensure they cover every possible interpretation: "the configuration, settings, and options parameters object." If the object is named `Config`, all three nouns refer to the same thing.

**Correction:** Choose one term. Use it consistently. "The `Config` object."

### Adjectives and the Three-Word Limit

The rule permits one or two adjectives when necessary for disambiguation. The adjectives must serve a purpose. They must distinguish the noun from other nouns in the same context. Adjectives that do not add disambiguating information are "noise adjectives" and must be removed.

**Noise adjective:** "the configurable application settings object" — All settings objects are configurable. The adjective adds no information.

**Disambiguating adjective:** "the production application settings object" — In a context where production, staging, and development settings all exist, "production" disambiguates.

**Noise adjective:** "the secure HTTPS protocol" — HTTPS is secure by definition.

**Disambiguating adjective:** "the legacy HTTPS endpoint" — In a context where old and new endpoints coexist, "legacy" disambiguates.

When you add an adjective, add exactly one. If the noun phrase reaches three words (adjective + adjective + noun), verify that both adjectives are necessary. If one can be removed without creating ambiguity, remove it.

### The Role of Abbreviations and Acronyms

Abbreviations and acronyms are the most direct application of Rule 1.9 in code documentation. The long form is a technical noun (permitted by Rule 1.5). The abbreviation is the short form (permitted by Rule 1.9). The decision to abbreviate depends on audience familiarity:

- **Universal abbreviations:** API, JSON, SQL, HTML, HTTP, URL, DNS, TCP, TLS, CPU, RAM, SSD. These are understood by all professional developers. Use the abbreviation on first reference. Expansion is optional.
- **Domain-specific abbreviations:** JWT (JSON Web Token), CORS (Cross-Origin Resource Sharing), ORM (Object-Relational Mapping), SPA (Single Page Application), SSR (Server-Side Rendering). These are understood within specific domains. Expand on first use in documents that serve a general audience. Use bare in documents that serve the domain audience.
- **Project-specific abbreviations:** Internal abbreviations that are defined in the project glossary. Expand on first use in every document. The abbreviation is acceptable only after it has been defined.

Do not create new abbreviations to satisfy Rule 1.9. An abbreviation is a word that the community recognizes. An abbreviation you invent today is a word nobody recognizes. It fails the "easy to understand" criterion.

### Shortening Without Losing Precision

The most common objection to Rule 1.9 is that shortening a noun phrase loses precision. This objection misunderstands the role of context. Precision comes from the combination of the noun phrase and its context. A long noun phrase in isolation is precise. A short noun phrase in context is equally precise and easier to read.

Consider the original ASD-STE100 example again. "Stainless steel pan head machine screws" is more precise in isolation than "screws." But in context — the illustration labels the screws, the index number (10) identifies them, the procedure step says "remove" — "screws" is precise enough. The precision lives in the context, not the noun phrase.

The same principle applies to code documentation. The code, the API spec, the diagram, and the preceding text all provide context. The noun phrase does not need to carry all the information alone. Trust the context. Write the short term.

## Practical Application: Documentation Review Checklist

Use this checklist when reviewing code documentation for Rule 1.9 compliance:

1. Identify every noun phrase of four or more words. Is there a shorter form?
2. For each long noun phrase, check if the context already identifies the item. Does a code reference, diagram, or preceding definition make the long form unnecessary?
3. If the context identifies the item, replace the long phrase with the shortest unambiguous form.
4. If the context does not identify the item, reduce the phrase to three words or fewer by removing noise adjectives and embedded implementation details.
5. Move removed details into separate sentences. One detail per sentence.
6. Check that every adjective in the shortened phrase serves a disambiguating purpose. Remove noise adjectives.
7. Verify that the shortened form is a recognized term (Rule 1.8), not a newly invented abbreviation.
8. Verify that the same shortened form is used consistently throughout the document (Rule 1.11).
9. For abbreviations, expand on first use unless the abbreviation is universal.
10. Read the shortened phrase aloud. Is it easy to understand? If not, the phrase is too short. Add one disambiguating adjective.

NOTE: This checklist is a guide. Professional judgment is always necessary when deciding between brevity and clarity. When the two conflict, clarity wins.
