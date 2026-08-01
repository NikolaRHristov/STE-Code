<!-- a-sec5-rule5.1.md -->

# Rule 5.1 — Short Sentences (Maximum 20 Words)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 5.1
> **Source:** [master.md#sec5-rule5.1](ste-code/grouped/)

## Original Rule

Write short sentences. Use a maximum of 20 words in each sentence.

Procedures give instructions that tell you how to do a task. Long sentences in work steps are not easy to understand.

In STE, the maximum length of a sentence for procedures is 20 words.

Warnings, cautions, and other safety instructions must also obey this rule.

Examples in STE:

> **STE:** Install the three auxiliary screws (2) in the flange of the motor assembly (9). (This sentence has 14 words.)

> **CAUTION:** WHEN YOU REMOVE THE SHROUD (26), BE CAREFUL NOT TO CAUSE DAMAGE TO THE SURFACE OF THE FLANGE ASSEMBLY (22). (This sentence has 20 words.)

> **Non-STE:** Put preservation oil into the unit through the vent hole until the oil level is approximately 6 mm (0.24 inches) below the surface of the flange cover. (25 words)
>
> **STE:** Put preservation oil into the unit through the vent hole. (10 words) Continue until the oil level is approximately 6 mm (0.24 in) below the surface of the flange cover. (16 words)

Note: Section 8 gives all the rules about word count.

Notes (rule 5.5) do not obey rule 5.1. Notes are important in procedures, but they contain information only. Thus, the maximum length of a sentence in a note is 25 words.

> **See also:** Rule 5.5 — Notes Give Information Only, Not Instructions

## STE-Code Adaptation

In code documentation, procedures include installation instructions, setup steps, deployment checklists, debugging workflows, and API usage guides. Long sentences in these procedures make them difficult to follow, especially when the reader is executing commands or writing code while reading.

Keep every sentence in code documentation procedures to a maximum of 20 words. Break long procedural sentences into shorter sentences, each focusing on one part of the task. Warnings and caution statements about security, data loss, or system stability must also obey the 20-word limit.

Notes in code documentation procedures have a maximum sentence length of 25 words. Notes give supplementary information only and are not required for the reader to complete the procedure.

This rule applies to sentences in procedural documentation text. Code snippets, command examples, and terminal output that appear inside code blocks are not subject to the word count rule. String literals and identifier names inside code examples are also excluded from the word count.

### Examples

> *Adapted from spec pair:* Non-STE: Put preservation oil into the unit through the vent hole until the oil level is approximately 6 mm (0.24 inches) below the surface of the flange cover. | STE: Put preservation oil into the unit through the vent hole. Continue until the oil level is approximately 6 mm (0.24 in) below the surface of the flange cover.

> **Non-STE:** Run the database migration script from the project root directory and then restart the application server to apply all pending schema changes to the production environment. (27 words)
>
> **STE:** Run the database migration script from the project root directory. (9 words) Then, restart the application server to apply all pending schema changes. (13 words)
>
> *Source pairing: the long-sentence-to-two-shorter-sentences split in the Non-STE/STE pair directly above follows the same principle as the original STE example in Rule 5.1.*

```bash
cd /srv/payments-service
alembic upgrade head
systemctl restart payments.service
```

> **Non-STE:** The initialization process will automatically create the required directory structure and populate it with default configuration files before the application starts. (22 words)
>
> **STE:** The initialization process automatically creates the required directory structure. (8 words) Then, it populates the directory with default configuration files. (10 words)
>
> *Additional code-domain example — no direct spec pair*

```bash
./payments-service init
# creates ./config and ./data, then writes config/default.toml
```

> **Non-STE:** Set the environment variable HTTP_TIMEOUT to the value 30000 which represents the maximum number of milliseconds that the client will wait for a response from the upstream server. (30 words)
>
> **STE:** Set the environment variable HTTP_TIMEOUT to 30000. (8 words) This value is the maximum wait time in milliseconds for a response from the upstream server. (17 words)
>
> *Additional code-domain example — no direct spec pair*

```bash
export HTTP_TIMEOUT=30000
```

> **CAUTION:** IF YOU DELETE THE CONFIGURATION DIRECTORY WITHOUT A BACKUP, YOU CANNOT RESTORE THE APPLICATION SETTINGS TO THEIR PREVIOUS STATE. (18 words)
>
> *Adapted from spec example: a CAUTION that stays within the 20-word limit on destructive operations — see the original STE example in Rule 5.1.*

```bash
cp -r ./config ./config.bak   # back up first
rm -rf ./config               # then delete
```

> **Non-STE:** For more detailed information about the supported authentication methods and their respective configuration parameters in this release, please refer to the official authentication module documentation page. (27 words)
> **STE (note):** For more information about the supported authentication methods, refer to the authentication module documentation. (15 words)
>
> *Adapted from original rule — notes have a maximum sentence length of 25 words; no direct spec pair*

```text
NOTE: Supported methods are OAuth2, API key, and mTLS.
See docs/auth.md for setup steps.
```

## Code-Domain Explanation

Rule 5.1 applies to all procedural text in software documentation. A procedure is any sequence of instructions that tells the reader how to complete a task. In code documentation, procedures appear in many forms. Each form must obey the 20-word sentence limit.

### README Files

README files contain installation procedures, configuration steps, and quick-start guides. Each step in these procedures must use sentences of 20 words or fewer. A long installation instruction is difficult to follow while the reader types commands in a terminal window. Break long steps into two or more shorter steps. Each step must give exactly one instruction.

> **Non-STE:** Clone the repository to your local machine using the command shown below and then navigate into the newly created project directory before running the setup script. (28 words)

```bash
git clone https://github.com/example/payments-service.git && cd payments-service && ./setup.sh
```

> **STE:** Clone the repository to your local machine. (6 words) Then, navigate into the new project directory. (7 words) Run the setup script. (4 words)

```bash
git clone https://github.com/example/payments-service.git
cd payments-service
./setup.sh
```

> *Principle: P12 (technical verbs: clone, navigate, run). Four instructions become four sentences. Each step is a separate command the reader can copy and run.*

### API Documentation

API reference pages describe endpoints, parameters, return types, and error codes. Procedural sentences in API docs include setup instructions, authentication flows, and request sequencing. Parameter descriptions in tables are descriptive, not procedural. Use the 25-word limit for descriptive sentences in API parameter tables. Apply the 20-word limit to sentences that tell the reader to perform an action.

> **Non-STE:** The `page` query parameter accepts a positive integer value that specifies which page of results the server should return in the paginated response to this endpoint. (28 words)
>
> **STE (descriptive):** The `page` query parameter accepts a positive integer. (8 words) It specifies which page of results to return. (9 words) This is for paginated responses. (6 words)
>
> *Principle: P1 (use approved words: accepts, specifies, return). Descriptive sentences may use up to 25 words each. Here, the longest is 9 words. The original sentence packs three pieces of information into one clause chain.*

Request the second page of a paginated list:

```http
GET /v1/orders?page=2&page_size=50 HTTP/1.1
Host: api.example.com
Authorization: Bearer <token>
```

### Docstrings and Inline Comments

Docstrings for functions and methods often contain procedural instructions for callers. Each sentence in a docstring procedure must obey the 20-word limit. Descriptive sentences about return values or side effects may use up to 25 words. Inline comments that give instructions must also obey the limit.

> **Non-STE:** Call this method to initialize the connection pool with the provided configuration and establish the minimum number of idle connections specified in the pool settings before returning control to the caller. (32 words)
>
> **STE:** Call this method to initialize the connection pool. (8 words) Use the provided configuration. (4 words) The method establishes the minimum number of idle connections. (10 words) Then, it returns control to the caller. (8 words)
>
> *Principle: P2 (use words only as specified part of speech: "initialize" as verb, "configuration" as noun). One long sentence with three embedded actions becomes four sentences.*

Compliant Python docstring:

```python
def init_pool(config: PoolConfig) -> ConnectionPool:
    """Initialize the connection pool.

    Use the provided configuration. The method establishes the minimum
    number of idle connections. Then, it returns control to the caller.
    """
    ...
```

### Commit Messages

A commit message subject line is a short summary of the change. Keep the subject line to 72 characters or fewer. This is a separate constraint from the word count rule. The commit message body contains procedural or descriptive sentences. Apply the 20-word limit to procedural sentences in the body. Apply the 25-word limit to descriptive sentences.

> **Non-STE:** Refactored the authentication middleware to extract the token validation logic into a separate utility function so that it can be reused by the WebSocket upgrade handler and the GraphQL subscription resolver as well. (35 words)
>
> **STE (body):** Refactored the authentication middleware. (4 words) Extracted the token validation logic into a separate utility function. (11 words) The WebSocket upgrade handler and the GraphQL subscription resolver now reuse this function. (15 words)
>
> *Principle: P11 (one term per concept: "token validation logic" is used consistently). The justification ("so that it can be reused...") becomes a separate declarative sentence.*

Compliant commit:

```text
Refactor authentication middleware

Extracted the token validation logic into a separate utility function.
The WebSocket upgrade handler and the GraphQL subscription resolver now
reuse this function.
```

### Error Messages

Error messages shown to the user must be short and clear. Use the 20-word limit for error messages that tell the user to take action. Error messages that only report a condition may use the 25-word descriptive limit. Error messages are read under stress. Short sentences reduce the cognitive load on the user.

> **Non-STE:** The configuration file could not be parsed because it contains a syntax error on line 42 that is most likely caused by a missing closing bracket or an unquoted string value containing special characters. (35 words)
>
> **STE:** The configuration file has a syntax error on line 42. (11 words) Check for a missing closing bracket or an unquoted string value. (13 words)
>
> *Principle: P3 (use words only with approved meanings: "has" instead of "contains," "check" instead of "is most likely caused by"). The diagnosis and the remedy are separated.*

Show the message as a short, actionable string:

```text
Config error on line 42: missing closing bracket or unquoted string.
```

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

OOP documentation describes class hierarchies, constructor parameters, method signatures, and inheritance chains. Procedural sentences in OOP docs include step-by-step instantiation guides, dependency injection setup, and mock configuration for tests.

Sentence-length pitfalls in OOP docs include long sentences that describe all constructor parameters at once, sentences that chain multiple method calls in one instruction, and sentences that explain both the "what" and the "why" of a design pattern in a single breath.

> **Non-STE:** The constructor accepts a database connection string, a logger instance that must implement the ILogger interface, and an optional configuration object for setting the retry policy and the connection timeout duration. (33 words)
>
> **STE:** The constructor accepts three parameters. (5 words) Parameter one is a database connection string. (7 words) Parameter two is a logger instance. It must implement the ILogger interface. (6 + 7 words) Parameter three is an optional configuration object. (7 words) Use this object to set the retry policy and the connection timeout. (14 words)
>
> *Principle: P5 (technical code nouns: ILogger, configuration object). Each parameter is documented in its own sentence cluster. The reader can focus on one parameter at a time.*

C# constructor signature:

```csharp
public DatabaseClient(
    string connectionString,
    ILogger logger,
    ClientConfig? config = null
) { ... }
```

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, type signatures, monadic chains, and pattern matching. The 20-word rule helps readers follow the flow of data through function compositions. Long sentences that trace data through multiple composed functions are common in functional docs and must be split.

> **Non-STE:** The `process` function first maps the transformation over each element in the list and then filters out any results that are `None` before finally folding the remaining values into a single accumulator using the provided binary operator. (35 words)
>
> **STE:** The `process` function maps a transformation over each element in the list. (13 words) Then, it filters out any `None` results. (8 words) Finally, it folds the remaining values into a single accumulator. (13 words) The provided binary operator controls the fold. (8 words)
>
> *Principle: P12 (technical verbs: maps, filters, folds). Each stage of the pipeline gets its own sentence. The reader traces data flow one transformation at a time.*

Haskell implementation:

```haskell
process :: (a -> b) -> (b -> Bool) -> (b -> b -> b) -> [a] -> b
process f p op = foldl1 op . filter p . map f
```

### Procedural Documentation (C, Go, Bash)

Procedural code tends to have long sequences of setup, validation, and teardown steps. Documentation that mirrors this structure is especially prone to long sentences. Sentence-length pitfalls include sentences that combine error checking with the operation being checked and sentences that describe conditional branching in prose.

> **Non-STE:** Run the configure script to detect your system's available libraries and compiler features and then run make with the -j flag set to the number of CPU cores on your machine to compile the program from source. (37 words)
>
> **STE:** Run the configure script. (4 words) This script detects your system libraries and compiler features. (10 words) Then, run make to compile the program from source. (12 words) Use the -j flag. Set it to the number of CPU cores on your machine. (14 + 11 words)
>
> *Principle: P9 (short, clear technical nouns: configure script, make, -j flag). The detection phase and the compilation phase are separated. Flag usage is its own step.*

Bash build commands:

```bash
./configure
make -j"$(nproc)"
```

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes the desired state of a system. Procedures in declarative docs include migration runbooks, apply-and-verify workflows, and rollback instructions. Long sentences that describe a resource and all its attributes together are the most common violation.

> **Non-STE:** Execute the migration script against the production database after taking a full backup and verifying that the replication lag on all read replicas is less than five seconds to prevent any data inconsistency during the schema change. (38 words)
>
> **STE:** Take a full backup of the production database. (8 words) Verify that the replication lag on all read replicas is less than five seconds. (16 words) Then, execute the migration script against the production database. (11 words)
>
> *Principle: P8 (standard, well-known technical nouns: backup, replication lag, migration script). Prerequisites are checked before the action. The sequence is explicit. The justification ("to prevent data inconsistency") is implied by the ordering.*

Terraform migration runbook:

```bash
pg_dump "$PROD_DSN" > backup_$(date +%F).sql
REPLICA_LAG=$(psql "$PROD_DSN" -t -c "SELECT EXTRACT(SECONDS FROM now() - pg_last_xact_replay_timestamp());")
[ "$(echo "$REPLICA_LAG < 5" | bc)" -eq 1 ] && alembic upgrade head
```

### Systems Documentation (Rust Ownership, C Memory Management)

Systems documentation describes ownership models, memory allocation, lifetimes, and safety guarantees. These topics are complex. Short sentences prevent the reader from missing critical safety information. Long safety warnings that bury the hazard in context are dangerous and must be split.

> **Non-STE:** After calling this function the caller must not use the original buffer pointer because ownership of the memory has been transferred to the callee and any subsequent access through the old pointer will result in undefined behavior. (37 words)
>
> **STE:** After you call this function, do not use the original buffer pointer. (14 words) Ownership of the memory is transferred to the callee. (11 words) Access through the old pointer causes undefined behavior. (10 words)
>
> *Principle: P1 (use approved words: "causes" instead of "will result in"). The prohibition, the reason, and the consequence each get their own sentence. Safety-critical information is never buried in a subordinate clause.*

Rust signature that transfers ownership:

```rust
fn take_buffer(buf: Vec<u8>) -> Parser {
    // buf is moved into Parser; the caller's buf is no longer valid.
    Parser::new(buf)
}
```

## Extended Examples

Each example below shows a Non-STE sentence (violating the rule) and the STE-Code compliant version. The principle applied and a brief explanation follow each pair.

### Example 1 — Docker Setup Instructions

> **Non-STE:** Build the Docker image using the Dockerfile in the project root and then run a container from that image with port 8080 on the host mapped to port 80 inside the container. (33 words)
>
> **STE:** Build the Docker image. (4 words) Use the Dockerfile in the project root. (8 words) Then, run a container from that image. (9 words) Map port 8080 on the host to port 80 inside the container. (15 words)
>
> *Principle: P8 (standard technical nouns: Docker image, Dockerfile, container), P12 (technical verbs: build, run, map). The original sentence combines three procedural steps into one. The STE version splits the build, the file specification, the run command, and the port mapping into separate sentences. Each sentence now focuses on one action.*

Docker commands:

```bash
docker build -t payments-service:latest .
docker run -p 8080:80 payments-service:latest
```

### Example 2 — Git Workflow Instructions

> **Non-STE:** Create a new feature branch from the main branch, implement your changes in that branch, push the branch to the remote repository, and then open a pull request against the main branch for code review. (35 words)
>
> **STE:** Create a new feature branch from the main branch. (10 words) Implement your changes in that branch. (7 words) Push the branch to the remote repository. (9 words) Then, open a pull request against the main branch. (11 words)
>
> *Principle: P12 (technical verbs: create, push, open), P9 (short, clear technical nouns: branch, pull request). A four-step workflow was written as one sentence joined by commas and "and." The STE version gives each step its own sentence. The reader can complete one step before reading the next.*

Git commands:

```bash
git switch -c feature/token-cache main
# ... make changes, commit ...
git push -u origin feature/token-cache
gh pr create --base main --title "Add token cache"
```

### Example 3 — Configuration File Documentation

> **Non-STE:** The `retry_policy` section of the configuration file lets you define whether the client should retry failed requests, how many times it should retry before giving up and throwing an error, and the backoff strategy to use between consecutive retry attempts. (39 words)
>
> **STE:** The `retry_policy` section controls how the client handles failed requests. (12 words) Set the number of retry attempts. (7 words) Set the backoff strategy between attempts. (7 words) The client throws an error when all retries fail. (11 words)
>
> *Principle: P1 (use approved verbs: controls, handles, set — instead of "lets you define"), P11 (one term per concept, consistent throughout). The original sentence describes three configuration options in one breath. The STE version separates the conceptual overview from each specific setting.*

YAML configuration:

```yaml
retry_policy:
  max_attempts: 3
  backoff: exponential
```

### Example 4 — API Rate Limiting Documentation

> **Non-STE:** When a client exceeds the rate limit of 100 requests per minute the server will respond with HTTP status code 429 and include a Retry-After header that tells the client how many seconds it must wait before sending another request to the same endpoint. (42 words)
>
> **STE:** The rate limit is 100 requests per minute. (8 words) When a client exceeds this limit, the server responds with HTTP status 429. (14 words) The response includes a Retry-After header. (7 words) This header tells the client how many seconds to wait. (12 words) Then, the client can send another request. (8 words)
>
> *Principle: P2 (use words only as specified part of speech), P12 (technical verbs: responds, includes, send), P5 (technical code nouns: HTTP status 429, Retry-After). A complex conditional with embedded clauses is restructured into a sequence of short, declarative sentences. Each sentence states one fact about the system behavior.*

Server response:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
Content-Type: application/json

{"error": "rate_limit_exceeded", "retry_after": 30}
```

### Example 5 — Debugging Instructions

> **Non-STE:** To debug the authentication failure you should first check the application logs for any error messages related to token validation and then verify that the JWT secret in your environment variables matches the secret that was used to sign the token that the client is sending. (44 words)
>
> **STE:** To debug the authentication failure, check the application logs. (10 words) Look for error messages about token validation. (8 words) Then, verify that the JWT secret in your environment variables matches the signing secret. (17 words)
>
> *Principle: P3 (use words only with approved meanings), P13 (do not use technical verbs as nouns: "sign" is a verb here). The original sentence has embedded relative clauses ("that was used to sign the token that the client is sending"). The STE version removes the nesting and restates the verification as a simple equality check. The longest sentence drops from 44 to 17 words.*

Bash debug steps:

```bash
kubectl logs deploy/auth-service | grep -i "token"
echo "$JWT_SECRET"
jwt decode "$ACCESS_TOKEN" | grep -i secret
```

### Example 6 — CI/CD Pipeline Documentation

> **Non-STE:** The deployment pipeline will automatically run the full test suite on every push to the main branch and if all tests pass it will build a production Docker image and push it to the container registry before updating the Kubernetes deployment with the new image tag. (44 words)
>
> **STE:** The deployment pipeline runs the full test suite on every push to the main branch. (17 words) If all tests pass, the pipeline builds a production Docker image. (13 words) Then, it pushes the image to the container registry. (11 words) Finally, it updates the Kubernetes deployment with the new image tag. (14 words)
>
> *Principle: P12 (technical verbs: runs, builds, pushes, updates), P8 (standard technical nouns: Docker image, container registry, Kubernetes deployment), P11 (consistent term: "pipeline" throughout). A CI/CD pipeline description is restructured into a sequential narrative. Each stage of the pipeline gets its own sentence. The conditional is isolated from the build step.*

CI configuration (GitHub Actions):

```yaml
on:
  push:
    branches: [main]
jobs:
  deploy:
    steps:
      - run: pytest
      - run: docker build -t registry.example.com/app:${{ github.sha }} .
      - run: docker push registry.example.com/app:${{ github.sha }}
      - run: kubectl set image deploy/app app=registry.example.com/app:${{ github.sha }}
```

## Edge Cases

### Edge Case 1 — Long Framework or Service Names

Some technical names are unavoidably long. "Amazon Web Services Elastic Kubernetes Service" is one technical noun phrase with six words. When a sentence must include a long proper noun, the word count may exceed 20 words through no fault of the writer.

**Guidance:** Use the shortest accepted form of the name on first use. Define an abbreviation. Then, use the abbreviation in later sentences. This is consistent with Rule 1.9 (prefer short, clear technical nouns). The abbreviation itself counts as one word.

> **Non-STE:** Create a new cluster in Amazon Web Services Elastic Kubernetes Service using the eksctl command-line tool with the provided cluster configuration YAML file that specifies three worker nodes of type t3.medium. (30 words)
>
> **STE:** Create a new cluster in Amazon EKS. (7 words) Use the eksctl command-line tool. (6 words) Use the provided cluster configuration YAML file. (8 words) The file must specify three worker nodes of type t3.medium. (13 words)

```bash
eksctl create cluster -f cluster-config.yaml
```

```yaml
# cluster-config.yaml
nodeGroups:
  - name: workers
    instanceType: t3.medium
    desiredCapacity: 3
```

### Edge Case 2 — Code Keywords That Form Long Phrases

Some code keyword sequences form long noun phrases that consume many word-count slots. For example: "the `async fn` with `impl Future<Output = Result<T, E>>` return type" contains several tokens. Counting conventions matter for compliance.

**Guidance:** Code elements inside backticks count as one word each, regardless of their character length. This aligns with the principle that code identifiers are opaque tokens, not prose words. Apply this rule consistently: `Result<T, E>` is one word, `async fn` is two words. Do not expand generics or type parameters into prose words.

> **Non-STE:** The function signature `pub async fn fetch_user(id: UserId) -> Result<User, Error>` specifies that the function is public and asynchronous and returns a Result type that wraps either a User value or an Error value. (33 words under prose counting rules)
>
> **STE:** The function signature is `pub async fn fetch_user(id: UserId) -> Result<User, Error>`. (8 words) The function is public and asynchronous. (6 words) It returns a Result type. (6 words) The Result wraps a User value or an Error value. (11 words)
>
> *Under the code-token counting convention, the STE version's longest procedural sentence is 11 words. The code block in backticks counts as one word.*

Rust signature:

```rust
pub async fn fetch_user(id: UserId) -> Result<User, Error> {
    let row = db.query_one("SELECT * FROM users WHERE id = $1", &[&id]).await?;
    Ok(User::from_row(row)?)
}
```

### Edge Case 3 — Generated Documentation

Auto-generated API reference docs (from Javadoc, Sphinx, rustdoc, or TypeDoc) may produce sentences that exceed the 20-word limit. These tools often concatenate parameter descriptions or return-type explanations into compound sentences without the writer's control.

**Guidance:** Apply the 20-word rule to the source docstrings and comments that the generator reads. The generator output inherits compliance from its input. If a generator produces non-compliant output from compliant input, file a bug against the generator. Do not manually edit generated output — fix the source docstring.

If fixing the source is not practical (third-party library, legacy code), apply the 25-word descriptive limit to the generated sentences. Document the exception in a project style guide. Never relax the rule for generated code that you control.

### Edge Case 4 — Legal and Compliance Disclaimers

Legal disclaimers, license headers, and regulatory compliance statements are not procedural documentation. They are legal text. The 20-word procedural limit does not apply to legal text.

**Guidance:** Place legal text in a clearly marked section separate from procedures. Use a NOTE block or a dedicated "Legal" heading. This prevents readers from confusing legal text with actionable instructions. If a legal sentence appears inside a procedure, move it to a NOTE that precedes or follows the procedure. Annotate it clearly: "NOTE (legal requirement): ..."

### Edge Case 5 — Multi-Line Code Examples Embedded in Prose

When a sentence introduces a multi-line code example mid-sentence, the sentence may appear to exceed 20 words if the code block is mistakenly counted as prose. The code block itself is excluded from the count (as stated in the STE-Code Adaptation section). The sentence that introduces or follows the code block must still obey the limit independently.

> **Non-STE:** Use the following configuration block in your docker-compose.yml file to set up the service with the correct environment variables and port mappings as shown in the example below. (27 words, excluding the code block)
>
> **STE:** Use this configuration block in your docker-compose.yml file: (9 words) This configuration sets the correct environment variables and port mappings. (11 words)

```yaml
services:
  web:
    image: nginx:1.27
    environment:
      - LOG_LEVEL=info
    ports:
      - "8080:80"
```

> *The introductory sentence and the follow-up sentence are each under the 20-word limit. The code block is not counted.*

## Grammar Notes

### Sentence Boundaries

A sentence is a group of words that ends with a period (.), a question mark (?), or an exclamation point (!). Each sentence must express a complete thought. Do not join independent clauses with commas. Use a period instead. A comma does not end a sentence for the purpose of word counting.

The word count of a sentence includes all words between the initial capital letter and the terminal punctuation. Hyphenated compound words count as one word (for example, "command-line" is one word). Numbers, symbols, and parenthetical references each count as one word. For example, "(2)" is one word. "HTTP/2" is one word.

### Splitting Long Sentences

When a procedural sentence exceeds 20 words, split it using one of these techniques:

**1. Split at coordinating conjunctions.** Replace "and," "but," or "or" with a period. Start the next sentence with a transition word: "Then," "After that," or "Next."

> **Non-STE:** Run the migration script if the database version is earlier than 4.2 and the backup job has completed successfully without errors or warnings. (24 words)
>
> **STE:** Make sure the database version is 4.2 or later. (10 words) Make sure the backup job completed successfully. (7 words) Then, run the migration script. (5 words)

```sql
SELECT version();          -- must be >= 4.2
SELECT status FROM backups;  -- must be 'completed'
-- then:
alembic upgrade head
```

**2. Extract conditions into their own sentence.** Move a conditional clause ("if X, then Y") into a separate sentence that precedes or follows the main instruction. This also improves comprehension because the reader checks the condition before attempting the action.

**3. Separate the action from its purpose.** Put the instruction in one sentence. Put the reason or result in the next sentence.

> **Non-STE:** Set the `NODE_ENV` variable to `production` so that the application loads the optimized configuration and disables the development-only debugging middleware and hot-reload features. (26 words)
>
> **STE:** Set the `NODE_ENV` variable to `production`. (6 words) This setting loads the optimized configuration. (6 words) It disables debugging middleware and hot-reload features. (8 words)

```bash
export NODE_ENV=production
```

**4. Use lists.** Convert a sentence that enumerates items into a bulleted or numbered list. Each list item can be a fragment or a short sentence. List items are not subject to the 20-word sentence limit because they are not sentences — but keep each item short for readability.

### Avoiding Run-On Sentences

A run-on sentence joins two or more independent clauses without proper punctuation or conjunctions. In code documentation, run-on sentences often appear when describing a sequence of API calls or a multi-step process.

Do not use semicolons to join independent clauses. Semicolons create ambiguity about where one instruction ends and the next begins. Use periods. Each instruction deserves its own sentence. The semicolon suggests a relationship between clauses that the writer should make explicit by using separate sentences with clear transition words.

### Coordinating Conjunction Policy

Coordinating conjunctions (and, but, or, nor, for, so, yet) may join two short, related clauses in a single sentence only when the total word count remains at or below 20. If the combined sentence exceeds 20 words, split it at the conjunction.

> **STE (allowed):** Run the tests and check the output. (8 words)
>
> *"And" joins two short clauses. The total is 8 words, well under 20. No split is needed.*

> **Non-STE:** Run the full test suite with coverage reporting enabled and check the generated report for any untested code paths that might indicate gaps in the test plan. (28 words)
>
> **STE:** Run the full test suite with coverage reporting enabled. (9 words) Then, check the generated report for untested code paths. (11 words) These gaps can indicate missing test coverage. (8 words)

```bash
pytest --cov=src --cov-report=term-missing
```

### Subordinate Clause Depth

Limit subordinate clause depth to two levels. A sentence with three or more levels of embedding is difficult to parse and usually exceeds the 20-word limit. Flatten deep structures by promoting embedded clauses to their own sentences.

> **Non-STE:** The server returns an error when the client sends a request that contains a payload that exceeds the limit that the administrator configured in the settings file. (27 words, 4 levels of embedding)
>
> **STE:** The server returns an error when the request payload exceeds the configured limit. (13 words) The administrator sets this limit in the settings file. (11 words)
>
> *Two levels of embedding replaced with two sentences at one level each.*

```python
MAX_PAYLOAD = settings["max_payload_bytes"]  # set by the administrator

def handle(req):
    if len(req.body) > MAX_PAYLOAD:
        raise PayloadTooLarge(settings["max_payload_bytes"])
```

## Cross-References

- **Rule 1.1** — Use Approved Words: Short sentences are easier to write when you choose short, approved words from the STE-Code dictionary. See the Canonical Synonym Table for preferred single-word verbs.
- **Rule 1.2** — Use Words Only as Their Specified Part of Speech: Incorrect part-of-speech usage often produces wordy constructions. Correct usage produces tighter sentences that stay within the limit.
- **Rule 1.4** — Use Only Approved Verb and Adjective Forms: Non-standard verb forms (for example, "-ing" forms as main verbs) add words. Approved forms are shorter.
- **Rule 1.5** — Technical Code Nouns Are Allowed: Technical nouns may be long. Use abbreviations after first definition to stay within the 20-word limit. See Edge Case 1.
- **Rule 1.7** — Do Not Use Technical Nouns as Verbs: Nominalization adds words. "Perform an initialization" (3 words) becomes "initialize" (1 word). Short verbs keep sentences short.
- **Rule 1.9** — Prefer Short, Clear Technical Nouns: Short technical nouns help keep sentences under 20 words. "Config" is one word; "configuration parameters" is two.
- **Rule 1.12** — Technical Verbs Are Allowed: Use short technical verbs (build, push, run, test, lint) instead of long descriptive phrases ("carry out a build process").
- **Rule 5.2** — Use the Active Voice: Passive constructions add words ("The file is read by the parser" vs. "The parser reads the file"). Active voice keeps sentences short.
- **Rule 5.3** — Use Imperative Mood for Instructions: Imperative sentences drop the subject ("You must run the command" becomes "Run the command"). This removes one or two words per sentence.
- **Rule 5.5** — Notes Give Information Only, Not Instructions: Notes have a 25-word sentence limit. Procedures have a 20-word limit. Know which type of text you are writing.
- **Rule 5.7** — Use Bulleted or Numbered Lists for Complex Information: Lists break long compound sentences into scannable items. See Grammar Notes, technique 4.
- **Section 8** — Word Count Rules: Contains all rules about counting words in STE sentences. Refer to Section 8 for hyphenation, abbreviation counting, and numerical expression rules.

## Compliance Checklist

Use this checklist to verify that procedural sentences in your code documentation obey Rule 5.1:

- [ ] Every procedural sentence has 20 words or fewer.
- [ ] Every note sentence has 25 words or fewer.
- [ ] Warning and caution statements obey the 20-word limit.
- [ ] No two independent clauses are joined by a comma (no comma splices).
- [ ] No semicolons join independent clauses.
- [ ] Each procedural sentence gives exactly one instruction.
- [ ] Long sentences are split at conjunctions or conditional boundaries.
- [ ] Code blocks, terminal output, and string literals are excluded from word counts.
- [ ] Code tokens inside backticks count as one word each.
- [ ] Long technical names are abbreviated after first definition.
- [ ] Generated documentation is reviewed for compliance at the source level.
- [ ] Subordinate clauses are limited to two levels of depth.
- [ ] Coordinating conjunctions join two clauses only when the total is 20 words or fewer.

---

<!-- a-sec5-rule5.2.md -->

# Rule 5.2 — One Instruction Per Sentence

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 5.2
> **Source:** [master.md#sec5-rule5.2](ste-code/grouped/)

## Original Rule

Write only one instruction in each sentence unless two or more actions occur at the same time.

If there are too many instructions in a sentence, the sentence is not easy to read and understand.

Write only one instruction in each sentence and clearly show (usually with numbers or letters) the sequence of the work steps. You can use as many work steps as you want in a procedure.

Examples:

> **STE:** (1) Set the TEST switch to the middle position.
> **STE:** (2) Make sure that all the switches on the control panel are OFF.

(Two work steps)

> **Non-STE:** Put preservation oil into the unit through the vent hole until the oil level is approximately 6 mm (0.24 inches) below the surface of the flange cover. (25 words)
>
> **STE:** Put preservation oil into the unit through the vent hole. (10 words) Continue until the oil level is approximately 6 mm (0.24 in) below the surface of the flange cover. (16 words)

Examples of actions that occur at the same time:

- Hold the panel in its open position and install the fastener.
- Slowly extend the rod fully and make sure that it does not touch other parts.
- Cut and remove the wire.
- Remove and discard the seal.

## Procedures

You can write more than one sentence in a work step:

- When actions occur at the same time
- When a result occurs immediately after an action.

Examples in STE:

Make sure that the locking torque of each of the four bolts (6) is a minimum of 0.30 Nm. Then, torque each of the four bolts (6) to 4.20 Nm.

(During a torque procedure, the torque action immediately follows the check of the locking torque in one action. Thus, you cannot divide the sentence into two different work steps.)

Measure the leakage from the outlet port. The leakage must not be more than 0.5 cc/minute.

(The second sentence here gives the limit for the result of the test. The work step occurs in one action, and you cannot divide the sentence into two different work steps.)

## STE-Code Adaptation

In code documentation, procedural steps must be easy for the reader to execute one at a time. When a sentence contains multiple instructions, the reader can miss or skip an action, leading to errors in configuration, deployment, or debugging.

Write only one instruction for the reader to perform in each sentence. Use numbered or bulleted lists to show the sequence of steps clearly. There is no limit on the number of work steps in a procedure.

You may write two instructions in one sentence with the conjunction "and" only when both actions must occur at the same time and cannot be separated into distinct steps. Examples include operations where the reader must hold one state while performing another action, or where two actions are part of a single continuous motion.

You may write more than one sentence in a single work step when:

- Two or more actions occur at the same time and are inseparable
- A result or measurement occurs immediately after an action, and describing them in separate steps would break the logical flow of the procedure.

### Examples

> *Adapted from spec pair:* Non-STE: Put preservation oil into the unit through the vent hole until the oil level is approximately 6 mm (0.24 inches) below the surface of the flange cover. | STE: Put preservation oil into the unit through the vent hole. Continue until the oil level is approximately 6 mm (0.24 in) below the surface of the flange cover.

> **Non-STE:** Open the configuration file in a text editor and locate the database section and change the connection string to point to the staging server and then save the file and close the editor. (37 words, 5 instructions)
>
> **STE:** (1) Open the configuration file in a text editor. (2) Locate the database section. (3) Change the connection string to point to the staging server. (4) Save the file. (5) Close the editor.
>
> (Each instruction is a separate work step.)
>
> *Source pairing: split one compound instruction into separate numbered work steps — follows the same principle as the original STE example in Rule 5.2.*

*Documentation context — the STE version in `docs/CONFIGURATION.md`:*

```markdown
## Point the app at the staging database

1. Open `config/database.toml` in a text editor.
2. Find the `[database]` section.
3. Set `connection_string = "postgres://staging-db:5432/app"`.
4. Save the file.
5. Close the editor.

The file has this shape:

```toml
[database]
connection_string = "postgres://localhost:5432/app"
pool_size = 10
```
```

> **Non-STE:** Run the test suite with the coverage flag enabled and verify that the total line coverage is above 80 percent across all modules in the project. (27 words)
>
> **STE:** Run the test suite with the coverage flag enabled. (9 words) The total line coverage must be more than 80 percent across all project modules. (14 words)
>
> (The second sentence states the result limit. The work step is one action and cannot be divided into two separate work steps.)
>
> *Source pairing: a result or limit that follows the action immediately in the same work step — follows the same principle as the original STE example in Rule 5.2.*

*Documentation context — the STE version in `CONTRIBUTING.md` and the command that produces it:*

```markdown
## Run the tests

Run the suite with coverage:

    pytest --cov=src --cov-report=term-missing

The total line coverage must be more than 80 percent across all project modules.
```

> **Non-STE:** Make sure the environment variable DATABASE_URL is set correctly and then execute the initialization script to create the required database tables and populate them with the seed data. (31 words)
>
> **STE:** Make sure that the environment variable DATABASE_URL is set correctly. Then, execute the initialization script. The script creates the required database tables and populates them with the seed data.
>
> (The check and the execution form one continuous work step. The third sentence explains what the script does.)
>
> *Source pairing: a check that is immediately followed by the related action in one work step — follows the same principle as the original STE example in Rule 5.2.*

*Documentation context — the STE version in `docs/local-dev.md`:*

```markdown
## Set up the local database

Make sure that the `DATABASE_URL` environment variable is set correctly:

    export DATABASE_URL="postgres://localhost:5432/app"

Then, run the initialization script:

    python scripts/init_db.py

The script creates the required tables and loads the seed data.
```

Actions that occur at the same time:

- Hold the Shift key and click the Reload button.
- Press and release the reset button on the device.
- Copy and replace the existing configuration file.
- Download and extract the archive to the target directory.

> **Non-STE:** Set the logging level to debug mode and then restart the application server and after that monitor the log output in the terminal for any error messages that appear during the startup sequence. (35 words)
>
> **STE:** (1) Set the logging level to debug. (2) Restart the application server. (3) Monitor the terminal log output for error messages during the startup sequence.
>
> (Three separate instructions, three work steps.)
>
> *Additional code-domain example — no direct spec pair*

*Documentation context — the STE version in `docs/ops/runbook.md`:*

```markdown
## Debug a slow startup

1. Set the logging level to debug in `config/logging.yaml`:

   ```yaml
   logging:
     level: debug
   ```

2. Restart the application server:

       systemctl restart app-server

3. Watch the terminal log output for error messages during the startup sequence:

       journalctl -u app-server -f
```

## Code-Domain Explanation

This rule operates differently across the five primary code documentation types. Each type has a distinct audience, reading pattern, and failure mode when instructions are combined in a single sentence.

### README Files

README files serve as the entry point for new users and contributors. Readers scan README sections quickly — often while simultaneously typing commands in a terminal. When a sentence embeds multiple instructions, the reader must pause, re-read, and decompose the compound instruction into individual actions. This increases the probability that a step is skipped or executed out of order.

Every numbered step in a README quick-start or installation section must contain exactly one instruction. If a step produces a result that must be checked, state the result in a second sentence within the same numbered step (as allowed by the result-immediately-after-action exception).

Example of a correctly structured README setup section:

```markdown
## Quick start

1. Install the package with pip:

       pip install ste-code

2. Copy the example configuration file to your project root.
   The file `config.example.toml` includes default values for all settings.

3. Set the `DATABASE_URL` environment variable:

       export DATABASE_URL="postgres://localhost:5432/app"

4. Run the initialization command.
   The command `python scripts/init_db.py` creates the required database tables.
```

Do not write:

```markdown
## Quick start

1. Install the package with pip and copy the example config file and set DATABASE_URL.
```

### API Documentation

API reference documentation describes discrete operations. Each endpoint, method parameter, return value, and error condition must be described in its own sentence. When an endpoint description combines the HTTP method, request body format, authentication requirement, and expected response into one paragraph, the reader must mentally partition the information — a task that generates errors during integration.

Each API documentation block should follow this sentence structure:

- Sentence 1: What the endpoint does (one operation).
- Sentence 2: The HTTP method and path.
- Sentence 3: Required authentication or headers.
- Subsequent sentences: One per request body field, one per query parameter, one per response field, one per error code.

Example of a correctly structured OpenAPI description block:

```markdown
### Create a user

Create a new user account.
Send a `POST` request to `/v1/users`.
The request needs a `Bearer` token in the `Authorization` header.
The request body has a `username` field of type string.
The request body has an `email` field of type string.
The response returns status `201 Created` on success.
The response body has an `id` field of type string.
The response returns status `409 Conflict` when the username is taken.
```

### Docstrings

Docstrings (Python, Java, Rust, Go, and similar) have a constrained format. The first line is a single-sentence summary of what the function or class does. If the summary contains multiple instructions joined by "and", it violates Rule 5.2.

The body of the docstring may contain multiple sentences, but each must describe one aspect of the function's contract:

- One sentence for each parameter.
- One sentence for the return value.
- One sentence for each raised exception or error condition.
- One sentence for each side effect or precondition.

**Non-STE docstring:**

```python
def connect(db_url, timeout):
    """Connect to the database using the given URL and configure the
    connection pool with the specified timeout and start the background
    health check thread."""
```

**STE-Code docstring:**

```python
def connect(db_url, timeout):
    """Open a connection to the database at the given URL.
    Configure the connection pool with the specified timeout.
    Start the background health check thread.

    Args:
        db_url: The connection string for the database.
        timeout: The maximum wait time for a connection, in seconds.

    Returns:
        A live database connection.

    Raises:
        ConnectionError: The database is unreachable.
    """
```

### Commit Messages

Commit messages have two parts: a subject line and an optional body. The subject line must be one imperative sentence describing one change. If a commit makes multiple unrelated changes, split the commit — do not combine them in one subject line.

The body may contain multiple sentences, but each sentence must describe one change, one reason, or one effect. Use bullet points in the body when describing multiple distinct changes within the same commit.

**Non-STE commit subject:**

```
Add user authentication and refactor database layer and update API docs
```

**STE-Code commit subject:**

```
Add user authentication module
```

(The refactor and doc update belong in separate commits, or as body bullets.)

**STE-Code commit with related changes in the body:**

```
Add user authentication module

- Add the login and session endpoints.
- Update the OpenAPI schema with the new routes.
- Add the auth integration tests.
```

### Error Messages

Error messages must state exactly one problem. When an error message combines multiple failure conditions, the reader cannot determine which condition triggered the error or which corrective action to take first.

Each error message must:

- State what went wrong (one condition).
- State what action to take (one instruction), if applicable.
- Not combine multiple failure paths with "or", "and", or "also".

**Non-STE error message:**

```text
ERROR: The database connection failed and the retry limit was exceeded or the
configuration file is missing required fields.
```

**STE-Code error messages (two separate conditions):**

```text
ERROR: The database connection failed. The retry limit of 3 attempts was exceeded.
```

```text
ERROR: The configuration file is missing required fields: host, port, database.
```

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Class documentation must separate construction, configuration, and invocation instructions. A constructor's documentation should describe initialization in one sentence per parameter. Method documentation must describe the method's single responsibility in the summary sentence, then elaborate with one sentence per precondition, side effect, and postcondition.

When documenting a class that requires a multi-step setup sequence (e.g., factory pattern, builder pattern), number each step. Do not chain method calls in a single prose sentence.

**Non-STE class setup:**

```java
// Create a new HttpClient, set the timeout and retry policy, then
// call execute with the request object.
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(30))
    .retryPolicy(RetryPolicy.exponentialBackoff())
    .build();
