# Rule 3.3 — Use the Past Participle Form as an Adjective

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.3

## Original Rule

Use the past participle form as an adjective.

When you use the past participle form as an adjective, it shows the condition of something. This is not passive voice. Use the past participle form of a verb as an adjective as follows:

- Before a noun
- After a verb form of the verbs "to be," "to become," or "to stay."

Do not use the past participle form if it is not in the dictionary.

Examples:

> **STE:** Examine all parts of the disassembled unit for damage.
> ("Disassembled" is an adjective before the noun "unit." It shows the condition of the unit.)

> **Source:** Issue 9, Part 1 — Writing rules, Page 1-3-2, 2025-01-15

> **STE:** When the unit is fully disassembled, clean all the parts.
> ("Disassembled" is an adjective after the verb "to be" that shows the condition of the unit.)

There are also approved adjectives in the dictionary that are the past participle form of verbs that are not approved. For example, "permitted," and "damaged." Their approved part of speech in the dictionary is "(adj)" and thus you can use them.

## STE-Code Adaptation

Use the past participle form of an approved verb only as an adjective. The past participle as an adjective describes the condition of a code entity (a file, a binary, a service, a module) and is not a verb form in a compound tense.

Use the past participle form as an adjective in these two positions:

- Before a noun: "the compiled binary," "the encrypted payload," "the deprecated endpoint"
- After a verb form of "to be," "to become," or "to stay": "When the binary is compiled," "After the module becomes initialized," "The service stays connected"

Do not use the past participle as part of a compound verb construction with "have" (Rule 3.4). If a past participle form is not listed in the approved vocabulary, do not use it.

> **See also:** Rule 3.4 — Do Not Use Auxiliary Verbs to Make Complex Verb Constructions

The STE-Code vocabulary also has approved adjectives that are the past participle form of verbs that are not approved as verbs. For example, "deprecated" is approved as an adjective (adj) even though "deprecate" is not an approved verb. You can use these adjectives when they describe a condition.

### Examples

The sentence below is already in STE because "compiled" is an adjective before the noun "binary," not a verb in a compound tense:

> **STE:** Examine all parts of the compiled binary for errors.

> *Adapted from spec pair: "Examine all parts of the disassembled unit for damage."* Just as "disassembled" is an adjective before the noun "unit" in STE, "compiled" is an adjective before the noun "binary" in STE-Code. Both describe the condition of the thing being examined.

The pairs below show transformations from non-compliant compound-verb constructions to compliant adjective usage:

> **Non-STE:** When you have compiled the binary, run the test suite.
>
> **STE:** When the binary is compiled, run the test suite.
> ("Compiled" is an adjective after the verb "to be" that shows the condition of the binary.)

> *Adapted from spec pair: "When the unit is fully disassembled, clean all the parts."* Just as "disassembled" after "is" describes the condition of the unit in STE, "compiled" after "is" describes the condition of the binary in STE-Code. This is an adjective, not a passive verb construction.

> **Non-STE:** Review all of the updated configuration settings that the script has generated.
>
> **STE:** Review all the updated configuration settings.
> ("Updated" is an adjective before the noun "configuration settings." It shows the condition of the settings.)

> *Adapted from spec pair: "Examine all parts of the disassembled unit for damage."* Just as "disassembled" is a past participle used as an adjective before the noun in STE, "updated" is a past participle used as an adjective before "configuration settings" in STE-Code. The compound verb construction "has generated" is removed entirely, leaving only the adjective "updated" to describe the condition.

---

## Code-Domain Explanation

Rule 3.3 controls whether a past participle form describes a condition (adjective, permitted) or forms part of a compound verb tense (verb, not permitted). The distinction is subtle but critical across all code documentation types because the same word can serve either role depending on its syntactic position.

### README Files

README files use past participles as adjectives to describe the state of artifacts, dependencies, or configurations. The adjective describes a condition that the reader must understand before proceeding: "the installed dependencies," "the configured environment," "the built binary."

Do not write: "After you have installed the dependencies, you have configured the environment." Write: "After the dependencies are installed, check that the environment is configured." The past participles "installed" and "configured" appear after forms of "to be" and describe conditions. The compound verb constructions "have installed" and "have configured" are removed.

> **Non-STE:** Once you have cloned the repository and have installed the toolchain, the project has been set up for development.
>
> **STE:** After you clone the repository and install the toolchain, the project is set up for development.
> ("Set up" after "is" describes the condition of the project. The compound forms "have cloned," "have installed," and "has been set up" are removed.)

### API Documentation

API reference docs use past participles as adjectives to describe the state of a response, a resource, or a system after an operation completes. The adjective form of the past participle is the correct choice for describing post-condition states: "the created resource," "the updated record," "the deleted entity."

