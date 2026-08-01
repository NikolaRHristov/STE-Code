# Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec9-rule9.3](ste-code/grouped/), Rule 9.3

## Original Rule

When you use two words together, do not make phrasal verbs.

In English, a verb and one or more prepositions can go together to form a "phrasal verb." This phrasal verb has a meaning that is different from the meanings of its parts. Phrasal verbs usually have two meanings: the original, more concrete meaning, and a more general and abstract meaning.

To prevent ambiguity, it is not permitted in STE to use approved words together to make a new phrase (phrasal verb).

You will not usually find phrasal verbs listed as "not approved" in the dictionary. When you write a standard English sentence in STE, always make sure that the new sentence is grammatically correct. And make sure that you use the approved words with the meaning that they have in the dictionary.

Only a small number of phrasal verbs are approved in the dictionary. They all have a restricted meaning.

## STE-Code Adaptation

> **See also:** Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient; Rule 9.2 — Use Each Approved Word Correctly

When you use two words together in code documentation, do not make phrasal verbs.

A verb and one or more prepositions can go together to form a phrasal verb with a meaning that is different from the meanings of its individual parts. Phrasal verbs usually have two meanings: the original, concrete meaning, and a more general, abstract meaning. To prevent ambiguity, do not use approved words together to make a new phrase unless the phrasal verb is specifically approved in the controlled terminology.

Replace the phrasal verb with a single approved verb that has the same meaning. When you write a standard English sentence in the controlled terminology, always make sure that the new sentence is grammatically correct and that you use the approved words with the meaning that they have in the controlled terminology.

Only a small number of phrasal verbs are approved. They all have a restricted meaning.

### Examples

> **Non-STE:** The compiler puts out a warning when the type annotation is missing.
>
> **STE:** The compiler emits a warning when the type annotation is missing.

("Put" and "out" are approved words individually. Together, "put out" forms a phrasal verb with a meaning different from the approved meanings of "put" and "out." The approved verb "emit" has the meaning "to send out" and is the word that is most usual in code documentation.)
*Adapted from spec pair: "Put out the fire." (abstract) / "Extinguish the fire." — "put" and "out" are approved individually, but together they form a phrasal verb; the approved verb "extinguish" replaces it.*

> **Non-STE:** The function gives off an error code when the input is not valid.
>
> **STE:** The function returns an error code when the input is not valid.

("Give" and "off" are approved words individually. Together, "give off" forms a phrasal verb with a meaning different from the approved meanings of "give" and "off." The approved verb "return" has the meaning "to send back a value" and is the correct word for this context in code documentation.)
*Adapted from spec pair: "Give off gas." / "Release gas." — "give" and "off" are approved individually, but together they form a phrasal verb; the approved verb "release" replaces it.*

> **Non-STE:** The cleanup task carries out the memory deallocation after each request.
>
> **STE:** The cleanup task does the memory deallocation after each request.

("Carry" and "out" are approved words individually. Together, "carry out" forms a phrasal verb. The approved verb "do" replaces the phrasal verb and keeps the same meaning.)
*Adapted from spec pattern: replace unapproved phrasal verbs with a single approved verb that has the same meaning.*

## Code-Domain Explanation

This rule applies across all forms of code documentation. Phrasal verbs are common in informal technical writing. Each form of documentation has a different risk profile for phrasal verb ambiguity.

### README Files

README files are the entry point for users. Phrasal verbs in README files can confuse non-native English speakers. A user who searches for a single approved verb will not find a section that uses only a phrasal verb. Replace common README phrasal verbs:

- "Set up the project" → "Configure the project" or "Install the project"
- "Run through the quickstart" → "Complete the quickstart" or "Do the quickstart"
- "Check out the examples" → "Examine the examples" or "See the examples"
- "Go through the configuration" → "Read the configuration" or "Complete the configuration"
- "Pick up where you left off" → "Continue where you stopped"
- "Break down the architecture" → "Describe the architecture" or "Explain the architecture"

Each heading and paragraph in a README file must use a single approved verb. Do not use a verb+preposition combination when one approved verb is sufficient.

### API Documentation

API reference documentation must be exact. A method description that uses a phrasal verb can hide the actual behavior of the method. Two readers can understand the same phrasal verb differently.

When you document an API endpoint or a function signature, use the approved verb that is most precise for that operation:

- "Looks up a user by ID" → "Finds a user by ID" (the method finds exactly one record)
- "Hands off the request to the worker" → "Sends the request to the worker" (the method transfers control)
- "Takes in a configuration object" → "Receives a configuration object" (the parameter is the input)
- "Spits out the result as JSON" → "Returns the result as JSON" (the method sends back a value)
- "Fills in the missing fields" → "Completes the missing fields" (the method supplies defaults)

