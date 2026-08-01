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

the CROSS FEED port is more than 5 cc/minute.

(One sentence, 22 words.)

results.

(Two sentences, 6 words and 8 words.)

Do not use the imperative form in a note. If you use the imperative form, the note becomes an instruction for a work step.

Example:

correctly.

(This text is not a note because it contains the imperative form.)

> **STE:** (6) Make sure that the avionics ventilation system continues to operate correctly.

(This is work step number 6 in the applicable procedure.)

If you include instructions in a note, it is possible that the reader will not see the information. If the information given in a note is important to prevent damage or injury, you must give such information in a safety instruction.

Examples:

| Non-STE: | NOTE: When you connect the lines, do not bend them too much. If you bend the lines too much, you can cause damage to them. (This text is not a note. It is a safety instruction.) |
| --- | --- |
| STE: | CAUTION: WHEN YOU CONNECT THE LINES, DO NOT BEND THEM TOO MUCH. IF YOU BEND THE LINES TOO MUCH, YOU CAN CAUSE DAMAGE TO THEM. |

airflow to the compartment and therefore there is a risk of suffocation.

(Although the non-STE text does not contain the imperative form, it is not a note. It is a safety instruction.)

> **STE:** WARNING: BEFORE YOU CLOSE THE HATCH, MAKE SURE THAT NO PERSONS ARE IN THE CREW REST COMPARTMENT. WHEN THE HATCH IS CLOSED, THERE IS NO AIRFLOW TO THE COMPARTMENT AND THERE IS A RISK OF SUFFOCATION.

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

## STE-Code Adaptation

In code documentation, notes provide supplementary information that helps the reader understand context, behavior, or background details about a procedure. Notes must contain descriptive information only. Notes must not contain instructions for the reader to execute, commands to run, or step-by-step actions.

Notes must not give requirements, limits, tolerances, or expected results of a work step. This information belongs directly in the work step itself, after the related action, so the reader sees it while executing the step. Notes must not contain imperative verbs. If you need to give an instruction, write it as a numbered work step.

If a note contains information that is critical for preventing data loss, security issues, or system damage, move that information into a WARNING or CAUTION safety instruction. A note is never a substitute for a safety instruction.

Each sentence in a note can have a maximum of 25 words. A note can contain one or more sentences.

To verify correct note usage, read the procedure without the notes. If the reader cannot complete the procedure correctly, move the missing information from the notes into work steps and repeat the test.


> *Adapted from spec pair:* Non-STE: Put preservation oil into the unit through the vent hole until the oil level is approximately 6 mm (0.24 inches) below the surface of the flange cover._ (25 words)  |  STE: Put preservation oil into the unit through the vent hole. (10 words) Continue until the oil level is approximately 6 mm (0.24 in) below the surface of the flange cover. (16 words)
### Examples

> **STE:** NOTE: The API rate limiter allows a maximum of 1000 requests per minute per client IP address on the free tier.
>
> *Source pairing: a note gives descriptive information only, with no instruction — follows the same principle as the original STE example in Rule 5.5.*

(One sentence, 20 words. This note gives context about the API behavior without instructing the reader to do anything.)

> **STE:** NOTE: The configuration cache refreshes automatically every 60 seconds. Manual changes to the configuration file will not take effect until the next cache refresh cycle.
>
> *Adapted from spec: multi-sentence note example — a note can have one or more sentences, each with a maximum of 25 words.*

(Two sentences, 8 words and 19 words. Descriptive information only, no instructions.)

> **Non-STE:** NOTE: When you update the dependencies, run the command `npm audit fix` to resolve known vulnerabilities. If you skip this step, your application may have security issues.
>
> **STE:** (5) Run the command `npm audit fix` to resolve known vulnerabilities.
>
> *Source pairing: an instruction written inside a note becomes a numbered work step — follows the same principle as the original STE example in Rule 5.5.*

(Do not put instructions in a note. The instruction to run a command is a work step.)

