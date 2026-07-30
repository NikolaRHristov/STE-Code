# Rule 3.5 — Use the "-ing" Form of a Verb Only as a Technical Noun or as a Modifier in a Technical Noun

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.5

## Original Rule

Use the "-ing" form of a verb only as a technical noun or as a modifier in a technical noun.

In English, words that have an "-ing" form can have different functions in a sentence (different parts of speech).

General examples:

Words that have an "-ing" form can be part of a verb to describe an action in the present.

*Be careful while the door is opening.*

They can also be adjectives.

*An opening door can be dangerous.*

They can be nouns or parts of noun phrases.

*Opening a door can be dangerous.*

They can make long groups of modifiers, noun phrases, and dependent clauses.

*A mechanic opening a door without obeying the specified safety precautions can easily cause injury to persons standing near the door.*

These different functions for words that have an "-ing" form can frequently cause ambiguity or long, complex sentences. Thus, words that have an "-ing" form are usually not permitted.

Examples:

> **Non-STE:** When you are doing this procedure, obey all the safety precautions.
>
> **STE:** When you do this procedure, obey all the safety precautions.

> **Non-STE:** [fragment] inappropriate tools without observing the manufacturer's instructions, are in danger of coming into contact with these materials and thus suffering from skin irritation and breathing problems.
>
> **STE:** Before you use dangerous materials, obey these precautions:
>
> 1. Read the manufacturer's instructions.
> 2. Make sure that there is sufficient airflow in the work area.
> 3. Put on a face mask and protective clothing.
> 4. Get the correct tools to open the containers for these materials.
>
> If you do not obey these precautions, injury to your skin and your lungs can occur.

Words that have an "-ing" form and are technical nouns or parts of technical nouns

You can use a word that has an "-ing" form as a technical noun (for example, in procedural titles or headings).

Examples:

*Cleaning, Testing and Fault Isolation, Handling, Packaging, Shipping, Troubleshooting*

You can also use the "-ing" form of a verb as a modifier in a technical noun. This modifier is an adjective that is related to the function of a system, component, part, tool, material, or equipment.

Examples:

*Air-conditioning system, degreasing agent, grinding wheel, polishing disc, sanding machine, switching relay, welding torch*

Approved words that have an "-ing" form

Only a small number of approved words in the dictionary have an "-ing" form. They are:

- Nouns (*lighting, opening, routing,* and *servicing*)
- Adjectives (*mating, missing,* and *remaining*)
- A pronoun (*something*)
- A preposition (*during*).

## STE-Code Adaptation

In code documentation, words with an "-ing" form cause ambiguity when they are used as part of a compound verb tense (present progressive, past progressive). STE-Code prohibits the "-ing" form in verb constructions.

The "-ing" form is permitted in only two contexts:

1. As a technical noun — used in section titles, headings, or the name of a code process:
   *Building, Testing, Deploying, Logging, Parsing, Routing, Serializing*

2. As a modifier in a technical noun — used to describe the function of a system, module, tool, or service:
   *building system, testing framework, routing module, logging service, parsing library, scheduling middleware, rate-limiting gateway*

Do not use the "-ing" form as part of a compound verb. Convert the sentence to a simple tense instead. If the "-ing" form appears in a long, complex sentence with multiple modifiers, break the sentence into a vertical list of clear instructions.

### Examples

> **Non-STE:** When you are running the build command, check the terminal for errors.
>
> **STE:** When you run the build command, check the terminal for errors.
>
> *Adapted from spec pair: "When you are doing this procedure, obey all the safety precautions." / "When you do this procedure, obey all the safety precautions."*

> **Non-STE:** Developers writing code without following the style guide can cause formatting conflicts and merge issues.
>
> **STE:** Obey the style guide when you write code. If you do not obey the style guide, formatting conflicts and merge issues can occur.
>
> *Adapted from spec pair: "[fragment] inappropriate tools without observing the manufacturer's instructions, are in danger of coming into contact with these materials and thus suffering from skin irritation and breathing problems." / "Before you use dangerous materials, obey these precautions: ... If you do not obey these precautions, injury to your skin and your lungs can occur."*