client.execute(request);
```

**STE-Code class setup:**

```java
// 1. Create a new HttpClient instance.
// 2. Set the connect timeout to 30 seconds.
// 3. Set the retry policy to exponential backoff.
// 4. Call execute with the request object.
HttpClient client = HttpClient.newBuilder()
    .connectTimeout(Duration.ofSeconds(30))
    .retryPolicy(RetryPolicy.exponentialBackoff())
    .build();
client.execute(request);
```

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional code documentation describes pure transformations. Each function's documentation must describe one transformation. When documenting a pipeline or composition of functions, describe each stage in its own sentence — do not combine multiple map/filter/reduce operations into one explanatory sentence.

Function signatures in functional languages often express multiple constraints. Document each type parameter, each constraint, and each argument in its own sentence.

**Non-STE pipeline description:**

```rust
/// Filters the list to remove null values, maps each remaining element
/// through the parser, and collects the successful results.
fn parse_all(items: Vec<Option<&str>>) -> Vec<Value> { /* ... */ }
```

**STE-Code pipeline description:**

```rust
/// Remove null values from the list.
/// Map each remaining element through the parser.
/// Collect the successful results.
fn parse_all(items: Vec<Option<&str>>) -> Vec<Value> { /* ... */ }
```

### Procedural Documentation (C, Go, Bash)

Procedural code executes statements sequentially. The documentation for procedural code must mirror this sequential nature: one documented step per executable statement. Bash script comments are especially vulnerable to multi-instruction compression because script authors often write one comment block before a sequence of commands.

**Non-STE Bash comment:**

```bash
# Download the latest release binary, verify its checksum, and move it to
# /usr/local/bin.
curl -fsSL "$URL" -o /tmp/cli
sha256sum -c /tmp/cli.sha256
mv /tmp/cli /usr/local/bin/cli
```

**STE-Code Bash comments:**

```bash
# Download the latest release binary.
curl -fsSL "$URL" -o /tmp/cli

