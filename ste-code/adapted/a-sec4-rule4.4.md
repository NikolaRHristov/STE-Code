# Rule 4.4 — Use Connecting Words and Connecting Phrases to Connect Sentences That Contain Related Topics

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.4

## Original Rule

Connecting words and connecting phrases connect a topic in one sentence with an idea in a sentence that follows.

In a descriptive text, connecting words and connecting phrases give your writing a logical structure and give information that is easy to understand.

Some of the connecting words that are approved in the dictionary are "and," "but," "then," and "thus."

"As a result" and "at the same time" are examples of connecting phrases that you can use.

You can also use demonstrative adjectives as connecting words to connect ideas in related sentences.

In procedures, you can use these connecting words when an explanation is necessary after a work step. Connecting words can also be necessary in safety instructions to connect related sentences or make the text clear.

## STE-Code Adaptation

Connecting words and connecting phrases connect a topic in one sentence with an idea in a sentence that follows. In code documentation, they give your writing a logical structure and make technical information easy to understand.

Use approved connecting words such as "and," "but," "then," and "thus."

Use connecting phrases such as "as a result" and "at the same time."

You can also use demonstrative adjectives (this, these) as connecting words to connect ideas in related sentences. They refer back to a topic introduced in the previous sentence.

In procedural documentation (function and method descriptions), use connecting words when an explanation is necessary after a work step. In warning and caution statements, use connecting words to connect related sentences and make the text clear.

### Examples

**Using "and" to connect two related descriptions:**

> **STE:** The `parseInput` function validates the request payload. **And** the `formatOutput` function serializes the response data.
>
> *Adapted from original rule principle — approved connecting word "and"; no direct spec pair*

**Using "but" to show an exception or alternative:**

> **STE:** These error-handling rules are the minimum necessary for the API layer. **But** the local project conventions can give other necessary error-handling rules.
>
> *Adapted from original rule principle — approved connecting word "but"; no direct spec pair*

**Using "thus" to show a logical consequence:**

> **STE:** If the validation step fails, the middleware sets an error code on the response object. **Thus**, the downstream handler receives the error code and skips the processing step.
>
> *Adapted from original rule principle — approved connecting word "thus"; no direct spec pair*

**Using "as a result" to show cause and effect:**

> **STE:** When the cache eviction policy runs, expired entries are removed from the cache. **As a result**, the cache has free capacity for new entries.
>
> *Adapted from original rule principle — connecting phrase "as a result"; no direct spec pair*

**Using demonstrative adjectives as connecting words in procedures:**

> **STE:** Tag the deprecated methods with the `@deprecated` annotation. **This** annotation will help developers during the migration to the new API.
>
> *Adapted from original rule principle — demonstrative adjectives as connecting words; no direct spec pair*

**Using demonstrative adjectives in safety instructions:**

> **STE:**
>
> **WARNING:** ALWAYS VALIDATE USER INPUT IN THIS MODULE. **THIS** PRECAUTION WILL PREVENT INJECTION ATTACKS.
>
> *Adapted from original rule principle — connecting words in safety instructions; no direct spec pair*

## Code-Domain Explanation

In code documentation, connecting words and phrases serve as the logical scaffold that holds separate sentences together. Without them, technical documents become a list of disconnected facts. With them, the reader understands how each piece of information relates to the next.

### README Files

README files describe a project from high-level purpose down to setup steps. Connecting words link the architectural overview to the installation instructions. They also connect feature descriptions to usage examples. Use "thus" to show why a design choice matters. Use "and" to group related capabilities. Use "but" to introduce limitations or prerequisites.

### API Documentation

API documentation describes endpoints, parameters, request bodies, and response schemas. Connecting words link the description of an input to the description of the output. Use "as a result" to connect a request to its expected response. Use "then" to show the sequence of middleware or filter operations. Use "this" to refer back to a status code or header introduced in the previous sentence.

### Docstrings and Inline Comments

