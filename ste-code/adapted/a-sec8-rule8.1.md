# Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon (;)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.1

## Original Rule

**Rule 8.1** You can use all standard English punctuation marks but not the semicolon (;).

The semicolon (;) is not permitted in STE because it lets you write very long sentences. It is also not easy to use correctly. As an alternative to the semicolon, always write two different sentences.

Examples:

| **Non-STE:** | (1) Examine the removed parts; replace the damaged ones. |

| **STE:** | (1) Examine the removed parts for damage. |

| | (2) Replace the damaged part(s). |

## STE-Code Adaptation

**Rule 8.1** In code documentation, you can use all standard English punctuation marks but not the semicolon (;).

The semicolon (;) is not permitted in STE-Code because it lets you write very long sentences that are difficult to read in code comments and documentation. It is also not easy to use correctly. As an alternative to the semicolon, always write two different sentences.

### Examples

> **Non-STE:** Call the function to parse the response data; handle any errors that occur.
>
> **STE:** Call the function to parse the response data. Handle any errors that occur.
>
> *Adapted from spec pair: "Examine the removed parts; replace the damaged ones." → split into two sentences.*

> **Non-STE:** The cache is invalid after a write operation; you must flush it before the next read.
>
> **STE:** The cache is invalid after a write operation. You must flush it before the next read.
>
> *Adapted from spec pair: "Examine the removed parts; replace the damaged ones." → split into two sentences.*

## Code-Domain Explanation

Rule 8.1 forbids the semicolon in all code documentation. The semicolon lets a writer pack two or more independent clauses into one sentence. In code documentation, this compression makes sentences hard to parse, especially for non-native English readers. The semicolon also has a different meaning in many programming languages (statement terminator in C, Java, JavaScript, Rust, Go), which creates cognitive interference when the same symbol appears in documentation prose.

The fix is always the same: split the semicolon-separated sentence into two or more independent sentences. Each sentence stands alone with its own subject and verb. The reader processes one complete thought before moving to the next. This aligns with Rule 3.1 (use simple sentences) and Rule 4.1 (keep sentences short).

### README Files

README files describe project purpose, installation, usage, and contribution guidelines. Semicolons often appear when the writer tries to cram a feature description and its rationale into one sentence. The fix: write the feature description as one sentence. Write the rationale as a second sentence. Use a connecting word (Rule 4.4) if the relationship between the two sentences needs to be explicit.

Example of a semicolon violation in a README:

```
The server supports WebSocket connections; these use a persistent
channel instead of the standard request-response cycle.
```

The second clause ("these use a persistent channel...") explains what WebSocket connections are. It deserves its own sentence:

```
The server supports WebSocket connections. These connections use a
persistent channel instead of the standard request-response cycle.
```

### API Documentation

API documentation describes endpoints, parameters, request bodies, and response schemas. Semicolons often appear in endpoint descriptions that list two effects of a single operation. The fix: write the primary effect as one sentence. Write the secondary effect as a second sentence.

Example of a semicolon violation in API docs:

```
POST /sessions creates a new session and returns a token; the token
must be included in the Authorization header of subsequent requests.
```

The first clause describes the operation. The second clause gives a usage requirement. Each is a complete thought:

```
A POST request to /sessions makes a new session and returns a token.
You must include the token in the Authorization header of all later
requests.
```

### Docstrings and Inline Comments

Docstrings describe what a function does, what parameters it accepts, and what it returns. Semicolons often appear when the writer lists two return conditions or two side effects. The fix: use a bullet list for multiple return conditions. Use separate sentences for multiple side effects. Inline comments rarely need semicolons because they should be one short sentence each.

Example of a semicolon violation in a docstring:

```
Returns the user record if found; raises UserNotFoundError otherwise.
```

Split into a bullet list or two sentences:

```
Returns:
    - The user record when the user ID matches a database entry.
    - A UserNotFoundError when the user ID does not match any entry.
```

### Commit Messages

Commit messages describe what changed and why. The subject line is one sentence (50 characters or fewer). The body is a series of short sentences. Semicolons in commit messages are almost always unnecessary — each sentence in the body should state one fact about the change. If you feel the need for a semicolon, you are likely combining two distinct facts. Split them.

Example of a semicolon violation in a commit message body:

```
The cache layer now uses a TTL of 300 seconds; expired entries
are evicted by a background thread rather than on access.
```

