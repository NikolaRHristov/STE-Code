# Rule 3.4 — Do Not Use Auxiliary Verbs to Make Complex Verb Constructions

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.4

## Original Rule

Do not use auxiliary verbs to make complex verb constructions.

Do not use the past participle form as a verb form together with the auxiliary verb "have." This construction will make a tense that is not approved.

Example:

> **STE:** When the unit is fully disassembled, clean all the parts.
> ("Disassembled" is an adjective after the verb "to be" that shows the condition of the unit.)
> (The simple past tense is approved.)

Some complex verb constructions include other auxiliary verbs with the past participle form as a verb. Sentences with these constructions become complex sentences in the passive voice.

## STE-Code Adaptation

Do not use auxiliary verbs ("have," "has," "had," "will have") together with the past participle form of a verb to make compound tenses. This construction creates verb forms that are not approved in STE-Code.

The auxiliary verb "have" with a past participle produces the present perfect or past perfect tense, which violates Rule 3.2. Instead, use one of the approved simple tenses.

> **See also:** Rule 3.2 — Use Only These Verb Forms and Tenses of Verbs

Complex verb constructions that combine auxiliary verbs with the past participle often also create passive voice constructions. Simplify these sentences by using the active voice (Rule 3.6) and the simple past tense.

> **See also:** Rule 3.6 — Use the Active Voice

A sentence that uses the past participle after "to be" is permitted only when the past participle functions as an adjective describing a condition (Rule 3.3), not as part of a passive verb construction.

> **See also:** Rule 3.3 — Use the Past Participle Form as an Adjective

### Examples

> **Non-STE:** After the pipeline has deployed the application, the monitoring service will have started the health checks.
>
> **STE:** After the pipeline deploys the application, the monitoring service starts the health checks.

> *Adapted from spec pair: "When the unit is fully disassembled, clean all the parts."* Just as STE avoids the present perfect ("has disassembled") by using the simple present/past, STE-Code avoids compound tenses ("has deployed," "will have started") by using the simple present tense. The auxiliary verbs "have" and "will have" are removed.

> **Non-STE:** The developer had committed the changes before the reviewer had approved the pull request.
>
> **STE:** The developer committed the changes. Then the reviewer approved the pull request.

> *Adapted from spec pair: the past perfect tense is not approved in STE.* Just as STE does not permit "had adjusted," STE-Code does not permit "had committed" or "had approved." Replace with simple past tense and break into separate sentences.

> **Non-STE:** The test runner has executed all the unit tests and has written the coverage report.
>
> **STE:** The test runner executed all the unit tests. Then it wrote the coverage report.

> *Adapted from spec pair: the present perfect tense is not approved in STE.* Just as STE does not permit "has adjusted," STE-Code does not permit "has executed" or "has written." Replace with simple past tense and use separate sentences sequenced with "Then."

---

## Code-Domain Explanation

This rule controls whether you can combine auxiliary verbs with past participles to form compound tenses. The restriction applies across all code documentation types, but the correct replacement strategy differs by context.

### README Files

README files describe project setup, usage, and current status. The present perfect often sneaks into status statements and prerequisite descriptions. Replace it with the simple present for current facts or the simple past for completed events.

Do not write: "You must have installed Node.js version 18 or higher." Write: "You must install Node.js version 18 or higher." The auxiliary "have" with the past participle "installed" creates a perfect infinitive construction that violates this rule. The simple present "install" is direct and correct.

Do not write: "The project has been tested on macOS, Linux, and Windows." Write: "The project runs on macOS, Linux, and Windows." Or use the simple past: "We tested the project on macOS, Linux, and Windows." The present perfect passive "has been tested" combines the auxiliary "has" with the past participle "tested" and adds passive voice. Both violations are removed by using the active voice with a simple tense.

### API Documentation

API reference documentation states permanent facts about endpoints, parameters, and responses. The present perfect is often used incorrectly to describe when a feature became available or what an endpoint has historically returned.

Do not write: "This endpoint has returned a 200 OK status since version 3.0." Write: "This endpoint returns a 200 OK status. This behavior applies from version 3.0." The simple present "returns" states the permanent fact. The separate sentence attaches the version qualification.

Do not write: "The parameter has been deprecated and will have been removed by version 4.0." Write: "This parameter is deprecated. Version 4.0 will remove it." The present perfect passive "has been deprecated" becomes the adjective "deprecated" after "is" (permitted by Rule 3.3). The future perfect "will have been removed" becomes the simple future "will remove" in the active voice.

### Docstrings and Inline Comments