Docstrings describe what a function does, what parameters it accepts, and what it returns. Connecting words link the parameter descriptions to the return value description. They also link the function summary to the detailed behavior. Use "and" to connect closely related parameter descriptions. Use "but" to introduce a precondition or exception. Use "thus" to connect an algorithm step to its effect on the return value.

### Commit Messages

Commit messages describe what changed and why. The subject line states the change. The body explains the reason. Connecting words link the what to the why. Use "thus" to connect a bug description to the fix rationale. Use "as a result" to connect a refactor to its downstream effects. Use "but" to note a deliberate omission or trade-off.

### Error Messages

Error messages tell the user what went wrong and what to do next. Connecting words link the error condition to the recovery action. Use "thus" to connect the detected state to the system response. Use "and" to list concurrent failure conditions. Use "this" to refer back to the named error code or input value.

## Paradigm-Specific Guidance

### Object-Oriented Paradigm (Java, C++, C#, Python classes)

Class documentation describes the class purpose, its fields, and its methods. Connecting words link the class-level summary to the method-level details. They also link constructor descriptions to instance state descriptions.

Pattern: Describe the class invariants in one sentence. Use "thus" to connect them to the behavioral guarantees of the public API. Use "this" to refer back to a private field whose state governs method behavior. Use "and" to group methods that form a logical unit (getter/setter pairs, open/close pairs).

Example flow: "The `ConnectionPool` class keeps a fixed number of open connections. **Thus**, each `acquire` call blocks until a connection becomes available. **This** blocking behavior prevents resource exhaustion under high load. **And** the `release` method returns a connection to the pool."

### Functional Paradigm (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, their inputs, their outputs, and their composition. Connecting words link the description of a function to the description of the composed pipeline.

Pattern: Describe the input type and constraints in one sentence. Use "and" to connect the happy-path behavior to the error-path behavior. Use "thus" to connect a transformation step to the shape of the output. Use "but" to introduce a monadic context or effect that modifies the return type.

Example flow: "The `validate` function checks the input against the schema. **And** it collects all validation errors into a list. **Thus**, the caller receives a comprehensive error report instead of only the first failure. **But** the function does not halt on the first error."

### Procedural Paradigm (C, Go, Bash)

Procedural documentation describes sequences of steps: allocate, initialize, process, clean up. Connecting words show the temporal and causal relationships between these steps.

Pattern: Describe the allocation step in one sentence. Use "then" to introduce the initialization step. Use "after" (as part of a connecting phrase) to show sequencing. Use "as a result" to connect the processing step to the final state.

Example flow: "The `initBuffer` function allocates a memory block of the requested size. **Then** it fills the block with zero bytes. **As a result**, the caller receives a clean buffer ready for use. **And** the function returns the buffer pointer for immediate access."

### Declarative Paradigm (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes resources, their desired state, and their dependencies. Connecting words link the resource definition to the effects the system will apply.

Pattern: Describe the resource spec in one sentence. Use "thus" to connect the spec to the reconciliation outcome. Use "and" to group related resource properties. Use "this" to refer back to a named resource that another resource depends on.

Example flow: "The `Deployment` resource specifies three replicas and a container image. **Thus**, the Kubernetes control plane creates three Pods from that image. **This** Deployment also defines a rolling update strategy. **And** the strategy replaces Pods one at a time during updates."

### Systems Paradigm (Rust ownership docs, C memory docs)

Systems documentation describes ownership, lifetimes, and safety guarantees. Connecting words link the rule statement to the consequence of violating it.

Pattern: Describe the ownership rule in one sentence. Use "thus" to connect the rule to the compiler guarantee. Use "but" to introduce an unsafe escape hatch. Use "as a result" to connect a borrow-checker decision to a runtime behavior.

Example flow: "The `Box<T>` type owns its heap-allocated data. **Thus**, the data is freed when the `Box` goes out of scope. **As a result**, the program cannot leak memory through forgotten deallocations. **But** the `unsafe` keyword permits raw pointer access that bypasses this guarantee."

## Extended Examples

### Example 1 — README: Connecting features to prerequisites

