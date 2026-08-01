# Rule 3.6 — Use the Active Voice

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.6

> Source: master.md#sec3-rule3.6

## Original Rule

Use the active voice. In descriptive writing, you can use the passive voice only if the agent is unknown.

Technical texts consist of procedural writing and descriptive writing. When you write in STE, always use the active voice. In descriptive writing, the passive voice is permitted only when the agent (the person or thing that does the action) is unknown.

What is active voice?

In the active voice, the subject of the sentence does the action of the sentence ("A" does "B"). Thus, the grammatical subject (A) is also the logical subject (agent).

What is passive voice?

In the passive voice, the subject of the sentence receives the action ("B" is done by "A"). Here, the grammatical subject is B, and the logical subject, or agent, is A.

General examples:

> **Active:** The manufacturer gives the safety procedures.
> **Passive:** The safety procedures are given by the manufacturer.

How do you know if a sentence is in the passive voice?

The best test for the passive voice is to think of the question "by whom or by what?" (the agent). If your text gives you an answer to this question, then the text is in the passive voice. When a sentence contains the preposition "by," it is a good indication that the sentence is in the passive voice. The object of the preposition "by" is then the agent and you can use the agent as the subject of a sentence in the active voice.

But a passive construction does not always contain an agent.

The dimensions are given in the table.

The main gear leg is held in its position.

A sentence in the active voice always has a grammatical subject (the agent), but in the passive sentence in the example below, the agent is unknown (and we do not know the cause of data corruption). In the active sentence, the agent ("transmission") is incorrect ("transmission" is not the cause of data corruption), and the meaning of the sentence is different. Thus, the active sentence becomes technically incorrect.

Example:

> **Passive:** During transmission, the data was corrupted. (Correct, the agent is unknown.)
> **Active:** During transmission, something corrupted the data. (Correct, you do not know the identity of "something," but you can use it as the agent.)
> **Active:** Transmission corrupted the data. (Incorrect, "transmission" is not the correct agent.)

In the example, if you use the word "something" ("a thing that is not determined or specified") as the agent, the active voice will be technically correct.

How do you change a sentence that is in the passive voice to the active voice?

To change a sentence from the passive voice to the active voice, you can use one of these four methods:

Method 1

When the sentence gives the agent (usually the object of the preposition "by"), put the agent at the start of the sentence. Then, use the agent as the subject. The subject must always be the noun that does the action in the sentence.

> **Non-STE:** The circuits are connected by a switching relay. (Passive)
>
> **STE:** A switching relay connects the circuits. (Active)

Method 2

Change an infinitive verb to an active verb.

> **STE:** The computer calculates the energy consumption from these values. (Active)

Method 3

In procedural writing, change the verb to the imperative ("command") form.

Method 4

When the agent (the person or thing that does the action) is not given in the sentence, you can use the pronouns "you" or "we" as subjects in the active form. If the agent is the reader, use "you." If the agent is your company, or organization, use "we."

Examples:

> **Non-STE:** On the ground, the valve can be opened with the override handle. (Passive)
>
> **STE:** On the ground, you can open the valve with the override handle. (Active)

When you find complex sentences in the passive voice that include auxiliary verbs, decide if you want to write a procedural sentence or a descriptive sentence.

> **STE:** This type of fuel does not contain additives. (Descriptive sentence)

## STE-Code Adaptation

Use the active voice in all code documentation. In descriptive writing, the passive voice is permitted only when the agent (the person, service, or component that does the action) is unknown.

In the active voice, the subject of the sentence does the action. This makes code documentation clearer because the reader immediately knows who or what performs the operation.

To test if a sentence is in the passive voice, ask "by whom or by what?" (the agent). If the sentence answers this question, it is passive. Convert it to active by using the agent as the subject.

To change a sentence from the passive voice to the active voice, use one of these four methods:

**Method 1:** When the preposition "by" identifies the agent, move the agent to the subject position:

> **Non-STE:** The API response is parsed by the middleware. (Passive)
>
> **STE:** The middleware parses the API response. (Active)
>
> *Adapted from spec pair: "The circuits are connected by a switching relay." / "A switching relay connects the circuits."*

Realistic context — a README section that documents an HTTP request pipeline:

> **Non-STE:**
> ```markdown
> ## How the request pipeline works
>
> After the client sends a request, the raw HTTP body is read by the server.
> The API response is parsed by the middleware. The parsed data is then
> validated by the schema checker before the controller receives it.
> ```
>
> **STE:**
> ```markdown
> ## How the request pipeline works
>
> After the client sends a request, the server reads the raw HTTP body.
> The middleware parses the API response. The schema checker then validates
> the parsed data before the controller receives it.
> ```

**Method 2:** Change an infinitive verb to an active verb:

> **STE:** The profiler calculates the memory usage from these values. (Active)
>
> *Adapted from spec pair: "The computer calculates the energy consumption from these values."*

Realistic context — a docstring for a profiling helper:

> **Non-STE:**
> ```python
> def report_memory(samples):
>     """To calculate the memory usage from these values. The peak is
>     returned as a percentage of the allocated heap."""
> ```
>
> **STE:**
> ```python
> def report_memory(samples):
>     """Calculate the memory usage from these values. Return the peak
>     as a percentage of the allocated heap."""
> ```

**Method 3:** In procedural writing, change the verb to the imperative ("command") form:

> **Non-STE:** The dependencies can be installed with the following command. (Passive)
>
> **STE:** Install the dependencies with this command: npm install (Active, imperative)
>
> *Adapted from original Method 3 principle — imperative ("command") form*

Realistic context — a contributing guide:

> **Non-STE:**
> ```markdown
> ## Setup
>
> The dependencies can be installed with the following command. The test
> suite can then be run from the same directory.
> ```
>
> **STE:**
> ```markdown
> ## Setup
>
> Install the dependencies with this command:
>
>     npm install
>
> Then run the test suite from the same directory:
>
>     npm test
> ```

**Method 4:** When the agent is not given in the sentence, use the pronouns "you" or "we" as subjects in the active form. If the agent is the reader, use "you." If the agent is your organization, use "we."

> **Non-STE:** The configuration file can be edited with a text editor. (Passive)
>
> **STE:** You can edit the configuration file with a text editor. (Active)
>
> *Adapted from spec pair: "On the ground, the valve can be opened with the override handle." / "On the ground, you can open the valve with the override handle."*