Docstrings describe what a function does. The present perfect in docstrings often arises from describing setup or preconditions that the function assumes.

Do not write: "Call this function after you have initialized the connection pool." Write: "Call this function after you initialize the connection pool." The present perfect "have initialized" in a subordinate clause is replaced by the simple present "initialize."

Do not write: "The cache has stored the result and the function returns it directly." Write: "The cache stores the result. The function returns it directly." The present perfect "has stored" is replaced by the simple present "stores." The compound sentence is broken into two.

Inline comments describe why code exists. Use the simple present tense. Do not write: "This check has prevented a race condition since the v2 refactor." Write: "This check prevents a race condition." The present perfect "has prevented" with a time qualifier is replaced by the simple present "prevents." The time qualifier is unnecessary in an inline comment.

### Commit Messages

Commit messages use the imperative mood by convention. The present perfect and past perfect often appear in commit bodies that describe the state before and after the change.

Do not write a commit body that says: "The authentication module had leaked memory on each request. This commit has fixed the leak and has added a regression test." Write: "The authentication module leaked memory on each request. This commit fixes the leak and adds a regression test." The past perfect "had leaked" becomes the simple past "leaked." The present perfect "has fixed" and "has added" become the imperative "fixes" and "adds" (conventional for commit bodies describing the commit's effect).

### Error Messages

Error messages must tell the user what condition exists now. The present perfect adds temporal indirection that weakens the message.

Do not write: "The configuration file has not been found." Write: "The configuration file does not exist." Or: "The system cannot find the configuration file." The present perfect passive "has not been found" is both a compound construction and passive. Replace it with the simple present active construction.

Do not write: "The server has encountered an error and has stopped responding." Write: "The server encountered an error. The server stopped responding." The present perfect "has encountered" and "has stopped" become the simple past "encountered" and "stopped." Break into two sentences for clarity.

---

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python classes)

Class and method documentation in object-oriented codebases often uses the present perfect to describe state that was established during construction or initialization. Replace these with the simple present or simple past.

Do not write: "The constructor has set the default timeout to 30 seconds." Write: "The constructor sets the default timeout to 30 seconds." The present perfect "has set" is a one-time action described as if it has ongoing relevance. The simple present "sets" describes the constructor's permanent behavior.

Do not write: "This singleton has been initialized and all subsequent calls have returned the same instance." Write: "This singleton initializes on the first call. All subsequent calls return the same instance." The present perfect passive "has been initialized" becomes the simple present "initializes." The present perfect "have returned" becomes the simple present "return."

Inheritance documentation should avoid compound tenses entirely. Do not write: "This subclass has overridden the validate method and has added custom error handling." Write: "This subclass overrides the validate method and adds custom error handling." The simple present describes the class as it exists now.

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Pure function documentation describes timeless input-to-output relationships. The present perfect is almost always incorrect because pure functions have no temporal dimension.

Do not write: "The function has applied the transformation to each element and has collected the results." Write: "The function applies the transformation to each element and collects the results." The simple present is the only correct tense for pure function behavior.

Monadic and effectful function documentation can describe sequencing, but still must avoid compound tenses. Do not write: "The first effect has read the file, and the second effect has written the output." Write: "The first effect reads the file. The second effect writes the output." Sequence with separate sentences, not with tense nesting.

### Procedural Documentation (C, Go, Bash)

Procedural documentation often describes multi-step processes where one step must complete before the next begins. The present perfect and past perfect frequently appear to express this sequencing requirement. Replace them with the simple past plus "Then" or with the simple present for prerequisites.

Do not write: "After the script has sourced the environment file, it has checked all the variables and has started the daemon." Write: "The script sources the environment file. Then it checks all the variables. Then it starts the daemon." Three present perfect clauses become three simple present sentences sequenced with "Then."

Do not write: "The function had allocated the buffer before it had validated the size parameter." Write: "The function allocated the buffer. Then it validated the size parameter." Or restructure to show the correct order: "The function validates the size parameter. Then it allocates the buffer."

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative configuration documentation describes desired state. Compound tenses are especially confusing here because they imply a time dimension that does not exist in declarative systems.

Do not write: "The deployment has created three replicas and the service has exposed port 8080." Write: "The deployment specifies three replicas. The service exposes port 8080." The configuration declares what should exist, not what has happened. Use the simple present for all declarations.

Do not write: "After Terraform has applied the plan, the infrastructure will have matched the desired state." Write: "After Terraform applies the plan, the infrastructure matches the desired state." Both the present perfect "has applied" and the future perfect "will have matched" are replaced by the simple present.

