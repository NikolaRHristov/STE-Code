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
