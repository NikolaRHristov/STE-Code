# Rule 3.7 — Use an Approved Verb to Describe an Action, Not a Noun or Other Parts of Speech

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.7

## Original Rule

Use an approved verb to describe an action, not a noun or other parts of speech.

There can be different solutions to give the same information in STE. If there is an approved verb that describes an action, use the approved verb. Verbs describe actions more clearly than nouns or other parts of speech.

Examples:

> **Do not write:** The ohmmeter gives an indication of 450 ohms.
> **WRITE:** The ohmmeter shows 450 ohms.

In the examples, all sentences are in STE but those with direct verbs describe the action more clearly.

If a word is not approved as a verb in the dictionary, do not use it as a verb. Use a different sentence construction to give the same information.

Example:

> **Non-STE:** Check the laptop battery.
>
> **STE:** Do a check of the laptop battery.

## STE-Code Adaptation

Use an approved verb from the STE-Code vocabulary to describe an action directly. Do not use a noun or another part of speech to describe an action when an approved verb exists. Direct verbs make documentation clearer than noun-based constructions.

When you write code documentation, look for verb-avoiding constructions that use nouns to carry the action. Replace them with the approved verb. The canonical synonym table in the STE-Code vocabulary lists the preferred verb for each action.

If a word is not approved as a verb in the STE-Code vocabulary, do not use it as a verb. Instead, restructure the sentence to use an approved verb, or pair the non-approved verb as a noun with an approved support verb such as "do" or "run."

### Examples

> **Non-STE:** The linter gives an indication of three errors.
>
> **STE:** The linter shows three errors.
>
> *Adapted from spec pair: "The ohmmeter gives an indication of 450 ohms." / "The ohmmeter shows 450 ohms."*

> **Non-STE:** The debugger performs an analysis of the memory allocation pattern.
>
> **STE:** The debugger analyzes the memory allocation pattern.
>
> *Additional code-domain example — no direct spec pair*

> **Non-STE:** Benchmark the application to measure the response time.
>
> **STE:** Do a benchmark of the application to measure the response time.
>
> *Adapted from spec pair: "Check the laptop battery." / "Do a check of the laptop battery."*

> **Non-STE:** The function does the initialization of the database connection.
>
> **STE:** The function initializes the database connection.
>
> *Additional code-domain example — no direct spec pair*

---

## Code-Domain Explanation

Rule 3.7 requires that every action in code documentation is carried by an approved verb. This rule targets two related problems: nominalization (using a noun where a verb is clearer) and verbing (using a non-verb word as if it were a verb). Each documentation type has characteristic violations and remedies.

### README Files

README files mix procedural instructions (imperative mood) with descriptive sections (simple present). Rule 3.7 violations in README files fall into two patterns. The first pattern is nominalization: using a noun phrase to carry an action that an approved verb can carry directly. "The build process performs the compilation of all source files" buries the action in the noun "compilation." The approved verb "compiles" makes the sentence direct: "The build process compiles all source files."

The second pattern is verbing a code-domain noun that is not approved as a verb. "Dockerize the application" uses "Dockerize" as a verb. The noun "Docker" is a technical noun (Rule 1.5) but not an approved verb. Restructure with a support verb: "Put the application in a Docker container."

In README installation sections, the "do/run + noun" pattern is especially common and often correct when the noun names a process or tool that has no approved verb: "Run the build" (BUILD is a technical noun), "Do a test of the endpoint" (TEST is a technical noun when "test" is not approved as a verb).

> **Non-STE:** Dockerize the application and perform the deployment to the cluster.
>
> **STE:** Put the application in a Docker container and deploy it to the cluster.
> *(Rule 3.7 applied: "Dockerize" is verbing a technical noun — use support construction. "Perform the deployment" is nominalization — use the approved verb "deploy.")*

### API Documentation

API documentation describes what functions do. Every function description needs a verb. Rule 3.7 violations in API docs typically use "performs," "does," or "carries out" plus a noun instead of a direct verb. "The `validateInput` function performs validation of the user input" wastes words. "The `validateInput` function validates the user input" uses the direct verb.

API documentation also suffers from the reverse problem: using an approved verb where the API method name is a noun. If the method is called `getUser()`, the documentation should not say "This method users the database" because "user" is a noun, not a verb. Instead: "This method gets the user from the database."

When an API endpoint name contains a noun that describes an action (e.g., `POST /api/verification`), the documentation must supply an approved verb: "Send a verification request" not "Verification the data."

> **Non-STE:** POST /api/validation — Performs validation of the input payload and returns a validation result.
>
> **STE:** POST /api/validation — Validates the input payload and gives a result.
> *(Rule 3.7 applied: "Performs validation" → "Validates" (direct verb). "Returns" → "gives" per P1 synonym table. "Validation result" is a noun — restructure with the approved verb.)*

