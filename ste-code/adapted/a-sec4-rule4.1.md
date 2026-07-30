# Rule 4.1 — Write Short and Clear Sentences

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.1

## Original Rule

Write short and clear sentences that give accurate instructions and information.

In procedures, give short and clear instructions directly to the reader (imperative form).

In a descriptive text, make sure that each sentence has only one topic (subject or idea) and does not contain the imperative form. Then, in the sentences that follow, gradually give information about that topic.

For the two types of writing, always make sure that your text is not abstract. Make sure that it clearly shows how to do a task or how a system operates. Be accurate. Do not give information that is not accurate or can have different meanings.

## STE-Code Adaptation

Write short and clear sentences in code documentation. Each sentence must give accurate information about the code.

In API method and function descriptions (procedural writing), give short and clear instructions directly to the reader in the imperative form. Each work step describes one action.

In class, module, and type descriptions (descriptive writing), make sure that each sentence has only one topic. Do not use the imperative form. Give information about the topic gradually across the sentences that follow.

Always make sure that your documentation is not abstract. Make sure that it clearly shows how to use a function or how a module operates. Be accurate. Do not give information that is not accurate or can have different meanings.

### Examples

**Procedural writing (function description):**

> **Non-STE:** To call the `initialize` method, first pass the three configuration parameters that set up the connection to the database, and then, after calling the method, check the return value for a success code or an error object.
>
> **STE:**
> 1. Call the `initialize` method as follows:
>    A. Pass the three configuration parameters that set the connection to the database.
>    B. Call the method.
>    C. Check the return value. The return value is a success code or an error object.
>
> *Adapted from original rule principle — procedural writing uses short, clear instructions; no direct spec pair*

**Descriptive writing (class description):**

> **Non-STE:** The `HttpClient` class has two internal buffers connected together and linked with callbacks between the request handler and the response dispatcher.
>
> **STE:** The `HttpClient` class has two internal buffers. The internal buffers are connected together with callbacks. These callbacks link the request handler to the response dispatcher.
>
> *Adapted from original rule principle — descriptive writing uses one topic per sentence; no direct spec pair*

**Avoid abstract statements:**

> **Non-STE:** No null values are permitted.
>
> **STE:** Make sure that the function does not return a null value.
>
> *Adapted from original rule principle — text must not be abstract and must clearly show how to do a task; no direct spec pair*

---

## Code-Domain Explanation

This rule applies across all code documentation types. Each type has a different primary mode (procedural or descriptive). The sentence-length limits help readers scan and understand quickly.

### README Files

A README file uses both procedural and descriptive writing. Use procedural writing for setup instructions. Use descriptive writing for project overviews and architecture summaries.

**Procedural section (setup instructions):**

> **Non-STE:** After you run the build command, you should then deploy the container to the registry and finally run the integration tests against the staging environment.
>
> **STE:**
> 1. Run the build command.
> 2. Deploy the container to the registry.
> 3. Run the integration tests against the staging environment.
>
> *Principles applied: P1 (approved words), clarity through short sentences*

**Descriptive section (project overview):**

> **Non-STE:** This project is a high-performance HTTP router written in Rust that uses a radix tree for route matching and supports middleware, path parameters, and nested route groups.
>
> **STE:** This project is a high-performance HTTP router. The router uses a radix tree for route matching. The router supports middleware. The router supports path parameters. The router supports nested route groups.
>
> *Principles applied: One topic per sentence, no nested clauses*

### API Documentation

API reference docs use descriptive writing for endpoint and type summaries. They use procedural writing for request/response examples and error handling.

**Descriptive (endpoint summary):**

> **Non-STE:** GET /users/:id returns a user object with their profile information and a list of permissions that they have been granted, or a 404 if the user does not exist.
>
> **STE:** GET /users/:id returns a user object. The user object contains profile information. The user object contains a list of granted permissions. The endpoint returns a 404 error if the user does not exist.
>
> *Principles applied: One topic per sentence, gradual information delivery*

**Procedural (error handling):**

> **Non-STE:** If the API returns a 429 status code, you need to check the Retry-After header and wait for the specified number of seconds before sending the request again.
>
> **STE:**
> 1. Check the status code of the response.
> 2. If the status code is 429, read the `Retry-After` header.
> 3. Wait for the specified number of seconds.
> 4. Send the request again.
>
> *Principles applied: One instruction per step, imperative mood*