Two distinct facts: the TTL value and the eviction strategy. They belong in separate sentences:

```
The cache layer now uses a TTL of 300 seconds. Expired entries
are evicted by a background thread rather than on access.
```

### Error Messages

Error messages tell the user what went wrong and what to do next. Semicolons often appear when the error condition and the recovery action are joined into one sentence. The fix: write the error condition as one sentence. Write the recovery action as a second sentence. Better yet, follow the error message pattern: "X is not found. Do Y to fix this."

Example of a semicolon violation in an error message:

```
Invalid port number; specify a value between 1024 and 65535.
```

Two distinct pieces of information: what is wrong and what to do:

```
The port number is not valid. Specify a value between 1024 and
65535.
```

## Paradigm-Specific Guidance

### Object-Oriented Paradigm (Java, C++, C#, Python classes)

Class documentation describes constructors, fields, methods, and invariants. Semicolons tend to appear in constructor documentation that describes both the initialization and the post-condition in one breath. In method docs, semicolons appear when the writer lists two return states (success value, exception) in one sentence.

Pattern: Write the constructor's initialization behavior as one sentence. Write the post-condition (the state of the object after construction) as a second sentence. For methods with multiple return states, use a bullet list or separate sentences. For getter/setter pairs, write each method's description as its own sentence — do not use a semicolon to chain the getter and setter together.

Example of a semicolon violation in a class docstring:

```
The ConnectionPool constructor opens N connections to the database;
the pool is immediately ready for use after construction.
```

Split the initialization step and the readiness guarantee:

```
The ConnectionPool constructor opens N connections to the database.
The pool is ready for use immediately after the constructor returns.
```

### Functional Paradigm (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, their inputs, their outputs, and their composition. Semicolons often appear in function docstrings that describe both the happy path and the error path in one sentence, or that chain multiple transformation steps.

