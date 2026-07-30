# Rule 2.2 — Long Technical Nouns (Shorter Forms and Hyphens)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 2.2

## Original Rule

When a technical noun has more than three words, write it in full. Then, you can use one of these methods to make the technical noun clear:

- Give a shorter form of the technical noun.
- Use hyphens (-) between words that you use as one unit.

A long multi-word noun can be a long technical noun, or it can be a combination of shorter technical nouns. Frequently, it is not possible to divide technical nouns into smaller parts because they are the technical nouns that your company, industry, or subject field uses. Thus, you must write technical nouns as they are, in their approved form.

### Method 1 – Shorter form of technical nouns

If a long technical noun comes from an official document (for example, an engineering drawing or an illustrated parts catalog), write it in full the first time that it occurs in the text. Then, if it is possible, explain the technical noun and in the remaining text of your document, use a shorter form or an approved abbreviation.

**Examples in STE:**

Before you do this procedure, engage the ramp service door safety connector pin (the pin that holds the ramp service door, referred to in this procedure as the "safety connector pin").

In this example, you write "ramp service door safety connector pin" in full. Then, after an explanation, you give a shorter technical noun: "safety connector pin." This shorter technical noun has three words and obeys rule 2.1.

The Main Fuel Metering Unit (MFMU) is an aluminum alloy unit that includes a Main Engine Control Unit (MECU) and a Distribution Block (DB). The MFMU is installed in the engine bypass duct and operates in the engine fuel system. The function of the MFMU is to meter and supply the fuel from the Main Engine Fuel Pump (MEFP) to the fuel manifolds and the starter jets. The Digital Engine Control Unit (DECU) sends electrical signals to operate the MFMU.

In this example, the explanation is not necessary because the text gives all the necessary information about the unit. You write all official technical nouns that include more than three nouns in full the first time that they occur. Then, in the remaining parts of the text, you use their related approved abbreviations.

If an approved technical noun includes three words or less, it is not necessary to use abbreviations.

Example:

> **Do not write:**
> The primary parts of the valve are:
> - The DA (8)
> - The PVA (15)
> - The BA (17)
> - The VB (20).
>
> **Write:**
> The primary parts of the valve are:
> - The diaphragm assembly (8)
> - The poppet valve assembly (15)
> - The bush assembly (17)
> - The valve body (20).

You can use abbreviations that come from your official company documentation but be careful. A text full of abbreviations in a procedure, although shorter, is not easy to read.

### Method 2 — Hyphens (-) between the words that you use as one unit

A hyphen is a punctuation mark that connects words or parts of words. You can use hyphens between words to show how related words operate as one unit. This method will make the multi-word nouns that you use agree with rule 2.1. Hyphenated words always count as one word.

Examples in STE:

Make sure that the cutoff-switch power connection is safe. (3 words)

Inspection of the lavatory rapid-decompression device. (3 words)

Make sure that you do not connect words which are not related, because this hyphen will change the meaning of the multi-word noun. If you are not sure, only explain the multi-word noun. Then, use a shorter form, or an official approved abbreviation.

If an approved technical noun includes hyphens, do not change it. If it is too long, write it in full the first time it occurs and then use the recommended method (shorter technical nouns) specified in this rule.

Do not use hyphens to make groups of more than three words. If you use hyphens for all the words, this multi-word noun will not be easy to read and understand.

Example:

> **Non-STE:** Move the main-gear-door-retraction-winch handle. (2 words, but not correct)
> **STE:** Move the main-gear-door retraction-winch handle. (3 words)

If an approved technical noun includes three words or less (for example "poppet valve assembly" and "diaphragm assembly"), it is not necessary to use hyphens.

Example:

> **Do not write:**
> A. Remove the diaphragm-assembly (8) from the valve body (20).
> B. Remove the poppet-valve assembly (15) from its seat.
>
> **Write:**
> A. Remove the diaphragm assembly (8) from the valve body (20).
> B. Remove the poppet valve assembly (15) from its seat.

