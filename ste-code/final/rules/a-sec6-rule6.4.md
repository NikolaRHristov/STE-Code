# Rule 6.4 — Use Paragraphs to Show Related Information

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec6-rule6.4](ste-code/grouped/), Rule 6.4

## Original Rule

In procedures, work steps usually have numbers and letters to show their sequence. In descriptive writing, paragraphs keep related information together and give a logical sequence to the text.

In STE, a paragraph starts with a "topic sentence" which tells the reader about the topic of that paragraph. Then, the sentences that follow the topic sentence explain it, or give more information related to it.

In the example, the underlined topic sentence at the start of each paragraph helps the reader understand the content of the paragraph and its topic. When a new paragraph starts, the reader knows that there will be a new topic or different information in that paragraph.

## STE-Code Adaptation

In procedures, work steps usually have numbers and letters to show their sequence. In descriptive code documentation, paragraphs keep related information together and give a logical sequence to the text.

In STE-Code, a paragraph starts with a "topic sentence" which tells the developer about the topic of that paragraph. Then, the sentences that follow the topic sentence explain it, or give more information related to it.

The topic sentence at the start of each paragraph helps the developer understand the content of the paragraph and its topic. When a new paragraph starts, the developer knows that there will be a new topic or different information in that paragraph.

### Examples

> *Adapted from spec pair:* Non-STE: *Instrument Landing System — "The Instrument Landing System (the system) on the aircraft shows data that helps the pilot during the approach… This data about deviations from the localizer course and glideslope path comes…" (one dense paragraph, mixed topics)* | STE: *Each topic gets its own paragraph that starts with a topic sentence: "The Instrument Landing System shows data to the pilot during the approach to the runway." then "The localizer course aligns with the centerline of the runway." then "The glideslope path is at a constant angle to the threshold of the runway."* (restructured into topic-sentence-led paragraphs)

> **Non-STE:** The data pipeline processes incoming events through a sequence of stages. Each stage transforms the event payload and passes it to the next stage. The first stage is validation, which checks the event schema and rejects malformed events. The second stage is enrichment, which adds metadata such as timestamps, source identifiers, and geolocation data from an external lookup service. The third stage is transformation, which converts the event into the target format required by downstream consumers such as the analytics warehouse and the real-time dashboard. The final stage is persistence, which writes the transformed event to the primary data store and to the event log for audit purposes. Error handling is implemented at each stage to catch exceptions without breaking the entire pipeline. If a stage fails, the pipeline logs the error and routes the event to the dead-letter queue for manual inspection.

> **STE:** The data pipeline uses a sequence of stages to process events. Validation checks the event schema and rejects malformed events. Enrichment adds metadata to the event. Transformation converts the event into a target format. Persistence writes the event to the data store and the event log. Each stage has error handling. If a stage fails, the pipeline sends the event to the dead-letter queue.

> **1. Data Pipeline Overview**

> The data pipeline processes incoming events through a sequence of stages. Each stage transforms the event payload and passes it to the next stage. Error handling is implemented at each stage to catch exceptions without breaking the pipeline. If a stage fails, the pipeline logs the error and routes the event to the dead-letter queue for manual inspection.

> **2. Validation Stage**

> The first stage is validation. This stage checks the event schema. It rejects events that are malformed.

> **3. Enrichment Stage**

> The second stage is enrichment. This stage adds metadata to the event:
> - Timestamps
> - Source identifiers
> - Geolocation data from an external lookup service.

> **4. Transformation Stage**

> The third stage is transformation. This stage converts the event into the target format. Downstream consumers use this format. These consumers include:
> - The analytics warehouse
> - The real-time dashboard.

> **5. Persistence Stage**

> The final stage is persistence. This stage writes the transformed event to two destinations. It writes the event to the primary data store. It also writes the event to the event log for audit purposes.

> *Code-domain example — each paragraph starts with a topic sentence and keeps related information together, giving the documentation a logical sequence.*

A full, runnable implementation that matches the STE description above:

```python
# pipeline.py — the data pipeline described in the STE example.
from dataclasses import dataclass
from typing import Any

@dataclass
class Event:
    payload: dict[str, Any]
    schema: str = "v1"

DEAD_LETTER_QUEUE: list[Event] = []

def process(events: list[Event]) -> None:
    """Process each event through the five stages."""
    for event in events:
        try:
            valid = validate(event)
            enriched = enrich(valid)
            transformed = transform(enriched)
            persist(transformed)
        except PipelineError as err:
            log_error(err)
            DEAD_LETTER_QUEUE.append(event)

def validate(event: Event) -> Event:
    """Validation checks the event schema and rejects malformed events."""
    if event.schema != "v1":
        raise PipelineError(f"bad schema: {event.schema}")
    return event

def enrich(event: Event) -> Event:
    """Enrichment adds metadata to the event."""
    event.payload["received_at"] = now()
    event.payload["source"] = event.payload.get("source", "unknown")
    return event

def transform(event: Event) -> Event:
    """Transformation converts the event into the target format."""
    event.payload["target"] = to_target_format(event.payload)
    return event

def persist(event: Event) -> None:
    """Persistence writes the event to the data store and the event log."""
    data_store.write(event)
    event_log.append(audit_record(event))
```

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure; Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic

## Code-Domain Explanation

Paragraph structure is the backbone of all descriptive code documentation. This rule applies differently across documentation types based on how developers read each type.

### README Files

A README file is the entry point for a repository. Each section of a README must start with a clear topic sentence. The topic sentence tells the developer what the section covers. The sentences that follow give more information about that topic.

A README paragraph that mixes installation steps with configuration options is not compliant. Move each topic to its own paragraph. Use section headings to separate major topics. Use paragraph breaks to separate sub-topics within a section.

> **Non-STE:** To install, run `pip install mylib` and then create a config file at `~/.mylib.toml` with your API key. The library supports Python 3.9 and above and requires a Redis instance for caching, which you can start with `redis-server`. You can also use SQLite for development without Redis.

> **STE:** Install the library with `pip install mylib`. Create a configuration file at `~/.mylib.toml` with your API key. The library supports Python 3.9 and above. A Redis instance is necessary for caching. Start Redis with `redis-server`. For development, use SQLite without Redis.

> **Installation**

> Install the library with pip:
> ```
> pip install mylib
> ```

> **Configuration**

> Create a configuration file at `~/.mylib.toml`. Add your API key to this file.

> **Dependencies**

> The library supports Python 3.9 and above. A Redis instance is necessary for caching. Start Redis with: `redis-server`.

> For development without Redis, use SQLite as the cache backend.

> *Principles applied: P1, P11 — uses approved vocabulary and one topic per paragraph. Each paragraph has a clear topic sentence (Install the library, Create a configuration file, The library supports, A Redis instance is necessary).*

A complete `README.md` section that applies this structure end to end:

```markdown
# mylib

A small cache library with pluggable backends.

## Installation

Install the library with pip:

    pip install mylib

## Configuration

Create a configuration file at `~/.mylib.toml`. Add your API key to this file.

## Dependencies

The library supports Python 3.9 and above. A Redis instance is necessary
for caching. Start Redis with `redis-server`.

For development without Redis, use SQLite as the cache backend.

## Usage

Import the client and connect to the cache:

    from mylib import Cache
    cache = Cache.from_config("~/.mylib.toml")
    cache.set("user:1", {"name": "ada"})
```

### API Documentation

API reference pages document endpoints, parameters, return values, and error codes. Each endpoint description must start with a topic sentence that states what the endpoint does. Parameter tables, response schemas, and error descriptions must follow in separate paragraphs.

Do not embed the authentication requirements inside the endpoint description. Give authentication its own paragraph before the endpoint details. Do not mix the request schema with the response schema in one paragraph. Separate them with clear topic sentences.

> **Non-STE:** GET /api/users returns a paginated list of users with optional query parameters for filtering by role and status. You need a Bearer token in the Authorization header. The response includes a `users` array and a `pagination` object with `next` and `prev` cursors. Status 200 on success, 401 if the token is missing or expired, and 403 if the token lacks the `users:read` scope.

> **STE:** The `GET /api/users` endpoint returns a paginated list of users. You can filter the results with `role` and `status` parameters. Include a Bearer token in the `Authorization` header. The response has a `users` array and a `pagination` object. The status codes are 200 for success, 401 for a missing token, and 403 for an invalid scope.

> **GET /api/users**

> This endpoint returns a paginated list of users.

> **Authentication**

> Include a Bearer token in the `Authorization` header. The token must have the `users:read` scope.

> **Query Parameters**

> You can filter results with these optional parameters:
> - `role` — Filter by user role.
> - `status` — Filter by account status.

> **Response**

> A successful response includes:
> - A `users` array with the matching user objects.
> - A `pagination` object with `next` and `prev` cursors.

> **Status Codes**

> - `200` — The request succeeded.
> - `401` — The token is missing or has expired.
> - `403` — The token does not have the `users:read` scope.