When an API endpoint returns a resource that has been modified, use the past participle as an adjective before the noun: "the encrypted response," "the serialized payload," "the validated input." Never use the past participle with "have" in API documentation: "The endpoint has encrypted the response" becomes "The endpoint gives the encrypted response."

> **Non-STE:** After the request has completed, the server has cached the result, and the client has received the updated state.
>
> **STE:** After the request completes, the server caches the result. The client gets the updated state.
> ("Updated" is an adjective before "state." The compound verbs "has completed," "has cached," and "has received" are replaced with simple present tense verbs.)

### Docstrings and Inline Comments

Docstrings describe what a function returns or what state it produces. The past participle as an adjective is the correct form for describing the output condition: "Returns the sorted list," "Gives the parsed configuration," "Writes the encrypted data to the output stream."

The most common Rule 3.3 violation in docstrings is using the past participle as part of a return-value description that accidentally forms a compound tense: "The function has returned the sorted list." The simple present tense "Returns the sorted list" is correct because "sorted" is an adjective before "list."

Inline comments describe the state of variables or the condition of the system at a point in the code. Use past participles as adjectives: "The buffer contains the encoded payload," "The cache holds the compiled templates." Never use compound forms: "The buffer has contained the encoded payload" is incorrect.

> **Non-STE:** /** 
>  * This method has built the query and has returned the prepared statement.
>  * The connection has been closed after the result set has been read.
>  */
> **STE:** /**
>  * This method builds the query and gives the prepared statement.
>  * The method closes the connection after it reads the result set.
>  */
> ("Prepared" remains as an adjective before "statement" — it is a code-domain technical term. The compound forms are removed.)

### Commit Messages

Commit messages use the imperative mood, not the past participle. However, the commit body can use past participles as adjectives to describe the state of the codebase before or after the change: "The broken test suite," "The deprecated middleware," "The corrupted index file."

Never use a past participle as a main verb in a commit message body to form a compound tense: "The parser had broken the input handling" becomes "The parser broke the input handling" (simple past) or "The parser caused broken input handling" (adjective before noun).

> **Non-STE:** The old cache layer has caused corrupted entries. This commit has replaced the cache with a version that has passed all integration tests.
>
> **STE:** The old cache layer caused corrupted entries. This commit replaces the cache with a version that passed all integration tests.
> ("Corrupted" is an adjective before "entries." The compound forms "has caused," "has replaced," and "has passed" are removed.)

### Error Messages

Error messages use past participles as adjectives to describe the failed condition: "The connection is closed," "The input is malformed," "The file is locked." These constructions use "is" plus a past participle adjective to state the condition. They are not passive voice because no agent performs the action.

Do not use past participles with "have" in error messages: "The connection has closed" becomes "The connection is closed." The "is + adjective" construction states the current condition. The "has + past participle" construction describes a past event with present relevance, which is less direct.

> **Non-STE:** ERROR: The request has failed because the database has become disconnected and the retry policy has stopped.
>
> **STE:** ERROR: The request failed because the database is disconnected. The retry policy stopped.
> ("Disconnected" is an adjective after "is" describing the database condition. The compound forms "has failed," "has become," and "has stopped" are replaced with simple past tense.)

---

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Class documentation uses past participles as adjectives to describe object state, initialization status, and lifecycle phases. The adjective form is the correct choice for describing the condition of a class member or a constructed object.

Common OOP adjectives from past participles: "the initialized field," "the disposed resource," "the locked mutex," "the connected socket," "the configured instance," "the overridden method," "the inherited property."

The distinction between adjective and passive voice is especially important in constructor documentation. "The constructor initializes the fields" (active) describes the action. "The fields are initialized" (adjective after "to be") describes the post-condition. Both are correct for different purposes. Neither uses "have initialized."

> **Non-STE:** After the factory has created the object, the dependency injector has resolved all the required services, and the lifecycle manager has initialized the component.
>
> **STE:** After the factory creates the object, the dependency injector resolves all the required services. The lifecycle manager initializes the component.
> ("Required" is an adjective before "services." The compound verbs are replaced with simple present tense.)

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional documentation rarely uses the past tense or past participle because pure functions describe timeless transformations. The past participle as an adjective appears most often in descriptions of data that has been transformed: "the mapped collection," "the filtered list," "the reduced value."

In functional programming, many code-domain technical nouns are themselves past participles: "folded," "zipped," "curried," "composed." These are technical adjectives that describe the processing that produced a value. They are permitted as adjectives under Rule 3.3 even though the corresponding verbs ("to fold," "to zip," "to curry") are technical verbs not in the controlled terminology.

> **Non-STE:** After the transducer has transformed the stream, the reducer has combined the results, and the pipeline has produced the final output.
>
> **STE:** The transducer transforms the stream. The reducer combines the results. The pipeline produces the final output.
> *("Transformed," "combined," and "produced" would be compound verb forms if kept. The STE version uses simple present tense throughout.)*