But, if an approved technical noun includes a hyphen (for example "inward-outward valve"), do not remove the hyphen. Keep the technical noun that comes from your official company documentation.

## STE-Code Adaptation

In code documentation, some technical terms have more than three words and cannot be broken down because they are the official names used by your company, programming language, framework, or subject field. Examples include formal class names, design pattern names, official API names, or names from architecture diagrams.

### Method 1 – Shorter form of technical nouns

Write the long technical noun in full the first time it occurs. Provide an explanation, then use a shorter form or the official abbreviation in the remaining text. Do not abbreviate technical nouns that already have three words or fewer.

### Method 2 — Hyphens

Use hyphens to group related words that function as a single unit within a multi-word noun. A hyphenated group counts as one word. Do not hyphenate words that are not related, and do not create hyphenated groups of more than three words. If an official technical noun already contains a hyphen (for example, from the source code or framework documentation), keep the hyphen.

### Examples

**Method 1 – Shorter form with explanation:**

> **Non-STE:** Before you run this script, configure the HTTP request pipeline middleware authentication handler.
> **STE:** Before you run this script, configure the HTTP request pipeline middleware authentication handler (the component that authenticates requests in the middleware pipeline, referred to in this document as the "authentication handler").

In this example, you write "HTTP request pipeline middleware authentication handler" in full. Then, after an explanation, you give a shorter technical noun: "authentication handler." This shorter technical noun has three words and obeys rule 2.1.

> **See also:** Rule 2.1 — Multi-word Nouns (Maximum Three Words)

**Method 1 – Shorter form with official abbreviation:**

> **Non-STE:** Before you run this script, configure the HTTP request pipeline middleware authentication handler.
> **STE:** Before you run this script, configure the HTTP request pipeline middleware authentication handler (the component that authenticates requests in the middleware pipeline, referred to in this document as the "authentication handler").
>
> The Object Relational Mapping (ORM) layer is a middleware component that includes a Query Builder (QB) and a Unit of Work (UoW) manager. The ORM layer operates in the data access pipeline and manages persistence for the domain model. The QB constructs database queries from the domain object graph. The UoW manager tracks changes to entities during a transaction.

**Method 1 – Do not abbreviate short technical nouns (three words or fewer):**

> **Non-STE:**
> The primary parts of the system are:
> - The CM (8)
> - The EB (15)
> - The CR (17)
> - The DTL (20).
>
> **STE:**
> The primary parts of the system are:
> - The cache manager (8)
> - The event bus (15)
> - The command router (17)
> - The data transfer layer (20).

This shorter technical noun has three words and obeys rule 2.1.

> **See also:** Rule 2.1 — Multi-word Nouns (Maximum Three Words)

**Method 2 – Hyphens between related words:**

> **Non-STE:** Move the data-access-layer-query-builder interface. (2 words, but not correct)
> **STE:** Move the data-access-layer query-builder interface. (3 words)

**Method 2 – Do not add hyphens to short approved technical nouns:**

> **Non-STE:**
> A. Remove the cache-manager (8) from the service container (20).
> B. Remove the event-bus (15) from its listener.
>
> **STE:**
> A. Remove the cache manager (8) from the service container (20).
> B. Remove the event bus (15) from its listener.

**Method 2 – Keep official hyphens from approved terms:**

> **Non-STE:**
> A. Remove the cache manager (8) from the service container (20). (removes the official hyphen from a framework term)
> B. Remove the read write lock (15) from its mutex. (removes the official hyphen from a concurrency primitive)
>
> **STE:**
> A. Remove the cache-manager (8) from the service container (20). (keeps the official hyphen from the framework documentation)
> B. Remove the read-write lock (15) from its mutex. (keeps the official hyphen from the concurrency library)

---

## Code-Domain Explanation

This rule applies to all forms of code documentation. Method 1 (shorter forms) and Method 2 (hyphens) have different applications depending on the documentation type.

### Method 1 Across Documentation Types

**README Files**