> *Principles applied: P1, P6, P7 — uses approved words, allows technical nouns as API terms, and does not use technical nouns as verbs. Each paragraph has one topic (authentication, query parameters, response, status codes).*

A runnable handler that implements the endpoint described above:

```python
# app/users.py — Flask route for GET /api/users.
from flask import request, jsonify
from functools import wraps

def require_scope(scope):
    """Check that the bearer token has the required scope."""
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization", "").removeprefix("Bearer ")
            if not token:
                return jsonify({"error": "missing token"}), 401
            if not has_scope(token, scope):
                return jsonify({"error": "invalid scope"}), 403
            return view(*args, **kwargs)
        return wrapper
    return decorator

@require_scope("users:read")
def list_users():
    """Return a paginated list of users."""
    role = request.args.get("role")
    status = request.args.get("status")
    page = query_users(role=role, status=status)
    return jsonify({
        "users": page.items,
        "pagination": {"next": page.next, "prev": page.prev},
    }), 200
```

### Docstrings and Inline Comments

Docstrings describe what a function, class, or module does. A docstring must start with a one-line topic sentence. Add a blank line. Then add more information in one or more paragraphs.

Each paragraph in a docstring must cover one sub-topic: parameters, return values, exceptions, side effects, or usage examples. Do not combine the description of a parameter with the description of a return value in the same paragraph.

Inline comments explain a single line or block of code. An inline comment is a one-sentence paragraph. It must state the topic of the code that follows. Do not chain multiple unrelated comments into one long comment block without paragraph breaks.

> **Non-STE:** `// Initialize the cache, then load the user profile from the database using the ORM, and if that fails fall back to the file cache, but first check the request signature using HMAC-SHA256 to make sure the request hasn't been tampered with.`

> **STE:** Check the request signature first. Then load the user profile from the cache. If the cache does not have the profile, load it from the database.

> ```javascript
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

> *Principles applied: P1, P3, P6 — uses approved words with approved meanings. Each comment is a topic sentence for the code that follows. Paragraph breaks between comments show topic changes.*

A complete Python docstring that follows the one-topic-per-paragraph rule:

```python
def send_email(recipient: str, subject: str, body: str) -> bool:
    """Send an email to the recipient and return True on success.

    The function connects to the SMTP server that the configuration
    file defines. It uses TLS for the connection.

    Parameters:
        recipient — The destination address.
        subject — The email subject line.
        body — The plain-text message body.

    Returns:
        True when the server accepts the message.
        False when the server rejects the message.

    Raises:
        ConfigError — The SMTP host is not set in the configuration.

    Side effects:
        The function writes one line to the send log.
    """
    ...
```

### Commit Messages

A commit message describes a change in a repository. The first line is the topic sentence. It tells what the commit does. The body of the commit message uses paragraphs to group related details.

Separate the motivation for the change from the implementation details. Use different paragraphs. Separate the list of files changed from the reasoning. Use different paragraphs. Each paragraph starts with a topic sentence.

> **Non-STE:** Fix race condition in connection pool that was causing deadlocks under high load, changed the mutex to a read-write lock, also updated the retry logic to use exponential backoff with jitter, and added a metrics counter for connection timeouts so we can monitor it in production, also cleaned up some old debug logging.

> **STE:** Fix a race condition in the connection pool. The pool had deadlocks under high load. Replace the mutex with a read-write lock. Update the retry logic to use exponential backoff with jitter. Add a metrics counter for connection timeouts.

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

> *Principles applied: P1, P11 — uses approved words and one term per concept. The first line is the topic sentence. Each paragraph after the blank line covers one sub-topic (the problem, the changes, the monitoring).*

The code change that the commit message describes:

```go
// pool.go — before: a single mutex guarded both reads and writes.
type Pool struct {
    mu       sync.Mutex // replaced by rwMutex below
    conns    []*Conn
    timeouts int
}

// pool.go — after: a read-write lock removes the deadlock.
type Pool struct {
    rwMutex   sync.RWMutex
    conns     []*Conn
    timeouts  int
}

