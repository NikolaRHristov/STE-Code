# Rule 1.10 — Do Not Use Regional, Slang, or Jargon Words as Technical Nouns

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.10
> **Upstream:** ste-code/grouped/ section 1 (Rules, pages 42–59)
> **Domain:** Code documentation (README, API docs, docstrings, commit messages, error messages, CLI help)

## Original Rule

**Rule 1.10** Do not use regional, slang, or jargon words as technical nouns.

There can be technical words that only persons in confined regions or geographical areas use. These words are not easy to understand for persons who are from a different region or area. When you select technical nouns, always use well-known words.

This rule is also applicable to technical slang or jargon words. If only a small number of persons understand a word, it will cause confusion and non-effective communication.

Spec examples:

- "Skid road" is a term used in some regions of North America and Canada, Northern Europe, and New Zealand. Its meaning is not immediately clear to the reader.
- "Gear" is technical jargon that refers to tools and equipment, and its meaning is not immediately clear to the reader.

> **STE (spec):** During logging operations, attach a cable to the heavy machinery to hold the logs in their position.

## STE-Code Adaptation

**Rule 1.10** Do not use regional, slang, or jargon words as code-domain technical nouns.

There can be technical words that only persons in confined communities or specific programming-language ecosystems use. These words are not easy to understand for persons who are from a different background or use a different technology stack. When you select code-domain technical nouns, always use well-known words.

This rule also applies to technical slang or jargon. If only a small number of persons understand a word, it will cause confusion and non-effective communication. Code documentation is read by developers with diverse backgrounds: junior developers, developers from different language communities, and non-native English speakers. A docstring or commit message written today may be read five years from now by a developer who does not know the slang of the current era.

Use the approved verbs and nouns from the STE-Code dictionary (Rule 1.1) and the extension list: `use`, `start`, `stop`, `show`, `make`, `get`, `set`, `check`, `do`, `send`, `remove`, `keep`. Do not use `utilize`, `leverage`, `employ`, `commence`, `terminate`, or `initiate` when a simpler verb works.

### Code-Domain Explanation

This rule applies differently across documentation types. The audience and purpose of each type determine the acceptable vocabulary.

**README files:** README documents are the entry point for new users and contributors. They must use words that are clear to developers who have no prior context with the project. Avoid community-specific slang, inside jokes, and regional expressions. A README is read by a global audience.

**API documentation:** API documentation is reference material consumed by integrators who may not share the language ecosystem of the API author. Use standard terms from the STE-Code dictionary. Do not use framework-specific nicknames. Do not use slang verbs like "hit the endpoint" when "send a request to the endpoint" is clearer.

**Docstrings and inline comments:** Docstrings are embedded in source code and read by maintainers. While the audience is more technical, the same rules apply. A docstring written today may be read by a developer five years from now who does not know the slang of the current era. Avoid temporal jargon like "modern," "old-school," or "legacy" without clear definition.

**Commit messages:** Commit messages form the permanent history of a project. They are read during code reviews, blame annotations, and release notes. Slang in commit messages creates ambiguity during forensic debugging. Write commit messages as if they will be read by a developer who joined the team yesterday.

**Error messages:** Error messages are user-facing communication. They must be understood by operators, integrators, and end users who may not be developers. Slang or jargon in error messages causes support tickets and frustration. Error messages must use approved words and complete sentences.

**CLI help text and man pages:** Command-line tools often use terse, idiomatic language. Avoid regional idioms like "tweak the knobs" or "twiddle the bits." Use the approved verbs `change` and `set` instead.

### Paradigm-Specific Guidance

Different programming paradigms develop their own community vocabularies. These terms become jargon when used outside the community.