README files introduce a project. Long technical names for architecture components, services, or subsystems must appear in full on first use with a shorter form declared for the remaining document.

> **Non-STE (README architecture section):** The system depends on the Distributed Event Sourcing Aggregate Root Snapshot Storage Strategy.
> **STE (README architecture section):** The system depends on the Distributed Event Sourcing Aggregate Root Snapshot Storage Strategy (the strategy for storage of snapshots of the aggregate roots, referred to in this document as the "snapshot storage strategy").

> **Principle applied:** P1, P5 — "event sourcing," "aggregate root," and "snapshot" are approved technical nouns. The long official name appears once. The shorter form "snapshot storage strategy" then appears throughout the README.

**API Documentation**

API reference pages describe endpoints, parameters, and return types. Long endpoint paths or parameter groups benefit from a shorter reference name after the first full mention.

> **Non-STE (API endpoint description):** `POST /v1/user/profile/image/upload/progress` — Returns the user profile image upload progress percentage completion status.
> **STE (API endpoint description):** `POST /v1/user/profile/image/upload/progress` — Returns the user profile image upload progress percentage completion status (referred to in this reference as the "upload progress status").

> **Principle applied:** P1, P9 — the shorter form uses three words for quick scanning in the remaining endpoint descriptions.

**Docstrings and Inline Comments**

Docstrings are read by developers during maintenance. Long class names, type aliases, or design pattern names should be shortened after the first full mention in the module or class docstring.

> **Non-STE (module docstring):** This module implements the ObserverPatternNotificationDispatchRegistry. The ObserverPatternNotificationDispatchRegistry manages the subscriber list.
> **STE (module docstring):** This module implements the Observer Pattern Notification Dispatch Registry (referred to in this module as the "notification registry"). The notification registry manages the subscriber list.

> **Principle applied:** P1, P11 — once shortened, the term "notification registry" is used consistently throughout the module docstring and all function docstrings that reference it.

**Commit Messages**

Commit messages are scannable summaries. If a commit touches a component with a long official name, use the official abbreviation or a shorter form established in the project README. Do not introduce a new abbreviation in the commit message.

> **Non-STE (commit subject):** fix: race condition in DistributedEventSourcingAggregateRootSnapshotStorageStrategy initialization
> **STE (commit subject):** fix: race condition in snapshot storage strategy initialization

> **Principle applied:** P9, P11 — the shorter form matches the project README. The reader of the git log can scan the subject line without parsing a 6-word technical noun.

**Error Messages**

Error messages appear in logs under pressure. Long technical names in error messages delay diagnosis. Use the official abbreviation or a shorter form established in the codebase. If no shorter form exists, provide one in the project glossary and use it in error messages.

> **Non-STE (error message):** ERROR: DistributedEventSourcingAggregateRootSnapshotStorageStrategy configuration validation failed.
> **STE (error message):** ERROR: Configuration validation failed for the snapshot storage strategy (DistributedEventSourcingAggregateRootSnapshotStorageStrategy).

> **Principle applied:** P1, P9 — the shorter form "snapshot storage strategy" appears first for fast scanning. The full official name appears in parentheses for reference.

**Configuration Files and Environment Variables**

Configuration documentation describes settings that operators tune. When a group of settings belongs to a long-named subsystem, introduce the full name and its shorter form in the configuration file header comment. Use the shorter form in the individual setting descriptions.

> **Non-STE (config file):** `# Distributed Event Sourcing Aggregate Root Snapshot Storage Strategy settings` (then repeats the long name for each setting)
> **STE (config file):** `# Snapshot storage strategy settings (Distributed Event Sourcing Aggregate Root Snapshot Storage Strategy)` (then uses "snapshot storage strategy" for each setting description)

> **Principle applied:** P9, P11 — the header establishes the mapping. Each setting description uses the shorter, clearer form.

### Method 2 Across Documentation Types

**README Files**

