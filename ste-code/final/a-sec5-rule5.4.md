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

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** Rule 1.4 — Use Only the Approved Forms of Verbs and Adjectives
> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category
> **See also:** Rule 5.3 — Imperative (Command) Form for Instructions
> **See also:** Rule 5.4 — Descriptive Statement Before the Command
> **See also:** Rule 5.5 — Notes Give Information Only, Not Instructions

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


> *Adapted from spec pair:* Non-STE: Put preservation oil into the unit through the vent hole until the oil level is approximately 6 mm (0.24 inches) below the surface of the flange cover._ (25 words)  |  STE: Put preservation oil into the unit through the vent hole. (10 words) Continue until the oil level is approximately 6 mm (0.24 in) below the surface of the flange cover. (16 words)
### Examples

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

> *Adapted from spec: comma placement guidance — the comma shows where the condition ends and the main clause begins.*

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

#### Example 2 — Database Migration Rollback

> **Non-STE:** You can manually revert the migration by executing the down script but first make sure that no other instances of the application are currently connected to the database because concurrent schema changes will corrupt the migration history table.
>
> **STE:** Before you run the down script, make sure that no other application instances connect to the database. Then, run the down script to revert the migration.
>
> *Principle applied: P1 ("run" instead of "execute," "make sure" instead of "verify that" per synonym table context), P5 (down script as technical noun). The condition "Before you run the down script" comes first. Two separate sentences keep each step clear. The NOTICE "Concurrent schema changes can corrupt the migration history table" is implied but could be added as a separate NOTE line.*

#### Example 3 — Terraform Infrastructure as Code

> **Non-STE:** The apply command will provision all the resources defined in your configuration files in the correct dependency order but you should always run terraform plan first to preview the changes and make sure that no unexpected resource destruction will happen.
>
> **STE:** Before you run `terraform apply`, run `terraform plan`. Check the plan output for unexpected resource destruction. If the plan is correct, run `terraform apply`.
>
> *Principle applied: P2, P5 (terraform commands as technical nouns), P8. Three separate steps. Each condition-command pair is its own sentence. "Before you run `terraform apply`, run `terraform plan`" places the prerequisite condition first.*

#### Example 4 — Kubernetes Pod Troubleshooting

> **Non-STE:** To figure out why the pod keeps restarting you should describe the pod to see its events and check the logs of the previous container instance with the --previous flag if the current container is still running.
>
> **STE:** If a pod restarts again and again, get its events. Run `kubectl describe pod <name>`. To see the logs from the previous container instance, use the `--previous` flag.
>
> *Principle applied: P1 ("get" instead of "to figure out," "use" instead of "check"), P5 (kubectl, pod as technical nouns), P8. The condition "If a pod restarts again and again" comes first. The infinitive phrase "To see the logs..." is an alternative condition form. Both place the condition before the command.*

#### Example 5 — SQL Query Documentation

> **Non-STE:** The UPDATE statement modifies rows in the specified table but you must always include a WHERE clause unless you intend to update every single row in the table which is rarely the desired behavior in a production database.
>
> **STE:** Always include a `WHERE` clause in an `UPDATE` statement. If you do not include a `WHERE` clause, the statement updates all rows in the table.
>
> *Principle applied: P1, P5 (SQL keywords as technical nouns), P8. Two sentences. The first is a direct command (Rule 5.3 — imperative form). The second uses condition-before-command: "If you do not include a `WHERE` clause" comes first, then the descriptive result. This warns the reader about the consequence of violating the instruction.*

#### Example 6 — Git Workflow Documentation

> **Non-STE:** You should rebase your feature branch onto the latest main branch to incorporate upstream changes and resolve any merge conflicts locally instead of during the pull request review process but only after you have committed or stashed all of your current work.
>
> **STE:** Before you rebase your feature branch, commit or stash your current work. After you commit or stash your work, rebase your feature branch onto the latest `main` branch. If merge conflicts occur, resolve them locally.
>
> *Principle applied: P1 ("rebase" as technical verb per P12), P5 (branch as technical noun), P8. Three separate condition-command pairs. Each condition comes first. The comma separates the condition from the command in every sentence. The original nested three conditions inside one sentence, violating the one-condition-per-step principle.*

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

For constructor documentation, state the preconditions that must be true before object creation.