For API reference pages, the verb must match the HTTP method or the function behavior exactly. A GET endpoint "gets" data, not "pulls down" or "fetches." A POST endpoint "creates" or "sends" data, not "puts in" or "hands over."

### Docstrings and Inline Documentation

Docstrings in Python, Javadoc in Java, and doc comments in Rust, Go, and C# are the most common places where phrasal verbs appear. Developers write docstrings quickly and use informal language. Edit docstrings to remove phrasal verbs:

````
# Non-STE:
def process(data):
    """Runs through the data and picks out the valid entries."""
    ...

# STE:
def process(data):
    """Examines the data and selects the valid entries."""
    ...
````

````
// Non-STE:
/// Sets up the connection pool and kicks off the health check.
pub fn init() -> Pool { ... }

// STE:
/// Configures the connection pool and starts the health check.
pub fn init() -> Pool { ... }
````

### Commit Messages

Commit messages are permanent records of changes. A phrasal verb in a commit message makes the change less clear to a reviewer or a future maintainer. Common phrasal verbs in commit messages and their approved replacements:

| Phrasal Verb (Avoid) | Approved Verb (Use) |
|----------------------|---------------------|
| clean up             | remove, delete, tidy |
| fix up               | correct, repair     |
| speed up             | accelerate, make faster |
| cut down             | reduce, decrease    |
| rip out              | remove              |
| wire up              | connect             |
| strip out            | remove              |
| flesh out            | complete, expand    |

A commit message such as "Clean up the old API endpoints" is ambiguous. "Remove the old API endpoints" or "Refactor the old API endpoints" makes the change exact.

### Error Messages

Error messages must tell the user exactly what went wrong and what to do. A phrasal verb in an error message can make the recovery action unclear:

```
// Non-STE:
Error: Could not hook up to the database.

// STE:
Error: Could not connect to the database.
```

```
// Non-STE:
Error: The build process blew up during the linking step.

// STE:
Error: The build process failed during the linking step.
```

```
// Non-STE:
Warning: The lock file is out of whack. Run `install` to sort it out.

// STE:
Warning: The lock file is not consistent. Run `install` to correct it.
```

### Changelogs and Release Notes

Release notes document what changed for users. Phrasal verbs in release notes reduce the professional quality of the communication:

- "We did away with the legacy parser" → "We removed the legacy parser" (BREAKING)
- "Added back the export feature" → "Restored the export feature"
- "The team ironed out the performance issues" → "The team corrected the performance issues"
- "We phased out support for Python 3.7" → "We ended support for Python 3.7" (DEPRECATED)

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Object-oriented documentation describes classes, methods, constructors, and destructors. Phrasal verbs often appear in method descriptions that involve resource management, initialization, and cleanup:

- "Sets up the object state" → "Initializes the object state" (constructor docs)
- "Tears down the resources" → "Releases the resources" (destructor/`close` docs)
- "Hands off ownership to the caller" → "Transfers ownership to the caller" (factory method)
- "Looks up the dependency in the container" → "Finds the dependency in the container" (DI docs)
- "Wraps up the transaction" → "Completes the transaction" (unit of work pattern)

````java
// Non-STE:
/**
 * Tears down the connection and cleans up all associated resources.
 * Call this method when you are done with the connection.
 */
public void close() { ... }

// STE:
/**
 * Closes the connection and releases all associated resources.
 * Call this method when you no longer need the connection.
 */
public void close() { ... }
````

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, pipelines, and data transformations. Phrasal verbs can obscure the nature of the transformation:

- "The function maps over the list and filters out nulls" → "The function applies a transformation to each element of the list and removes nulls"
- "It pipes through the middleware stack" → "It sends the request through the middleware stack" (or "It applies the middleware stack")
- "The reducer folds the values down into a single result" → "The reducer combines the values into a single result"
- "The function reaches out to the external service" → "The function sends a request to the external service"

In functional languages, prefer verbs that describe pure transformations: "transforms," "applies," "filters," "maps," "reduces." Do not use phrasal verbs that suggest side effects when the function is pure.

### Procedural Documentation (C, Go, Bash)

Procedural documentation describes step-by-step algorithms, system calls, and shell scripts. Phrasal verbs are especially common in procedural code because scripts often "do things" in sequence:

````bash
# Non-STE:
# 1. Reach out to the API and pull down the latest data.
# 2. Go through each record and pick out the changed fields.
# 3. Put together the update payload and send it off.

# STE:
# 1. Send a request to the API and get the latest data.
# 2. Examine each record and select the changed fields.
# 3. Make the update payload and send it.
````

In C documentation, avoid phrasal verbs that describe memory operations:

- "Free up the allocated memory" → "Release the allocated memory" or "Free the allocated memory"
- "The pointer hands back the result" → "The pointer returns the result" (but pointers do not return values — "The function writes the result through the pointer" is more exact)

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state, not step-by-step procedures. Phrasal verbs can accidentally introduce an imperative tone that conflicts with the declarative model:

- "The Terraform plan brings up three EC2 instances" → "The Terraform plan creates three EC2 instances"
- "The deployment spins up new pods when the load increases" → "The deployment starts new pods when the load increases"
- "The migration tears down the old index before it builds the new one" → "The migration removes the old index before it creates the new one"
- "The query joins together the users and orders tables" → "The query joins the users table with the orders table"

### Systems Documentation (Rust Ownership, C Memory)

Systems documentation describes ownership, lifetimes, memory safety, and concurrency. Phrasal verbs can make these already-complex topics harder to understand:

- "The function hands off ownership of the buffer" → "The function transfers ownership of the buffer"
- "The closure holds onto the captured variable" → "The closure keeps a reference to the captured variable"
- "The thread gives up the lock when it finishes" → "The thread releases the lock when it finishes"
- "The allocator carves out a new memory region" → "The allocator allocates a new memory region"

````rust
// Non-STE:
/// Takes ownership of the string and hands back a parsed Config.
/// If parsing fails, it gives back the original string.
pub fn parse_config(input: String) -> Result<Config, String> { ... }

// STE:
/// Receives ownership of the string and returns a parsed Config.
/// If parsing fails, it returns the original string.
pub fn parse_config(input: String) -> Result<Config, String> { ... }
````

## Extended Examples

> **Non-STE:** The test runner runs through all test suites and prints out a summary report.
>
> **STE:** The test runner executes all test suites and prints a summary report.
>
> *Principles applied: P1, P11 — "run through" is a phrasal verb (verb + preposition). Replace with the single approved verb "execute." Also "prints out" becomes "prints" — "out" adds no meaning and the verb "print" alone is approved for this meaning.*

> **Non-STE:** The framework sets up the routing table from the annotation data.
>
> **STE:** The framework configures the routing table from the annotation data.
>
> *Principles applied: P1 — "set up" is one of the most common phrasal verbs in code documentation. The approved verb "configure" replaces it when the context is about initialization with parameters. Use "install" when the context is about placing files on a system. Use "create" when the context is about making a new resource from nothing.*

> **Non-STE:** The middleware looks at the request headers and filters out the sensitive fields.
>
> **STE:** The middleware examines the request headers and removes the sensitive fields.
>
> *Principles applied: P1, P2 — "look at" is a phrasal verb that means "examine" or "inspect." "Filter out" is also a phrasal verb. The approved verbs "examine" and "remove" each replace one phrasal verb. Note: "filter" alone (without "out") is an approved technical verb. The sentence "The middleware filters the request headers" uses "filter" as an approved verb; adding "out" makes it a phrasal verb.*

> **Non-STE:** The cleanup job kicks in after 30 seconds of idle time and clears out the expired sessions.
>
> **STE:** The cleanup job starts after 30 seconds of idle time and removes the expired sessions.
>
> *Principles applied: P1 — "kick in" is an informal phrasal verb with no place in technical documentation. The approved verb "start" gives the exact meaning: the job begins execution. "Clear out" is replaced by "remove" — the expired sessions are deleted, not "cleared out."*

> **Non-STE:** The compiler breaks down the source file into an abstract syntax tree, then goes on to generate the intermediate representation.
>
> **STE:** The compiler divides the source file into an abstract syntax tree, then continues to generate the intermediate representation.
>
> *Principles applied: P1, P11 — "break down" and "go on" are both phrasal verbs. "Break down" (meaning "analyze into parts") becomes "divides" or "separates." "Go on" (meaning "proceed to the next step") becomes "continues." The approved verb "analyze" is also acceptable for the first replacement when the emphasis is on examination rather than separation.*

> **Non-STE:** The plugin system lets you hook into the build pipeline at three different points. You can also tap into the logging stream.
>
> **STE:** The plugin system lets you connect to the build pipeline at three different points. You can also subscribe to the logging stream.
>
> *Principles applied: P1, P10 — "hook into" and "tap into" are both informal phrasal verbs with abstract meanings. "Connect to" and "subscribe to" use approved verbs with exact meanings. "Hook into" is also slang (P10), which makes it doubly non-compliant. The approved verb "connect" is standard for describing integration points between systems.*

