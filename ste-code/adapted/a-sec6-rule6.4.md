# Rule 6.4 — Use Paragraphs to Show Related Information

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.4

## Original Rule

In procedures, work steps usually have numbers and letters to show their sequence. In descriptive writing, paragraphs keep related information together and give a logical sequence to the text.

In STE, a paragraph starts with a "topic sentence" which tells the reader about the topic of that paragraph. Then, the sentences that follow the topic sentence explain it, or give more information related to it.

In the example, the underlined topic sentence at the start of each paragraph helps the reader understand the content of the paragraph and its topic. When a new paragraph starts, the reader knows that there will be a new topic or different information in that paragraph.

## STE-Code Adaptation

In procedures, work steps usually have numbers and letters to show their sequence. In descriptive code documentation, paragraphs keep related information together and give a logical sequence to the text.

In STE-Code, a paragraph starts with a "topic sentence" which tells the developer about the topic of that paragraph. Then, the sentences that follow the topic sentence explain it, or give more information related to it.

The topic sentence at the start of each paragraph helps the developer understand the content of the paragraph and its topic. When a new paragraph starts, the developer knows that there will be a new topic or different information in that paragraph.

### Examples

> **Non-STE:** The data pipeline processes incoming events through a sequence of stages. Each stage transforms the event payload and passes it to the next stage. The first stage is validation, which checks the event schema and rejects malformed events. The second stage is enrichment, which adds metadata such as timestamps, source identifiers, and geolocation data from an external lookup service. The third stage is transformation, which converts the event into the target format required by downstream consumers such as the analytics warehouse and the real-time dashboard. The final stage is persistence, which writes the transformed event to the primary data store and to the event log for audit purposes. Error handling is implemented at each stage to catch exceptions without breaking the entire pipeline. If a stage fails, the pipeline logs the error and routes the event to the dead-letter queue for manual inspection.

> **STE:**
>
> **1. Data Pipeline Overview**
>
> The data pipeline processes incoming events through a sequence of stages. Each stage transforms the event payload and passes it to the next stage. Error handling is implemented at each stage to catch exceptions without breaking the pipeline. If a stage fails, the pipeline logs the error and routes the event to the dead-letter queue for manual inspection.
>
> **2. Validation Stage**
>
> The first stage is validation. This stage checks the event schema. It rejects events that are malformed.
>
> **3. Enrichment Stage**
>
> The second stage is enrichment. This stage adds metadata to the event:
> - Timestamps
> - Source identifiers
> - Geolocation data from an external lookup service.
>
> **4. Transformation Stage**
>
> The third stage is transformation. This stage converts the event into the target format. Downstream consumers use this format. These consumers include:
> - The analytics warehouse
> - The real-time dashboard.
>
> **5. Persistence Stage**
>
> The final stage is persistence. This stage writes the transformed event to two destinations. It writes the event to the primary data store. It also writes the event to the event log for audit purposes.
>
> *Code-domain example — each paragraph starts with a topic sentence and keeps related information together, giving the documentation a logical sequence.*

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure; Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic

## Code-Domain Explanation

Paragraph structure is the backbone of all descriptive code documentation. This rule applies differently across documentation types based on how developers read each type.

### README Files

A README file is the entry point for a repository. Each section of a README must start with a clear topic sentence. The topic sentence tells the developer what the section covers. The sentences that follow give more information about that topic.

A README paragraph that mixes installation steps with configuration options is not compliant. Move each topic to its own paragraph. Use section headings to separate major topics. Use paragraph breaks to separate sub-topics within a section.

