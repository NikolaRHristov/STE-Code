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

> **Non-STE:** Open the configuration file in a text editor and locate the database section and change the connection string to point to the staging server and then save the file and close the editor. (37 words, 5 instructions)
>
> **STE:** (1) Open the configuration file in a text editor. (2) Locate the database section. (3) Change the connection string to point to the staging server. (4) Save the file. (5) Close the editor.
>
> (Each instruction is a separate work step.)
>
> *Source pairing: split one compound instruction into separate numbered work steps — follows the same principle as the original STE example in Rule 5.2.*

> **Non-STE:** Run the test suite with the coverage flag enabled and verify that the total line coverage is above 80 percent across all modules in the project. (27 words)
>
> **STE:** Run the test suite with the coverage flag enabled. (9 words) The total line coverage must be more than 80 percent across all project modules. (14 words)
>
> (The second sentence states the result limit. The work step is one action and cannot be divided into two separate work steps.)
>
> *Source pairing: a result or limit that follows the action immediately in the same work step — follows the same principle as the original STE example in Rule 5.2.*

> **Non-STE:** Make sure the environment variable DATABASE_URL is set correctly and then execute the initialization script to create the required database tables and populate them with the seed data. (31 words)
>
> **STE:** Make sure that the environment variable DATABASE_URL is set correctly. Then, execute the initialization script. The script creates the required database tables and populates them with the seed data.
>
> (The check and the execution form one continuous work step. The third sentence explains what the script does.)
>
> *Source pairing: a check that is immediately followed by the related action in one work step — follows the same principle as the original STE example in Rule 5.2.*

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

## Code-Domain Explanation

This rule operates differently across the five primary code documentation types. Each type has a distinct audience, reading pattern, and failure mode when instructions are combined in a single sentence.

### README Files

README files serve as the entry point for new users and contributors. Readers scan README sections quickly — often while simultaneously typing commands in a terminal. When a sentence embeds multiple instructions, the reader must pause, re-read, and decompose the compound instruction into individual actions. This increases the probability that a step is skipped or executed out of order.

Every numbered step in a README quick-start or installation section must contain exactly one instruction. If a step produces a result that must be checked, state the result in a second sentence within the same numbered step (as allowed by the result-immediately-after-action exception).

Example of a correctly structured README setup section:

```
(1) Install the package with pip.
(2) Copy the example configuration file to your project root.
    The file includes default values for all settings.
(3) Set the DATABASE_URL environment variable.
(4) Run the initialization command.
    The command creates the required database tables.
```

Do not write:

```
(1) Install the package with pip and copy the example config file and set DATABASE_URL.
```

### API Documentation

API reference documentation describes discrete operations. Each endpoint, method parameter, return value, and error condition must be described in its own sentence. When an endpoint description combines the HTTP method, request body format, authentication requirement, and expected response into one paragraph, the reader must mentally partition the information — a task that generates errors during integration.

Each API documentation block should follow this sentence structure:

- Sentence 1: What the endpoint does (one operation).
- Sentence 2: The HTTP method and path.
- Sentence 3: Required authentication or headers.
- Subsequent sentences: One per request body field, one per query parameter, one per response field, one per error code.

### Docstrings

Docstrings (Python, Java, Rust, Go, and similar) have a constrained format. The first line is a single-sentence summary of what the function or class does. If the summary contains multiple instructions joined by "and", it violates Rule 5.2.

The body of the docstring may contain multiple sentences, but each must describe one aspect of the function's contract:

- One sentence for each parameter.
- One sentence for the return value.
- One sentence for each raised exception or error condition.
- One sentence for each side effect or precondition.

**Non-STE docstring:**

```
def connect(db_url, timeout):
    """Connect to the database using the given URL and configure the
    connection pool with the specified timeout and start the background
    health check thread."""
```

**STE-Code docstring:**

