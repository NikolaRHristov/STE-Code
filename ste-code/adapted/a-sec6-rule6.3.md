# Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence.

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.3

## Original Rule

Good technical writing uses short sentences for complex topics. Short sentences give a clear structure to your writing and make information easier to understand.

In descriptive writing, the maximum sentence length is 25 words. This is because descriptive text is more complex than procedural text.

## STE-Code Adaptation

Good code documentation uses short sentences for complex topics. Short sentences give a clear structure to your documentation and make information easier to understand.

In descriptive code documentation, the maximum sentence length is 25 words. This is because descriptive text is more complex than procedural text.

### Examples

> **STE:** The authentication middleware validates each incoming request before the controller processes it. (11 words)
>
> *Code-domain example — a short, single-subject sentence that respects the 25-word limit.*

> **Non-STE:** This function provides the ability to run arbitrary software applications within a sandboxed execution environment that isolates system resources. (21 words)
>
> **STE:** This function lets you run software applications in a sandbox. The sandbox isolates system resources. (8 words and 5 words)
>
> *Code-domain example — breaking one complex sentence into two shorter sentences improves clarity, even when the original is under 25 words.*

> **Non-STE:** The configuration loader reads the YAML manifest file from the filesystem and parses it into an in-memory representation that other modules can query at runtime to determine their operational parameters. (32 words)
>
> **STE:** The configuration loader reads the YAML manifest file from the filesystem. It parses the file into an in-memory representation. Other modules can query this representation at runtime. They use it to find their operational parameters. (20 words, 8 words, 7 words, and 8 words)
>
> *Code-domain example — a 32-word sentence is split into four sentences, each under the 25-word limit.*

> **Non-STE:** The cache invalidation strategy employs a time-to-live mechanism combined with a least-recently-used eviction policy to ensure that stale data is removed and memory consumption remains within the allocated heap budget. (34 words)
>
> **STE:** The cache invalidation strategy uses a time-to-live mechanism. It also uses a least-recently-used eviction policy. Together, these mechanisms remove stale data. They also keep memory consumption within the allocated heap budget. (16 words, 10 words, 7 words, and 10 words)
>
> *Code-domain example — a 34-word sentence is split into four sentences, each under the 25-word limit.*

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure; Rule 6.4 — Use Paragraphs to Show Related Information; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic

## Code-Domain Explanation

### README Files

README files are the first document a new contributor reads. Long sentences in a README hide the essential information. Break each concept into its own sentence. Use one sentence to describe the project. Use another to list the prerequisites. Use a third to give the install command.

A README that obeys the 25-word limit helps readers scan quickly. They can find the install steps without reading a dense paragraph. They can find the API example without parsing a complex sentence.

### API Documentation

API reference docs describe endpoints, parameters, responses, and error codes. Each of these parts must stand alone. A 40-word sentence that mixes the URL, the method, the parameters, and the response is not useful. Instead, use one short sentence for each part.

For example, describe the endpoint path and method in one sentence. Describe each parameter in its own sentence. Describe the response schema in separate sentences for each field. This structure matches the way developers read API docs: they scan for the one detail they need.

### Docstrings

Docstrings have limited space. A short sentence communicates the function's purpose. If the docstring has one 30-word sentence, the reader must parse it fully to understand the function. If the docstring has two 12-word sentences, the reader gets the purpose and the return value separately.

Follow this pattern for docstrings: one sentence for the purpose, one sentence for each parameter, one sentence for the return value, and one sentence for each exception. Each sentence must stay under 25 words.

### Commit Messages

Commit messages benefit from the same discipline. A commit subject line must not exceed 72 characters. But the sentence structure also matters. Use one short sentence to describe the change. Use additional short sentences in the body to explain why.

Avoid packing multiple logical changes into one sentence. If the commit does three things, use three sentences. This makes `git log` output readable and bisect debugging faster.

### Error Messages

Error messages must be clear and actionable. A long error message buries the cause and the fix. A short error message tells the user what failed and what to do next.

Structure error messages in two parts: the problem and the action. For example: "The database connection failed. Check your network connection and credentials." Each part is a short sentence under 25 words.

Error messages in log files also benefit from short sentences. Log aggregation tools parse messages by line. A single long sentence that spans 40 words is harder to search and filter.

