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
