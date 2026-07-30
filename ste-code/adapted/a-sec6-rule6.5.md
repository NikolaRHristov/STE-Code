# Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.5

## Original Rule

In descriptive writing, paragraphs describe topics, and it is important that each paragraph has only one topic. The topic sentence is the first and most important sentence in a paragraph. The topic sentence gives new information and makes a logical connection between the new information and previous information. To make a logical connection in a paragraph, the topic sentence usually contains a key word and/or a connecting word or connecting phrase.

From the topic sentences, the reader will understand the contents of your text and will find the applicable information quickly. If the reader writes down each of the topic sentences from a text, they will make a good outline of its content. The other sentences in each paragraph give the information a logical structure and add more information on the topic of the paragraph.

## STE-Code Adaptation

In descriptive code documentation, paragraphs describe topics, and it is important that each paragraph has only one topic. The topic sentence is the first and most important sentence in a paragraph. The topic sentence gives new information and makes a logical connection between the new information and previous information. To make a logical connection in a paragraph, the topic sentence usually contains a key word and/or a connecting word or connecting phrase.

From the topic sentences, the developer will understand the contents of your documentation and will find the applicable information quickly. If the developer writes down each of the topic sentences from the documentation, they will make a good outline of its content. The other sentences in each paragraph give the information a logical structure and add more information on the topic of the paragraph.

### Examples

> **Non-STE:** The authentication middleware validates each request and the logging system records all validation failures to the audit trail while the response pipeline returns JSON error bodies with error codes and the database connection pool maintains idle connections for reuse and the configuration module reloads settings when the manifest file changes on disk.

> **STE:** [FIXME: generate STE correction for: The authentication middleware validates each request and the...]
>
> The authentication middleware validates each incoming request. The middleware reads the bearer token from the `Authorization` header. It sends the token to the `validateToken` function in the `security` module. The `validateToken` function decodes the JWT payload using the `HS256` algorithm from the `jwt-signer` library. Then it compares the `exp` claim with the current server time. If the token is not expired and not malformed, the function gets the `sub` and `role` claims and attaches them to the `request.auth` object.
>
> If the token is expired, the middleware returns a `401 Unauthorized` response. The response body is a JSON object with a `message` field and an `errorCode` field set to `TOKEN_EXPIRED`. If the token is malformed, the middleware returns a `401 Unauthorized` response with the `errorCode` field set to `TOKEN_MALFORMED`.
>
> The middleware also logs each failure to the audit trail. It calls the `AuditLogger.log` static method. This method writes a record to the `audit_events` table in the primary database. The write uses an asynchronous pattern that does not block the response pipeline.
>
> *Code-domain example — the Non-STE version combines multiple topics into one sentence; the STE version separates them into three paragraphs, each with one topic.*

In the STE text, the documentation is divided into three paragraphs:

- Paragraph 1 – The topic is: "How the authentication middleware validates a token."
- Paragraph 2 – The topic is: "What error responses the middleware returns."
- Paragraph 3 – The topic is: "How the middleware logs failures to the audit trail."

When you read only the topic sentences, you get an outline of the documentation:

- "The authentication middleware validates each incoming request."
- "If the token is expired, the middleware returns a `401 Unauthorized` response."
- "The middleware also logs each failure to the audit trail."

## Code-Domain Explanation

This rule applies differently to each type of code documentation. The core principle is the same: one topic per paragraph. But the definition of a "topic" changes with the documentation format.

### README Files

A README file is the first document a developer reads. Each section of the README must focus on one topic. For example, the "Installation" section must not also explain the API design. The "Configuration" section must not show usage examples.

A good README has these one-topic paragraphs:

- **What the project does** — one paragraph that gives the purpose.
- **How to install** — one paragraph per platform or method.
- **How to configure** — one paragraph per configuration group.
- **How to contribute** — one paragraph per contribution type.

If a README paragraph starts to discuss two different things, split it. The topic sentence in each paragraph tells the developer what to expect next.

### API Documentation

