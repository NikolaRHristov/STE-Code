<!-- a-sec6-rule6.1.md -->

# Rule 6.1 — Give Information Gradually

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec6-rule6.1](ste-code/grouped/), Rule 6.1

## Original Rule

In a descriptive text, give information gradually and make sure that each sentence contains only one subject. If you give too much information too quickly, your text will not be easy to understand, and it will be necessary for the reader to read it again.

## STE-Code Adaptation

In code documentation, give information gradually and make sure that each sentence contains only one subject. If you give too much information too quickly, your documentation will not be easy to understand, and it will be necessary for the developer to read it again.

Give the reader one piece of information at a time. Do not combine multiple actions, multiple conditions, or multiple subjects in one sentence. This rule applies to every form of code documentation: README files, API reference docs, docstrings, inline comments, commit messages, error messages, log entries, changelogs, and configuration files.

### Examples

> *Adapted from spec pair:* Non-STE: *During the approach to the runway, deviation pointers in the course indicators give commands to fly up or down and left or right. This information comes from the VHF transceivers, which are part of the Instrument Landing System … When the pilot responds to the commands, the aircraft can be flown over the runway centerline … and at a fixed angle … to the runway threshold. The localizer signals are processed by the transceiver and data are transmitted to Air Traffic Control.*  |  STE: *The Instrument Landing System on the aircraft shows data that helps the pilot during the approach to the runway. This system shows the pilot the deviations from the localizer course and the glideslope path. The localizer course aligns with the centerline of the runway … During the approach … deviation pointers … show the pilot in which direction the aircraft must go: Left or right … Up or down … This data … comes from two VHF transceivers. These transceivers transmit this data to Air Traffic Control.*

The code-domain example below maps the same principle onto an authentication middleware: the Non-STE version packs the whole request lifecycle into one sentence; the STE version gives it one subject per sentence.

> **Non-STE:** The authentication middleware validates bearer tokens from the authorization header by calling the `validateToken` function in the security module which decodes the JWT payload using the `HS256` algorithm from the `jwt-signer` library and checks the `exp` claim against the current server time before extracting the `sub` and `role` claims and attaching them as properties on the `request.auth` object, and if the token is expired or malformed the middleware returns a `401 Unauthorized` response with a JSON error body containing a `message` field and an `errorCode` field set to `TOKEN_EXPIRED` or `TOKEN_MALFORMED` respectively, while also logging the failure to the audit trail via the `AuditLogger.log` static method which writes to the `audit_events` table in the primary database using an asynchronous write pattern that does not block the response pipeline.

> **STE:** The authentication middleware validates each incoming request. The middleware reads the bearer token from the `Authorization` header. It sends the token to the `validateToken` function in the `security` module. The `validateToken` function decodes the JWT payload. It uses the `HS256` algorithm from the `jwt-signer` library. Then it compares the `exp` claim with the current server time. If the token is not expired and not malformed, the function gets the `sub` and `role` claims. It attaches these claims as properties on the `request.auth` object. If the token is expired, the middleware returns a `401 Unauthorized` response. The response body is a JSON object:
> - The `message` field contains a description of the error.
> - The `errorCode` field is set to `TOKEN_EXPIRED`.
> If the token is malformed, the middleware returns a `401 Unauthorized` response. The `errorCode` field in the response is set to `TOKEN_MALFORMED`. The middleware also logs each failure to the audit trail. It calls the `AuditLogger.log` static method. This method writes a record to the `audit_events` table in the primary database. The write uses an asynchronous pattern that does not block the response pipeline.
>
> *Code-domain example — each sentence in the STE version contains only one subject, giving information gradually.*

The STE prose above describes the following middleware contract. A reader who wants the runnable shape can read it directly:

```typescript
// Non-STE: one dense comment that describes the whole pipeline at once.
// The authenticate middleware validates bearer tokens from the request
// authorization header by calling validateToken which decodes the JWT with
// HS256, checks the exp claim, attaches sub/role to request.auth, returns
// 401 with TOKEN_EXPIRED or TOKEN_MALFORMED on failure, and logs to audit.

// STE: split the contract into one fact per line.
// The authenticate middleware checks each incoming request.
// It reads the bearer token from the Authorization header.
// It sends the token to validateToken in the security module.
// If the token is expired, the middleware returns 401 with errorCode TOKEN_EXPIRED.
// If the token is malformed, the middleware returns 401 with errorCode TOKEN_MALFORMED.
// The middleware logs each failure through AuditLogger.log.
function authenticate(req: Request, res: Response, next: NextFunction): void {
  const token = req.headers.authorization?.replace("Bearer ", "");
  if (!token) { return res.status(401).json({ message: "Missing token", errorCode: "TOKEN_MALFORMED" }); }
  const result = validateToken(token);
  if (result.status === "expired") { return res.status(401).json({ message: "Token expired", errorCode: "TOKEN_EXPIRED" }); }
  if (result.status === "malformed") { return res.status(401).json({ message: "Token malformed", errorCode: "TOKEN_MALFORMED" }); }
  req.auth = { sub: result.sub, role: result.role };
  next();
}
```

> **See also:** Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure; Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence; Rule 6.4 — Use Paragraphs to Show Related Information; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic; Rule 1.1 — Use Approved Words from the STE-Code Dictionary; Rule 1.11 — One Term per Concept

### Code-Domain Explanation

This rule applies to all forms of code documentation. The goal is the same in each context: give the reader one piece of information at a time. Do not combine multiple actions, multiple conditions, or multiple subjects in one sentence.

**README files.** A README is the first document a developer reads. Each section must introduce one concept. Do not describe the architecture, the installation steps, and the API overview in one long paragraph. Start with the purpose of the project. Then give the installation instructions in a separate section. Then show a basic usage example. Each sentence inside a section must have only one subject. If the installation needs three commands, explain each command in its own sentence.

```markdown
<!-- Non-STE: three unrelated topics in one sentence -->
Our library is a fast, type-safe HTTP client that you install with `npm i httpkit`,
configure with a base URL and retry policy, and call from React, Node, and Deno.

<!-- STE: one concept per sentence -->
This library is a type-safe HTTP client.
Install it with `npm i httpkit`.
Set the base URL in the client configuration.
The client supports a retry policy.
You can use the client in React, Node, and Deno.
```

**API documentation.** Each endpoint description must be a self-contained unit. Describe the HTTP method and the path in one sentence. Describe the request parameters in separate sentences. Describe the response structure with one sentence per field or one sentence per status code. Do not chain the parameter descriptions into one compound sentence that also includes the response format and the error conditions. A developer who looks up one parameter must not read a paragraph that describes ten unrelated things.

**Docstrings and inline comments.** A function docstring must describe one behavior per sentence. If a function does three things, use three sentences. Do not write a single sentence that lists all parameters, all return values, and all side effects. Each parameter needs its own line or sentence. Each return condition needs its own sentence. Comments inside the function body must explain one line or one block at a time — not summarize the entire function in one dense sentence.

**Commit messages.** Each commit message must describe one logical change. A commit message that lists five unrelated modifications forces the reviewer to read it multiple times. Use one sentence for the summary line. Use separate sentences in the body for each sub-change. Do not write: "Add user auth, fix login bug, update deps, and refactor DB layer" as one sentence. Split it into a summary and bullet points.

**Error messages and log entries.** Each error message must state one problem clearly. A message that says "The file could not be opened because it does not exist or the permissions are wrong or the disk is full" gives too much information too quickly. Split the conditions into separate error messages with distinct error codes. Log entries must also follow this rule: one event per log line, with one subject and one action.

**Changelogs and release notes.** Each entry must describe one change. Do not combine a new feature, a bug fix, and a deprecation notice in one sentence. Use one sentence per change type. Use bullet lists to separate unrelated changes.

### Paradigm-Specific Guidance