Realistic context — a getting-started page:

> **Non-STE:**
> ```markdown
> ## First run
>
> The configuration file can be edited with a text editor. The server
> can be started after you save your changes.
> ```
>
> **STE:**
> ```markdown
> ## First run
>
> You can edit the configuration file with a text editor. After you save
> your changes, you can start the server.
> ```

When the agent is unknown and you cannot identify it:

> **Passive:** During the network request, the data was corrupted. (Correct, the agent is unknown.)
> **Active:** During the network request, something corrupted the data. (Correct, you do not know the identity of "something.")
> **Active:** The network request corrupted the data. (Incorrect, "network request" is not the correct agent.)
>
> *Adapted from spec pair: "During transmission, the data was corrupted." / "During transmission, something corrupted the data." / "Transmission corrupted the data."*

Realistic context — an error report from a flaky integration test:

> **Passive (correct):**
> ```text
> During the network request, the payload was corrupted before the checksum
> was computed. The agent is unknown because the failure occurs only under
> heavy load and leaves no stack trace.
> ```
>
> **Active (incorrect):**
> ```text
> During the network request, the socket corrupted the payload.
> ```
> "socket" is not the true cause — the active sentence becomes technically
> wrong and misleads the reader about where to fix the bug.

### Examples

> *Adapted from spec pair: Non-STE: "The circuits are connected by a switching relay."  |  STE: "A switching relay connects the circuits." (Method 1) — and Non-STE: "On the ground, the valve can be opened with the override handle."  |  STE: "On the ground, you can open the valve with the override handle." (Method 4)*

> **Non-STE:** The database connection is established by the connection pool at startup.
>
> **STE:** The connection pool establishes the database connection at startup.
>
> *Adapted from spec pair: "The circuits are connected by a switching relay." / "A switching relay connects the circuits." (Method 1)*

Realistic context — an architecture overview for a backend service:

> **Non-STE:**
> ```markdown
> ## Startup sequence
>
> The configuration is loaded by the bootstrap routine. The database
> connection is established by the connection pool at startup. The cache
> is warmed by a background worker before the first request is served.
> ```
>
> **STE:**
> ```markdown
> ## Startup sequence
>
> The bootstrap routine loads the configuration. The connection pool
> establishes the database connection at startup. A background worker
> warms the cache before it serves the first request.
> ```

> **Non-STE:** The test results can be viewed in the terminal output.
>
> **STE:** You can see the test results in the terminal output.
>
> *Adapted from spec pair: "On the ground, the valve can be opened with the override handle." / "On the ground, you can open the valve with the override handle." (Method 4)*

Realistic context — a CI job summary in a pull-request template:

> **Non-STE:**
> ```markdown
> ## Checks
>
> The linting errors are reported by the linter. The test results can be
> viewed in the terminal output. The coverage report is generated by the
> coverage tool.
> ```
>
> **STE:**
> ```markdown
> ## Checks
>
> The linter reports the linting errors. You can see the test results in
> the terminal output. The coverage tool generates the coverage report.
> ```

## Code-Domain Explanation

This rule has different effects on each type of code documentation. The following sections explain the effects in detail.

### README Files

README files contain a mix of procedural instructions (installation, build, usage) and descriptive text (project overview, feature list, architecture summary). Both sections benefit from the active voice.

In procedural sections, use the imperative mood with "you" as the implied subject. The reader is the agent who performs the action. Passive voice in a procedural section hides the agent and makes the instruction less clear.

> **Non-STE:** The package can be installed with pip install. (Passive — who does the installation?)
>
> **STE:** Install the package with this command: pip install . (Active imperative — the reader is the agent.)

Realistic context — the install section of a Python library README:

> **Non-STE:**
> ```markdown
> ## Installation
>
> The package can be installed with `pip install`. A virtual environment
> should be created before the install is done.
> ```
>
> **STE:**
> ```markdown
> ## Installation
>
> Install the package with this command:
>
>     pip install .
>
> Create a virtual environment before you install the package.
> ```

In descriptive sections, use the active voice with the project, library, or tool as the subject. The passive voice in a descriptive section makes the project seem like a passive object instead of an active system.

> **Non-STE:** Support for WebSocket connections is provided by this library. (Passive)
>
> **STE:** This library supports WebSocket connections. (Active — the library is the agent.)

Realistic context — the feature list of a networking library README:

> **Non-STE:**
> ```markdown
> ## Features
>
> Support for WebSocket connections is provided by this library. Automatic
> reconnection is handled by the transport layer. Message compression is
> applied by the codec before each frame is sent.
> ```
>
> **STE:**
> ```markdown
> ## Features
>
> This library supports WebSocket connections. The transport layer handles
> automatic reconnection. The codec compresses each message before it sends
> the frame.
> ```

### API Documentation

API reference documentation describes what each method, function, or endpoint does. The active voice convention is well-established in API documentation. Use the method or function as the grammatical subject.

> **Non-STE:** The input string is validated and a boolean is returned by this method. (Passive)
>
> **STE:** This method validates the input string and returns a boolean. (Active)

Realistic context — a JSDoc block for an email validator:

> **Non-STE:**
> ```javascript
> /**
>  * Checks a user-supplied address.
>  * The input string is validated and a boolean is returned by this method.
>  * @param {string} address - the address to check
>  * @returns {boolean} true when the address is well formed
>  */
> ```
>
> **STE:**
> ```javascript
> /**
>  * Check a user-supplied address.
>  * This method validates the input string and returns a boolean.
>  * @param {string} address - the address to check
>  * @returns {boolean} true when the address is well formed
>  */
> ```

When you document a callback parameter, the callback is the agent that performs the action. Use the callback as the subject.

> **Non-STE:** The URL is transformed by the callback before the request is sent. (Passive)
>
> **STE:** The callback transforms the URL. Then the client sends the request. (Active)

Realistic context — an OpenAPI parameter description:

> **Non-STE:**
> ```yaml
> parameters:
>   - name: onRequest
>     description: >
>       A function that runs before the call. The URL is transformed by the
>       callback before the request is sent to the upstream service.
> ```
>
> **STE:**
> ```yaml
> parameters:
>   - name: onRequest
>     description: >
>       A function that runs before the call. The callback transforms the
>       URL. Then the client sends the request to the upstream service.
> ```

