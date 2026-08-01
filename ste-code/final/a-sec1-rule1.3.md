# Rule 1.3 — Use Approved Words Only with Their Approved Meanings

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.3](ste-code/grouped/), Rule 1.3

## Original Rule

**Rule 1.3** Use approved words only with their approved meanings.

Each approved word in the dictionary has a specified approved meaning. Some of these words can have more restricted meanings compared with their meanings in standard English. Always use the approved words only with their approved meanings.

Examples:

The approved meaning of the verb "follow" is "come after, go after."

> **STE:** Do the procedures that follow:

You cannot use the verb "follow" with other meanings that are not approved.

In this sentence, always use "obey" with the approved meaning "to do that which the procedures or instructions tell you."

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** Rule 1.11 — Do Not Use Different Technical Nouns for the Same Item
> **See also:** Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category
> **See also:** Rule 1.13 — Do Not Use Technical Verbs as Nouns
> **See also:** Rule 1.2 — Use Approved Words Only as the Specified Part of Speech
> **See also:** Rule 1.3 — Use Approved Words Only with Their Approved Meanings

## STE-Code Adaptation

**Rule 1.3** Use approved words only with their approved meanings.

Each approved word in the controlled terminology has a specified approved meaning. Some of these words can have more restricted meanings compared with their meanings in standard English. Always use the approved words only with their approved meanings.

The approved meaning of the verb "follow" is "come after, go after." You can use "follow" to describe the sequence of steps in a procedure. This is the same approved meaning as in the spec — the verb "follow" carries over directly from STE to STE-Code because procedural writing occurs in both domains.

The approved meaning of the verb "obey" is "to do that which the procedures or instructions tell you." You can use "obey" to tell the reader to comply with instructions. This is the same approved meaning as in the spec and carries over directly to STE-Code.

When an approved word has only one approved meaning in the controlled terminology, do not use it with any other meaning from standard English. If you need to express a different meaning, find an alternative approved word or use a different sentence construction.


> *Adapted from spec pair:* Non-STE: Test the system for leaks.  |  STE: Do the leak test of the system.
### Examples

> **Non-STE:** Follow the configuration steps to set up the server.
>
> **STE:** Obey the configuration instructions to set up the server.

> *Adapted from spec concept: "follow" (approved meaning: "come after, go after") is misused to mean "act in accordance with." In the spec, you must use "obey" when you mean "comply with instructions." The same distinction applies in STE-Code: use "follow" only for sequence ("Do the steps that follow") and use "obey" for compliance ("Obey the instructions").*

> **Non-STE:** The function will return you to the login screen.
>
> **STE:** The function will go back to the login screen.

> *Adapted from spec concept: each approved word has a specified approved meaning that limits its use. In STE-Code, the approved meaning of "return" is "to send a value back from a function to its caller." Using "return" to mean "go back" is not an approved meaning. The STE version uses the approved phrase "go back."*

---

## Code-Domain Explanation

Rule 1.3 governs semantic precision in code documentation. An approved word is not a blank check — it carries exactly the meaning assigned to it in the controlled terminology. This rule prevents the most common class of documentation bugs: using the right word with the wrong meaning. A reader who sees "run" assumes "execute a program." If the writer meant "manage" or "operate," the documentation is misleading even though "run" is an approved verb. This section explains how Rule 1.3 applies to each documentation type.

### README Files

README files use a small set of approved verbs with precise approved meanings. The most frequent violations occur when a writer uses an approved verb in a general-English sense that differs from its controlled-terminology meaning.

**High-risk approved words in README files:**

- **run** — Approved meaning: "execute a program or command." Do not use "run" to mean "manage" (run a team), "operate" (run a machine), or "continue" (run indefinitely). Use "manage," "operate," or "continue" — all are approved verbs with different approved meanings.
- **call** — Approved meaning: "invoke a function, method, or subroutine." Do not use "call" to mean "name" (call it X) or "shout." Use "name" or "refer to as."
- **set** — Approved meaning: "put a value into a variable or configuration." Do not use "set" to mean "become solid" (the concrete sets) or "prepare" (set the table). Use "become solid" or "prepare" — "prepare" is an approved verb.
- **make** — Approved meaning: "bring into existence by building or assembling." Do not use "make" to mean "force" (make someone do something) or "earn" (make money). Use "cause" or "earn."

Example — README project description:

> **Non-STE:** This tool runs your CI pipeline. It runs on any platform and runs 24/7 without supervision.
>
> **STE:** This tool executes your CI pipeline. It operates on any platform and operates continuously without supervision.
> *(P3 applied: first "runs" = execute (approved meaning, correct); second "runs" = operates (wrong approved meaning, replaced with "operates"); third "runs" = operates (wrong approved meaning, replaced))*

### API Documentation

