# Level 4 — Section 4: Sentence Construction (Rules 4.1–4.5)

Scope: how to build a single sentence of code documentation — one topic, all
words present, vertical lists for complex text, explicit connecting words, and
correct articles.

Source: adapted from ASD-STE100 Issue 9, Section 4. Examples are code-domain
only. Use this file as the operative rule set for API docs, docstrings, code
comments, README sections, commit messages, changelogs, CLI help, and error
text.

Two writing modes are referenced throughout:

- Descriptive writing — a class, module, type, or resource description. No
  imperative form. One fact per sentence.
- Procedural writing — a function, method, or CLI step. Imperative form. One
  instruction per sentence.

Quick index:

| Rule | Requirement |
| --- | --- |
| 4.1 | One topic per sentence. No abstract text. |
| 4.2 | Do not omit words. Do not use contractions. |
| 4.3 | Use a vertical list for complex text. |
| 4.4 | Use connecting words and connecting phrases. |
| 4.5 | Use an article or a demonstrative adjective before a noun. |

---

## Rule 4.1 — One topic per sentence, no abstract text

### Requirement

- In descriptive text, give each sentence one topic and do not use the
  imperative form. Give more information about that topic in the sentences that
  follow.
- In procedural text, give one instruction per sentence in the imperative form.
- Do not write abstract text. Show how to use a function or how a module
  operates. Give the value and the condition for each measurable claim.

Limits: 20 words maximum for a procedural sentence, 25 words maximum for a
descriptive sentence. Inline code spans and URLs do not count.

### Examples

Descriptive — split the topics:

> **Non-STE:** The `HttpClient` class has two internal buffers connected together and linked with callbacks between the request handler and the response dispatcher.
>
> **STE:** The `HttpClient` class has two internal buffers. The internal buffers are connected together with callbacks. These callbacks link the request handler to the response dispatcher.

```java
/**
 * STE:
 * The ConnectionPool manages a set of reusable TCP connections.
 * The connections are created lazily when the pool starts.
 * Each connection is validated when the caller checks it out.
 * Each connection is reset before the caller returns it to the pool.
 * The caller always receives a clean socket from the pool.
 */
public class ConnectionPool { /* ... */ }
```

Do not state a prohibition abstractly; state the action:

> **Non-STE:** No null values are permitted.
>
> **STE:** Make sure that the function does not return a null value.

```python
# STE:
def read_config(path: str) -> dict:
    """Load the configuration from the file at the given path.
    Return an empty dictionary if the file does not exist.
    Do not return null. Raise ConfigError if the file is not valid."""
```

Show the direction of change and the measured value:

> **Non-STE:** Different payload sizes will change the parse time.
>
> **STE:** When the payload size increases, the parse time increases.
>
> **STE:** The parse time is 2 milliseconds for a payload of 1 KB.

```go
// STE:
// ParseMessage decodes a message from the given byte slice.
// The function parses 1 KB of input in 2 milliseconds.
// When the input size doubles, the parse time increases by 1.8 milliseconds.
// The function returns ErrTooLarge if the input is larger than 4 MB.
func ParseMessage(buf []byte) (*Message, error)
```

Procedural — one instruction per step:

```python
# STE:
# 1. Build the HttpClient with the default configuration.
# 2. Set the timeout to 30 seconds.
# 3. Call the send method with the request object.
# 4. Check the response status code.
# 5. Read the response body into a string.
```

```bash
# STE:
# 1. Export the API token to the TOKEN variable.
# 2. Select the staging environment with the --env flag.
# 3. Run the deploy script.
# 4. Check the build log for the success message.
```

Declarative resource — one fact per sentence:

```hcl
# STE:
# The aws_s3_bucket resource creates a storage bucket for application logs.
# The bucket name is "app-logs".
# The bucket keeps a version of each object that you overwrite.
# The bucket encrypts each object with the AES256 algorithm.
resource "aws_s3_bucket" "logs" {
  bucket = "app-logs"
}
```

### By paradigm

