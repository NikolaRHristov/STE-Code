# Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec9-rule9.1](ste-code/grouped/), Rule 9.1

## Original Rule

Use a different sentence construction to write a sentence when a word-for-word replacement is not sufficient.

STE is a controlled natural language with a controlled dictionary. To help you use the approved words correctly, the dictionary gives approved alternatives for words that are not approved. If you find an alternative that has the same part of speech, you can use it to replace the word that is not permitted (a word-for-word replacement).

When you replace a word, always make sure that the alternative that you select does not change the meaning of the sentence. If the meaning changes, or if the alternative does not have the same part of speech, you must use a different sentence construction.

A different sentence construction is necessary because:

1. You must change the grammatical structure of the sentence to use the alternative that you selected.
2. The word-for-word replacement of the word that is not approved gives a meaningless result.
3. The approved alternative that you find changes the meaning of the sentence.
4. The word that you must replace is not in the dictionary.

## STE-Code Adaptation

> **See also:** Rule 9.2 — Use Each Approved Word Correctly; Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs; Rule 9.4 — When You Select Terminology or Wording, Always Use a Consistent Style

Use a different sentence construction to write a sentence when a word-for-word replacement is not sufficient.

In code documentation, when a word is not approved in the controlled terminology, the dictionary gives approved alternatives. If the alternative has the same part of speech and does not change the meaning, you can do a word-for-word replacement. If the meaning changes, the part of speech differs, or a word-for-word replacement gives a meaningless result, you must write a new sentence with a different structure that uses only approved words while keeping the same technical meaning.

A different sentence construction is necessary because:

1. You must change the grammatical structure to use the approved alternative.
2. The word-for-word replacement gives a meaningless or unclear result.
3. The approved alternative changes the meaning of the sentence.
4. The word to replace is not in the controlled terminology.

When you cannot do a word-for-word replacement, think about the purpose of the sentence and use different words to get the same result. Frequently, you must select different words, use different verb forms, write shorter sentences, remove information that is not necessary, or get more information from a developer.

### Examples

> **Non-STE:** A timeout value of 5000 ms is acceptable for this endpoint.
>
> **STE:** A timeout value of 5000 ms is permitted for this endpoint.

("Acceptable" is not approved. The approved adjective "permitted" has the same part of speech and does not change the meaning, so a word-for-word replacement is sufficient.)
*Adapted from spec pair: "A value of 2 mm is acceptable." / "A value of 2 mm is permitted."*

> **Non-STE:** The stack trace in the console must be visible during the debugging session.
>
> **STE:** During the debugging session, make sure that you can see the stack trace in the console.

(The approved verb "see" replaces the adjective "visible." To use the verb "see," replace "must be" with "make sure that you can.")
*Adapted from spec pair: "The oil level on the sight gauge must be visible during the test." / "During the test, make sure that you can see the oil level on the sight gauge."*

> **Non-STE:** Loop the function twice to remove null values from the array.
>
> **STE:** Run the function for two iterations to remove null values from the array.

(The approved noun "iteration" together with the approved verb "run" replaces the verb "loop." The technical noun "two" replaces the adverb "twice.")
*Adapted from spec pair: "Cycle the unit twice to remove air from the lines." / "Operate the unit for two cycles to remove air from the lines."*

> **Non-STE:** Without this configuration change, the behavior of the function can be uncertain.
>
> **STE:** Without this configuration change, it is possible that the function will not behave as expected.

("Uncertain" is not in the controlled terminology. A word-for-word replacement such as "cannot be sure" or "cannot be known" gives a meaningless result. You must think about the meaning and write a new sentence.)
*Adapted from spec pair: "Without this modification, the service life of the unit can be uncertain." / "Without this modification, it is possible that the service life of this unit will be shorter than usual."*

> **Non-STE:** Just add a single log statement to the method.
>
> **STE:** Only add a single log statement to the method.
>
> NOT: Immediately add a single log statement to the method.