### Docstrings and Inline Comments

Docstrings combine descriptive and procedural writing. The first line is a short descriptive summary. The body gives procedural details for parameters, return values, and exceptions.

**Python docstring — before:**

```python
def connect(host: str, port: int, timeout: int = 30) -> Connection:
    """Connect to the remote server specified by the host parameter on the
    given port and then return a new Connection object with the specified
    timeout, raising a ConnectionError if the server cannot be reached."""
```

**Python docstring — after (STE):**

```python
def connect(host: str, port: int, timeout: int = 30) -> Connection:
    """Connect to a remote server.

    Parameters:
        host: The server address.
        port: The server port.
        timeout: The connection timeout in seconds. The default is 30.

    Returns:
        A new Connection object.

    Raises:
        ConnectionError: If the server does not respond.
    """
```

*Principles applied: One topic per sentence, imperative mood for action description*

### Commit Messages

Commit messages use the imperative mood. A commit message has two parts: a short summary line (max 72 characters) and an optional body with one topic per paragraph.

> **Non-STE:** This commit fixes the bug where the login page crashes when a user enters a password that contains special characters and the password validation library throws an error that is not caught by the controller.
>
> **STE:**
> ```
> Fix crash on login with special-character passwords
>
> The password validation library threw an uncaught error.
> The controller did not catch the error.
> Add a try-catch block in the login controller.
> ```
>
> *Principles applied: Short summary, one topic per body sentence*

### Error Messages

Error messages must be short, accurate, and not abstract. Use descriptive writing. Tell the user what went wrong and how to fix it.

> **Non-STE:** An error occurred while attempting to process the configuration that you provided because it contains values that are not valid for the current environment.
>
> **STE:** The configuration file has an invalid value. Check the `database.url` property. The value must start with `postgres://`.
>
> *Principles applied: Short sentences, no abstract language, one topic per sentence*

---

## Paradigm-Specific Guidance

### Object-Oriented (Java, C++, C#, Python Classes)

Class and interface documentation uses descriptive writing. Method documentation uses procedural writing. Keep class summaries to one short sentence. Break method descriptions into numbered steps.

**Class documentation:**

> **Non-STE:** The `UserRepository` class provides methods for creating, reading, updating, and deleting user records from the database using an internal connection pool and a query builder with support for transactions.
>
> **STE:** The `UserRepository` class manages user records in the database. The class uses a connection pool. The class uses a query builder. The query builder supports transactions.
>
> *Principles applied: One topic per sentence, gradual information delivery*

**Method documentation (procedural):**

> **Non-STE:** Call the `save` method with a User object and it will either insert a new record if the user has no ID or update the existing record if the user does have an ID, returning the saved User object.
>
> **STE:**
> 1. Call the `save` method with a User object.
> 2. The method inserts a new record if the user has no ID.
> 3. The method updates the record if the user has an ID.
> 4. The method returns the saved User object.
>
> *Principles applied: One action per step, imperative mood*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional code documentation uses descriptive writing for type signatures and pure function behavior. Use procedural writing only for effectful functions (IO, side effects). Keep type descriptions short.

**Type signature documentation (descriptive):**

> **Non-STE:** `parseConfig :: String -> Either ParseError Config` takes a raw configuration string and attempts to parse it into a Config value, returning either the parse error or the Config.
>
> **STE:** `parseConfig` receives a raw configuration string. The function returns an `Either ParseError Config` value. `Left ParseError` means the input was not valid. `Right Config` means the parse was successful.
>
> *Principles applied: One topic per sentence, descriptive writing for pure functions*

**Effectful function documentation (procedural):**

> **Non-STE:** To read the file at the given path and return its contents as a string, call `readConfigFile` with the path and it will return an IO action that reads the file.
>
> **STE:**
> 1. Call `readConfigFile` with a file path.
> 2. The function returns an IO action.
> 3. The IO action reads the file.
> 4. The IO action returns the file contents as a string.
>
> *Principles applied: One action per step, procedural writing for effectful functions*

### Procedural (C, Go, Bash)

Procedural code documentation uses procedural writing heavily. Each function description is a sequence of steps. Use descriptive writing only for data structure overviews.

**Function documentation:**