> **Non-STE:** The script is processing all the input files while logging the results to the console.
>
> **STE:** The script processes all the input files. Then it writes the results to the console.
>
> *Additional code-domain example — no direct spec pair*

## Code-Domain Explanation

This rule has different effects on each type of code documentation. The following sections explain the effects in detail.

### README Files

README files contain installation steps, build instructions, and usage guides. The "-ing" form in a README file can make an instruction seem continuous or incomplete. Use the imperative mood with simple present verbs instead.

When a README file has a section title with an "-ing" technical noun (for example, "Building the Project" or "Testing Your Changes"), this use is correct. The "-ing" form is a technical noun in a heading. The error occurs when the same "-ing" word appears in a procedural sentence below the heading.

> **Non-STE:** You should be running the tests after making each change.
>
> **STE:** Run the tests after each change.

### API Documentation

API reference documents describe what a method or function does. The simple present tense is the standard convention for API documentation. The present progressive ("is returning," "is throwing") is not standard and can confuse readers who expect a simple tense.

> **Non-STE:** This method is returning a list of active connections.
>
> **STE:** This method returns a list of active connections.

When an API method name contains an "-ing" word (for example, `getPendingTasks` or `StreamingResponse`), the "-ing" word is a technical noun inside an identifier. This use is correct. The rule applies to the documentation text around the identifier, not to the identifier itself.

### Docstrings and Inline Comments

Docstrings describe the purpose, parameters, and return value of a function or class. Use the simple present indicative for descriptions and the imperative mood for the summary line.

> **Non-STE:** This function is computing the hash of the input string and returning it as a hex digest.
>
> **STE:** Compute the hash of the input string. Return the result as a hex digest.

Inline comments explain a specific line or block of code. The "-ing" form in an inline comment can make the comment read as a narration of ongoing action instead of a static explanation.

> **Non-STE:** // looping through the array and checking each element
>
> **STE:** // Loop through the array and check each element.

### Commit Messages

Commit messages follow the convention of imperative mood ("Add feature," "Fix bug"). The "-ing" form in a commit message ("Adding feature," "Fixing bug") breaks this convention and can make the message less clear about what the commit contains.

> **Non-STE:** Fixing the race condition in the connection pool.
>
> **STE:** Fix the race condition in the connection pool.

NOTE: Some projects use the "-ing" form as a commit message convention (for example, in changelog auto-generation scripts). In these projects, apply the project convention. The STE-Code rule applies to all other code documentation in the repository.

### Error Messages and Log Output

Error messages and log entries describe an event or state. The simple present or simple past tense is more direct and easier to parse in a log stream than the present progressive.

> **Non-STE:** The server is starting on port 8080...
>
> **STE:** Server started on port 8080.

> **Non-STE:** The parser is encountering an unexpected token at line 42.
>
> **STE:** Unexpected token at line 42.

## Paradigm-Specific Guidance

### Object-Oriented Paradigm (Java, C++, C#, Python Classes)

In object-oriented documentation, class method descriptions and constructor documentation use the simple present. The "-ing" form often appears in descriptions of state or behavior that span across method calls. Replace it with a simple tense and, if necessary, add a clarifying sentence about state.

> **Non-STE:** The `connect()` method is establishing a persistent connection and is returning a session object.
>
> **STE:** The `connect()` method opens a persistent connection. It returns a session object.

When you document an abstract class or interface, use the simple present for the contract description. The "-ing" form can make the contract seem provisional or incomplete.

> **Non-STE:** Classes implementing this interface are providing a streaming data source.
>
> **STE:** Classes that implement this interface provide a streaming data source.

NOTE: "Streaming" in "streaming data source" is a modifier in a technical noun. This use is correct.