### Docstrings and Inline Comments

Docstrings use the imperative mood for the first line. The imperative mood naturally favors direct verbs. A Rule 3.7 violation in a docstring occurs when the first line uses a noun instead of a verb: "Configuration of the database connection parameters" is a noun phrase. The correct form is "Configure the database connection parameters."

Inline comments have limited space. Every word counts. Nominalization wastes words and obscures the action. "// Performs the calculation of the hash value for the input string" can be "// Calculates the hash of the input." The direct verb "calculates" replaces three words ("the calculation of").

When inline comments describe what a block of code does, use the third-person singular form of an approved verb: "Builds," "Checks," "Sets," "Gets," "Sends," "Writes." Avoid: "Does a build of," "Does a check of," "Does a set of."

> **Non-STE:** /** Performs the initialization of the connection pool and does a verification of the credentials. */
>
> **STE:** /** Initializes the connection pool and verifies the credentials. */
> *(Rule 3.7 applied: "Performs the initialization" → "Initializes." "Does a verification" → "verifies.")*

### Commit Messages

Commit messages use the imperative mood and the subject line is typically 50-72 characters. Rule 3.7 violations in commit messages waste characters on nominalization when an approved verb is shorter. "Perform the update of the dependency versions" uses 41 characters. "Update the dependency versions" uses 29 characters.

Commit messages also verb code-domain nouns: "Hotfix the production issue" uses "hotfix" as a verb. The correct form uses an approved support verb: "Apply a hotfix for the production issue."

> **Non-STE:** Perform the removal of the deprecated API and do a refactor of the controller.
>
> **STE:** Remove the deprecated API and refactor the controller.
> *(Rule 3.7 applied: "Perform the removal" → "Remove." "Do a refactor" → "refactor." REFACTOR is a code-domain technical verb under Rule 1.12.)*

### Error Messages

Error messages report what happened. They must be short and direct. A Rule 3.7 violation in an error message buries the action: "The system experienced a failure during the initialization of the database connection." The corrected form uses the direct verb: "The database connection failed to initialize."

Error messages also face the "verbing" problem when the error code or component name is a noun: "The service 500s on the health endpoint." "500" is an HTTP status code (noun), not a verb. Use: "The service gives a 500 status on the health endpoint."

> **Non-STE:** ERROR: The connection pool experienced a timeout during the establishment of the database connection.
>
> **STE:** ERROR: The connection pool timed out during the database connection.
> *(Rule 3.7 applied: "Experienced a timeout" → "timed out" (TIMEOUT as phrasal verb, code-domain). "The establishment of" → remove and use direct verb construction.)*

---

## Paradigm-Specific Guidance

Rule 3.7 applies to all code documentation regardless of paradigm. Each paradigm introduces characteristic noun-heavy constructions that violate the rule.

### Object-Oriented (Java, C++, C#, Python Classes)

Object-oriented documentation describes classes, methods, and their interactions. The most common Rule 3.7 violation in OOP documentation is nominalization of method actions: "The `UserService` performs the creation of a new user record" instead of "The `UserService` creates a new user record."

Design pattern documentation is especially susceptible. Patterns are often described with nominalized verbs: "The Factory pattern enables the instantiation of objects" becomes "The Factory pattern creates objects."

When a class name is a noun (e.g., `Validator`, `Builder`, `Connector`), the documentation tends to mirror the noun form: "The Validator does the validation of the input." Use the approved verb: "The Validator validates the input." The class name is a technical noun (Rule 1.5). The approved verb that matches it carries the action.

> **Non-STE:** The `CacheManager` performs the invalidation of stale cache entries and does the re-population of the cache from the database.
>
> **STE:** The `CacheManager` invalidates stale cache entries and repopulates the cache from the database.
> *(Rule 3.7 applied: "Performs the invalidation" → "invalidates." "Does the re-population" → "repopulates.")*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure transformations. The simple present tense is the primary tense. Functional code documentation has fewer Rule 3.7 violations than OOP because functional style emphasizes verbs (functions) over nouns (objects). But nominalization still appears in descriptions of evaluation or reduction: "The `fold` function does the accumulation of values" becomes "The `fold` function accumulates values."

Functional documentation introduces domain-specific nouns like "monad," "functor," "applicative," and "transducer." These are technical nouns (Rule 1.5). Do not verb them: "The function monads the value" is incorrect. Use: "The function wraps the value in a monad."

> **Non-STE:** The `reduce` function performs the combination of elements using the given accumulator function.
>
> **STE:** The `reduce` function combines elements with the given accumulator function.
> *(Rule 3.7 applied: "Performs the combination" → "combines.")*

