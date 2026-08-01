# Rule 9.4 — When You Select Terminology or Wording, Always Use a Consistent Style

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec9-rule9.4](ste-code/grouped/), Rule 9.4

## Original Rule

When you select terminology or wording, always use a consistent style.

In procedures, you will frequently give the same information again and again. For example, most procedures give instructions on how to remove or install components or parts. When you select terminology or wording for a work step, use the same terminology or wording each time that type of work step occurs. The reader will identify the terminology or wording and will quickly understand the action. Different terminology or wording can cause confusion and delays.

In descriptive writing, the reader must understand the text as a unit. Thus, it is important to use words and sentences correctly and give a logical structure to the text. This method makes the text easier to read and understand.

## STE-Code Adaptation

> **See also:** Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient; Rule 9.2 — Use Each Approved Word Correctly

When you select terminology or wording in code documentation, always use a consistent style.

In procedural code documentation, you frequently give the same type of instruction again and again. For example, most setup guides give instructions on how to install dependencies, configure settings, or initialize a project. When you select terminology or wording for a step, use the same terminology or wording each time that type of step occurs. The reader will identify the consistent terminology and will quickly understand the action. Different terminology or wording for the same action can cause confusion and delays.

This applies to all levels of consistency: use the same name for the same item (do not alternate between "configuration file," "settings file," and "config"), use the same verb for the same action (do not alternate between "compile," "build," and "make"), and use the same sentence structure for the same type of instruction.

In descriptive writing, the reader must understand the text as a unit. Use words and sentences correctly and give a logical structure to the text. This method makes the text easier to read and understand.


> *Adapted from spec pair:* Non-STE: The oil level on the sight gauge must be visible during the test.  |  STE: During the test, make sure that you can see the oil level on the sight gauge.
### Examples

Inconsistent (non-STE) documentation:

```
1. Open the configuration file in a text editor.
2. Change the port number in the settings file.
3. Save the config and close it.
4. Compile the project with the build command.
5. Make the binary for the target platform.
6. If you get errors, look at the log file.
```

STE-Code (consistent):

```
1. Open the configuration file in a text editor.
2. Change the port number in the configuration file.
3. Save the configuration file and close it.
4. Build the project with the build command.
5. Build the binary for the target platform.
6. If you get errors, look at the log file.
```

In the non-STE text, you can see different wordings:
- Different terms for the same file ("configuration file," "settings file," and "config")
- Different verbs for the same action ("compile," "build," and "make")

In the STE-Code text, each time that the same item occurs, it has the same noun, and the same action always has the same verb. This makes the text clear and easy to read.

*Adapted from spec pair: the bolt lubrication procedure example showing inconsistent naming ("main body" / "body" / "body assembly") vs. consistent naming throughout a procedure — see spec pages 122–123 for the full original.*

## Code-Domain Explanation

This rule operates at every level of code documentation. Inconsistency creates a cognitive tax on the reader — each synonym forces the reader to pause and ask "is this the same thing or a different thing?" When the reader must resolve ambiguity, the documentation has failed its purpose.

### How the Rule Applies to Each Documentation Type

**README files:** The README is often the first and only document a user reads. If the README calls the project a "library" in paragraph 1 and a "package" in paragraph 3, the reader must guess whether these refer to the same artifact. Pick one term and use it throughout.

**API documentation:** An endpoint, method, or parameter must have exactly one name across all references. If the reference documentation for `GET /users/:id` describes the response field as `createdAt` but the prose calls it "creation date," "timestamp," and "created time" across different sections, the reader cannot map the prose to the schema.

**Docstrings and inline comments:** A function's docstring must use the same term that appears in the function signature. If a parameter is named `max_retries`, do not call it "maximum attempts" or "retry limit" in the docstring body. The reader correlates prose with the signature by name, not by inference.

**Commit messages:** Within a project, use the same imperative verb for the same category of change. If the convention is `Add`, do not mix in `Introduce`, `Insert`, or `Create` for new files. If the convention is `Fix`, do not mix in `Resolve`, `Correct`, or `Patch`.

**Error messages:** An error code must produce the same message text every time. If `E_CONNECT_FAIL` says "connection refused" in module A and "cannot connect to server" in module B, the operator cannot search logs reliably. Error message consistency is a reliability property.

**CLI output and help text:** If the `--output` flag is described as "output directory" in `--help`, the same phrase must appear in man pages, online docs, and error messages about that flag.

### Consistency Domains

Rule 9.4 governs consistency across three orthogonal dimensions, each of which must be maintained independently:

**Lexical consistency (same term for same thing):** Within a document or project, each concept maps to exactly one term. This is the most visible dimension and the easiest to audit with grep.

