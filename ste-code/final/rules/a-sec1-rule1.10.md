# Rule 1.10 — Do Not Use Regional, Slang, or Jargon Words as Technical Nouns

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.10](ste-code/grouped/), Rule 1.10

## Original Rule

**Rule 1.10** Do not use regional, slang, or jargon words as technical nouns.

There can be technical words that only persons in confined regions or geographical areas use. These words are not easy to understand for persons who are from a different region or area. When you select technical nouns, always use well-known words.

This rule is also applicable to technical slang or jargon words. If only a small number of persons understand a word, it will cause confusion and non-effective communication.

Examples:

[The spec gives examples of regional and jargon terms:]

"Skid road" is a term used in some regions of North America and Canada, Northern Europe, and New Zealand. Its meaning is not immediately clear to the reader.

> **STE:** During logging operations, attach a cable to the heavy machinery to hold the logs in their position.

"Gear" is technical jargon that refers to tools and equipment, and its meaning is not immediately clear to the reader.

> **STE:** During logging operations, attach a cable to the heavy machinery to hold the logs in their position.

## STE-Code Adaptation

**Rule 1.10** Do not use regional, slang, or jargon words as code-domain technical nouns.

There can be technical words that only persons in confined communities or specific programming language ecosystems use. These words are not easy to understand for persons who are from a different background or use a different technology stack. When you select code-domain technical nouns, always use well-known words.

This rule is also applicable to technical slang or jargon words. If only a small number of persons understand a word, it will cause confusion and non-effective communication. Code documentation is read by developers with diverse backgrounds, including junior developers, developers from different language communities, and non-native English speakers.

### Examples

> **Non-STE:** Remove all the cruft from the legacy module.
>
> **STE:** Remove all the unnecessary code from the legacy module.

> *Adapted from spec example: "Gear" is technical jargon for "tools and equipment" — its meaning is not immediately clear to the reader. Just as "gear" is unclear to readers outside a specific community, "cruft" is hacker jargon that means "poorly designed or unnecessary code." Its meaning is not immediately clear to readers who are not familiar with the jargon. The STE version uses the approved words "unnecessary code," just as the spec example replaces "gear" with the clearer phrase "tools and equipment."*

> **Non-STE:** The function monkeys with the input data before validation.
>
> **STE:** The function changes the input data before validation.

> *Adapted from spec example: "Skid road" is a regional term not understood by readers from other areas. Just as "skid road" is a forestry term used only in specific regions, "monkey with" is slang used only in certain developer communities. Its meaning ("to tamper with or change in an uncontrolled way") is not clear to non-native English readers or developers from other backgrounds. The STE version uses the approved verb "change."*

> **Non-STE:** Bikeshedding delayed the API design by two weeks.
>
> **STE:** Unnecessary discussion about small details delayed the API design by two weeks.

> *Principle: P10. "Bikeshedding" is jargon from Parkinson's Law of Triviality. It means "spending disproportionate time on trivial details." Only developers familiar with the history of this term understand it. The STE version uses the approved adjective "unnecessary" with the noun "discussion."*

> **Non-STE:** I spent the morning yak shaving before I could write the test.
>
> **STE:** I spent the morning completing unrelated prerequisite tasks before I could write the test.

> *Principle: P10. "Yak shaving" is hacker jargon that describes a chain of small, seemingly unrelated tasks that must be completed before the main task. Its meaning is opaque to any reader not familiar with the Ren and Stimpy reference. The STE version describes the actual activity without metaphor.*

> **Non-STE:** Replace the foo and bar placeholders with real values.
>
> **STE:** Replace the example and placeholder values with real values.

> *Principle: P10. "Foo" and "bar" are metasyntactic variables from early hacker culture. While widely used in code examples, they have no semantic meaning and confuse readers who are not familiar with the convention. Use "example" or "placeholder" to make the purpose clear.*

> **Non-STE:** Take time to grok the authentication module before making changes.
>
> **STE:** Take time to understand the authentication module before making changes.

> *Principle: P1, P10. "Grok" is a term from Robert Heinlein's 1961 novel "Stranger in a Strange Land." It entered hacker vocabulary through early computing culture. It means "to understand deeply and intuitively." The approved verb "understand" is clear to all readers.*