When you document a return value, use the method as the subject in the active voice. Do not use a passive construction that makes the return value the subject.

> **Non-STE:** A `Promise<User>` is returned by this function. (Passive)
>
> **STE:** This function returns a `Promise<User>`. (Active)

Realistic context — a TypeScript function signature comment:

> **Non-STE:**
> ```typescript
> /**
>  * Fetches the current user. A `Promise<User>` is returned by this function.
>  * The user record is read from the session store while the promise is pending.
>  */
> function getCurrentUser(): Promise<User>
> ```
>
> **STE:**
> ```typescript
> /**
>  * Fetch the current user. This function returns a `Promise<User>`.
>  * While the promise is pending, the function reads the user record from
>  * the session store.
>  */
> function getCurrentUser(): Promise<User>
> ```

### Docstrings and Inline Comments

Docstrings describe the purpose, parameters, return value, and behavior of a function or class. The summary line (first line) follows the imperative convention. The body uses the active voice with the function as the subject.

> **Non-STE:** """A hash of the input data is computed and then it is returned as a hex string."""
>
> **STE:** """Compute the hash of the input data. Return the result as a hex string."""

Realistic context — a Python hashing utility:

> **Non-STE:**
> ```python
> def sha256_hex(data: bytes) -> str:
>     """A hash of the input data is computed and then it is returned as a
>     hex string. The digest is calculated by the hashlib module."""
> ```
>
> **STE:**
> ```python
> def sha256_hex(data: bytes) -> str:
>     """Compute the hash of the input data. Return the result as a hex
>     string. The hashlib module calculates the digest."""
> ```

Inline comments explain a specific line or block of code. Use the active voice with the code entity or the developer as the subject. Passive voice in an inline comment can make the responsibility for an action unclear.

> **Non-STE:** // The buffer is flushed before new data is written.
>
> **STE:** // Flush the buffer before you write new data.

> **Non-STE:** // The connection is closed by the finally block.
>
> **STE:** // The finally block closes the connection.

Realistic context — a Go function that writes a record:

> **Non-STE:**
> ```go
> func (w *Writer) Write(rec Record) error {
>     // The buffer is flushed before new data is written.
>     if err := w.buf.Flush(); err != nil {
>         return err
>     }
>     // The connection is closed by the finally block.
>     defer w.conn.Close()
>     return w.conn.Send(rec)
> }
> ```
>
> **STE:**
> ```go
> func (w *Writer) Write(rec Record) error {
>     // Flush the buffer before you write new data.
>     if err := w.buf.Flush(); err != nil {
>         return err
>     }
>     // The finally block closes the connection.
>     defer w.conn.Close()
>     return w.conn.Send(rec)
> }
> ```

### Commit Messages

Commit messages follow the imperative mood convention, which is inherently active voice. The commit message describes what the commit does when applied to the codebase. Passive voice in a commit message breaks this convention and makes the message less direct.

> **Non-STE:** The authentication bug was fixed. (Passive — who fixed it? what did the commit do?)
>
> **STE:** Fix the authentication bug. (Active imperative — the commit is the agent.)

> **Non-STE:** Rate limiting was added to the API endpoints. (Passive)
>
> **STE:** Add rate limiting to the API endpoints. (Active imperative)

Realistic context — two commits in a feature branch:

> **Non-STE:**
> ```text
> git log --oneline
> a1b2c3d The authentication bug was fixed.
> e4f5g6h Rate limiting was added to the API endpoints.
> ```
>
> **STE:**
> ```text
> git log --oneline
> a1b2c3d Fix the authentication bug.
> e4f5g6h Add rate limiting to the API endpoints.
> ```

NOTE: Some projects use changelog auto-generation tools that extract commit messages. If the tool wraps commit messages in passive sentences (for example, "A fix was made for the authentication bug"), the generated changelog is not subject to this rule. The rule applies to the commit messages you write, not to the changelog the tool generates.

### Error Messages and Log Output

Error messages describe what went wrong and, when possible, what action to take. Active voice in an error message helps the user identify the component that detected the error.

> **Non-STE:** An invalid configuration value was encountered while the file was being parsed. (Passive — what encountered it? what was parsing?)
>
> **STE:** The parser found an invalid configuration value in the file. (Active — the parser is the agent.)

> **Non-STE:** The request was rejected by the rate limiter. (Passive)
>
> **STE:** The rate limiter rejected the request. (Active)

Realistic context — log lines from a config loader and an API gateway:

> **Non-STE:**
> ```text
> [warn]  An invalid configuration value was encountered while the file was
>         being parsed.
> [error] The request was rejected by the rate limiter.
> ```
>
> **STE:**
> ```text
> [warn]  The parser found an invalid configuration value in the file.
> [error] The rate limiter rejected the request.
> ```

When the agent is truly unknown (for example, a network timeout with no identifiable cause), the passive voice is correct. This is the exception defined in the original rule.

> **Correct:** The connection was reset. (The agent is unknown — no process or component can be identified as the cause.)

Realistic context — a raw socket error with no local cause:

> **Correct (passive):**
> ```text
> [error] The connection was reset. The peer closed the TCP session without
>         sending a FIN or RST that our client could observe.
> ```

## Paradigm-Specific Guidance

### Object-Oriented Paradigm (Java, C++, C#, Python Classes)

In object-oriented documentation, classes, methods, and design patterns are the agents of their documented behavior. Use the class or method as the grammatical subject in the active voice.

> **Non-STE:** The dependency is resolved by the container at runtime. (Passive)
>
> **STE:** The container resolves the dependency at runtime. (Active)

Realistic context — a Spring-style DI container description:

> **Non-STE:**
> ```markdown
> ## Dependency resolution
>
> The dependency is resolved by the container at runtime. The bean is
> created after all its prerequisites are satisfied by the registrar.
> ```
>
> **STE:**
> ```markdown
> ## Dependency resolution
>
> The container resolves the dependency at runtime. After the registrar
> satisfies all prerequisites, the container creates the bean.
> ```

When you document a design pattern, the pattern's components have clear agency. The factory creates objects. The observer receives notifications. The decorator wraps behavior. Use these components as subjects.