**Object-Oriented (Java, C++, C#, Python classes).** Describe one method or one class behavior per sentence. When you document method chaining or inheritance chains, give the information in sequence. First describe the base class behavior. Then describe the override. Do not write a sentence that covers the base class, the override, and the side effect on a parent field all at once.

````markdown
> **Non-STE:** The `PaymentProcessor` class extends `BaseProcessor` and overrides the `validate` method to check the card number format using a regex pattern before calling `super.validate()` which runs the standard fraud check and then, if both checks pass, calls the `charge` method on the `gateway` field which was injected via the constructor that also accepts an optional `Logger` instance for recording transaction outcomes.

> **STE:** The `PaymentProcessor` class extends `BaseProcessor`. It overrides the `validate` method. The override checks the card number format. It uses a regex pattern for the check. After the format check passes, the method calls `super.validate()`. The parent `validate` method runs the standard fraud check. If both checks pass, the method calls the `charge` method on the `gateway` field. The `gateway` field is injected through the constructor. The constructor also accepts an optional `Logger` instance. The `Logger` records the transaction outcome.
>
> *Principles applied: P10, P11 — each sentence has one subject; the override chain is described step by step.*
````

```java
// STE docstring for the class — one fact per line.
/**
 * The PaymentProcessor class extends BaseProcessor.
 * It overrides the validate method.
 * The override checks the card number format with a regex pattern.
 * After the format check passes, it calls super.validate().
 * If both checks pass, it calls charge on the gateway field.
 * The gateway field is injected through the constructor.
 */
public class PaymentProcessor extends BaseProcessor {
  private final Gateway gateway;
  private final Logger logger;
  public PaymentProcessor(Gateway gateway, Logger logger) {
    this.gateway = gateway;
    this.logger = logger;
  }
}
```

**Functional (Haskell, Elixir, Clojure, Rust).** Describe one transformation or one function application per sentence. When you document a pipeline of functions or a chain of monadic operations, describe each step in its own sentence. Do not write one sentence that describes an entire `>>=` chain or a deeply nested composition.

````markdown
> **Non-STE:** The `processOrder` function takes an `Order` and pipes it through `validateOrder` which returns an `Either ValidationError ValidatedOrder`, then through `calculateTotal` which applies discount rules and tax rates, then through `createInvoice` which generates a PDF and stores it in S3, and finally through `sendConfirmation` which emails the customer and updates the order status in the database.

> **STE:** The `processOrder` function accepts an `Order` value. It applies `validateOrder` to the order. The `validateOrder` function returns an `Either ValidationError ValidatedOrder`. Then it applies `calculateTotal` to the validated order. The `calculateTotal` function applies the discount rules. It also applies the tax rates. Then it applies `createInvoice` to the order with the total. This function makes a PDF invoice. It stores the PDF in S3. Then it applies `sendConfirmation` to the invoice. This function sends an email to the customer. It also updates the order status in the database.
>
> *Principles applied: P2, P10 — each transformation gets its own sentence; the pipeline is broken into discrete steps with one subject each.*
````

```elixir
# STE: document each pipeline step on its own line.
# process_order accepts an Order.
# It applies validate_order to the order.
# It applies calculate_total to the validated order.
# It applies create_invoice to the order with the total.
# It applies send_confirmation to the invoice.
def process_order(order) do
  order
  |> validate_order()
  |> calculate_total()
  |> create_invoice()
  |> send_confirmation()
end
```

**Procedural (C, Go, Bash).** Describe one step or one branch per sentence. When you document a multi-step procedure or a branching control flow, each sentence must contain exactly one subject performing one action. Do not describe an if-else chain, a loop body, and the cleanup code all in one sentence.

````markdown
> **Non-STE:** The `backup` script checks if the target directory exists and creates it if it doesn't, then iterates over all files in the source directory, compresses each one with gzip, copies the compressed file to the backup location while verifying the checksum, and finally removes files older than 30 days from the backup directory while logging each removal to syslog.

> **STE:** The `backup` script checks if the target directory exists. If the target directory does not exist, the script creates it. Then the script iterates over all files in the source directory. It compresses each file with gzip. It copies the compressed file to the backup location. The script checks the checksum of each copied file. Then the script removes files that are older than 30 days from the backup directory. It logs each removal to syslog.
>
> *Principles applied: P7, P10 — each procedural step is its own sentence; conditional branches are separate sentences.*
````

```bash
# STE: one step per comment line.
# The script checks if the target directory exists.
# If the target directory does not exist, the script makes it.
# Then the script iterates over all files in the source directory.
# It compresses each file with gzip.
# It copies the compressed file to the backup location.
# It checks the checksum of each copied file.
# Then it removes files older than 30 days.
for f in "$SRC"/*; do
  gzip -c "$f" > "$DST/$(basename "$f").gz"
  sha256sum "$DST/$(basename "$f").gz" >> "$DST/checksums.txt"
done
find "$DST" -mtime +30 -delete
```

**Declarative (SQL, Terraform, Kubernetes YAML).** Describe one resource, one constraint, or one column per sentence. When you document a declarative configuration, do not describe the resource, its dependencies, its conditions, and its outputs all in one sentence. Each declaration needs its own sentence.

````markdown
> **Non-STE:** The `aws_instance` resource creates an EC2 instance with the specified AMI and instance type, attaches the security group defined in `aws_security_group.web_sg` which allows inbound traffic on ports 80 and 443 from the VPC CIDR block, and also attaches an IAM instance profile that grants S3 read access for fetching application artifacts during the user-data bootstrap script which installs nginx and starts the service.

> **STE:** The `aws_instance` resource makes an EC2 instance. It uses the AMI that the `ami` variable specifies. It uses the instance type that the `instance_type` variable specifies. The resource attaches the security group from `aws_security_group.web_sg`. This security group allows inbound traffic on ports 80 and 443. The traffic comes from the VPC CIDR block. The resource also attaches an IAM instance profile. This profile gives S3 read access. The access lets the instance get application artifacts. The user-data script installs nginx. Then it starts the nginx service.
>
> *Principles applied: P5, P10 — each resource relationship gets its own sentence; dependencies are described one by one.*
````

```hcl
# STE: one relationship per comment line.
# The aws_instance resource makes an EC2 instance.
# It uses the AMI that the ami variable specifies.
# It uses the instance type that the instance_type variable specifies.
# The resource attaches the security group from aws_security_group.web_sg.
# This security group allows inbound traffic on ports 80 and 443.
resource "aws_instance" "web" {
  ami           = var.ami
  instance_type = var.instance_type
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.web.name
  user_data = <<-EOT
    #!/bin/bash
    # The user-data script installs nginx.
    # Then it starts the nginx service.
    apt-get install -y nginx
    systemctl start nginx
  EOT
}
```

**Systems (Rust ownership docs, C memory docs).** Describe one ownership rule, one lifetime constraint, or one memory operation per sentence. When you document borrowing rules or memory allocation patterns, each sentence must state one rule clearly. Do not combine the allocation, the ownership transfer, the lifetime annotation, and the deallocation guarantee in one sentence.

````markdown
> **Non-STE:** The `allocate_buffer` function allocates a buffer of the given size on the heap using `malloc`, returns a pointer to the caller who becomes responsible for freeing it with `free` when done, but if allocation fails it returns `NULL` and sets `errno` to `ENOMEM` without modifying the output parameter that holds the allocated size.

> **STE:** The `allocate_buffer` function allocates a buffer on the heap. It uses `malloc` for the allocation. The buffer size is the value of the `size` parameter. The function returns a pointer to the buffer. The caller becomes the owner of the buffer. The caller must free the buffer with `free`. If the allocation fails, the function returns `NULL`. It also sets `errno` to `ENOMEM`. The output parameter for the allocated size stays unchanged.
>
> *Principles applied: P7, P10, P11 — each memory contract rule gets its own sentence; ownership transfer and error handling are separate subjects.*
````

```c
// STE: document each memory contract rule on its own line.
// The allocate_buffer function allocates a buffer on the heap.
// It uses malloc for the allocation.
// The function returns a pointer to the buffer.
// The caller becomes the owner of the buffer.
// The caller must free the buffer with free.
// If the allocation fails, the function returns NULL.
// It also sets errno to ENOMEM.
void* allocate_buffer(size_t size, size_t* out_size) {
  void* buf = malloc(size);
  if (!buf) { errno = ENOMEM; return NULL; }
  *out_size = size;
  return buf;
}
```

### Extended Examples

**Example 2: Commit message — single vs. compound change description**

> **Non-STE:** Add user authentication with JWT tokens, fix the race condition in the connection pool that caused timeouts under load, update all dependencies to their latest stable versions, and refactor the error handling middleware to use a centralized error handler.

> **STE:** Add user authentication with JWT tokens. Fix race condition in connection pool. The race condition caused timeouts under load. Update all dependencies to latest stable versions. Refactor error handling middleware. The middleware now uses a centralized error handler.
>
> *Principles applied: P6, P10 — each commit message describes one change; the summary line and body both use single-subject sentences.*

```text
# Non-STE — one compound sentence in the subject line
Add user auth, fix pool race, bump deps, refactor error middleware

# STE — one change per line
Add user authentication with JWT tokens.

Fix race condition in connection pool.
The race condition caused timeouts under load.

Update all dependencies to latest stable versions.

Refactor error handling middleware.
The middleware now uses a centralized error handler.
```

**Example 3: Changelog entry — compound vs. gradual release note**

> **Non-STE:** The v2.4.0 release introduces a new `BatchProcessor` API that allows processing up to 10,000 items concurrently with configurable backpressure, deprecates the old `ProcessQueue` class which will be removed in v3.0.0, fixes a memory leak in the WebSocket handler that occurred when clients disconnected without sending a close frame, and improves the performance of the JSON parser by 40% through SIMD optimizations.

> **STE:** The v2.4.0 release has these changes. BREAKING: The `ProcessQueue` class is deprecated. It will be removed in v3.0.0. Use the new `BatchProcessor` API instead. The `BatchProcessor` API can process up to 10,000 items concurrently. It supports configurable backpressure. Fix memory leak in the WebSocket handler. The leak occurred when clients disconnected without a close frame. Improve JSON parser performance by 40 percent. The improvement uses SIMD optimizations.
>
> *Principles applied: P10, P11 — each release note entry is its own sentence; the deprecation notice and its replacement are separate but adjacent.*

```markdown
<!-- STE changelog entry -->
## v2.4.0

BREAKING: The `ProcessQueue` class is deprecated.
It will be removed in v3.0.0.
Use the new `BatchProcessor` API instead.

The `BatchProcessor` API can process up to 10,000 items concurrently.
It supports configurable backpressure.

Fix memory leak in the WebSocket handler.
The leak occurred when clients disconnected without a close frame.

Improve JSON parser performance by 40 percent.
The improvement uses SIMD optimizations.
```

**Example 4: API reference — compound vs. gradual parameter documentation**

> **Non-STE:** The `GET /api/users` endpoint accepts optional `page` and `limit` query parameters for pagination, a `filter` parameter that supports `role`, `status`, and `created_after` fields with comma-separated values, and returns a JSON object containing a `data` array of user objects each with `id`, `email`, `name`, and `role` fields along with a `meta` object that includes `total`, `page`, and `has_more` pagination fields, and responds with `400` if the filter syntax is invalid or `401` if the request is missing a valid bearer token.

> **STE:** The `GET /api/users` endpoint returns a list of users. The endpoint accepts these optional query parameters for pagination:
> - `page` — the page number, starting from 1.
> - `limit` — the number of users per page.
> The endpoint accepts a `filter` parameter. The `filter` parameter supports these fields:
> - `role`
> - `status`
> - `created_after`
> Separate the values with commas. The response is a JSON object with these fields:
> - `data` — an array of user objects.
> - `meta` — a pagination metadata object.
> Each user object has these fields: `id`, `email`, `name`, `role`.
> The `meta` object has these fields: `total`, `page`, `has_more`.
> The endpoint returns `400` for an invalid filter syntax. It returns `401` for a missing or invalid bearer token.
>
> *Principles applied: P10, P11 — each parameter, response field, and error code gets its own sentence; the structure is built gradually with one concept per line.*

```yaml
# STE OpenAPI snippet — each parameter and response field on its own line
get:
  summary: Return a list of users.
  parameters:
    - name: page          # The page number, starting from 1.
    - name: limit         # The number of users per page.
    - name: filter        # Supports role, status, created_after (comma-separated).
  responses:
    '200':
      description: A list of users.
      content:
        application/json:
          schema:
            properties:
              data:   # An array of user objects.
              meta:   # A pagination metadata object.
    '400':
      description: The filter syntax is invalid.
    '401':
      description: The request is missing a valid bearer token.
```

**Example 5: Docstring — compound vs. gradual function description**

> **Non-STE:** `def connect(db_url, timeout=30, retries=3)` establishes a database connection using the provided URL string, waits up to `timeout` seconds for the connection to succeed, and automatically retries up to `retries` times with exponential backoff if the initial attempt fails, returning a `Connection` object on success or raising `ConnectionError` if all retries are exhausted.

> **STE:** Connect to a database with the specified URL. Wait up to `timeout` seconds for the connection. Retry up to `retries` times if the connection fails. Use exponential backoff between retries. Return a `Connection` object on success. Raise `ConnectionError` if all retries are exhausted.
>
> *Principles applied: P2, P10 — each behavior is its own sentence; the return type and error condition are separate subjects.*

```python
# Non-STE: one sentence lists the URL, timeout, retries, backoff, return, and raise.
def connect(db_url, timeout=30, retries=3):
    """Establishes a database connection using the provided URL string, waits up
    to timeout seconds for the connection to succeed, and automatically retries
    up to retries times with exponential backoff if the initial attempt fails,
    returning a Connection object on success or raising ConnectionError if all
    retries are exhausted."""

# STE: one behavior per line.
def connect(db_url, timeout=30, retries=3):
    """Connect to a database with the specified URL.
    Wait up to timeout seconds for the connection.
    Retry up to retries times if the connection fails.
    Use exponential backoff between retries.
    Return a Connection object on success.
    Raise ConnectionError if all retries are exhausted.
    """
```

**Example 6: Configuration file comment — compound vs. gradual explanation**

> **Non-STE:** The `cache.ttl` setting controls how long cached items live in memory before they are evicted and must be re-fetched from the origin server, and setting it too low will increase load on the database while setting it too high will serve stale data to users, so the recommended value is 300 seconds for most workloads unless you have a write-heavy workload in which case 60 seconds is more appropriate.

> **STE:** The `cache.ttl` setting controls the cache item lifetime. Items that are older than this value are evicted from memory. After eviction, items are fetched again from the origin server. A low value increases the load on the database. A high value can serve stale data to users. The recommended value is 300 seconds for most workloads. For write-heavy workloads, use 60 seconds instead.
>
> *Principles applied: P10, P12 — each configuration behavior, trade-off, and recommendation has its own sentence with a single subject.*

```yaml
# Non-STE: one comment sentence combines lifetime, eviction, trade-offs, and the recommendation.
cache.ttl: 300   # Controls how long cached items live before eviction and re-fetch; low increases DB load, high serves stale data; 300 for most, 60 for write-heavy.

# STE: one fact per comment line.
cache.ttl: 300
# The cache.ttl setting controls the cache item lifetime.
# Items older than this value are evicted from memory.
# After eviction, items are fetched again from the origin server.
# A low value increases the load on the database.
# A high value can serve stale data to users.
# The recommended value is 300 seconds for most workloads.
# For write-heavy workloads, use 60 seconds instead.
```

### Edge Cases

**When a framework name contains multiple concepts.** Some technical names combine multiple actions or entities into one identifier (for example, `CreateReadUpdateDelete` or `UserAuthenticationService`). Treat the full identifier as one technical noun. Do not split it across sentences. The rule applies to the surrounding prose, not to the technical name itself.

````markdown
> **Non-STE:** The `UserAuthenticationAndAuthorizationService` handles login and permission checks.

> **STE:** The `UserAuthenticationAndAuthorizationService` handles user login. It also handles permission checks.
>
> *Principles applied: P5 — the technical noun stays intact; the description around it uses single-subject sentences.*
````

**When generated documentation produces compound output.** Tools such as OpenAPI generators, JSDoc renderers, and Sphinx autodoc often produce compound sentences from structured metadata. If you cannot control the output format, add a plain-language summary above the generated content. The summary must follow Rule 6.1. The generated content is exempt from this rule unless you edit the source annotations.

**When a code keyword conflicts with single-subject structure.** Control flow keywords such as `if`, `else`, `while`, and `try/catch` describe branching logic that naturally has multiple subjects. Use one sentence per branch. Do not describe the condition, the success path, and the failure path in one sentence. Use separate sentences for the `try` block description and the `catch` block description.

````markdown
> **Non-STE:** If the file exists and is readable, the function reads its contents into a buffer and parses it as JSON, otherwise it returns a `FileNotFound` error or a `PermissionDenied` error depending on which check failed.

> **STE:** The function checks if the file exists. It also checks if the file is readable. If both checks pass, the function reads the file contents. It stores the contents in a buffer. Then it parses the buffer as JSON. If the file does not exist, the function returns a `FileNotFound` error. If the file is not readable, the function returns a `PermissionDenied` error.
>
> *Principles applied: P10, P11 — each condition and each outcome is its own sentence; the branching logic is described step by step.*
````

```python
# STE: one branch per comment line.
# The function checks if the file exists.
# It also checks if the file is readable.
# If both checks pass, the function reads the file contents.
# Then it parses the buffer as JSON.
# If the file does not exist, the function returns FileNotFound.
# If the file is not readable, the function returns PermissionDenied.
def load_config(path: str) -> dict:
    if not os.path.exists(path):
        raise FileNotFound(path)
    if not os.access(path, os.R_OK):
        raise PermissionDenied(path)
    with open(path) as fh:
        return json.load(fh)
```

**When brevity is required (CLI help text and error codes).** Some contexts require very short text. A CLI `--help` flag or an error code string has limited space. In these contexts, use the minimum number of sentences. However, each sentence must still have only one subject. Use sentence fragments only when the display format enforces them (for example, a one-line usage string). For all other text, use complete single-subject sentences.

```text
# Non-STE: one packed usage string that mixes the command, the flag, and the effect.
# Usage: app sync --remote <url> fetches and merges remote changes into your local branch

# STE: one subject per fragment, as the display format enforces.
# Usage: app sync
#   --remote <url>   The remote repository URL.
#   Fetches remote changes.
#   Merges them into your local branch.
```

**When translating existing documentation.** When you rewrite documentation that uses compound sentences, check if the compound structure hides a logical dependency. If action B depends on action A, describe A first in its own sentence. Then describe B. Do not combine them. If the actions are independent, still separate them but use paragraph structure to group related sentences.

### Cross-References

- **Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure:** After you apply Rule 6.1 to split compound sentences, use key words and key phrases (such as "Then", "After", "If", "When") to connect the resulting short sentences into a logical flow.
- **Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence:** Single-subject sentences naturally have fewer words. Apply Rule 6.1 first, then check each sentence against the 25-word limit.
- **Rule 6.4 — Use Paragraphs to Show Related Information:** After you split a compound sentence into several short sentences, group the related sentences into one paragraph. Use paragraph breaks to separate different subjects or different phases of a process.
- **Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic:** Each paragraph that results from applying Rule 6.1 must have one topic. If the sentences in a paragraph describe different subjects, split the paragraph.
- **Rule 1.11 — One Term per Concept:** When you split a compound sentence, make sure you use the same term for the same concept across all the new sentences.
- **Rule 1.1 — Use Approved Words:** The short sentences that you make with Rule 6.1 must use words from the STE-Code dictionary. Prefer plain verbs: use `make` (not "create" or "generate"), `start` (not "initiate" or "commence"), `stop` (not "terminate" or "halt"), `get` (not "retrieve" or "fetch"), `send` (not "transmit" or "dispatch"), `show` (not "display" or "render"), `set` (not "configure" or "assign"), `check` (not "verify" or "ensure").

### Grammar Notes

The original ASD-STE100 Rule 6.1 is based on a principle from cognitive linguistics: the human working memory can hold approximately four to seven items at one time. When a sentence contains multiple subjects, multiple verbs, and multiple objects, the reader must hold all of them in working memory until the sentence ends. This increases the cognitive load and the risk of misunderstanding. In code documentation, where the reader is already processing technical concepts, code structure, and logic, the cognitive load is even higher.

**Single-subject constraint.** Each sentence must have exactly one grammatical subject. The subject is the noun phrase that performs the action of the main verb. In the sentence "The function validates the input and returns a result", there is one subject ("The function") and two verbs ("validates" and "returns"). This is acceptable because the two actions share the same subject. However, in the sentence "The function validates the input and the middleware logs the result", there are two subjects ("The function" and "the middleware"). This must be split into two sentences: "The function validates the input. The middleware logs the result."

**Coordinating conjunctions.** The words "and", "or", and "but" often signal that a sentence has multiple subjects. When you see a coordinating conjunction that joins two independent clauses (each with its own subject and verb), split the sentence at the conjunction. When the conjunction joins two verbs or two objects that share the same subject, keep the sentence.

**Subordinating conjunctions.** The words "because", "since", "although", "while", "when", "if", and "unless" introduce dependent clauses. A sentence with one main clause and one dependent clause is acceptable under Rule 6.1, provided the dependent clause does not introduce a new subject with its own chain of actions. If the dependent clause contains multiple subjects or multiple actions, move it to its own sentence.

**Relative clauses.** The words "which", "that", and "who" introduce relative clauses. A relative clause that describes the main subject is acceptable. A relative clause that introduces a new subject and a chain of new actions is not acceptable. Split it into its own sentence.

**Paragraph flow after splitting.** When you split a long compound sentence into many short sentences, the text can feel choppy. Use the techniques from Rule 6.2 (key words and key phrases) to connect the short sentences. Use Rule 6.4 (paragraphs) to group related sentences. The result is a text that is easy to scan and easy to understand on the first reading.

**Imperative mood in procedures.** In procedural documentation, each step uses the imperative mood with an implied subject ("you"). The implied subject is the same for every step. This means that imperative sentences naturally follow Rule 6.1: each step has one implied subject and one action. Do not combine two actions in one imperative step. Write "Stop the server. Then restart the server." Do not write "Stop and restart the server."

---

<!-- a-sec6-rule6.2.md -->

# Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec6-rule6.2](ste-code/grouped/), Rule 6.2

## Original Rule

Key words are words that occur in a text to connect different ideas, and key phrases are phrases that have the same function.

These key words and key phrases show how information in a text is related and give the text a logical structure.

You can also use connecting words and connecting phrases to help the reader understand the logical flow of ideas in the text. Connecting words and connecting phrases have the function of traffic signs, which tell the reader if the information is new, different, or a result of previous information. Examples of approved connecting words are: "and," "but," "then," "thus," and examples of connecting phrases are "as a result," and "at the same time."

When you use key words and key phrases, make sure that you do not change them in your text. The same terminology will keep your text clear and correct.

## STE-Code Adaptation

In code documentation, use key words and key phrases to connect related ideas across sentences. Key words are terms that occur multiple times in a documentation block to link different concepts together. Key phrases are multi-word expressions that serve the same connecting function.

These key words and key phrases show how information in the documentation is related and give the documentation a logical structure.

You can also use connecting words and connecting phrases to help the developer understand the logical flow of ideas. Connecting words and connecting phrases have the function of traffic signs, which tell the reader if the information is new, different, or a result of previous information. Examples of approved connecting words are: "and," "but," "then," "thus," and examples of connecting phrases are "as a result," and "at the same time."

When you use key words and key phrases, make sure that you do not change them in your documentation. The same terminology will keep your documentation clear and correct.

> **Connecting words and phrases approved in STE-Code:** `and`, `but`, `then`, `thus`, `also`, `however`, `therefore`, `for example`, `as a result`, `at the same time`. Use these at the start of a sentence so the reader sees the signal before the content. Do not use `moreover`, `furthermore`, `nevertheless`, `subsequently`, or `utilize`/`leverage` as connectors — they are not in the approved set.

### Examples

> *Adapted from spec pair:* Non-STE: "Use key words to connect ideas in a text and keep them unchanged."  |  STE: "Use key words and key phrases to connect related ideas across sentences, and do not change them in your text."

The example that follows is the STE text from the adapted example for rule 6.1. In the text, you can see how the underlined key words and key phrases connect sentences and their related ideas. This makes the documentation much easier to read and understand.

**Sentence 1 and Sentence 2:**

> Sentence 1: The authentication middleware validates each incoming request.
> Sentence 2: The middleware reads the bearer token from the `Authorization` header.

Sentence 2 uses the key word "middleware" again to add more information about sentence 1.

**Sentence 2 and Sentence 3:**

> Sentence 2: The middleware reads the bearer token from the `Authorization` header.
> Sentence 3: It sends the token to the `validateToken` function in the `security` module.

Sentence 3 uses the key word "token" again and adds new information about what the middleware does with it.

**Sentence 3 and Sentence 4:**

> Sentence 3: It sends the token to the `validateToken` function in the `security` module.
> Sentence 4: The `validateToken` function decodes the JWT payload.

Sentence 4 uses the key phrase "`validateToken` function" again and gives more details about its behavior.

**Sentence 4 and Sentence 5:**

> Sentence 4: The `validateToken` function decodes the JWT payload.
> Sentence 5: It uses the `HS256` algorithm from the `jwt-signer` library.

Sentence 5 uses the key word "uses" to connect to "decodes" in sentence 4, showing the method by which the function operates.

**Sentence 8 and Sentence 9:**

> Sentence 8: If the token is expired, the middleware returns a `401 Unauthorized` response.
> Sentence 9: The response body is a JSON object.

Sentence 9 uses the key word "response" again to add more detail about what the response contains.

**Sentence 11 and Sentence 12:**

> Sentence 11: The `errorCode` field is set to `TOKEN_EXPIRED`.
> Sentence 12: If the token is malformed, the middleware returns a `401 Unauthorized` response.

Sentences 11 and 12 use the key word "token" again. Sentence 12 then introduces the alternative condition "malformed" by contrasting with the previous condition "expired."

**Sentence 14 and Sentence 15:**

> Sentence 14: The middleware also logs each failure to the audit trail.
> Sentence 15: It calls the `AuditLogger.log` static method.

Sentence 15 uses the key phrase "audit" again (from "audit trail") to connect the logging mechanism with the specific method name.

There is also a logical connection between the three groups of sentences:

- Group 1 (Sentences 1 thru 7): token validation, `validateToken`, JWT, claims, `request.auth`
- Group 2 (Sentences 8 thru 13): error responses, `401 Unauthorized`, `errorCode`, `TOKEN_EXPIRED`, `TOKEN_MALFORMED`
- Group 3 (Sentences 14 thru 17): audit trail, `AuditLogger.log`, database, `audit_events`, asynchronous write

Full runnable source that shows the key-word chain across the whole block (the documentation describes exactly this code):

```python
# security/middleware.py
from security.validate import validate_token
from security.audit import AuditLogger

MALFORMED = "TOKEN_MALFORMED"
EXPIRED = "TOKEN_EXPIRED"

def authentication_middleware(request):
    # The middleware reads the bearer token from the Authorization header.
    token = request.headers.get("Authorization", "").removeprefix("Bearer ")
    # The middleware sends the token to validate_token.
    claims = validate_token(token)
    # The middleware writes request.auth from the claims.
    request.auth = claims
    return request

def validate_token(token):
    # validate_token decodes the JWT payload with HS256.
    # validate_token raises TOKEN_EXPIRED when the token is old.
    # validate_token raises TOKEN_MALFORMED when the token is broken.
    ...

def error_response(code):
    # The middleware returns a 401 response when the token fails.
    return {"errorCode": code, "message": "Unauthorized"}

AuditLogger.log("auth_failure", {"errorCode": EXPIRED})
```

> *The analysis above applies Rule 6.2 to the STE text from Rule 6.1, demonstrating how key words and key phrases create a logical structure across sentences.*

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence; Rule 6.4 — Use Paragraphs to Show Related Information; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic; Rule 1.11 — One Term per Concept

## Code-Domain Explanation

This rule applies to all forms of code documentation. Key words and key phrases are the threads that bind a documentation block into a single coherent unit. When a developer reads your documentation, they follow these threads from sentence to sentence. Without them, each sentence becomes an isolated statement that the reader must manually connect.

### README Files

In README files, key words establish the project identity. Use the project name, the primary library name, and the core concept (such as "middleware," "pipeline," or "plugin") as key words that repeat across sections. The installation section, usage section, and configuration section all refer to the same project name. This repetition tells the reader they are still reading about the same system.

```markdown
# AuthKit

AuthKit is an authentication middleware for FastAPI.

## Install

Install AuthKit with pip: `pip install authkit`.

## Use

Add the AuthKit middleware to your FastAPI app.
The AuthKit middleware validates each request.
```

The key word "AuthKit" repeats in the title, the install section, and the use section. Do not switch to "the library" or "this tool" in later sections.

### API Documentation

In API documentation, key words are the function names, parameter names, and return type names. Each sentence in a function description must use the function name or a pronoun that refers to it. When you describe a parameter, use the parameter name as the key word. When you describe a return value, use "returns" as the key phrase. Consistent key words prevent the reader from losing track of which parameter or which function a sentence describes.

```markdown
### `get_user(user_id)`

The `get_user` function reads a user from the database.
The `user_id` parameter selects the row to read.
The `get_user` function returns a `User` object.
The `get_user` function returns `None` when the user is absent.
```

### Docstrings

In docstrings, the first sentence introduces the function or class name as the key word. Each subsequent sentence uses that name, the parameter names, or pronouns that refer back to the subject. A docstring for `def send_message(channel, payload)` must use "send," "message," "channel," and "payload" as key words. Do not switch to synonyms like "transmit," "data," or "queue" mid-description.

```python
def send_message(channel, payload):
    """Send a message to a channel.

    The send_message function writes the payload to the channel.
    The channel parameter is the target queue.
    The payload parameter is the body of the message.
    The send_message function returns the message ID.
    """
```

### Commit Messages

In commit messages, key words are the component name, the action verb, and the affected module. A commit message that starts with "Fix race condition in connection pool" must use "connection pool" as the key phrase in the body. Do not switch to "pool," "conn pool," or "connection manager" within the same commit message.

```text
Fix race condition in connection pool

The connection pool used an unsafe counter for active links.
The connection pool now uses an atomic counter.
Add a test that starts 100 workers on the connection pool.
```

### Error Messages

In error messages, key words are the operation name and the resource name. An error message such as "Cannot read file: permission denied" introduces "file" as the key word. Any follow-up message or recovery instruction must use "file" again, not switch to "document" or "path."

```text
Cannot read config file: permission denied.
Check that the config file is readable by the user that starts the service.
Move the config file to a directory the service can read.
```

### Key Word Consistency Across Documentation Types

The same key word must carry the same meaning across all documentation types within a project. If your README calls a component the "authentication middleware," your API docs, docstrings, and commit messages must also call it the "authentication middleware." Do not rename it to "auth middleware" in one place and "auth layer" in another. This cross-document consistency is part of Rule 1.11 (one term per concept).

## Paradigm-Specific Guidance

### Object-Oriented (Java, C++, C#, Python Classes)

In object-oriented documentation, use class names, method names, and property names as key words. When you describe a class hierarchy, repeat the base class name as the key word across sentences that describe derived classes.

```python
class DataExporter:
    """Write records to an output stream.

    The DataExporter class writes records to an output stream.
    The DataExporter class extends BaseExporter.
    Each DataExporter instance uses an output strategy.
    """
    def write(self, record):
        ...
```

> **Non-STE:** The `DataExporter` class writes records. The superclass manages the connection lifecycle. Instances can be configured with different output strategies.
>
> **STE:** The `DataExporter` class writes records to an output stream. The `DataExporter` class extends `BaseExporter`. Each `DataExporter` instance uses an output strategy.
>
> *Principles applied: P11, P2 — consistent use of "DataExporter" as the key word instead of switching to "superclass" and "instances."*

When you document a method chain or builder pattern, repeat the return type as the key word to show how calls connect.

```java
Stream<Order> orders = getOrders()
    .filter(o -> o.isPaid())   // the filter method returns a Stream
    .map(Order::toInvoice);    // the Stream supports the map method
List<Invoice> result = orders.collect(toList()); // collect on the Stream
```

> **Non-STE:** `.filter()` removes unwanted entries. The result can be mapped to a new shape. Chaining `.collect()` finalizes it.
>
> **STE:** The `filter` method returns a new `Stream`. The `Stream` object supports the `map` method. Call the `collect` method on the `Stream` to get a `List`.
>
> *Principles applied: P2, P11 — "Stream" is the key word that connects the three sentences, showing the reader the chain flows through the same type.*

### Functional (Haskell, Elixir, Clojure, Rust)

In functional documentation, use type names, function names, and data constructors as key words. Purity and immutability mean that each sentence describes a transformation. The key word is the value that flows through the transformations.

```rust
fn open_connection(config: Config) -> Result<Db, Error> {
    // parse_config returns a Result value.
    let url = config.parse_config()        // Result value
        .map(|c| c.database_url)           // map over the Result value
        .map_err(Error::bad_config)?;
    Db::connect(url)                        // use the database URL
}
```

> **Non-STE:** `parse_config` reads the file and returns a result. It gets mapped to extract the database URL. The connection is opened with that value.
>
> **STE:** The `parse_config` function returns a `Result` value. Map over the `Result` value to get the database URL. Use the database URL to open a connection.
>
> *Principles applied: P11, P2 — "Result" and "database URL" are the key words that show the data flow from parsing to connection.*

In Elixir pipe chains, the key word is the data structure that passes through each pipe step.

```elixir
changeset =
  %User{}
  |> User.changeset(params)        # the changeset goes through validate
  |> User.validate()               # the validated changeset goes through transform
  |> User.transform()              # the transformed changeset is serialized
  |> Jason.encode!()
```

> **Non-STE:** The input is piped through validation, then transformed, then serialized to JSON.
>
> **STE:** The `changeset` goes through the `validate` function. The validated `changeset` goes through the `transform` function. The transformed `changeset` is serialized to JSON.
>
> *Principles applied: P6, P11 — "changeset" is the key word repeated at each stage so the chain is easy to follow.*

### Procedural (C, Go, Bash)

In procedural documentation, use variable names, struct field names, and error codes as key words. Procedural code often has sequential steps. Each step must refer to the same variable by the same name.

```go
func handleRequest(req *Request) error {
    buffer := make([]byte, req.size)   // allocate a buffer for the request
    copy(buffer, req.payload)          // write the payload bytes into the buffer
    _, err := sock.Write(buffer)       // send the buffer over the socket
    return err
}
```

> **Non-STE:** Allocate a buffer for the request. Fill the memory with the payload bytes. Send the data over the socket.
>
> **STE:** Allocate a `buffer` for the `request`. Write the `payload` bytes into the `buffer`. Send the `buffer` over the `socket`.
>
> *Principles applied: P11, P1 — "buffer" is the key word that connects allocation, writing, and sending. Do not switch to "memory" or "data."*

### Declarative (SQL, Terraform, Kubernetes YAML)

In declarative documentation, use resource names, column names, and attribute names as key words. The reader must map documentation sentences to the exact identifiers in the declarative file.

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0abc123"
  subnet_id     = aws_subnet.public.id   # the aws_instance references the aws_subnet
}

