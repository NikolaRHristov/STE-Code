<!-- a-sec9-rule9.1.md -->

# Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec9-rule9.1](ste-code/grouped/), Rule 9.1

## Original Rule

Use a different sentence construction to write a sentence when a word-for-word replacement is not sufficient.

STE is a controlled natural language with a controlled dictionary. To help you use the approved words correctly, the dictionary gives approved alternatives for words that are not approved. If you find an alternative that has the same part of speech, you can use it to replace the word that is not permitted (a word-for-word replacement).

When you replace a word, always make sure that the alternative that you select does not change the meaning of the sentence. If the meaning changes, or if the alternative does not have the same part of speech, you must use a different sentence construction.

A different sentence construction is necessary because:

1. You must change the grammatical structure of the sentence to use the alternative that you selected.
2. The word-for-word replacement of the word that is not approved gives a meaningless result.
3. The approved alternative that you find changes the meaning of the sentence.
4. The word that you must replace is not in the dictionary.

## STE-Code Adaptation

> **See also:** Rule 9.2 — Use Each Approved Word Correctly; Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs; Rule 9.4 — When You Select Terminology or Wording, Always Use a Consistent Style

Use a different sentence construction to write a sentence when a word-for-word replacement is not sufficient.

In code documentation, when a word is not approved in the controlled terminology, the dictionary gives approved alternatives. If the alternative has the same part of speech and does not change the meaning, you can do a word-for-word replacement. If the meaning changes, the part of speech differs, or a word-for-word replacement gives a meaningless result, you must write a new sentence with a different structure that uses only approved words while keeping the same technical meaning.

A different sentence construction is necessary because:

1. You must change the grammatical structure to use the approved alternative.
2. The word-for-word replacement gives a meaningless or unclear result.
3. The approved alternative changes the meaning of the sentence.
4. The word to replace is not in the controlled terminology.

When you cannot do a word-for-word replacement, think about the purpose of the sentence and use different words to get the same result. Frequently, you must select different words, use different verb forms, write shorter sentences, remove information that is not necessary, or get more information from a developer.

### Examples

> *Adapted from spec pair:* Non-STE: "A value of 2 mm is acceptable." | STE: "A value of 2 mm is permitted."

> **Non-STE:** A timeout value of 5000 ms is acceptable for this endpoint.
>
> In an API reference this appears as:
>
> **`POST /ingest` — Request parameters**
>
> | Parameter | Type | Description |
> |---|---|---|
> | `timeout_ms` | integer | A timeout value of 5000 ms is acceptable for this endpoint. |
>
> ```http
> POST /ingest HTTP/1.1
> Host: api.example.com
> Content-Type: application/json
>
> { "timeout_ms": 5000 }
> ```

> **STE:** A timeout value of 5000 ms is permitted for this endpoint.
>
> In an API reference this appears as:
>
> **`POST /ingest` — Request parameters**
>
> | Parameter | Type | Description |
> |---|---|---|
> | `timeout_ms` | integer | A timeout value of 5000 ms is permitted for this endpoint. |
>
> ```http
> POST /ingest HTTP/1.1
> Host: api.example.com
> Content-Type: application/json
>
> { "timeout_ms": 5000 }
> ```

("Acceptable" is not approved. The approved adjective "permitted" has the same part of speech and does not change the meaning, so a word-for-word replacement is sufficient. No restructuring is necessary.)
*Adapted from spec pair: "A value of 2 mm is acceptable." / "A value of 2 mm is permitted."*

> **Non-STE:** The stack trace in the console must be visible during the debugging session.
>
> From a runbook for the payment service:
>
> ```markdown
> ## Debug the payment service
>
> 1. Start the service in debug mode.
> 2. Reproduce the failed transaction.
> 3. The stack trace in the console must be visible during the debugging session.
> ```

> **STE:** During the debugging session, make sure that you can see the stack trace in the console.
>
> From a runbook for the payment service:
>
> ```markdown
> ## Debug the payment service
>
> 1. Start the service in debug mode.
> 2. Reproduce the failed transaction.
> 3. During the debugging session, make sure that you can see the stack trace in the console.
> ```

(The approved verb "see" replaces the adjective "visible." To use the verb "see," replace "must be" with "make sure that you can.")
*Adapted from spec pair: "The oil level on the sight gauge must be visible during the test." / "During the test, make sure that you can see the oil level on the sight gauge."*

> **Non-STE:** Loop the function twice to remove null values from the array.
>
> From the README of a data-cleaning utility:
>
> ```markdown
> ### Quick start
>
> Loop the function twice to remove null values from the array.
> ```

> **STE:** Run the function for two iterations to remove null values from the array.
>
> From the README of a data-cleaning utility:
>
> ```markdown
> ### Quick start
>
> Run the function for two iterations to remove null values from the array.
> ```

(The approved noun "iteration" together with the approved verb "run" replaces the verb "loop." The technical noun "two" replaces the adverb "twice.")
*Adapted from spec pair: "Cycle the unit twice to remove air from the lines." / "Operate the unit for two cycles to remove air from the lines."*

> **Non-STE:** Without this configuration change, the behavior of the function can be uncertain.
>
> From the configuration guide for a rate limiter:
>
> ```markdown
> ## `strict_mode`
>
> Set this value to `true` to apply the strict limit.
> Without this configuration change, the behavior of the function can be uncertain.
> ```

> **STE:** Without this configuration change, it is possible that the function will not behave as expected.
>
> From the configuration guide for a rate limiter:
>
> ```markdown
> ## `strict_mode`
>
> Set this value to `true` to apply the strict limit.
> Without this configuration change, it is possible that the function will not behave as expected.
> ```

("Uncertain" is not in the controlled terminology. A word-for-word replacement such as "cannot be sure" or "cannot be known" gives a meaningless result. You must think about the meaning and write a new sentence.)
*Adapted from spec pair: "Without this modification, the service life of the unit can be uncertain." / "Without this modification, it is possible that the service life of this unit will be shorter than usual."*

> **Non-STE:** Just add a single log statement to the method.
>
> From a contribution guide:
>
> ```markdown
> ### Add a trace
>
> Just add a single log statement to the method.
> ```

> **STE:** Only add a single log statement to the method.
>
> From a contribution guide:
>
> ```markdown
> ### Add a trace
>
> Only add a single log statement to the method.
> ```
>
> NOT: Immediately add a single log statement to the method.

("Immediately" is the approved alternative for "just." But if you use it in this context, the meaning of the instruction changes.)
*Adapted from spec pair: "Just apply very light pressure to the surface." / "Only apply very light pressure to the surface." NOT: "Immediately apply very light pressure to the surface."*

> **Non-STE:** The occurrence of type errors in the build output is a serious problem.
>
> From the build documentation:
>
> ```markdown
> ## Common build failures
>
> The occurrence of type errors in the build output is a serious problem.
> Fix each error before you run the tests.
> ```

> **STE:** Type errors in the build output are a serious problem.
>
> From the build documentation:
>
> ```markdown
> ## Common build failures
>
> Type errors in the build output are a serious problem.
> Fix each error before you run the tests.
> ```

("Occurrence" is not in the controlled terminology. You must think of a different construction that keeps the same meaning without the unapproved word.)
*Adapted from spec pair: "The incidence of water in fuel is dangerous." / "Water in fuel is dangerous."*

> **Non-STE:** Scroll the editor pane so that it clears the minimap overlay.
>
> From the editor user guide:
>
> ```markdown
> ### View the full file
>
> Scroll the editor pane so that it clears the minimap overlay.
> ```

> **STE:** Scroll the editor pane until it is away from the minimap overlay.
>
> From the editor user guide:
>
> ```markdown
> ### View the full file
>
> Scroll the editor pane until it is away from the minimap overlay.
> ```
>
> NOT: Scroll the editor pane so that it cleans the minimap overlay.

("Clear" is not an approved verb. Its only alternative in the controlled terminology is "clean" as a verb, but "clean" does not have the intended meaning in this context. The intended meaning is "to increase the distance between" — use "until it is away from.")
*Adapted from spec pair: "Lift the seat so that it clears the track locks." / "Lift the seat until it is away from the track locks." NOT: "Lift the seat so that it cleans the track locks."*

> **Non-STE:** If linting errors are detected during this procedure, the developer must perform the correction within a certain number of commits depending on error severity. Refer to following table:
>
> | Error severity detected | Time before correction |
> |---|---|
> | Critical | 1 commit |
> | Major | 3 commits |
> | Minor | 5 commits |
>
> ```markdown
> ## Fix linting errors
>
> If linting errors are detected during this procedure, the developer must
> perform the correction within a certain number of commits depending on
> error severity. Refer to following table:
> ```

> **STE:** If you find linting errors, refer to the table that follows:
>
> | If the error is of this severity | Do the correction before |
> |---|---|
> | Critical | 1 commit |
> | Major | 3 commits |
> | Minor | 5 commits |
>
> ```markdown
> ## Fix linting errors
>
> If you find linting errors, refer to the table that follows:
> ```

(In the non-STE example: the underlined words are not approved; the verb form "are detected" is passive; the first sentence is too long; an article is missing before "following table"; the instruction is not imperative. The STE version uses approved words, active voice, imperative form, and moves the instruction into the table heading to avoid repeating information.)
*Adapted from spec pair: the crack detection and repair table example using "If you find cracks, refer to the table that follows:" — see spec pages 117–119 for the full original.*

## Code-Domain Explanation

Rule 9.1 is the most powerful rule in the STE-Code system. It is the rule you use when all other word-level rules fail. In code documentation, this rule applies differently to each documentation type because each type has a different audience, a different level of formality, and a different set of technical constraints.

### README Files

README files are the first document a new developer sees. They must be clear, short, and welcoming. When a word-for-word replacement fails in a README, you must restructure the sentence to use simple, direct language. Frequently, this means you must:

- Replace passive descriptions with active instructions.
- Move complex explanations to a separate document.
- Use bullet points instead of long paragraphs.
- Remove marketing language and replace it with factual statements.

For example, a README that says "This library leverages asynchronous I/O to facilitate high-throughput data processing" has multiple unapproved words. A word-for-word replacement of each word individually ("This library uses asynchronous I/O to make easy high-throughput data processing") gives a meaningless result. You must think about the purpose of the sentence and write:

> **Non-STE:** This library leverages asynchronous I/O to facilitate high-throughput data processing.
>
> ```markdown
> # fastqueue
>
> fastqueue leverages asynchronous I/O to facilitate high-throughput
> data processing for message pipelines.
> ```

> **STE:** This library uses async I/O. It can process large quantities of data quickly.
>
> ```markdown
> # fastqueue
>
> fastqueue uses async I/O. It can process large quantities of data quickly.
> ```

### API Documentation

API documentation has strict structural requirements. Each endpoint, parameter, and return value must be described precisely. When a word-for-word replacement fails in API docs, you must:

- Keep the technical parameter names unchanged (Rule 1.5).
- Restructure the description sentence around the approved word.
- Use a different grammatical subject if the original subject depends on an unapproved word.
- Split compound descriptions into separate sentences, one per parameter or behavior.

For example, an API description that says "This endpoint facilitates the retrieval of user profiles" cannot be fixed by replacing "facilitates" with "makes easy" and "retrieval" with "the action to get." You must restructure:

> **Non-STE:** This endpoint facilitates the retrieval of user profiles.
>
> ```http
> GET /users
>
> This endpoint facilitates the retrieval of user profiles.
> The response contains the full record for each account.
> ```

> **STE:** This endpoint gets user profiles.
>
> ```http
> GET /users
>
> This endpoint gets user profiles.
> The response contains the full record for each account.
> ```

### Docstrings and Inline Comments

Docstrings and inline comments are the most constrained documentation type. They must be short, appear directly next to the code they describe, and frequently include code symbols that cannot be changed. When a word-for-word replacement fails in a docstring:

- Use the approved verb form even if it makes the sentence longer (Rule 1.4).
- Move complex explanations to a separate design document.
- If a word-for-word replacement is impossible in the available space, remove the sentence and replace it with a reference to a longer document.
- Never change a code symbol to match an approved word. Code symbols are technical nouns (Rule 1.5).

> **Non-STE:** """Computes the aggregate of the supplied metrics and persists them."""
> ```python
> def summarize(metrics):
>     """Computes the aggregate of the supplied metrics and persists them."""
>     ...
> ```

> **STE:** """Gets the total of the metrics and saves them."""
> ```python
> def summarize(metrics):
>     """Gets the total of the metrics and saves them."""
>     ...
> ```

### Commit Messages

Commit messages have a conventional format: a short summary line, a blank line, and a body. When a word-for-word replacement fails in a commit message:

- Use imperative mood in the summary line ("Add feature" not "Added feature").
- Replace unapproved verbs with approved technical verbs from the STE-Code dictionary.
- If the commit message describes a complex change that needs many unapproved words, write a shorter message and put the details in the pull request description.
- Never use the commit message body as a substitute for proper documentation.

> **Non-STE:** Implemented utilization of the cached connection pool to expedite request handling.
>
> ```text
> Implemented utilization of the cached connection pool to expedite
> request handling.
> ```

> **STE:** Use the cached connection pool to make requests faster.
>
> ```text
> Use the cached connection pool to make requests faster.
> ```

### Error Messages

Error messages must be short, clear, and actionable. They appear in logs, terminals, and monitoring dashboards. When a word-for-word replacement fails in an error message:

- Restructure the message to tell the user what occurred and what to do.
- Remove technical jargon that the user cannot act on.
- Use the approved words "cannot" and "do not" instead of unapproved negative forms.
- If the error message includes a stack trace or a code symbol, keep it unchanged (Rule 1.5).

> **Non-STE:** The application encountered an unrecoverable exception while attempting to instantiate the connection pool.
>
> ```text
> ERROR 2026-08-01T09:14:02Z com.db.PoolFactory
> The application encountered an unrecoverable exception while
> attempting to instantiate the connection pool.
> ```

> **STE:** The application cannot start the connection pool. Look at the log for more data.
>
> ```text
> ERROR 2026-08-01T09:14:02Z com.db.PoolFactory
> The application cannot start the connection pool.
> Look at the log for more data.
> ```

*Principles applied: P1, P2, P11. "Encountered" replaced with cannot + start. "Unrecoverable" removed because the user cannot act on it. "Exception" and "instantiate" replaced with simpler constructions.*

### Generated Code and Automated Output

When you document generated code (code produced by a compiler, a code generator, or an AI tool), the generated code itself is not subject to STE-Code rules. The documentation that describes the generated code must follow the rules. If the generated code includes unapproved words in its symbol names, you must keep those symbol names unchanged in the documentation (Rule 1.5), but you can describe their function using approved words in a restructured sentence.

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Object-oriented documentation uses class names, method signatures, and inheritance hierarchies as technical nouns. When you must restructure a sentence for Rule 9.1, you frequently encounter these patterns:

- **Abstract class descriptions** use words like "facilitate," "provide a mechanism for," and "serve as a base for." Replace these with "let you," "are used to," or restructure around the concrete behavior: "This abstract class lets subclasses share database connection logic."
- **Interface documentation** uses words like "contract," "guarantee," and "enforce." These are unapproved. Restructure: "All classes that use this interface must have a `save` method."
- **Inheritance descriptions** use "extend," "override," and "specialize." These are technical nouns (Rule 1.5) when they refer to code keywords, but they are unapproved verbs when used in descriptive sentences. When the keyword is the subject of the sentence, keep it. When it is a verb in the description, replace it.

> **Non-STE:** The `BaseRepository` class provides an abstraction that facilitates data access operations across multiple database backends.
>
> ```java
> /**
>  * The BaseRepository class provides an abstraction that
>  * facilitates data access operations across multiple
>  * database backends.
>  */
> public abstract class BaseRepository<T> { ... }
> ```

> **STE:** The `BaseRepository` class lets you use the same data access methods with different databases.
>
> ```java
> /**
>  * The BaseRepository class lets you use the same data
>  * access methods with different databases.
>  */
> public abstract class BaseRepository<T> { ... }
> ```

*Principles applied: P1, P2, P7, P11. "Provides an abstraction that facilitates" is a chain of unapproved words. The STE version identifies the purpose (let you use the same methods) and states it directly. "Backends" replaced with "databases."*

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, immutable data, and type transformations. These concepts frequently use words like "evaluate," "reduce," "compose," and "curry" that are technical nouns in the functional paradigm but may not be in the STE-Code dictionary. When you must restructure:

- **Type signatures** are code, not prose. They are technical nouns (Rule 1.5) and must stay unchanged.
- **Function descriptions** use words like "maps over," "folds," and "lifts." These are technical verbs (Rule 1.12) when they name a specific operation. When they are used in a general descriptive sense, replace them: "applies a function to each element" instead of "maps over."
- **Monad and functor descriptions** use abstract mathematical language. Restructure around the practical effect: "lets you chain operations that can fail" instead of "provides a monadic interface for effectful computations."

> **Non-STE:** This function `fmap`s the provided transformation over the `Maybe` value, yielding a new `Maybe` that encapsulates the transformed result.
>
> ```haskell
> -- This function fmaps the provided transformation over the
> -- Maybe value, yielding a new Maybe that encapsulates
> -- the transformed result.
> mapMaybe :: (a -> b) -> Maybe a -> Maybe b
> ```

> **STE:** This function applies the transformation to the `Maybe` value. If the `Maybe` value is `Just x`, the result is `Just (f x)`. If it is `Nothing`, the result is `Nothing`.
>
> ```haskell
> -- This function applies the transformation to the Maybe value.
> -- If the Maybe value is Just x, the result is Just (f x).
> -- If it is Nothing, the result is Nothing.
> mapMaybe :: (a -> b) -> Maybe a -> Maybe b
> ```

*Principles applied: P1, P5. The code symbols `fmap`, `Maybe`, `Just`, `Nothing` are kept as technical nouns. "Yielding," "encapsulates," and "transformed result" are restructured into concrete conditional descriptions.*

### Procedural Documentation (C, Go, Bash)

Procedural documentation describes sequences of steps, memory operations, and system calls. When you must restructure for Rule 9.1:

- **Memory management descriptions** use words like "allocate," "deallocate," "free," and "dereference." "Allocate" and "free" are technical verbs (Rule 1.12). "Deallocate" is not approved; replace with "free" or "release."
- **Error handling in C** uses words like "errno," "perror," and "return codes." These are technical nouns (Rule 1.5). The descriptions around them must use approved words.
- **Shell script documentation** uses words like "pipe," "redirect," and "subshell." These are technical nouns when they name shell features, but unapproved when used as general verbs. "Send the output of command A to command B" instead of "pipe command A to command B" when the word "pipe" is not a code keyword in context.

> **Non-STE:** The program allocates a buffer on the heap, then deallocates it after processing to prevent memory leaks.
>
> ```c
> /* The program allocates a buffer on the heap, then deallocates
>    it after processing to prevent memory leaks. */
> void run(void) {
>     char *buf = malloc(SIZE);
>     process(buf);
>     free(buf);
> }
> ```

> **STE:** The program gets a buffer from the heap. After it uses the buffer, it releases the memory to prevent memory leaks.
>
> ```c
> /* The program gets a buffer from the heap. After it uses the
>    buffer, it releases the memory to prevent memory leaks. */
> void run(void) {
>     char *buf = malloc(SIZE);
>     process(buf);
>     free(buf);
> }
> ```

*Principles applied: P1, P2, P11. "Allocates" replaced with "gets." "Deallocates" replaced with "releases the memory." The sentence is split into two shorter sentences.*

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state, not procedures. This creates a unique challenge for Rule 9.1 because declarative descriptions naturally use passive voice and stative verbs. When you must restructure:

- **SQL documentation** describes what a query returns, not what it does. Use "the query gets rows where..." instead of "the query retrieves rows that satisfy..."
- **Terraform documentation** describes resource configurations. Use "this resource makes a virtual machine with the given settings" instead of "this resource provisions a compute instance."
- **Kubernetes YAML documentation** describes workload specifications. Keep field names as technical nouns (Rule 1.5). Restructure the surrounding description: "the `replicas` field sets the number of Pods" instead of "the `replicas` field specifies the desired Pod count."

> **Non-STE:** This Deployment manifest orchestrates the rollout of three replicated Pods, ensuring high availability through automated rescheduling.
>
> ```yaml
> # This Deployment manifest orchestrates the rollout of three
> # replicated Pods, ensuring high availability through
> # automated rescheduling.
> apiVersion: apps/v1
> kind: Deployment
> spec:
>   replicas: 3
> ```

> **STE:** This Deployment makes three copies of the Pod. If a Pod stops, the system starts a new Pod automatically.
>
> ```yaml
> # This Deployment makes three copies of the Pod.
> # If a Pod stops, the system starts a new Pod automatically.
> apiVersion: apps/v1
> kind: Deployment
> spec:
>   replicas: 3
> ```

*Principles applied: P1, P2, P7, P11. "Orchestrates," "rollout," "ensuring," and "high availability" are all restructured. The sentence is split. "Replicated" becomes "copies." "Automated rescheduling" becomes "starts a new Pod automatically."*

### Systems Documentation (Rust Ownership, C Memory)

Systems documentation describes ownership, lifetimes, and memory safety guarantees. These concepts use words like "borrow," "own," "move," and "drop" that are both code keywords (Rule 1.5) and general English words. The context determines whether they are approved:

- When used as Rust keywords (in code font): keep unchanged.
- When used as descriptive verbs in prose: check against the STE-Code dictionary. "Borrow" is not an approved verb; replace with "get a reference to." "Own" is not an approved verb; replace with "has" or "controls." "Move" is an approved verb but has a specific meaning in Rust; when the meaning is the Rust ownership transfer, use "gives" or "moves" depending on context.

> **Non-STE:** When a value is moved, the original binding can no longer be utilized to access that value.
>
> ```rust
> // When a value is moved, the original binding can no longer
> // be utilized to access that value.
> let first = String::from("data");
> let second = first;
> println!("{}", first); // error
> ```

> **STE:** When you move a value, you cannot use the first variable name to get the value.
>
> ```rust
> // When you move a value, you cannot use the first variable
> // name to get the value.
> let first = String::from("data");
> let second = first;
> println!("{}", first); // error
> ```

*Principles applied: P1, P2, P13. "Utilized" replaced with "use." "Binding" is a technical noun (kept as "variable name" for clarity). "Original" and "access" are restructured. The passive "is moved" becomes active "you move."*

## Extended Examples

> **Non-STE:** The middleware intercepts incoming requests and modifies the headers prior to forwarding them to the downstream service.
>
> ```python
> # The middleware intercepts incoming requests and modifies the
> # headers prior to forwarding them to the downstream service.
> def handle(req):
>     req = add_trace(req)
>     return next_service(req)
> ```

> **STE:** The middleware gets each request. It changes the headers. Then it sends the request to the next service.
>
> ```python
> # The middleware gets each request. It changes the headers.
> # Then it sends the request to the next service.
> def handle(req):
>     req = add_trace(req)
>     return next_service(req)
> ```

*Principles applied: P1, P2, P6, P11. "Intercepts" is not approved. "Modifies" replaced with "changes." "Prior to forwarding" replaced with "Then it sends." "Downstream service" is jargon (P10); "next service" is clearer. The long sentence is split into three short sentences.*

> **Non-STE:** Utilize the `--verbose` flag to surface detailed diagnostic information during the build process.
>
> ```bash
> # Utilize the --verbose flag to surface detailed diagnostic
> # information during the build process.
> ./build.sh --verbose
> ```

> **STE:** Use the `--verbose` flag to show detailed diagnostic data during the build.
>
> ```bash
> # Use the --verbose flag to show detailed diagnostic data
> # during the build.
> ./build.sh --verbose
> ```

*Principles applied: P1, P11. "Utilize" is in the Synonym Table (prefer "use"). "Surface" as a verb is not approved; "show" is the approved alternative. "Information" replaced with "data" (see dictionary). "Process" removed as redundant.*

> **Non-STE:** This configuration option governs whether the linter enforces the rule set in a strict or permissive fashion.
>
> ```yaml
> # This configuration option governs whether the linter
> # enforces the rule set in a strict or permissive fashion.
> linter:
>   mode: strict
> ```

> **STE:** This configuration option sets how the linter applies the rules. You can set it to strict or permitted.
>
> ```yaml
> # This configuration option sets how the linter applies the
> # rules. You can set it to strict or permitted.
> linter:
>   mode: strict
> ```

*Principles applied: P1, P2, P7. "Governs" is not approved. "Enforces" is not approved. "Fashion" is not approved. The sentence is restructured around "sets" and split. "Permissive" has no direct approved alternative; "permitted" (adjective) is used after restructuring.*

> **Non-STE:** The garbage collector reclaims memory from objects that are no longer referenced, thereby preventing the application from exhausting available heap space.
>
> ```javascript
> // The garbage collector reclaims memory from objects that are
> // no longer referenced, thereby preventing the application
> // from exhausting available heap space.
> ```

> **STE:** The garbage collector frees memory that the application does not use. This prevents the application from using all the available heap memory.
>
> ```javascript
> // The garbage collector frees memory that the application
> // does not use. This prevents the application from using
> // all the available heap memory.
> ```

*Principles applied: P1, P2, P11. "Reclaims" replaced with "frees." "No longer referenced" restructured to "does not use." "Thereby preventing" split into a new sentence. "Exhausting" replaced with "using all."*

> **Non-STE:** Should the connection pool become saturated, the system will automatically spawn additional worker threads to handle the overflow.
>
> ```go
> // Should the connection pool become saturated, the system will
> // automatically spawn additional worker threads to handle
> // the overflow.
> for len(pool) == cap(pool) {
>     go worker()
> }
> ```

> **STE:** If the connection pool is full, the system automatically starts more worker threads.
>
> ```go
> // If the connection pool is full, the system automatically
> // starts more worker threads.
> for len(pool) == cap(pool) {
>     go worker()
> }
> ```

*Principles applied: P1, P2, P10, P11. "Should" as a conditional is not approved; "If" is the approved alternative. "Saturated" is jargon (P10). "Spawn" is not approved; "starts" is approved. "Handle the overflow" is unnecessary detail removed for clarity.*

> **Non-STE:** The `render` method leverages a virtual DOM diffing algorithm to minimize expensive DOM manipulations.
>
> ```javascript
> // The render method leverages a virtual DOM diffing algorithm
> // to minimize expensive DOM manipulations.
> render() {
>   return diff(this.state, this.prev);
> }
> ```

> **STE:** The `render` method uses a virtual DOM diff algorithm. This algorithm decreases the number of DOM changes.
>
> ```javascript
> // The render method uses a virtual DOM diff algorithm.
> // This algorithm decreases the number of DOM changes.
> render() {
>   return diff(this.state, this.prev);
> }
> ```

*Principles applied: P1, P2, P11. "Leverages" is in the Synonym Table (prefer "use"). "Minimize" is not approved as a verb in this sense; restructured. "Expensive" in the sense of "computationally costly" is jargon (P10); the specific meaning is restated as "decreases the number of." "Manipulations" replaced with "changes."*

## Edge Cases

### Framework Names That Are Also Unapproved Words

Some framework names are identical to unapproved English words. For example, the JavaScript build tool "Vite" (French for "fast"), the Python web framework "Flask," and the CSS framework "Tailwind" are all technical nouns (Rule 1.5). When you document these frameworks, keep the framework name unchanged. The framework name is a proper noun and a technical noun. It is not subject to word-level rules. However, do not use the framework name as a verb (Rule 1.7). Do not write "Flask your application." Write "Use Flask with your application."

When a framework name is also a common English word (for example, "Express," "Next," "Fresh"), the context in the sentence tells the reader if the word is a framework name or a common word. Use code font for framework names to make the distinction clear.

> **Non-STE:** Flask the service before you run the integration tests.
>
> **STE:** Use Flask with the service before you run the integration tests.

### Code Keywords That Conflict With Approved Words

Some programming language keywords are identical to approved STE-Code words but have a different meaning. For example, "use" is an approved STE-Code verb meaning "to put into service." In Rust, `use` is also a keyword that imports names from a module. When you document Rust code, the keyword `use` in code font is a technical noun (Rule 1.5). The same word in prose follows the STE-Code dictionary. Write: "Put `use std::io` at the top of the file. Then you can use the `io` module."

The same applies to "move" (approved STE-Code verb; Rust keyword for ownership transfer), "return" (approved STE-Code verb; keyword in most languages), and "break" (approved STE-Code verb; keyword for loop exit). Always use code font for the keyword and prose for the approved meaning.

> **Non-STE:** You must move the value with the move keyword, then return it from the function.
>
> **STE:** You must move the value with the `move` keyword, then give it back from the function.

### Generated Code and Automated Output

When you document generated code, the generated code itself is not subject to STE-Code rules. Only your documentation prose must follow the rules. If the generated code includes symbol names that use unapproved words, keep those symbol names unchanged in your documentation. For example, if a code generator produces a function named `utilizeData()`, you must keep the function name `utilizeData()` in your documentation because it is a code symbol (Rule 1.5). However, your description of what the function does must use approved words:

> **Non-STE:** The `utilizeData()` function leverages the cached payload to facilitate report generation.
>
> **STE:** The `utilizeData()` function uses the data to make a report.

### Quoted Log Output and Error Messages

When you quote log output or error messages from a system, keep the quoted text exactly as it appears. The quoted text is data, not documentation. Your surrounding prose must follow STE-Code rules. For example, if a log message says "Encountered irrecoverable error," you write:

> **Non-STE:** Encountered irrecoverable error means the app crashed.
>
> **STE:** The log shows: "Encountered irrecoverable error." This message means that the application found an error from which it cannot continue.

### When Restructuring Changes the Technical Precision

Sometimes a word-for-word replacement is not sufficient, but a full restructuring removes technical precision that the reader needs. For example, in a security audit document, the phrase "the attacker can exploit the race condition to achieve arbitrary code execution" uses many unapproved words. A word-for-word replacement fails. A full restructuring to "a bad actor can use the timing problem to run code" loses precision. In this case, you have three options:

1. Split the sentence and add a clarifying note that uses approved words to define the technical term.
2. Keep the technical term in code font with a glossary definition.
3. If the document is an internal security audit and the audience is security engineers, you can keep the term as a technical noun (Rule 1.5) with an approved-word definition on first use.

The choice depends on the audience and the document type. When in doubt, prefer option 1 or 2.

> **Non-STE:** The attacker can exploit the race condition to achieve arbitrary code execution.
>
> **STE:** A user can use the timing problem to run their own code in the process. A race condition is a fault where two operations happen at the same time and the result depends on the order. (Option 1: split + clarifying note.)

### Code Comments That Quote an Algorithm Name

When you document an algorithm with a standard name (for example, "Dijkstra's shortest path," "QuickSort," "Two-Phase Commit"), the algorithm name is a technical noun (Rule 1.5). Keep the algorithm name unchanged even if it contains unapproved words. Your description of what the algorithm does must use approved words.

> **Non-STE:** The `QuickSort` algorithm orchestrates the partitioning of the array to facilitate ordered output.
>
> **STE:** The `QuickSort` algorithm sorts the array. It selects a pivot element and moves smaller elements before it and larger elements after it.

## Grammar Notes

### The Parts-of-Speech Constraint

The original ASD-STE100 Rule 9.1 emphasizes that a word-for-word replacement is only possible when the approved alternative has the same part of speech as the word it replaces. This constraint is the most frequent reason that you must restructure a sentence.

In code documentation, the parts-of-speech constraint applies with additional complexity because code documentation mixes natural language with code symbols. A word in your documentation can be:

1. A natural language word subject to STE-Code rules.
2. A code keyword in code font (technical noun, Rule 1.5).
3. A framework or library name (technical noun, Rule 1.5).
4. A parameter name or variable name (technical noun, Rule 1.5).

When you evaluate if a word-for-word replacement is possible, first identify which category the word belongs to. If the word is in categories 2, 3, or 4, it is not subject to replacement. If it is in category 1, check the STE-Code dictionary for an approved alternative with the same part of speech.

### Adjective-to-Verb Restructuring

A common pattern in Rule 9.1 is the change from an adjective to a verb. When an unapproved adjective describes a state, the sentence frequently uses "is + adjective" or "must be + adjective." The approved alternative is frequently a verb. To use the verb, you must restructure the sentence around an action. The pattern is:

1. Identify the adjective (for example, "visible").
2. Find the approved verb alternative (for example, "see").
3. Identify the agent who does the action (frequently "you").
4. Restructure: "X is visible" becomes "make sure that you can see X."