### Procedural (C, Go, Bash)

Procedural documentation describes step-by-step sequences. The imperative mood naturally resists nominalization because instructions demand direct verbs: "Compile the source," "Link the objects," "Run the binary." But procedural documentation still suffers from verbing code-domain nouns: "Makefile the project" uses "Makefile" as a verb. Use: "Build the project with Make."

In shell script documentation, pipeline descriptions tend toward nominalization: "The script does the extraction of the archive and does the installation of the binaries." Use direct verbs: "The script extracts the archive and installs the binaries."

C memory-management documentation is especially dense with nominalizations: "The function performs the allocation of memory on the heap" becomes "The function allocates memory on the heap." The approved verb "allocates" is shorter and clearer.

> **Non-STE:** Do the compilation of the source files, then do the linking of the object files, then do the execution of the binary.
>
> **STE:** Compile the source files, then link the object files, then run the binary.
> *(Rule 3.7 applied: "Do the compilation" → "Compile." "Do the linking" → "Link." "Do the execution" → "run" — P1 synonym table.)*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state. It uses the simple present tense for resource descriptions and the imperative mood for apply instructions. Nominalization is common in resource descriptions: "This resource performs the provisioning of a virtual machine" becomes "This resource provisions a virtual machine."

Kubernetes documentation describes controllers and operators. The tendency is to mirror the resource name in the documentation: "The Deployment does the management of Pod replicas" becomes "The Deployment manages Pod replicas."

Terraform documentation describes providers and resources. Nominalization appears in state descriptions: "The `aws_instance` resource handles the creation of an EC2 instance" becomes "The `aws_instance` resource creates an EC2 instance."

> **Non-STE:** The Ingress resource does the routing of external HTTP traffic to internal services.
>
> **STE:** The Ingress resource routes external HTTP traffic to internal services.
> *(Rule 3.7 applied: "Does the routing" → "routes." ROUTE is a code-domain technical verb under Rule 1.12.)*

### Systems (Rust Ownership, C Memory Management)

Systems documentation describes ownership, lifetimes, and memory layout. The density of technical nouns (borrow, ownership, lifetime, allocation, deallocation) makes nominalization a persistent risk. "The borrow checker performs the enforcement of the ownership rules" becomes "The borrow checker enforces the ownership rules."

In Rust documentation, the concept of "moving" ownership is an approved verb (MOVE). Do not nominalize it: "The assignment causes the movement of ownership" becomes "The assignment moves ownership."

In C documentation, pointer operations are described with verbs that are often nominalized: "The function does the dereferencing of the pointer" becomes "The function dereferences the pointer." DEREFERENCE is a code-domain technical verb under Rule 1.12.

> **Non-STE:** The compiler performs the analysis of the lifetime annotations and does the verification of the borrow rules.
>
> **STE:** The compiler analyzes the lifetime annotations and verifies the borrow rules.
> *(Rule 3.7 applied: "Performs the analysis" → "analyzes." "Does the verification" → "verifies.")*

---

## Extended Examples

Each example pair below shows a real code documentation scenario, the STE-Code compliant rewrite, which principle was applied, and an explanation of the fix.

### Example 5 — README: Project Setup Instructions

> **Non-STE:** To get started, perform the cloning of the repository to your local machine. After cloning, do the installation of the dependencies with npm. Then, execute the build of the project. Finally, do the start of the development server to verify the setup.
>
> **STE:** To start, clone the repository to your local machine. After you clone the repository, install the dependencies with npm. Then, build the project. Finally, start the development server to check the setup.
>
> **Principle applied:** Rule 3.7 (use approved verbs, not nouns: "perform the cloning" → "clone"; "do the installation" → "install"; "execute the build" → "build"; "do the start" → "start"); P1 (synonym table: "get started" → "start"; "verify" → "check").
> **Explanation:** Five nominalizations in a short README section. Each buries an approved verb inside a noun phrase with a light verb ("perform," "do," "execute"). The STE version uses the direct verbs: CLONE, INSTALL, BUILD, START, CHECK. These are all approved technical verbs under Rule 1.12. The phrase "do the start" is especially awkward — the verb START exists and is the direct choice. The synonym table in P1 prefers "check" over "verify" and "start" over "get started."

### Example 6 — API Reference: Endpoint Behavior