resource "aws_eip" "web_ip" {
  instance = aws_instance.web.id          # attach the aws_eip to the aws_instance
}
```

> **Non-STE:** The resource creates a virtual machine. It references the subnet defined earlier. The instance gets a public IP attached.
>
> **STE:** The `aws_instance` resource creates a virtual machine. The `aws_instance` references the `aws_subnet`. Attach an `aws_eip` to the `aws_instance`.
>
> *Principles applied: P11, P5 — "aws_instance" is the technical noun and the key word. Do not switch to "resource," "VM," or "instance."*

### Systems (Rust Ownership, C Memory)

In systems documentation, use ownership terms, lifetime names, and pointer names as key words. Memory safety documentation relies on precise key word repetition because ambiguity causes bugs.

```rust
fn read<'a>(buffer: &'a [u8]) -> &'a str {
    // the function borrows the buffer
    // the borrow of the buffer is valid for lifetime 'a
    std::str::from_utf8(buffer).unwrap()
} // the caller keeps ownership of the buffer
```

> **Non-STE:** The function borrows the buffer. The reference is valid for the scope. The caller retains ownership of the allocated memory.
>
> **STE:** The function borrows the `buffer`. The borrow of the `buffer` is valid for lifetime `'a`. The caller keeps ownership of the `buffer`.
>
> *Principles applied: P11, P2 — "buffer" is the key word. "Borrow" is used consistently as the connecting concept. Do not switch between "borrow," "reference," and "retain ownership" for the same relationship.*

## Extended Examples

### Example 1: Configuration Documentation

```yaml
redis:
  host: localhost
  port: 6379
```

> **Non-STE:** `redis.host` sets the Redis server address. The default is `localhost` on the usual port. You can override this with an environment variable.
>
> **STE:** The `redis.host` option sets the Redis server hostname. The default hostname is `localhost`. Set the `REDIS_HOST` environment variable to override the default hostname.
>
> *Principles applied: P11 — "hostname" is the key word that connects the option, the default, and the override method. Do not switch from "address" to "host" to "this."*

### Example 2: Error Handling Flow

```python
def parse(text):
    if not is_valid_json(text):
        raise ParseError("invalid JSON at position 0")
    return json.loads(text)

try:
    parse(body)
except ParseError as err:
    log.error("parse failed: %s", err)
```

> **Non-STE:** The parser encounters invalid JSON. An exception gets raised with the position. The caller catches it and logs the incident.
>
> **STE:** The parser finds invalid JSON. The parser raises a `ParseError` exception. The caller catches the `ParseError`. The caller logs the `ParseError` to the error log.
>
> *Principles applied: P11, P1 — "parser" and "ParseError" are the key words. Each sentence repeats them so the reader follows the error path from detection to logging.*

### Example 3: Database Migration Script

```sql
ALTER TABLE users ADD COLUMN last_login TIMESTAMP NOT NULL DEFAULT NOW();
-- migration is not reversible: no DOWN script is provided
```