("Immediately" is the approved alternative for "just." But if you use it in this context, the meaning of the instruction changes.)
*Adapted from spec pair: "Just apply very light pressure to the surface." / "Only apply very light pressure to the surface." NOT: "Immediately apply very light pressure to the surface."*

> **Non-STE:** The occurrence of type errors in the build output is a serious problem.
>
> **STE:** Type errors in the build output are a serious problem.

("Occurrence" is not in the controlled terminology. You must think of a different construction that keeps the same meaning without the unapproved word.)
*Adapted from spec pair: "The incidence of water in fuel is dangerous." / "Water in fuel is dangerous."*

> **Non-STE:** Scroll the editor pane so that it clears the minimap overlay.
>
> **STE:** Scroll the editor pane until it is away from the minimap overlay.
>
> NOT: Scroll the editor pane so that it cleans the minimap overlay.

("Clear" is not an approved verb. Its only alternative in the controlled terminology is "clean" as a verb, but "clean" does not have the intended meaning in this context. The intended meaning is "to increase the distance between" — use "until it is away from.")
*Adapted from spec pair: "Lift the seat so that it clears the track locks." / "Lift the seat until it is away from the track locks." NOT: "Lift the seat so that it cleans the track locks."*

> **Non-STE:** If linting errors are detected during this procedure, the developer must perform the correction within a certain number of commits depending on error severity. Refer to following table:
>
> | Error severity detected | Time before correction |
> |---|---|
> | Critical | 1 commit |
> | Major | 3 commits |
> | Minor | 5 commits |

> **STE:** If you find linting errors, refer to the table that follows:
>
> | If the error is of this severity | Do the correction before |
> |---|---|
> | Critical | 1 commit |
> | Major | 3 commits |
> | Minor | 5 commits |

(In the non-STE example: the underlined words are not approved; the verb form "are detected" is passive; the first sentence is too long; an article is missing before "following table"; the instruction is not imperative. The STE version uses approved words, active voice, imperative form, and moves the instruction into the table heading to avoid repeating information.)
*Adapted from spec pair: the crack detection and repair table example using "If you find cracks, refer to the table that follows:" — see spec pages 117–119 for the full original.*

## Code-Domain Explanation

Rule 9.1 is the most powerful rule in the STE-Code system. It is the rule you use when all other word-level rules fail. In code documentation, this rule applies differently to each documentation type because each type has a different audience, a different level of formality, and a different set of technical constraints.

### README Files

README files are the first document a new developer sees. They must be clear, short, and welcoming. When a word-for-word replacement fails in a README, you must restructure the sentence to use simple, direct language. Frequently, this means you must:

- Replace passive descriptions with active instructions.
- Move complex explanations to a separate document.
- Use bullet points instead of long paragraphs.
- Remove marketing language and replace it with factual statements.

For example, a README that says "This library leverages asynchronous I/O to facilitate high-throughput data processing" has multiple unapproved words. A word-for-word replacement of each word individually ("This library uses asynchronous I/O to make easy high-throughput data processing") gives a meaningless result. You must think about the purpose of the sentence and write: "This library uses async I/O. It can process large quantities of data quickly."

### API Documentation

API documentation has strict structural requirements. Each endpoint, parameter, and return value must be described precisely. When a word-for-word replacement fails in API docs, you must:

- Keep the technical parameter names unchanged (Rule 1.5).
- Restructure the description sentence around the approved word.
- Use a different grammatical subject if the original subject depends on an unapproved word.
- Split compound descriptions into separate sentences, one per parameter or behavior.

For example, an API description that says "This endpoint facilitates the retrieval of user profiles" cannot be fixed by replacing "facilitates" with "makes easy" and "retrieval" with "the action to get." You must restructure: "This endpoint gets user profiles."

### Docstrings and Inline Comments

Docstrings and inline comments are the most constrained documentation type. They must be short, appear directly next to the code they describe, and frequently include code symbols that cannot be changed. When a word-for-word replacement fails in a docstring:

- Use the approved verb form even if it makes the sentence longer (Rule 1.4).
- Move complex explanations to a separate design document.
- If a word-for-word replacement is impossible in the available space, remove the sentence and replace it with a reference to a longer document.
- Never change a code symbol to match an approved word. Code symbols are technical nouns (Rule 1.5).

### Commit Messages

Commit messages have a conventional format: a short summary line, a blank line, and a body. When a word-for-word replacement fails in a commit message:

- Use imperative mood in the summary line ("Add feature" not "Added feature").
- Replace unapproved verbs with approved technical verbs from the STE-Code dictionary.
- If the commit message describes a complex change that needs many unapproved words, write a shorter message and put the details in the pull request description.
- Never use the commit message body as a substitute for proper documentation.

### Error Messages

Error messages must be short, clear, and actionable. They appear in logs, terminals, and monitoring dashboards. When a word-for-word replacement fails in an error message:

- Restructure the message to tell the user what occurred and what to do.
- Remove technical jargon that the user cannot act on.
- Use the approved words "cannot" and "do not" instead of unapproved negative forms.
- If the error message includes a stack trace or a code symbol, keep it unchanged (Rule 1.5).

> **Non-STE:** The application encountered an unrecoverable exception while attempting to instantiate the connection pool.
>
> **STE:** The application cannot start the connection pool. Look at the log for more data.

*Principles applied: P1, P2, P11. "Encountered" replaced with cannot + start. "Unrecoverable" removed because the user cannot act on it. "Exception" and "instantiate" replaced with simpler constructions.*

### Generated Code and Automated Output

When you document generated code (code produced by a compiler, a code generator, or an AI tool), the generated code itself is not subject to STE-Code rules. The documentation that describes the generated code must follow the rules. If the generated code includes unapproved words in its symbol names, you must keep those symbol names unchanged in the documentation (Rule 1.5), but you can describe their function using approved words in a restructured sentence.

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Object-oriented documentation uses class names, method signatures, and inheritance hierarchies as technical nouns. When you must restructure a sentence for Rule 9.1, you frequently encounter these patterns:

- **Abstract class descriptions** use words like "facilitate," "provide a mechanism for," and "serve as a base for." Replace these with "let you," "are used to," or restructure around the concrete behavior: "This abstract class lets subclasses share database connection logic."
- **Interface documentation** uses words like "contract," "guarantee," and "enforce." These are unapproved. Restructure: "All classes that use this interface must have a `save` method."
- **Inheritance descriptions** use "extend," "override," and "specialize." These are technical nouns (Rule 1.5) when they refer to code keywords, but they are unapproved verbs when used in descriptive sentences. When the keyword is the subject of the sentence, keep it. When it is a verb in the description, replace it.

> **Non-STE:** The `BaseRepository` class provides an abstraction that facilitates data access operations across multiple database backends.
>
> **STE:** The `BaseRepository` class lets you use the same data access methods with different databases.

*Principles applied: P1, P2, P7, P11. "Provides an abstraction that facilitates" is a chain of unapproved words. The STE version identifies the purpose (let you use the same methods) and states it directly. "Backends" replaced with "databases."*

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, immutable data, and type transformations. These concepts frequently use words like "evaluate," "reduce," "compose," and "curry" that are technical nouns in the functional paradigm but may not be in the STE-Code dictionary. When you must restructure:

- **Type signatures** are code, not prose. They are technical nouns (Rule 1.5) and must stay unchanged.
- **Function descriptions** use words like "maps over," "folds," and "lifts." These are technical verbs (Rule 1.12) when they name a specific operation. When they are used in a general descriptive sense, replace them: "applies a function to each element" instead of "maps over."
- **Monad and functor descriptions** use abstract mathematical language. Restructure around the practical effect: "lets you chain operations that can fail" instead of "provides a monadic interface for effectful computations."