> **Non-STE:** GET /api/users/:id — Does the retrieval of a user record by its unique identifier. If the user does not exist, the endpoint provides a 404 status and gives the indication of a not-found error. The response body contains a JSON representation of the user object.
>
> **STE:** GET /api/users/:id — Gets a user record by its unique identifier. If the user does not exist, the endpoint gives a 404 status and shows a not-found error. The response body contains a JSON representation of the user object.
>
> **Principle applied:** Rule 3.7 (use approved verbs: "Does the retrieval" → "Gets"; "provides" → "gives" per P1; "gives the indication of" → "shows"); P1 (synonym table: "provides" → "gives").
> **Explanation:** Three Rule 3.7 violations. "Does the retrieval of" nominalizes the action of the GET method — the direct verb "Gets" matches the HTTP method name and is more concise. "Provides" is not in the synonym table; the preferred verb is "gives." "Gives the indication of" is a wordy construction that buries the action — "shows" is direct and clear. Note that "contains" is an approved verb and the phrase "a JSON representation" is a technical description, not a nominalized action — this part is already correct.

### Example 7 — Commit Message: Multi-Step Change

> **Non-STE:** Do the refactoring of the authentication module and perform the addition of rate limiting. The change makes the implementation of a token bucket algorithm and does the configuration of the limit to 100 requests per minute.
>
> **STE:** Refactor the authentication module and add rate limiting. The change implements a token bucket algorithm and sets the limit to 100 requests per minute.
>
> **Principle applied:** Rule 3.7 (use approved verbs: "Do the refactoring" → "Refactor"; "perform the addition" → "add"; "makes the implementation" → "implements"; "does the configuration" → "sets"); P1 (synonym table: "make" → preferred, but "implements" is the direct verb here; "configure" → "set").
> **Explanation:** Four nominalizations in two sentences of a commit message. "Do the refactoring" wastes characters compared to "Refactor." "Perform the addition" is wordy — "add" is a simpler approved verb. "Makes the implementation of" is a double indirection: a light verb ("makes") plus a nominalization ("implementation") — the direct verb "implements" does both jobs. "Does the configuration of" is a support-verb construction where the approved verb "set" is available and clearer. The P1 synonym table prefers "set" over "configure."

### Example 8 — Configuration File Comment: YAML Settings

> **Non-STE:** # The connection pool settings. These values perform the control
> # of how many database connections the application maintains.
> # max_connections: Does the specification of the maximum number of
> # connections. The application does the creation of this many connections
> # at startup and keeps them for the lifetime of the process.
> **STE:** # The connection pool settings. These values control
> # how many database connections the application keeps.
> # max_connections: Specifies the maximum number of
> # connections. The application creates this many connections
> # at startup and keeps them for the lifetime of the process.
>
> **Principle applied:** Rule 3.7 (use approved verbs: "perform the control" → "control"; "Does the specification" → "Specifies"; "does the creation" → "creates").
> **Explanation:** Configuration file comments have limited line width and benefit from conciseness. Three nominalizations waste space. "Perform the control of" uses six words where one ("control") suffices. CONTROL is an approved verb. "Does the specification of" uses five words where one ("Specifies") suffices. SPECIFY is an approved verb. "Does the creation of" uses five words where one ("creates") suffices. CREATE is in the synonym table with "make" as the preferred alternative, but "creates" is an approved verb and is direct. The word "maintains" in the non-STE version is replaced with "keeps" per the P1 synonym table.

### Example 9 — Error Message: Validation Failure

> **Non-STE:** VALIDATION_ERROR: The system performed the validation of the request body and found an issue. The 'email' field underwent the failure of the format check. Please perform the correction of the value and do the re-submission of the request.
>
> **STE:** VALIDATION_ERROR: The system validated the request body and found an issue. The 'email' field failed the format check. Please correct the value and send the request again.
>
> **Principle applied:** Rule 3.7 (use approved verbs: "performed the validation" → "validated"; "underwent the failure" → "failed"; "perform the correction" → "correct"; "do the re-submission" → "send again"); P1 (synonym table: "send" preferred over "submit").
> **Explanation:** Four nominalizations in a user-facing error message. "Performed the validation of" buries the action — the direct verb "validated" is available. "Underwent the failure of the format check" is a triple indirection: the verb "underwent" + the noun "failure" + the noun phrase "format check." The direct construction "failed the format check" is shorter and clearer. "Perform the correction of" uses four words where one ("correct") suffices. "Do the re-submission" uses "do" as a support verb plus the noun "re-submission" — "send the request again" uses the approved verb "send" and the adverb "again." The prefix "re-" in "re-submission" is an unnecessary word-formation pattern that Rule 1.4 discourages.

---

## Edge Cases

The following scenarios show where the boundary between approved verb usage and acceptable noun construction requires careful judgment.

### Edge Case 1: When the Approved Verb Does Not Exist for a Code-Domain Action

**Scenario:** Some code-domain actions have no direct approved verb. For example, "lint" as a verb (meaning "to run a linter on source code") is a code-domain technical verb under Rule 1.12. But if the project's STE-Code dictionary does not approve "lint" as a verb, the action must be expressed with a support verb construction: "run the linter" or "do a lint check."

