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

> **Non-STE:** Run the database migration script from the project root directory and then restart the application server to apply all pending schema changes to the production environment. (27 words)
>
> **STE:** Run the database migration script from the project root directory. (9 words) Then, restart the application server to apply all pending schema changes. (13 words)
>
> *Source pairing: the long-sentence-to-two-shorter-sentences split in the Non-STE/STE pair directly above follows the same principle as the original STE example in Rule 5.1.*

> **Non-STE:** The initialization process will automatically create the required directory structure and populate it with default configuration files before the application starts. (22 words)
>
> **STE:** The initialization process automatically creates the required directory structure. (8 words) Then, it populates the directory with default configuration files. (10 words)
>
> *Additional code-domain example — no direct spec pair*

> **Non-STE:** Set the environment variable HTTP_TIMEOUT to the value 30000 which represents the maximum number of milliseconds that the client will wait for a response from the upstream server. (30 words)
>
> **STE:** Set the environment variable HTTP_TIMEOUT to 30000. (8 words) This value is the maximum wait time in milliseconds for a response from the upstream server. (17 words)
>
> *Additional code-domain example — no direct spec pair*

> **CAUTION:** IF YOU DELETE THE CONFIGURATION DIRECTORY WITHOUT A BACKUP, YOU CANNOT RESTORE THE APPLICATION SETTINGS TO THEIR PREVIOUS STATE. (18 words)
>
> *Adapted from spec example: a CAUTION that stays within the 20-word limit on destructive operations — see the original STE example in Rule 5.1.*

> **Non-STE:** For more detailed information about the supported authentication methods and their respective configuration parameters in this release, please refer to the official authentication module documentation page. (27 words)
> **STE (note):** For more information about the supported authentication methods, refer to the authentication module documentation. (15 words)
>
> *Adapted from original rule — notes have a maximum sentence length of 25 words; no direct spec pair*

## Code-Domain Explanation

Rule 5.1 applies to all procedural text in software documentation. A procedure is any sequence of instructions that tells the reader how to complete a task. In code documentation, procedures appear in many forms. Each form must obey the 20-word sentence limit.

### README Files

README files contain installation procedures, configuration steps, and quick-start guides. Each step in these procedures must use sentences of 20 words or fewer. A long installation instruction is difficult to follow while the reader types commands in a terminal window. Break long steps into two or more shorter steps. Each step must give exactly one instruction.

> **Non-STE:** Clone the repository to your local machine using the command shown below and then navigate into the newly created project directory before running the setup script. (28 words)
>
> **STE:** Clone the repository to your local machine. (6 words) Use the command shown below. (5 words) Then, navigate into the new project directory. (7 words) Run the setup script. (4 words)
>
> *Principle: P12 (technical verbs: clone, navigate, run). Four instructions become four sentences.*

### API Documentation

API reference pages describe endpoints, parameters, return types, and error codes. Procedural sentences in API docs include setup instructions, authentication flows, and request sequencing. Parameter descriptions in tables are descriptive, not procedural. Use the 25-word limit for descriptive sentences in API parameter tables. Apply the 20-word limit to sentences that tell the reader to perform an action.

> **Non-STE:** The `page` query parameter accepts a positive integer value that specifies which page of results the server should return in the paginated response to this endpoint. (28 words)
>
> **STE (descriptive):** The `page` query parameter accepts a positive integer. (8 words) It specifies which page of results to return. (9 words) This is for paginated responses. (6 words)
>
> *Principle: P1 (use approved words: accepts, specifies, return). Descriptive sentences may use up to 25 words each. Here, the longest is 9 words. The original sentence packs three pieces of information into one clause chain.*

### Docstrings and Inline Comments

Docstrings for functions and methods often contain procedural instructions for callers. Each sentence in a docstring procedure must obey the 20-word limit. Descriptive sentences about return values or side effects may use up to 25 words. Inline comments that give instructions must also obey the limit.

> **Non-STE:** Call this method to initialize the connection pool with the provided configuration and establish the minimum number of idle connections specified in the pool settings before returning control to the caller. (32 words)
>
> **STE:** Call this method to initialize the connection pool. (8 words) Use the provided configuration. (4 words) The method establishes the minimum number of idle connections. (10 words) Then, it returns control to the caller. (8 words)
>
> *Principle: P2 (use words only as their specified part of speech: "initialize" as verb, "configuration" as noun). One long sentence with three embedded actions becomes four sentences.*

### Commit Messages

A commit message subject line is a short summary of the change. Keep the subject line to 72 characters or fewer. This is a separate constraint from the word count rule. The commit message body contains procedural or descriptive sentences. Apply the 20-word limit to procedural sentences in the body. Apply the 25-word limit to descriptive sentences.