func (p *Pool) Acquire() (*Conn, error) {
    backoff := time.Millisecond * 10
    for attempt := 0; attempt < maxAttempts; attempt++ {
        p.rwMutex.RLock()
        c := p.getIdle()
        p.rwMutex.RUnlock()
        if c != nil {
            return c, nil
        }
        time.Sleep(backoff)
        backoff = min(backoff*2+jitter(), maxBackoff)
    }
    atomic.AddInt64(&p.timeouts, 1)
    return nil, ErrPoolExhausted
}
```

### Error Messages

Error messages tell the user or developer what went wrong. An error message is a single sentence that states the topic: what failed and why. Multi-line error output must use paragraphs to separate the error description from the diagnostic information and the suggested fix.

Do not combine the error description, the stack trace, and the remediation advice into one paragraph. Use paragraph breaks to separate these topics.

> **Non-STE:** Connection refused to database at postgresql://db.internal:5432/app — make sure the database is running, check your network configuration, verify the hostname resolves, and ensure the TLS certificate is valid, stack trace: at ConnectionPool.connect (pool.js:42) at Database.init (db.js:15) at Server.start (server.js:88).

> **STE:** The database server refused the connection. Check that the database is running. Check that the hostname resolves. Check that the network allows the connection. Check that the TLS certificate is valid.

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

> *Principles applied: P1, P3 — uses approved words with approved meanings. Each paragraph has a clear topic (the error, the cause, the checks, the stack trace). The developer can read each paragraph independently.*

A typed error in Go that produces this multi-paragraph output:

```go
// db.go — explicit connection error with separate diagnostic paragraphs.
type ConnError struct {
    Addr string
    Cause error
}

func (e *ConnError) Error() string {
    return "Could not connect to the database.\n" +
        "\n" +
        "The database server at " + e.Addr + " refused the connection.\n" +
        "\n" +
        "Check these items:\n" +
        "  - The database process is running.\n" +
        "  - The hostname resolves correctly.\n" +
        "  - The network allows traffic on port 5432.\n" +
        "  - The TLS certificate is valid.\n"
}
```

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Class documentation must use paragraphs to separate the class purpose from the constructor details, the public API, and the internal design notes. Each method description is a paragraph group.

> **Non-STE:** The `AuthenticationService` handles user login, session management, and token refresh, it uses the `UserRepository` for database access and the `TokenProvider` for JWT generation, the `login` method takes a username and password, validates them against the database, and returns a signed JWT, while `refreshToken` accepts an expired token and returns a new one if the refresh window is still open.

> **STE:** The `AuthenticationService` manages user authentication and sessions. It uses `UserRepository` for database access. It uses `TokenProvider` for JWT generation. The `login` method validates credentials and returns a signed JWT. The `refreshToken` method accepts an expired token and returns a new token if the refresh window is open.

> **AuthenticationService**

> The `AuthenticationService` manages user authentication and sessions.

> **Dependencies**

> This service uses:
> - `UserRepository` — Database access for user records.
> - `TokenProvider` — JWT generation and validation.

> **Public Methods**

> `login(username, password)` validates credentials against the database. It returns a signed JWT on success.

> `refreshToken(token)` accepts an expired token. It returns a new token if the refresh window is still open.

> *Principles applied: P1, P7, P11 — uses approved words, does not use technical nouns as verbs, one term per concept. Each paragraph covers one aspect of the class (purpose, dependencies, methods).*

The class that the documentation describes:

```java
// AuthenticationService.java
public class AuthenticationService {
    private final UserRepository users;
    private final TokenProvider tokens;

    /** AuthenticationService manages user authentication and sessions. */
    public AuthenticationService(UserRepository users, TokenProvider tokens) {
        this.users = users;
        this.tokens = tokens;
    }

    /** login validates credentials and returns a signed JWT. */
    public String login(String username, String password) {
        User user = users.findByUsername(username);
        if (user == null || !user.checkPassword(password)) {
            throw new AuthException("invalid credentials");
        }
        return tokens.sign(user.getId());
    }

