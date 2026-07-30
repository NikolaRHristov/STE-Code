# Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.1

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

> **Non-STE:** Utilize the build tool to generate the artifact. Execute the binary to bootstrap the service. Utilize environment variables to configure runtime behavior.
>
> **STE:** Use the build tool to make the binary. Run the binary to start the service. Use environment variables to set the runtime behavior.
> *(P1 applied: "utilize" → "use"; "generate" → "make"; "execute" → "run"; "bootstrap" → "start"; "configure" → "set")*

### API Documentation

API documentation describes functions, methods, endpoints, and their inputs and outputs. The technical nouns (function names, parameter names, type names, endpoint paths) are code-domain technical nouns covered by Rule 1.5. The descriptive prose that surrounds them must use approved words.

Return value descriptions, parameter explanations, and error condition notes must follow Rule 1.1. Use "get" instead of "retrieve" or "fetch." Use "send" instead of "transmit." Use "remove" instead of "delete" or "purge." Use "check" instead of "validate" or "verify."

Example — JSDoc parameter description:

> **Non-STE:** @param {number} timeout — The duration in milliseconds the client shall await a response prior to terminating the connection attempt.
>
> **STE:** @param {number} timeout — The time in milliseconds that the client waits for a response before it stops the connection.
> *(P1 applied: "duration" → "time"; "shall await" → "waits"; "prior to" → "before"; "terminating" → "stops")*

### Docstrings and Inline Comments

Docstrings and inline comments are written for developers who read the source code. They must be concise and unambiguous. Rule 1.1 prevents the use of casual or imprecise vocabulary that could confuse readers from different language backgrounds.

For docstrings, prefer approved verbs: "do" instead of "perform," "check" instead of "ensure," "make" instead of "construct." For inline comments, use the shortest approved word available: "NOTE:" (approved noun) for important information, "WARNING:" (approved noun) for cautionary notes, and "FIXME:" as a code-domain technical noun for known issues.

Example — Python docstring:

> **Non-STE:** Perform validation on the input data to ensure it conforms to the expected schema. Returns a boolean indicating whether the data is valid.
>
> **STE:** Check the input data against the schema. Gives `true` when the data is correct and `false` when the data is not correct.
> *(P1 applied: "perform" → "do"; "validation" restructured to "check"; "ensure" → "when"; "conforms to" → "against"; "indicating whether" restructured)*

### Commit Messages

Commit messages are the most constrained form of code documentation. They have a conventional format (type: description) and a character limit. Rule 1.1 forces commit messages to use the smallest possible approved vocabulary.

Use approved imperative verbs: "add," "fix," "remove," "update," "set," "make," "check," "run." These are all approved in the controlled terminology. Do not use "implement" (not approved; use "make" or "add"), "refactor" (code-domain technical verb, acceptable per Rule 1.12), or "optimize" (not approved; use "make faster" or "make smaller").

Example — conventional commit:

> **Non-STE:** feat: implement JWT authentication middleware for API routes
>
> **STE:** feat: add JWT authentication middleware for API routes
> *(P1 applied: "implement" → "add")*

> **Non-STE:** perf: optimize database query performance in user listing endpoint
>
> **STE:** perf: make the database query faster in the user listing endpoint
> *(P1 applied: "optimize" → "make faster"; "performance" removed as redundant)*

### Error Messages

Error messages are read by end users and developers. They must use approved words to be clear to non-native English speakers. Do not use jargon, slang, or domain-specific abbreviations unless they are code-domain technical nouns.

Use "cannot" (approved) instead of "unable to" (not approved). Use "incorrect" (approved adjective) instead of "invalid" or "malformed." Use "N/A" or "N/A" only when it is a code-domain technical noun for a missing value.

Example — CLI error message:

> **Non-STE:** Error: Unable to establish connection to the database. Please verify your credentials and retry.
>
> **STE:** Error: Cannot connect to the database. Check your credentials and try again.
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

> **Non-STE:** The `UserRepository` class is responsible for persisting and retrieving `User` entities from the database. It leverages an ORM to abstract away the underlying SQL queries.
>
> **STE:** The `UserRepository` class keeps `User` records in the database and gets `User` records from the database. It uses an ORM to hide the SQL queries.
> *(P1 applied: "persisting" → "keeps"; "retrieving" → "gets"; "leverages" → "uses"; "abstract away" → "hide")*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional documentation uses terms like "pure function," "immutable," "monad," "closure," and "higher-order function" as code-domain technical nouns. These are permitted under Rule 1.5 and Rule 1.6. The functional paradigm reuses some approved words with special meanings — for example, "apply" is an approved verb in STE but in functional programming it also refers to the act of giving arguments to a function.