> **Non-STE:** The `process_buffer` function takes a pointer to a buffer and its size, iterates over the buffer to find all occurrences of the null byte and replaces them with spaces, returning the number of replacements that were made.
>
> **STE:**
> 1. Call `process_buffer` with a buffer pointer and a buffer size.
> 2. The function finds all null bytes in the buffer.
> 3. The function replaces each null byte with a space character.
> 4. The function returns the number of replacements.
>
> *Principles applied: One action per step, clear imperative structure*

**Struct documentation (descriptive):**

> **Non-STE:** The `Connection` struct holds a file descriptor for the socket, the remote address as a sockaddr_in, and a buffer for reading incoming data, all of which are initialized by `new_connection`.
>
> **STE:** The `Connection` struct holds a socket file descriptor. The struct holds a remote address (`sockaddr_in`). The struct holds a read buffer. Call `new_connection` to initialize the struct.
>
> *Principles applied: One topic per sentence, descriptive for data structures*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation uses descriptive writing almost exclusively. Describe what the configuration does. Do not give step-by-step procedures. The system handles execution order.

**Terraform resource documentation:**

> **Non-STE:** The `aws_instance` resource creates an EC2 virtual machine in the specified subnet with the given AMI and instance type, and you can also attach security groups and IAM roles to control access.
>
> **STE:** The `aws_instance` resource creates an EC2 virtual machine. The resource uses the specified AMI. The resource uses the specified instance type. The resource starts in the specified subnet. Attach security groups to control network access. Attach IAM roles to control AWS service access.
>
> *Principles applied: Descriptive writing for resource behavior, short sentences*

**SQL schema documentation:**

> **Non-STE:** The `orders` table stores customer orders with a foreign key to the customers table, shipping and billing addresses, and the order status, all using the InnoDB engine with row-level locking.
>
> **STE:** The `orders` table stores customer orders. The `customer_id` column is a foreign key to the `customers` table. The table stores a shipping address. The table stores a billing address. The table stores an order status. The table uses the InnoDB engine. The engine uses row-level locking.
>
> *Principles applied: One topic per sentence, descriptive writing for schemas*

### Systems (Rust Ownership, C Memory)

Systems documentation describes ownership, lifetimes, and memory behavior. Use descriptive writing for invariants. Use procedural writing for unsafe operations.

**Ownership documentation (descriptive):**

> **Non-STE:** The `Buffer` struct owns a heap-allocated byte slice and when the Buffer is dropped the allocation is freed, but you can call `split` to transfer ownership of a portion of the buffer to a new Buffer and the original keeps the remaining portion.
>
> **STE:** The `Buffer` struct owns a heap-allocated byte slice. The allocation is freed when the `Buffer` is dropped. Call `split` to transfer ownership of a part of the buffer. The method returns a new `Buffer`. The original `Buffer` keeps the remaining bytes.
>
> *Principles applied: One topic per sentence, imperative for unsafe/side-effect operations*

**Unsafe block documentation (procedural):**

> **Non-STE:** Before dereferencing the raw pointer, make sure that the pointer is not null, that it points to a valid memory region of the correct size, and that no other thread is writing to that memory region at the same time.
>
> **STE:**
> 1. Check that the raw pointer is not null.
> 2. Check that the pointer points to a valid memory region.
> 3. Check that the memory region has the correct size.
> 4. Check that no other thread writes to the memory region.
> 5. Dereference the pointer.
>
> *Principles applied: One precondition per step, imperative mood for unsafe operations*

---

## Extended Examples

### Example 1 — Nested Clauses in API Documentation

> **Non-STE:** The `transform` method accepts a list of items, applies a mapping function to each item in parallel, collects the results, and then filters out any null values before sorting the remaining items and returning them as a new list.
>
> **STE:** The `transform` method processes a list of items:
> 1. Apply a mapping function to each item. The mapping runs in parallel.
> 2. Collect the results into a new list.
> 3. Remove null values from the list.
> 4. Sort the remaining items.
> 5. Return the sorted list.
>
> *Principles applied: P1 (approved words: use→apply), one action per step, imperative mood*

### Example 2 — Abstract Language in Error Messages

> **Non-STE:** The system encountered an unexpected condition that prevents the requested operation from completing successfully.
>
> **STE:** The operation failed. The database connection timed out. Check the `DATABASE_URL` environment variable. Make sure that the database server is running.
>
> *Principles applied: No abstract language, short sentences, descriptive then procedural*