### Procedural Documentation (C, Go, Bash)

Procedural documentation uses past participles as adjectives to describe the state of resources, buffers, file descriptors, and memory allocations. The adjective form describes conditions that the next step depends on: "the opened file descriptor," "the allocated buffer," "the linked library."

In C documentation, memory-state adjectives are critical for correctness: "the freed pointer," "the initialized struct," "the zeroed memory." These describe the condition of memory after an operation, not the operation itself. "The pointer was freed" (adjective) describes the state. "The function freed the pointer" describes the action. Both are correct STE-Code — neither uses "has freed."

> **Non-STE:** After the program has allocated the buffer and has opened the file, it has read the data into the initialized memory region.
>
> **STE:** After the program allocates the buffer and opens the file, it reads the data into the initialized memory region.
> ("Initialized" is an adjective before "memory region." The compound verbs are replaced with simple present tense.)

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documentation uses past participles as adjectives to describe the desired or actual state of infrastructure. The adjective form maps directly to the declarative model: the configuration declares the desired condition, and the system enforces it.

Common declarative adjectives from past participles: "the provisioned resource," "the applied configuration," "the deployed pod," "the indexed column," "the encrypted secret," "the mounted volume." These describe conditions that the system maintains. They are never verbs in compound tenses.

> **Non-STE:** After Terraform has applied the plan, the VPC has been provisioned, and the subnets have been created in the configured availability zones.
>
> **STE:** After Terraform applies the plan, the VPC is provisioned. The subnets exist in the configured availability zones.
> ("Configured" is an adjective before "availability zones." "Provisioned" is an adjective after "is" describing the VPC condition. The compound forms are removed.)

### Systems Documentation (Rust Ownership, C Memory Management)

Systems documentation uses past participles as adjectives to describe invariants and safety conditions. The adjective form states a permanent condition that the type system or runtime enforces: "the borrowed reference," "the moved value," "the dropped allocation."

In Rust, many safety-critical states are described with past participles as adjectives: "the pinned future," "the locked mutex guard," "the initialized memory." These are conditions, not actions. The Rust compiler enforces these conditions. The documentation describes them.

> **Non-STE:** After the thread has acquired the lock and has read the shared data, the borrow checker has verified that no aliased mutable references exist.
>
> **STE:** After the thread acquires the lock and reads the shared data, the borrow checker verifies that no aliased mutable references exist.
> ("Aliased" is an adjective before "mutable references." The compound verbs are replaced with simple present tense.)

---

## Extended Examples

### Example 1 — README: Build State Description

> **Non-STE:** After you have run the build script, the compiled artifacts have been placed in the dist/ directory. The tests have passed, and the linter has checked the source for style violations.
>
> **STE:** After you run the build script, the compiled artifacts are in the dist/ directory. The tests passed. The linter checked the source for style violations.

> **Principle applied:** Rule 3.3 (past participle as adjective, not compound verb) + Rule 3.4 (no auxiliary verbs). "Compiled" is retained as an adjective before "artifacts" — it describes the condition of the artifacts. The compound forms "have run," "have been placed," "have passed," and "has checked" are replaced with simple past tense or "to be" constructions. **Explanation:** The non-STE version uses four compound verb constructions with "have" that violate Rules 3.3 and 3.4. The STE version keeps the one legitimate adjective use ("compiled artifacts") and replaces all compound verb forms with simple tenses. This is the core discipline of Rule 3.3: identify whether the past participle describes a condition (keep) or forms part of a compound tense (replace).

### Example 2 — API Documentation: Response Description

> **Non-STE:** The GET /api/config endpoint has returned the updated configuration. The middleware has encrypted the response, and the logger has written the access event to the audit trail.
>
> **STE:** The GET /api/config endpoint gives the updated configuration. The middleware encrypts the response. The logger writes the access event to the audit trail.

> **Principle applied:** Rule 3.3 + Rule 3.2 (approved tenses) + P1 (approved words: "return" → "give"). "Updated" is an adjective before "configuration." The compound verb forms "has returned," "has encrypted," and "has written" are replaced with simple present tense verbs. **Explanation:** API documentation describes permanent behavior. The simple present tense is correct for what each component does. The past participle "updated" correctly describes the condition of the configuration data (it has been changed from a previous state). The non-STE version incorrectly uses the present perfect to describe permanent behavior, conflating "what happened once" with "what always happens."

### Example 3 — Python Docstring: Data Pipeline