This pattern applies to many code documentation scenarios: "is configurable" becomes "you can set"; "is accessible" becomes "you can get to" or "you can open"; "is extensible" becomes "you can add to."

> **Non-STE:** The configuration panel is accessible only to administrators.
>
> **STE:** Only administrators can open the configuration panel.

### Noun-to-Verb Restructuring

Another common pattern is the change from a noun to a verb. When an unapproved noun names an action, the approved alternative is frequently a verb. The pattern is:

1. Identify the noun that names an action (for example, "retrieval," "validation," "execution").
2. Find the approved verb alternative (for example, "get," "check," "do").
3. Remove the light verb that carries the noun (for example, "perform," "carry out," "conduct").
4. Restructure: "perform the retrieval of X" becomes "get X."

This pattern is especially common in API documentation and formal technical specifications where nominalizations (action nouns) are used to sound formal. The STE-Code version is always shorter and clearer.

> **Non-STE:** The service performs the validation of each request before it sends a response.
>
> **STE:** The service checks each request before it sends a response.

### Splitting Long Sentences

When a word-for-word replacement is not sufficient, the restructured sentence is frequently longer than the original because approved words are simpler and need more context. Sometimes the restructured sentence becomes too long (more than 20 words for a procedural sentence or 25 words for a descriptive sentence). In this case, you must split the sentence.

The split point is usually:

- Before a conjunction ("and," "or," "but").
- Before a conditional clause ("if," "when").
- Between the cause and the effect.
- Between the problem and the solution.

After splitting, make sure that the first sentence has a complete meaning and the second sentence does not depend on the first sentence for its grammatical subject.

> **Non-STE:** The cache stores the result of the query and returns it on the next call if the data has not changed and the time to live has not expired.
>
> **STE:** The cache stores the result of the query. It returns the result on the next call if the data has not changed. It also returns the result if the time to live has not expired.

### Removing Unnecessary Information

The original ASD-STE100 notes that "frequently, a word-for-word replacement is impossible because the word has no synonym that is sufficiently close in meaning. You must think of what you are trying to say and, frequently, some of the meaning must be lost."

This is also true for code documentation. Some sentences in code documentation contain information that is not necessary for the reader to complete a task. When a word-for-word replacement fails and a restructuring would make the sentence too long, examine if the information is necessary. Remove:

- Marketing adjectives ("robust," "scalable," "enterprise-grade").
- Redundant modifiers ("completely," "totally," "absolutely").
- Implementation details that belong in the code, not the documentation.
- Historical context that belongs in a changelog or an architecture decision record.

> **Non-STE:** This highly robust, enterprise-grade caching layer completely eliminates all redundant database round-trips.
>
> **STE:** This cache stores the result of the query. The application does not get the same data from the database again.

## Cross-References

This rule interacts with many other rules in the STE-Code system. The most important cross-references are:

- **Rule 1.1 (Use Approved Words):** Rule 9.1 is the fallback when Rule 1.1 cannot be satisfied with a word-for-word replacement. Always try a word-for-word replacement first. Only use Rule 9.1 when the replacement fails.
- **Rule 1.4 (Keep Sentences Short and Simple):** When you restructure a sentence with Rule 9.1, keep it short and use simple verb forms, even if the restructured sentence is longer than the original.
- **Rule 1.5 (Technical Code Nouns):** Code keywords, framework names, and library names are technical nouns and are not subject to replacement. When a sentence contains a technical noun and also an unapproved word, you must restructure only the parts of the sentence that are not technical nouns.
- **Rule 1.7 (Do Not Use Technical Nouns as Verbs):** When a technical noun is used as a verb (for example, "to docker the application"), you must restructure the sentence. Rule 9.1 gives the method for restructuring.
- **Rule 1.12 (Technical Verbs):** Technical verbs like "build," "deploy," "test," and "lint" are approved. Do not replace them. Rule 9.1 applies only to non-technical words in descriptive prose.
- **Rule 3.1 (Use Simple Verb Tenses):** When you restructure a sentence with Rule 9.1, use only the simple present, simple past, or imperative. Do not introduce continuous or perfect tenses.
- **Rule 5.1 (Short Sentences):** After restructuring, check that the new sentence is not longer than 20 words (procedural) or 25 words (descriptive). If it is longer, split it further or remove unnecessary information.
- **Rule 6.1 (Active Voice):** When possible, restructure the sentence in the active voice. Active voice makes the agent clear and helps you select the correct approved verb.
- **Rule 9.2 (Use Each Approved Word Correctly):** After you restructure a sentence with Rule 9.1, make sure that each approved word in the new sentence is used with its approved meaning. Rule 9.2 applies to the restructured sentence.
- **Rule 9.3 (Do Not Make Phrasal Verbs):** When you restructure a sentence, do not introduce phrasal verbs. For example, do not restructure "initiate the process" to "kick off the process." Use "start the process."
- **Rule 9.4 (Consistent Style):** When you restructure a sentence about a concept, use the same construction for all sentences about that concept in the document. Consistency is as important as correctness.

> **See also:** Rule 1.1 — Use Approved Words; Rule 1.4 — Keep Sentences Short and Simple; Rule 1.5 — Technical Code Nouns; Rule 1.7 — Do Not Use Technical Nouns as Verbs; Rule 1.12 — Technical Verbs; Rule 3.1 — Use Simple Verb Tenses; Rule 5.1 — Short Sentences; Rule 6.1 — Active Voice; Rule 9.2 — Use Each Approved Word Correctly; Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs; Rule 9.4 — When You Select Terminology or Wording, Always Use a Consistent Style

---

<!-- a-sec9-rule9.2.md -->

# Rule 9.2 — Use Each Approved Word Correctly

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec9-rule9.2](ste-code/grouped/), Rule 9.2
> **Domain:** Code documentation (API docs, README files, docstrings, commit messages, error messages, generated code)

## Original Rule

Use each approved word correctly.

Some STE-approved words have meanings that are applicable only in some contexts (restricted meaning). Before you use a word, read its definition in the approved meaning column of the dictionary. Words frequently have many different meanings in standard English. In STE, approved words usually only have one approved meaning. Other meanings that the word can have in standard English are not approved.

Always make sure that the word that you select has the correct meaning in the applicable context.

Also, make sure that you use approved words as their approved part of speech. In English, words usually do not have different forms that immediately show their function in a sentence. Thus, readers can frequently think differently about the same word. To make sentences clearer, an approved word can usually only have one function (part of speech). In STE, use each approved word as the approved part of speech.

There are a small number of words that are approved as more than one part of speech and have more than one meaning. These words are important and frequently occur in technical English.

## STE-Code Adaptation

> **See also:** Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient; Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs

Use each approved word correctly in code documentation.

Some words in the controlled terminology have restricted meanings that apply only in specific contexts. Before you use a word, read its definition in the approved meaning column of the controlled terminology. Words frequently have many different meanings in standard English. In the controlled terminology, approved words usually have only one approved meaning. Other meanings that the word can have in standard English are not approved.

Always make sure that the word that you select has the correct meaning in the applicable code documentation context.

Also, make sure that you use approved words as their approved part of speech. In English, words do not usually have different forms that immediately show their function. Thus, use each approved word as the approved part of speech only.

A small number of words are approved as more than one part of speech and have more than one meaning. These words are important and occur frequently in software development documentation.

### Examples

> *Adapted from spec pair:* Non-STE: "Wear protective clothing."  |  STE: "Use (or put on) protective clothing." — in ASD-STE100 the word "wear" is approved only with the meaning "to become damaged by friction," not "to have on one's body." This restriction carries over: a word may be approved for one meaning only.
> *Adapted from spec pair:* Non-STE: "When the pressure goes down, lift the cover."  |  STE: "When the pressure decreases, lift the cover." — a verb combined with a preposition can imply physical movement; use the single approved verb for the numeric or state change.
> *Adapted from spec pair:* Non-STE: "Flush the pipes with a disinfectant solution." / "Make sure that the surface is flush with the mating surface."  |  STE: same wording — "flush" is approved as both a verb ("to remove remaining data from a buffer") and an adjective ("where one surface fully touches a different surface"). It is the primary example of a word approved as more than one part of speech.

> **Non-STE:** Execute the initialization script before you start the server.
>
> **STE:** Run the initialization script before you start the server.

(The word "execute" is not approved in STE-Code. In standard English it can mean "to carry out a death sentence" or "to run a program," but STE-Code gives only one approved word for "to run a program": "run." Use "run" for this context.)

Realistic code-documentation context — a Python test fixture docstring:

```python
# Non-STE docstring
def start_integration_server():
    """Execute the initialization script before you start the server."""
    subprocess.run(["./init.sh"], check=True)
    subprocess.run(["./server", "--port", "8080"], check=True)


# STE docstring
def start_integration_server():
    """Run the initialization script before you start the server."""
    subprocess.run(["./init.sh"], check=True)
    subprocess.run(["./server", "--port", "8080"], check=True)
```

> **Non-STE:** When the error count goes down, restart the service.
>
> **STE:** When the error count decreases, restart the service.

(The verb "goes" together with the preposition "down" makes a phrase that refers to physical movement. "Decrease" is better because it refers to the error count, a number, not to a physical indicator that monitors the count.)

Realistic code-documentation context — a runbook note in Markdown:

```markdown
## Recovery

Non-STE: When the error count goes down for 5 minutes, restart the service to clear the circuit breaker.

STE: When the error count decreases for 5 minutes, restart the service to clear the circuit breaker.
```

> **Non-STE:** Log the exception details to the output stream.
>
> **STE:** Write the exception details to the log.

(The word "log" is approved as a noun, but not as a verb. Use the approved noun "log" with the approved verb "write.")

Realistic code-documentation context — a Python exception handler docstring:

```python
# Non-STE
def handle_error(exc: Exception) -> None:
    """Log the exception details to the output stream."""
    logger.error("error: %s", exc)


# STE
def handle_error(exc: Exception) -> None:
    """Write the exception details to the log."""
    logger.error("error: %s", exc)
```

> **Non-STE:** The config help shows all available command-line options.
>
> **STE:** The configuration help text shows all available command-line options.

(The word "help" is approved as a verb, but not as a noun. Use the approved noun phrase "help text" or "help information.")

Realistic code-documentation context — a README section that describes the `--help` flag:

```markdown
## Get help

Non-STE: The config help shows all available command-line options.

STE: The configuration help text shows all available command-line options,
including `--port` and `--verbose`.
```

> **Non-STE:** The recursive call damaged the call stack.
>
> **STE:** The recursive call caused damage to the call stack.

(The word "damage" is approved as a noun, but not as a verb. Use "cause damage" or "do damage" instead of the verb form.)

Realistic code-documentation context — an inline comment in a C crash report:

```c
/* Non-STE: The recursive call damaged the call stack and corrupted the return addresses. */

/* STE: The recursive call caused damage to the call stack and corrupted the return addresses. */
```

> **STE:** Flush the output buffer before you close the file handle.

("Flush" is a verb here with the approved meaning "to remove remaining data from a buffer.")

Realistic code-documentation context — a file writer docstring:

```python
def close_writer(self) -> None:
    """Flush the output buffer before you close the file handle."""
    self.buffer.flush()
    self.handle.close()
```

> **STE:** Make sure that the connector is flush with the port.

("Flush" is an adjective here with the approved meaning "where one surface fully touches a different surface." The word "flush" is approved as both a verb and an adjective because the different positions and contexts make it easy to see their function.)

Realistic code-documentation context — a hardware setup doc:

```markdown
## Install the cable

Push the connector in until it stops. Make sure that the connector is flush
with the port before you tighten the screw.
```

## Code-Domain Explanation

Rule 9.2 is the quality-control rule of the STE-Code system. It makes sure that every approved word in your documentation is used with its correct meaning and its correct part of speech. This is more difficult in code documentation than in general technical English because code documentation mixes natural language with code symbols, and many words have specialized meanings in software engineering that they do not have in other technical fields.

In the original ASD-STE100, most approved words have exactly one approved meaning and one approved part of speech. This is intentional. When a word can mean only one thing, the reader never needs to guess which meaning you intend. The same principle applies to code documentation: each approved word in your prose must have one clear meaning. When a word could mean two different things in a software context, you must choose a different word or add context that removes the ambiguity.

### README Files

README files introduce a project to new developers. They must be clear on first reading. Rule 9.2 applies to README files in these ways:

- Every verb in a README must be an approved verb used in its approved meaning. Do not use "leverage" when you mean "use." Do not use "facilitate" when you mean "help" or "let you."

  ```markdown
  Non-STE: You can leverage the cache layer to facilitate faster lookups.
  STE:     You can use the cache layer to help you do faster lookups.
  ```

- Every noun that describes a concept must be an approved noun. Do not use "functionality" when you mean "feature." Do not use "capability" when you mean "can."

  ```markdown
  Non-STE: This release adds logging functionality for the export capability.
  STE:     This release adds a logging feature. You can now export logs.
  ```

- The word "build" is approved as both a noun and a verb. In a README, "build the project" (verb, imperative) and "the build output" (noun, the result) are both correct. But "the build" used to mean "the build process" is less clear. Prefer "the build process" or "when you build the project."

  ```markdown
  Non-STE: Run the tests after the build.
  STE:     Run the tests after you build the project.   # or: ... after the build process.
  ```

- The word "run" is approved as a verb. Do not use it as a noun ("do a run of the tests" must be "run the tests"). The exception is when "run" is part of a technical noun phrase like "test run" or "dry run," which are technical nouns (Rule 1.5).

  ```markdown
  Non-STE: Do a run of the test suite before you merge.
  STE:     Run the test suite before you merge.   # or: Do a test run before you merge.
  ```

### API Documentation

API documentation must be precise because developers use it as a reference while writing code. Rule 9.2 applies strictly:

- The word "get" is approved as a verb meaning "to obtain." In HTTP API documentation, "GET" (uppercase, the HTTP method) is a technical noun (Rule 1.5). Do not confuse the two. Write: "Send a GET request to this endpoint to get the user data."

  ```http
  # Non-STE: Make a GET to /users to retrieve the user data.
  # STE:     Send a GET request to /users to get the user data.
  GET /users HTTP/1.1
  Host: api.example.com
  ```

- The word "set" is approved as a verb meaning "to put into a specified state" and as a noun meaning "a group of related items." In API documentation, use "set the timeout value" (verb) and "a set of endpoints" (noun). Do not use "set" to mean "configured" as an adjective ("the set timeout value" is ambiguous; use "the timeout value that you set").

  ```markdown
  Non-STE: The set timeout value applies to all requests.
  STE:     The timeout value that you set applies to all requests.
  ```

- The word "check" is approved as a verb meaning "to make sure that something is correct." Do not use it as a noun ("do a check" must be "check"). The exception is when "check" is part of a technical noun like "type check" or "health check" (Rule 1.5).

  ```markdown
  Non-STE: Do a check before you deploy.
  STE:     Check before you deploy.   # or: Do a health check before you deploy.
  ```

- The word "return" is approved as a verb meaning "to go back" or "to give back." In API documentation, "the function returns a value" is correct. "The return value" is also correct because "return" modifies "value" (it is a noun adjunct, not a standalone noun). But "the return of the function" is not approved because "return" is used as a standalone noun.

  ```typescript
  // Non-STE: The return of the function is a User object.
  // STE:     The function returns a User object.   # or: The return value is a User object.
  function getUser(id: string): User { /* ... */ }
  ```

### Docstrings and Inline Comments

Docstrings and inline comments are short and appear next to the code they describe. Rule 9.2 applies with these considerations:

- The word "do" is approved as a verb meaning "to perform an action." In docstrings, use "do" as a main verb only when the action is general: "Do the setup before you call this function." For specific actions, use the specific verb: "Run the database migration before you call this function."

  ```python
  # Non-STE: Do a database migration before you call this function.
  # STE:     Run the database migration before you call this function.
  ```

- The word "make" is approved as a verb meaning "to create." Do not use it as a light verb in phrases like "make a call" (use "call") or "make an update" (use "update"). The exception is when the object of "make" is a thing that you create: "make a copy of the file" is correct because the copy is a new thing. "Make a request" is less good; prefer "send a request."

  ```python
  # Non-STE: Make a call to the upstream service.
  # STE:     Call the upstream service.

  # Non-STE: Make a request to the API.
  # STE:     Send a request to the API.

  # STE (acceptable): Make a copy of the config file before you change it.
  ```