API documentation describes functions, methods, endpoints, parameters, and return values. The approved verbs that appear in API documentation have meanings that are specific to the software domain. Using them with their general-English meanings creates ambiguity.

**High-risk approved words in API documentation:**

- **return** — Approved meaning: "send a value back from a function to its caller." Do not use "return" to mean "go back to a previous state or location." Use "go back."
- **get** — Approved meaning: "fetch or retrieve data from a source." Do not use "get" to mean "become" (get ready), "understand" (get it), or "receive passively" (get a gift). Use "become," "understand," or "receive."
- **send** — Approved meaning: "transmit data to a destination." Do not use "send" to mean "cause to go" (send someone home). Use "cause to go" or a different construction.
- **post** — Approved meaning (for HTTP APIs): "submit data to create a resource" (code-domain technical verb, Rule 1.12). Do not use "post" in prose to mean "publish" outside the HTTP context. Use "publish" or "put."
- **put** — Approved meaning: "place data at a location to store or update." Do not use "put" to mean "express in words" (put it simply). Use "say" or "write."

Example — API endpoint description:

> **Non-STE:** GET /users returns a list of users. It gets the data from the cache first. If the cache misses, it gets the data from the database.
>
> **STE:** GET /users gives a list of users. It gets the data from the cache first. If the cache does not have the data, it gets the data from the database.
> *(P3 applied: "returns" → "gives" — the endpoint gives data to the client, the function returns a value; "misses" → "does not have" — "miss" is not an approved verb in this context)*

### Docstrings and Inline Comments

Docstrings and inline comments explain what code does. The most common Rule 1.3 violation in docstrings is using an approved verb in a sense that belongs to a different approved meaning or to no approved meaning at all.

**High-risk approved words in docstrings:**

- **raise** — Approved meaning: "cause an exception or error to occur." Do not use "raise" to mean "increase" (raise the limit) or "lift" (raise the window). Use "increase" or "lift" — both are approved verbs.
- **catch** — Approved meaning: "handle or intercept an exception." Do not use "catch" to mean "capture a moving object" (catch a ball) or "become trapped" (catch on fire). Use "capture" or "become trapped."
- **pass** — Approved meaning: "give data as an argument to a function or method." Do not use "pass" to mean "go past" (pass the building), "succeed" (pass the test), or "transfer possession" (pass the salt). Use "go past," "succeed," or "give."
- **check** — Approved meaning: "examine something to determine correctness or state." Do not use "check" to mean "stop or restrain" (check your anger) or "leave in safekeeping" (check your bags). Use "stop" or "leave."

Example — Python docstring:

> **Non-STE:** Raises the value by 10% and passes it through the pipeline. Checks the result before returning.
>
> **STE:** Increases the value by 10% and sends it through the pipeline. Examines the result before it goes back.
> *(P3 applied: "raises" → "increases" — "raise" means "cause an exception," not "increase"; "passes" → "sends" — "pass" means "give as argument," not "send through"; "checks" → "examines" — "check" is approved but "examines" is more precise; "returning" → "goes back" — "return" means "send a value back," not "go back")*

### Commit Messages

Commit messages use a constrained vocabulary where each approved verb has exactly one approved meaning. The restricted format (type: description) leaves no room for semantic ambiguity. Every verb in a commit message must be used with its single approved meaning.

**Commit-message-specific approved meanings:**

- **add** — Approved meaning: "include new code, files, or features that did not exist before." Not "perform arithmetic addition."
- **fix** — Approved meaning: "correct a defect or unintended behavior." Not "attach firmly" or "repair physical damage."
- **remove** — Approved meaning: "delete code, files, or features so they no longer exist in the codebase." Not "move to a different location."
- **update** — Approved meaning: "change existing code or configuration to a newer version or state." Not "give someone the latest information" in a conversational sense.
- **set** — Approved meaning: "configure a value, flag, or option." Not "harden" or "solidify."

Example — commit message:

> **Non-STE:** fix: set the timeout to stop connections from running forever
>
> **STE:** fix: set the timeout to stop connections that do not complete
> *(P3 applied: "running" → "that do not complete" — "run" means "execute," not "continue indefinitely")*

### Error Messages

Error messages appear at runtime and must be understood quickly by users and developers under stress. Rule 1.3 violations in error messages cause confusion because the reader interprets the approved word with its approved meaning, but the writer intended a different meaning.

**High-risk approved words in error messages:**

- **fail** — Approved meaning: "an operation that did not complete successfully." Do not use "fail" to mean "not pass a test or examination." Use "not pass."
- **timeout** — Approved meaning: "a time limit was exceeded" (code-domain technical noun). Do not use "timeout" to mean "a break or pause." Use "pause" (approved noun).
- **refuse** — Approved meaning: "decline to accept or process." Do not use "refuse" to mean "garbage" (the noun sense). Use "waste" or "garbage."
- **deny** — Approved meaning: "reject a request for access." Do not use "deny" to mean "declare something to be untrue." Use "say something is not true."

