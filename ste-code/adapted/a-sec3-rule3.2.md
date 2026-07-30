# Rule 3.2 — Use Only These Verb Forms and Tenses of Verbs

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.2

## Original Rule

Use only these verb forms and tenses of verbs:

- The infinitive form
- The imperative form (command form)
- The simple present tense
- The simple past tense
- The simple future tense
- The past participle form (as an adjective).

Use only the verb forms and the tenses of verbs that are approved.

Examples:

| Form | Regular verb (Adjust) | Irregular verb (Give) |
|---|---|---|
| Infinitive (base form) | (To) Adjust | (To) Give |
| Imperative (command form) | Adjust + object | Give + object |
| Simple present tense | You/we/they adjust / It adjusts | You/we/they give / It gives |
| Simple past tense | You/we/they adjusted / It adjusted | You/we/they gave / It gave |
| Simple future tense | You/we/they will adjust / It will adjust | You/we/they will give / It will give |
| Past participle (as an adjective) | The adjusted linkage | The given information |

Do not use other forms and tenses that are not approved, for example:

- The present perfect (have/has adjusted)
- The past perfect (had adjusted)
- The present/past progressive (is/was adjusting)
- And all other complex verb constructions.

## STE-Code Adaptation

Use only these verb forms and tenses of verbs in code documentation:

- The infinitive form (to build, to write, to deploy)
- The imperative form or command form (Build the project. Write the function. Deploy to staging.)
- The simple present tense (The function builds the output. The linter writes the report.)
- The simple past tense (The pipeline built the artifact. The test wrote the result.)
- The simple future tense (The next release will build all modules. The script will write the log.)
- The past participle form used only as an adjective (the built artifact, the written output)

Do not use complex verb constructions that are not approved. Specifically, never use:

- The present perfect (has built, have written)
- The past perfect (had built, had written)
- The present progressive (is building, is writing)
- The past progressive (was building, was writing)
- Any other compound tense that combines auxiliary verbs with the past participle or the "-ing" form.

### Examples

> **Non-STE:** The linter has found three errors in the source file.
>
> **STE:** The linter found three errors in the source file.

> *Adapted from spec pair: present perfect "have/has adjusted" is prohibited in STE.* Just as STE does not permit "has adjusted," STE-Code does not permit "has found." The simple past tense "found" is the approved form.

> **Non-STE:** The server was processing the request when the timeout occurred.
>
> **STE:** The server processed the request. Then the timeout occurred.

> *Adapted from spec pair: past progressive "was adjusting" is prohibited in STE.* Just as STE does not permit "was adjusting," STE-Code does not permit "was processing." Use the simple past tense and break into separate sentences when necessary.

> **Non-STE:** The framework had already initialized the connection pool before the query started.
>
> **STE:** The framework initialized the connection pool. Then the query started.

> *Adapted from spec pair: past perfect "had adjusted" is prohibited in STE.* Just as STE does not permit "had adjusted," STE-Code does not permit "had initialized." Use the simple past tense and sequence events with "Then."

---

## Code-Domain Explanation

This rule controls which verb forms are permitted in software documentation. It applies differently across documentation types because each type has a distinct purpose and reader expectation.

### README Files

README files describe what a project does, how to set it up, and how to use it. The imperative mood commands most README content because the reader follows instructions: "Clone the repository," "Install the dependencies," "Build the project." Use the simple present tense to describe what the project does: "This library validates JSON schemas." Use the simple future tense to describe planned features: "The next release will include WebSocket support."

Do not write: "The project has been written in Rust and is using async I/O." Write: "The project uses Rust and async I/O." The present perfect "has been written" and the present progressive "is using" are not approved.

### API Documentation

API reference docs describe what each endpoint, function, or method does. Use the simple present tense for all descriptive content: "This endpoint returns a list of users," "The function traverses the binary tree," "The middleware authenticates each request." The simple present tense states permanent facts about the API. The simple past tense is rarely needed in API reference docs.

Use the imperative mood only in code examples or quick-start guides: "Send a GET request to /api/users." Never use the present progressive: "This endpoint is returning a list of users" is incorrect — the endpoint always returns that list, not just at the moment of reading.

### Docstrings and Inline Comments

Docstrings describe what a function, class, or module does. Use the simple present tense with the third-person singular: "Returns the sorted list," "Handles the authentication flow," "Serializes the object to JSON." The subject is the code entity itself.