### Systems Documentation (Rust ownership, C memory management)

Systems documentation describes invariants, guarantees, and safety conditions that are permanently true. Compound tenses introduce temporal ambiguity into statements that must be absolute.

Do not write: "The function has taken ownership of the string and the caller has lost access to it." Write: "The function takes ownership of the string. The caller loses access to it." Ownership transfer is a permanent fact about the function signature, not a completed event.

Do not write: "The unsafe block has dereferenced the raw pointer after the caller had guaranteed its validity." Write: "The unsafe block dereferences the raw pointer. The caller must guarantee the pointer is valid." The present perfect "has dereferenced" becomes the simple present "dereferences." The past perfect "had guaranteed" becomes a separate requirement statement with "must guarantee."

---

## Extended Examples

### Example 1 — Present Perfect Passive in Build Documentation

> **Non-STE:** The Docker image has been built from the Dockerfile and has been pushed to the registry.
>
> **STE:** The Docker image is built from the Dockerfile. Then it is pushed to the registry.

> *Principle P3 (approved meanings) + Rule 3.4 + Rule 3.6:* "has been built" and "has been pushed" are present perfect passive constructions. The auxiliary "has" combines with the past participle "built" and the passive "been." Use the simple present passive "is built" (which uses "is" + adjective/past participle as a condition, permitted by Rule 3.3). Break into separate sentences.

### Example 2 — Past Perfect in Incident Reports

> **Non-STE:** The monitoring service had detected the memory leak, but the on-call engineer had already restarted the server.
>
> **STE:** The monitoring service detected the memory leak. But the on-call engineer already restarted the server.

> *Principle P3 + Rule 3.4:* "had detected" and "had restarted" are past perfect constructions. Use the simple past "detected" and "restarted." The word "already" preserves the temporal relationship without needing the past perfect.

### Example 3 — Future Perfect in Roadmap Documentation

> **Non-STE:** By the end of Q4, the team will have migrated all microservices to the new service mesh and will have decommissioned the legacy gateway.
>
> **STE:** By the end of Q4, the team will migrate all microservices to the new service mesh. The team will also decommission the legacy gateway.

> *Principle P3 + P4 (approved verb forms) + Rule 3.4:* "will have migrated" and "will have decommissioned" are future perfect constructions. Use the simple future "will migrate" and "will decommission." Break into separate sentences.

### Example 4 — Perfect Infinitive in Setup Instructions

> **Non-STE:** You need to have configured the environment variables before you run the application.
>
> **STE:** Configure the environment variables. Then run the application.

> *Principle P3 + P9 (prefer short, clear instructions) + Rule 3.4:* "to have configured" is a perfect infinitive that combines the infinitive marker "to" with the auxiliary "have" and the past participle "configured." Use the imperative mood with two separate sentences. This is shorter, clearer, and avoids the auxiliary verb entirely.

### Example 5 — Present Perfect in CI/CD Pipeline Logs

> **Non-STE:** The test suite has run 847 tests. The linter has checked 312 files. The coverage tool has generated the report.
>
> **STE:** The test suite ran 847 tests. The linter checked 312 files. The coverage tool generated the report.

> *Principle P3 + Rule 3.4:* Each sentence uses the present perfect "has run," "has checked," "has generated." Pipeline logs describe completed steps. The simple past tense is the correct choice: each step finished, and the log records that fact.

### Example 6 — Compound Auxiliary in Architecture Decision Records

> **Non-STE:** The system will have been operating with the new caching layer for six months before the team will have collected enough data to evaluate the performance gain.
>
> **STE:** The system will operate with the new caching layer for six months. Then the team will collect the data to evaluate the performance gain.

> *Principle P3 + P4 + Rule 3.4:* "will have been operating" combines the auxiliary "will have" with the past participle "been" and the present participle "operating." This is a future perfect progressive construction — three layers of auxiliary nesting. Replace with the simple future "will operate." "will have collected" becomes "will collect." Break into separate sentences.

---

## Edge Cases

### Edge Case 1 — Framework Names That Resemble Auxiliary Verbs

Some tool and library names contain or resemble auxiliary verbs. "Hasura" (a GraphQL engine) contains the substring "has," and "Have I Been Pwned" (a security service) begins with "have." These are proper nouns and technical names (Rule 1.5), not auxiliary verbs. Their use in documentation does not violate Rule 3.4.

> **Correct:** Hasura generates a GraphQL API from your database schema.
> ("Hasura" is a technical noun, not the auxiliary verb "has." The main verb "generates" is in the simple present tense.)