**Guidance:** When a code-domain action has no approved verb, use the support-verb construction: a light verb ("do," "run," "make," "send") plus the code-domain technical noun. This is not a Rule 3.7 violation — it is the correct construction when no approved verb exists. The rule's requirement is "use an approved verb to describe an action." The support verb ("do," "run") IS the approved verb. The code-domain noun specifies the type of action.

> **Non-STE:** Lint the source code before you commit.
>
> **STE:** Run the linter on the source code before you commit.
> *(Rule 3.7 applied: "Lint" as a verb is not approved in this scenario. The support verb "Run" carries the action, and "linter" is a technical noun.)*

### Edge Case 2: When a Framework Name Is Also a Verb in Common Usage

**Scenario:** Some framework and tool names are commonly used as verbs in developer speech: "Dockerize," "Kubernetize," "Terraform," "Webpack it," "Babel it," "Prettier it." None of these are approved verbs. They are technical nouns (proper names) that developers verb.

**Guidance:** Never verb a framework or tool name. The tool name is a proper noun and a technical noun under Rule 1.5. To describe the action of using the tool, use the support-verb construction: "Put the application in a Docker container," "Deploy to Kubernetes," "Apply the Terraform configuration," "Bundle with Webpack," "Transpile with Babel," "Format with Prettier."

> **Non-STE:** Dockerize the service and then Kubernetes it to the cluster.
>
> **STE:** Put the service in a Docker container and then deploy it to the Kubernetes cluster.
> *(Rule 3.7 applied: "Dockerize" → support construction. "Kubernetes it" → "deploy it to the Kubernetes cluster." DEPLOY is an approved verb under Rule 1.12.)*

### Edge Case 3: When the Noun Construction Is More Common and the Verb Construction Sounds Forced

**Scenario:** Some code-domain concepts have a strong noun identity. For example, "backup" is more commonly used as a noun: "create a backup," "restore from a backup." The verb "back up" (two words, phrasal verb) is also valid but less common in some documentation styles. Is "Create a backup" a Rule 3.7 violation when "Back up" exists?

**Guidance:** When both the verb and the noun construction are accepted in the domain, prefer the verb construction per Rule 3.7. But when the noun construction is deeply established and the verb construction sounds unnatural or creates ambiguity, the noun construction is acceptable. "Create a backup" is clear and widely understood. "Back up the database" is also correct but the phrasal verb "back up" can be confused with the non-technical meaning ("move backward" or "support"). In this case, the established noun construction with a support verb is acceptable.

> **Non-STE:** Perform a backup of the database before the migration.
> **STE 1:** Back up the database before the migration. (Direct verb — Rule 3.7 preferred)
> **STE 2:** Create a backup of the database before the migration. (Support verb — acceptable when the direct verb is ambiguous)
> *(Both STE versions are acceptable. Version 1 follows Rule 3.7 strictly. Version 2 is acceptable because "back up" as a phrasal verb can be ambiguous. "Create a backup" uses the approved verb "create" (from the "make" synonym family) and the established technical noun "backup.")*

### Edge Case 4: The "Do + Gerund" Construction

**Scenario:** In developer speech, "do some debugging," "do some testing," "do some profiling" are common. The "-ing" form here is a gerund (a noun formed from a verb) not a progressive verb form. Is "do some debugging" a Rule 3.7 violation when "debug" is an approved verb?

**Guidance:** The "do some + gerund" construction is a specific idiomatic pattern in English that describes an informal, open-ended activity rather than a specific, bounded action. "Debug the crash" describes a specific action with a clear endpoint. "Do some debugging" describes an activity without a clear boundary. In formal code documentation, prefer the direct verb construction. Reserve the "do some + gerund" construction for informal contexts where the open-ended meaning is intentional.

> **Non-STE:** Do some debugging to find the cause of the crash.
>
> **STE:** Debug the crash to find the cause.
> *(Rule 3.7 applied: "Do some debugging" is a gerund construction. DEBUG is an approved verb under Rule 1.12. The direct verb is clearer and more specific.)*

### Edge Case 5: When the Direct Verb Has a Different Meaning from the Noun Construction

**Scenario:** Some verbs and their related nouns have diverged in meaning in the code domain. "Commit" as a verb means "to record changes in a version control system." "Commit" as a noun means "a set of changes recorded in a version control system." "Make a commit" describes creating the noun. "Commit the changes" describes performing the version-control operation. Are these equivalent?

**Guidance:** When the verb and the noun have different, established meanings in the code domain, choose the construction that conveys the intended meaning most precisely. "Commit the changes" describes the git operation. "Make a commit" describes the result of that operation. Both use approved constructions. The choice depends on what you want to emphasize: the action or the result.