Do not use the imperative mood in docstrings. The imperative mood in a docstring conflicts with the reader's expectation that the docstring describes behavior, not commands it. A docstring that says "Return the sorted list" is ambiguous — does the function return it, or must the caller return it?

Inline comments explain why code does something. Use the simple present tense: "This check prevents a race condition," "The cache stores the result for five minutes." Do not use the past tense in comments: "This was added to fix bug #1234" becomes "This fixes bug #1234." Use the simple present because the code and the reason for it exist now.

### Commit Messages

Commit messages use the imperative mood by widespread convention: "Add rate limiting middleware," "Fix null pointer in parser," "Update dependency versions." The imperative mood describes what the commit does to the codebase. Never use the past tense: "Added rate limiting middleware" is a common mistake. The past tense describes what you did. The imperative mood describes what the commit does to the project.

Use the simple present tense in the commit body to describe the current state or reason: "The old parser does not handle null bytes." Use the simple future tense for planned follow-ups: "A future commit will add integration tests."

### Error Messages

Error messages told to the user should use the simple present tense to describe the condition: "The file does not exist," "The connection timed out," "The input is not valid." Error messages in logs can use the simple past tense to describe what occurred: "The server stopped unexpectedly," "The request failed after three attempts."

Never use the present perfect in error messages. "The file has not been found" is less direct and less clear than "The file does not exist." Never use the progressive: "The server is experiencing high load" becomes "The server load is high."

---

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python classes)

Class documentation describes state and behavior. Use the simple present tense for all method descriptions: "The `connect` method opens a TCP connection to the database," "The `dispose` method releases unmanaged resources." The class exists as a permanent entity. Its behavior does not change over time.

Constructor documentation uses the simple present tense: "Initializes a new instance with the default configuration." Do not use the future tense for constructors: "Will initialize a new instance" is incorrect — the constructor does this now, always.

Inheritance documentation uses the simple present tense: "This class extends the base handler and overrides the `process` method." The present perfect "has extended" or "has overridden" is not approved.

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Pure function documentation describes input-to-output transformations. Use the simple present tense exclusively: "The function takes a list and returns the head element," "This combinator applies the predicate to each element." Pure functions have no state and no time dependence. The simple present tense is the only correct choice.

Pipeline and composition documentation uses the simple present tense for each step: "The first map transforms the input, the filter removes null values, and the reduce combines the results." Do not use the progressive: "The first map is transforming the input" incorrectly implies a temporary action.

Type signatures and type-level documentation can use the infinitive form in explanatory text: "Use this type to represent an optional value." The infinitive form is appropriate when explaining the purpose of a type definition.

### Procedural Documentation (C, Go, Bash)

Procedural code documentation often describes sequences of operations. Use the simple present tense to describe what each function does: "The function opens the file, reads its contents, and returns a buffer." Use the imperative mood for scripts and build instructions: "Run the configure script before you compile the kernel."

In C documentation, ownership and lifetime descriptions use the simple present tense: "The caller owns the returned pointer and must free it." Do not use the future tense: "The caller will own the returned pointer" is unclear — ownership transfers now, not later.

Go documentation follows the same pattern. Use the simple present tense for function behavior: "NewServer creates a new HTTP server with the specified handler." The Go doc convention uses the function name as the subject: "Serve accepts incoming HTTP connections on the listener."

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative configuration documentation describes what the system should be, not what it does. Use the simple present tense: "This resource defines a virtual machine with 4 CPUs," "The deployment specifies three replicas," "The index enforces uniqueness on the email column."

The imperative mood applies to instructions for applying the configuration: "Apply the manifest with kubectl," "Run terraform plan before you apply." Never use the future tense for declarations: "This resource will define a virtual machine" is incorrect — the declaration defines it now, and the system enforces that state continuously.

### Systems Documentation (Rust ownership, C memory management)

Systems documentation describes invariants, guarantees, and safety conditions. Use the simple present tense for permanent guarantees: "This function does not panic," "The reference is valid for the lifetime `'a`," "The mutex prevents concurrent access."

Ownership and borrowing documentation uses the simple present tense to describe rules: "The function borrows the value immutably," "The caller transfers ownership to the callee." These are permanent properties of the function signature, not time-bound events.

Safety documentation uses the imperative mood in the "Safety" section: "The caller must ensure that the pointer is not null." This is a command to the caller, not a description of the function. The simple present tense then describes what the function assumes: "The function assumes the pointer points to valid memory."

---

## Extended Examples

### Example 1 — Present Perfect in README