Pattern: Describe the happy-path transformation as one sentence. Describe the error path as a second sentence, introduced with a connecting word like "but" or "thus." For composed pipelines, write each transformation step as a separate sentence. The pipe operator (`|>` in Elixir, `>>` in F#, `.` in Haskell) already provides visual composition — do not reinforce it with a semicolon in prose.

Example of a semicolon violation in a Rust docstring:

```
Parses the input string into a Config struct; returns an Err if any
field fails validation.
```

Two distinct outcomes:

```
This function parses the input string into a Config struct. The
function returns an Err value when a field does not pass validation.
```

### Procedural Paradigm (C, Go, Bash)

Procedural documentation describes sequences of steps: allocate, initialize, process, clean up. Semicolons often appear when the writer chains two sequential steps into one sentence. This is particularly tempting in C where the semicolon is the statement terminator — the writer unconsciously carries the punctuation habit from code into prose.

Pattern: Write each procedural step as its own sentence. If the steps form a tight sequence, use the connecting word "then" (Rule 4.4) at the start of the second sentence. Do not use a semicolon to compress the sequence into one sentence. For error-handling steps (check return code, handle error), write the check as one sentence and the handler as a second.

Example of a semicolon violation in a Go function comment:

```
InitBuffer allocates a 4KB memory block; it fills the block with
zeros before returning the pointer.
```

Two steps in sequence:

```
The InitBuffer function allocates a 4 KB memory block. Then it fills
the block with zeros. The function returns the pointer after the
block is filled.
```

### Declarative Paradigm (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes resources, their desired state, and their dependencies. Semicolons often appear in resource descriptions that list two properties or two effects in one sentence.

Pattern: Write each resource property as its own sentence. Write each effect of the resource declaration as its own sentence. Use connecting words ("thus," "as a result") to link the property to its effect. For multi-field resource specs, use a table or bullet list instead of a semicolon-separated prose list.

Example of a semicolon violation in a Terraform variable description:

```
The instance_type variable sets the EC2 instance size; valid values
include t3.micro, t3.small, and t3.medium.
```

Two independent pieces of information:

```
The instance_type variable sets the EC2 instance size. Valid values
include t3.micro, t3.small, and t3.medium.
```

### Systems Paradigm (Rust ownership docs, C memory docs)

Systems documentation describes ownership, lifetimes, memory layouts, and safety guarantees. Semicolons often appear when the writer describes a rule and its consequence in one sentence. This is dangerous in safety-critical documentation — the reader might miss the consequence because it is buried in a compound sentence.

Pattern: Write the ownership or memory rule as one sentence. Write the consequence of violating the rule as a second sentence, introduced with "thus" or "as a result." For Undefined Behavior documentation, never use a semicolon — the consequence must be a standalone sentence that cannot be missed.

Example of a semicolon violation in a Rust safety doc:

```
The caller must ensure the pointer is non-null and aligned; undefined
behavior occurs if either condition is violated.
```

The safety requirement and its consequence must be separate and unmissable:

```
The caller must make sure that the pointer is not null. The caller
must also make sure that the pointer is aligned. Undefined Behavior
occurs if either condition is not met.
```

## Extended Examples

### Example 3 — API Endpoint: Two effects of a mutation

> **Non-STE:** PATCH /config updates the runtime settings and writes the new values to disk immediately; a restart is not required for the changes to take effect.
>
> **STE:** A PATCH request to /config updates the runtime settings and writes the new values to disk. A restart is not necessary for the changes to take effect.
>
> *Principles applied: P1 (split semicolon into two sentences), Rule 4.1 (each sentence under 25 words). The first sentence describes the operation. The second sentence states the operational benefit. The reader gets two complete, independent thoughts.*

### Example 4 — Docstring: Multiple return conditions

> **Non-STE:** Returns the parsed configuration as a dict if the file is valid YAML; returns an empty dict if the file is empty; raises ConfigError if the file contains invalid syntax.
>
> **STE:** The function returns the parsed configuration as a dict when the file is valid YAML. The function returns an empty dict when the file is empty. The function raises a ConfigError when the file contains incorrect syntax.
>
> *Principles applied: P1 (split semicolon chain into three sentences), Rule 3.1 (each sentence is a simple subject-verb-object clause). The original had three independent clauses joined by two semicolons. Each clause now stands alone with a repeated subject ("The function") for clarity.*

### Example 5 — Commit Message: Two independent facts

> **Non-STE:** The authentication middleware now checks token expiry before decoding; expired tokens return a 401 before reaching the route handler.
>
> **STE:** The authentication middleware now checks token expiry before decoding. Expired tokens return a 401 status code before they reach the route handler.
>
> *Principles applied: P1 (split semicolon), Rule 3.1 (simple sentences). The first sentence states the behavioral change. The second sentence states the user-visible effect. Each fact is independently verifiable in the diff.*

### Example 6 — Error Message: Condition and recovery

> **Non-STE:** Database connection timed out after 30 seconds; check that the DB_HOST environment variable is set correctly and the server is reachable.
>
> **STE:** The database connection timed out after 30 seconds. Check that the DB_HOST environment variable is set correctly. Make sure that the server is reachable.
>
> *Principles applied: P1 (split semicolon), Rule 6.1 (imperative mood for recovery action). The error condition is one sentence. The two recovery checks are two imperative sentences. The user reads the problem, then executes the fixes one at a time.*

### Example 7 — README: Feature and constraint

> **Non-STE:** The plugin system supports hot-reloading during development; production builds load plugins at startup only and cannot reload them without a restart.
>
> **STE:** The plugin system supports hot-reloading during development. Production builds load plugins at startup only. These builds cannot reload plugins without a restart.
>
> *Principles applied: P1 (split semicolon), P1 (demonstrative adjective "these"), Rule 4.4 (connecting words). The original had a semicolon and an "and" inside the second clause. The fix splits into three clean sentences with a demonstrative adjective linking the last two.*

### Example 8 — Configuration File Comment: Option and trade-off

> **Non-STE:** Set this to false for read-heavy workloads; the write path becomes slower but consistency guarantees improve under concurrent access.
>
> **STE:** Set this option to false for read-heavy workloads. The write path becomes slower with this setting. But the consistency guarantees improve when many clients access the data at the same time.
>
> *Principles applied: P1 (split semicolon), P1 (connecting word "but"), Rule 4.4. The first sentence gives the instruction. The second states the cost. The third states the benefit. The trade-off is explicit and the reader weighs both sides independently.*

## Edge Cases

### Edge Case 1 — Semicolons Inside Code Blocks

Code blocks (fenced with triple backticks or indented by four spaces) contain source code, not documentation prose. Semicolons inside code blocks are part of the programming language syntax — they are not subject to Rule 8.1. This rule applies only to the prose that surrounds and explains the code.

Guidance: Do not remove semicolons from code examples to comply with Rule 8.1. The rule governs documentation text, not the code being documented. A JavaScript example that shows `const x = 5;` is correct and must keep its semicolon. The prose that describes the example ("This statement declares a constant named x.") must not use semicolons.

> **NOTE:** When you show a code snippet inline with backticks (`const x = 5;`), the semicolon inside the backticks is permitted. The backtick boundary separates code tokens from prose tokens.

### Edge Case 2 — Semicolons in Generated Documentation

Auto-generated documentation (OpenAPI spec descriptions, protobuf source comments, JSDoc output, Javadoc output) may contain semicolons inserted by the generator. These are not under the writer's control.

Guidance: When you write the source comments that feed into the generator (JSDoc `@param` tags, protobuf `//` comments, OpenAPI `description` fields), apply Rule 8.1. When the generator splices your comments together with semicolons in the rendered output, that is a generator behavior issue — not a violation you must fix. File an issue with the generator project to request semicolon-free output.

> **NOTE:** For documentation that you author directly (README files, hand-written API docs, commit messages), Rule 8.1 applies in full. The generator exemption applies only to machine-composed output that you cannot control.

### Edge Case 3 — When a Semicolon Appears Inside a Quoted String

Documentation sometimes quotes error messages, log output, or terminal text that contains semicolons. A quoted string is not your prose — it is the thing being quoted. Do not modify the content of quoted strings to remove semicolons.

Guidance: Keep the semicolon inside the quoted material. Use quotation marks or a code block to delimit the quoted text. The surrounding prose must obey Rule 8.1. The quoted material is exempt.

> **STE:** The compiler shows the error message: "missing semicolon at line 42; expected ';' after expression." Add a semicolon at the end of line 42 to fix this error.
>
> *The semicolons inside the quoted error message are preserved. The prose that explains the fix ("Add a semicolon...") uses no semicolons. The reader can see the exact compiler output while the documentation prose remains compliant.*

### Edge Case 4 — Lists That Look Like Semicolon-Separated Clauses

Some writers use a semicolon as a list separator for complex list items (items that contain internal commas). This is standard English punctuation for "super-commas." For example: "The function accepts three parameters: the input string, which must be UTF-8; the output format, which can be 'json' or 'xml'; and a callback, which is optional."

Guidance: In STE-Code, do not use semicolons as super-commas in lists. Instead, structure the list as a bullet list or a table. Each list item becomes a separate line with its own sentence or phrase. This removes the need for semicolons entirely and improves readability.

> **Non-STE:** The endpoint accepts three query parameters: `sort`, which sets the sort field; `order`, which must be "asc" or "desc"; and `limit`, which caps the result count.
>
> **STE:** The endpoint accepts three query parameters:
> - `sort` — Sets the sort field.
> - `order` — Must be "asc" or "desc."
> - `limit` — Caps the result count.
>
> *Principles applied: P1 (no semicolons), Rule 3.3 (use lists for complex items). The bullet list replaces the super-comma structure. Each parameter gets its own line with a clear description.*

### Edge Case 5 — Winking Semicolons in Chat and Informal Communication

Some development teams use semicolons in chat messages, code review comments, and informal wiki pages as a stylistic convention. This is not code documentation in the STE-Code sense — it is informal communication.

Guidance: Rule 8.1 applies to formal code documentation: README files, API reference docs, docstrings, commit messages, error messages, and specification documents. It does not apply to chat messages, pull request discussions, or informal team communication. Use your judgment: if the text will be read by users outside your team or will persist in the repository for more than one release cycle, apply Rule 8.1. If it is a transient message in a pull request thread, the rule is optional.

> **NOTE:** This edge case does not create a loophole for commit messages. Commit messages are permanent repository history and must follow Rule 8.1. The exemption applies only to ephemeral communication channels like chat and code review comments.

## Cross-References

- **Rule 1.1 — Use Approved Words:** The words you use to connect split sentences (and, but, thus, then) must come from the STE-Code approved dictionary. Do not invent new connecting words to replace semicolons.
- **Rule 1.3 — Use Words Only with Their Approved Meanings:** When you split a semicolon sentence into two, make sure each connecting word you add carries its approved meaning. Do not use "thus" to mean "and" or "but" to mean "then."
- **Rule 3.1 — Use Simple Sentences:** The fix for a semicolon violation is always to write two or more simple sentences. If either resulting sentence is complex, simplify it further.
- **Rule 4.1 — Keep Sentences Short:** Semicolons let you evade the 20-word (procedural) and 25-word (descriptive) sentence length limits. Removing semicolons and splitting sentences makes length compliance verifiable.
- **Rule 4.4 — Use Connecting Words and Connecting Phrases to Connect Sentences:** After splitting a semicolon sentence, use a connecting word or phrase to show the logical relationship between the two new sentences. The connecting word replaces the semicolon and adds semantic clarity.
- **Rule 8.2 — Use Hyphens to Connect Words That Are Directly Related:** Hyphens connect words. Semicolons connect clauses. Do not confuse these two punctuation marks. If you are connecting words, use a hyphen. If you are connecting clauses, split into two sentences.
- **STE-Code Dictionary — Section: Punctuation:** The dictionary defines all approved punctuation marks and their usage constraints. Consult it for the full list of permitted punctuation and the rules for each mark.

## Grammar Notes

### The Semicolon as a Clause Joiner

In standard English grammar, the semicolon joins two independent clauses that are closely related in meaning. The clauses must each be able to stand as a complete sentence. This grammatical requirement means that a semicolon sentence always contains two complete subject-verb structures — effectively two sentences compressed into one.

STE-Code rejects this compression on cognitive grounds. A reader must parse the first clause, hold it in working memory, parse the second clause, and then integrate the relationship between them. For non-native English readers — the majority audience of most open-source documentation — this two-clause parsing is measurably harder than processing two separate sentences. The period between sentences gives the reader a full cognitive break. The semicolon denies that break.

### The Semicolon as a Super-Comma

In standard English, semicolons also serve as "super-commas" — stronger separators than commas, used in lists where the list items themselves contain commas. For example: "The team includes Alice, the architect; Bob, the lead developer; and Carol, the designer."

STE-Code does not permit this usage. The super-comma forces the reader to maintain a stack of nesting levels: list items separated by semicolons, sub-items separated by commas. This nested structure violates Rule 3.1 (simple sentences) and the two-level nesting limit. The fix is to restructure the list using bullets, dashes, or a table — formats that make the nesting visually explicit rather than encoding it in punctuation.

### Programming Language Interference

Many programming languages use the semicolon as a statement terminator (C, C++, Java, JavaScript, Rust, Go, and others). Developers who write documentation for these languages have deeply ingrained muscle memory for the semicolon. They read and write semicolons thousands of times per day in code. When switching to documentation prose, this muscle memory can cause unconscious semicolon insertion — the writer types a semicolon out of habit, not because the sentence needs one.

This cognitive interference is unique to code documentation. An aerospace technical writer does not type semicolons in a C compiler all day before writing the aircraft maintenance manual. The code documentation writer does. Rule 8.1 is therefore more important — and harder to obey — in code documentation than in the original aerospace domain. Review your documentation prose separately from your code. Look specifically for semicolons that belong in code but not in prose.

### The Period as the Only Sentence Boundary

STE-Code recognizes exactly three sentence-ending punctuation marks: the period (.), the question mark (?), and the exclamation mark (!). The semicolon, colon (when used between clauses), and em-dash (when used to separate clauses) are not sentence boundaries. This means a text that uses semicolons cannot be mechanically checked for sentence length (Rule 4.1) because the tool does not know where one sentence ends and the next begins.

When every sentence boundary is a period, automated rule checkers can reliably count words per sentence. This mechanical verifiability is a deliberate design goal of STE-Code: a tool should be able to validate compliance without understanding the semantics. Semicolons break this property by hiding sentence boundaries inside a single punctuation-delimited string.

### Semicolon Avoidance in Technical Writing Traditions

The prohibition on semicolons is not unique to STE. Several major technical style guides discourage or limit semicolons in technical prose. The Microsoft Writing Style Guide recommends avoiding semicolons in technical content. The Google Developer Documentation Style Guide advises writers to "prefer shorter sentences" over semicolon-joined clauses. The Chicago Manual of Style permits semicolons but notes they are "not common in technical writing."

STE-Code takes the strongest position: a complete ban. This is consistent with the STE philosophy that documentation must be understandable by non-native English speakers under operational pressure. A developer debugging a production incident at 3:00 AM should not have to parse a semicolon-joined sentence to find the recovery procedure. Each sentence must deliver one complete, actionable thought with no internal clause boundaries.