    /** refreshToken accepts an expired token and returns a new one. */
    public String refreshToken(String token) {
        if (!tokens.isInRefreshWindow(token)) {
            throw new AuthException("refresh window closed");
        }
        return tokens.sign(tokens.subjectOf(token));
    }
}
```

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional code emphasizes pure functions, immutability, and type signatures. Documentation must separate the type signature explanation from the behavior description and the algebraic properties. Use paragraphs to separate the pure from the effectful.

> **Non-STE:** `validateInput :: Input -> Either ValidationError ValidatedInput` parses and validates raw user input, returning a `ValidatedInput` on success or a `ValidationError` with a list of field-level problems, it's pure and doesn't perform any I/O, composed internally from `parseField` and `checkConstraints` which are also pure.

> **STE:** `validateInput` parses and validates raw user input. It returns a `ValidatedInput` on success. It returns a `ValidationError` on failure. The function is pure and does not do I/O. It uses `parseField` and `checkConstraints` internally.

> **validateInput**

> `validateInput :: Input -> Either ValidationError ValidatedInput`

> This function parses and validates raw user input.

> **Return Value**

> The function returns a `ValidatedInput` on success. It returns a `ValidationError` on failure. The error includes a list of field-level problems.

> **Purity**

> This function is pure. It does not do I/O.

> **Internal Composition**

> The function composes two pure sub-functions:
> - `parseField` — Parses each input field.
> - `checkConstraints` — Validates field constraints.

> *Principles applied: P1, P2, P3 — uses approved words as their specified part of speech with approved meanings. The type signature gets its own paragraph. Purity and composition are separate topics with separate paragraphs.*

The Haskell implementation that the documentation describes:

```haskell
-- validateInput parses and validates raw user input.
validateInput :: Input -> Either ValidationError ValidatedInput
validateInput input =
    case parseField input of
        Left err  -> Left err
        Right fld -> checkConstraints fld

-- Return value:
--   Right ValidatedInput on success.
--   Left ValidationError on failure (with a list of field problems).

-- Purity:
--   The function is pure. It does no I/O.

-- Internal composition:
--   parseField    :: Input -> Either ValidationError Field
--   checkConstraints :: Field -> Either ValidationError ValidatedInput
```

### Procedural Documentation (C, Go, Bash)

Procedural code executes instructions in sequence. Documentation must separate the initialization from the main loop and the cleanup. Use paragraphs to show the phases of execution.

> **Non-STE:** The `processFiles` function scans a directory, opens each file, reads its contents line by line, applies a transformation, writes the output to a new file in the output directory, and then closes the file handle and logs the processing time for each file before moving to the next one, and finally prints a summary of how many files were processed and how long the whole operation took.

> **STE:** The `processFiles` function transforms each file in a directory. It scans the input directory and opens each file. It reads the contents and applies a transformation. It writes the output and closes the file. It records the processing time. It prints a summary with the file count and the total time.

> **processFiles**

> The `processFiles` function transforms every file in a directory.

> **Initialization**

> The function scans the input directory. It creates the output directory if it does not exist.

> **Processing Loop**

> For each file, the function:
> 1. Opens the file.
> 2. Reads the contents line by line.
> 3. Applies the transformation.
> 4. Writes the output to a new file in the output directory.
> 5. Closes the file handle.
> 6. Records the processing time.

> **Cleanup and Summary**

> The function closes all open handles. It prints a summary with the total number of files and the total processing time.

> *Principles applied: P1, P6, P7 — uses approved words, allows technical nouns (file, handle, directory), does not use technical nouns as verbs. The three phases (initialization, loop, cleanup) are separate paragraphs.*

The Go implementation that the documentation describes:

```go
// processFiles transforms every file in a directory.
func processFiles(inputDir, outputDir string) error {
    // Initialization: scan the input directory and make the output directory.
    entries, err := os.ReadDir(inputDir)
    if err != nil {
        return err
    }
    if err := os.MkdirAll(outputDir, 0o755); err != nil {
        return err
    }

    // Processing loop: open, read, transform, write, close, record.
    var total time.Duration
    for _, e := range entries {
        start := time.Now()
        data, err := os.ReadFile(filepath.Join(inputDir, e.Name()))
        if err != nil {
            return err
        }
        out := transform(data)
        if err := os.WriteFile(filepath.Join(outputDir, e.Name()), out, 0o644); err != nil {
            return err
        }
        total += time.Since(start)
    }

    // Cleanup and summary: close handles and print the summary.
    log.Printf("processed %d files in %s", len(entries), total)
    return nil
}
```

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative code describes the desired state. Documentation must separate the resource identity from the resource specification and the dependencies. Each resource gets its own paragraph group.

> **Non-STE:** This Terraform module creates an auto-scaling group with a launch template that provisions EC2 instances running Amazon Linux 2, attaches them to an application load balancer with a target group that health-checks the `/health` endpoint every 30 seconds, and creates security group rules to allow inbound traffic on port 443 from the load balancer and on port 22 from the bastion host CIDR `10.0.1.0/24`.

> **STE:** This Terraform module creates an auto-scaling group. It uses a launch template with Amazon Linux 2. It attaches the instances to an application load balancer. The load balancer checks the `/health` endpoint every 30 seconds. The security rules permit inbound traffic on port 443 and port 22.

> **Auto-Scaling Group Module**

> This module creates an auto-scaling group for EC2 instances.

> **Launch Template**

> The launch template defines the instance configuration:
> - Amazon Linux 2 as the operating system.
> - The application AMI from the latest build pipeline.

> **Load Balancer**

> The module creates an application load balancer. A target group routes traffic to the instances. The health check monitors the `/health` endpoint every 30 seconds.

> **Security Groups**

> The security rules permit:
> - Inbound traffic on port 443 from the load balancer.
> - Inbound traffic on port 22 from the bastion host CIDR `10.0.1.0/24`.

> *Principles applied: P1, P3, P11 — uses approved words with approved meanings, one term per concept. Each AWS resource type gets its own paragraph with a clear topic sentence.*

The Terraform source that the documentation describes:

```hcl
# main.tf — auto-scaling group module.
resource "aws_launch_template" "app" {
  # Launch template: Amazon Linux 2 with the latest build AMI.
  image_id      = data.aws_ami.latest.id
  instance_type = "t3.medium"
}