> **Correct:** Check your email address with Have I Been Pwned.
> ("Have I Been Pwned" is a service name, a technical noun phrase. The main verb "Check" is in the imperative mood.)

Do not let a framework name that looks like an auxiliary verb prevent you from using the framework name. The technical noun exemption (Rule 1.5, Rule 1.6) applies.

### Edge Case 2 — Code Method Names That Contain "Has" or "Had"

Many programming languages use method name prefixes like `has`, `have`, or `had` for Boolean checks or property access. JavaScript has `hasOwnProperty`. Java has `hasNext` on iterators. These are technical code nouns (method names), not auxiliary verbs in the grammatical sense.

> **Correct:** The `hasOwnProperty` method checks if the object has a direct property.
> (The first "has" is part of the method name. The second "has" is the main verb in the simple present tense, not an auxiliary.)

Do not write: "Call `hasOwnProperty` after you have checked the prototype chain." Instead write: "Call `hasOwnProperty` after you check the prototype chain." The method name is exempt. The prose verb "have checked" is not.

### Edge Case 3 — Auto-Generated Changelogs and Tool Output

Changelogs generated automatically from commit messages or issue trackers often contain the present perfect or past perfect tense. When you publish these changelogs without manual editing, the raw tool output is exempt from Rule 3.4. When you manually curate or edit the changelog, convert all compound tenses to the simple past or imperative mood.

> **Auto-generated (permitted as-is):** The API gateway has added rate limiting for all endpoints.
> **Manually edited (required):** Add rate limiting for all endpoints. Or: The API gateway added rate limiting for all endpoints.

The exemption applies only to unedited, verbatim tool output. Any human-authored or human-edited changelog entry must follow Rule 3.4.

### Edge Case 4 — The Boundary Between Adjective and Compound Tense

The past participle after "to be" can be either a legitimate adjective (permitted by Rule 3.3) or part of a passive compound construction (prohibited by Rule 3.4 and Rule 3.6). The distinction depends on whether the past participle describes a condition or an action.

> **Correct (adjective / condition):** The configuration file is encrypted.
> ("Encrypted" describes the condition of the file. No agent performs the encryption in this sentence. This is Rule 3.3, not a passive verb construction.)

> **Incorrect (passive action):** The configuration file is encrypted by the setup script.
> (The agent "setup script" performs the action. This is a present passive construction. Rule 3.6 requires the active voice: "The setup script encrypts the configuration file.")

When "by" followed by an agent appears after the past participle, the construction is passive voice and must be restructured. When no agent is present and the past participle describes a state or condition, the construction is an adjective use and is permitted.

### Edge Case 5 — Third-Party Specifications and Quoted Text

When you quote a third-party specification, RFC, or standards document verbatim, the quoted text is not required to follow Rule 3.4. Your own surrounding text must follow all rules.

> **Correct:** The OAuth 2.0 specification states: "The authorization server has issued an access token." (The quoted text uses the present perfect "has issued," which violates Rule 3.4. But it is verbatim third-party content and is permitted.)

Do not modify a third-party quote to make it STE-Code compliant. Either quote it exactly or paraphrase it in your own STE-Code compliant words.

### Edge Case 5 — Historical Narrative in Postmortems and Retrospectives

Postmortem documents describe a sequence of past events. The simple past tense is the primary narrative tense. Do not use the past perfect to sequence events relative to each other. Use the simple past with explicit sequencing words instead.

> **Non-STE:** The load balancer had removed the unhealthy instance before the health check had reported the failure.
> **STE (simple past with sequencing):** The health check reported the failure. Then the load balancer removed the unhealthy instance.

The simple past with "Then" reorders the events into chronological sequence. The reader does not need to decode a two-level temporal relationship.

---

## Cross-References

This rule works together with the verb-form inventory defined in Rule 3.2. Rule 3.2 lists the six approved verb forms. Rule 3.4 prevents you from combining those forms with auxiliary verbs to create unapproved compound tenses.

> **See:** Rule 3.2 — Use Only These Verb Forms and Tenses of Verbs

The past participle is permitted only as an adjective after "to be," "to become," or "to stay." It must not combine with "have" to form a compound tense.

> **See:** Rule 3.3 — Use the Past Participle Form as an Adjective

The auxiliary "have" with a past participle often appears in passive constructions ("has been deployed"). Rule 3.6 requires the active voice, which eliminates both the auxiliary and the passive structure.

> **See:** Rule 3.6 — Use the Active Voice