**Syntactic consistency (same structure for same action):** Instructions of the same type share the same grammatical template. For example, all setup steps start with an imperative verb and end with a purpose clause: "Install the package to add the CLI tool." Do not switch to passive voice or conditional mood for some steps.

**Semantic consistency (same meaning for same term across boundaries):** A term must carry the same meaning across all files, modules, and documentation types in the project. If "build" means "compile and link" in the README, it must not mean "compile, link, and package" in the CI docs.

## Paradigm-Specific Guidance

### Object-Oriented (Java, C++, C#, Python classes)

In OO documentation, consistency is critical for inheritance chains. When you document a class hierarchy, use the same phrasing for overridden methods. If the base class `connect()` docstring says "Establishes a connection to the remote host," every subclass `connect()` docstring must reuse the same template, adding only the subclass-specific behavior:

> **Non-STE:** Base: "Connects to server." Subclass: "Opens a socket to the backend." Sub-subclass: "Initiates TCP handshake with data node."
>
> **STE:** Base: "Establishes a connection to the remote host." Subclass: "Establishes a connection to the remote host, with TLS encryption." Sub-subclass: "Establishes a connection to the remote host, with mTLS and certificate pinning."
>
> *Principles applied: P3, P13 — using "establishes a connection" consistently; avoiding noun-as-verb "opens a socket."*

Class and interface names must not be abbreviated inconsistently. If you introduce `UserRepository`, do not later refer to it as `UserRepo` or `the user repo` in prose.

### Functional (Haskell, Elixir, Clojure, Rust with functional style)

Functional documentation describes transformations, not state changes. Maintain consistent terminology for the transformation pattern. If one pure function is described as "returns a new value," all pure functions must use the same phrase. Do not describe some pure functions as "produces a result" and others as "yields output."

For monadic or effectful code, pick one metaphor and stay with it. If you describe `IO` as "a description of an effect," do not later call it "a computation" or "an action."

> **Non-STE:** `map` docstring: "Applies a function to each element and returns a new list." `filter` docstring: "Selects elements matching a predicate, producing a fresh collection."
>
> **STE:** `map` docstring: "Returns a new list with the function applied to each element." `filter` docstring: "Returns a new list with only the elements that satisfy the predicate."
>
> *Principles applied: P3, P11 — "returns a new list" is the consistent anchor phrase; one term ("satisfy") replaces "matching."*

### Procedural (C, Go, Bash)

Procedural code documents sequences of steps. Consistency here means step structures are predictable. If step 3 says "Write the buffer to the file descriptor," step 5 must not say "Output the data to the fd." The reader should see the same verb-noun pattern on every I/O step.

In Go, error handling is idiomatic and repetitive. All error-checking documentation must use the same pattern. Do not describe `if err != nil` as "check for an error" in one place and "handle the error condition" in another.

> **Non-STE:** "Check the return code. If it is non-zero, abort." vs. "Verify the exit status. On failure, terminate."
>
> **STE:** "Check the return code. If the return code is not 0, stop the program." (every occurrence)
>
> *Principles applied: P11, P1 — "check" over "verify," "return code" over "exit status," "stop" over "abort"/"terminate."*

### Declarative (SQL, Terraform, Kubernetes YAML, Docker Compose)

Declarative documentation describes desired state, not imperative steps. Use the same declarative phrasing for the same resource type. In Terraform docs, if `aws_instance` is described as "a virtual machine in AWS EC2," every reference must use that phrase — do not alternate with "EC2 instance," "AWS VM," or "cloud server."

In Kubernetes documentation, resource names are proper nouns. Use `ConfigMap` (the Kubernetes resource name) consistently. Do not write "config map," "configmap," or "configuration map" in prose.

> **Non-STE:** "Create a ConfigMap to store settings. Mount the config map into the pod. The configuration map provides env vars."
>
> **STE:** "Create a ConfigMap to store settings. Mount the ConfigMap into the Pod. The ConfigMap provides environment variables."
>
> *Principles applied: P5, P11 — `ConfigMap` and `Pod` are technical code nouns used consistently; no abbreviation of "environment variables."*

### Systems (Rust ownership docs, C memory docs, assembly-level docs)

Systems documentation describes guarantees, invariants, and safety conditions. Consistency here is a safety property — inconsistent terminology about ownership or memory can cause the reader to violate an invariant.

In Rust, "ownership," "borrow," and "lifetime" are terms of art with precise meanings. Never substitute synonyms. "The value is moved" is not "the value is transferred" — "moved" has a specific compiler-enforced meaning.

> **Non-STE:** "The function takes possession of the buffer. The caller relinquishes control. After the call, the caller cannot access the memory region."
>
> **STE:** "The function takes ownership of the buffer. The function moves the buffer. After the move, the caller cannot use the buffer."
>
> *Principles applied: P3, P11 — "ownership" and "move" are the canonical Rust terms; "takes possession" and "relinquishes control" break consistency with the Rust Reference.*

