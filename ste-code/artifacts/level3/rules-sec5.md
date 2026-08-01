# Level 3 — Section 5: Procedural Writing Rules (5.1–5.5)

Scope: how to write procedures in code documentation — README steps, quickstarts,
runbooks, API walkthroughs, docstrings, commit messages, error messages, and CLI help.

Section 5 has five rules:

| Rule | Requirement | One-line test |
| --- | --- | --- |
| 5.1 | Maximum 20 words in a procedural sentence (25 in a note) | Count the words. |
| 5.2 | One instruction per sentence | Count the imperative verbs. |
| 5.3 | Write instructions in the imperative (command) form | Does the sentence start with a base-form verb? |
| 5.4 | Put the condition first, then a comma, then the command | Is the condition before the comma? |
| 5.5 | Notes give information only, never instructions | Can the reader finish the task with the notes removed? |

Counting conventions used throughout Section 5:

- Code blocks, terminal output, and string literals are excluded from word counts.
- A code token inside backticks counts as one word, whatever its length
  (`Result<T, E>` = 1 word; `async fn` = 2 words).
- Hyphenated compounds count as one word (`command-line` = 1 word).
- Numbers, symbols, and parenthetical references count as one word each
  (`(2)` = 1 word; `HTTP/2` = 1 word).
- Procedural sentence: 20-word limit. Descriptive sentence and note: 25-word limit.

---

## Rule 5.1 — Short Sentences (Maximum 20 Words)

> Source: ASD-STE100 Issue 9, Rule 5.1

### Rule

Write short sentences. Use a maximum of 20 words in each procedural sentence.
Warnings and cautions obey the same 20-word limit. Notes (Rule 5.5) may use up
to 25 words per sentence, because notes give information only.

In code documentation, procedures include installation instructions, setup steps,
deployment checklists, debugging workflows, and API usage guides. The reader
executes commands while reading. Long sentences cause skipped actions.

### Apply

- Break a long procedural sentence into shorter sentences. Each sentence covers
  one part of the task.
- Split at the coordinating conjunction. Start the next sentence with
  `Then,`, `Next,`, or `After that,`.
- Move a condition into its own sentence (see Rule 5.4).
- Separate the action from its purpose: instruction first, reason second.
- Convert an enumeration into a bulleted or numbered list. List items are not
  sentences and are not subject to the 20-word limit, but keep them short.

### Examples

> **Non-STE:** Run the database migration script from the project root directory and then restart the application server to apply all pending schema changes to the production environment. (27 words)
>
> **STE:** Run the database migration script from the project root directory. (9 words) Then, restart the application server to apply all pending schema changes. (13 words)

```bash
cd /srv/payments-service
alembic upgrade head
systemctl restart payments.service
```

> **Non-STE:** Set the environment variable HTTP_TIMEOUT to the value 30000 which represents the maximum number of milliseconds that the client will wait for a response from the upstream server. (30 words)
>
> **STE:** Set the environment variable HTTP_TIMEOUT to 30000. (8 words) This value is the maximum wait time in milliseconds for a response from the upstream server. (17 words)

```bash
export HTTP_TIMEOUT=30000
```

> **CAUTION:** IF YOU DELETE THE CONFIGURATION DIRECTORY WITHOUT A BACKUP, YOU CANNOT RESTORE THE APPLICATION SETTINGS TO THEIR PREVIOUS STATE. (18 words)

```bash
cp -r ./config ./config.bak   # back up first
rm -rf ./config               # then delete
```

> **Non-STE:** For more detailed information about the supported authentication methods and their respective configuration parameters in this release, please refer to the official authentication module documentation page. (27 words)
>
> **STE (note, 25-word limit):** For more information about the supported authentication methods, refer to the authentication module documentation. (15 words)

### By document type

**README files.** Installation and quick-start steps. One instruction per step,
each step a command the reader can copy.

> **Non-STE:** Clone the repository to your local machine using the command shown below and then navigate into the newly created project directory before running the setup script. (28 words)
>
> **STE:** Clone the repository to your local machine. (6 words) Then, navigate into the new project directory. (7 words) Run the setup script. (4 words)

```bash
git clone https://github.com/example/payments-service.git
cd payments-service
./setup.sh
```