**Object-Oriented (Java, C++, C#, Python classes):** The OO community uses terms like "POJO" (Plain Old Java Object), "DTO" (Data Transfer Object), and "bean." These are acceptable as technical code nouns under Rule 1.5 because they name specific patterns. However, avoid slang derived from these terms: "POJO-ify," "bean-ize," or "DTO-ification." Use full descriptions: "convert to a plain object" instead of "POJO-ify the response."

**Functional (Haskell, Elixir, Clojure, Rust):** The FP community has a dense vocabulary of mathematical and category-theory terms. "Monad," "functor," and "applicative" are technical code nouns allowed under Rule 1.5. However, avoid informal FP slang: "point-free style" is jargon; use "tacit programming" or describe the technique. "Eta-reduce" is jargon; use "simplify the function" or describe the specific transformation.

**Procedural (C, Go, Bash):** Procedural communities use hardware-derived slang. "Bang on the bits," "twiddle the register," and "massage the buffer" are all informal. Use `change`, `write to`, and `adjust` instead. The C community uses "pointer gymnastics" to describe complex pointer arithmetic; use "pointer arithmetic" or describe the specific operation.

**Declarative (SQL, Terraform, Kubernetes YAML):** Declarative communities use operations slang. "Blast radius," "scream test," and "cattle not pets" are infrastructure jargon. These terms are not clear to developers from other backgrounds. Use "scope of impact," "verification by controlled outage," and "disposable resources" instead.

**Systems (Rust ownership docs, C memory docs):** Systems programming has precise technical vocabulary: "undefined behavior," "data race," "use-after-free." These are technical code nouns under Rule 1.5. However, informal extensions like "UB" (abbreviation for undefined behavior) or "UAF" (use-after-free) are jargon. Spell out the full term on first use.

### Examples

> *Adapted from spec pair:* Non-STE: "Skid road" (a regional term used in North America, Canada, Northern Europe, and New Zealand) and "gear" (jargon for tools and equipment)  |  STE: "During logging operations, attach a cable to the heavy machinery to hold the logs in their position."

**Example 1 — Hacker jargon in a README (cruft)**

> **Non-STE:**
> # README.md — Local Development
> Before you run the test suite, remove all the cruft from the legacy
> `auth` module. There is a lot of cruft in there from the 2019 OAuth
> rewrite that you can just delete.
>
> **STE:**
> # README.md — Local Development
> Before you run the test suite, remove all the unnecessary code from the
> legacy `auth` module. The module contains unnecessary code from the
> 2019 OAuth rewrite that you can delete.

> *Principle: P10. "Cruft" is hacker jargon that means "poorly designed or unnecessary code." Its meaning is not immediately clear to readers who are not familiar with the jargon. The STE version uses the approved words "unnecessary code," just as the spec example replaces "gear" with the clearer phrase "tools and equipment."*

**Example 2 — Slang verb in a docstring (monkeys with)**

> **Non-STE:**
> def normalize_request(data: dict) -> dict:
>     """Normalize the request before validation.
>
>     This function monkeys with the input data before validation to
>     make it fit the schema. It is not safe to call twice.
>     """
>     ...
>
> **STE:**
> def normalize_request(data: dict) -> dict:
>     """Normalize the request before validation.
>
>     This function changes the input data before validation to make it
>     fit the schema. Do not call this function more than once for the
>     same request.
>     """
>     ...

> *Principle: P10. "Monkey with" is slang used only in certain developer communities. Its meaning ("to tamper with or change in an uncontrolled way") is not clear to non-native English readers or developers from other backgrounds. The STE version uses the approved verb "change."*

**Example 3 — Process jargon in a commit message (bikeshedding)**

> **Non-STE:**
> git commit -m "Stop bikeshedding about the enum names; ship the API"
>
> **STE:**
> git commit -m "Remove unnecessary discussion about the enum names; release the API"

> *Principle: P10. "Bikeshedding" is jargon from Parkinson's Law of Triviality. It means "spending disproportionate time on trivial details." Only developers familiar with the history of this term understand it. The STE version uses the approved adjective "unnecessary" with the noun "discussion."*

**Example 4 — Metaphor jargon in a task comment (yak shaving)**

> **Non-STE:**
> // TODO: I spent the morning yak shaving before I could write the test.
> // First I updated the linter, then I fixed the CI cache, then the
> // docs build broke. Now I can finally add the test.
>
> **STE:**
> // TODO: I spent the morning completing unrelated prerequisite tasks
> // before I could write the test. First I updated the linter, then I
> // fixed the CI cache, then the docs build broke. Now I can add the test.

> *Principle: P10. "Yak shaving" is hacker jargon that describes a chain of small, seemingly unrelated tasks that must be completed before the main task. Its meaning is opaque to any reader not familiar with the Ren and Stimpy reference. The STE version describes the actual activity without metaphor.*

**Example 5 — Metasyntactic variables in API docs (foo and bar)**

> **Non-STE:**
> ## POST /v1/translate
> Send a request with `foo` and `bar` in the body. The server reads
> `foo` as the source text and `bar` as the target language.
>
> **STE:**
> ## POST /v1/translate
> Send a request with `text` and `language` in the body. The server
> reads `text` as the source string and `language` as the target
> language code.

> *Principle: P10. "Foo" and "bar" are metasyntactic variables from early hacker culture. While widely used in code examples, they have no semantic meaning and confuse readers who are not familiar with the convention. Use "example" or "placeholder" to make the purpose clear.*

**Example 6 — Science-fiction jargon in onboarding docs (grok)**

> **Non-STE:**
> # Contributor Guide
> Take time to grok the authentication module before you make changes.
> You will not be able to review pull requests until you grok it.
>
> **STE:**
> # Contributor Guide
> Take time to understand the authentication module before you make
> changes. You will not be able to review pull requests until you
> understand it.

> *Principle: P1, P10. "Grok" is a term from Robert Heinlein's 1961 novel "Stranger in a Strange Land." It entered hacker vocabulary through early computing culture. It means "to understand deeply and intuitively." The approved verb "understand" is clear to all readers.*

**Example 7 — Slang in a code-review comment (dumpster fire / nuke)**

> **Non-STE:**
> // PR review comment on `validate_input.py`
> This regex is a dumpster fire. Nuke it from orbit and write a new one
> that actually works.
>
> **STE:**
> // PR review comment on `validate_input.py`
> This regular expression is too complex and unreliable. Remove it and
> write a new one that passes all test cases.

> *Principle: P6, P10. "Dumpster fire" is American slang for a complete failure. "Nuke it from orbit" is a movie reference (Aliens, 1986). Neither phrase is clear to a global audience. The STE version states the problem and the required action in approved words.*

**Example 8 — Gaming slang in performance docs (nerfed)**

> **Non-STE:**
> # CHANGELOG.md
> ## Version 2.4
> The garbage collector is totally nerfed in v2.4. Large batch jobs now
> take twice as long to finish.
>
> **STE:**
> # CHANGELOG.md
> ## Version 2.4
> The garbage collector has decreased performance in version 2.4. Large
> batch jobs now take twice as long to finish.

> *Principle: P10. "Nerfed" comes from online gaming culture. It means "made weaker or less effective." A developer who does not play online games does not understand this word. The STE version uses "decreased performance," which is clear to all readers.*

**Example 9 — Cultural metaphor in architecture docs (Gordian knot / strangle pattern)**

> **Non-STE:**
> # Architecture Decision Record 14
> The monolith is our Gordian knot. We need a strangle pattern to cut
> the dependency tangle before we can scale.
>
> **STE:**
> # Architecture Decision Record 14
> The monolithic application has many tightly connected parts. Use a
> gradual replacement pattern to reduce the dependencies before we can
> scale.

> *Principle: P10. "Gordian knot" is a reference to Greek mythology. "Strangle pattern" (short for "strangler fig pattern") is a metaphor from botany. Both assume cultural and domain knowledge. The STE version describes the architecture without metaphor.*

**Example 10 — Community nickname in API docs (shiny new hotness)**

> **Non-STE:**
> ## Migration Guide
> The v2 endpoint is the shiny new hotness. You should probably move
> your integrations over soon-ish.
>
> **STE:**
> ## Migration Guide
> The version 2 endpoint is the current interface. Use it for all new
> integrations. Version 1 stops receiving updates on 2027-01-01.

> *Principle: P1, P10. "Shiny new hotness" is informal English with no technical meaning. It does not tell the reader what to do or why version 2 matters. The STE version uses approved words and gives a clear instruction with a date.*

**Example 11 — Regional idiom in an error message (went pear-shaped)**

> **Non-STE:**
> ERROR: the upload went pear-shaped halfway through, sorry m8
>
> **STE:**
> ERROR: The upload failed at 50 percent. Check your network connection
> and try the upload again.

> *Principle: P10. "Went pear-shaped" is a British idiom meaning "went wrong." American and Asian readers may not know this expression. The STE version states the failure point precisely and gives a recovery action.*

**Example 12 — Internet slang in a commit message (yeet)**

> **Non-STE:**
> git commit -m "yeet the deprecated config parser, we don't need it"
>
> **STE:**
> git commit -m "remove the deprecated configuration parser"

> *Principle: P10. "Yeet" is recent internet slang meaning "to discard forcefully." Its meaning is unknown to most professional developers and will age poorly. The approved verb "remove" is timeless and clear.*

**Example 13 — Slang verb in API documentation (hit the endpoint)**

> **Non-STE:**
> ## Quickstart
> To get a user, just hit the `/users/{id}` endpoint with a GET. You can
> also hit it with a POST to make a new user.
>
> **STE:**
> ## Quickstart
> To get a user, send a GET request to the `/users/{id}` endpoint. You
> can also send a POST request to the same endpoint to create a user.

> *Principle: P1, P10. "Hit" as a verb for "send a request" is regional slang in developer speech. The approved verb "send" with the noun "request" is clear to integrators from any language background.*

**Example 14 — Regional idiom in CLI help (tweak the knobs / twiddle the bits)**

> **Non-STE:**
> $ mytool --help
>   --tune    tweak the knobs until it feels right
>   --raw     twiddle the bits directly if you know what you're doing
>
> **STE:**
> $ mytool --help
>   --tune    change the configuration values to adjust performance
>   --raw     change the byte values directly if you know the format

> *Principle: P10. "Tweak the knobs" and "twiddle the bits" are regional idioms. Use the approved verbs "change" and "adjust" instead.*

**Example 15 — OO slang verb in a refactor note (POJO-ify)**

> **Non-STE:**
> // We should POJO-ify the response so the frontend stops choking on it.
>
> **STE:**
> // Convert the response to a plain object so the frontend can read it.

> *Principle: P5, P10. "POJO-ify" is slang derived from the technical noun "POJO." The term names a specific pattern (allowed under Rule 1.5), but the slang verb is not approved. Describe the operation directly.*

**Example 16 — FP slang in a code comment (point-free / eta-reduce)**

> **Non-STE:**
> -- refactor: make this point-free and eta-reduce the wrapper
>
> **STE:**
> -- refactor: write this in tacit style and remove the redundant
> -- function wrapper

> *Principle: P5, P10. "Point-free" and "eta-reduce" are community slang. Use "tacit programming" or describe the transformation: "remove the redundant function wrapper."*

**Example 17 — Systems abbreviation in docs (UB / UAF)**

> **Non-STE:**
> // If you call free twice, you get UB, and a double UAF is undefined.
>
> **STE:**
> // If you call free twice, the behavior is undefined, and a second
> // use-after-free access is also undefined behavior.

> *Principle: P5, P10. "UB" and "UAF" are informal abbreviations of "undefined behavior" and "use-after-free." Spell out the full term on first use so the reader does not need prior community knowledge.*

**Example 18 — Principle abbreviation in a docstring (DRY / KISS / YAGNI)**

> **Non-STE:**
> def cache_user(user):
>     """Cache the user. DRY — don't repeat the lookup. KISS. YAGNI."""
>     ...
>
> **STE:**
> def cache_user(user):
>     """Store the user in the cache so the lookup runs once per request.
>
>     Do not repeat the database lookup in each function that needs the
>     user. Do not add features that the current callers do not use.
>     """
>     ...

> *Principle: P10. "DRY," "KISS," and "YAGNI" are jargon abbreviations. Spell out the principle on first use, or state it directly: "remove duplicate code," "keep the design simple," "do not add unused features."*

**Example 19 — Temporal jargon in a README (modern / legacy)**

> **Non-STE:**
> # README.md
> This service uses a modern event-driven architecture. The legacy
> REST layer is old-school and should be replaced.
>
> **STE:**
> # README.md
> This service uses an event-driven architecture with a message queue
> (added in 2024). The REST layer was written in 2019 and we plan to
> replace it in the next release.

> *Principle: P1, P10. "Modern," "legacy," and "old-school" are temporal slang with no fixed meaning because time passes. Describe the specific characteristic or date instead.*

**Example 20 — Framework name confused with a common noun (Edge Case 1)**

> **Non-STE:**
> The rails of the pipeline route each request to the correct handler.
>
> **STE:**
> The Ruby on Rails application routes each request to the correct
> handler through the pipeline.

> *Edge Case 1: Framework name that is also an unapproved word. Some frameworks have names that are common English words: Rails, Spring, Django, Flask. When used as a proper noun (Ruby on Rails), these are technical code nouns under Rule 1.5. When used as a common noun ("the rails of the pipeline"), they become ambiguous. Always capitalize framework names to distinguish them from common nouns.*

**Example 21 — Code keyword used as informal description (Edge Case 2)**

> **Non-STE:**
> The function breaks before the loop finishes, so the data is partial.
>
> **STE:**
> The function exits before the loop finishes, so the data is partial.

> *Edge Case 2: Code keyword that conflicts with the rule. Keywords like `goto`, `break`, `continue`, and `finally` have specific meanings in code. Do not use them as informal descriptions. "The function breaks" is ambiguous: "break" could mean "malfunctions" or "executes a break statement." Use "the function exits" for the colloquial meaning, and "the function executes a break statement" for the keyword meaning.*

**Example 22 — Community-standard abbreviation is a technical noun (Edge Case 4)**

> **Non-STE:**
> AFAICT the JSON payload is valid, but IIRC the API used to return XML.
>
> **STE:**
> The JSON payload appears valid based on the schema, and the API
> returned XML in previous versions.

> *Edge Case 4: Community-standard abbreviations. "API," "JSON," "SQL," and "HTML" are technical code nouns under Rule 1.5. However, less universal abbreviations like "AFAICT" (as far as I can tell), "IIRC" (if I recall correctly), and "IMHO" (in my humble opinion) remain jargon. Spell out these phrases or omit them.*

**Example 23 — Jargon that is the documented tool name (Edge Case 5)**

> **Non-STE:**
> Run ESLint to lint your junk before you push.
>
> **STE:**
> Run ESLint to check your code before you push.

> *Edge Case 5: When the jargon is the documented concept. If you document a tool named with a jargon term (a build tool called "Gradle" or a linter called "ESLint"), the name itself is a technical code noun. Use the tool name as given. The rule applies to the prose around the name, not the name itself.*

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

> **See also:** Rule 1.1 — Use approved words from the STE-Code dictionary
> **See also:** Rule 1.5 — Technical code nouns are allowed
> **See also:** Rule 1.6 — Non-approved words are permitted only as technical nouns
> **See also:** Rule 1.11 — Use one term for one concept
> **See also:** Rule 1.12 — Technical verbs are allowed
> **See also:** Rule 1.13 — Do not use technical verbs as nouns
> **See also:** Rule 1.14 — Use American English spelling