### Code-Domain Explanation

This rule applies differently across documentation types. The audience and purpose of each type determine the acceptable vocabulary.

**README files:** README documents are the entry point for new users and contributors. They must use words that are clear to developers who have no prior context with the project. Avoid community-specific slang, inside jokes, and regional expressions. A README is read by a global audience.

**API documentation:** API documentation is reference material consumed by integrators who may not share the language ecosystem of the API author. Use standard terms from the STE-Code dictionary. Do not use framework-specific nicknames. Do not use slang verbs like "hit the endpoint" when "send a request to the endpoint" is clearer.

**Docstrings and inline comments:** Docstrings are embedded in source code and read by maintainers. While the audience is more technical, the same rules apply. A docstring written today may be read by a developer five years from now who does not know the slang of the current era. Avoid temporal jargon like "modern," "old-school," or "legacy" without clear definition.

**Commit messages:** Commit messages form the permanent history of a project. They are read during code reviews, blame annotations, and release notes. Slang in commit messages creates ambiguity during forensic debugging. Write commit messages as if they will be read by a developer who joined the team yesterday.

**Error messages:** Error messages are user-facing communication. They must be understood by operators, integrators, and end users who may not be developers. Slang or jargon in error messages causes support tickets and frustration. Error messages must use approved words and complete sentences.

**CLI help text and man pages:** Command-line tools often use terse, idiomatic language. Avoid regional idioms like "tweak the knobs" or "twiddle the bits." Use the approved verbs "change" and "set" instead.

### Paradigm-Specific Guidance

Different programming paradigms develop their own community vocabularies. These terms become jargon when used outside the community.