## Extended Examples

### Example 1: Verb Consistency in Setup Instructions

> **Non-STE:** Install the dependencies. Then fetch the source code. After that, you need to set up the environment. Finally, get the database running.
>
> **STE:** Install the dependencies. Then download the source code. After that, set the environment variables. Finally, start the database.
>
> *Principles applied: P1, P2, P11 — each action uses one approved verb consistently across the procedure; "fetch" is replaced by "download" (canonical synonym table). "Set up" is split into "set" + object. "Get ... running" is replaced by "start."*

### Example 2: Noun Consistency Across Documentation Types

> **Non-STE:** README: "This library provides authentication utilities." API docs: "The auth package handles login." Error message: "Authentication module failed to initialize."
>
> **STE:** README: "This library provides authentication." API docs: "The authentication library handles login." Error message: "The authentication library failed to initialize."
>
> *Principles applied: P11, P1 — "authentication library" is the only term for the artifact; "auth" is not used as an abbreviation; "module" and "package" are not mixed with "library."*

### Example 3: Structural Consistency in API Reference

> **Non-STE:**
> - `GET /items` — Retrieves all items.
> - `POST /items` — Use this to create a new item.
> - `GET /items/:id` — Gets item by ID.
> - `DELETE /items/:id` — Removes the specified item.
>
> **STE:**
> - `GET /items` — Returns all items.
> - `POST /items` — Creates a new item.
> - `GET /items/:id` — Returns the item with the specified ID.
> - `DELETE /items/:id` — Removes the item with the specified ID.
>
> *Principles applied: P11, P4 — every endpoint description starts with a third-person singular verb; "retrieves" and "gets" are unified to "returns"; the `:id` description is identical across endpoints.*

### Example 4: Commit Message Convention Consistency

> **Non-STE:**
> ```
> 12a7b3 Add user login endpoint
> 8f2c41 Introduce rate limiting
> d4e901 Insert health check route
> 77b3f2 Create logout handler
> ```
>
> **STE:**
> ```
> 12a7b3 Add user login endpoint
> 8f2c41 Add rate limiting middleware
> d4e901 Add health check route
> 77b3f2 Add logout handler
> ```
>
> *Principles applied: P11, P1 — "Add" is the single imperative verb for new features; "Introduce," "Insert," and "Create" are removed. P11: one term per concept.*

### Example 5: Error Message Consistency Across a Service

> **Non-STE:**
> - Service A: "Connection refused by peer"
> - Service B: "Cannot establish link to remote"
> - Service C: "Failed to connect to upstream server"
>
> **STE:**
> - Service A: "Cannot connect to the remote host"
> - Service B: "Cannot connect to the remote host"
> - Service C: "Cannot connect to the remote host"
>
> *Principles applied: P11, P1 — identical error text for the same failure mode; "refused," "establish link," and "failed to connect" all collapse to "cannot connect"; "peer," "remote," and "upstream server" all collapse to "remote host."*

### Example 6: CLI Flag Documentation Consistency

> **Non-STE:**
> `--verbose` — Enable verbose output
> `--quiet` — Suppress all logging
> `--debug` — Turns on debug-level messages
>
> **STE:**
> `--verbose` — Enables verbose output
> `--quiet` — Disables all output
> `--debug` — Enables debug output
>
> *Principles applied: P11, P4 — each flag description uses the same grammatical template: "Enables/Disables [adjective] output"; "Suppress" and "Turns on" are replaced; "logging"/"messages" unified to "output."*

## Edge Cases

### Edge Case 1: Framework-Mandated Terminology

Some frameworks enforce specific terminology that conflicts with STE-Code preferences. For example, React uses "props" (not "properties") and "hooks" (a term STE-Code might prefer to avoid because "hook" can also mean a network hook or a system hook). When the framework is the authority, use the framework term consistently — do not translate it to an STE-Code synonym. The consistency rule defers to the framework: use "props" everywhere, never alternating with "properties" or "arguments."

> **Non-STE:** "Pass properties to the component via its props. The component receives these arguments and renders accordingly."
>
> **STE:** "Pass props to the component. The component receives the props and renders the output."
>
> *Principles applied: P5, P11 — "props" is a technical code noun and the canonical React term; do not translate it.*

### Edge Case 2: Generated Documentation

Generated API docs (Javadoc, Sphinx, rustdoc) often insert boilerplate text from code structure. If the generator produces inconsistent phrasing between methods, fix the source docstrings rather than post-processing the output. Consistency must be authored, not patched.

For auto-generated changelogs (from conventional commits), define a commit message convention document that enforces the allowed verbs. If the generator encounters a commit with a non-standard verb, the CI pipeline must reject the commit rather than emit inconsistent output.