Example — error message:

> **Non-STE:** Connection failed: the server refused to negotiate the handshake. The operation timed out after 30s.
>
> **STE:** Connection did not complete: the server refused the handshake. The operation stopped after 30 seconds.
> *(P3 applied: "failed" → "did not complete" — "fail" means "did not complete successfully"; "negotiate" → removed — "negotiate" is not approved in this sense; "timed out" → "stopped after 30 seconds" — "timeout" is a noun, and the approved meaning is "time limit exceeded," but restructured to avoid the noun-as-verb issue)*

---

## Paradigm-Specific Guidance

Rule 1.3 applies to all code documentation regardless of paradigm. But each paradigm loads approved words with paradigm-specific approved meanings. A word that is unremarkable in one paradigm may have a highly constrained approved meaning in another. This section gives guidance for each paradigm.

### Object-Oriented (Java, C++, C#, Python Classes)

Object-oriented documentation uses a set of approved words that have narrow, paradigm-specific meanings. These meanings are more restricted than the words' general-English senses and must not drift.

**Words with paradigm-specific approved meanings in OOP documentation:**

| Word | Approved Meaning (OOP) | Unapproved Meaning (do not use) |
|------|------------------------|--------------------------------|
| **class** | A blueprint for creating objects (code-domain technical noun, Rule 1.5) | A group of students, a category of service (use "category" or "type") |
| **object** | An instance of a class (code-domain technical noun) | A physical thing, a goal or purpose (use "thing" or "goal") |
| **method** | A function defined inside a class (code-domain technical noun) | A way of doing something, a procedure (use "procedure" or "technique") |
| **interface** | A contract or specification of behavior (code-domain technical noun) | A boundary between surfaces, a user interface (use "boundary" or "UI") |
| **abstract** | A class or method declared without complete implementation (code-domain technical noun/adjective) | A summary of a document (use "summary") |
| **extend** | Create a subclass from a parent class (approved verb, inheritance sense) | Make something longer or larger in physical space (use "make longer" or "increase") |
| **override** | Replace an inherited method with a new implementation (approved verb) | Use authority to reject a decision (use "reject" or "overrule") |
| **call** | Invoke a method or function (approved verb) | Name something, shout (use "name" or "shout") |

Example — class hierarchy documentation:

> **Non-STE:** The `AdminUser` class extends `User` and overrides the `authenticate` method. It calls the parent method before running its own checks.
>
> **STE:** The `AdminUser` class extends `User` and overrides the `authenticate` method. It calls the parent method before it does its own checks.
> *(P3 applied: "running" → "does" — "run" means "execute a program," not "perform checks"; the OOP-specific uses of "extends," "overrides," and "calls" all use their approved OOP meanings correctly)*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional documentation uses approved words with meanings that are often more mathematically precise than their general-English senses. The controlled terminology preserves these distinctions.

**Words with paradigm-specific approved meanings in functional documentation:**

| Word | Approved Meaning (Functional) | Unapproved Meaning (do not use) |
|------|------------------------------|--------------------------------|
| **pure** | Having no side effects (adjective, referring to functions) | Not mixed with anything, morally clean (use "clean" or "not mixed") |
| **apply** | Call a function with arguments (approved verb, code-domain sense) | Put something on a surface (use "put on") |
| **map** | Transform each element of a collection using a function (code-domain technical verb) | A geographical chart (use "chart"), to plan a route (use "plan") |
| **reduce** | Combine elements of a collection into a single value (code-domain technical verb) | Make something smaller in size (use "make smaller" or "decrease") |
| **filter** | Select elements from a collection based on a predicate (code-domain technical verb) | A device for removing impurities (use "strainer" or "purifier") |
| **fold** | Reduce a collection using an accumulator (code-domain technical verb) | Bend something over itself (use "bend") |
| **compose** | Combine two or more functions into one (code-domain technical verb) | Create a piece of music, write a letter (use "write") |
| **curry** | Transform a multi-argument function into a chain of single-argument functions (code-domain technical verb) | A spice, to prepare food with spices (use "spice") |

Example — module documentation:

> **Non-STE:** This module composes pure functions that map, filter, and reduce collections without mutating state.
>
> **STE:** This module composes pure functions that map, filter, and reduce collections without changing state.
> *(P3 applied: "mutating" → "changing" — "mutate" is a code-domain technical verb with a specific approved meaning ("change state destructively"), and here it is used in its general English sense; "changing" is the approved alternative)*

### Procedural (C, Go, Bash)

Procedural documentation uses a lean set of approved verbs, each with exactly one approved meaning. The procedural paradigm borrows little vocabulary from other domains, so Rule 1.3 violations tend to involve general-English meanings intruding on approved technical meanings.