**Guidance points for functional documentation:**

- "Apply" as a verb meaning "put something on something" is approved. The functional-programming sense of "apply a function to arguments" is a code-domain technical verb and is permitted under Rule 1.12. Both uses are valid under Rule 1.1.
- "Map" as a noun (the `map` data structure or the `map` higher-order function) is a code-domain technical noun. "Map" as a verb (to transform each element of a collection) is a code-domain technical verb. Both are permitted.
- "Fold," "reduce," "filter," "compose," and "curry" are code-domain technical verbs. They are not in the approved word list but are permitted under Rule 1.12.
- "Pure" as an adjective meaning "not mixed with anything" is approved. The functional-programming sense of "pure function" (no side effects) is a compound code-domain technical noun. Both uses are valid.

Example — module documentation:

> **Non-STE:** This module furnishes a collection of pure utility functions for transforming and combining data structures in a declarative fashion.
>
> **STE:** This module gives a set of pure utility functions for changing and joining data structures.
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

> **Non-STE:** Allocate a buffer of the specified size on the heap. The caller is responsible for deallocating the buffer when it is no longer needed.
>
> **STE:** Make a buffer of the given size on the heap. The caller must free the buffer when the buffer is no longer necessary.
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

> **Non-STE:** This module provisions an auto-scaling group with a launch template. It orchestrates the deployment of EC2 instances across multiple availability zones to ensure high availability.
>
> **STE:** This module makes an auto-scaling group with a launch template. It controls the deployment of EC2 instances across many availability zones to give high availability.
> *(P1 applied: "provisions" → "makes"; "orchestrates" → "controls"; "multiple" → "many"; "ensure" → "give")*

### Systems (Rust Ownership, C Memory Management)

Systems documentation explains ownership, lifetimes, memory layout, and concurrency. These concepts have dense technical vocabularies. Rule 1.1 requires that the framing prose around these technical terms uses approved words, even when the technical terms themselves are domain-specific.

**Guidance points for systems documentation:**

- "Own," "borrow," and "move" are code-domain technical verbs in Rust and are permitted under Rule 1.12. Their standard English meanings are different from their Rust meanings, but this is acceptable because they are technical terms.
- "Allocate" and "deallocate" are not approved verbs. Use the code-domain technical verbs "allocate" (when describing memory operations precisely) or restructure to use "make" and "free" in general prose.
- "Dangle" (as in "dangling pointer") is not an approved word. Use "dangling pointer" as a compound code-domain technical noun (category 15, defects and errors).
- "Undefined behavior" is a compound code-domain technical noun (category 15).

Example — Rust documentation:

> **Non-STE:** The borrow checker ensures that references do not outlive the data they refer to, preventing dangling pointers and use-after-free bugs at compile time.
>
> **STE:** The borrow checker makes sure that references do not live longer than the data they point to. This prevents dangling pointers and use-after-free defects at compile time.
> *(P1 applied: "ensures" → "makes sure"; "outlive" → "live longer than"; "bugs" → "defects")*

---

## Extended Examples

Each example pair below shows a real code documentation scenario, the STE-Code compliant rewrite, which principle was applied, and an explanation of the fix.

### Example 1 — API Reference: Return Value Description

> **Non-STE:** Returns a promise that resolves to an array of User objects, or rejects with an ApiError if the request fails.
>
> **STE:** Gives a `Promise` that completes with a list of `User` objects. If the request does not complete, the `Promise` gives an `ApiError`.
>
> **Principle applied:** P1 (use approved words: "resolve" → "complete," "reject" → "gives an error")
> **Explanation:** "Resolve" and "reject" are Promise-specific technical verbs. In prose, they are replaced with the approved verb "complete" and the approved construction "gives an error." The technical nouns `Promise`, `User`, and `ApiError` are code-domain technical nouns and remain unchanged. The structure is split into two sentences to keep each sentence under 25 words (descriptive limit).

### Example 2 — README: Feature Description