**Object-Oriented (Java, C++, C#, Python classes):** The OO community uses terms like "POJO" (Plain Old Java Object), "DTO" (Data Transfer Object), and "bean." These are acceptable as technical code nouns under Rule 1.5 because they name specific patterns. However, avoid slang derived from these terms: "POJO-ify," "bean-ize," or "DTO-ification." Use full descriptions: "convert to a plain object" instead of "POJO-ify the response."

**Functional (Haskell, Elixir, Clojure, Rust):** The FP community has a dense vocabulary of mathematical and category-theory terms. "Monad," "functor," and "applicative" are technical code nouns allowed under Rule 1.5. However, avoid informal FP slang: "point-free style" is jargon; use "tacit programming" or describe the technique. "Eta-reduce" is jargon; use "simplify the function" or describe the specific transformation.

**Procedural (C, Go, Bash):** Procedural communities use hardware-derived slang. "Bang on the bits," "twiddle the register," and "massage the buffer" are all informal. Use "change," "write to," and "adjust" instead. The C community uses "pointer gymnastics" to describe complex pointer arithmetic; use "pointer arithmetic" or describe the specific operation.

**Declarative (SQL, Terraform, Kubernetes YAML):** Declarative communities use operations slang. "Blast radius," "scream test," and "cattle not pets" are infrastructure jargon. These terms are not clear to developers from other backgrounds. Use "scope of impact," "verification by controlled outage," and "disposable resources" instead.

**Systems (Rust ownership docs, C memory docs):** Systems programming has precise technical vocabulary: "undefined behavior," "data race," "use-after-free." These are technical code nouns under Rule 1.5. However, informal extensions like "UB" (abbreviation for undefined behavior) or "UAF" (use-after-free) are jargon. Spell out the full term on first use.

### Extended Examples

Each example below shows a common code-documentation scenario where slang or jargon causes confusion. The STE version provides a clear alternative.

**Example 1: Hacker Jargon in Code Review Comments**

> **Non-STE:** This regex is a dumpster fire. Nuke it from orbit.
>
> **STE:** This regular expression is too complex and unreliable. Remove it and write a new one.

> *Principle: P10, P6. "Dumpster fire" is American slang for a complete failure. "Nuke it from orbit" is a movie reference (Aliens, 1986). Neither phrase is clear to a global audience. The STE version states the problem and the required action in approved words.*

**Example 2: Gaming Slang in Performance Documentation**

> **Non-STE:** The garbage collector is totally nerfed in v2.4.
>
> **STE:** The garbage collector has decreased performance in version 2.4.

> *Principle: P10. "Nerfed" comes from online gaming culture. It means "made weaker or less effective." A developer who does not play online games does not understand this word. The STE version uses "decreased performance," which is clear to all readers.*

**Example 3: Cultural Metaphor in Architecture Docs**

> **Non-STE:** The monolith is our Gordian knot. We need a strangle pattern.
>
> **STE:** The monolithic application has many tightly connected parts. Use a gradual replacement pattern.

> *Principle: P10. "Gordian knot" is a reference to Greek mythology. "Strangle pattern" (short for "strangler fig pattern") is a metaphor from botany. Both assume cultural and domain knowledge. The STE version describes the architecture without metaphor.*

**Example 4: Community Nickname in API Docs**

> **Non-STE:** The v2 endpoint is the shiny new hotness.
>
> **STE:** The version 2 endpoint is the current interface. Use it for all new integrations.

> *Principle: P10, P1. "Shiny new hotness" is informal English with no technical meaning. It does not tell the reader what to do or why version 2 matters. The STE version uses approved words and gives a clear instruction.*

**Example 5: Regional Idiom in Error Messages**

> **Non-STE:** The upload went pear-shaped halfway through.
>
> **STE:** The upload failed at 50 percent. Check your network connection and try again.

> *Principle: P10. "Went pear-shaped" is a British idiom meaning "went wrong." American and Asian readers may not know this expression. The STE version states the failure point precisely and gives a recovery action.*

**Example 6: Slang Verb in Commit Messages**

> **Non-STE:** Yeet the deprecated config parser.
>
> **STE:** Remove the deprecated configuration parser.

> *Principle: P10. "Yeet" is recent internet slang meaning "to discard forcefully." Its meaning is unknown to most professional developers and will age poorly. The approved verb "remove" is timeless and clear.*

### Edge Cases

The boundary between jargon and technical vocabulary is not always clear. These scenarios require judgment.

**Edge Case 1: Framework name that is also an unapproved word.** Some frameworks have names that are common English words: Rails, Spring, Django, Flask. When used as a proper noun (Ruby on Rails), these are technical code nouns under Rule 1.5. When used as a common noun ("the rails of the pipeline"), they become ambiguous. Always capitalize framework names to distinguish them from common nouns.

**Edge Case 2: Code keyword that conflicts with the rule.** Keywords like `goto`, `break`, `continue`, and `finally` have specific meanings in code. Do not use them as informal descriptions. "The function breaks before the loop" is ambiguous: "break" could mean "malfunctions" or "executes a break statement." Use "the function exits before the loop" for the colloquial meaning, and "the function executes a break statement" for the keyword meaning.

**Edge Case 3: Relaxed application for generated code.** Automatically generated documentation (Swagger/OpenAPI output, JSDoc stubs, godoc) may include auto-generated text that does not follow this rule. This is acceptable because generated documentation reflects the source code, not human-authored prose. However, any human-written descriptions within generated docs must follow this rule.

**Edge Case 4: Community-standard abbreviations.** Some abbreviations are so widely used that they transcend jargon status: "API," "JSON," "SQL," "HTML." These are technical code nouns under Rule 1.5. However, less universal abbreviations like "AFAICT" (as far as I can tell), "IIRC" (if I recall correctly), and "IMHO" (in my humble opinion) remain jargon. Spell out these phrases or omit them.

**Edge Case 5: When the jargon is the documented concept.** If you are documenting a tool named with a jargon term (for example, a build tool called "Gradle" or a linter called "ESLint"), the name itself is a technical code noun. Use the tool name as given. The rule applies to the prose around the name, not the name itself. Write "Run ESLint to check your code" not "Run ESLint to lint your junk."

### Cross-References

This rule interacts with several other STE-Code rules. Apply them together for maximum clarity.

- **Rule 1.1 (Use approved words):** Rule 1.1 provides the dictionary of approved words. When this rule requires you to replace slang or jargon, consult Rule 1.1 for the approved replacement.

- **Rule 1.5 (Technical code nouns are allowed):** Rule 1.5 defines the boundary between acceptable technical nouns and prohibited jargon. A term used by a specific framework or language is a technical code noun. A term used only by a subculture within that community is jargon.

- **Rule 1.6 (Non-approved words only as technical nouns):** Rule 1.6 reinforces that non-approved words are permitted only when they are technical code nouns. Slang and jargon are not technical code nouns and are not permitted even under Rule 1.6.

- **Rule 1.11 (One term per concept):** Rule 1.11 requires consistency. When you replace a jargon term with an approved word, use the same approved word every time. Do not use "remove" in one location and "delete" in another for the same concept.

- **Rule 1.12 (Technical verbs are allowed):** Rule 1.12 permits technical verbs like "build," "deploy," "test," and "lint." These are not slang. However, informal extensions like "buildify," "deploy-ify," or "test-athon" are slang and are not permitted.

- **Rule 1.13 (Do not use technical verbs as nouns):** Slang often converts verbs to nouns ("the build" becomes "the buildage") or nouns to verbs ("to architect"). Rule 1.13 prevents this pattern, which also helps enforce Rule 1.10.

- **Rule 1.14 (Use American English spelling):** Regional terms are prohibited by this rule. Regional spellings are also prohibited. When a term exists in both American and British English, use the American spelling: "color" not "colour," "initialize" not "initialise."

### Grammar Notes: Slang and Jargon in Code Documentation

The original ASD-STE100 spec identifies three categories of problematic words: regional terms, slang, and jargon. Each has distinct grammatical patterns that cause confusion in code documentation.

**Regional Terms:** These are words used only in specific geographical areas. In code documentation, regional terms also include vocabulary from specific technology ecosystems. A term common in the Ruby community ("gem," "rake task") may be unknown to a Python developer. The grammatical danger is that the reader may think they understand the word (its surface meaning) while missing its technical meaning entirely.

**Slang:** Slang words often originate as metaphors. "Spaghetti code," "brittle tests," and "flaky behavior" are all slang metaphors. The grammatical pattern is adjective + noun where the adjective has a non-literal meaning. These metaphors are culture-bound. "Spaghetti" as a metaphor for tangled code assumes familiarity with Italian cuisine. Replace slang metaphors with literal descriptions: "code with complex control flow," "tests that fail intermittently," "behavior that is not consistent."

**Jargon:** Jargon differs from technical vocabulary. Technical vocabulary ("polymorphism," "memoization," "serialization") has a precise, agreed-upon meaning. Jargon ("grok," "cruft," "bikeshedding") has a fuzzy, community-dependent meaning. The grammatical test is: can the term be found in a standard dictionary of computing with the same definition? If not, it is likely jargon.

**Abbreviations as Jargon:** Initialisms like "DRY" (Don't Repeat Yourself), "KISS" (Keep It Simple, Stupid), and "YAGNI" (You Aren't Gonna Need It) are jargon abbreviations. While they encode useful principles, the abbreviations themselves are not transparent. Spell out the principle on first use and use the abbreviation sparingly afterward. Better: state the principle directly without the abbreviation. "Remove duplicate code" is clearer than "Apply DRY."

**Temporal Jargon:** Words like "modern," "legacy," "cutting-edge," and "state-of-the-art" are temporal slang. They have no fixed meaning because time passes. Code described as "modern" in 2020 will not be "modern" in 2030. Describe the specific characteristic: "uses async/await syntax" instead of "uses modern patterns." Describe the specific age: "written in 2018" instead of "legacy code."

### Practical Application: Documentation Review Checklist

Use this checklist when reviewing code documentation for Rule 1.10 compliance:

1. Read the text aloud. Would a developer from a different country understand every word?
2. Identify all metaphors and idioms. Replace them with literal descriptions.
3. Identify all abbreviations. Expand them on first use.
4. Check for community-specific nicknames. Replace them with standard terms.
5. Check for temporal words ("modern," "legacy," "old"). Replace them with specific dates or characteristics.
6. Verify that every noun and verb appears in the STE-Code dictionary (Rule 1.1) or is a justified technical code noun (Rule 1.5).
7. Confirm that slang verbs are not used as technical actions. "Hit," "nuke," "yeet," "tweak," and "twiddle" are not approved verbs.

NOTE: This checklist is a guide. Professional judgment is always necessary when deciding if a term is jargon or a necessary technical noun.