## Approved Phrasal Verbs in STE-Code

A small number of phrasal verbs are approved because no single verb replaces them with the same precision. These approved phrasal verbs have restricted meanings:

| Approved Phrasal Verb | Restricted Meaning | Example |
|----------------------|-------------------|---------|
| log in / log out | Start or end an authenticated session | "The user must log in before they can access the dashboard." |
| follow up | Take further action after an initial step | "Follow up the installation with the configuration step." |
| back up | Make a copy for safekeeping | "Back up the database before you apply the migration." |
| roll back | Return to a previous state | "Roll back the deployment if the health check fails." |

NOTE: "Log in" and "log out" use the approved verb "log" with the prepositions "in" and "out." Do not use "sign in," "sign out," "log on," or "log off." The verb "back up" (two words) is approved only for making copies. Do not use it for movement ("the car backs up") or support ("back up your claim").

## Edge Cases

### Edge Case 1: When a Framework or Tool Name Contains a Phrasal Verb

Some frameworks and tools have names that are phrasal verbs. Per Rule 1.5, technical code nouns are allowed. When you refer to the framework by its official name, use the phrasal verb form:

- "Use `setuptools` to package the Python project." (tool name)
- "The `cleanup` task runs after each deployment." (task name in a build system)
- "Configure the `rollback` strategy in the deployment manifest." (feature name)

When you describe what the framework does — not what it is called — apply Rule 9.3:

- "`setuptools` configures the package metadata." (not "sets up the package metadata")
- "The `cleanup` task removes the temporary files." (not "cleans up the temporary files")

The distinction: a proper name is a noun (P1.5). A description of behavior is a verb phrase and must follow Rule 9.3.

### Edge Case 2: When a Code Keyword Is Also a Phrasal Verb Component

Some code keywords overlap with phrasal verb components. "Break," "continue," "throw," and "catch" are all approved as code keywords (P1.5). In documentation, use them as technical nouns or as approved verbs with their technical meaning:

- "The `break` statement exits the loop immediately." (keyword as noun — approved)
- "The function throws an exception when the input is null." (technical verb — approved, P1.12)
- "The code breaks out of the loop when the condition is true." (phrasal verb — NOT approved)

The last example violates Rule 9.3 because "breaks out of" is a phrasal verb. Replace it: "The code exits the loop when the condition is true."

Similarly, "catch" in "the handler catches the error" is approved (technical verb). But "the handler catches up with the event stream" is a phrasal verb and is not approved. Replace: "the handler synchronizes with the event stream."

### Edge Case 3: Two Approved Words That Are Not a Phrasal Verb

Not every verb+preposition combination is a phrasal verb. The rule applies only when the combination creates a meaning different from the meanings of the individual words.

When the preposition is part of a prepositional phrase that describes location, direction, or time — and the verb keeps its approved meaning — the combination is permitted:

- "The application runs on the server." ("runs" keeps its approved meaning; "on the server" is a prepositional phrase of location)
- "The data flows from the input channel to the output channel." ("flows" keeps its approved meaning; the prepositions describe direction)
- "Write the configuration to the file." ("write" keeps its approved meaning; "to the file" describes the target)

Contrast these with actual phrasal verbs where the meaning changes:

- "The application runs on for too long." ("run on" = continues without stopping — phrasal verb, not approved)
- "The team writes up the test plan." ("write up" = compose formally — phrasal verb, not approved)

The test: if you can remove the preposition and the sentence still has approximately the same meaning, the preposition is part of a prepositional phrase and the combination is not a phrasal verb. If removing the preposition changes the meaning completely, it is a phrasal verb.

### Edge Case 4: Generated Documentation and Code Comments

Auto-generated documentation from tools such as JSDoc, Sphinx, or `rustdoc` can contain phrasal verbs that the developer wrote in the source code. The generated output inherits the phrasal verbs from the source.

When you write doc comments that a tool will extract and publish, apply Rule 9.3 to the source text. The generated documentation will then be compliant.

When you consume third-party generated documentation that you cannot edit, you do not need to correct it. The rule applies to documentation that you write or maintain.

### Edge Case 5: When a Single Approved Verb Does Not Exist for the Exact Meaning

Some phrasal verbs have no exact single-verb replacement in the approved vocabulary. In these cases, apply Rule 9.1: use a different sentence construction.