> **Non-STE:** def transform(self, data: list) -> dict:
>     """
>     Has processed the input and has returned a grouped result.
>     The method has filtered invalid entries and has sorted the
>     remaining items. It has written the transformed output to
>     the configured destination.
>     """
> **STE:** def transform(self, data: list) -> dict:
>     """
>     Process the input and give a grouped result.
>     The method filters invalid entries and sorts the
>     remaining items. It writes the transformed output to
>     the configured destination.
>     """

> **Principle applied:** Rule 3.3 + Rule 3.1 (approved verb forms) + Rule 3.2. "Transformed" is an adjective before "output" — it describes the condition of the output data. "Configured" is an adjective before "destination" — it describes the condition of the destination. The compound forms "has processed," "has returned," "has filtered," "has sorted," and "has written" are removed. **Explanation:** This docstring uses the present perfect ("has processed") throughout, which is incorrect for docstrings that describe permanent behavior. The STE version uses the imperative mood for the first line ("Process" and "give") and the simple present tense for the descriptive sentences. The two legitimate adjective uses — "transformed output" and "configured destination" — are preserved because they describe conditions, not compound actions.

### Example 4 — Commit Message Body: State Before and After

> **Non-STE:** The authentication middleware has leaked memory under load.
> The session store has kept references to expired tokens that the
> garbage collector has failed to reclaim. This fix has added an
> explicit cleanup step and has improved the test coverage for the
> affected code paths.
> **STE:** The authentication middleware leaked memory under load.
> The session store kept references to expired tokens. The garbage
> collector failed to reclaim these tokens. This fix adds an explicit
> cleanup step and improves the test coverage for the affected code paths.

> **Principle applied:** Rule 3.3 + Rule 3.2 (approved tenses) + P1 (keep simple). "Expired" is an adjective before "tokens" — it describes the condition of the tokens. "Affected" is an adjective before "code paths." The compound forms "has leaked," "has kept," "has failed," "has added," and "has improved" are replaced with simple past tense (for the bug description) and simple present tense (for what the fix does). **Explanation:** Commit message bodies describe past events (the bug) and present changes (the fix). The simple past tense correctly reports the bug behavior. The simple present tense correctly reports what the commit does. The two adjective uses — "expired tokens" and "affected code paths" — correctly describe conditions without forming compound tenses.

### Example 5 — Configuration File Comment: System Settings

> **Non-STE:** # The cache TTL (time-to-live) in seconds. Cached entries older
> # than this value are considered expired and will be evicted by the
> # background cleaner. This setting has been tuned based on the
> # production workload that has averaged 500 requests per second.
> # CACHE_TTL=300
> **STE:** # The cache TTL (time-to-live) in seconds. Cached entries older
> # than this value are expired. The background cleaner evicts them.
> # This value comes from tuning with the production workload. The
> # workload averages 500 requests per second.
> # CACHE_TTL=300

> **Principle applied:** Rule 3.3 + Rule 3.2 + P1 (use approved words: "evicted" → "evicts" or restructured; "tuned" → restructured). "Expired" is an adjective after "are" — it describes the condition of the entries. "Cached" is an adjective before "entries." The compound forms "has been tuned" and "has averaged" are removed. **Explanation:** Configuration file comments describe permanent settings and their rationale. The adjective "expired" correctly describes the condition that triggers eviction. The compound passive "has been tuned" is replaced with an active, simple-present explanation of the setting's origin. The word "evicted" is a technical term for cache removal — it is used as an active simple-present verb ("evicts"), not a past participle.

### Example 6 — Error Message: Resource State

> **Non-STE:** FATAL: The connection pool has exhausted its available
> connections. The health check has detected the condition after the
> connection timeout has expired. The failed request has been logged.
> **STE:** FATAL: The connection pool is exhausted. The health check
> detected the condition after the connection timeout expired.
> The system logged the failed request.

> **Principle applied:** Rule 3.3 + Rule 3.4 (no auxiliary verbs) + Rule 3.6 (active voice). "Exhausted" is an adjective after "is" — it describes the condition of the pool. "Failed" is an adjective before "request." The compound forms "has exhausted," "has detected," "has expired," and "has been logged" are replaced. **Explanation:** Error messages should state the current condition directly. "The connection pool is exhausted" tells the user the condition now. "The connection pool has exhausted" describes a past event that may or may not still be true. The simple past "detected" and "expired" correctly report completed events in sequence. The passive "has been logged" is replaced with active voice "The system logged."

---

## Edge Cases

### Edge Case 1 — The Adjective vs. Passive Voice Distinction

**Scenario:** The past participle after a form of "to be" can be either an adjective describing a condition or a passive voice verb describing an action. "The file is encrypted" is ambiguous: it could mean the file is in an encrypted state (adjective) or the file receives encryption from an unnamed agent (passive voice). Rule 3.3 permits the adjective reading. Rule 3.6 requires active voice.