# Verify the checksum of the downloaded binary.
sha256sum -c /tmp/cli.sha256

# Move the binary to /usr/local/bin.
mv /tmp/cli /usr/local/bin/cli
```

Each comment sits on the line immediately before the command it describes.

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative configurations describe desired state. Each resource, each property, and each constraint must be described in its own sentence. When a Terraform resource documentation block combines the resource's purpose, required arguments, optional arguments, and output attributes into one paragraph, the reader must disentangle the information before they can write the configuration.

**Non-STE Terraform resource docs:**

```hcl
# Creates an S3 bucket with versioning enabled, a lifecycle policy to
# delete old objects after 30 days, and a private ACL.
resource "aws_s3_bucket" "logs" {
  bucket = "app-logs"
  versioning { enabled = true }
  lifecycle_rule { expiration { days = 30 } }
  acl = "private"
}
```

**STE-Code Terraform resource docs:**

```hcl
# This resource creates an S3 bucket.
# It enables versioning on the bucket.
# It configures a lifecycle policy to delete objects after 30 days.
# It sets the bucket ACL to private.
resource "aws_s3_bucket" "logs" {
  bucket = "app-logs"
  versioning { enabled = true }
  lifecycle_rule { expiration { days = 30 } }
  acl = "private"
}
```

### Systems Documentation (Rust Ownership, C Memory Model)

Systems documentation describes invariants, guarantees, and safety conditions. Each invariant must be stated in its own sentence because combining multiple invariants obscures which condition applies to which component. Rust ownership documentation is particularly sensitive: a sentence that combines borrowing rules, lifetime constraints, and safety guarantees can cause the reader to misunderstand the memory model.

**Non-STE ownership docs:**

```rust
/// Borrows the buffer immutably for the read operation and returns a
/// reference to the parsed data that is valid for the lifetime of the input.
fn parse<'a>(buf: &'a [u8]) -> &'a Parsed { /* ... */ }
```

**STE-Code ownership docs:**

```rust
/// Borrow the buffer immutably for the duration of the read operation.
/// Return a reference to the parsed data.
/// The returned reference is valid for the lifetime of the input buffer.
fn parse<'a>(buf: &'a [u8]) -> &'a Parsed { /* ... */ }
```

## Extended Examples

Each example below shows a real code documentation scenario, the Non-STE violation, the STE-Code compliant version, the principle applied, and an explanation.

### Example 1: API Endpoint Setup Documentation

> **Non-STE:** Send a POST request to the /users endpoint with a JSON body that contains the username and email fields and then check that the response status code is 201 and verify that the Location header contains the URL of the newly created user resource. (45 words, 4 instructions)
>
> **STE:** (1) Send a POST request to the /users endpoint. Include a JSON body with the username and email fields. (2) Check that the response status code is 201. (3) Make sure that the Location header contains the URL of the new user resource.
>
> **Principle applied:** Rule 5.2 (one instruction per sentence) and Rule 5.1 (short sentences, max 20 words per procedural sentence).
>
> **Explanation:** The Non-STE version chains four instructions (send, include, check, verify) with "and". The STE version numbers the steps and separates the request body description from the response validation. Step (1) contains two sentences because describing the body immediately after the action is a result-immediately-after-action exception.

*Documentation context — the full `docs/api/users.md` block:*

```markdown
## Create a user

1. Send a `POST` request to `/v1/users`.
   Include a JSON body with the `username` and `email` fields:

   ```json
   { "username": "ada", "email": "ada@example.com" }
   ```

2. Check that the response status code is `201`.
3. Make sure that the `Location` header contains the URL of the new user resource.
```

### Example 2: Docker Compose Quick-Start

> **Non-STE:** Clone the repository to your local machine and then navigate into the project directory and run docker compose up to start all the services and after that open your browser and go to http://localhost:3000 to see the application. (38 words, 5 instructions)
>
> **STE:** (1) Clone the repository to your local machine. (2) Go to the project directory. (3) Run `docker compose up` to start all the services. (4) Open a browser. (5) Go to http://localhost:3000.
>
> **Principle applied:** Rule 5.2 (one instruction per sentence) and Rule 1.12 (technical verbs: clone, run are allowed).
>
> **Explanation:** The Non-STE version uses "and then" / "and after that" to chain five sequential actions. The STE version assigns a numbered step to each action. The infinitive phrase "to start all the services" is preserved in step (3) as a purpose clause, which is not an instruction.

*Documentation context — the full `README.md` quick-start:*

````markdown
## Run locally

1. Clone the repository:

       git clone https://github.com/example/app.git

2. Go to the project directory:

       cd app

3. Run `docker compose up` to start all the services.
4. Open a browser.
5. Go to http://localhost:3000.
````

### Example 3: Configuration File Editing Guide

> **Non-STE:** Open the .env file in your preferred text editor and locate the line that starts with JWT_SECRET and replace the placeholder value with a randomly generated 256-bit key that you can create using the openssl rand -hex 32 command and then save the file and restart the application server for the changes to take effect. (52 words, 5 instructions)
>
> **STE:** (1) Open the .env file in a text editor. (2) Find the line that starts with `JWT_SECRET`. (3) Replace the placeholder value with a new secret key. To generate a key, run: `openssl rand -hex 32`. (4) Save the file. (5) Restart the application server. The changes take effect after the restart.
>
> **Principle applied:** Rule 5.2 and the result-immediately-after-action exception. Also Rule 1.1 (use approved words: "find" not "locate", "make" not "create").
>
> **Explanation:** The key-generation instruction is separated from the replacement instruction. The final sentence states the result (changes take effect) as a separate descriptive sentence within step (5).

*Documentation context — the full `docs/configuration.md` guide:*

````markdown
## Rotate the JWT secret

1. Open the `.env` file in a text editor.
2. Find the line that starts with `JWT_SECRET`.
3. Replace the placeholder value with a new secret key.
   To generate a key, run:

       openssl rand -hex 32

4. Save the file.
5. Restart the application server.
   The changes take effect after the restart.
````

### Example 4: Database Migration Rollback

> **BREAKING:** This migration drops the legacy_orders table and all associated indexes and foreign key constraints and cannot be rolled back automatically so you must create a full database backup before running this migration. (33 words, 4 warnings/instructions)
>
> **STE:**
> **BREAKING:** This migration drops the `legacy_orders` table. It removes all associated indexes and foreign key constraints.
> **IMPORTANT:** You cannot roll back this migration automatically. Create a full database backup before you run this migration.
>
> **Principle applied:** Rule 5.2 and the BREAKING safety marker conventions. Result-immediately-after-action: the removal of indexes follows the table drop.
>
> **Explanation:** The Non-STE version combines the destructive action description, the consequence, and the mitigation instruction in one sentence. The STE version separates the BREAKING block (what the migration does) from the operational instruction (what the user must do before running it).

*Documentation context — the full `migrations/0042_drop_legacy_orders.md` notice:*

````markdown
# Migration 0042 — Drop legacy_orders

**BREAKING:** This migration drops the `legacy_orders` table.
It removes all indexes and foreign key constraints that reference it.

**IMPORTANT:** You cannot roll back this migration automatically.
Create a full database backup before you run this migration:

    pg_dump app > backup-before-0042.sql
````

### Example 5: CI/CD Pipeline Step Documentation

> **Non-STE:** The build stage compiles the TypeScript source files and runs the unit tests with Jest and then packages the application into a Docker image and pushes it to the container registry with the git commit SHA as the image tag. (38 words, 4 actions described)
>
> **STE:** The build stage has four steps: (1) Compile the TypeScript source files. (2) Run the unit tests with Jest. (3) Package the application into a Docker image. (4) Push the image to the container registry. The image tag is the git commit SHA.
>
> **Principle applied:** Rule 5.2. Descriptive sentences (building the pipeline documentation) must also obey the one-instruction-per-sentence rule when they describe a sequence of actions.
>
> **Explanation:** Even when documenting an automated pipeline (not instructing a human), describing actions one per step improves clarity and maintainability. The final sentence is a descriptive detail, not an instruction.

*Documentation context — the full `.github/workflows/build.yml` step list:*

````yaml
# The build job runs these steps in order:
# 1. Compile the TypeScript source files.
# 2. Run the unit tests with Jest.
# 3. Package the application into a Docker image.
# 4. Push the image to the container registry.
# The image tag is the git commit SHA.
jobs:
  build:
    steps:
      - run: tsc --noEmit
      - run: jest
      - run: docker build -t registry/app:${GITHUB_SHA} .
      - run: docker push registry/app:${GITHUB_SHA}
````

### Example 6: Git Workflow Documentation

> **Non-STE:** Create a new feature branch from the main branch and make your code changes on that branch and then commit your changes with a descriptive message and push the branch to the remote repository and open a pull request against the main branch. (40 words, 5 instructions)
>
> **STE:** (1) Create a new feature branch from the `main` branch. (2) Make your code changes on the feature branch. (3) Commit your changes with a descriptive message. (4) Push the branch to the remote repository. (5) Open a pull request against the `main` branch.
>
> **Principle applied:** Rule 5.2. Each git operation is a discrete action that the user executes as a separate command.
>
> **Explanation:** This is the most common violation in open-source contributing guides. Writers compress the entire git workflow into one or two sentences. The STE version mirrors how the user actually works: one command, one step, one sentence.

*Documentation context — the full `CONTRIBUTING.md` workflow:*

````markdown
## Submit a change

1. Create a feature branch from `main`:

       git switch -c feat/short-description

2. Make your code changes on the feature branch.
3. Commit your changes with a descriptive message:

       git commit -m "Add rate limit to login endpoint"

4. Push the branch to the remote repository:

       git push -u origin feat/short-description

5. Open a pull request against `main`.
````

## Edge Cases

### Edge Case 1: Framework CLI Commands That Look Like Multiple Instructions

When a framework CLI command name contains an action word (e.g., `docker compose up`, `kubectl apply`, `terraform destroy`), the command is one technical noun phrase (Rule 1.5). Do not split the command name into separate instructions. Use backticks to mark the command as a technical noun.

> **STE:** Run `docker compose up` to start the services.
>
> **Do not write:** Run docker. Then run compose. Then run up.

Even though "compose" and "up" resemble action words, the token `docker compose up` is a single technical invocation.

### Edge Case 2: Error Messages With Multiple Root Causes

Sometimes a single failure produces multiple cascading symptoms. The error message should state the root cause (one instruction) and, if helpful for debugging, list the symptoms in a separate descriptive sentence.

> **STE ERROR:** The database connection failed. The host `db.example.com` is not reachable on port 5432.

Do not write:

> **Non-STE ERROR:** The database connection failed and the connection pool is exhausted and the health check endpoint is returning 503.

The connection pool exhaustion and the 503 status are consequences of the connection failure, not separate problems. State the root cause first.

### Edge Case 3: Generated or Auto-Formatted Documentation

Tools like Sphinx, JSDoc, Terraform docs, and `swagger-ui` generate documentation from source annotations. These generators may combine parameter descriptions or return value descriptions into single output blocks. When the generated output is not directly authored by a human, relax Rule 5.2 — but prefer annotation formats that enable one-sentence-per-item generation.

For example, prefer this JSDoc annotation style:

```javascript
/**
 * Creates a new user account.
 * @param {string} username - The unique username for the account.
 * @param {string} email - The email address for the account.
 * @returns {User} The newly created user object.
 */
function createUser(username, email) {
  // ...
}
```

Over this:

```javascript
/**
 * Creates a new user account with the given username and email and returns
 * the user object.
 */
function createUser(username, email) {
  // ...
}
```

The first style generates one sentence per parameter automatically. The second style generates a compound sentence that may violate Rule 5.2.

### Edge Case 4: Multi-Step Test Assertions

Test case descriptions and assertion messages often combine multiple conditions. When documenting test cases, describe each assertion in its own sentence. When writing assertion messages, use one message per assertion.

**Non-STE test description:**

```python
def test_login():
    # Test that the endpoint returns 200 and sets the session cookie
    # and redirects to the dashboard.
    ...
```

**STE-Code test description:**

```python
def test_login():
    # This test checks three conditions:
    # (1) The login endpoint returns status code 200.
    # (2) The response sets the session cookie.
    # (3) The response redirects to the dashboard.
    ...