> **Non-STE:** NOTE: The response time must be less than 200 milliseconds under normal load conditions. If the response time is higher, investigate the database query performance.
>
> **STE:** The response time must be less than 200 milliseconds under normal load conditions.
>
> *Adapted from spec: notes must not give limits, tolerances, or results — this information belongs directly in the work step.*

(Do not put limits or requirements in a note. The limit belongs directly in the work step.)

| Non-STE: | NOTE: Before you deploy to production, make sure that all environment variables are set correctly. If you deploy with missing variables, the application will not start and the deployment will fail. (This text is not a note. It is a safety instruction.) |
| --- | --- |
| STE: | CAUTION: BEFORE YOU DEPLOY TO PRODUCTION, MAKE SURE THAT ALL ENVIRONMENT VARIABLES ARE SET CORRECTLY. IF YOU DEPLOY WITH MISSING VARIABLES, THE APPLICATION WILL NOT START. |

> *Source pairing: a note that contains a safety instruction must become a CAUTION — follows the same principle as the original STE example in Rule 5.5.*

> **Non-STE:** NOTE: Do not run the migration script on the production database without first creating a full backup. Running the migration without a backup can cause irreversible data loss.
>
> **STE:** WARNING: DO NOT RUN THE MIGRATION SCRIPT ON THE PRODUCTION DATABASE WITHOUT A FULL BACKUP. RUNNING THE MIGRATION WITHOUT A BACKUP CAN CAUSE IRREVERSIBLE DATA LOSS.
>
> *Source pairing: critical safety information belongs in a WARNING, not a note — follows the same principle as the original STE example in Rule 5.5.*

(Critical safety information belongs in a WARNING, not a note.)

### Code-Domain Explanation

This rule applies differently across documentation types in software engineering. Each type has a distinct audience and purpose. The separation of notes from instructions is critical in all types.

#### README Files

README files serve as the entry point for a project. They mix descriptive content with setup instructions. Notes in README files must provide context that helps the reader understand the project. They must not replace setup steps.

A note in a README can explain why a dependency exists or give background on a design decision. It must not tell the reader to install a package or run a command. Place those instructions in the numbered setup steps.

> **STE:** NOTE: This project uses SQLite for local development. The production deployment uses PostgreSQL for concurrent write support.
>
> (Descriptive context. The reader does not need this information to complete the setup steps.)

#### API Documentation

API reference documents describe endpoints, parameters, and response formats. Notes in API documentation explain behavior, side effects, or constraints. They must not include instructions for using the API endpoint.

A note about rate limiting is acceptable. A note that says "Call the /refresh endpoint before this one" is an instruction. Move that instruction to the endpoint description or write it as a prerequisite step.

> **STE:** NOTE: The `/search` endpoint returns a maximum of 50 results per page. Use the `cursor` parameter to get the next page of results.
>
> (The second sentence gives an instruction and violates this rule. It must become a separate descriptive statement before the endpoint specification.)

#### Docstrings

Function and class docstrings are the most constrained documentation type. They appear inline with code and are read by both humans and tools. Notes in docstrings must describe behavior, not tell the caller what to do.

A docstring note can explain that a function is not thread-safe. It must not say "Call this function only from the main thread." That is a requirement. Write it as a constraint in the function description.

> **Non-STE:** NOTE: You must call `initialize()` before calling any other function in this module. If you do not call it first, the other functions will throw an exception.
>
> **STE:** This module requires a call to `initialize()` before any other function call. Other function calls will raise `ModuleNotInitializedError` if `initialize()` has not completed.
>
> *Principle applied: P4 (approved verb forms). The requirement is part of the function specification, not a note.*

#### Commit Messages

Commit messages follow a specific format: a summary line followed by a blank line and a body. Notes in commit message bodies must explain why a change was made. They must not give instructions for using the change.

A commit message note can explain that a refactor was necessary because of a performance regression. It must not say "Run the migration after checking out this commit." That instruction belongs in release notes or a migration guide.