- Object-oriented (Java, C++, C#, Python): class documentation is descriptive.
  Keep the class summary to one short sentence with one topic. Break method
  descriptions into numbered imperative steps.
- Functional (Haskell, Elixir, Clojure, Rust): type signatures are descriptive.
  State one property per sentence. Effectful functions use procedural steps.
- Procedural (C, Go, Bash): function documentation is a sequence of steps. Each
  step is one imperative sentence with one instruction.
- Declarative (SQL, Terraform, Kubernetes YAML): resource documentation is
  descriptive. Describe what the configuration does, one fact per sentence.
- Systems (Rust ownership, C memory): describe invariants and ownership rules in
  descriptive sentences. Use imperative steps only for unsafe operations.

### Edge cases

- Generated documentation: JSDoc, Sphinx, and `go doc` output may combine
  sentences. Apply the rule to the source docstrings, not to the generated file.
- Single-sentence module summary: the first docstring line may carry the purpose
  in one sentence. Expand the details below, one topic per sentence.
- Safety callouts (BREAKING, DEPRECATED, NOTE): keep the callout to one short
  sentence. Put detail in the paragraph that follows.
- Error messages: state what failed as one topic. Tell the reader how to fix it
  in a second sentence. Do not write "Invalid input occurred."
- Commit messages: one topic in the subject line. One change per bullet in the
  body.
- README sections: one idea per paragraph, one sentence per listed feature.

### Grammar notes

- Use the imperative verb first in a procedural step: call, set, pass, check,
  start, send, remove, add, make, use, run, build, test, deploy. Do not write
  "you should" or "the user must". Reserve "we recommend" for optional actions.
- Do not nest clauses deeper than two levels. Split them into sentences.
- Prefer the active voice. The subject must perform the action.
- Replace "performance may vary" with the measured value and its condition.

### Checklist

- [ ] The sentence has 20 words maximum (procedural) or 25 (descriptive).
- [ ] The sentence has one topic or one instruction.
- [ ] Procedural sentences use the imperative mood; descriptive sentences do not.
- [ ] The text shows how to use the code and is not abstract.
- [ ] Each descriptive sentence states one fact in the active voice.
- [ ] Each measurable claim gives the value and the condition.

### See also

Rule 1.1 (approved words), Rule 1.3 (approved meanings), Rule 4.2 (no omitted
words), Section 5 (procedural writing), Section 6 (descriptive writing).

---

## Rule 4.2 — Do not omit words or use contractions

### Requirement

Each sentence must have all its parts. Write all words in full. A shorter
sentence is not necessarily easier to read.

- Do not omit nouns. The reader must know which code element the sentence
  refers to.
- Do not omit verbs. The reader must understand the action that the code
  performs.
- Do not omit the subject. The reader must know which function, class, or
  module performs the action.
- Do not omit articles (the, a, an). An omitted article makes the sentence
  ambiguous about which element is specified.
- Do not use contractions. Write "do not", "is not", "are not", "cannot",
  "will not", "does not", and "did not" in full.

### Examples

Do not omit the subject:

> **Non-STE:** Can be a maximum length of 256 characters.
>
> **STE:** The input string can have a maximum length of 256 characters.

```python
def validate_username(name: str) -> bool:
    """Check whether the user name is valid.

    The user name can have a maximum length of 256 characters.
    The user name must contain only letters, digits, and underscores.
    """
    return len(name) <= 256 and name.isidentifier()
```

Do not omit the verb:

> **Non-STE:** The return value a boolean that indicates success.
>
> **STE:** The return value is a boolean that indicates success.

```java
/**
 * Attempts to lock the resource for exclusive access.
 *
 * The return value is a boolean that indicates success.
 * The method returns true when the lock is acquired.
 * The method returns false when the lock is already held.
 */
public boolean tryLock() { ... }
```

Do not omit the noun:

> **Non-STE:** The function returns the parsed.
>
> **STE:** The function returns the parsed configuration object.

```go
// LoadConfig reads the settings file and returns the parsed configuration object.
// The function returns an error when the file is missing or malformed.
func LoadConfig(path string) (*Config, error) { ... }
```

Do not omit articles:

> **Non-STE:** `validate` function checks input parameter.
>
> **STE:** The `validate` function checks the input parameter.

```typescript
/**
 * The `validate` function checks the input parameter.
 * The `validate` function returns a boolean that reports the result.
 * A missing input parameter causes the function to return false.
 */
function validate(input: Request): boolean { ... }
```

Do not use contractions:

> **Non-STE:** The method doesn't throw an exception when the input is null.
>
> **STE:** The method does not throw an exception when the input is null.

```csharp
/// <remarks>
/// The method does not throw an exception when the input is null.
/// The method returns null when the end of the stream is reached.
/// </remarks>
public Record? ReadNext(Stream? input) { ... }
```

Give the subject in a safety statement:

> **Non-STE:** BREAKING: MAKE SURE THAT THE DATABASE IS BACKED UP. IF NOT, THIS CAN CAUSE DATA LOSS.
>
> **STE:** BREAKING: MAKE SURE THAT THE DATABASE IS BACKED UP. A MISSING BACKUP CAN CAUSE DATA LOSS.

```markdown
## BREAKING CHANGES

BREAKING: MAKE SURE THAT THE DATABASE IS BACKED UP.
A MISSING BACKUP CAN CAUSE DATA LOSS.
The migration deletes the `sessions` table.
The migration runs automatically when you start version 3.0.
```

Repeat the article across parallel nouns:

> **Non-STE:** Remove the bolt and stop.
>
> **STE:** Remove the bolt and the stop.

Without the second article, the reader can read `stop` as a verb. In code
prose the same trap appears with words such as `lock`, `check`, `run`, and
`build`. Write "Remove the lock file and the build directory."

Keep the verb in a conditional step:

> **Non-STE:** If installed, remove the shims.
>
> **STE:** If shims are installed, remove them.

```python
# If shims are installed, remove them before you run the calibration.
# The calibration step reads the raw sensor values.
```

Do not contract inside a warning:

```markdown
> **WARNING**
> If your hands are wet, do not touch the USB power adapter.
> The adapter supplies current that can cause injury.
> Keep the adapter away from water while it is connected.
```

### By paradigm

- Object-oriented (Java, C#, C++, Python): write "The method returns…", "The
  constructor creates…", "The getter returns the value of the field."
- Functional (Haskell, Elixir, Clojure, F#): write each pattern-match arm as a
  full sentence with a verb. Add a subject such as "The type variable
  represents…". Write "The first law states that…".
- Procedural (C, Go, Bash, Rust): write "The function reads a configuration
  file." Write "The script removes the build directory."
- Declarative (SQL, Terraform, Kubernetes YAML, Ansible): write "The view
  returns the active users." Write "The resource creates a storage bucket."
- Systems (Rust unsafe code, C memory management): write "The caller must
  ensure that the pointer is valid." An omitted subject hides the party that
  owns the obligation and causes real bugs.

### Edge cases

- Commit message summary line: the 72-character limit permits a relaxed form.
  The body must follow the rule strictly: "The patch removes the unused import.
  The change does not alter the behavior of the function."
- CLI help text: terminal width permits a relaxed form such as `rm FILE`. The
  manual page must write "The command removes the file."
- A code token that looks like a contraction: a test named `won't`, a variable
  `can't`, or a map key `it's` is a technical code noun. Keep it in backticks
  and do not expand it. Write "The test `won't` checks the failure path."
- Error messages and log lines: a short error string may omit articles. The
  documentation that explains the error uses full sentences: "The error means
  that the connection is closed."
- Tables and lists: a cell may hold a short phrase. The column header and the
  surrounding prose supply the subject and the verb. Write the header "The
  function returns the status code", not "Returns status".

### Grammar notes

- Every sentence needs a subject, a verb, and the required articles.
- Repeat the article when two nouns joined by "and" are different things.
- Prefer plain dictionary verbs: "check" for verify, "make" for create, "get"
  for retrieve, "set" for configure, "remove" for delete, when the simpler word
  fits the meaning.

### Checklist

- [ ] Every sentence has a subject, a verb, and the required articles.
- [ ] No words are omitted to shorten the sentence.
- [ ] No contractions are used.
- [ ] The reader knows which element performs the action.
- [ ] Parallel nouns joined by "and" each keep their article.
- [ ] Code tokens that look like contractions stay in backticks.

### See also

Rule 1.1, Rule 1.3, Rule 4.1, Rule 4.3, Rule 4.4, Rule 4.5, Section 5,
Section 6.

---

## Rule 4.3 — Use a vertical list for complex text

### Requirement

When a sentence must include many items (parameters, return fields, error
codes, configuration options, environment variables, dependencies, test cases)
or many actions, put them in a vertical list.

When you make a vertical list:

- Put a colon (:) at the end of the introductory sentence.
- Identify each item with a number, a letter, a dash, or a bullet.
- Start each item with an uppercase letter.
- Use an article before the noun that is the subject of each item, where
  applicable.
- Put a period at the end of an item if it is a full sentence. An imperative
  step such as "Set the timeout value" is a full sentence.
- Do not put a period at the end of an item if it is not a full sentence.
- Do not put a comma or a semicolon at the end of an item.
- Put a period at the end of the last item.

Do not mix imperative instructions and descriptive statements in one list.

In safety instructions, put a negative command (DO NOT) on each item that needs
one. This makes the instruction more direct.

Each item must connect to the introductory text. Test the connection by reading
"Introductory text [item]" as one sentence.

Do not nest a second vertical list inside the primary list. Use the same level
for all items. If a sub-item needs a list, start a new introductory sentence
after the parent item, or use a table.

### Examples

Constructor parameters (descriptive):

> **Non-STE:** The `UserService` constructor accepts the database URL, the cache backend, and the maximum retry count.
>
> **STE:** The `UserService` constructor accepts these parameters:
> - The `database_url` for the PostgreSQL connection string.
> - The `cache_backend` for session storage.
> - The `max_retries` for transient failure handling.

```python
class UserService:
    """Manage application users and their sessions.

    The UserService constructor accepts these parameters:
    - The database_url for the PostgreSQL connection string.
    - The cache_backend for session storage.
    - The max_retries for transient failure handling.
    """

    def __init__(self, database_url, cache_backend, max_retries=3):
        self.database_url = database_url
        self.cache_backend = cache_backend
        self.max_retries = max_retries
```

Deployment steps (procedural, one mode only):

> **Non-STE:** To deploy the application: set the `DATABASE_URL` variable, the server binds to port 8080 after startup, run the migration command.
>
> **STE:** To deploy the application, do these steps:
> - Set the `DATABASE_URL` environment variable.
> - Run the `apply-migrations` command.
> - Start the server on port 8080.

The descriptive fact "The server binds to port 8080 after startup" goes in the
prose after the list, not inside it.

Error codes for an HTTP API:

> **STE:** The API returns these error codes:
> - `400 Bad Request` for a failed input validation.
> - `401 Unauthorized` for an expired or missing token.
> - `403 Forbidden` for insufficient permissions.
> - `404 Not Found` for a missing resource.

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": "unauthorized",
  "message": "The token is expired. Get a new token and send the request again."
}
```

Safety instruction with a negative command on each item:

```text
CAUTION: WHEN YOU ACCESS THE CONFIGURATION THROUGH THE ADMIN PANEL:

- DO NOT CHANGE THE SECRET KEY.
- DO NOT DISABLE THE AUDIT LOG.
```

Configuration options (declarative):

> **STE:** The `config.yaml` file has these top-level fields:
> - The `server.port` that sets the listen port.
> - The `log.level` that sets the log verbosity.
> - The `database.pool_size` that sets the maximum open connections.
> - The `features` that lists the enabled feature flags.

```yaml
server:
  port: 8080
log:
  level: info
database:
  pool_size: 20
features:
  - new_checkout
  - dark_mode
```

Data-transfer-object fields:

> **STE:** The `CreateUserRequest` object has these fields:
> - The `email` that gives the user login.
> - The `display_name` that gives the name that shows in the UI.
> - The `role` that gives the access level.

Return codes (procedural, Go):

> **STE:** The `openFile` function returns these codes:
> - `0` for a successful open.
> - `-1` for a missing path.
> - `-2` for insufficient permission.

```go
func openFile(path string) (int, error) {
    if _, err := os.Stat(path); errors.Is(err, os.ErrNotExist) {
        return -1, fmt.Errorf("the path %q is missing", path)
    }
    f, err := os.Open(path)
    if err != nil {
        return -2, fmt.Errorf("the user lacks permission for %q", path)
    }
    defer f.Close()
    return 0, nil
}
```

Test cases:

> **STE:** The `parse_interval` function passes these test cases:
> - Accept `"10s"` and return 10 seconds.
> - Accept `"0"` and return an error.
> - Accept `"abc"` and return an error.

Dependencies:

> **STE:** The project uses these dependencies:
> - `express` for HTTP routing.
> - `pg` for the PostgreSQL database.
> - `redis` for cache storage.

Environment variables:

> **STE:** The worker reads these environment variables:
> - The `LOG_LEVEL` that sets the log verbosity.
> - The `QUEUE_URL` that sets the message queue address.
> - The `MAX_WORKERS` that sets the maximum concurrent tasks.

```bash
export LOG_LEVEL=info
export QUEUE_URL=amqp://broker:5672/tasks
export MAX_WORKERS=8
```

### By paradigm

- Object-oriented: use a list for constructor parameters, public methods,
  data-transfer-object fields, and the exceptions that a method can send.
- Functional: use a list for each variant of a sum type or each pattern-match
  arm.
- Procedural (C, Go, Bash): use a list for function return codes. One code and
  its meaning per item.
- Declarative (SQL, Terraform, YAML): use a list for top-level fields. Use a
  separate list for the sub-fields of a complex field.
- Systems (Rust, C memory): use a list for ownership or lifecycle rules. One
  constraint per item.

### Edge cases

- Nested fields: do not nest lists. Use a new introductory sentence after the
  parent item, or a table.
- Generated documentation: generated API docs (JSDoc, Sphinx, rustdoc) may use
  tables. That is acceptable. Apply the rule to prose that a human writes.
- Very short lists: two or three very short items may stay inline. Use a
  vertical list when an item has more than five words or the inline sentence
  exceeds 25 words.
- Code blocks in items: put the code block after the item text, indented under
  the item. Do not start an item with a code fence.

### Grammar notes

- Each item must complete the introductory sentence grammatically.
- Use "the" or "a/an" consistently across all items. Put the article before the
  backticks when the item starts with a code identifier.
- An item with a verb phrase ("Set the timeout value") is a full imperative
  sentence and takes a period. An item that is a relative clause ("The
  `timeout` parameter that controls the delay") takes no period until the last
  item.

### Checklist

- [ ] The introductory sentence ends with a colon.
- [ ] Each item starts with an uppercase letter.
- [ ] Each item connects to the introductory text.
- [ ] No period on non-sentence items; a period on the last item.
- [ ] No mixed procedural and descriptive items in one list.
- [ ] No nested vertical lists.
- [ ] Each code sample comes after its item sentence.

### See also

Rule 1.1, Rule 1.6 (technical code nouns), Rule 4.1, Rule 4.2, Rule 5.1
(active voice in steps).

---

## Rule 4.4 — Use connecting words and connecting phrases

### Requirement

Connecting words and connecting phrases connect a topic in one sentence with an
idea in the sentence that follows. They give code documentation a logical
structure.

- Approved connecting words: "and", "but", "then", "thus".
- Approved connecting phrases: "as a result", "at the same time".
- Demonstrative adjectives ("this", "these") also connect ideas in related
  sentences. They must point back to a topic that the previous sentence named.
- In procedural documentation, use a connecting word when an explanation is
  necessary after a work step.
- In safety instructions, use a connecting word to connect the precaution to
  its reason.

| Connector | Use it for |
| --- | --- |
| and | A second, parallel fact or step |
| but | An exception, a limit, or a correction |
| then | A time sequence in a procedure |
| thus | A logical consequence |
| as a result | A state change caused by the previous sentence |
| at the same time | Concurrent work |
| this / these + noun | A reference back to the named topic |

### Examples

"and" — two related descriptions:

> **Non-STE:** `parseInput` validates the request payload and `formatOutput` serializes the response, and they're both called in the handler.
>
> **STE:** The `parseInput` function validates the request payload. And the `formatOutput` function serializes the response data.

"but" — an exception or an alternative:

> **Non-STE:** These error-handling rules are the minimum necessary for the API layer, although the local project conventions may specify additional ones.
>
> **STE:** These error-handling rules are the minimum necessary for the API layer. But the local project conventions can give other necessary error-handling rules.

"thus" — a logical consequence:

> **Non-STE:** If the validation step fails, the middleware sets an error code on the response object, so the downstream handler gets it and skips processing.
>
> **STE:** If the validation step fails, the middleware sets an error code on the response object. Thus, the downstream handler receives the error code and skips the processing step.

"as a result" — cause and effect:

> **Non-STE:** When the cache eviction policy runs, expired entries are removed, which frees up capacity for new entries.
>
> **STE:** When the cache eviction policy runs, expired entries are removed from the cache. As a result, the cache has free capacity for new entries.

"then" — a time sequence:

> **Non-STE:** Open the database connection, after that run the migration script, and finally start the API server.
>
> **STE:** Open the database connection. Then run the migration script. And then start the API server.

Demonstrative adjective in a procedure:

> **Non-STE:** Tag the deprecated methods with the `@deprecated` annotation; it helps developers migrate to the new API.
>
> **STE:** Tag the deprecated methods with the `@deprecated` annotation. This annotation will help developers during the migration to the new API.

Safety instruction:

> **Non-STE:** Always validate user input in this module because it prevents injection attacks.
>
> **STE:** BREAKING: ALWAYS VALIDATE USER INPUT IN THIS MODULE. THIS PRECAUTION WILL PREVENT INJECTION ATTACKS.

Making an implicit link explicit in API prose:

> **Non-STE:** POST /users creates a new user account and returns a 201 status. The response body contains the created user object with an auto-generated ID. The ID can be used in later requests to reference this user.
>
> **STE:** A POST request to `/users` makes a new user account. As a result, the API returns a 201 status code. And the response body contains the created user object with an auto-generated ID. You can use this ID in later requests to refer to the user.

Configuration description:

> **STE:** Set the `max_connections` value to 64 in the config file. As a result, the connection pool reuses idle sockets. And the average request latency decreases under load.

Test description:

> **STE:** The test seeds one row in the database. Thus, the delete endpoint removes that row. And the database has zero rows after the call.

Concurrency:

> **STE:** The worker fetches the page from the remote server. At the same time, the parser reads the response stream. And both tasks finish before the timeout.

Error behavior:

> **Non-STE:** The `read_file` function returns the contents; however, it raises `PermissionError` when the path is not readable.
>
> **STE:** The `read_file` function returns the contents of the file. But it raises a `PermissionError` when the path is not readable.

### By paradigm

- Object-oriented: state the class invariant in one sentence. Use "thus" to
  connect it to the behavioral guarantee of the public API. Use "this" to refer
  back to a private field. Use "and" to group related methods.
- Functional: state the input type in one sentence. Use "and" to connect the
  happy path to the error path. Use "thus" to connect a transformation step to
  the shape of the output.
- Procedural (C, Go, Bash): state the allocation step. Use "then" for
  initialization. Use "as a result" to connect processing to the final state.
- Declarative (SQL, Terraform, YAML): state the resource spec. Use "thus" to
  connect the spec to the reconciliation outcome. Use "this" to refer back to a
  named resource.
- Systems (Rust, C memory): state the ownership rule. Use "thus" to connect it
  to the compiler guarantee. Use "but" to introduce an unsafe escape hatch.

### Edge cases

- A connecting word that is also a framework name: the `Then` assertion library
  and the Rust `and_then` combinator are technical nouns. Keep them in
  backticks. A sentence-initial connecting word is not in backticks.
- "Then" ambiguity: "then" can mean time sequence or logical consequence. When
  the meaning is not clear, use "after" for time and "thus" for logic.
- Generated code comments: the rule applies to documentation you write. Do not
  edit generated comments to add connecting words.
- Long chains: limit a connecting-word chain to two or three sentences. Use a
  list or a table for more.
- Start of a section: do not open a new section with a connecting word. The
  heading provides the structural connection. Restate the topic so the section
  stands alone.

### Grammar notes

- Starting a sentence with "and" or "but" is permitted and encouraged. It gives
  short, independent sentences with an explicit link.
- "Thus" and "as a result" sit at the start of the second sentence. Do not use
  a semicolon before "thus".
- Prefer the adjective form of a demonstrative with an explicit noun ("this
  function", "these parameters").
- Keep two sentences joined by "and" parallel in structure.

### Checklist

- [ ] Each connecting word links a sentence to the one that follows.
- [ ] Only approved connecting words and phrases are used.
- [ ] Demonstrative adjectives refer back to a clearly introduced topic.
- [ ] No mixed procedural and descriptive modes inside one connected pair.
- [ ] Connecting-word chains do not exceed three sentences.

### See also

Rule 1.1, Rule 1.3, Rule 1.11 (one term per concept), Rule 3.1, Rule 4.1.

---

## Rule 4.5 — Use an article or a demonstrative adjective before a noun

### Requirement

Articles ("the", "a", "an") and demonstrative adjectives ("this", "these") show
the position of nouns and multi-word nouns. Use them correctly. Do not remove
them to shorten the text.

- Do not use an article in a general statement or before an abstract concept:
  performance, scalability, error handling, concurrency, backward
  compatibility.
- In short sentences, use an article before each noun. This helps readers and
  machine translation.
- In a long series of items, use the article only before the first noun.
- Repeat the article in a series when an adjective applies to one item only.
- Do not use a definite article directly before a code identifier. A function
  name, a class name, a variable name, a file name, an environment variable, an
  error code, and a version tag are proper nouns.
- Keep the noun after a demonstrative adjective. Do not write "this" or "these"
  alone.

### Examples

Article in a short instruction:

> **Non-STE:** Call callback function. Pass response object to handler and set retry flag.
>
> **STE:** Call the callback function. Pass the response object to the handler. Then set the retry flag.

Article in an API reference sentence:

> **Non-STE:** Method reads configuration file and returns settings object.
>
> **STE:** The `load` method reads the configuration file and returns the settings object.

No article in a general statement:

> **Non-STE:** The error handling is important for the production applications. A function throws the error when the input is not valid.
>
> **STE:** Error handling is important for production applications. The function throws an error when the input is not valid.

> **Non-STE:** The backward compatibility is a requirement for the public API.
>
> **STE:** Backward compatibility is a requirement for the public API. The `v2` endpoints keep the response shape of the `v1` endpoints.

Article only before the first noun in a long series:

> **Non-STE:** Delete temporary files, log files, cache entries, and lock files before you start the build.
>
> **STE:** Delete the temporary files, log files, cache entries, and lock files before you start the build.

> **STE:** Close the database connection, file handle, socket, and worker pool in the shutdown hook.

Repeat the article when an adjective applies to one item only:

> **Non-STE:** Register the new event listeners, timers, subscriptions, and cleanup callbacks.
>
> **STE:** Register the new event listeners, the timers, the subscriptions, and the cleanup callbacks. (Only the event listeners are new.)

> **Non-STE:** The release includes the deprecated helper functions, adapters, and CLI flags.
>
> **STE:** The release includes the deprecated helper functions, the adapters, and the CLI flags. (Only the helper functions are deprecated.)

No definite article before an identifier:

> **Non-STE:** Call the function `validateInput` before you send the request.
>
> **STE:** Call function `validateInput` before you send the request.
>
> **STE (alternative):** Call the `validateInput` function before you send the request.

> **STE:** Configure module `AuthService` in the container.
>
> **STE:** Set variable `LOG_LEVEL` to `debug`.
>
> **STE:** Error `ERR_TIMEOUT_1042` shows in the console log.
>
> **STE:** Install version 3.2.1 of the package.

Demonstrative adjective for sentence linking:

> **Non-STE:** The function returns a configuration object. Configuration object has three fields: host, port, and timeout.
>
> **STE:** The function returns a configuration object. This object has three fields: `host`, `port`, and `timeout`.

> **Non-STE:** The middleware writes two headers to the response. They are used by the cache layer.
>
> **STE:** The middleware writes two headers to the response. These headers control the behavior of the cache layer.

Commit message and release note:

> **Non-STE:** Fix race condition in scheduler; worker pool now waits for queue drain.
>
> **STE:** Fix the race condition in the scheduler. The worker pool now waits for the queue to become empty.

> **STE:** Adds retry logic to the `HttpClient` class. Removes deprecated method `sendSync`.

Error message and test description:

> **Non-STE:** Input not valid: field must be string.
>
> **STE:** The input is not valid. The `name` field must be a string.

> **Non-STE:** Test verifies handler returns 404 when record missing.
>
> **STE:** The test checks that the handler returns the status code 404 when the record is not in the database.

### By paradigm

- Object-oriented (Java, C#, Python, TypeScript): use the article to separate a
  class from an instance. "The `ConnectionPool` class manages a pool of
  database connections. Each instance keeps a list of open connections." Use no
  article before a bare identifier: "Call `connect`."
- Functional (Haskell, Elixir, F#, Scala): separate a type constructor from a
  value. "The `Ok(value)` pattern shows a successful result. A `Result` value
  is either `Ok` or `Err`." Write "immutability" and "referential transparency"
  with no article.
- Procedural (C, Go, Bash): separate a pointer from the value at the address.
  "The function receives a pointer to a buffer. The buffer must hold at least
  512 bytes."
- Declarative (SQL, Terraform, YAML, Kubernetes): separate a resource type from
  a resource instance. "A `Deployment` resource manages a set of pods. The
  `web` deployment runs three replicas." Write no article before a named
  resource: "Apply manifest `web-deployment.yaml`."
- Systems (Rust, C memory, embedded): make ownership and lifetime clear. "The
  pointer must point to an initialized region of memory. A borrow of the value
  must not outlive the owner."

### Edge cases

- Identifier compared with concept: `ConnectionPool` alone takes no article.
  "The `ConnectionPool` class" takes "the" because "class" is the noun. "Call
  `initialize`" takes no article. "The `initialize` function" takes "the".
- "a" compared with "an": use "an" before a vowel sound (an SQL query, an HTML
  element, an XML parser, an ID, an API key). Use "a" before a consonant sound
  (a URL, a Unix system, a UUID, a JSON payload, a `User` record).
- Headings, titles, table cells, and UI labels may omit the article. The first
  sentence below the heading obeys the full rule.
- A product name that starts with "The", such as `TheMovieDB`, is a proper
  noun. The leading "The" is part of the identifier.
- Plural types in a general statement take no article: "Iterators are lazy in
  this library." One identifiable item takes "the": "The iterator stops at the
  end of the sequence."
- Do not add an article inside a code block, a command, or a log line. The rule
  applies to prose only.
- Choose the article for the spoken form of an acronym: "an API", not "a API".
- Uncountable technical nouns (memory, throughput, latency, state) take no
  indefinite article. Write "The function allocates memory."

### Grammar notes

- "A" refers to any instance of a type. "The" refers to one specific,
  identifiable item. No article refers to the type or the concept as a whole.
- Use "a" for the first mention and "the" for each later mention.
- A code identifier is a proper noun. "Call `connect`" is correct. "Call the
  `connect`" is not correct.
- Write "this object" or "these headers". Do not use "this" or "these" alone.
- Put the article before the full multi-word noun: "the retry policy object".
- A possessive form replaces the article. Write "its return value" or "the
  return value of the method". Do not write "the its return value."

### Checklist

- [ ] Articles and demonstrative adjectives are used correctly and are not removed to shorten the text.
- [ ] No article appears before a general statement or an abstract concept.
- [ ] Short sentences use an article before each noun.
- [ ] A long series uses the article only before the first noun, unless an adjective applies to one item only.
- [ ] No definite article appears directly before a code identifier.
- [ ] "a" and "an" match the spoken sound of the term that follows.
- [ ] Each demonstrative adjective is followed by a noun and refers to one clear topic.

### See also

Rule 1.1, Rule 1.5 (technical nouns), Rule 1.11, Rule 3.1, Rule 4.1, Rule 4.4.

---

## Section 4 — Combined checklist

- [ ] One topic or one instruction per sentence (4.1).
- [ ] No abstract claim without a value and a condition (4.1).
- [ ] Every sentence has its subject, verb, and articles; no contractions (4.2).
- [ ] Complex enumerations use a vertical list of one mode only (4.3).
- [ ] Related sentences are joined by an approved connecting word (4.4).
- [ ] Articles and demonstratives are correct, and identifiers take no definite article (4.5).