resource "aws_autoscaling_group" "app" {
  # Auto-scaling group: EC2 instances from the launch template.
  desired_capacity = 3
  launch_template {
    id = aws_launch_template.app.id
  }
}

resource "aws_lb_target_group" "app" {
  # Load balancer: health check on /health every 30 seconds.
  port     = 443
  protocol = "HTTPS"
  health_check {
    path     = "/health"
    interval = 30
  }
}

resource "aws_security_group_rule" "ssh" {
  # Security groups: SSH from the bastion CIDR only.
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  cidr_blocks       = ["10.0.1.0/24"]
}
```

### Systems Documentation (Rust Ownership, C Memory Management)

Systems documentation explains ownership, lifetimes, and memory safety. These are complex topics that need careful paragraph structure. Separate the ownership model explanation from the lifetime annotations and the unsafe code justifications.

> **Non-STE:** The `SharedBuffer` struct holds a reference-counted pointer to a heap-allocated byte buffer that can be shared across threads because it uses `Arc<Mutex<Vec<u8>>>` internally, the `read` method acquires the lock, copies the data out, and releases the lock; the `write` method acquires the lock, appends to the buffer, and releases the lock; and the `Drop` implementation decrements the reference count and frees the buffer when the last reference is dropped, but callers must ensure they don't hold the lock across await points because the `Mutex` is from `std` not `tokio`.

> **STE:** The `SharedBuffer` struct holds a reference-counted pointer to a byte buffer. It uses `Arc<Mutex<Vec<u8>>>` for thread safety. The `read` method acquires the lock, copies the data, and releases the lock. The `write` method acquires the lock, appends data, and releases the lock. The `Drop` implementation frees the buffer when the last reference is dropped. Do not hold the lock across await points.

> **SharedBuffer**

> `SharedBuffer` holds a reference-counted pointer to a heap-allocated byte buffer. It is safe to share across threads.

> **Internal Representation**

> The struct uses `Arc<Mutex<Vec<u8>>>`:
> - `Arc` provides shared ownership with atomic reference counting.
> - `Mutex` provides mutual exclusion for concurrent access.
> - `Vec<u8>` stores the raw bytes on the heap.

> **Methods**

> `read()` acquires the lock, copies the data out, and releases the lock.

> `write(data)` acquires the lock, appends `data` to the buffer, and releases the lock.

> **Drop Behavior**

> The `Drop` implementation decrements the reference count. It frees the buffer when the last reference is dropped.

> **Important Constraint**

> This struct uses `std::sync::Mutex`, not `tokio::sync::Mutex`. Do not hold the lock across `.await` points. Holding a `std` mutex across an await point causes a deadlock.

> *Principles applied: P1, P6, P7 — uses approved words, allows technical nouns (Arc, Mutex, Vec), does not use technical nouns as verbs. Ownership, methods, drop behavior, and constraints are separate paragraphs with clear topic sentences.*

The Rust implementation that the documentation describes:

```rust
// shared_buffer.rs — thread-safe shared byte buffer.
use std::sync::{Arc, Mutex};

pub struct SharedBuffer {
    // Internal representation: Arc<Mutex<Vec<u8>>>.
    inner: Arc<Mutex<Vec<u8>>>,
}

impl SharedBuffer {
    /// read acquires the lock, copies the data out, releases the lock.
    pub fn read(&self) -> Vec<u8> {
        let guard = self.inner.lock().unwrap();
        guard.clone()
    }

    /// write acquires the lock, appends data, releases the lock.
    pub fn write(&self, data: &[u8]) {
        let mut guard = self.inner.lock().unwrap();
        guard.extend_from_slice(data);
    }
}