- The word "use" is approved as a verb. Do not confuse it with "using" as a preposition meaning "by means of." In C# and some other languages, `using` is a keyword for resource management. In docstrings, the keyword `using` in code font is a technical noun (Rule 1.5). In prose, "use" is the approved verb. Do not write "Using this method, you can..." Write "Use this method to..." or "You can use this method to..."

  ```csharp
  /// Non-STE: Using this method, you can open the file and read it.
  /// STE:     Use this method to open the file and read it.
  public void OpenAndRead(string path) { /* ... */ }
  ```

### Commit Messages

Commit messages have a strict format. Rule 9.2 applies to the summary line and the body:

- The summary line must use the imperative mood with an approved verb: "Add feature," "Remove deprecated method," "Set default timeout." Do not use unapproved verbs in the summary: "Implement feature" must be "Add feature" (unless "implement" is a technical verb for your project, Rule 1.12). "Introduce breaking change" must be "Add breaking change" or restructured.

  ```text
  Non-STE: Implement retry logic for the uploader
  STE:     Add retry logic to the uploader

  Non-STE: Introduce breaking change to the config schema
  STE:     Add breaking change to the config schema
  ```

- The word "fix" is approved as a verb. "Fix the memory leak" is correct. But "fix" as a noun ("a fix for the bug") is not approved. Use "correction" or restructure: "correct the bug."

  ```text
  Non-STE: Add a fix for the null-pointer bug
  STE:     Correct the null-pointer bug

  STE (acceptable): Fix the null-pointer bug
  ```

- The word "update" is approved as a verb meaning "to make something more current." Do not use it as a noun ("an update to the config" must be "an update of the config" or restructure to "update the config").

  ```text
  Non-STE: Ship an update to the config
  STE:     Update the config
  ```

### Error Messages

Error messages must tell the user what is wrong and what to do. Rule 9.2 applies with special strictness because error messages are read under stress:

- Use "cannot" (the approved negative form of "can"). Do not use "unable to" or "failed to" when "cannot" is sufficient. Write "Cannot open the config file" instead of "Failed to open the config file" or "Unable to open the config file."

  ```text
  Non-STE: Failed to open the config file
  STE:     Cannot open the config file

  Non-STE: Unable to connect to the database
  STE:     Cannot connect to the database
  ```

- The word "must" is approved to express a requirement. In error messages, use "must" only when the user must do something to continue: "You must set the API key before you can use this feature." Do not use "must" to describe a system state: "The file must exist" is less clear than "The file does not exist."

  ```text
  Non-STE: The config file must exist.
  STE:     The config file does not exist.

  STE (acceptable): You must set the API key before you can use this feature.
  ```

- The word "if" is approved as a conjunction for conditions. In error messages, use "if" to give the user a conditional action: "If the problem continues, look at the log for more data."

  ```text
  STE: If the problem continues, look at the log for more data.
  ```

### Generated Code and Automated Output

When you document generated code, the generated symbols (function names, variable names, class names) are technical nouns (Rule 1.5) and are not subject to Rule 9.2. However, your prose that describes the generated code must follow Rule 9.2. If a generated symbol uses a word that is unapproved in its meaning or part of speech, keep the symbol unchanged but describe its function with approved words.

```python
# Generated by an OpenAPI client generator (kept unchanged):
def utilize_config(self) -> None:
    """Configure the client from the loaded spec."""
    self._apply_settings()

# Your documentation of the generated symbol:
# The `utilize_config()` function uses the configuration to set
# the application state. (The word "utilize" appears only inside the
# symbol name in code font; your prose uses the approved verb "uses".)
```

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Object-oriented documentation uses class hierarchies, interfaces, and design patterns as its organizing structure. Rule 9.2 applies to these patterns as follows:

- The word "extend" is a keyword in Java, C++, and many other languages. In code font, `extend` is a technical noun (Rule 1.5). In prose, "extend" is an unapproved verb. Do not write "This class extends the base class." Write "This class is a child of the base class" or "This class inherits from the base class" (where "inherits" is a technical verb, Rule 1.12). If the sentence refers to the keyword, use code font: "Put `extends BaseClass` in the class declaration."

  ```java
  // Non-STE docstring: This class extends the base class to add retry logic.
  // STE docstring:     This class is a child of the base class. It adds retry logic.
  public class RetryClient extends BaseClient { /* ... */ }
  ```

- The word "implement" is a keyword in Java and C#. In code font, `implements` is a technical noun. In prose, "implement" is an unapproved verb in the context of interfaces. Write "This class uses the `Serializable` interface" instead of "This class implements `Serializable`." When you describe the act of writing code for a method, use "write" or "add": "Write the `save` method" instead of "Implement the `save` method."

  ```java
  // Non-STE docstring: This class implements the `Serializable` interface.
  // STE docstring:     This class uses the `Serializable` interface.
  public class User implements Serializable { /* ... */ }
  ```

- The word "override" is a keyword in Java, C#, and C++. In code font, `@Override` or `override` is a technical noun. In prose, do not use "override" as a verb. Write "This method replaces the parent method" instead of "This method overrides the parent method." When you refer to the keyword, use code font: "Put `@Override` before the method."

  ```java
  // Non-STE docstring: This method overrides the parent method.
  // STE docstring:     This method replaces the parent method.
  @Override
  public String toString() { /* ... */ }
  ```

- The word "abstract" is a keyword in Java and C#. In code font, `abstract` is a technical noun. In prose, "abstract" as an adjective is not approved (it does not appear in the STE-Code dictionary with this meaning). Write "This class is a base class. You cannot make an instance of it" instead of "This is an abstract class." When you refer to the keyword, use code font.

  ```java
  // Non-STE docstring: This is an abstract class for all handlers.
  // STE docstring:     This is a base class for all handlers. You cannot make an instance of it.
  public abstract class Handler { /* ... */ }
  ```

> **Non-STE:** The `PaymentProcessor` abstract class implements the `TransactionHandler` interface and provides a default implementation for the `validate` method, which subclasses can override.
>
> **STE:** The `PaymentProcessor` base class uses the `TransactionHandler` interface. It gives a default `validate` method. Child classes can replace this method.

*Principles applied: P1, P2, P5, P7. "Abstract" in prose is not approved; "base class" is clearer. "Implements" as a verb is replaced with "uses." "Provides a default implementation" is restructured to "gives a default method." "Override" is replaced with "replace." The long sentence is split into three shorter sentences.*

Realistic code-documentation context — a Java class header comment:

```java
/**
 * Non-STE: The PaymentProcessor abstract class implements the
 * TransactionHandler interface and provides a default implementation for
 * the validate method, which subclasses can override.
 *
 * STE: The PaymentProcessor base class uses the TransactionHandler
 * interface. It gives a default validate method. Child classes can
 * replace this method.
 */
public abstract class PaymentProcessor implements TransactionHandler {
    public void validate(Transaction t) { /* default behaviour */ }
}
```

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, type transformations, and immutable data. Rule 9.2 applies to the unique vocabulary of functional programming:

- The word "map" is approved as a noun meaning "a visual representation of an area." In functional programming, `map` is a function name (technical noun, Rule 1.5) and a general operation. In prose, do not use "map" as a verb meaning "to apply a function to each element." Write "apply the function to each element of the list" instead of "map the function over the list." When you refer to the `map` function itself, use code font: "Use `map` to apply a function to each element."

  ```haskell
  -- Non-STE docstring: Maps the parser function over the input list.
  -- STE docstring:     Applies the parser function to each element of the input list.
  parseAll :: [String] -> [Value]
  parseAll = map parse
  ```

- The word "reduce" is not approved as a verb in STE-Code. In functional programming, `reduce` (or `fold`) is a function name (technical noun, Rule 1.5). In prose, write "combine the elements of the list into a single value" instead of "reduce the list." When you refer to the function, use code font: "Use `reduce` to combine all elements."

  ```clojure
  ;; Non-STE docstring: Reduces the list to a single sum.
  ;; STE docstring:     Combines the elements of the list into a single sum.
  (defn total [xs] (reduce + 0 xs))
  ```

- The word "filter" is approved as a noun meaning "a device that removes unwanted parts." In functional programming, `filter` is a function name (technical noun, Rule 1.5). In prose, do not use "filter" as a verb. Write "remove elements that do not match the condition" instead of "filter the list." When you refer to the function, use code font: "Use `filter` to remove unwanted elements."

  ```elixir
  # Non-STE docstring: Filters the list to keep only active users.
  # STE docstring:     Removes elements that do not match the condition (keep only active users).
  def active_users(users), do: Enum.filter(users, & &1.active)
  ```

- The word "apply" is not approved in STE-Code (use "use" or "put on"). In functional programming, `apply` (or `ap`) is a function name associated with applicative functors. Keep the function name in code font as a technical noun. In prose, write "use the function on the value" instead of "apply the function to the value."

  ```haskell
  -- Non-STE docstring: Applies the function to the value inside the functor.
  -- STE docstring:     Uses the function on the value inside the functor.
  runReader :: Reader r a -> r -> a
  ```

> **Non-STE:** The `sequence` function maps an `Effect`-producing function over a list of elements, then collects all the effects into a single `Effect` that produces a list.
>
> **STE:** The `sequence` function applies an `Effect`-producing function to each element of a list. Then it collects all the effects into one `Effect` that gives a list.

*Principles applied: P1, P2, P5. "Maps" as a verb is replaced with "applies to each element." "Collects" is an unapproved verb; kept here because it is the name of the operation in the type signature context — but in a stricter application, "puts together" would be used. The sentence is split.*

Realistic code-documentation context — a Haskell module comment:

```haskell
-- Non-STE: The sequence function maps an Effect-producing function over a
-- list of elements, then collects all the effects into a single Effect
-- that produces a list.
--
-- STE: The sequence function applies an Effect-producing function to each
-- element of a list. Then it collects all the effects into one Effect that
-- gives a list.
sequence :: [Effect a] -> Effect [a]
```

### Procedural Documentation (C, Go, Bash)

Procedural documentation describes step-by-step operations, memory management, and system interaction. Rule 9.2 applies to these patterns:

- The word "free" is approved as a verb meaning "to release" and as an adjective meaning "not restricted." In C documentation, `free()` is a function name (technical noun, Rule 1.5). In prose, use "free" as a verb: "free the memory" is correct. "The memory is free" (adjective) is also correct. Do not confuse the two: "free the pointer" is ambiguous; write "free the memory that the pointer points to."

  ```c
  /* Non-STE: Free the pointer when you finish. */
  /* STE:     Free the memory that the pointer points to when you finish. */
  free(ptr);
  ```

- The word "open" is approved as a verb meaning "to make accessible." In C and Go, `open()` is a function name. In prose, "open the file" is correct. Do not use "open" as an adjective in the sense of "available": "the port is open" could mean "the port is not closed" (physical) or "the port is available for connections." Prefer "the port is available" for the second meaning.

  ```go
  // Non-STE: Open the file, then read the port. The port is open for connections.
  // STE:     Open the file, then read the port. The port is available for connections.
  f, _ := os.Open("data.txt")
  ```

- The word "close" is approved as a verb and as an adjective meaning "near." In C and Go, `close()` is a function name. In prose, "close the file" (verb) is correct. Do not use "close" as an adjective meaning "near" in a technical context where it could be confused with the verb: "close the connection" is clear; "the close port" is ambiguous. Use "the nearest port" for proximity.

  ```c
  /* Non-STE: Close the file and use the close port for the next socket. */
  /* STE:     Close the file and use the nearest port for the next socket. */
  fclose(fp);
  ```

- The word "read" is approved as a verb. In C and Go, `read()` is a function name. In prose, "read the data from the buffer" is correct. Do not use "read" as a noun: "the read operation" is acceptable as a noun adjunct, but "do a read" must be "read the data."

  ```go
  // Non-STE: Do a read from the buffer to get the header.
  // STE:     Read the data from the buffer to get the header.
  n, _ := buf.Read(header)
  ```

> **Non-STE:** After you allocate memory on the heap with `malloc`, you must deallocate it with `free` when the program no longer needs it. Failing to free allocated memory causes memory leaks.
>
> **STE:** After you get memory from the heap with `malloc`, you must free the memory with `free` when the program does not need it. If you do not free the memory, the program uses more memory over time.

*Principles applied: P1, P2, P11. "Allocate" is replaced with "get" (the memory comes from the heap). "Deallocate" is not approved; "free" is the approved verb. "Failing to" becomes "If you do not." "Memory leaks" is jargon (P10); restructured to "uses more memory over time."*

Realistic code-documentation context — a C function comment:

```c
/* Non-STE: After you allocate memory on the heap with malloc, you must
 * deallocate it with free when the program no longer needs it. Failing to
 * free allocated memory causes memory leaks.
 *
 * STE: After you get memory from the heap with malloc, you must free the
 * memory with free when the program does not need it. If you do not free the
 * memory, the program uses more memory over time.
 */
void process(void) {
    char *buf = malloc(1024);
    /* ... use buf ... */
    free(buf);
}
```

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state, not procedures. Rule 9.2 applies to the stative vocabulary of declarative systems:

- The word "create" is not approved in STE-Code (use "make"). In SQL, `CREATE` is a keyword (technical noun, Rule 1.5). In prose, do not use "create" as a verb. Write "make a table" instead of "create a table." When you refer to the SQL keyword, use code font: "Use `CREATE TABLE` to make a new table."

  ```sql
  -- Non-STE prose: Create a table for the users.
  -- STE prose:     Make a table for the users.
  -- keyword in code font:
  CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
  ```

- The word "select" is not approved in STE-Code (use "choose" or "get" depending on context). In SQL, `SELECT` is a keyword (technical noun, Rule 1.5). In prose, write "get rows from the table" instead of "select rows from the table." When you refer to the SQL keyword, use code font: "The `SELECT` statement gets data from a table."

  ```sql
  -- Non-STE prose: Select rows from the table where active is true.
  -- STE prose:     Get rows from the table where active is true.
  SELECT * FROM users WHERE active = TRUE;
  ```

- The word "drop" is approved as a verb meaning "to let fall." In SQL, `DROP` is a keyword (technical noun, Rule 1.5). In prose, write "remove the table" instead of "drop the table" unless you are directly quoting the SQL statement. When you refer to the SQL keyword, use code font.

  ```sql
  -- Non-STE prose: Drop the table if it exists.
  -- STE prose:     Remove the table if it exists.
  DROP TABLE IF EXISTS users;
  ```

- The word "apply" is not approved. In Terraform, `terraform apply` is a command (technical noun, Rule 1.5). In prose, write "use `terraform apply` to make the changes" instead of "apply the configuration."

  ```hcl
  # Non-STE prose: Apply the configuration to make the bucket.
  # STE prose:     Use `terraform apply` to make the bucket.
  resource "aws_s3_bucket" "logs" { bucket = "app-logs" }
  ```

> **Non-STE:** The `Deployment` resource creates and manages a set of replicated Pods. It ensures that the specified number of Pods are running at all times.
>
> **STE:** The `Deployment` resource makes and controls a set of Pod copies. It makes sure that the set number of Pods runs at all times.

*Principles applied: P1, P2, P11. "Creates" replaced with "makes." "Manages" is unapproved; replaced with "controls." "Replicated" is unapproved; replaced with "copies." "Ensures" is unapproved; replaced with "makes sure." "Specified" is unapproved; replaced with "set." "Running" (adjective) is restructured to "runs" (verb).*

Realistic code-documentation context — a Kubernetes manifest comment:

```yaml
# Non-STE: The Deployment resource creates and manages a set of replicated
# Pods. It ensures that the specified number of Pods are running at all times.
#
# STE: The Deployment resource makes and controls a set of Pod copies.
# It makes sure that the set number of Pods runs at all times.
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
```

### Systems Documentation (Rust Ownership, C Memory)

Systems documentation has the strictest requirements for word precision because it describes memory safety, ownership, and lifetimes. Rule 9.2 applies with special attention to words that have both a standard English meaning and a systems-programming meaning:

- The word "move" is approved as a verb meaning "to change position." In Rust, `move` is a keyword for ownership transfer (technical noun, Rule 1.5). In prose, when you describe Rust ownership, "move" as a verb is acceptable as a technical verb (Rule 1.12) because it names a specific Rust operation. But make sure the context makes the Rust meaning clear: "When you move a value, the first variable can no longer use it."

  ```rust
  // Non-STE docstring: Transfers ownership of the buffer to the worker.
  // STE docstring:     Moves the buffer to the worker. The first variable
  //                   can no longer use the buffer.
  let buf = String::from("data");
  let worker = buf; // move
  ```