**Words with paradigm-specific approved meanings in procedural documentation:**

| Word | Approved Meaning (Procedural) | Unapproved Meaning (do not use) |
|------|------------------------------|--------------------------------|
| **return** | Send a value back from a function to its caller | Go back to a previous location or state (use "go back") |
| **call** | Invoke a function or subroutine | Name something, shout (use "name") |
| **pass** | Give data as an argument to a function | Go past, succeed, transfer (use "go past," "succeed," "give") |
| **break** | Exit a loop or switch statement immediately | Damage something, interrupt (use "damage" or "interrupt") |
| **continue** | Skip to the next iteration of a loop | Keep doing something without interruption (use "keep") |
| **goto** | Jump to a labeled statement (code-domain technical noun) | Move toward a destination (use "go to" — two words) |
| **declare** | Specify a variable with its type (but not allocate it) | State something formally, announce (use "state" or "announce") |
| **allocate** | Reserve memory for use (code-domain technical verb) | Distribute resources among recipients (use "distribute") |

Example — C function documentation:

> **Non-STE:** The function allocates a buffer, passes it to the handler, and breaks if the handler returns an error.
>
> **STE:** The function allocates a buffer, gives it to the handler, and stops if the handler gives an error.
> *(P3 applied: "passes" → "gives" — "pass" means "give as argument," not "hand over"; "breaks" → "stops" — "break" means "exit a loop," not "stop executing"; "returns" → "gives" — "return" means "send a value back from a function," and "gives" is clearer in this context)*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state. The approved words in declarative contexts often double as keywords in the declarative language. When they appear in documentation prose, they must be used with their controlled-terminology meanings, not their general-English meanings or their keyword behavior.

**Words with paradigm-specific approved meanings in declarative documentation:**

| Word | Approved Meaning (Declarative) | Unapproved Meaning (do not use) |
|------|-------------------------------|--------------------------------|
| **select** | Retrieve rows from a database table | Choose from a set of options (use "choose") |
| **join** | Combine rows from two or more tables | Connect things physically, become a member (use "connect" or "become a member") |
| **create** | Make a new resource, table, or object | Invent something new, cause a situation (use "invent" or "cause") |
| **drop** | Remove a table, database, or resource permanently | Let something fall, stop doing something (use "let fall" or "stop") |
| **apply** | Execute a configuration plan (Terraform) | Put something on a surface, request a job (use "put on" or "request") |
| **describe** | Show the current state of a resource (Kubernetes) | Give a verbal account of something (use "tell about") |
| **declare** | Specify desired state in a manifest | State formally (use "state") |
| **provision** | Set up infrastructure resources (code-domain technical verb) | Supply with necessities (use "supply") |

Example — Terraform documentation:

> **Non-STE:** Apply the configuration to provision the resources. The plan will create three instances and join them to the load balancer.
>
> **STE:** Apply the configuration to make the resources. The plan will create three instances and connect them to the load balancer.
> *(P3 applied: "provision" → "make" — "provision" as a general verb is not approved; "join" → "connect" — "join" as a SQL keyword means "combine rows," and in prose it should use "connect" for the general sense)*

### Systems (Rust Ownership, C Memory Management)

Systems documentation uses approved words that have been given highly specific meanings in the context of ownership, borrowing, lifetimes, and memory. These meanings often diverge significantly from general English.

**Words with paradigm-specific approved meanings in systems documentation:**

| Word | Approved Meaning (Systems) | Unapproved Meaning (do not use) |
|------|---------------------------|--------------------------------|
| **move** | Transfer ownership of a value (Rust) | Change physical position (use "go," "travel," or "change position") |
| **borrow** | Take a reference to a value without taking ownership | Take something temporarily with intent to return (use "take temporarily") |
| **own** | Hold ownership of a value (Rust) | Possess something, admit to something (use "have" or "admit") |
| **drop** | Run the destructor and deallocate memory (Rust) | Let something fall (use "let fall") |
| **copy** | Duplicate data using bitwise or `Clone` semantics | Make a duplicate of anything (use "make a copy") |
| **clone** | Explicitly create a deep copy (Rust) | Create a genetic copy of an organism (use "copy" or "duplicate") |
| **free** | Deallocate memory that was previously allocated | Release from confinement, without cost (use "release" or "no cost") |
| **dangling** | Referring to memory that has been deallocated (code-domain technical adjective) | Hanging loosely (use "hanging") |

Example — Rust ownership documentation:

> **Non-STE:** When you move a value, the original owner can no longer use it. You can borrow a reference to read the value without taking ownership.
>
> **STE:** When you move a value, the first owner can no longer use it. You can borrow a reference to read the value without taking ownership.
> *(P3 applied: "original" → "first" — "original" is an approved adjective meaning "existing from the beginning," but "first" is more precise; the systems-specific uses of "move," "borrow," "own," and "reference" all use their approved systems meanings correctly)*