> **Non-STE:** To install, run `pip install mylib` and then create a config file at `~/.mylib.toml` with your API key. The library supports Python 3.9 and above and requires a Redis instance for caching, which you can start with `redis-server`. You can also use SQLite for development without Redis.
>
> **STE:**
>
> **Installation**
>
> Install the library with pip:
> ```
> pip install mylib
> ```
>
> **Configuration**
>
> Create a configuration file at `~/.mylib.toml`. Add your API key to this file.
>
> **Dependencies**
>
> The library supports Python 3.9 and above. A Redis instance is necessary for caching. Start Redis with: `redis-server`.
>
> For development without Redis, use SQLite as the cache backend.
>
> *Principles applied: P1, P11 — uses approved vocabulary and one topic per paragraph. Each paragraph has a clear topic sentence (Install the library, Create a configuration file, The library supports, A Redis instance is necessary).*

### API Documentation

API reference pages document endpoints, parameters, return values, and error codes. Each endpoint description must start with a topic sentence that states what the endpoint does. Parameter tables, response schemas, and error descriptions must follow in separate paragraphs.

Do not embed the authentication requirements inside the endpoint description. Give authentication its own paragraph before the endpoint details. Do not mix the request schema with the response schema in one paragraph. Separate them with clear topic sentences.

> **Non-STE:** GET /api/users returns a paginated list of users with optional query parameters for filtering by role and status. You need a Bearer token in the Authorization header. The response includes a `users` array and a `pagination` object with `next` and `prev` cursors. Status 200 on success, 401 if the token is missing or expired, and 403 if the token lacks the `users:read` scope.
>
> **STE:**
>
> **GET /api/users**
>
> This endpoint returns a paginated list of users.
>
> **Authentication**
>
> Include a Bearer token in the `Authorization` header. The token must have the `users:read` scope.
>
> **Query Parameters**
>
> You can filter results with these optional parameters:
> - `role` — Filter by user role.
> - `status` — Filter by account status.
>
> **Response**
>
> A successful response includes:
> - A `users` array with the matching user objects.
> - A `pagination` object with `next` and `prev` cursors.
>
> **Status Codes**
>
> - `200` — The request succeeded.
> - `401` — The token is missing or has expired.
> - `403` — The token does not have the `users:read` scope.
>
> *Principles applied: P1, P6, P7 — uses approved words, allows technical nouns as API terms, and does not use technical nouns as verbs. Each paragraph has one topic (authentication, query parameters, response, status codes).*

### Docstrings and Inline Comments

Docstrings describe what a function, class, or module does. A docstring must start with a one-line topic sentence. Add a blank line. Then add more information in one or more paragraphs.

Each paragraph in a docstring must cover one sub-topic: parameters, return values, exceptions, side effects, or usage examples. Do not combine the description of a parameter with the description of a return value in the same paragraph.

Inline comments explain a single line or block of code. An inline comment is a one-sentence paragraph. It must state the topic of the code that follows. Do not chain multiple unrelated comments into one long comment block without paragraph breaks.

> **Non-STE:** `// Initialize the cache, then load the user profile from the database using the ORM, and if that fails fall back to the file cache, but first check the request signature using HMAC-SHA256 to make sure the request hasn't been tampered with.`
>
> **STE:**
>
> ```
> // Check the request signature.
> if (!verifySignature(req)) {
>   return error(401, "Invalid signature");
> }
>
> // Load the user profile from the cache.
> let profile = cache.get(userId);
>
> // The cache missed. Load from the database.
> if (!profile) {
>   profile = await db.users.findById(userId);
> }
> ```
>
> *Principles applied: P1, P3, P6 — uses approved words with approved meanings. Each comment is a topic sentence for the code that follows. Paragraph breaks between comments show topic changes.*

### Commit Messages

A commit message describes a change in a repository. The first line is the topic sentence. It tells what the commit does. The body of the commit message uses paragraphs to group related details.

Separate the motivation for the change from the implementation details. Use different paragraphs. Separate the list of files changed from the reasoning. Use different paragraphs. Each paragraph starts with a topic sentence.