> **Non-STE:** New instances are created by the factory method when they are requested by the client. (Passive)
>
> **STE:** The factory method creates a new instance when the client requests one. (Active)

Realistic context — a factory pattern docstring:

> **Non-STE:**
> ```python
> class ConnectionFactory:
>     """New instances are created by the factory method when they are
>     requested by the client. The pool is checked before a connection
>     is made."""
> ```
>
> **STE:**
> ```python
> class ConnectionFactory:
>     """Create a new instance with the factory method when the client
>     requests one. The factory method checks the pool before it makes a
>     connection."""
> ```

When you document an abstract class or interface contract, use the implementing class as the grammatical subject. Passive voice in a contract description makes the obligation unclear.

> **Non-STE:** The `validate()` method is called before the data is processed by the handler. (Passive)
>
> **STE:** The handler calls the `validate()` method before it processes the data. (Active)

Realistic context — an interface contract in a Java service:

> **Non-STE:**
> ```java
> /**
>  * The validate() method is called before the data is processed by the
>  * handler. A ValidationException is thrown when the record is rejected.
>  */
> interface RequestHandler { void handle(Request req); }
> ```
>
> **STE:**
> ```java
> /**
>  * The handler calls the validate() method before it processes the data.
>  * The handler throws a ValidationException when it rejects the record.
>  */
> interface RequestHandler { void handle(Request req); }
> ```

### Functional Paradigm (Haskell, Elixir, Clojure, Rust)

Functional code documentation describes pure functions, data transformations, and pipelines. Functions are the agents in functional documentation. Use the function name as the grammatical subject.

> **Non-STE:** Each element in the list is transformed by the `map` function. (Passive)
>
> **STE:** The `map` function transforms each element in the list. (Active)

Realistic context — a Haskell list pipeline comment:

> **Non-STE:**
> ```haskell
> -- Each element in the list is transformed by the map function. The result
> -- is then filtered and the sum is computed by foldl.
> total = foldl (+) 0 . filter (>0) . map (*2) $ xs
> ```
>
> **STE:**
> ```haskell
> -- The map function transforms each element in the list. The filter function
> -- keeps the positive values. Then foldl computes the sum.
> total = foldl (+) 0 . filter (>0) . map (*2) $ xs
> ```

When you document a pipeline of composed functions, break the pipeline into active sentences. Each sentence names the function that performs an action.

> **Non-STE:** The input is filtered, then mapped, and finally the result is reduced to a single value. (Passive)
>
> **STE:** The `filter` function removes invalid items. The `map` function transforms each item. The `reduce` function combines the results into a single value. (Active)

Realistic context — a Clojure threading macro doc:

> **Non-STE:**
> ```clojure
> ;; The input is filtered, then mapped, and finally the result is reduced to
> ;; a single value by the reduce step.
> (->> items (filter valid?) (map enrich) (reduce merge {}))
> ```
>
> **STE:**
> ```clojure
> ;; The filter function removes invalid items. The map function transforms
> ;; each item. The reduce function combines the results into a single map.
> (->> items (filter valid?) (map enrich) (reduce merge {}))
> ```

When you document higher-order functions or combinators, use the combinator as the grammatical subject.

> **Non-STE:** Two functions are composed into a new function by the `compose` combinator. (Passive)
>
> **STE:** The `compose` combinator combines two functions into a new function. (Active)

Realistic context — a Rust combinator doc:

> **Non-STE:**
> ```rust
> /// Two functions are composed into a new function by the compose
> /// combinator. The result is cached by the memoize wrapper.
> fn compose<A, B, C>(f: fn(B) -> C, g: fn(A) -> B) -> impl Fn(A) -> C
> ```
>
> **STE:**
> ```rust
> /// The compose combinator combines two functions into a new function.
> /// The memoize wrapper caches the result.
> fn compose<A, B, C>(f: fn(B) -> C, g: fn(A) -> B) -> impl Fn(A) -> C
> ```

### Procedural Paradigm (C, Go, Bash)

Procedural documentation contains step-by-step instructions and descriptions of sequential execution. Each step has a clear agent: the program, the function, or the developer. Use the agent as the subject.

> **Non-STE:** The file is opened, the contents are read, and the connection is closed. (Passive — who does each step?)
>
> **STE:** The script opens the file. It reads the contents. Then it closes the connection. (Active)

Realistic context — a backup shell script header:

> **Non-STE:**
> ```bash
> # The file is opened, the contents are read, and the connection is closed
> # by the dump routine. The archive is written to /var/backups.
> pg_dump app > /var/backups/app.sql
> ```
>
> **STE:**
> ```bash
> # The script opens the file, reads the contents, and closes the connection.
> # Then it writes the archive to /var/backups.
> pg_dump app > /var/backups/app.sql
> ```

When you document a shell script or command-line tool, use the script or tool as the subject in descriptive text and the imperative mood in procedural text.

> **Non-STE:** Environment variables are checked before the build process is started. (Passive)
>
> **STE:** The script checks the environment variables. Then it starts the build process. (Active)

> **Non-STE:** The log file can be rotated with the --rotate flag. (Passive)
>
> **STE:** Use the --rotate flag to rotate the log file. (Active imperative)

Realistic context — a Makefile help target:

> **Non-STE:**
> ```makefile
> # Environment variables are checked before the build process is started.
> # The log file can be rotated with the --rotate flag.
> build:
> 	./configure && $(MAKE)
> ```
>
> **STE:**
> ```makefile
> # The script checks the environment variables. Then it starts the build.
> # Use the --rotate flag to rotate the log file.
> build:
> 	./configure && $(MAKE)
> ```

### Declarative Paradigm (SQL, Terraform, Kubernetes YAML, Dockerfile)

Declarative documentation describes the desired state that a system moves toward. The active voice names the tool or engine that applies the declaration. The declaration itself does not act — the tool that reads the declaration acts.

> **Non-STE:** An AWS VPC with three subnets is provisioned by this Terraform module. (Passive)
>
> **STE:** This Terraform module provisions an AWS VPC with three subnets. (Active)

Realistic context — a Terraform module README:

> **Non-STE:**
> ```markdown
> ## What this module builds
>
> An AWS VPC with three subnets is provisioned by this Terraform module.
> A NAT gateway is attached to the private subnet by the same module.
> ```
>
> **STE:**
> ```markdown
> ## What this module builds
>
> This Terraform module provisions an AWS VPC with three subnets. The same
> module attaches a NAT gateway to the private subnet.
> ```