The "-ing" form combined with "have been" creates complex progressive perfect constructions ("has been running"). Rule 3.5 restricts the "-ing" form to technical nouns and modifiers only.

> **See:** Rule 3.5 — Use the "-ing" Form of a Verb Only as a Technical Noun or as a Modifier in a Technical Noun

The dictionary lists the approved forms for each verb. Only the infinitive, imperative, simple present, simple past, simple future, and past participle as an adjective are approved.

> **See:** Rule 3.1 — Use Only the Verb Forms That Are Given in the Dictionary

> **See:** STE-Code Approved Dictionary — Verbs Section

Technical verbs that are approved for code documentation (build, deploy, test, lint, compile, run) follow the same form restrictions as all other verbs. A technical verb combined with "has" is still a compound tense and is not approved.

> **See:** Rule 1.12 — Technical Verbs Are Allowed

---

## Grammar Notes

### The Auxiliary Verb "Have" as a Tense Marker

In English grammar, the auxiliary verb "have" combines with the past participle to mark perfect aspect. The present perfect ("has built") marks a past action with present relevance. The past perfect ("had built") marks an action completed before another past point. The future perfect ("will have built") marks an action completed before a future point.

All three perfect constructions add a layer of temporal reasoning. The reader must compute the relationship between the action, the reference point, and the present moment. In code documentation, this temporal reasoning is unnecessary. Code entities have permanent behavior. Build steps complete in sequence. Functions return values every time they are called. The simple tenses express all of these relationships directly.

### Why the Present Perfect Is Not Approved

The present perfect ("has deployed," "have tested") bridges past and present. It tells the reader that a past action has consequences now. But in code documentation, you can state the consequence directly. Instead of "The linter has found three errors" (action in the past, result relevant now), write "The linter found three errors" (simple past for the action) or "Three errors exist in the source file" (simple present for the current state).

The present perfect also introduces ambiguity about when the action occurred. "The team has fixed the bug" does not tell the reader when the fix happened. "The team fixed the bug in version 2.3" states both the action and the time. The simple past with a time qualifier is more informative.

### Why the Past Perfect Is Not Approved

The past perfect ("had committed," "had initialized") places one past event before another past event. This two-level temporal nesting forces the reader to build a timeline. Code documentation can sequence events with simpler tools: separate sentences, the word "Then," or chronological ordering.

The past perfect is also unnecessary when the sequence of events is obvious from context. "The developer committed the changes. Then the reviewer approved the pull request." The word "Then" makes the sequence explicit. The past perfect "had committed" and "had approved" add no information that "committed" and "approved" with "Then" do not already provide.

### Why the Future Perfect Is Not Approved

The future perfect ("will have migrated," "will have completed") projects the reader forward to a future point and then looks backward at a completed action. This double temporal shift is the most complex of the perfect constructions. Replace it with the simple future plus a time qualifier.

> **Complex:** By December, the team will have decommissioned the monolith.
> **Simple:** The team will decommission the monolith by December.

The simple future version places the action in the future and specifies the deadline. The reader processes one temporal relationship instead of two.

### The Perfect Infinitive

The perfect infinitive ("to have built," "to have configured") combines the infinitive marker "to" with the auxiliary "have" and the past participle. It often appears in prerequisite instructions: "You need to have installed the dependencies." This construction is not approved because it embeds a compound tense inside an infinitive phrase.

Replace the perfect infinitive with either the simple imperative or the simple present. "Install the dependencies" (imperative) or "You must install the dependencies" (simple present with modal "must") are both approved alternatives.

### The Distinction Between Auxiliary "Have" and Main Verb "Have"

The verb "have" can function as either an auxiliary verb or a main verb. As an auxiliary, it combines with a past participle to form a perfect tense: "The server has stopped." As a main verb, it expresses possession or requirement: "The function has three parameters," "You have to install the dependencies."

When "have" is a main verb, Rule 3.4 does not apply. The main verb "have" is permitted in all approved tenses: "The class has two constructors" (simple present), "The old API had five endpoints" (simple past), "The next version will have WebSocket support" (simple future).

The distinction is syntactic: if "have" is followed by a past participle and there is no direct object between them, "have" is probably an auxiliary. If "have" is followed by a noun phrase or an infinitive with "to," it is a main verb.

> **Correct (main verb "have"):** The service has a health check endpoint.
> **Correct (main verb "have"):** You have to set the environment variables.
> **Incorrect (auxiliary "have"):** The service has exposed a health check endpoint.
> **Correct (simple past):** The service exposed a health check endpoint.
