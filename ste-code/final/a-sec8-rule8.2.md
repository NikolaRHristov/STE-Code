# Rule 8.2 — Use Hyphens (-) to Connect Words That Are Directly Related

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.2

> **Source:** [master.md#sec8-rule8.2](ste-code/grouped/)

## Original Rule

**Rule 8.2** Use hyphens (-) to connect words that are directly related.

A hyphen (-) is a punctuation mark that connects words or parts of words. Use the hyphen for technical nouns to show that two or more words are directly related. This construction helps the reader to understand words and phrases more easily.

The examples that follow show how to use hyphens to connect words that are directly related.

1. Terms that have two or more words and are adjectives before a noun:

   low-altitude flight, high-pressure chamber, air-conditioned compartment, transmitter-receiver system, quick-release fastener, clamshell-type flap, eighteen-inch monitor, cast-aluminum bracket, three-to-one ratio, trial-and-error method, air-to-air refueling, soap-and-water solution, up-to-date information, run-on torque, break-away torque, cut-in speed, in-flight entertainment system, stiff-bristled brush, fire-resistant material, self-sealing hose

2. Two-word fractions or numbers:

   forty-seven, ninety-ninth, one hundred and sixty-two, three-sixteenths, one thirty-second

3. Terms that contain an uppercase letter plus a noun, or a number plus a noun, and that usually give the shape or configuration of something:

   L-shaped bracket, O-ring, T-shirt, U-beam, Y-coupling, V-band clamp, 3-prong connector, 180-grit abrasive cloth

4. Verbs that contain a noun or a different part of speech as the first part:

   die-cast, arc-weld, fusion-bond, stop-drill, vacuum-pack, heat-treat, jump-start, air-condition, short-circuit, fast-forward, cold-roll, dry-clean, blow-dry

5. Terms in which the end of the prefix is a vowel, and the root word starts with a vowel:

   pre-amplifier, de-icing, anti-icing, pre-engage

A hyphen is different from a dash, which divides ideas, shows a range, or gives a signal for a pause. A dash is usually longer than a hyphen, but it is at times shown as a hyphen with a space on each side.

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** Rule 1.11 — Do Not Use Different Technical Nouns for the Same Item
> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category
> **See also:** Rule 1.9 — When You Must Select a Technical Noun, Use One Which Is Short and Easy to Understand
> **See also:** Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon (;)
> **See also:** Rule 8.2 — Use Hyphens (-) to Connect Words That Are Directly Related

## STE-Code Adaptation

**Rule 8.2** In code documentation, use hyphens (-) to connect words that are directly related.

A hyphen (-) is a punctuation mark that connects words or parts of words. Use the hyphen for code-domain technical nouns to show that two or more words are directly related. This construction helps the reader to understand words and phrases more easily in code comments, API documentation, and README files.

The same categories of hyphenation apply to code documentation:

1. Terms that have two or more words and are adjectives before a noun:

   high-priority task, read-only file, thread-safe method, event-driven architecture, type-safe interface, run-time error, end-to-end test, point-to-point connection, server-side rendering, client-side validation, just-in-time compilation, fire-and-forget pattern

2. Two-word fractions or numbers in code documentation:

   seventy-two, one hundred and twenty-eight, three-fourths

3. Terms that contain an uppercase letter plus a noun, or a number plus a noun, and that usually give the shape or configuration of something:

   L-shaped bracket, T-shaped connector, 64-bit register, 8-byte alignment

4. Verbs that contain a noun or a different part of speech as the first part:

   dry-run, hot-reload, cold-start, hard-code, soft-delete

5. Terms in which the end of the prefix is a vowel, and the root word starts with a vowel:

   pre-initialized, re-entrant, de-allocated, anti-aliasing

A hyphen is different from a dash, which divides ideas, shows a range, or gives a signal for a pause.


> *Adapted from spec pair:* Non-STE: A value of 2 mm is acceptable. ("Acceptable" is not approved.)  |  STE: A value of 2 mm is permitted.
### Examples

> **Non-STE:** The high priority task must acquire the write lock before it can modify the shared data structure.
>
> **STE:** The high-priority task must get the write lock before it can change the shared data structure.
>
> *Principles applied: P1, P2, P3. "High-priority" is a compound adjective before the noun "task." Added hyphen to show direct relationship. Replaced "acquire" with "get" and "modify" with "change" per STE vocabulary.*

> **Non-STE:** Use a read only file descriptor to open the configuration for parsing.
>
> **STE:** Use a read-only file descriptor to open the configuration for parsing.
>
> *Principles applied: P1, P2. "Read-only" is a compound adjective before the noun "file descriptor." Hyphen connects the words to prevent ambiguity about what "only" modifies.*

## Code-Domain Explanation

Rule 8.2 applies differently across code documentation formats. The hyphen signals to the reader that two or more words function as a single concept. In code documentation, missing hyphens cause ambiguity about which word modifies which. This section explains how the rule applies to each documentation type.

### README Files

README files introduce a project to new users. Compound adjectives in README files describe the project's qualities, requirements, and behavior. Use hyphens consistently to make these descriptions immediately clear.

Common README patterns that need hyphens:

- **Quality descriptors:** production-ready, enterprise-grade, battle-tested, well-documented
- **Installation prerequisites:** pre-installed dependencies, system-level packages, network-accessible registry
- **Feature descriptions:** auto-generated documentation, multi-threaded execution, cross-platform support
- **Configuration flags:** opt-in feature, opt-out behavior, on-by-default setting

NOTE: A README section title such as "Getting Started" is a gerund phrase, not a compound adjective. Do not hyphenate it.

### API Documentation

API documentation describes function signatures, parameters, return types, and behavior contracts. Hyphens prevent ambiguity in parameter descriptions and return-value qualifiers.

Common API patterns that need hyphens:

- **Parameter constraints:** non-negative integer, null-terminated string, zero-based index
- **Return value descriptors:** read-only reference, copy-on-write handle, reference-counted pointer
- **State qualifiers:** thread-safe access, re-entrant call, idempotent operation
- **Behavior modifiers:** fail-fast strategy, best-effort delivery, least-recently-used eviction

Example: A parameter documented as "a read only reference" is ambiguous. "Read-only reference" makes clear that the reference itself is read-only, not that it references read-only data (though it may also do that).

### Docstrings

Docstrings live inside source code and describe what a function, class, or module does. Hyphens in docstrings keep descriptions compact and unambiguous.

Common docstring patterns that need hyphens:

- **Preconditions:** The input must be a well-formed JSON string. The buffer must be null-terminated.
- **Postconditions:** Returns a deep-copied instance. The output is a newline-delimited list.
- **Side effects:** This method is not thread-safe. The operation is non-blocking.
- **Complexity:** Average-case O(n log n). Worst-case O(n squared).

### Commit Messages

Commit messages are brief and benefit from hyphenated compounds that pack meaning into few words. Use hyphens to make commit subjects self-contained.

| Non-STE commit subject | STE commit subject |
|------------------------|---------------------|
| Fix race condition in thread safe cache | Fix race condition in thread-safe cache |
| Add end to end test for auth flow | Add end-to-end test for auth flow |
| Implement just in time compilation pass | Implement just-in-time compilation pass |
| Handle null terminated input in parser | Handle null-terminated input in parser |

### Error Messages

Error messages must be precise. A missing hyphen can make an error message confusing at exactly the moment the user needs clarity.

| Non-STE error message | STE error message |
|-----------------------|-------------------|
| Cannot open read only file | Cannot open read-only file |
| Expected non negative integer | Expected non-negative integer |
| Thread safe violation detected | Thread-safe violation detected |
| Buffer must be null terminated | Buffer must be null-terminated |

## Paradigm-Specific Guidance

Hyphenation conventions vary by programming paradigm because each paradigm introduces its own set of compound technical terms. Apply Rule 8.2 consistently within each paradigm's vocabulary.

### Object-Oriented (Java, C++, C#, Python classes)

Object-oriented code uses compound adjectives to describe class properties, method contracts, and design patterns.

**Key compound terms:**

- **Access and visibility:** read-only property, write-only field, package-private class, file-private extension
- **Initialization:** lazy-initialized singleton, eagerly-loaded dependency, constructor-injected service, setter-injected component
- **Design patterns:** factory-created instance, decorator-wrapped object, observer-registered handler, visitor-traversed tree
- **Threading:** thread-safe collection, lock-free algorithm, wait-free data structure, single-threaded context
- **Lifecycle:** reference-counted pointer, garbage-collected object, stack-allocated buffer, heap-allocated array

> **Non-STE:** The thread safe singleton uses lazy initialization to defer object creation until the first access.
>
> **STE:** The thread-safe singleton uses lazy initialization to defer object creation until the first access.
>
> *Principles applied: P1, P2. "Thread-safe" is a compound adjective before "singleton." The hyphen removes ambiguity: without it, "thread safe singleton" could be read as "thread" modifying "safe singleton."*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional programming emphasizes purity, immutability, and higher-order abstractions. Compound adjectives describe these properties.

**Key compound terms:**

- **Purity and side effects:** pure-function semantics, side-effect-free computation, referentially-transparent expression
- **Function types:** higher-order function, first-class continuation, partially-applied argument, curried-parameter list
- **Data structures:** persistent-data structure, copy-on-write map, structurally-shared tree
- **Evaluation:** lazily-evaluated sequence, strictly-evaluated argument, tail-recursive call, pattern-matched clause
- **Concurrency:** message-passing actor, software-transactional memory, lock-free CAS loop

> **Non-STE:** The higher order function returns a lazily evaluated sequence that is side effect free.
>
> **STE:** The higher-order function returns a lazily-evaluated sequence that is side-effect-free.
>
> *Principles applied: P1, P2, P11. Three compound adjectives in one sentence, each needing a hyphen. "Higher-order" and "side-effect-free" are multi-word compounds. Consistent hyphenation makes the sentence parse correctly on first reading.*

### Procedural (C, Go, Bash)

Procedural code deals with memory layout, pointers, and sequential control flow. Compound adjectives describe data representation and control constructs.

**Key compound terms:**

- **Memory layout:** null-terminated string, zero-initialized struct, stack-allocated array, heap-allocated buffer, page-aligned address, cache-line-aligned field
- **Pointer semantics:** pointer-to-pointer indirection, double-indirected reference, const-qualified parameter
- **Control flow:** short-circuit evaluation, early-return pattern, fall-through case, set-jmp context, computed-goto dispatch
- **I/O and files:** newline-delimited output, null-separated records, byte-order-mark prefixed, CRLF-terminated line
- **Build and linking:** statically-linked binary, dynamically-loaded library, position-independent code, link-time optimization

> **Non-STE:** The function expects a null terminated string and returns a zero initialized struct.
>
> **STE:** The function expects a null-terminated string and returns a zero-initialized struct.
>
> *Principles applied: P1, P2. Without hyphens, "null terminated string" could mean "null" modifies "terminated string" rather than "null-terminated" modifying "string." The hyphen binds "null" to "terminated" as a unit.*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative languages describe desired state. Compound adjectives qualify resources, constraints, and relationships.

**Key compound terms:**

- **SQL:** left-joined table, fully-qualified column name, auto-incremented primary key, composite-index lookup, read-committed isolation, write-ahead log, row-level lock, table-valued function
- **Terraform:** user-provided input, provider-managed resource, state-locked backend, read-only attribute, computed-only field, force-new recreation
- **Kubernetes:** cluster-scoped resource, namespace-scoped object, ready-state pod, crash-looping container, health-check endpoint, rolling-update strategy, blue-green deployment
- **Configuration:** well-formed document, schema-validated input, base64-encoded value, newline-separated list

> **Non-STE:** The left joined table uses a fully qualified column name from the user provided input.
>
> **STE:** The left-joined table uses a fully-qualified column name from the user-provided input.
>
> *Principles applied: P1, P2. Three compound adjectives in one sentence. Each pair of words functions as a single modifier before its noun. Without hyphens, the reader must pause to parse which word modifies which.*

### Systems (Rust ownership docs, C memory docs)

Systems programming documentation describes ownership, lifetimes, memory models, and hardware interaction. Precision is critical because errors in this domain cause crashes or undefined behavior.

**Key compound terms:**

- **Ownership and borrowing:** move-semantics transfer, borrow-checked reference, lifetime-annotated parameter, ownership-taking function, reference-counted smart pointer, atomically-reference-counted handle
- **Memory model:** memory-mapped I/O, copy-on-write page, zero-cost abstraction, cache-coherent domain, sequentially-consistent ordering, acquire-release semantics
- **Concurrency primitives:** lock-free stack, wait-free queue, compare-and-swap loop, spin-lock guard, read-copy-update mechanism
- **Low-level representation:** little-endian byte order, two's-complement representation, sign-extended value, bit-packed field, aligned-to-16-bytes address
- **Safety:** undefined-behavior risk, data-race condition, use-after-free bug, double-free error, dangling-pointer access

> **Non-STE:** The memory mapped file uses a copy on write page that is atomically reference counted.
>
> **STE:** The memory-mapped file uses a copy-on-write page that is atomically-reference-counted.
>
> *Principles applied: P1, P2, P11. Systems documentation has dense compound adjectives. "Memory-mapped," "copy-on-write," and "atomically-reference-counted" are each single concepts. The hyphens prevent the reader from misreading "copy on write page" as an instruction to copy something onto a write page.*

## Extended Examples

> **Non-STE:** The anti aliasing filter is applied before the pixel data enters the re entrant rendering pipeline.
>
> **STE:** The anti-aliasing filter is applied before the pixel data enters the re-entrant rendering pipeline.
>
> *Principles applied: P1, P2. Category 5 hyphenation: prefix ending in a vowel plus root starting with a vowel. "Anti-aliasing" and "re-entrant" each need a hyphen to separate the prefix from the root. Without the hyphen, the double vowel is visually confusing and slows reading.*

> **Non-STE:** The 64 bit register alignment requires an 8 byte offset for each 128 bit value.
>
> **STE:** The 64-bit register alignment requires an 8-byte offset for each 128-bit value.
>
> *Principles applied: P1, P2. Category 3 hyphenation: number plus noun giving configuration. "64-bit" functions as a single adjective modifying "register." The same pattern applies to "8-byte" and "128-bit." Without hyphens, the reader sees "64" as a standalone number rather than part of a compound modifier.*

> **Non-STE:** Run a dry run of the deployment before you hot reload the production server.
>
> **STE:** Run a dry-run of the deployment before you hot-reload the production server.
>
> *Principles applied: P1, P2, P13. Category 4 hyphenation: verbs containing a noun as the first part. "Dry-run" is a verb here (not a noun), so it needs the hyphen. "Hot-reload" follows the same pattern. Compare: "Do a dry run" (noun, no hyphen) versus "Dry-run the deployment" (verb, hyphen required).*

> **Non-STE:** The end to end test covers the entire data flow from server side rendering to client side hydration.
>
> **STE:** The end-to-end test covers the entire data flow from server-side rendering to client-side hydration.
>
> *Principles applied: P1, P2, P11. Category 1 hyphenation: multi-word compound adjectives before nouns. "End-to-end" is a three-word adjective modifying "test." "Server-side" and "client-side" are two-word adjectives modifying "rendering" and "hydration." Consistent hyphenation across all three compounds makes the sentence parse clearly.*

> **Non-STE:** This is a self contained module with a well defined interface and a fail fast error handling strategy.
>
> **STE:** This is a self-contained module with a well-defined interface and a fail-fast error-handling strategy.
>
> *Principles applied: P1, P2. Category 1 hyphenation: compound adjectives before nouns. "Self-" compounds always take a hyphen. "Well-defined" is a standard compound. "Fail-fast" and "error-handling" are code-domain compounds. Four hyphenated terms in one sentence is acceptable when each is a genuine compound adjective.*

> **Non-STE:** The just in time compiler produces machine code at run time using a fire and forget compilation strategy.
>
> **STE:** The just-in-time compiler produces machine code at run time using a fire-and-forget compilation strategy.
>
> *Principles applied: P1, P2, P11. Category 1 hyphenation: multi-word compound adjectives. "Just-in-time" is a four-word adjective before "compiler." "Fire-and-forget" is a three-word adjective before "strategy." Note: "at run time" is not hyphenated because "run time" is a noun phrase, not a compound adjective before a noun.*

## Edge Cases

### Edge Case 1: Framework and Library Names That Are Already Hyphenated

Some frameworks, libraries, and tools have hyphens in their official names. When you refer to these names in documentation, keep the hyphens as part of the proper noun. Do not add or remove hyphens from tool names.

Examples of hyphenated tool names: `create-react-app`, `server-side-rendering`, `tailwind-merge`, `eslint-plugin-react`, `github-actions`

When you use the tool name as a modifier, do not add a second hyphen:

> **Correct:** The create-react-app template includes a pre-configured webpack setup.
>
> **Incorrect:** The create-react-app-template includes a pre-configured webpack setup.

In the incorrect version, the extra hyphen makes the tool name look like "create-react" applied to "app-template." Use the official name as-is.

### Edge Case 2: When a Code Keyword Conflicts With Hyphenation

Some programming language keywords are compound words that dictionaries write without hyphens. In documentation prose, hyphenate them when they serve as compound adjectives. In code examples, reproduce the keyword exactly as the language requires.

Examples:

- **JavaScript `typeof`:** In prose: "The type-of operator returns a string." In code: `typeof x`
- **Python `nonlocal`:** In prose: "The non-local variable binding." In code: `nonlocal x`
- **SQL `FULL OUTER JOIN`:** In prose: "A full-outer-join operation." In code: `FULL OUTER JOIN`

NOTE: When a keyword appears in a code block or inline code span (backtick-delimited), reproduce it exactly as the language defines it. Apply Rule 8.2 only in narrative documentation prose outside code spans.

### Edge Case 3: Generated Code and Auto-Generated Documentation

Generated code and auto-generated documentation often come from tools that do not apply STE-Code rules. Do not manually hyphenate generated output. If you control the generator, configure it to produce hyphenated compounds. If you do not control the generator, leave the output as-is and add a NOTE in surrounding prose.

> **Non-STE generated output:** "This is a high priority read only file descriptor."
>
> **STE-Code prose surrounding it:** NOTE: The generated documentation uses unhyphenated compounds. In STE-Code, write "high-priority" and "read-only."

### Edge Case 4: Compound Terms Established Without Hyphens in a Codebase

Some compound terms become so common in a specific codebase that they are treated as single words. Examples include "codebase" itself, "filename," and "namespace." When a compound is consistently written without a hyphen across an entire project and the meaning is unambiguous, you may keep the established form.

Decision criteria for keeping an unhyphenated compound:

1. The term appears without a hyphen in the project's style guide or glossary.
2. All contributors use the unhyphenated form consistently.
3. The unhyphenated form causes no ambiguity in any documentation context.
4. The term is a single dictionary word (e.g., "filename") not a fresh compound (e.g., "threadsafe" is not yet standard).

If any of these criteria fail, apply Rule 8.2 and hyphenate.

### Edge Case 5: Hyphens in API Endpoint Names and URL Paths

API endpoint names and URL path segments follow their own conventions. Many REST APIs use hyphens in path segments (kebab-case). Document these endpoints using their exact path form. In prose that describes the endpoint, hyphenate compound adjectives normally.

Examples:

| URL path | Prose description |
|----------|-------------------|
| `/api/user-settings` | The user-settings endpoint returns the current-user profile. |
| `/api/read-only-access` | The read-only-access endpoint provides a read-only view of the data. |

In the prose description, "current-user" is a compound adjective before "profile" and takes a hyphen. "Read-only" before "view" also takes a hyphen. The endpoint name "read-only-access" keeps its hyphens because it is a proper noun.

NOTE: Do not confuse URL path hyphens with documentation prose hyphens. They serve different purposes and follow different rules. The URL path uses kebab-case for machine readability. The prose uses hyphens per Rule 8.2 for human readability.

## Cross-References

This rule interacts with several other STE-Code rules. Apply them together for consistent documentation.

### Rule 1.1 — Use Approved Words From the STE-Code Dictionary

Many hyphenated compounds contain approved words. When you form a compound adjective, each component word must be an approved STE-Code word (or a permitted technical noun under Rule 1.5). Example: "thread-safe" uses "thread" (technical noun, Rule 1.5) and "safe" (approved adjective).

### Rule 1.5 — Technical Code Nouns Are Allowed

Technical code nouns often appear as the first element in a hyphenated compound. Examples: "thread-safe," "stack-allocated," "type-safe," "cache-aligned." The technical noun is permitted under Rule 1.5. The hyphen connects it to the qualifying word.

### Rule 1.9 — Prefer Short, Clear Technical Nouns

When a hyphenated compound becomes long (three or more words before a noun), ask whether you can shorten it. Example: "least-recently-used eviction policy" could become "LRU eviction policy" after the acronym is defined. Prefer the shorter form when the audience knows the acronym.

### Rule 1.11 — One Term Per Concept

Hyphenated compounds are terms. Once you choose a hyphenated form for a concept, use that same form everywhere. Do not write "thread-safe" in one section and "thread safe" in another. Inconsistency confuses readers and undermines the purpose of Rule 8.2.

### Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon

Rule 8.2 and Rule 8.1 work together as the punctuation rules. Rule 8.1 governs sentence-level punctuation (periods, commas, colons). Rule 8.2 governs word-level punctuation (hyphens in compounds). Apply both rules in every documentation sentence. A sentence can be correctly punctuated under Rule 8.1 but still violate Rule 8.2 if a compound adjective lacks a hyphen.

### Rule 8.3 — Use Dashes Carefully and Do Not Confuse Them With Hyphens

A hyphen connects words. A dash separates ideas. Do not use a hyphen where a dash is needed, and do not use a dash where a hyphen is needed. In code documentation, an em-dash (—) sets off a parenthetical thought. A hyphen (-) joins words into a compound. See Rule 8.3 for full guidance on dashes.

## Grammar Notes

The grammar behind Rule 8.2 comes from standard English compound-adjective formation, adapted for the technical vocabulary of code documentation. This section explains the grammatical principles that justify the rule.

### Attributive vs. Predicative Position

A compound adjective takes a hyphen when it appears **before** the noun it modifies (attributive position). The same compound usually does not take a hyphen when it appears **after** a linking verb (predicative position).

| Attributive (hyphen) | Predicative (no hyphen) |
|----------------------|-------------------------|
| The thread-safe collection | The collection is thread safe |
| A read-only file descriptor | The file descriptor is read only |
| A well-defined interface | The interface is well defined |
| A null-terminated string | The string is null terminated |

Exception: Some compounds are always hyphenated regardless of position. These include "self-" compounds (self-contained, self-evident) and compounds where the unhyphenated form would be ambiguous.

### Adverb-Adjective Compounds: When NOT to Hyphenate

Do not hyphenate a compound when the first word is an adverb ending in "-ly." The "-ly" ending already signals that the adverb modifies the adjective, so the hyphen is unnecessary.

| Correct (no hyphen) | Incorrect (unnecessary hyphen) |
|---------------------|-------------------------------|
| a fully qualified name | a fully-qualified name |
| a dynamically allocated buffer | a dynamically-allocated buffer |
| a lazily evaluated expression | a lazily-evaluated expression |
| a statically linked library | a statically-linked library |

This rule applies because the "-ly" adverb unambiguously modifies the following adjective. The hyphen adds no clarity and is considered incorrect in standard English.

### The "Temporary Compound" Principle

In code documentation, many hyphenated compounds are "temporary compounds" — words that combine only in a specific technical context. The hyphen signals that the words form a unit for this sentence. When the same words appear separately elsewhere, they carry different meanings.

Example: "write lock" vs. "write-lock"

- "The function must acquire a write lock." — "write" is an adjective modifying "lock." No hyphen needed because "write" directly describes the type of lock.
- "The write-lock acquisition failed." — "write-lock" is a compound noun used attributively before "acquisition." The hyphen clarifies that "write-lock" is the compound concept being acquired, not that "write" modifies "lock acquisition."

Example: "run time" vs. "run-time"

- "The algorithm completes in O(n) run time." — "run time" is a noun phrase. No hyphen.
- "A run-time error occurred." — "run-time" is a compound adjective before "error." Hyphen required.

### Code Identifiers and Hyphens in Prose

When you describe a code identifier in prose, do not insert hyphens into the identifier itself. Identifiers in most languages cannot contain hyphens. Use the identifier exactly as it appears in code, and use hyphenated prose around it.

```
Incorrect: The get-user-profile function returns a user-profile object.

Correct: The `getUserProfile` function returns a user-profile object.
```

The backtick-delimited identifier `getUserProfile` is a code token, not prose. It keeps its source form (camelCase). The prose phrase "user-profile object" follows Rule 8.2 because "user-profile" is a compound adjective before "object."

### Hyphenation With Multi-Word Technical Nouns

When a technical noun is itself a multi-word phrase, and you use it as a modifier before another noun, you must decide where to place hyphens. The principle: hyphenate the entire modifying phrase as a single unit.

| Without hyphen (ambiguous) | With hyphen (clear) |
|---------------------------|---------------------|
| read only file descriptor | read-only file descriptor |
| high priority task scheduler | high-priority task scheduler |
| least recently used cache entry | least-recently-used cache entry |
| first in first out queue | first-in-first-out queue |

In "high-priority task scheduler," the hyphenated "high-priority" modifies "task scheduler" as a unit. The reader understands that it is a scheduler for high-priority tasks, not a high scheduler for priority tasks.

### The Self- Prefix Rule

Words with the prefix "self-" always take a hyphen in standard English and in STE-Code. This rule has no exceptions.

| Correct | Incorrect |
|---------|-----------|
| self-contained module | selfcontained module |
| self-documenting code | selfdocumenting code |
| self-signed certificate | selfsigned certificate |
| self-healing system | selfhealing system |

The "self-" prefix rule is a sub-rule of Rule 8.2. Apply it consistently across all documentation types.