**Guidance:** When the sentence describes a condition without naming an agent, treat the past participle as an adjective (Rule 3.3 permits this). When the sentence names or implies an agent (especially with "by"), treat it as passive voice and convert to active voice (Rule 3.6 requires this). The test: can you add "by the system" or "by the user" after the past participle? If the sentence still makes sense, it is passive voice and should be rewritten. If the addition sounds unnatural, it is an adjective.

> **Adjective (permitted):** The database is connected. (Condition. Adding "by the administrator" changes the meaning.)
> **Passive (requires rewrite):** The database is connected by the startup script. → The startup script connects the database.
> **Adjective (permitted):** The file is encrypted. (Condition. The file is in an encrypted state.)
> **Passive (not permitted as written):** The file is encrypted by the pipeline. → The pipeline encrypts the file.

### Edge Case 2 — Verbs Where the Past Participle Is Identical to the Base Form

**Scenario:** Some approved verbs have a past participle identical to the base form: SET (SET, SETS, SET, SET), PUT (PUT, PUTS, PUT, PUT), SHUT (SHUT, SHUTS, SHUT, SHUT), CUT (CUT, CUTS, CUT, CUT), HIT (HIT, HITS, HIT, HIT). When the word "set" appears in documentation, it could be an adjective, a base-form verb, or a past-tense verb. The reader must rely on context to determine the role.

**Guidance:** When these words appear before a noun, they are adjectives: "the set configuration," "the put request," "the shut connection." When they appear after a form of "to be," check whether they describe a condition (adjective) or form part of a pattern where the agent is implied (passive): "The configuration is set" describes the condition. "The configuration is set by the installer" is passive and should become "The installer sets the configuration."

Never add "-ed" to these verbs to form the past participle. "Setted," "putted," "shutted," "cutted," and "hitted" are not listed forms and violate Rule 3.1.

> **Correct:** The timeout is set to 30 seconds. (Adjective after "is" — condition.)
> **Correct:** The worker shut the connection. (Simple past tense — completed action.)
> **Incorrect:** The timeout has been setted to 30 seconds. ("Setted" is not a listed form. Use "The timeout is set to 30 seconds.")
> **Incorrect:** The worker has shutted the connection. ("Shutted" is not a listed form. Use "The worker shut the connection.")

### Edge Case 3 — Code-Domain Technical Nouns That Are Past Participles

**Scenario:** Many code-domain technical nouns are themselves past participles. Examples: "compiled" as in "compiled language," "interpreted" as in "interpreted language," "managed" as in "managed code," "unmanaged" as in "unmanaged resources," "distributed" as in "distributed system," "embedded" as in "embedded database." These words are technical nouns or modifiers, not verbs in compound tenses.

**Guidance:** When a past participle form is a recognized code-domain technical term that names a category or classification, treat it as a technical noun or modifier (permitted under Rule 1.5). The fact that the word is also a past participle of a verb is not relevant — its role in the sentence is noun or modifier, not verb. The test: does the word name a category of thing in the domain? If yes, it is a technical term. If the word describes what an agent did, it is a verb use and must follow Rule 3.3.

> **Correct (technical modifier):** This library targets compiled languages and interpreted runtimes.
> ("Compiled" and "interpreted" classify languages and runtimes — technical modifiers.)
> **Correct (technical modifier):** The framework handles distributed transactions across multiple nodes.
> ("Distributed" classifies transactions — technical modifier.)
> **Incorrect (verb use):** The build system has compiled the library and has distributed the artifacts.
> (These are compound verb forms. Use: "The build system compiled the library and distributed the artifacts.")

### Edge Case 4 — Generated Code and Documentation

**Scenario:** Auto-generated documentation, scaffolded code comments, and tool-produced README files often contain compound verb constructions with "have" + past participle. For example, a code generator might produce: "This class has been generated by the OpenAPI code generator." Generated content is raw tool output.

**Guidance:** Apply the same exemption as Rule 3.2: fully automated output from tools (with no manual editing) is exempt from Rule 3.3. The tool output is a raw data feed, not authored documentation. However, any content you write manually — including the introduction, surrounding explanation, or manually edited sections of the generated document — must follow Rule 3.3.

If you edit a generated document, convert compound verb constructions to compliant forms for the sections you touch. Do not rewrite the entire generated file unless you own the maintenance of that file.

> **Auto-generated (permitted):** This client library has been generated from the OpenAPI specification v2.3.1.
> **Manually written (preferred):** The OpenAPI specification v2.3.1 generated this client library.
> **Guidance for hybrid documents:** If the README is 90% generated and 10% manually written, the 10% must follow Rule 3.3. The 90% is exempt.

### Edge Case 5 — Adjectives from Unapproved Verbs That Are Not in the Dictionary