```
def connect(db_url, timeout):
    """Open a connection to the database at the given URL.
    Configure the connection pool with the specified timeout.
    Start the background health check thread."""
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

### Error Messages

Error messages must state exactly one problem. When an error message combines multiple failure conditions, the reader cannot determine which condition triggered the error or which corrective action to take first.

Each error message must:

- State what went wrong (one condition).
- State what action to take (one instruction), if applicable.
- Not combine multiple failure paths with "or", "and", or "also".

**Non-STE error message:**

```
ERROR: The database connection failed and the retry limit was exceeded or the
configuration file is missing required fields.
```

**STE-Code error messages (two separate conditions):**

```
ERROR: The database connection failed. The retry limit of 3 attempts was exceeded.
```

```
ERROR: The configuration file is missing required fields: host, port, database.
```

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Class documentation must separate construction, configuration, and invocation instructions. A constructor's documentation should describe initialization in one sentence per parameter. Method documentation must describe the method's single responsibility in the summary sentence, then elaborate with one sentence per precondition, side effect, and postcondition.

When documenting a class that requires a multi-step setup sequence (e.g., factory pattern, builder pattern), number each step. Do not chain method calls in a single prose sentence.

**Non-STE class setup:**

```
Create a new HttpClient instance, set the timeout and retry policy, and then
call the execute method with the request object.
```

**STE-Code class setup:**

```
(1) Create a new HttpClient instance.
(2) Set the timeout property.
(3) Set the retry policy.
(4) Call the execute method with the request object.
```

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional code documentation describes pure transformations. Each function's documentation must describe one transformation. When documenting a pipeline or composition of functions, describe each stage in its own sentence — do not combine multiple map/filter/reduce operations into one explanatory sentence.

Function signatures in functional languages often express multiple constraints. Document each type parameter, each constraint, and each argument in its own sentence.

**Non-STE pipeline description:**

```
This function filters the list to remove null values and then maps each
remaining element through the parser and collects the successful results.
```

**STE-Code pipeline description:**

```
This function removes null values from the list. It maps each remaining
element through the parser. It collects the successful results.
```

### Procedural Documentation (C, Go, Bash)

Procedural code executes statements sequentially. The documentation for procedural code must mirror this sequential nature: one documented step per executable statement. Bash script comments are especially vulnerable to multi-instruction compression because script authors often write one comment block before a sequence of commands.

**Non-STE Bash comment:**

```
# Download the latest release binary, verify its checksum, and move it to
# /usr/local/bin.
```

**STE-Code Bash comments:**

```
# Download the latest release binary.
# Verify the checksum of the downloaded binary.
# Move the binary to /usr/local/bin.
```

Each comment sits on the line immediately before the command it describes.

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative configurations describe desired state. Each resource, each property, and each constraint must be described in its own sentence. When a Terraform resource documentation block combines the resource's purpose, required arguments, optional arguments, and output attributes into one paragraph, the reader must disentangle the information before they can write the configuration.

**Non-STE Terraform resource docs:**

```
This resource creates an S3 bucket with versioning enabled and configures a
lifecycle policy to delete old objects after 30 days and sets the bucket ACL
to private.
```

**STE-Code Terraform resource docs:**

```
This resource creates an S3 bucket. It enables versioning on the bucket.
It configures a lifecycle policy to delete objects after 30 days. It sets
the bucket ACL to private.
```

### Systems Documentation (Rust Ownership, C Memory Model)

Systems documentation describes invariants, guarantees, and safety conditions. Each invariant must be stated in its own sentence because combining multiple invariants obscures which condition applies to which component. Rust ownership documentation is particularly sensitive: a sentence that combines borrowing rules, lifetime constraints, and safety guarantees can cause the reader to misunderstand the memory model.

**Non-STE ownership docs:**

```
The function borrows the buffer immutably for the duration of the read
operation and returns a reference to the parsed data that is valid for the
lifetime of the input buffer.
```

**STE-Code ownership docs:**

```
The function borrows the buffer immutably for the duration of the read
operation. It returns a reference to the parsed data. The returned reference
is valid for the lifetime of the input buffer.
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

### Example 2: Docker Compose Quick-Start