- The word "borrow" is not approved as a verb in STE-Code. In Rust, `borrow` (via `&`) is an ownership concept. In prose, do not use "borrow" as a verb. Write "get a reference to the value" instead of "borrow the value." The Rust concept of borrowing is a technical noun: "the borrow checker" is correct because "borrow" modifies "checker."

  ```rust
  // Non-STE docstring: Borrow the value to read it without a copy.
  // STE docstring:     Get a reference to the value to read it without a copy.
  let r: &String = &buf;
  ```

- The word "drop" is approved as a verb meaning "to let fall." In Rust, `drop` is a trait and a function (technical noun, Rule 1.5). In prose, when describing the Rust concept, use "drop" as a technical verb (Rule 1.12): "The value drops when it goes out of scope." This is acceptable because "drop" in Rust has a specific, well-defined meaning.

  ```rust
  // STE docstring: The value drops when it goes out of scope.
  fn scoped() {
      let v = String::from("x");
  } // v drops here
  ```

- The word "own" is not approved as a verb in STE-Code. In Rust, ownership is a core concept. In prose, do not use "own" as a verb. Write "the variable has the value" or "the value is in the variable" instead of "the variable owns the value." The noun "ownership" is a technical noun (Rule 1.5): "Rust's ownership system" is correct.

  ```rust
  // Non-STE docstring: The variable owns the value and frees it on drop.
  // STE docstring:     The variable has the value and frees it on drop.
  let s = String::from("hi");
  ```

> **Non-STE:** When a variable goes out of scope, Rust automatically drops the value, freeing the memory it owned. You do not need to manually deallocate memory.
>
> **STE:** When a variable goes out of scope, Rust automatically drops the value and frees the memory. You do not need to free memory manually.

*Principles applied: P1, P2, P5. "Owned" as a verb is replaced with restructured sentence. "Automatically" is an approved adverb. "Manually" is an approved adverb. "Deallocate" is not approved; "free" is used instead. The sentence is split and simplified.*

Realistic code-documentation context — a Rust function comment:

```rust
/// Non-STE: When a variable goes out of scope, Rust automatically drops the
/// value, freeing the memory it owned. You do not need to manually deallocate
/// memory.
///
/// STE: When a variable goes out of scope, Rust automatically drops the value
/// and frees the memory. You do not need to free memory manually.
fn run() {
    let data = load();
} // data drops and the memory is free
```

## Extended Examples

> **Non-STE:** The initialization function bootstraps the dependency injection container and registers all service implementations.
>
> **STE:** The initialization function starts the dependency injection container and adds all service implementations.

*Principles applied: P1, P11. "Bootstraps" is not approved; replaced with "starts" from the Synonym Table. "Registers" is not approved as a verb in this sense; "adds" is clearer. "Container" and "dependency injection" are technical nouns (Rule 1.5) and kept unchanged.*

Realistic code-documentation context — a Go startup function comment:

```go
// Non-STE: The initialization function bootstraps the dependency injection
// container and registers all service implementations.
//
// STE: The initialization function starts the dependency injection container
// and adds all service implementations.
func Initialize(services *Container) {
    services.Add(NewAuth())
    services.Add(NewBilling())
}
```

> **Non-STE:** If the validation check fails, the form will display an error message beneath the input field.
>
> **STE:** If the validation check does not pass, the form shows an error message below the input field.

*Principles applied: P1, P2. "Fails" as a verb is approved only in the sense of "to become weaker" or "to not do something." Here, "does not pass" is clearer. "Display" is in the Synonym Table (prefer "show"). "Beneath" is not approved; "below" is the approved alternative.*

Realistic code-documentation context — a JavaScript form handler docstring:

```javascript
/**
 * Non-STE: If the validation check fails, the form will display an error
 * message beneath the input field.
 *
 * STE: If the validation check does not pass, the form shows an error
 * message below the input field.
 */
function onSubmit(values) {
  if (!validate(values)) showError("Invalid input");
}
```

> **Non-STE:** The caching layer intercepts database queries and serves cached results when possible, dramatically reducing latency.
>
> **STE:** The caching layer gets database queries. When possible, it gives cached results. This decreases latency.

*Principles applied: P1, P2, P10. "Intercepts" is not approved; "gets" is the approved alternative. "Serves" as a verb meaning "to provide" is not approved; "gives" is the approved alternative. "Dramatically" is a marketing word (P10); removed. The long sentence is split into three sentences.*

Realistic code-documentation context — a Python cache docstring:

```python
class Cache:
    """Non-STE: The caching layer intercepts database queries and serves
    cached results when possible, dramatically reducing latency.

    STE: The caching layer gets database queries. When possible, it gives
    cached results. This decreases latency."""

    def get(self, key):
        return self._store.get(key)
```

> **Non-STE:** You can leverage the `--parallel` flag to execute multiple test suites concurrently, which significantly accelerates the overall test duration.
>
> **STE:** You can use the `--parallel` flag to run multiple test suites at the same time. This decreases the total test duration.

*Principles applied: P1, P11. "Leverage" is in the Synonym Table (prefer "use"). "Execute" is not approved; replaced with "run." "Concurrently" is not in the controlled terminology; "at the same time" is clearer. "Significantly" and "accelerates" are marketing words; "decreases" is the approved verb. "Overall" is replaced with "total." The sentence is split.*

Realistic code-documentation context — a pytest configuration note:

```ini
# Non-STE: You can leverage the --parallel flag to execute multiple test
# suites concurrently, which significantly accelerates the overall test duration.
#
# STE: You can use the --parallel flag to run multiple test suites at the
# same time. This decreases the total test duration.
[pytest]
addopts = --parallel
```

> **Non-STE:** Upon completion of the build pipeline, the artifacts are persisted to the configured storage backend.
>
> **STE:** When the build pipeline is complete, the system keeps the artifacts in the configured storage.

*Principles applied: P1, P2, P7, P11. "Upon" is not approved as a preposition; "When" is the approved alternative. "Completion" is not approved as a noun (the verb "complete" is approved). "Persisted" as a verb is not approved; "keeps" is the approved alternative. "Backend" is jargon (P10); removed because "storage" communicates the meaning. "Are persisted" (passive) becomes active "the system keeps."*

Realistic code-documentation context — a CI workflow comment:

```yaml
# Non-STE: Upon completion of the build pipeline, the artifacts are
# persisted to the configured storage backend.
#
# STE: When the build pipeline is complete, the system keeps the artifacts
# in the configured storage.
jobs:
  build:
    steps:
      - run: make build
      - run: cp dist/* storage/
```

> **Non-STE:** This configuration option dictates the verbosity level of the logging output, ranging from "error" to "trace."
>
> **STE:** This configuration option sets the log detail level. You can set it from "error" to "trace."

*Principles applied: P1, P2, P11. "Dictates" is not approved; "sets" is the approved alternative. "Verbosity" is not approved; "detail" is the approved alternative. "Ranging from" is replaced with "You can set it from." The sentence is split for clarity.*

Realistic code-documentation context — a config schema comment:

```json
{
  "// Non-STE": "This configuration option dictates the verbosity level of the logging output, ranging from 'error' to 'trace'.",
  "// STE": "This configuration option sets the log detail level. You can set it from 'error' to 'trace'.",
  "log_level": "info"
}
```

## Edge Cases

### Words Approved as Multiple Parts of Speech

A small number of words in the STE-Code dictionary are approved as more than one part of speech, each with a different approved meaning. These words need special attention because the same spelling appears in different grammatical roles. The original ASD-STE100 gives "flush" as the primary example: approved as a verb ("to remove remaining data from a buffer") and as an adjective ("where one surface fully touches a different surface"). In code documentation, the following words are approved as more than one part of speech:

- **"build"** — Verb: "to construct software from source code" (technical verb, Rule 1.12). Noun: "the result of a build process" or "a specific version." In a sentence, the position of "build" tells the reader its function: "Build the project" (verb, imperative) vs. "The build completed successfully" (noun, subject). When "build" is used as a noun, make sure the context makes its meaning clear. Do not write "the build" when you mean "the build output" or "the build process." Be specific.

  ```text
  Verb:    Build the project before you run the tests.
  Noun:    The build completed successfully and the artifact is in dist/.
  Avoid:   The build failed.                 # does it mean the process or the artifact?
  Prefer:  The build process failed.          # or: The build output is missing.
  ```

- **"run"** — Verb: "to start and operate software." Noun: approved only in the compound noun "test run" or "dry run" (technical noun, Rule 1.5). Do not use "run" as a standalone noun: "the run failed" must be "the test run failed" or "the program did not run correctly."

  ```text
  Verb:    Run the migration before you deploy.
  Noun:    Do a test run before you deploy.
  Avoid:   The run failed.
  Prefer:  The test run failed.               # or: The program did not run correctly.
  ```

- **"set"** — Verb: "to put into a specified state." Noun: "a group of related items." In documentation, "set the timeout" (verb) and "a set of configuration options" (noun) are both correct. The context must make the function clear. When ambiguity is possible, add a determiner or a modifier: "the set of options" (noun) vs. "you can set the options" (verb).

  ```text
  Verb:    Set the timeout to 30 seconds.
  Noun:    A set of configuration options is available.
  Ambiguous: The set timeout applies.          # "set" looks like an adjective here.
  Prefer:    The timeout value that you set applies.
  ```

- **"check"** — Verb: "to make sure that something is correct." Noun: approved only in compound technical nouns like "type check," "health check," or "lint check." Do not use "check" as a standalone noun: "do a check" must be "check" (verb) or "do a type check" (compound technical noun).

  ```text
  Verb:    Check the input before you save it.
  Noun:    Do a health check before you deploy.
  Avoid:   Do a check before you deploy.
  Prefer:  Check before you deploy.            # or: Do a health check before you deploy.
  ```

### When a Framework or Tool Name Is Also an Unapproved Word

Some framework and tool names are ordinary English words that are not approved in STE-Code. For example, "Express" (the Node.js web framework), "Flask" (the Python web framework), "Fresh" (the Deno web framework), and "FastAPI" (contains "fast," which appears in the Synonym Table only with the note that it is approved as an adjective). These names are technical nouns (Rule 1.5) and must stay unchanged in your documentation. The rule is:

1. Always put the framework name in code font or with its official capitalization so the reader knows it is a proper noun.
2. Never use the framework name as a verb (Rule 1.7). Do not write "Express your API" or "Flask your application."
3. When the framework name appears next to prose that uses the same word with a different meaning, the code font and prose font make the distinction clear: "Use `Express` to express your API routes" would be unacceptable because "express" appears both as a name and as a verb meaning "to state." Restructure: "Use the `Express` framework to write your API routes."

Realistic code-documentation context — a README for a Node.js service:

```markdown
## Routes

Non-STE: Express your API routes with the Express router.
STE:     Use the `Express` framework to write your API routes.
```

### When a Code Keyword Conflicts With an Approved Word

Some programming language keywords are spelled the same as approved STE-Code words but have a different meaning. For example:

- Rust `use` — keyword for importing names. STE-Code "use" — verb meaning "to put into service." When you document Rust code, use code font for the keyword: "Put `use std::io` at the top of the file. Then you can use the `io` module." The code font tells the reader that the first "use" is a keyword and the second "use" is prose.

  ```rust
  // Put `use std::io` at the top of the file.
  // Then you can use the `io` module to read from the console.
  use std::io;
  fn main() {
      let mut input = String::new();
      io::stdin().read_line(&mut input).unwrap();
  }
  ```

- Rust `move` — keyword for ownership transfer. STE-Code "move" — verb meaning "to change position" or technical verb for the Rust operation. When you describe Rust ownership, "move" as a technical verb (Rule 1.12) is acceptable: "When you move a value, the first variable can no longer use it." But when you describe non-Rust movement, "move" has its standard STE-Code meaning.

  ```rust
  // When you move a value, the first variable can no longer use it.
  let a = String::from("x");
  let b = a; // move
  // a can no longer use the value.
  ```

- `return` — keyword in most languages. STE-Code "return" — verb meaning "to go back" or "to give back." In documentation, "return" in prose is correct: "The function returns a string." When you refer to the keyword, use code font: "Put `return` at the end of the function."

  ```python
  # The function returns a string.
  # Put `return` at the end of the function to give back the result.
  def name() -> str:
      return "app"
  ```

- `break` — keyword for loop exit. STE-Code "break" — verb meaning "to separate into pieces." In documentation, use "break" in prose only when you mean physical separation: "Do not break the API contract" is ambiguous. Write "Do not change the API contract" unless you mean "Do not separate the API contract into parts."

  ```text
  Non-STE: Do not break the API contract.
  STE:     Do not change the API contract.
  ```

### When the Rule Should Allow Flexibility for Generated Code

Generated code (code produced by a compiler, a code generator, or an AI tool) frequently uses symbol names that contain unapproved words or use words in unapproved parts of speech. Your documentation of generated code must handle this:

1. The generated symbols themselves are technical nouns (Rule 1.5). Keep them unchanged.
2. When you describe what a generated symbol does, you can use approved words that do not match the symbol name. For example, if a generator produces `utilizeConfig()`, your description says: "The `utilizeConfig()` function uses the configuration to set the application state." The word "utilize" appears only in code font as part of the symbol name.
3. If the generated code is part of a public API that developers will call directly, consider adding a wrapper with an approved name. Document the wrapper using approved words and note that it calls the generated function.
4. If you are the author of the code generator, apply STE-Code rules to the generator's output templates so that generated symbol names use approved words from the start.

Realistic code-documentation context — an OpenAPI-generated client and an approved wrapper:

```python
# Generated (kept unchanged):
def utilizeConfig(self) -> None:
    """Generated client method."""
    ...

# Approved wrapper (document with approved words):
def use_config(self) -> None:
    """Use the configuration to set the application state.
    This function calls the generated `utilizeConfig()` function."""
    self.utilizeConfig()
```

### Quoted Error Messages and Log Output

When you quote an error message or log output from a system that does not follow STE-Code, the quoted text is data, not documentation. Keep it exactly as it appears. Your surrounding prose must follow Rule 9.2:

- Put the quoted text in quotation marks or a code block.
- Use approved words to explain what the quoted text means.
- If the quoted text uses a word in an unapproved meaning, explain the meaning with approved words.
- Do not edit the quoted text to make it follow STE-Code. The quote must be accurate.

Realistic code-documentation context — a troubleshooting section:

```markdown
## Troubleshooting

The database log shows: "FATAL: could not allocate memory for shared buffer."
This error means that the database cannot get memory for the shared buffer.
Increase the memory limit or restart the service.
```

## Grammar Notes

### The One-Meaning-Per-Word Principle

The original ASD-STE100 is built on the principle that each approved word should have exactly one approved meaning. This principle comes from aerospace documentation, where a misunderstood word can cause a fatal error. In code documentation, a misunderstood word can cause a bug, a security vulnerability, or a system failure. The same principle applies: each approved word must have one clear meaning in your documentation.

When a word has two meanings that are both common in software engineering, the STE-Code dictionary assigns only one approved meaning. The other meaning must be expressed with a different word or a phrase. This is intentional. It removes ambiguity. For example:

- "Log" is approved as a noun (the record of events). It is not approved as a verb. If you want to describe the action of adding to a log, use "write to the log."
- "Help" is approved as a verb (to assist). It is not approved as a noun. If you want to refer to help documentation, use "help text" or "help information."
- "Damage" is approved as a noun (harm or injury). It is not approved as a verb. If you want to describe causing damage, use "cause damage" or "do damage."

### Parts of Speech in the Code-Documentation Mix

In standard English, a word's part of speech is shown by its position in the sentence and by inflectional endings (-s, -ed, -ing). In code documentation, a word's part of speech is further complicated because code documentation mixes natural language with code symbols. A word in your documentation can be:

1. A natural language word whose part of speech follows English grammar rules and STE-Code restrictions.
2. A code keyword in code font (technical noun, Rule 1.5), which has no English part of speech.
3. A framework, library, or tool name (technical noun, Rule 1.5), which is a proper noun.
4. A parameter, variable, or function name (technical noun, Rule 1.5), which is a proper noun.