---

## Extended Examples

Each example pair below shows a real code documentation scenario, the STE-Code compliant rewrite, which principle was applied, and an explanation of the fix.

### Example 1 — API Reference: Return Value Description

> **Non-STE:** Returns the authenticated user object. If authentication fails, returns null and logs the error.
>
> **STE:** Gives the authenticated `User` object. If authentication does not complete, gives `null` and writes the error to the log.

> **Principle applied:** P3 (use approved words only with their approved meanings: "returns" → "gives" — the function gives a value to the caller; "fails" → "does not complete" — "fail" means "did not complete successfully," used correctly but restructured for clarity); P1 (use approved words: "logs" → "writes to the log")
> **Explanation:** The verb "return" has the approved meaning "send a value back from a function to its caller." But in API documentation, the endpoint "gives" data to the client. The distinction is between intra-process return and inter-process delivery. "Logs" as a verb is not approved — use the approved verb "write" with the approved noun "log."

### Example 2 — README: Project Feature Description

> **Non-STE:** This library runs on Node.js and runs in the browser. It runs your transformations in parallel to maximize throughput.
>
> **STE:** This library operates on Node.js and operates in the browser. It runs your transformations together to increase throughput.

> **Principle applied:** P3 (use approved words only with their approved meanings: first two "runs" → "operates" — "run" means "execute a program," not "function on a platform"; third "runs" → "runs" — correct, it executes the transformations); P1 ("maximize" → "increase" — "maximize" is not approved)
> **Explanation:** "Run" has exactly one approved meaning in STE-Code: "execute a program or command." When the writer says "runs on Node.js," the intended meaning is "operates on" or "functions on." The third use ("runs your transformations") uses the correct approved meaning. This example shows that the same word in the same paragraph can be both correct and incorrect depending on the intended meaning.

### Example 3 — Docstring: Exception Handling

> **Non-STE:** This method raises an error when the input is empty. Catch the error and return a default value to prevent the application from crashing.
>
> **STE:** This method raises an error when the input is empty. Catch the error and give a default value to prevent the application from stopping.

> **Principle applied:** P3 (use approved words only with their approved meanings: "return" → "give" — "return" means "send a value back from a function," but the prose describes what to do with the caught error, not a function return; "crashing" → "stopping" — "crash" is a code-domain technical noun meaning "abnormal program termination," and "stopping" is more precise here); P1 ("prevent" → "prevent" — correct, "prevent" is approved)
> **Explanation:** "Raise" and "catch" use their approved exception-handling meanings correctly. But "return" is used to mean "provide as a substitute," which is not the approved meaning. "Give" is the approved replacement. "Crash" is a code-domain technical noun, but using it as a verb ("crashing") violates Rule 1.7. Restructure to use "stop."

### Example 4 — CLI Error Message

> **Non-STE:** Error: Could not connect to the server. The connection timed out. Check your network and try running the command again.
>
> **STE:** Error: Cannot connect to the server. The connection stopped after 30 seconds. Check your network and try the command again.

> **Principle applied:** P3 (use approved words only with their approved meanings: "timed out" → "stopped after 30 seconds" — "timeout" is an approved noun meaning "time limit exceeded," but using it as a verb violates Rule 1.13); P1 ("could not" → "cannot" — "cannot" is the approved modal; "running" → removed — redundant next to "try")
> **Explanation:** "Timed out" as a verb phrase uses the noun "timeout" in an unapproved verb construction. The rewrite uses the approved verb "stop" with the time specification. "Try running" uses "run" in its approved meaning ("execute"), but the "-ing" form as a main verb violates the anti-pattern rule. "Try the command again" is simpler and compliant.

### Example 5 — Commit Message: Refactoring

> **Non-STE:** refactor: break the UserService into smaller classes to improve testability
>
> **STE:** refactor: split the `UserService` into smaller classes to make testing easier

> **Principle applied:** P3 (use approved words only with their approved meanings: "break" → "split" — "break" means "exit a loop," not "divide into parts"); P1 ("improve testability" → "make testing easier" — "improve" is an approved verb but "testability" is not an approved noun)
> **Explanation:** "Break" has the approved meaning "exit a loop or switch statement immediately." Using "break" to mean "divide" is a violation. "Split" is an approved verb. "Testability" is not an approved noun — restructure to "make testing easier" using the approved verb "make," the approved noun "testing" (code-domain technical noun), and the approved adjective "easier."

### Example 6 — Configuration File Documentation