Hyphens clarify compound adjectives that describe system properties. Use them sparingly to avoid visual clutter but apply them when the adjective pair would otherwise be ambiguous.

> **Non-STE:** The system provides real time data processing capabilities.
> **STE:** The system provides real-time data-processing capabilities.

> **Principle applied:** P4 — "real-time" and "data-processing" are hyphenated compound adjectives. Each counts as one word.

**API Documentation**

Parameter descriptions with compound adjectives benefit from hyphens. A hyphenated pair tells the reader that the two words form one semantic unit.

> **Non-STE (parameter description):** `mode` — Sets the read write access control mode.
> **STE (parameter description):** `mode` — Sets the read-write access-control mode.

> **Principle applied:** P4 — "read-write" is an official hyphenated term from the concurrency library. "access-control" groups the modifier pair.

**Docstrings and Inline Comments**

Hyphens in docstrings help when a function parameter name combines two concepts.

> **Non-STE (Python docstring):** timeout_ms: The request response timeout in milliseconds.
> **STE (Python docstring):** timeout_ms: The request-response timeout, in milliseconds.

> **Principle applied:** P1 — "request-response" clarifies that the timeout covers the full round trip, not only the request or only the response.

**Error Messages**

Hyphens in error messages group error categories for log parsing tools.

> **Non-STE:** ERROR: [auth] token validation failure
> **STE:** ERROR: [auth] token-validation failure

> **Principle applied:** P2 — "token-validation" acts as one compound noun describing the type of failure.

**Configuration Files**

Configuration setting groups use hyphens to connect related words without creating long unbroken chains.

> **Non-STE (env var):** `CACHE_MAX_IDLE_TIME_SECONDS`
> **STE (env var description):** The maximum idle-time, in seconds, for the connection pool.

> **Principle applied:** P4 — "idle-time" groups the modifier and the measured quantity as one concept.

---

## Paradigm-Specific Guidance

Different programming paradigms produce different types of long technical nouns. The strategies of this rule (shorter forms and hyphens) apply universally, but the patterns vary.

### Object-Oriented Programming (Java, C++, C#, Python Classes)

OOP documentation contains design pattern names, inheritance chain descriptors, and interface composition names. These frequently exceed three words and are official technical nouns.

> **Non-STE:** The AbstractFactoryMethodPatternImplementationRegistryBuilder constructs the registry.
> **STE:** The Abstract Factory Method Pattern Implementation Registry Builder (referred to in this document as the "registry builder") constructs the registry.

Design pattern names such as "Abstract Factory Method Pattern" are official technical nouns from the Gang of Four catalog. Write them in full the first time. After explanation, use the shorter form "registry builder."

> **Non-STE:** Inject the UserRepositoryInterfaceDependencyInjectionContainerBinding into the controller.
> **STE:** Inject the binding of the dependency injection container for the user repository interface (referred to in this class as the "repository binding") into the controller.

> **Principle applied:** P1, P7 — "binding" is used as a noun. The long official class name is restructured with prepositions and shortened for reuse.

For hyphen usage in OOP documentation:

> **Non-STE:** The single responsibility principle violation detection mechanism runs during static analysis.
> **STE:** The single-responsibility-principle violation-detection mechanism runs during static analysis.

> **Principle applied:** P4 — "single-responsibility-principle" groups the three words of the principle name into one hyphenated unit. "violation-detection" groups the action pair. Together the multi-word noun has 2 words instead of 5.

### Functional Programming (Haskell, Elixir, Clojure, Rust)

Functional documentation describes monadic transformer stacks, function composition chains, and algebraic data type hierarchies. These create technical nouns with many modifiers.

> **Non-STE:** The monadic error handling pipeline transformer composition chain evaluates the input.
> **STE:** The monadic error-handling pipeline transformer composition chain (referred to in this section as the "transformer chain") evaluates the input.

> **Principle applied:** P1, P4 — "error-handling" is hyphenated to count as one word. The shorter form "transformer chain" is then used throughout the section.