```

Assertion messages, one per condition:

```python
assert response.status_code == 200, "Expected status code 200"
assert "session" in response.cookies, "Expected a session cookie"
assert response.headers["Location"].endswith("/dashboard"), "Expected redirect to dashboard"
```

### Edge Case 5: Console Log Messages During Multi-Step Operations

When a script or CLI tool logs progress during a multi-step operation, each log message should describe one completed step — not what will happen next.

**Non-STE log output:**

```text
INFO: Connecting to the database and running migrations and seeding data...
```

**STE-Code log output:**

```text
INFO: Connecting to the database...
INFO: Database connection established.
INFO: Running migrations...
INFO: Migrations complete (3 applied).
INFO: Seeding data...
INFO: Seed data inserted (150 rows).
```

Each log line reports one action or one result. The reader can identify exactly where a failure occurred.

## Cross-References

This rule interacts with several other STE-Code rules. A violation of Rule 5.2 often signals a violation of one or more of these related rules.

| Rule | Relationship |
|------|-------------|
| **Rule 5.1 — Short Sentences (Max 20 Words)** | When sentences are short, they naturally contain fewer instructions. Splitting a multi-instruction sentence per Rule 5.2 often brings each resulting sentence below the 20-word limit of Rule 5.1. Apply Rule 5.2 first, then check each resulting sentence against Rule 5.1. |
| **Rule 5.3 — Imperative (Command) Form** | Each instruction separated by Rule 5.2 must be in the imperative mood. A sentence split from a compound instruction must still begin with an imperative verb. See Rule 5.3 for verb form requirements. |
| **Rule 1.1 — Use Approved Words** | When you split a sentence into separate instructions, replace unapproved action words (utilize, leverage, employ) with approved alternatives (use). Consult the STE-Code Dictionary for the approved verb list. |
| **Rule 1.12 — Technical Verbs** | Technical verbs (build, deploy, test, lint, clone, commit, push, merge) are allowed as action words in separated instructions. Rule 1.12 confirms that these domain verbs are permitted despite not appearing in the general dictionary. |
| **Rule 1.13 — Do Not Use Technical Verbs as Nouns** | When you split a sentence, check that technical verbs remain verbs. Do not write "Do a build of the project." Write "Build the project." Rule 1.13 reinforces this. |
| **Rule 5.5 — Notes Give Information Only** | Notes (marked with NOTE:) must not contain instructions. If a sentence contains both a note and an instruction, split them: move the instruction to a numbered step and keep only information in the NOTE. |
| **STE-Code Dictionary** | The dictionary defines which action verbs are approved for use in separated instructions. Always consult the dictionary when choosing the verb for each split sentence. |

## Grammar Notes

The original ASD-STE100 Rule 5.2 is grounded in a syntactic principle: an imperative sentence in a technical procedure should have exactly one main verb phrase (predicate) that the reader can map to a single executable action. When a sentence contains multiple predicates joined by coordinating conjunctions ("and", "or") or sequential adverbs ("then", "after that", "subsequently"), the reader must parse a compound instruction structure. This parsing increases cognitive load and introduces ambiguity about the order of operations.

For code documentation, this syntactic principle translates into the following grammatical rules:

### Single Predicate Rule

Each imperative sentence in a procedure must contain exactly one main verb in the imperative mood. The main verb is the first word of the sentence (or follows an adverb like "slowly" or "carefully").

**Correct:** `Install the package.` (one predicate: "Install")
**Incorrect:** `Install the package and configure the settings.` (two predicates: "Install", "configure")

### Simultaneous Action Exception

Two predicates may appear in one sentence joined by "and" when both actions must occur at the same moment and cannot be meaningfully separated. The grammatical test: if you can insert a pause between the actions, they are sequential and must be split.

**Simultaneous (allowed):** `Hold the Shift key and click the Reload button.`
The holding and clicking occur simultaneously — you cannot click the modified reload without holding Shift.

**Sequential (must be split):** `Install the package and run the tests.`
You can install, then pause, then run tests. These are two steps.

### Result Clause Separation

When an action sentence contains a result clause introduced by "until", "so that", "to", or "such that", separate the result into its own sentence. The result clause is not an instruction — it states the expected outcome or stopping condition.

**Before:** `Run the migration until the output shows "Migration complete".`
**After:** `Run the migration. Continue until the output shows "Migration complete".`

**Before:** `Set the timeout to 30 seconds so that the connection does not hang.`
**After:** `Set the timeout to 30 seconds. This prevents the connection from hanging.`

### Compound Objects Are Not Compound Instructions

A sentence may have a compound direct object without violating Rule 5.2, as long as there is only one verb. The verb acts on multiple items in a single action.

**Allowed:** `Remove the log files, cache files, and temporary directories.`
(One verb "Remove", three objects. This is one instruction — remove all of these things.)

**Not allowed:** `Remove the log files and restart the server.`
(Two verbs: "Remove" and "restart". These are two instructions.)

### The "-ing" Form Prohibition

The STE-Code anti-pattern against "-ing" forms as main verbs directly supports Rule 5.2. Present participles and gerunds blur the boundary between actions and descriptions, making it unclear whether a sentence contains one instruction or multiple. When a sentence uses an "-ing" form as a main verb, it often smuggles in additional implied instructions.

**Before:** `After installing the package, configuring the environment, and setting up the database, run the application.`
(Three implied instructions hidden in gerund phrases before the main instruction.)

**After:**
```text
(1) Install the package.
(2) Configure the environment.
(3) Set up the database.
(4) Run the application.
```

### Subordinate Clauses and Instruction Count

A sentence with one main clause and one subordinate clause may still violate Rule 5.2 if the subordinate clause contains an implicit instruction. The test: can the reader execute the main clause instruction without also executing the subordinate clause action? If the subordinate clause describes a precondition that the reader must satisfy, that precondition is an instruction and requires its own step.

**Before:** `Before you run the tests, set the TEST_MODE environment variable to true.`
**After:** `(1) Set the TEST_MODE environment variable to true. (2) Run the tests.`

**Before:** `After the build completes, deploy the artifact to the staging server.`
**After:** `(1) Wait for the build to complete. (2) Deploy the artifact to the staging server.`

## See also

> **See also:** Rule 5.1 — Short Sentences (Max 20 Words)
> **See also:** Rule 5.3 — Imperative (Command) Form
> **See also:** Rule 1.1 — Use Approved Words
> **See also:** Rule 1.12 — Technical Verbs
> **See also:** Rule 1.13 — Do Not Use Technical Verbs as Nouns
> **See also:** Rule 5.5 — Notes Give Information Only

---

<!-- a-sec5-rule5.3.md -->

# Rule 5.3 — Imperative (Command) Form for Instructions

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 5.3
> **Source:** [master.md#sec5-rule5.3](ste-code/grouped/)

## Original Rule

Write instructions in the imperative (command) form.

An instruction tells the reader to do something. Write the verb in the imperative (command) form.

Examples in STE:

Set the switch to ON.
Remove the four bolts.
Increase the pressure to 60 psi.
Inflate the tires.
Install the new O-ring.

The imperative form gives the reader a clear instruction. If you use other types of sentence structure, you can cause ambiguity. Thus, the reader will not know:

- If it is important to do a work step.
- If a different person did the work step.
- If a different person must do the work step in the future.

Examples:

> **Non-STE:** The test can be continued.
>
> **STE:** Continue the test.

> **Non-STE:** Oil and grease are to be removed with a degreasing agent.
>
> **STE:** Remove oil and grease with a degreasing agent.

Do not use the verb "must" before the imperative form, unless the instruction is very important for safety (for example, in a safety instruction) or when you give an important condition.

Example:

| Do not write: | Before you remove the clamp, you must disconnect the hose. |
| --- | --- |
| WRITE: | Before you remove the clamp, disconnect the hose. |
| STE: | WARNING: IF YOU MUST CUT THE WIRE, ALWAYS USE A PROTECTIVE MASK. PIECES OF WIRES CAN CAUSE INJURY. |

## STE-Code Adaptation

In code documentation, instructions that tell the reader to execute a command, edit a file, change a setting, or run a script must use the imperative (command) form. The imperative form gives a direct and unambiguous instruction. Passive constructions, modal verbs, and indirect phrasing create ambiguity about whether the reader needs to act, whether the action has already been completed, or whether someone else will perform it.

Start each procedural instruction with an imperative verb. Common imperative verbs in code documentation include: "run," "set," "open," "save," "install," "configure," "restart," "execute," "copy," "delete," "create," "add," "enter," "select," "click," "type," and "check."

Do not use passive voice, gerunds, or modal verbs (such as "can," "could," "should," "may," or "might") for instructions. Do not use "must" before the imperative form in a standard instruction. Reserve "must" for security warnings, data loss cautions, and conditions that are critical for safety.

### Code-Domain Explanation

This rule applies differently across the documentation types common in software engineering. Each type serves a distinct audience and purpose. The imperative form must adapt while staying unambiguous.

#### README Files

README files mix procedural setup steps with descriptive overview content. The imperative form applies only to the procedural sections: installation, configuration, building from source, and quick-start commands. Descriptive sections such as project goals, architecture summaries, and feature lists can use declarative sentences because they do not instruct the reader to act.

Identify the boundary clearly. Start each procedural step with an imperative verb. Do not nest instructions inside descriptive paragraphs.

Procedural README section (imperative):

```markdown
## Setup

Clone the repository.
Install the dependencies with `npm install`.
Set the `DATABASE_URL` environment variable in `.env`.
Run the development server with `npm run dev`.
```

Descriptive README section (not imperative):

```markdown
## About

This project provides a real-time chat server with WebSocket support. The
server handles up to 10,000 concurrent connections on commodity hardware.
```

#### API Documentation

API reference pages document endpoint behavior, parameter schemas, and response formats. Most API documentation is descriptive. The imperative form applies only to setup instructions, authentication walkthroughs, and "getting started" sections.

Endpoint descriptions can use the third person ("Returns a list of users") because they describe system behavior, not reader action. Example request blocks and code snippets are inherently imperative because they show the reader what to type.

Do not mix imperative instructions with endpoint descriptions in the same paragraph.

> **Non-STE:** You can authenticate by sending a POST request to `/auth/login` with your credentials, and you should include the returned token in the Authorization header.
>
> **STE (API doc):** Send a POST request to `/auth/login` with your credentials. Include the returned token in the `Authorization` header.

```http
POST /auth/login HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "username": "dev",
  "password": "s3cret"
}

HTTP/1.1 200 OK
{
  "token": "eyJhbGciOi..."
}

// STE: include the returned token in the Authorization header
GET /users/me HTTP/1.1
Authorization: Bearer eyJhbGciOi...
```

#### Docstrings and Inline Comments

Function and method docstrings describe what the code does, not what the reader must do. Use descriptive sentences in docstrings. The imperative form in a docstring can confuse the reader because it mimics a command to the function itself.

Exception: Shell script headers and Makefile targets that document usage can use the imperative form because the reader executes them directly.

> **Non-STE:** Call this function with a user ID and it will return the profile data.
>
> **STE (Python docstring):** This function returns the profile data for the given user ID.

```python
def get_profile(user_id: int) -> Profile:
    """Return the profile data for the given user ID.

    Query the database for the row that matches `user_id` and return
    a Profile object. Raise ValueError if the user does not exist.
    """
    return db.query(Profile).filter_by(id=user_id).one()
```

> **STE (Makefile target comment):** Build the production Docker image.

```makefile
# Build the production Docker image.
build:
	docker build -t myapp:latest --target production .
```

#### Commit Messages

Commit messages describe completed actions. Use the imperative form to state what the commit does when applied. This convention matches Git's own auto-generated messages ("Merge branch," "Revert commit"). Write the subject line as if it completes the sentence: "If applied, this commit will..."

> **Non-STE:** Fixed the race condition in the connection pool.
>
> **STE:** Fix the race condition in the connection pool.

> **Non-STE:** Added validation for empty form submissions.
>
> **STE:** Add validation for empty form submissions.

```text
# Non-STE commit log
* Fixed the race condition in the connection pool
* Added validation for empty form submissions

# STE commit log (git log --oneline)
a1b2c3d Fix the race condition in the connection pool
e4f5g6h Add validation for empty form submissions
```

NOTE: Commit bodies can use descriptive sentences to explain the rationale, context, and impact. The imperative form applies primarily to the subject line.

```text
Fix the race condition in the connection pool

The pool returned the same connection to two threads under load.
Add a lock around the checkout path so each thread gets a unique
connection. The retry test in tests/test_pool.py now passes.
```

#### Error Messages

Error messages report what went wrong to the user. Do not use the imperative form in error messages unless you also tell the user how to recover. An error message that says "Set the port number" without identifying the failure is confusing.

A well-formed error message tells the user what happened and then gives a recovery instruction. Separate the error description from the recovery instruction with a period or a newline.

> **Non-STE:** Port is already in use.
>
> **STE (error message):** The port 8080 is already in use. Set a different port with the `--port` option.

> **Non-STE:** Invalid configuration file. Check the schema.
>
> **STE (error message):** The configuration file failed schema validation. Check the `config.schema.json` file for required fields.

```python
# Non-STE: raises a bare, unrecoverable string
raise RuntimeError("Port is already in use")

# STE: describes the failure, then gives a recovery instruction
raise RuntimeError(
    "The port 8080 is already in use. "
    "Set a different port with the --port option."
)

# Non-STE
raise ConfigError("Invalid configuration file. Check the schema.")

# STE
raise ConfigError(
    "The configuration file failed schema validation. "
    "Check the config.schema.json file for required fields."
)
```

### Grammar Notes

The original ASD-STE100 justifies the imperative form with grammatical precision. This section adapts that reasoning for code documentation grammar.

#### Subject Omission

The English imperative mood omits the subject "you." The implied subject is always the reader. This omission removes ambiguity: the reader knows the instruction is directed at them, not at a third party or at the system.

Passive constructions hide the agent entirely. The sentence "The file is saved" does not specify who performs the action. The reader cannot determine if the system saves the file automatically or if the reader must invoke a save command.

Gerunds ("Saving the file...," "Running the tests...") function as nouns. They describe an action as a concept, not as a directive. A reader who sees "Saving the configuration before deployment" cannot tell if this is a prerequisite, a step they must perform, or a description of system behavior.

#### Modal Verb Elimination

Modal verbs ("can," "could," "should," "may," "might," "would") express possibility, permission, or recommendation. In instructions, they introduce uncertainty. The reader must decide whether the action is optional, recommended, or required.

"You can set the timeout to 30 seconds" allows the reader to interpret the action as optional even when it is not. "Set the timeout to 30 seconds" gives no room for that misinterpretation.

The verb "must" expresses necessity. In standard instructions, "must" is redundant because the imperative form already conveys necessity. Reserve "must" for WARNING and CAUTION blocks where the consequence of non-compliance is severe.

#### Tense Consistency

The imperative form uses the base verb form. It does not inflect for tense, number, or person. This consistency simplifies translation, machine processing, and reading by non-native English speakers. A reader never needs to parse subject-verb agreement or tense from an imperative instruction.

#### Coordination with Rule 5.4

Rule 5.4 allows a descriptive statement before an imperative command when context is necessary. The descriptive statement sets the stage. The imperative command follows and delivers the instruction. This two-part structure keeps descriptive and imperative content separate. The reader processes the context, then acts on the command.

Example (descriptive statement + imperative command):

The Docker daemon must be running. Build the image with `docker build`.

The first sentence is descriptive (not imperative). The second sentence is imperative. The separation is clear because each sentence has a different grammatical role.

```bash
# Descriptive: states a required condition.
# The Docker daemon must be running.
# Imperative: tells the reader the action to take.
docker build -t myapp:dev .
```

### Paradigm-Specific Guidance

Different programming paradigms produce different types of code documentation. The imperative form adapts to each paradigm while staying consistent with Rule 5.3.

#### Object-Oriented (Java, C++, C#, Python Classes)

Class documentation, constructor guides, and factory method descriptions often document instantiation patterns. The imperative form applies to setup and configuration instructions. Descriptive forms apply to class invariants, inheritance hierarchies, and design rationale.

> **Non-STE:** An instance of the DatabaseConnection class can be created by calling the static factory method `create`, and you should pass a valid connection string.
>
> **STE (OOP doc):** Create an instance of the `DatabaseConnection` class with the static factory method `create`. Pass a valid connection string.

```python
# STE (docstring usage section)
# Create an instance of the DatabaseConnection class with the static
# factory method create. Pass a valid connection string:
conn = DatabaseConnection.create("postgresql://user:pass@localhost:5432/app")
```

#### Functional (Haskell, Elixir, Clojure, Rust)

Functional documentation emphasizes pure functions, data flow, and immutability. The imperative form applies to project setup, build tool usage, and REPL interactions. Function descriptions use declarative forms because they describe transformations, not commands to the reader.

> **Non-STE:** You should apply `map` to transform the list and then you can pipe the result into `filter`.
>
> **STE (Functional doc):** Apply `map` to transform the list. Then, pipe the result into `filter`.

```haskell
-- STE (REPL walkthrough)
-- Apply map to transform the list. Then, pipe the result into filter.
-- λ> map (*2) [1,2,3]
-- [2,4,6]
-- λ> map (*2) [1,2,3] |> filter (> 3)
-- [4,6]
```

NOTE: When documenting a function that the reader must call, the imperative form is correct. When documenting what a function does internally, the descriptive form is correct.

#### Procedural (C, Go, Bash)

Procedural code often appears in scripts, system tools, and command-line utilities. The documentation for these tools is inherently instructional. The imperative form dominates: build steps, compile flags, linking instructions, and runtime configuration are all actions the reader performs.

> **Non-STE:** The binary can be compiled with `gcc -O2 -Wall main.c -o tool` and then you are to place it in `/usr/local/bin`.
>
> **STE (Procedural doc):** Compile the binary with `gcc -O2 -Wall main.c -o tool`. Place the binary in `/usr/local/bin`.

```bash
# STE (install section of a project README)
gcc -O2 -Wall main.c -o tool
sudo cp tool /usr/local/bin/tool
```

#### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state, not step-by-step procedures. Schema references, resource definitions, and query syntax are descriptive. The imperative form applies only to the tooling that applies the declarative configuration: CLI commands, pipeline steps, and operator workflows.

> **Non-STE:** The deployment can be applied with `kubectl apply -f deployment.yaml` and you should verify the pods are running afterward.
>
> **STE (Declarative doc):** Apply the deployment with `kubectl apply -f deployment.yaml`. Check that the pods are running.

```yaml
# deployment.yaml — declarative desired state (descriptive, not imperative)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
```

```bash
# STE (operator workflow that applies the state)
kubectl apply -f deployment.yaml
kubectl get pods -l app=web
```

#### Systems (Rust Ownership, C Memory Management)

Systems documentation explains resource lifetimes, ownership models, and memory safety invariants. These are inherently descriptive because they explain constraints, not actions. The imperative form appears in "how to comply" sections: how to structure code to satisfy the borrow checker, how to free memory correctly, or how to use unsafe blocks safely.

> **Non-STE:** The memory should be freed with `free()` after the pointer is no longer needed, and you can use `valgrind` to check for leaks.
>
> **STE (Systems doc):** Free the memory with `free()` when the pointer is no longer needed. Use `valgrind` to check for leaks.

```c
// STE (how-to-comply comment)
// Free the memory with free() when the pointer is no longer needed.
// Use valgrind to check for leaks.
char *buf = malloc(1024);
/* ... use buf ... */
free(buf);
buf = NULL;
```

### Core Examples

> *Adapted from spec pair:* Non-STE: "The test can be continued."  |  STE: "Continue the test."
> *Adapted from spec pair:* Non-STE: "Oil and grease are to be removed with a degreasing agent."  |  STE: "Remove oil and grease with a degreasing agent."
> *Adapted from spec pair:* Non-STE: "Before you remove the clamp, you must disconnect the hose."  |  STE: "Before you remove the clamp, disconnect the hose."

Imperative form in code documentation procedures:

Set the environment variable to the production value.
Run the database migration command.
Install the required dependencies.
Save the configuration file.
Restart the application server.

> **Non-STE:** The unit tests can be executed with the command `npm test`.
>
> **STE:** Run the unit tests with the command `npm test`.
>
> *Adapted from spec pair: "The test can be continued." → "Continue the test."*

```json
// Non-STE: a docs sentence hides the agent and the obligation
{ "note": "The unit tests can be executed with the command npm test." }

// STE: a direct, runnable instruction
// Run the unit tests with the command npm test.
//   $ npm test
```

> **Non-STE:** The old log files are to be removed before the new deployment.
>
> **STE:** Remove the old log files before the new deployment.
>
> *Source pairing: a passive "are to be" construction becomes a direct imperative — follows the same principle as the original STE example in Rule 5.3.*

```bash
# Non-STE (cron comment states a duty, not an action)
# The old log files are to be removed before the new deployment.

