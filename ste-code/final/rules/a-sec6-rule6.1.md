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