> **Non-STE:** Apply the higher order function currying partial application optimization.
> **STE:** Apply the higher-order function currying partial-application optimization (referred to as the "currying optimization").

> **Principle applied:** P4 — "higher-order" and "partial-application" use hyphens to group the modifiers. The shorter form makes the remaining explanation scannable.

### Procedural Programming (C, Go, Bash)

Procedural documentation names system calls, buffer chains, and handler sequences. These names are often official names from man pages or kernel documentation.

> **Non-STE:** The file descriptor read buffer allocation failure handler signals the caller.
> **STE:** The file-descriptor read-buffer allocation-failure handler (referred to as the "failure handler") signals the caller.

> **Principle applied:** P4 — hyphens group "file-descriptor" (one concept), "read-buffer" (one concept), and "allocation-failure" (one concept). The multi-word noun reduces from 6 words to 3.

> **Non-STE:** Execute the memory arena deallocation safety check routine.
> **STE:** Execute the memory-arena deallocation safety-check routine (referred to as the "safety check").

> **Principle applied:** P5, P9 — "memory-arena" is a technical code noun from systems programming. "safety-check" groups the action pair into one word.

### Declarative Programming (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes resource specifications, policy definitions, and query structures. These often come from official provider documentation or language specifications.

> **Non-STE:** The Kubernetes pod resource limit specification defines the maximum memory.
> **STE:** The Kubernetes pod resource-limit specification (referred to in this manifest as the "limit spec") defines the maximum memory.

> **Principle applied:** P5 — "Kubernetes" and "pod" are technical code nouns. "resource-limit" is hyphenated as one modifier. The shorter form "limit spec" is then used in the remaining resource descriptions.

> **Non-STE:** The Terraform module output variable dependency graph resolution algorithm runs before apply.
> **STE:** The Terraform module output-variable dependency-graph resolution algorithm (referred to as the "graph resolver") runs before the apply step.

> **Principle applied:** P4, P9 — hyphens in "output-variable" and "dependency-graph" reduce the word count. The shorter form "graph resolver" is used in the remaining plan documentation.

### Systems Programming (Rust Ownership, C Memory)

Systems documentation describes ownership models, lifetime annotations, and memory layout specifications. These are dense technical nouns that frequently exceed three words.

> **Non-STE:** The heap allocated reference counted thread safe pointer dereference operation returns the value.
> **STE:** The heap-allocated reference-counted thread-safe pointer dereference operation (referred to as the "smart-pointer dereference") returns the value.

> **Principle applied:** P4, P1 — "heap-allocated," "reference-counted," and "thread-safe" are hyphenated compound adjectives (one word each). After the full technical noun appears once, the shorter form "smart-pointer dereference" is used.

> **Non-STE:** The stack frame return address overflow protection mechanism prevents attacks.
> **STE:** The stack-frame return-address overflow-protection mechanism (referred to as the "stack protector") prevents attacks.

> **Principle applied:** P4 — each hyphenated pair counts as one word. The shorter form "stack protector" then replaces the long technical noun.

---

## Extended Examples

Each pair shows a real code-documentation scenario, the STE-Code fix, the method used, and the principle applied.

### Example 1 — README Architecture Section (Method 1: Shorter Form)

> **Non-STE:** The project uses the Command Query Responsibility Segregation pattern with a separate read model.
> **STE:** The project uses the Command Query Responsibility Segregation (CQRS) pattern with a separate read model. The CQRS pattern separates the command model from the query model.

**Method applied:** Method 1 — official abbreviation. **Principle applied:** P1, P5 — "Command Query Responsibility Segregation" is an official design pattern name (technical code noun). The abbreviation "CQRS" is the industry-standard short form. After the first full mention, "CQRS" is used throughout the README.

**Explanation:** The non-STE version repeats the 4-word pattern name in every section. The STE version introduces the official abbreviation once and uses it consistently.

### Example 2 — API Documentation (Method 1: Shorter Form with Explanation)