> **Non-STE:** This function `fmap`s the provided transformation over the `Maybe` value, yielding a new `Maybe` that encapsulates the transformed result.
>
> **STE:** This function applies the transformation to the `Maybe` value. If the `Maybe` value is `Just x`, the result is `Just (f x)`. If it is `Nothing`, the result is `Nothing`.

*Principles applied: P1, P5. The code symbols `fmap`, `Maybe`, `Just`, `Nothing` are kept as technical nouns. "Yielding," "encapsulates," and "transformed result" are restructured into concrete conditional descriptions.*

### Procedural Documentation (C, Go, Bash)

Procedural documentation describes sequences of steps, memory operations, and system calls. When you must restructure for Rule 9.1:

- **Memory management descriptions** use words like "allocate," "deallocate," "free," and "dereference." "Allocate" and "free" are technical verbs (Rule 1.12). "Deallocate" is not approved; replace with "free" or "release."
- **Error handling in C** uses words like "errno," "perror," and "return codes." These are technical nouns (Rule 1.5). The descriptions around them must use approved words.
- **Shell script documentation** uses words like "pipe," "redirect," and "subshell." These are technical nouns when they name shell features, but unapproved when used as general verbs. "Send the output of command A to command B" instead of "pipe command A to command B" when the word "pipe" is not a code keyword in context.

> **Non-STE:** The program allocates a buffer on the heap, then deallocates it after processing to prevent memory leaks.
>
> **STE:** The program gets a buffer from the heap. After it uses the buffer, it releases the memory to prevent memory leaks.

*Principles applied: P1, P2, P11. "Allocates" replaced with "gets." "Deallocates" replaced with "releases the memory." The sentence is split into two shorter sentences.*

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state, not procedures. This creates a unique challenge for Rule 9.1 because declarative descriptions naturally use passive voice and stative verbs. When you must restructure:

- **SQL documentation** describes what a query returns, not what it does. Use "the query gets rows where..." instead of "the query retrieves rows that satisfy..."
- **Terraform documentation** describes resource configurations. Use "this resource makes a virtual machine with the given settings" instead of "this resource provisions a compute instance."
- **Kubernetes YAML documentation** describes workload specifications. Keep field names as technical nouns (Rule 1.5). Restructure the surrounding description: "the `replicas` field sets the number of Pods" instead of "the `replicas` field specifies the desired Pod count."

> **Non-STE:** This Deployment manifest orchestrates the rollout of three replicated Pods, ensuring high availability through automated rescheduling.
>
> **STE:** This Deployment makes three copies of the Pod. If a Pod stops, the system starts a new Pod automatically.

*Principles applied: P1, P2, P7, P11. "Orchestrates," "rollout," "ensuring," and "high availability" are all restructured. The sentence is split. "Replicated" becomes "copies." "Automated rescheduling" becomes "starts a new Pod automatically."*

### Systems Documentation (Rust Ownership, C Memory)

Systems documentation describes ownership, lifetimes, and memory safety guarantees. These concepts use words like "borrow," "own," "move," and "drop" that are both code keywords (Rule 1.5) and general English words. The context determines whether they are approved:

- When used as Rust keywords (in code font): keep unchanged.
- When used as descriptive verbs in prose: check against the STE-Code dictionary. "Borrow" is not an approved verb; replace with "get a reference to." "Own" is not an approved verb; replace with "has" or "controls." "Move" is an approved verb but has a specific meaning in Rust; when the meaning is the Rust ownership transfer, use "gives" or "moves" depending on context.

> **Non-STE:** When a value is moved, the original binding can no longer be utilized to access that value.
>
> **STE:** When you move a value, you cannot use the first variable name to get the value.

*Principles applied: P1, P2, P13. "Utilized" replaced with "use." "Binding" is a technical noun (kept as "variable name" for clarity). "Original" and "access" are restructured. The passive "is moved" becomes active "you move."*

## Extended Examples