### Example 3 — Multiple Topics in a Class Description

> **Non-STE:** The `CacheManager` class wraps a Redis client with automatic serialization, configurable TTLs, and a fallback to an in-memory store, and provides methods for atomic get-and-set operations that prevent race conditions.
>
> **STE:** The `CacheManager` class wraps a Redis client. The class adds automatic serialization. The class supports configurable TTLs. The class uses an in-memory store as a fallback. The class provides atomic get-and-set methods. These methods prevent race conditions.
>
> *Principles applied: One topic per sentence, descriptive writing, gradual information delivery*

### Example 4 — Imperative/Narrative Mix in a README

> **Non-STE:** First you need to install the dependencies with `npm install` and then you should configure the environment variables in the `.env` file before starting the development server which will be available at `http://localhost:3000`.
>
> **STE:**
> 1. Install the dependencies: `npm install`
> 2. Set the environment variables in the `.env` file.
> 3. Start the development server: `npm run dev`
>
> The server is available at `http://localhost:3000`.
>
> *Principles applied: One instruction per step, imperative mood, descriptive sentence separated*

### Example 5 — Long Sentences in Commit Messages

> **Non-STE:** Refactor the authentication middleware to extract the token validation logic into a separate module and add unit tests for the token parser and the validation functions.
>
> **STE:**
> ```
> Refactor authentication middleware
>
> Extract token validation logic into a separate module.
> Add unit tests for the token parser.
> Add unit tests for the validation functions.
> ```
>
> *Principles applied: Short summary, one topic per body sentence*

### Example 6 — Semicolons and Clause Nesting in Docstrings

> **Non-STE:** This decorator caches the return value of the function for the given TTL; subsequent calls with the same arguments return the cached value without executing the function body, which improves performance for expensive computations.
>
> **STE:** This decorator caches the return value of the function. The cache uses the given TTL. Later calls with the same arguments return the cached value. The function body does not execute again. This behavior improves performance for expensive computations.
>
> *Principles applied: P1 (approved words), no semicolons, one topic per sentence*

---

## Edge Cases

### Edge Case 1 — Framework Names That Are Also Common Words

Some frameworks use common English words as names (for example, `Express`, `FastAPI`, `Bun`, `Next`). These names are technical code nouns and are allowed (Rule 1.5). Do not treat them as unapproved words.

> **Non-STE:** Utilize the Express framework to serve the static assets.
>
> **STE:** Use the Express framework to serve the static assets.
>
> *The word "Express" is a technical code noun, not an unapproved adverb.*

### Edge Case 2 — Code Keywords That Conflict with Sentence Structure

Code keywords (for example, `return`, `if`, `for`, `while`) can appear in documentation. When a keyword is the topic of a sentence, format it as inline code. This formatting prevents ambiguity between the keyword and the English word.

> **Ambiguous:** The return value is a string.
> **STE:** The `return` value is a string.
>
> *Backticks show that `return` is a code keyword, not the English verb.*

> **Ambiguous:** If the condition is true, call the handler.
> **STE:** When the `if` condition is true, call the handler.
>
> *Use "when" instead of "if" to start the sentence. Put the keyword `if` in backticks. This avoids confusion with the English conjunction.*

### Edge Case 3 — Generated Code Documentation

Generated documentation (from tools such as JSDoc, Sphinx, or `go doc`) may produce long sentences. The generator controls the output format. For generated documentation:

- Apply Rule 4.1 to the source docstrings and comments.
- Accept that generated output may combine sentences.
- Prefer to fix the source text, not the generated output.

> **Generated (acceptable if source is STE):** The `parse` method receives a string and returns a Config object, or throws a ParseError if the string is not valid JSON.
> **Source docstring (must be STE):**
> 1. Call `parse` with a JSON string.
> 2. The method returns a `Config` object.
> 3. The method throws a `ParseError` if the string is not valid JSON.

### Edge Case 4 — Single-Sentence Module Summaries

Module summaries often need to convey multiple facts in one sentence. This is acceptable for the first line of a module docstring. Expand the details in the body.

> **Acceptable short summary:** The `auth` module handles user authentication and session management.
> **Body (must follow Rule 4.1):** The module supports OAuth 2.0. The module supports JWT tokens. The module manages user sessions. Each session has a configurable timeout.
>
> *The summary line is limited to one sentence by convention. The body must still follow the rule.*