> **Non-STE:** The migration adds a `last_login` column to the users table. It's populated with a default timestamp. The operation is not reversible.
>
> **STE:** The migration adds a `last_login` column to the `users` table. The `last_login` column gets the default value `NOW()`. The migration is not reversible.
>
> *Principles applied: P11, P2 — "last_login" and "migration" are the key words. Do not switch to "it," "the operation," or "populated."*

### Example 4: CLI Tool Description

```text
ste-code lint docs/
  checks documentation files for rule violations
  writes report.json
  exits with code 1 on failure
```

> **Non-STE:** `ste-code lint` checks documentation files. It scans for rule violations and emits a report. The tool exits with a non-zero code on failure.
>
> **STE:** The `ste-code lint` command checks documentation files. The `lint` command scans for rule violations. The `lint` command writes a report. The `lint` command exits with code 1 on failure.
>
> *Principles applied: P11, P6 — "lint" is the key word and a technical code noun. Repeat "lint" or "lint command" in every sentence so the reader always knows the subject.*

### Example 5: Test Case Description

```python
def test_calculate_tax_exempt():
    result = calculate_tax(items=EXEMPT, quantity=0)
    assert result == 0.00
```

> **Non-STE:** The test verifies that `calculate_tax` returns zero for exempt items. It exercises the edge case where quantity is zero. The expected output is `0.00`.
>
> **STE:** The test checks that `calculate_tax` returns `0.00` for exempt items. The test uses a quantity of zero. The test checks that the result is `0.00`.
>
> *Principles applied: P11, P12 — "test" is the key word. "Checks" is an approved verb from the canonical synonym table. Do not switch between "verifies," "exercises," and "expected output."*

### Example 6: Deployment Pipeline Documentation

```yaml
build:
  script: docker build -t app:1.2 .
push:
  script: docker push registry/app:1.2
deploy:
  script: |
    docker pull registry/app:1.2
    docker run -d --name app registry/app:1.2
```

> **Non-STE:** The CI pipeline builds the Docker image. If the build succeeds, it pushes the artifact to the registry. The deploy step pulls the container and rolls it out.
>
> **STE:** The CI pipeline builds the Docker image. The CI pipeline pushes the image to the container registry. The deploy step pulls the image from the registry. The deploy step starts the container.
>
> *Principles applied: P11, P1 — "image" is the key word that connects build, push, and pull. Do not switch to "artifact," "container," and "it."*

## Edge Cases

### Edge Case 1: Framework Name Conflicts with an Unapproved Word

Some framework names use words that are not in the STE-Code approved dictionary. For example, a framework named "Leverage" or a library named "Commence." Rule 1.5 and Rule 1.6 permit technical code nouns even when they are not approved words. When the framework name is the key word, use it as-is. Do not replace it with an STE-approved synonym.

```python
from leverage import Workflow

wf = Workflow()            # the Leverage framework handles task orchestration
wf.define(leverage_dag)    # the Leverage framework uses a DAG to define workflows
```

> **Non-STE:** The Leverage framework handles task orchestration. Leverage uses a DAG to define workflows. The DAG scheduler runs tasks in dependency order.
>
> **STE:** The `Leverage` framework handles task orchestration. The `Leverage` framework uses a DAG to define workflows. The DAG scheduler runs tasks in dependency order.
>
> *Principles applied: P5, P6 — "Leverage" is a technical code noun. It is the key word even though "leverage" is not an approved STE verb. Use code formatting to mark it as a technical name.*

### Edge Case 2: Code Keyword That Conflicts with the Rule

Some programming language keywords are very short and do not carry enough meaning to serve as key words. For example, the Go keyword `go` or the Rust keyword `mut`. In these cases, use a longer descriptive key phrase that includes the keyword.

```go
go func() {
    // the goroutine runs concurrently with the caller
    process()
}() // the goroutine stops when the function returns
```

> **Non-STE:** Use `go` to start a goroutine. The goroutine runs concurrently. It finishes when the function returns.
>
> **STE:** Use the `go` keyword to start a goroutine. The goroutine runs concurrently with the caller. The goroutine stops when the function returns.
>
> *Principles applied: P5, P11 — "goroutine" is the key word, not the bare keyword `go`. The keyword itself is a technical code noun but does not work alone as a key word.*

### Edge Case 3: Generated Code Documentation

Generated code (from protobuf compilers, OpenAPI generators, or ORMs) often produces documentation with inconsistent key words. When you write documentation that references generated code, use the generated type names as key words even if they are verbose. Do not abbreviate or rename them.

```python
from protobuf.user_pb2 import UserServiceClientImpl

client = UserServiceClientImpl(channel)  # the generated class connects to the server
client.serialize()                        # the class handles serialization automatically
```

> **Non-STE:** The generated `UserServiceClientImpl` connects to the gRPC server. The client stub handles serialization. The RPC call returns a response.
>
> **STE:** The generated `UserServiceClientImpl` class connects to the gRPC server. The `UserServiceClientImpl` handles serialization automatically. Call a method on the `UserServiceClientImpl` to make an RPC.
>
> *Principles applied: P11, P5 — "UserServiceClientImpl" is the key word even though it is long. Do not shorten it to "client," "stub," or "it" in critical sentences.*

### Edge Case 4: Key Words in Multi-Language Repositories

When a repository contains code in multiple languages, the same concept may have different names in each language. For example, a "dictionary" in Python is a "HashMap" in Java and a "map" in Go. In cross-language documentation (such as the top-level README), choose one key word and use it consistently. Add a note that explains the language-specific names.

```python
# Python
config: dict = load_config()
```
```java
// Java
Map<String, String> config = loadConfig();  // HashMap at runtime
```
```go
// Go
config := make(map[string]string) // Go calls it a map
```

> **Non-STE:** The configuration is stored in a dict in Python and a HashMap in Java. Both structures map string keys to values.
>
> **STE:** The configuration is stored in a map (Python: `dict`, Java: `HashMap`, Go: `map`). The map uses string keys. Look up values in the map by key.
>
> *Principles applied: P11, P8 — "map" is the key word for the cross-language concept. The language-specific names are given once as a clarification, not repeated as key words.*

### Edge Case 5: Key Phrases That Span Multiple Words

When a key phrase is a multi-word technical term (such as "connection pool," "rate limiter," or "retry policy"), keep the full phrase as the key unit. Do not break it into separate words or abbreviate it mid-documentation.

```python
pool = ConnectionPool(max_size=10)  # the connection pool limits concurrent links
pool.resize(20)                     # the connection pool size is configurable
pool.recycle_idle(timeout=30)       # the connection pool recycles idle connections
```

> **Non-STE:** The connection pool limits concurrent database connections. The pool size is configurable. Idle connections are recycled after the timeout.
>
> **STE:** The connection pool limits concurrent database connections. The connection pool size is configurable. The connection pool recycles idle connections after the timeout.
>
> *Principles applied: P11, P9 — "connection pool" is the full key phrase. Do not shorten it to "pool" or break it into "pool" and "connections" in different sentences.*

## Cross-References

This rule is part of Section 6, which governs sentence structure and text organization. The rules in this section work together to create clear, scannable documentation:

- **Rule 6.1 — Give Information Gradually:** Key words from Rule 6.2 are the mechanism by which you introduce new information gradually. Each sentence adds to the reader's understanding of the key word, one detail at a time.
- **Rule 6.3 — Write Short Sentences:** Key words help you keep sentences short. When every sentence explicitly names its subject, you avoid long sentences that cram multiple ideas into one clause.
- **Rule 6.4 — Use Paragraphs to Show Related Information:** A paragraph is a group of sentences that share a key word. The key word is the topic of the paragraph. When the key word changes, start a new paragraph.
- **Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic:** The "one topic" is the key word. If you use two different key words as subjects in the same paragraph, you have two topics.

The following rules from Section 1 (Vocabulary) support Rule 6.2:

- **Rule 1.11 — One Term per Concept:** Key words work only if you use the same term for the same concept. If you switch between synonyms, the key word chain breaks.
- **Rule 1.5 — Technical Code Nouns Are Allowed:** When your key word is a class name, function name, or library name, it is a technical code noun and is permitted even if it is not in the approved dictionary.
- **Rule 1.8 — Use Standard, Well-Known Technical Nouns:** Choose key words that are standard in the domain. An unusual or invented key word weakens the logical structure because the reader does not recognize it as a key term.
- **Rule 1.9 — Prefer Short, Clear Technical Nouns:** Long key words are harder to repeat. If your key word is `AbstractAsynchronousDatabaseConnectionManager`, consider whether the documentation can use a shorter approved term.

Cross-reference to the STE-Code dictionary for approved connecting words and connecting phrases. The dictionary lists all permitted transition words such as "and," "but," "then," "thus," "also," "however," "therefore," "as a result," "at the same time," and "for example."

## Grammar Notes

### Anaphora and Cohesion in Code Documentation

In linguistics, the repetition of key words across sentences is a form of lexical cohesion. Cohesion is the grammatical and lexical linking within a text that holds it together. Rule 6.2 applies the principle of lexical cohesion to code documentation. When you repeat a key word such as "middleware," "token," or "buffer" across consecutive sentences, you create a cohesive chain that the reader can follow.

There are three types of cohesive ties that Rule 6.2 uses:

1. **Repetition:** The same word appears again. Example: "The middleware validates the request. The middleware reads the token."
2. **Pronoun reference:** A pronoun (it, they, this) refers back to the key word. Example: "The middleware validates the request. It reads the token." Use pronouns sparingly. After two sentences, repeat the full key word to prevent ambiguity.
3. **Synonym or hypernym:** An approved related term refers to the key word. Example: "The function returns a `Result`. The value contains the parsed data." The STE-Code synonym table makes this safe by restricting which synonyms are permitted.

### Topic-Comment Structure

In English grammar, most sentences have a topic (what the sentence is about) and a comment (what is said about the topic). In code documentation, the key word is the topic. Each sentence in a documentation block should have the same topic (the same key word) in subject position.

```python
# Non-STE: the topic shifts across three sentences.
def parse(stream):
    text = stream.read()          # topic: parser? stream?
    bad = lexer.find_invalid(text) # topic: invalid tokens
    return error(bad)             # topic: an error

# STE: "parser" is the topic of every sentence.
def parser(stream):
    text = stream.read()          # the parser reads the input stream
    bad = parser.find_invalid(text) # the parser detects invalid tokens
    return parser.error(bad)        # the parser returns an error to the caller
```

> **Non-STE:** The parser reads the input stream. Invalid tokens are detected by the lexer. An error is returned to the caller.
>
> **STE (stable topic):** The parser reads the input stream. The parser detects invalid tokens. The parser returns an error to the caller.
>
> *Grammar note: In the Non-STE version, the topic shifts from "parser" to "invalid tokens" to "an error." The reader must reconstruct that all three sentences are about the parser. In the STE version, "parser" is the topic of every sentence.*

### Connecting Words as Grammatical Signals

Connecting words ("and," "but," "then," "thus," "however," "therefore," "also") are grammatical signals that tell the reader how the new sentence relates to the previous one. In STE-Code, these connecting words appear at or near the start of a sentence:

- **"And"** signals addition: the new sentence adds more information about the same key word.
- **"But"** signals contrast: the new sentence gives information that differs from the expectation set by the previous sentence.
- **"Then"** signals sequence: the new sentence describes the next step that involves the key word.
- **"Thus"** or **"Therefore"** signals consequence: the new sentence describes a result that follows from the previous sentence.

Use connecting words at the start of sentences, not buried in the middle. The reader must see the signal before reading the sentence content.

### Avoiding Dangling Key Words

A dangling key word is a term introduced once and never repeated. The reader sees the term, expects it to be important, and then never encounters it again. This breaks the logical structure.

```text
# Non-STE
The build system compiles TypeScript and bundles static assets.
The output goes to the dist/ directory.
Deployment uses a Docker container.

# STE (resolved)
The build system compiles TypeScript and bundles static assets.
The build system writes the output to the dist/ directory.
The deploy system copies the dist/ directory into a Docker container.
```

> **Non-STE:** The build system compiles TypeScript and bundles static assets. The output goes to the `dist/` directory. Deployment uses a Docker container.
>
> **STE (resolved):** The build system compiles TypeScript and bundles static assets. The build system writes the output to the `dist/` directory. The deploy system copies the `dist/` directory into a Docker container.
>
> *Grammar note: In the Non-STE version, "static assets" and "output" appear once and disappear. The reader does not know if "output" refers to "static assets," "TypeScript," or both. In the STE version, "build system" and the `dist/` directory are the key words repeated across sentences.*

## Examples

> *Adapted from spec pair:* Non-STE: "Key words connect ideas in a text; keep them unchanged."  |  STE: "Use key words and key phrases to give your text a logical structure, and do not change them in your documentation."

The key-word chain in this rule holds across every documentation type. The short consolidated pair below shows the pattern in one place:

> **Non-STE:** The logger writes events. It uses a queue. The thing then flushes to disk on a timer.
>
> **STE:** The logger writes events to a queue. The logger flushes the queue to disk on a timer. The logger uses a background thread for the flush.
>
> *Principles applied: P11, P1 — "logger" and "queue" are the key words repeated in every sentence. Do not switch to "it," "the thing," or "the flush."*

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence; Rule 6.4 — Use Paragraphs to Show Related Information; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic; Rule 1.11 — One Term per Concept; Rule 1.5 — Technical Code Nouns Are Allowed; Rule 1.8 — Use Standard, Well-Known Technical Nouns; Rule 1.9 — Prefer Short, Clear Technical Nouns

---

<!-- a-sec6-rule6.3.md -->

# Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence.

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec6-rule6.3](ste-code/grouped/), Rule 6.3

## Original Rule

Good technical writing uses short sentences for complex topics. Short sentences give a clear structure to your writing and make information easier to understand.

In descriptive writing, the maximum sentence length is 25 words. This is because descriptive text is more complex than procedural text.

## STE-Code Adaptation

Good code documentation uses short sentences for complex topics. Short sentences give a clear structure to your documentation and make information easier to understand.

In descriptive code documentation, the maximum sentence length is 25 words. This is because descriptive text is more complex than procedural text.

### Examples

> *Adapted from spec pair:* Non-STE: "The Instrument Landing System (the system) on the aircraft shows data that helps the pilot during the approach to the runway." (ASD-STE100 Issue 9, p. 91)  |  STE: "The authentication middleware validates each incoming request before the controller processes it." (code-domain compliant rewrite)

> **STE:** The authentication middleware validates each incoming request before the controller processes it. (11 words)
>
> *Code-domain example — a short, single-subject sentence that respects the 25-word limit.*
>
> ```python
> # auth/middleware.py
> async def auth_middleware(request: Request, call_next):
>     # Validate the token on every request.
>     # Stop the request if the token is not valid.
>     user = validate_token(request.headers.get("Authorization"))
>     if user is None:
>         raise HTTPException(401, "The token is not valid.")
>     request.state.user = user
>     return await call_next(request)
> ```

> **Non-STE:** This function provides the ability to run arbitrary software applications within a sandboxed execution environment that isolates system resources. (21 words)
>
> **STE:** This function lets you run software applications in a sandbox. The sandbox isolates system resources. (8 words and 5 words)
>
> *Code-domain example — breaking one complex sentence into two shorter sentences improves clarity, even when the original is under 25 words.*
>
> ```python
> # runner/sandbox.py
> def run_in_sandbox(app: Path, sandbox: Sandbox) -> int:
>     """Run a software application inside a sandbox.
>
>     The sandbox isolates the system resources.
>     It returns the exit code of the application.
>     """
>     sandbox.mount_volume(app)
>     return sandbox.execute([str(app)])
> ```