> **Non-STE:** # Set this flag to "true" to enable debug mode. When enabled, the server
> # will dump verbose logs to stdout. Setting this flag impacts performance
> # significantly, so do not enable it in production.
> **STE:** # Set this flag to `true` to turn on debug mode. When debug mode is on,
> # the server writes detailed logs to stdout. This setting decreases performance.
> # Do not turn on debug mode in production.

> **Principle applied:** P3 (use approved words only with their approved meanings: "enable" → "turn on" — "enable" is an approved verb meaning "make something possible," but "turn on" is the correct phrase for activating a feature; "dump" → "writes" — "dump" is a code-domain technical noun, not a verb; "impacts" → "decreases" — "impact" as a verb meaning "affect" is not approved; "significantly" → removed — unnecessary adverb); P1 ("verbose" → "detailed" — approved adjective; "setting" → "setting" — approved noun, correct)
> **Explanation:** "Enable" has the approved meaning "make something possible." But for toggling a boolean flag to `true`, "turn on" is the correct phrase. "Dump" is a code-domain technical noun ("core dump," "memory dump"), not a verb. "Impacts" as a verb meaning "affects" is not approved — "decreases" is more precise and approved. The sentence is split to keep each under 20 words (procedural limit).

---

## Edge Cases

The following scenarios show where the boundary of an approved meaning requires careful judgment in code documentation.

### Edge Case 1: Framework Name That Shares a Spelling with an Approved Word

**Scenario:** A framework or library has a name that spells the same as an approved word. For example, "Express" (the Node.js web framework) shares its spelling with the verb "express" (approved meaning: "show or state clearly"). A writer might write: "Express your API using Express."

**Guidance:** Framework names are code-domain technical nouns (Rule 1.5, category 3) and are exempt from Rule 1.3 meaning restrictions. The approved word "express" (verb, "show or state clearly") and the technical noun "Express" (proper noun, the framework) are different words that happen to share spelling. Always capitalize the framework name to distinguish it. Do not use the framework name as a verb.

> **Non-STE:** Express your API using Express.
>
> **STE:** Use Express to make your API.

> In the non-STE version, "Express" appears twice with two different meanings: first as a verb (approved meaning: "show or state"), second as a proper noun (framework name). The STE version avoids the verb use entirely.

**When the framework name is a verb:** Some frameworks have names that are verbs in general English (for example, "React," "Build," "Run"). Treat the framework name as a code-domain technical noun regardless of its general-English part of speech. "I built the project with Build" is confusing but technically compliant because "Build" (capitalized) is a technical noun. Prefer restructured sentences: "I used Build to make the project."

### Edge Case 2: Code Keyword Whose Behavior Conflicts with Its Approved Meaning

**Scenario:** A programming language keyword has behavior that does not match the approved meaning of the same word in the controlled terminology. For example, `static` in C means "a variable with a lifetime equal to the program's lifetime." But "static" is an approved adjective meaning "not moving or changing." The keyword behavior and the approved meaning overlap but are not identical.

**Guidance:** When the keyword appears in a code block (backtick-quoted), it is quoted text (Rule 1.5, category 10) and is exempt from Rule 1.3. When you document what the keyword does, use the approved meaning in your prose and let the code block carry the language-specific semantics. The reader sees the keyword in context and understands its behavior from the code, not from your adjective choice.

> **Non-STE:** The `static` variable keeps its value between function calls. It is static.
>
> **STE:** The `static` variable keeps its value between function calls. The variable does not change between calls.

> The non-STE version uses "static" twice: first as a quoted keyword (exempt), second as an adjective in prose. The prose adjective "static" carries the approved meaning "not moving." The rewrite avoids the adjective and uses a clause that describes the behavior precisely.

### Edge Case 3: Word Approved with More Than One Meaning

**Scenario:** Some approved words have more than one approved meaning in the controlled terminology. For example, "call" is approved as a verb meaning "invoke a function" and also as a noun meaning "a function invocation." Both meanings are approved. The writer must choose the meaning that matches the part of speech used.

**Guidance:** When a word has multiple approved meanings, all of them are valid under Rule 1.3. The part of speech disambiguates. "Call the function" uses the verb meaning (invoke). "The function call" uses the noun meaning (invocation). Do not use "call" to mean "name" ("we call this X") — this is not an approved meaning for either the verb or noun form.

> **Non-STE:** Call the function `getUser`. We call this pattern the Repository Pattern.
>
> **STE:** Call the function `getUser`. We name this pattern the Repository Pattern.

> "Call" in the first sentence uses the approved verb meaning "invoke." "Call" in the second sentence means "name," which is not an approved meaning. "Name" is the approved replacement.

**Other words with multiple approved meanings:**

| Word | Approved Meaning 1 | Approved Meaning 2 | Unapproved Meaning |
|------|-------------------|-------------------|-------------------|
| **set** | (v) put a value into a variable | (n) a collection of unique elements | (v) become solid |
| **run** | (v) execute a program | (n) a single execution | (v) manage or operate |
| **file** | (n) a named collection of data on a disk | (v) to store data in a file | (n) a tool for smoothing surfaces |
| **test** | (n) a procedure to check correctness | (v) to run tests against code | (n) an examination in school |