> **Non-STE:** The middleware intercepts incoming requests and modifies the headers prior to forwarding them to the downstream service.
>
> **STE:** The middleware gets each request. It changes the headers. Then it sends the request to the next service.

*Principles applied: P1, P2, P6, P11. "Intercepts" is not approved. "Modifies" replaced with "changes." "Prior to forwarding" replaced with "Then it sends." "Downstream service" is jargon (P10); "next service" is clearer. The long sentence is split into three short sentences.*

> **Non-STE:** Utilize the `--verbose` flag to surface detailed diagnostic information during the build process.
>
> **STE:** Use the `--verbose` flag to show detailed diagnostic data during the build.

*Principles applied: P1, P11. "Utilize" is in the Synonym Table (prefer "use"). "Surface" as a verb is not approved; "show" is the approved alternative. "Information" replaced with "data" (see dictionary). "Process" removed as redundant.*

> **Non-STE:** This configuration option governs whether the linter enforces the rule set in a strict or permissive fashion.
>
> **STE:** This configuration option sets how the linter applies the rules. You can set it to strict or permitted.

*Principles applied: P1, P2, P7. "Governs" is not approved. "Enforces" is not approved. "Fashion" is not approved. The sentence is restructured around "sets" and split. "Permissive" has no direct approved alternative; "permitted" (adjective) is used after restructuring.*

> **Non-STE:** The garbage collector reclaims memory from objects that are no longer referenced, thereby preventing the application from exhausting available heap space.
>
> **STE:** The garbage collector frees memory that the application does not use. This prevents the application from using all the available heap memory.

*Principles applied: P1, P2, P11. "Reclaims" replaced with "frees." "No longer referenced" restructured to "does not use." "Thereby preventing" split into a new sentence. "Exhausting" replaced with "using all."*

> **Non-STE:** Should the connection pool become saturated, the system will automatically spawn additional worker threads to handle the overflow.
>
> **STE:** If the connection pool is full, the system automatically starts more worker threads.

*Principles applied: P1, P2, P10, P11. "Should" as a conditional is not approved; "If" is the approved alternative. "Saturated" is jargon (P10). "Spawn" is not approved; "starts" is approved. "Handle the overflow" is unnecessary detail removed for clarity.*

> **Non-STE:** The `render` method leverages a virtual DOM diffing algorithm to minimize expensive DOM manipulations.
>
> **STE:** The `render` method uses a virtual DOM diff algorithm. This algorithm decreases the number of DOM changes.

*Principles applied: P1, P2, P11. "Leverages" is in the Synonym Table (prefer "use"). "Minimize" is not approved as a verb in this sense; restructured. "Expensive" in the sense of "computationally costly" is jargon (P10); the specific meaning is restated as "decreases the number of." "Manipulations" replaced with "changes."*

## Edge Cases

### Framework Names That Are Also Unapproved Words

Some framework names are identical to unapproved English words. For example, the JavaScript build tool "Vite" (French for "fast"), the Python web framework "Flask," and the CSS framework "Tailwind" are all technical nouns (Rule 1.5). When you document these frameworks, keep the framework name unchanged. The framework name is a proper noun and a technical noun. It is not subject to word-level rules. However, do not use the framework name as a verb (Rule 1.7). Do not write "Flask your application." Write "Use Flask with your application."

When a framework name is also a common English word (for example, "Express," "Next," "Fresh"), the context in the sentence tells the reader if the word is a framework name or a common word. Use code font for framework names to make the distinction clear.

### Code Keywords That Conflict With Approved Words

Some programming language keywords are identical to approved STE-Code words but have a different meaning. For example, "use" is an approved STE-Code verb meaning "to put into service." In Rust, `use` is also a keyword that imports names from a module. When you document Rust code, the keyword `use` in code font is a technical noun (Rule 1.5). The same word in prose follows the STE-Code dictionary. Write: "Put `use std::io` at the top of the file. Then you can use the `io` module."