> **Non-STE:** Constructs a new HttpClient instance with the provided configuration. The configuration object must not be null and must have at least a base URL set otherwise an IllegalStateException will be thrown at construction time.
>
> **STE (Java):** Make a new `HttpClient` instance with the specified configuration. If the configuration is `null`, the constructor throws `IllegalStateException`. If the base URL is not set, the constructor throws `IllegalStateException`.
>
> *Principle applied: P1 ("make" instead of "constructs"), P5 (`HttpClient`, `IllegalStateException` as technical nouns). Each error condition is a separate condition-result pair.*

### Functional Programming (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, type signatures, and data transformations. Conditions in functional documentation often appear as guard clauses, pattern match descriptions, or type constraints.

State the input condition before describing the transformation. Use the condition-before-command pattern even when the "command" is a descriptive statement about function behavior.

> **Non-STE:** The function returns the head of the list if the list is non-empty and returns Nothing when given an empty list.
>
> **STE (Haskell):** If the list is not empty, the function returns `Just (head list)`. If the list is empty, the function returns `Nothing`.
>
> *Principle applied: P1, P5 (Haskell types as technical nouns). Each case is a condition-before-result pair. The comma separates the condition from the result clause.*

> **Non-STE:** unwrap_or() returns the contained Some value or a provided default if the Option is None and panics if called on a None value with unwrap() instead of unwrap_or().
>
> **STE (Rust):** If the `Option` is `Some(value)`, `unwrap_or(default)` returns `value`. If the `Option` is `None`, `unwrap_or(default)` returns `default`. NOTE: Do not use `unwrap()` on a `None` value. `unwrap()` causes a panic on `None`.
>
> *Principle applied: P5 (Rust types and methods as technical nouns), P8. Each branch is a separate condition-result pair. The NOTE uses imperative form (Rule 5.5 — notes give information, not instructions; here the instruction is acceptable as a warning).*

### Procedural Programming (C, Go, Bash)

Procedural documentation describes sequences of steps, resource lifecycle, and error handling. Conditions in procedural code are often system-state checks, file existence tests, or return-code evaluations.

State the system-state condition before the action. In Bash scripts and Makefiles, the condition-before-command pattern maps directly to shell constructs, but documentation should still use natural-language condition clauses.

> **Non-STE:** The function reads the entire contents of the file at the given path into memory and returns it as a byte slice but callers must ensure the file exists and is readable before calling this function otherwise it returns an error.
>
> **STE (Go):** Read the file at `path` into memory. Return the contents as a `[]byte`. If the file does not exist, the function returns an error. If the file is not readable, the function returns an error.
>
> *Principle applied: P1 ("read" instead of "reads"), P5 (Go type notation as technical noun). The precondition "If the file does not exist" comes before the result clause.*

> **Non-STE:** Kill the process using the PID from the lockfile after checking that the process is actually still running and the PID hasn't been reused by the operating system for a different process.
>
> **STE (Bash script comment):** If the process is still running, stop it. Use the PID from the lockfile. Before you stop the process, make sure that the PID is correct.
>
> *Principle applied: P1 ("stop" instead of "kill"), P5 (PID as technical noun). The condition "If the process is still running" comes first, followed by the command "stop it."*

### Declarative Programming (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state, not procedural steps. However, operational documentation for declarative tools (how to apply a Terraform plan, how to run a migration) still uses procedural language. Condition-before-command applies to the operational wrapper, not the declarative specification itself.

> **Non-STE:** Run terraform destroy to tear down all the infrastructure defined in your state file after you have backed up any important data and confirmed that no other teams depend on the resources you are about to destroy.
>
> **STE:** Before you run `terraform destroy`, back up all important data. Make sure that no other teams use the resources. Then, run `terraform destroy`.
>
> *Principle applied: P1, P5 (`terraform destroy` as technical noun). Three sentences. The condition "Before you run `terraform destroy`" comes first. Each prerequisite is its own step.*

For SQL documentation, state the condition for a query or mutation before the statement.

> **Non-STE:** The DELETE FROM statement removes rows from the table but you must run it inside a transaction if you want to be able to roll back the deletion in case you made a mistake with the WHERE clause.
>
> **STE:** Run `DELETE FROM` inside a transaction. If you do not use a `WHERE` clause, the statement removes all rows. If the `WHERE` clause is incorrect, you can roll back the transaction.
>
> *Principle applied: P1, P5 (SQL keywords as technical nouns). The imperative command "Run `DELETE FROM` inside a transaction" comes first (Rule 5.3). The conditions "If you do not use..." and "If the `WHERE` clause is incorrect..." each precede their result clauses.*

### Systems Programming (Rust Ownership, C Memory Management)