### Edge Case 4: Approved Word Whose Meaning Drifts Across Documentation Types

**Scenario:** The same approved word means slightly different things in different documentation types. "Return" in a docstring means "send a value from a function to its caller." "Return" in a README means "go back to a previous step." The first meaning is approved; the second is not. But the writer may not notice the shift.

**Guidance:** Use the approved meaning consistently across all documentation types. If the approved meaning does not fit the context, use a different approved word. Do not stretch an approved meaning to cover a different concept just because the word is approved and familiar.

> **Non-STE:** If the installation fails, return to step 2 and check your configuration.
> **STE (README):** If the installation does not complete, go back to step 2 and check your configuration.

> "Return" has the approved meaning "send a value from a function to its caller." The README context uses "return" to mean "go back," which is not approved. "Go back" is the approved phrase.

### Edge Case 5: Domain Borrowing — When a Word's Approved Meaning in One Domain Conflicts with Another

**Scenario:** "Probe" is an approved noun in aerospace STE meaning "a device for testing or measuring." In software, "probe" is a code-domain technical noun meaning "a monitoring or diagnostic tool inserted into running code" (for example, a "liveness probe" in Kubernetes, an "observability probe"). The aerospace meaning and the software meaning are related but not identical.

**Guidance:** When a word is both an approved word in the controlled terminology and a code-domain technical noun, use the more specific meaning for the context. In software documentation, the code-domain technical noun meaning takes priority. If the context is ambiguous, add a modifier: "Kubernetes liveness probe" or "measurement probe." This follows the same principle as Rule 1.8 (use standard, well-known technical nouns).

> **Non-STE:** The probe checks if the container is alive.
>
> **STE:** The liveness probe checks if the container is alive.

> "Liveness probe" is a compound code-domain technical noun. Adding the modifier "liveness" disambiguates between the general approved noun "probe" and the domain-specific technical noun.

---

## Cross-References

Rule 1.3 is the semantic constraint on the approved vocabulary. It works with the other rules in Section 1 to build a complete system of vocabulary control.

| Rule | Title | Relationship to Rule 1.3 |
|------|-------|---------------------------|
| **Rule 1.1** | Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs | Rule 1.1 tells you which words you may use. Rule 1.3 tells you what those words mean. A word that passes Rule 1.1 must then pass Rule 1.3 — it must be used with its approved meaning. |
| **Rule 1.2** | Use Approved Words Only as the Specified Part of Speech | Rule 1.2 constrains the grammatical role of an approved word. When an approved word has more than one approved meaning, the part of speech selects the meaning. "Call" as a verb means "invoke." "Call" as a noun means "an invocation." Rule 1.2 and Rule 1.3 are applied together. |
| **Rule 1.4** | Use Only the Approved Verb Forms and Adjective Forms | Rule 1.4 constrains the morphological forms of approved words. Even when a word is used with its approved meaning (Rule 1.3), only the approved inflected forms are permitted. "Run," "runs," "ran," and "running" are all approved verb forms of "run." But "runned" is not — even though the meaning is the same. |
| **Rule 1.7** | Do Not Use Technical Nouns as Verbs | When a code-domain technical noun has an approved meaning as a noun, using it as a verb violates Rule 1.7 even if the meaning is clear. For example, "docker" is a technical noun. "Dockerize the application" uses it as a verb — not permitted. |
| **Rule 1.11** | One Term Per Concept — Be Consistent | Rule 1.11 requires that you use the same approved word for the same concept throughout a document. Rule 1.3 ensures that when you use that word, you use it with the correct meaning. Together, these rules enforce consistency of both vocabulary and semantics. |
| **Rule 1.13** | Do Not Use Technical Verbs as Nouns | When a code-domain technical verb has an approved meaning as a verb, using it as a noun violates Rule 1.13. For example, "deploy" is a technical verb. "The deploy failed" uses it as a noun — not permitted. Use "deployment." |

**Dictionary reference:** See `a-dictionary.md` for the full STE-Code controlled terminology. Each entry includes the approved word, its part(s) of speech, and its approved meaning(s). When you are unsure whether a word is being used with its approved meaning, consult the dictionary entry. The dictionary also lists unapproved words with their approved alternatives, organized by meaning category.

**Categories reference:** See `a-categories.md` for the 22 code-domain technical noun categories defined under Rule 1.5. When a domain-specific meaning is needed and no approved word carries that meaning, a code-domain technical noun from the appropriate category can fill the gap.

---

## Grammar Notes

### Semantic Narrowing: The Core Mechanism of Rule 1.3