**Non-STE:**
> The image processing pipeline leverages GPU acceleration for real-time transforms. You'll need CUDA 11.8 or higher installed. The pipeline also supports CPU fallback mode.

*Problem: No connecting word between the feature claim and the prerequisite. The "also" is vague.*

> **STE:** The image processing pipeline uses GPU acceleration for real-time transforms. **Thus**, you must install CUDA 11.8 or a newer version. **And** the pipeline includes a CPU fallback mode.
>
> *Applied: P1 (approved connecting word "thus"), P1 (approved connecting word "and")*
> *Fix: "Thus" shows the logical dependency between the feature and the prerequisite. "And" groups the two capability descriptions. "Leverages" replaced with "uses" per canonical synonym table.*

### Example 2 — API Doc: Connecting request to response

**Non-STE:**
> POST /users creates a new user account and returns a 201 status. The response body contains the created user object with an auto-generated ID. The ID can be utilized in subsequent requests to reference this user.

*Problem: The relationship between the 201 status and the response body is implicit. "And" is overloaded inside a single sentence instead of connecting separate sentences. "Utilized" is not an approved word.*

> **STE:** A POST request to `/users` makes a new user account. **As a result**, the API returns a 201 status code. **And** the response body contains the created user object with an auto-generated ID. You can use **this** ID in later requests to refer to the user.
>
> *Applied: P1 (connecting phrase "as a result"), P1 (connecting word "and"), P1 (demonstrative adjective "this"), canonical synonym table ("use" replaces "utilized")*
> *Fix: "As a result" connects the POST action to the 201 response. "And" connects the status code to the body content. "This" refers back to the ID. The procedural "POST /users creates" was rewritten to a descriptive sentence.*

### Example 3 — Docstring: Connecting parameters to return value

**Non-STE:**
> Filters items from the collection that don't match the predicate function. Returns a new collection containing only matching items. The original collection is not modified. The predicate receives each item as its sole argument.

*Problem: No connecting words link the filter behavior to the return guarantee. The immutability note floats without connection. The predicate contract is isolated.*

> **STE:** The `filter` method removes items that do not match the predicate function. **Thus**, the method returns a new collection with only the matching items. **And** the original collection stays unchanged. **This** predicate function receives each item as its only argument.
>
> *Applied: P1 (connecting word "thus"), P1 (connecting word "and"), P1 (demonstrative adjective "this")*
> *Fix: "Thus" connects the filter operation to the return value. "And" connects the return value description to the immutability guarantee. "This" refers back to the predicate function to describe its contract. "Filters" changed to "removes" for clarity.*

### Example 4 — Commit Message: Connecting bug to fix

**Non-STE:**
> Fix race condition in connection pool. The acquire() method could return an already-closed connection under high concurrency. Added a state check before returning from the wait queue.

*Problem: No connecting word links the bug description to the fix description. The three sentences are a flat list with no logical structure.*

> **STE:** The `acquire()` method returned an already-closed connection when many callers used the pool at the same time. **As a result**, the caller received a stale connection and failed on the first write. **Thus**, this commit adds a state check before the method removes a connection from the wait queue.
>
> *Applied: P1 (connecting phrase "as a result"), P1 (connecting word "thus")*
> *Fix: "As a result" connects the race condition to the observable failure. "Thus" connects the failure description to the fix rationale. The fix is now the logical conclusion of the problem description, not a separate fact.*

### Example 5 — Error Message: Connecting error to recovery

**Non-STE:**
> Configuration file not found. Specify a path with --config or set the CONFIG_PATH environment variable.

*Problem: No connecting word links the error condition to the recovery action. The two sentences feel disconnected.*

> **STE:** The configuration file is not found. **Thus**, you must specify a path with the `--config` flag. **Or** you must set the `CONFIG_PATH` environment variable.
>
> *Applied: P1 (connecting word "thus"), P1 (connecting word "or")*
> *Fix: "Thus" connects the detected error condition to the required action. "Or" presents the two alternative recovery paths clearly. The instruction changes from a suggestion to a requirement.*