When you document a SQL query, the database engine is the agent. Use the query or the engine as the subject.

> **Non-STE:** All rows with a status of 'active' are selected by this query. (Passive)
>
> **STE:** This query selects all rows with a status of 'active'. (Active)

Realistic context — a query comment in a migration file:

> **Non-STE:**
> ```sql
> -- All rows with a status of 'active' are selected by this query. The
> -- matching accounts are then counted by the aggregate.
> SELECT count(*) FROM accounts WHERE status = 'active';
> ```
>
> **STE:**
> ```sql
> -- This query selects all rows with a status of 'active'. The aggregate
> -- then counts the matching accounts.
> SELECT count(*) FROM accounts WHERE status = 'active';
> ```

When you document a Kubernetes manifest, the Kubernetes controller is the agent. Use the controller or the resource as the subject.

> **Non-STE:** Three replicas of the pod are maintained by the deployment controller. (Passive)
>
> **STE:** The deployment controller maintains three replicas of the pod. (Active)

Realistic context — a Deployment manifest description:

> **Non-STE:**
> ```markdown
> ## Scaling
>
> Three replicas of the pod are maintained by the deployment controller. The
> rollout is paused by the operator during a canary release.
> ```
>
> **STE:**
> ```markdown
> ## Scaling
>
> The deployment controller maintains three replicas of the pod. During a
> canary release, the operator pauses the rollout.
> ```

NOTE: YAML comments and Dockerfile comments are procedural by nature. Use the imperative mood and active voice in these comments because they instruct the reader or the build engine.

> **Non-STE:** # The base image is set to Ubuntu 22.04. (Passive)
>
> **STE:** # Use Ubuntu 22.04 as the base image. (Active imperative)

Realistic context — a Dockerfile preamble:

> **Non-STE:**
> ```dockerfile
> # The base image is set to Ubuntu 22.04. The working directory is created
> # at /app by the build stage.
> FROM ubuntu:22.04
> ```
>
> **STE:**
> ```dockerfile
> # Use Ubuntu 22.04 as the base image. The build stage creates the working
> # directory at /app.
> FROM ubuntu:22.04
> ```

### Systems Programming (Rust Ownership Docs, C Memory Docs)

Systems documentation describes ownership, lifetimes, memory allocation, and concurrency. These topics involve precise relationships between components. Active voice makes the relationship between the agent and the action explicit.

> **Non-STE:** The memory block is allocated by the allocator and a pointer is returned. (Passive)
>
> **STE:** The allocator allocates the memory block. It returns a pointer. (Active)

Realistic context — a C allocator doc:

> **Non-STE:**
> ```c
> /* The memory block is allocated by the allocator and a pointer is returned.
>    The block is zeroed before it is handed to the caller. */
> void *alloc_block(size_t bytes);
> ```
>
> **STE:**
> ```c
> /* The allocator allocates the memory block. It returns a pointer. The
>    allocator zeroes the block before it hands the block to the caller. */
> void *alloc_block(size_t bytes);
> ```

When you document ownership transfer in Rust, the function or scope that takes ownership is the agent. Use it as the subject.

> **Non-STE:** Ownership of the string is taken by the `process` function. (Passive)
>
> **STE:** The `process` function takes ownership of the string. (Active)

Realistic context — a Rust function that consumes a value:

> **Non-STE:**
> ```rust
> /// Ownership of the string is taken by the process function. The buffer
> /// is freed when the function returns.
> fn process(input: String) { /* ... */ }
> ```
>
> **STE:**
> ```rust
> /// The process function takes ownership of the string. The function frees
> /// the buffer when it returns.
> fn process(input: String) { /* ... */ }
> ```

When you document a concurrency primitive, the primitive is the agent. Mutexes lock. Channels send. Atomics store.

> **Non-STE:** Access to the shared state is controlled by the mutex. (Passive)
>
> **STE:** The mutex controls access to the shared state. (Active)

Realistic context — a Rust concurrency comment:

> **Non-STE:**
> ```rust
> // Access to the shared state is controlled by the mutex. The value is sent
> // to the worker by the channel.
> let guard = state.lock().unwrap();
> tx.send(guard.clone());
> ```
>
> **STE:**
> ```rust
> // The mutex controls access to the shared state. The channel sends the
> // value to the worker.
> let guard = state.lock().unwrap();
> tx.send(guard.clone());
> ```

## Extended Examples

### Example 1 — README Feature Description

> **Non-STE:** Authentication via OAuth2 and JWT tokens is supported by this service. Rate limiting is applied to all endpoints. Requests are logged to a centralized logging system.
>
> **STE:** This service supports authentication with OAuth2 and JWT tokens. It applies rate limiting to all endpoints. It sends request logs to a centralized logging system.
>
> **Principle applied:** P14 — Use American English spelling. P8 — Use standard, well-known technical nouns. Method 1 applied: the agent ("this service") moves to the subject position.
>
> **Explanation:** The original text has three consecutive passive constructions. The reader must work backward to find the agent. The STE version establishes "this service" as the agent once, then uses active verbs for each feature.

Realistic context — the full feature section of a gateway service README:

> **Non-STE:**
> ```markdown
> ## What this service does
>
> Authentication via OAuth2 and JWT tokens is supported by this service.
> Rate limiting is applied to all endpoints. Requests are logged to a
> centralized logging system. Health checks are exposed on port 8080.
> ```
>
> **STE:**
> ```markdown
> ## What this service does
>
> This service supports authentication with OAuth2 and JWT tokens. It applies
> rate limiting to all endpoints. It sends request logs to a centralized
> logging system. It exposes health checks on port 8080.
> ```

### Example 2 — API Method Documentation

> **Non-STE:** `createUser(payload)` — A new user is created with the provided payload. The payload is validated before the user record is inserted into the database. A `User` object is returned upon success.
>
> **STE:** `createUser(payload)` — Create a new user with the provided payload. The method validates the payload. Then it inserts the user record into the database. It returns a `User` object on success.
>
> **Principle applied:** P2 — Use words only as their specified part of speech. P4 — Use only approved verb forms. The passive constructions are replaced with active imperatives and indicative verbs.
>
> **Explanation:** The original text uses three passive constructions in a row. The reader does not know if "is validated" means the method does it, the database does it, or the caller must do it. The STE version names the method as the agent and uses active verbs.