> **Non-STE:** Refactored the authentication middleware to extract the token validation logic into a separate utility function so that it can be reused by the WebSocket upgrade handler and the GraphQL subscription resolver as well. (35 words)
>
> **STE (body):** Refactored the authentication middleware. (4 words) Extracted the token validation logic into a separate utility function. (11 words) The WebSocket upgrade handler and the GraphQL subscription resolver now reuse this function. (15 words)
>
> *Principle: P11 (one term per concept: "token validation logic" is used consistently). The justification ("so that it can be reused...") becomes a separate declarative sentence.*

### Error Messages

Error messages shown to the user must be short and clear. Use the 20-word limit for error messages that tell the user to take action. Error messages that only report a condition may use the 25-word descriptive limit. Error messages are read under stress. Short sentences reduce the cognitive load on the user.

> **Non-STE:** The configuration file could not be parsed because it contains a syntax error on line 42 that is most likely caused by a missing closing bracket or an unquoted string value containing special characters. (35 words)
>
> **STE:** The configuration file has a syntax error on line 42. (11 words) Check for a missing closing bracket or an unquoted string value. (13 words)
>
> *Principle: P3 (use words only with approved meanings: "has" instead of "contains," "check" instead of "is most likely caused by"). The diagnosis and the remedy are separated.*

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

OOP documentation describes class hierarchies, constructor parameters, method signatures, and inheritance chains. Procedural sentences in OOP docs include step-by-step instantiation guides, dependency injection setup, and mock configuration for tests.

Sentence-length pitfalls in OOP docs include long sentences that describe all constructor parameters at once, sentences that chain multiple method calls in one instruction, and sentences that explain both the "what" and the "why" of a design pattern in a single breath.

> **Non-STE:** The constructor accepts a database connection string, a logger instance that must implement the ILogger interface, and an optional configuration object for setting the retry policy and the connection timeout duration. (33 words)
>
> **STE:** The constructor accepts three parameters. (5 words) Parameter one is a database connection string. (7 words) Parameter two is a logger instance. It must implement the ILogger interface. (6 + 7 words) Parameter three is an optional configuration object. (7 words) Use this object to set the retry policy and the connection timeout. (14 words)
>
> *Principle: P5 (technical code nouns: ILogger, configuration object). Each parameter is documented in its own sentence cluster. The reader can focus on one parameter at a time.*

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, type signatures, monadic chains, and pattern matching. The 20-word rule helps readers follow the flow of data through function compositions. Long sentences that trace data through multiple composed functions are common in functional docs and must be split.

> **Non-STE:** The `process` function first maps the transformation over each element in the list and then filters out any results that are `None` before finally folding the remaining values into a single accumulator using the provided binary operator. (35 words)
>
> **STE:** The `process` function maps a transformation over each element in the list. (13 words) Then, it filters out any `None` results. (8 words) Finally, it folds the remaining values into a single accumulator. (13 words) The provided binary operator controls the fold. (8 words)
>
> *Principle: P12 (technical verbs: maps, filters, folds). Each stage of the pipeline gets its own sentence. The reader traces data flow one transformation at a time.*

### Procedural Documentation (C, Go, Bash)

Procedural code tends to have long sequences of setup, validation, and teardown steps. Documentation that mirrors this structure is especially prone to long sentences. Sentence-length pitfalls include sentences that combine error checking with the operation being checked and sentences that describe conditional branching in prose.

> **Non-STE:** Run the configure script to detect your system's available libraries and compiler features and then run make with the -j flag set to the number of CPU cores on your machine to compile the program from source. (37 words)
>
> **STE:** Run the configure script. (4 words) This script detects your system libraries and compiler features. (10 words) Then, run make to compile the program from source. (12 words) Use the -j flag. Set it to the number of CPU cores on your machine. (14 + 11 words)
>
> *Principle: P9 (short, clear technical nouns: configure script, make, -j flag). The detection phase and the compilation phase are separated. Flag usage is its own step.*

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes the desired state of a system. Procedures in declarative docs include migration runbooks, apply-and-verify workflows, and rollback instructions. Long sentences that describe a resource and all its attributes together are the most common violation.

> **Non-STE:** Execute the migration script against the production database after taking a full backup and verifying that the replication lag on all read replicas is less than five seconds to prevent any data inconsistency during the schema change. (38 words)
>
> **STE:** Take a full backup of the production database. (8 words) Verify that the replication lag on all read replicas is less than five seconds. (16 words) Then, execute the migration script against the production database. (11 words)
>
> *Principle: P8 (standard, well-known technical nouns: backup, replication lag, migration script). Prerequisites are checked before the action. The sequence is explicit. The justification ("to prevent data inconsistency") is implied by the ordering.*