> **STE:** NOTE: The database schema change removes the `legacy_status` column. This column was deprecated in version 2.4 and no code references it.
>
> (Descriptive context about the change. No instructions.)

#### Error Messages

Error messages are the most constrained context for notes. An error message must tell the user what went wrong and possibly how to fix it. A note in an error message must describe state or context. It must not contain the fix instruction as a note.

> **Non-STE:** Error: Connection refused.
> NOTE: Check that the database server is running on port 5432. Verify your credentials in the `.env` file.
>
> **STE:** Error: Connection refused.
> The database server on port 5432 did not respond. Check that the server is running. Make sure that the credentials in the `.env` file are correct.
>
> *Principle applied: P4. The fix guidance is part of the error description. It is not a note. The sentences use descriptive mood followed by imperative mood.*

### Paradigm-Specific Guidance

The application of this rule changes slightly across programming paradigms. The core principle stays the same: notes give information, not instructions. The form of the note changes with the paradigm's documentation conventions.

#### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Class documentation describes types, their state, and their behavior. Notes in class documentation explain design decisions or constraints on state.

> **Non-STE:** NOTE: After calling `dispose()`, you must not call any other method on this object. Doing so will cause an `ObjectDisposedException`.
>
> **STE:** NOTE: The object enters a disposed state after a call to `dispose()`. Method calls on a disposed object cause an `ObjectDisposedException`.
>
> *Principle applied: P4. The constraint is a property of the object state. It is not an instruction to the reader.*

#### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional code documents pure functions, type signatures, and data transformations. Notes explain purity constraints or performance characteristics.

> **Non-STE:** NOTE: This function is pure and has no side effects. You can safely memoize it. Re-run it as many times as you want with the same arguments.
>
> **STE:** NOTE: This function is pure. It has no side effects. Repeated calls with the same arguments return the same result.
>
> *Principle applied: P4, P11 (one term per concept). The function's properties are described. The reader is not told what to do.*

#### Procedural Documentation (C, Go, Bash)

Procedural code documents sequences of steps. Notes explain state between steps or prerequisites for steps.

> **Non-STE:** NOTE: The file descriptor remains open until you explicitly call `close()`. You must close it to prevent a file descriptor leak.
>
> **STE:** NOTE: The file descriptor stays open until the code calls `close()`. An unclosed file descriptor causes a resource leak.
>
> *Principle applied: P4, P2 (words only as specified part of speech). "Remains" → "stays" for simpler vocabulary.*

#### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documents describe desired state. Notes explain constraints or platform behavior that affects the declared state.

> **Non-STE:** NOTE: The `depends_on` attribute ensures that the database is created before the application. Always set this attribute if your application needs a database.
>
> **STE:** NOTE: The `depends_on` attribute controls resource creation order. Terraform creates the database resource before the application resource when this attribute is set.
>
> *Principle applied: P4. The attribute behavior is described. The instruction "Always set this" is removed.*

#### Systems Documentation (Rust Ownership, C Memory)

Systems documentation explains ownership, lifetime, and memory semantics. Notes clarify constraints that the compiler enforces.

> **Non-STE:** NOTE: This function borrows the value immutably. Do not mutate the value while the borrow is active. The compiler will reject your code if you try.
>
> **STE:** NOTE: This function borrows the value immutably. The borrow prevents mutation of the value until the borrow ends. The compiler rejects code that violates this constraint.
>
> *Principle applied: P4, P11. The compiler's behavior is described. The reader is not given instructions.*

### Extended Examples

Each example shows a Non-STE version that violates the rule and an STE-Code compliant version. The principle applied and a brief explanation follow each pair.

**Example 1: Instructions hidden in a note**

> **Non-STE:** NOTE: The build process generates static assets in the `dist/` directory. Before you run the build, make sure you have Node.js version 18 or higher installed. Run `node --version` to check your current version.
>
> **STE:** (3) Make sure that Node.js version 18 or higher is installed.
>
> *Principle applied: P1, P4. The version check instruction is a work step. The note about static assets is removed because it is not necessary for the procedure.*