**Scenario:** The original ASD-STE100 rule notes that some approved adjectives are the past participle form of verbs that are not approved. Examples from aerospace: "permitted" (from "permit," not approved), "damaged" (from "damage," not approved). In code documentation, the equivalent case is an adjective like "deprecated" (from "deprecate," not an approved verb) or "obfuscated" (from "obfuscate," not an approved verb). The adjective is approved and usable. The verb is not.

**Guidance:** Check the STE-Code dictionary for the adjective entry. If the word appears with part-of-speech tag "(adj)" and the meaning matches your usage, you can use it as an adjective regardless of whether the corresponding verb is approved. You cannot use the verb form. "This function is deprecated" (adjective after "is") is correct. "The developer deprecated this function" (verb) is not correct — use "The developer marked this function as deprecated."

This edge case also applies to code-domain adjectives that the community widely uses: "minified" (from "minify"), "transpiled" (from "transpile"), "serialized" (from "serialize"), "memoized" (from "memoize"). These are technical adjectives under Rule 1.5. They are not verbs in the STE-Code controlled terminology.

> **Correct (adjective from unapproved verb):** The deprecated endpoint gives a 410 Gone status.
> **Correct (adjective from unapproved verb):** The minified bundle loads faster than the source files.
> **Incorrect (verb from unapproved verb):** The team deprecated the endpoint in version 3.0.
> **Correct (rewrite with approved verb):** The team marked the endpoint as deprecated in version 3.0.

---

## Cross-References

This rule is the third rule in Section 3 (Verbs) of the STE-Code specification. It defines the only legitimate use of the past participle form: as an adjective describing a condition. Every other use of the past participle form — in compound tenses, in passive voice, or as a main verb — is prohibited by other rules that this rule supports.

| Rule | Title | Relationship to Rule 3.3 |
|------|-------|---------------------------|
| **Rule 3.1** | Use Only the Verb Forms That Are Given in the Dictionary | Supplies the past participle form for every approved verb. Rule 3.3 requires that the past participle you use as an adjective is the listed fourth form. If the dictionary does not list a past participle, you cannot use it as an adjective (unless it is separately approved as an adjective entry). |
| **Rule 3.2** | Use Only These Verb Forms and Tenses of Verbs | Lists the past participle as the sixth and final approved form, with the restriction "as an adjective." Rule 3.3 is the detailed specification of that restriction. Together, the two rules define the boundary: past participle as adjective (permitted) vs. past participle as verb form (not permitted). |
| **Rule 3.4** | Do Not Use Auxiliary Verbs to Make Complex Verb Constructions | Prohibits "have/has/had" + past participle as a compound tense. Rule 3.3 provides the escape: convert the past participle to an adjective after "to be" or before a noun. Rule 3.4 says what not to do. Rule 3.3 says what to do instead. |
| **Rule 3.6** | Use the Active Voice | Requires active voice over passive voice. Rule 3.3 distinguishes the adjective reading from the passive reading: "The file is encrypted" (adjective, permitted) is distinct from "The file is encrypted by the pipeline" (passive, requires rewrite). Rule 3.3 defines what stays adjective. Rule 3.6 defines what must become active. |
| **Rule 1.2** | Use Approved Words Only as the Specified Part of Speech | Ensures that a past participle used as an adjective is indeed approved as an adjective in the dictionary. If the word is only approved as a verb, its past participle form is not approved as a standalone adjective. |
| **Rule 1.4** | Use Only the Approved Forms of Verbs and Adjectives | The general morphological rule. Rule 3.3 is the application of Rule 1.4 to past participles specifically. For verb-based adjectives, Rule 1.4 requires the listed adjective form (which is often the past participle). Rule 3.3 defines the two syntactic positions where that form is permitted as an adjective. |
| **Rule 1.5** | You Can Use Words That You Can Include in a Technical Noun Category | Permits technical nouns and modifiers that are past participles (e.g., "compiled language," "distributed system"). Rule 3.3 does not restrict technical modifiers — they are nouns/modifiers, not verbs. But the distinction between a technical modifier and a verb use requires Rule 3.3's syntactic-position test. |

**Dictionary reference:** See `a-dictionary.md` for the full STE-Code controlled terminology. The dictionary lists each approved verb's past participle as the fourth form. It also lists standalone adjectives that are past participles of unapproved verbs (e.g., DEPRECATED (adj), PERMITTED (adj)). Rule 3.3 applies to both categories: the fourth form of an approved verb used as an adjective, and the standalone adjective entry that happens to be a past participle form.

**Key dictionary entries referenced in this rule:**