> **Non-STE:** Perform a commit of the changes to the repository.
> **STE 1:** Commit the changes to the repository. (Emphasizes the action)
> **STE 2:** Make a commit of the changes. (Emphasizes the resulting object)
> *(Both STE versions are correct. Version 1 uses the direct verb and follows Rule 3.7 strictly. Version 2 uses the support verb "make" with the technical noun "commit" — this is acceptable when the noun has an established meaning distinct from the action.)*

---

## Cross-References

Rule 3.7 is the second-to-last rule in Section 3 (Verbs) of the STE-Code specification. It bridges the vocabulary rules in Section 1 with the verb-structure rules in Section 3. The rule depends on the vocabulary rules to define what counts as an approved verb, and it constrains how non-verb words can appear in sentence construction.

| Rule | Title | Relationship to Rule 3.7 |
|------|-------|---------------------------|
| **Rule 1.1** | Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs | Determines the pool of approved verbs that Rule 3.7 requires the writer to use. A word must be approved as a verb under Rule 1.1 before Rule 3.7 can prefer it over a noun construction. |
| **Rule 1.2** | Use Approved Words Only as the Specified Part of Speech | Directly complementary to Rule 3.7. Rule 1.2 says: use a word only as its approved part of speech. Rule 3.7 says: when expressing an action, use a word that IS approved as a verb. Together they prevent both verbing nouns (Rule 1.2) and nounifying verbs (Rule 3.7). |
| **Rule 1.3** | Use Approved Words Only with Their Approved Meanings | Constrains the meaning of each approved verb. When Rule 3.7 directs the writer to use an approved verb, Rule 1.3 ensures the verb's meaning matches the intended action. |
| **Rule 1.4** | Use Only the Approved Forms of Verbs and Adjectives | Governs verb morphology. When Rule 3.7 directs the writer to use an approved verb, Rule 1.4 (and Rule 3.1) constrain which forms of that verb are permitted. |
| **Rule 1.7** | Do Not Use Technical Nouns as Verbs | The verbing prohibition. Every violation of Rule 1.7 (using a technical noun as a verb) is also a violation of Rule 3.7 (using a non-verb to describe an action). Rule 3.7 provides the positive instruction: "use an approved verb." Rule 1.7 provides the negative counterpart: "do not use a technical noun as a verb." |
| **Rule 1.12** | Technical Verbs Are Allowed | Permits code-domain technical verbs that are not in the base STE vocabulary. Rule 3.7 can direct the writer to use a technical verb under Rule 1.12 when no base-STE verb describes the action. For example, "refactor" is a technical verb that Rule 3.7 prefers over "do a refactor." |
| **Rule 1.13** | Do Not Use Technical Verbs as Nouns | The inverse of Rule 1.7. When a technical verb is nouned (e.g., "the deploy" instead of "the deployment"), Rule 1.13 prohibits it. Rule 3.7's discipline of using verbs for actions naturally resists the nouning of technical verbs. |
| **Rule 3.1** | Use Only the Verb Forms That Are Given in the Dictionary | Governs the morphological forms of approved verbs. Once Rule 3.7 has identified the correct approved verb, Rule 3.1 constrains which forms of that verb may appear in the sentence. |
| **Rule 3.2** | Use the Correct Verb Tense | Governs tense selection. When Rule 3.7 directs the writer to use an approved verb, Rule 3.2 ensures the verb's tense matches the temporal context. |
| **Rule 3.3** | Use the Active Voice as Much as Possible in Procedural Writing | Governs voice. Nominalization often accompanies passive voice: "The validation is performed by the system" (passive + nominalization). Rule 3.3 (active voice) and Rule 3.7 (direct verb) work together to produce sentences like "The system validates the input." |
| **Rule 3.4** | Use the Imperative Mood for Instructions | Governs mood for procedural writing. The imperative mood naturally requires the base form of an approved verb, which aligns with Rule 3.7's preference for direct verbs over noun constructions. |
| **Rule 3.6** | Use the Active Voice | Governs voice in all writing contexts. Nominalization ("The system does the processing of the request") often pairs with passive voice ("The request is processed by the system"). Rules 3.6 and 3.7 together push toward "The system processes the request." |

**Section 3 rule chain context:** Rule 3.1 defines the verb form inventory. Rule 3.2 assigns tenses. Rule 3.3 and Rule 3.6 govern voice (procedural and general). Rule 3.4 governs imperative mood. Rule 3.5 governs helping verbs. Rule 3.7 is the closure rule for Section 3: it ensures that the subject of every sentence in Section 3 — the verb — is in fact a verb, not a noun or adjective masquerading as one.