> **Non-STE:** The application leverages machine learning algorithms to analyze user behavior patterns and generate personalized recommendations in real time.
>
> **STE:** The application uses machine learning to examine user behavior and make personal recommendations immediately.
>
> **Principle applied:** P1 (use approved words: "leverage" → "use," "analyze" → "examine," "generate" → "make," "personalized" → "personal"); P9 (prefer short technical nouns: "algorithms" removed as redundant next to "machine learning"); P8 (use standard technical nouns: "real time" → "immediately")
> **Explanation:** "Leverage" is a banned word under P1. "Analyze" is not in the approved verb list; "examine" is approved and has the same meaning in this context. "Patterns" and "algorithms" add no information that "machine learning" does not already carry. "Real time" is replaced with "immediately," an approved adverb. The sentence structure is simplified to one clause.

### Example 3 — Docstring: Function Purpose

> **Non-STE:** /**
>  * Validates the provided configuration object against the schema
>  * and populates default values for any missing fields.
>  *
>  * @param {Object} config - The configuration object to validate.
>  * @returns {Object} The validated and populated configuration.
>  * @throws {ValidationError} If the configuration is invalid.
>  */
> **STE:** /**
>  * Checks the given configuration object against the schema
>  * and adds default values for all missing fields.
>  *
>  * @param {Object} config - The configuration object to check.
>  * @returns {Object} The checked configuration with defaults.
>  * @throws {ValidationError} If the configuration is not correct.
>  */
>
> **Principle applied:** P1 (use approved words: "validate" → "check," "provided" → "given," "populate" → "add," "any" → "all," "invalid" → "not correct"); P6 (non-approved word used as technical noun: "ValidationError" is a code-domain technical noun)
> **Explanation:** "Validate" is not an approved verb; "check" is the approved alternative with the same meaning. "Populate" is replaced with "add," which is simpler and approved. "Invalid" is not an approved adjective; "not correct" uses the approved adjective "correct" with the approved negation "not." The technical noun `ValidationError` is a code-domain technical noun and remains unchanged.

### Example 4 — Error Message: User-Facing

> **Non-STE:** Unable to process your request at this time. Please verify your input and try again. If the problem persists, contact support.
>
> **STE:** Cannot process your request now. Check your input and try again. If the problem continues, speak to support.
>
> **Principle applied:** P1 (use approved words: "unable to" → "cannot," "at this time" → "now," "verify" → "check," "persists" → "continues," "contact" → "speak to")
> **Explanation:** "Unable to" is not approved; "cannot" is the approved modal verb. "Verify" is not an approved verb in this context; "check" is approved. "Persist" is not approved; "continue" is approved. "Contact" as a verb is not approved; "speak to" uses the approved verb "speak."

### Example 5 — Commit Message: Bug Fix

> **Non-STE:** fix: rectify race condition in connection pool that caused intermittent failures under load
>
> **STE:** fix: correct race condition in connection pool that caused failures under load
>
> **Principle applied:** P1 (use approved words: "rectify" → "correct"); P9 (prefer short terms: "intermittent" removed as unnecessary — the fix implies it was intermittent)
> **Explanation:** "Rectify" is not an approved verb; "correct" is approved (as both adjective and verb). "Intermittent" is not needed in a commit message because the fix itself implies the problem was intermittent. "Race condition" and "connection pool" are code-domain technical nouns and remain unchanged.

### Example 6 — Configuration File Comment

> **Non-STE:** # This parameter dictates the maximum quantity of concurrent connections
> # the server shall entertain before commencing to reject additional requests.
> **STE:** # This parameter sets the largest number of connections that the server
> # accepts at the same time. When the server has this many connections,
> # it refuses new requests.
>
> **Principle applied:** P1 (use approved words: "dictates" → "sets," "quantity" → "number," "concurrent" → "at the same time," "shall entertain" → "accepts," "commencing" → removed, "reject" → "refuses," "additional" → "new"); P9 (prefer short terms); anti-pattern: no semicolons, no "-ing" as main verb in procedure
> **Explanation:** This example shows many violations at once. "Dictate" is replaced with "set." "Shall entertain" is a double violation — "shall" is not approved in descriptive writing and "entertain" is not the approved meaning. The entire sentence is restructured into two shorter sentences that use approved verbs ("sets," "accepts," "refuses") and approved constructions.

---

## Edge Cases

The following scenarios show where the boundary between approved words, technical nouns, and technical verbs requires careful judgment.

### Edge Case 1: Framework Name That Is Also an Unapproved Word

**Scenario:** A popular framework uses a name that is not an approved word in the STE-Code controlled terminology. For example, "Express" (the Node.js web framework) or "FastAPI" (the Python framework).