> **Non-STE:** The configuration loader reads the YAML manifest file from the filesystem and parses it into an in-memory representation that other modules can query at runtime to determine their operational parameters. (32 words)
>
> **STE:** The configuration loader reads the YAML manifest file from the filesystem. It parses the file into an in-memory representation. Other modules can query this representation at runtime. They use it to find their operational parameters. (20 words, 8 words, 7 words, and 8 words)
>
> *Code-domain example — a 32-word sentence is split into four sentences, each under the 25-word limit.*
>
> ```python
> # config/loader.py
> def load_config(path: Path) -> Config:
>     """Read the YAML manifest from the filesystem.
>
>     Parse the file into an in-memory representation.
>     Other modules query this representation at runtime.
>     They use it to find their operational parameters.
>     """
>     raw = path.read_text()
>     data = yaml.safe_load(raw)
>     return Config(data)
> ```

> **Non-STE:** The cache invalidation strategy employs a time-to-live mechanism combined with a least-recently-used eviction policy to ensure that stale data is removed and memory consumption remains within the allocated heap budget. (34 words)
>
> **STE:** The cache invalidation strategy uses a time-to-live mechanism. It also uses a least-recently-used eviction policy. Together, these mechanisms remove stale data. They also keep memory consumption within the allocated heap budget. (16 words, 10 words, 7 words, and 10 words)
>
> *Code-domain example — a 34-word sentence is split into four sentences, each under the 25-word limit.*
>
> ```python
> # cache/policy.py
> class CachePolicy:
>     """Control how the cache removes stale entries.
>
>     The policy uses a time-to-live mechanism.
>     It also uses a least-recently-used eviction policy.
>     Together, these mechanisms remove stale data.
>     They keep memory use within the heap budget.
>     """
>     def __init__(self, ttl_seconds: int, max_entries: int) -> None:
>         self.ttl_seconds = ttl_seconds
>         self.max_entries = max_entries
> ```

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure; Rule 6.4 — Use Paragraphs to Show Related Information; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic

## Code-Domain Explanation

### README Files

README files are the first document a new contributor reads. Long sentences in a README hide the essential information. Break each concept into its own sentence. Use one sentence to describe the project. Use another to list the prerequisites. Use a third to give the install command.

A README that obeys the 25-word limit helps readers scan quickly. They can find the install steps without reading a dense paragraph. They can find the API example without parsing a complex sentence.

```markdown
# DataSync

DataSync copies files between cloud storage providers.
It supports AWS S3, Google Cloud Storage, and Azure Blob.
Install it with `pip install datasync`.
Set your credentials in the `.env` file before you run it.
```

### API Documentation

API reference docs describe endpoints, parameters, responses, and error codes. Each of these parts must stand alone. A 40-word sentence that mixes the URL, the method, the parameters, and the response is not useful. Instead, use one short sentence for each part.

For example, describe the endpoint path and method in one sentence. Describe each parameter in its own sentence. Describe the response schema in separate sentences for each field. This structure matches the way developers read API docs: they scan for the one detail they need.

```yaml
# openapi.yaml (documented descriptions)
/orders/{id}:
  get:
    summary: Get one order by its ID.
    parameters:
      - name: id
        description: The unique ID of the order.
        required: true
        in: path
        schema:
          type: string
    responses:
      '200':
        description: The request succeeded.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Order'
```

### Docstrings

Docstrings have limited space. A short sentence communicates the function's purpose. If the docstring has one 30-word sentence, the reader must parse it fully to understand the function. If the docstring has two 12-word sentences, the reader gets the purpose and the return value separately.

Follow this pattern for docstrings: one sentence for the purpose, one sentence for each parameter, one sentence for the return value, and one sentence for each exception. Each sentence must stay under 25 words.

```python
def send_email(to: str, subject: str, body: str) -> bool:
    """Send one email to the address you give.

    The `to` argument is the recipient email address.
    The `subject` argument is the email subject line.
    The `body` argument is the plain-text email content.
    The function returns True when the send succeeds.
    It raises `SMTPError` when the mail server rejects the send.
    """
```

### Commit Messages

Commit messages benefit from the same discipline. A commit subject line must not exceed 72 characters. But the sentence structure also matters. Use one short sentence to describe the change. Use additional short sentences in the body to explain why.

Avoid packing multiple logical changes into one sentence. If the commit does three things, use three sentences. This makes `git log` output readable and bisect debugging faster.

```text
Add a retry loop to the payment client

The payment API fails under load.
Add a retry loop with a backoff delay.
Log each retry with the request ID.
Keep the retry count under the API quota.
```

### Error Messages

Error messages must be clear and actionable. A long error message buries the cause and the fix. A short error message tells the user what failed and what to do next.

Structure error messages in two parts: the problem and the action. For example: "The database connection failed. Check your network connection and credentials." Each part is a short sentence under 25 words.

Error messages in log files also benefit from short sentences. Log aggregation tools parse messages by line. A single long sentence that spans 40 words is harder to search and filter.

```text
The migration failed. The "users" table already exists.
Drop the table or set FORCE_MIGRATE=true to continue.
```

## Paradigm-Specific Guidance

### Object-Oriented Documentation

Object-oriented code has class hierarchies, inheritance chains, and interface implementations. These relationships cause long descriptive sentences. A developer writes: "The `AuthenticatedController` class extends `BaseController` and implements the `Auditable` and `Loggable` interfaces to provide authentication-aware request handling with audit trail support." This is 26 words.

Instead, break the inheritance and the behavior into separate sentences:

> The `AuthenticatedController` class extends `BaseController`. It implements the `Auditable` and `Loggable` interfaces. These interfaces add authentication-aware request handling. They also add audit trail support.

```python
class AuthenticatedController(BaseController):
    """Handle requests that need a logged-in user.

    This class extends BaseController.
    It implements the Auditable interface.
    It implements the Loggable interface.
    These interfaces add authentication-aware request handling.
    They also add audit trail support.
    """
    def handle(self, request: Request) -> Response:
        ...
```

When documenting a class with many methods, do not describe all methods in one sentence. Describe each method in its own sentence or paragraph.

### Functional Documentation

Functional code often uses composition, pipelines, and monadic chains. The documentation for these patterns can become dense. A writer explains: "The `processOrder` function composes `validateOrder`, `calculateTotal`, and `applyDiscount` through a monadic pipeline that short-circuits on the first validation failure and accumulates errors in an `Either` type." This is 32 words.

Split the composition from the error behavior:

> The `processOrder` function composes three functions: `validateOrder`, `calculateTotal`, and `applyDiscount`. It uses a monadic pipeline. The pipeline stops on the first validation failure. It collects errors in an `Either` type.

```haskell
-- Process an order through three pure steps.
-- The pipeline stops on the first failure.
processOrder :: Order -> Either [Error] Receipt
processOrder = validateOrder >=> calculateTotal >=> applyDiscount
```

Pure function signatures are short by nature. But the prose that explains them must also be short.

### Procedural Documentation

Procedural code follows a sequence of steps. Documentation for procedural code maps naturally to short sentences. Each step becomes one sentence. Each sentence describes one action.

Do not combine three steps into one sentence. This pattern: "The function allocates a buffer, copies the input data into the buffer, and returns a pointer to the caller." is acceptable at 22 words. But it is better to split the allocation from the copy for clarity when safety is important:

> The function allocates a buffer. It copies the input data into the buffer. It returns a pointer to the caller.

```c
/* Copy the input string into a heap buffer.
 * The caller must free the returned pointer.
 */
char *copy_input(const char *input) {
    size_t len = strlen(input) + 1;   /* Allocate the buffer. */
    char *buf = malloc(len);          /* Allocate a buffer. */
    if (!buf) return NULL;
    memcpy(buf, input, len);          /* Copy the data into the buffer. */
    return buf;                       /* Return the pointer to the caller. */
}
```

Procedural documentation for C and Go code often documents preconditions and postconditions. Give each condition its own sentence.

### Declarative Documentation

Declarative code includes SQL schemas, Terraform configurations, and Kubernetes manifests. These documents describe the desired state. Long sentences mix resource properties and make the schema difficult to read.

For Terraform, document each resource block separately. For each resource, document each argument in its own sentence. Do not write: "The `aws_instance` resource creates an EC2 instance in the specified subnet with the given security groups and attaches the provided IAM instance profile." This is 28 words.

Instead:

> The `aws_instance` resource creates an EC2 instance. It launches the instance in the specified subnet. It applies the given security groups. It attaches the provided IAM instance profile.

```hcl
# aws_instance.tf
resource "aws_instance" "web" {
  # Launch an EC2 instance.
  # Start the instance in the "web" subnet.
  # Apply the "web-sg" security group.
  # Attach the "web-profile" IAM instance profile.
  ami           = "ami-0abc123"
  subnet_id     = aws_subnet.web.id
  vpc_security_group_ids = [aws_security_group.web.id]
  iam_instance_profile = aws_iam_instance_profile.web.name
}
```

### Systems Documentation

Systems documentation describes memory models, ownership rules, and concurrency guarantees. These topics are inherently complex. Short sentences are essential here.

Rust ownership documentation is a good example. The Rust Book uses short sentences to explain borrowing and lifetimes. A concept like "the borrow checker ensures that references do not outlive the data they refer to by tracking lifetimes at compile time" is 25 words. But Rust documentation often splits this further:

> The borrow checker tracks references. It makes sure that references do not outlive their data. It does this at compile time. It uses lifetimes to enforce these rules.

```rust
/// Track a borrowed value.
///
/// The borrow checker tracks each reference.
/// It makes sure references do not outlive their data.
/// It does this check at compile time.
/// It uses lifetimes to enforce the rules.
fn print_length(s: &String) {
    println!("Length: {}", s.len());
}
```

Systems documentation also covers unsafe code blocks, FFI boundaries, and memory layout. These are safety-critical topics. Short sentences reduce the risk of misunderstanding.

## Extended Examples

### Example 4 — API Endpoint Documentation

> **Non-STE:** The `GET /api/v2/users` endpoint returns a paginated list of user objects sorted by creation date in descending order with an optional query parameter to filter results by account status. (30 words)
>
> **STE:** The `GET /api/v2/users` endpoint returns a paginated list of user objects. The list is sorted by creation date in descending order. You can use the `status` query parameter to filter results. (18 words, 9 words, and 12 words)
>
> *Principles applied: P1, P2 — short sentences make each API detail independently scannable. The original sentence mixes four concepts (method, sorting, pagination, filtering). The STE version gives each concept its own sentence.*

```http
GET /api/v2/users?status=active&sort=-created_at HTTP/1.1
Host: api.example.com
Authorization: Bearer <token>

# Response: a paginated list of users.
# The list is sorted by creation date, newest first.
# Use the `status` parameter to filter by account status.
```

### Example 5 — Commit Message Body

> **Non-STE:** Refactored the JWT middleware to extract token validation into a separate utility module and added comprehensive error handling for expired tokens, malformed headers, and missing claims with descriptive log messages. (31 words)
>
> **STE:** Refactor the JWT middleware. Extract the token validation logic into a utility module. Add error handling for expired tokens. Add error handling for malformed headers. Add error handling for missing claims. Include descriptive log messages. (12 words, 9 words, 7 words, 7 words, 7 words, and 4 words)
>
> *Principles applied: P1, P8, P12 — the imperative mood for commits is preserved. Each logical change gets its own sentence. The git log becomes scannable line by line.*

```text
Refactor the JWT middleware

Extract the token validation logic into a utility module.
Add error handling for expired tokens.
Add error handling for malformed headers.
Add error handling for missing claims.
Include descriptive log messages for each failure path.
```

### Example 6 — Error Message

> **Non-STE:** The database connection could not be established because the server at the specified hostname was unreachable due to a network timeout or the provided credentials were invalid after the maximum number of retry attempts. (34 words)
>
> **STE:** The database connection failed. The server is not reachable. Or the credentials are not valid. Check your network connection. Check your credentials. (4 words, 5 words, 6 words, 5 words, and 3 words)
>
> *Principles applied: P1, P3, P10 — short error messages tell the user exactly what to do. Each possible cause gets its own sentence. Each action gets its own sentence.*

```text
DB_CONNECTION_FAILED: the database connection failed.
Cause: the server is not reachable, or the credentials are not valid.
Action: check your network connection.
Action: check your credentials.
```

### Example 7 — Class Constructor Docstring

> **Non-STE:** Initializes a new instance of the `HttpClient` class with the specified base URL string and an optional dictionary of default HTTP headers along with a retry policy configuration that determines how many times a failed request should be retried before the client throws a `MaxRetriesExceededException`. (43 words)
>
> **STE:** Make a new `HttpClient` instance. Use the specified base URL. Use the optional default headers dictionary. Set a retry policy. The policy sets the number of retries. The client throws `MaxRetriesExceededException` when retries run out. (7 words, 5 words, 6 words, 4 words, 7 words, and 11 words)
>
> *Principles applied: P1, P2, P4, P12 — each constructor parameter gets its own sentence. The exception behavior is separated from the parameter list. The docstring is readable line by line.*

```python
class HttpClient:
    def __init__(self, base_url: str, headers: dict | None = None,
                 max_retries: int = 3):
        """Make a new HttpClient instance.

        Use the base_url string as the request root.
        Use the headers dictionary for default request headers.
        Set a retry policy with max_retries attempts.
        The client throws MaxRetriesExceededException when retries run out.
        """
```

### Example 8 — README Project Description

> **Non-STE:** This project is a lightweight, high-performance logging library designed for distributed microservices architectures that supports structured JSON output, log level filtering, and asynchronous batch writing to multiple backends including Elasticsearch, Loki, and CloudWatch. (36 words)
>
> **STE:** This project is a lightweight logging library. It is designed for distributed microservices. It supports structured JSON output. It supports log level filtering. It supports asynchronous batch writing. It writes to multiple backends. These backends include Elasticsearch, Loki, and CloudWatch. (10 words, 6 words, 5 words, 5 words, 4 words, 9 words, and 8 words)
>
> *Principles applied: P1, P8, P11 — the project description is split into one sentence per feature. A reader can scan the feature list without parsing a dense paragraph. Each backend is listed in a separate sentence for clarity.*

```markdown
# LogKit

LogKit is a lightweight logging library.
It is built for distributed microservices.
It writes structured JSON logs.
It filters logs by level.
It batches writes asynchronously.
It ships logs to Elasticsearch, Loki, and CloudWatch.
```

### Example 9 — Release Notes Entry

> **Non-STE:** The v2.4 release introduces a new caching layer that reduces database query latency by 60 percent on average across all API endpoints and also includes a fix for the race condition that occurred when multiple workers attempted to update the same configuration key simultaneously. (44 words)
>
> **STE:** The v2.4 release adds a new caching layer. This layer reduces database query latency by 60 percent. The improvement applies to all API endpoints. This release also fixes a race condition. The race condition occurred during concurrent configuration updates. (10 words, 8 words, 8 words, 7 words, and 9 words)
>
> *Principles applied: P1, P2, P12 — release notes are read by users and operators. Short sentences help them find breaking changes and new features quickly. The problem and the fix get separate sentences.*