**Dictionary reference:** See `a-dictionary.md` for the full STE-Code controlled terminology. Each dictionary entry specifies the part of speech (v, n, adj, adv, prep, conj, pron, art, TN, TV). Rule 3.7 requires the writer to check this part-of-speech tag: if the word needed to describe an action is tagged as anything other than "(v)" or "(TV)," restructure the sentence to use a word that IS tagged as a verb.

**Key dictionary entries relevant to Rule 3.7:**

- **CHECK (v) / CHECK (n):** CHECK is approved as both a verb and a noun with different meanings. As a verb, it means "to examine or test." As a noun, it means "an examination or test." Rule 3.7 prefers the verb: "Check the configuration" not "Do a check of the configuration." But note the ASD-STE100 original exception: when CHECK is not approved as a verb in a specific controlled terminology, the support construction "Do a check" is correct.
- **TEST (v) / TEST (n):** Same dual-status word as CHECK. Rule 3.7 prefers "Test the endpoint" over "Do a test of the endpoint" when TEST is approved as a verb.
- **BUILD (v) / BUILD (n):** BUILD is approved as a verb ("compile and link") and as a noun ("a compiled artifact"). Rule 3.7 prefers "Build the project" over "Do a build of the project" when describing the action.
- **MAKE (v):** MAKE is the primary approved support verb for construction actions. When no direct approved verb exists, MAKE + noun is correct: "Make a backup," "Make a copy," "Make a commit." MAKE must not be used when a direct approved verb exists: "Make an installation of" is incorrect — use "Install."
- **DO (v):** DO is the primary approved support verb for process actions: "Do a test," "Do a check," "Do an analysis." DO + noun is correct when no direct approved verb describes the action. DO must not be used when a direct approved verb exists.
- **RUN (v):** RUN is the primary approved verb for execution actions: "Run the script," "Run the test suite," "Run the build." RUN also serves as a support verb for tool-based actions: "Run the linter," "Run the profiler."

---

## Grammar Notes

### The Distinction Between Light Verbs and Content Verbs

Rule 3.7 draws a fundamental grammatical distinction between light verbs (also called "delexical verbs" or "support verbs") and content verbs. A light verb carries grammatical information (tense, person, number) but minimal semantic content. The semantic content lives in the noun that follows. A content verb carries both grammatical and semantic information.

In "The function does the validation of the input," "does" is a light verb. It carries the third-person singular present marker "-es" but the action is the validation. The sentence has two words ("does" + "validation") where one content verb ("validates") would suffice.

Rule 3.7 instructs the writer to replace the light-verb + noun construction with a content verb whenever the content verb exists and is approved. This rule is not about grammatical correctness — both constructions are grammatically correct English. It is about clarity and conciseness. The content verb is always shorter, always more direct, and always places the action in the grammatically strongest position (the main verb slot).

The structural transformation is:

```
[light verb] + [determiner] + [nominalization] + [prepositional complement]
         ↓
[content verb] + [direct object]
```

Examples of the transformation:

| Light Verb Construction | Content Verb |
|-------------------------|-------------|
| Do the installation of | Install |
| Perform the analysis of | Analyze |
| Make the implementation of | Implement |
| Give an indication of | Show |
| Do the configuration of | Set, Configure |
| Perform the execution of | Run |
| Make the deployment of | Deploy |
| Do the verification of | Check |
| Experience a timeout | Time out |
| Undergo the failure of | Fail |

### When the Support Verb Construction Is Correct

The support verb construction ("do + noun," "run + noun," "make + noun") is correct in STE-Code when no approved verb exists for the action. The original ASD-STE100 gives the example "Do a check of the laptop battery" where "check" is not approved as a verb. The support verb "do" carries the action, and the noun "check" specifies the type of action.

In STE-Code, the support verb construction is correct in three scenarios:

1. **The word is not approved as a verb.** If the dictionary does not list the word as "(v)" or "(TV)," it cannot serve as a content verb. Use a support verb: "Do a benchmark" if BENCHMARK is approved only as a noun.

2. **The action noun has an established technical meaning distinct from the verb.** "Make a commit" emphasizes the resulting object. "Commit the changes" emphasizes the action. Both are valid depending on the intended emphasis.

3. **The code-domain action has no equivalent English verb.** "Do a POST request" describes an HTTP method. POST is a technical noun (the HTTP method name), and there is no English verb that means "to send an HTTP POST request." The support construction is the only option.

### Nominalization: The Linguistic Process and Its Reversal

Nominalization is the linguistic process of turning a verb into a noun. In English, this is most commonly done with the suffixes "-tion" (validate → validation), "-ment" (deploy → deployment), "-al" (approve → approval), "-ance" (perform → performance), and "-ing" (build → building).

Code documentation inherited nominalization from academic and business writing, where it serves a legitimate purpose: nominalization allows the writer to talk about an action as an abstract concept rather than a specific event. "The validation of user input is important" treats validation as a topic of discussion. "You must validate user input" is a direct instruction.