### Example 6 — Configuration File Comment: Connecting option to effect

**Non-STE:**
> # Enable JIT compilation for query plans. This trades startup time for runtime performance. Set to false if your workload consists of many short-lived connections.

*Problem: No connecting word links the option purpose to the trade-off. The conditional advice floats without logical anchor.*

> **STE:** # Use this option to enable JIT compilation for query plans. **As a result**, the startup time increases. **But** the runtime performance improves. Set **this** option to `false` if your workload uses many short-lived connections.
>
> *Applied: P1 (connecting phrase "as a result"), P1 (connecting word "but"), P1 (demonstrative adjective "this")*
> *Fix: "As a result" connects the option to its cost. "But" introduces the compensating benefit. "This" refers back to the option name. The trade-off is explicit and the conditional advice is anchored.*

## Edge Cases

### Edge Case 1 — Connecting Word That Is Also a Framework Name

Some frameworks use names that overlap with connecting words. For example, "Then" is a testing assertion library (Swift, Kotlin). "And" appears in method names like `and_then` (Rust `Result` combinators).

Guidance: When the word is part of a code token (backtick-delimited), use it as a technical noun per Rule 1.5. The backtick markup distinguishes the code token from the connecting word. Do not capitalize connecting words at the start of a sentence unless they are proper nouns.

> **STE:** The test uses the `Then` assertion to check the output. **And** the test verifies the side effects in a separate block.
>
> *The backtick-delimited `Then` is a technical noun. The sentence-initial "And" is a connecting word. The reader can tell them apart because only the technical noun has code markup.*

### Edge Case 2 — When a Connecting Word Creates Ambiguity

The connecting word "then" has two approved uses: as a time-sequence connector ("do A, then do B") and as a logical-consequence connector ("if A, then B"). In code documentation, these two uses can collide.

Guidance: When "then" could mean either time or logic, use a connecting phrase instead. Replace ambiguous "then" with "after" for time sequence or "thus" for logical consequence. This follows Rule 1.3 (use words only with their approved meanings) and avoids the ambiguity.

> **Ambiguous:** The validator runs on the input. Then the sanitizer processes the output.
>
> *Does "then" mean the sanitizer runs after the validator (time), or the sanitizer runs because the validator finished (logic)?*
>
> **STE (time):** The validator runs on the input. **After** the validator finishes, the sanitizer processes the output.
>
> **STE (logic):** The validator runs on the input. **Thus**, the sanitizer processes only validated output.

### Edge Case 3 — Connecting Words in Generated Code Comments

Generated code (OpenAPI client stubs, protocol buffer outputs, GraphQL codegen) often includes auto-generated comments. These comments may violate Rule 4.4 because the generator concatenates template fragments without connecting words.

Guidance: This rule applies to documentation you write, not to auto-generated comments. Do not modify generated comments to add connecting words — the generator will overwrite your changes on the next run. If the generated comments are unclear, file an issue with the generator project.

> **NOTE:** When you write a wrapper or adapter around generated code, the wrapper documentation must follow Rule 4.4. The generated code itself is exempt.

### Edge Case 4 — Connecting Across Three or More Sentences

A chain of three or more connected sentences can overwhelm the reader. Each connecting word carries the reader forward, but after three links the logical thread becomes hard to follow.

Guidance: Limit connecting-word chains to two or three sentences. If the explanation needs more sentences, restructure into a list or a table. This aligns with Rule 4.1 (sentence length) and Rule 3.1 (simple sentences).

> **Non-STE (chain too long):** The cache eviction policy runs every 60 seconds. Thus, expired entries are removed. And the eviction log is written to disk. As a result, the cache has free capacity. But the eviction process locks the cache for the duration. And concurrent reads must wait.
>
> **STE (restructured):** The cache eviction policy runs every 60 seconds:
> - Expired entries are removed from the cache.
> - The eviction log is written to disk.
>
> **Thus**, the cache has free capacity for new entries. **But** the eviction process locks the cache for its full duration. **As a result**, all concurrent reads must wait until the eviction completes.