> **Non-STE:** Fix race condition in connection pool that was causing deadlocks under high load, changed the mutex to a read-write lock, also updated the retry logic to use exponential backoff with jitter, and added a metrics counter for connection timeouts so we can monitor it in production, also cleaned up some old debug logging.
>
> **STE:**
>
> ```
> Fix race condition in connection pool under high load
>
> The connection pool had a race condition between the acquire()
> and release() methods. This caused deadlocks when more than
> 100 connections were active at the same time.
>
> Changes:
> - Replaced the mutex with a read-write lock in the pool struct.
> - Updated the retry logic to use exponential backoff with jitter.
> - Added a metrics counter for connection timeouts.
>
> Monitoring:
> The new `pool.timeouts` counter lets operators monitor timeout
> frequency in production dashboards.
> ```
>
> *Principles applied: P1, P11 — uses approved words and one term per concept. The first line is the topic sentence. Each paragraph after the blank line covers one sub-topic (the problem, the changes, the monitoring).*

### Error Messages

Error messages tell the user or developer what went wrong. An error message is a single sentence that states the topic: what failed and why. Multi-line error output must use paragraphs to separate the error description from the diagnostic information and the suggested fix.

Do not combine the error description, the stack trace, and the remediation advice into one paragraph. Use paragraph breaks to separate these topics.