The same applies to "move" (approved STE-Code verb; Rust keyword for ownership transfer), "return" (approved STE-Code verb; keyword in most languages), and "break" (approved STE-Code verb; keyword for loop exit). Always use code font for the keyword and prose for the approved meaning.

### Generated Code and Automated Output

When you document generated code, the generated code itself is not subject to STE-Code rules. Only your documentation prose must follow the rules. If the generated code includes symbol names that use unapproved words, keep those symbol names unchanged in your documentation. For example, if a code generator produces a function named `utilizeData()`, you must keep the function name `utilizeData()` in your documentation because it is a code symbol (Rule 1.5). However, your description of what the function does must use approved words: "The `utilizeData()` function uses the data to make a report."

### Quoted Log Output and Error Messages

When you quote log output or error messages from a system, keep the quoted text exactly as it appears. The quoted text is data, not documentation. Your surrounding prose must follow STE-Code rules. For example, if a log message says "Encountered irrecoverable error," you write: The log shows: "Encountered irrecoverable error." This message means that the application found an error from which it cannot continue.

### When Restructuring Changes the Technical Precision

Sometimes a word-for-word replacement is not sufficient, but a full restructuring removes technical precision that the reader needs. For example, in a security audit document, the phrase "the attacker can exploit the race condition to achieve arbitrary code execution" uses many unapproved words. A word-for-word replacement fails. A full restructuring to "a bad actor can use the timing problem to run code" loses precision. In this case, you have three options:

1. Split the sentence and add a clarifying note that uses approved words to define the technical term.
2. Keep the technical term in code font with a glossary definition.
3. If the document is an internal security audit and the audience is security engineers, you can keep the term as a technical noun (Rule 1.5) with an approved-word definition on first use.

The choice depends on the audience and the document type. When in doubt, prefer option 1 or 2.

### Code Comments That Quote an Algorithm Name

When you document an algorithm with a standard name (for example, "Dijkstra's shortest path," "QuickSort," "Two-Phase Commit"), the algorithm name is a technical noun (Rule 1.5). Keep the algorithm name unchanged even if it contains unapproved words. Your description of what the algorithm does must use approved words. Write: "The `QuickSort` algorithm sorts the array. It selects a pivot element and moves smaller elements before it and larger elements after it."

## Grammar Notes

### The Parts-of-Speech Constraint

The original ASD-STE100 Rule 9.1 emphasizes that a word-for-word replacement is only possible when the approved alternative has the same part of speech as the word it replaces. This constraint is the most frequent reason that you must restructure a sentence.

In code documentation, the parts-of-speech constraint applies with additional complexity because code documentation mixes natural language with code symbols. A word in your documentation can be:

1. A natural language word subject to STE-Code rules.
2. A code keyword in code font (technical noun, Rule 1.5).
3. A framework or library name (technical noun, Rule 1.5).
4. A parameter name or variable name (technical noun, Rule 1.5).

When you evaluate if a word-for-word replacement is possible, first identify which category the word belongs to. If the word is in categories 2, 3, or 4, it is not subject to replacement. If it is in category 1, check the STE-Code dictionary for an approved alternative with the same part of speech.

### Adjective-to-Verb Restructuring

A common pattern in Rule 9.1 is the change from an adjective to a verb. When an unapproved adjective describes a state, the sentence frequently uses "is + adjective" or "must be + adjective." The approved alternative is frequently a verb. To use the verb, you must restructure the sentence around an action. The pattern is:

1. Identify the adjective (for example, "visible").
2. Find the approved verb alternative (for example, "see").
3. Identify the agent who does the action (frequently "you").
4. Restructure: "X is visible" becomes "make sure that you can see X."

This pattern applies to many code documentation scenarios: "is configurable" becomes "you can set"; "is accessible" becomes "you can get to" or "you can open"; "is extensible" becomes "you can add to."

### Noun-to-Verb Restructuring