### Edge Case 5 — Connecting Word at the Start of a Documentation Section

Documentation sections (README headings, API endpoint groups, docstring sections like "Parameters" and "Returns") are separated by headings, not by connecting words. The heading itself provides the structural connection.

Guidance: Do not use a connecting word at the very start of a new section to link it to the previous section. The heading breaks the sentence-level flow. Instead, restate the topic in the new section so it stands alone. The connecting word belongs inside a section, not between sections.

> **Non-STE:**
> ## Returns
> Thus, the function returns a `Result` object with the parsed data.
>
> **STE:** The function returns a `Result` object with the parsed data.

## Cross-References

- **Rule 1.1 — Use Approved Words:** The connecting words and phrases in this rule must come from the STE-Code approved dictionary. Do not invent new connecting words.
- **Rule 1.3 — Use Words Only with Their Approved Meanings:** Each connecting word has a specific logical meaning (addition, contrast, consequence). Do not use "and" to mean "but" or "thus" to mean "then."
- **Rule 1.11 — One Term per Concept:** Choose one connecting word for each logical relationship and use it consistently across the document. Do not switch between "thus" and "as a result" for the same causal link within the same section.
- **Rule 3.1 — Use Simple Sentences:** Connecting words join simple sentences. If either sentence is complex, simplify it first, then connect them.
- **Rule 4.1 — Keep Sentences Short:** Adding a connecting word does not permit longer sentences. Each sentence before and after the connecting word must independently obey the 20/25-word limit.
- **STE-Code Dictionary — Section: Connecting Words:** The dictionary lists all approved connecting words and phrases with their exact meanings and usage constraints. Consult it before using a connecting word that is not listed in this rule.

## Grammar Notes

### Coordinating Conjunctions as Sentence Connectors

Standard English grammar discourages starting a sentence with "and" or "but." STE-Code permits and encourages this pattern because it creates short, independent sentences with an explicit logical link. Each sentence stands alone grammatically, and the connecting word makes the relationship between sentences explicit.

The length limit (Rule 4.1) is easier to obey when you split a long compound sentence into two sentences joined by "and" or "but." A 40-word compound sentence becomes two 20-word sentences, each independently verifiable.

### Transitional Adverbs and Connecting Phrases

"Thus" is a transitional adverb. "As a result" is a connecting phrase. Both function the same way: they sit at the start of the second sentence and show the logical relationship to the first. In STE-Code, treat them as equivalent but distinct — choose one and use it consistently per document (Rule 1.11).

Unlike English prose, STE-Code does not require a semicolon before "thus." The period-plus-capital pattern ("...error code. **Thus**, the handler...") is preferred because it keeps sentences short and independent.

### Demonstrative Adjectives

"This" and "these" are demonstrative adjectives when they modify a noun ("this function," "these parameters"). They are demonstrative pronouns when they stand alone ("this is the result"). STE-Code prefers the adjective form with an explicit noun because it removes ambiguity — the reader knows exactly what "this" refers to. The pronoun form is permitted only when the referent is unmistakably clear from the prior sentence.

### Parallel Structure Across Connected Sentences

When you connect two sentences with "and," the two sentences benefit from parallel grammatical structure. If the first sentence is "The function validates the input," the second should be "And the function formats the output," not "And the output is formatted by the function." Parallel structure reduces the cognitive load on the reader and aligns with Rule 3.1 (simple sentences).

### Connecting Words in Imperative Procedures

In procedural documentation (Rule 6 series), connecting words follow a work step when an explanation is necessary. The pattern is: step instruction, period, connecting word, explanation sentence. The connecting word never appears inside the step instruction itself. This separation keeps the step instruction actionable and the explanation informative, without mixing the two modes.

> **Correct pattern:**
> Set the `timeout` option to 30000. **Thus**, the connection does not close during long database operations.
>
> **Incorrect pattern (mixed):**
> Set the `timeout` option to 30000 and thus the connection does not close during long database operations.
