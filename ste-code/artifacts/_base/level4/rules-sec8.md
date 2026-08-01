<!-- a-sec8-rule8.1.md -->

# Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon (;)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.1

> **Source:** [master.md#sec8-rule8.1](ste-code/grouped/)

## Original Rule

**Rule 8.1** You can use all standard English punctuation marks but not the semicolon (;).

The semicolon (;) is not permitted in STE because it lets you write very long sentences. It is also not easy to use correctly. As an alternative to the semicolon, always write two different sentences.

Examples:

| **Non-STE:** | (1) Examine the removed parts; replace the damaged ones. |

| **STE:** | (1) Examine the removed parts for damage. |

| | (2) Replace the damaged part(s). |

| **Non-STE:** | The battery is not user-replaceable; it can only be replaced by an approved service station. |

| **STE:** | Users cannot replace the battery. Only specialists at approved service stations can replace it. |

## STE-Code Adaptation

**Rule 8.1** In code documentation, you can use all standard English punctuation marks but not the semicolon (;).

The semicolon (;) is not permitted in STE-Code because it lets you write very long sentences that are difficult to read in code comments and documentation. It is also not easy to use correctly. As an alternative to the semicolon, always write two different sentences.

This rule applies to every form of code documentation: README files, API reference docs, docstrings, inline comments, commit messages, error messages, configuration comments, and specification documents. It does not apply to source code (where the semicolon is part of the language syntax) or to code shown inside code blocks. See Edge Case 1 for the full boundary.

### Examples

> *Adapted from spec pair:* Non-STE: `Examine the removed parts; replace the damaged ones.`  |  STE: `Examine the removed parts for damage. Replace the damaged part(s).` (ASD-STE100 Issue 9, Rule 8.1, page 103 — the semicolon joins two independent clauses; the fix splits them into two sentences.)

> **Non-STE:** Call the function to parse the response data; handle any errors that occur.

```python
def fetch_user(client, user_id):
    """Call the function to parse the response data; handle any errors that occur.

    Parameters:
        client: The HTTP client.
        user_id: The identifier of the user.

    Returns:
        A user record.
    """
    response = client.get(f"/users/{user_id}")
    data = json.loads(response.text)
    if "error" in data:
        raise UserError(data["error"])
    return data
```

> **STE:** Call the function to parse the response data. Handle any errors that occur.

```python
def fetch_user(client, user_id):
    """Call the function to parse the response data. Handle any errors that occur.

    Parameters:
        client: The HTTP client.
        user_id: The identifier of the user.

    Returns:
        A user record.
    """
    response = client.get(f"/users/{user_id}")
    data = json.loads(response.text)
    if "error" in data:
        raise UserError(data["error"])
    return data
```

> *Adapted from spec pair: "Examine the removed parts; replace the damaged ones." — the semicolon packs an action and its follow-up into one sentence. The STE version shows the same split applied to a fetch-and-parse function.*

> **Non-STE:** The cache is invalid after a write operation; you must flush it before the next read.

```go
// The cache is invalid after a write operation; you must flush it before the next read.
func (c *Cache) Write(key string, value []byte) error {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.store[key] = value
    return nil
}
```

> **STE:** The cache is invalid after a write operation. You must flush it before the next read.

```go
// The cache is invalid after a write operation. You must flush it before
// the next read.
func (c *Cache) Write(key string, value []byte) error {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.store[key] = value
    c.flush(key)
    return nil
}
```

> *Adapted from spec pair: "Examine the removed parts for damage." — the second clause states a required follow-up action. The STE version gives the cache behavior and the flush requirement as two sentences.*

> **See also:** Rule 1.1 — Use Approved Words; Rule 3.1 — Use Simple Sentences; Rule 4.1 — Keep Sentences Short; Rule 4.4 — Use Connecting Words and Connecting Phrases to Connect Sentences; Rule 8.2 — Use Hyphens to Connect Words That Are Directly Related

---

## Code-Domain Explanation

Rule 8.1 forbids the semicolon in all code documentation. The semicolon lets a writer pack two or more independent clauses into one sentence. In code documentation, this compression makes sentences hard to parse, especially for non-native English readers. The semicolon also has a different meaning in many programming languages (statement terminator in C, C++, Java, JavaScript, Rust, Go), which creates cognitive interference when the same symbol appears in documentation prose.

The fix is always the same: split the semicolon-separated sentence into two or more independent sentences. Each sentence stands alone with its own subject and verb. The reader processes one complete thought before moving to the next. This aligns with Rule 3.1 (use simple sentences) and Rule 4.1 (keep sentences short).

### README Files

README files describe project purpose, installation, usage, and contribution guidelines. Semicolons often appear when the writer tries to cram a feature description and its rationale into one sentence. The fix: write the feature description as one sentence. Write the rationale as a second sentence. Use a connecting word (Rule 4.4) if the relationship between the two sentences needs to be explicit.

Example of a semicolon violation in a README:

> **Non-STE:** The server supports WebSocket connections; these use a persistent channel instead of the standard request-response cycle.

> **STE:** The server supports WebSocket connections. These connections use a persistent channel instead of the standard request-response cycle.

A full README section that applies the rule:

```markdown
## Real-Time Updates

The server supports WebSocket connections. These connections use a
persistent channel instead of the standard request-response cycle.

Open a connection to `/ws` after the client signs in. The server
pushes an event when a record changes. Close the connection on sign-out
to free the channel.
```

### API Documentation

API documentation describes endpoints, parameters, request bodies, and response schemas. Semicolons often appear in endpoint descriptions that list two effects of a single operation. The fix: write the primary effect as one sentence. Write the secondary effect as a second sentence.

Example of a semicolon violation in API docs:

> **Non-STE:** POST /sessions creates a new session and returns a token; the token must be included in the Authorization header of subsequent requests.

> **STE:** A POST request to /sessions makes a new session and returns a token. You must include the token in the Authorization header of all later requests.

A full OpenAPI description block that applies the rule:

```yaml
/sessions:
  post:
    summary: Make a new session and return a token.
    description: >
      A POST request to /sessions makes a new session and returns a token.
      You must include the token in the Authorization header of all later
      requests.
    responses:
      '201':
        description: The session was created.
```

### Docstrings and Inline Comments

Docstrings describe what a function does, what parameters it accepts, and what it returns. Semicolons often appear when the writer lists two return conditions or two side effects. The fix: use a bullet list for multiple return conditions. Use separate sentences for multiple side effects. Inline comments rarely need semicolons because they should be one short sentence each.

Example of a semicolon violation in a docstring:

> **Non-STE:** Returns the user record if found; raises UserNotFoundError otherwise.

> **STE:** The function returns the user record when the user ID matches a database entry. The function raises a UserNotFoundError when the user ID does not match any entry.

A full docstring that applies the rule:

```python
def get_user(user_id: str) -> User:
    """Get the user record for the given identifier.

    The function returns the user record when the user ID matches a
    database entry. The function raises a UserNotFoundError when the
    user ID does not match any entry.

    Parameters:
        user_id: The identifier of the user.

    Returns:
        The matching user record.
    """
    record = db.query(User).filter_by(id=user_id).first()
    if record is None:
        raise UserNotFoundError(user_id)
    return record
```

### Commit Messages

Commit messages describe what changed and why. The subject line is one sentence (50 characters or fewer). The body is a series of short sentences. Semicolons in commit messages are almost always unnecessary — each sentence in the body should state one fact about the change. If you feel the need for a semicolon, you are likely combining two distinct facts. Split them.

Example of a semicolon violation in a commit message body:

> **Non-STE:** The cache layer now uses a TTL of 300 seconds; expired entries are evicted by a background thread rather than on access.

> **STE:** The cache layer now uses a TTL of 300 seconds. Expired entries are evicted by a background thread rather than on access.

A full commit message that applies the rule:

```text
Use a 300-second TTL for the cache

The cache layer now uses a TTL of 300 seconds. Expired entries are
evicted by a background thread rather than on access. This change
stops the handler thread from blocking on cache misses.
```

### Error Messages

Error messages tell the user what went wrong and what to do next. Semicolons often appear when the error condition and the recovery action are joined into one sentence. The fix: write the error condition as one sentence. Write the recovery action as a second sentence. Better yet, follow the error message pattern: "X is not valid. Do Y to fix this."

Example of a semicolon violation in an error message:

> **Non-STE:** Invalid port number; specify a value between 1024 and 65535.

> **STE:** The port number is not valid. Specify a value between 1024 and 65535.

A full error-string definition that applies the rule:

```python
def parse_port(value: str) -> int:
    port = int(value)
    if not 1024 <= port <= 65535:
        # The port number is not valid. Specify a value between
        # 1024 and 65535.
        raise ValueError(
            "The port number is not valid. "
            "Specify a value between 1024 and 65535."
        )
    return port
```

### Configuration Files

Configuration files use comments to explain each option. Semicolons often appear when the writer joins the purpose of an option with its trade-off in one sentence. The fix: write the purpose as one sentence. Write the trade-off as a second sentence. Keep each comment line short.

Example of a semicolon violation in a config comment:

> **Non-STE:** Set this to false for read-heavy workloads; the write path becomes slower but consistency guarantees improve under concurrent access.

> **STE:** Set this option to false for read-heavy workloads. The write path becomes slower with this setting. But the consistency guarantees improve when many clients access the data at the same time.

A full configuration block that applies the rule:

```yaml
# retry_on_conflict: set this option to true to retry a write when
# the record changed during the operation. The write path becomes
# slower with this setting. But the consistency guarantees improve
# when many clients access the data at the same time.
retry_on_conflict: true
```

### Test Documentation

Test files describe what each test checks and what failure means. Semicolons often appear when the writer joins the setup with the assertion in one sentence. The fix: write the setup as one sentence. Write the assertion as a second sentence.

Example of a semicolon violation in a test comment:

> **Non-STE:** This test creates a user with an empty name; the API must reject the request with a 400 status.

> **STE:** This test creates a user with an empty name. The API must reject the request with a 400 status.

A full test docstring that applies the rule:

```python
def test_reject_empty_name():
    """Check that the API rejects a user with an empty name.

    This test creates a user with an empty name. The API must reject
    the request with a 400 status.
    """
    response = client.post("/users", json={"name": ""})
    assert response.status_code == 400
```

---

## Paradigm-Specific Guidance

### Object-Oriented Paradigm (Java, C++, C#, Python classes)

Class documentation describes constructors, fields, methods, and invariants. Semicolons tend to appear in constructor documentation that describes both the initialization and the post-condition in one breath. In method docs, semicolons appear when the writer lists two return states (success value, exception) in one sentence.

Pattern: Write the constructor's initialization behavior as one sentence. Write the post-condition (the state of the object after construction) as a second sentence. For methods with multiple return states, use a bullet list or separate sentences. For getter/setter pairs, write each method's description as its own sentence — do not use a semicolon to chain the getter and setter together.

Example of a semicolon violation in a class docstring:

> **Non-STE:** The ConnectionPool constructor opens N connections to the database; the pool is immediately ready for use after construction.

> **STE:** The ConnectionPool constructor opens N connections to the database. The pool is ready for use immediately after the constructor returns.

A full class docstring that applies the rule:

```python
class ConnectionPool:
    """Manage a set of reusable database connections.

    The ConnectionPool constructor opens N connections to the database.
    The pool is ready for use immediately after the constructor returns.

    The get_connection method returns a free connection from the pool.
    The release_connection method returns a used connection to the pool.
    """

    def __init__(self, size: int):
        self._pool = [connect() for _ in range(size)]

    def get_connection(self):
        return self._pool.pop()

    def release_connection(self, conn):
        self._pool.append(conn)
```

### Functional Paradigm (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, their inputs, their outputs, and their composition. Semicolons often appear in function docstrings that describe both the happy path and the error path in one sentence, or that chain multiple transformation steps.

Pattern: Describe the happy-path transformation as one sentence. Describe the error path as a second sentence, introduced with a connecting word like "but" or "thus." For composed pipelines, write each transformation step as a separate sentence. The pipe operator (`|>` in Elixir, `>>` in F#, `.` in Haskell) already provides visual composition — do not reinforce it with a semicolon in prose.

Example of a semicolon violation in a Rust docstring:

> **Non-STE:** Parses the input string into a Config struct; returns an Err if any field fails validation.

> **STE:** This function parses the input string into a Config struct. The function returns an Err value when a field does not pass validation.

A full Rust doc comment that applies the rule:

```rust
/// Parse a configuration string.
///
/// This function parses the input string into a Config struct.
/// The function returns an Err value when a field does not pass
/// validation.
///
/// # Examples
/// ```
/// let cfg = parse_config("port = 8080");
/// assert!(cfg.is_ok());
/// ```
pub fn parse_config(src: &str) -> Result<Config, ConfigError> {
    // ...
}
```

### Procedural Paradigm (C, Go, Bash)

Procedural documentation describes sequences of steps: allocate, initialize, process, clean up. Semicolons often appear when the writer chains two sequential steps into one sentence. This is particularly tempting in C where the semicolon is the statement terminator — the writer unconsciously carries the punctuation habit from code into prose.

Pattern: Write each procedural step as its own sentence. If the steps form a tight sequence, use the connecting word "then" (Rule 4.4) at the start of the second sentence. Do not use a semicolon to compress the sequence into one sentence. For error-handling steps (check return code, handle error), write the check as one sentence and the handler as a second.

Example of a semicolon violation in a Go function comment:

> **Non-STE:** InitBuffer allocates a 4KB memory block; it fills the block with zeros before returning the pointer.

> **STE:** The InitBuffer function allocates a 4 KB memory block. Then it fills the block with zeros. The function returns the pointer after the block is filled.

A full Go comment block that applies the rule:

```go
// InitBuffer makes a new buffer for raw I/O.
//
// The InitBuffer function allocates a 4 KB memory block. Then it fills
// the block with zeros. The function returns the pointer after the
// block is filled. Call FreeBuffer to release the memory when you
// finish with the buffer.
func InitBuffer() *Buffer {
    block := make([]byte, 4096)
    for i := range block {
        block[i] = 0
    }
    return &Buffer{data: block}
}
```

### Declarative Paradigm (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes resources, their desired state, and their dependencies. Semicolons often appear in resource descriptions that list two properties or two effects in one sentence.

Pattern: Write each resource property as its own sentence. Write each effect of the resource declaration as its own sentence. Use connecting words ("thus," "as a result") to link the property to its effect. For multi-field resource specs, use a table or bullet list instead of a semicolon-separated prose list.

Example of a semicolon violation in a Terraform variable description:

> **Non-STE:** The instance_type variable sets the EC2 instance size; valid values include t3.micro, t3.small, and t3.medium.

> **STE:** The instance_type variable sets the EC2 instance size. Valid values include t3.micro, t3.small, and t3.medium.

A full Terraform comment block that applies the rule:

```hcl
# The instance_type variable selects the EC2 instance size.
# Valid values include t3.micro, t3.small, and t3.medium.
# The default is t3.small.
variable "instance_type" {
  type    = string
  default = "t3.small"
}
```

### Systems Paradigm (Rust ownership docs, C memory docs)

Systems documentation describes ownership, lifetimes, memory layouts, and safety guarantees. Semicolons often appear when the writer describes a rule and its consequence in one sentence. This is dangerous in safety-critical documentation — the reader might miss the consequence because it is buried in a compound sentence.

Pattern: Write the ownership or memory rule as one sentence. Write the consequence of violating the rule as a second sentence, introduced with "thus" or "as a result." For Undefined Behavior documentation, never use a semicolon — the consequence must be a standalone sentence that cannot be missed.

Example of a semicolon violation in a Rust safety doc:

> **Non-STE:** The caller must ensure the pointer is non-null and aligned; undefined behavior occurs if either condition is violated.

> **STE:** The caller must make sure that the pointer is not null. The caller must also make sure that the pointer is aligned. Undefined Behavior occurs if either condition is not met.

A full Rust safety comment that applies the rule:

```rust
/// Read a value from a raw pointer.
///
/// # Safety
///
/// The caller must make sure that the pointer is not null. The caller
/// must also make sure that the pointer is aligned. Undefined Behavior
/// occurs if either condition is not met.
///
/// The caller must make sure that the pointer points to valid,
/// initialized memory. The memory must not be mutated by another
/// thread during the read.
pub unsafe fn read_value(ptr: *const u32) -> u32 {
    *ptr
}
```

---

## Extended Examples

### Example 3 — API Endpoint: Two effects of a mutation

> **Non-STE:** PATCH /config updates the runtime settings and writes the new values to disk immediately; a restart is not required for the changes to take effect.

```yaml
/config:
  patch:
    summary: Update runtime settings.
    description: >
      PATCH /config updates the runtime settings and writes the new
      values to disk immediately; a restart is not required for the
      changes to take effect.
```

> **STE:** A PATCH request to /config updates the runtime settings and writes the new values to disk. A restart is not necessary for the changes to take effect.

```yaml
/config:
  patch:
    summary: Update runtime settings.
    description: >
      A PATCH request to /config updates the runtime settings and
      writes the new values to disk. A restart is not necessary for
      the changes to take effect.
```

> *Principles applied: P1 (split semicolon into two sentences), Rule 4.1 (each sentence under 25 words). The first sentence describes the operation. The second sentence states the operational benefit. The reader gets two complete, independent thoughts.*

### Example 4 — Docstring: Multiple return conditions

> **Non-STE:** Returns the parsed configuration as a dict if the file is valid YAML; returns an empty dict if the file is empty; raises ConfigError if the file contains invalid syntax.

```python
def load_config(path: str) -> dict:
    """Returns the parsed configuration as a dict if the file is valid YAML;
    returns an empty dict if the file is empty; raises ConfigError if the
    file contains invalid syntax."""
    ...
```

> **STE:** The function returns the parsed configuration as a dict when the file is valid YAML. The function returns an empty dict when the file is empty. The function raises a ConfigError when the file contains incorrect syntax.

```python
def load_config(path: str) -> dict:
    """Load configuration data from a YAML file.

    The function returns the parsed configuration as a dict when the
    file is valid YAML. The function returns an empty dict when the
    file is empty. The function raises a ConfigError when the file
    contains incorrect syntax.

    Parameters:
        path: The path to the configuration file.

    Returns:
        The parsed configuration as a dict.
    """
    ...
```

> *Principles applied: P1 (split semicolon chain into three sentences), Rule 3.1 (each sentence is a simple subject-verb-object clause). The original had three independent clauses joined by two semicolons. Each clause now stands alone with a repeated subject ("The function") for clarity.*

### Example 5 — Commit Message: Two independent facts

> **Non-STE:** The authentication middleware now checks token expiry before decoding; expired tokens return a 401 before reaching the route handler.

```text
auth: check token expiry first

The authentication middleware now checks token expiry before decoding;
expired tokens return a 401 before reaching the route handler.
```

> **STE:** The authentication middleware now checks token expiry before decoding. Expired tokens return a 401 status code before they reach the route handler.

```text
auth: check token expiry first

The authentication middleware now checks token expiry before decoding.
Expired tokens return a 401 status code before they reach the route
handler.
```

> *Principles applied: P1 (split semicolon), Rule 3.1 (simple sentences). The first sentence states the behavioral change. The second sentence states the user-visible effect. Each fact is independently verifiable in the diff.*

### Example 6 — Error Message: Condition and recovery

> **Non-STE:** Database connection timed out after 30 seconds; check that the DB_HOST environment variable is set correctly and the server is reachable.

```python
raise ConnectionError(
    "Database connection timed out after 30 seconds; check that the "
    "DB_HOST environment variable is set correctly and the server is "
    "reachable."
)
```

> **STE:** The database connection timed out after 30 seconds. Check that the DB_HOST environment variable is set correctly. Make sure that the server is reachable.

```python
raise ConnectionError(
    "The database connection timed out after 30 seconds. "
    "Check that the DB_HOST environment variable is set correctly. "
    "Make sure that the server is reachable."
)
```

> *Principles applied: P1 (split semicolon), Rule 6.1 (imperative mood for recovery action). The error condition is one sentence. The two recovery checks are two imperative sentences. The user reads the problem, then executes the fixes one at a time.*

### Example 7 — README: Feature and constraint

> **Non-STE:** The plugin system supports hot-reloading during development; production builds load plugins at startup only and cannot reload them without a restart.

```markdown
## Plugins

The plugin system supports hot-reloading during development; production
builds load plugins at startup only and cannot reload them without a
restart.
```

> **STE:** The plugin system supports hot-reloading during development. Production builds load plugins at startup only. These builds cannot reload plugins without a restart.

```markdown
## Plugins

The plugin system supports hot-reloading during development. Production
builds load plugins at startup only. These builds cannot reload
plugins without a restart.
```

> *Principles applied: P1 (split semicolon), P1 (demonstrative adjective "these"), Rule 4.4 (connecting words). The original had a semicolon and an "and" inside the second clause. The fix splits into three clean sentences with a demonstrative adjective linking the last two.*

### Example 8 — Configuration File Comment: Option and trade-off

> **Non-STE:** Set this to false for read-heavy workloads; the write path becomes slower but consistency guarantees improve under concurrent access.

```yaml
# read_optimized: set this to false for read-heavy workloads; the
# write path becomes slower but consistency guarantees improve under
# concurrent access.
read_optimized: false
```

> **STE:** Set this option to false for read-heavy workloads. The write path becomes slower with this setting. But the consistency guarantees improve when many clients access the data at the same time.

```yaml
# read_optimized: set this option to false for read-heavy workloads.
# The write path becomes slower with this setting. But the consistency
# guarantees improve when many clients access the data at the same
# time.
read_optimized: false
```

> *Principles applied: P1 (split semicolon), P1 (connecting word "but"), Rule 4.4. The first sentence gives the instruction. The second states the cost. The third states the benefit. The trade-off is explicit and the reader weighs both sides independently.*

### Example 9 — Inline Comment: Two sequential steps

> **Non-STE:** Acquire the lock then read the shared counter; release the lock after you record the value.

```go
// Acquire the lock then read the shared counter; release the lock
// after you record the value.
mu.Lock()
count := sharedCounter
mu.Unlock()
log.Printf("count=%d", count)
```

> **STE:** Acquire the lock. Then read the shared counter. Release the lock after you record the value.

```go
// Acquire the lock. Then read the shared counter. Release the lock
// after you record the value.
mu.Lock()
count := sharedCounter
mu.Unlock()
log.Printf("count=%d", count)
```

> *Principles applied: P1 (split semicolon), Rule 4.4 (connecting word "then"). The two steps become three short sentences. Each step is a clear, separate instruction.*

### Example 10 — Pull Request Description: Two linked claims

> **Non-STE:** This change removes the global singleton; all callers must now pass a Logger instance to the constructor.

```markdown
## Summary

This change removes the global singleton; all callers must now pass a
Logger instance to the constructor.
```

> **STE:** This change removes the global singleton. All callers must now pass a Logger instance to the constructor.

```markdown
## Summary

This change removes the global singleton. All callers must now pass a
Logger instance to the constructor.

## Migration

Update each `new Service()` call to `new Service(logger)`.
```

> *Principles applied: P1 (split semicolon). The removal and the caller requirement are two separate facts. The STE version splits them and adds a Migration section so each fact gets its own space.*

---

## Edge Cases

### Edge Case 1 — Semicolons Inside Code Blocks

Code blocks (fenced with triple backticks or indented by four spaces) contain source code, not documentation prose. Semicolons inside code blocks are part of the programming language syntax — they are not subject to Rule 8.1. This rule applies only to the prose that surrounds and explains the code.

Guidance: Do not remove semicolons from code examples to comply with Rule 8.1. The rule governs documentation text, not the code being documented. A JavaScript example that shows `const x = 5;` is correct and must keep its semicolon. The prose that describes the example ("This statement declares a constant named x.") must not use semicolons.

> **NOTE:** When you show a code snippet inline with backticks (`const x = 5;`), the semicolon inside the backticks is permitted. The backtick boundary separates code tokens from prose tokens.

Example of the correct boundary:

```javascript
// This function declares a constant and returns its doubled value.
// The semicolons below are JavaScript syntax, not documentation prose.
function doubleValue(x) {
  const result = x * 2;
  return result;
}
```

The comment lines above use no semicolons. The `const result = x * 2;` line keeps its semicolon because it is code.

### Edge Case 2 — Semicolons in Generated Documentation

Auto-generated documentation (OpenAPI spec descriptions, protobuf source comments, JSDoc output, Javadoc output) may contain semicolons inserted by the generator. These are not under the writer's control.

Guidance: When you write the source comments that feed into the generator (JSDoc `@param` tags, protobuf `//` comments, OpenAPI `description` fields), apply Rule 8.1. When the generator splices your comments together with semicolons in the rendered output, that is a generator behavior issue — not a violation you must fix. File an issue with the generator project to request semicolon-free output.

> **NOTE:** For documentation that you author directly (README files, hand-written API docs, commit messages), Rule 8.1 applies in full. The generator exemption applies only to machine-composed output that you cannot control.

Example of a source comment that you control:

```python
def send_email(to: str, subject: str) -> bool:
    """Send an email to the given address. Return true when the send succeeds.

    Parameters:
        to: The recipient address.
        subject: The email subject.

    Returns:
        True when the email was sent. False when the send failed.
    """
```

Write the source comment with periods only. If the generator joins these lines with a semicolon in the rendered page, that is a generator defect.

### Edge Case 3 — When a Semicolon Appears Inside a Quoted String

Documentation sometimes quotes error messages, log output, or terminal text that contains semicolons. A quoted string is not your prose — it is the thing being quoted. Do not modify the content of quoted strings to remove semicolons.

Guidance: Keep the semicolon inside the quoted material. Use quotation marks or a code block to delimit the quoted text. The surrounding prose must obey Rule 8.1. The quoted material is exempt.

> **STE:** The compiler shows the error message: "missing semicolon at line 42; expected ';' after expression." Add a semicolon at the end of line 42 to fix this error.

> *The semicolons inside the quoted error message are preserved. The prose that explains the fix ("Add a semicolon...") uses no semicolons. The reader can see the exact compiler output while the documentation prose remains compliant.*

### Edge Case 4 — Lists That Look Like Semicolon-Separated Clauses

Some writers use a semicolon as a list separator for complex list items (items that contain internal commas). This is standard English punctuation for "super-commas." For example: "The function accepts three parameters: the input string, which must be UTF-8; the output format, which can be 'json' or 'xml'; and a callback, which is optional."

Guidance: In STE-Code, do not use semicolons as super-commas in lists. Instead, structure the list as a bullet list or a table. Each list item becomes a separate line with its own sentence or phrase. This removes the need for semicolons entirely and improves readability.

> **Non-STE:** The endpoint accepts three query parameters: `sort`, which sets the sort field; `order`, which must be "asc" or "desc"; and `limit`, which caps the result count.

> **STE:** The endpoint accepts three query parameters:
> - `sort` — Sets the sort field.
> - `order` — Must be "asc" or "desc."
> - `limit` — Caps the result count.

> *Principles applied: P1 (no semicolons), Rule 3.3 (use lists for complex items). The bullet list replaces the super-comma structure. Each parameter gets its own line with a clear description.*

A full parameter table that applies the rule:

| Parameter | Type | Description |
|-----------|------|-------------|
| `sort` | string | Sets the sort field. |
| `order` | string | Must be "asc" or "desc." |
| `limit` | integer | Caps the result count. The default is 20. |

### Edge Case 5 — Semicolons in Chat and Informal Communication

Some development teams use semicolons in chat messages, code review comments, and informal wiki pages as a stylistic convention. This is not code documentation in the STE-Code sense — it is informal communication.

Guidance: Rule 8.1 applies to formal code documentation: README files, API reference docs, docstrings, commit messages, error messages, and specification documents. It does not apply to chat messages, pull request discussions, or informal team communication. Use your judgment: if the text will be read by users outside your team or will persist in the repository for more than one release cycle, apply Rule 8.1. If it is a transient message in a pull request thread, the rule is optional.

> **NOTE:** This edge case does not create a loophole for commit messages. Commit messages are permanent repository history and must follow Rule 8.1. The exemption applies only to ephemeral communication channels like chat and code review comments.

### Edge Case 6 — Semicolon Inside a Regular Expression or Data String

Some documentation shows a regular expression, a CSV row, or a data format that uses a semicolon as a delimiter. The semicolon is part of the data, not the prose.

Guidance: Keep the semicolon inside the code span or code block that holds the data. The prose that explains the pattern must not use semicolons.

> **STE:** The parser splits each row on the `;` character. Put one field between each pair of semicolons. Use a quoted field when the value contains a semicolon.

The three code spans above (`;`, `;`, and `;`) hold data delimiters. The surrounding sentences use periods only.

---

## Cross-References

- **Rule 1.1 — Use Approved Words:** The words you use to connect split sentences (and, but, thus, then) must come from the STE-Code approved dictionary. Do not invent new connecting words to replace semicolons.
- **Rule 1.3 — Use Words Only with Their Approved Meanings:** When you split a semicolon sentence into two, make sure each connecting word you add carries its approved meaning. Do not use "thus" to mean "and" or "but" to mean "then."
- **Rule 3.1 — Use Simple Sentences:** The fix for a semicolon violation is always to write two or more simple sentences. If either resulting sentence is complex, simplify it further.
- **Rule 3.3 — Use Lists for Complex Items:** When a semicolon serves as a super-comma in a list, replace the list with bullets or a table (see Edge Case 4).
- **Rule 4.1 — Keep Sentences Short:** Semicolons let you evade the 20-word (procedural) and 25-word (descriptive) sentence length limits. Removing semicolons and splitting sentences makes length compliance verifiable.
- **Rule 4.4 — Use Connecting Words and Connecting Phrases to Connect Sentences:** After splitting a semicolon sentence, use a connecting word or phrase to show the logical relationship between the two new sentences. The connecting word replaces the semicolon and adds semantic clarity.
- **Rule 6.3 — Write Short Sentences (Maximum 25 Words):** Short sentences make the split from a semicolon easy to verify by word count.
- **Rule 8.2 — Use Hyphens to Connect Words That Are Directly Related:** Hyphens connect words. Semicolons connect clauses. Do not confuse these two punctuation marks. If you are connecting words, use a hyphen. If you are connecting clauses, split into two sentences.
- **STE-Code Dictionary — Section: Punctuation:** The dictionary defines all approved punctuation marks and their usage constraints. Consult it for the full list of permitted punctuation and the rules for each mark.

---

## Grammar Notes

### The Semicolon as a Clause Joiner

In standard English grammar, the semicolon joins two independent clauses that are closely related in meaning. The clauses must each be able to stand as a complete sentence. This grammatical requirement means that a semicolon sentence always contains two complete subject-verb structures — effectively two sentences compressed into one.

STE-Code rejects this compression on cognitive grounds. A reader must parse the first clause, hold it in working memory, parse the second clause, and then integrate the relationship between them. For non-native English readers — the majority audience of most open-source documentation — this two-clause parsing is measurably harder than processing two separate sentences. The period between sentences gives the reader a full cognitive break. The semicolon denies that break.

### The Semicolon as a Super-Comma

In standard English, semicolons also serve as "super-commas" — stronger separators than commas, used in lists where the list items themselves contain commas. For example: "The team includes Alice, the architect; Bob, the lead developer; and Carol, the designer."

STE-Code does not permit this usage. The super-comma forces the reader to maintain a stack of nesting levels: list items separated by semicolons, sub-items separated by commas. This nested structure violates Rule 3.1 (simple sentences) and the two-level nesting limit. The fix is to restructure the list using bullets, dashes, or a table — formats that make the nesting visually explicit rather than encoding it in punctuation.

### Programming Language Interference

Many programming languages use the semicolon as a statement terminator (C, C++, Java, JavaScript, Rust, Go, and others). Developers who write documentation for these languages have deeply ingrained muscle memory for the semicolon. They read and write semicolons thousands of times per day in code. When switching to documentation prose, this muscle memory can cause unconscious semicolon insertion — the writer types a semicolon out of habit, not because the sentence needs one.

This cognitive interference is unique to code documentation. A technical writer who documents a language that uses the semicolon as a statement terminator types semicolons thousands of times per day in source files. When that writer switches to documentation prose, the habit can cause unconscious semicolon insertion. Rule 8.1 is therefore more important — and harder to obey — in code documentation than in general-purpose prose. Review your documentation prose separately from your code. Look specifically for semicolons that belong in code but not in prose.

### The Period as the Only Sentence Boundary

STE-Code recognizes exactly three sentence-ending punctuation marks: the period (.), the question mark (?), and the exclamation mark (!). The semicolon, colon (when used between clauses), and em-dash (when used to separate clauses) are not sentence boundaries. This means a text that uses semicolons cannot be mechanically checked for sentence length (Rule 4.1) because the tool does not know where one sentence ends and the next begins.

When every sentence boundary is a period, automated rule checkers can reliably count words per sentence. This mechanical verifiability is a deliberate design goal of STE-Code: a tool should be able to validate compliance without understanding the semantics. Semicolons break this property by hiding sentence boundaries inside a single punctuation-delimited string.

### Semicolon Avoidance in Technical Writing Traditions

The prohibition on semicolons is not unique to STE. Several major technical style guides discourage or limit semicolons in technical prose. The Microsoft Writing Style Guide recommends avoiding semicolons in technical content. The Google Developer Documentation Style Guide advises writers to "prefer shorter sentences" over semicolon-joined clauses. The Chicago Manual of Style permits semicolons but notes they are "not common in technical writing."

STE-Code takes the strongest position: a complete ban. This is consistent with the STE philosophy that documentation must be understandable by non-native English speakers under operational pressure. A developer debugging a production incident at 3:00 AM should not have to parse a semicolon-joined sentence to find the recovery procedure. Each sentence must deliver one complete, actionable thought with no internal clause boundaries.

---

<!-- a-sec8-rule8.2.md -->

# Rule 8.2 — Use Hyphens (-) to Connect Words That Are Directly Related

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.2

> **Source:** [master.md#sec8-rule8.2](ste-code/grouped/)

## Original Rule

**Rule 8.2** Use hyphens (-) to connect words that are directly related.

A hyphen (-) is a punctuation mark that connects words or parts of words. Use the hyphen for technical nouns to show that two or more words are directly related. This construction helps the reader to understand words and phrases more easily.

The examples that follow show how to use hyphens to connect words that are directly related.

1. Terms that have two or more words and are adjectives before a noun:

   low-altitude flight, high-pressure chamber, air-conditioned compartment, transmitter-receiver system, quick-release fastener, clamshell-type flap, eighteen-inch monitor, cast-aluminum bracket, three-to-one ratio, trial-and-error method, air-to-air refueling, soap-and-water solution, up-to-date information, run-on torque, break-away torque, cut-in speed, in-flight entertainment system, stiff-bristled brush, fire-resistant material, self-sealing hose

2. Two-word fractions or numbers:

   forty-seven, ninety-ninth, one hundred and sixty-two, three-sixteenths, one thirty-second

3. Terms that contain an uppercase letter plus a noun, or a number plus a noun, and that usually give the shape or configuration of something:

   L-shaped bracket, O-ring, T-shirt, U-beam, Y-coupling, V-band clamp, 3-prong connector, 180-grit abrasive cloth

4. Verbs that contain a noun or a different part of speech as the first part:

   die-cast, arc-weld, fusion-bond, stop-drill, vacuum-pack, heat-treat, jump-start, air-condition, short-circuit, fast-forward, cold-roll, dry-clean, blow-dry

5. Terms in which the end of the prefix is a vowel, and the root word starts with a vowel:

   pre-amplifier, de-icing, anti-icing, pre-engage

A hyphen is different from a dash, which divides ideas, shows a range, or gives a signal for a pause. A dash is usually longer than a hyphen, but it is at times shown as a hyphen with a space on each side.

## STE-Code Adaptation

**Rule 8.2** In code documentation, use hyphens (-) to connect words that are directly related.

A hyphen (-) is a punctuation mark that connects words or parts of words. Use the hyphen for code-domain technical nouns to show that two or more words are directly related. This construction helps the reader to understand words and phrases more easily in code comments, API documentation, README files, commit messages, and error strings.

The same five categories of hyphenation apply to code documentation:

1. Terms that have two or more words and are adjectives before a noun:

   high-priority task, read-only file, thread-safe method, event-driven architecture, type-safe interface, run-time error, end-to-end test, point-to-point connection, server-side rendering, client-side validation, just-in-time compilation, fire-and-forget pattern

2. Two-word fractions or numbers in code documentation:

   seventy-two, one hundred and twenty-eight, three-fourths, forty-seven, one hundred and sixty-two

3. Terms that contain an uppercase letter plus a noun, or a number plus a noun, and that usually give the shape or configuration of something:

   L-shaped bracket, T-shaped connector, 64-bit register, 8-byte alignment, 128-bit value, 3-prong connector

4. Verbs that contain a noun or a different part of speech as the first part:

   dry-run, hot-reload, cold-start, hard-code, soft-delete, short-circuit

5. Terms in which the end of the prefix is a vowel, and the root word starts with a vowel:

   pre-initialized, re-entrant, de-allocated, anti-aliasing, re-indexed

A hyphen is different from a dash, which divides ideas, shows a range (for example, "lines 12-48"), or gives a signal for a pause. A dash is usually longer than a hyphen. In code documentation, keep the two distinct: the hyphen joins words into one concept, the dash separates ideas.

### Examples

> *Adapted from spec pair:* Non-STE: "low-altitude flight, high-pressure chamber, air-conditioned compartment, self-sealing hose" (ASD-STE100 Issue 9, Rule 8.2, category 1) | STE: "high-priority task, read-only file, thread-safe method, self-contained module" (STE-Code Rule 8.2, category 1)

> **Non-STE:**
> ```
> // The high priority task must acquire the write lock before it can modify the
> // shared data structure.
> void processQueue(SharedMap& map, const Entry& entry) {
>     std::unique_lock lock(map.write_lock);
>     map.modify(entry);
> }
> ```
>
> **STE:**
> ```
> // The high-priority task must get the write lock before it can change the
> // shared data structure.
> void processQueue(SharedMap& map, const Entry& entry) {
>     std::unique_lock lock(map.write_lock);
>     map.change(entry);
> }
> ```
>
> *Principles applied: P1, P2, P3. "High-priority" is a compound adjective before the noun "task." Added the hyphen to show the direct relationship. Replaced "acquire" with "get" and "modify" with "change" per STE-Code vocabulary (prefer short approved verbs over utilize/leverage-style wording).*

> **Non-STE:**
> ```
> /**
>  * Opens the config file for parsing.
>  * @param fd  A read only file descriptor to open the configuration for parsing.
>  * @return    0 on success, -1 on error.
>  */
> int openConfig(int fd);
> ```
>
> **STE:**
> ```
> /**
>  * Opens the config file for parsing.
>  * @param fd  A read-only file descriptor to open the configuration for parsing.
>  * @return    0 on success, -1 on error.
>  */
> int openConfig(int fd);
> ```
>
> *Principles applied: P1, P2. "Read-only" is a compound adjective before the noun "file descriptor." The hyphen connects the words and prevents ambiguity about what "only" modifies: without it, "read only file descriptor" can be read as a file descriptor that only "reads" rather than one that is read-only.*

## Code-Domain Explanation

Rule 8.2 applies differently across code documentation formats. The hyphen signals to the reader that two or more words function as a single concept. In code documentation, missing hyphens cause ambiguity about which word modifies which. This section explains how the rule applies to each documentation type.

### README Files

README files introduce a project to new users. Compound adjectives in README files describe the project's qualities, requirements, and behavior. Use hyphens consistently to make these descriptions immediately clear.

Common README patterns that need hyphens:

- **Quality descriptors:** production-ready, enterprise-grade, battle-tested, well-documented
- **Installation prerequisites:** pre-installed dependencies, system-level packages, network-accessible registry
- **Feature descriptions:** auto-generated documentation, multi-threaded execution, cross-platform support
- **Configuration flags:** opt-in feature, opt-out behavior, on-by-default setting

NOTE: A README section title such as "Getting Started" is a gerund phrase, not a compound adjective. Do not hyphenate it.

> **Non-STE:** "Our framework is battle tested and ready for production. It supports cross platform and is well documented."
>
> **STE:** "Our framework is battle-tested and production-ready. It supports cross-platform builds and is well-documented."
>
> *Principles applied: P1, P2. Each quality descriptor is a compound adjective before an implied or stated noun. The hyphens make the README parse on first read.*

### API Documentation

API documentation describes function signatures, parameters, return types, and behavior contracts. Hyphens prevent ambiguity in parameter descriptions and return-value qualifiers.

Common API patterns that need hyphens:

- **Parameter constraints:** non-negative integer, null-terminated string, zero-based index
- **Return value descriptors:** read-only reference, copy-on-write handle, reference-counted pointer
- **State qualifiers:** thread-safe access, re-entrant call, idempotent operation
- **Behavior modifiers:** fail-fast strategy, best-effort delivery, least-recently-used eviction

Example: A parameter documented as "a read only reference" is ambiguous. "Read-only reference" makes clear that the reference itself is read-only, not that it references read-only data (though it may also do that).

> **Non-STE:**
> ```
> /**
>  * @param count  A non negative integer that sets the buffer size.
>  * @return       A read only reference to the internal cache.
>  */
> const Cache& resize(size_t count);
> ```
>
> **STE:**
> ```
> /**
>  * @param count  A non-negative integer that sets the buffer size.
>  * @return       A read-only reference to the internal cache.
>  */
> const Cache& resize(size_t count);
> ```
>
> *Principles applied: P1, P2. "Non-negative" and "read-only" are compound adjectives before "integer" and "reference." The hyphens bind the words so the reader parses one concept, not two separate modifiers.*

### Docstrings

Docstrings live inside source code and describe what a function, class, or module does. Hyphens in docstrings keep descriptions compact and unambiguous.

Common docstring patterns that need hyphens:

- **Preconditions:** The input must be a well-formed JSON string. The buffer must be null-terminated.
- **Postconditions:** Returns a deep-copied instance. The output is a newline-delimited list.
- **Side effects:** This method is not thread-safe. The operation is non-blocking.
- **Complexity:** Average-case O(n log n). Worst-case O(n squared).

> **Non-STE:**
> ```
> def parse(text: str) -> list[str]:
>     """Parse the input.
>
>     Precondition: the input must be a well formed JSON string.
>     The buffer must be null terminated.
>     """
> ```
>
> **STE:**
> ```
> def parse(text: str) -> list[str]:
>     """Parse the input.
>
>     Precondition: the input must be a well-formed JSON string.
>     The buffer must be null-terminated.
>     """
> ```
>
> *Principles applied: P1, P2. "Well-formed" and "null-terminated" are compound adjectives before "JSON string" and "buffer." The hyphens mark each pair as a single qualifier.*

### Commit Messages

Commit messages are brief and benefit from hyphenated compounds that pack meaning into few words. Use hyphens to make commit subjects self-contained.

| Non-STE commit subject | STE commit subject |
|------------------------|---------------------|
| Fix race condition in thread safe cache | Fix race condition in thread-safe cache |
| Add end to end test for auth flow | Add end-to-end test for auth flow |
| Implement just in time compilation pass | Implement just-in-time compilation pass |
| Handle null terminated input in parser | Handle null-terminated input in parser |

> **Non-STE:** `git commit -m "Add end to end test for auth flow"`
>
> **STE:** `git commit -m "Add end-to-end test for auth flow"`
>
> *Principles applied: P1, P2. "End-to-end" is a three-word compound adjective before "test." A reviewer scanning the log reads it as one concept.*

### Error Messages

Error messages must be precise. A missing hyphen can make an error message confusing at exactly the moment the user needs clarity.

| Non-STE error message | STE error message |
|-----------------------|-------------------|
| Cannot open read only file | Cannot open read-only file |
| Expected non negative integer | Expected non-negative integer |
| Thread safe violation detected | Thread-safe violation detected |
| Buffer must be null terminated | Buffer must be null-terminated |

> **Non-STE:** `raise ValueError("Expected non negative integer for port number")`
>
> **STE:** `raise ValueError("Expected non-negative integer for port number")`
>
> *Principles applied: P1, P2. "Non-negative" is a compound adjective before "integer." The hyphen shows the negation applies to the whole word, not to "negative" alone.*

## Paradigm-Specific Guidance

Hyphenation conventions vary by programming paradigm because each paradigm introduces its own set of compound technical terms. Apply Rule 8.2 consistently within each paradigm's vocabulary.

### Object-Oriented (Java, C++, C#, Python classes)

Object-oriented code uses compound adjectives to describe class properties, method contracts, and design patterns.

**Key compound terms:**

- **Access and visibility:** read-only property, write-only field, package-private class, file-private extension
- **Initialization:** lazy-initialized singleton, eagerly-loaded dependency, constructor-injected service, setter-injected component
- **Design patterns:** factory-created instance, decorator-wrapped object, observer-registered handler, visitor-traversed tree
- **Threading:** thread-safe collection, lock-free algorithm, wait-free data structure, single-threaded context
- **Lifecycle:** reference-counted pointer, garbage-collected object, stack-allocated buffer, heap-allocated array

> **Non-STE:**
> ```
> // The thread safe singleton uses lazy initialization to defer object creation
> // until the first access.
> class CacheManager {
> public:
>     static CacheManager& instance();
> };
> ```
>
> **STE:**
> ```
> // The thread-safe singleton uses lazy initialization to defer object creation
> // until the first access.
> class CacheManager {
> public:
>     static CacheManager& instance();
> };
> ```
>
> *Principles applied: P1, P2. "Thread-safe" is a compound adjective before "singleton." The hyphen removes ambiguity: without it, "thread safe singleton" can be read as "thread" modifying "safe singleton."*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional programming emphasizes purity, immutability, and higher-order abstractions. Compound adjectives describe these properties.

**Key compound terms:**

- **Purity and side effects:** pure-function semantics, side-effect-free computation, referentially-transparent expression
- **Function types:** higher-order function, first-class continuation, partially-applied argument, curried-parameter list
- **Data structures:** persistent-data structure, copy-on-write map, structurally-shared tree
- **Evaluation:** lazily-evaluated sequence, strictly-evaluated argument, tail-recursive call, pattern-matched clause
- **Concurrency:** message-passing actor, software-transactional memory, lock-free CAS loop

> **Non-STE:**
> ```
> -- The higher order function returns a lazily evaluated sequence that is
> -- side effect free.
> map :: (a -> b) -> [a] -> [b]
> map f xs = f <$> xs
> ```
>
> **STE:**
> ```
> -- The higher-order function returns a lazily-evaluated sequence that is
> -- side-effect-free.
> map :: (a -> b) -> [a] -> [b]
> map f xs = f <$> xs
> ```
>
> *Principles applied: P1, P2, P11. Three compound adjectives in one sentence, each needing a hyphen. "Higher-order" and "side-effect-free" are multi-word compounds. Consistent hyphenation makes the sentence parse correctly on first reading.*

### Procedural (C, Go, Bash)

Procedural code deals with memory layout, pointers, and sequential control flow. Compound adjectives describe data representation and control constructs.

**Key compound terms:**

- **Memory layout:** null-terminated string, zero-initialized struct, stack-allocated array, heap-allocated buffer, page-aligned address, cache-line-aligned field
- **Pointer semantics:** pointer-to-pointer indirection, double-indirected reference, const-qualified parameter
- **Control flow:** short-circuit evaluation, early-return pattern, fall-through case, set-jmp context, computed-goto dispatch
- **I/O and files:** newline-delimited output, null-separated records, byte-order-mark prefixed, CRLF-terminated line
- **Build and linking:** statically-linked binary, dynamically-loaded library, position-independent code, link-time optimization

> **Non-STE:**
> ```
> /* The function expects a null terminated string and returns a zero
>    initialized struct. */
> void parse_config(const char* text, Config* out);
> ```
>
> **STE:**
> ```
> /* The function expects a null-terminated string and returns a
>    zero-initialized struct. */
> void parse_config(const char* text, Config* out);
> ```
>
> *Principles applied: P1, P2. Without hyphens, "null terminated string" can mean "null" modifies "terminated string" rather than "null-terminated" modifying "string." The hyphen binds "null" to "terminated" as a unit.*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative languages describe desired state. Compound adjectives qualify resources, constraints, and relationships.

**Key compound terms:**

- **SQL:** left-joined table, fully-qualified column name, auto-incremented primary key, composite-index lookup, read-committed isolation, write-ahead log, row-level lock, table-valued function
- **Terraform:** user-provided input, provider-managed resource, state-locked backend, read-only attribute, computed-only field, force-new recreation
- **Kubernetes:** cluster-scoped resource, namespace-scoped object, ready-state pod, crash-looping container, health-check endpoint, rolling-update strategy, blue-green deployment
- **Configuration:** well-formed document, schema-validated input, base64-encoded value, newline-separated list

> **Non-STE:**
> ```
> -- The left joined table uses a fully qualified column name from the
> -- user provided input.
> SELECT users.name
> FROM users
> LEFT JOIN orders ON users.id = orders.user_id;
> ```
>
> **STE:**
> ```
> -- The left-joined table uses a fully-qualified column name from the
> -- user-provided input.
> SELECT users.name
> FROM users
> LEFT JOIN orders ON users.id = orders.user_id;
> ```
>
> *Principles applied: P1, P2. Three compound adjectives in one sentence. Each pair of words functions as a single modifier before its noun. Without hyphens, the reader must pause to parse which word modifies which.*

### Systems (Rust ownership docs, C memory docs)

Systems programming documentation describes ownership, lifetimes, memory models, and hardware interaction. Precision is critical because errors in this domain cause crashes or undefined behavior.

**Key compound terms:**

- **Ownership and borrowing:** move-semantics transfer, borrow-checked reference, lifetime-annotated parameter, ownership-taking function, reference-counted smart pointer, atomically-reference-counted handle
- **Memory model:** memory-mapped I/O, copy-on-write page, zero-cost abstraction, cache-coherent domain, sequentially-consistent ordering, acquire-release semantics
- **Concurrency primitives:** lock-free stack, wait-free queue, compare-and-swap loop, spin-lock guard, read-copy-update mechanism
- **Low-level representation:** little-endian byte order, two's-complement representation, sign-extended value, bit-packed field, aligned-to-16-bytes address
- **Safety:** undefined-behavior risk, data-race condition, use-after-free bug, double-free error, dangling-pointer access

> **Non-STE:**
> ```
> // The memory mapped file uses a copy on write page that is
> // atomically reference counted.
> fn map_region(handle: &Arc<MappedFile>) { /* ... */ }
> ```
>
> **STE:**
> ```
> // The memory-mapped file uses a copy-on-write page that is
> // atomically-reference-counted.
> fn map_region(handle: &Arc<MappedFile>) { /* ... */ }
> ```
>
> *Principles applied: P1, P2, P11. Systems documentation has dense compound adjectives. "Memory-mapped," "copy-on-write," and "atomically-reference-counted" are each single concepts. The hyphens prevent the reader from misreading "copy on write page" as an instruction to copy something onto a write page.*

## Extended Examples

> **Non-STE:**
> ```
> # The anti aliasing filter is applied before the pixel data enters the
> # re entrant rendering pipeline.
> def render(pixels: Image) -> Image:
>     return apply_filter(pixels, ANTI_ALIAS)
> ```
>
> **STE:**
> ```
> # The anti-aliasing filter is applied before the pixel data enters the
> # re-entrant rendering pipeline.
> def render(pixels: Image) -> Image:
>     return apply_filter(pixels, ANTI_ALIAS)
> ```
>
> *Principles applied: P1, P2. Category 5 hyphenation: prefix ending in a vowel plus root starting with a vowel. "Anti-aliasing" and "re-entrant" each need a hyphen to separate the prefix from the root. Without the hyphen, the double vowel is visually confusing and slows reading.*

> **Non-STE:**
> ```
> // The 64 bit register alignment requires an 8 byte offset for each
> // 128 bit value.
> struct Packet { uint64_t header; uint8_t pad[8]; uint128_t payload; };
> ```
>
> **STE:**
> ```
> // The 64-bit register alignment requires an 8-byte offset for each
> // 128-bit value.
> struct Packet { uint64_t header; uint8_t pad[8]; uint128_t payload; };
> ```
>
> *Principles applied: P1, P2. Category 3 hyphenation: number plus noun giving configuration. "64-bit" functions as a single adjective modifying "register." The same pattern applies to "8-byte" and "128-bit." Without hyphens, the reader sees "64" as a standalone number rather than part of a compound modifier.*

> **Non-STE:**
> ```
> # Run a dry run of the deployment before you hot reload the
> # production server.
> deploy(dry_run=True)
> reload_server("prod", hot=True)
> ```
>
> **STE:**
> ```
> # Dry-run the deployment before you hot-reload the production server.
> deploy(dry_run=True)
> reload_server("prod", hot=True)
> ```
>
> *Principles applied: P1, P2, P13. Category 4 hyphenation: verbs containing a noun as the first part. "Dry-run" is a verb here (not a noun), so it needs the hyphen. "Hot-reload" follows the same pattern. Compare: "Do a dry run" (noun, no hyphen) versus "Dry-run the deployment" (verb, hyphen required).*

> **Non-STE:**
> ```
> // The end to end test covers the entire data flow from server side
> // rendering to client side hydration.
> test_e2e();
> ```
>
> **STE:**
> ```
> // The end-to-end test covers the entire data flow from server-side
> // rendering to client-side hydration.
> test_e2e();
> ```
>
> *Principles applied: P1, P2, P11. Category 1 hyphenation: multi-word compound adjectives before nouns. "End-to-end" is a three-word adjective modifying "test." "Server-side" and "client-side" are two-word adjectives modifying "rendering" and "hydration." Consistent hyphenation across all three compounds makes the sentence parse clearly.*

> **Non-STE:**
> ```
> // This is a self contained module with a well defined interface and a
> // fail fast error handling strategy.
> class Pipeline { /* ... */ };
> ```
>
> **STE:**
> ```
> // This is a self-contained module with a well-defined interface and a
> // fail-fast error-handling strategy.
> class Pipeline { /* ... */ };
> ```
>
> *Principles applied: P1, P2. Category 1 hyphenation: compound adjectives before nouns. "Self-" compounds always take a hyphen. "Well-defined" is a standard compound. "Fail-fast" and "error-handling" are code-domain compounds. Four hyphenated terms in one sentence is acceptable when each is a genuine compound adjective.*

> **Non-STE:**
> ```
> // The just in time compiler produces machine code at run time using a
> // fire and forget compilation strategy.
> jit_compile(source);
> ```
>
> **STE:**
> ```
> // The just-in-time compiler produces machine code at run time using a
> // fire-and-forget compilation strategy.
> jit_compile(source);
> ```
>
> *Principles applied: P1, P2, P11. Category 1 hyphenation: multi-word compound adjectives. "Just-in-time" is a four-word adjective before "compiler." "Fire-and-forget" is a three-word adjective before "strategy." Note: "at run time" is not hyphenated because "run time" is a noun phrase, not a compound adjective before a noun.*

## Edge Cases

### Edge Case 1: Framework and Library Names That Are Already Hyphenated

Some frameworks, libraries, and tools have hyphens in their official names. When you refer to these names in documentation, keep the hyphens as part of the proper noun. Do not add or remove hyphens from tool names.

Examples of hyphenated tool names: `create-react-app`, `server-side-rendering`, `tailwind-merge`, `eslint-plugin-react`, `github-actions`

When you use the tool name as a modifier, do not add a second hyphen:

> **Correct:** The create-react-app template includes a pre-configured webpack setup.
>
> **Incorrect:** The create-react-app-template includes a pre-configured webpack setup.

In the incorrect version, the extra hyphen makes the tool name look like "create-react" applied to "app-template." Use the official name as-is.

### Edge Case 2: When a Code Keyword Conflicts With Hyphenation

Some programming language keywords are compound words that dictionaries write without hyphens. In documentation prose, hyphenate them when they serve as compound adjectives. In code examples, reproduce the keyword exactly as the language requires.

Examples:

- **JavaScript `typeof`:** In prose: "The type-of operator returns a string." In code: `typeof x`
- **Python `nonlocal`:** In prose: "The non-local variable binding." In code: `nonlocal x`
- **SQL `FULL OUTER JOIN`:** In prose: "A full-outer-join operation." In code: `FULL OUTER JOIN`

NOTE: When a keyword appears in a code block or inline code span (backtick-delimited), reproduce it exactly as the language defines it. Apply Rule 8.2 only in narrative documentation prose outside code spans.

### Edge Case 3: Generated Code and Auto-Generated Documentation

Generated code and auto-generated documentation often come from tools that do not apply STE-Code rules. Do not manually hyphenate generated output. If you control the generator, configure it to produce hyphenated compounds. If you do not control the generator, leave the output as-is and add a NOTE in surrounding prose.

> **Non-STE generated output:** "This is a high priority read only file descriptor."
>
> **STE-Code prose surrounding it:** NOTE: The generated documentation uses unhyphenated compounds. In STE-Code, write "high-priority" and "read-only."

### Edge Case 4: Compound Terms Established Without Hyphens in a Codebase

Some compound terms become so common in a specific codebase that they are treated as single words. Examples include "codebase" itself, "filename," and "namespace." When a compound is consistently written without a hyphen across an entire project and the meaning is unambiguous, you may keep the established form.

Decision criteria for keeping an unhyphenated compound:

1. The term appears without a hyphen in the project's style guide or glossary.
2. All contributors use the unhyphenated form consistently.
3. The unhyphenated form causes no ambiguity in any documentation context.
4. The term is a single dictionary word (e.g., "filename") not a fresh compound (e.g., "threadsafe" is not yet standard).

If any of these criteria fail, apply Rule 8.2 and hyphenate.

### Edge Case 5: Hyphens in API Endpoint Names and URL Paths

API endpoint names and URL path segments follow their own conventions. Many REST APIs use hyphens in path segments (kebab-case). Document these endpoints using their exact path form. In prose that describes the endpoint, hyphenate compound adjectives normally.

Examples:

| URL path | Prose description |
|----------|-------------------|
| `/api/user-settings` | The user-settings endpoint returns the current-user profile. |
| `/api/read-only-access` | The read-only-access endpoint provides a read-only view of the data. |

In the prose description, "current-user" is a compound adjective before "profile" and takes a hyphen. "Read-only" before "view" also takes a hyphen. The endpoint name "read-only-access" keeps its hyphens because it is a proper noun.

NOTE: Do not confuse URL path hyphens with documentation prose hyphens. They serve different purposes and follow different rules. The URL path uses kebab-case for machine readability. The prose uses hyphens per Rule 8.2 for human readability.

## Cross-References

This rule interacts with several other STE-Code rules. Apply them together for consistent documentation.

### Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs

Many hyphenated compounds contain approved words. When you form a compound adjective, each component word must be an approved STE-Code word (or a permitted technical noun under Rule 1.5). Example: "thread-safe" uses "thread" (technical noun, Rule 1.5) and "safe" (approved adjective).

### Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category

Technical code nouns often appear as the first element in a hyphenated compound. Examples: "thread-safe," "stack-allocated," "type-safe," "cache-aligned." The technical noun is permitted under Rule 1.5. The hyphen connects it to the qualifying word.

### Rule 1.9 — When You Must Select a Technical Noun, Use One Which Is Short and Easy to Understand

When a hyphenated compound becomes long (three or more words before a noun), ask whether you can shorten it. Example: "least-recently-used eviction policy" could become "LRU eviction policy" after the acronym is defined. Prefer the shorter form when the audience knows the acronym.

### Rule 1.11 — Do Not Use Different Technical Nouns for the Same Item

Hyphenated compounds are terms. Once you choose a hyphenated form for a concept, use that same form everywhere. Do not write "thread-safe" in one section and "thread safe" in another. Inconsistency confuses readers and undermines the purpose of Rule 8.2.

### Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon (;)

Rule 8.2 and Rule 8.1 work together as the punctuation rules. Rule 8.1 governs sentence-level punctuation (periods, commas, colons). Rule 8.2 governs word-level punctuation (hyphens in compounds). Apply both rules in every documentation sentence. A sentence can be correctly punctuated under Rule 8.1 but still violate Rule 8.2 if a compound adjective lacks a hyphen.

### Rule 8.6 — Elements That Count as One Word

Rule 8.6 defines which constructions count as one word for the STE-Code word-count limit. A hyphenated compound counts as one word, so a fully hyphenated phrase does not inflate your sentence word count the way a space-separated phrase does. See Rule 8.6 for the full list of what counts as one word.

### Rule 8.7 — Hyphenated Words Count as One Word

Rule 8.7 is the complement to this rule: it confirms that a hyphenated compound (for example, "read-only" or "end-to-end") counts as a single word when you measure sentence length against the STE-Code limit. Apply Rule 8.2 to form the compound and Rule 8.7 to count it correctly.

## Grammar Notes

The grammar behind Rule 8.2 comes from standard English compound-adjective formation, adapted for the technical vocabulary of code documentation. This section explains the grammatical principles that justify the rule.

### Attributive vs. Predicative Position

A compound adjective takes a hyphen when it appears **before** the noun it modifies (attributive position). The same compound usually does not take a hyphen when it appears **after** a linking verb (predicative position).

| Attributive (hyphen) | Predicative (no hyphen) |
|----------------------|-------------------------|
| The thread-safe collection | The collection is thread safe |
| A read-only file descriptor | The file descriptor is read only |
| A well-defined interface | The interface is well defined |
| A null-terminated string | The string is null terminated |

Exception: Some compounds are always hyphenated regardless of position. These include "self-" compounds (self-contained, self-evident) and compounds where the unhyphenated form would be ambiguous.

### Adverb-Adjective Compounds: When NOT to Hyphenate

Do not hyphenate a compound when the first word is an adverb ending in "-ly." The "-ly" ending already signals that the adverb modifies the adjective, so the hyphen is unnecessary.

| Correct (no hyphen) | Incorrect (unnecessary hyphen) |
|---------------------|-------------------------------|
| a fully qualified name | a fully-qualified name |
| a dynamically allocated buffer | a dynamically-allocated buffer |
| a lazily evaluated expression | a lazily-evaluated expression |
| a statically linked library | a statically-linked library |

This rule applies because the "-ly" adverb unambiguously modifies the following adjective. The hyphen adds no clarity and is considered incorrect in standard English.

### The "Temporary Compound" Principle

In code documentation, many hyphenated compounds are "temporary compounds" — words that combine only in a specific technical context. The hyphen signals that the words form a unit for this sentence. When the same words appear separately elsewhere, they carry different meanings.

Example: "write lock" vs. "write-lock"

- "The function must acquire a write lock." — "write" is an adjective modifying "lock." No hyphen needed because "write" directly describes the type of lock.
- "The write-lock acquisition failed." — "write-lock" is a compound noun used attributively before "acquisition." The hyphen clarifies that "write-lock" is the compound concept being acquired, not that "write" modifies "lock acquisition."

Example: "run time" vs. "run-time"

- "The algorithm completes in O(n) run time." — "run time" is a noun phrase. No hyphen.
- "A run-time error occurred." — "run-time" is a compound adjective before "error." Hyphen required.

### Code Identifiers and Hyphens in Prose

When you describe a code identifier in prose, do not insert hyphens into the identifier itself. Identifiers in most languages cannot contain hyphens. Use the identifier exactly as it appears in code, and use hyphenated prose around it.

```
Incorrect: The get-user-profile function returns a user-profile object.

Correct: The `getUserProfile` function returns a user-profile object.
```

The backtick-delimited identifier `getUserProfile` is a code token, not prose. It keeps its source form (camelCase). The prose phrase "user-profile object" follows Rule 8.2 because "user-profile" is a compound adjective before "object."

### Hyphenation With Multi-Word Technical Nouns

When a technical noun is itself a multi-word phrase, and you use it as a modifier before another noun, you must decide where to place hyphens. The principle: hyphenate the entire modifying phrase as a single unit.

| Without hyphen (ambiguous) | With hyphen (clear) |
|---------------------------|---------------------|
| read only file descriptor | read-only file descriptor |
| high priority task scheduler | high-priority task scheduler |
| least recently used cache entry | least-recently-used cache entry |
| first in first out queue | first-in-first-out queue |

In "high-priority task scheduler," the hyphenated "high-priority" modifies "task scheduler" as a unit. The reader understands that it is a scheduler for high-priority tasks, not a high scheduler for priority tasks.

### The Self- Prefix Rule

Words with the prefix "self-" always take a hyphen in standard English and in STE-Code. This rule has no exceptions.

| Correct | Incorrect |
|---------|-----------|
| self-contained module | selfcontained module |
| self-documenting code | selfdocumenting code |
| self-signed certificate | selfsigned certificate |
| self-healing system | selfhealing system |

The "self-" prefix rule is a sub-rule of Rule 8.2. Apply it consistently across all documentation types.

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs

> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category

> **See also:** Rule 1.9 — When You Must Select a Technical Noun, Use One Which Is Short and Easy to Understand

> **See also:** Rule 1.11 — Do Not Use Different Technical Nouns for the Same Item

> **See also:** Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon (;)

> **See also:** Rule 8.6 — Elements That Count as One Word

> **See also:** Rule 8.7 — Hyphenated Words Count as One Word

---

<!-- a-sec8-rule8.3.md -->

# Rule 8.3 — Use of Parentheses

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.3

> **Source:** [master.md#sec8-rule8.3](ste-code/grouped/)

## Original Rule

**Rule 8.3** You can use parentheses:

- To make references to illustrations or text
- To include letters or numbers that identify items on an illustration or in a text
- To identify the work steps in a procedure
- To include abbreviations
- To give the singular and plural forms of a noun at the same time
- To explain words or a part of a sentence
- To include an alternative.

In STE, you can use parentheses as follows:

1. To make references to illustrations or text

   > **STE:** Remove the valve (10, Figure 1).
   > **STE:** Install the cover (refer to paragraphs 2 thru 5).

2. To include letters or numbers that identify items on an illustration or in a text

   > **STE:** Disconnect the hoses (2) and (12) from the suction ejector (8).
   > **STE:** Remove the nuts (74), the washers (76), the bolts (68), the seals (70), and the bonding straps (72).

3. To identify the work steps in a procedure

   > **STE:** (1) Install the locking cap (4) on the body (8).
   > **STE:** (2) Safety the locking cap (4) with the cotter pin (5).
   > **STE:** (3) Install a new retaining ring (6).

4. To include abbreviations

   > **STE:** A Liquid Crystal Display (LCD) is a flat-panel display that uses the light-modulating properties of liquid crystals.

5. To give the singular and plural forms of a noun at the same time

   | Example | Text |
   |---------|------|
   | A | Before you do the test(s), install the component(s). |
   | B | Do the applicable test(s). |

6. To explain words or a part of a sentence

   > **STE:** Increase the pressure slowly (not more than 10 psi each minute).
   > **STE:** Make sure that the BLEED pushbutton switch is released (the ON legend is off).

7. To include an alternative

   > **STE:** Open the left (right) access panel L42 (R42).

## STE-Code Adaptation

**Rule 8.3** In code documentation, you can use parentheses:

- To make references to code modules, diagrams, or text
- To include letters or numbers that identify items in a diagram or in a text
- To identify the work steps in a procedure
- To include abbreviations
- To give the singular and plural forms of a noun at the same time
- To explain words or a part of a sentence
- To include an alternative.

1. To make references to code modules, diagrams, or text

   > **Non-STE:** You can call the request handler from the auth middleware, which is described in the architecture diagram in the third figure, and the bootstrap routine is documented across chapters two through five of the integration guide.
   >
   > **STE:** Call the request handler (Figure 3, Module A).
   >
   > **STE:** Deploy the service (refer to sections 2 thru 5).

   Where this appears in real documentation:

   ```markdown
   ## Request flow

   Call the request handler (Figure 3, Module A) to validate the incoming
   payload. Deploy the service (refer to sections 2 thru 5) after the
   canary passes.
   ```

2. To include letters or numbers that identify items in a diagram or in a text

   > **Non-STE:** Disconnect both the inbound endpoint that is labelled number two on the topology diagram and the outbound endpoint labelled twelve, and remove them from the load balancer that the diagram marks as item eight.
   >
   > **STE:** Disconnect the endpoints (2) and (12) from the load balancer (8).
   >
   > **STE:** Remove the configuration keys (74), the environment variables (76), the secrets (68), the tokens (70), and the certificates (72).

   Where this appears in real documentation:

   ```markdown
   ## Teardown

   Disconnect the endpoints (2) and (12) from the load balancer (8).
   Remove the configuration keys (74), the environment variables (76),
   the secrets (68), the tokens (70), and the certificates (72).
   ```

3. To identify the work steps in a procedure

   > **Non-STE:** First, you should install the dependency package that is shown as item four in the project layout, and you put it in the project directory, which the layout marks as item eight. Then, you need to pin that dependency package with the lock file, which is item five. Finally, you should add a new test case, which is item six in the layout.
   >
   > **STE:** (1) Install the dependency package (4) in the project directory (8).
   >
   > **STE:** (2) Pin the dependency package (4) with the lock file (5).
   >
   > **STE:** (3) Add a new test case (6).

   Where this appears in real documentation:

   ```markdown
   ## Set up the build

   (1) Install the dependency package (4) in the project directory (8).
   (2) Pin the dependency package (4) with the lock file (5).
   (3) Add a new test case (6).
   ```

4. To include abbreviations

   > **Non-STE:** A Command Line Interface, which people often call a CLI, is a text-based interface that lets you type commands to control the operating system.
   >
   > **STE:** A Command Line Interface (CLI) is a text-based interface that uses typed commands to interact with the operating system.

   Where this appears in real documentation:

   ```markdown
   ## Overview

   A Command Line Interface (CLI) is a text-based interface that uses
   typed commands to interact with the operating system. The CLI reads
   each command and runs the matching program.
   ```

5. To give the singular and plural forms of a noun at the same time

   > **Non-STE:** Before you run the test or the tests, you must set the environment variable or the environment variables that the job needs.
   >
   > **STE:** Before you run the test(s), set the environment variable(s).

   Where this appears in real documentation:

   ```markdown
   ## Prerequisites

   Before you run the test(s), set the environment variable(s) that the
   job reads. Use the CI secret store for the production value(s).
   ```

6. To explain words or a part of a sentence

   > **Non-STE:** You should increase the timeout value by a small amount each time the loop runs, and you must not let it grow by more than one thousand milliseconds for each step, or else the client will time out.
   >
   > **STE:** Increase the timeout slowly (not more than 1000 ms each step).
   >
   > **STE:** Make sure that the DEBUG flag is released (the ON indicator is off).

   Where this appears in real documentation:

   ```markdown
   ## Tuning

   Increase the timeout slowly (not more than 1000 ms each step) to avoid
   client-side failures. Make sure that the DEBUG flag is released
   (the ON indicator is off) before you ship.
   ```

7. To include an alternative

   > **Non-STE:** If you are in the staging environment you should use the left API key, but if you are in the production environment you should use the right API key instead.
   >
   > **STE:** Use the left (right) API key for the staging (production) environment.

   Where this appears in real documentation:

   ```markdown
   ## Authentication

   Use the left (right) API key for the staging (production) environment.
   Store the key in the secret manager, not in the source tree.
   ```

## Examples

> *Adapted from spec pair:* Non-STE: A Representational State Transfer Application Programming Interface, or REST API, is an architectural style for designing networked applications relying on stateless, client-server communication.  |  STE: A Representational State Transfer Application Programming Interface (REST API) is an architectural style for designing networked applications that uses stateless, client-server communication.

> *Adapted from spec pair:* Non-STE: Before you do the test(s), install the component(s).  |  STE: Run the migration on all database shard(s) before you deploy.

> **Non-STE:** A Representational State Transfer Application Programming Interface, or REST API, is an architectural style for designing networked applications relying on stateless, client-server communication.
>
> **STE:** A Representational State Transfer Application Programming Interface (REST API) is an architectural style for designing networked applications that uses stateless, client-server communication.
>
> *Adapted from spec pattern: abbreviation in parentheses — "A Liquid Crystal Display (LCD) is a flat-panel display..."*

> **Non-STE:** Run the migration on all database shard servers, the primary and all replica instances, before you deploy.
>
> **STE:** Run the migration on all database shard(s) before you deploy.
>
> *Adapted from spec pattern: singular/plural in parentheses — "Before you do the test(s), install the component(s)."*

## Code-Domain Explanation

Rule 8.3 governs how parentheses appear across all code documentation types. Each documentation type uses parentheses differently because each type has a unique audience and purpose.

### README Files

README files introduce a project to new users. Use parentheses to define abbreviations on first use. The abbreviation must follow immediately after the full term, enclosed in parentheses. This pattern helps the reader scan the document quickly.

> **Non-STE:** This project provides a CLI, or command-line interface, for managing your deployment pipeline, and you can use it to build, test, and ship your services without leaving the terminal.
>
> **STE:** This project provides a Command Line Interface (CLI) for managing your deployment pipeline.
>
> *Principles applied: P11, P3 — one term per concept, use words with approved meanings*

Where this appears in a real README:

```markdown
# deploy-bot

This project provides a Command Line Interface (CLI) for managing your
deployment pipeline. Run `deploy-bot help` to see the list of commands.
```

Use parentheses to reference related documentation files or sections. Keep the reference concise. Do not use parentheses to inject commentary or asides that distract from the main instruction.

> **Non-STE:** Follow the setup guide, which you can find in the docs folder, specifically in the getting-started subdirectory, before you run the server, otherwise the server will fail to start because the config file is missing.
>
> **STE:** Follow the setup guide (refer to docs/getting-started.md) before you run the server.
>
> *Principles applied: P9, P1 — prefer short technical nouns, use approved words*

Where this appears in a real README:

```markdown
## Quick start

Follow the setup guide (refer to docs/getting-started.md) before you run
the server. The guide shows how to create the config file.
```

### API Documentation

API documentation describes endpoints, parameters, and return types. Use parentheses to explain parameter constraints or to show the unit of measurement for numeric values. Do not use parentheses to nest multiple levels of conditional logic.

> **Non-STE:** The timeout parameter accepts an integer representing milliseconds, though you can also use seconds if you set the unit flag to the string "s", and that option has been available starting in version 2.1 of the API.
>
> **STE:** The timeout parameter accepts an integer in milliseconds (ms). To use seconds, set the unit flag to "s" (available in version 2.1 and later).
>
> *Principles applied: P9, P6 — prefer short nouns, non-approved words only as technical nouns*

Where this appears in real API reference:

```markdown
### POST /v1/jobs

| Parameter | Type    | Description                                          |
|-----------|---------|------------------------------------------------------|
| timeout   | integer | Wait time in milliseconds (ms). Range: 100 to 30000. |

The timeout parameter accepts an integer in milliseconds (ms). To use
seconds, set the unit flag to "s" (available in version 2.1 and later).
```

Use parentheses around HTTP status codes or error codes to keep the main sentence flow uninterrupted.

> **Non-STE:** If the request fails you will get back a 404 which means the resource was not found on the server, and you should show an error page to the user.
>
> **STE:** If the request fails, the server returns a 404 (Not Found) status.
>
> *Principles applied: P2, P3 — use words only as their specified part of speech, use approved meanings*

Where this appears in real API reference:

```markdown
## Responses

- 200 (OK): the resource was returned.
- 404 (Not Found): the requested id does not exist.
- 500 (Internal Server Error): the server failed to process the request.
```

### Docstrings and Inline Comments

Docstrings describe a function, method, or class at its point of definition. Use parentheses to show parameter types, return types, or valid value ranges. In statically typed languages, do not repeat the type in parentheses when the type signature already states it. Use parentheses only for clarifying constraints the type system cannot express.

> **Non-STE:** // the timeout argument is an integer, it must be between one and thirty thousand, and it represents the number of milliseconds to wait before the call gives up
>
> **STE:** // timeout: milliseconds (1 to 30000)
>
> *Principles applied: P9, P4 — prefer short nouns, use approved adjective forms*

Where this appears in real source:

```python
def fetch(url: str, timeout: int) -> Response:
    """Get a URL.

    Args:
        url: the address to fetch.
        timeout: milliseconds to wait (1 to 30000).
    """
    ...
```

> **Non-STE:** """Calculate the factorial of n. n must be a non-negative integer, and the function raises an error if you pass a negative number."""
>
> **STE:** """Calculate the factorial of n (a non-negative integer)."""
>
> *Principles applied: P6, P9 — non-approved words only as technical nouns, prefer short nouns*

Where this appears in real source:

```python
def factorial(n: int) -> int:
    """Calculate the factorial of n (a non-negative integer)."""
    if n < 0:
        raise ValueError("n must be >= 0")
    return 1 if n in (0, 1) else n * factorial(n - 1)
```

### Commit Messages

Commit messages benefit from the alternative-use pattern of parentheses. Use parentheses to indicate the scope of a change or to reference an issue tracker identifier. The scope word must be short and standard.

> **Non-STE:** feat: add Proof Key for Code Exchange support to the authentication module, which covers the whole OAuth2 flow including the token refresh step, so that public clients can authenticate safely
>
> **STE:** feat(auth): add PKCE support (issue #482)
>
> *Principles applied: P9, P11 — prefer short nouns, one term per concept*

Where this appears in a real commit log:

```text
commit 9f2c1a4
Author: dev@corp.example
Date:   2026-08-01

    feat(auth): add PKCE support (issue #482)

    Public clients now use the code challenge to stop interception.
```

> **Non-STE:** fix: resolve problem where the dropdown menu sometimes displayed behind the modal dialog because the stacking context was wrong
>
> **STE:** fix(ui): correct z-index conflict between dropdown and modal (regression from v2.3)
>
> *Principles applied: P6, P1 — technical nouns allowed, use approved words*

Where this appears in a real commit log:

```text
commit 4b8e0d2
Author: dev@corp.example
Date:   2026-08-01

    fix(ui): correct z-index conflict between dropdown and modal
    (regression from v2.3)
```

### Error Messages

Error messages must be unambiguous. Use parentheses to include diagnostic values (file paths, line numbers, actual versus expected values) without breaking the sentence structure. Put the diagnostic data at the end of the message in parentheses.

> **Non-STE:** Couldn't find the config file you specified; looked in /etc/myapp/config.yaml, ~/.config/myapp/config.yaml, and ./config.yaml but none existed or were readable so the program cannot start.
>
> **STE:** Cannot find the configuration file (searched: /etc/myapp/config.yaml, ~/.config/myapp/config.yaml, ./config.yaml).
>
> *Principles applied: P1, P2 — use approved words, use words only as their specified part of speech*

Where this appears in real source:

```python
raise FileNotFoundError(
    "Cannot find the configuration file "
    "(searched: /etc/myapp/config.yaml, "
    "~/.config/myapp/config.yaml, ./config.yaml)."
)
```

> **Non-STE:** The value for --workers must be between 1 and 64 inclusive but you supplied 0 which is out of range so the command will not run
>
> **STE:** Invalid value for --workers: 0 (valid range: 1 to 64).
>
> *Principles applied: P9, P3 — prefer short nouns, use approved meanings*

Where this appears in real source:

```python
parser.error("Invalid value for --workers: 0 (valid range: 1 to 64).")
```

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python)

Object-oriented documentation uses parentheses to show method parameters, constructor arguments, and type parameters (generics). In narrative documentation, use parentheses to note the class hierarchy or to identify which interface a method implements. Do not use parentheses to nest multiple inheritance chains.

> **Non-STE:** The process method, which belongs to the DataPipeline class that extends BasePipeline, which itself implements the Pipeline interface from the core package, orchestrates the extract, transform, and load workflow for the batch job.
>
> **STE:** The `process` method (inherited from `BasePipeline`, which implements `core.Pipeline`) orchestrates the ETL workflow.
>
> *Principles applied: P9, P6 — prefer short nouns, technical nouns allowed*

Where this appears in real documentation:

```markdown
## DataPipeline

The `process` method (inherited from `BasePipeline`, which implements
`core.Pipeline`) orchestrates the ETL workflow. Call it after you load
the source rows.
```

Use parentheses to show default parameter values in documentation tables. This mirrors how IDEs display method signatures.

> **Non-STE:** | timeout | int | how long to wait before giving up, defaults to 5000 |
>
> **STE:** | timeout | int | milliseconds to wait before failure (default: 5000) |
>
> *Principles applied: P1, P4 — use approved words, use approved adjective forms*

Where this appears in real documentation:

```markdown
| Parameter | Type | Description                                  |
|-----------|------|----------------------------------------------|
| timeout   | int  | milliseconds to wait before failure (default: 5000) |
| retries   | int  | attempts on failure (default: 3)             |
```

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure transformations, type signatures, and algebraic data types. Use parentheses to group type parameters or to show the shape of a curried function. In narrative text, use parentheses to explain the difference between a function's pure and effectful variants.

> **Non-STE:** map is a higher-order function that takes a transformation function and applies it to every element inside a functor, producing a new functor with the transformed elements, and most people use it to change a list of values.
>
> **STE:** `map` applies a function to each element of a functor (a container type that supports mapping). It returns a new functor with the transformed values.
>
> *Principles applied: P6, P7 — technical nouns allowed, do not use technical nouns as verbs*

Where this appears in real documentation:

```markdown
## map

`map` applies a function to each element of a functor (a container type
that supports mapping). It returns a new functor with the transformed
values.

```haskell
map :: (a -> b) -> f a -> f b
```
```

> **Non-STE:** The state monad threads an immutable state value through a sequence of computations, and StateT is the monad transformer version that lets you stack it on top of another monad so you can mix state with IO.
>
> **STE:** The `State` monad passes an immutable state value through a chain of computations. Use `StateT` (the transformer variant) to combine it with another monad.
>
> *Principles applied: P9, P11 — prefer short nouns, one term per concept*

Where this appears in real documentation:

```markdown
## State

The `State` monad passes an immutable state value through a chain of
computations. Use `StateT` (the transformer variant) to combine it with
another monad such as `IO`.
```

### Procedural Documentation (C, Go, Bash)

Procedural documentation focuses on sequential steps, error codes, and resource lifecycle. Use parentheses to show return codes or exit statuses. Use parentheses to note ownership or allocation responsibility (who must free or close a resource).

> **Non-STE:** The function returns 0 if everything went fine, -1 if there was an I/O error, -2 if the input was malformed, and -3 if the operation timed out, so check the code after each call.
>
> **STE:** The function returns: 0 (success), -1 (I/O error), -2 (malformed input), -3 (timeout).
>
> *Principles applied: P9, P2 — prefer short nouns, use words only as their specified part of speech*

Where this appears in real documentation:

```c
/*
 * open_socket connects to the remote host.
 * Returns: 0 (success), -1 (I/O error),
 *          -2 (malformed input), -3 (timeout).
 */
int open_socket(const char *host, int port);
```

> **Non-STE:** The caller is responsible for deallocating the buffer that this function allocates, and failure to do so will cause a memory leak that the runtime cannot recover.
>
> **STE:** The caller must free the returned buffer (allocated by this function). Failure to free the buffer causes a memory leak.
>
> *Principles applied: P1, P12 — use approved words, technical verbs allowed*

Where this appears in real documentation:

```c
/*
 * read_packet copies the next packet into a new buffer.
 * The caller must free the returned buffer (allocated by this function).
 * Failure to free the buffer causes a memory leak.
 */
char *read_packet(int fd);
```

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state, schema, and resource definitions. Use parentheses to show valid enumeration values. Use parentheses to note the unit of a numeric field. Do not use parentheses to embed conditional logic that belongs in a separate note or warning.

> **Non-STE:** The `provider` field must be set to one of the following: "aws", "gcp", or "azure" and the value is case-sensitive so do not use uppercase letters.
>
> **STE:** Set the `provider` field to one of: "aws", "gcp", "azure" (lowercase only).
>
> *Principles applied: P1, P3 — use approved words, use approved meanings*

Where this appears in real documentation:

```hcl
# Set the provider field to one of: "aws", "gcp", "azure" (lowercase only).
variable "provider" {
  type    = string
  default = "aws"
}
```

> **Non-STE:** The `replicas` field controls how many copies of the pod the deployment maintains, and you can set it to any integer from 1, which is the minimum that you need for production, up to 100.
>
> **STE:** Set `replicas` to the number of pod copies (range: 1 to 100, production minimum: 1).
>
> *Principles applied: P9, P2 — prefer short nouns, use words only as their specified part of speech*

Where this appears in real documentation:

```yaml
# Set replicas to the number of pod copies (range: 1 to 100,
# production minimum: 1).
spec:
  replicas: 3
```

### Systems Documentation (Rust Ownership, C Memory)

Systems documentation explains ownership, lifetimes, and memory safety. Use parentheses to mark the ownership transfer point or to note the lifetime relationship. Use parentheses to annotate unsafe blocks with the safety invariant they uphold.

> **Non-STE:** When you pass a value to this function, ownership moves into the function and the caller can no longer access that value unless the function returns it back to the caller at the end.
>
> **STE:** This function takes ownership of the value (the caller cannot use it after the call). To keep access, pass a reference instead.
>
> *Principles applied: P6, P7 — technical nouns allowed, do not use technical nouns as verbs*

Where this appears in real documentation:

```rust
/// Consume the buffer and write it to the socket.
/// This function takes ownership of the value (the caller cannot use it
/// after the call). To keep access, pass a reference instead.
fn send(buf: Vec<u8>) -> std::io::Result<()> {
    // ...
}
```

> **Non-STE:** // SAFETY: the pointer must be non-null, properly aligned for the type T, and point to a valid initialized instance of T, and the caller must keep that true for the whole time the function runs.
>
> **STE:** // SAFETY: the pointer must be non-null, aligned for type T, and point to a valid initialized T (invariant enforced by caller).
>
> *Principles applied: P9, P1 — prefer short nouns, use approved words*

Where this appears in real source:

```rust
// SAFETY: the pointer must be non-null, aligned for type T, and point to
// a valid initialized T (invariant enforced by caller).
unsafe fn read_at<T>(p: *const T) -> T {
    std::ptr::read(p)
}
```

## Extended Examples

### Example 1: Abbreviation on First Use

> **Non-STE:** Set up CI/CD, meaning continuous integration and continuous delivery, for your project by adding a pipeline configuration file to the repository root, and then you can run the build from your laptop.
>
> **STE:** Set up Continuous Integration and Continuous Delivery (CI/CD) for your project. Add a pipeline configuration file to the repository root.
>
> *Principles applied: P1, P4 — use approved words, use approved adjective forms. The abbreviation follows immediately after the full term in parentheses, as the original STE spec requires. The original sentence was split into two shorter procedural sentences per STE length limits.*

Where this appears in a real README:

```markdown
## CI/CD

Set up Continuous Integration and Continuous Delivery (CI/CD) for your
project. Add a pipeline configuration file to the repository root.
The pipeline runs the test suite on every push.
```

### Example 2: Step Numbering in Procedures

> **Non-STE:** To initialize the database, first run the schema migration, then seed the reference data, and finally create the admin user account, and make sure you do them in that order or the seed will fail.
>
> **STE:** To initialize the database:
> (1) Run the schema migration.
> (2) Seed the reference data.
> (3) Create the admin user account.
>
> *Principles applied: P2, P9 — use words only as their specified part of speech, prefer short nouns. The numbered steps in parentheses follow the original STE pattern for procedure identification. Each step is one instruction.*

Where this appears in real documentation:

```markdown
## Initialize the database

To initialize the database:
(1) Run the schema migration.
(2) Seed the reference data.
(3) Create the admin user account.
```

### Example 3: Alternative Configuration Values

> **Non-STE:** Set the log level to either debug if you are troubleshooting or info if you are running in production mode, and never use trace in production because it writes too much to disk.
>
> **STE:** Set the log level to debug (troubleshooting) or info (production).
>
> *Principles applied: P3, P9 — use approved meanings, prefer short nouns. The alternative-value pattern from the original STE spec ("left (right)") is adapted here for configuration options. Each option's purpose is explained concisely in parentheses.*

Where this appears in real documentation:

```yaml
# Set the log level to debug (troubleshooting) or info (production).
logging:
  level: info
```

### Example 4: Explaining a Code Statement

> **Non-STE:** The retry loop will attempt the request up to five times, waiting one second between each attempt, and if all five fail it will propagate the last error to the caller so the caller can decide what to do next.
>
> **STE:** The retry loop attempts the request (maximum 5 attempts, 1-second delay between attempts). If all attempts fail, it propagates the last error to the caller.
>
> *Principles applied: P1, P2 — use approved words, use words only as their specified part of speech. The parenthetical explanation clarifies the loop parameters without interrupting the sentence flow. "Maximum" replaces the informal "up to."*

Where this appears in real source:

```python
def request_with_retry(url: str) -> Response:
    """Send the request (maximum 5 attempts, 1-second delay between
    attempts). If all attempts fail, it propagates the last error to
    the caller."""
    ...
```

### Example 5: Singular/Plural in Configuration Instructions

> **Non-STE:** Before starting the service, make sure all necessary environment variable or variables have been set in the .env file or through the shell, because a missing one will stop the service from booting.
>
> **STE:** Before you start the service, set the necessary environment variable(s) in the .env file.
>
> *Principles applied: P1, P11 — use approved words, one term per concept. The "(s)" pattern from the original STE spec eliminates the awkward "variable or variables" construction. The instruction is direct and uses one term consistently.*

Where this appears in real documentation:

```markdown
## Configuration

Before you start the service, set the necessary environment variable(s)
in the .env file. The service reads each variable at start time.
```

### Example 6: Reference to External Documentation

> **Non-STE:** For detailed information about the authentication protocol, check out the OAuth 2.0 specification which is documented in RFC 6749 and available online if you search for it.
>
> **STE:** For detailed information about the authentication protocol, refer to RFC 6749 (OAuth 2.0 Authorization Framework).
>
> *Principles applied: P1, P3 — use approved words, use approved meanings. The parenthetical title of the referenced document helps the reader confirm they have the correct standard. "Refer to" replaces the informal "check out."*

Where this appears in real documentation:

```markdown
## Authentication

For detailed information about the authentication protocol, refer to
RFC 6749 (OAuth 2.0 Authorization Framework). The server uses the
authorization code flow.
```

## Edge Cases

### Edge Case 1: Framework Names That Are Also Unapproved Words

When a framework or library name is identical to a common English word that STE restricts, parentheses clarify meaning. For example, the Python web framework "Flask" is also a common noun. Use parentheses to distinguish the technical noun from the common word.

> **Non-STE:** Use Flask to serve the application. Flask is a microframework that does not require particular tools or libraries, and you can add only what you need.
>
> **STE:** Use Flask (the Python web framework) to serve the application. Flask does not require particular tools or libraries.
>
> *Principles applied: P6, P8 — non-approved words only as technical nouns, use standard technical nouns. The parenthetical clarification eliminates ambiguity between the framework name and the common English word.*

Where this appears in real documentation:

```markdown
## Web layer

Use Flask (the Python web framework) to serve the application. Flask
does not require particular tools or libraries. Add routes with
`@app.route`.
```

Similarly, when a framework uses an STE-approved word in an unapproved sense (for example, "React" does not mean "to respond"), add a brief parenthetical on first use.

> **Non-STE:** This project uses React to build the user interface. React components are reusable pieces of UI that you compose into pages.
>
> **STE:** This project uses React (a JavaScript UI library) to build the user interface. React components are reusable pieces of UI.
>
> *Principles applied: P6, P8 — non-approved words only as technical nouns, use standard technical nouns.*

Where this appears in real documentation:

```markdown
## Front end

This project uses React (a JavaScript UI library) to build the user
interface. React components are reusable pieces of UI.
```

### Edge Case 2: Code Keywords That Conflict with the Rule

Some programming language keywords are also punctuation characters. For example, Rust uses parentheses for tuple types and unit types. In documentation, do not add extra parentheses around these keywords — the code syntax itself is unambiguous. Reserve narrative parentheses for explanations.

> **Non-STE:** The function returns `()` (pronounced "unit"), which is Rust's equivalent of void (meaning no meaningful value), and you see it when a function does work but returns nothing.
>
> **STE:** The function returns `()` (the unit type, equivalent to void in other languages).
>
> *Principles applied: P6, P9 — technical nouns allowed, prefer short nouns. The parenthetical explanation is kept because "unit type" is a domain concept that some readers may not know. The nested parenthetical "(meaning no meaningful value)" was removed to avoid clutter.*

Where this appears in real documentation:

```rust
/// Finish the task and return.
/// The function returns `()` (the unit type, equivalent to void in
/// other languages).
fn finish() {
    // ... no value returned
}
```

When documentation describes generic type parameters in angle brackets (for example, `<T>`), do not place the angle brackets inside parentheses. Keep the code literal distinct from the narrative explanation.

> **Non-STE:** The `Option` type (which is generic over `<T>`) represents an optional value that may or may not be present, and you use it to replace null checks.
>
> **STE:** The `Option<T>` type represents an optional value. The type parameter `T` can be any type.
>
> *Principles applied: P9, P7 — prefer short nouns, do not use technical nouns as verbs. The code literal `Option<T>` is self-documenting. The explanation is separated into its own sentence instead of being nested in parentheses.*

Where this appears in real documentation:

```rust
/// The `Option<T>` type represents an optional value. The type
/// parameter `T` can be any type. Use `Some(T)` for a value and
/// `None` for absence.
enum Option<T> {
    Some(T),
    None,
}
```

### Edge Case 3: Parentheses in Generated Code or Auto-Generated Docs

Generated API reference docs (for example, from JSDoc, Sphinx, or rustdoc) often include parentheses around types and return values automatically. Do not remove these — they are not part of the narrative text. Apply Rule 8.3 only to the portions of documentation that a human writes, such as description fields and summary paragraphs.

> **Auto-generated (acceptable as-is):** `getUser(id: number): Promise<User>`
>
> **STE description field:** Get a user by their identifier (returns a Promise that resolves to a User object).
>
> *Principles applied: P6, P11 — technical nouns allowed, one term per concept. The auto-generated signature is left untouched. The human-written description follows STE rules, using parentheses to explain the return type.*

Where this appears in real source:

```typescript
/**
 * Get a user by their identifier (returns a Promise that resolves to a
 * User object).
 */
function getUser(id: number): Promise<User> {
  // ...
}
```

> **Auto-generated (acceptable as-is):** `fn connect(addr: SocketAddr) -> Result<TcpStream, Error>`
>
> **STE description field:** Connect to the address. Returns a Result (Ok with a TcpStream on success, Err with an Error on failure).
>
> *Principles applied: P6, P1 — technical nouns allowed, use approved words. Parentheses explain the two Result variants concisely.*

Where this appears in real source:

```rust
/// Connect to the address. Returns a Result (Ok with a TcpStream on
/// success, Err with an Error on failure).
fn connect(addr: SocketAddr) -> Result<TcpStream, Error> {
    // ...
}
```

### Edge Case 4: Nested Parentheses

Never nest parentheses. The original STE standard does not permit nesting because it reduces readability. If a sentence requires nested parenthetical information, restructure the sentence or split it.

> **Non-STE:** Set the cache TTL to 3600 (one hour (or 86400 for one day in production)), and pick the value that matches your traffic pattern.
>
> **STE:** Set the cache TTL to 3600 (one hour). For production, set the cache TTL to 86400 (one day).
>
> *Principles applied: P1, P9 — use approved words, prefer short nouns. The nested parentheses are eliminated by splitting into two sentences. Each parenthetical stands alone.*

Where this appears in real documentation:

```markdown
## Caching

Set the cache TTL to 3600 (one hour). For production, set the cache TTL
to 86400 (one day).
```

> **Non-STE:** The middleware pipeline processes requests through authentication (via JWT (JSON Web Token)), authorization, and rate limiting, and each stage can reject the request.
>
> **STE:** The middleware pipeline processes requests through authentication (via JWT), authorization, and rate limiting. JWT is an abbreviation for JSON Web Token.
>
> *Principles applied: P1, P11 — use approved words, one term per concept. The abbreviation is defined in a separate sentence. Nested parentheses are eliminated.*

Where this appears in real documentation:

```markdown
## Middleware

The middleware pipeline processes requests through authentication
(via JWT), authorization, and rate limiting. JWT is an abbreviation
for JSON Web Token.
```

### Edge Case 5: Parentheses in Command-Line Help Text

Command-line help text appears in terminal output with limited formatting. Use parentheses sparingly. Prefer the alternative-use pattern (for example, `--verbose (--quiet)`) or the explanation pattern (for example, `--timeout MILLISECONDS (default: 5000)`). Do not use parentheses for long descriptions that belong in a man page.

> **Non-STE:** --config PATH    Path to config file (can be JSON, YAML, or TOML, and the loader picks the parser from the file extension)
>
> **STE:** --config PATH    Path to the configuration file (JSON, YAML, or TOML)
>
> *Principles applied: P1, P9 — use approved words, prefer short nouns. The parenthetical lists valid formats concisely.*

Where this appears in real help output:

```text
Usage: deploy-bot [options]

Options:
  --config PATH    Path to the configuration file (JSON, YAML, or TOML)
  --verbose        Show detailed logs (use --quiet to silence)
  --timeout MS     Wait time in milliseconds (default: 5000)
```

## Cross-References

This rule interacts with several other STE-Code rules:

- **Rule 1.1 (Approved Words):** Parentheses introduce abbreviations. The word inside parentheses must be the approved abbreviation form. See the STE-Code Dictionary for the canonical abbreviation list.

- **Rule 1.3 (Approved Meanings):** When parentheses explain a word, the explanation must use words with their approved meanings. Do not use parentheses to sneak in an unapproved meaning.

- **Rule 1.9 (Short Technical Nouns):** Parenthetical explanations must use short, standard technical nouns. Long explanatory phrases defeat the purpose of concise parenthetical notation.

- **Rule 5.1 (Sentence Length):** Parenthetical content counts toward the sentence word limit (20 procedural, 25 descriptive). If a parenthetical pushes a sentence over the limit, split the sentence.

- **Rule 6.3 (Procedural Steps):** When parentheses identify work steps, each step number must have its own line. Do not list multiple steps inside one set of parentheses.

- **Bracket usage:** Parentheses are the only permitted brackets in STE. Do not use square brackets `[ ]` for parenthetical information. Square brackets are reserved for optional parameters in code syntax.

- **Comma usage with parentheses:** Do not use a comma before an opening parenthesis unless the parenthetical is an alternative at the end of a list (for example, "the staging server (node 3), and the production server (node 1)").

- **Rule 8.2 (Hyphens):** Do not confuse parentheses with hyphens when listing compound adjectives. Parentheses explain. Hyphens join words into a single modifier.

> **See also:** Rule 1.1 — Approved Words
> **See also:** Rule 1.3 — Approved Meanings
> **See also:** Rule 1.5 — Technical Noun Categories
> **See also:** Rule 1.9 — Short Technical Nouns
> **See also:** Rule 5.1 — Sentence Length
> **See also:** Rule 6.3 — Procedural Steps
> **See also:** Rule 8.2 — Use of Hyphens

## Grammar Notes

### Syntactic Function of Parentheses in STE

In the original ASD-STE100, parentheses serve as a secondary syntactic boundary. The primary boundary is the period (full stop). Commas separate items within a clause. Parentheses enclose supplementary information that relates to but does not interrupt the main clause structure.

In code documentation, parentheses serve the same role but must also coexist with code syntax that uses parentheses for function calls, type parameters, and grouping expressions. The writer must distinguish narrative parentheses from code parentheses.

### Parentheses vs. Commas vs. Dashes

Original STE permits parentheses but does not permit em dashes or en dashes for parenthetical asides. The comma is the only other permitted punctuation for supplementary information. Use commas for brief, non-essential clauses. Use parentheses when the supplementary information is a discrete unit (an abbreviation, a reference, a range, or an alternative value).

> **Non-STE:** The API gateway -- which sits between clients and microservices -- routes requests to the correct backend, and it also applies rate limits.
>
> **STE:** The API gateway (which sits between clients and microservices) routes requests to the correct backend.
>
> *Principles applied: P1, P2 — use approved words, use words only as their specified part of speech. Dashes are not permitted in STE. Parentheses handle the non-restrictive clause.*

Where this appears in real documentation:

```markdown
## Gateway

The API gateway (which sits between clients and microservices) routes
requests to the correct backend.
```

### Punctuation Inside and Outside Parentheses

In STE, the punctuation of the main sentence is not affected by the parenthetical content. A period that ends a sentence goes outside the closing parenthesis. A period that ends only the parenthetical content (when the parenthetical is a complete sentence) goes inside. However, complete-sentence parentheticals are discouraged in STE because they can be written as separate sentences.

> **Non-STE:** Deploy to the staging environment first. (The production deployment follows after approval.)
>
> **STE:** Deploy to the staging environment first. Deploy to the production environment after approval.
>
> *Principles applied: P1, P9 — use approved words, prefer short nouns. The parenthetical complete sentence is converted to a standalone imperative sentence. This improves readability and follows STE conventions.*

Where this appears in real documentation:

```markdown
## Rollout

Deploy to the staging environment first. Deploy to the production
environment after approval.
```

When the parenthetical ends the sentence and is not a complete sentence, the period goes outside:

> **STE:** Set the log level to debug (recommended for development).
>
> *Principles applied: P1, P2 — use approved words, use words only as their specified part of speech.*

Where this appears in real documentation:

```yaml
# Set the log level to debug (recommended for development).
logging:
  level: debug
```

### Abbreviation Placement

The original STE rule requires that the abbreviation appear in parentheses immediately after the first use of the full term. Do not place the full term in parentheses after the abbreviation. The pattern is always: "Full Term (ABBR)." After the first definition, use only the abbreviation.

> **Non-STE:** Use the CLI (Command Line Interface) to deploy. The Command Line Interface provides quick access.
>
> **STE:** Use the Command Line Interface (CLI) to deploy. The CLI gives quick access.
>
> *Principles applied: P4, P11 — use approved adjective forms, one term per concept. The abbreviation follows the full term, not vice versa. After definition, only the abbreviation is used.*

Where this appears in real documentation:

```markdown
## Deploy

Use the Command Line Interface (CLI) to deploy. The CLI gives quick
access to every environment. Run `cli deploy --env staging` to start.
```

---

<!-- a-sec8-rule8.4.md -->

# Rule 8.4 — Colon in a Vertical List

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.4

> **Source:** [master.md#sec8-rule8.4](ste-code/grouped/)

## Original Rule

**Rule 8.4** In a vertical list, a colon (:) has the same effect on word count as a period and shows the end of a sentence.

In a vertical list, a colon (:) divides the first part of the sentence from the subsequent items in the vertical list. This colon has the effect of a period (full stop). Thus:

- In procedural sentences, you can use a maximum of 20 words before the colon.
- In descriptive sentences, you can use a maximum of 25 words before the colon.

Each item in a vertical list that comes after the colon counts as a new sentence. Thus, the limit for each item in a vertical list is:

- 20 words for procedural sentences
- 25 words for descriptive sentences.

> **STE:** To extinguish a possible fire, portable fire extinguishers are installed in these areas: (13 words)
>
> - The cockpit (2 words)
> - The cabin (2 words)
> - The cabin sub-compartment (3 words)
> - The crew rest compartment. (4 words)

## STE-Code Adaptation

**Rule 8.4** In code documentation, a colon (:) in a vertical list has the same effect on word count as a period and shows the end of a sentence.

In a vertical list, a colon (:) divides the first part of the sentence from the subsequent items in the vertical list. This colon has the effect of a period (full stop). Thus:

- In procedural sentences, you can use a maximum of 20 words before the colon.
- In descriptive sentences, you can use a maximum of 25 words before the colon.

Each item in a vertical list that comes after the colon counts as a new sentence. Thus, the limit for each item in a vertical list is:

- 20 words for procedural sentences
- 25 words for descriptive sentences.

### Examples

> *Adapted from spec pair:* Non-STE: `To extinguish a possible fire, portable fire extinguishers are installed in these areas:` followed by a vertical list of locations with word counts | STE: `To handle possible error conditions, the error handler catches these exception types:` followed by a vertical list (ASD-STE100 Issue 9, Rule 8.4, page 105 — the colon before a vertical list acts as a period and each list item is a new sentence with its own word-count limit).

> **Non-STE:** To handle all possible error conditions, the following exception types must be caught and processed by the error handler: database connection timeouts which occur when the primary node is unreachable, authentication failures caused by expired or invalid tokens, and validation errors due to malformed request payloads.
>
> **STE:** To handle possible error conditions, the error handler catches these exception types:
>
> - Database connection timeout (3 words)
> - Authentication failure (2 words)
> - Validation error. (2 words)
>
> *Adapted from spec pair: "To extinguish a possible fire, portable fire extinguishers are installed in these areas:" followed by a vertical list of locations with word counts.*

The non-STE sentence buries three distinct catch cases in one 31-word introduction. Written as a handler, the same content is hard to scan:

```python
# Non-STE: one long comment, no clear list of cases.
# To handle all possible error conditions, the following exception types
# must be caught and processed by the error handler: database connection
# timeouts which occur when the primary node is unreachable, authentication
# failures caused by expired or invalid tokens, and validation errors due
# to malformed request payloads.
try:
    result = call_external_service(request)
except Exception as exc:        # catches everything in one branch
    logger.error("unhandled error: %s", exc)
    raise
```

The STE version names each case as a separate, scannable item and maps it to its own `except` branch:

```python
# STE: the comment lists each exception type on its own line.
# To handle possible error conditions, the error handler catches
# these exception types:
#   - Database connection timeout
#   - Authentication failure
#   - Validation error
try:
    result = call_external_service(request)
except DatabaseTimeout as exc:    # Database connection timeout
    retry_with_backoff(exc)
except AuthenticationFailure as exc:  # Authentication failure
    redirect_to_login(exc)
except ValidationError as exc:    # Validation error
    return error_response(exc)
```

> **Non-STE:** The configuration file, which is located in the project root, supports these environment profiles that you can use for deployment: a development profile for local testing and debugging, a staging profile for pre-production integration verification, and a production profile for the live customer-facing environment.
>
> **STE:** The configuration file supports these environment profiles:
>
> - Development (1 word)
> - Staging (1 word)
> - Production. (1 word)
>
> *Adapted from spec pair: vertical list with colon introducing enumerated items, each counted as a separate sentence.*

The non-STE comment hides the three profile names behind a 31-word introduction:

```yaml
# Non-STE: the profile names are buried in the lead-in sentence.
# The configuration file, which is located in the project root, supports
# these environment profiles that you can use for deployment: a development
# profile for local testing and debugging, a staging profile for
# pre-production integration verification, and a production profile for
# the live customer-facing environment.
profiles:
  development: { url: "http://localhost:8080" }
  staging:     { url: "https://staging.example.com" }
  production:  { url: "https://example.com" }
```

The STE comment states the category in 7 words and lets the list carry the names:

```yaml
# STE: short introduction, then a vertical list.
# The configuration file supports these environment profiles:
#   - Development
#   - Staging
#   - Production
profiles:
  development: { url: "http://localhost:8080" }
  staging:     { url: "https://staging.example.com" }
  production:  { url: "https://example.com" }
```

## Code-Domain Explanation

Rule 8.4 sets word-count limits for vertical lists in all code documentation. The colon (:) before a vertical list acts as a period. The introductory text before the colon must obey the sentence-length rules: a maximum of 20 words for procedural text and 25 words for descriptive text. Each list item after the colon is a new sentence with its own length limit.

This rule prevents the most common vertical list abuse: a long, clause-heavy introduction that tries to include qualifiers, conditions, and justifications before the colon. The introduction should state only what the list contains. The list items should deliver the full content. The colon is the boundary between the "setup" and the "payload." A reader processes the introduction, understands the category, and then reads each list item as a standalone sentence.

When the introductory text before the colon exceeds the word limit, the writer has three options: (1) move the extra words into the list items themselves, (2) split the introduction into two sentences — one sentence before the list (without a colon) and a second sentence that introduces the list, or (3) remove unnecessary qualifiers from the introduction. The third option is usually correct. Writers tend to over-explain the list's contents in the introduction instead of trusting the list items to speak for themselves.

Word count in list items follows standard STE-Code rules. Articles (a, an, the) count as words. Code tokens inside backticks count as one word each regardless of their length. Parenthetical word counts in examples serve as training aids and are not required in production documentation.

### README Files

README files use vertical lists for installation steps, prerequisites, feature lists, supported platforms, and contribution guidelines. A common violation: the introductory sentence embeds version numbers, compatibility notes, and caveats before the colon. The reader must parse a 30-plus-word introduction before reaching the list items.

The fix: move qualifiers into the list items or into a separate sentence before the introduction. The introduction to a vertical list should state only the category of items that follow.

Example of a colon-in-list violation in a README installation section:

````
To install this package, which requires Python 3.10 or later and a
working C compiler for the native extensions on Linux and macOS
systems only, you need these dependencies: libssl-dev, pkg-config,
and cmake version 3.20 or later.
````

The introduction has 32 words before the colon. The dependency names and version requirements are buried in a single long sentence:

````
This package needs Python 3.10 or later. It also needs a C compiler
for native extensions on Linux and macOS systems. Install these
dependencies:

- libssl-dev
- pkg-config
- cmake (version 3.20 or later).
````

### API Documentation

API documentation uses vertical lists for endpoint parameters, request body fields, response fields, error codes, and authentication methods. The introductory sentence should name the endpoint or resource and state what the list enumerates. It should not describe each parameter's type, default value, and validation rules — those details belong in the list items.

A common violation: the introduction tries to summarize every nuance of the parameter list. Example:

````
POST /users accepts the following JSON body fields, all of which are
required except for middle_name which is optional and defaults to
null:
````

The introduction embeds type and optionality information for one field. The fix keeps the introduction generic:

````
A POST request to /users accepts these JSON body fields:

- username (string, required)
- email (string, required)
- middle_name (string, optional — the default value is null)
- role (string, required).
````

### Docstrings and Inline Comments

Docstrings use vertical lists for parameter descriptions (Args:), return value descriptions (Returns:), raised exceptions (Raises:), and usage examples. Many docstring formats (Google style, NumPy style, Sphinx reStructuredText) already enforce a colon-before-list structure. Rule 8.4 aligns with these formats but adds the explicit word-count constraint for the introductory text.

In practice, docstring introductions are usually short — "Args:", "Returns:", "Raises:" — and trivially comply with Rule 8.4. The risk appears in custom section headers where the writer crafts a longer introduction. Example of a violation:

````
The following edge cases are handled by this function and must be
considered by any caller that passes untrusted input to the parser:
````

The fix shortens the introduction and puts the nuance in the list:

````
This function handles these edge cases:

- Empty input strings
- Input with only whitespace characters
- Input longer than the maximum buffer size
- Input with non-UTF-8 byte sequences.
````

### Commit Messages

Commit messages use vertical lists in the body to enumerate related changes, breaking changes, or migration steps. A common violation: the subject line or the first body sentence becomes a long introduction that summarizes all the changes. The subject line is not an introduction to a vertical list — it is a standalone sentence that summarizes the commit. The body's introductory sentence (if any) must be short.

Example of a violation in a commit message body:

````
This commit refactors the authentication middleware to support
multiple token providers including JWT, OAuth2, and SAML, and makes
these related changes:
````

The introduction has 17 words — within the limit — but it also duplicates information that belongs in the list items. The fix:

````
This commit makes these changes to the authentication middleware:

- Add support for JWT tokens
- Add support for OAuth2 tokens
- Add support for SAML tokens
- Remove the deprecated Basic Auth provider.
````

### Error Messages

Error messages sometimes use vertical lists to enumerate possible causes or recovery steps. This is common in CLI tools and server applications that produce multi-line error output. The colon introduction must be short ("The command failed for one of these reasons:"). Each reason or step is a separate sentence. Do not chain multiple reasons into one long list item.

The word-count limit for procedural list items (20 words) applies to each recovery step. If a step needs more than 20 words, it is too complex — split it into two steps or simplify the instruction.

Example of a violation in a CLI error message:

````
The database migration failed due to one of the following possible
causes which you should investigate in order: the database server is
not reachable on the configured host and port, the migration user
does not have the ALTER TABLE privilege, or the migration scripts
directory contains SQL files with syntax errors.
````

The introduction and the single list item both violate the limits. The fix:

````
The database migration failed for one of these reasons:

- The database server is not reachable. Check the host and port.
- The migration user does not have the ALTER TABLE privilege.
- A SQL file in the migrations directory has a syntax error.
````

Underlying code that emits the message:

```python
# STE: the message uses a short introduction and one item per cause.
def run_migration(db, migrations_dir):
    causes = []
    if not db.reachable():
        causes.append("The database server is not reachable. Check the host and port.")
    if not db.user_has_privilege("ALTER TABLE"):
        causes.append("The migration user does not have the ALTER TABLE privilege.")
    bad = find_sql_syntax_error(migrations_dir)
    if bad is not None:
        causes.append(f"A SQL file in the {migrations_dir} directory has a syntax error.")
    if causes:
        raise MigrationError("The database migration failed for one of these reasons:")
```

## Paradigm-Specific Guidance

### Object-Oriented Paradigm (Java, C++, C#, Python classes)

In OOP documentation, vertical lists appear in class overviews (list of public methods), interface specifications (list of implementing classes), constructor documentation (list of parameters), and exception specifications (list of thrown exceptions). The introductory text should name the class and state the list category. Avoid embedding type constraints, access modifiers, or inheritance details in the introduction.

Pattern: Write the class or method name in the introduction. State the list category with a generic phrase ("accepts these parameters," "throws these exceptions," "implements these interfaces"). Put the type, default value, and constraint information in each list item. Never use the introduction to describe the first parameter in detail and then append the remaining parameters as an afterthought.

Example of a colon-in-list violation in a Java class docstring:

````
The ConnectionPool constructor accepts the following arguments
including the database URL which must be a valid JDBC connection
string with the host, port, and database name:
````

The introduction embeds detail about one argument. The fix:

````
The ConnectionPool constructor accepts these arguments:

- url — A valid JDBC connection string (host, port, and database name)
- maxConnections — The largest number of concurrent connections
- timeout — The connection timeout value in milliseconds.
````

Full docstring context:

```java
/**
 * The ConnectionPool constructor accepts these arguments:
 *   - url — A valid JDBC connection string (host, port, and database name)
 *   - maxConnections — The largest number of concurrent connections
 *   - timeout — The connection timeout value in milliseconds.
 */
public ConnectionPool(String url, int maxConnections, int timeout) { ... }
```

### Functional Paradigm (Haskell, Elixir, Clojure, Rust)

In functional documentation, vertical lists appear in ADT (algebraic data type) documentation (list of variants), function composition descriptions (list of transformation steps), and pattern matching documentation (list of match arms). Each list item often describes a separate case, variant, or transformation. The introduction should state the type or function name and the cases it handles.

Pattern: Use the introduction to name the type or function. Use list items to describe each case independently. Do not use the introduction to describe the "happy path" and relegate error cases to an unindented continuation after the colon.

Example of a violation in a Rust enum docstring:

````
The ParseResult enum represents the possible outcomes of parsing a
configuration file which can succeed with the parsed Config struct,
fail due to an I/O error when the file cannot be read, or fail due to
invalid syntax when the file contains malformed TOML:
````

The introduction is 38 words — far over the 25-word descriptive limit. The fix:

````
The ParseResult enum represents the result of parsing a configuration
file. The enum has these variants:

- Ok(Config) — The file was parsed successfully.
- Err(ParseError::Io) — The file could not be read.
- Err(ParseError::Syntax) — The file contains incorrect TOML syntax.
````

Full doc context:

```rust
/// The ParseResult enum represents the result of parsing a configuration
/// file. The enum has these variants:
///   - Ok(Config) — The file was parsed successfully.
///   - Err(ParseError::Io) — The file could not be read.
///   - Err(ParseError::Syntax) — The file contains incorrect TOML syntax.
enum ParseResult {
    Ok(Config),
    Err(ParseError),
}
```

### Procedural Paradigm (C, Go, Bash)

In procedural documentation, vertical lists are central to step-by-step procedures. Each step is a list item. The introduction states the goal of the procedure. A common violation: the introduction tries to summarize all the steps before the colon, effectively duplicating the list.

Pattern: Write a short goal statement before the colon ("To configure the server, do these steps:"). Write each step as an imperative list item. Do not use the introduction to describe the first step in detail and then list the remaining steps. Every step gets equal treatment as a list item.

Example of a violation in a Go setup guide:

````
To compile the project from source, first make sure you have Go 1.21
or later installed and your GOPATH is set correctly, then run these
commands:
````

The introduction includes a prerequisite check that should be a separate step or a separate sentence. The fix:

````
Make sure that Go 1.21 or later is installed. Make sure that the
GOPATH environment variable is set correctly. Then do these steps:

- Clone the repository.
- Run the `go mod download` command.
- Run the `go build` command.
````

### Declarative Paradigm (SQL, Terraform, Kubernetes YAML)

In declarative documentation, vertical lists appear in resource property specifications (list of allowed values), constraint descriptions (list of validation rules), and configuration option documentation (list of valid settings). The introduction names the resource or option. Each list item gives one value, one rule, or one setting.

Pattern: The introduction states the resource name and the list category ("The `instance_type` variable accepts these values:"). Each list item is one value with an optional short description. Do not use the introduction to explain why certain values are excluded — put that in a NOTE after the list.

Example of a violation in a Terraform variable description:

````
The instance_type variable, which controls the EC2 instance size for
the application tier and must be compatible with the selected AMI,
accepts these values:
````

The introduction embeds AMI compatibility constraints. The fix:

````
The instance_type variable sets the EC2 instance size. The variable
accepts these values:

- t3.micro
- t3.small
- t3.medium.

NOTE: The value must be compatible with the selected AMI.
````

### Systems Paradigm (Rust ownership docs, C memory docs)

In systems documentation, vertical lists appear in safety requirement specifications (list of preconditions), UB (Undefined Behavior) catalogs (list of triggering conditions), and ownership/borrowing rule documentation. The introduction states what the list enumerates. Each list item is a standalone safety condition. The word-count limit for list items ensures that safety-critical conditions are not buried in long sentences.

Systems documentation is the most safety-sensitive domain for Rule 8.4 compliance. A precondition buried in a long introduction is a precondition that a developer might miss during a code review. Each precondition must be a separate, numbered or bulleted list item. Each consequence must be explicit.

Example of a violation in a Rust unsafe function doc:

````
The caller must ensure that all of the following safety conditions
are met before calling this function including pointer validity,
alignment, and lifetime constraints:
````

This introduction is within the 25-word limit but it does not list the conditions — it only gestures at them. The fix enumerates each condition:

````
The caller must obey these safety conditions:

- The pointer must not be null.
- The pointer must be aligned to a 4-byte boundary.
- The data that the pointer refers to must be valid for the lifetime
  parameter `'a`.
- No other thread must write to the data during the call.
````

## Extended Examples

### Example 3 — README: Supported Platform List

> **Non-STE:** This library has been tested and verified to work correctly on the following operating system platforms and their respective versions including both 64-bit and ARM architectures where applicable: Ubuntu 22.04 LTS and 24.04 LTS, macOS 14 Sonoma and 15 Sequoia, and Windows 11 with MSVC 2022 or later.
>
> **STE:** This library operates on these platforms:
>
> - Ubuntu 22.04 LTS and 24.04 LTS (x86_64 and ARM64)
> - macOS 14 Sonoma and 15 Sequoia (x86_64 and ARM64)
> - Windows 11 with MSVC 2022 or later (x86_64).
>
> *Principles applied: P1, P2 (short introduction, 7 words before colon). The original introduction was 37 words with embedded architecture and version details. The fix moves architecture information into each list item as a parenthetical. Each list item stands as a complete descriptive sentence.*

Repository CI workflow that pins the same matrix — note the list stays short:

```yaml
# STE: the comment lists the supported platforms; the matrix mirrors it.
# This library operates on these platforms:
#   - Ubuntu 22.04 LTS and 24.04 LTS (x86_64 and ARM64)
#   - macOS 14 Sonoma and 15 Sequoia (x86_64 and ARM64)
#   - Windows 11 with MSVC 2022 or later (x86_64)
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-22.04, ubuntu-24.04, macos-14, macos-15, windows-2022]
```

### Example 4 — API Documentation: Response Fields

> **Non-STE:** A successful request to the GET /users/{id} endpoint returns a JSON response body that contains the following fields which describe the user account and its current state in the system: an id field with the unique user identifier as a UUID string, a username field with the display name chosen by the user during registration, an email field containing the verified email address, a created_at field with the ISO 8601 timestamp of account creation, and a status field that can be either active, suspended, or pending_verification.
>
> **STE:** A GET request to /users/{id} returns a JSON response with these fields:
>
> - `id` — The unique user identifier (UUID string)
> - `username` — The display name
> - `email` — The verified email address
> - `created_at` — The account creation timestamp (ISO 8601)
> - `status` — The account status (`active`, `suspended`, or `pending_verification`).
>
> *Principles applied: P1, P2 (introduction under 25 words, list items under 25 words each). The original had a 60-plus-word introduction with field descriptions embedded inline. The fix uses a short introduction and a dash-separated field description format. Code tokens in backticks count as one word each.*

OpenAPI schema that documents the same fields — each field is its own entry, mirroring the list:

```yaml
# STE: A GET request to /users/{id} returns a JSON response with these fields:
#   - id — The unique user identifier (UUID string)
#   - username — The display name
#   - email — The verified email address
#   - created_at — The account creation timestamp (ISO 8601)
#   - status — The account status (active, suspended, or pending_verification)
components:
  schemas:
    User:
      type: object
      properties:
        id:         { type: string, format: uuid }
        username:   { type: string }
        email:      { type: string, format: email }
        created_at: { type: string, format: date-time }
        status:     { type: string, enum: [active, suspended, pending_verification] }
```

### Example 5 — Docstring: Raised Exceptions

> **Non-STE:** This method can potentially raise the following exception types under various error conditions that the caller should be prepared to handle with appropriate try-catch blocks: a ValueError when the input string cannot be parsed into a valid integer representation, a TypeError when the provided argument is not a string type as expected by the parser, and an OverflowError when the parsed integer value exceeds the maximum allowed size for the platform's native integer type.
>
> **STE:** This method can raise these exceptions:
>
> - ValueError — The input string is not a valid integer.
> - TypeError — The argument is not a string.
> - OverflowError — The parsed value is too large for the platform.
>
> *Principles applied: P2 (descriptive sentence, 6 words before colon). The original introduction contained 29 words with redundant "try-catch" guidance. The fix puts the exception name and condition in each list item. The caller's responsibility to handle exceptions is implied by the method contract and does not need to be repeated.*

Python function where the docstring matches the `raise` statements:

```python
def parse_int(text):
    """Convert a string to an integer.

    This method can raise these exceptions:
      - ValueError — The input string is not a valid integer.
      - TypeError — The argument is not a string.
      - OverflowError — The parsed value is too large for the platform.
    """
    if not isinstance(text, str):
        raise TypeError("The argument is not a string.")
    try:
        value = int(text)
    except ValueError as exc:
        raise ValueError("The input string is not a valid integer.") from exc
    return value
```

### Example 6 — Commit Message: Breaking Changes

> **Non-STE:** This release introduces several breaking changes that affect the public API surface and require updates to existing integration code in downstream projects that consume this library: the authenticate function now returns a Promise instead of accepting a callback as its final parameter, the User type no longer includes the deprecated avatarUrl field which has been moved to the Profile type, and the minimum supported Node.js version has been increased from 16 to 18.
>
> **STE:** This release introduces these breaking changes:
>
> - The `authenticate` function returns a Promise. It no longer accepts a callback.
> - The `User` type does not include the `avatarUrl` field. Use the `Profile` type instead.
> - The minimum Node.js version is now 18 (was 16).
>
> *Principles applied: P2 (descriptive sentence, 7 words before colon). The original introduction was 48 words and described the nature of the changes instead of letting the list items speak. Each list item is now a descriptive or imperative sentence under 25 words.*

```text
Subject:  Bump to v3.0.0 with auth and type breaking changes

This release introduces these breaking changes:
- The `authenticate` function returns a Promise. It no longer accepts a callback.
- The `User` type does not include the `avatarUrl` field. Use the `Profile` type instead.
- The minimum Node.js version is now 18 (was 16).
```

### Example 7 — Error Message: Validation Errors

> **Non-STE:** The configuration file failed validation because of the following problems that must be fixed before the application can start and accept any incoming requests: the server.port value of "0" is not within the allowed range of 1024 to 65535 for privileged and non-privileged ports respectively, the database.url field is empty but is marked as required in the configuration schema, and the logging.level field contains "verbose" which is not one of the recognized log level values.
>
> **STE:** The configuration file has these problems:
>
> - The server.port value "0" is not in the range 1024 to 65535.
> - The database.url field is empty. This field is required.
> - The logging.level value "verbose" is not a valid log level.
>
> *Principles applied: P1 (short introduction, 6 words before colon), P2 (list items as new sentences). The original introduction was 42 words. Each list item now obeys the 25-word descriptive limit. The recovery instruction is implicit in the error format and does not need a separate "must be fixed" preamble.*

Validation routine that builds the message from the same list:

```python
# STE: the error uses a short introduction and one item per problem.
errors = []
if not (1024 <= cfg.server.port <= 65535):
    errors.append(f'The server.port value "{cfg.server.port}" is not in the range 1024 to 65535.')
if not cfg.database.url:
    errors.append("The database.url field is empty. This field is required.")
if cfg.logging.level not in {"debug", "info", "warn", "error"}:
    errors.append(f'The logging.level value "{cfg.logging.level}" is not a valid log level.')
if errors:
    raise ConfigError("The configuration file has these problems:")
```

### Example 8 — Configuration File Comment: Option Values

> **Non-STE:** The retry_strategy option in this configuration block controls how the client handles transient network failures and supports the following strategies with different trade-offs between consistency guarantees and tail latency characteristics that you should evaluate based on your workload profile: a fixed strategy that retries with a constant delay between attempts, an exponential strategy that doubles the delay after each failed retry, and a jittered strategy that adds random variation to the delay to avoid thundering herd problems during widespread outages.
>
> **STE:** The retry_strategy option accepts these values:
>
> - fixed — Retry with a constant delay between attempts.
> - exponential — Double the delay after each failed retry.
> - jittered — Add random variation to the delay.
>
> *Principles applied: P1, P2 (short introduction, 5 words before colon). The original introduction was 57 words with trade-off analysis embedded. The fix moves the strategy descriptions to the list items. The trade-off analysis belongs in a separate paragraph below the list, not in the introduction.*

Config file where the comment documents the option as a list:

```toml
# STE: the retry_strategy option accepts these values:
#   - fixed — Retry with a constant delay between attempts.
#   - exponential — Double the delay after each failed retry.
#   - jittered — Add random variation to the delay.
# The trade-off analysis belongs in a separate paragraph below the list,
# not in the introduction.
retry_strategy = "exponential"
```

## Edge Cases

### Edge Case 1 — When the Introductory Text Contains Inline Code

Code tokens inside backticks in the introductory text count as one word each, regardless of their character length. This means `docker-compose` counts as one word, and `com.example.service.UserRepository` also counts as one word. A long code token does not inflate the word count of the introduction.

However, this can create a false sense of compliance. An introduction that is technically 25 words but contains 12 code tokens is hard to read. Use the word-count limit as a ceiling, not a target. Prefer introductions with one or zero code tokens and fewer than 15 total words.

> **STE:** The `UserRepository` interface declares these methods: (6 words)
>
> - `findById(id: UserId): Option<User>`
> - `save(user: User): Result<(), Error>`
> - `delete(id: UserId): Result<(), Error>`.

> *The introduction uses one code token and six total words. Each list item is a function signature that counts as one "word" in STE-Code counting rules because it is a single code token.*

### Edge Case 2 — Nested Vertical Lists

A vertical list item can itself contain a nested vertical list. In this case, the parent list item is a sentence with its own word-count limit (20 procedural, 25 descriptive). The nested list has its own introductory text and its own colon, each subject to the same limits.

Guidance: Limit nesting to one level. A list item that introduces a nested list should be short — it serves only as a category heading. The nested list items carry the detail. If you find yourself writing a three-level nested list, restructure the content with subheadings.

> **STE:** The build system supports these output formats:
>
> - JavaScript bundles:
>   - ES module format
>   - CommonJS format
>   - UMD format.
> - CSS bundles:
>   - Standard CSS
>   - CSS modules.

> *The parent list items ("JavaScript bundles:" and "CSS bundles:") are short category headings. Each has its own colon and its own nested list. The structure stays at two levels.*

### Edge Case 3 — Code Blocks Inside List Items

A list item can contain a fenced code block. In this case, the list item's prose text must obey the word-count limit. The code block itself is exempt from word counting — it is code, not documentation prose. The code block does not contribute to the list item's word count.

Guidance: Use a short introductory sentence in the list item ("The command has this format:"), then place the code block. Do not put a long explanation before the code block inside a single list item. If the explanation is long, split it: one list item for the explanation, another for the code block.

> **STE:** The configuration file uses this format:
>
> - The `[server]` section sets the host and port:
>
>   ```
>   [server]
>   host = "0.0.0.0"
>   port = 8080
>   ```
>
> - The `[database]` section sets the connection parameters:
>
>   ```
>   [database]
>   url = "postgres://localhost:5432/app"
>   pool_size = 10
>   ```

> *Each list item has a short prose introduction followed by a code block. The prose introductions are 8 and 7 words respectively — well under the limit. The code blocks contribute zero words to the count.*

### Edge Case 4 — When a Framework or Tool Name Pushes the Introduction Over the Limit

Some framework names, API endpoint paths, or tool names are long by nature. For example, `KubernetesHorizontalPodAutoscaler` is a single code token but a visually heavy one. When the introduction must include several such names, the word count can appear within limits while the visual density is high.

Guidance: If the introduction feels visually heavy even when technically compliant, rewrite it. Move the long names into the list items. Use a generic introduction and let each list item introduce its own subject.

> **Non-STE:** The KubernetesHorizontalPodAutoscaler, PrometheusServiceMonitor, and IstioVirtualService custom resources support these configuration annotations: (10 words, but visually dense)
>
> **STE:** These custom resources support configuration annotations:
>
> - KubernetesHorizontalPodAutoscaler
> - PrometheusServiceMonitor
> - IstioVirtualService.
>
> *Principles applied: P1, P9 (prefer short, clear technical nouns in the introduction). The fix moves the long resource names into the list items. The introduction is now 6 common words with no code tokens. The reader processes the introduction quickly and encounters the domain-specific names in a scannable list.*

### Edge Case 5 — Generated Documentation with Automatic Colon-List Structures

Auto-generated API documentation (OpenAPI/Swagger UI, JSDoc HTML output, Sphinx autodoc, `--help` CLI output) often produces vertical lists with colons automatically. The generator controls the introduction text and the list formatting. The writer cannot always control the word count of the generated introduction.

Guidance: When you write the source comments or annotations that feed the generator, obey Rule 8.4. When the generator renders the output, accept its default formatting. If the generator produces introductions that consistently violate word-count limits, file an issue with the generator project. For hand-written documentation (README files, standalone API docs, commit messages), Rule 8.4 applies in full.

> **NOTE:** CLI `--help` output generated by argument parsers (clap for Rust, argparse for Python, cobra for Go) is often auto-formatted. The help text for each flag or argument becomes a list item. You control the help text you write in the source code. You do not control the generated list introduction ("Options:", "Commands:", "Arguments:"). Focus your compliance effort on the help text you author, not on the generator's boilerplate.

## Cross-References

- **Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs:** The words in your list introductions and list items must come from the STE-Code approved dictionary. Use the canonical synonyms (get, set, check, use) in list items. Do not use non-approved words just because a list item gives you a fresh sentence boundary.
- **Rule 1.3 — Use Approved Words Only with Their Approved Meanings:** When a list item describes a function's return value, make sure the verb "return" carries its approved meaning. Do not use "return" to mean "send back to the caller" in one list item and "produce as output" in another. Consistency across list items is mandatory.
- **Rule 3.1 — Use only the verb forms that are given in the dictionary:** Each list item after a colon is a new sentence. It must obey Rule 3.1: one subject, one verb, one object. Do not nest clauses inside a list item. If a list item feels complex, split it into two list items.
- **Rule 3.3 — Use the past participle form as an adjective:** Vertical lists are a way to obey Rule 3.3 organically. A dense paragraph with a buried enumeration can be restructured as a short introduction plus a vertical list. The combined structure satisfies both Rule 3.3 and Rule 8.4.
- **Rule 4.1 — One Topic Per Sentence, No Abstract Text:** Rule 8.4 enforces Rule 4.1 at two points: the introduction before the colon (20/25 words) and each list item (20/25 words). A document that passes Rule 4.1 on all prose sentences can still fail Rule 8.4 on its vertical list introductions. Check both.
- **Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence.:** Procedural vertical lists are the standard format for step-by-step instructions. Rule 6.3 governs when to use a list for procedures. Rule 8.4 governs the word counts within those lists. Together, they define the structure and the length of procedural documentation.
- **Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon (;):** The semicolon ban in Rule 8.1 means writers cannot use semicolons to join list items into a single sentence. They must use a vertical list with a colon instead. The colon in Rule 8.4 is the approved replacement for semicolon-joined enumerations.
- **STE-Code Dictionary — Section: Punctuation:** The dictionary defines the colon (:) as a sentence-boundary punctuation mark in the context of vertical lists. It also defines the period (.), question mark (?), and exclamation mark (!) as the other sentence terminators. Consult the dictionary for the full set of approved sentence boundaries.

## Grammar Notes

### The Colon as a Sentence Boundary

In standard English grammar, the colon can serve several functions: it introduces a list, it introduces an explanation, it introduces a quotation, or it separates independent clauses where the second clause explains the first. Not all of these functions create a sentence boundary.

In STE-Code, the colon before a vertical list is always a sentence boundary. The text before the colon is a complete sentence that ends at the colon. The text after the colon consists of separate sentences, one per list item. This grammatical rule simplifies mechanical compliance checking: a tool can split text on the colon, count words in the introduction, and then count words in each list item independently.

This is a stricter rule than standard English grammar, which permits a colon to appear mid-sentence in constructions like "The algorithm needs three inputs: X, Y, and Z." In STE-Code, this construction becomes:

> The algorithm needs these inputs:
>
> - X
> - Y
> - Z.

The colon always ends the introductory sentence. The enumerated items are always vertical, never inline.

### Vertical List Items as Independent Clauses

In standard English, vertical list items can be fragments (noun phrases, verb phrases, prepositional phrases) or complete sentences. STE-Code inherits this flexibility but adds the word-count rule: whether a list item is a fragment or a complete sentence, it must not exceed the word limit.

This creates an interesting tension. A fragment like "Database connection timeout" is 3 words and trivially compliant. But a fragment does not always give enough information. A complete sentence like "The database connection timed out because the primary node was unreachable" is 11 words — compliant but borderline. The writer must balance completeness against conciseness.

Guidance: When a list item needs more than 15 words to be complete, it probably contains two ideas. Split it into two list items. A vertical list of 8 short items is easier to read than a list of 4 long items. The visual structure of the list makes fragmentation acceptable — the reader uses the list introduction to establish the context, so each item can be terse.

### Word Counting Mechanics

The mechanics of word counting in vertical list contexts:

- **Introduction:** Count all words from the first word of the introductory sentence through the word before the colon. The colon itself is not a word. Parenthetical word counts in examples are for training and are not required in production text.
- **List items:** Count all words in each list item. If a list item contains a period at the end, the period is not a word. If a list item contains inline code in backticks, each backtick-delimited token counts as one word.
- **Nested lists:** Count the words in the parent list item up to its colon. Then count the words in each nested list item. The parent list item's word count does not include the nested list items.

A tool can verify Rule 8.4 compliance mechanically: (1) find all colons followed by a newline and a list marker, (2) count words in the text before each such colon, (3) count words in each list item, (4) flag any sentence that exceeds its type-specific limit.

### Parallel Structure in List Items

Rule 8.4 does not explicitly require parallel structure across list items, but parallel structure is a natural consequence of the rule. When each list item is a new sentence with its own subject and verb, and the introduction establishes the shared context, the items tend toward parallel structure organically.

If the first list item starts with a noun phrase ("Database connection timeout"), all items should start with noun phrases. If the first item is an imperative verb ("Check the database connection"), all items should be imperative verbs. Mixing structures within one vertical list violates Rule 6.3 (consistency in procedural lists) and makes the list harder to scan.

### The Colon Versus the Em-Dash in List Introductions

Some writers use an em-dash (—) instead of a colon to introduce a vertical list. In standard English, this is a stylistic choice. In STE-Code, only the colon is approved for vertical list introductions. The em-dash is reserved for parenthetical asides and emphasis — it does not function as a sentence boundary in the STE-Code punctuation model.

If you encounter a vertical list introduced by an em-dash, replace the em-dash with a colon. Count the words in the introduction as usual. The replacement is mechanical and does not require rewriting the introduction.

### Historical Context and Domain Origins

The ASD-STE100 vertical list rule (Rule 8.4 in the original specification) was designed for technical manuals, where a vertical list of components, tools, or steps is the primary documentation format. The colon divides the procedural context ("To remove the pump, disconnect these hoses:") from the actionable items. The word-count limit prevents the context from overwhelming the items.

In code documentation, the same principle applies with different nouns. Instead of "hoses" and "pumps," the list enumerates parameters, return values, exceptions, dependencies, or steps. The structural need is identical: a short context-setter followed by a scannable list of items. The rule has been tested in high-stakes operational environments where misreading a list item causes real harm. In software, the stakes are lower but the readability benefit is the same.

## See Also

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs

> **See also:** Rule 1.3 — Use Approved Words Only with Their Approved Meanings

> **See also:** Rule 3.1 — Use only the verb forms that are given in the dictionary.

> **See also:** Rule 3.3 — Use the past participle form as an adjective.

> **See also:** Rule 4.1 — One Topic Per Sentence, No Abstract Text

> **See also:** Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence.

> **See also:** Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon (;)

---

<!-- a-sec8-rule8.5.md -->

# Rule 8.5 — Parentheses and Word Count

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.5

> **Source:** [master.md#sec8-rule8.5](ste-code/grouped/)

## Original Rule

**Rule 8.5** When you put text in parentheses, it counts as one word in that sentence.

When you count words for sentence length, text in parentheses counts as one word of that sentence. But the words that you put between parentheses also make a new sentence. Thus, count them in that different sentence.

> **STE:** Make sure that the EMER pushbutton switch is released (the EMER legend is off).

(This sentence has 10 words, because the text in parentheses counts as one word. The sentence in parentheses has 5 words and counts as a different sentence.)

If there is an identifier in parentheses (a number, a letter, or an alphanumeric identifier), this identifier counts as one word in the sentence. Abbreviations in parentheses also count as one word.

> **STE:** Remove the safety pin (10). (5 words)
> **STE:** Installation of a Business Class (B/C) Seat (7 words)

| Example | Text |

|---------|------|

| | Hardware and Software Configuration Check of the In-Flight Entertainment (IFE) System (11 words) |

## STE-Code Adaptation

**Rule 8.5** In code documentation, when you put text in parentheses, it counts as one word in that sentence.

When you count words for sentence length, text in parentheses counts as one word of that sentence. But the words that you put between parentheses also make a new sentence. Thus, count them in that different sentence.

If there is an identifier in parentheses (a number, a letter, or an alphanumeric identifier), this identifier counts as one word in the sentence. Abbreviations in parentheses also count as one word.

### Examples

> *Adapted from spec pair:* Non-STE: n/a (source rule is illustrative)  |  STE: Make sure that the EMER pushbutton switch is released (the EMER legend is off). — Remove the safety pin (10). — Installation of a Business Class (B/C) Seat

> **Non-STE:** Make sure that the DEBUG environment variable is set to false before you run the deployment script in the production cluster (the DEBUG flag must be explicitly disabled for all production workloads to prevent accidental log leakage).
>
> **STE:** Make sure that the DEBUG environment variable is set to false (the DEBUG flag is off). (12 words)
>
> *Adapted from spec pair: "Make sure that the EMER pushbutton switch is released (the EMER legend is off)." — text in parentheses counts as one word in the main sentence but forms a separate sentence.*

(This sentence has 12 words, because the text in parentheses counts as one word. The sentence in parentheses has 5 words and counts as a different sentence.)

Realistic code-domain anchor — a deployment runbook step:

````
# deploy.sh (excerpt)
# WRONG: the aside buries a production safety rule inside parentheses
export DEBUG=false (set DEBUG to false on all production hosts to stop log leakage)

# RIGHT
export DEBUG=false
# The DEBUG flag is off on all production hosts.
````

> **Non-STE:** Remove the health check flag number ten from the deployment configuration.
>
> **STE:** Remove the health check flag (10). (5 words)
>
> *Adapted from spec pair: "Remove the safety pin (10)." — identifier in parentheses counts as one word.*

Realistic code-domain anchor — a config schema comment:

````
# config.yaml (excerpt)
# WRONG
# remove the health check flag number ten from the deployment configuration
health_check_flag: 10

# RIGHT
# Remove the health check flag (10).
health_check_flag: 10
````

> **Non-STE:** Installation and Configuration of a Continuous Integration and Continuous Deployment Pipeline for the Application
>
> **STE:** Configuration of a Continuous Integration/Continuous Deployment (CI/CD) Pipeline (7 words)
>
> *Adapted from spec pair: "Installation of a Business Class (B/C) Seat" — abbreviation in parentheses counts as one word.*

Realistic code-domain anchor — a README heading and intro line:

````
# WRONG
# Installation and Configuration of a Continuous Integration and Continuous Deployment Pipeline for the Application

# RIGHT
# Configuration of a Continuous Integration/Continuous Deployment (CI/CD) Pipeline
````

## Code-Domain Explanation

Rule 8.5 governs how parenthetical text affects word counting in all code documentation. The rule has two parts: (1) the parenthetical block counts as exactly one word in the enclosing sentence, and (2) the words inside the parentheses form their own separate sentence with its own word-count limit. This dual counting system lets you add clarifying asides without inflating the word count of the main sentence, while still enforcing brevity on the aside itself.

The most important practical effect of Rule 8.5 is that parentheses become a tool for managing sentence length. When a sentence approaches the 20-word procedural limit or the 25-word descriptive limit, moving qualifying information into parentheses reduces the main sentence's word count by the length of the moved text minus one. This is not a loophole — it is the intended mechanism. The parenthetical text remains subject to the same length limits as any other sentence. A parenthetical with 30 words violates the spirit of the rule even though the main sentence gains only one word.

A secondary effect is that parentheses create a hierarchy of attention. The main sentence carries the primary message. The parenthetical carries secondary or clarifying information. A reader who skips the parenthetical should still understand the main sentence. If the parenthetical contains information that the reader must act on, that information belongs in the main sentence, not in parentheses.

### README Files

README files use parentheses for version qualifications, platform notes, and dependency clarifications. A common violation: the writer puts long conditional instructions inside parentheses, creating a parenthetical sentence that far exceeds the 25-word descriptive limit. The parenthetical becomes a second paragraph hidden inside the first.

Example of a parenthetical violation in a README installation section:

````
Install the package with pip (if you are using a virtual environment
which we strongly recommend for all Python projects to avoid dependency
conflicts with system-level packages, make sure you activate it first
with the source venv/bin/activate command before running the install).
````

The parenthetical has 35 words — 10 over the descriptive limit. The fix splits the aside into its own sentence or moves it before the instruction:

````
We recommend that you use a virtual environment. Activate it with the
`source venv/bin/activate` command. Then install the package with pip.
````

### API Documentation

API documentation uses parentheses for HTTP status codes, content types, default values, and optionality markers. These parenthetical identifiers (200, 404, application/json, optional) count as one word each. They do not inflate the word count of endpoint descriptions.

A common violation: the writer uses parentheses to embed full conditional logic inside a parameter description. The parenthetical describes when the parameter is required, what it defaults to, and how it interacts with other parameters — all inside one pair of parentheses.

Example of a violation in an API parameter description:

````
The timeout parameter sets the request timeout in seconds (this
parameter is optional and defaults to 30 if not provided, but if
you set retries to a value greater than zero you should increase
the timeout accordingly to account for the cumulative wait time
across all retry attempts).
````

The parenthetical is 43 words. The fix moves the conditional guidance to a separate paragraph or a NOTE:

````
The timeout parameter sets the request timeout in seconds. The
default value is 30. This parameter is optional.

NOTE: If you set retries to a value larger than zero, increase the
timeout to account for the cumulative wait time.
````

### Docstrings and Inline Comments

Docstrings use parentheses for type annotations in some formats, default value indicators, and short clarifications about parameter behavior. Parentheses in docstrings are usually short — `(int, optional)`, `(default: 30)`, `(in seconds)` — and trivially comply with Rule 8.5.

The risk appears when a docstring uses parentheses to embed a full algorithmic explanation or a caution about side effects. The writer tries to keep the docstring concise by parenthesizing the complex part, but the parenthetical itself becomes a dense paragraph.

Example of a violation in a Python docstring:

````
def connect(timeout: int) -> Connection:
    """Open a connection to the database server.

    The timeout parameter controls how long the client waits for a
    response (this timeout applies to the initial TCP handshake only
    and does not cover query execution time, which is controlled by
    the separate query_timeout parameter on the Connection object
    returned by this function).
    """
````

The parenthetical is 32 words. The fix makes it a separate sentence or a separate paragraph:

````
def connect(timeout: int) -> Connection:
    """Open a connection to the database server.

    The timeout parameter controls how long the client waits for the
    initial TCP handshake. It does not cover query execution time.
    Use the query_timeout parameter on the returned Connection object
    to control query execution time.
    """
````

### Commit Messages

Commit messages use parentheses for issue tracker references, breaking change indicators, and scope qualifiers. These are almost always identifiers: `(#1234)`, `(breaking)`, `(auth)`. As identifiers, they count as one word each.

A common violation in longer commit message bodies: the writer uses parentheses to add retrospective commentary or justification for the change. This commentary belongs in the commit body as a separate paragraph, not in parentheses.

Example of a violation in a commit message body:

````
This commit removes the deprecated User.findByEmail method (this
method was deprecated in v2.1 and had a known bug where it returned
stale results from the cache when the underlying database record
had been updated by another process, which caused several production
incidents in the billing service).
````

The parenthetical has 41 words. The fix separates the justification:

````
This commit removes the deprecated User.findByEmail method.

This method was deprecated in v2.1. It had a known bug: it returned
stale cache results when another process updated the database record.
This bug caused production incidents in the billing service.
````

### Error Messages

Error messages use parentheses for error codes, suggested actions, and contextual data. These are usually short: `(Error code: EACCES)`, `(try: chmod 600)`, `(file: config.yaml)`. Each parenthetical is a separate sentence and must stay under the word-count limit.

A common violation: the error message puts the entire recovery procedure in parentheses, creating a procedural parenthetical that exceeds 20 words. Recovery instructions should be separate sentences, not parenthetical asides.

Example of a violation in a CLI error message:

````
Error: Cannot write to the configuration file (check that the file
exists and is not read-only, that the parent directory is writable,
and that your user account has the necessary file permissions — you
can use the ls -l command to inspect permissions and chmod to change
them if you have sufficient privileges).
````

The parenthetical is 46 words. The fix:

````
Error: Cannot write to the configuration file.

To fix this problem:
- Make sure that the file exists.
- Make sure that the file is not read-only.
- Make sure that the parent directory is writable.
- Make sure that your user account has the necessary permissions.

Use the `ls -l` command to inspect permissions. Use the `chmod`
command to change them.
````

## Paradigm-Specific Guidance

### Object-Oriented Paradigm (Java, C++, C#, Python classes)

In OOP documentation, parentheses appear most often around type names, class references, and design pattern qualifiers. These are identifier parentheses and count as one word each: `(User)`, `(abstract)`, `(Factory pattern)`.

A common OOP-specific violation: the writer uses parentheses to embed inheritance justifications or interface contract explanations inside class-level docstrings. The parenthetical describes why a class extends another class or implements an interface in a specific way. This design rationale belongs in a separate paragraph, not in a parenthetical aside.

> **Non-STE:** A Java class docstring that embeds the inheritance justification in parentheses:
> ```java
> /**
>  * The CachingUserRepository extends the BaseRepository class and
>  * implements the UserRepository interface (the BaseRepository provides
>  * generic CRUD operations with connection pooling, and UserRepository
>  * adds user-specific query methods — we extend rather than compose
>  * because the caching layer needs access to protected connection
>  * management methods on BaseRepository).
>  */
> public class CachingUserRepository extends BaseRepository
>         implements UserRepository {
>     // ...
> }
> ```
>
> **STE:** Move the design rationale to its own paragraph:
> ```java
> /**
>  * The CachingUserRepository extends the BaseRepository class. It
>  * implements the UserRepository interface.
>  *
>  * The BaseRepository class provides generic CRUD operations with
>  * connection pooling. The UserRepository interface adds user-specific
>  * query methods. This class extends BaseRepository rather than
>  * composing it. The caching layer needs access to protected
>  * connection management methods.
>  */
> public class CachingUserRepository extends BaseRepository
>         implements UserRepository {
>     // ...
> }
> ```
>
> *Principles applied: Rule 8.5 (the parenthetical is an explanatory aside that violates the sentence limit; the fix makes it a separate paragraph), Rule 3.3 (keep paragraphs short).*

### Functional Paradigm (Haskell, Elixir, Clojure, Rust)

In functional documentation, parentheses appear around type parameters, pattern match conditions, and guard clauses. These are often short and trivially compliant: `(Eq a)`, `(when x > 0)`, `(:else)`.

A functional-specific violation: the writer uses parentheses to embed a full explanation of a monadic transformation or a lazy evaluation behavior inside a function description. Functional paradigms favor composition and transformation chains — writers sometimes try to parenthesize the entire chain description.

> **Non-STE:** A Rust docstring that buries the transformation chain in parentheses:
> ```rust
> /// The transform function applies a series of operations to the input
> /// stream (it first filters out all None values using filter_map, then
> /// converts each remaining value through the provided mapper function,
> /// and finally collects the results into a Vec — the entire chain is
> /// lazy and does not allocate until collect is called at the end).
> pub fn transform(input: impl Iterator<Item = Option<i32>>,
>                  mapper: impl Fn(i32) -> i32) -> Vec<i32> {
>     // ...
> }
> ```
>
> **STE:** Move the chain description to its own paragraph:
> ```rust
> /// The transform function applies a series of operations to the input
> /// stream.
> ///
> /// The function does these steps:
> /// - Remove all None values with filter_map.
> /// - Convert each remaining value with the mapper function.
> /// - Collect the results into a Vec.
> ///
> /// The chain is lazy. It does not allocate until collect is called.
> pub fn transform(input: impl Iterator<Item = Option<i32>>,
>                  mapper: impl Fn(i32) -> i32) -> Vec<i32> {
>     // ...
> }
> ```
>
> *Principles applied: Rule 8.5 (the parenthetical is an explanatory aside; the fix splits it into a list and a separate sentence), Rule 3.1 (use simple sentences).*

### Procedural Paradigm (C, Go, Bash)

In procedural documentation, parentheses appear around exit codes, flag values, and short condition qualifiers: `(exit code 1)`, `(-v)`, `(if root)`. These are identifier parentheses and count as one word.

A procedural-specific violation: the writer uses parentheses to embed error-handling logic inside a step description. The parenthetical describes the full if-else branching for an error condition. Procedural documentation should use separate sentences or a NOTE block for error handling.

> **Non-STE:** A Go docstring that embeds error branching in parentheses:
> ```go
> // WriteConfig saves the application configuration to the specified
> // file path (if the file already exists, the function returns an
> // ErrExists error and the caller must check for this error and decide
> // whether to overwrite by calling WriteConfigForce or to abort — if
> // the parent directory does not exist, the function creates it with
> // 0755 permissions before writing).
> func WriteConfig(path string, cfg Config) error {
>     // ...
> }
> ```
>
> **STE:** Separate the error conditions into their own sentences:
> ```go
> // WriteConfig saves the application configuration to the specified
> // file path.
> //
> // If the file exists, the function returns an ErrExists error. The
> // caller must check for this error. To overwrite the file, call
> // WriteConfigForce. To abort, return the error.
> //
> // If the parent directory does not exist, the function creates it with
> // 0755 permissions.
> func WriteConfig(path string, cfg Config) error {
>     // ...
> }
> ```
>
> *Principles applied: Rule 8.5 (the parenthetical is an explanatory aside that breaches the procedural limit; the fix promotes each branch to its own sentence), Rule 4.1 (keep sentences short).*

### Declarative Paradigm (SQL, Terraform, Kubernetes YAML)

In declarative documentation, parentheses appear around allowed values, validation constraints, and version qualifiers: `(PostgreSQL 14+)`, `(required)`, `(default: true)`. These are short and usually compliant.

A declarative-specific violation: the writer uses parentheses to embed migration instructions or backward-compatibility notes inside a resource property description. Declarative configurations often evolve across versions, and the writer tries to capture the full evolution history in a parenthetical.

> **Non-STE:** A Terraform variable description that embeds the migration history in parentheses:
> ```hcl
> variable "schema_version" {
>   description = "The schema_version variable sets the database schema version (in
>   version 1.x of this module the default was \"13\" but in version 2.x
>   the default changed to \"15\" — if you are upgrading from 1.x you
>   must run the database migration script before changing this value
>   to avoid data loss, and you should also update the parameter group
>   family to match the new schema version)."
>   type        = string
> }
> ```
>
> **STE:** Move the breaking-change note to its own block:
> ```hcl
> variable "schema_version" {
>   description = "The schema_version variable sets the database schema version. The
>   default value is \"15\".
>
>   BREAKING: The default value changed from \"13\" in version 1.x to
>   \"15\" in version 2.x. Before you change this value during an upgrade,
>   run the database migration script. Also update the parameter group
>   family to match the new version."
>   type        = string
> }
> ```
>
> *Principles applied: Rule 8.5 (the parenthetical is an explanatory aside that exceeds the limit; the fix moves it out of parentheses), Rule 3.3 (keep paragraphs short).*

### Systems Paradigm (Rust ownership docs, C memory docs)

In systems documentation, parentheses appear around safety preconditions, lifetime constraints, and UB (Undefined Behavior) qualifiers. These are safety-critical. A parenthetical that buries a safety precondition is a parenthetical that a developer might skip — and skipping a safety precondition in systems code can cause memory corruption.

The systems-specific rule is stricter than the general rule: do not put safety-critical information in parentheses. Put it in the main sentence or in its own `# Safety` section. Parentheses in systems documentation should contain only secondary clarifications, never preconditions.

> **Non-STE:** A Rust unsafe docstring that buries the safety contract in parentheses:
> ```rust
> /// The set_ptr function writes a value to the memory location that
> /// the pointer refers to (the caller must ensure that the pointer is
> /// valid for writes, that it is properly aligned for type T, and that
> /// no other thread holds a reference to the same memory location
> /// during the write — violating any of these conditions causes
> /// undefined behavior).
> ///
> /// # Safety
> /// (none)
> pub unsafe fn set_ptr<T>(ptr: *mut T, value: T) {
>     // ...
> }
> ```
>
> **STE:** Promote the safety contract out of parentheses into its own section:
> ```rust
> /// The set_ptr function writes a value to the memory location that the
> /// pointer refers to.
> ///
> /// # Safety
> ///
> /// The caller must obey these conditions:
> /// - The pointer must be valid for writes.
> /// - The pointer must be properly aligned for type T.
> /// - No other thread must hold a reference to the same memory location
> ///   during the write.
> ///
> /// If any of these conditions is not obeyed, the behavior is undefined.
> pub unsafe fn set_ptr<T>(ptr: *mut T, value: T) {
>     // ...
> }
> ```
>
> *Principles applied: Rule 8.5 (no parenthetical used for safety information), Rule 3.1 (use simple sentences for each precondition).*

## Extended Examples

### Example 4 — README: Version-Dependent Instruction

> **Non-STE:** Run the database migration script to upgrade your schema (if you are currently running version 2.3.x or earlier you must first apply the intermediate migration for version 2.4 because the 2.5 migration depends on schema changes that were introduced in the 2.4 release cycle and cannot be applied directly to a pre-2.4 database without causing migration failures and potential data corruption).
>
> **STE:** Run the database migration script. If you use version 2.3.x or earlier, apply the version 2.4 migration first (the 2.5 migration needs schema changes from version 2.4). (12 words in the main sentence, 7 words in the parenthetical)
>
> *Principles applied: P3 (use words with approved meanings — "needs" instead of "depends on"), Rule 8.5 (the parenthetical counts as one word in the second sentence and forms a separate 7-word sentence). The original parenthetical was 57 words and buried a data-corruption warning. The fix splits the instruction into two sentences and uses a short parenthetical for the rationale.*

### Example 5 — API Documentation: Status Code Parentheses

> **Non-STE:** A successful deletion operation returns an HTTP 204 No Content response with an empty body and no further information about the deleted resource (if the resource was already deleted or never existed the endpoint returns 404 Not Found to maintain idempotency guarantees, and if the caller does not have delete permissions on the parent collection the endpoint returns 403 Forbidden).
>
> **STE:** A successful deletion returns an HTTP 204 status code (No Content). The response body is empty. If the resource was already deleted, the endpoint returns 404 (Not Found). If the caller does not have delete permissions, the endpoint returns 403 (Forbidden).
>
> *Principles applied: P1 (use "successful" instead of "returns successfully"), Rule 8.5 (each status code explanation in parentheses counts as one word in its sentence and forms a separate sentence). The original used one sentence with a 54-word parenthetical that described three different response scenarios. The fix separates each scenario into its own sentence with short parenthetical status code names.*

### Example 6 — Docstring: Default Value with Condition

> **Non-STE:** The cache_ttl parameter (which controls how many seconds cached entries remain valid before they are automatically evicted by the background cleanup worker that runs every 60 seconds by default) accepts any positive integer value greater than zero.
>
> **STE:** The cache_ttl parameter sets the cache time-to-live in seconds (default: 300). The value must be a positive integer. A background worker removes expired entries (the worker runs every 60 seconds).
>
> *Principles applied: Rule 8.5 (each parenthetical counts as one word and forms a separate sentence), P2 (the word "set" replaces "controls" — approved word from the STE-Code dictionary). The original had a 31-word parenthetical embedded in the middle of the parameter description. The fix uses three sentences with two short parentheticals (3 words and 4 words).*

### Example 7 — Commit Message: Issue Reference

> **Non-STE:** Fix the race condition in the connection pool that caused sporadic test failures in CI when multiple test workers tried to acquire connections simultaneously during high-load periods on shared CI runners (this issue was reported by the QA team in ticket PROJ-2847 and was initially thought to be a test environment problem but turned out to be a genuine concurrency bug in the pool implementation that only manifested under specific timing conditions).
>
> **STE:** Fix a race condition in the connection pool (PROJ-2847). The bug caused test failures when many workers acquired connections at the same time on shared CI runners.
>
> *Principles applied: Rule 8.5 (the issue reference "PROJ-2847" is an alphanumeric identifier in parentheses — counts as one word, forms a 1-word separate sentence), P5 (technical code nouns like "connection pool" and "CI runners" are allowed). The original had a 57-word parenthetical with investigative history. The fix moves the issue reference to a short parenthetical and separates the description.*

### Example 8 — Error Message: Error Code with Recovery Hint

> **Non-STE:** Failed to bind to port 8080 because the address is already in use by another process that was started previously and is still holding the socket open on that port number (you can identify the process using the lsof -i :8080 command and then stop it with kill followed by the process ID, or you can configure this application to use a different port by setting the PORT environment variable to an alternative value such as 3000 or 9090 before restarting).
>
> **STE:** Cannot bind to port 8080 (EADDRINUSE). The address is in use. To find the process, run `lsof -i :8080`. To use a different port, set the PORT environment variable (example: 3000). Then restart the application.
>
> *Principles applied: Rule 8.5 (the error code "EADDRINUSE" in parentheses counts as one word, the example value "3000" in parentheses counts as one word), P1 (use "cannot" instead of "failed to" — approved word). The original had a 71-word parenthetical containing both diagnostic and recovery instructions. The fix separates the error identification, diagnostic step, and recovery steps into distinct sentences with short parenthetical identifiers.*

### Example 9 — Configuration File Comment: Allowed Range

> **Non-STE:** The max_connections setting controls the upper limit of simultaneous database connections that the application will open (the valid range for this value is between 10 and 1000 inclusive because values below 10 can cause connection starvation under normal load and values above 1000 can exhaust the database server's connection limit which is typically configured to 1000 by default in most PostgreSQL installations unless the system administrator has adjusted the max_connections server parameter).
>
> **STE:** The max_connections setting controls the largest number of simultaneous database connections. The valid range is 10 to 1000 (inclusive). Values below 10 can cause connection starvation. Values above 1000 can exhaust the database server limit.
>
> *Principles applied: Rule 8.5 (the qualifier "(inclusive)" counts as one word), P2 (use "largest" instead of "upper limit" — approved adjective form). The original had a 55-word parenthetical that embedded the full range rationale. The fix breaks the rationale into separate sentences and uses a one-word parenthetical for the range qualifier.*

## Edge Cases

### Edge Case 1 — When a Function Call Name Looks Like a Parenthetical

Code documentation often includes function names followed by parentheses: `authenticate()`, `parse(input)`, `User.find(id)`. In prose documentation, these function-call notations use parentheses as part of the code token, not as STE-Code parenthetical boundaries. A code token inside backticks that contains parentheses (`authenticate()`) counts as one word total. The parentheses inside the token do not create a separate sentence.

Guidance: Backtick-delimited code tokens are atomic. A token like `setTimeout(callback, 1000)` is one word regardless of its internal parentheses. Only parentheses that appear outside backticks in the documentation prose trigger Rule 8.5 counting.

> **STE:** Call the `authenticate()` function. Then call `validate(token)`. (6 words)

> *The parentheses inside the backtick-delimited code tokens are part of the token, not Rule 8.5 parentheticals. The sentence has six prose words. The code tokens count as one word each.*

### Edge Case 2 — When Parentheses Contain a URL

Documentation sometimes places a URL in parentheses: `(https://example.com/docs)`. A URL is a single identifier for word-count purposes — it counts as one word. The URL does not need to obey the 20/25-word limit as a separate sentence because it is an identifier, not a prose sentence. This is consistent with the rule for alphanumeric identifiers in parentheses.

Guidance: Treat URLs in parentheses as identifiers. Count them as one word. Do not attempt to count the words inside the URL (slashes, dots, hyphens are not word boundaries). If the parenthetical contains both a URL and explanatory text, the explanatory text forms a sentence and must obey the word-count limit.

> **STE:** Read the deployment guide (https://example.com/deploy). (6 words)
> **STE:** Read the deployment guide (https://example.com/deploy — this guide has the full procedure). (6 words in the main sentence, 5 words in the parenthetical)

> *In the first example, the URL alone is an identifier parenthetical (1 word). In the second example, the parenthetical contains text after the URL (5 words) and forms a separate sentence.*

### Edge Case 3 — Nested Parentheses

Standard English permits nested parentheses in some contexts, but they are difficult to parse. In code documentation, nested parentheses create ambiguity about which closing parenthesis ends which parenthetical. The reader must mentally pair the delimiters.

Guidance: Do not use nested parentheses in STE-Code documentation. If you have a parenthetical that itself needs a parenthetical, restructure the content. Use an em-dash for the inner aside, or move one level of the aside to a separate sentence.

> **Non-STE:** The function returns a Result type (which can be either Ok (containing the parsed value) or Err (containing a ParseError)).
>
> **STE:** The function returns a Result type. The Result is either Ok (containing the parsed value) or Err (containing a ParseError).
>
> *Principles applied: Rule 8.5 (each single-level parenthetical counts as one word), P3 (use approved meanings). The original had nested parentheses — the inner parentheticals "(containing the parsed value)" and "(containing a ParseError)" were nested inside an outer parenthetical. The fix eliminates one level by making the outer parenthetical a separate sentence.*

### Edge Case 4 — When a Library or Framework Name Contains Parentheses

Some library names or API method names include parentheses as part of their canonical spelling. For example, a test framework might have a method literally called `expect()` with the parentheses as part of the API name. When you write documentation about this method, the parentheses are part of the technical noun, not Rule 8.5 punctuation.

Guidance: When a framework or tool name includes parentheses as part of its identifier, place the name in backticks. The backtick-delimited token is atomic and counts as one word. If you must write the name without backticks (in a heading, for example), treat the parentheses as part of the identifier and count the entire name as one word.

> **STE:** The `expect()` method checks a value against a condition. (8 words)

> *The `expect()` token is one word. The parentheses are part of the method signature, not a Rule 8.5 parenthetical.*

### Edge Case 5 — When Parentheses Appear in Generated Documentation

Auto-generated documentation (OpenAPI/Swagger, JSDoc, Sphinx autodoc, `--help` output) often inserts parentheses around type information, default values, and optionality markers automatically: `timeout (int, optional)`, `port (default: 8080)`. These generated parentheticals are usually short and automatically compliant.

Guidance: When you author the source annotations that feed the generator, follow Rule 8.5 for any parentheticals you write manually. When the generator inserts its own parentheticals (type hints, defaults), accept the generated output. If the generator produces parentheticals that consistently exceed 25 words, the generator likely has a configuration bug — file an issue with the generator project.

For CLI `--help` output: argument parsers often append parenthetical defaults automatically (`--port PORT (default: 8080)`). You control the help text you write in the source code. You do not control the auto-appended parenthetical. Focus your compliance effort on the help text you author.

## Cross-References

- **Rule 1.5 — Technical Code Nouns Are Allowed:** When a parenthetical contains a code noun (a class name, a function name, a framework identifier), that noun is a technical noun and is permitted. The parenthetical counting rule still applies: the code noun in parentheses counts as one word in the main sentence and as a one-word separate sentence. Example: `(UserRepository)` counts as one word.

- **Rule 1.6 — Non-Approved Words Only as Technical Code Nouns:** If a parenthetical contains a word that is not in the STE-Code dictionary, that word must be a technical code noun. Do not use parentheticals as a backdoor for non-approved descriptive words. The parenthetical's separate-sentence status does not exempt it from the approved-word rules.

- **Rule 3.1 — Use Simple Sentences:** A parenthetical counts as a separate sentence under Rule 8.5. That separate sentence must also obey Rule 3.1: one subject, one verb, one object. Do not put a complex multi-clause sentence inside parentheses. The parenthetical is a sentence, not a paragraph.

- **Rule 3.3 — Keep Paragraphs Short:** Parentheticals that grow beyond 15-20 words often indicate that the paragraph should be restructured. A long parenthetical is a sign that the paragraph has too many ideas. Split the parenthetical into its own sentence or paragraph. Rule 3.3 and Rule 8.5 work together: if the parenthetical is long enough to violate paragraph length norms, restructure.

- **Rule 4.1 — Keep Sentences Short:** The word-count limits (20 procedural, 25 descriptive) apply to the parenthetical sentence just as they apply to the main sentence. A parenthetical with 30 words violates Rule 4.1 for that separate sentence. Check the word count of every parenthetical against its sentence type.

- **Rule 8.1 — Do Not Use the Semicolon:** A semicolon inside a parenthetical is still a semicolon and is still forbidden. Do not use parentheses as a container for semicolon-joined clauses. If a parenthetical contains a semicolon, split it into two sentences. Consider whether the content even belongs in parentheses — semicolons in a parenthetical suggest the aside is too complex for its parenthetical form.

- **Rule 8.4 — Colon in a Vertical List:** A vertical list item can contain a parenthetical, and a parenthetical can contain a vertical list (rare, but possible). When these two structures combine, count words according to both rules: the parenthetical counts as one word in the list item, and the words inside the parenthetical form a separate sentence (which may itself be a vertical list with its own colon boundary).

- **STE-Code Dictionary — Section: Punctuation:** The dictionary defines parentheses as punctuation marks that create a subordinate sentence. The subordinate sentence has its own word-count limit and its own sentence-type classification (procedural or descriptive). Consult the dictionary for the full punctuation model and how parentheses interact with periods, commas, and dashes.

## Grammar Notes

### The Parenthetical as a Subordinate Sentence

In standard English grammar, a parenthetical is an aside — a phrase or clause that interrupts the main sentence to add qualifying, explanatory, or illustrative information. The parenthetical can be a fragment (a noun phrase, a prepositional phrase) or a complete clause. Standard grammar does not assign parentheticals their own sentence status.

In STE-Code, a parenthetical is always a separate sentence. This is a stricter rule than standard English. The grammatical justification: the parenthetical contains a complete thought that the writer considered important enough to include. That thought deserves the same structural discipline as any other sentence. If the thought is not important enough to be a sentence, it is not important enough to be a parenthetical — delete it.

This means that every parenthetical must have its own grammatical integrity. A fragmentary parenthetical like "(the DEBUG flag is off)" is acceptable because it is a complete clause (subject: "the DEBUG flag," verb: "is," complement: "off"). A truly fragmentary parenthetical like "(off)" is borderline — it is an identifier-style parenthetical, not a prose sentence, and should be used only for flags, states, or short qualifiers.

### Identifier Parentheticals Versus Explanatory Parentheticals

Rule 8.5 distinguishes two categories of parentheticals: identifier parentheticals and explanatory parentheticals.

Identifier parentheticals contain a number, a letter, an alphanumeric code, or an abbreviation. These count as one word and do not need to obey the sentence-length limits because they are not prose sentences. Examples: `(10)`, `(EACCES)`, `(CI/CD)`, `(v2.1)`. An identifier parenthetical can be a single word or token without a verb.

Explanatory parentheticals contain prose that explains, qualifies, or adds context to the main sentence. These count as one word in the main sentence but form a full separate sentence that must obey the word-count limits. Examples: `(the DEBUG flag is off)`, `(the worker runs every 60 seconds)`, `(this guide has the full procedure)`. An explanatory parenthetical must be a grammatically complete clause with a subject and verb.

The boundary between the two categories can blur. A parenthetical like `(optional)` is usually an identifier (a status label). A parenthetical like `(this parameter is optional)` is an explanatory parenthetical. When in doubt, treat the parenthetical as explanatory and apply the word-count limit. It is better to enforce the limit unnecessarily than to let a long explanatory parenthetical slip through as an identifier.

### Parentheses Versus Em-Dashes

Standard English offers three punctuation marks for asides: parentheses, em-dashes, and commas. Each has a different degree of separation from the main sentence. Commas provide the weakest separation — the aside blends into the flow of the sentence. Em-dashes provide a medium separation — the aside is set off but still feels connected. Parentheses provide the strongest separation — the aside is visually and grammatically cordoned off.

In STE-Code, parentheses are the approved punctuation for asides that need a separate sentence. Em-dashes are permitted for emphasis and for asides that must remain integrated in the main sentence's flow. Commas should not be used for asides longer than a few words — use parentheses or em-dashes instead.

The choice between parentheses and em-dashes depends on whether the aside forms a complete thought. If the aside is a complete clause that could stand as its own sentence, use parentheses (and count the words as a separate sentence). If the aside is a short qualifying phrase that cannot stand alone, use em-dashes (and count the words as part of the main sentence).

> **STE (em-dash):** The server — a Node.js application — listens on port 3000. (10 words, the em-dash aside counts as part of the main sentence)
> **STE (parentheses):** The server listens on port 3000 (the server is a Node.js application). (6 words in the main sentence, 5 words in the parenthetical)

> *In the first version, the aside is a noun phrase and integrates into the main sentence. In the second version, the aside is a complete clause and becomes its own parenthetical sentence.*

### Word Counting Mechanics for Parentheticals

The mechanics of word counting under Rule 8.5:

- **Main sentence:** Count every word outside the parentheses. The parenthetical block — regardless of its internal word count — contributes exactly one word to the main sentence's total. The opening parenthesis and closing parenthesis are not words and do not add to the count.

- **Parenthetical sentence:** Count every word between the opening parenthesis and the closing parenthesis. This forms a separate sentence. Apply the sentence-type limit (20 procedural, 25 descriptive) based on the content of the parenthetical, not the content of the enclosing sentence. A parenthetical inside a procedural sentence can be descriptive if its content describes rather than instructs.

- **Multiple parentheticals in one sentence:** Each parenthetical counts as one word in the main sentence. Each parenthetical forms its own separate sentence. There is no limit on the number of parentheticals in one sentence, but more than two parentheticals in one sentence suggest the sentence is overloaded. Restructure.

- **Parentheticals at the end of a sentence:** When a parenthetical appears at the end of a sentence, the closing parenthesis is followed by the end punctuation. The end punctuation belongs to the main sentence, not the parenthetical. Example: `(...).` — the period ends the main sentence. Do not put a period inside the closing parenthesis before the end punctuation: `(...).` is correct; `(....).` is incorrect.

A tool can verify Rule 8.5 compliance mechanically: (1) find all text between matching parentheses that are not inside backtick-delimited code tokens, (2) count the words in the text outside the parentheses for the main sentence limit, (3) count the words between the parentheses for the separate-sentence limit, (4) flag any sentence that exceeds its type-specific limit.

### Avoid Using Parentheses to Hide Important Information

A common misuse of parentheses: the writer puts a critical precondition, warning, or requirement in parentheses because it does not fit smoothly into the main sentence. The parentheses downgrade the visual priority of the information. A reader scanning the documentation sees the parenthetical as secondary and may skip it.

If the information is important enough to include, it is important enough to be a main sentence. Use parentheses for clarifications, examples, and secondary qualifications. Never use parentheses for safety conditions, required steps, or warnings that the reader must act on.

> **Non-STE:** Call the deallocate function to free the memory (the pointer must not be null and must have been previously allocated by the allocate function — calling deallocate on a null pointer or an unallocated pointer causes undefined behavior).
>
> **STE:** Call the deallocate function to free the memory. The pointer must not be null. The pointer must have been allocated by the allocate function. If you call deallocate on a null pointer or an unallocated pointer, the behavior is undefined.
>
> *Principles applied: Rule 8.5 (no parenthetical used for safety information), P3 (use approved meanings). The original buried undefined behavior warnings in a parenthetical. The fix promotes each precondition to its own sentence.*

### Historical Context and Domain Origins

The ASD-STE100 parentheses rule (Rule 8.5 in the original specification) was designed for technical manuals, where parenthetical text often contains part numbers, tool identifiers, measurement values, and safety condition clarifications. The dual counting system ensures that a reader can read the main procedural sentence (counting the parenthetical as one word) without the parenthetical inflating the sentence length, while the parenthetical's internal text remains constrained to prevent burying critical information.

In a technical manual, a parenthetical like `(set the parameter to 50-55 Nm)` is an explanatory parenthetical that forms a separate procedural sentence. The reader reads the main step, then reads the parenthetical for the specific parameter. The word-count limit on the parenthetical prevents the parameter from being buried in a sea of text.

In code documentation, the same principle applies with different nouns. Instead of measurement values, the parenthetical contains error codes, default values, version numbers, and rationale. The structural need is identical: the main sentence carries the action or description, and the parenthetical carries the qualifying detail. The rule is a reminder that parentheticals are not dumping grounds — they are structured asides with their own sentence discipline.

The original rule also emphasizes that parentheses should not be used to hide information the reader must see. The same applies to code documentation: do not use parentheses to hide deprecation warnings, breaking change notices, or safety-critical conditions. These deserve their own sentences, their own paragraphs, or their own labeled blocks (BREAKING, DEPRECATED, NOTE).

## See also

> **See also:** Rule 1.5 — Technical Code Nouns Are Allowed
> **See also:** Rule 1.6 — Non-Approved Words Only as Technical Code Nouns
> **See also:** Rule 3.1 — Use Simple Sentences
> **See also:** Rule 3.3 — Keep Paragraphs Short
> **See also:** Rule 4.1 — Keep Sentences Short
> **See also:** Rule 8.1 — Do Not Use the Semicolon
> **See also:** Rule 8.4 — Colon in a Vertical List

---

<!-- a-sec8-rule8.6.md -->

# Rule 8.6 — Elements That Count as One Word

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.6

> **Source:** [master.md#sec8-rule8.6](ste-code/grouped/)

## Original Rule

**Rule 8.6** Count each of these elements as one word:

- Numbers
- Numbers together with units of measurement
- Abbreviations
- Alphanumeric identifiers
- Quoted text
- Titles, headings, and text on placards and labels
- Proper nouns of individuals, groups, organizations, and geopolitical entities.

When you count words for sentence length, count each of these as one word:

1. Numbers

   > **STE:** Do steps 13 thru 16 a minimum of three times. (10 words)

   ("13" and "16" are numbers and each of them counts as one word.)

   > **STE:** The spar box has twenty-one ribs. (6 words)

   ("Twenty-one" is a number and counts as one word.)

   Do not count numbers that identify paragraphs or work steps. These numbers are usually part of the document numbering systems.

2. Numbers together with units of measurement

   Units of measurement usually follow their related number (for example, 10 mA). When you write a number together with its unit of measurement, count them as one word.

   > **STE:** Make sure that the temperature in the room is 10 °C. (10 words)
   > **STE:** Make sure that the temperature in the room is 10 degrees Celsius. (10 words)
   > **STE:** The unit weighs 20 kg. (4 words)
   > **STE:** The unit weighs 20 kilograms. (4 words)
   > **STE:** The resistance must be 10 Ω. (5 words)
   > **STE:** The resistance must be 10 ohms. (5 words)

3. Abbreviations

   In technical texts, you can use abbreviations (also acronyms and initialisms) to make sentences shorter and easier to read. But these abbreviations only help the reader if the reader knows their meanings. Each abbreviation counts as one word.

   > **STE:** The maintenance team does a test of this system each day at 10 a.m. (13 words)

   ("a.m." is an abbreviation and counts as one word together with its number.)

   > **STE:** During this safety check, obey NASA protocols. (7 words)

   (NASA is an abbreviation (acronym) and counts as one word.)

   > **STE:** For remote access, use the VPN. (6 words)

   (VPN is an abbreviation (initialism) and counts as one word.)

4. Alphanumeric identifiers

   An alphanumeric identifier is a combination of letters and numbers that identifies something. Each alphanumeric identifier counts as one word.

   > **STE:** Examine the No. 1 bearing installation. (5 words)

   ("No. 1" is an alphanumeric identifier and counts as one word.)

   > **STE:** Tag circuit breaker 36L7. (4 words)

   ("36L7" is an alphanumeric identifier and counts as one word.)

5. Quoted text

   Quoted text is usually given in quotation marks ("..."). Words between quotation marks count as one word in a sentence. In some sentences, or parts of the document, uppercase letters or differences in font can also show quoted text. Such text also counts as one word.

   Examples in STE:

   > **STE:** Touch the "Service Overview" arrow to select the function page. (9 words)

   ("Service Overview" is quoted text and counts as one word.)

   > **STE:** Release the SHORT-CIRCUIT TEST switch. (4 words)

   (SHORT-CIRCUIT TEST is quoted text and counts as one word.)

   > **STE:** C = (A - B) - 0.063 mm (1 word)

   (In STE, a formula is quoted text and counts as one word.)

6. Titles, headings, and text on placards and labels

   In some texts, there are words or groups of words that you cannot change. These are:

   - Titles and headings
   - Text on placards (for example, a warning notice in a work area or public place)
   - Text on labels (for example, warning and caution labels that are attached to objects).

   Examples in STE:

   > **STE:** Before you start a repair, refer to the Structural Repair Manual for the applicable safety procedures and precautions. (16 words)

   ("Structure Repair Manual" is the title of the document and counts as one word.)

   > **STE:** Refer to Testing and Fault Isolation, page block 1001. (6 words)

   ("Testing and Fault Isolation" is the title of a section in a manual and counts as one word.)

   > **STE:** Refer to Requirements after Job Completion for the applicable procedures. (7 words)

   ("Requirements after Job Completion" is a heading in a data module and counts as one word.)

   > **STE:** This procedure is for the inspection of SSI No. 57-21-16, "Outer wing bottom skin lower surface spanwise skin joints at stringer 13 and stringer 20 between Rib 12 and Rib 27 excluding areas covered by flap track fairings 3, 4, and 5." (9 words)

   ("This procedure is for the inspection of" has 7 words. "SSI No. 57-21-16" is the reference number of the Structurally Significant Item (SSI) and counts as one word. The subsequent text given in quotation marks is the title of the SSI. It is not in STE, and it is not possible to change it. Thus, this text counts as one word. As a result, the full sentence has a total of 9 words.)

   > **STE:** "Interior hazards exist to such a degree that interior operations may be conducted only after full examination, and with extreme caution." (1 word)

   (The text given in quotation marks is not in STE. It comes from a placard, and it is not possible to change it. It counts as one word.)

   > **STE:** "FRAGILE - Please handle with care." (1 word)

   (The text given in quotation marks is not in STE. It comes from a label on shipping containers, and it is not possible to change it. It counts as one word.)

7. Proper nouns of individuals, groups, organizations, and geopolitical entities

   There are groups of words that you cannot change because they identify:

   - Individuals (for example, John Smith)
   - Groups or organizations (for example, World Health Organization)
   - Geopolitical entities (for example, Republic of Ireland).

   Examples in STE:

   > **STE:** The first president of the United States of America was George Washington. (8 words)

   ("United States of America" is the proper noun of a geopolitical entity and counts as one word. "George Washington" is a proper noun of an individual and counts as one word.)

   > **STE:** The owner of STE is the Aerospace, Security and Defence Industries Association of Europe. (7 words)

   ("Aerospace, Security and Defence Industries Association of Europe" is the proper noun of an organization and counts as one word.)

## STE-Code Adaptation

**Rule 8.6** In code documentation, count each of these elements as one word:

- Numbers
- Numbers together with units of measurement
- Abbreviations
- Alphanumeric identifiers
- Quoted text
- Titles, headings, and text on user interface elements and labels
- Proper nouns of individuals, groups, organizations, and geopolitical entities.

When you count words for sentence length, count each of these as one word:

1. Numbers

   > **STE:** Do steps 13 thru 16 a minimum of three times. (10 words)

   ("13" and "16" are numbers and each of them counts as one word.)

   > **STE:** The configuration file has twenty-one keys. (6 words)

   ("Twenty-one" is a number and counts as one word.)

   Do not count numbers that identify paragraphs or work steps. These numbers are usually part of the document numbering systems.

2. Numbers together with units of measurement

   Units of measurement usually follow their related number (for example, 10 ms). When you write a number together with its unit of measurement, count them as one word.

   > **STE:** Make sure that the timeout is 10 ms. (7 words)
   > **STE:** Make sure that the timeout is 10 milliseconds. (7 words)
   > **STE:** The payload is 20 MB. (4 words)
   > **STE:** The payload is 20 megabytes. (4 words)
   > **STE:** The latency must be 10 μs. (5 words)
   > **STE:** The latency must be 10 microseconds. (5 words)

3. Abbreviations

   In code documentation, you can use abbreviations (also acronyms and initialisms) to make sentences shorter and easier to read. But these abbreviations only help the reader if the reader knows their meanings. Each abbreviation counts as one word.

   > **STE:** The CI pipeline does a test of this module each day at 10 a.m. (13 words)

   ("a.m." is an abbreviation and counts as one word together with its number.)

   > **STE:** During this security check, obey OWASP guidelines. (7 words)

   (OWASP is an abbreviation (acronym) and counts as one word.)

   > **STE:** For remote access, use the VPN. (6 words)

   (VPN is an abbreviation (initialism) and counts as one word.)

4. Alphanumeric identifiers

   An alphanumeric identifier is a combination of letters and numbers that identifies something in code or documentation. Each alphanumeric identifier counts as one word.

   > **STE:** Examine the No. 1 handler installation. (5 words)

   ("No. 1" is an alphanumeric identifier and counts as one word.)

   > **STE:** Tag error code E36L7. (4 words)

   ("E36L7" is an alphanumeric identifier and counts as one word.)

5. Quoted text

   Quoted text is usually given in quotation marks ("..."). Words between quotation marks count as one word in a sentence. In code documentation, backtick-quoted text (`...`) and inline `<code>` text also count as quoted text. Uppercase letters or differences in font can also show quoted text. Such text also counts as one word.

   > **STE:** Touch the "Service Overview" button to select the function page. (9 words)

   ("Service Overview" is quoted text and counts as one word.)

   > **STE:** Release the SHORT-CIRCUIT TEST switch. (4 words)

   (SHORT-CIRCUIT TEST is quoted text and counts as one word.)

   > **STE:** `C = (A - B) - 0.063 mm` (1 word)

   (In STE-Code, a formula is quoted text and counts as one word.)

6. Titles, headings, and text on user interface elements and labels

   In some texts, there are words or groups of words that you cannot change. These are:

   - Titles and headings (for example, a document title or a section heading)
   - Text on user interface elements (for example, a button label, a menu item, or a dialog title)
   - Text on labels (for example, warning and caution labels that are shown in a web page or application).

   > **STE:** Before you start a deployment, refer to the Operations Runbook for the applicable safety procedures and precautions. (16 words)

   ("Operations Runbook" is the title of the document and counts as one word.)

   > **STE:** Refer to Error Handling and Recovery, page block 1001. (6 words)

   ("Error Handling and Recovery" is the title of a section in a manual and counts as one word.)

   > **STE:** Refer to Requirements after Job Completion for the applicable procedures. (7 words)

   ("Requirements after Job Completion" is a heading in a data module and counts as one word.)

   > **STE:** This procedure is for the inspection of API No. 57-21-16, "Rate limiter middleware integration with the gateway service across all regional edge nodes and the central traffic management controller excluding traffic routed through canary deployment slots." (9 words)

   ("This procedure is for the inspection of" has 7 words. "API No. 57-21-16" is the reference number of the API and counts as one word. The subsequent text given in quotation marks is the title of the API specification. It is not in STE-Code, and it is not possible to change it. Thus, this text counts as one word. As a result, the full sentence has a total of 9 words.)

   > **STE:** "Security vulnerability detected. Immediate administrator action required before system operations can resume." (1 word)

   (The text given in quotation marks is not in STE-Code. It comes from a user interface warning, and it is not possible to change it. It counts as one word.)

   > **STE:** "WARNING: This operation permanently deletes all user data." (1 word)

   (The text given in quotation marks is not in STE-Code. It comes from a label on a confirmation dialog, and it is not possible to change it. It counts as one word.)

7. Proper nouns of individuals, groups, organizations, and geopolitical entities

   There are groups of words that you cannot change because they identify:

   - Individuals (for example, John Smith)
   - Groups or organizations (for example, World Health Organization)
   - Geopolitical entities (for example, Republic of Ireland).

   > **STE:** The creator of Linux was Linus Torvalds. (6 words)

   ("Linus Torvalds" is a proper noun of an individual and counts as one word.)

   > **STE:** The maintainer of this library is the Apache Software Foundation. (7 words)

   ("Apache Software Foundation" is the proper noun of an organization and counts as one word.)

## Examples

> *Adapted from spec pair:* Non-STE: "The spar box has twenty-one ribs." | STE: "The configuration file has twenty-one keys." (number counts as one word) — and Non-STE: "During this safety check, obey NASA protocols." | STE: "During this security check, obey OWASP guidelines." (abbreviation counts as one word) — and Non-STE: "Before you start a repair, refer to the Structural Repair Manual for the applicable safety procedures and precautions." | STE: "Before you start a deployment, refer to the Operations Runbook for the applicable safety procedures and precautions." (document title counts as one word).

> **Non-STE:** The JSON Web Token authentication middleware must validate the signature of each incoming request using the public key obtained from the OpenID Connect identity provider, and the token must have an expiry time of not more than three hundred and sixty seconds to be valid for processing.
>
> **STE:** The JWT authentication middleware must validate the signature of each incoming request. The token must have an expiry time of not more than 360 seconds to be valid for processing. (11 words each)
>
> *Adapted from spec pattern: abbreviation counts as one word — "During this safety check, obey NASA protocols." — and number with unit counts as one word — "Make sure that the temperature in the room is 10 °C."*

("JWT" is an abbreviation and counts as one word. "360 seconds" is a number together with a unit of measurement and counts as one word.)

```python
# STE-Code compliant docstring for the split sentences above
def validate_token(token: "JWT", public_key: "RSAPublicKey") -> "bool":
    """Validate the signature of an incoming JWT.

    The token must have an expiry time of not more than 360 seconds
    to be valid for processing. Return True when the signature is
    valid and the token is not expired.
    """
    payload = decode(token, public_key, algorithms=["RS256"])
    return payload["exp"] - time.time() > 0
```

> **Non-STE:** Before you run the database migration script, refer to the document titled Migration Procedures and Rollback Strategies for PostgreSQL Version 15 Cluster Deployments for the applicable safety procedures and precautionary measures.
>
> **STE:** Before you run the migration, refer to the Migration Procedures and Rollback Strategies for the applicable safety procedures. (16 words)
>
> *Adapted from spec pair: "Before you start a repair, refer to the Structural Repair Manual for the applicable safety procedures and precautions." — document title counts as one word.*

("Migration Procedures and Rollback Strategies" is the title of the document and counts as one word.)

```sql
-- STE-Code compliant migration header comment
-- Before you run the migration, refer to the Migration Procedures
-- and Rollback Strategies for the applicable safety procedures.
BEGIN;
ALTER TABLE users ADD COLUMN last_login_at TIMESTAMPTZ;
COMMIT;
```

> **Non-STE:** To configure the retry behavior of the HTTP client you must open the file named application.properties which is located in the resources directory and then change the property called http.client.retry.max.attempts to a numeric value of five and also set the property http.client.retry.backoff.millis to a numeric value of one thousand so that the client will retry failed requests five times with a one second delay between each attempt.
>
> **STE:** In `application.properties`, set `http.client.retry.max.attempts` to 5. Set `http.client.retry.backoff.millis` to 1000. The client retries failed requests 5 times with a 1 second delay. (11 words, 11 words, 14 words)
>
> *Adapted from spec pair: "Make sure that the timeout is 10 ms." (number with unit counts as one word) and "Tag circuit breaker 36L7." (alphanumeric identifier counts as one word).*

(The file path in backticks is quoted text, 1 word. Each property name is an alphanumeric identifier, 1 word. "5", "1000", and "1 second" are numbers or numbers with units, 1 word each.)

```properties
# application.properties — STE-Code compliant config comments
http.client.retry.max.attempts=5
http.client.retry.backoff.millis=1000
```

> **Non-STE:** When the payment service raises an exception of the type PaymentGatewayTimeoutException with the error code ERR_PG_TIMEOUT_0099 because the downstream credit card processor did not respond within the configured threshold of thirty seconds, the order orchestrator must publish an event with the name OrderPaymentFailed and include the correlation identifier that was generated at the start of the request.
>
> **STE:** The `PaymentGatewayTimeoutException` with code `ERR_PG_TIMEOUT_0099` occurs when the processor does not respond in 30 seconds. The orchestrator publishes the `OrderPaymentFailed` event with the request correlation identifier. (15 words, 16 words)
>
> *Adapted from spec pair: "Tag circuit breaker 36L7." (alphanumeric identifier) and "During this safety check, obey OWASP guidelines." (proper noun / abbreviation).*

("PaymentGatewayTimeoutException" and "ERR_PG_TIMEOUT_0099" are alphanumeric identifiers, 1 word each. "OrderPaymentFailed" is a proper noun, 1 word. "30 seconds" is a number with a unit, 1 word.)

```java
// STE-Code compliant exception javadoc
/**
 * The PaymentGatewayTimeoutException with code ERR_PG_TIMEOUT_0099 occurs
 * when the processor does not respond in 30 seconds.
 */
public class PaymentGatewayTimeoutException extends RuntimeException {
    public static final String CODE = "ERR_PG_TIMEOUT_0099";
}
```

> **Non-STE:** The function which the developer must call in order to retrieve the current user profile from the React application programming interface is named useUserProfile and it accepts a single argument which is the unique identifier of the user and it returns an object which contains the display name, the email address, and the list of roles that have been assigned to that user.
>
> **STE:** Call `useUserProfile(userId)` to get the current user profile. It returns an object with the `displayName`, the `email`, and the `roles` list. (14 words, 13 words)
>
> *Adapted from spec pattern: "Touch the 'Service Overview' button to select the function page." (quoted identifier counts as one word) and "Examine the No. 1 handler installation." (alphanumeric identifier).*

("useUserProfile(userId)" is quoted text, 1 word. "displayName", "email", and "roles" are quoted identifiers, 1 word each.)

```typescript
// STE-Code compliant hook documentation
/**
 * Call useUserProfile(userId) to get the current user profile.
 * It returns an object with the displayName, the email, and the roles list.
 */
function useUserProfile(userId: string): UserProfile { /* ... */ }
```

> **Non-STE:** In the Kubernetes manifest file you should make sure that the container which runs the checkout service has its resource requests set to two hundred and fifty millicores of CPU and five hundred and twelve mebibytes of memory and its resource limits set to five hundred millicores of CPU and one gibibyte of memory so that the scheduler can place the pod on a node that has enough capacity.
>
> **STE:** In the Kubernetes manifest, set the `checkout` container to 250m CPU and 512Mi memory. Set the limit to 500m CPU and 1Gi memory. (15 words, 12 words)
>
> *Adapted from spec pair: "The unit weighs 20 kg." (number with unit counts as one word).*

("checkout" is quoted text, 1 word. "250m CPU", "512Mi", "500m CPU", and "1Gi" are numbers with units, 1 word each.)

```yaml
# checkout-deployment.yaml — STE-Code compliant manifest comment
# In the Kubernetes manifest, set the checkout container to 250m CPU
# and 512Mi memory. Set the limit to 500m CPU and 1Gi memory.
resources:
  requests:
    cpu: 250m
    memory: 512Mi
  limits:
    cpu: 500m
    memory: 1Gi
```

> **Non-STE:** The test suite must verify that when the cache layer returns a null value for a key that does not exist the repository implementation does not attempt to query the primary database and instead the method named getOrNull returns the value None and the test should also confirm that the recorded metric with the name cache.miss.count is increased by exactly one for each missing key.
>
> **STE:** The test must check that `getOrNull` returns `None` for a missing key. It must check that the `cache.miss.count` metric increases by 1 for each miss. (17 words, 16 words)
>
> *Adapted from spec pattern: "Tag circuit breaker 36L7." (alphanumeric identifier) and "C = (A - B) - 0.063 mm" (quoted text).*

("getOrNull" and "None" are quoted text, 1 word each. "cache.miss.count" is an alphanumeric identifier, 1 word. "1" is a number, 1 word.)

```go
// STE-Code compliant test comment
// The test must check that getOrNull returns None for a missing key.
// It must check that the cache.miss.count metric increases by 1 for each miss.
func TestGetOrNull_MissingKey(t *testing.T) {
    repo := NewCacheBackedRepository(emptyCache, primaryDB)
    if got := repo.getOrNull("absent"); got != None {
        t.Fatalf("expected None, got %v", got)
    }
    if metric("cache.miss.count") != 1 {
        t.Fatalf("expected cache.miss.count to increase by 1")
    }
}
```

## Code-Domain Explanation

This rule has a direct effect on how you count words for sentence-length limits in different types of code documentation. The maximum sentence length in STE-Code is 20 words for procedural sentences and 25 words for descriptive sentences. When you apply Rule 8.6 correctly, many sentences that seem too long become compliant because multi-word elements collapse into single-word counts.

### README Files

README files frequently contain project names, badge URLs, version numbers, and tool abbreviations. Each of these counts as one word under this rule.

A README sentence such as "This project uses GitHub Actions for CI/CD and deploys to AWS Lambda via the Serverless Framework" has these multi-word elements that each count as one word: "GitHub Actions" (proper noun, 1 word), "CI/CD" (abbreviation, 1 word), "AWS Lambda" (proper noun, 1 word), and "Serverless Framework" (proper noun, 1 word). The sentence appears to have 17 words but counts as only 12 words under Rule 8.6.

```markdown
# acme-cli

This project uses GitHub Actions for CI/CD and deploys to AWS Lambda via the
Serverless Framework. The badge `build-passing` shows the latest test result.
```

In the sentence above, "build-passing" (the badge name, quoted text) is also 1 word.

### API Documentation

API documentation contains endpoint paths, HTTP status codes, parameter names, and response field identifiers. Each of these is an alphanumeric identifier or quoted text and counts as one word.

An endpoint description such as "Send a POST request to `/api/v1/users/{userId}/orders` with the `X-API-Key` header" has `/api/v1/users/{userId}/orders` (quoted path, 1 word), `X-API-Key` (quoted identifier, 1 word), and `POST` (quoted method, 1 word). The sentence appears to have 14 words but counts as 10 words.

```http
POST /api/v1/users/{userId}/orders HTTP/1.1
Host: api.example.com
X-API-Key: <token>
Content-Type: application/json
```

### Docstrings and Inline Comments

Docstrings often reference parameter types, return types, and exception classes. These are proper nouns or alphanumeric identifiers.

A Python docstring such as "Raises `ValueError` if the input is not a positive `float` between `0.0` and `1.0`" has `ValueError` (proper noun, 1 word), `float` (quoted type name, 1 word), `0.0` (number, 1 word), and `1.0` (number, 1 word). The sentence appears to have 14 words but counts as 10 words.

```python
def normalize_ratio(value: float) -> float:
    """Return a number between 0.0 and 1.0.

    Raises ValueError if the input is not a positive float between
    0.0 and 1.0.
    """
```

### Commit Messages

Commit messages often contain issue tracker identifiers, branch names, and abbreviated command names. Each counts as one word under this rule.

A commit message such as "Fix NPE in `UserService.authenticate()` when `SecurityContext.getPrincipal()` returns null for OAuth2 tokens from Azure AD B2C" has `NPE` (abbreviation, 1 word), `UserService.authenticate()` (quoted identifier, 1 word), `SecurityContext.getPrincipal()` (quoted identifier, 1 word), `OAuth2` (proper noun, 1 word), and `Azure AD B2C` (proper noun, 1 word). The sentence appears to have 17 words but counts as 12 words.

```text
Fix NPE in UserService.authenticate() when SecurityContext.getPrincipal()
returns null for OAuth2 tokens from Azure AD B2C

Closes PROJ-4821
```

### Error Messages

Error messages shown to users or logged by systems often contain error codes, field names, and type identifiers. Each of these is an alphanumeric identifier and counts as one word.

An error message such as "Validation failed for field `email_address`: value must match pattern `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`" has `email_address` (quoted identifier, 1 word) and the regex pattern (quoted text, 1 word). The sentence appears to have 14 words but counts as 12 words.

```text
Validation failed for field email_address: value must match pattern
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

### Practical Impact on Sentence-Length Compliance

When you apply Rule 8.6 across all seven element categories, the average code documentation sentence reduces its word count by 3 to 8 words compared to a naive word count. This makes it easier to obey the 20-word procedural limit and the 25-word descriptive limit (Rule 8.7). The reduction is largest in API documentation and README files because these document types contain the highest density of identifiers, abbreviations, and proper nouns.

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Object-oriented documentation contains class names, method signatures, interface names, and package names. Each of these is a proper noun or alphanumeric identifier and counts as one word.

Class hierarchy descriptions benefit from this rule. A sentence such as "The `AbstractUserRepository` implements `CrudRepository<User, Long>` and extends `PagingAndSortingRepository<User, Long>`" has `AbstractUserRepository` (proper noun, 1 word), `CrudRepository<User, Long>` (proper noun with type parameters as quoted text, 1 word), and `PagingAndSortingRepository<User, Long>` (proper noun with type parameters, 1 word).

Method signature documentation also benefits. A sentence such as "Call `buildQuery(SearchCriteria criteria, Pageable pageable, Sort.Direction direction)` to get a `TypedQuery<ResultDTO>`" has three identifiers that each count as one word.

Design pattern references are proper nouns: "This class uses the Abstract Factory Pattern" counts "Abstract Factory Pattern" as one word. "Apply the Dependency Inversion Principle" counts "Dependency Inversion Principle" as one word.

```java
// The AbstractUserRepository implements CrudRepository<User, Long> and
// extends PagingAndSortingRepository<User, Long>.
public abstract class AbstractUserRepository
        implements CrudRepository<User, Long>,
        PagingAndSortingRepository<User, Long> { }
```

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional documentation contains type signatures, pattern matches, monad names, and function compositions. Each type signature or monad stack counts as one word when quoted.

A Haskell type signature such as "`validate :: Config -> Either ValidationError Config`" counts as quoted text (1 word). A monad transformer stack such as "`ReaderT Env (ExceptT AppError IO) a`" counts as one word when quoted.

Function pipeline documentation benefits: "Pipe the input through `validate >>= normalize >>= persist`" has the pipeline as quoted text (1 word). Algebraic data type constructors such as "`Just value`" or "`Left error`" each count as one word when quoted.

```haskell
-- validate :: Config -> Either ValidationError Config
validate :: Config -> Either ValidationError Config
validate cfg = runValidate cfg >>= normalize >>= persist

-- ReaderT Env (ExceptT AppError IO) a
type App a = ReaderT Env (ExceptT AppError IO) a
```

### Procedural Documentation (C, Go, Bash)

Procedural documentation contains function names, struct tags, error codes, and signal names. Each counts as one word under the appropriate category.

C documentation: "Call `pthread_mutex_lock(&mtx)` before you access the shared buffer" has `pthread_mutex_lock(&mtx)` as quoted text (1 word). "The function returns `EAGAIN` when the operation would block" has `EAGAIN` as an alphanumeric identifier (1 word).

Go documentation: "The `context.Context` value carries deadlines and cancellation signals" has `context.Context` as a proper noun (1 word). "Wrap the error with `fmt.Errorf("user %s: %w", id, err)`" has the format string as quoted text (1 word).

Bash documentation: "Set `IFS=$'\n'` before you read the file line by line" has `IFS=$'\n'` as an alphanumeric identifier with assignment (1 word). "Trap `SIGINT` and `SIGTERM` to clean up temporary files" has two signal names that each count as one word.

```c
/* Call pthread_mutex_lock(&mtx) before you access the shared buffer.
   The function returns EAGAIN when the operation would block. */
pthread_mutex_lock(&mtx);
```

```bash
# Set IFS=$'\n' before you read the file line by line
IFS=$'\n'
trap 'rm -f "$TMPFILE"' SIGINT SIGTERM
```

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documentation contains resource names, column identifiers, constraint names, and provider references. Each of these counts as one word.

SQL documentation: "Create an index on `users(email_address, created_at)` with the `CONCURRENTLY` option" has the column list as quoted text (1 word) and `CONCURRENTLY` as a keyword quoted for emphasis (1 word). "The foreign key `fk_orders_user_id` references `users(id) ON DELETE CASCADE`" has two identifiers and a clause that each count as one word.

Terraform documentation: "The `aws_lambda_function.main` resource depends on `aws_iam_role.lambda_exec`" has two resource identifiers that each count as one word. "Set `var.environment = "production"` in your `terraform.tfvars` file" has the assignment and filename as one word each.

Kubernetes documentation: "Apply the `nginx-ingress-controller` Deployment from the `ingress-nginx` namespace" has two proper nouns that each count as one word. "The `readinessProbe.httpGet.path` must return a 200 status code" has the field path as an alphanumeric identifier (1 word) and `200` as a number (1 word).

```sql
-- Create an index on users(email_address, created_at) with the CONCURRENTLY
-- option. The foreign key fk_orders_user_id references users(id)
-- ON DELETE CASCADE.
CREATE INDEX CONCURRENTLY idx_users_email ON users (email_address, created_at);
```

```hcl
# The aws_lambda_function.main resource depends on aws_iam_role.lambda_exec.
resource "aws_lambda_function" "main" {
  function_name = "api"
  depends_on    = [aws_iam_role.lambda_exec]
}
```

### Systems Documentation (Rust Ownership, C Memory)

Systems documentation contains lifetime annotations, ownership diagrams, memory layout descriptions, and unsafe block justifications. Each annotation or diagram counts as one word when quoted.

Rust ownership documentation: "The function signature `fn process<'a>(data: &'a [u8]) -> Cow<'a, str>`" counts as quoted text (1 word). "The borrow checker rejects this because `data` is borrowed as immutable at line 42 and as mutable at line 47" has line numbers that count as one word each.

C memory documentation: "The buffer at address `0x7fff5fbff8c0` must be freed after the call to `process_buffer(void *buf, size_t len)`" has the address and function call as one word each. "Use `valgrind --leak-check=full --show-leak-kinds=all ./program` to find memory leaks" has the full command as quoted text (1 word).

```rust
// The function signature fn process<'a>(data: &'a [u8]) -> Cow<'a, str>
// borrows data for the lifetime 'a.
fn process<'a>(data: &'a [u8]) -> Cow<'a, str> {
    String::from_utf8_lossy(data)
}
```

```bash
# Use valgrind --leak-check=full --show-leak-kinds=all ./program to find
# memory leaks.
valgrind --leak-check=full --show-leak-kinds=all ./program
```

## Extended Examples

### Example 1: Combining Multiple One-Word Elements in an API Reference

> **Non-STE:** The endpoint located at the uniform resource locator path of /api/v2/organizations/{organizationId}/repositories/{repositoryId}/branches accepts a Hypertext Transfer Protocol Secure GET request and requires an OAuth two point zero bearer token in the Authorization header with the format Bearer followed by a space and then the access token, and it returns a JavaScript Object Notation response body with a two hundred status code.
>
> **STE:** The `GET /api/v2/orgs/{orgId}/repos/{repoId}/branches` endpoint needs an OAuth 2.0 bearer token in the `Authorization` header. It returns a JSON response body with a 200 status code. (10 words, then 10 words)
>
> *Principles applied: P3 (use words only with approved meanings — "needs" not "requires"), P9 (prefer short, clear technical nouns — "orgId" not "organizationId"). The quoted path counts as 1 word. "OAuth 2.0" is a proper noun (1 word). "Authorization" is quoted text (1 word). "JSON" is an abbreviation (1 word). "200" is a number (1 word).*

```http
GET /api/v2/orgs/{orgId}/repos/{repoId}/branches HTTP/1.1
Authorization: Bearer <access-token>
```

### Example 2: Error Code and Stack Trace Documentation

> **Non-STE:** The NullPointerException error with the identifier ERR_NULL_REF_0042 is thrown by the processRequest method located in the class com.example.service.RequestHandler at line one hundred and twenty-seven when the incoming GraphQL query contains a null value for the required field named userContext, and the stack trace will also include frames from the DataFetcherExceptionHandler class and the ExecutionStrategy class.
>
> **STE:** The error `ERR_NULL_REF_0042` occurs in `RequestHandler.processRequest()` at line 127. The `GraphQL` query has a null value for the required field `userContext`. The stack trace includes `DataFetcherExceptionHandler` and `ExecutionStrategy`. (8 words, 12 words, 5 words)
>
> *Principles applied: P5 (technical code nouns are allowed — "GraphQL"), P7 (do not use technical nouns as verbs — "occurs" not "is thrown"). "ERR_NULL_REF_0042" and "RequestHandler.processRequest()" are alphanumeric/quoted identifiers (1 word each). "GraphQL" is a proper noun (1 word). "DataFetcherExceptionHandler" and "ExecutionStrategy" are proper nouns (1 word each).*

```text
com.example.service.RequestHandler.processRequest(RequestHandler.java:127)
  Caused by: ERR_NULL_REF_0042
  at DataFetcherExceptionHandler.handle(DataFetcherExceptionHandler.java:44)
  at ExecutionStrategy.execute(ExecutionStrategy.java:88)
```

### Example 3: Configuration File Documentation

> **Non-STE:** In the YAML Ain't Markup Language configuration file located at the path etc/application/configuration/production.yaml, set the property spring.datasource.hikari.maximumPoolSize to a value of fifty and set the property server.tomcat.maxThreads to a value of two hundred, then also make sure that the property logging.level.com.example is set to the value DEBUG and the property management.endpoints.web.exposure.include is set to the value health,info,metrics.
>
> **STE:** In `etc/application/config/production.yaml`, set `spring.datasource.hikari.maximumPoolSize` to 50. Set `server.tomcat.maxThreads` to 200. Set `logging.level.com.example` to `DEBUG`. Set `management.endpoints.web.exposure.include` to `health,info,metrics`. (8 words, 5 words, 6 words, 7 words)
>
> *Principles applied: P9 (prefer short, clear technical nouns — "config" not "configuration"), P12 (technical verbs like "set" are allowed). The file path is quoted text (1 word). Each property name is an alphanumeric identifier (1 word). "50" and "200" are numbers (1 word each).*

```yaml
# etc/application/config/production.yaml
spring:
  datasource:
    hikari:
      maximumPoolSize: 50
server:
  tomcat:
    maxThreads: 200
logging:
  level:
    com.example: DEBUG
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
```

### Example 4: Commit Message with Multiple Identifiers

> **Non-STE:** Implement the continuous integration and continuous delivery pipeline workflow for the automatic deployment of the user interface application to the Amazon Web Services Simple Storage Service bucket when a pull request is merged into the main branch, which triggers the GitHub Actions workflow file located at .github/workflows/deploy-ui-to-production.yml and uses the OpenID Connect protocol for authentication.
>
> **STE:** Add the CI/CD pipeline workflow for the UI app deployment to the AWS S3 bucket. The workflow triggers on pull request merges to `main`. It uses OIDC for authentication. (12 words, 8 words, 6 words)
>
> *Principles applied: P2 (use words only as their specified part of speech — "Add" as imperative verb), P3 (use words only with approved meanings — "triggers" not "is triggered"). "CI/CD" is an abbreviation (1 word). "AWS S3" is a proper noun (1 word). "main" is quoted text (1 word). "OIDC" is an abbreviation (1 word).*

```text
Add the CI/CD pipeline workflow for the UI app deployment to the AWS S3 bucket

The workflow triggers on pull request merges to main. It uses OIDC for
authentication.
```

### Example 5: Database Migration Documentation

> **Non-STE:** Execute the structured query language migration script with the filename V2_3_1__add_user_preferences_table.sql which creates a new relational database table called user_preferences that has a universally unique identifier primary key column, a foreign key column referencing the users table on the id column with a cascade on delete action, and a JavaScript Object Notation Binary column for storing the preference data with a default value of an empty JSON object represented by the characters opening curly brace followed by closing curly brace.
>
> **STE:** Run the migration `V2_3_1__add_user_preferences_table.sql`. It makes the `user_preferences` table with a UUID primary key. The table has a foreign key to `users(id) ON DELETE CASCADE`. It has a JSONB column with the default value `{}`. (9 words, 11 words, 8 words, 10 words)
>
> *Principles applied: P12 (technical verbs like "run" are allowed — "Run" not "Execute"), P1 (use approved words — "makes" not "creates"). "V2_3_1__add_user_preferences_table.sql" is an alphanumeric identifier (1 word). "user_preferences" is quoted text (1 word). "UUID" is an abbreviation (1 word). "JSONB" is an abbreviation (1 word).*

```sql
-- Run the migration V2_3_1__add_user_preferences_table.sql.
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    data JSONB DEFAULT '{}'::jsonb
);
```

### Example 6: Dependency Declaration

> **Non-STE:** This particular module depends on version two point one point zero or later of the org.springframework.boot.spring-boot-starter-web artifact, version one point eighteen point twenty-four of the com.google.guava.guava artifact, and version four point thirteen point two of the junit.junit artifact for testing purposes only using the test scope in Apache Maven.
>
> **STE:** This module uses `org.springframework.boot:spring-boot-starter-web` version 2.1.0 or later. It uses `com.google.guava:guava` version 1.18.24. It uses `org.junit:junit` version 4.13.2 for tests only. (9 words, 8 words, 9 words)
>
> *Principles applied: P1 (use approved words — "uses" not "depends on"), P8 (use standard, well-known technical nouns — "tests" not "testing purposes"). Each Maven coordinate is quoted text (1 word). Version numbers are numbers (1 word each when paired with "version").*

```xml
<!-- pom.xml — this module uses the dependencies below -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
  <version>2.1.0</version>
</dependency>
<dependency>
  <groupId>com.google.guava</groupId>
  <artifactId>guava</artifactId>
  <version>1.18.24</version>
</dependency>
<dependency>
  <groupId>org.junit</groupId>
  <artifactId>junit</artifactId>
  <version>4.13.2</version>
  <scope>test</scope>
</dependency>
```

### Example 7: Test Specification with Assertion Identifiers

> **Non-STE:** The integration test must confirm that after the message broker delivers the event with the topic name order.created to the subscriber that is registered under the channel identifier orders.v1 and the payload contains a field called totalAmount that is greater than zero, the assertion framework records a pass result and writes the value of the correlation identifier to the test report file.
>
> **STE:** The test must check that the broker sends `order.created` to `orders.v1`. It must check that `totalAmount` is greater than 0. The framework records a pass and writes the correlation identifier to the report. (18 words, 15 words, 16 words)
>
> *Principles applied: P3 (use words only with approved meanings — "check" not "confirm"), P12 (technical verbs like "send" are allowed). "order.created" and "orders.v1" are quoted identifiers (1 word each). "totalAmount" is quoted text (1 word). "0" is a number (1 word).*

```go
// The test must check that the broker sends order.created to orders.v1.
// It must check that totalAmount is greater than 0.
func TestOrderCreated(t *testing.T) {
    broker.Publish("order.created", orders.v1, payload{totalAmount: 42})
    assert.Greater(t, payload.totalAmount, 0)
    assert.True(t, report.HasCorrelationID())
}
```

### Example 8: TypeScript Generic and React Component Documentation

> **Non-STE:** You should create a new component which is a generic version of the data table that accepts a type parameter called TRow that represents the shape of each row object and it also accepts the array of rows as a property named rows and a callback function as a property named onRowClick so that the parent component can respond when the user selects a specific row in the interface.
>
> **STE:** Make the `DataTable<TRow>` component. Pass the `rows` array and the `onRowClick` callback as props. The parent responds when the user selects a row. (13 words, 13 words, 11 words)
>
> *Principles applied: P2 (use "Make" as imperative verb), P9 (prefer short technical nouns — "props" not "properties"). "DataTable<TRow>" is quoted text (1 word). "rows" and "onRowClick" are quoted identifiers (1 word each).*

```tsx
// Make the DataTable<TRow> component. Pass the rows array and the
// onRowClick callback as props.
function DataTable<TRow>({ rows, onRowClick }: Props<TRow>) {
  return rows.map((row) => <Row key={row.id} onClick={onRowClick} />);
}
```

## Edge Cases

### Edge Case 1: Framework Names That Contain "Unapproved" Words

Some framework names contain words that are not in the STE-Code dictionary. For example, "Express" (a Node.js framework) and "Swift" (an Apple programming language) are also common English words. When these names appear in documentation, they are proper nouns and count as one word under category 7 of Rule 8.6. Do not apply Rule 1.1 (use approved words) to proper nouns.

A second concern: framework names sometimes contain verbs used as nouns, which would violate Rule 1.7. For example, "React" is a JavaScript library whose name is a verb. When your documentation says "Use React to build the user interface," treat "React" as a proper noun (1 word), not as a verb. Do not rewrite framework names to obey STE-Code word rules.

```tsx
// Use React to build the user interface. "React" is a proper noun (1 word).
import React from "react";
export const App = () => <main>Hello</main>;
```

### Edge Case 2: Code Keywords That Conflict with the Rule

Code keywords such as `class`, `function`, `return`, and `async` have specific meanings in programming languages. When you quote them in documentation, they count as one word under the quoted text category (category 5). Do not replace them with STE-Code synonyms.

The keyword `class` in Java or Python documentation should stay as `class`, not be replaced with "category" or "type." The keyword `return` should stay as `return`, not be replaced with "give back." These keywords are quoted text and count as one word.

However, when you use these words as part of your own prose — not as quoted code — apply the STE-Code dictionary normally. "The function returns a value" uses "returns" as a technical verb (Rule 1.12). "The class has three methods" uses "class" as a technical noun (Rule 1.5). Both are allowed.

```python
# The class has three methods. The function returns a value.
class Handler:
    def process(self) -> int:
        return 0
```

### Edge Case 3: Generated Code and Automated Documentation

Generated code comments and auto-generated API reference pages often contain long identifiers, fully qualified class names, and machine-generated descriptions. These are not written by a human author and cannot be changed. Apply Rule 8.6 category 6 (titles, headings, and text on labels) to these elements: they count as one word because they are not possible to change.

For example, a Javadoc `@see` tag such as `@see com.example.service.impl.UserServiceImpl#authenticate(String, char[])` counts as one word — it is generated text on a label. Similarly, an OpenAPI specification description auto-generated from code annotations counts as one word when you cannot change it.

When you write new documentation that wraps around generated text, count the generated portions as one word and apply STE-Code rules to your own prose.

```java
/**
 * Authenticates the given user.
 * @see com.example.service.impl.UserServiceImpl#authenticate(String, char[])
 */
public boolean login(String user, char[] password) { return true; }
```

### Edge Case 4: Nested Quoted Text and Backtick Escaping

Code documentation sometimes contains quoted text inside quoted text — for example, a shell command that includes a quoted string. The outer quoting mechanism (markdown backticks or HTML `<code>` tags) defines the quoted text boundary. Everything inside counts as one word.

A documentation sentence such as "Run `curl -H "Authorization: Bearer $TOKEN" https://api.example.com/v2/status` to check the service" has the entire backtick-quoted command as one word, even though the command itself contains double quotes.

When you write markdown documentation that shows how to use markdown code fences — a meta-documentation scenario — use four-backtick fences to escape three-backtick fences:

````
The README must include a ```` ```bash ```` code fence example.
````

In the outer sentence, the inner ```` ```bash ```` counts as quoted text (1 word).

```bash
# Run curl -H "Authorization: Bearer $TOKEN" https://api.example.com/v2/status
# to check the service.
curl -H "Authorization: Bearer $TOKEN" https://api.example.com/v2/status
```

### Edge Case 5: Semantic Version Strings and Complex Identifiers

Semantic version strings such as `1.2.3-alpha.1+build.456` contain dots, hyphens, and plus signs. These are alphanumeric identifiers and count as one word under category 4 of Rule 8.6. The same applies to Git commit hashes (`a1b2c3d`), container image digests (`sha256:abc123...`), and package lockfile integrity hashes.

A sentence such as "The fix is in version `2.4.1-hotfix.3` and commit `a1b2c3d4e5f6`" has two alphanumeric identifiers that each count as one word. Version range expressions such as `>=1.0.0 <2.0.0` also count as one word when quoted.

Do not split a semantic version string into its components for word counting. "Version 1.2.3" is two words: "Version" (1 word) and "1.2.3" (1 word).

```text
# The fix is in version 2.4.1-hotfix.3 and commit a1b2c3d4e5f6
docker pull registry.example.com/api@sha256:abc123def456
```

### Edge Case 6: Numbers That Identify Document Parts

Rule 8.6 (category 1) says do not count numbers that identify paragraphs or work steps because they are part of the document numbering system. In code documentation this applies to:

- Rule or section numbers in cross-references (for example, "see Rule 8.7" — "8.7" is a document number, not counted).
- Step numbers in numbered procedures (for example, "Step 3: set the flag" — "3" is a step number, not counted).
- Issue or ticket IDs used as document references (for example, "fixes PROJ-4821" — treat "PROJ-4821" as an alphanumeric identifier, 1 word; it is not a count of quantity).

This exception keeps procedural documentation readable without inflating the word count for structural numbering that the reader skips.

```text
Step 3: set the feature flag. See Rule 8.7 for the sentence-length limit.
Fixes PROJ-4821.
```

## Cross-References

This rule works together with other STE-Code rules. Use these cross-references to apply Rule 8.6 correctly:

- **Rule 1.1 (Use approved words):** Proper nouns, quoted text, and alphanumeric identifiers are exempt from the approved-word requirement. Do not reject a sentence because a proper noun contains a non-approved word.
- **Rule 1.5 (Technical code nouns are allowed):** Framework names, library names, and tool names are technical nouns. They are also proper nouns under Rule 8.6 category 7 and count as one word.
- **Rule 1.6 (Non-approved words only when they are technical code nouns):** When a word is not in the STE-Code dictionary but is part of a proper noun, abbreviation, or quoted identifier, Rule 8.6 allows it. Do not flag it as a violation of Rule 1.6.
- **Rule 8.7 (Maximum sentence length):** Rule 8.6 makes it possible to write sentences that obey the 20/25-word limits. When you split a long procedural sentence, use Rule 8.6 to count the words in each new sentence. An identifier that spans two words in naive counting may let each split sentence stay under the limit. A sentence that appears to have 30 words may have only 22 words after applying Rule 8.6 and be compliant.
- **STE-Code Dictionary:** The dictionary lists approved words and their parts of speech. Proper nouns, abbreviations, and alphanumeric identifiers are not in the dictionary and do not need to be. They count as one word regardless.
- **Rule 1.14 (Use American English spelling):** When a proper noun uses British or another non-American spelling (for example, "Centre" in an organization name), do not change the spelling. The proper noun is exempt and counts as one word.

## Grammar Notes

### The Linguistic Principle Behind the Rule

Rule 8.6 is based on a principle from computational linguistics: a token is not always a word. In natural language processing, a tokenizer splits text on whitespace and punctuation. But a "word" for the purpose of sentence-length measurement is a unit of meaning, not a unit of whitespace separation.

In code documentation, the density of non-word tokens is much higher than in general prose. Identifiers such as `getUserById`, version strings such as `2.1.0`, and abbreviations such as `JWT` carry meaning as whole units. Splitting them into sub-tokens would inflate the word count without adding meaning.

### Why Multi-Word Proper Nouns Collapse

Proper nouns of organizations and geopolitical entities often contain function words (articles, prepositions, conjunctions). "The Apache Software Foundation" has five whitespace-separated tokens, but "The" and "of" carry no independent meaning in this context. The entire phrase identifies one entity. Counting each token separately would penalize sentences that reference well-known organizations — the opposite of what clear documentation requires.

### Abbreviations vs. Spelled-Out Forms

When you write an abbreviation, you choose to collapse a multi-word phrase into a single token. "JSON" replaces "JavaScript Object Notation" (three words becomes one). "CI/CD" replaces "continuous integration and continuous delivery" (five words becomes one). Rule 8.6 recognizes this intentional compression and counts the abbreviation as one word.

However, when you spell out the abbreviation on first use — for example, "JavaScript Object Notation (JSON)" — count the spelled-out form as its component words and the abbreviation separately. The full phrase "JavaScript Object Notation (JSON)" is a proper noun definition with a parenthetical abbreviation. Count "JavaScript Object Notation" as one word (proper noun, category 7) and "(JSON)" as one word (abbreviation with parentheses as quoted text, category 3).

### The Interaction with Sentence Splitting

Rule 8.6 is not only a counting rule. It is a design rule for sentence structure. When you know that identifiers, abbreviations, and proper nouns count as one word, you can include more technical precision in each sentence without violating length limits. This lets you write documentation that is both technically complete and easy to read.

A well-designed STE-Code sentence front-loads the action or condition, then places the multi-word element near the end: "Set the timeout to 30 seconds" (6 words) rather than "The timeout value that you should configure must be set to a duration of 30 seconds" (17 words). Rule 8.6 rewards this structure because the number-with-unit at the end counts as one word.

### Word-Count Verification Pattern

To verify that a sentence obeys Rule 8.6, use this step-by-step pattern:

1. Write the sentence.
2. Identify all numbers and replace each with a placeholder (1 word).
3. Identify all numbers with units and replace each pair with a placeholder (1 word).
4. Identify all abbreviations and replace each with a placeholder (1 word).
5. Identify all alphanumeric identifiers and replace each with a placeholder (1 word).
6. Identify all quoted text (including backtick-quoted text) and replace each with a placeholder (1 word).
7. Identify all document titles, headings, and UI text and replace each with a placeholder (1 word).
8. Identify all proper nouns and replace each with a placeholder (1 word).
9. Count the remaining words plus the placeholders.

This pattern is useful for automated word-count tools and linters that enforce Rule 8.7 sentence-length limits in documentation CI pipelines.

```python
# Word-count helper that applies Rule 8.6 (illustrative, not normative)
import re

ONE_WORD_PATTERNS = [
    r"`[^`]+`",                 # backtick-quoted text
    r'"[^"]+"',                 # double-quoted text
    r"\b[A-Za-z]+\d[A-Za-z0-9]*\b",  # alphanumeric identifier
    r"\d+\s*(?:ms|s|μs|MB|KB|GB|Mi|Gi|m|°C|kg|Ω)\b",  # number + unit
    r"\b\d+(?:\.\d+)*[A-Za-z]*\b",   # number or version
]

def count_ste_words(sentence: str) -> int:
    # Replace each one-word element with a single placeholder token.
    for pat in ONE_WORD_PATTERNS:
        sentence = re.sub(pat, " X ", sentence)
    return len(sentence.split())
```

## See also

> **See also:** Rule 1.1 — Use Approved Words
> **See also:** Rule 1.5 — Technical Code Nouns Are Allowed
> **See also:** Rule 1.6 — Non-Approved Words Only as Technical Code Nouns
> **See also:** Rule 1.14 — Use American English Spelling
> **See also:** Rule 8.7 — Maximum Sentence Length

---

<!-- a-sec8-rule8.7.md -->

# Rule 8.7 — Hyphenated Words Count as One Word

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.7

> **Source:** [master.md#sec8-rule8.7](ste-code/grouped/)

## Original Rule

**Rule 8.7** Hyphenated words count as one word.

Groups of words that are not usually adjectives but have the function of an adjective before a noun are hyphenated. Such groups of words count as one word.

Examples:

| Example | Word count |
|----------|-------------|
| Clean the surface with a soap-and-water solution. | (7 words) |
| Use the trial-and-error method. | (4 words) |

When you use hyphens in long technical nouns to make them clearer to the reader, a hyphenated group of words also counts as one word.

Examples:

| Example | Word count |
|----------|-------------|
| Cutoff-switch power connection | (3 words) |
| Main-gear-door retraction-winch handle | (3 words) |

## STE-Code Adaptation

**Rule 8.7** Hyphenated words count as one word.

Groups of words that are not usually adjectives but have the function of an adjective before a noun are hyphenated. Such groups of words count as one word.

In code documentation, this rule applies directly. A hyphenated technical term, whether it is a compound adjective or a long technical noun, counts as one word when you count words for sentence length. The hyphen joins two or more words into a single unit that the reader processes as one concept, so the word-count limits in Rules 4.1 and 4.2 measure the unit as one word, not as the number of words inside it.

### Examples

> *Adapted from spec pair:* Non-STE: "Clean the surface with a soap and water solution."  |  STE: "Clean the surface with a soap-and-water solution." (7 words — "soap-and-water" is a hyphenated compound adjective and counts as one word.)

> **Non-STE:** The open function returns a read only file descriptor. The caller parses the config from the descriptor and then closes it.
>
> **STE:** The open function returns a read-only file descriptor. The caller parses the config from the descriptor and then closes it.
>
> *Adapted from spec pair: "Clean the surface with a soap-and-water solution." → "read-only" is a hyphenated compound adjective and counts as one word.*

> *Adapted from spec pair:* Non-STE: "Use the trial and error method."  |  STE: "Use the trial-and-error method." (4 words — "trial-and-error" is a hyphenated compound adjective and counts as one word.)

> **Non-STE:** To calibrate the retry interval, use the try and error method. Run the probe, record the latency, and adjust the value until the timeout stops.
>
> **STE:** To calibrate the retry interval, use the trial-and-error method. Run the probe, record the latency, and adjust the value until the timeout stops.
>
> *Adapted from spec pair: "Use the trial-and-error method." → "trial-and-error" is a hyphenated compound adjective and counts as one word.*

> *Adapted from spec pair:* Non-STE: "Cutoff switch power connection"  |  STE: "Cutoff-switch power connection" (3 words: `cutoff-switch` / `power` / `connection`). The hyphenated noun group counts as one word.

> **Non-STE:** The cutoff switch power connection must stay isolated during the test. If the relay closes, the test fails and the harness records a short circuit.
>
> **STE:** The cutoff-switch power connection must stay isolated during the test. If the relay closes, the test fails and the harness records a short circuit.
>
> *Adapted from spec pair: "Cutoff-switch power connection" (3 words). The hyphenated noun group counts as one word.*

> *Adapted from spec pair:* Non-STE: "Main gear door retraction winch handle"  |  STE: "Main-gear-door retraction-winch handle" (3 words: `main-gear-door` / `retraction-winch` / `handle`). The hyphenated noun group counts as one word.

> **Non-STE:** The main gear door retraction winch handle must lock before the door opens. The controller checks the sensor and blocks the actuator until the latch engages.
>
> **STE:** The main-gear-door retraction-winch handle must lock before the door opens. The controller checks the sensor and blocks the actuator until the latch engages.
>
> *Adapted from spec pair: "Main-gear-door retraction-winch handle" (3 words). The hyphenated noun group counts as one word.*

> *Adapted from spec pair:* Non-STE: "The build-time environment variable points to staging."  |  STE: "The build-time environment variable must point to the staging cluster." (10 words — "build-time" is one word). Compound identifiers written as words use the same structure as the spec's long technical nouns.

> **Non-STE:** Set the build time environment variable to the path of the staging cluster before you run the pipeline. The job fails when the value is empty.
>
> **STE:** Set the build-time environment variable to the path of the staging cluster before you run the pipeline. The job fails when the value is empty.
>
> *Adapted from spec pair: "Cutoff-switch power connection" (3 words). "build-time" is a hyphenated technical noun and counts as one word; the two following words are separate.*

> *Adapted from spec pair:* Non-STE: "Run the end to end test suite in the pipeline."  |  STE: "Run the end-to-end test suite in the pipeline." (8 words — "end-to-end" is one word). The same pre-noun hyphen pattern applies to compound code-domain adjectives.

> **Non-STE:** The client side rendering pipeline builds the page in the browser. The server sends the data as JSON and the view updates after the fetch returns.
>
> **STE:** The client-side rendering pipeline builds the page in the browser. The server sends the data as JSON and the view updates after the fetch returns.
>
> *Adapted from spec pair: "soap-and-water solution" → "client-side" is a hyphenated compound adjective before "rendering pipeline" and counts as one word.*

> *Adapted from spec pair:* Non-STE: "Use a thread safe singleton for the cache."  |  STE: "Use a thread-safe singleton for the cache." (7 words — "thread-safe" is one word). Approved STE-Code adjectives (thread-safe, idempotent, stateless) keep the hyphen before the noun.

> **Non-STE:** The event driven architecture sends a message to the queue after the worker finishes the task. The consumer reads the event and updates the record.
>
> **STE:** The event-driven architecture sends a message to the queue after the worker finishes the task. The consumer reads the event and updates the record.
>
> *Adapted from spec pair: "trial-and-error method" → "event-driven" is a hyphenated compound adjective and counts as one word.*

## Code-Domain Explanation

Rule 8.7 tells you how to count words when a term is hyphenated. The hyphen joins two or more words into a single unit that the reader processes as one concept. For word-count limits in STE-Code (Rules 4.1 and 4.2), a hyphenated unit counts as one word, not as the number of words inside it.

There are two cases.

### Case 1: Hyphenated compound adjectives

When a group of words describes a noun and sits before that noun, you hyphenate it. Examples from the spec: "soap-and-water solution," "trial-and-error method." The same pattern appears throughout code documentation:

- `read-only file descriptor` — "read-only" is one word.
- `thread-safe singleton` — "thread-safe" is one word.
- `event-driven architecture` — "event-driven" is one word.
- `low-latency cache` — "low-latency" is one word.
- `client-side rendering pipeline` — "client-side" is one word.
- `end-to-end test suite` — "end-to-end" is one word.
- `backward-compatible API` — "backward-compatible" is one word.
- `idempotent retry handler` — "idempotent" is a single approved word; no hyphen needed, but when you write "exactly-once delivery" the hyphenated unit is one word.
- `stateless authentication service` — "stateless" is a single approved word; "request-response cycle" keeps "request-response" as one word.

If you put the same words after the noun, do not hyphenate them: "the cache is low latency." Hyphenation is a pre-noun signal only. The word count does not change; the hyphen group still counts as one word.

When the compound adjective follows a linking verb, write the words as separate words and count each one:

- Non-STE: "The singleton is thread safe."
- STE: "The singleton is thread safe." (5 words — "thread" and "safe" are two words because the adjective is after the noun.)

### Case 2: Long hyphenated technical nouns

When a technical noun is long and the hyphen makes it easier to read, the whole hyphenated group counts as one word. Examples from the spec: "cutoff-switch power connection" (3 words: `cutoff-switch` / `power` / `connection`), "main-gear-door retraction-winch handle" (3 words: `main-gear-door` / `retraction-winch` / `handle`).

In the code domain, the same structure applies to compound identifiers that are written as words:

- `build-time environment variable` (3 words: `build-time` / `environment` / `variable`)
- `client-side rendering pipeline` (3 words: `client-side` / `rendering` / `pipeline`)
- `end-to-end test suite` (3 words: `end-to-end` / `test` / `suite`)
- `check-out request handler` (3 words: `check-out` / `request` / `handler`)
- `sign-in error message` (3 words: `sign-in` / `error` / `message`)
- `look-up table index` (3 words: `look-up` / `table` / `index`)

The words after the hyphenated unit are separate words. Only the hyphenated group counts as one word.

### Why this matters for word count

STE-Code limits procedural sentences to 20 words and descriptive sentences to 25 words (Rules 4.1, 4.2). If you count each word inside a hyphenated term, you over-report the sentence length and may break a limit that the sentence actually meets. Count the hyphenated unit as one word.

Example:

> **STE:** The build-time environment variable must point to the staging cluster. (10 words)

Word count: `The` (1) `build-time` (2) `environment` (3) `variable` (4) `must` (5) `point` (6) `to` (7) `the` (8) `staging` (9) `cluster` (10). The hyphenated `build-time` is one word. The sentence has 10 words, not 11.

Another example with a hyphenated compound adjective:

> **STE:** The thread-safe singleton must cache the read-only file descriptor. (9 words)

Word count: `The` (1) `thread-safe` (2) `singleton` (3) `must` (4) `cache` (5) `the` (6) `read-only` (7) `file` (8) `descriptor` (9). Both `thread-safe` and `read-only` are one word each.

### Interaction with Rule 8.2

Rule 8.2 tells you when to use a hyphen to connect directly related words. Rule 8.7 tells you how to count those words after you hyphenate them. The two rules work together: hyphenate per Rule 8.2, then count the hyphenated unit as one word per Rule 8.7.

Example that joins both rules:

> **Non-STE:** Use the open source library to parse the json config in the build time phase.
>
> **STE:** Use the open-source library to parse the JSON config in the build-time phase.

`open-source` is hyphenated per Rule 8.2 and counts as one word per Rule 8.7. `build-time` is a hyphenated technical noun and counts as one word. `JSON` is an abbreviation and counts as one word per Rule 8.6.

### Interaction with Rule 8.6

Rule 8.6 lists elements that count as one word (numbers, units, abbreviations, alphanumeric identifiers, quoted text, titles, proper nouns). A hyphenated word is a separate case: it is not an abbreviation or an identifier, but it still counts as one word because the hyphen makes it a single unit. Do not double-count — a hyphenated term is one word under Rule 8.7, and it is not also an abbreviation or an identifier.

Example that shows both rules in one sentence:

> **STE:** Set API_TIMEOUT_MS to 5000 in the client-side test suite. (10 words)

Word count: `Set` (1) `API_TIMEOUT_MS` (2, identifier per Rule 8.6) `to` (3) `5000` (4, number per Rule 8.6) `in` (5) `the` (6) `client-side` (7, hyphenated adjective per Rule 8.7) `test` (8) `suite` (9). The sentence has 9 words, not 11.

### Exception: hyphen in a numeral or a range

A hyphen that joins the parts of a spelled-out numeral (`twenty-one`, `forty-seven`) or marks a range (`pages 10-15`) is covered by Rule 8.6 (numbers count as one word) and by standard number counting. Rule 8.7 applies to hyphenated word groups that are adjectives or technical nouns, not to numerals.

> **STE:** Do steps 13 thru 16 a minimum of three times. (10 words — "13" and "16" each count as one word under Rule 8.6.)

This is distinct from "cutoff-switch power connection," which Rule 8.7 covers as a hyphenated noun group.

### Common code-domain hyphenated terms

Use these approved patterns in your documentation. Each hyphenated unit counts as one word before a noun:

| Term | Type | Counts as |
|------|------|-----------|
| read-only | compound adjective | one word |
| write-only | compound adjective | one word |
| thread-safe | compound adjective | one word |
| event-driven | compound adjective | one word |
| client-side | compound adjective | one word |
| server-side | compound adjective | one word |
| end-to-end | compound adjective | one word |
| backward-compatible | compound adjective | one word |
| low-latency | compound adjective | one word |
| build-time | technical noun | one word |
| run-time | technical noun | one word |
| sign-in | technical noun | one word |
| check-out | technical noun | one word |
| request-response | technical noun | one word |

When a term in this table follows the noun or a linking verb, write it as separate words and count each word.

## Verification of the Adaptation

- Rule number preserved: 8.7.
- Each STE/non-STE pair replaced with a code-domain pair (`read only` → `read-only`, `try and error` → `trial-and-error`, `cutoff switch` → `cutoff-switch`, `main gear door retraction winch` → `main-gear-door retraction-winch`, `build time` → `build-time`, `client side` → `client-side`, `end to end` → `end-to-end`, `thread safe` → `thread-safe`, `event driven` → `event-driven`).
- No aerospace-domain terms outside the `## Original Rule` block.
- American English spelling, no contractions, no progressive or perfect tenses in the adapted text.
- Part of speech preserved: "hyphenated" (adjective), "count" (verb), "word" (noun) keep their STE source roles.

> **See also:** Rule 8.2 — Use Hyphens (-) to Connect Words That Are Directly Related

> **See also:** Rule 8.6 — Elements That Count as One Word

> **See also:** Rule 4.1 — One Topic Per Sentence, No Abstract Text

> **See also:** Rule 4.2 — Do Not Omit Words or Use Contractions