Another common pattern is the change from a noun to a verb. When an unapproved noun names an action, the approved alternative is frequently a verb. The pattern is:

1. Identify the noun that names an action (for example, "retrieval," "validation," "execution").
2. Find the approved verb alternative (for example, "get," "check," "do").
3. Remove the light verb that carries the noun (for example, "perform," "carry out," "conduct").
4. Restructure: "perform the retrieval of X" becomes "get X."

This pattern is especially common in API documentation and formal technical specifications where nominalizations (action nouns) are used to sound formal. The STE-Code version is always shorter and clearer.

### Splitting Long Sentences

When a word-for-word replacement is not sufficient, the restructured sentence is frequently longer than the original because approved words are simpler and need more context. Sometimes the restructured sentence becomes too long (more than 20 words for a procedural sentence or 25 words for a descriptive sentence). In this case, you must split the sentence.

The split point is usually:

- Before a conjunction ("and," "or," "but").
- Before a conditional clause ("if," "when").
- Between the cause and the effect.
- Between the problem and the solution.

After splitting, make sure that the first sentence has a complete meaning and the second sentence does not depend on the first sentence for its grammatical subject.

### Removing Unnecessary Information

The original ASD-STE100 notes that "frequently, a word-for-word replacement is impossible because the word has no synonym that is sufficiently close in meaning. You must think of what you are trying to say and, frequently, some of the meaning must be lost."

This is also true for code documentation. Some sentences in code documentation contain information that is not necessary for the reader to complete a task. When a word-for-word replacement fails and a restructuring would make the sentence too long, examine if the information is necessary. Remove:

- Marketing adjectives ("robust," "scalable," "enterprise-grade").
- Redundant modifiers ("completely," "totally," "absolutely").
- Implementation details that belong in the code, not the documentation.
- Historical context that belongs in a changelog or an architecture decision record.

## Cross-References

This rule interacts with many other rules in the STE-Code system. The most important cross-references are:

- **Rule 1.1 (Use Approved Words):** Rule 9.1 is the fallback when Rule 1.1 cannot be satisfied with a word-for-word replacement. Always try a word-for-word replacement first. Only use Rule 9.1 when the replacement fails.

- **Rule 1.5 (Technical Code Nouns):** Code keywords, framework names, and library names are technical nouns and are not subject to replacement. When a sentence contains a technical noun and also an unapproved word, you must restructure only the parts of the sentence that are not technical nouns.

- **Rule 1.12 (Technical Verbs):** Technical verbs like "build," "deploy," "test," and "lint" are approved. Do not replace them. Rule 9.1 applies only to non-technical words in descriptive prose.

- **Rule 1.7 (Do Not Use Technical Nouns as Verbs):** When a technical noun is used as a verb (for example, "to docker the application"), you must restructure the sentence. Rule 9.1 gives the method for restructuring.

- **Rule 9.2 (Use Each Approved Word Correctly):** After you restructure a sentence with Rule 9.1, make sure that each approved word in the new sentence is used with its approved meaning. Rule 9.2 applies to the restructured sentence.

- **Rule 9.3 (Do Not Make Phrasal Verbs):** When you restructure a sentence, do not introduce phrasal verbs. For example, do not restructure "initiate the process" to "kick off the process." Use "start the process."

- **Rule 9.4 (Consistent Style):** When you restructure a sentence about a concept, use the same construction for all sentences about that concept in the document. Consistency is as important as correctness.

- **Rule 3.1 (Use Simple Verb Tenses):** When you restructure a sentence with Rule 9.1, use only the simple present, simple past, or imperative. Do not introduce continuous or perfect tenses.

- **Rule 5.1 (Short Sentences):** After restructuring, check that the new sentence is not longer than 20 words (procedural) or 25 words (descriptive). If it is longer, split it further or remove unnecessary information.

- **Rule 6.1 (Active Voice):** When possible, restructure the sentence in the active voice. Active voice makes the agent clear and helps you select the correct approved verb.