# STE (deployment script step)
rm -f /var/log/app/*.log.old
```

> **Non-STE:** The configuration file should be validated against the schema before the application is started.
>
> **STE:** Check the configuration file against the schema before you start the application.
>
> *Adapted from spec: modal verb guidance — replace "should," "can," "could," "may," "might" with the direct imperative form.*

```bash
# Non-STE
# The configuration file should be validated against the schema before the application is started.

# STE
python -m app.validate --schema config.schema.json config.yaml
./start-app.sh
```

> **Non-STE:** The SSL certificate must be renewed and then the web server must be restarted to apply the changes.
>
> **STE:** Renew the SSL certificate. Then, restart the web server to apply the changes.
>
> *Adapted from spec: "must" guidance — do not use "must" before the imperative form in standard instructions.*

(No "must" is necessary because certificate renewal is a standard procedure, not a safety-critical instruction.)

```bash
# Non-STE
# The SSL certificate must be renewed and then the web server must be restarted to apply the changes.

# STE
certbot renew --webroot -w /var/www/html
systemctl restart nginx
```

> **Non-STE:** It is recommended that you create a backup of the database before running the migration script.
>
> **STE:** Create a backup of the database before you run the migration script.
>
> *Adapted from spec: indirect phrasing guidance — replace "it is recommended that" with the direct imperative form.*

(Do not use "it is recommended that." Give the instruction directly.)

```bash
# Non-STE
# It is recommended that you create a backup of the database before running the migration script.

# STE
pg_dump app > backup-$(date +%F).sql
alembic upgrade head
```

| Do not write: | Before you delete the branch, you must push all local commits to the remote repository. |
| --- | --- |
| WRITE: | Before you delete the branch, push all local commits to the remote repository. |

> *Source pairing: drop "must" before a standard imperative — follows the same principle as the original STE example in Rule 5.3.*

> **WARNING:** IF YOU MUST STORE CREDENTIALS IN THE CONFIGURATION FILE, ALWAYS USE AN ENCRYPTED SECRETS MANAGER. PLAIN-TEXT CREDENTIALS CAN CAUSE SECURITY BREACHES.
>
> *Source pairing: reserve "must" for a security-critical condition — follows the same principle as the original STE example in Rule 5.3.*

("Must" is correct here because the instruction is critical for security. The warning format signals the importance to the reader.)

```yaml
# Non-STE: plain-text secret in a config file
database:
  password: "s3cret"

# STE: reference an encrypted secrets manager instead
database:
  password: "${vault:app/database#password}"
```

### Extended Examples

The examples below address common violations found in real code documentation. Each pair shows a non-compliant version, the STE-Code compliant version, the principle applied, and a brief explanation.

#### Example 1: Gerund as Instruction (Docker Documentation)

> **Non-STE:** Building the image with `--no-cache` to ensure a clean build.
>
> **STE:** Build the image with `--no-cache` to make sure that the build is clean.
>
> **Principle:** Rule 1.4 (use only approved verb forms). The gerund "Building" functions as a noun phrase header, not as a command. Replace it with the base imperative form "Build." Also replace "ensure" with the approved synonym "make sure" (Rule 1.1, Rule 1.3).

```dockerfile
# Non-STE (comment header reads like a status, not an action)
# Building the image with --no-cache to ensure a clean build.
#   docker build --no-cache -t myapp .

# STE (direct command the reader runs)
# Build the image with --no-cache to make sure that the build is clean.
#   docker build --no-cache -t myapp .
```

#### Example 2: Passive Voice in a Procedural Step (CI/CD Pipeline Docs)

> **Non-STE:** The test suite is executed automatically after each push to the main branch. The results are posted to the Slack channel.
>
> **STE:** The CI pipeline runs the test suite after each push to the main branch. It posts the results to the Slack channel. To run the tests locally, run `npm test`.
>
> **Principle:** Rule 5.3 (imperative form). The original uses passive voice ("is executed," "are posted") which describes system behavior. The rewritten version separates system description from reader instruction. The descriptive sentences explain what the system does. The imperative sentence tells the reader what to do.

```yaml
# .github/workflows/ci.yml — descriptive of system behavior
# The CI pipeline runs the test suite after each push to the main branch.
# It posts the results to the Slack channel.
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

# STE (local runbook for the reader)
# To run the tests locally, run npm test.
#   $ npm test
```

#### Example 3: Multiple Modal Verbs in One Paragraph (API Quickstart)

> **Non-STE:** You should first generate an API key from the dashboard. Then you can set it in the environment as `API_KEY`. You may also want to configure the rate limit, which can be done by editing the `config.yaml` file.
>
> **STE:** Generate an API key from the dashboard. Set the key in the environment as `API_KEY`. To configure the rate limit, edit the `config.yaml` file.
>
> **Principle:** Rule 5.3 (imperative form) and Rule 1.2 (use words only as their specified part of speech). The original stacks "should," "can," "may," and "can" in rapid succession. Each modal verb introduces a different level of obligation. The reader cannot distinguish required from optional. The STE version uses three direct imperatives.

```bash
# STE (quickstart script the reader copies)
export API_KEY=$(curl -s -X POST https://api.example.com/keys \
  -H "Authorization: Bearer $DASHBOARD_TOKEN" | jq -r .key)
echo "api_key: $API_KEY" >> config.yaml
$EDITOR config.yaml   # set rate_limit under the client section
```

#### Example 4: "Must" Misuse in Standard Procedure (Database Migration)

> **Non-STE:** Before you deploy to production, you must run the migration script, you must back up the database, and you must notify the on-call engineer.
>
> **STE:** Before you deploy to production, run the migration script. Back up the database. Notify the on-call engineer.
>
> **Principle:** Rule 5.3 ("must" restriction). The original uses "must" three times for a standard deployment checklist. None of these steps is a safety-critical condition. The imperative form alone conveys the necessity.

```bash
# STE (deploy checklist)
# Before you deploy to production:
#   run the migration script
alembic upgrade head
#   back up the database
pg_dump app > pre-deploy-$(date +%F).sql
#   notify the on-call engineer
./notify oncall "Deploying app v1.4.2 to production"
```

#### Example 5: Indirect Phrasing in README (Open-Source Project)

> **Non-STE:** It is suggested that contributors run the linter before submitting a pull request. It is also helpful if you squash your commits into a single change.
>
> **STE:** Run the linter before you submit a pull request. Squash your commits into a single change.
>
> **Principle:** Rule 5.3 (indirect phrasing avoidance) and Rule 1.1 (use approved words). The original uses "It is suggested that" and "It is also helpful if" as hedging language. The STE version gives direct instructions without qualifiers.

```markdown
## Contributing

Run the linter before you submit a pull request.

    pre-commit run --all-files

Squash your commits into a single change.

    git rebase -i main
```

#### Example 6: Conditional Imperative with "Must" (Security-Critical Context)

> **Non-STE:** When handling user passwords, you should hash them with bcrypt and you must never store them in plain text.
>
> **STE:** **WARNING:** IF YOU MUST STORE USER PASSWORDS, ALWAYS HASH THEM WITH BCRYPT. DO NOT STORE PASSWORDS IN PLAIN TEXT. PLAIN-TEXT PASSWORDS CAN CAUSE DATA BREACHES.
>
> **Principle:** Rule 5.3 ("must" reserved for safety/security) and Rule 7.1 (risk level identification). The original mixes a weak recommendation ("should") with a critical prohibition ("must never"). The STE version elevates the entire paragraph to a WARNING block with the approved conditional "must" and a clear consequence statement.

```python
# Non-STE
# When handling user passwords, you should hash them with bcrypt
# and you must never store them in plain text.
import hashlib
stored = hashlib.md5(password.encode()).hexdigest()  # wrong: unsalted, fast hash

# STE
# WARNING: IF YOU MUST STORE USER PASSWORDS, ALWAYS HASH THEM WITH BCRYPT.
# DO NOT STORE PASSWORDS IN PLAIN TEXT. PLAIN-TEXT PASSWORDS CAN CAUSE DATA BREACHES.
import bcrypt
stored = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### Edge Cases

Real-world code documentation presents situations where the rule's application requires nuance. The scenarios below describe edge cases and their resolutions.

#### Edge Case 1: Framework Name That Is Also a Verb

Some framework and tool names are identical to English verbs: "React," "Spring," "Go," "Build" (the Bazel tool), "Make." When a framework name appears at the start of a sentence, the reader can mistake it for an imperative command.

Resolution: Restructure the sentence so the framework name does not start the sentence. Use the full product name or prefix it with an article.

> **Acceptable:** Use React to build the user interface. (Imperative verb "Use" starts the sentence. "React" is the object.)
> **Acceptable:** The React library provides a component model for the user interface. (Descriptive. "React" is preceded by an article.)
> **Avoid:** React to state changes with hooks. (Ambiguous. "React" could be read as an imperative verb or the framework name.)

```jsx
// STE (instruction the reader follows)
// Use React to build the user interface.
import { useState } from "react";
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

#### Edge Case 2: Generated Code and Tool Output

Auto-generated documentation, such as `--help` output from CLI tools, changelogs produced by release automation, and API reference pages generated from OpenAPI specs, can contain non-imperative constructions. The STE-Code rule applies to human-authored content. Generated content should follow the rule where the generation template allows.

Resolution: Audit the generation templates, not the generated output. If a CLI tool's `--help` text uses passive voice, fix the source code that produces the help text. If a changelog generator uses "Added feature X," adjust the generator's template to use "Add feature X."

```python
# Non-STE: --help text the tool prints
parser.add_argument("--out", help="The output file is written here")

# STE: direct, imperative help text
parser.add_argument("--out", help="Write the output to this file")
```

```text
# Non-STE changelog template
{{ version }}: Added support for OAuth2

# STE changelog template
{{ version }}: Add support for OAuth2
```

#### Edge Case 3: Code Keywords That Conflict with the Rule

Some programming language keywords are modal verbs in English: `try`, `catch`, `finally`, `throw`, `async`, `await`, `yield`, `require`. When documenting code snippets that include these keywords, the surrounding prose must clearly separate the code token from the instruction.

Resolution: Use code formatting (backticks) for keywords. Do not place a code keyword at the start of an imperative sentence unless it is the instruction verb.

> **Non-STE:** `await` the promise before you access the result.
>
> **STE:** Use `await` on the promise before you access the result.

```javascript
// STE
// Use await on the promise before you access the result.
const result = await fetchUser(userId);
show(result);
```

#### Edge Case 4: Release Notes and Changelogs

Release notes document what changed between versions. They are neither purely descriptive nor purely instructional. The reader consults release notes to understand impact, not to perform steps (unless upgrade instructions are included).

Resolution: Use the imperative form for upgrade instructions and migration steps. Use the past tense or present perfect for feature descriptions and bug fixes. The convention "If applied, this release will..." mirrors the commit message convention.

> **STE (upgrade instruction):** Run the database migration for schema version 12.
> **STE (feature description):** This release adds support for PostgreSQL 16.

```text
# STE (release note)
## 2.3.0
- Add support for PostgreSQL 16.
- Fix a memory leak in the background worker.
- Run the database migration for schema version 12 before you deploy.
```

#### Edge Case 5: Interactive Tutorials and Walkthroughs

Interactive tutorials blend instructional prose with expected output. The instructional steps use the imperative form. The expected output, code blocks, and system responses use descriptive forms. A tutorial that uses the imperative form for all text confuses the reader about what they type and what the system displays.

Resolution: Label each block clearly ("Run this command," "You will see output like this," "The system responds with"). Keep the imperative form in the instructional labels and the step descriptions. Use descriptive forms for the system response annotations.

```text
Run this command to start the server:

    python -m app.server

You will see output like this:

    INFO  Starting server on http://127.0.0.1:8000

The system responds with a 200 status code when the health check passes.
```

### Cross-References

- **Rule 1.1** — Use approved words from the STE-Code dictionary. Many modal verbs ("should," "could," "might") are not in the approved dictionary and violate both Rule 1.1 and Rule 5.3.
- **Rule 1.2** — Use words only as their specified part of speech. Gerunds used as imperative substitutes violate Rule 1.2 because the gerund is a noun form, not a verb form.
- **Rule 1.4** — Use only approved verb forms and adjective forms. The imperative mood uses the base verb form, which is the approved form for all verbs in the STE-Code dictionary.
- **Rule 1.7** — Do not use technical nouns as verbs. An imperative instruction must start with a verb. If a technical noun starts the sentence, it violates both Rule 1.7 and Rule 5.3.
- **Rule 5.4** — Descriptive Statement Before the Command. When context must precede an instruction, use a descriptive statement followed by an imperative command. This rule defines the boundary between descriptive and imperative content.
- **Rule 7.1** — Use an Applicable Word to Identify the Level of Risk. WARNING and CAUTION blocks are the only contexts where "must" is permitted before an imperative verb.
- **Rule 7.2** — Start a Safety Instruction with a Clear and Accurate Command or Condition. Safety instructions combine a conditional clause with an imperative command. The "must" in the conditional clause is governed by Rule 5.3's safety exception.
- **STE-Code Dictionary** — See the canonical synonym table for approved imperative verbs. Prefer "use" over "utilize," "start" over "initiate," "stop" over "terminate," "check" over "verify," "set" over "configure."

> **See also:** Rule 5.4 — Descriptive Statement Before the Command; Rule 7.1 — Use an Applicable Word to Identify the Level of Risk; Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition

---

<!-- a-sec5-rule5.4.md -->

# Rule 5.4 — Descriptive Statement Before the Command

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 5.4
> **Source:** [master.md#sec5-rule5.4](ste-code/grouped/)

## Original Rule

When there is a condition that the reader must know about first, start the instruction with a descriptive statement. Then, divide that descriptive statement from the command with a comma.

If a special condition is necessary for a work step, the reader must know the condition first. Write the condition first in the sentence, and then use a comma to show the end of the condition, and the start of the instruction.

Examples:

| Do not write: | Before you remove the clamp, you must disconnect the hose. |
| --- | --- |
| WRITE: | Before you remove the clamp, disconnect the hose. |

WRITE: If the Constant Speed Drive (CSD) does not operate correctly, disconnect it from the gearbox.

The comma is important. Be careful when you use it because the position of the comma can change the meaning of your sentence.

| STE: | WARNING: IF YOU MUST CUT THE WIRE, ALWAYS USE A PROTECTIVE MASK. PIECES OF WIRES CAN CAUSE INJURY. |
| --- | --- |

If the Constant Speed Drive (CSD) does not operate, correctly disconnect it from the gearbox.

The two sentences in the examples are correct, but their meanings are different. In the first sentence, the comma after "correctly" shows that the adverb modifies the verb "operate." In the second sentence, the comma after "operate" shows that the adverb modifies the verb "disconnect."

## STE-Code Adaptation

In code documentation, many procedural steps have conditions that the reader must know before they act. Examples include checking that a service is running before stopping it, verifying that a file exists before editing it, or confirming that a previous step completed successfully before proceeding.

Write the condition as a descriptive statement at the start of the sentence, followed by a comma, and then the instruction in the imperative form. This structure ensures the reader evaluates the condition before executing the command.

The comma is critical for correct meaning. The position of the comma determines which part of the sentence an adverb or adverbial phrase modifies. Place the comma immediately after the condition clause, before the instruction.

### Code-Domain Explanation

Rule 5.4 applies across all code documentation types. The condition-before-command structure is universal, but its application varies by document type. Each domain demands the reader to evaluate a condition before they act, and the comma is the syntactic marker that enforces that evaluation order.

#### README Files

README files contain installation steps, build instructions, and environment setup procedures. Many of these steps depend on prior conditions. A reader who misses a condition can break their local environment or waste time on a failing build.

Place the condition clause first. Use a comma to separate it from the command. Do not bury the condition in a dependent clause after the command. The reader must not start the action until they have processed the condition.

> **Non-STE:** Run the database migration script after you set the `DATABASE_URL` environment variable to your production database connection string and confirmed that the database server is accepting connections.
>
> **STE:** After you set the `DATABASE_URL` environment variable, run the database migration script.
>
> *Principle applied: P8 (standard technical nouns), P1 (approved words). The condition "After you set..." comes first, separated by a comma from the command "run." The original buried the condition after the instruction, violating the reader's need to know the prerequisite first.*

For multi-step README procedures, do not combine several conditions into one sentence. Write each condition-command pair as a separate step.

> **Non-STE:** First you need to have Node.js version 18 or higher installed then run `npm install` and after all dependencies finish downloading if there are no errors you can run `npm run build` to compile the TypeScript source files.
>
> **STE:** Make sure that Node.js version 18 or higher is installed. Run `npm install`. After the dependencies install without errors, run `npm run build`.
>
> *Principle applied: P1, P8. One condition-command pair per step. The comma separates "After the dependencies install without errors" from "run." Each step is self-contained.*

#### API Documentation

API reference documentation describes endpoints, parameters, and return values. Procedural API docs (quickstart guides, integration walkthroughs) use condition-before-command to protect the reader from making requests that will fail.

> **Non-STE:** You can call the `/users` endpoint to retrieve a list of users but only after you have obtained a valid OAuth2 access token from the `/auth/token` endpoint and included it in the Authorization header of your request.
>
> **STE:** After you get a valid OAuth2 access token from the `/auth/token` endpoint, call the `/users` endpoint. Include the token in the `Authorization` header.
>
> *Principle applied: P2 (words only as specified part of speech), P1. "Get" replaces "obtain." The condition "After you get a valid OAuth2 access token" precedes the command. The supplemental instruction is a separate sentence.*

For error response documentation, state the condition that triggers the error before describing the response.

> **Non-STE:** The API returns a 429 Too Many Requests status code with a Retry-After header indicating how long to wait before making another request if the client exceeds the rate limit of 100 requests per minute.
>
> **STE:** If the client sends more than 100 requests per minute, the API returns a `429 Too Many Requests` status code. The response includes a `Retry-After` header that shows the wait time.
>
> *Principle applied: P1, P8. The condition clause "If the client sends more than 100 requests per minute" comes first. The comma separates it from the main clause. "Shows" replaces "indicating."*

#### Docstrings and Inline Comments

Docstrings describe function behavior, parameters, and return values. When a function has preconditions, the docstring must state them before describing the action. The condition-before-command pattern in docstrings maps to precondition-before-behavior.

> **Non-STE:** Deletes the specified file from the filesystem. A FileNotFoundError will be raised if the file does not exist at the given path.
>
> **STE (Python docstring):** Remove the file at `path` from the filesystem. If the file does not exist, this function raises `FileNotFoundError`.
>
> *Principle applied: P1 ("remove" replaces "deletes"), P8 (Python exception name as technical noun). The behavior comes first as a command. The precondition "If the file does not exist" comes before the result clause.*

> **Non-STE:** Processes the items in the provided array by applying the transformer function to each one and then collecting the results into a new array, but if the array is null or undefined it'll return an empty array right away.
>
> **STE (JavaScript JSDoc):** Apply `transformer` to each item in `items`. Return a new array with the results. If `items` is `null` or `undefined`, return an empty array.
>
> *Principle applied: P1, P8. Three separate sentences. The final sentence uses condition-before-command: "If `items` is `null` or `undefined`, return an empty array."*

#### Commit Messages

Commit messages describe what a change does and why. The condition-before-command pattern in commit messages takes the form of context-before-action. State the problem or context first, then describe the fix.

> **Non-STE:** fix race condition in connection pool when max connections reached by adding mutex lock around pool access
>
> **STE:** When the connection pool reaches its maximum capacity, add a mutex lock around pool access to prevent a race condition.
>
> *Principle applied: P1, P8. The condition "When the connection pool reaches its maximum capacity" comes first, separated by a comma from the action. The commit message reads as a complete sentence.*

> **Non-STE:** handle edge case where user session expires during long-running file upload by automatically refreshing the token before the upload completes
>
> **STE:** If a user session expires during a file upload, refresh the token automatically before the upload completes.
>
> *Principle applied: P1. Condition first ("If a user session expires"), comma, then command ("refresh the token automatically"). The adverb "automatically" modifies "refresh."*

#### Error Messages

Error messages must tell the user what went wrong and what to do. The condition-before-command pattern in error messages takes the form of problem-before-resolution. State what condition failed, then give the corrective action.

> **Non-STE:** The configuration file couldn't be parsed because it contains invalid YAML syntax on line 42 so please fix the syntax error and try running the application again.
>
> **STE:** The configuration file has invalid YAML syntax on line 42. Fix the syntax error, then run the application again.
>
> *Principle applied: P1, P2. Two sentences. The first states the condition (the problem). The second gives the command. No comma needed between sentences, but within the second sentence, the implied condition "after you fix" is expressed through the sequencing word "then."*

> **Non-STE:** Unable to connect to the database server at host db.example.com on port 5432 after trying for 30 seconds — verify that the server is running and that your network firewall allows outbound connections on this port.
>
> **STE:** Cannot connect to the database server at `db.example.com:5432`. If the server is not running, start it. If a firewall blocks the connection, open port 5432.
>
> *Principle applied: P1 ("cannot" instead of "unable to"), P8 (host and port as technical nouns). Each corrective action is a separate condition-command pair: "If the server is not running, start it."*

### Examples

> *Adapted from spec pair:* Non-STE: `Before you remove the clamp, you must disconnect the hose.`  |  STE: `Before you remove the clamp, disconnect the hose.`

> **Non-STE:** Before you change the database schema you must shut down the application server and stop all background worker processes that are connected to the database.
>
> **STE:** Before you change the database schema, shut down the application server and stop all background worker processes that connect to the database.
>
> *Source pairing: condition first, comma, then command — follows the same principle as the original STE example in Rule 5.4.*

(The comma separates the condition from the instruction. The reader evaluates the condition first.)

> **Non-STE:** You should disconnect the active client sessions first if the connection pool has reached its maximum capacity and new connections are being rejected by the server.
>
> **STE:** If the connection pool has reached its maximum capacity, disconnect the active client sessions.
>
> *Source pairing: condition first, comma, then command — follows the same principle as the original STE example in Rule 5.4.*

(The condition comes first. The comma separates the descriptive "if" clause from the command "disconnect.")

| Do not write: | When the configuration file fails to load the application uses the default settings from the built-in configuration provider. |
| --- | --- |
| WRITE: | When the configuration file fails to load, the application uses the default settings from the built-in configuration provider. |

> *Adapted from spec pair:* Non-STE: `When the configuration file fails to load the application uses the default settings...`  |  STE: `When the configuration file fails to load, the application uses the default settings...` (comma placement guidance — the comma shows where the condition ends and the main clause begins.)

(The comma after "load" is necessary to show where the condition ends and the main clause begins.)

> **Non-STE:** Run the cleanup script to remove temporary build artifacts after the test suite completes successfully and all test results have been written to the output directory.
>
> **STE:** After the test suite completes successfully, run the cleanup script to remove temporary build artifacts.
>
> *Adapted from spec: condition-before-command principle — write the condition first, then the instruction.*

(The condition "after the test suite completes successfully" comes first, separated by a comma from the instruction.)

Comma placement changes meaning:

> If the service does not start, automatically restart it with the recovery script.
> (The comma after "start" shows that "automatically" modifies the verb "restart." The restart happens automatically.)

> If the service does not start automatically, restart it with the recovery script.
> (The comma after "automatically" shows that "automatically" modifies the verb "start." The reader must restart the service manually if it does not start automatically.)

> *Source pairing: comma placement changes which verb an adverb modifies — follows the same principle as the original STE example in Rule 5.4.*

> **WARNING:** IF YOU MUST DELETE THE ENCRYPTION KEY, ALWAYS VERIFY THAT NO ACTIVE SESSIONS USE THE KEY. DELETING AN ACTIVE ENCRYPTION KEY CAN CAUSE PERMANENT DATA LOSS.
>
> *Source pairing: condition first in a safety instruction — follows the same principle as the original STE example in Rule 5.4.*

(The condition "IF YOU MUST DELETE THE ENCRYPTION KEY" comes first, followed by a comma and the safety instruction.)

### Extended Examples

Each example below shows a real code documentation scenario. The Non-STE version violates Rule 5.4. The STE-Code version applies the condition-before-command pattern with correct comma placement.

#### Example 1 — CI/CD Pipeline Configuration

> **Non-STE:** The deployment pipeline pushes the Docker image to the container registry after it runs all the unit tests, integration tests, and the security vulnerability scan with zero failures and all quality gates have passed.
>
> **STE:** After all tests pass and the security scan finds no vulnerabilities, the deployment pipeline pushes the Docker image to the container registry.
>
> *Principle applied: P1 ("push" instead of "pushes"), P5 (Docker as technical noun), P8. The condition "After all tests pass and the security scan finds no vulnerabilities" comes first. The comma separates the condition from the main clause "the deployment pipeline pushes." The original buried the condition after the action.*

Full configuration that the documentation describes:

```yaml
# .github/workflows/deploy.yml
name: deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test                 # unit + integration tests
      - run: npm run scan             # security vulnerability scan
      - name: push image
        run: docker push registry.example.com/app:${{ github.sha }}
```

The STE version of the surrounding README instruction reads: "After all tests pass and the security scan finds no vulnerabilities, the deployment pipeline pushes the Docker image to the container registry."

#### Example 2 — Database Migration Rollback

> **Non-STE:** You can manually revert the migration by executing the down script but first make sure that no other instances of the application are currently connected to the database because concurrent schema changes will corrupt the migration history table.
>
> **STE:** Before you run the down script, make sure that no other application instances connect to the database. Then, run the down script to revert the migration.
>
> *Principle applied: P1 ("run" instead of "execute," "make sure" instead of "verify that" per synonym table context), P5 (down script as technical noun). The condition "Before you run the down script" comes first. Two separate sentences keep each step clear.*

Supporting migration files:

```sql
-- migrations/0042_add_audit_log.up.sql
CREATE TABLE audit_log (id BIGSERIAL PRIMARY KEY, event TEXT NOT NULL);

-- migrations/0042_add_audit_log.down.sql
DROP TABLE audit_log;
```

```bash
# Run the rollback. The STE instruction applies:
# Before you run the down script, make sure that no other application instances connect to the database.
psql "$DATABASE_URL" -f migrations/0042_add_audit_log.down.sql
```

NOTE: Concurrent schema changes can corrupt the migration history table.

#### Example 3 — Terraform Infrastructure as Code

> **Non-STE:** The apply command will provision all the resources defined in your configuration files in the correct dependency order but you should always run terraform plan first to preview the changes and make sure that no unexpected resource destruction will happen.
>
> **STE:** Before you run `terraform apply`, run `terraform plan`. Check the plan output for unexpected resource destruction. If the plan is correct, run `terraform apply`.
>
> *Principle applied: P2, P5 (terraform commands as technical nouns), P8. Three separate steps. Each condition-command pair is its own sentence. "Before you run `terraform apply`, run `terraform plan`" places the prerequisite condition first.*

```hcl
# main.tf
resource "aws_s3_bucket" "logs" {
  bucket = "app-logs-prod"
}
```

```bash
# STE-ordered commands:
# Before you run terraform apply, run terraform plan.
terraform plan -out=tfplan
# Check the plan output for unexpected resource destruction.
terraform show tfplan
# If the plan is correct, run terraform apply.
terraform apply tfplan
```

#### Example 4 — Kubernetes Pod Troubleshooting

> **Non-STE:** To figure out why the pod keeps restarting you should describe the pod to see its events and check the logs of the previous container instance with the --previous flag if the current container is still running.
>
> **STE:** If a pod restarts again and again, get its events. Run `kubectl describe pod <name>`. To see the logs from the previous container instance, use the `--previous` flag.
>
> *Principle applied: P1 ("get" instead of "to figure out," "use" instead of "check"), P5 (kubectl, pod as technical nouns), P8. The condition "If a pod restarts again and again" comes first. The infinitive phrase "To see the logs..." is an alternative condition form. Both place the condition before the command.*

```bash
# STE-ordered troubleshooting:
# If a pod restarts again and again, get its events.
kubectl get events --field-selector involvedObject.kind=Pod
# Run kubectl describe pod <name>.
kubectl describe pod payment-worker-7c9f4
# To see the logs from the previous container instance, use the --previous flag.
kubectl logs payment-worker-7c9f4 --previous
```

#### Example 5 — SQL Query Documentation

> **Non-STE:** The UPDATE statement modifies rows in the specified table but you must always include a WHERE clause unless you intend to update every single row in the table which is rarely the desired behavior in a production database.
>
> **STE:** Always include a `WHERE` clause in an `UPDATE` statement. If you do not include a `WHERE` clause, the statement updates all rows in the table.
>
> *Principle applied: P1, P5 (SQL keywords as technical nouns), P8. Two sentences. The first is a direct command (Rule 5.3 — imperative form). The second uses condition-before-command: "If you do not include a `WHERE` clause" comes first, then the descriptive result. This warns the reader about the consequence of violating the instruction.*

```sql
-- Correct: a WHERE clause limits the update.
UPDATE accounts SET balance = balance - 100 WHERE id = 42;

-- Violation: no WHERE clause. The statement updates all rows in the table.
UPDATE accounts SET balance = 0;
```

The documentation warns: "Always include a `WHERE` clause in an `UPDATE` statement. If you do not include a `WHERE` clause, the statement updates all rows in the table."

#### Example 6 — Git Workflow Documentation

> **Non-STE:** You should rebase your feature branch onto the latest main branch to incorporate upstream changes and resolve any merge conflicts locally instead of during the pull request review process but only after you have committed or stashed all of your current work.
>
> **STE:** Before you rebase your feature branch, commit or stash your current work. After you commit or stash your work, rebase your feature branch onto the latest `main` branch. If merge conflicts occur, resolve them locally.
>
> *Principle applied: P1 ("rebase" as technical verb per P12), P5 (branch as technical noun), P8. Three separate condition-command pairs. Each condition comes first. The comma separates the condition from the command in every sentence. The original nested three conditions inside one sentence, violating the one-condition-per-step principle.*

```bash
# STE-ordered workflow:
# Before you rebase your feature branch, commit or stash your current work.
git add -A && git commit -m "WIP: in-progress change"
# After you commit or stash your work, rebase your feature branch onto main.
git fetch origin && git rebase origin/main
# If merge conflicts occur, resolve them locally.
git status   # shows the conflicting files; open and edit them, then git add
```

## Paradigm-Specific Guidance

The condition-before-command pattern applies across all programming paradigms. Each paradigm has distinct documentation conventions, but the principle remains the same: the reader must evaluate the condition before they act.

### Object-Oriented Programming (Java, C++, C#, Python Classes)

Object-oriented documentation describes class hierarchies, method contracts, and state mutations. Preconditions on method calls are the most common form of condition-before-command in OOP documentation.

State the precondition before the method call instruction. If a method mutates object state, state the required initial state as a condition.

> **Non-STE:** Call the `.save()` method on the entity object to persist it to the database after setting all the required fields and making sure that the entity is in a valid state according to the validation rules defined in the entity class annotations.
>
> **STE:** Set all required fields on the entity. After the entity passes validation, call `.save()`.
>
> *Principle applied: P1, P5 (`.save()` as technical noun). Two sentences. The condition "After the entity passes validation" comes before the command.*

```python
# STE documentation for the method:
# Set all required fields on the entity.
entity.name = "billing-service"
entity.port = 8080
# After the entity passes validation, call .save().
entity.save()   # raises ValidationError if a required field is empty
```

For constructor documentation, state the preconditions that must be true before object creation.

> **Non-STE:** Constructs a new HttpClient instance with the provided configuration. The configuration object must not be null and must have at least a base URL set otherwise an IllegalStateException will be thrown at construction time.
>
> **STE (Java):** Make a new `HttpClient` instance with the specified configuration. If the configuration is `null`, the constructor throws `IllegalStateException`. If the base URL is not set, the constructor throws `IllegalStateException`.
>
> *Principle applied: P1 ("make" instead of "constructs"), P5 (`HttpClient`, `IllegalStateException` as technical nouns). Each error condition is a separate condition-result pair.*

```java
// STE constructor contract:
// Make a new HttpClient instance with the specified configuration.
// If the configuration is null, the constructor throws IllegalStateException.
// If the base URL is not set, the constructor throws IllegalStateException.
public HttpClient(Config config) {
    if (config == null) throw new IllegalStateException("config is null");
    if (config.baseUrl() == null) throw new IllegalStateException("base URL not set");
    this.config = config;
}
```

### Functional Programming (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, type signatures, and data transformations. Conditions in functional documentation often appear as guard clauses, pattern match descriptions, or type constraints.

State the input condition before describing the transformation. Use the condition-before-command pattern even when the "command" is a descriptive statement about function behavior.

> **Non-STE:** The function returns the head of the list if the list is non-empty and returns Nothing when given an empty list.
>
> **STE (Haskell):** If the list is not empty, the function returns `Just (head list)`. If the list is empty, the function returns `Nothing`.
>
> *Principle applied: P1, P5 (Haskell types as technical nouns). Each case is a condition-before-result pair. The comma separates the condition from the result clause.*

```haskell
-- STE documentation:
-- If the list is not empty, the function returns Just (head list).
-- If the list is empty, the function returns Nothing.
safeHead :: [a] -> Maybe a
safeHead []     = Nothing
safeHead (x:xs) = Just x
```

> **Non-STE:** unwrap_or() returns the contained Some value or a provided default if the Option is None and panics if called on a None value with unwrap() instead of unwrap_or().
>
> **STE (Rust):** If the `Option` is `Some(value)`, `unwrap_or(default)` returns `value`. If the `Option` is `None`, `unwrap_or(default)` returns `default`. NOTE: Do not use `unwrap()` on a `None` value. `unwrap()` causes a panic on `None`.
>
> *Principle applied: P5 (Rust types and methods as technical nouns), P8. Each branch is a separate condition-result pair. The NOTE uses imperative form (Rule 5.5 — notes give information, not instructions; here the instruction is acceptable as a warning).*

```rust
// STE documentation:
// If the Option is Some(value), unwrap_or(default) returns value.
// If the Option is None, unwrap_or(default) returns default.
// NOTE: Do not use unwrap() on a None value. unwrap() causes a panic on None.
let config = settings.get("timeout").unwrap_or(default_timeout);
```

### Procedural Programming (C, Go, Bash)

Procedural documentation describes sequences of steps, resource lifecycle, and error handling. Conditions in procedural code are often system-state checks, file existence tests, or return-code evaluations.

State the system-state condition before the action. In Bash scripts and Makefiles, the condition-before-command pattern maps directly to shell constructs, but documentation should still use natural-language condition clauses.

> **Non-STE:** The function reads the entire contents of the file at the given path into memory and returns it as a byte slice but callers must ensure the file exists and is readable before calling this function otherwise it returns an error.
>
> **STE (Go):** Read the file at `path` into memory. Return the contents as a `[]byte`. If the file does not exist, the function returns an error. If the file is not readable, the function returns an error.
>
> *Principle applied: P1 ("read" instead of "reads"), P5 (Go type notation as technical noun). The precondition "If the file does not exist" comes before the result clause.*

```go
// STE documentation:
// Read the file at path into memory.
// Return the contents as a []byte.
// If the file does not exist, the function returns an error.
// If the file is not readable, the function returns an error.
func ReadAll(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("read %s: %w", path, err)
    }
    return data, nil
}
```

> **Non-STE:** Kill the process using the PID from the lockfile after checking that the process is actually still running and the PID hasn't been reused by the operating system for a different process.
>
> **STE (Bash script comment):** If the process is still running, stop it. Use the PID from the lockfile. Before you stop the process, make sure that the PID is correct.
>
> *Principle applied: P1 ("stop" instead of "kill"), P5 (PID as technical noun). The condition "If the process is still running" comes first, followed by the command "stop it."*

```bash
# STE-ordered shutdown:
# If the process is still running, stop it.
# Use the PID from the lockfile.
PID=$(cat /var/run/app.pid)
# Before you stop the process, make sure that the PID is correct.
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
fi
```

### Declarative Programming (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state, not procedural steps. However, operational documentation for declarative tools (how to apply a Terraform plan, how to run a migration) still uses procedural language. Condition-before-command applies to the operational wrapper, not the declarative specification itself.

> **Non-STE:** Run terraform destroy to tear down all the infrastructure defined in your state file after you have backed up any important data and confirmed that no other teams depend on the resources you are about to destroy.
>
> **STE:** Before you run `terraform destroy`, back up all important data. Make sure that no other teams use the resources. Then, run `terraform destroy`.
>
> *Principle applied: P1, P5 (`terraform destroy` as technical noun). Three sentences. The condition "Before you run `terraform destroy`" comes first. Each prerequisite is its own step.*

```bash
# STE-ordered teardown:
# Before you run terraform destroy, back up all important data.
aws s3 sync s3://app-state-prod s3://app-state-backup-$(date +%F)
# Make sure that no other teams use the resources.
# Then, run terraform destroy.
terraform destroy -auto-approve
```

For SQL documentation, state the condition for a query or mutation before the statement.

> **Non-STE:** The DELETE FROM statement removes rows from the table but you must run it inside a transaction if you want to be able to roll back the deletion in case you made a mistake with the WHERE clause.
>
> **STE:** Run `DELETE FROM` inside a transaction. If you do not use a `WHERE` clause, the statement removes all rows. If the `WHERE` clause is incorrect, you can roll back the transaction.
>
> *Principle applied: P1, P5 (SQL keywords as technical nouns). The imperative command "Run `DELETE FROM` inside a transaction" comes first (Rule 5.3). The conditions "If you do not use..." and "If the `WHERE` clause is incorrect..." each precede their result clauses.*

```sql
-- STE documentation:
-- Run DELETE FROM inside a transaction.
BEGIN;
DELETE FROM sessions WHERE expires_at < now();
-- If the WHERE clause is incorrect, you can roll back the transaction.
ROLLBACK;   -- or COMMIT; once you confirm the row count
```

### Systems Programming (Rust Ownership, C Memory Management)

Systems documentation describes memory models, ownership semantics, and safety invariants. Conditions in systems documentation are often safety constraints, lifetime requirements, or synchronization prerequisites. Misreading a condition in systems documentation can cause undefined behavior, data races, or security vulnerabilities.

State the safety condition before the operation. Use WARNING or BREAKING prefixes when the consequence of violating the condition is severe.

> **Non-STE:** You can call unsafe functions but only after manually verifying that all the safety invariants documented in the function's safety section are upheld by the calling code.
>
> **STE (Rust):** Before you call an `unsafe` function, read its safety documentation. Make sure that your code upholds all documented safety invariants. WARNING: IF YOUR CODE DOES NOT UPHOLD THE SAFETY INVARIANTS, THE PROGRAM CAN HAVE UNDEFINED BEHAVIOR.
>
> *Principle applied: P5 (Rust keyword as technical noun), P8. The condition "Before you call an `unsafe` function" comes first. The WARNING uses the condition-before-command pattern inside a safety instruction (see Rule 7.2).*

```rust
// STE documentation for the raw pointer dereference:
// Before you call an unsafe function, read its safety documentation.
// Make sure that your code upholds all documented safety invariants.
// WARNING: IF YOUR CODE DOES NOT UPHOLD THE SAFETY INVARIANTS, THE PROGRAM CAN HAVE UNDEFINED BEHAVIOR.
unsafe fn deref(ptr: *const u32) -> u32 {
    *ptr   // caller must ensure ptr is non-null and points to valid memory
}
```

> **Non-STE:** Call free() on the pointer to release the dynamically allocated memory back to the heap after making absolutely sure that no other part of the program still holds a reference to that memory because use-after-free is a critical security vulnerability.
>
> **STE (C):** Before you call `free(ptr)`, make sure that no other code uses `ptr`. WARNING: IF YOU CALL `free(ptr)` AND OTHER CODE STILL USES `ptr`, THE PROGRAM CAN HAVE A USE-AFTER-FREE VULNERABILITY. AFTER YOU CALL `free(ptr)`, DO NOT USE `ptr`.
>
> *Principle applied: P1 ("call" as approved verb), P5 (C function as technical noun). The condition "Before you call `free(ptr)`" comes first. The WARNING and the final command both follow the condition-before-command pattern.*

```c
/* STE documentation:
   Before you call free(ptr), make sure that no other code uses ptr.
   WARNING: IF YOU CALL free(ptr) AND OTHER CODE STILL USES ptr,
   THE PROGRAM CAN HAVE A USE-AFTER-FREE VULNERABILITY.
   AFTER YOU CALL free(ptr), DO NOT USE ptr. */