> **Non-STE:** The `POST /webhooks/payment-gateway/transaction/rollback/failure/recovery` endpoint initiates the payment gateway transaction rollback failure recovery procedure.
> **STE:** The `POST /webhooks/payment-gateway/transaction/rollback/failure/recovery` endpoint initiates the payment gateway transaction rollback failure recovery procedure (the sequence for recovery after a rollback fails, referred to in this reference as the "recovery procedure").

**Method applied:** Method 1 — shorter form with explanation. **Principle applied:** P1, P9 — "recovery procedure" uses canonical STE-Code words. The shorter form has 2 words.

**Explanation:** The API endpoint path itself is not shortened (it is a code identifier). The description introduces the long technical noun once with a parenthetical explanation, then uses "recovery procedure" for all subsequent mentions.

### Example 3 — Error Message (Method 2: Hyphens)

> **Non-STE:** ERROR: database connection pool timeout configuration value is out of range.
> **STE:** ERROR: Database-connection-pool timeout-configuration value is out of range.

**Method applied:** Method 2 — hyphens. **Principle applied:** P4 — "database-connection-pool" groups three words into one hyphenated unit. "timeout-configuration" groups the action pair. The multi-word noun has 2 hyphenated words.

**Explanation:** The hyphen groups help the log parser and the human reader identify the subject (the "value") and its qualifiers quickly without ambiguity.

### Example 4 — Docstring (Method 2: Selective Hyphens)

> **Non-STE:** Handles the Redis cache key expiration event notification dispatch.
> **STE:** Handles the Redis cache-key expiration-event notification dispatch (referred to in this module as "event dispatch").

**Method applied:** Method 2 — hyphens, with Method 1 — shorter form. **Principle applied:** P4, P9 — "cache-key" and "expiration-event" use hyphens to group modifiers. Then "event dispatch" is established as the shorter form.

**Explanation:** The non-STE version chains 5 nouns. The STE version hyphenates two pairs to reduce the chain to 3 nouns, then introduces a shorter form for reuse.

### Example 5 — Commit Message (Method 1: Project-Established Shorter Form)

> **Non-STE:** feat: add retry policy to payment gateway transaction rollback failure recovery procedure
> **STE:** feat: add retry policy to the recovery procedure