When you apply Rule 9.2, first identify which category the word belongs to. If the word is in category 1, check the STE-Code dictionary for its approved part of speech and approved meaning. If the word is in categories 2, 3, or 4, the part-of-speech restriction does not apply because the word is not English prose — it is a technical identifier.

### The Noun-Verb Boundary in Code Documentation

The boundary between noun and verb is the most frequent source of Rule 9.2 violations in code documentation. Many words that are used as both nouns and verbs in general software English have only one approved part of speech in STE-Code. The pattern is:

- If a word is approved only as a verb, you must restructure sentences that use it as a noun. For example, "run" is approved as a verb and as part of compound nouns like "test run." You cannot write "do a run" — write "run the program" or "do a test run."
- If a word is approved only as a noun, you must restructure sentences that use it as a verb. For example, "log" is approved as a noun. You cannot write "log the error" — write "write the error to the log."
- If a word is approved as both, you must make the function clear from context. Add determiners for nouns ("the build," "a set"), and use imperative or inflected forms for verbs ("build the project," "sets the value").

The original ASD-STE100 notes that "in English, words usually do not have different forms that immediately show their function in a sentence." This is exactly why Rule 9.2 is necessary. In standard English, "log" could be a noun or a verb, and the reader must guess from context. In STE-Code, the dictionary removes the guess by assigning one approved part of speech.

### The Adjective-Verb Distinction

Some approved words can function as adjectives when they modify a noun, even if the dictionary lists them only as verbs or nouns. This is because English allows nouns and verbs to function as noun adjuncts (a noun that modifies another noun) or participles (a verb form that functions as an adjective). The original ASD-STE100 permits this when the meaning is clear:

- "The build process" uses "build" (noun) as a noun adjunct modifying "process." This is allowed because "build" is approved as a noun and its meaning does not change.
- "The configured storage" uses "configured" (past participle of the verb "configure") as an adjective. This is allowed because "configure" is approved as a technical verb (Rule 1.12) and the past participle keeps the same meaning.
- "The running service" uses the -ing form of "run" as an adjective. The original ASD-STE100 Rule 1.4 gives guidance on when -ing forms are permitted as adjectives. In general, prefer the simple form: "the service that runs" is clearer than "the running service."

When you use an approved word in a noun-adjunct or participle role, make sure that its approved meaning does not change. If the meaning shifts (for example, "the running total" where "running" means "continuously updated," which is a different meaning from "run" as a verb), use a different construction or a different approved word.

### Using the Dictionary as the Source of Truth

Rule 9.2 cannot be applied without the STE-Code dictionary. The dictionary is the authoritative reference for which words are approved, which part of speech they are approved for, and which meaning they are approved with. Before you write any documentation, you must be familiar with the dictionary entries for the words you plan to use. When you are not sure about a word, look it up.

The dictionary also gives approved alternatives for unapproved words. When you find an unapproved word in your draft, first check if the dictionary gives an approved alternative with the same part of speech. If it does, do a word-for-word replacement. If it does not, apply Rule 9.1 to restructure the sentence. After restructuring, apply Rule 9.2 again to make sure that every word in the new sentence is used correctly.

## Cross-References

This rule is the central quality-control rule in the STE-Code system. It interacts with most other rules. The most important cross-references are:

- **Rule 1.1 (Use Approved Words):** Rule 9.2 is the rule that tells you how to use the approved words from Rule 1.1. Rule 1.1 says which words you can use. Rule 9.2 says how you must use them.
- **Rule 1.2 (Use Words Only as Their Specified Part of Speech):** This rule is a direct statement of the part-of-speech constraint. Rule 9.2 gives the detailed justification and the procedure for applying the constraint. Together, they make sure that each word appears only in its approved grammatical role.
- **Rule 1.3 (Use Words Only With Their Approved Meanings):** This rule is a direct statement of the meaning constraint. Rule 9.2 gives the detailed justification and examples. Together, they make sure that each word communicates exactly one concept.
- **Rule 1.4 (Use Only Approved Verb Forms and Adjective Forms):** When you use an approved word in a verb form or adjective form that is not in the dictionary, Rule 1.4 applies. Rule 9.2 tells you to check the dictionary for the approved part of speech. Rule 1.4 tells you which inflections are permitted.
- **Rule 1.5 (Technical Code Nouns Are Allowed):** Technical code nouns (keywords, framework names, library names, function names) are not subject to the part-of-speech and meaning restrictions of Rule 9.2. When you apply Rule 9.2, first identify technical nouns and exclude them from the check.
- **Rule 1.7 (Do Not Use Technical Nouns as Verbs):** When a technical noun is used as a verb (for example, "to docker the application"), Rule 1.7 applies. Rule 9.2 reinforces this by requiring that each word be used as its approved part of speech. If a word is approved as a noun, it cannot be used as a verb even if it is a technical term.
- **Rule 1.12 (Technical Verbs Are Allowed):** Technical verbs like "build," "deploy," "test," "lint," "compile," and "debug" are approved as verbs even if they are not in the general STE-Code dictionary. Rule 9.2 applies to technical verbs: you must use them with their correct technical meaning and not confuse them with their general-English meanings.
- **Rule 9.1 (Use a Different Sentence Construction):** When a word-for-word replacement is not sufficient because the approved alternative has a different part of speech or changes the meaning, you must use Rule 9.1 to restructure the sentence. After restructuring, apply Rule 9.2 to the new sentence.
- **Rule 9.3 (Do Not Make Phrasal Verbs):** When you use approved verbs, do not combine them with prepositions to make phrasal verbs that have unapproved meanings. Rule 9.2 tells you to use approved words with their approved meanings. Rule 9.3 prevents you from creating new meanings by combining approved words.
- **Rule 9.4 (Consistent Style):** After you apply Rule 9.2 to individual words, apply Rule 9.4 to make sure that you use the same approved words for the same concepts throughout the document and across the project.
- **The STE-Code Dictionary (A-Z):** The dictionary is the source of truth for Rule 9.2. You cannot apply this rule without consulting the dictionary. Every word you write must be checked against the dictionary's approved meaning column and approved part of speech.

> **See also:** Rule 1.1 — Use Approved Words
> **See also:** Rule 1.2 — Use Words Only as Their Specified Part of Speech
> **See also:** Rule 1.3 — Use Words Only With Their Approved Meanings
> **See also:** Rule 1.4 — Use Only Approved Verb Forms and Adjective Forms
> **See also:** Rule 1.5 — Technical Code Nouns Are Allowed
> **See also:** Rule 1.7 — Do Not Use Technical Nouns as Verbs
> **See also:** Rule 1.12 — Technical Verbs Are Allowed
> **See also:** Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient
> **See also:** Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs
> **See also:** Rule 9.4 — Consistent Style

---

<!-- a-sec9-rule9.3.md -->

# Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec9-rule9.3](ste-code/grouped/), Rule 9.3

## Original Rule

When you use two words together, do not make phrasal verbs.

In English, a verb and one or more prepositions can go together to form a "phrasal verb." This phrasal verb has a meaning that is different from the meanings of its parts. Phrasal verbs usually have two meanings: the original, more concrete meaning, and a more general and abstract meaning.

To prevent ambiguity, it is not permitted in STE to use approved words together to make a new phrase (phrasal verb).

You will not usually find phrasal verbs listed as "not approved" in the dictionary. When you write a standard English sentence in STE, always make sure that the new sentence is grammatically correct. And make sure that you use the approved words with the meaning that they have in the dictionary.

Only a small number of phrasal verbs are approved in the dictionary. They all have a restricted meaning.

## STE-Code Adaptation

> **See also:** Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient; Rule 9.2 — Use Each Approved Word Correctly

When you use two words together in code documentation, do not make phrasal verbs.

A verb and one or more prepositions can go together to form a phrasal verb with a meaning that is different from the meanings of its individual parts. Phrasal verbs usually have two meanings: the original, concrete meaning, and a more general, abstract meaning. To prevent ambiguity, do not use approved words together to make a new phrase unless the phrasal verb is specifically approved in the controlled terminology.

Replace the phrasal verb with a single approved verb that has the same meaning. When you write a standard English sentence in the controlled terminology, always make sure that the new sentence is grammatically correct and that you use the approved words with the meaning that they have in the controlled terminology.

Only a small number of phrasal verbs are approved. They all have a restricted meaning.

### Examples

> *Adapted from spec pair:* Non-STE: "Put out the fire." (abstract) / STE: "Extinguish the fire." — "put" and "out" are approved individually, but together they form a phrasal verb; the approved verb "extinguish" replaces it. | Non-STE: "Give off gas." / STE: "Release gas." — "give" and "off" are approved individually, but together they form a phrasal verb; the approved verb "release" replaces it. | Non-STE: "Carry out the test." / STE: "Do the test." — "carry" and "out" are approved individually, but together they form a phrasal verb; the approved verb "do" replaces it.

> **Non-STE:** The compiler puts out a warning when the type annotation is missing.
>
> **STE:** The compiler emits a warning when the type annotation is missing.

("Put" and "out" are approved words individually. Together, "put out" forms a phrasal verb with a meaning different from the approved meanings of "put" and "out." The approved verb "emit" has the meaning "to send out" and is the word that is most usual in code documentation.)

```python
# Non-STE — emit_warning.py
def check_annotation(node):
    """Validate the type annotation and put out a warning on failure."""
    if node.annotation is None:
        logger.warning("Missing type annotation on %s", node.name)


# STE — emit_warning.py
def check_annotation(node):
    """Validate the type annotation and emit a warning on failure."""
    if node.annotation is None:
        logger.warning("Missing type annotation on %s", node.name)
```

*Adapted from spec pair: "Put out the fire." (abstract) / "Extinguish the fire." — "put" and "out" are approved individually, but together they form a phrasal verb; the approved verb "extinguish" replaces it.*

> **Non-STE:** The function gives off an error code when the input is not valid.
>
> **STE:** The function returns an error code when the input is not valid.

("Give" and "off" are approved words individually. Together, "give off" forms a phrasal verb with a meaning different from the approved meanings of "give" and "off." The approved verb "return" has the meaning "to send back a value" and is the correct word for this context in code documentation.)

```go
// Non-STE — handler.go
func ParseInput(input []byte) (Record, error) {
    rec, err := decode(input)
    if err != nil {
        // gives off an error code that the caller must inspect
        return Record{}, ErrInvalidInput
    }
    return rec, nil
}

// STE — handler.go
func ParseInput(input []byte) (Record, error) {
    rec, err := decode(input)
    if err != nil {
        // returns an error code that the caller must inspect
        return Record{}, ErrInvalidInput
    }
    return rec, nil
}
```

*Adapted from spec pair: "Give off gas." / "Release gas." — "give" and "off" are approved individually, but together they form a phrasal verb; the approved verb "release" replaces it.*

> **Non-STE:** The cleanup task carries out the memory deallocation after each request.
>
> **STE:** The cleanup task does the memory deallocation after each request.

("Carry" and "out" are approved words individually. Together, "carry out" forms a phrasal verb. The approved verb "do" replaces the phrasal verb and keeps the same meaning.)

```rust
// Non-STE — scheduler.rs
pub struct CleanupTask;

impl CleanupTask {
    /// Carries out the memory deallocation after each request.
    pub fn run(&self, allocations: &mut Vec<Allocation>) {
        for alloc in allocations.drain(..) {
            alloc.free();
        }
    }
}

// STE — scheduler.rs
pub struct CleanupTask;

impl CleanupTask {
    /// Does the memory deallocation after each request.
    pub fn run(&self, allocations: &mut Vec<Allocation>) {
        for alloc in allocations.drain(..) {
            alloc.free();
        }
    }
}
```

*Adapted from spec pattern: replace unapproved phrasal verbs with a single approved verb that has the same meaning.*

## Code-Domain Explanation

This rule applies across all forms of code documentation. Phrasal verbs are common in informal technical writing. Each form of documentation has a different risk profile for phrasal verb ambiguity.

### README Files

README files are the entry point for users. Phrasal verbs in README files can confuse non-native English speakers. A user who searches for a single approved verb will not find a section that uses only a phrasal verb. Replace common README phrasal verbs:

- "Set up the project" → "Configure the project" or "Install the project"
- "Run through the quickstart" → "Complete the quickstart" or "Do the quickstart"
- "Check out the examples" → "Examine the examples" or "See the examples"
- "Go through the configuration" → "Read the configuration" or "Complete the configuration"
- "Pick up where you left off" → "Continue where you stopped"
- "Break down the architecture" → "Describe the architecture" or "Explain the architecture"

Each heading and paragraph in a README file must use a single approved verb. Do not use a verb+preposition combination when one approved verb is sufficient.

```markdown
<!-- Non-STE README excerpt -->
## Getting started
1. Set up the project with `npm install`.
2. Run through the quickstart to see the CLI in action.
3. Check out the examples folder for sample configs.

<!-- STE README excerpt -->
## Getting started
1. Install the project with `npm install`.
2. Complete the quickstart to see the CLI in action.
3. Examine the examples folder for sample configs.
```

### API Documentation

API reference documentation must be exact. A method description that uses a phrasal verb can hide the actual behavior of the method. Two readers can understand the same phrasal verb differently.

When you document an API endpoint or a function signature, use the approved verb that is most precise for that operation:

- "Looks up a user by ID" → "Finds a user by ID" (the method finds exactly one record)
- "Hands off the request to the worker" → "Sends the request to the worker" (the method transfers control)
- "Takes in a configuration object" → "Receives a configuration object" (the parameter is the input)
- "Spits out the result as JSON" → "Returns the result as JSON" (the method sends back a value)
- "Fills in the missing fields" → "Completes the missing fields" (the method supplies defaults)

For API reference pages, the verb must match the HTTP method or the function behavior exactly. A GET endpoint "gets" data, not "pulls down" or "fetches." A POST endpoint "creates" or "sends" data, not "puts in" or "hands over."

```http
// Non-STE — OpenAPI description
// get:
//   summary: Pulls down the user profile by ID.
// post:
//   summary: Puts in a new order for the cart.

// STE — OpenAPI description
// get:
//   summary: Gets the user profile by ID.
// post:
//   summary: Creates a new order for the cart.
```

### Docstrings and Inline Documentation

Docstrings in Python, Javadoc in Java, and doc comments in Rust, Go, and C# are the most common places where phrasal verbs appear. Developers write docstrings quickly and use informal language. Edit docstrings to remove phrasal verbs:

````python
# Non-STE:
def process(data):
    """Runs through the data and picks out the valid entries."""
    results = []
    for entry in data:
        if entry.is_valid():
            results.append(transform(entry))
    return results

# STE:
def process(data):
    """Examines the data and selects the valid entries."""
    results = []
    for entry in data:
        if entry.is_valid():
            results.append(transform(entry))
    return results
````

````rust
// Non-STE:
/// Sets up the connection pool and kicks off the health check.
pub fn init() -> Pool {
    let pool = Pool::new(get_config());
    pool.run_health_check();
    pool
}

// STE:
/// Configures the connection pool and starts the health check.
pub fn init() -> Pool {
    let pool = Pool::new(get_config());
    pool.run_health_check();
    pool
}
````

### Commit Messages

Commit messages are permanent records of changes. A phrasal verb in a commit message makes the change less clear to a reviewer or a future maintainer. Common phrasal verbs in commit messages and their approved replacements:

| Phrasal Verb (Avoid) | Approved Verb (Use) |
|----------------------|---------------------|
| clean up             | remove, delete, tidy |
| fix up               | correct, repair     |
| speed up             | accelerate, make faster |
| cut down             | reduce, decrease    |
| rip out              | remove              |
| wire up              | connect             |
| strip out            | remove              |
| flesh out            | complete, expand    |

A commit message such as "Clean up the old API endpoints" is ambiguous. "Remove the old API endpoints" or "Refactor the old API endpoints" makes the change exact.

```text
# Non-STE commit messages
git commit -m "Clean up the old API endpoints"
git commit -m "Speed up the image resize loop"

# STE commit messages
git commit -m "Remove the old API endpoints"
git commit -m "Accelerate the image resize loop"
```

### Error Messages

Error messages must tell the user exactly what went wrong and what to do. A phrasal verb in an error message can make the recovery action unclear:

```text
// Non-STE:
Error: Could not hook up to the database.

// STE:
Error: Could not connect to the database.
```

```text
// Non-STE:
Error: The build process blew up during the linking step.

// STE:
Error: The build process failed during the linking step.
```