void release(Buffer *ptr) {
    free(ptr);   /* after this line, ptr is invalid */
    ptr = NULL;
}
```

## Edge Cases

### Edge Case 1 — Framework Name Is Also a Common Word

Some framework names are common English words that might appear in the STE-Code approved word list with a different meaning. When a framework name conflicts with an approved word, the framework name takes priority as a technical code noun under Rule 1.5. The comma placement rule still applies to the condition clause that contains the framework name.

> **Non-STE:** Before you start the Next.js development server you must set the environment variables in the .env.local file because Next.js reads them at startup and caches them for the entire lifetime of the process.
>
> **STE:** Before you start the Next.js development server, set the environment variables in the `.env.local` file.
>
> *Principle applied: P5 (Next.js as framework name), P1. The word "start" is an approved STE-Code verb. "Next.js" is a framework name that includes a period, which is acceptable as a technical noun. The comma after "server" separates the condition from the command.*

```bash
# STE-ordered setup:
# Before you start the Next.js development server, set the environment variables.
echo "DATABASE_URL=postgres://localhost:5432/app" > .env.local
npm run dev   # Next.js reads .env.local at startup and caches the values
```

> **Non-STE:** When you run the Express app in production mode it loads the production middleware stack that excludes the development-only error handler and the hot module replacement plugin.
>
> **STE:** When you run the Express application in production mode, it loads the production middleware stack.
>
> *Principle applied: P5 (Express as framework name). "Express" is both an English word and a framework name. In code documentation, it is a technical noun. The condition "When you run the Express application in production mode" comes first, separated by a comma.*

```javascript
// STE documentation:
// When you run the Express application in production mode, it loads the production middleware stack.
if (process.env.NODE_ENV === "production") {
  app.use(productionMiddleware);   // no dev error overlay, no HMR
}
```

### Edge Case 2 — Code Keyword Inside the Condition Clause

Code keywords, function names, and variable names are technical nouns under Rule 1.5. When they appear inside a condition clause, the comma placement rule still applies. The reader must be able to identify where the condition ends and the command begins, even when the condition contains punctuation characters (backticks, parentheses, dots).

> **Non-STE:** If `someCondition && anotherCondition || fallbackFlag` evaluates to true you can safely proceed with the state transition.
>
> **STE:** If `someCondition && anotherCondition || fallbackFlag` is `true`, start the state transition.
>
> *Principle applied: P5 (code expression as technical noun). The condition clause contains a code expression with `&&`, `||`, and backticks. The comma after `` `true` `` separates the condition from the command. The reader can see where the condition ends because the comma follows the closing backtick.*

```python
# STE documentation:
# If someCondition && anotherCondition || fallbackFlag is true, start the state transition.
if some_condition and another_condition or fallback_flag:
    start_state_transition()