### Functional Paradigm (Haskell, Elixir, Clojure, Rust)

Functional code documentation describes pure functions, data transformations, and pipelines. The "-ing" form often appears in descriptions of function composition or lazy evaluation. Replace it with the simple present and, if necessary, use a vertical list to show the pipeline steps.

> **Non-STE:** The `process` function is mapping over the list, filtering out null values, and reducing the result.
>
> **STE:** The `process` function:
> 1. Maps over the list.
> 2. Removes null values.
> 3. Reduces the result.

When you document a recursive function, the "-ing" form can obscure the base case and recursive case distinction. Use separate sentences with simple tenses for each case.

> **Non-STE:** This function is recursing through the tree while accumulating the sum.
>
> **STE:** This function recurses through the tree. It accumulates the sum at each node.

### Procedural Paradigm (C, Go, Bash)

Procedural documentation often contains step-by-step instructions. The "-ing" form can blur the boundary between steps. Use imperative mood with simple verbs, one step per sentence.

> **Non-STE:** The program is opening the config file, parsing the YAML, and loading the settings.
>
> **STE:** The program:
> 1. Opens the config file.
> 2. Parses the YAML.
> 3. Loads the settings.

### Declarative Paradigm (SQL, Terraform, Kubernetes YAML, Dockerfile)

Declarative documentation describes the desired state of a system. The "-ing" form can introduce an unintended sense of ongoing action into a state description. Use the simple present or the imperative mood.

> **Non-STE:** This Terraform module is provisioning an AWS VPC with public and private subnets.
>
> **STE:** This Terraform module provisions an AWS VPC with public and private subnets.

> **Non-STE:** The Dockerfile is building the image in two stages.
>
> **STE:** The Dockerfile builds the image in two stages.

When a Kubernetes resource name or Dockerfile instruction contains an "-ing" word (for example, `RollingUpdate` or `HEALTHCHECK`), the word is a technical noun. This use is correct. The rule applies only to the surrounding documentation text.

### Systems Programming (Rust Ownership Docs, C Memory Docs)

Systems documentation describes ownership, lifetimes, and memory models. These concepts are complex. The "-ing" form adds unnecessary grammatical complexity. Use simple sentences with clear subjects and verbs.

> **Non-STE:** The borrow checker is preventing multiple mutable references while allowing concurrent immutable borrows.
>
> **STE:** The borrow checker prevents multiple mutable references. It permits concurrent immutable borrows.

> **Non-STE:** The allocator is requesting a memory block from the operating system and returning a pointer.
>
> **STE:** The allocator requests a memory block from the operating system. It returns a pointer.

## Extended Examples

### Example 1 — README Installation Instructions

> **Non-STE:** After downloading the repository, you should be running the setup script to install all dependencies.
>
> **STE:** After you download the repository, run the setup script to install all dependencies.
>
> **Principle applied:** P4 — Use only approved verb forms. The compound verb "should be running" is replaced with the simple imperative "run."
>
> **Explanation:** The "-ing" form in "should be running" makes the instruction less direct. The imperative "run" is a clear, single-step command.

### Example 2 — API Method Documentation

> **Non-STE:** `getUser(id)` is querying the database and returning a User object, or it is throwing a NotFoundError if the user doesn't exist.
>
> **STE:** `getUser(id)` queries the database. It returns a `User` object. If the user does not exist, it throws a `NotFoundError`.
>
> **Principle applied:** P12 — Technical verbs (query, return, throw) are allowed. The compound "-ing" form is replaced with the simple present.
>
> **Explanation:** The original sentence has three "-ing" verb forms in one sentence. The STE version uses three short sentences, each with a simple present verb. This structure is easier to parse in an API reference.

### Example 3 — Docstring for a Function