Realistic context — the full JSDoc for the endpoint handler:

> **Non-STE:**
> ```javascript
> /**
>  * POST /users
>  * createUser(payload) — A new user is created with the provided payload.
>  * The payload is validated before the user record is inserted into the
>  * database. A User object is returned upon success.
>  */
> ```
>
> **STE:**
> ```javascript
> /**
>  * POST /users
>  * createUser(payload) — Create a new user with the provided payload. The
>  * method validates the payload. Then it inserts the user record into the
>  * database. It returns a User object on success.
>  */
> ```

### Example 3 — Docstring for a Class

> **Non-STE:** """A pool of database connections is managed by this class. Connections are borrowed when a request is received and they are returned when the request is complete."""
>
> **STE:** """Manage a pool of database connections. The class lends a connection when a request arrives. It returns the connection when the request is complete."""
>
> **Principle applied:** P1 — Use approved words. "Borrowed" and "received" are replaced with approved alternatives ("lends," "arrives"). Method 3 and Method 4 are applied.
>
> **Explanation:** The original docstring uses passive voice throughout. The reader cannot tell if the class manages the pool automatically or if the caller must manage it. The STE version uses imperatives and active voice to clarify the class's responsibility.

Realistic context — the full Python class docstring and a usage note:

> **Non-STE:**
> ```python
> class ConnectionPool:
>     """A pool of database connections is managed by this class. Connections
>     are borrowed when a request is received and they are returned when the
>     request is complete. Idle connections are closed by the reaper thread."""
> ```
>
> **STE:**
> ```python
> class ConnectionPool:
>     """Manage a pool of database connections. The class lends a connection
>     when a request arrives. It returns the connection when the request is
>     complete. The reaper thread closes idle connections."""
> ```

### Example 4 — Commit Message

> **Non-STE:** The memory leak in the image processing pipeline was fixed. Redundant allocations were removed and the buffer pool was refactored.
>
> **STE:** Fix the memory leak in the image processing pipeline. Remove redundant allocations. Refactor the buffer pool.
>
> **Principle applied:** P4 — Use only approved verb forms. P9 — Prefer short, clear technical nouns. Method 3 (imperative) applied throughout.
>
> **Explanation:** The original commit message uses three passive constructions. The STE version uses three imperative verbs. Each verb describes one change. The reader immediately knows what the commit does.

Realistic context — the commit shown in `git show`:

> **Non-STE:**
> ```text
> commit 9f2c1ab
> Author:Dev <dev@example.com>
>
>     The memory leak in the image processing pipeline was fixed. Redundant
>     allocations were removed and the buffer pool was refactored.
> ```
>
> **STE:**
> ```text
> commit 9f2c1ab
> Author:Dev <dev@example.com>
>
>     Fix the memory leak in the image processing pipeline. Remove redundant
>     allocations. Refactor the buffer pool.
> ```

### Example 5 — Error Message

> **Non-STE:** Error: A malformed token was encountered during request validation. The request was rejected.
>
> **STE:** Error: The token validator found a malformed token. The server rejected the request.
>
> **Principle applied:** P8 — Use standard, well-known technical nouns. Method 1 applied: the agent ("token validator") moves to subject position.
>
> **Explanation:** The original error message uses passive voice. The user does not know which component detected the error. The STE version names two agents: the token validator (which found the problem) and the server (which rejected the request).

Realistic context — the structured log entry for a failed request:

> **Non-STE:**
> ```json
> {
>   "level": "error",
>   "msg": "A malformed token was encountered during request validation. The request was rejected."
> }
> ```
>
> **STE:**
> ```json
> {
>   "level": "error",
>   "msg": "The token validator found a malformed token. The server rejected the request."
> }
> ```

### Example 6 — Configuration File Comment

> **Non-STE:** # The maximum number of concurrent connections is controlled by this setting. Requests beyond this limit are queued.
>
> **STE:** # This setting controls the maximum number of concurrent connections. The server queues requests beyond this limit.
>
> **Principle applied:** P11 — One term per concept. Method 1 applied: the agent ("this setting") moves to subject position. The second sentence adds a clear agent ("the server").
>
> **Explanation:** Configuration comments describe static behavior. Passive voice in a configuration comment can make the relationship between the setting and the behavior unclear. Active voice names the setting as the agent that controls the behavior.

Realistic context — the config block in a TOML file:

> **Non-STE:**
> ```toml
> # The maximum number of concurrent connections is controlled by this
> # setting. Requests beyond this limit are queued.
> max_connections = 100
> ```
>
> **STE:**
> ```toml
> # This setting controls the maximum number of concurrent connections.
> # The server queues requests beyond this limit.
> max_connections = 100
> ```

## Edge Cases

### Edge Case 1 — Unknown Agent (Standard Exception)

When the agent that performed an action is genuinely unknown, the passive voice is correct. This is the standard exception defined by the original ASD-STE100 rule. In code documentation, this applies to:

- Unexpected data corruption with no identifiable cause
- External network failures where the remote endpoint is unknown
- Hardware faults that manifest as software errors
- Race conditions where the exact sequence of events is not reproducible

> **Correct (passive):** The data was corrupted before the checksum was computed.
> **Incorrect (active):** Something corrupted the data before the checksum was computed. (Too vague — "something" adds no information.)

Realistic context — a crash report from a corrupted write:

> **Correct (passive):**
> ```text
> [fatal] The data was corrupted before the checksum was computed. The write
> completed without an error from the storage driver, so no component on our
> side can be named as the cause.
> ```
> **Incorrect (active):**
> ```text
> [fatal] Something corrupted the data before the checksum was computed.
> ```
> "something" adds no information and sends the reader looking for a phantom
> process.

NOTE: Use the word "something" as the agent only when you can describe the type of agent (for example, "some process," "some external service"). If you cannot even describe the type, keep the passive voice.

### Edge Case 2 — Topic-Comment Structure in Descriptive Text

In descriptive writing, a sentence sometimes needs to make the object the topic (the thing the paragraph is about). When the object is the established topic of the paragraph and the agent is irrelevant to the description, the passive voice can be clearer than the active voice.