### Edge Case 5 — Warnings, Cautions, and Callouts

Safety callouts (BREAKING, DEPRECATED, NOTE, WARNING) must remain short. Each callout is a single short sentence. Place additional details in the paragraph that follows.

> **Correct:**
> BREAKING: The `host` parameter is now required.
>
> In version 2.0, the `host` parameter has no default value. Update all callers to supply the `host` argument.
>
> *The callout itself is one short sentence. The following paragraph gives more information with one topic per sentence.*

---

## Grammar Notes

### Sentence Length Limits

The original ASD-STE100 rule sets a maximum of 20 words for procedural sentences and 25 words for descriptive sentences. This limit helps non-native English readers understand technical text. Apply the same limits to code documentation.

**Procedural limit:** Maximum 20 words per instruction step.

**Descriptive limit:** Maximum 25 words per descriptive sentence.

NOTE: Code blocks, inline code spans, and URLs do not count toward the word limit. Only the natural language part of the sentence counts.

**Word count procedure:**

> **Test:** "Call the `initialize` method with a `Config` object and a `Logger` instance.
> **Count:** 6 words (call, the, method, with, object, and, instance). The code spans `initialize`, `Config`, and `Logger` are not counted.

### Imperative Mood

The imperative mood gives commands directly to the reader. Use the base form of the verb. Do not use "you should", "you must", or "the user should".

> **Not imperative:** You should call the `connect` method first.
> **Imperative:** Call the `connect` method first.

In procedural writing, start each step with an imperative verb. Approved verbs include: call, pass, set, get, check, start, stop, send, remove, add, make, use, run, build, test, deploy.

### Article Use

Do not omit articles. Use "a", "an", and "the" as needed. Omission of articles causes ambiguity for non-native readers.

> **Ambiguous:** Function returns string.
> **Clear:** The function returns a string.

> **Ambiguous:** Call method with argument.
> **Clear:** Call the method with the argument.

### Clause Nesting Limit

Do not nest clauses deeper than 2 levels. A clause nest occurs when a subordinate clause is inside another subordinate clause. Break nested clauses into separate sentences.

> **3-level nest (do not use):** The function returns a value that the caller must check before it passes the value to the handler.
> **Restructured (max 2 levels):** The function returns a value. The caller must check the value. Then the caller passes the value to the handler.

### Sentence Connectors

Do not use semicolons to join independent clauses. Use a period and start a new sentence.

> **With semicolon (do not use):** The method returns a result; the result is a JSON object.
> **Restructured:** The method returns a result. The result is a JSON object.

Use "and" or "but" only to join two short, closely related clauses within one sentence. If the result is longer than 25 words, split into two sentences.

> **Acceptable:** The method validates the input and returns a result.
> **Split (if too long):** The method validates the input. The method returns a result.

---

## Cross-References

- **Rule 1.1** — Use approved words from the STE-Code dictionary. Short sentences are easier to write when you use approved words.
- **Rule 1.2** — Use words only as their specified part of speech. This prevents ambiguous sentence structures.
- **Rule 1.3** — Use words only with their approved meanings. Accurate word meaning supports short, clear sentences.
- **Rule 1.10** — No slang, jargon, or regional terms. Slang adds unnecessary words to sentences.
- **Rule 1.11** — One term per concept. Consistent terminology makes short sentences easier to understand.
- **Rule 4.2** — Use the active voice. The active voice produces shorter sentences than the passive voice.
- **Section 5 (Procedural Writing)** — Detailed guidance for writing step-by-step instructions.
- **Section 6 (Descriptive Writing)** — Detailed guidance for writing descriptions and explanations.

---

## Summary Checklist

Before you publish code documentation, check each sentence:

- [ ] The sentence has a maximum of 20 words (procedural) or 25 words (descriptive).
- [ ] The sentence has only one topic or one instruction.
- [ ] Procedural sentences use the imperative mood (start with a verb).
- [ ] Descriptive sentences do not use the imperative mood.
- [ ] The text is not abstract. It gives concrete information about the code.
- [ ] The text has no semicolons.
- [ ] The text has no clause nesting deeper than 2 levels.
- [ ] Articles (a, an, the) are not omitted.
- [ ] Code keywords are in backticks when they are the topic of the sentence.
- [ ] Contractions (don't, can't, it's) are not used.