> **Non-STE:** """This function is validating the input parameters before passing them to the downstream service, logging any validation failures along the way."""
>
> **STE:** """Validate the input parameters. Send the valid parameters to the downstream service. Log all validation failures."""
>
> **Principle applied:** P1 — Use approved words. "Downstream" is replaced with a simpler construction. The "-ing" forms are replaced with imperatives.
>
> **Explanation:** The original docstring is one long sentence with two "-ing" forms. The STE version breaks it into three short imperative sentences. Each sentence describes one task.

### Example 4 — Commit Message

> **Non-STE:** Updating the authentication middleware to handle expired tokens.
>
> **STE:** Update the authentication middleware to handle expired tokens.
>
> **Principle applied:** P4 — Use only approved verb forms. The "-ing" form "Updating" is replaced with the imperative "Update."
>
> **Explanation:** The "-ing" form in a commit message describes the change as an ongoing action. The imperative form describes the change as a completed instruction. Most version control conventions prefer the imperative form.

### Example 5 — Error Message in a CLI Tool

> **Non-STE:** Error: The configuration file is missing required fields. The application is stopping now.
>
> **STE:** Error: The configuration file does not contain the required fields. The application stops.
>
> **Principle applied:** P1/P3 — Use approved words with their approved meanings. "Missing" as an approved adjective is replaced with a clear verb construction. "Now" is removed as redundant.
>
> **Explanation:** The "-ing" form in "is missing" and "is stopping" makes the error message seem like a narration. The simple present makes the error message declarative and final. Error messages should state facts, not describe ongoing events.

### Example 6 — Configuration File Comment

> **Non-STE:** # The server is binding to this port and listening for incoming connections.
>
> **STE:** # The server binds to this port. It listens for connections.
>
> **Principle applied:** P9 — Prefer short, clear technical nouns. "Incoming" as a modifier is removed. The sentence is split for clarity.
>
> **Explanation:** Configuration file comments explain static settings. The "-ing" form in "is binding" and "listening" suggests a dynamic, ongoing process. The simple present describes the static behavior of the configuration parameter.

## Edge Cases

### Edge Case 1 — Framework Names with "-ing"

Some framework and library names contain an "-ing" form as part of their proper noun identity. Examples include the Spring Framework (Java), Flutter rendering engine (Dart), and the Streaming module (Node.js). These names are technical nouns (Rule 1.5) and are correct in all documentation contexts.

> **Correct:** The Spring Framework manages dependency injection.
> **Correct:** The Flutter rendering engine draws widgets on the screen.

Do not change the framework name. The rule applies only to the verbs and modifiers in the surrounding documentation text.

> **Non-STE:** Spring is wiring the dependencies at runtime.
>
> **STE:** Spring wires the dependencies at runtime.

### Edge Case 2 — Code Keywords That Look Like "-ing" Verbs