### Systems Documentation (Rust Ownership, C Memory Management)

Systems documentation describes ownership models, memory allocation, lifetimes, and safety guarantees. These topics are complex. Short sentences prevent the reader from missing critical safety information. Long safety warnings that bury the hazard in context are dangerous and must be split.

> **Non-STE:** After calling this function the caller must not use the original buffer pointer because ownership of the memory has been transferred to the callee and any subsequent access through the old pointer will result in undefined behavior. (37 words)
>
> **STE:** After you call this function, do not use the original buffer pointer. (14 words) Ownership of the memory is transferred to the callee. (11 words) Access through the old pointer causes undefined behavior. (10 words)
>
> *Principle: P1 (use approved words: "causes" instead of "will result in"). The prohibition, the reason, and the consequence each get their own sentence. Safety-critical information is never buried in a subordinate clause.*

## Extended Examples

Each example below shows a Non-STE sentence (violating the rule) and the STE-Code compliant version. The principle applied and a brief explanation follow each pair.

### Example 1 — Docker Setup Instructions

> **Non-STE:** Build the Docker image using the Dockerfile in the project root and then run a container from that image with port 8080 on the host mapped to port 80 inside the container. (33 words)
>
> **STE:** Build the Docker image. (4 words) Use the Dockerfile in the project root. (8 words) Then, run a container from that image. (9 words) Map port 8080 on the host to port 80 inside the container. (15 words)
>
> *Principle: P8 (standard technical nouns: Docker image, Dockerfile, container), P12 (technical verbs: build, run, map). The original sentence combines three procedural steps into one. The STE version splits the build, the file specification, the run command, and the port mapping into separate sentences. Each sentence now focuses on one action.*

### Example 2 — Git Workflow Instructions

> **Non-STE:** Create a new feature branch from the main branch, implement your changes in that branch, push the branch to the remote repository, and then open a pull request against the main branch for code review. (35 words)
>
> **STE:** Create a new feature branch from the main branch. (10 words) Implement your changes in that branch. (7 words) Push the branch to the remote repository. (9 words) Then, open a pull request against the main branch. (11 words)
>
> *Principle: P12 (technical verbs: create, push, open), P9 (short, clear technical nouns: branch, pull request). A four-step workflow was written as one sentence joined by commas and "and." The STE version gives each step its own sentence. The reader can complete one step before reading the next.*

### Example 3 — Configuration File Documentation

> **Non-STE:** The `retry_policy` section of the configuration file lets you define whether the client should retry failed requests, how many times it should retry before giving up and throwing an error, and the backoff strategy to use between consecutive retry attempts. (39 words)
>
> **STE:** The `retry_policy` section controls how the client handles failed requests. (12 words) Set the number of retry attempts. (7 words) Set the backoff strategy between attempts. (7 words) The client throws an error when all retries fail. (11 words)
>
> *Principle: P1 (use approved verbs: controls, handles, set — instead of "lets you define"), P11 (one term per concept, consistent throughout). The original sentence describes three configuration options in one breath. The STE version separates the conceptual overview from each specific setting.*

### Example 4 — API Rate Limiting Documentation

> **Non-STE:** When a client exceeds the rate limit of 100 requests per minute the server will respond with HTTP status code 429 and include a Retry-After header that tells the client how many seconds it must wait before sending another request to the same endpoint. (42 words)
>
> **STE:** The rate limit is 100 requests per minute. (8 words) When a client exceeds this limit, the server responds with HTTP status 429. (14 words) The response includes a Retry-After header. (7 words) This header tells the client how many seconds to wait. (12 words) Then, the client can send another request. (8 words)
>
> *Principle: P2 (use words only as specified part of speech), P12 (technical verbs: responds, includes, send), P5 (technical code nouns: HTTP status 429, Retry-After). A complex conditional with embedded clauses is restructured into a sequence of short, declarative sentences. Each sentence states one fact about the system behavior.*

### Example 5 — Debugging Instructions

> **Non-STE:** To debug the authentication failure you should first check the application logs for any error messages related to token validation and then verify that the JWT secret in your environment variables matches the secret that was used to sign the token that the client is sending. (44 words)
>
> **STE:** To debug the authentication failure, check the application logs. (10 words) Look for error messages about token validation. (8 words) Then, verify that the JWT secret in your environment variables matches the signing secret. (17 words)
>
> *Principle: P3 (use words only with approved meanings), P13 (do not use technical verbs as nouns: "sign" is a verb here). The original sentence has embedded relative clauses ("that was used to sign the token that the client is sending"). The STE version removes the nesting and restates the verification as a simple equality check. The longest sentence drops from 44 to 17 words.*