> **Non-STE:** The build system has cached all the intermediate artifacts, so subsequent builds are much faster.
>
> **STE:** The build system caches all intermediate artifacts. Subsequent builds are faster.

> *Principle P3 (approved meanings) + Rule 3.2:* "has cached" is the present perfect tense. Use the simple present "caches." Break the compound sentence into two simple sentences.

### Example 2 — Past Progressive in Error Documentation

> **Non-STE:** When the crash occurred, the worker thread was processing a large payload and the connection pool was draining.
>
> **STE:** When the crash occurred, the worker thread processed a large payload. The connection pool drained at the same time.

> *Principle P3 + Rule 3.2:* "was processing" and "was draining" are past progressive forms. Use the simple past "processed" and "drained." Break into separate sentences.

### Example 3 — Present Perfect in API Docs

> **Non-STE:** This endpoint has returned a 200 OK for every valid request since version 2.1.
>
> **STE:** This endpoint returns a 200 OK for every valid request. This behavior applies from version 2.1.

> *Principle P3 + Rule 3.2:* "has returned" is the present perfect. Use the simple present "returns." Move the version qualification to a separate sentence.

### Example 4 — Future Perfect in Release Notes

> **Non-STE:** By the time version 3.0 ships, the team will have migrated all legacy endpoints to the new router.
>
> **STE:** Version 3.0 will include a migration of all legacy endpoints to the new router.

> *Principle P3 + Rule 3.2:* "will have migrated" is the future perfect tense, which is not approved. Use the simple future "will include" with a technical noun "migration."

### Example 5 — Past Perfect in Commit Messages

> **Non-STE:** Fixed a bug where the parser had already consumed the token before the validator checked the schema.
>
> **STE:** Fix a bug where the parser consumed the token before the validator checked the schema.

> *Principle P3 + P12 (approved technical verbs) + Rule 3.2:* "had consumed" is the past perfect. Use the simple past "consumed." Also change "Fixed" to the imperative "Fix" for commit message convention.

### Example 6 — Present Progressive in Docstrings

> **Non-STE:** This method is iterating over the collection and is building an index for each element.
>
> **STE:** This method iterates over the collection and builds an index for each element.

> *Principle P3 + Rule 3.2:* "is iterating" and "is building" are present progressive forms. Use the simple present "iterates" and "builds." The method does this every time it is called.

---

## Edge Cases

### Edge Case 1 — Framework Names That Conflict With Verb Forms

Some framework and tool names are also verb forms or contain verb forms. "Rollup" is a build tool and also an approved verb. "Docker" is a platform name that resembles an agent noun. When a framework name appears in documentation, its status as a technical noun (Rule 1.5) overrides the verb-form restriction.

> **Correct:** Use Rollup to bundle the JavaScript modules.
> (Rollup is a technical noun, not a verb. The verb "use" is the main verb in the imperative mood.)

> **Correct:** Docker builds the container from the Dockerfile.
> (Docker is a technical noun, not a verb. "Builds" is the main verb in the simple present tense.)

Never use a framework name as a verb: "Dockerize the application" is not approved. Write: "Package the application in a Docker container."

### Edge Case 2 — Code Keywords in Descriptive Sentences

When code keywords appear inside descriptive sentences, they are technical nouns and do not need to follow verb-form rules. The surrounding prose must still use approved verb forms.

> **Correct:** The `async` keyword marks a function as asynchronous. The `await` operator pauses execution until the promise resolves.
> ("async" and "await" are technical nouns. "Marks," "pauses," and "resolves" are simple present tense verbs.)

> **Incorrect:** The `async` keyword is marking a function as asynchronous and has paused execution.
> (The prose verbs "is marking" and "has paused" violate Rule 3.2, even though the keyword references are valid.)

### Edge Case 3 — Generated Documentation and Changelogs

Auto-generated changelogs often use the past tense because a tool extracts commit messages verbatim. When you manually edit a changelog, convert past-tense entries to the imperative mood or simple present tense. However, fully automated changelogs (generated from `git log` output with no manual editing) are exempt from this rule because the tool output is a raw data feed, not authored documentation.

> **Auto-generated (permitted):** Added rate limiting to the API gateway.
> **Manually edited (preferred):** Add rate limiting to the API gateway.

If you write a changelog entry by hand, use the imperative mood or the simple present tense. Only raw, unedited tool output may use the past tense.

### Edge Case 4 — Third-Party Documentation Republished Verbatim