> **Active (awkward):** The developer stores the configuration file in the `/etc/myapp` directory.
> **Passive (acceptable):** The configuration file is stored in the `/etc/myapp` directory.

In this pair, the configuration file is the topic of the documentation section. The developer is not relevant to the description. The passive voice keeps the topic consistent.

However, if the documentation section describes the developer's responsibilities, use the active voice with "you" as the subject.

> **Correct:** You must store the configuration file in the `/etc/myapp` directory.

Realistic context — a config reference table where the file is the topic:

> **Topic-comment (acceptable passive):**
> ```markdown
> ## Configuration files
>
> The configuration file is stored in the `/etc/myapp` directory. The
> environment file is stored in the same directory. The session file is
> written next to them at runtime.
> ```
> **Developer-responsibility (active):**
> ```markdown
> ## Before you deploy
>
> You must store the configuration file in the `/etc/myapp` directory. You
> must also copy the environment file to the same directory.
> ```

**Decision rule:** If the paragraph topic is the object (the thing acted upon) and changing to active voice would introduce an agent that distracts from the topic, use the passive voice. If the paragraph topic is the agent, use the active voice.

### Edge Case 3 — Academic or RFC-Style References in Code Documentation

Some code documentation includes references to academic papers, RFCs, or formal specifications. These external documents often use passive voice as a convention. When you quote or paraphrase an external document, you may keep the passive voice and add a NOTE that identifies the non-STE source.

> NOTE: The following description quotes RFC 7230. The passive voice in the quotation is from the original RFC text.
>
> > "The request message is parsed by the server into its component parts."

Do not rewrite the quotation. The rule applies only to the documentation text that you write.

Realistic context — a proxy server doc that quotes the RFC:

> **Your prose (STE):**
> ```markdown
> Our proxy reads the request line first. The server parses the headers after
> it reads the body.
> ```
> **Quoted RFC (unchanged passive):**
> ```markdown
> NOTE: The following description quotes RFC 7230. The passive voice in the
> quotation is from the original RFC text.
>
> > "The request message is parsed by the server into its component parts."
> ```

### Edge Case 4 — Framework-Generated Documentation

Some frameworks and tools generate API documentation automatically from code annotations, type definitions, or schema files (for example, OpenAPI/Swagger, JSDoc templates, Sphinx autodoc summaries). These generators sometimes produce passive voice constructions.

If you control the generator template (for example, a Sphinx theme or a JSDoc template), configure it to use active voice. If you do not control the generator output, add a NOTE at the top of the generated documentation.

> NOTE: This document was generated by [tool name]. Some sentences use the passive voice. Refer to the source code comments for STE-Code compliant descriptions.

Realistic context — a generated OpenAPI page:

> **Generated doc (passive, not yours to fix):**
> ```markdown
> NOTE: This document was generated by openapi-generator. Some sentences use
> the passive voice. Refer to the source code comments for STE-Code compliant
> descriptions.
>
> > The user object is returned by the GET /users endpoint.
> ```
> **Your source comment (STE, which the template should copy):**
> ```javascript
> /**
>  * Get the current user. The GET /users endpoint returns the user object.
>  */
> ```

### Edge Case 5 — Passive Voice in Established Error Message Standards

Some operating systems, language runtimes, and standard libraries produce error messages in the passive voice. Examples include POSIX error strings ("Permission denied"), HTTP status reason phrases ("Not Found"), and database error codes.

Do not rewrite error messages from external systems. The rule applies only to error messages that you write in your own application code.

> **Your error message (STE):** The server cannot connect to the database at host:port.
> **System error message (unchanged):** Connection refused.

Realistic context — an application catch block:

> **Your code (STE message you write):**
> ```go
> if err != nil {
>     return fmt.Errorf("the server cannot connect to the database at %s:%s", host, port)
> }
> ```
> **System string (unchanged, from the OS):**
> ```text
> Connection refused
> ```

## Cross-References

This rule interacts with several other STE-Code rules. Obey all related rules when you apply Rule 3.6.

- **Rule 1.1 (Approved Words):** When you convert a passive sentence to active voice, you may need to introduce a new agent as the subject. Make sure the agent is an approved word from the STE-Code dictionary or a permitted technical noun (Rule 1.5). Refer to the Canonical Synonym Table for preferred replacements.
- **Rule 1.5 (Technical Code Nouns):** Technical nouns that name code entities (for example, *middleware*, *validator*, *container*, *allocator*, *mutex*) are permitted as agents in active voice sentences. The agent must be a real code entity, not a vague abstraction.
- **Rule 1.12 (Technical Verbs):** When you write an active voice sentence, the verb is often a technical verb (for example, *parse*, *compile*, *deploy*, *render*, *query*, *allocate*). Use these verbs in their approved simple forms. Do not use them in compound passive constructions.
- **Rule 3.1 (Simple Verb Tenses):** Active voice sentences use the simple present or simple past tense. A passive sentence can hide a compound tense behind the auxiliary verb "be." When you convert to active voice, you also simplify the tense.
- **Rule 3.4 (Auxiliary Verbs):** Passive voice uses the auxiliary verb "be" plus a past participle. Converting a passive sentence to active voice removes the unnecessary auxiliary verb. If the passive construction also uses "have" (for example, "has been parsed"), refer to Rule 3.4 for guidance on removing compound auxiliaries.
- **Rule 3.5 (-ing Forms):** Passive progressive constructions (for example, "is being parsed") combine a passive auxiliary with an "-ing" form. These constructions violate both Rule 3.5 and Rule 3.6. Convert them to active voice first, then check for any remaining "-ing" forms.
- **Rule 3.7 (Sentence Length):** Sentences must not exceed 20 words in procedural text and 25 words in descriptive text. Passive constructions are often longer than their active equivalents. Converting to active voice usually shortens the sentence. If the active sentence is still too long, split it into two or more sentences.

> **See also:** Rule 1.1 — Use approved words (dictionary and Canonical Synonym Table)
> **See also:** Rule 1.5 — Use technical nouns from the code-domain categories
> **See also:** Rule 1.12 — Use approved technical verbs in their simple forms
> **See also:** Rule 3.1 — Use only the simple verb tenses
> **See also:** Rule 3.4 — Use only the approved auxiliary verbs
> **See also:** Rule 3.5 — Use the "-ing" form only as a technical noun or modifier
> **See also:** Rule 3.7 — Write sentences that do not exceed the word limit