Rule 1.3 enforces semantic narrowing — the principle that an approved word has a meaning that is more restricted and more precise than its general-English meaning. This is the linguistic mechanism that makes STE-Code unambiguous.

In general English, the verb "run" has over 20 distinct meanings (execute, manage, operate, flow, extend, compete, publish, and more). In STE-Code, "run" has exactly one approved meaning: "execute a program or command." This semantic narrowing eliminates 19+ possible interpretations. The reader cannot misunderstand because there is only one possible meaning.

Semantic narrowing is not the same as vocabulary restriction (Rule 1.1). Rule 1.1 says "do not use the word 'execute.'" Rule 1.3 says "when you use the word 'run,' it means exactly this and nothing else." Both rules reduce ambiguity, but Rule 1.3 operates on meaning, not on word choice.

### Polysemy Control

Many approved words are polysemous — they have multiple related meanings. Rule 1.3 selects exactly one meaning as the approved meaning and forbids the others. This is polysemy control.

Example: The verb "set" in general English can mean "put something in a specified place," "adjust a device," "establish a rule," "become solid," "cause to start," and more. In STE-Code, "set" has the approved meaning "put a value into a variable or configuration." All other meanings are forbidden.

Polysemy control is especially important in code documentation because many verbs that describe software operations also describe physical actions. "Run a program" vs. "run a marathon." "Call a function" vs. "call your mother." "Return a value" vs. "return home." The approved meaning is always the software-domain meaning. When the writer needs the physical meaning, they must use a different approved word.

### Context-Dependent Meaning Resolution

When an approved word has more than one approved meaning (Edge Case 3 above), the correct meaning is resolved by context. The part of speech (Rule 1.2) is the primary resolver. If the word is used as a verb, select the verb meaning. If it is used as a noun, select the noun meaning.

The documentation type is the secondary resolver. In a docstring, "call" means "invoke." In an error message, "call" means "invocation." The context makes the distinction clear even though both meanings are approved.

When context cannot resolve the ambiguity, restructure the sentence. Add a modifier, use a different approved word, or split the sentence into two simpler sentences. Never rely on the reader to guess which approved meaning applies.

### Meaning and Part of Speech: The Intersection of Rule 1.2 and Rule 1.3

Rule 1.2 (part of speech) and Rule 1.3 (meaning) are applied in sequence. First, verify that the word is used with its approved part of speech (Rule 1.2). Second, verify that the approved part of speech carries the approved meaning (Rule 1.3).

A word can pass Rule 1.2 but fail Rule 1.3. For example:

> **Non-STE:** The server runs on port 8080.

"Runs" is a verb (passes Rule 1.2 — "run" is approved as a verb). But the intended meaning is "operates on a given port," not "executes." The approved meaning of the verb "run" is "execute a program or command." This sentence fails Rule 1.3.

> **STE:** The server operates on port 8080.

"Operates" is a verb (passes Rule 1.2). The approved meaning of "operate" is "to function or work in a specified way." This sentence passes Rule 1.3.

### The "Approved Meaning" as a Semantic Constraint (Not a Syntactic One)

Rule 1.3 constrains semantics, not syntax. It does not restrict sentence structure, word order, or grammatical construction. It only restricts what a word is allowed to mean. This distinction is important because writers sometimes confuse "I cannot use this word" (Rule 1.1 violation) with "I am using this word incorrectly" (Rule 1.3 violation).

A word that appears in a sentence with correct syntax, correct part of speech, and correct morphological form can still violate Rule 1.3 if the intended meaning does not match the approved meaning. This is the hardest class of violations to detect because the sentence looks correct on the surface.

### Historical Note: ASD-STE100 Precedent

In ASD-STE100 Issue 9, Rule 1.3 is one of the most actively enforced rules in aerospace technical writing. The original specification gives the example of "follow" (approved meaning: "come after, go after") vs. "obey" (approved meaning: "do that which the procedures or instructions tell you"). This distinction has safety implications in aerospace: a maintenance procedure that says "follow the steps" does not communicate the same obligation as "obey the steps."

STE-Code adapts the same severity to code documentation. A docstring that says "the function returns you to the login screen" suggests that the function navigates the user somewhere. The correct documentation is "the function gives the login screen back to the caller" (if it does) or "the function sends the user to the login screen" (if it redirects). The difference between "returns" (sends a value back) and "redirects" (sends the user somewhere else) is the difference between correct and incorrect documentation.

The original ASD-STE100 uses a dictionary (Part 2) to define approved meanings. STE-Code uses a controlled terminology (also Part 2, in `a-dictionary.md`) to do the same. Each entry specifies the approved word, its part of speech, its approved meaning, and (for unapproved words) approved alternatives. The dictionary is the single source of truth for approved meanings. When a meaning dispute arises, the dictionary resolves it.