**API documentation.** Parameter descriptions in tables are descriptive: 25 words.
Setup, authentication, and request-sequencing sentences are procedural: 20 words.

> **Non-STE:** The `page` query parameter accepts a positive integer value that specifies which page of results the server should return in the paginated response to this endpoint. (28 words)
>
> **STE:** The `page` query parameter accepts a positive integer. (8 words) It specifies which page of results to return. (9 words) This is for paginated responses. (6 words)

```http
GET /v1/orders?page=2&page_size=50 HTTP/1.1
Host: api.example.com
Authorization: Bearer ***
```

**Docstrings and inline comments.** Procedural sentences for callers: 20 words.
Return-value and side-effect descriptions: 25 words.

> **Non-STE:** Call this method to initialize the connection pool with the provided configuration and establish the minimum number of idle connections specified in the pool settings before returning control to the caller. (32 words)
>
> **STE:** Call this method to initialize the connection pool. (8 words) Use the provided configuration. (4 words) The method establishes the minimum number of idle connections. (10 words) Then, it returns control to the caller. (8 words)

```python
def init_pool(config: PoolConfig) -> ConnectionPool:
    """Initialize the connection pool.

    Use the provided configuration. The method establishes the minimum
    number of idle connections. Then, it returns control to the caller.
    """
    ...
```

**Commit messages.** Keep the subject line to 72 characters or fewer; this is a
separate constraint from the word count. Body: 20 words for procedural sentences,
25 for descriptive ones.

> **Non-STE:** Refactored the authentication middleware to extract the token validation logic into a separate utility function so that it can be reused by the WebSocket upgrade handler and the GraphQL subscription resolver as well. (35 words)

```text
Refactor authentication middleware

Extracted the token validation logic into a separate utility function.
The WebSocket upgrade handler and the GraphQL subscription resolver now
reuse this function.
```

**Error messages.** Read under stress. Actionable messages: 20 words. Messages that
only report a condition: 25 words. Separate the diagnosis from the remedy.

> **Non-STE:** The configuration file could not be parsed because it contains a syntax error on line 42 that is most likely caused by a missing closing bracket or an unquoted string value containing special characters. (35 words)
>
> **STE:** The configuration file has a syntax error on line 42. (11 words) Check for a missing closing bracket or an unquoted string value. (13 words)

```text
Config error on line 42: missing closing bracket or unquoted string.
```

### By paradigm