Systems documentation describes memory models, ownership semantics, and safety invariants. Conditions in systems documentation are often safety constraints, lifetime requirements, or synchronization prerequisites. Misreading a condition in systems documentation can cause undefined behavior, data races, or security vulnerabilities.

State the safety condition before the operation. Use WARNING or BREAKING prefixes when the consequence of violating the condition is severe.

> **Non-STE:** You can call unsafe functions but only after manually verifying that all the safety invariants documented in the function's safety section are upheld by the calling code.
>
> **STE (Rust):** Before you call an `unsafe` function, read its safety documentation. Make sure that your code upholds all documented safety invariants. WARNING: IF YOUR CODE DOES NOT UPHOLD THE SAFETY INVARIANTS, THE PROGRAM CAN HAVE UNDEFINED BEHAVIOR.
>
> *Principle applied: P5 (Rust keyword as technical noun), P8. The condition "Before you call an `unsafe` function" comes first. The WARNING uses the condition-before-command pattern inside a safety instruction (see Rule 7.2).*

> **Non-STE:** Call free() on the pointer to release the dynamically allocated memory back to the heap after making absolutely sure that no other part of the program still holds a reference to that memory because use-after-free is a critical security vulnerability.
>
> **STE (C):** Before you call `free(ptr)`, make sure that no other code uses `ptr`. WARNING: IF YOU CALL `free(ptr)` AND OTHER CODE STILL USES `ptr`, THE PROGRAM CAN HAVE A USE-AFTER-FREE VULNERABILITY. AFTER YOU CALL `free(ptr)`, DO NOT USE `ptr`.
>
> *Principle applied: P1 ("call" as approved verb), P5 (C function as technical noun). The condition "Before you call `free(ptr)`" comes first. The WARNING and the final command both follow the condition-before-command pattern.*

## Edge Cases

### Edge Case 1 — Framework Name Is Also a Common Word

Some framework names are common English words that might appear in the STE-Code approved word list with a different meaning. When a framework name conflicts with an approved word, the framework name takes priority as a technical code noun under Rule 1.5. The comma placement rule still applies to the condition clause that contains the framework name.

> **Non-STE:** Before you start the Next.js development server you must set the environment variables in the .env.local file because Next.js reads them at startup and caches them for the entire lifetime of the process.
>
> **STE:** Before you start the Next.js development server, set the environment variables in the `.env.local` file.
>
> *Principle applied: P5 (Next.js as framework name), P1. The word "start" is an approved STE-Code verb. "Next.js" is a framework name that includes a period, which is acceptable as a technical noun. The comma after "server" separates the condition from the command.*

> **Non-STE:** When you run the Express app in production mode it loads the production middleware stack that excludes the development-only error handler and the hot module replacement plugin.
>
> **STE:** When you run the Express application in production mode, it loads the production middleware stack.
>
> *Principle applied: P5 (Express as framework name). "Express" is both an English word and a framework name. In code documentation, it is a technical noun. The condition "When you run the Express application in production mode" comes first, separated by a comma.*

### Edge Case 2 — Code Keyword Inside the Condition Clause

Code keywords, function names, and variable names are technical nouns under Rule 1.5. When they appear inside a condition clause, the comma placement rule still applies. The reader must be able to identify where the condition ends and the command begins, even when the condition contains punctuation characters (backticks, parentheses, dots).

> **Non-STE:** If `someCondition && anotherCondition || fallbackFlag` evaluates to true you can safely proceed with the state transition.
>
> **STE:** If `someCondition && anotherCondition || fallbackFlag` is `true`, start the state transition.
>
> *Principle applied: P5 (code expression as technical noun). The condition clause contains a code expression with `&&`, `||`, and backticks. The comma after `` `true` `` separates the condition from the command. The reader can see where the condition ends because the comma follows the closing backtick.*

> **Non-STE:** When `response.status === 429` the client should wait for the duration specified in the `Retry-After` header before retrying the request.
>
> **STE:** When `response.status === 429`, wait for the duration in the `Retry-After` header. Then, send the request again.
>
> *Principle applied: P5 (JavaScript expression as technical noun), P1 ("send... again" instead of "retrying"). The comma after the code expression `response.status === 429` (inside backticks) separates the condition from the command. Two sentences keep each action clear.*

### Edge Case 3 — Condition Clause Contains a Comma for a Different Reason