- **BUILD (v), BUILDS, BUILT, BUILT:** BUILT is the past participle. Use as adjective: "the built artifact," "the binary is built."
- **COMPILE (v), COMPILES, COMPILED, COMPILED:** COMPILED is the past participle. Use as adjective: "the compiled output," "the code is compiled."
- **ENCRYPT (v), ENCRYPTS, ENCRYPTED, ENCRYPTED:** ENCRYPTED is the past participle. Use as adjective: "the encrypted payload," "the channel is encrypted."
- **DEPRECATED (adj):** Standalone adjective from the unapproved verb "deprecate." Use as adjective: "the deprecated function," "the API is deprecated."
- **PERMITTED (adj):** Standalone adjective from the unapproved verb "permit." Use as adjective: "the permitted values," "the operation is permitted."
- **WRITE (v), WRITES, WROTE, WRITTEN:** WRITTEN is the past participle. Note the distinct form from the simple past (WROTE). Use as adjective: "the written data," "the file is written."

---

## Grammar Notes

### The Adjective vs. Verb Distinction: Syntactic Position

Rule 3.3 is the only rule in Section 3 that permits a verb form to function as another part of speech. The past participle is simultaneously a verb form (the fourth listed form) and an adjective form (when used in the two approved syntactic positions). This dual nature is the source of most Rule 3.3 violations: the writer uses the past participle in the wrong syntactic position, converting an adjective into a verb in a compound tense.

The two approved syntactic positions are:

1. **Attributive position** (before a noun): The past participle modifies a noun directly, like any adjective. "The compiled binary" follows the pattern "article + adjective + noun." The past participle "compiled" supplies a condition attribute to "binary." This position is unambiguous: the word before a noun and after a determiner is an adjective.

2. **Predicative position** (after "to be," "to become," "to stay"): The past participle follows a linking verb and describes the subject. "The binary is compiled" follows the pattern "subject + linking verb + subject complement." The past participle "compiled" is the complement. This position is superficially identical to the passive voice pattern "subject + to be + past participle," which is why Edge Case 1 exists.

The unapproved syntactic position is:

3. **Compound tense position** (after "have/has/had"): "The pipeline has compiled the binary" follows the pattern "subject + have + past participle + object." This is the present perfect tense, which Rule 3.2 prohibits. The past participle "compiled" is the main verb in a compound tense construction, not an adjective.

The writer's task under Rule 3.3 is to inspect every past participle and confirm it occupies position 1 or 2 (adjective) rather than position 3 (compound verb).

### Why "Have" + Past Participle Is Prohibited but "To Be" + Past Participle Is Permitted

The original ASD-STE100 makes a fundamental distinction: "to be" + past participle can be an adjective construction, but "have" + past participle is always a verb construction. This distinction carries directly into STE-Code.

When "to be" (is, are, was, were) precedes a past participle, the construction can describe a condition: "The service is stopped" (the service is in a stopped condition). The past participle functions as an adjective describing the subject. This is the predicative adjective position.

When "have" (has, have, had) precedes a past participle, the construction always forms a compound tense: "The service has stopped" (the stopping action completed at some point before now). The past participle is part of the verb phrase. This is the compound tense position, which Rule 3.4 explicitly prohibits.

The test for adjective vs. verb is substitution. An adjective in the predicative position can be replaced with any other adjective: "The service is stopped" → "The service is ready," "The service is active." The sentence structure remains valid. A past participle in a compound tense cannot be replaced with a simple adjective: "The service has stopped" → "The service has ready" is ungrammatical. The test confirms that "stopped" in the first sentence is an adjective, and "stopped" in the second sentence is a verb.

### The "To Become" and "To Stay" Constructions

The original ASD-STE100 lists three linking verbs that can precede a past participle adjective: "to be," "to become," and "to stay." In code documentation, "to become" describes a state transition: "The module becomes initialized after the bootstrap sequence completes." "Initialized" is an adjective describing the post-transition condition of the module.

"To stay" describes a condition that persists: "The connection stays encrypted for the duration of the session." "Encrypted" is an adjective describing the persistent condition of the connection.

These two linking verbs are less common than "to be" in code documentation, but they serve specific purposes. "To become" is useful for describing initialization, startup, and warm-up phases. "To stay" is useful for describing invariants, guarantees, and persistent configurations.

Do not use "to become" or "to stay" as a workaround for passive voice. "The configuration becomes applied" is not an improvement over "The configuration is applied." The past participle after "to become" must describe a genuine condition change, not an action. If an agent performs the action, use active voice: "The system applies the configuration."

### Adjectives from Unapproved Verbs: The Dictionary Mechanism

The original ASD-STE100 rule explicitly states: "There are also approved adjectives in the dictionary that are the past participle form of verbs that are not approved." The dictionary mechanism is the key. The adjective must have its own entry with the "(adj)" part-of-speech tag.