> **Non-STE:** Clone the repository to your local machine and then navigate into the project directory and run docker compose up to start all the services and after that open your browser and go to http://localhost:3000 to see the application. (38 words, 5 instructions)
>
> **STE:** (1) Clone the repository to your local machine. (2) Go to the project directory. (3) Run `docker compose up` to start all the services. (4) Open a browser. (5) Go to http://localhost:3000.
>
> **Principle applied:** Rule 5.2 (one instruction per sentence) and Rule 1.12 (technical verbs: clone, run are allowed).
>
> **Explanation:** The Non-STE version uses "and then" / "and after that" to chain five sequential actions. The STE version assigns a numbered step to each action. The infinitive phrase "to start all the services" is preserved in step (3) as a purpose clause, which is not an instruction.

### Example 3: Configuration File Editing Guide

> **Non-STE:** Open the .env file in your preferred text editor and locate the line that starts with JWT_SECRET and replace the placeholder value with a randomly generated 256-bit key that you can create using the openssl rand -hex 32 command and then save the file and restart the application server for the changes to take effect. (52 words, 5 instructions)
>
> **STE:** (1) Open the .env file in a text editor. (2) Find the line that starts with `JWT_SECRET`. (3) Replace the placeholder value with a new secret key. To generate a key, run: `openssl rand -hex 32`. (4) Save the file. (5) Restart the application server. The changes take effect after the restart.
>
> **Principle applied:** Rule 5.2 and the result-immediately-after-action exception. Also Rule 1.1 (use approved words: "find" not "locate", "make" not "create").
>
> **Explanation:** The key-generation instruction is separated from the replacement instruction. The final sentence states the result (changes take effect) as a separate descriptive sentence within step (5).

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

### Example 5: CI/CD Pipeline Step Documentation

> **Non-STE:** The build stage compiles the TypeScript source files and runs the unit tests with Jest and then packages the application into a Docker image and pushes it to the container registry with the git commit SHA as the image tag. (38 words, 4 actions described)
>
> **STE:** The build stage has four steps: (1) Compile the TypeScript source files. (2) Run the unit tests with Jest. (3) Package the application into a Docker image. (4) Push the image to the container registry. The image tag is the git commit SHA.
>
> **Principle applied:** Rule 5.2. Descriptive sentences (building the pipeline documentation) must also obey the one-instruction-per-sentence rule when they describe a sequence of actions.
>
> **Explanation:** Even when documenting an automated pipeline (not instructing a human), describing actions one per step improves clarity and maintainability. The final sentence is a descriptive detail, not an instruction.

### Example 6: Git Workflow Documentation

> **Non-STE:** Create a new feature branch from the main branch and make your code changes on that branch and then commit your changes with a descriptive message and push the branch to the remote repository and open a pull request against the main branch. (40 words, 5 instructions)
>
> **STE:** (1) Create a new feature branch from the `main` branch. (2) Make your code changes on the feature branch. (3) Commit your changes with a descriptive message. (4) Push the branch to the remote repository. (5) Open a pull request against the `main` branch.
>
> **Principle applied:** Rule 5.2. Each git operation is a discrete action that the user executes as a separate command.
>
> **Explanation:** This is the most common violation in open-source contributing guides. Writers compress the entire git workflow into one or two sentences. The STE version mirrors how the user actually works: one command, one step, one sentence.

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
```

Over this:

```javascript
/**
 * Creates a new user account with the given username and email and returns
 * the user object.
 */
```

The first style generates one sentence per parameter automatically. The second style generates a compound sentence that may violate Rule 5.2.

### Edge Case 4: Multi-Step Test Assertions

Test case descriptions and assertion messages often combine multiple conditions. When documenting test cases, describe each assertion in its own sentence. When writing assertion messages, use one message per assertion.

**Non-STE test description:**

```
Test that the login endpoint returns 200 and sets the session cookie and
redirects to the dashboard.
```

**STE-Code test description:**

```
This test checks three conditions:
(1) The login endpoint returns status code 200.
(2) The response sets the session cookie.
(3) The response redirects to the dashboard.
```

### Edge Case 5: Console Log Messages During Multi-Step Operations

When a script or CLI tool logs progress during a multi-step operation, each log message should describe one completed step — not what will happen next.

**Non-STE log output:**

```
INFO: Connecting to the database and running migrations and seeding data...
```

**STE-Code log output:**

```
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

```
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