```

> **Non-STE:** When `response.status === 429` the client should wait for the duration specified in the `Retry-After` header before retrying the request.
>
> **STE:** When `response.status === 429`, wait for the duration in the `Retry-After` header. Then, send the request again.
>
> *Principle applied: P5 (JavaScript expression as technical noun), P1 ("send... again" instead of "retrying"). The comma after the code expression `response.status === 429` (inside backticks) separates the condition from the command. Two sentences keep each action clear.*

```javascript
// STE documentation:
// When response.status === 429, wait for the duration in the Retry-After header.
// Then, send the request again.
if (response.status === 429) {
  const wait = Number(response.headers.get("Retry-After")) || 1;
  await sleep(wait * 1000);
  return sendRequestAgain();
}
```

### Edge Case 3 — Condition Clause Contains a Comma for a Different Reason

Sometimes a condition clause itself contains a comma (for example, a list of items). In this case, do not rely on the comma alone to separate the condition from the command. Use a stronger delimiter, restructure the sentence, or break it into multiple sentences.

> **Non-STE:** If you change the database schema, the API contract, or the message queue format, you must update the corresponding version number in the configuration file.
>
> **STE:** The database schema, the API contract, and the message queue format are part of the system interface. If you change one or more of these parts, update the version number in the configuration file.
>
> *Principle applied: P1, P8. The condition clause "If you change the database schema, the API contract, or the message queue format" contains internal commas (list separators). Adding another comma after "format" would create ambiguity. The STE version introduces the list in a separate descriptive sentence, then uses a simple condition clause "If you change one or more of these parts" that has no internal commas.*

```yaml
# config.yaml
interface:
  version: 3          # bump this number when you change a listed part
  parts:
    - database_schema
    - api_contract
    - message_queue_format
```

> STE (alternative): Before you change the database schema, the API contract, or the message queue format, update the version number in the configuration file.
>
> *This works when the condition is short enough that the reader can parse both the list commas and the separating comma. Use this pattern only when the condition clause has at most one internal comma. For longer lists, use the two-sentence approach above.*

### Edge Case 4 — Condition Implied by Tool Output

Some documentation assumes the reader observes a condition from tool output (a log message, a status code, a test result). When the condition is implied by observable output, state the observable output as the condition clause.

> **Non-STE:** If you see the error message "Connection refused" when you try to connect to the database then the database server is probably not running so you need to start it.
>
> **STE:** If the terminal shows "Connection refused," start the database server.
>
> *Principle applied: P1 ("shows" instead of "you see"). The condition "If the terminal shows 'Connection refused'" comes first, separated by a comma. The observable output is the condition.*

```bash
# STE troubleshooting:
# If the terminal shows "Connection refused," start the database server.
pg_ctl start -D /var/lib/postgresql/data
```

> **Non-STE:** You'll know the build succeeded when you see "BUILD SUCCESSFUL" in the terminal output at which point you can proceed to deploy the artifact to the staging environment.
>
> **STE:** When the terminal shows "BUILD SUCCESSFUL," deploy the artifact to the staging environment.
>
> *Principle applied: P1, P5 (build output string as technical noun). The observable condition comes first. The comma separates it from the command.*

```bash
# STE-ordered release:
# When the terminal shows "BUILD SUCCESSFUL," deploy the artifact to staging.
./gradlew build
# output: BUILD SUCCESSFUL
aws s3 cp build/app.jar s3://staging-binaries/app.jar
```

### Edge Case 5 — Generated Code and Automated Documentation

Generated documentation (from tools like Sphinx, JSDoc, godoc, or rustdoc) cannot always follow the condition-before-command pattern because the generation tool extracts text from source code in a fixed order. In these cases, the rule is relaxed for the generated output, but the source docstrings and comments should still follow Rule 5.4.

> **Source docstring (correct):** If `timeout_ms` is `0`, the function waits indefinitely.
>
> **Generated output (acceptable):** The function waits indefinitely if `timeout_ms` is `0`. (The generator placed the main clause first. This is acceptable for automated output, but the source docstring must follow Rule 5.4.)

```python
def await_ready(timeout_ms: int) -> bool:
    """If timeout_ms is 0, the function waits indefinitely.

    Args:
        timeout_ms: Maximum wait time in milliseconds.
    """
    if timeout_ms == 0:
        while not ready():
            pass
    return ready()