API reference pages describe endpoints, parameters, and responses. Each paragraph must cover exactly one aspect of the API:

- One paragraph for the endpoint purpose.
- One paragraph for the request format.
- One paragraph for each response status code group (success, client error, server error).
- One paragraph for authentication requirements.

Do not mix the description of a `200 OK` response with the description of a `404 Not Found` response. Give each status code its own paragraph.

### Docstrings and Inline Comments

A function docstring is a small paragraph. It must describe only what the function does. Do not use the docstring to:

- Explain why the function exists (put that in the module docstring).
- Describe side effects of other functions.
- List all callers of the function.

The topic of a docstring is the function's contract: its inputs, its outputs, and its behavior.

### Commit Messages

A commit message is a one-paragraph description of one change. If a commit has two unrelated changes, it should be two commits. The topic sentence of a commit message (the subject line) must summarize the change. The body must expand only on that change.

### Error Messages

An error message is a one-topic paragraph. It must tell the developer:

- What went wrong (one sentence).
- Why it went wrong (one sentence).
- How to fix it (one sentence, if applicable).

Do not include stack traces, debugging hints, or unrelated system state in the error message body. Put those in a log file or a debug panel.

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Class documentation must use one paragraph per concern:

- One paragraph for the class purpose and its role in the system.
- One paragraph for the constructor and initialization requirements.
- One paragraph for the public interface (methods grouped by behavior).
- One paragraph for inheritance and interface implementation.
- One paragraph for thread safety guarantees.

Do not describe the internal implementation of a method in the class-level documentation. That is a different topic. Put method implementation details in the method docstring.

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional code emphasizes data transformations and pure functions. Each paragraph must focus on one transformation:

- One paragraph for the input data shape.
- One paragraph for the transformation logic.
- One paragraph for the output data shape.
- One paragraph for edge cases (empty input, error values).

In a pipeline of composed functions, document each stage in its own paragraph. Do not describe the whole pipeline in one dense block.

### Procedural Documentation (C, Go, Bash)

Procedural code follows step-by-step sequences. Each paragraph must document one step or one phase:

- One paragraph for the initialization phase.
- One paragraph for the main processing loop.
- One paragraph for the cleanup phase.
- One paragraph for error handling.

In a shell script, document each major command block in its own paragraph. Do not merge the description of the `setup` function with the `teardown` function.

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative code describes desired state. Each paragraph must describe one resource or one constraint:

- One paragraph per table or view in SQL schema documentation.
- One paragraph per Terraform resource block.
- One paragraph per Kubernetes object (Deployment, Service, ConfigMap).

Do not describe a Kubernetes Deployment and its associated Service in one paragraph. Even though they work together, they are separate topics.

### Systems Documentation (Rust Ownership, C Memory)

Systems code documents memory and ownership patterns. Each paragraph must cover one ownership relationship or one memory lifecycle:

- One paragraph for allocation strategy.
- One paragraph for ownership transfer points.
- One paragraph for deallocation guarantees.
- One paragraph for unsafe blocks and their safety invariants.

Do not document both the allocation and the deallocation of a resource in one paragraph unless they are the same topic (for example, RAII patterns where construction and destruction are one lifecycle).

## Extended Examples

### Example 2 — API Endpoint Documentation

> **Non-STE:** The `POST /users` endpoint creates a new user in the database, sends a welcome email via the `EmailService`, hashes the password using bcrypt with a cost factor of 12, returns a `201 Created` response with the user's public profile in JSON format, and if the email is already taken it returns a `409 Conflict` with an error message while also rate-limiting requests to 10 per minute per IP address using the token bucket algorithm implemented in the `RateLimiter` middleware.