**Method applied:** Method 1 — shorter form (using the project README's established term). **Principle applied:** P9, P11 — the shorter form matches the established project terminology. The commit message is scannable.

**Explanation:** The commit message assumes the reader knows the project glossary. If the shorter form "recovery procedure" is established in the README, the commit message uses it without reintroducing the full name.

### Example 6 — Configuration File (Method 1 and Method 2 Combined)

> **Non-STE (YAML config):**
> ```yaml
> # Payment gateway transaction rollback failure recovery procedure settings
> payment_gateway_transaction_rollback_failure_recovery_procedure_max_attempts: 3
> payment_gateway_transaction_rollback_failure_recovery_procedure_backoff_ms: 1000
> ```
>
> **STE (YAML config):**
> ```yaml
> # Recovery procedure settings (payment gateway transaction rollback failure recovery procedure)
> recovery_procedure:
>   max_attempts: 3
>   backoff_ms: 1000
> ```

**Method applied:** Method 1 — shorter form with nested structure. **Principle applied:** P9, P11 — the YAML structure groups settings under a shorter key. The full official name appears in the comment for traceability.

**Explanation:** The non-STE version repeats the 6-word technical noun in every key. The STE version uses YAML nesting to group settings under the shorter form "recovery_procedure." Each individual key is now short and clear.

---

## Edge Cases

### Edge Case 1 — Framework Names That Contain "Unapproved" Words

Some framework names contain words that are not approved in STE-Code. The framework name itself is a technical code noun under Rule 1.5 and Rule 1.6. When introducing a long framework-based technical noun, apply Method 1 (shorter form) or Method 2 (hyphens) to the surrounding prose, not to the framework name.

> **Non-STE:** Configure the Spring Boot auto configuration bean post processor registry before the application context starts.
> **STE:** Configure the Spring Boot auto-configuration bean post-processor registry (referred to in this document as the "post-processor registry") before the application context starts.

"Spring" and "Boot" are not approved STE words individually, but "Spring Boot" is a framework name (technical code noun, Rule 1.5). The hyphens in "auto-configuration" and "post-processor" follow Method 2 to reduce the word count. The shorter form "post-processor registry" follows Method 1.

### Edge Case 2 — Code Keywords Inside Long Technical Nouns

When a code keyword (reserved word) appears as part of a long descriptive technical noun, the keyword itself is not subject to this rule. Apply hyphens or shorter forms to the surrounding prose words only. Keep the keyword in backticks.

> **Non-STE:** The `finally` block cleanup resource deallocation handler runs after the try-catch.
> **STE:** The `finally` block cleanup resource-deallocation handler (referred to as the "cleanup handler") runs after the try-catch statement.

> **Principle applied:** P5 — `finally` is a reserved word in Java, Python, and JavaScript. It appears in backticks to indicate code. The hyphen in "resource-deallocation" applies Method 2 to the prose words. The shorter form "cleanup handler" applies Method 1.

### Edge Case 3 — Relaxation for Auto-Generated Documentation

Auto-generated documentation (JSDoc output, Sphinx autodoc, Swagger/OpenAPI generated docs) may contain long technical nouns derived from code identifiers. These are acceptable in generated output because they reflect the source code directly. However, any manually written descriptions within the docstrings that feed the generator must follow this rule.

> **Acceptable in generated docs:** `getPaymentGatewayTransactionRollbackFailureRecoveryProcedureStatus()`
> *(This is a function name from source code, generated verbatim. Not subject to the rule.)*

> **Must be corrected in the source docstring:**
> **Non-STE (docstring):** Gets the payment gateway transaction rollback failure recovery procedure status.
> **STE (docstring):** Gets the status of the recovery procedure (the payment gateway transaction rollback failure recovery procedure).

The docstring introduces the shorter form "recovery procedure" and uses it. If the function name is long, the docstring serves as the bridge between the code identifier and the human-readable shortened term.

### Edge Case 4 — Hyphen Placement That Changes Meaning

Incorrect hyphen placement can change the meaning of a multi-word noun. Only hyphenate words that genuinely operate as one unit. When in doubt, use Method 1 (shorter form) instead of Method 2 (hyphens).

> **Ambiguous hyphen placement:**
> "small-business owner" (the owner of a small business) vs. "small business-owner" (a business owner who is small)
> "foreign-car dealer" (a dealer of foreign cars) vs. "foreign car-dealer" (a car dealer who is foreign)

In code documentation, the same risk exists:

> **Ambiguous:** "data-processing pipeline" vs. "data processing-pipeline"
> **Correct:** "data-processing pipeline" (the pipeline that processes data)

If you are not sure where to place the hyphen, do not use one. Instead, use a shorter form: "the pipeline for processing of the data" → "the data pipeline."

### Edge Case 5 — Abbreviation Collision

When two long technical nouns in the same document produce the same shorter form or abbreviation, you must disambiguate. Do not use the same short form for two different concepts.

> **Problem:**
> - "Distributed Transaction Coordinator" → DTC
> - "Data Transfer Controller" → DTC
>
> **Solution:** Use different shorter forms:
> - "Distributed Transaction Coordinator" → "transaction coordinator"
> - "Data Transfer Controller" → "transfer controller"

If the shorter forms are still ambiguous, add a distinguishing word:

> - "Distributed Transaction Coordinator" → DTC (distributed)
> - "Data Transfer Controller" → DTC (transfer)

---

## Cross-References

- **Rule 1.1 — Use Approved Words:** The words in the shorter form must all be approved STE-Code words. Do not introduce non-approved words when creating a shorter form.
- **Rule 1.5 — Technical Code Nouns:** Framework names, design pattern names, and official API names are technical code nouns. This rule provides the methods for handling them when they exceed three words.
- **Rule 1.6 — Non-Approved Words as Technical Code Nouns:** A long technical noun may contain non-approved words that are part of a framework name. The framework name stays intact under Rule 1.6. Apply Method 1 or Method 2 to the surrounding documentation.
- **Rule 1.11 — One Term per Concept:** After you introduce a shorter form, use it consistently. Do not switch between the full technical noun and the shorter form in the same document.
- **Rule 2.1 — Multi-word Nouns (Maximum Three Words):** The shorter forms and hyphenated groups produced by this rule must obey Rule 2.1. A shorter form must be three words or fewer. A hyphenated group must not connect more than three words.
- **Rule 1.4 — Approved Verb and Adjective Forms:** Hyphens frequently create compound adjectives. Ensure each component word uses its approved form from the STE-Code dictionary.
- **Rule 1.7 — Do Not Use Technical Nouns as Verbs:** When you create a shorter form, ensure the words in the shorter form are used as nouns (for a noun phrase) or as adjectives (for a compound adjective), never as verbs.
- **STE-Code Dictionary (a-dictionary.md):** Consult the dictionary for the approved status, part of speech, and approved meaning of each word used in the shorter form or hyphenated compound.

---

## Grammar Notes

### The Function of the Hyphen in Technical English

A hyphen serves two grammatical functions relevant to this rule:

1. **Compound modifier:** Two or more words joined by a hyphen to form a single adjective that modifies a following noun. Example: "real-time system" — "real-time" is one compound adjective modifying "system."

2. **Noun-unit binding:** Two or more nouns joined by a hyphen to indicate they form one conceptual unit within a larger multi-word noun. Example: "cutoff-switch power connection" — "cutoff-switch" is one unit (a type of switch), and the full multi-word noun has 3 words.

The original ASD-STE100 uses the hyphen for the second function primarily. In code documentation, both functions are relevant. Compound modifiers are common in API parameter descriptions ("read-write mode"). Noun-unit binding is common when describing system components ("data-access layer").

### When Hyphens Are Wrong

Do not use hyphens when:

1. **The words are already a recognized compound noun.** "Database" is one word, not "data-base." "Middleware" is one word, not "middle-ware." Check the STE-Code dictionary for approved compound nouns.

2. **The hyphen connects more than three words.** "Main-gear-door-retraction-winch" is 4 hyphenated words and is not permitted. Break the chain: "main-gear-door retraction-winch" (2 hyphenated units).

3. **The hyphen creates ambiguity.** As shown in Edge Case 4, misplaced hyphens can change meaning. If you are not sure, use Method 1 (shorter form) instead.

### Abbreviation Governance

Abbreviations introduced through Method 1 must be governed consistently across a project. Establish a project glossary (a `GLOSSARY.md` file or a section in the README) that lists:

- The full official technical noun
- The approved shorter form or abbreviation
- The document or section where it was first introduced

This prevents abbreviation collision (Edge Case 5) and ensures that every contributor uses the same shorter forms.

### When to Introduce the Shorter Form

Introduce the shorter form at the first occurrence of the long technical noun in each major document section. If a reader jumps to a section without reading the introduction, they must still find the shorter form defined.

For long documents (more than 10 printed pages), reintroduce the shorter form at the start of each chapter:

> The recovery procedure (the payment gateway transaction rollback failure recovery procedure, described in Section 2) is the focus of this chapter.

### Interaction With Code Identifiers

Code identifiers (variable names, function names, class names) are not subject to this rule. A function named `initializeDistributedTransactionCoordinator()` remains unchanged. However, the documentation that describes the function must apply this rule:

> **Non-STE (function description):** Initializes the Distributed Transaction Coordinator and returns the initialization status.
> **STE (function description):** Initializes the Distributed Transaction Coordinator (referred to as the "transaction coordinator") and returns the initialization status. The transaction coordinator manages distributed transactions across the cluster.

The shorter form "transaction coordinator" is now established for the remaining documentation of this module.
