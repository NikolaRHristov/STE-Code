# Rule 4.4 — Use Connecting Words and Connecting Phrases

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.4
> **Source:** [master.md#sec4-rule4.4](ste-code/grouped/)
> **Domain:** code documentation (API docs, commit messages, README sections, code comments)

## Original Rule

Connecting words and connecting phrases connect a topic in one sentence with an idea in a sentence that follows.

In a descriptive text, connecting words and connecting phrases give your writing a logical structure and give information that is easy to understand.

Some of the connecting words that are approved in the dictionary are "and," "but," "then," and "thus."

"As a result" and "at the same time" are examples of connecting phrases that you can use.

You can also use demonstrative adjectives as connecting words to connect ideas in related sentences.

In procedures, you can use these connecting words when an explanation is necessary after a work step. Connecting words can also be necessary in safety instructions to connect related sentences or make the text clear.

### Examples (from source):

> **STE:** The localizer course aligns with the centerline of the runway. And the glideslope path is at a constant angle to the threshold of the runway.
>
> **STE:** These safety precautions are the minimum necessary for work in the pit lane. But the local regulations can give other necessary safety precautions.
>
> **STE:** If the pressure increases, it changes the electrical currents in the transmitter. Thus, the power unit supplies currents to the indicator on the related panel.
>
> **STE:** When the hydraulic pressure is released, the sequence valve moves to the open position. As a result, the actuators are connected to the hydraulic return.

## STE-Code Adaptation

Connecting words and connecting phrases connect a topic in one sentence with an idea in a sentence that follows. In code documentation, they give your writing a logical structure and make technical information easy to understand.

Use approved connecting words such as "and," "but," "then," and "thus."

Use connecting phrases such as "as a result" and "at the same time."

You can also use demonstrative adjectives (this, these) as connecting words to connect ideas in related sentences. They refer back to a topic introduced in the previous sentence.

In procedural documentation (function and method descriptions), use connecting words when an explanation is necessary after a work step. In safety instructions, use connecting words to connect related sentences and make the text clear.

### Code-Domain Examples

> *Adapted from spec pair:* Non-STE: "The localizer course aligns with the centerline of the runway. The glideslope path is at a constant angle to the threshold of the runway." (two related facts joined only by context)  |  STE: "The localizer course aligns with the centerline of the runway. And the glideslope path is at a constant angle to the threshold of the runway."

**Using "and" to connect two related descriptions:**

The two sentences stay independent. Each sentence has one topic. The connecting word makes the link explicit.

> **Non-STE:** `parseInput` validates the request payload and `formatOutput` serializes the response, and they're both called in the handler.
>
> **STE:** The `parseInput` function validates the request payload. And the `formatOutput` function serializes the response data.

**Using "but" to show an exception or alternative:**

Use "but" when the second sentence corrects, limits, or extends the first.

> **Non-STE:** These error-handling rules are the minimum necessary for the API layer, although the local project conventions may specify additional ones.
>
> **STE:** These error-handling rules are the minimum necessary for the API layer. But the local project conventions can give other necessary error-handling rules.

**Using "thus" to show a logical consequence:**

Use "thus" when the second sentence is a direct result of the first.

> **Non-STE:** If the validation step fails, the middleware sets an error code on the response object, so the downstream handler gets it and skips processing.
>
> **STE:** If the validation step fails, the middleware sets an error code on the response object. Thus, the downstream handler receives the error code and skips the processing step.

**Using "as a result" to show cause and effect:**

Use "as a result" for a clear physical or state change caused by the first sentence.

> **Non-STE:** When the cache eviction policy runs, expired entries are removed, which frees up capacity for new entries.
>
> **STE:** When the cache eviction policy runs, expired entries are removed from the cache. As a result, the cache has free capacity for new entries.

**Using "then" to show a time sequence in a procedure:**

Use "then" for an ordered work step, not for logical consequence.

> **Non-STE:** Open the database connection, after that run the migration script, and finally start the API server.
>
> **STE:** Open the database connection. Then run the migration script. And then start the API server.

**Using demonstrative adjectives as connecting words in procedures:**

The demonstrative adjective must point back to a topic that the previous sentence already named.

> **Non-STE:** Tag the deprecated methods with the `@deprecated` annotation; it helps developers migrate to the new API.
>
> **STE:** Tag the deprecated methods with the `@deprecated` annotation. This annotation will help developers during the migration to the new API.

**Connecting words in a safety instruction:**

Safety instructions use the imperative form. The connecting word still links the precaution to its reason.

> **Non-STE:** Always validate user input in this module because it prevents injection attacks.
>
> **STE:** BREAKING: ALWAYS VALIDATE USER INPUT IN THIS MODULE. THIS PRECAUTION WILL PREVENT INJECTION ATTACKS.

**Non-STE versus STE (missing connection):**

When you omit the connecting word, the reader must guess the link. STE makes the link explicit.

> **Non-STE:** POST /users creates a new user account and returns a 201 status. The response body contains the created user object with an auto-generated ID. The ID can be used in later requests to reference this user.
>
> **STE:** A POST request to `/users` makes a new user account. As a result, the API returns a 201 status code. And the response body contains the created user object with an auto-generated ID. You can use this ID in later requests to refer to the user.

**Using "as a result" in a configuration description:**

> **Non-STE:** When you set `max_connections` to 64, the pool reuses sockets and latency drops under load.
>
> **STE:** Set the `max_connections` value to 64 in the config file. As a result, the connection pool reuses idle sockets. And the average request latency decreases under load.

**Using "thus" in a test description:**

> **Non-STE:** The test seeds a row, calls the delete endpoint, and the row is gone from the database afterward.
>
> **STE:** The test seeds one row in the database. Thus, the delete endpoint removes that row. And the database has zero rows after the call.

**Using "at the same time" to show concurrency:**

> **Non-STE:** The worker fetches the page and parses it concurrently using asyncio tasks.
>
> **STE:** The worker fetches the page from the remote server. At the same time, the parser reads the response stream. And both tasks finish before the timeout.

**Using "but" in an error-message description:**

> **Non-STE:** The `read_file` function returns the contents; however, it raises `PermissionError` when the path is not readable.
>
> **STE:** The `read_file` function returns the contents of the file. But it raises a `PermissionError` when the path is not readable.

### Paradigm-Specific Guidance

- **Object-Oriented:** Describe the class invariants in one sentence. Use "thus" to connect them to the behavioral guarantees of the public API. Use "this" to refer back to a private field. Use "and" to group related methods.
- **Functional:** Describe the input type in one sentence. Use "and" to connect the happy path to the error path. Use "thus" to connect a transformation step to the shape of the output.
- **Procedural (C, Go, Bash):** Describe the allocation step in one sentence. Use "then" to introduce initialization. Use "as a result" to connect processing to the final state.
- **Declarative (SQL, Terraform, YAML):** Describe the resource spec in one sentence. Use "thus" to connect the spec to the reconciliation outcome. Use "this" to refer back to a named resource.
- **Systems (Rust, C memory):** Describe the ownership rule in one sentence. Use "thus" to connect the rule to the compiler guarantee. Use "but" to introduce an unsafe escape hatch.

### Edge Cases

- **Connecting word that is also a framework name:** Some frameworks use names that overlap with connecting words (for example, the `Then` assertion library, the Rust `and_then` combinator). When the word is a code token in backticks, treat it as a technical noun. The sentence-initial connecting word is not in backticks.
- **"Then" ambiguity:** "Then" can mean time sequence ("do A, then do B") or logical consequence ("if A, then B"). When ambiguous, use "after" for time or "thus" for logic.
- **Generated code comments:** This rule applies to documentation you write, not to auto-generated comments. Do not edit generated comments to add connecting words.
- **Connecting across three or more sentences:** Limit connecting-word chains to two or three sentences. If more are needed, restructure into a list or a table.
- **Connecting word at the start of a section:** Do not use a connecting word at the very start of a new section to link it to the previous section. The heading provides the structural connection. Restate the topic so the section stands alone.

### Grammar Notes

- Starting a sentence with "and" or "but" is permitted and encouraged. It creates short, independent sentences with an explicit logical link.
- "Thus" and "as a result" sit at the start of the second sentence. Do not use a semicolon before "thus."
- "This" and "these" are demonstrative adjectives when they modify a noun ("this function," "these parameters"). Prefer the adjective form with an explicit noun to remove ambiguity.
- When you connect two sentences with "and," keep the two sentences parallel in structure.

## Cross-References

- **Rule 1.1** — The connecting words and phrases must come from the approved dictionary.
- **Rule 1.3** — Use each connecting word only with its approved meaning.
- **Rule 1.11** — Use one term per concept. Use "thus" or "as a result" consistently, not both, for the same link.
- **Rule 3.1** — Connecting words join simple sentences. Simplify a complex sentence before you connect it.
- **Rule 4.1** — Each sentence before and after the connecting word must obey the length limit.

> **See also:** Rule 1.1 — Approved Words Come from the Dictionary
> **See also:** Rule 1.3 — Use Approved Words with the Approved Meaning
> **See also:** Rule 1.11 — Use One Term per Concept
> **See also:** Rule 3.1 — Write One Topic per Sentence
> **See also:** Rule 4.1 — Write Sentences That Are Not Too Long

## Summary Checklist

- [ ] Each connecting word links a sentence to the one that follows.
- [ ] Only approved connecting words and phrases are used.
- [ ] Demonstrative adjectives refer back to a clearly introduced topic.
- [ ] No mixed procedural and descriptive modes inside one connected pair.
- [ ] Connecting-word chains do not exceed three sentences.