In code documentation, nominalization is harmful for two reasons. First, it increases sentence length without adding information. "The function performs the validation of the input" uses eight words. "The function validates the input" uses five. Second, it weakens the grammatical position of the action. In a sentence, the main verb is the most prominent position. When the action is hidden in a noun, the reader must do extra work to extract the meaning.

Rule 3.7's discipline is to reverse the nominalization: find the noun that carries the action, identify the verb from which it was derived, and use that verb as the main verb of the sentence.

### The Zero-Derivation Problem: Words That Are Both Noun and Verb

Many code-domain words function as both nouns and verbs without any change in form: "build," "test," "check," "deploy," "commit," "push," "pull," "merge," "branch," "fork," "tag," "release." These are zero-derivation words (also called "conversion"). The part of speech is determined by context, not by morphology.

Rule 3.7 interacts with zero-derivation words in a specific way. If the dictionary approves the word as both a noun and a verb, Rule 3.7 prefers the verb form when describing an action. But the sentence structure, not the word itself, determines whether the word is functioning as a verb or a noun.

In "Run the build," BUILD is a noun (direct object of RUN). In "Build the project," BUILD is a verb (imperative). Both are correct STE-Code as long as BUILD is approved as both a noun and a verb. Rule 3.7 does not prohibit the noun use. It only says: when you want to describe the action of building, use the verb "build," not the noun construction "do a build."

The test for zero-derivation words: can you replace the word with an unambiguous verb? If yes, the word is being used as a verb and Rule 3.7 is satisfied. If the word is the object of a light verb ("do a build," "run a test"), it is being used as a noun — and the construction is acceptable only if the direct verb is unavailable or inappropriate per the edge cases above.

### Interaction with the Canonical Synonym Table

The STE-Code canonical synonym table (P1) lists preferred verbs and their avoided alternatives. Rule 3.7 and the synonym table work together: Rule 3.7 says "use a verb, not a noun." The synonym table says "when you choose the verb, use the preferred one."

The synonym table preferences most relevant to Rule 3.7:

| Preferred Verb | Avoided Verb (and its nominalization) |
|---------------|--------------------------------------|
| use | utilize (utilization), leverage (leverage), employ (employment) |
| start | initiate (initiation), commence (commencement), bootstrap |
| stop | terminate (termination), halt, kill |
| show | display, render, present (presentation) |
| make | create (creation), generate (generation), produce (production) |
| get | retrieve (retrieval), fetch, obtain |
| set | configure (configuration), assign (assignment), establish (establishment) |
| check | verify (verification), validate (validation), ensure |
| do | perform (performance), execute (execution), carry out |
| send | transmit (transmission), dispatch, forward |
| remove | delete (deletion), eliminate (elimination), purge |
| keep | retain (retention), preserve (preservation), maintain (maintenance) |

When a writer replaces a nominalization with a verb, they must choose the verb from the preferred column, not the avoided column. "The function performs the verification of the data" becomes "The function checks the data" (not "The function verifies the data").

### Historical Note: ASD-STE100 Precedent

In ASD-STE100 Issue 9, Rule 3.7 is the closure rule for Section 3 (Verbs). The original aerospace specification gives the rule in two paragraphs with two example pairs. Despite its brevity, the rule encapsulates a central STE philosophy: verbs are for actions. Nouns are for things. Do not use a noun when a verb will do the action better.

The original examples are revealing. The first pair ("The ohmmeter gives an indication of 450 ohms" / "The ohmmeter shows 450 ohms") targets the verb "gives" used as a light verb where the content verb "shows" is available. The second pair ("Check the laptop battery" / "Do a check of the laptop battery") targets the opposite problem: using a verb that is not approved, where the support construction with the approved noun is the correct alternative. Together, the two examples establish Rule 3.7 as a two-way gate: replace light-verb + noun with content verb when the content verb is approved, and replace an unapproved verb with support-verb + noun when the noun is approved.

In code documentation, the same two-way gate applies. "The linter gives an indication of three errors" → "The linter shows three errors" (light verb replaced with content verb). "Benchmark the application" → "Do a benchmark of the application" (unapproved verb replaced with support construction). The discipline is symmetric: always put the action in the approved part of speech.

The aerospace justification for Rule 3.7 is readability and precision. A light-verb construction ("gives an indication of") adds words that carry no information. Each extra word increases the cognitive load on the reader, who is often a maintenance technician working under time pressure. In code documentation, the reader is often a developer debugging a problem or integrating an API, also under time pressure. Every extra word in "performs the initialization of" compared to "initializes" is a tax on the reader's attention. Rule 3.7 removes that tax.