In STE-Code, this mechanism applies to code-domain adjectives like "deprecated," "minified," "obfuscated," and "serialized." These words are not approved as verbs (DEPRECATE, MINIFY, OBFUSCATE, SERIALIZE do not appear in the controlled terminology as verb entries). They are approved as adjectives (DEPRECATED (adj), MINIFIED (adj), etc.). Rule 3.3 permits their use as adjectives in the two approved syntactic positions.

The dictionary mechanism prevents the back-formation of verbs from these adjectives. If DEPRECATED is only in the dictionary as "(adj)," you cannot write "The developer deprecated the function." The verb does not exist in the controlled terminology. You must restructure: "The developer marked the function as deprecated" (using the approved verb "mark" and the adjective "deprecated").

This mechanism is a safety feature adapted from aerospace. In aircraft maintenance, "damaged" is an approved adjective but "damage" is not an approved verb. You can say "The part is damaged" (condition) but not "The mechanic damaged the part" (action using an unapproved verb). The same discipline applies to code documentation: you can describe the condition of deprecated code, but you cannot describe the action of deprecating it with the unapproved verb "deprecate."

### The Past Participle in Technical Noun Phrases

A past participle before a noun can form part of a larger technical noun phrase. The adjective + noun combination itself becomes a technical term: "compiled language," "interpreted runtime," "managed heap," "distributed ledger," "embedded system." These are compound technical nouns, not just adjective + noun sequences.

Rule 3.3 does not need to distinguish between a simple adjective + noun and a compound technical noun. Both are in the attributive position and both are permitted. The past participle supplies a classification attribute. The resulting phrase names a category of thing in the software domain.

When the technical noun phrase becomes so common that it is a single lexical item, the past participle may even lose its participial force. "Compiled language" names a category of programming language implementation. The fact that someone compiled the language at some point is irrelevant — the phrase is a classification label, not a description of an action. Rule 3.3 applies mechanically: the past participle is before the noun, so it is an adjective.

### Interaction with Rule 3.4: The Compound Tense Prohibition

Rule 3.3 and Rule 3.4 form a complementary pair. Rule 3.4 prohibits "have" + past participle as a compound tense. Rule 3.3 provides the two alternative constructions that keep the past participle's semantic content while eliminating the compound tense.

The transformation pathway from a Rule 3.4 violation to a Rule 3.3-compliant sentence follows two patterns:

**Pattern A — Adjective before noun:** "The pipeline has encrypted the payload" (violation) → "The pipeline produces the encrypted payload" (compliant). The past participle "encrypted" moves from the compound tense position to the attributive position. The action verb is supplied by an approved simple-tense verb ("produces," "gives," "sends").

**Pattern B — Adjective after "to be":** "The pipeline has encrypted the payload" (violation) → "The payload is encrypted" (compliant). The past participle moves to the predicative position after "is." The agent ("the pipeline") is removed if it is not necessary for the sentence's purpose. The sentence now describes the condition of the payload, not the action of the pipeline.

Neither pattern loses information. Pattern A keeps the agent and adds an approved action verb. Pattern B drops the agent and focuses on the condition. The choice between them depends on whether the agent is important to the documentation context.

### Historical Note: ASD-STE100 Precedent

In ASD-STE100 Issue 9, Rule 3.3 is the third rule in Section 3 (Verbs). The aerospace specification devotes this rule to the single legitimate use of the past participle outside the approved tense system: as an adjective describing a condition. The rule is brief — two example pairs in the Issue 9 text — but the principle it establishes is fundamental: the past participle has a second life as an adjective, and writers must use it only in that capacity.

The aerospace justification is safety through clarity of state. In aircraft maintenance, the past participle as an adjective communicates the condition of a component. "The disassembled unit" tells the technician that the unit is in a disassembled state. "The unit is disassembled" tells the technician the same thing in a different sentence structure. Neither sentence tells the technician who disassembled the unit or when. The condition is the only information conveyed, and that is deliberate. Condition descriptions reduce the cognitive load on the technician, who needs to know what state a component is in, not the history of actions that produced that state.

In code documentation, the same safety principle applies through clarity of system state. "The compiled binary" tells the developer that the binary is in a compiled condition, ready for execution or distribution. "The binary is compiled" tells the developer the same thing. Neither sentence specifies who compiled the binary, when, or with what toolchain. The condition is the information the developer needs to make a decision about the next step. The discipline of Rule 3.3 strips away the action history and presents only the condition, reducing the developer's cognitive load.

The original rule's note about adjectives from unapproved verbs — "permitted" and "damaged" — reflects the aerospace domain's need to describe conditions without implying unauthorized actions. A part can be damaged without specifying who or what damaged it. This pattern maps directly to code documentation, where code can be "deprecated" without specifying who deprecated it and when. The adjective preserves the condition while avoiding the verb that would require an agent and a tense that might violate other rules.