```text
// Non-STE:
Warning: The lock file is out of whack. Run `install` to sort it out.

// STE:
Warning: The lock file is not consistent. Run `install` to correct it.
```

### Changelogs and Release Notes

Release notes document what changed for users. Phrasal verbs in release notes reduce the professional quality of the communication:

- "We did away with the legacy parser" → "We removed the legacy parser" (BREAKING)
- "Added back the export feature" → "Restored the export feature"
- "The team ironed out the performance issues" → "The team corrected the performance issues"
- "We phased out support for Python 3.7" → "We ended support for Python 3.7" (DEPRECATED)

```markdown
<!-- Non-STE changelog -->
## 2.0.0
- Did away with the legacy parser.
- Ironed out the performance issues on the export job.

<!-- STE changelog -->
## 2.0.0
- Removed the legacy parser.
- Corrected the performance issues on the export job.
```

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Object-oriented documentation describes classes, methods, constructors, and destructors. Phrasal verbs often appear in method descriptions that involve resource management, initialization, and cleanup:

- "Sets up the object state" → "Initializes the object state" (constructor docs)
- "Tears down the resources" → "Releases the resources" (destructor/`close` docs)
- "Hands off ownership to the caller" → "Transfers ownership to the caller" (factory method)
- "Looks up the dependency in the container" → "Finds the dependency in the container" (DI docs)
- "Wraps up the transaction" → "Completes the transaction" (unit of work pattern)

````java
// Non-STE:
/**
 * Tears down the connection and cleans up all associated resources.
 * Call this method when you are done with the connection.
 */
public void close() {
    connection.disconnect();
    resourceRegistry.releaseAll();
}

// STE:
/**
 * Closes the connection and releases all associated resources.
 * Call this method when you no longer need the connection.
 */
public void close() {
    connection.disconnect();
    resourceRegistry.releaseAll();
}
````

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, pipelines, and data transformations. Phrasal verbs can obscure the nature of the transformation:

- "The function maps over the list and filters out nulls" → "The function applies a transformation to each element of the list and removes nulls"
- "It pipes through the middleware stack" → "It sends the request through the middleware stack" (or "It applies the middleware stack")
- "The reducer folds the values down into a single result" → "The reducer combines the values into a single result"
- "The function reaches out to the external service" → "The function sends a request to the external service"

In functional languages, prefer verbs that describe pure transformations: "transforms," "applies," "filters," "maps," "reduces." Do not use phrasal verbs that suggest side effects when the function is pure.

```haskell
-- Non-STE
process :: [Entry] -> [Entry]
process = map transform . filterOut isNull

-- STE
process :: [Entry] -> [Entry]
process = map transform . remove isNull
```

### Procedural Documentation (C, Go, Bash)

Procedural documentation describes step-by-step algorithms, system calls, and shell scripts. Phrasal verbs are especially common in procedural code because scripts often "do things" in sequence:

````bash
# Non-STE:
# 1. Reach out to the API and pull down the latest data.
# 2. Go through each record and pick out the changed fields.
# 3. Put together the update payload and send it off.

# STE:
# 1. Send a request to the API and get the latest data.
# 2. Examine each record and select the changed fields.
# 3. Make the update payload and send it.
````

In C documentation, avoid phrasal verbs that describe memory operations:

- "Free up the allocated memory" → "Release the allocated memory" or "Free the allocated memory"
- "The pointer hands back the result" → "The pointer returns the result" (but pointers do not return values — "The function writes the result through the pointer" is more exact)

```c
// Non-STE:
// The caller must free up the buffer that read_config hands back.
void read_config(char **out);

// STE:
// The caller must release the buffer that read_config returns.
void read_config(char **out);
```

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state, not step-by-step procedures. Phrasal verbs can accidentally introduce an imperative tone that conflicts with the declarative model:

- "The Terraform plan brings up three EC2 instances" → "The Terraform plan creates three EC2 instances"
- "The deployment spins up new pods when the load increases" → "The deployment starts new pods when the load increases"
- "The migration tears down the old index before it builds the new one" → "The migration removes the old index before it creates the new one"
- "The query joins together the users and orders tables" → "The query joins the users table with the orders table"

```hcl
# Non-STE — main.tf comment
# The module brings up three EC2 instances and spins up a load balancer.

# STE — main.tf comment
# The module creates three EC2 instances and starts a load balancer.
```

### Systems Documentation (Rust Ownership, C Memory)

Systems documentation describes ownership, lifetimes, memory safety, and concurrency. Phrasal verbs can make these already-complex topics harder to understand:

- "The function hands off ownership of the buffer" → "The function transfers ownership of the buffer"
- "The closure holds onto the captured variable" → "The closure keeps a reference to the captured variable"
- "The thread gives up the lock when it finishes" → "The thread releases the lock when it finishes"
- "The allocator carves out a new memory region" → "The allocator allocates a new memory region"

````rust
// Non-STE:
/// Takes ownership of the string and hands back a parsed Config.
/// If parsing fails, it gives back the original string.
pub fn parse_config(input: String) -> Result<Config, String> {
    match Config::from_str(&input) {
        Ok(config) => Ok(config),
        Err(_) => Err(input),
    }
}

// STE:
/// Receives ownership of the string and returns a parsed Config.
/// If parsing fails, it returns the original string.
pub fn parse_config(input: String) -> Result<Config, String> {
    match Config::from_str(&input) {
        Ok(config) => Ok(config),
        Err(_) => Err(input),
    }
}
````

## Extended Examples

> **Non-STE:** The test runner runs through all test suites and prints out a summary report.
>
> **STE:** The test runner executes all test suites and prints a summary report.

> *Principles applied: P1, P11 — "run through" is a phrasal verb (verb + preposition). Replace with the single approved verb "execute." Also "prints out" becomes "prints" — "out" adds no meaning and the verb "print" alone is approved for this meaning.*

```python
# Non-STE
def run(tester):
    tester.runs_through_all_suites()
    tester.prints_out_summary()

# STE
def run(tester):
    tester.executes_all_suites()
    tester.prints_summary()
```

> **Non-STE:** The framework sets up the routing table from the annotation data.
>
> **STE:** The framework configures the routing table from the annotation data.

> *Principles applied: P1 — "set up" is one of the most common phrasal verbs in code documentation. The approved verb "configure" replaces it when the context is about initialization with parameters. Use "install" when the context is about placing files on a system. Use "create" when the context is about making a new resource from nothing.*

```python
# Non-STE
router = Router()
router.sets_up_routing_table(annotations)

# STE
router = Router()
router.configures_routing_table(annotations)
```

> **Non-STE:** The middleware looks at the request headers and filters out the sensitive fields.
>
> **STE:** The middleware examines the request headers and removes the sensitive fields.

> *Principles applied: P1, P2 — "look at" is a phrasal verb that means "examine" or "inspect." "Filter out" is also a phrasal verb. The approved verbs "examine" and "remove" each replace one phrasal verb. Note: "filter" alone (without "out") is an approved technical verb. The sentence "The middleware filters the request headers" uses "filter" as an approved verb; adding "out" makes it a phrasal verb.*

```python
# Non-STE
class SecurityMiddleware:
    def process(self, request):
        request = self.looks_at_headers(request)
        request = self.filters_out_sensitive(request)
        return request

# STE
class SecurityMiddleware:
    def process(self, request):
        request = self.examines_headers(request)
        request = self.removes_sensitive(request)
        return request
```

> **Non-STE:** The cleanup job kicks in after 30 seconds of idle time and clears out the expired sessions.
>
> **STE:** The cleanup job starts after 30 seconds of idle time and removes the expired sessions.

> *Principles applied: P1 — "kick in" is an informal phrasal verb with no place in technical documentation. The approved verb "start" gives the exact meaning: the job begins execution. "Clear out" is replaced by "remove" — the expired sessions are deleted, not "cleared out."*

```python
# Non-STE
def cleanup_job():
    if idle_for() > 30:
        kick_in()
        clear_out_expired_sessions()

# STE
def cleanup_job():
    if idle_for() > 30:
        start()
        remove_expired_sessions()
```

> **Non-STE:** The compiler breaks down the source file into an abstract syntax tree, then goes on to generate the intermediate representation.
>
> **STE:** The compiler divides the source file into an abstract syntax tree, then continues to generate the intermediate representation.

> *Principles applied: P1, P11 — "break down" and "go on" are both phrasal verbs. "Break down" (meaning "analyze into parts") becomes "divides" or "separates." "Go on" (meaning "proceed to the next step") becomes "continues." The approved verb "analyze" is also acceptable for the first replacement when the emphasis is on examination rather than separation.*

```python
# Non-STE
def compile(source):
    ast = breaks_down_source(source)
    goes_on_to_generate_ir(ast)

# STE
def compile(source):
    ast = divides_source(source)
    continues_to_generate_ir(ast)
```

> **Non-STE:** The plugin system lets you hook into the build pipeline at three different points. You can also tap into the logging stream.
>
> **STE:** The plugin system lets you connect to the build pipeline at three different points. You can also subscribe to the logging stream.

> *Principles applied: P1, P10 — "hook into" and "tap into" are both informal phrasal verbs with abstract meanings. "Connect to" and "subscribe to" use approved verbs with exact meanings. "Hook into" is also slang (P10), which makes it doubly non-compliant. The approved verb "connect" is standard for describing integration points between systems.*

```python
# Non-STE
pipeline = BuildPipeline()
pipeline.hook_into(stage="lint")
pipeline.tap_into(stream="logs")

# STE
pipeline = BuildPipeline()
pipeline.connect_to(stage="lint")
pipeline.subscribe_to(stream="logs")
```

## Approved Phrasal Verbs in STE-Code

A small number of phrasal verbs are approved because no single verb replaces them with the same precision. These approved phrasal verbs have restricted meanings:

| Approved Phrasal Verb | Restricted Meaning | Example |
|----------------------|-------------------|---------|
| log in / log out | Start or end an authenticated session | "The user must log in before they can access the dashboard." |
| follow up | Take further action after an initial step | "Follow up the installation with the configuration step." |
| back up | Make a copy for safekeeping | "Back up the database before you apply the migration." |
| roll back | Return to a previous state | "Roll back the deployment if the health check fails." |

NOTE: "Log in" and "log out" use the approved verb "log" with the prepositions "in" and "out." Do not use "sign in," "sign out," "log on," or "log off." The verb "back up" (two words) is approved only for making copies. Do not use it for movement ("the car backs up") or support ("back up your claim").

```sql
-- Approved phrasal verbs in use
-- Non-STE: BEGIN; sign in as admin; ...
-- STE:
-- Log in as admin before you run the migration.
-- Back up the orders table before you apply the schema change.
-- Roll back the deployment if the health check fails.
```

## Edge Cases

### Edge Case 1: When a Framework or Tool Name Contains a Phrasal Verb

Some frameworks and tools have names that are phrasal verbs. Per Rule 1.5, technical code nouns are allowed. When you refer to the framework by its official name, use the phrasal verb form:

- "Use `setuptools` to package the Python project." (tool name)
- "The `cleanup` task runs after each deployment." (task name in a build system)
- "Configure the `rollback` strategy in the deployment manifest." (feature name)

When you describe what the framework does — not what it is called — apply Rule 9.3:

- "`setuptools` configures the package metadata." (not "sets up the package metadata")
- "The `cleanup` task removes the temporary files." (not "cleans up the temporary files")

The distinction: a proper name is a noun (P1.5). A description of behavior is a verb phrase and must follow Rule 9.3.

```python
# Non-STE — behavior described with a phrasal verb
setuptools.sets_up_package_metadata()

# STE — behavior described with an approved verb
setuptools.configures_package_metadata()
```

### Edge Case 2: When a Code Keyword Is Also a Phrasal Verb Component

Some code keywords overlap with phrasal verb components. "Break," "continue," "throw," and "catch" are all approved as code keywords (P1.5). In documentation, use them as technical nouns or as approved verbs with their technical meaning:

- "The `break` statement exits the loop immediately." (keyword as noun — approved)
- "The function throws an exception when the input is null." (technical verb — approved, P1.12)
- "The code breaks out of the loop when the condition is true." (phrasal verb — NOT approved)

The last example violates Rule 9.3 because "breaks out of" is a phrasal verb. Replace it: "The code exits the loop when the condition is true."

Similarly, "catch" in "the handler catches the error" is approved (technical verb). But "the handler catches up with the event stream" is a phrasal verb and is not approved. Replace: "the handler synchronizes with the event stream."

```java
// Non-STE
// The loop breaks out of the iteration when the flag is set.
while (running) {
    if (flag) break; // phrasal verb in the comment — not approved
}

// STE
// The loop exits the iteration when the flag is set.
while (running) {
    if (flag) break;
}
```

### Edge Case 3: Two Approved Words That Are Not a Phrasal Verb

Not every verb+preposition combination is a phrasal verb. The rule applies only when the combination creates a meaning different from the meanings of the individual words.

When the preposition is part of a prepositional phrase that describes location, direction, or time — and the verb keeps its approved meaning — the combination is permitted:

- "The application runs on the server." ("runs" keeps its approved meaning; "on the server" is a prepositional phrase of location)
- "The data flows from the input channel to the output channel." ("flows" keeps its approved meaning; the prepositions describe direction)
- "Write the configuration to the file." ("write" keeps its approved meaning; "to the file" describes the target)

Contrast these with actual phrasal verbs where the meaning changes:

- "The application runs on for too long." ("run on" = continues without stopping — phrasal verb, not approved)
- "The team writes up the test plan." ("write up" = compose formally — phrasal verb, not approved)

The test: if you can remove the preposition and the sentence still has approximately the same meaning, the preposition is part of a prepositional phrase and the combination is not a phrasal verb. If removing the preposition changes the meaning completely, it is a phrasal verb.

```python
# Permitted: "write" keeps its meaning; "to the file" is a prepositional phrase
write(config, to=config_file)

# Not approved: "write up" is a phrasal verb (compose formally)
write_up(test_plan)  # replace with: compose(test_plan)
```

### Edge Case 4: Generated Documentation and Code Comments

Auto-generated documentation from tools such as JSDoc, Sphinx, or `rustdoc` can contain phrasal verbs that the developer wrote in the source code. The generated output inherits the phrasal verbs from the source.

When you write doc comments that a tool will extract and publish, apply Rule 9.3 to the source text. The generated documentation will then be compliant.

When you consume third-party generated documentation that you cannot edit, you do not need to correct it. The rule applies to documentation that you write or maintain.

```javascript
// Non-STE source comment — generates non-compliant docs
/**
 * Sets up the cache and kicks off the warmup.
 */
function initCache() { /* ... */ }

// STE source comment — generates compliant docs
/**
 * Configures the cache and starts the warmup.
 */
function initCache() { /* ... */ }
```

### Edge Case 5: When a Single Approved Verb Does Not Exist for the Exact Meaning

Some phrasal verbs have no exact single-verb replacement in the approved vocabulary. In these cases, apply Rule 9.1: use a different sentence construction.

- "The function calls back the caller with the result." → "The function sends the result to the caller through a callback." (rewrite the sentence)
- "The cache warms up before it serves traffic." → "The cache loads the data before it serves traffic." (use a different approved verb with a close meaning)
- "The validator flags up any missing fields." → "The validator reports any missing fields." (use "reports" or "marks")
- "The loop churns through the dataset." → "The loop processes the dataset." ("process" is not in the canonical synonym table but it is a well-known technical verb, P1.12)

When no single approved verb is a perfect replacement, prefer the verb that is closest in meaning and add clarifying context in a subsequent sentence if necessary.

```python
# Non-STE
def fetch_user(uid):
    return client.calls_back_caller_with_result(uid)

# STE — rewrite the sentence (Rule 9.1)
def fetch_user(uid):
    result = client.get(uid)
    return send_result_to_caller(result, via="callback")
```

## Cross-References