### Edge Case 3: Cross-Project Documentation (Monorepos and Multi-Service Systems)

In a monorepo or multi-service system, different teams may own different services. Each service's documentation must use internally consistent terminology, but the system-level documentation (architecture docs, onboarding guides) must reconcile the differences. The rule: per-service docs follow the service's glossary; system-level docs define a system-wide glossary that may differ from individual service conventions. The system glossary must map each system-level term to the corresponding service-level term.

### Edge Case 4: Domain-Specific Terms with Multiple Valid Names

Some tools have multiple widely-used names. For example, "GitHub Actions workflow" is also called a "GitHub Actions pipeline" in some communities. When a concept has multiple names in the industry, pick one for your documentation and use it exclusively. Document the choice in the project glossary. Do not alternate for variety — variety is the enemy of clarity.

### Edge Case 5: Version-Specific Terminology Changes

When a project renames a feature across versions (e.g., "workspaces" became "packages" in one version and back to "workspaces" in another), the documentation for each version must use that version's canonical name. However, migration guides must explicitly state the rename: "In version 2.0, 'packages' are called 'workspaces.' This document uses 'workspaces' unless referring to version 1.x behavior."

## Grammar Notes

### The Cognitive Load of Synonymy

In technical documentation, every synonym forces the reader to perform a set membership test: "Is X the same thing as Y?" This test takes cognitive resources that should be spent on understanding the content. The original ASD-STE100 rule 9.4 is grounded in the observation that aerospace maintenance errors often trace back to a technician misidentifying a component because the manual used two different names. The same hazard exists in code documentation: a developer who misidentifies a configuration parameter because the docs call it "retry count" in one section and "max attempts" in another introduces a runtime bug.

### Structural Parallelism

When instructions follow a predictable grammatical pattern, the reader can scan for the action verb and skip the scaffolding. Inconsistent structures force the reader to parse every sentence fully. This is why all installation steps should share the same template, all configuration steps should share the same template, and all verification steps should share the same template. The template itself signals the step type before the reader processes the content.

### The "Term Drift" Problem

Terminology drifts when a document is maintained over time by multiple authors. Author A writes "configuration file." Author B, six months later, writes "config file" without checking the existing text. Author C writes "settings file." The result is a document with three names for one thing. Rule 9.4 requires active maintenance: when you add content to an existing document, search the document for the terms you plan to use and match the existing convention even if you prefer a different term.

### Cross-Language Consistency

When a project has documentation in multiple programming languages (e.g., a Python SDK with a TypeScript port), consistency must cross language boundaries. The Python `connect()` and TypeScript `connect()` must use the same description template. The reader who learns the Python SDK must not need to re-learn the terminology for the TypeScript SDK.

## Cross-References

### Rules That Support Rule 9.4

- **Rule 1.1 (Approved Words):** Consistency depends on choosing from the approved dictionary. You cannot be consistent if you alternate between approved and unapproved words for the same concept.
- **Rule 1.3 (Approved Meanings):** Each approved word has exactly one approved meaning. Consistent terminology requires consistent semantics — you cannot use "set" to mean "configure" in one place and "collection" in another.
- **Rule 1.11 (One Term Per Concept):** This is the lexical foundation of Rule 9.4. Rule 1.11 governs word choice; Rule 9.4 governs usage across an entire document.
- **Rule 1.5 (Technical Nouns):** Technical nouns (framework names, tool names, language keywords) are exempt from the dictionary but not from consistency. Rule 9.4 applies to technical nouns with the same force as approved words.
- **Rule 9.1 (Different Sentence Construction):** When a synonym substitution would break consistency, Rule 9.1 provides the escape hatch — restructure the sentence rather than introduce a synonym.
- **Rule 9.2 (Correct Usage):** Consistency in wording depends on using each word correctly. A word used incorrectly in one place breaks the consistency chain even if the same word is used elsewhere.

### STE-Code Dictionary Entries

The canonical synonym table (see the STE-Code specification, Section 1) lists the preferred term for each concept. Rule 9.4 requires that once you select the preferred term, you use it in every occurrence. The synonym table is the starting point; consistency is the discipline that sustains it.

Key entries most affected by Rule 9.4:
- **use** (not utilize, leverage, employ)
- **start** (not initiate, commence, bootstrap)
- **show** (not display, render, present)
- **make** (not create, generate, produce)
- **get** (not retrieve, fetch, obtain)
- **set** (not configure, assign, establish)
- **check** (not verify, validate, ensure)
- **remove** (not delete, eliminate, purge)
- **keep** (not retain, preserve, maintain)
- **send** (not transmit, dispatch, forward)

For each entry, pick the preferred term and use it in every sentence that expresses that concept. Do not use "use" in paragraph 1 and "utilize" in paragraph 3 for variation. Variation in technical documentation is a defect, not a stylistic virtue.