```

When you write generator templates that produce human-readable documentation (README generators, CLI help text templates), apply Rule 5.4 to the template text, not to the generated variable substitutions.

> **Non-STE:** Run {{command}} to {{action}} after you {{condition}}.
>
> **STE (template):** After you {{condition}}, run {{command}} to {{action}}.
>
> *Principle applied: P1, P8. The template places the condition placeholder first, then the command. The generated output will inherit the correct structure regardless of the substituted values.*

```jinja
{# CLI help template — keeps the condition before the command #}
{% for step in steps %}
After you {{ step.condition }}, run `{{ step.command }}` to {{ step.action }}.
{% endfor %}
```

## Grammar Notes

### The Comma as a Scope Delimiter

In the original ASD-STE100, the comma after a condition clause functions as a scope delimiter. It marks the boundary between the condition scope and the command scope. This grammatical function is borrowed from English adverbial clause punctuation: when a dependent clause (the condition) precedes an independent clause (the command), a comma is mandatory.

In code documentation, the comma serves the same function. It tells the reader: "The condition scope ends here. The command scope begins now." Without the comma, the reader cannot reliably identify the boundary, especially in sentences that contain technical nouns with punctuation (backtick-delimited code terms, dot-separated identifiers, or parenthesized parameter lists).

The comma is not optional. It is a required syntactic marker that enforces the condition-before-command reading order. The reader's eye scans for the comma, and the comma signals the transition from evaluation to action.

### Adverb Placement and Ambiguity

The original ASD-STE100 uses the "CSD does not operate correctly" example to illustrate that comma placement determines which verb an adverb modifies. In code documentation, the same ambiguity exists with adverbs like "automatically," "correctly," "safely," and "securely."

Pattern: `[condition clause] , [adverb] [command]` — the adverb modifies the command.
Pattern: `[condition clause with adverb] , [command]` — the adverb modifies the condition.

> `If the token expires, automatically refresh it.` (The refresh is automatic.)
> `If the token expires automatically, refresh it.` (The expiry is automatic. The refresh is manual.)

When the adverb is essential to the command's meaning, place it after the comma. When the adverb is essential to the condition's meaning, place it before the comma. When both the condition and the command need an adverb, use two sentences.

### Dependent Clause Types

Rule 5.4 applies to several types of dependent clauses that serve as conditions:

1. **Time clauses** (before, after, when, while, until, as soon as):
   > Before you deploy, run the test suite.

2. **Conditional clauses** (if, unless, provided that, as long as):
   > If the build fails, check the error log.

3. **Reason clauses** (because, since — but prefer "because" for STE-Code clarity):
   > Because the port is in use, use a different port. (Better: "The port is in use. Use a different port.")

4. **Purpose clauses** (to, in order to — these set a goal condition before an action):
   > To see all running containers, run `docker ps`.

5. **Concessive clauses** (although, even though):
   > Although the server starts without errors, check the health endpoint.

In each case, the dependent clause comes first. The comma separates it from the main clause. Do not reverse the order (main clause first, dependent clause second) because the reader would then read the command before the condition.

### Punctuation After WARNING, BREAKING, and DEPRECATED Prefixes

When a WARNING, BREAKING, or DEPRECATED prefix introduces a condition-before-command sentence, the comma after the condition clause still applies inside the prefixed sentence.

> WARNING: IF YOU DELETE THE PRODUCTION DATABASE, YOU CANNOT RECOVER THE DATA.

The colon after WARNING separates the prefix from the instruction. The comma after DATABASE separates the condition from the command. Both punctuation marks are necessary.

### Multiple Conditions in One Sentence

Rule 5.4 applies to one condition per sentence. If a step requires two or more conditions before the reader can act, use one of these strategies:

**Strategy A — Separate sentences:**
> Make sure that the database server is running. After the server accepts connections, run the migration script.

**Strategy B — Compound condition with "and":**
> If the database server is running and the backup is complete, run the migration script.

**Strategy C — Sequential condition-command pairs:**
> Before you run the migration, make sure that the database server is running. After the server accepts connections, run the migration script.

Strategy C is the preferred approach. It gives each condition its own sentence and its own comma, making the scope of each condition unambiguous.

### Interaction with Rule 5.3 (Imperative Form)

Rule 5.3 requires instructions to use the imperative mood. Rule 5.4 requires the condition to precede the imperative command. The two rules work together:

> [Condition clause] , [imperative verb] [object] [optional complement].

The comma is the bridge between the descriptive condition (which may use indicative mood) and the imperative command. The condition clause sets the context. The comma signals the end of the context. The imperative verb begins the action.

### Interaction with Rule 1.5 (Technical Code Nouns)

When a condition clause contains a technical code noun (a keyword, a tool name, a file path), the noun is not subject to the approved-word dictionary. Only the surrounding natural-language words must use approved vocabulary. The comma placement rule applies to the entire clause, including the technical noun.

> If `kubectl get pods` returns `ErrImagePull`, check the image name in the pod specification.

The condition clause contains technical nouns (`kubectl`, `pods`, `ErrImagePull`, `image name`, `pod specification`). The word "check" is an approved STE-Code verb. The comma after `` `ErrImagePull` `` separates the condition from the command.

## Cross-References

> **See also:** Rule 1.1 — Use Approved Words: The condition clause and command must use words from the STE-Code dictionary. Technical code nouns are exempt under Rule 1.5.
> **See also:** Rule 1.4 — Approved Verb Forms: The command that follows the condition clause must use an approved verb form. The condition clause may use tense-marked verbs ("runs," "starts," "fails") because conditions describe states, not actions.
> **See also:** Rule 1.5 — Technical Code Nouns: Keywords, frameworks, tool names, and file paths in condition clauses are technical nouns and are not subject to the approved-word dictionary.
> **See also:** Rule 5.3 — Imperative (Command) Form for Instructions: The command that follows the condition clause must use the imperative mood. Rule 5.4 supplies the condition; Rule 5.3 supplies the verb form.
> **See also:** Rule 5.5 — Notes Give Information Only, Not Instructions: If a condition does not lead to a command, it is a note, not an instruction. Do not use the condition-before-command pattern for notes. Use NOTE: instead.
> **See also:** Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition: When a condition clause leads to a safety-critical command, use the WARNING prefix. The condition-before-command pattern applies inside the safety instruction.

- **STE-Code Dictionary:** Consult the dictionary for approved verbs ("start," "stop," "check," "make," "get," "set," "remove," "send," "show," "run," "use") and approved nouns to use in condition clauses. Use the synonym table to replace non-approved words ("verify" → "check," "obtain" → "get," "terminate" → "stop").

---

<!-- a-sec5-rule5.5.md -->

# Rule 5.5 — Notes Give Information Only, Not Instructions

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 5.5
> **Source:** [master.md#sec5-rule5.5](ste-code/grouped/)

## Original Rule

Write notes only to give information, not instructions.

Notes only give information to help the reader during a procedure. They contain descriptive text and obey the rules for descriptive writing.

Notes must not give instructions, requirements, or limits.

Examples in STE:

| NOTE: | The gyroscope will become stable after approximately 15 seconds. |
| --- | --- |

A note can have one or more sentences. Each sentence in a note can have a maximum of 25 words.

Examples in STE:

| NOTE: | The flow through the CROSS FEED port is more than 5 cc/minute. |
| --- | --- |

(One sentence, 22 words.)

| NOTE: | The test verifies the installation. The test shows the results. |
| --- | --- |

(Two sentences, 6 words and 8 words.)

Do not use the imperative form in a note. If you use the imperative form, the note becomes an instruction for a work step.

Example:

| NOTE: | Make sure that the avionics ventilation system continues to operate correctly. |
| --- | --- |

(This text is not a note because it contains the imperative form.)

> **STE:** (6) Make sure that the avionics ventilation system continues to operate correctly.

(This is work step number 6 in the applicable procedure.)

If you include instructions in a note, it is possible that the reader will not see the information. If the information given in a note is important to prevent damage or injury, you must give such information in a safety instruction.

Examples:

| Non-STE: | NOTE: When you connect the lines, do not bend them too much. If you bend the lines too much, you can cause damage to them. (This text is not a note. It is a safety instruction.) |
| --- | --- |
| STE: | CAUTION: WHEN YOU CONNECT THE LINES, DO NOT BEND THEM TOO MUCH. IF YOU BEND THE LINES TOO MUCH, YOU CAN CAUSE DAMAGE TO THEM. |

| Non-STE: | NOTE: Before you close the hatch, make sure that no persons are in the crew rest compartment. When the hatch is closed, there is no airflow to the compartment and therefore there is a risk of suffocation. (Although the non-STE text does not contain the imperative form, it is not a note. It is a safety instruction.) |
| --- | --- |
| STE: | WARNING: BEFORE YOU CLOSE THE HATCH, MAKE SURE THAT NO PERSONS ARE IN THE CREW REST COMPARTMENT. WHEN THE HATCH IS CLOSED, THERE IS NO AIRFLOW TO THE COMPARTMENT AND THERE IS A RISK OF SUFFOCATION. |

Do not use a note to give limits, tolerances, or results of a work step. This information must come directly after the related action in the work step.

## How to use notes correctly

When you write a procedure, and this procedure contains notes, do this test:

- Carefully read the procedure without the notes.
- Make sure that the reader can do the procedure correctly without the notes.

A satisfactory result of this test tells you that you used the notes correctly.

If important information is missing from the procedure and this information is in a note:

- Remove the information from the note.
- Write the missing information in a work step.
- Include this new work step where applicable in the procedure.
- Do the test again until you are fully sure that the reader can do the procedure without the notes.

In STE, you use notes in procedures. You can write notes in descriptions only if the notes are necessary for illustrations or tables that are parts of such descriptions.

In code documentation, this test applies to any procedure that the reader follows: a setup walkthrough, an upgrade guide, a debugging playbook, or a CI pipeline. The reader must be able to complete the task from the numbered steps and the inline code alone, with every note treated as optional background.

## STE-Code Adaptation

In code documentation, notes provide supplementary information that helps the reader understand context, behavior, or background details about a procedure. Notes must contain descriptive information only. Notes must not contain instructions for the reader to execute, commands to run, or step-by-step actions.

Notes must not give requirements, limits, tolerances, or expected results of a work step. This information belongs directly in the work step itself, after the related action, so the reader sees it while executing the step. Notes must not contain imperative verbs. If you need to give an instruction, write it as a numbered work step.

If a note contains information that is critical for preventing data loss, security issues, or system damage, move that information into a WARNING or CAUTION safety instruction. A note is never a substitute for a safety instruction.

Each sentence in a note can have a maximum of 25 words. A note can contain one or more sentences.

To verify correct note usage, read the procedure without the notes. If the reader cannot complete the procedure correctly, move the missing information from the notes into work steps and repeat the test.

### Examples

> *Adapted from spec pair:* Non-STE: NOTE: When you connect the lines, do not bend them too much. If you bend the lines too much, you can cause damage to them. | STE: CAUTION: WHEN YOU CONNECT THE LINES, DO NOT BEND THEM TOO MUCH. IF YOU BEND THE LINES TOO MUCH, YOU CAN CAUSE DAMAGE TO THEM.

> **STE:** NOTE: The API rate limiter allows a maximum of 1000 requests per minute per client IP address on the free tier.
>
> *Source pairing: a note gives descriptive information only, with no instruction — follows the same principle as the original STE example in Rule 5.5.*

(One sentence, 20 words. This note gives context about the API behavior without instructing the reader to do anything. It appears in the reference page for the rate limiter, as background to the endpoint table.)

> **STE:** NOTE: The configuration cache refreshes automatically every 60 seconds. Manual changes to the configuration file will not take effect until the next cache refresh cycle.
>
> *Adapted from spec: multi-sentence note example — a note can have one or more sentences, each with a maximum of 25 words.*

(Two sentences, 8 words and 19 words. Descriptive information only, no instructions. This note sits above the `config.toml` reference table.)

> **Non-STE:** NOTE: When you update the dependencies, run the command `npm audit fix` to resolve known vulnerabilities. If you skip this step, your application may have security issues.
>
> **STE:** (5) Run the command `npm audit fix` to resolve known vulnerabilities.
>
> *Source pairing: an instruction written inside a note becomes a numbered work step — follows the same principle as the original STE example in Rule 5.5.*

(Do not put instructions in a note. The instruction to run a command is a work step. The non-STE note would appear in a README security section like this:)

```markdown
## Security

NOTE: When you update the dependencies, run the command `npm audit fix` to
resolve known vulnerabilities. If you skip this step, your application may have
security issues.
```

The STE-Code compliant README makes it a numbered step in the setup procedure:

```markdown
## Setup

1. Install the dependencies with `npm install`.
2. Copy `.env.example` to `.env`.
3. Set the `DATABASE_URL` value in `.env`.
4. Start the database with `docker compose up -d`.
5. Run the command `npm audit fix` to resolve known vulnerabilities.
```

> **Non-STE:** NOTE: The response time must be less than 200 milliseconds under normal load conditions. If the response time is higher, investigate the database query performance.
>
> **STE:** The response time must be less than 200 milliseconds under normal load conditions.
>
> *Adapted from spec: notes must not give limits, tolerances, or results — this information belongs directly in the work step.*

(Do not put limits or requirements in a note. The limit belongs directly in the work step. In an OpenAPI description, the limit is a statement in the endpoint body, not a note:)

```yaml
  /orders:
    get:
      summary: Get the list of orders for the current user.
      description: |
        The response time must be less than 200 milliseconds under normal load
        conditions. If the response time is higher, investigate the database
        query performance.
      responses:
        '200':
          description: The list of orders.
```

| Non-STE: | NOTE: Before you deploy to production, make sure that all environment variables are set correctly. If you deploy with missing variables, the application will not start and the deployment will fail. (This text is not a note. It is a safety instruction.) |
| --- | --- |
| STE: | CAUTION: BEFORE YOU DEPLOY TO PRODUCTION, MAKE SURE THAT ALL ENVIRONMENT VARIABLES ARE SET CORRECTLY. IF YOU DEPLOY WITH MISSING VARIABLES, THE APPLICATION WILL NOT START. |

> *Source pairing: a note that contains a safety instruction must become a CAUTION — follows the same principle as the original STE example in Rule 5.5.*

(The CAUTION belongs at the top of the deployment runbook, before the numbered deploy steps, so the reader sees the risk before they act.)

> **Non-STE:** NOTE: Do not run the migration script on the production database without first creating a full backup. Running the migration without a backup can cause irreversible data loss.
>
> **STE:** WARNING: DO NOT RUN THE MIGRATION SCRIPT ON THE PRODUCTION DATABASE WITHOUT A FULL BACKUP. RUNNING THE MIGRATION WITHOUT A BACKUP CAN CAUSE IRREVERSIBLE DATA LOSS.
>
> *Source pairing: critical safety information belongs in a WARNING, not a note — follows the same principle as the original STE example in Rule 5.5.*

(Critical safety information belongs in a WARNING, not a note. The WARNING sits at the top of the upgrade guide, above step 1.)

### Code-Domain Explanation

This rule applies differently across documentation types in software engineering. Each type has a distinct audience and purpose. The separation of notes from instructions is critical in all types.

#### README Files

README files serve as the entry point for a project. They mix descriptive content with setup instructions. Notes in README files must provide context that helps the reader understand the project. They must not replace setup steps.

A note in a README can explain why a dependency exists or give background on a design decision. It must not tell the reader to install a package or run a command. Place those instructions in the numbered setup steps.

> **STE:** NOTE: This project uses SQLite for local development. The production deployment uses PostgreSQL for concurrent write support.
>
> (Descriptive context. The reader does not need this information to complete the setup steps.)

The note appears in the README like this:

```markdown
# acme-cli

NOTE: This project uses SQLite for local development. The production deployment
uses PostgreSQL for concurrent write support.

## Setup

1. Install the tool with `npm install -g acme-cli`.
2. Run `acme init` to create the local database.
3. Start the local server with `acme serve`.
```

The note gives background only. The three setup steps stay as numbered instructions, with no note mixed into them.

#### API Documentation

API reference documents describe endpoints, parameters, and response formats. Notes in API documentation explain behavior, side effects, or constraints. They must not include instructions for using the API endpoint.

A note about rate limiting is acceptable. A note that says "Call the /refresh endpoint before this one" is an instruction. Move that instruction to the endpoint description or write it as a prerequisite step.

> **STE:** NOTE: The `/search` endpoint returns a maximum of 50 results per page. The `cursor` parameter gets the next page of results.
>
> (Both sentences are descriptive. The second sentence describes what the parameter does. It does not tell the reader to call anything.)

The compliant note in an OpenAPI document reads:

```yaml
  /search:
    get:
      summary: Search the catalog.
      description: |
        NOTE: The `/search` endpoint returns a maximum of 50 results per page.
        The `cursor` parameter gets the next page of results.
      parameters:
        - name: cursor
          in: query
          description: The pagination token from the previous response.
```

The original non-STE version wrote "Use the `cursor` parameter to get the next page of results," which is an instruction and breaks this rule.

#### Docstrings

Function and class docstrings are the most constrained documentation type. They appear inline with code and are read by both humans and tools. Notes in docstrings must describe behavior, not tell the caller what to do.

A docstring note can explain that a function is not thread-safe. It must not say "Call this function only from the main thread." That is a requirement. Write it as a constraint in the function description.

> **Non-STE:** NOTE: You must call `initialize()` before calling any other function in this module. If you do not call it first, the other functions will throw an exception.
>
> **STE:** This module requires a call to `initialize()` before any other function call. Other function calls will raise `ModuleNotInitializedError` if `initialize()` has not completed.
>
> *Principle applied: P4 (approved verb forms). The requirement is part of the function specification, not a note.*

The compliant docstring reads:

```python
def connect() -> Connection:
    """Open a connection to the cache server.

    This module requires a call to `initialize()` before any other function
    call. Other function calls will raise `ModuleNotInitializedError` if
    `initialize()` has not completed.
    """
```

The constraint is a descriptive statement in the docstring body, not a note that gives the reader an instruction.

#### Commit Messages

Commit messages follow a specific format: a summary line followed by a blank line and a body. Notes in commit message bodies must explain why a change was made. They must not give instructions for using the change.

A commit message note can explain that a refactor was necessary because of a performance regression. It must not say "Run the migration after checking out this commit." That instruction belongs in release notes or a migration guide.

> **STE:** NOTE: The database schema change removes the `legacy_status` column. This column was deprecated in version 2.4 and no code references it.
>
> (Descriptive context about the change. No instructions.)

The compliant commit message reads:

```
Remove the legacy_status column from the users table

NOTE: The database schema change removes the `legacy_status` column. This
column was deprecated in version 2.4 and no code references it. The upgrade
migration handles the data copy before the drop.
```

The message explains the reason for the change. It does not tell the reader to run a migration in the note; that instruction appears in the upgrade guide as a numbered step.

#### Error Messages

Error messages are the most constrained context for notes. An error message must tell the user what went wrong and possibly how to fix it. A note in an error message must describe state or context. It must not contain the fix instruction as a note.

> **Non-STE:** Error: Connection refused.
> NOTE: Check that the database server is running on port 5432. Verify your credentials in the `.env` file.
>
> **STE:** Error: Connection refused.
> The database server on port 5432 did not respond. Check that the server is running. Make sure that the credentials in the `.env` file are correct.
>
> *Principle applied: P4. The fix guidance is part of the error description. It is not a note. The sentences use descriptive mood followed by imperative mood.*

The compliant error is raised in code like this:

```python
raise ConnectionError(
    "Error: Connection refused. "
    "The database server on port 5432 did not respond. "
    "Check that the server is running. "
    "Make sure that the credentials in the .env file are correct."
)
```

The fix guidance is part of the error text itself (descriptive statement followed by imperative steps), not a separate note that the reader might skip.

### Paradigm-Specific Guidance

The application of this rule changes slightly across programming paradigms. The core principle stays the same: notes give information, not instructions. The form of the note changes with the paradigm's documentation conventions.

#### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Class documentation describes types, their state, and their behavior. Notes in class documentation explain design decisions or constraints on state.

> **Non-STE:** NOTE: After calling `dispose()`, you must not call any other method on this object. Doing so will cause an `ObjectDisposedException`.
>
> **STE:** NOTE: The object enters a disposed state after a call to `dispose()`. Method calls on a disposed object cause an `ObjectDisposedException`.
>
> *Principle applied: P4. The constraint is a property of the object state. It is not an instruction to the reader.*

The compliant docstring reads:

```python
class FileWriter:
    """Write text to a file on disk.

    NOTE: The object enters a disposed state after a call to `dispose()`.
    Method calls on a disposed object cause an `ObjectDisposedException`.
    """
```

#### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional code documents pure functions, type signatures, and data transformations. Notes explain purity constraints or performance characteristics.

> **Non-STE:** NOTE: This function is pure and has no side effects. You can safely memoize it. Re-run it as many times as you want with the same arguments.
>
> **STE:** NOTE: This function is pure. It has no side effects. Repeated calls with the same arguments return the same result.
>
> *Principle applied: P4, P11 (one term per concept). The function's properties are described. The reader is not told what to do.*

The compliant doc comment reads:

```rust
/// Compute the SHA-256 digest of the input bytes.
///
/// NOTE: This function is pure. It has no side effects. Repeated calls with
/// the same arguments return the same result.
pub fn digest(input: &[u8]) -> [u8; 32] {
    // ...
}
```

#### Procedural Documentation (C, Go, Bash)

Procedural code documents sequences of steps. Notes explain state between steps or prerequisites for steps.

> **Non-STE:** NOTE: The file descriptor remains open until you explicitly call `close()`. You must close it to prevent a file descriptor leak.
>
> **STE:** NOTE: The file descriptor stays open until the code calls `close()`. An unclosed file descriptor causes a resource leak.
>
> *Principle applied: P4, P2 (words only as specified part of speech). "Remains" → "stays" for simpler vocabulary.*

The compliant comment reads:

```go
// Open the log file for append access.
//
// NOTE: The file descriptor stays open until the code calls `close()`.
// An unclosed file descriptor causes a resource leak.
f, err := os.OpenFile("app.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
```

#### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documents describe desired state. Notes explain constraints or platform behavior that affects the declared state.

> **Non-STE:** NOTE: The `depends_on` attribute ensures that the database is created before the application. Always set this attribute if your application needs a database.
>
> **STE:** NOTE: The `depends_on` attribute controls resource creation order. Terraform creates the database resource before the application resource when this attribute is set.
>
> *Principle applied: P4. The attribute behavior is described. The instruction "Always set this" is removed.*

The compliant Terraform comment reads:

```hcl
# NOTE: The `depends_on` attribute controls resource creation order.
# Terraform creates the database resource before the application resource
# when this attribute is set.
resource "kubernetes_deployment" "app" {
  metadata { name = "app" }
  depends_on = [kubernetes_deployment.database]
}
```

#### Systems Documentation (Rust Ownership, C Memory)

Systems documentation explains ownership, lifetime, and memory semantics. Notes clarify constraints that the compiler enforces.

> **Non-STE:** NOTE: This function borrows the value immutably. Do not mutate the value while the borrow is active. The compiler will reject your code if you try.
>
> **STE:** NOTE: This function borrows the value immutably. The borrow prevents mutation of the value until the borrow ends. The compiler rejects code that violates this constraint.
>
> *Principle applied: P4, P11. The compiler's behavior is described. The reader is not given instructions.*

The compliant doc comment reads:

```rust
/// Read the length of the buffer without taking ownership.
///
/// NOTE: This function borrows the value immutably. The borrow prevents
/// mutation of the value until the borrow ends. The compiler rejects code
/// that violates this constraint.
pub fn len(buf: &Buffer) -> usize {
    buf.data.len()
}
```

### Extended Examples

Each example shows a Non-STE version that violates the rule and an STE-Code compliant version. The principle applied and a brief explanation follow each pair.

**Example 1: Instructions hidden in a note**

> **Non-STE:** NOTE: The build process generates static assets in the `dist/` directory. Before you run the build, make sure you have Node.js version 18 or higher installed. Run `node --version` to check your current version.
>
> **STE:** (3) Make sure that Node.js version 18 or higher is installed.
>
> *Principle applied: P1, P4. The version check instruction is a work step. The note about static assets is removed because it is not necessary for the procedure.*

The non-STE note appears in a contributor guide like this:

```markdown
## Build

NOTE: The build process generates static assets in the `dist/` directory.
Before you run the build, make sure you have Node.js version 18 or higher
installed. Run `node --version` to check your current version.
```

The compliant guide lists the prerequisite as a numbered step and drops the optional background note:

```markdown
## Build

1. Make sure that Node.js version 18 or higher is installed.
2. Install the dependencies with `npm install`.
3. Build the static assets with `npm run build`.
```

Explanation: The Non-STE version hides a prerequisite check in a note. The reader might skip the note and use an incompatible Node.js version. The STE version makes the check a numbered work step.

**Example 2: Requirement disguised as a note**

> **Non-STE:** NOTE: The authentication token expires after 3600 seconds. You must refresh the token before making any API call that requires authentication.
>
> **STE:** The authentication token is valid for 3600 seconds. After the token expires, the API returns a `401 Unauthorized` status code.
>
> *Principle applied: P4, P5. The token lifetime and the API behavior are descriptive statements. They belong in the endpoint specification, not in a note.*

The compliant API description reads:

```yaml
  /profile:
    get:
      summary: Get the current user profile.
      description: |
        The authentication token is valid for 3600 seconds. After the token
        expires, the API returns a `401 Unauthorized` status code. Send a
        valid bearer token in the `Authorization` header.
      security:
        - bearerAuth: []
```

Explanation: The Non-STE version gives a requirement ("you must refresh") inside a note. The STE version moves the descriptive information about token lifetime and error behavior into the API specification body.

**Example 3: Configuration guidance in a note**

> **Non-STE:** NOTE: The default connection pool size is 10. For high-traffic applications, increase this value to 25 or higher. Set the `POOL_SIZE` environment variable in your `.env` file.
>
> **STE:** NOTE: The default connection pool size is 10.
>
> *Principle applied: P1 (use, not utilize), P2. The tuning guidance is a configuration instruction. It belongs in the configuration reference section, not in a note.*

The compliant note keeps only the descriptive fact, and the tuning guidance moves to a configuration reference table:

```markdown
NOTE: The default connection pool size is 10.

## Configuration

| Variable    | Default | Description                                         |
| ----------- | ------- | --------------------------------------------------- |
| `POOL_SIZE` | `10`    | Set a higher value, such as `25`, for high traffic. |
```

Explanation: The Non-STE version gives tuning instructions in a note. The STE version keeps only the descriptive fact about the default value. The tuning guidance must appear in a dedicated configuration section or work step.

**Example 4: Debugging instructions in a note**

> **Non-STE:** NOTE: If the application fails to start, check the log file at `/var/log/app/error.log`. Look for lines that contain the word "FATAL". Contact the operations team if you see a "connection refused" error.
>
> **STE:** NOTE: The application writes startup errors to the file `/var/log/app/error.log`. Fatal errors start with the word "FATAL" in the log.
>
> *Principle applied: P4, P13 (do not use technical verbs as nouns). The debugging procedure is not a note. The note only describes the log file location and format.*

The compliant project README separates the note from the troubleshooting steps:

```markdown
NOTE: The application writes startup errors to the file `/var/log/app/error.log`.
Fatal errors start with the word "FATAL" in the log.

## Troubleshooting

1. Open `/var/log/app/error.log`.
2. Search for lines that contain the word "FATAL".
3. If you see a "connection refused" error, contact the operations team.
```

Explanation: The Non-STE version gives a troubleshooting procedure inside a note. The STE version describes where errors are logged and what to look for. The troubleshooting procedure must be a separate section with numbered steps.

**Example 5: Migration note with hidden commands**

> **Non-STE:** NOTE: This release adds a new `email_verified` column to the `users` table. Run the migration with `php artisan migrate`. If the migration fails, roll back with `php artisan migrate:rollback` and check your database permissions.
>
> **STE:** NOTE: This release adds a new `email_verified` column to the `users` table.
>
> *Principle applied: P1, P4. The migration commands are work steps. They must be numbered steps in the upgrade procedure.*

The compliant upgrade guide reads:

```markdown
NOTE: This release adds a new `email_verified` column to the `users` table.

## Upgrade

1. Back up the production database.
2. Run the migration with `php artisan migrate`.
3. If the migration fails, roll back with `php artisan migrate:rollback` and
   check your database permissions.
```

Explanation: The Non-STE version embeds run and rollback commands in a note. The STE version only describes the schema change. The migration commands belong in numbered upgrade steps.

**Example 6: Timeout behavior explained incorrectly**

> **Non-STE:** NOTE: The request timeout is 30 seconds by default. Do not set a timeout longer than 60 seconds because the load balancer will drop the connection. Always handle timeout errors in your client code.
>
> **STE:** NOTE: The default request timeout is 30 seconds. The load balancer drops connections that stay open longer than 60 seconds.
>
> *Principle applied: P4, P11. The constraints about maximum timeout and error handling are requirements. They belong in the API specification or client library documentation.*

The compliant client library documentation reads:

```markdown
NOTE: The default request timeout is 30 seconds. The load balancer drops
connections that stay open longer than 60 seconds.

## Client configuration

1. Keep the request timeout at or below 60 seconds.
2. Handle `408 Request Timeout` responses in your client code.
```

Explanation: The Non-STE version gives a constraint and an instruction inside a note. The STE version only describes the default timeout and the load balancer behavior. The constraint and the error handling requirement must appear in the appropriate specification section.

### Edge Cases

The following edge cases describe scenarios where the application of Rule 5.5 requires judgment.

**Edge Case 1: Framework names that look like verbs**

Some framework names are also common verbs. For example, `React`, `Express`, `Spring`, and `Build`. When these names appear in a note, they are technical code nouns (Rule 1.5). They do not make the note an instruction.

> **STE:** NOTE: The `React` component tree re-renders when the state changes. The `Express` middleware stack processes requests in the order of registration.
>
> (Both sentences are descriptive. `React` and `Express` are proper nouns. They are not imperative verbs.)

**Edge Case 2: Generated code documentation**

Documentation generated by tools such as JSDoc, Sphinx, or `go doc` often includes notes from source comments. These generators do not know about this rule. If a generated note contains an instruction, the source comment is the problem. Fix the source comment.

> **Non-STE (source comment):** NOTE: Call this method before any other method on the object.
>
> **STE (source comment):** This method must be the first call on the object.

The compliant source comment reads:

```javascript
/**
 * Prepare the client for use.
 *
 * This method must be the first call on the object. Other method calls
 * before this one raise `NotReadyError`.
 */
prepare() { /* ... */ }
```

Do not rely on the generator to filter or rephrase notes. The rule applies at the source level.

**Edge Case 3: Interactive tutorials and workshops**

Interactive tutorials often use a conversational tone. A note that says "Try changing the value and see what happens" is an instruction. In a tutorial context, this style is acceptable if the note is clearly part of an exploratory exercise and not a required step.

However, for production documentation that ships with a product, follow this rule strictly. Tutorial-style notes are not acceptable in reference documentation, README files, or API specifications.

**Edge Case 4: Notes that reference a command without commanding**

A note can reference a command name as a technical noun without instructing the reader to run it. The distinction is in the sentence structure.

> **STE:** NOTE: The `terraform plan` command shows the changes that Terraform will apply. The output does not include sensitive values.
>
> (Descriptive. The command name `terraform plan` is a technical noun. The sentence describes what the command does. It does not tell the reader to run it.)

> **Non-STE:** NOTE: Run `terraform plan` to see the changes before you apply them.
>
> (Instruction. The sentence tells the reader to do something.)

**Edge Case 5: Notes with conditional descriptive clauses**

A note can describe conditional behavior without giving an instruction. The keyword "if" in a note does not automatically make it an instruction. The test is whether the clause describes what the system does or tells the reader what to do.

> **STE:** NOTE: The server returns a `503 Service Unavailable` status if the upstream service does not respond within 10 seconds.
>
> (Descriptive conditional. The clause describes system behavior. It does not tell the reader to do anything.)

> **Non-STE:** NOTE: If you get a `503 Service Unavailable` status, check the upstream service health endpoint at `/health`.
>
> (Instructional conditional. The clause tells the reader to check something. This is a troubleshooting step, not a note.)

### Grammar Notes

The grammar of notes in code documentation follows the same principles as the original STE rule. The key grammatical distinction is between descriptive mood and imperative mood.

**Descriptive mood:** The subject performs or experiences the action. The sentence states a fact about the system, the code, or the environment. Examples: "The cache expires after 300 seconds." "The function returns a promise."

**Imperative mood:** The reader is the implied subject. The sentence tells the reader to perform an action. Examples: "Run the build command." "Check the log file."

A note must use descriptive mood. If a sentence uses imperative mood, it is not a note. It is a work step or a safety instruction.

**Modal verbs in notes:** The modal verbs "can," "may," and "will" are acceptable in notes when they describe system capability or behavior. The modal verb "must" in a note is a warning sign. It often signals a requirement or constraint that belongs in a work step or safety instruction.

> **STE:** NOTE: The system can process a maximum of 500 concurrent connections.
>
> ("Can" describes capability. Acceptable.)

> **Non-STE:** NOTE: You must close the connection after each request to prevent a memory leak.
>
> ("Must" signals a requirement. This is a safety instruction, not a note. The compliant form is a CAUTION: WARNING: CLOSE THE CONNECTION AFTER EACH REQUEST TO PREVENT A MEMORY LEAK.)

**Sentence length in notes:** Each sentence in a note can have a maximum of 25 words. This constraint comes from the original STE standard. It prevents notes from becoming too dense for the reader to parse quickly. If a descriptive statement needs more than 25 words, split it into two sentences or move the information to the procedure body.

**Article usage in notes:** Do not omit articles (the, a, an) in notes. The note format does not grant an exception to the standard STE-Code article rule. Articles help the reader parse sentence structure and identify nouns.

**Technical code nouns in notes:** Technical nouns such as function names, class names, and command names follow Rule 1.5. They do not need to come from the STE-Code dictionary. However, the words around them must follow STE-Code rules for approved vocabulary and part of speech.

### Cross-References

This rule interacts with several other rules in the STE-Code specification. The most important cross-references are listed below.

- **Rule 1.1 (Approved Words):** Notes must use words from the STE-Code dictionary. The descriptive statements in notes follow the same vocabulary constraints as all other descriptive writing.

- **Rule 1.5 (Technical Code Nouns):** Framework names, function names, and command names in notes are technical code nouns. They do not need dictionary approval.

- **Rule 1.7 (Do Not Use Technical Nouns as Verbs):** A note must not use a technical noun as a verb. For example, a note must not say "The function `arrays` the input" (using "arrays" as a verb).

- **Rule 5.3 (Imperative Form for Instructions):** Work steps use imperative mood. Notes use descriptive mood. The two forms must not be mixed in a note.

- **Rule 5.4 (Descriptive Statement Before the Command):** A work step can start with a descriptive statement followed by an imperative command. A note must not follow this pattern. A note must contain only descriptive statements.

- **Rule 5.6 (Separate Steps for Separate Actions):** If a note contains multiple instructions, those instructions must become separate work steps. Each action gets its own step.

- **Rule 7.1 (Signal Words for Risk Level):** If a note contains information about data loss, security risks, or system damage, it must become a WARNING or CAUTION safety instruction. The signal word must match the risk level.

- **Rule 9.1 (Descriptive Writing):** Notes contain descriptive text. The descriptive writing rules in Section 9 apply fully to notes.

> **See also:** Rule 1.1 — Use Approved Words from the STE-Code Dictionary; Rule 1.5 — Technical Code Nouns; Rule 1.7 — Do Not Use Technical Nouns as Verbs; Rule 5.3 — Imperative (Command) Form for Instructions; Rule 5.4 — Descriptive Statement Before the Command; Rule 5.6 — Separate Steps for Separate Actions; Rule 7.1 — Use an Applicable Word to Identify the Level of Risk; Rule 9.1 — Descriptive Writing Rules