Sometimes a condition clause itself contains a comma (for example, a list of items). In this case, do not rely on the comma alone to separate the condition from the command. Use a stronger delimiter, restructure the sentence, or break it into multiple sentences.

> **Non-STE:** If you change the database schema, the API contract, or the message queue format, you must update the corresponding version number in the configuration file.
>
> **STE:** The database schema, the API contract, and the message queue format are part of the system interface. If you change one or more of these parts, update the version number in the configuration file.
>
> *Principle applied: P1, P8. The condition clause "If you change the database schema, the API contract, or the message queue format" contains internal commas (list separators). Adding another comma after "format" would create ambiguity. The STE version introduces the list in a separate descriptive sentence, then uses a simple condition clause "If you change one or more of these parts" that has no internal commas.*

Alternative approach: use a semicolon-free restructuring.

> **STE (alternative):** Before you change the database schema, the API contract, or the message queue format, update the version number in the configuration file.
>
> *This works when the condition is short enough that the reader can parse both the list commas and the separating comma. Use this pattern only when the condition clause has at most one internal comma. For longer lists, use the two-sentence approach above.*

### Edge Case 4 — Condition Implied by Tool Output

Some documentation assumes the reader observes a condition from tool output (a log message, a status code, a test result). When the condition is implied by observable output, state the observable output as the condition clause.

> **Non-STE:** If you see the error message "Connection refused" when you try to connect to the database then the database server is probably not running so you need to start it.
>
> **STE:** If the terminal shows "Connection refused," start the database server.
>
> *Principle applied: P1 ("shows" instead of "you see"). The condition "If the terminal shows 'Connection refused'" comes first, separated by a comma. The observable output is the condition.*

> **Non-STE:** You'll know the build succeeded when you see "BUILD SUCCESSFUL" in the terminal output at which point you can proceed to deploy the artifact to the staging environment.
>
> **STE:** When the terminal shows "BUILD SUCCESSFUL," deploy the artifact to the staging environment.
>
> *Principle applied: P1, P5 (build output string as technical noun). The observable condition comes first. The comma separates it from the command.*

### Edge Case 5 — Generated Code and Automated Documentation

Generated documentation (from tools like Sphinx, JSDoc, godoc, or rustdoc) cannot always follow the condition-before-command pattern because the generation tool extracts text from source code in a fixed order. In these cases, the rule is relaxed for the generated output, but the source docstrings and comments should still follow Rule 5.4.

> **Source docstring (correct):** If `timeout_ms` is `0`, the function waits indefinitely.
>
> **Generated output (acceptable):** The function waits indefinitely if `timeout_ms` is `0`. (The generator placed the main clause first. This is acceptable for automated output, but the source docstring must follow Rule 5.4.)

When you write generator templates that produce human-readable documentation (README generators, CLI help text templates), apply Rule 5.4 to the template text, not to the generated variable substitutions.

> **Non-STE:** Run {{command}} to {{action}} after you {{condition}}.
>
> **STE (template):** After you {{condition}}, run {{command}} to {{action}}.
>
> *Principle applied: P1, P8. The template places the condition placeholder first, then the command. The generated output will inherit the correct structure regardless of the substituted values.*

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

- **Rule 1.1 — Use Approved Words:** The condition clause and command must use words from the STE-Code dictionary. Technical code nouns are exempt under Rule 1.5.
- **Rule 1.5 — Technical Code Nouns:** Keywords, frameworks, tool names, and file paths in condition clauses are technical nouns and are not subject to the approved-word dictionary.
- **Rule 5.3 — Imperative (Command) Form for Instructions:** The command that follows the condition clause must use the imperative mood. Rule 5.4 supplies the condition; Rule 5.3 supplies the verb form.
- **Rule 5.5 — Notes Give Information Only, Not Instructions:** If a condition does not lead to a command, it is a note, not an instruction. Do not use the condition-before-command pattern for notes. Use NOTE: instead.
- **Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition:** When a condition clause leads to a safety-critical command, use the WARNING prefix. The condition-before-command pattern applies inside the safety instruction.
- **STE-Code Dictionary:** Consult the dictionary for approved verbs ("start," "stop," "check," "make," "get," "set," "remove," "send," "show," "run," "use") and approved nouns to use in condition clauses. Use the synonym table to replace non-approved words ("verify" → "check," "obtain" → "get," "terminate" → "stop").
- **Rule 1.4 — Approved Verb Forms:** The command that follows the condition clause must use an approved verb form. The condition clause may use tense-marked verbs ("runs," "starts," "fails") because conditions describe states, not actions.