## Grammar Notes

### The Linguistic Basis of the Rule

In English grammar, voice is a property of the clause that expresses the relationship between the verb and its arguments. The two voices in English — active and passive — assign different grammatical roles to the same logical participants.

**Active Voice Structure**

```
Subject (Agent) + Verb + Object (Patient)
```

The grammatical subject is the agent (the doer). The grammatical object is the patient (the receiver of the action).

**Passive Voice Structure**

```
Subject (Patient) + be + Past Participle (+ by + Agent)
```

The grammatical subject is the patient. The agent is either placed in an optional "by"-phrase or omitted entirely.

### Why Passive Voice Obscures Agency

In technical documentation, the reader needs to know two things about every action:

1. What action happens
2. Who or what performs the action

Active voice delivers both pieces of information in the natural reading order. Passive voice delivers the action first and the agent last (or not at all). This reversal makes the reader work harder to understand the sentence.

Consider this passive sentence from API documentation:

> *The request is validated by the middleware.*

The reader must:
1. Identify the action ("is validated")
2. Search for the agent in the "by"-phrase ("by the middleware")
3. Mentally reconstruct the active version ("The middleware validates the request")

In the active version, the reader gets the agent and the action in the natural subject-verb-object order.

### The "By" Test

The most reliable test for passive voice is the "by whom or by what?" test. Ask this question after the verb phrase:

> *The data was encrypted...* → by whom? → *by the crypto module.* (Passive detected.)

If the sentence does not contain a "by"-phrase but can accept one without changing the meaning, it is still passive:

> *The file was saved.* → The file was saved *by the application.* (Passive detected, agent omitted.)

If the sentence cannot accept a "by"-phrase with the same meaning, the construction is not passive. It may be a past participle used as an adjective (Rule 3.3) or a copular construction:

> *The file is saved.* (Adjective — describes the state of the file, not a passive action.)

### Common Passive Constructions in Code Documentation

The table below shows passive constructions that are common in code documentation and their active equivalents. Use this table as a quick reference when you edit documentation.

| Passive Construction | Active Equivalent | Conversion Method |
|---|---|---|
| *is returned by* | *returns* | Method 1: move agent to subject |
| *can be used to* | *you can use ... to* | Method 4: insert "you" |
| *is configured by* | *configures* | Method 1: move agent to subject |
| *is called when* | *calls* | Method 1: move agent to subject |
| *was added in version* | *(we) added ... in version* | Method 4: insert "we" |
| *should be installed* | *install* (imperative) | Method 3: imperative form |
| *is designed to* | *(we) designed ... to* | Method 4: insert "we" |
| *has been deprecated* | *(we) deprecated* | Method 4: insert "we" |
| *will be removed in* | *(we) will remove ... in* | Method 4: insert "we" |

### Interaction with Modal Verbs

Passive constructions that include modal verbs (can, must, should, may, will) require a two-step conversion:

1. Identify the agent.
2. Move the agent to the subject position and keep the modal verb.

| Passive with Modal | Active with Modal |
|---|---|
| *The file can be opened with this command.* | *You can open the file with this command.* |
| *The setting must be configured before startup.* | *You must configure the setting before startup.* |
| *The output will be written to stdout.* | *The program will write the output to stdout.* |

When the agent is the reader, use "you" with the modal verb. When the agent is a code component, use the component name with the modal verb.

### Structural Avoidance Patterns

When you edit documentation to convert passive voice to active voice, apply these three structural patterns. Each pattern maps to a specific type of passive construction.

**Pattern A — Agent in "by"-Phrase (Method 1)**

Use this pattern when the sentence contains a "by"-phrase that identifies the agent. Move the agent to the subject position and change the verb to the active form.

| Input Structure | Output Structure |
|---|---|
| *Patient + be + past participle + by + Agent* | *Agent + active verb + Patient* |

> **Input:** The token is validated by the auth middleware.
> **Output:** The auth middleware validates the token.

**Pattern B — No Agent, Procedural Context (Method 3)**

Use this pattern when the sentence is in a procedural section and the agent is the reader. Change the verb to the imperative form.

| Input Structure | Output Structure |
|---|---|
| *Patient + modal + be + past participle* | *Imperative verb + Patient* |

> **Input:** The dependencies should be installed before the build.
> **Output:** Install the dependencies before the build.

**Pattern C — No Agent, Descriptive Context (Method 4)**

Use this pattern when the sentence is in a descriptive section and the agent is the reader or your organization. Insert "you" or "we" as the subject.

| Input Structure | Output Structure |
|---|---|
| *Patient + be + past participle* | *You/We + active verb + Patient* |

> **Input:** The configuration file is stored in the config directory.
> **Output:** You must store the configuration file in the config directory.
> **Alternative:** We store the configuration file in the config directory. (If "we" refers to the project.)

### Interaction with the Canonical Synonym Table

When you convert a passive sentence to active voice, you must also check the replacement verb against the STE-Code Canonical Synonym Table. Many passive constructions contain avoided words that need replacement.

> **Non-STE:** The result is used by the downstream pipeline.
>
> **STE:** The downstream pipeline uses the result.

In this pair, three fixes work together:
1. Convert passive to active (*is used by* → active verb) — Rule 3.6.
2. Replace the avoided word (*used* → *uses*) — Rule 1.1 and Canonical Synonym Table.
3. Apply active voice correctly (*pipeline uses the result*) — Rule 3.6.

> **Non-STE:** The error is displayed on the console by the logger.
>
> **STE:** The logger shows the error on the console.

In this pair, two fixes work together:
1. Convert passive to active (*is displayed by* → *shows*) — Rule 3.6.
2. Replace the avoided word (*display* → *show*) — Rule 1.1 and Canonical Synonym Table.

> **Non-STE:** The report is generated by the scheduler every night.
>
> **STE:** The scheduler makes the report every night.

In this pair, two fixes work together:
1. Convert passive to active (*is generated by* → *makes*) — Rule 3.6 and Method 1.
2. Replace the avoided word (*generated* → *makes*) — Rule 1.1 and Canonical Synonym Table (approved verb: *make* replaces *generate*).