| Rule | Relationship |
|------|-------------|
| Rule 1.1 — Use approved words from the STE-Code dictionary | The dictionary lists which words are approved and their approved meanings. Check the dictionary before you use a verb+preposition combination to confirm each word is approved individually. |
| Rule 1.2 — Use words only as their specified part of speech | A phrasal verb often changes the effective part of speech of the preposition. "Up" in "set up" is not a preposition of direction but a particle that modifies the verb. |
| Rule 1.4 — Use only approved verb forms and adjective forms | Phrasal verbs create non-standard verb forms that are not in the approved list. Replacing a phrasal verb with a single approved verb guarantees the form is approved. |
| Rule 1.11 — One term per concept | Two documentation sections that describe the same action — one with "set up" and another with "configure" — violate the consistency rule. Using a single approved verb everywhere prevents this. |
| Rule 1.12 — Technical verbs are allowed | Technical verbs such as "deploy," "compile," "parse," "serialize," and "deserialize" are approved. Do not replace a technical verb with a phrasal verb: "serialize the object" is correct; "turn the object into a string" is not. |
| Rule 9.1 — Use a different sentence construction | When no single approved verb replaces a phrasal verb, rewrite the entire sentence. This is the primary escape hatch for Rule 9.3. |
| Rule 9.2 — Use each approved word correctly | Each word in a non-phrasal-verb combination must carry its approved meaning. Even when a combination is not a phrasal verb, confirm that each word is used with its dictionary meaning. |

## Grammar Notes

### Particle vs. Preposition

A phrasal verb combines a verb with a particle (a word that looks like a preposition but functions as part of the verb). The particle changes the meaning of the verb instead of introducing a prepositional phrase.

In the sentence "The function writes the value to the file," the word "to" is a preposition. It introduces the prepositional phrase "to the file." The verb "write" keeps its approved meaning. This is not a phrasal verb.

In the sentence "The function writes up the report," the word "up" is a particle. It combines with "write" to create the meaning "compose formally." This is a phrasal verb and is not approved.

### Separable vs. Inseparable Phrasal Verbs

English phrasal verbs can be separable (the object can go between the verb and the particle) or inseparable (the object must follow the particle). This rule applies to both types equally:

- Separable: "The script sets the environment up." → "The script configures the environment." ("set up" is separable)
- Inseparable: "The handler looks after the connection pool." → "The handler manages the connection pool." ("look after" is inseparable)

The separability does not change the rule. Both forms are prohibited unless the phrasal verb is specifically approved.

### Why Phrasal Verbs Are Dangerous in Code Documentation

Phrasal verbs cause three types of problems in code documentation:

1. **Ambiguity.** Many phrasal verbs have multiple meanings. "Take off" can mean "remove," "depart," or "become successful." A reader of the documentation cannot be sure which meaning applies.

2. **Non-native comprehension.** Phrasal verbs are one of the most difficult features of English for non-native speakers. A developer who knows the approved meanings of "take" and "off" will not understand "take off" as a phrasal verb.

3. **Searchability.** A user who searches for "remove" will not find documentation that uses the phrasal verb "take off" or "strip out." Consistent use of single approved verbs makes documentation searchable.

### The "One Word Where Possible" Principle

The ASD-STE100 standard has an underlying principle that applies strongly to code documentation: where one word can do the work of two, use the one word. A phrasal verb uses two or three words (verb + one or two particles) to express one meaning. A single approved verb is always preferred:

- "Put up with" (3 words) → "Tolerate" (1 word) — but "tolerate" is not in the code-domain synonym table; "accept" is preferred
- "Come up with" (3 words) → "Propose" or "suggest" (1 word)
- "Cut down on" (3 words) → "Reduce" (1 word)
- "Get rid of" (3 words) → "Remove" (1 word)

This principle aligns with the core STE-Code value: precision through simplicity. Every extra word is a chance for misunderstanding.

> **See also:** Rule 1.1 — Use approved words from the STE-Code dictionary; Rule 1.2 — Use words only as their specified part of speech; Rule 1.4 — Use only approved verb forms and adjective forms; Rule 1.11 — One term per concept; Rule 1.12 — Technical verbs are allowed; Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient; Rule 9.2 — Use Each Approved Word Correctly

---

<!-- a-sec9-rule9.4.md -->

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

### Examples

> *Adapted from spec pair:* Non-STE: "Apply grease to the main body. Wipe the body clean. Inspect the body assembly for cracks." | STE: "Apply grease to the body. Wipe the body clean. Inspect the body for cracks."

Inconsistent (non-STE) documentation — a README "Configure the server" section that uses three names for one file and three verbs for one action:

> **Non-STE:**
> ```markdown
> ## Configure the server
>
> 1. Open the configuration file in a text editor.
> 2. Change the port number in the settings file.
> 3. Save the config and close it.
> 4. Compile the project with the build command.
> 5. Make the binary for the target platform.
> 6. If you get errors, look at the log file.
> ```

STE-Code (consistent) — the same section, with one noun for the file and one verb for each action:

> **STE:**
> ```markdown
> ## Configure the server
>
> 1. Open the configuration file in a text editor.
> 2. Change the port number in the configuration file.
> 3. Save the configuration file and close it.
> 4. Build the project with the build command.
> 5. Build the binary for the target platform.
> 6. If you get errors, look at the log file.
> ```

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

> **Non-STE:**
> ```python
> class Connection:
>     """Connects to server."""
>     def connect(self):
>         ...
>
> class TlsConnection(Connection):
>     """Opens a socket to the backend."""
>     def connect(self):
>         ...
>
> class MtlsConnection(TlsConnection):
>     """Initiates TCP handshake with data node."""
>     def connect(self):
>         ...
> ```

> **STE:**
> ```python
> class Connection:
>     """Establishes a connection to the remote host."""
>     def connect(self):
>         ...
>
> class TlsConnection(Connection):
>     """Establishes a connection to the remote host, with TLS encryption."""
>     def connect(self):
>         ...
>
> class MtlsConnection(TlsConnection):
>     """Establishes a connection to the remote host, with mTLS and certificate pinning."""
>     def connect(self):
>         ...
> ```

> *Principles applied: P3, P13 — using "establishes a connection" consistently; avoiding noun-as-verb "opens a socket."*

Class and interface names must not be abbreviated inconsistently. If you introduce `UserRepository`, do not later refer to it as `UserRepo` or `the user repo` in prose.

### Functional (Haskell, Elixir, Clojure, Rust with functional style)

Functional documentation describes transformations, not state changes. Maintain consistent terminology for the transformation pattern. If one pure function is described as "returns a new value," all pure functions must use the same phrase. Do not describe some pure functions as "produces a result" and others as "yields output."

For monadic or effectful code, pick one metaphor and stay with it. If you describe `IO` as "a description of an effect," do not later call it "a computation" or "an action."

> **Non-STE:**
> ```haskell
> -- Applies a function to each element and returns a new list.
> map :: (a -> b) -> [a] -> [b]
>
> -- Selects elements matching a predicate, producing a fresh collection.
> filter :: (a -> Bool) -> [a] -> [a]
> ```

> **STE:**
> ```haskell
> -- Returns a new list with the function applied to each element.
> map :: (a -> b) -> [a] -> [b]
>
> -- Returns a new list with only the elements that satisfy the predicate.
> filter :: (a -> Bool) -> [a] -> [a]
> ```

> *Principles applied: P3, P11 — "returns a new list" is the consistent anchor phrase; one term ("satisfy") replaces "matching."*

### Procedural (C, Go, Bash)

Procedural code documents sequences of steps. Consistency here means step structures are predictable. If step 3 says "Write the buffer to the file descriptor," step 5 must not say "Output the data to the fd." The reader should see the same verb-noun pattern on every I/O step.

In Go, error handling is idiomatic and repetitive. All error-checking documentation must use the same pattern. Do not describe `if err != nil` as "check for an error" in one place and "handle the error condition" in another.

> **Non-STE:**
> ```go
> // Check the return code. If it is non-zero, abort.
> func run(cmd *exec.Cmd) error {
>     if err := cmd.Run(); err != nil {
>         return err
>     }
>     // Verify the exit status. On failure, terminate.
>     if code := cmd.ProcessState.ExitCode(); code != 0 {
>         return fmt.Errorf("bad exit: %d", code)
>     }
>     return nil
> }
> ```

> **STE:**
> ```go
> // Check the return code. If the return code is not 0, stop the program.
> func run(cmd *exec.Cmd) error {
>     if err := cmd.Run(); err != nil {
>         return err
>     }
>     // Check the return code. If the return code is not 0, stop the program.
>     if code := cmd.ProcessState.ExitCode(); code != 0 {
>         return fmt.Errorf("bad exit: %d", code)
>     }
>     return nil
> }
> ```

> *Principles applied: P11, P1 — "check" over "verify," "return code" over "exit status," "stop" over "abort"/"terminate."*

### Declarative (SQL, Terraform, Kubernetes YAML, Docker Compose)

Declarative documentation describes desired state, not imperative steps. Use the same declarative phrasing for the same resource type. In Terraform docs, if `aws_instance` is described as "a virtual machine in AWS EC2," every reference must use that phrase — do not alternate with "EC2 instance," "AWS VM," or "cloud server."

In Kubernetes documentation, resource names are proper nouns. Use `ConfigMap` (the Kubernetes resource name) consistently. Do not write "config map," "configmap," or "configuration map" in prose.

> **Non-STE:**
> ```yaml
> # Create a ConfigMap to store settings.
> apiVersion: v1
> kind: ConfigMap
> metadata:
>   name: app-config
> data:
>   LOG_LEVEL: info
> ---
> # Mount the config map into the pod.
> spec:
>   containers:
>     - name: app
>       # The configuration map provides env vars.
>       envFrom:
>         - configMapRef:
>             name: app-config
> ```

> **STE:**
> ```yaml
> # Create a ConfigMap to store settings.
> apiVersion: v1
> kind: ConfigMap
> metadata:
>   name: app-config
> data:
>   LOG_LEVEL: info
> ---
> # Mount the ConfigMap into the Pod.
> spec:
>   containers:
>     - name: app
>       # The ConfigMap provides environment variables.
>       envFrom:
>         - configMapRef:
>             name: app-config
> ```

> *Principles applied: P5, P11 — `ConfigMap` and `Pod` are technical code nouns used consistently; no abbreviation of "environment variables."*

### Systems (Rust ownership docs, C memory docs, assembly-level docs)

Systems documentation describes guarantees, invariants, and safety conditions. Consistency here is a safety property — inconsistent terminology about ownership or memory can cause the reader to violate an invariant.

In Rust, "ownership," "borrow," and "lifetime" are terms of art with precise meanings. Never substitute synonyms. "The value is moved" is not "the value is transferred" — "moved" has a specific compiler-enforced meaning.

> **Non-STE:**
> ```rust
> /// The function takes possession of the buffer. The caller relinquishes
> /// control. After the call, the caller cannot access the memory region.
> fn consume(buf: Vec<u8>) {
>     drop(buf);
> }
> ```

> **STE:**
> ```rust
> /// The function takes ownership of the buffer. The function moves the
> /// buffer. After the move, the caller cannot use the buffer.
> fn consume(buf: Vec<u8>) {
>     drop(buf);
> }
> ```

> *Principles applied: P3, P11 — "ownership" and "move" are the canonical Rust terms; "takes possession" and "relinquishes control" break consistency with the Rust Reference.*

## Extended Examples

### Example 1: Verb Consistency in Setup Instructions

> **Non-STE:** Install the dependencies. Then fetch the source code. After that, you need to set up the environment. Finally, get the database running.
>
> From a project README:
> ```markdown
> ## Quick start
>
> 1. Install the dependencies.
> 2. Then fetch the source code.
> 3. After that, you need to set up the environment.
> 4. Finally, get the database running.
> ```

> **STE:** Install the dependencies. Then download the source code. After that, set the environment variables. Finally, start the database.
>
> From a project README:
> ```markdown
> ## Quick start
>
> 1. Install the dependencies.
> 2. Then download the source code.
> 3. After that, set the environment variables.
> 4. Finally, start the database.
> ```

> *Principles applied: P1, P2, P11 — each action uses one approved verb consistently across the procedure; "fetch" is replaced by "download" (canonical synonym table). "Set up" is split into "set" + object. "Get ... running" is replaced by "start."*

### Example 2: Noun Consistency Across Documentation Types

> **Non-STE:** README: "This library provides authentication utilities." API docs: "The auth package handles login." Error message: "Authentication module failed to initialize."
>
> README, API reference, and error log:
> ```markdown
> # authkit
> This library provides authentication utilities.
> ```
> ```http
> GET /login
> The auth package handles login.
> ```
> ```text
> ERROR  auth.module.init.failed: Authentication module failed to initialize.
> ```

> **STE:** README: "This library provides authentication." API docs: "The authentication library handles login." Error message: "The authentication library failed to initialize."
>
> README, API reference, and error log:
> ```markdown
> # authkit
> This library provides authentication.
> ```
> ```http
> GET /login
> The authentication library handles login.
> ```
> ```text
> ERROR  auth.library.init.failed: The authentication library failed to initialize.
> ```

> *Principles applied: P11, P1 — "authentication library" is the only term for the artifact; "auth" is not used as an abbreviation; "module" and "package" are not mixed with "library."*

### Example 3: Structural Consistency in API Reference

> **Non-STE:**
> ```http
> GET /items    — Retrieves all items.
> POST /items   — Use this to create a new item.
> GET /items/:id    — Gets item by ID.
> DELETE /items/:id — Removes the specified item.
> ```

> **STE:**
> ```http
> GET /items    — Returns all items.
> POST /items   — Creates a new item.
> GET /items/:id    — Returns the item with the specified ID.
> DELETE /items/:id — Removes the item with the specified ID.
> ```

> *Principles applied: P11, P4 — every endpoint description starts with a third-person singular verb; "retrieves" and "gets" are unified to "returns"; the `:id` description is identical across endpoints.*

### Example 4: Commit Message Convention Consistency

> **Non-STE:**
> ```text
> 12a7b3 Add user login endpoint
> 8f2c41 Introduce rate limiting
> d4e901 Insert health check route
> 77b3f2 Create logout handler
> ```
> `git log --oneline` output mixes four verbs for the same category of change ("new feature").

> **STE:**
> ```text
> 12a7b3 Add user login endpoint
> 8f2c41 Add rate limiting middleware
> d4e901 Add health check route
> 77b3f2 Add logout handler
> ```
> `git log --oneline` output uses the single verb "Add" for every new feature.

> *Principles applied: P11, P1 — "Add" is the single imperative verb for new features; "Introduce," "Insert," and "Create" are removed. P11: one term per concept.*

### Example 5: Error Message Consistency Across a Service

> **Non-STE:**
> ```text
> [service-a] Connection refused by peer
> [service-b] Cannot establish link to remote
> [service-c] Failed to connect to upstream server
> ```
> The same failure mode produces three different messages, so the operator cannot search one string across all logs.

> **STE:**
> ```text
> [service-a] Cannot connect to the remote host
> [service-b] Cannot connect to the remote host
> [service-c] Cannot connect to the remote host
> ```
> The same failure mode produces one message, so the operator can search one string across all logs.

> *Principles applied: P11, P1 — identical error text for the same failure mode; "refused," "establish link," and "failed to connect" all collapse to "cannot connect"; "peer," "remote," and "upstream server" all collapse to "remote host."*

### Example 6: CLI Flag Documentation Consistency

> **Non-STE:**
> ```text
> --verbose  Enable verbose output
> --quiet    Suppress all logging
> --debug    Turns on debug-level messages
> ```
> From `mycli --help`: "Suppress" and "Turns on" break the template; "logging" and "messages" are two words for "output."

> **STE:**
> ```text
> --verbose  Enables verbose output
> --quiet    Disables all output
> --debug    Enables debug output
> ```
> From `mycli --help`: each flag uses the same template "Enables/Disables [adjective] output."

> *Principles applied: P11, P4 — each flag description uses the same grammatical template: "Enables/Disables [adjective] output"; "Suppress" and "Turns on" are replaced; "logging"/"messages" unified to "output."*

## Edge Cases

### Edge Case 1: Framework-Mandated Terminology

Some frameworks enforce specific terminology that conflicts with STE-Code preferences. For example, React uses "props" (not "properties") and "hooks" (a term STE-Code might prefer to avoid because "hook" can also mean a network hook or a system hook). When the framework is the authority, use the framework term consistently — do not translate it to an STE-Code synonym. The consistency rule defers to the framework: use "props" everywhere, never alternating with "properties" or "arguments."

> **Non-STE:** "Pass properties to the component via its props. The component receives these arguments and renders accordingly."
>
> **STE:** "Pass props to the component. The component receives the props and renders the output."

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

> **See also:** Rule 1.1 — Approved Words; Rule 1.3 — Approved Meanings; Rule 1.5 — Technical Noun Categories; Rule 1.11 — One Term Per Concept; Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient; Rule 9.2 — Use Each Approved Word Correctly