**Object-oriented (Java, C++, C#, Python classes).** Do not describe all
constructor parameters in one sentence. Give each parameter its own sentence.

> **Non-STE:** The constructor accepts a database connection string, a logger instance that must implement the ILogger interface, and an optional configuration object for setting the retry policy and the connection timeout duration. (33 words)
>
> **STE:** The constructor accepts three parameters. Parameter one is a database connection string. Parameter two is a logger instance. It must implement the ILogger interface. Parameter three is an optional configuration object. Use this object to set the retry policy and the connection timeout.

```csharp
public DatabaseClient(
    string connectionString,
    ILogger logger,
    ClientConfig? config = null
) { ... }
```

**Functional (Haskell, Elixir, Clojure, Rust).** Give each stage of a composition
pipeline its own sentence, so the reader traces one transformation at a time.

> **Non-STE:** The `process` function first maps the transformation over each element in the list and then filters out any results that are `None` before finally folding the remaining values into a single accumulator using the provided binary operator. (35 words)
>
> **STE:** The `process` function maps a transformation over each element in the list. Then, it filters out any `None` results. Finally, it folds the remaining values into a single accumulator. The provided binary operator controls the fold.

```haskell
process :: (a -> b) -> (b -> Bool) -> (b -> b -> b) -> [a] -> b
process f p op = foldl1 op . filter p . map f
```

**Procedural (C, Go, Bash).** Do not combine an error check with the operation
being checked. Do not describe conditional branching in prose.

> **Non-STE:** Run the configure script to detect your system's available libraries and compiler features and then run make with the -j flag set to the number of CPU cores on your machine to compile the program from source. (37 words)
>
> **STE:** Run the configure script. This script detects your system libraries and compiler features. Then, run make to compile the program from source. Use the -j flag. Set it to the number of CPU cores on your machine.

```bash
./configure
make -j"$(nproc)"
```

**Declarative (SQL, Terraform, Kubernetes YAML).** Do not describe a resource and
all its attributes in one sentence. Check prerequisites before the action.

> **Non-STE:** Execute the migration script against the production database after taking a full backup and verifying that the replication lag on all read replicas is less than five seconds to prevent any data inconsistency during the schema change. (38 words)
>
> **STE:** Take a full backup of the production database. Verify that the replication lag on all read replicas is less than five seconds. Then, execute the migration script against the production database.

```bash
pg_dump "$PROD_DSN" > backup_$(date +%F).sql
REPLICA_LAG=$(psql "$PROD_DSN" -t -c "SELECT EXTRACT(SECONDS FROM now() - pg_last_xact_replay_timestamp());")
[ "$(echo "$REPLICA_LAG < 5" | bc)" -eq 1 ] && alembic upgrade head
```

**Systems (Rust ownership, C memory management).** Never bury a hazard in a
subordinate clause. Prohibition, reason, and consequence each get a sentence.

> **Non-STE:** After calling this function the caller must not use the original buffer pointer because ownership of the memory has been transferred to the callee and any subsequent access through the old pointer will result in undefined behavior. (37 words)
>
> **STE:** After you call this function, do not use the original buffer pointer. Ownership of the memory is transferred to the callee. Access through the old pointer causes undefined behavior.

```rust
fn take_buffer(buf: Vec<u8>) -> Parser {
    // buf is moved into Parser; the caller's buf is no longer valid.
    Parser::new(buf)
}
```

### Edge cases

1. **Long framework or service names.** Use the shortest accepted form on first
   use, define an abbreviation, then use the abbreviation. The abbreviation counts
   as one word. (`Amazon Web Services Elastic Kubernetes Service` → `Amazon EKS`.)
2. **Code keywords that form long phrases.** A backticked token is one word. Do
   not expand generics or type parameters into prose words.
3. **Generated documentation.** Apply the rule to the source docstrings the
   generator reads; the output inherits compliance. Do not edit generated output —
   fix the source. If the source is third-party, apply the 25-word descriptive
   limit and record the exception in the project style guide.
4. **Legal and compliance text.** Not procedural; the 20-word limit does not apply.
   Keep it in a separate "Legal" section or a `NOTE (legal requirement):` block.
5. **Multi-line code examples in prose.** The code block is not counted. The
   introducing sentence and the following sentence each obey the limit
   independently.

### Grammar notes

- A sentence ends with `.`, `?`, or `!`. A comma does not end a sentence.
- Do not join independent clauses with a comma (no comma splices).
- Do not use semicolons to join independent clauses. Use periods.
- Coordinating conjunctions (and, but, or, nor, for, so, yet) may join two short
  clauses only when the total stays at or below 20 words.
  Allowed: `Run the tests and check the output.` (8 words)
- Limit subordinate clause depth to two levels. Flatten deeper structures into
  separate sentences.

> **Non-STE:** The server returns an error when the client sends a request that contains a payload that exceeds the limit that the administrator configured in the settings file. (27 words, 4 levels)
>
> **STE:** The server returns an error when the request payload exceeds the configured limit. The administrator sets this limit in the settings file.

```python
MAX_PAYLOAD = settings["max_payload_bytes"]  # set by the administrator

def handle(req):
    if len(req.body) > MAX_PAYLOAD:
        raise PayloadTooLarge(settings["max_payload_bytes"])
```

### Checklist — Rule 5.1

- [ ] Every procedural sentence has 20 words or fewer.
- [ ] Every note sentence has 25 words or fewer.
- [ ] Warnings and cautions obey the 20-word limit.
- [ ] No comma splices; no semicolons joining independent clauses.
- [ ] Long sentences are split at conjunctions or condition boundaries.
- [ ] Code blocks, terminal output, and string literals are excluded from counts.
- [ ] Backticked code tokens count as one word each.
- [ ] Long technical names are abbreviated after first definition.
- [ ] Generated documentation is fixed at the source level.
- [ ] Subordinate clauses stay within two levels of depth.

> **See also:** Rule 5.2, Rule 5.3, Rule 5.5, Rule 1.1, Rule 1.9, Rule 1.12, Section 8 (word count).

---

## Rule 5.2 — One Instruction Per Sentence

> Source: ASD-STE100 Issue 9, Rule 5.2

### Rule

Write only one instruction in each sentence, unless two or more actions occur at
the same time. Show the sequence of the work steps clearly, usually with numbers
or letters. A procedure may have as many work steps as it needs.

When a sentence carries several instructions, the reader can skip an action. In
code documentation, a skipped action causes a broken configuration, a failed
deployment, or a debugging session that starts from a wrong state.

### Apply

- One instruction for the reader to perform per sentence.
- Use a numbered list to show sequence.
- Join two instructions with "and" only when both actions occur at the same
  moment and cannot be separated.
- You may write more than one sentence in a single work step when:
  - two or more actions occur at the same time and are inseparable, or
  - a result, limit, or measurement follows the action immediately.

Actions that occur at the same time (one sentence is correct):

- Hold the Shift key and click the Reload button.
- Press and release the reset button on the device.
- Copy and replace the existing configuration file.
- Download and extract the archive to the target directory.

### Examples

> **Non-STE:** Open the configuration file in a text editor and locate the database section and change the connection string to point to the staging server and then save the file and close the editor. (37 words, 5 instructions)
>
> **STE:** (1) Open the configuration file in a text editor. (2) Locate the database section. (3) Change the connection string to point to the staging server. (4) Save the file. (5) Close the editor.

```markdown
## Point the app at the staging database

1. Open `config/database.toml` in a text editor.
2. Find the `[database]` section.
3. Set `connection_string = "postgres://staging-db:5432/app"`.
4. Save the file.
5. Close the editor.
```

> **Non-STE:** Run the test suite with the coverage flag enabled and verify that the total line coverage is above 80 percent across all modules in the project. (27 words)
>
> **STE:** Run the test suite with the coverage flag enabled. (9 words) The total line coverage must be more than 80 percent across all project modules. (14 words)
>
> (The second sentence states the result limit. The work step is one action and is not divided.)

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
> (The check and the execution form one continuous work step. The third sentence describes what the script does.)

```markdown
## Set up the local database

Make sure that the `DATABASE_URL` environment variable is set correctly:

    export DATABASE_URL="postgres://localhost:5432/app"

Then, run the initialization script:

    python scripts/init_db.py

The script creates the required tables and loads the seed data.
```

> **Non-STE:** Set the logging level to debug mode and then restart the application server and after that monitor the log output in the terminal for any error messages that appear during the startup sequence. (35 words)
>
> **STE:** (1) Set the logging level to debug. (2) Restart the application server. (3) Monitor the terminal log output for error messages during the startup sequence.

```markdown
## Debug a slow startup

1. Set the logging level to debug in `config/logging.yaml`.
2. Restart the application server: `systemctl restart app-server`.
3. Watch the log output: `journalctl -u app-server -f`.
```

### By document type

- **README files.** Quick-start sections are the most common violation site.
  Turn each verb into its own numbered step, so the reader can copy one command
  at a time.
- **API documentation.** Split authentication, request construction, and response
  handling into separate steps. Do not fold "get a token" into "call the endpoint".
- **Docstrings.** A usage section is a procedure. One call per sentence. Describe
  the return value in its own sentence.
- **Commit messages.** The body may list several changes, but each sentence
  describes one change. Use a bulleted list when the change has several parts.
- **Error messages.** When a failure has several remedies, give each remedy its
  own sentence, not one chained sentence.

### By paradigm

**Object-oriented.** Instantiation guides, dependency injection setup, and mock
configuration all chain method calls. Give each call its own step.

**Functional.** Do not chain "map, then filter, then fold" as one instruction to
the reader. Document each stage separately.

**Procedural (C, Go, Bash).** Comments in build scripts often compress three
actions into one line.

```bash
# Non-STE
# Download the latest release binary, verify its checksum, and move it to
# /usr/local/bin.

# STE
# Download the latest release binary.
curl -LO https://example.com/tool.tar.gz
# Verify the checksum of the downloaded binary.
sha256sum -c tool.tar.gz.sha256
# Move the binary to /usr/local/bin.
sudo mv tool /usr/local/bin/
```

**Declarative (SQL, Terraform, Kubernetes YAML).** A resource comment that lists
every attribute in one sentence violates the rule.

```hcl
# Non-STE
# Creates an S3 bucket with versioning enabled, a lifecycle policy to
# delete old objects after 30 days, and a private ACL.

# STE
# This resource creates an S3 bucket.
# It enables versioning on the bucket.
# It configures a lifecycle policy to delete objects after 30 days.
# It sets the bucket ACL to private.
```

**Systems (Rust ownership, C memory model).** Allocation, use, and release are
three instructions. Never combine them, because a missed step causes a leak or
undefined behavior.

### Edge cases

1. **A framework CLI command that looks like several instructions.** One command
   the reader runs is one instruction, even when the tool performs many actions
   internally. `npx create-next-app --typescript --eslint` is one step.
2. **Error messages with several root causes.** Give one sentence per cause and
   one sentence per remedy. Do not chain them with "or".
3. **Generated or auto-formatted documentation.** Fix the source comment. The
   generator inherits compliance from its input.
4. **Multi-step test assertions.** A test that asserts several conditions is one
   work step for the reader ("Run the test"), but the documented assertions are
   listed one per line.
5. **Console log messages during a multi-step operation.** Each log line reports
   one completed action. Do not report two actions in one line.

### Grammar notes

**Single predicate rule.** Each imperative sentence has exactly one main verb in
the imperative mood.

- Correct: `Install the package.`
- Incorrect: `Install the package and configure the settings.`

**Simultaneous action exception.** Two predicates may share a sentence when the
actions occur at the same moment. Test: if you can insert a pause between the
actions, they are sequential and must be split.

- Simultaneous (allowed): `Hold the Shift key and click the Reload button.`
- Sequential (split): `Install the package and run the tests.`

**Result clause separation.** Move a result clause introduced by "until", "so
that", "to", or "such that" into its own sentence.

- Before: `Run the migration until the output shows "Migration complete".`
- After: `Run the migration. Continue until the output shows "Migration complete".`
- Before: `Set the timeout to 30 seconds so that the connection does not hang.`
- After: `Set the timeout to 30 seconds. This prevents the connection from hanging.`

**Compound objects are not compound instructions.** One verb with several objects
is one instruction.

- Allowed: `Remove the log files, cache files, and temporary directories.`
- Not allowed: `Remove the log files and restart the server.`

**The "-ing" form prohibition.** Gerund phrases hide implied instructions.

- Before: `After installing the package, configuring the environment, and setting up the database, run the application.`
- After:

```text
(1) Install the package.
(2) Configure the environment.
(3) Set up the database.
(4) Run the application.
```

**Subordinate clauses and instruction count.** If a subordinate clause contains an
action the reader must perform, that action is an instruction and needs its own step.

- Before: `Before you run the tests, set the TEST_MODE environment variable to true.`
- After: `(1) Set the TEST_MODE environment variable to true. (2) Run the tests.`
- Before: `After the build completes, deploy the artifact to the staging server.`
- After: `(1) Wait for the build to complete. (2) Deploy the artifact to the staging server.`

### Checklist — Rule 5.2

- [ ] Each procedural sentence has exactly one imperative verb.
- [ ] Sequences use numbered or lettered steps.
- [ ] "and" joins two verbs only for simultaneous, inseparable actions.
- [ ] Result and limit clauses are separate sentences inside the same step.
- [ ] No gerund phrase hides an instruction.
- [ ] No subordinate clause hides a precondition action.

> **See also:** Rule 5.1, Rule 5.3, Rule 5.5, Rule 1.1, Rule 1.12, Rule 1.13.

---

## Rule 5.3 — Imperative (Command) Form for Instructions

> Source: ASD-STE100 Issue 9, Rule 5.3

### Rule

Write instructions in the imperative (command) form. Start each procedural
instruction with a base-form verb.

Other sentence forms cause ambiguity. The reader cannot tell whether a work step
is required, whether somebody else already did it, or whether the system does it
automatically.

Common imperative verbs in code documentation: run, set, open, save, install,
configure, restart, execute, copy, delete, create, add, enter, select, click,
type, check, build, push, test.

Do not use:

- passive voice (`The file is saved.`)
- gerunds as main verbs (`Saving the configuration before deployment.`)
- modal verbs for instructions (can, could, should, may, might, would)
- indirect phrasing (`It is recommended that you...`, `You are to...`)
- `must` before an imperative in a standard instruction

Reserve `must` for security warnings, data-loss cautions, and safety-critical
conditions.

| Do not write: | Before you remove the cache directory, you must stop the service. |
| --- | --- |
| WRITE: | Before you remove the cache directory, stop the service. |
| STE (safety): | WARNING: IF YOU MUST STORE USER PASSWORDS, ALWAYS HASH THEM WITH BCRYPT. DO NOT STORE PASSWORDS IN PLAIN TEXT. |

### Core examples

> **Non-STE:** The test can be continued.
>
> **STE:** Continue the test.

> **Non-STE:** The old log files are to be removed before the new deployment.
>
> **STE:** Remove the old log files. Then, start the deployment.

> **Non-STE:** The configuration file should be validated against the schema before the application is started.
>
> **STE:** Validate the configuration file against the schema. Then, start the application.

> **Non-STE:** The SSL certificate must be renewed and then the web server must be restarted to apply the changes.
>
> **STE:** Renew the SSL certificate. Then, restart the web server to apply the changes.

> **Non-STE:** It is recommended that you create a backup of the database before running the migration script.
>
> **STE:** Before you run the migration script, create a backup of the database.

### By document type

**README files.** A setup section is instructional; an about section is descriptive.
Do not mix the two moods inside a numbered list.

```markdown
## Setup

1. Install the dependencies with `npm install`.
2. Copy `.env.example` to `.env`.
3. Start the development server with `npm run dev`.
```

**API documentation.** Quickstarts use the imperative. Endpoint behavior is
descriptive: `The endpoint returns a 201 status code.`

**Docstrings and inline comments.** A comment that tells the reader (or the next
maintainer) to act uses the imperative.

```dockerfile
# Build the production Docker image.
docker build -t myapp:prod .
```

**Commit messages.** Write the subject line in the imperative, as an instruction
to the codebase.

```text
# Non-STE commit log
Fixed the login bug
Adding retry logic

# STE commit log (git log --oneline)
Fix the login redirect loop
Add retry logic to the payment client
```

**Error messages.** Describe the failure in the descriptive mood, then give the
recovery step in the imperative.

```text
# Non-STE: a bare, unrecoverable string
ERROR: bad config

# STE: failure, then instruction
Config error on line 42: missing closing bracket. Fix the syntax, then restart the service.
```

### Grammar notes

**Subject omission.** The imperative omits "you". The implied subject is always
the reader, so there is no ambiguity about who acts. Passive constructions hide
the agent. Gerunds function as nouns and describe an action as a concept, not as
a directive.

**Modal verb elimination.** Modals express possibility, permission, or
recommendation. In instructions they create doubt. `You can set the timeout to 30
seconds` reads as optional; `Set the timeout to 30 seconds` does not. `Must` is
redundant before an imperative, because the imperative already conveys necessity.

**Tense consistency.** The imperative uses the base verb form. It does not inflect
for tense, number, or person. This helps translation, machine processing, and
non-native readers.

**Coordination with Rule 5.4.** A descriptive statement may set the context before
the imperative command. Each sentence then has a distinct grammatical role.

```bash
# Descriptive: states a required condition.
# The Docker daemon must be running.
# Imperative: gives the action.
docker build -t myapp:dev .
```

### By paradigm

**Object-oriented.** Setup and configuration use the imperative. Class invariants,
inheritance hierarchies, and design rationale stay descriptive.

> **Non-STE:** An instance of the DatabaseConnection class can be created by calling the static factory method `create`, and you should pass a valid connection string.
>
> **STE:** Create an instance of the `DatabaseConnection` class with the static factory method `create`. Pass a valid connection string.

**Functional.** Project setup, build tool usage, and REPL walkthroughs use the
imperative. Function descriptions stay declarative, because they describe
transformations rather than commands to the reader.

> **Non-STE:** You should apply `map` to transform the list and then you can pipe the result into `filter`.
>
> **STE:** Apply `map` to transform the list. Then, pipe the result into `filter`.

NOTE: When you document a function that the reader must call, the imperative form
is correct. When you document what a function does internally, the descriptive
form is correct.

**Procedural (C, Go, Bash).** Build steps, compile flags, and linking instructions
are all reader actions, so the imperative dominates.

> **Non-STE:** The binary can be compiled with `gcc -O2 -Wall main.c -o tool` and then you are to place it in `/usr/local/bin`.
>
> **STE:** Compile the binary with `gcc -O2 -Wall main.c -o tool`. Then, move the binary to `/usr/local/bin`.

**Declarative (SQL, Terraform, Kubernetes YAML).** The manifest itself is
descriptive: it states desired state. The operator workflow that applies the
manifest is imperative.

```bash
kubectl apply -f deployment.yaml
kubectl rollout status deployment/web
```

**Systems (Rust ownership, C memory management).** Safety instructions use the
imperative and, when the consequence is severe, the `must` form inside a WARNING.

```text
WARNING: DO NOT USE THE BUFFER POINTER AFTER YOU MOVE THE BUFFER.
ACCESS AFTER A MOVE CAUSES UNDEFINED BEHAVIOR.
```

### Extended examples

**Gerund as instruction (Docker docs).**

```text
# Non-STE (reads like a status, not an action)
# Building the image with --no-cache to ensure a clean build.

# STE (direct command the reader runs)
# Build the image with --no-cache to make sure that the build is clean.
docker build --no-cache -t myapp .
```

**Passive voice in a pipeline step (CI/CD docs).** Describe what the pipeline does
in the descriptive mood; give the local runbook in the imperative.

```text
# Descriptive: system behavior
# The CI pipeline runs the test suite after each push to the main branch.

# STE (local runbook for the reader)
# To run the tests locally, run npm test.
```

**"Must" misuse in a standard procedure (database migration).**

```text
# STE (deploy checklist)
Before you deploy to production:
  back up the database
  run the migration script
  notify the on-call engineer
```

**Indirect phrasing in a README (open-source project).**

```markdown
## Contributing

1. Fork the repository.
2. Create a feature branch from `main`.
3. Add tests for your change.
4. Open a pull request.
```

**Conditional imperative in a security-critical context.**

```text
# Non-STE
# When handling user passwords, you should hash them with bcrypt
# and you must never store them in plain text.

# STE
# WARNING: IF YOU MUST STORE USER PASSWORDS, ALWAYS HASH THEM WITH BCRYPT.
# DO NOT STORE PASSWORDS IN PLAIN TEXT. PLAIN-TEXT PASSWORDS CAN CAUSE DATA BREACHES.
```

### Edge cases

1. **A framework name that is also a verb.** `React`, `Express`, `Spring`, `Build`,
   `Watch` are technical code nouns (Rule 1.5) when they name a product. They do
   not turn a descriptive sentence into an instruction.
2. **Generated code and tool output.** Write `--help` text in the imperative at
   the source. Do not post-edit the generated output.
3. **Code keywords that conflict with the rule.** A keyword such as `return`,
   `import`, or `yield` inside backticks is a code token, not the sentence verb.
4. **Release notes and changelogs.** These describe completed work, so they use
   the past or descriptive form, not the imperative. Migration instructions inside
   a release note do use the imperative.
5. **Interactive tutorials and walkthroughs.** Exploratory prompts are acceptable
   in a tutorial. Reference documentation, README files, and API specifications
   follow the rule strictly.

### Checklist — Rule 5.3

- [ ] Every instruction starts with a base-form imperative verb.
- [ ] No passive voice in a procedural sentence.
- [ ] No gerund used as a main verb in an instruction.
- [ ] No modal verb (can, should, may, might) used to give an instruction.
- [ ] `must` appears only in WARNING or CAUTION content, or in a critical condition.
- [ ] Descriptive statements about system behavior stay in the descriptive mood.

> **See also:** Rule 5.1, Rule 5.2, Rule 5.4, Rule 5.5, Rule 1.5, Rule 7.1.