> **Non-STE:** Connection refused to database at postgresql://db.internal:5432/app — make sure the database is running, check your network configuration, verify the hostname resolves, and ensure the TLS certificate is valid, stack trace: at ConnectionPool.connect (pool.js:42) at Database.init (db.js:15) at Server.start (server.js:88).
>
> **STE:**
>
> ```
> Error: Could not connect to the database.
>
> The database server at `postgresql://db.internal:5432/app`
> refused the connection.
>
> Check these items:
> - The database process is running.
> - The hostname `db.internal` resolves correctly.
> - The network allows traffic on port 5432.
> - The TLS certificate is valid.
>
> Stack trace:
>   at ConnectionPool.connect (pool.js:42)
>   at Database.init (db.js:15)
>   at Server.start (server.js:88)
> ```
>
> *Principles applied: P1, P3 — uses approved words with approved meanings. Each paragraph has a clear topic (the error, the cause, the checks, the stack trace). The developer can read each paragraph independently.*

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Class documentation must use paragraphs to separate the class purpose from the constructor details, the public API, and the internal design notes. Each method description is a paragraph group.

> **Non-STE:** The `AuthenticationService` handles user login, session management, and token refresh, it uses the `UserRepository` for database access and the `TokenProvider` for JWT generation, the `login` method takes a username and password, validates them against the database, and returns a signed JWT, while `refreshToken` accepts an expired token and returns a new one if the refresh window is still open.
>
> **STE:**
>
> **AuthenticationService**
>
> The `AuthenticationService` manages user authentication and sessions.
>
> **Dependencies**
>
> This service uses:
> - `UserRepository` — Database access for user records.
> - `TokenProvider` — JWT generation and validation.
>
> **Public Methods**
>
> `login(username, password)` validates credentials against the database. It returns a signed JWT on success.
>
> `refreshToken(token)` accepts an expired token. It returns a new token if the refresh window is still open.
>
> *Principles applied: P1, P7, P11 — uses approved words, does not use technical nouns as verbs, one term per concept. Each paragraph covers one aspect of the class (purpose, dependencies, methods).*

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional code emphasizes pure functions, immutability, and type signatures. Documentation must separate the type signature explanation from the behavior description and the algebraic properties. Use paragraphs to separate the pure from the effectful.

> **Non-STE:** `validateInput :: Input -> Either ValidationError ValidatedInput` parses and validates raw user input, returning a `ValidatedInput` on success or a `ValidationError` with a list of field-level problems, it's pure and doesn't perform any I/O, composed internally from `parseField` and `checkConstraints` which are also pure.
>
> **STE:**
>
> **validateInput**
>
> `validateInput :: Input -> Either ValidationError ValidatedInput`
>
> This function parses and validates raw user input.
>
> **Return Value**
>
> The function returns a `ValidatedInput` on success. It returns a `ValidationError` on failure. The error includes a list of field-level problems.
>
> **Purity**
>
> This function is pure. It does not do I/O.
>
> **Internal Composition**
>
> The function composes two pure sub-functions:
> - `parseField` — Parses each input field.
> - `checkConstraints` — Validates field constraints.
>
> *Principles applied: P1, P2, P3 — uses approved words as their specified part of speech with approved meanings. The type signature gets its own paragraph. Purity and composition are separate topics with separate paragraphs.*

### Procedural Documentation (C, Go, Bash)

Procedural code executes instructions in sequence. Documentation must separate the initialization from the main loop and the cleanup. Use paragraphs to show the phases of execution.

> **Non-STE:** The `processFiles` function scans a directory, opens each file, reads its contents line by line, applies a transformation, writes the output to a new file in the output directory, and then closes the file handle and logs the processing time for each file before moving to the next one, and finally prints a summary of how many files were processed and how long the whole operation took.
>
> **STE:**
>
> **processFiles**
>
> The `processFiles` function transforms every file in a directory.
>
> **Initialization**
>
> The function scans the input directory. It creates the output directory if it does not exist.
>
> **Processing Loop**
>
> For each file, the function:
> 1. Opens the file.
> 2. Reads the contents line by line.
> 3. Applies the transformation.
> 4. Writes the output to a new file in the output directory.
> 5. Closes the file handle.
> 6. Records the processing time.
>
> **Cleanup and Summary**
>
> The function closes all open handles. It prints a summary with the total number of files and the total processing time.
>
> *Principles applied: P1, P6, P7 — uses approved words, allows technical nouns (file, handle, directory), does not use technical nouns as verbs. The three phases (initialization, loop, cleanup) are separate paragraphs.*

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative code describes the desired state. Documentation must separate the resource identity from the resource specification and the dependencies. Each resource gets its own paragraph group.

> **Non-STE:** This Terraform module creates an auto-scaling group with a launch template that provisions EC2 instances running Amazon Linux 2, attaches them to an application load balancer with a target group that health-checks the `/health` endpoint every 30 seconds, and creates security group rules to allow inbound traffic on port 443 from the load balancer and on port 22 from the bastion host CIDR `10.0.1.0/24`.
>
> **STE:**
>
> **Auto-Scaling Group Module**
>
> This module creates an auto-scaling group for EC2 instances.
>
> **Launch Template**
>
> The launch template defines the instance configuration:
> - Amazon Linux 2 as the operating system.
> - The application AMI from the latest build pipeline.
>
> **Load Balancer**
>
> The module creates an application load balancer. A target group routes traffic to the instances. The health check monitors the `/health` endpoint every 30 seconds.
>
> **Security Groups**
>
> The security rules permit:
> - Inbound traffic on port 443 from the load balancer.
> - Inbound traffic on port 22 from the bastion host CIDR `10.0.1.0/24`.
>
> *Principles applied: P1, P3, P11 — uses approved words with approved meanings, one term per concept. Each AWS resource type gets its own paragraph with a clear topic sentence.*

### Systems Documentation (Rust Ownership, C Memory Management)

Systems documentation explains ownership, lifetimes, and memory safety. These are complex topics that need careful paragraph structure. Separate the ownership model explanation from the lifetime annotations and the unsafe code justifications.

> **Non-STE:** The `SharedBuffer` struct holds a reference-counted pointer to a heap-allocated byte buffer that can be shared across threads because it uses `Arc<Mutex<Vec<u8>>>` internally, the `read` method acquires the lock, copies the data out, and releases the lock; the `write` method acquires the lock, appends to the buffer, and releases the lock; and the `Drop` implementation decrements the reference count and frees the buffer when the last reference is dropped, but callers must ensure they don't hold the lock across await points because the `Mutex` is from `std` not `tokio`.
>
> **STE:**
>
> **SharedBuffer**
>
> `SharedBuffer` holds a reference-counted pointer to a heap-allocated byte buffer. It is safe to share across threads.
>
> **Internal Representation**
>
> The struct uses `Arc<Mutex<Vec<u8>>>`:
> - `Arc` provides shared ownership with atomic reference counting.
> - `Mutex` provides mutual exclusion for concurrent access.
> - `Vec<u8>` stores the raw bytes on the heap.
>
> **Methods**
>
> `read()` acquires the lock, copies the data out, and releases the lock.
>
> `write(data)` acquires the lock, appends `data` to the buffer, and releases the lock.
>
> **Drop Behavior**
>
> The `Drop` implementation decrements the reference count. It frees the buffer when the last reference is dropped.
>
> **Important Constraint**
>
> This struct uses `std::sync::Mutex`, not `tokio::sync::Mutex`. Do not hold the lock across `.await` points. Holding a `std` mutex across an await point causes a deadlock.
>
> *Principles applied: P1, P6, P7 — uses approved words, allows technical nouns (Arc, Mutex, Vec), does not use technical nouns as verbs. Ownership, methods, drop behavior, and constraints are separate paragraphs with clear topic sentences.*

## Edge Cases

### Framework Names That Conflict with Approved Words

Some framework names are the same as unapproved STE words. The word `make` is an approved STE verb. GNU Make is a build tool. When documenting a Makefile, you must distinguish between the verb "make" and the tool name "Make".

**Guidance:** Capitalize the framework name when it conflicts with an approved word. Write "Make" for the tool, "make" for the verb. Use the topic sentence to establish which meaning applies.

> **Non-STE:** Run `make` to make the build artifacts. Then make sure the output directory exists before you make the tarball with `make package`.
>
> **STE:**
>
> **Build with Make**
>
> Use the Make tool to build the project.
>
> **Step 1 — Compile**
>
> Run `make` to compile the source files. Make writes the build artifacts to the `build/` directory.
>
> **Step 2 — Package**
>
> Check that the `output/` directory exists. Run `make package` to create the tarball.
>
> *Principles applied: P1, P3, P6 — uses approved words, allows "Make" as a technical noun, distinguishes the tool name from the verb. The topic sentence clarifies that "Make" refers to the build tool.*

### Code Keywords That Conflict with Paragraph Structure

Code keywords like `break`, `continue`, `return`, and `yield` have specific meanings in control flow. When documenting control flow in a paragraph, the keyword names are technical nouns (Rule 1.5). They do not violate Rule 1.7 even though they look like verbs.

Use backticks to set code keywords apart from prose. Start a paragraph about control flow with a topic sentence that names the keyword being discussed.

> **Non-STE:** The loop breaks when the sentinel value is found, and then we return the accumulated result; if it continues past the maximum iterations we throw an error instead.
>
> **STE:**
>
> **Loop Termination**
>
> The loop uses the `break` keyword to exit early. It `break`s when it finds the sentinel value.
>
> **Return Value**
>
> The function uses the `return` keyword to send the accumulated result to the caller.
>
> **Error Condition**
>
> The loop uses the `continue` keyword to skip the current iteration. If the loop runs past the maximum iterations, the function throws an error.
>
> *Principles applied: P5, P6, P7 — code keywords are technical nouns. Backticks mark them as code. Each paragraph covers one control flow concept.*

### When a Code Example Breaks Paragraph Flow

Long code blocks that show a complete function or class must sit in their own paragraph. Do not embed a multi-line code block inside a prose paragraph. The code block itself becomes a visual paragraph.

Start the paragraph before the code block with a topic sentence that tells what the code does. End the paragraph. Then insert the code block. Start a new paragraph after the code block to explain the important parts.

> **Non-STE:** The handler validates the request by checking the content type is `application/json`, parsing the body, and then calling `processPayload` like this:
> ```typescript
> function handler(req: Request): Response {
>   if (req.headers['content-type'] !== 'application/json') {
>     return { status: 415 };
>   }
>   const body = JSON.parse(req.body);
>   return processPayload(body);
> }
> ```
> which returns a `Response` with the processed data or an error status.
>
> **STE:**
>
> **Request Handler**
>
> The handler validates the request and calls `processPayload`.
>
> The handler checks these conditions:
> - The `Content-Type` header is `application/json`.
> - The request body is valid JSON.
>
> The code for the handler is:
>
> ```typescript
> function handler(req: Request): Response {
>   if (req.headers['content-type'] !== 'application/json') {
>     return { status: 415 };
>   }
>   const body = JSON.parse(req.body);
>   return processPayload(body);
> }
> ```
>
> The handler returns a `Response` object. It includes the processed data on success. It includes an error status on failure.
>
> *Principles applied: P1, P3 — uses approved words. The code block is a separate visual paragraph. The paragraphs before and after have clear topic sentences.*

### Paragraphs in Auto-Generated Documentation

Auto-generated documentation from tools like JSDoc, Sphinx, or `go doc` extracts paragraphs from source comments. The tool uses blank comment lines as paragraph separators. A doc comment with no blank lines generates a single paragraph. This often breaks Rule 6.4.

Always insert a blank comment line between topics in a doc comment. Each topic becomes its own paragraph in the generated output.

> **Non-STE:**
> ````
> /**
>  * Creates a new connection pool with the given configuration.
>  * The pool maintains up to `maxConnections` open connections.
>  * Connections are lazily created on first use.
>  * Use `pool.acquire()` to get a connection and `pool.release()`
>  * to return it to the pool. Always release connections in a
>  * `finally` block to prevent pool exhaustion.
>  */
> ````
>
> **STE:**
> ````
> /**
>  * Creates a new connection pool.
>  *
>  * The pool uses the given configuration. It maintains up to
>  * `maxConnections` open connections. Connections are lazily
>  * created on first use.
>  *
>  * Use `pool.acquire()` to get a connection. Use
>  * `pool.release()` to return the connection to the pool.
>  *
>  * Always release connections in a `finally` block. This
>  * prevents pool exhaustion.
>  */
> ````
>
> *Principles applied: P1, P3 — uses approved words with approved meanings. The blank `*` lines between topics produce separate paragraphs in generated documentation. Each paragraph has one topic (purpose, pool behavior, acquire/release, safety rule).*

### Multi-Author Documents with Mixed Paragraph Styles

When many contributors write documentation, paragraph styles can become inconsistent. A README section written by one author may use long, dense paragraphs. Another section by a different author may use short, focused paragraphs.

**Guidance:** Apply structural linting to documentation. A documentation lint rule can flag paragraphs that exceed 5 sentences or that lack a clear topic sentence. Review mixed-author documents before publication. Break long paragraphs at topic boundaries. Add topic sentences where they are missing.

> **Non-STE:** The caching layer supports multiple backends including Redis, Memcached, and an in-memory store for development, each backend implements the `CacheBackend` interface which requires `get`, `set`, `delete`, and `clear` methods, the Redis backend is recommended for production because it supports persistence, replication, and clustering, the in-memory backend is acceptable for local development but it loses all data when the process restarts, Memcached is a good middle-ground for staging environments because it is simpler to operate than Redis while still providing network-accessible shared caching.
>
> **STE:**
>
> **Caching Layer**
>
> The caching layer supports multiple backends: Redis, Memcached, and an in-memory store.
>
> **Backend Interface**
>
> Each backend implements the `CacheBackend` interface. The interface requires these methods:
> - `get(key)` — Get a cached value.
> - `set(key, value)` — Set a cached value.
> - `delete(key)` — Remove a cached value.
> - `clear()` — Remove all cached values.
>
> **Redis Backend (Recommended for Production)**
>
> The Redis backend supports persistence, replication, and clustering. Use Redis for production environments.
>
> **Memcached Backend (Staging)**
>
> The Memcached backend is simpler than Redis. It provides network-accessible shared caching. Use Memcached for staging environments.
>
> **In-Memory Backend (Development)**
>
> The in-memory backend stores data in the process memory. It loses all data when the process restarts. Use it only for local development.
>
> *Principles applied: P1, P3, P11 — uses approved words with approved meanings, one term per concept. The long paragraph was split into five topic-focused paragraphs. Each backend gets its own paragraph. The recommendation (production, staging, development) is explicit in each topic sentence.*

## Grammar Notes

### Topic Sentences as Grammatical Anchors

In English grammar, the topic sentence of a paragraph carries the main clause. The sentences that follow carry subordinate information. This mirrors the structure of a complex sentence but at the paragraph level.

For code documentation, the topic sentence must be a declarative sentence in the simple present tense. It must name the topic (a class, function, module, or concept) in the subject position. The verb must be an approved STE verb that describes what the topic does or what the topic is.

Do not start a paragraph with a subordinate clause. Do not start with "Because...", "When...", "If...", or "Although...". Start with the subject. Attach the subordinate clause to a later sentence in the paragraph.

> **Non-STE:** Because the scheduler uses a work-stealing algorithm, tasks can migrate between threads, which improves load balancing but makes thread-local storage unreliable for task state.
>
> **STE:**
>
> The scheduler uses a work-stealing algorithm. Tasks can migrate between threads. This improves load balancing. However, thread-local storage is not reliable for task state.
>
> *Principles applied: P1, P3 — uses approved words. The topic sentence starts with the subject ("The scheduler"). The cause-and-effect relationship is shown through paragraph structure, not a subordinating conjunction at the start.*

### Paragraph Length and Information Density

The original ASD-STE100 does not set a maximum paragraph length. However, the 25-word sentence limit (Rule 6.3) naturally constrains paragraph length. A paragraph of five sentences cannot exceed 125 words. Most STE paragraphs have two to four sentences.

For code documentation, the ideal paragraph length depends on the documentation type:
- Docstrings: one to three sentences per parameter or return value paragraph.
- README sections: three to five sentences per topic.
- API endpoint descriptions: four to six sentences per endpoint.
- Error messages: one sentence for the primary message.

When a paragraph grows beyond five sentences, check if it covers more than one topic. If it does, split it at the topic boundary. If all sentences cover the same topic, check if some sentences repeat information. Remove the repetition.

### Paragraph Breaks as Reader Signals

A paragraph break is a signal to the reader. It says: "The topic changes here." In code documentation, developers scan for topic changes to find the information they need. Well-placed paragraph breaks make scanning faster.

Place a paragraph break before:
- A new concept or term.
- A code example.
- A warning, note, or constraint.
- A list of items.
- A change in abstraction level (from high-level overview to low-level detail).

Do not place a paragraph break:
- Between a topic sentence and its supporting sentences.
- In the middle of a definition.
- Between a function name and its description.

## Cross-References

This rule is part of Section 6 — Sentence and Paragraph Structure. The rules in this section build on each other:

- **Rule 6.1 — Give Information Gradually:** Present information in a sequence the reader can follow. Paragraph structure implements this sequence at the section level.
- **Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure:** Key words and phrases signal the reader about what is important. Topic sentences use key words to signal the paragraph topic.
- **Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence:** Short sentences make paragraphs easier to read. The 25-word limit constrains paragraph length.
- **Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic:** This rule reinforces Rule 6.4. One paragraph, one topic. When the topic changes, start a new paragraph.

Rules from other sections that interact with paragraph structure:

- **Rule 1.1 — Use Approved Words:** Topic sentences must use words from the STE-Code dictionary.
- **Rule 1.5 — Technical Code Nouns Are Allowed:** Technical nouns (class names, function names, framework names) can appear in topic sentences.
- **Rule 1.11 — One Term Per Concept:** Use the same term for the same concept across paragraphs. Do not switch between synonyms in different paragraphs.
- **Rule 7.1 — Use Lists for Three or More Items:** When a paragraph describes multiple items, check if a list would present the information more clearly. A list often replaces a dense paragraph.