## Paradigm-Specific Guidance

### Object-Oriented Documentation

Object-oriented code has class hierarchies, inheritance chains, and interface implementations. These relationships cause long descriptive sentences. A developer writes: "The `AuthenticatedController` class extends `BaseController` and implements the `Auditable` and `Loggable` interfaces to provide authentication-aware request handling with audit trail support." This is 26 words.

Instead, break the inheritance and the behavior into separate sentences:

> The `AuthenticatedController` class extends `BaseController`. It implements the `Auditable` and `Loggable` interfaces. These interfaces add authentication-aware request handling. They also add audit trail support.

When documenting a class with many methods, do not describe all methods in one sentence. Describe each method in its own sentence or paragraph.

### Functional Documentation

Functional code often uses composition, pipelines, and monadic chains. The documentation for these patterns can become dense. A writer explains: "The `processOrder` function composes `validateOrder`, `calculateTotal`, and `applyDiscount` through a monadic pipeline that short-circuits on the first validation failure and accumulates errors in an `Either` type." This is 32 words.

Split the composition from the error behavior:

> The `processOrder` function composes three functions: `validateOrder`, `calculateTotal`, and `applyDiscount`. It uses a monadic pipeline. The pipeline stops on the first validation failure. It collects errors in an `Either` type.

Pure function signatures are short by nature. But the prose that explains them must also be short.

### Procedural Documentation

Procedural code follows a sequence of steps. Documentation for procedural code maps naturally to short sentences. Each step becomes one sentence. Each sentence describes one action.

Do not combine three steps into one sentence. This pattern: "The function allocates a buffer, copies the input data into the buffer, and returns a pointer to the caller." is acceptable at 22 words. But it is better to split the allocation from the copy for clarity when safety is important:

> The function allocates a buffer. It copies the input data into the buffer. It returns a pointer to the caller.

Procedural documentation for C and Go code often documents preconditions and postconditions. Give each condition its own sentence.

### Declarative Documentation

Declarative code includes SQL schemas, Terraform configurations, and Kubernetes manifests. These documents describe the desired state. Long sentences mix resource properties and make the schema difficult to read.

For Terraform, document each resource block separately. For each resource, document each argument in its own sentence. Do not write: "The `aws_instance` resource creates an EC2 instance in the specified subnet with the given security groups and attaches the provided IAM instance profile." This is 28 words.

Instead:

> The `aws_instance` resource creates an EC2 instance. It launches the instance in the specified subnet. It applies the given security groups. It attaches the provided IAM instance profile.

### Systems Documentation

Systems documentation describes memory models, ownership rules, and concurrency guarantees. These topics are inherently complex. Short sentences are essential here.

Rust ownership documentation is a good example. The Rust Book uses short sentences to explain borrowing and lifetimes. A concept like "the borrow checker ensures that references do not outlive the data they refer to by tracking lifetimes at compile time" is 25 words. But Rust documentation often splits this further:

> The borrow checker tracks references. It makes sure that references do not outlive their data. It does this at compile time. It uses lifetimes to enforce these rules.

Systems documentation also covers unsafe code blocks, FFI boundaries, and memory layout. These are safety-critical topics. Short sentences reduce the risk of misunderstanding.

## Extended Examples

### Example 4 — API Endpoint Documentation

> **Non-STE:** The `GET /api/v2/users` endpoint returns a paginated list of user objects sorted by creation date in descending order with an optional query parameter to filter results by account status. (30 words)
>
> **STE:** The `GET /api/v2/users` endpoint returns a paginated list of user objects. The list is sorted by creation date in descending order. You can use the `status` query parameter to filter results. (18 words, 9 words, and 12 words)
>
> *Principles applied: P1, P2 — short sentences make each API detail independently scannable. The original sentence mixes four concepts (method, sorting, pagination, filtering). The STE version gives each concept its own sentence.*

### Example 5 — Commit Message Body

> **Non-STE:** Refactored the JWT middleware to extract token validation into a separate utility module and added comprehensive error handling for expired tokens, malformed headers, and missing claims with descriptive log messages. (31 words)
>
> **STE:** Refactor the JWT middleware. Extract the token validation logic into a utility module. Add error handling for expired tokens. Add error handling for malformed headers. Add error handling for missing claims. Include descriptive log messages. (12 words, 9 words, 7 words, 7 words, 7 words, and 4 words)
>
> *Principles applied: P1, P8, P12 — the imperative mood for commits is preserved. Each logical change gets its own sentence. The git log becomes scannable line by line.*