> **STE:** [FIXME: generate STE correction for: The `POST /users` endpoint creates a new user in the databas...]
>
> The `POST /users` endpoint creates a new user account. The endpoint accepts a JSON body with `email`, `password`, and `name` fields. It hashes the password using bcrypt with a cost factor of 12. It stores the user record in the `users` table of the primary database. On success, the endpoint returns a `201 Created` response. The response body contains the user's public profile as a JSON object.
>
> The `EmailService` sends a welcome email after the user record is created. The email send is asynchronous. It does not block the HTTP response.
>
> If the email is already in use, the endpoint returns a `409 Conflict` response. The response body contains a JSON object with an `error` field set to `EMAIL_TAKEN`.
>
> The `RateLimiter` middleware limits requests to this endpoint. The limit is 10 requests per minute per IP address. The middleware uses a token bucket algorithm.
>
> *Principles applied: P1, P11. The Non-STE version mixes five topics (creation, email, error, rate limit, response format) into one sentence. The STE version gives each topic its own paragraph with a clear topic sentence.*

### Example 3 — README Installation Section

> **Non-STE:** To install this project, clone the repository and run `npm install` which downloads all dependencies including `express` for the server, `pg` for the PostgreSQL client, and `redis` for caching, then copy `.env.example` to `.env` and fill in your database credentials and API keys, and finally run `npm run migrate` to set up the database schema and `npm run seed` to populate it with sample data, after which you can start the development server with `npm run dev` which starts on port 3000 by default but you can change it with the `PORT` environment variable and it also starts a WebSocket server on the same port for real-time features.