**Guidance:** Framework names are code-domain technical nouns (category 3, development tools and environments) and are permitted under Rule 1.5. The fact that "express" as a verb is not approved does not affect the use of "Express" as a proper noun. Always write the framework name with its correct capitalization and treat it as a technical noun.

> **Non-STE:** Express your API using Express's routing capabilities.
>
> **STE:** Use Express routing to make your API endpoints.
>
> In the first sentence, "Express" as a verb (meaning "to show or state") conflicts with the framework name. The second sentence uses "Express" only as a technical noun and uses the approved verb "use" for the action.

### Edge Case 2: Code Keyword That Conflicts with the Rule

**Scenario:** A programming language keyword is identical to an unapproved word. For example, `yield` is a keyword in Python and JavaScript but "yield" is not an approved verb in STE-Code (its approved alternative is "give").

**Guidance:** When the keyword appears in a code block, it is quoted text (Rule 1.5, category 10) and does not need to follow Rule 1.1. When the keyword appears in prose documentation, treat it as a code-domain technical noun (use backticks: `` `yield` ``). If you must describe what `yield` does, use the approved verb "give" in the prose and mark the keyword with backticks.

> **Non-STE:** The `yield` keyword yields control back to the caller.
>
> **STE:** The `yield` keyword gives control back to the caller.
>
> `` `yield` `` is a code-domain technical noun. "Gives" is the approved verb that replaces the unapproved "yields" in the prose.

### Edge Case 3: Generated Code Documentation

**Scenario:** Auto-generated API documentation (for example, from OpenAPI specs, JSDoc, or Sphinx) produces text that does not follow Rule 1.1.

**Guidance:** Rule 1.1 applies to documentation that a human writes or reviews. Generated documentation is exempt when the generation tool does not support STE-Code. But when you write the source annotations that feed the generator (docstrings, JSDoc comments, OpenAPI descriptions), those source texts must follow Rule 1.1. The generated output inherits the quality of the source text.

**Recommendation:** Write STE-Code compliant source annotations. The generated documentation will be cleaner even if the generator adds non-STE boilerplate. For critical public-facing API docs, post-process the generated output to replace non-approved words.

### Edge Case 4: Technical Verb Used as a Noun in a Compound Term

**Scenario:** A code-domain technical verb like "build" appears as a noun in a compound term like "build system" or "build pipeline."

**Guidance:** Rule 1.13 states that you must not use technical verbs as nouns. But when a technical verb is part of a compound code-domain technical noun, the compound as a whole is a noun. "Build system" is a code-domain technical noun (category 3, development tools). The word "build" inside the compound is not functioning as a standalone noun — it is part of a recognized technical term. This is permitted under Rule 1.5 and Rule 1.6.

> **Non-STE:** The build took 45 minutes to complete.
>
> **STE:** The build procedure took 45 minutes.
>
> "Build" used alone as a noun violates Rule 1.13. Adding "procedure" makes it a compound technical noun that is acceptable. Alternatively, restructure: "The system built in 45 minutes."

### Edge Case 5: Non-English Words and Loanwords

**Scenario:** Code documentation sometimes includes non-English words that have become standard in the domain (for example, "rendezvous" in networking, "de facto" in standards discussions, "naïve" in algorithm names like "naïve Bayes").

**Guidance:** These words are code-domain technical nouns when they name a specific algorithm, protocol, or pattern. "Rendezvous" as part of "rendezvous protocol" is a technical noun. "Naïve Bayes" is a technical noun. When used outside of a technical term, replace with an approved English word. "De facto" in prose should be replaced with "usual" or "primary."

> **Non-STE:** This is the de facto standard for serialization in the ecosystem.
>
> **STE:** This is the usual standard for serialization in the ecosystem.
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

**Categories reference:** See `a-categories.md` for the 22 code-domain technical noun categories defined under Rule 1.5.

---

## Grammar Notes

### The Three-Gate Model

Rule 1.1 establishes a three-gate model for vocabulary selection in code documentation. Every word in a sentence must pass through one of three gates:

1. **Gate 1 — Approved Word:** The word is listed as APPROVED in the STE-Code controlled terminology. It must be used with its specified part of speech (Rule 1.2) and its approved meaning (Rule 1.3). This is the default gate for all general-purpose vocabulary.

2. **Gate 2 — Code-Domain Technical Noun:** The word is not in the controlled terminology (or is listed as UNAPPROVED) but fits into one of the 22 code-domain technical noun categories (Rule 1.5). It names a specific concept, component, tool, or entity in the software domain. A word that passes through Gate 2 must not be used as a verb (Rule 1.7).

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