```markdown
## v2.4

- Add a caching layer that cuts database query latency by 60 percent.
- Apply the improvement to all API endpoints.
- Fix a race condition during concurrent configuration updates.
```

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

```java
// The synchronized keyword guards the shared counter.
// Count it as one word in the sentence above.
public synchronized void increment() {
    counter++;
}
```

### Edge Case 3 — Compound Type Signatures

Type signatures in TypeScript, Rust, and Scala can be long. Describing a complex generic type in a sentence often exceeds 25 words. Split the description: one sentence for the type shape, another for the constraints, and another for the behavior.

Avoid this pattern: "The function accepts a generic type parameter `T` that must implement both the `Serialize` and `Deserialize` traits and returns a `Result<Vec<T>, ParseError>` wrapped in a `Future`." This is 30 words.

Use this pattern instead:

> The function accepts a generic type parameter `T`. The type must implement `Serialize` and `Deserialize`. The function returns a `Result<Vec<T>, ParseError>`. The result is wrapped in a `Future`.

```rust
/// Accept a generic type T.
/// The type must implement Serialize and Deserialize.
/// The function returns a Result<Vec<T>, ParseError>.
/// The result is wrapped in a Future.
async fn load_all<T: Serialize + Deserialize<'static>>(
    client: &Client,
) -> impl Future<Output = Result<Vec<T>, ParseError>> {
    ...
}
```

### Edge Case 4 — Legal and License Text

License headers and legal disclaimers are not covered by Rule 6.3. These texts follow legal conventions, not technical writing standards. Do not apply the 25-word limit to MIT, Apache, or GPL license text. Do not apply it to copyright notices.

However, the surrounding documentation that explains the license choice should obey the 25-word limit.

```text
// Copyright 2026 Example Corp.
// SPDX-License-Identifier: MIT

# License: MIT.
# You can use this code in closed-source projects.
# Keep the copyright notice in the source files.
```

### Edge Case 5 — Generated Documentation

Auto-generated documentation from tools like JSDoc, Sphinx, or `go doc` may produce long sentences from source code comments. The generator does not enforce the 25-word limit. But the source comments that feed the generator should obey the rule.

Fix the source docstrings. Do not edit the generated output directly. The generated output reflects the quality of the input.

```javascript
/**
 * Start the background worker.
 * It reads jobs from the queue.
 * It runs each job in a separate thread.
 * Stop the worker with the stop() method.
 *
 * @param {number} pollMs - The poll interval in milliseconds.
 */
function startWorker(pollMs) { /* ... */ }
```

## Cross-References

Rule 6.3 is part of the Sentence Length cluster in Section 6. These rules work together:

- **Rule 6.1 — Give Information Gradually:** Short sentences enable gradual information delivery. Each sentence adds one new piece of information. Long sentences deliver too much information at once. The reader cannot absorb it.

- **Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure:** Short sentences make key words visible. A keyword at the start of a sentence signals the topic. A keyword buried in the middle of a 35-word sentence lacks its signal value.

- **Rule 6.4 — Use Paragraphs to Show Related Information:** Short sentences form clear paragraphs. A paragraph of three 12-word sentences is easier to read than one 36-word sentence. Use paragraphs to group related short sentences.

- **Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic:** Short sentences help each paragraph stay on topic. When each sentence is short, the writer can see when a sentence drifts to a new topic. The writer can then start a new paragraph.

- **Rule 1.1 — Use Approved Words from the STE-Code Dictionary:** Short sentences reduce the need for complex vocabulary. When you must fit many ideas into one sentence, you reach for longer words. When you split the ideas, each sentence uses simpler words.

- **Rule 1.10 — No Slang, Jargon, or Regional Terms:** Short sentences reduce the temptation to use jargon. Long sentences are a place where jargon hides. When each sentence is short, jargon stands out and can be removed.

## Grammar Notes

### Clause Density

Long sentences in code documentation often contain multiple clauses. Each clause adds a subject, a verb, and an object. The reader must hold the first clause in memory while parsing the second. With three or more clauses, the reader misses the thread.

The 25-word limit indirectly limits clause density. Most English clauses are 6 to 12 words. A 25-word sentence can hold at most two clauses with connecting words. This is a natural limit that matches working memory capacity.

### Coordination vs. Subordination

Coordination joins two independent clauses with "and," "but," or "or." Subordination makes one clause dependent on another with "because," "when," "if," or "although."

Code documentation overuses subordination. A writer says: "The `parse` function throws a `SyntaxError` when the input string contains invalid JSON because the parser cannot construct a valid AST from malformed tokens." This is 27 words with three levels of subordination.

Prefer coordination with separate sentences:

> The `parse` function throws a `SyntaxError`. This error occurs when the input string contains invalid JSON. The parser cannot construct a valid AST from malformed tokens.

```python
def parse(text: str) -> Ast:
    """Parse a JSON string into an AST.

    The function throws a SyntaxError on bad input.
    This error occurs when the string is not valid JSON.
    The parser cannot build an AST from malformed tokens.
    """
```

### Implicit Connectives

Short sentences rely on implicit connectives. The reader infers the relationship between sentences from their order. This is different from academic writing, which uses explicit connectives like "therefore," "consequently," and "furthermore."

In code documentation, implicit connectives work well. The reader expects documentation to flow from purpose to usage to edge cases. Short sentences in that order need no explicit glue.

### Counting Rules

Count hyphenated compound words as one word. For example, "least-recently-used" counts as one word, not three. Count acronyms as one word: "JSON" is one word. Count code tokens as one word: `Result<Vec<T>>` is one word.

Do not count parenthetical word counts in examples. The notation "(12 words)" in an example sentence is metadata, not part of the sentence.

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure; Rule 6.4 — Use Paragraphs to Show Related Information; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic; Rule 1.1 — Use Approved Words from the STE-Code Dictionary; Rule 1.10 — No Slang, Jargon, or Regional Terms

---

<!-- a-sec6-rule6.4.md -->

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

---

<!-- a-sec6-rule6.5.md -->

# Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec6-rule6.5](ste-code/grouped/), Rule 6.5

## Original Rule

In descriptive writing, paragraphs describe topics, and it is important that each paragraph has only one topic. The topic sentence is the first and most important sentence in a paragraph. The topic sentence gives new information and makes a logical connection between the new information and previous information. To make a logical connection in a paragraph, the topic sentence usually contains a key word and/or a connecting word or connecting phrase.

From the topic sentences, the reader will understand the contents of your text and will find the applicable information quickly. If the reader writes down each of the topic sentences from a text, they will make a good outline of its content. The other sentences in each paragraph give the information a logical structure and add more information on the topic of the paragraph.

## STE-Code Adaptation

In descriptive code documentation, paragraphs describe topics, and it is important that each paragraph has only one topic. The topic sentence is the first and most important sentence in a paragraph. The topic sentence gives new information and makes a logical connection between the new information and previous information. To make a logical connection in a paragraph, the topic sentence usually contains a key word and/or a connecting word or connecting phrase.

From the topic sentences, the developer will understand the contents of your documentation and will find the applicable information quickly. If the developer writes down each of the topic sentences from the documentation, they will make a good outline of its content. The other sentences in each paragraph give the information a logical structure and add more information on the topic of the paragraph.

### Examples

> *Adapted from spec pair:* Non-STE: "The ILS system shows the pilot the deviation data and aligns the localizer with the runway centerline and the glideslope is at a constant angle and the pointers show the direction and this data comes from the receivers in the aircraft."  |  STE: "The Instrument Landing System (the system) on the aircraft shows data that helps the pilot during the approach to the runway. This system shows the pilot the deviations from the localizer course and the glideslope path. The localizer course aligns with the centerline of the runway. And the glideslope path is at a constant angle to the threshold of the runway." (ASD-STE100 Rule 6.5, pages 91-98)

> **Non-STE:** The authentication middleware validates each request and the logging system records all validation failures to the audit trail while the response pipeline returns JSON error bodies with error codes and the database connection pool maintains idle connections for reuse and the configuration module reloads settings when the manifest file changes on disk.

> **STE:** The authentication middleware validates each request and returns error responses when validation fails.
>
> The authentication middleware validates each incoming request. The middleware reads the bearer token from the `Authorization` header. It sends the token to the `validateToken` function in the `security` module. The `validateToken` function decodes the JWT payload using the `HS256` algorithm from the `jwt-signer` library. Then it compares the `exp` claim with the current server time. If the token is not expired and not malformed, the function gets the `sub` and `role` claims and attaches them to the `request.auth` object.
>
> If the token is expired, the middleware returns a `401 Unauthorized` response. The response body is a JSON object with a `message` field and an `errorCode` field set to `TOKEN_EXPIRED`. If the token is malformed, the middleware returns a `401 Unauthorized` response with the `errorCode` field set to `TOKEN_MALFORMED`.
>
> The middleware also logs each failure to the audit trail. It calls the `AuditLogger.log` static method. This method writes a record to the `audit_events` table in the primary database. The write uses an asynchronous pattern that does not block the response pipeline.
>
> ```typescript
> // auth.middleware.ts — one function, but its documentation has three
> // single-topic paragraphs (see above).
> export async function authenticate(
>   req: Request,
>   res: Response,
>   next: NextFunction
> ): Promise<void> {
>   const header = req.headers["authorization"]; // "Bearer <jwt>"
>   const result = await security.validateToken(header);
>   if (result.status === "ok") {
>     req.auth = { sub: result.sub, role: result.role };
>     return next();
>   }
>   res.status(401).json({ message: result.reason, errorCode: result.code });
>   AuditLogger.log({ event: "auth_failure", code: result.code });
> }
> ```
>
> *Code-domain example — the Non-STE version combines five topics into one sentence; the STE version separates them into three paragraphs, each with one topic. The code block shows that one function can have multiple documentation topics.*

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

> **STE:** The `POST /users` endpoint creates a new user account with a hashed password.
>
> The `POST /users` endpoint creates a new user account. The endpoint accepts a JSON body with `email`, `password`, and `name` fields. It hashes the password using bcrypt with a cost factor of 12. It stores the user record in the `users` table of the primary database. On success, the endpoint returns a `201 Created` response. The response body contains the user's public profile as a JSON object.
>
> ```json
> {
>   "email": "ada@example.com",
>   "password": "s3cret",
>   "name": "Ada Lovelace"
> }
> ```
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

> **STE:** Install the project in four stages: dependencies, configuration, database setup, and server start.
>
> To install the project, clone the repository and run `npm install`. This command downloads all Node.js dependencies. The dependencies include `express` for the HTTP server, `pg` for the PostgreSQL client, and `redis` for the cache.
>
> Configure the environment variables. Copy the `.env.example` file to `.env`. Set the `DATABASE_URL` and `API_KEY` values in the `.env` file.
>
> ```bash
> cp .env.example .env
> # then edit .env and set:
> # DATABASE_URL=postgres://user:pass@localhost:5432/app
> # API_KEY=your-secret-key
> ```
>
> Set up the database. Run `npm run migrate` to create the schema. Run `npm run seed` to add sample data.
>
> ```bash
> npm run migrate
> npm run seed
> ```
>
> Start the development server with `npm run dev`. The server listens on port 3000 by default. To change the port, set the `PORT` environment variable. The server also starts a WebSocket server on the same port.
>
> *Principles applied: P1, P3. The Non-STE version is one long sentence covering four distinct topics (dependency install, configuration, database setup, server start). Each STE paragraph has one topic with supporting sentences.*

### Example 4 — Commit Message

> **Non-STE:** Fix the login bug where users could not authenticate after password reset, also refactored the user service to use the new repository pattern, and updated the dependencies to latest versions because there was a security vulnerability in the old express version, plus added a loading spinner to the login page.

> **STE:** Fix authentication failure after password reset.
>
> Fix authentication failure after password reset
>
> The `validatePasswordResetToken` function used a stale database connection. It did not pick up the new password hash after the reset completed. This commit changes the function to use a fresh connection from the pool for each validation.
>
> ```text
> # Commit command (one topic, one commit):
> git commit -m "Fix authentication failure after password reset"
> ```
>
> The refactor of the user service, the dependency update, and the UI spinner are separate topics. They belong in their own commits:
>
> - `Refactor user service to use the repository pattern`
> - `Bump express to a version that fixes CVE-2024-1234`
> - `Add loading spinner to the login page`
>
> *Principles applied: P1, P6. The Non-STE commit message has four unrelated topics (bug fix, refactor, dependency update, UI change). The STE version is one commit with one topic. The other changes belong in separate commits.*

### Example 5 — Class Documentation (OOP)

> **Non-STE:** The `PaymentProcessor` class handles all payment operations including credit card validation through the Stripe API, PayPal integration, refund processing which requires a 24-hour waiting period, receipt generation as a PDF, and it also manages the transaction log for audit purposes while maintaining compliance with PCI-DSS standards and logging all operations to the audit trail.

> **STE:** The `PaymentProcessor` class handles payment transactions for multiple payment providers.
>
> The `PaymentProcessor` class handles payment transactions. It validates payment methods, processes charges, and issues refunds.
>
> ```java
> public class PaymentProcessor {
>     private final Map<Provider, PaymentAdapter> adapters;
>     public PaymentProcessor(Map<Provider, PaymentAdapter> adapters) {
>         this.adapters = adapters;
>     }
>     public Charge process(ChargeRequest req) { /* ... */ }
>     public Refund processRefund(RefundRequest req) { /* ... */ }
> }
> ```
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

> **STE:** The database server did not accept the connection.
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
> ```bash
> # Check that PostgreSQL accepts connections on its port:
> pg_isready -h localhost -p 5432
> # expected output: "accepting connections"
> ```
>
> *Principles applied: P1, P3, P10. The Non-STE error message mixes symptoms, causes, and solutions with informal language ("probably", "also make sure"). The STE version separates the description, the causes, and the fix steps into distinct paragraphs.*

### Example 7 — Configuration Documentation

> **Non-STE:** The cache module supports Redis for production and an in-memory store for development, you configure it by setting `CACHE_DRIVER` to either `redis` or `memory`, and when using Redis you also need to set `REDIS_URL` and `REDIS_PREFIX` and optional `REDIS_TIMEOUT` in milliseconds which defaults to 5000, and the in-memory store has a `MAX_ITEMS` setting that defaults to 1000, and if you exceed that limit it evicts the least recently used items, also Redis supports clustering by setting multiple URLs in `REDIS_CLUSTER_URLS` as a comma-separated list.

> **STE:** The cache module supports two drivers: Redis and in-memory.
>
> The cache module supports two drivers: Redis and in-memory. Set the `CACHE_DRIVER` environment variable to `redis` or `memory`.
>
> ```toml
> # .env (or config.toml)
> CACHE_DRIVER = "redis"        # or "memory"
> REDIS_URL = "redis://localhost:6379"
> REDIS_PREFIX = "app-cache:"
> REDIS_TIMEOUT = 5000          # milliseconds
> REDIS_CLUSTER_URLS = "redis://node1:6379,redis://node2:6379"
> MAX_ITEMS = 1000              # used only when CACHE_DRIVER = "memory"
> ```
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

---

<!-- a-sec6-rule6.6.md -->

# Rule 6.6 — Make Sure That No Paragraph Has More Than Six Sentences

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.6