### Example 6 — Error Message

> **Non-STE:** The database connection could not be established because the server at the specified hostname was unreachable due to a network timeout or the provided credentials were invalid after the maximum number of retry attempts. (34 words)
>
> **STE:** The database connection failed. The server is not reachable. Or the credentials are not valid. Check your network connection. Check your credentials. (4 words, 5 words, 6 words, 5 words, and 3 words)
>
> *Principles applied: P1, P3, P10 — short error messages tell the user exactly what to do. Each possible cause gets its own sentence. Each action gets its own sentence.*

### Example 7 — Class Constructor Docstring

> **Non-STE:** Initializes a new instance of the `HttpClient` class with the specified base URL string and an optional dictionary of default HTTP headers along with a retry policy configuration that determines how many times a failed request should be retried before the client throws a `MaxRetriesExceededException`. (43 words)
>
> **STE:** Make a new `HttpClient` instance. Use the specified base URL. Use the optional default headers dictionary. Set a retry policy. The policy sets the number of retries. The client throws `MaxRetriesExceededException` when retries run out. (7 words, 5 words, 6 words, 4 words, 7 words, and 11 words)
>
> *Principles applied: P1, P2, P4, P12 — each constructor parameter gets its own sentence. The exception behavior is separated from the parameter list. The docstring is readable line by line.*

### Example 8 — README Project Description

> **Non-STE:** This project is a lightweight, high-performance logging library designed for distributed microservices architectures that supports structured JSON output, log level filtering, and asynchronous batch writing to multiple backends including Elasticsearch, Loki, and CloudWatch. (36 words)
>
> **STE:** This project is a lightweight logging library. It is designed for distributed microservices. It supports structured JSON output. It supports log level filtering. It supports asynchronous batch writing. It writes to multiple backends. These backends include Elasticsearch, Loki, and CloudWatch. (10 words, 6 words, 5 words, 5 words, 4 words, 9 words, and 8 words)
>
> *Principles applied: P1, P8, P11 — the project description is split into one sentence per feature. A reader can scan the feature list without parsing a dense paragraph. Each backend is listed in a separate sentence for clarity.*

### Example 9 — Release Notes Entry

> **Non-STE:** The v2.4 release introduces a new caching layer that reduces database query latency by 60 percent on average across all API endpoints and also includes a fix for the race condition that occurred when multiple workers attempted to update the same configuration key simultaneously. (44 words)
>
> **STE:** The v2.4 release adds a new caching layer. This layer reduces database query latency by 60 percent. The improvement applies to all API endpoints. This release also fixes a race condition. The race condition occurred during concurrent configuration updates. (10 words, 8 words, 8 words, 7 words, and 9 words)
>
> *Principles applied: P1, P2, P12 — release notes are read by users and operators. Short sentences help them find breaking changes and new features quickly. The problem and the fix get separate sentences.*

## Edge Cases

### Edge Case 1 — Long Technical Terms

Some technical terms are multi-word phrases that count as a single unit: "single sign-on," "continuous integration and continuous deployment," "Hypertext Transfer Protocol Secure." These phrases add word count without adding complexity.

When a long technical term pushes a sentence over 25 words, check if the sentence can be split in another way. If the term itself is the bottleneck, use the acronym after the first mention. The acronym reduces the word count for subsequent sentences.

> **Non-STE:** The single sign-on integration with the external identity provider requires that the user has already been provisioned in the downstream application before the first authentication attempt. (28 words)
>
> **STE:** The single sign-on (SSO) integration requires an external identity provider. The user must be provisioned in the downstream application. This must happen before the first authentication attempt. (11 words, 8 words, and 8 words)

### Edge Case 2 — Code Keywords That Are Also Long

Some languages use verbose keywords. For example, `synchronized` in Java, `concurrent.futures` in Python, or `__attribute__((constructor))` in C. When a keyword appears in a sentence, count it as one word. But keep the rest of the sentence short.

Do not let verbose keywords justify long sentences. If the keyword adds 3 words, compensate with shorter phrasing elsewhere.