// Drop behavior: the last Arc clone frees the buffer automatically.
// Important constraint: do NOT hold the std Mutex across .await points.
```

## Edge Cases

### Framework Names That Conflict with Approved Words

Some framework names are the same as unapproved STE words. The word `make` is an approved STE verb. GNU Make is a build tool. When documenting a Makefile, you must distinguish between the verb "make" and the tool name "Make".

**Guidance:** Capitalize the framework name when it conflicts with an approved word. Write "Make" for the tool, "make" for the verb. Use the topic sentence to establish which meaning applies.

> **Non-STE:** Run `make` to make the build artifacts. Then make sure the output directory exists before you make the tarball with `make package`.

> **STE:** Build the artifacts with the Make tool. Run `make` to compile the source files. Check that the `output/` directory exists. Run `make package` to create the tarball.

> **Build with Make**

> Use the Make tool to build the project.

> **Step 1 — Compile**

> Run `make` to compile the source files. Make writes the build artifacts to the `build/` directory.

> **Step 2 — Package**

> Check that the `output/` directory exists. Run `make package` to create the tarball.

> *Principles applied: P1, P3, P6 — uses approved words, allows "Make" as a technical noun, distinguishes the tool name from the verb. The topic sentence clarifies that "Make" refers to the build tool.*

A `Makefile` that matches the documentation:

```makefile
# Makefile — build and package with the Make tool.
build:
	# Run 'make' to compile the source files.
	$(CC) -o build/app src/main.c

package: build
	# Check that output/ exists, then create the tarball.
	mkdir -p output
	tar -czf output/app.tar.gz build/app

.PHONY: build package
```

### Code Keywords That Conflict with Paragraph Structure

Code keywords like `break`, `continue`, `return`, and `yield` have specific meanings in control flow. When documenting control flow in a paragraph, the keyword names are technical nouns (Rule 1.5). They do not violate Rule 1.7 even though they look like verbs.

Use backticks to set code keywords apart from prose. Start a paragraph about control flow with a topic sentence that names the keyword being discussed.

> **Non-STE:** The loop breaks when the sentinel value is found, and then we return the accumulated result; if it continues past the maximum iterations we throw an error instead.

> **STE:** The loop uses `break` to exit when it finds the sentinel value. The function uses `return` to send the result to the caller. If the loop runs past the maximum iterations, the function throws an error.

> **Loop Termination**

> The loop uses the `break` keyword to exit early. It `break`s when it finds the sentinel value.

> **Return Value**

> The function uses the `return` keyword to send the accumulated result to the caller.

> **Error Condition**

> The loop uses the `continue` keyword to skip the current iteration. If the loop runs past the maximum iterations, the function throws an error.

> *Principles applied: P5, P6, P7 — code keywords are technical nouns. Backticks mark them as code. Each paragraph covers one control flow concept.*

The Python loop that the documentation describes:

```python
# find_sentinel scans the list and stops at the sentinel value.
def find_sentinel(items, sentinel, max_iter):
    """Return the index of the sentinel, or raise after max_iter."""
    count = 0
    for index, value in enumerate(items):
        if value == sentinel:
            # break exits the loop when the sentinel is found.
            break
        if count >= max_iter:
            # past the maximum iterations, raise an error.
            raise TooManyIterations(index)
        count += 1
        # continue moves to the next item.
        continue
    return index