> **Source:** [master.md#sec6-rule6.6](ste-code/grouped/)

> Source: master.md#sec6-rule6.6

## Original Rule

Make sure that no paragraph has more than six sentences. Paragraphs divide a text into logical units and help keep the reader's attention. If paragraphs are too long, they cannot have this function. Do not put different topics in the same paragraph. If a paragraph has more than six sentences, divide it into two smaller paragraphs. This structure will make your text easier to read.

## STE-Code Adaptation

In code documentation, make sure that no paragraph has more than six sentences. Paragraphs divide a documentation block into logical units and help keep the developer's attention. If paragraphs are too long, they cannot have this function. Do not put different topics in the same paragraph. If a paragraph has more than six sentences, divide it into two smaller paragraphs. This structure will make your documentation easier to read.

### Examples

> *Adapted from spec pair:* Non-STE: "Description of the fuel manifold (refer to figure 10001)" / "The shut-off valve operates in the valve body (21). The valve body (21) has: an aluminum alloy ball, a retaining ring, two seals, a spring." (one fuel-manifold description split into five short paragraphs, each under six sentences) | STE: the same description kept as short single-topic paragraphs — in the code domain this becomes the connection-pool and request-handler examples below, where each component or phase gets its own paragraph.

> **Non-STE:** The following Python docstring puts four unrelated components and their behaviors into one paragraph of five overlong sentences:
>
> ```python
> class ConnectionPool:
>     """The connection pool manager has these primary components: a set of
>     pre-allocated socket connections that the manager reuses across requests
>     to avoid the cost of repeated TCP handshakes and TLS negotiation, a
>     background reaper thread that closes connections that have been idle
>     longer than the idle timeout and that also runs a periodic health probe
>     to detect dropped links, a bounded queue that holds pending acquire
>     requests when all connections are in use and that rejects new requests
>     with a timeout error after the acquire timeout expires, and a metrics
>     collector that records the number of active connections, the wait time
>     distribution, and the count of rejected acquires for the observability
>     stack; together these parts let the application serve high request rates
>     without opening a new connection for every call."""
> ```
>
> **STE:** Split the description into one short outline paragraph and four short paragraphs, each with its own topic and fewer than six sentences:
>
> ```python
> class ConnectionPool:
>     """The connection pool manager has these primary parts:
>     - A set of pre-allocated socket connections that the manager reuses.
>     - A background reaper thread.
>     - A bounded queue for pending acquire requests.
>     - A metrics collector.
>
>     The socket connections let the application reuse one link for many
>     requests. The reuse avoids repeated TCP handshakes and TLS negotiation.
>
>     The reaper thread closes connections that are idle longer than the idle
>     timeout. The reaper thread also runs a periodic health probe to find
>     dropped links.
>
>     The bounded queue holds pending acquire requests when all connections
>     are in use. The queue rejects new requests with a timeout error after the
>     acquire timeout expires.
>
>     The metrics collector records the number of active connections. The
>     collector also records the wait time distribution and the count of
>     rejected acquires. The observability stack reads these metrics."""
> ```
>
> *Code-domain example — the Non-STE version puts four unrelated components and their behaviors into one paragraph of five overlong sentences. The STE version splits the description into one short outline paragraph and four short paragraphs, each with its own topic and fewer than six sentences.*

> **Non-STE:** The following request-handler documentation crams an entire request lifecycle into a single one-paragraph sentence:
>
> ```markdown
> ## POST /orders
> The request handler module accepts an HTTP request, parses the JSON body,
> validates the schema against the openapi specification, authenticates the
> caller with the OAuth provider, authorizes the action against the role
> table, loads the target record from the primary database, applies the
> business rules, writes the audit entry, commits the transaction, and returns
> a 200 response with the updated resource, and if any step fails it rolls
> back the transaction and returns the appropriate 4xx or 5xx status with an
> error body.
> ```
>
> **STE:** Break the lifecycle into four paragraphs of two to four sentences each, one paragraph per phase: parse, authorize, act, and fail.
>
> ```markdown
> ## POST /orders
> The request handler module accepts an HTTP request. It parses the JSON body
> of the request.
>
> The handler validates the request schema against the openapi specification.
> It authenticates the caller with the OAuth provider. The handler
> authorizes the action against the role table.
>
> The handler loads the target record from the primary database. It applies
> the business rules to the record. The handler writes an audit entry. It
> commits the transaction. The handler returns a 200 response with the
> updated resource.
>
> If any step fails, the handler rolls back the transaction. It returns the
> appropriate 4xx or 5xx status with an error body.
> ```
>
> *Code-domain example — the Non-STE version crams an entire request lifecycle into a single one-paragraph sentence. The STE version breaks the lifecycle into four paragraphs of two to four sentences each, one paragraph per phase: parse, authorize, act, and fail.*

## Code-Domain Explanation

This rule keeps documentation readable by limiting the size of each paragraph. A paragraph is a group of sentences that share one topic. When a paragraph grows past six sentences, the reader loses the thread of the topic and must re-read to recover the structure. The six-sentence limit is a practical ceiling, not a target. Most good paragraphs use two to four sentences.

Rule 6.6 works with Rule 6.4 (use paragraphs to show related information) and Rule 6.5 (each paragraph has only one topic). Rule 6.4 tells you to use paragraphs. Rule 6.5 tells you to give each paragraph one topic. Rule 6.6 tells you not to let a paragraph grow past six sentences. The three rules together produce short, single-topic paragraphs that the developer can scan quickly.

### When to split a paragraph

Split a paragraph when any of these conditions is true:

- The paragraph has more than six sentences.
- The paragraph covers two or more topics (see Rule 6.5).
- A sentence in the paragraph introduces a new key word that the earlier sentences do not use (see Rule 6.2).

When you split, put the sentences that share one key word in the first paragraph. Put the sentences that share a different key word in the second paragraph. Start the second paragraph with a topic sentence that names the new key word.

### README Files

In a README, keep each feature description to a short paragraph. A feature paragraph that lists installation, configuration, and usage in one block of eight sentences forces the reader to parse three topics at once. Split it: one paragraph for what the feature does, one paragraph for how to enable it, one paragraph for a usage example.

> **Non-STE:** The `rate-limiter` middleware blocks abuse. Add it to your app with `pip install rate-limiter`, set `RATE_LIMIT=100` in your environment, import it in your `app.py`, wrap your routes with the `@limit` decorator, configure the window with `RATE_WINDOW=60`, and read the metrics from the `/metrics` endpoint which exposes the current count and the reject rate, and you should also add a test that sends 200 requests in one second to check that only 100 pass.
>
> **STE:** The `rate-limiter` middleware blocks abuse. It counts requests per client in a sliding window.
>
> Add the middleware with `pip install rate-limiter`. Import it in your `app.py`. Wrap your routes with the `@limit` decorator.
>
> Set these environment variables: `RATE_LIMIT=100` and `RATE_WINDOW=60`. The `/metrics` endpoint shows the current count and the reject rate.
>
> Add a test that sends 200 requests in one second. Check that only 100 requests pass.
>
> *Code-domain example — the install, configure, and verify steps become separate short paragraphs instead of one dense block.*

### API Documentation

In API documentation, keep each endpoint description in a short paragraph. Do not describe the request format, the authentication requirement, the response shape, and the error conditions in one long paragraph. Use one paragraph for the purpose of the endpoint, one paragraph for the request, one paragraph for the response, and one paragraph for the errors. Each paragraph must stay under six sentences.

### Docstrings

In a docstring, keep the summary paragraph short. If the docstring explains the parameters, the return value, and the raised exceptions, use one short paragraph per concern. A docstring that lists every parameter and every exception in one six-sentence paragraph is acceptable only if all the sentences describe the same function. If the parameter list grows long, move it to a bulleted list (as shown in the Examples) and keep the prose paragraph under six sentences.

### Error Messages and Log Entries

An error message is usually one sentence. A log entry is usually one line. These rarely reach six sentences. The rule applies when you write a recovery note or a multi-line diagnostic block. Keep the diagnostic block to six lines or fewer, or split it into a cause paragraph and a recovery paragraph.

## Paradigm-Specific Guidance

### Object-Oriented (Java, C++, C#, Python Classes)

In object-oriented documentation, describe one responsibility per paragraph. When you document a class with several collaborators, give each collaborator its own short paragraph.

> **Non-STE:** The following class docstring mixes every responsibility of `OrderService` into one paragraph:
>
> ```python
> class OrderService:
>     """The OrderService class creates orders, validates the cart total
>     against the pricing service, reserves inventory through the warehouse
>     client, charges the payment gateway, sends a confirmation email via the
>     notification service, writes the order to the orders table, and emits an
>     OrderCreated event to the message bus, and it also handles the
>     compensation flow that releases inventory and refunds the payment if the
>     downstream confirmation fails."""
> ```
>
> **STE:** Give each phase of the order lifecycle its own short paragraph:
>
> ```python
> class OrderService:
>     """The OrderService class creates orders. It validates the cart total
>     with the pricing service.
>
>     The OrderService reserves inventory through the warehouse client. It
>     charges the payment gateway.
>
>     The OrderService sends a confirmation email via the notification
>     service. It writes the order to the orders table. The class emits an
>     OrderCreated event to the message bus.
>
>     If the downstream confirmation fails, the OrderService runs a
>     compensation flow. The flow releases the reserved inventory. The flow
>     also refunds the payment."""
> ```
>
> *Principles applied: P5, P11 — each paragraph covers one phase of the order lifecycle and stays under six sentences.*

### Functional (Haskell, Elixir, Clojure, Rust)

In functional documentation, describe one transformation stage per paragraph. A pipeline that maps, filters, and folds should not live in one paragraph.

> **Non-STE:** The following function docstring describes every compiler stage in a single dense paragraph:
>
> ```rust
> /// The compile function parses the source string into a token stream,
> /// builds an abstract syntax tree, runs the type checker to infer and
> /// unify types, applies the desugaring pass that removes syntactic sugar,
> /// optimizes the tree with constant folding and dead code elimination, and
> /// finally emits the target bytecode, logging each stage to the compiler
> /// trace for debugging.
> fn compile(src: &str) -> Bytecode { /* ... */ }
> ```
>
> **STE:** Give each pipeline stage its own paragraph:
>
> ```rust
> /// The compile function parses the source string into a token stream.
> /// It builds an abstract syntax tree from the tokens.
> ///
> /// The function runs the type checker. The checker infers and unifies the
> /// types.
> ///
> /// The function applies the desugaring pass. The pass removes syntactic
> /// sugar.
> ///
> /// The function optimizes the tree. The optimization uses constant folding
> /// and dead code elimination.
> ///
> /// The function emits the target bytecode. It logs each stage to the
> /// compiler trace.
> fn compile(src: &str) -> Bytecode { /* ... */ }
> ```
>
> *Principles applied: P2, P10 — each pipeline stage is its own paragraph with fewer than six sentences.*

### Procedural (C, Go, Bash)

In procedural documentation, describe one phase of the script per paragraph. Do not document setup, execution, and cleanup in one paragraph.

> **Non-STE:** The following script header comment documents the whole deploy in one paragraph:
>
> ```bash
> # deploy.sh reads the target environment from the first argument, loads the
> # secrets from the vault into environment variables, builds the container
> # image with the build tag, pushes the image to the registry, updates the
> # manifest in the cluster, waits for the rollout to complete, runs a smoke
> # test against the health endpoint, and sends a notification to the release
> # channel, and if the smoke test fails it rolls back the manifest and alerts
> # the on-call engineer.
> ```
>
> **STE:** Document the build, rollout, verify, and fail phases as separate paragraphs:
>
> ```bash
> # deploy.sh reads the target environment from the first argument.
> # It loads the secrets from the vault into environment variables.
> #
> # The script builds the container image with the build tag.
> # It pushes the image to the registry.
> #
> # The script updates the manifest in the cluster.
> # It waits for the rollout to complete.
> #
> # The script runs a smoke test against the health endpoint.
> # It sends a notification to the release channel.
> #
> # If the smoke test fails, the script rolls back the manifest.
> # It alerts the on-call engineer.
> ```
>
> *Principles applied: P7, P10 — the build, rollout, verify, and fail phases are separate paragraphs, each under six sentences.*

### Declarative (SQL, Terraform, Kubernetes YAML)

In declarative documentation, describe one resource or one block per paragraph. A module that declares a database, a cache, and a queue should document each in its own paragraph.

> **Non-STE:** The following Terraform module description lists every resource in one paragraph:
>
> ```hcl
> # The web_app module provisions a PostgreSQL instance with automated backups
> # and a read replica, a Redis cache with a fixed eviction policy, an S3
> # bucket for static assets with lifecycle rules that expire old objects, a
> # load balancer that distributes traffic across the instances, and a
> # CloudWatch alarm that pages on high CPU, and the module wires the security
> # groups so that only the app tier can reach the database and only the load
> # balancer can reach the app tier.
> module "web_app" {
>   source = "./modules/web_app"
> }
> ```
>
> **STE:** Give each resource its own paragraph:
>
> ```hcl
> # The web_app module provisions a PostgreSQL instance. The instance uses
> # automated backups. It also uses a read replica.
> #
> # The module provisions a Redis cache. The cache uses a fixed eviction
> # policy.
> #
> # The module provisions an S3 bucket for static assets. The bucket uses
> # lifecycle rules that expire old objects.
> #
> # The module provisions a load balancer. The load balancer distributes
> # traffic across the instances.
> #
> # The module provisions a CloudWatch alarm. The alarm pages on high CPU.
> #
> # The module wires the security groups. Only the app tier can reach the
> # database. Only the load balancer can reach the app tier.
> module "web_app" {
>   source = "./modules/web_app"
> }
> ```
>
> *Principles applied: P5, P11 — each resource is its own paragraph; the security group paragraph is the sixth and final paragraph, still under the limit.*

### Systems (Rust Ownership, C Memory)

In systems documentation, describe one ownership rule per paragraph. Memory contracts are easy to bury in a long paragraph. Keep each contract to a few sentences.

> **Non-STE:** The following type docstring hides five ownership rules in one paragraph:
>
> ```rust
> /// The Buffer type owns a heap allocation that it frees on drop, it hands
> /// out borrowed slices through the as_slice method that tie their lifetime
> /// to the Buffer, it supports a split_at method that returns two
> /// non-overlapping borrowed slices for parallel processing, it clones
> /// cheaply by reference counting the underlying allocation when the Arc
> /// backend is selected, and it panics if a caller holds a borrowed slice
> /// and then calls a method that would reallocate the underlying buffer.
> struct Buffer { /* ... */ }
> ```
>
> **STE:** Give each ownership rule its own short paragraph:
>
> ```rust
> /// The Buffer type owns a heap allocation. It frees the allocation on drop.
> ///
> /// The Buffer hands out borrowed slices through the as_slice method. The
> /// slice lifetime ties to the Buffer.
> ///
> /// The Buffer supports a split_at method. The method returns two
> /// non-overlapping borrowed slices for parallel processing.
> ///
> /// The Buffer clones cheaply when the Arc backend is selected. The clone
> /// reference counts the underlying allocation.
> ///
> /// The Buffer panics if a caller holds a borrowed slice and then calls a
> /// method that reallocates. The reallocation would invalidate the borrowed
> /// slice.
> struct Buffer { /* ... */ }
> ```
>
> *Principles applied: P7, P11 — each ownership rule is its own paragraph; the panic rule is the fifth paragraph, under the six-sentence limit.*

## Extended Examples

### Example 1: Module Overview That Stays Under the Limit

> **Non-STE:** The `AuthModule` documentation describes five responsibilities in one paragraph:
>
> ```python
> class AuthModule:
>     """The AuthModule provides login, logout, token refresh, and password
>     reset, it integrates with the OAuth provider for social login and with
>     the email service for reset links, it stores sessions in the Redis cache
>     with a configurable TTL and replicates them across regions for
>     availability, it enforces rate limits on the login endpoint to block
>     credential stuffing attacks, and it emits security events to the audit
>     log for every privileged action, and the module exposes a health check
>     that reports the status of the OAuth provider, the Redis cache, and the
>     email service so that the orchestrator can remove an unhealthy instance
>     from the pool."""
> ```
>
> **STE:** Use six paragraphs, each under six sentences, one topic per paragraph:
>
> ```python
> class AuthModule:
>     """The AuthModule provides login, logout, token refresh, and password
>     reset.
>
>     The AuthModule integrates with the OAuth provider for social login. It
>     also integrates with the email service for reset links.
>
>     The AuthModule stores sessions in the Redis cache. The sessions use a
>     configurable TTL. The module replicates sessions across regions for
>     availability.
>
>     The AuthModule enforces rate limits on the login endpoint. The limits
>     block credential stuffing attacks.
>
>     The AuthModule emits security events to the audit log for every
>     privileged action.
>
>     The AuthModule exposes a health check. The check reports the status of
>     the OAuth provider, the Redis cache, and the email service. The
>     orchestrator removes an unhealthy instance from the pool."""
> ```
>
> *Principles applied: P6, P11 — six paragraphs, each under six sentences, one topic per paragraph.*

### Example 2: A Long Paragraph That Must Be Split

> **Non-STE:** The following migration docstring describes seven distinct changes in one sentence and one paragraph:
>
> ```python
> def upgrade():
>     """The migration adds a tenant_id column to the invoices table,
>     backfills the column from the accounts table using the
>     account-to-tenant mapping, creates a partial index on tenant_id where
>     the row is active, updates the InvoiceRepository query methods to filter
>     by the current tenant, adds a foreign key from invoices.tenant_id to
>     tenants.id, enables row-level security on the invoices table with a
>     policy that matches the session tenant, and rewrites the reporting
>     queries to aggregate per tenant instead of globally, and the migration
>     runs online with concurrent index creation so that the invoices table
>     stays available during the backfill."""
> ```
>
> **STE:** The seven changes become six short paragraphs, each under six sentences:
>
> ```python
> def upgrade():
>     """The migration adds a tenant_id column to the invoices table. It
>     backfills the column from the accounts table.
>
>     The migration creates a partial index on tenant_id for active rows. It
>     adds a foreign key from invoices.tenant_id to tenants.id.
>
>     The migration updates the InvoiceRepository query methods. The methods
>     now filter by the current tenant.
>
>     The migration enables row-level security on the invoices table. The
>     policy matches the session tenant.
>
>     The migration rewrites the reporting queries. The queries now aggregate
>     per tenant instead of globally.
>
>     The migration runs online with concurrent index creation. The invoices
>     table stays available during the backfill."""
> ```
>
> *Principles applied: P10, P12 — the seven changes become six short paragraphs, each under six sentences, instead of one unreadable paragraph.*

### Example 3: Configuration Reference With a Bulleted Paragraph

> **Non-STE:** The following `server` config section description is one dense sentence:
>
> ```yaml
> # The server section of the configuration file has these settings: host sets
> # the bind address and defaults to 0.0.0.0, port sets the listen port and
> # defaults to 8080, max_connections caps the concurrent client connections
> # and defaults to 1024, read_timeout sets the time to wait for a request and
> # defaults to 30s, tls.cert points to the certificate file and tls.key
> # points to the private key file, and keepalive sets the idle connection
> # timeout and defaults to 60s, and all of these settings can be overridden
> # by environment variables with the same name prefixed by SERVER_.
> server:
>   host: 0.0.0.0
>   port: 8080
> ```
>
> **STE:** Make the settings one bulleted paragraph and keep the override rule in a separate short prose paragraph:
>
> ```yaml
> # The server section of the configuration file has these settings:
> # - host — the bind address. The default is 0.0.0.0.
> # - port — the listen port. The default is 8080.
> # - max_connections — the cap on concurrent client connections. The default
> #   is 1024.
> # - read_timeout — the time to wait for a request. The default is 30s.
> # - tls.cert — the path to the certificate file.
> # - tls.key — the path to the private key file.
> # - keepalive — the idle connection timeout. The default is 60s.
> #
> # You can override all of these settings with environment variables. Use
> # the same name with the SERVER_ prefix.
> server:
>   host: 0.0.0.0
>   port: 8080
> ```
>
> *Principles applied: P9 — the long list becomes a bulleted paragraph for the settings and one short prose paragraph for the override rule, keeping the prose under six sentences.*

### Example 4: Changelog Entry That Respects the Limit

> **Non-STE:** The following changelog entry packs five unrelated changes into one paragraph:
>
> ```markdown
> ## v3.1.0
> The v3.1.0 release adds a streaming export mode for the report builder that
> yields rows to the client as they are computed instead of buffering the
> whole result, deprecates the exportCsv synchronous method in favor of the
> new streamExport method, fixes a bug where the date filter ignored the
> timezone of the report viewer and returned rows from the wrong day, improves
> the dashboard load time by deferring the loading of the secondary widgets
> until the primary chart renders, and updates the dependency on the charting
> library to a version that patches a cross-site scripting vulnerability in
> the tooltip renderer.
> ```
>
> **STE:** Give each change type its own short paragraph. Mark the API removal as deprecated:
>
> ```markdown
> ## v3.1.0
> The v3.1.0 release has these changes:
>
> DEPRECATED: The exportCsv synchronous method is deprecated. Use the new
> streamExport method instead.
>
> Add a streaming export mode for the report builder. The mode yields rows to
> the client as they are computed. It does not buffer the whole result.
>
> Fix a bug in the date filter. The filter ignored the timezone of the report
> viewer. It returned rows from the wrong day.
>
> Improve the dashboard load time. Defer the loading of the secondary widgets
> until the primary chart renders.
>
> Update the charting library dependency. The new version patches a
> cross-site scripting vulnerability in the tooltip renderer.
> ```
>
> *Principles applied: P11 — each change type is its own short paragraph; the deprecation uses the DEPRECATED mapping for an API removal.*

### Example 5: Test Plan Description With Separate Paragraphs

> **Non-STE:** The following test-suite docstring describes setup, run, and teardown in one paragraph:
>
> ```python
> def test_integration_suite():
>     """The integration test suite sets up a temporary database, seeds it
>     with fixture data for three users and two tenants, starts the
>     application in a background process bound to a test port, waits for the
>     health check to report ready, runs the happy-path scenario that creates
>     an order and verifies the invoice, runs the failure scenario that
>     simulates a payment gateway timeout and verifies the compensation flow,
>     runs the concurrency scenario that issues one hundred parallel requests
>     and verifies that no two responses share a sequence number, tears down
>     the application process, and drops the temporary database, and the
>     suite writes a JUnit report to the build/reports directory and exits
>     with a non-zero status if any scenario fails."""
> ```
>
> **STE:** Keep the setup, run, and teardown phases as separate paragraphs, each under six sentences:
>
> ```python
> def test_integration_suite():
>     """The integration test suite sets up a temporary database. It seeds the
>     database with fixture data for three users and two tenants.
>
>     The suite starts the application in a background process. The process
>     binds to a test port. The suite waits for the health check to report
>     ready.
>
>     The suite runs the happy-path scenario. The scenario creates an order
>     and verifies the invoice.
>
>     The suite runs the failure scenario. The scenario simulates a payment
>     gateway timeout. It verifies the compensation flow.
>
>     The suite runs the concurrency scenario. The scenario issues one hundred
>     parallel requests. It verifies that no two responses share a sequence
>     number.
>
>     The suite tears down the application process. It drops the temporary
>     database. The suite writes a JUnit report to the build/reports
>     directory. It exits with a non-zero status if any scenario fails."""
> ```
>
> *Principles applied: P10, P12 — the setup, run, and teardown phases are separate paragraphs, each under six sentences.*

## Edge Cases

### Edge Case 1: A Paragraph That Needs More Than Six Sentences for One Topic

Some topics are intrinsically complex and need more than six sentences to explain one idea. In that case, keep the paragraph under six sentences and continue the same topic in a second paragraph. Start the second paragraph with a connecting phrase such as "Also," or "In addition," so the reader knows the topic continues.

> **Non-STE:** The following GC docstring buries ten behaviors in one paragraph:
>
> ```python
> def collect():
>     """The garbage collector traces live objects, marks them, sweeps the
>     unreachable ones, compacts the heap to reduce fragmentation, and records
>     the pause time to the metrics endpoint, and it also promotes long-lived
>     objects to the old generation, adjusts the survivor space ratio based on
>     the observed promotion rate, and logs a concurrent mode failure when the
>     heap fills faster than it can reclaim, which forces a full
>     stop-the-world collection that the latency budget must absorb."""
> ```
>
> **STE:** Continue the same topic (garbage collection) across two paragraphs, each under six sentences, and connect them with "In addition,":
>
> ```python
> def collect():
>     """The garbage collector traces live objects. It marks them. It sweeps
>     the unreachable objects. It compacts the heap to reduce fragmentation.
>     It records the pause time to the metrics endpoint.
>
>     In addition, the collector promotes long-lived objects to the old
>     generation. It adjusts the survivor space ratio from the promotion rate.
>     It logs a concurrent mode failure when the heap fills faster than it can
>     reclaim. The failure forces a full stop-the-world collection. The
>     latency budget must absorb that collection."""
> ```
>
> *Principles applied: P6, P10 — the topic (garbage collection) continues across two paragraphs, each under six sentences.*

### Edge Case 2: A List Paragraph Counts as One Paragraph

A bulleted or numbered list is one paragraph, regardless of how many items it contains. Rule 6.6 limits the prose sentences that surround or introduce the list, not the number of list items. Keep the introductory sentence short. Do not add a long closing sentence that restates every item.

> **Non-STE:** The following manifest docstring uses one long sentence to introduce and restate an eight-item list:
>
> ```markdown
> ## Deploy
> The deployment manifest must include all of the following resources, and you
> should verify each one before you apply the manifest because a missing
> resource will cause the rollout to fail and the orchestrator will not roll
> back automatically so you will need to inspect the events and apply the
> correction by hand: the config map, the secret, the deployment, the
> service, the ingress, the horizontal pod autoscaler, the pod disruption
> budget, and the network policy.
> ```
>
> **STE:** The list is one paragraph; keep the surrounding prose under six sentences:
>
> ```markdown
> ## Deploy
> The deployment manifest must include these resources:
> - The config map.
> - The secret.
> - The deployment.
> - The service.
> - The ingress.
> - The horizontal pod autoscaler.
> - The pod disruption budget.
> - The network policy.
>
> Verify each resource before you apply the manifest. A missing resource
> causes the rollout to fail.
> ```
>
> *Principles applied: P9 — the list is one paragraph; the surrounding prose stays under six sentences.*

### Edge Case 3: Generated Documentation That Produces Long Paragraphs

Auto-generated reference docs (from JSDoc, Sphinx, or OpenAPI generators) often emit one long paragraph per symbol. You cannot always control the generator output. When you can, set the generator to break the description at sentence boundaries. When you cannot, add a short human-written summary above the generated block. The summary must follow Rule 6.6. The generated block is exempt only if you do not edit its source annotations.

> **Non-STE (generator output, not edited):**
>
> ```markdown
> ### `validate_token`
> Validates the given JWT against the signing key, checks the expiry and the
> issuer claim, decodes the payload, loads the user from the cache or the
> database, and raises an error if any check fails. (one long generated
> paragraph)
> ```
>
> **STE (human-written summary added above the generated block):**
>
> ```markdown
> ### `validate_token`
> The function checks a JWT and loads the matching user.
>
> (generated) Validates the given JWT against the signing key, checks the
> expiry and the issuer claim, decodes the payload, loads the user from the
> cache or the database, and raises an error if any check fails.
> ```
>
> *Principles applied: P9 — the human summary is one short paragraph; the generated block is exempt because its source annotation was not edited.*

### Edge Case 4: A Paragraph That Mixes Two Topics but Stays Under Six Sentences

A short paragraph can still violate Rule 6.5 by mixing two topics. Rule 6.6 and Rule 6.5 are independent. A three-sentence paragraph that describes both the cache and the queue in unrelated ways must split even though it is under the sentence limit.

> **Non-STE:** The following comment mixes the cache topic and the queue topic in three sentences:
>
> ```python
> # The cache stores the rendered pages. The queue buffers the email jobs.
> # The cache uses a least-recently-used eviction policy.
> def serve(request): ...
> ```
>
> **STE:** Split the two topics even though the original is only three sentences:
>
> ```python
> # The cache stores the rendered pages. It uses a least-recently-used
> # eviction policy.
> #
> # The queue buffers the email jobs.
> def serve(request): ...
> ```
>
> *Principles applied: P11 — the cache and the queue are two topics; split them even though the original is only three sentences.*

## Cross-References

- **Rule 6.4 — Use Paragraphs to Show Related Information:** Rule 6.6 is the size limit that Rule 6.4 assumes. Use paragraphs to group related information, then keep each paragraph under six sentences.
- **Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic:** Rule 6.6 limits the sentence count; Rule 6.5 limits the topic count. A paragraph can be short and still wrong if it mixes topics. Check both rules.
- **Rule 6.1 — Give Information Gradually:** Short paragraphs support gradual information delivery. When you split a long paragraph, the new paragraphs continue the same flow sentence by sentence.
- **Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure:** The key word of a paragraph is the topic. When you split a paragraph, the new paragraph starts with the new key word as its topic sentence.
- **Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence:** Short sentences make it easier to stay under six sentences per paragraph. A paragraph of six short sentences reads faster than a paragraph of three long sentences.

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure; Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence; Rule 6.4 — Use Paragraphs to Show Related Information; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic

## Grammar Notes

### Why six sentences

The six-sentence limit comes from reading psychology. A reader holds the topic of a paragraph in working memory. After about six sentences, the topic fades and the reader must re-read to recover it. The limit is a guard against paragraph drift, where the writer adds one more sentence and the paragraph quietly changes topic.

### Sentence count, not word count

Rule 6.6 counts sentences, not words. A paragraph can have six short sentences or six long sentences and still pass the rule. However, a paragraph of six long sentences is harder to read than a paragraph of six short sentences. Apply Rule 6.3 (maximum 25 words per sentence) together with Rule 6.6 for the best result. A paragraph of six sentences that each have 25 words is at the edge of readability. Prefer two to four sentences per paragraph.

### Lists and tables reset the count

A bulleted list, a numbered list, or a table inside a paragraph does not add to the sentence count of the surrounding prose. The introductory sentence and the closing sentence are the prose. Keep those under six sentences total. If the list needs explanation, put the explanation in the list items, not in a long closing sentence.

### Splitting technique

When a paragraph exceeds six sentences, split at the sentence where the key word changes (see Rule 6.2) or where the topic changes (see Rule 6.5). Put the first group of sentences in the original paragraph. Start a new paragraph with a topic sentence that names the new key word. Do not repeat the old key word in the new paragraph unless it is part of the new topic.

### Interaction with procedures

In procedural writing (Section 5), each step is its own paragraph by convention. Rule 6.6 rarely applies to procedures because steps are short. It applies when a step description includes a long note or rationale. Keep the note under six sentences or move it to a separate note paragraph.