> **STE:** [FIXME: generate STE correction for: To install this project, clone the repository and run `npm i...]
>
> To install the project, clone the repository and run `npm install`. This command downloads all Node.js dependencies.
>
> Configure the environment variables. Copy the `.env.example` file to `.env`. Set the `DATABASE_URL` and `API_KEY` values in the `.env` file.
>
> Set up the database. Run `npm run migrate` to create the schema. Run `npm run seed` to add sample data.
>
> Start the development server with `npm run dev`. The server listens on port 3000 by default. To change the port, set the `PORT` environment variable. The server also starts a WebSocket server on the same port.
>
> *Principles applied: P1, P3. The Non-STE version is one long sentence covering four distinct topics (dependency install, configuration, database setup, server start). Each STE paragraph has one topic with supporting sentences.*

### Example 4 — Commit Message

> **Non-STE:** Fix the login bug where users could not authenticate after password reset, also refactored the user service to use the new repository pattern, and updated the dependencies to latest versions because there was a security vulnerability in the old express version, plus added a loading spinner to the login page.

> **STE:** [FIXME: generate STE correction for: Fix the login bug where users could not authenticate after p...]
>
> Fix authentication failure after password reset
>
> The `validatePasswordResetToken` function used a stale database connection. It did not pick up the new password hash after the reset completed. This commit changes the function to use a fresh connection from the pool for each validation.
>
> *Principles applied: P1, P6. The Non-STE commit message has four unrelated topics (bug fix, refactor, dependency update, UI change). The STE version is one commit with one topic. The other changes belong in separate commits.*

### Example 5 — Class Documentation (OOP)

> **Non-STE:** The `PaymentProcessor` class handles all payment operations including credit card validation through the Stripe API, PayPal integration, refund processing which requires a 24-hour waiting period, receipt generation as a PDF, and it also manages the transaction log for audit purposes while maintaining compliance with PCI-DSS standards and logging all operations to the audit trail.

> **STE:** [FIXME: generate STE correction for: The `PaymentProcessor` class handles all payment operations ...]
>
> The `PaymentProcessor` class handles payment transactions. It validates payment methods, processes charges, and issues refunds.
>
> The class supports two payment providers: Stripe and PayPal. Each provider has a separate adapter class. The `PaymentProcessor` delegates provider-specific logic to the applicable adapter.
>
> Refund processing has a 24-hour waiting period. The `processRefund` method checks the transaction age before it starts the refund. If the transaction is less than 24 hours old, the method returns a `REFUND_NOT_AVAILABLE` error.
>
> The class generates a PDF receipt after each successful charge. It calls the `ReceiptGenerator` service with the transaction details.
>
> All operations write an entry to the `transaction_log` table. The logger uses an asynchronous write pattern. The class also enforces PCI-DSS compliance rules during payment method validation.
>
> *Principles applied: P1, P8. The Non-STE version covers payment processing, provider adapters, refund policy, receipt generation, transaction logging, and compliance in one paragraph. The STE version gives each concern its own paragraph.*

### Example 6 — Error Message

> **Non-STE:** Connection refused — the database is probably down or the credentials are wrong, check your `.env` file and make sure the `DATABASE_URL` is correct, also make sure the VPN is connected if you are working remotely, and verify that the database server is running on the specified port, you can check this with `pg_isready` if you are using PostgreSQL, otherwise use the equivalent tool for your database.

> **STE:** [FIXME: generate STE correction for: Connection refused — the database is probably down or the cr...]
>
> Connection refused: the database server did not accept the connection.
>
> Possible causes:
> - The database server is not running.
> - The `DATABASE_URL` value in the `.env` file is not correct.
> - A firewall or VPN blocks the connection.
>
> To fix this problem, check that the database server is running. Verify the `DATABASE_URL` value. Make sure that your network allows connections to the database port.
>
> *Principles applied: P1, P3, P10. The Non-STE error message mixes symptoms, causes, and solutions with informal language ("probably", "also make sure"). The STE version separates the description, the causes, and the fix steps into distinct paragraphs.*

### Example 7 — Configuration Documentation

> **Non-STE:** The cache module supports Redis for production and an in-memory store for development, you configure it by setting `CACHE_DRIVER` to either `redis` or `memory`, and when using Redis you also need to set `REDIS_URL` and `REDIS_PREFIX` and optional `REDIS_TIMEOUT` in milliseconds which defaults to 5000, and the in-memory store has a `MAX_ITEMS` setting that defaults to 1000, and if you exceed that limit it evicts the least recently used items, also Redis supports clustering by setting multiple URLs in `REDIS_CLUSTER_URLS` as a comma-separated list.

> **STE:** [FIXME: generate STE correction for: The cache module supports Redis for production and an in-mem...]
>
> The cache module supports two drivers: Redis and in-memory. Set the `CACHE_DRIVER` environment variable to `redis` or `memory`.
>
> When you use the Redis driver, set these environment variables:
> - `REDIS_URL` — the connection string for the Redis server.
> - `REDIS_PREFIX` — a namespace prefix for all cache keys.
> - `REDIS_TIMEOUT` — the connection timeout in milliseconds. The default value is 5000.
>
> The Redis driver also supports clustering. Set the `REDIS_CLUSTER_URLS` variable to a comma-separated list of Redis node URLs.
>
> When you use the in-memory driver, set the `MAX_ITEMS` variable. It controls the maximum number of cache entries. The default is 1000. If the cache is full, the driver removes the least recently used items.
>
> *Principles applied: P1, P11. The Non-STE version jumps between Redis config, memory config, eviction policy, and clustering without paragraph breaks. The STE version gives each configuration group its own paragraph.*

## Edge Cases

### Framework Names That Are Also Unapproved Words

Some framework names use words that STE-Code marks as unapproved. For example, a framework named "Execute" conflicts with the STE synonym table (use "do" or "run").

**Guidance:** Framework names are technical code nouns (Rule 1.5). They are allowed. But do not use the framework name as a verb in the same paragraph. This confuses the topic. Write:

"Use the `Execute` library to run background jobs."

not:

"Execute background jobs with the `Execute` library."

### Large Multi-Topic Functions

Some legacy functions do many things. Documenting them with one topic per paragraph is difficult because the function itself has no single topic.

**Guidance:** Use the function's docstring to list its responsibilities as bullet points. Then give each responsibility its own paragraph in the module-level documentation. The docstring serves as a topic index. The module documentation gives each topic its full treatment.

### Generated Documentation

Generated API docs (JSDoc, Sphinx, rustdoc) merge docstrings from many functions into one page. The page as a whole may cover many topics. But each individual docstring must still follow the one-topic rule.

**Guidance:** Do not relax this rule for generated docs. The tool combines the paragraphs. The writer is responsible for making sure each docstring is a self-contained topic.

### Cross-Cutting Concerns

Some documentation topics cut across the codebase. Security, performance, and accessibility are cross-cutting concerns. They affect many modules.

**Guidance:** Give cross-cutting concerns their own document or their own top-level section. Do not sprinkle partial security notes across every module's documentation. In each module, write a one-paragraph summary with a link to the full security document.

### Error Code Reference Tables

Error code reference pages list many error codes in a table. Each row is a separate topic (one error, one paragraph). But the table itself is a single structural element.

**Guidance:** The table is the container. Each cell that contains a description is a mini-paragraph. Apply the one-topic rule to each cell. One cell must describe only one error condition.

## Grammar Notes

The original ASD-STE100 Rule 6.5 has no explicit grammatical rules. It is a structural rule about paragraph composition. But the rule implies several grammatical patterns that are useful for code documentation.

### Topic Sentence Position

In English technical writing, the topic sentence is usually the first sentence of the paragraph. This is the "deductive" paragraph structure. It gives the reader the main point immediately. Code documentation must always use deductive paragraphs.

Do not use "inductive" paragraphs where the topic sentence comes last. Developers scan documentation. They do not read every word in order. A topic sentence at the end of the paragraph is invisible to a scanning reader.

### Key Word Repetition

The topic sentence introduces a key word (or key phrase). The supporting sentences must repeat that key word or use a clear synonym. This repetition tells the reader: "I am still on the same topic."

For example, if the topic sentence is "The cache module supports two drivers," the supporting sentences must repeat "driver" or "cache module." If a sentence introduces a new key word without connecting it to the original topic, the paragraph has drifted.

### Connecting Words and Phrases

Use connecting words to link the topic sentence to the previous paragraph:

- "Also," — adds information on the same topic from a different angle.
- "However," — introduces a contrast or exception.
- "For example," — gives a concrete instance of the topic.
- "Therefore," — gives a result or consequence.

These connecting words belong in the topic sentence. They make the logical structure of the document explicit.

### Paragraph Length in Code Documentation

A paragraph in code documentation should be 3 to 7 sentences. A one-sentence paragraph is acceptable for a topic that is simple. But a paragraph of 10 or more sentences almost always has more than one topic. If a paragraph grows long, check for topic drift.

The procedural sentence structure of Rule 6.3 (maximum 25 words per sentence) helps control paragraph length. Short sentences make topic drift more visible because each sentence has less content to hide multiple topics.

### Visual Paragraph Separation

In markdown documentation, separate paragraphs with a blank line. Do not use indentation-only separation. Screen readers and some markdown renderers do not recognize indentation as a paragraph break.

In docstrings, use reStructuredText or JSDoc conventions for paragraph breaks. A blank line in a docstring is the standard way to separate paragraphs.

## Cross-References

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure; Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence; Rule 6.4 — Use Paragraphs to Show Related Information

### Related Rules in Other Sections

- **Rule 1.11 (One Term Per Concept):** Consistent terminology across paragraphs prevents the reader from thinking a new topic has started when it has not.
- **Rule 3.6 (Use the Approved Forms of Verbs):** The topic sentence usually starts with a verb in the simple present tense. Consistent verb forms help the reader identify topic sentences across paragraphs.
- **Rule 5.1 (Write Instructions in the Imperative Mood):** Procedural paragraphs have a different topic structure than descriptive paragraphs. Each step is its own micro-topic.
- **Rule 6.6 (Use Lists Where Applicable):** When a paragraph contains a series of related items, a list is usually clearer. But each list item must relate to the paragraph's single topic.

### STE-Code Dictionary Reference

The STE-Code dictionary defines approved words and their approved meanings. When you write a paragraph about a technical concept, check that your topic sentence uses an approved word from the dictionary. If the concept has no approved word, you must define it in the glossary before you use it as a paragraph topic.