When you republish third-party documentation (upstream README, specification, or license text) without modification, the third-party content is not required to follow STE-Code verb-form rules. Your surrounding documentation, introduction, and commentary must follow all rules.

> **Correct:** The upstream README states: "This library has been optimized for large datasets." (The quoted text violates Rule 3.2, but it is verbatim third-party content.)

Do not modify third-party content to force STE-Code compliance unless you also own that content.

### Edge Case 5 — Historical Context in Postmortems

Postmortem documents describe past events in chronological order. The simple past tense is the primary tense for narrative description: "The monitoring service detected the anomaly at 14:32 UTC." The simple past correctly places each event in sequence. Do not use the past perfect to sequence events: "The service had detected the anomaly before the alert fired." Use the simple past with "Then" or "before."

---

## Cross-References

This rule enforces the verb-form limit that the dictionary supplies. The dictionary lists the approved forms for each verb. Use only those forms.

> **See:** Rule 3.1 — Use Only the Verb Forms That Are Given in the Dictionary

The past participle is permitted only as an adjective, never as part of a compound tense with "have."

> **See:** Rule 3.3 — Use the Past Participle Form as an Adjective

Compound tenses that combine "have" with the past participle are explicitly prohibited.

> **See:** Rule 3.4 — Do Not Use Auxiliary Verbs to Make Complex Verb Constructions

The "-ing" form in progressive tenses (present progressive, past progressive) is prohibited. The "-ing" form is permitted only as a technical noun or modifier.

> **See:** Rule 3.5 — Use the "-ing" Form of a Verb Only as a Technical Noun or as a Modifier in a Technical Noun

The imperative mood is the primary voice for procedural documentation. Active voice is preferred over passive voice.

> **See:** Rule 3.6 — Use the Active Voice

The approved verb inventory defines which verbs are permitted and with what meanings.

> **See:** STE-Code Approved Dictionary — Verbs Section

---

## Grammar Notes

### Why the Present Perfect Is Prohibited

The present perfect tense ("has built," "have written") connects a past action to the present moment. This connection adds a layer of temporal reasoning that the reader must decode: did the action finish? Does its result persist now? In technical documentation, clarity comes from stating facts directly. The simple present states a permanent fact: "The function returns a string." The simple past states a completed event: "The test failed." Neither requires the reader to infer the relationship between past and present.

The present perfect also introduces the auxiliary verb "have," which increases sentence length and creates ambiguity. "The server has stopped" could mean the server stopped and remains stopped, or that the server stopped at some unspecified time before now. "The server stopped" is unambiguous: the event occurred and is complete.

### Why the Progressive Tenses Are Prohibited

The progressive tenses ("is building," "was processing") describe an action in progress at a point in time. Code documentation rarely needs to describe actions in progress because code entities have permanent behavior, not temporary behavior. A function that "is iterating" in the documentation implies that the iteration is somehow temporary or context-dependent. A function that "iterates" states the permanent truth.

The progressive also adds the "-ing" form, which Rule 3.5 restricts to technical nouns and modifiers. Using the progressive violates both Rule 3.2 and Rule 3.5 simultaneously.

### Why the Past Perfect Is Prohibited

The past perfect ("had built," "had initialized") places one past event before another past event. This two-level temporal nesting forces the reader to construct a timeline. In code documentation, you can sequence events with simpler tools: separate sentences, the word "Then," or the word "before." These tools produce the same meaning with less cognitive load.

> **Complex:** The parser had consumed the token before the validator checked the schema.
> **Simple:** The parser consumed the token. Then the validator checked the schema.

### The Infinitive Form in Code Documentation

The infinitive form ("to build," "to connect") serves a specific role in code documentation: it expresses purpose. "Use this function to validate the input" states the purpose of the function. "The module uses a mutex to prevent race conditions" states the purpose of the mutex.

The infinitive form is also the dictionary citation form for every approved verb. When you reference a verb as a concept rather than using it as a predicate, the infinitive form is correct: "The verb 'to build' replaces 'to compile' and 'to assemble.'"

### The Simple Future Tense in Code Documentation

The simple future tense ("will build," "will include") describes planned but not yet realized behavior. Use it sparingly and only for roadmap items, upcoming features, or deprecation warnings. Overusing the future tense makes documentation speculative rather than authoritative.

> **Correct (sparing use):** The next major version will remove the deprecated endpoints.
> **Incorrect (overuse):** The function will return a string and the caller will use that string to make a request.

The second example describes permanent behavior. Use the simple present: "The function returns a string. The caller uses that string to make a request."