Explanation: The Non-STE version hides a prerequisite check in a note. The reader might skip the note and use an incompatible Node.js version. The STE version makes the check a numbered work step.

**Example 2: Requirement disguised as a note**

> **Non-STE:** NOTE: The authentication token expires after 3600 seconds. You must refresh the token before making any API call that requires authentication.
>
> **STE:** The authentication token is valid for 3600 seconds. After the token expires, the API returns a `401 Unauthorized` status code.
>
> *Principle applied: P4, P5. The token lifetime and the API behavior are descriptive statements. They belong in the endpoint specification, not in a note.*

Explanation: The Non-STE version gives a requirement ("you must refresh") inside a note. The STE version moves the descriptive information about token lifetime and error behavior into the API specification body.

**Example 3: Configuration guidance in a note**

> **Non-STE:** NOTE: The default connection pool size is 10. For high-traffic applications, increase this value to 25 or higher. Set the `POOL_SIZE` environment variable in your `.env` file.
>
> **STE:** NOTE: The default connection pool size is 10.
>
> *Principle applied: P1 (use, not utilize), P2. The tuning guidance is a configuration instruction. It belongs in the configuration reference section, not in a note.*

Explanation: The Non-STE version gives tuning instructions in a note. The STE version keeps only the descriptive fact about the default value. The tuning guidance must appear in a dedicated configuration section or work step.

**Example 4: Debugging instructions in a note**

> **Non-STE:** NOTE: If the application fails to start, check the log file at `/var/log/app/error.log`. Look for lines that contain the word "FATAL". Contact the operations team if you see a "connection refused" error.
>
> **STE:** NOTE: The application writes startup errors to the file `/var/log/app/error.log`. Fatal errors start with the word "FATAL" in the log.
>
> *Principle applied: P4, P13 (do not use technical verbs as nouns). The debugging procedure is not a note. The note only describes the log file location and format.*

Explanation: The Non-STE version gives a troubleshooting procedure inside a note. The STE version describes where errors are logged and what to look for. The troubleshooting procedure must be a separate section with numbered steps.

**Example 5: Migration note with hidden commands**

> **Non-STE:** NOTE: This release adds a new `email_verified` column to the `users` table. Run the migration with `php artisan migrate`. If the migration fails, roll back with `php artisan migrate:rollback` and check your database permissions.
>
> **STE:** NOTE: This release adds a new `email_verified` column to the `users` table.
>
> *Principle applied: P1, P4. The migration commands are work steps. They must be numbered steps in the upgrade procedure.*

Explanation: The Non-STE version embeds run and rollback commands in a note. The STE version only describes the schema change. The migration commands belong in numbered upgrade steps.

**Example 6: Timeout behavior explained incorrectly**

> **Non-STE:** NOTE: The request timeout is 30 seconds by default. Do not set a timeout longer than 60 seconds because the load balancer will drop the connection. Always handle timeout errors in your client code.
>
> **STE:** NOTE: The default request timeout is 30 seconds. The load balancer drops connections that stay open longer than 60 seconds.
>
> *Principle applied: P4, P11. The constraints about maximum timeout and error handling are requirements. They belong in the API specification or client library documentation.*

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

> **Non-STE:** NOTE: Call this method before any other method on the object.
>
> **STE (source):** This method must be the first call on the object.

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
> ("Must" signals a requirement. This is a safety instruction, not a note.)

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

> **See also:** Rule 5.3 — Imperative (Command) Form for Instructions; Rule 5.4 — Descriptive Statement Before the Command; Rule 5.6 — Separate Steps for Separate Actions; Rule 7.1 — Use an Applicable Word to Identify the Level of Risk; Rule 9.1 — Descriptive Writing Rules; Rule 1.1 — Use Approved Words from the STE-Code Dictionary; Rule 1.5 — Technical Code Nouns; Rule 1.7 — Do Not Use Technical Nouns as Verbs