### Example 6 — CI/CD Pipeline Documentation

> **Non-STE:** The deployment pipeline will automatically run the full test suite on every push to the main branch and if all tests pass it will build a production Docker image and push it to the container registry before updating the Kubernetes deployment with the new image tag. (44 words)
>
> **STE:** The deployment pipeline runs the full test suite on every push to the main branch. (17 words) If all tests pass, the pipeline builds a production Docker image. (13 words) Then, it pushes the image to the container registry. (11 words) Finally, it updates the Kubernetes deployment with the new image tag. (14 words)
>
> *Principle: P12 (technical verbs: runs, builds, pushes, updates), P8 (standard technical nouns: Docker image, container registry, Kubernetes deployment), P11 (consistent term: "pipeline" throughout). A CI/CD pipeline description is restructured into a sequential narrative. Each stage of the pipeline gets its own sentence. The conditional is isolated from the build step.*

## Edge Cases

### Edge Case 1 — Long Framework or Service Names

Some technical names are unavoidably long. "Amazon Web Services Elastic Kubernetes Service" is one technical noun phrase with six words. When a sentence must include a long proper noun, the word count may exceed 20 words through no fault of the writer.

**Guidance:** Use the shortest accepted form of the name on first use. Define an abbreviation. Then, use the abbreviation in later sentences. This is consistent with Rule 1.9 (prefer short, clear technical nouns). The abbreviation itself counts as one word.

> **Non-STE:** Create a new cluster in Amazon Web Services Elastic Kubernetes Service using the eksctl command-line tool with the provided cluster configuration YAML file that specifies three worker nodes of type t3.medium. (30 words)
>
> **STE:** Create a new cluster in Amazon EKS. (7 words) Use the eksctl command-line tool. (6 words) Use the provided cluster configuration YAML file. (8 words) The file must specify three worker nodes of type t3.medium. (13 words)

### Edge Case 2 — Code Keywords That Form Long Phrases

Some code keyword sequences form long noun phrases that consume many word-count slots. For example: "the `async fn` with `impl Future<Output = Result<T, E>>` return type" contains several tokens. Counting conventions matter for compliance.

**Guidance:** Code elements inside backticks count as one word each, regardless of their character length. This aligns with the principle that code identifiers are opaque tokens, not prose words. Apply this rule consistently: `Result<T, E>` is one word, `async fn` is two words. Do not expand generics or type parameters into prose words.

> **Non-STE:** The function signature `pub async fn fetch_user(id: UserId) -> Result<User, Error>` specifies that the function is public and asynchronous and returns a Result type that wraps either a User value or an Error value. (33 words under prose counting rules)
>
> **STE:** The function signature is `pub async fn fetch_user(id: UserId) -> Result<User, Error>`. (8 words) The function is public and asynchronous. (6 words) It returns a Result type. (6 words) The Result wraps a User value or an Error value. (11 words)
>
> *Under the code-token counting convention, the STE version's longest procedural sentence is 11 words. The code block in backticks counts as one word.*

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
> **STE:** Use this configuration block in your docker-compose.yml file: (9 words) [code block] This configuration sets the correct environment variables and port mappings. (11 words)
>
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

**2. Extract conditions into their own sentence.** Move a conditional clause ("if X, then Y") into a separate sentence that precedes or follows the main instruction. This also improves comprehension because the reader checks the condition before attempting the action.

**3. Separate the action from its purpose.** Put the instruction in one sentence. Put the reason or result in the next sentence.

> **Non-STE:** Set the `NODE_ENV` variable to `production` so that the application loads the optimized configuration and disables the development-only debugging middleware and hot-reload features. (26 words)
>
> **STE:** Set the `NODE_ENV` variable to `production`. (6 words) This setting loads the optimized configuration. (6 words) It disables debugging middleware and hot-reload features. (8 words)

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

### Subordinate Clause Depth

Limit subordinate clause depth to two levels. A sentence with three or more levels of embedding is difficult to parse and usually exceeds the 20-word limit. Flatten deep structures by promoting embedded clauses to their own sentences.

> **Non-STE:** The server returns an error when the client sends a request that contains a payload that exceeds the limit that the administrator configured in the settings file. (27 words, 4 levels of embedding)
>
> **STE:** The server returns an error when the request payload exceeds the configured limit. (13 words) The administrator sets this limit in the settings file. (11 words)
>
> *Two levels of embedding replaced with two sentences at one level each.*

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