- "The function calls back the caller with the result." → "The function sends the result to the caller through a callback." (rewrite the sentence)
- "The cache warms up before it serves traffic." → "The cache loads the data before it serves traffic." (use a different approved verb with a close meaning)
- "The validator flags up any missing fields." → "The validator reports any missing fields." (use "reports" or "marks")
- "The loop churns through the dataset." → "The loop processes the dataset." ("process" is not in the canonical synonym table but it is a well-known technical verb, P1.12)

When no single approved verb is a perfect replacement, prefer the verb that is closest in meaning and add clarifying context in a subsequent sentence if necessary.

## Cross-References

| Rule | Relationship |
|------|-------------|
| Rule 1.1 — Use approved words from the STE-Code dictionary | The dictionary lists which words are approved and their approved meanings. Check the dictionary before you use a verb+preposition combination to confirm each word is approved individually. |
| Rule 1.2 — Use words only as their specified part of speech | A phrasal verb often changes the effective part of speech of the preposition. "Up" in "set up" is not a preposition of direction but a particle that modifies the verb. |
| Rule 1.4 — Use only approved verb forms and adjective forms | Phrasal verbs create non-standard verb forms that are not in the approved list. Replacing a phrasal verb with a single approved verb guarantees the form is approved. |
| Rule 1.11 — One term per concept | Two documentation sections that describe the same action — one with "set up" and another with "configure" — violate the consistency rule. Using a single approved verb everywhere prevents this. |
| Rule 1.12 — Technical verbs are allowed | Technical verbs such as "deploy," "compile," "parse," "serialize," and "deserialize" are approved. Do not replace a technical verb with a phrasal verb: "serialize the object" is correct; "turn the object into a string" is not. |
| Rule 9.1 — Use a different sentence construction | When no single approved verb replaces a phrasal verb, rewrite the entire sentence. This is the primary escape hatch for Rule 9.3. |
| Rule 9.2 — Use each approved word correctly | Each word in a non-phrasal-verb combination must carry its approved meaning. Even when a combination is not a phrasal verb, confirm that each word is used with its dictionary meaning. |

## Grammar Notes

### Particle vs. Preposition

A phrasal verb combines a verb with a particle (a word that looks like a preposition but functions as part of the verb). The particle changes the meaning of the verb instead of introducing a prepositional phrase.

In the sentence "The function writes the value to the file," the word "to" is a preposition. It introduces the prepositional phrase "to the file." The verb "write" keeps its approved meaning. This is not a phrasal verb.

In the sentence "The function writes up the report," the word "up" is a particle. It combines with "write" to create the meaning "compose formally." This is a phrasal verb and is not approved.

### Separable vs. Inseparable Phrasal Verbs

English phrasal verbs can be separable (the object can go between the verb and the particle) or inseparable (the object must follow the particle). This rule applies to both types equally:

- Separable: "The script sets the environment up." → "The script configures the environment." ("set up" is separable)
- Inseparable: "The handler looks after the connection pool." → "The handler manages the connection pool." ("look after" is inseparable)

The separability does not change the rule. Both forms are prohibited unless the phrasal verb is specifically approved.

### Why Phrasal Verbs Are Dangerous in Code Documentation

Phrasal verbs cause three types of problems in code documentation:

1. **Ambiguity.** Many phrasal verbs have multiple meanings. "Take off" can mean "remove," "depart," or "become successful." A reader of the documentation cannot be sure which meaning applies.

2. **Non-native comprehension.** Phrasal verbs are one of the most difficult features of English for non-native speakers. A developer who knows the approved meanings of "take" and "off" will not understand "take off" as a phrasal verb.

3. **Searchability.** A user who searches for "remove" will not find documentation that uses the phrasal verb "take off" or "strip out." Consistent use of single approved verbs makes documentation searchable.

### The "One Word Where Possible" Principle

The ASD-STE100 standard has an underlying principle that applies strongly to code documentation: where one word can do the work of two, use the one word. A phrasal verb uses two or three words (verb + one or two particles) to express one meaning. A single approved verb is always preferred:

- "Put up with" (3 words) → "Tolerate" (1 word) — but "tolerate" is not in the code-domain synonym table; "accept" is preferred
- "Come up with" (3 words) → "Propose" or "suggest" (1 word)
- "Cut down on" (3 words) → "Reduce" (1 word)
- "Get rid of" (3 words) → "Remove" (1 word)

This principle aligns with the core STE-Code value: precision through simplicity. Every extra word is a chance for misunderstanding.