### Edge Case 3 — Compound Type Signatures

Type signatures in TypeScript, Rust, and Scala can be long. Describing a complex generic type in a sentence often exceeds 25 words. Split the description: one sentence for the type shape, another for the constraints, and another for the behavior.

Avoid this pattern: "The function accepts a generic type parameter `T` that must implement both the `Serialize` and `Deserialize` traits and returns a `Result<Vec<T>, ParseError>` wrapped in a `Future`." This is 30 words.

Use this pattern instead:

> The function accepts a generic type parameter `T`. The type must implement `Serialize` and `Deserialize`. The function returns a `Result<Vec<T>, ParseError>`. The result is wrapped in a `Future`.

### Edge Case 4 — Legal and License Text

License headers and legal disclaimers are not covered by Rule 6.3. These texts follow legal conventions, not technical writing standards. Do not apply the 25-word limit to MIT, Apache, or GPL license text. Do not apply it to copyright notices.

However, the surrounding documentation that explains the license choice should obey the 25-word limit.

### Edge Case 5 — Generated Documentation

Auto-generated documentation from tools like JSDoc, Sphinx, or `go doc` may produce long sentences from source code comments. The generator does not enforce the 25-word limit. But the source comments that feed the generator should obey the rule.

Fix the source docstrings. Do not edit the generated output directly. The generated output reflects the quality of the input.

## Cross-References

Rule 6.3 is part of the Sentence Length cluster in Section 6. These rules work together:

- **Rule 6.1 — Give Information Gradually:** Short sentences enable gradual information delivery. Each sentence adds one new piece of information. Long sentences deliver too much information at once. The reader cannot absorb it.

- **Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure:** Short sentences make key words visible. A keyword at the start of a sentence signals the topic. A keyword buried in the middle of a 35-word sentence loses its signal value.

- **Rule 6.4 — Use Paragraphs to Show Related Information:** Short sentences form clear paragraphs. A paragraph of three 12-word sentences is easier to read than one 36-word sentence. Use paragraphs to group related short sentences.

- **Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic:** Short sentences help each paragraph stay on topic. When each sentence is short, the writer can see when a sentence drifts to a new topic. The writer can then start a new paragraph.

- **Rule 1.1 — Use Approved Words from the STE-Code Dictionary:** Short sentences reduce the need for complex vocabulary. When you must fit many ideas into one sentence, you reach for longer words. When you split the ideas, each sentence uses simpler words.

- **Rule 1.10 — No Slang, Jargon, or Regional Terms:** Short sentences reduce the temptation to use jargon. Long sentences are a place where jargon hides. When each sentence is short, jargon stands out and can be removed.

## Grammar Notes

### Clause Density

Long sentences in code documentation often contain multiple clauses. Each clause adds a subject, a verb, and an object. The reader must hold the first clause in memory while parsing the second. With three or more clauses, the reader loses the thread.

The 25-word limit indirectly limits clause density. Most English clauses are 6 to 12 words. A 25-word sentence can hold at most two clauses with connecting words. This is a natural limit that matches working memory capacity.

### Coordination vs. Subordination

Coordination joins two independent clauses with "and," "but," or "or." Subordination makes one clause dependent on another with "because," "when," "if," or "although."

Code documentation overuses subordination. A writer says: "The `parse` function throws a `SyntaxError` when the input string contains invalid JSON because the parser cannot construct a valid AST from malformed tokens." This is 27 words with three levels of subordination.

Prefer coordination with separate sentences:

> The `parse` function throws a `SyntaxError`. This error occurs when the input string contains invalid JSON. The parser cannot construct a valid AST from malformed tokens.

### Implicit Connectives

Short sentences rely on implicit connectives. The reader infers the relationship between sentences from their order. This is different from academic writing, which uses explicit connectives like "therefore," "consequently," and "furthermore."

In code documentation, implicit connectives work well. The reader expects documentation to flow from purpose to usage to edge cases. Short sentences in that order need no explicit glue.

### Counting Rules

Count hyphenated compound words as one word. For example, "least-recently-used" counts as one word, not three. Count acronyms as one word: "JSON" is one word. Count code tokens as one word: `Result<Vec<T>>` is one word.

Do not count parenthetical word counts in examples. The notation "(12 words)" in an example sentence is metadata, not part of the sentence.