Some programming languages have keywords or standard library identifiers that end in "-ing." Examples include `String` (Java, C#, Python), `Binding` (WPF, Angular), `Warning` (Python logging), and `Nothing` (Kotlin, Scala). These words are not verbs. They are nouns, type names, or severity levels.

> **Correct:** The function returns a `String`.
> **Correct:** The compiler emits a `Warning`.

Do not remove or rewrite these identifiers. The rule applies only to verb forms, not to nouns that happen to end in "-ing."

### Edge Case 3 — Generated Code Comments

Auto-generated code often contains comments that use the "-ing" form in a stative or descriptive way. Examples include `// Auto-generated file — do not edit` and `// Mapping fields from database schema`.

If the generated comment is part of a toolchain you control (for example, a protobuf compiler or an OpenAPI generator), configure the toolchain to use STE-Code compliant output. If the toolchain is external and you cannot change its output, add a NOTE in your documentation that explains the non-STE source.

NOTE: This file contains comments generated by [tool name]. The comments do not follow STE-Code Rule 3.5.

### Edge Case 4 — Technical Noun "-ing" Forms in Verb Positions

Some approved technical nouns with "-ing" forms (for example, *Logging*, *Routing*, *Testing*) can appear in positions that look like verb constructions. This use is correct when the word is the subject of the sentence or the object of a preposition.

> **Correct:** Logging records all HTTP requests.
> **Correct:** The routing module sends packets to the correct destination.
> **Correct:** Start the testing framework.

If the same word is used as a verb, the sentence is not correct.

> **Non-STE:** The module is routing packets.
>
> **STE:** The module routes packets.

### Edge Case 5 — Gerunds in Quoted Identifiers or Literal Text

When an "-ing" form appears inside a quoted string, a code identifier, or literal text that must stay unchanged, do not rewrite the quoted content. The rule applies to the documentation text that surrounds the quoted content.

> **Non-STE:** The script outputs the message "Starting deployment" when it begins running.
>
> **STE:** The script outputs the message "Starting deployment" when it starts.

The quoted string "Starting deployment" stays unchanged. The verb "begins running" is rewritten to "starts."

## Cross-References

This rule interacts with several other STE-Code rules. Obey all related rules when you apply Rule 3.5.

- **Rule 1.1 (Approved Words):** Only approved words can appear in STE-Code documentation. If you replace an "-ing" verb with a different verb, make sure the replacement verb is an approved word from the STE-Code dictionary. Refer to the Canonical Synonym Table for preferred replacements.

- **Rule 1.5 (Technical Code Nouns):** Technical nouns with "-ing" forms (for example, *Building*, *Testing*, *Routing*) are permitted. Rule 3.5 defines the two contexts where these nouns are correct: as technical nouns in headings and as modifiers in technical noun phrases.

- **Rule 1.12 (Technical Verbs):** Technical verbs such as *build*, *deploy*, *test*, *lint*, *parse*, *compile*, *render*, *serialize*, and *query* are permitted. Use the simple present or imperative form of these verbs. Do not use the "-ing" form (*building*, *deploying*, *testing*) as a verb.

- **Rule 3.1 (Simple Verb Tenses):** Use only the simple present, simple past, and imperative mood. The "-ing" form is part of the progressive aspect and is not a simple tense. When you rewrite an "-ing" construction, choose a simple tense.

- **Rule 3.6 (Sentence Length):** Sentences must not exceed 20 words in procedural text and 25 words in descriptive text. When you replace a long "-ing" construction with simple tenses, you often need to split the sentence. Use vertical lists and short sentences to obey this rule.

- **Rule 3.7 (Noun Clusters):** The "-ing" form as a modifier in a technical noun can create long noun clusters (for example, *rate-limiting gateway configuration file parser*). Limit noun clusters to three words. If the cluster is longer, rewrite the sentence.

## Grammar Notes

### The Linguistic Basis of the Rule

In English grammar, the "-ing" form of a verb has three distinct functions. Each function creates a different type of ambiguity in technical documentation.

#### Function 1: Present Participle (Progressive Aspect)

The present participle combines with a form of "be" to make the progressive aspect. The progressive aspect describes an action that is in progress at a reference time.

> *The server is starting.* (present progressive — action in progress now)
> *The server was starting when the error occurred.* (past progressive — action in progress at a past time)

In code documentation, the progressive aspect is almost never necessary. Code behavior is described as a fact (simple present) or as a completed action (simple past). The progressive aspect adds a temporal frame that makes the documentation less precise, not more precise.

**Recommendation:** Always replace the progressive aspect with the simple present, simple past, or imperative mood. The replacement depends on the documentation context:

| Context | Progressive | Replacement |
|---------|------------|-------------|
| API doc | *is returning* | *returns* (simple present — describes permanent behavior) |
| Error message | *is stopping* | *stopped* (simple past — describes a completed event) |
| Procedure | *you are running* | *run* (imperative — gives a command) |
| Log output | *is processing* | *processes* (simple present — describes a state) |

#### Function 2: Gerund (Verbal Noun)

A gerund is an "-ing" form that functions as a noun. Gerunds name actions or processes.

> *Building the project takes five minutes.* (gerund as subject)
> *The script starts by loading the configuration.* (gerund as object of preposition)

In STE-Code, gerunds are permitted in two contexts only: as technical nouns in section titles and as modifiers in technical noun phrases. This restriction is narrower than general English grammar. A gerund that is not a recognized technical noun must be rewritten.

**Recommendation:** If the gerund names a documented process in your codebase (for example, *Testing*, *Deployment*, *Logging*), use it as a technical noun. If the gerund is a general English noun (for example, *learning*, *understanding*, *thinking*), replace it with an approved verb in a different sentence structure.

| General Gerund | STE-Code Replacement |
|---------------|---------------------|
| *Learning the API takes time.* | *You must study the API. This takes time.* |
| *Understanding the algorithm is important.* | *You must understand the algorithm.* |

#### Function 3: Participial Modifier (Adjectival Phrase)

A participial modifier is an "-ing" form that modifies a noun. It can appear before the noun (attributive position) or after the noun (postpositive position) as part of a reduced relative clause.

> *The running process consumes 2 GB of memory.* (attributive modifier)
> *The process running on port 8080 is the API server.* (reduced relative clause — "the process that is running")

Attributive modifiers that are recognized technical terms (for example, *running average*, *streaming data*, *scheduling policy*) are correct. Postpositive participial modifiers are ambiguous and must be rewritten as full relative clauses or separate sentences.

> **Non-STE:** The function handling the request validates the token.
>
> **STE:** The function that handles the request validates the token.

> **Non-STE:** The variable storing the result is a mutable reference.
>
> **STE:** The variable stores the result. The variable is a mutable reference.

### Structural Avoidance Patterns

When you edit documentation to remove "-ing" forms, apply these three structural patterns. Each pattern maps to a specific type of "-ing" construction.

**Pattern A — Compound Verb to Simple Verb**

Use this pattern when the "-ing" form is part of a progressive verb phrase (be + -ing). Remove the auxiliary verb "be" and change the "-ing" form to the simple present or imperative.

| Input Structure | Output Structure |
|----------------|-----------------|
| *is/are/am + -ing* | Simple present or imperative |
| *was/were + -ing* | Simple past |
| *will be + -ing* | Simple future (or "will + verb") |

**Pattern B — Participial Phrase to Separate Sentence**

Use this pattern when the "-ing" form is a participial modifier in a long sentence. Extract the participial phrase into a separate sentence with a clear subject.

| Input Structure | Output Structure |
|----------------|-----------------|
| *Subject [participial phrase] verb...* | *Subject verb. [New sentence with same subject].* |

**Pattern C — Gerund Subject to "You" + Verb**

Use this pattern when the "-ing" form is a gerund acting as the subject of a sentence. Replace the gerund with "You" + an imperative or simple present verb. This pattern makes the agent of the action explicit.

| Input Structure | Output Structure |
|----------------|-----------------|
| *Gerund + verb + object* | *[Imperative verb] + object.* or *You + [simple present verb] + object.* |

### Interaction with the Canonical Synonym Table

When you replace an "-ing" verb, you must also check the replacement verb against the STE-Code Canonical Synonym Table. The table lists preferred and avoided words for the code domain. Many "-ing" verbs in non-STE documentation are part of a longer multi-word verb phrase that contains an avoided word.

> **Non-STE:** The pipeline is leveraging the cache to speed up builds.
>
> **STE:** The pipeline uses the cache to make builds faster.

In this pair, three fixes work together:
1. Replace the "-ing" form (*is leveraging* → *uses*) — Rule 3.5.
2. Replace the avoided word (*leverage* → *use*) — Rule 1.1 and Canonical Synonym Table.
3. Replace the avoided word (*speed up* → *make faster*) — Rule 1.1 and Canonical Synonym Table.