```

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

> **STE:**

> **Request Handler**

> The handler validates the request and calls `processPayload`.

> The handler checks these conditions:
> - The `Content-Type` header is `application/json`.
> - The request body is valid JSON.

> The code for the handler is:

> ```typescript
> function handler(req: Request): Response {
>   if (req.headers['content-type'] !== 'application/json') {
>     return { status: 415 };
>   }
>   const body = JSON.parse(req.body);
>   return processPayload(body);
> }
> ```

> The handler returns a `Response` object. It includes the processed data on success. It includes an error status on failure.

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

> *Principles applied: P1, P3 — uses approved words with approved meanings. The blank `*` lines between topics produce separate paragraphs in generated documentation. Each paragraph has one topic (purpose, pool behavior, acquire/release, safety rule).*

The Go doc comment that `go doc` renders into those paragraphs:

```go
// Package pool provides a bounded connection pool.
//
// New creates a pool with the given configuration. The pool keeps
// up to MaxConnections open connections. Connections are made on
// first use.
//
// Use Acquire to take a connection and Release to return it.
//
// Always call Release in a defer or finally block. This prevents
// the pool from running out of connections.
package pool
```

### Multi-Author Documents with Mixed Paragraph Styles

When many contributors write documentation, paragraph styles can become inconsistent. A README section written by one author may use long, dense paragraphs. Another section by a different author may use short, focused paragraphs.

**Guidance:** Apply structural linting to documentation. A documentation lint rule can flag paragraphs that exceed 5 sentences or that lack a clear topic sentence. Review mixed-author documents before publication. Break long paragraphs at topic boundaries. Add topic sentences where they are missing.

> **Non-STE:** The caching layer supports multiple backends including Redis, Memcached, and an in-memory store for development, each backend implements the `CacheBackend` interface which requires `get`, `set`, `delete`, and `clear` methods, the Redis backend is recommended for production because it supports persistence, replication, and clustering, the in-memory backend is acceptable for local development but it loses all data when the process restarts, Memcached is a good middle-ground for staging environments because it is simpler to operate than Redis while still providing network-accessible shared caching.

> **STE:** The caching layer supports Redis, Memcached, and an in-memory store. Each backend implements the `CacheBackend` interface. The interface requires `get`, `set`, `delete`, and `clear` methods. Use Redis for production. Redis supports persistence, replication, and clustering. Use Memcached for staging. Use the in-memory store only for development. The in-memory store loses data when the process restarts.

> **Caching Layer**

> The caching layer supports multiple backends: Redis, Memcached, and an in-memory store.

> **Backend Interface**

> Each backend implements the `CacheBackend` interface. The interface requires these methods:
> - `get(key)` — Get a cached value.
> - `set(key, value)` — Set a cached value.
> - `delete(key)` — Remove a cached value.
> - `clear()` — Remove all cached values.

> **Redis Backend (Recommended for Production)**

> The Redis backend supports persistence, replication, and clustering. Use Redis for production environments.

> **Memcached Backend (Staging)**

> The Memcached backend is simpler than Redis. It provides network-accessible shared caching. Use Memcached for staging environments.

> **In-Memory Backend (Development)**

> The in-memory backend stores data in the process memory. It loses all data when the process restarts. Use it only for local development.

> *Principles applied: P1, P3, P11 — uses approved words with approved meanings, one term per concept. The long paragraph was split into five topic-focused paragraphs. Each backend gets its own paragraph. The recommendation (production, staging, development) is explicit in each topic sentence.*

A lint rule (Vale) that enforces the guidance above:

```yaml
# .vale/styles/STE-Code/ParagraphStructure.yml
extends: existence
message: "Keep paragraphs to one topic; use a topic sentence and under 5 sentences."
scope: paragraph
level: warning
tokens:
  - '\b(utilize|leverage|employ|commence|terminate|initiate)\b'
```

## Grammar Notes

### Topic Sentences as Grammatical Anchors

In English grammar, the topic sentence of a paragraph carries the main clause. The sentences that follow carry subordinate information. This mirrors the structure of a complex sentence but at the paragraph level.

For code documentation, the topic sentence must be a declarative sentence in the simple present tense. It must name the topic (a class, function, module, or concept) in the subject position. The verb must be an approved STE verb that describes what the topic does or what the topic is.

Do not start a paragraph with a subordinate clause. Do not start with "Because...", "When...", "If...", or "Although...". Start with the subject. Attach the subordinate clause to a later sentence in the paragraph.

> **Non-STE:** Because the scheduler uses a work-stealing algorithm, tasks can migrate between threads, which improves load balancing but makes thread-local storage unreliable for task state.

> **STE:** The scheduler uses a work-stealing algorithm. Tasks can migrate between threads. This improves load balancing. Thread-local storage is not reliable for task state.

> The scheduler uses a work-stealing algorithm. Tasks can migrate between threads. This improves load balancing. However, thread-local storage is not reliable for task state.

> *Principles applied: P1, P3 — uses approved words. The topic sentence starts with the subject ("The scheduler"). The cause-and-effect relationship is shown through paragraph structure, not a subordinating conjunction at the start.*

The scheduler implementation that the paragraph describes:

```rust
// scheduler.rs — work-stealing scheduler.
pub struct Scheduler {
    queues: Vec<deque::Deque<Task>>,
}

impl Scheduler {
    /// The scheduler uses a work-stealing algorithm.
    pub fn run(&self) {
        for thread in 0..self.queues.len() {
            // Tasks migrate between threads. This improves load balancing.
            if let Some(task) = self.steal(thread) {
                task.execute();
            }
        }
    }
}
```

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
