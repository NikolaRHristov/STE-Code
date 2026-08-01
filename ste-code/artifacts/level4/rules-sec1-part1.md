# Level 4 — Section 1 Rules, Part 1 (Words: 1.1–1.4, 1.10–1.14)

This sub-document holds the first part of Section 1 of STE-Code: the rules that
govern **words**. Nine rules are in this part: 1.1, 1.2, 1.3, 1.4, 1.10, 1.11,
1.12, 1.13, and 1.14. Rules 1.5 to 1.9 are in Part 2.

Use this file when you generate, review, or lint code documentation with an LLM.
Each rule below gives:

- the rule statement in one line,
- what the rule permits and forbids,
- the code-domain application per document type,
- paradigm notes where the rule behaves differently,
- worked Non-STE → STE pairs,
- edge cases, and
- the related rules.

Section 1 assumes three gates. A word is allowed when it passes at least one:

1. it is **approved in the controlled terminology** (STE-Code part 2), or
2. it is a **code-domain technical noun** (Rule 1.5, 19 categories), or
3. it is a **code-domain technical verb** (Rule 1.12, 4 categories).

A word that passes no gate must be replaced, or the sentence must be
restructured so that approved words carry the meaning.

Source for all rules in this part: adapted from ASD-STE100 Issue 9, Section 1.

---

## Rule 1.1 — Use approved words, code-domain technical nouns, or code-domain technical verbs

**Rule.** In code documentation, use words that are approved in the project
controlled terminology, or that are code-domain technical nouns, or that are
code-domain technical verbs.

The controlled terminology gives the words most frequently used in code
documentation. You may use a word that is not in the controlled terminology only
when you can put it in a technical-noun category (Rule 1.5) or a technical-verb
category (Rule 1.12). The controlled terminology also lists words that are not
approved, with the approved alternative for each.

Definitions:

- **Code-domain technical noun** — a noun term for a specified concept in
  software development, applicable to a subject field.
- **Code-domain technical verb** — a verb term for a specified operation or
  process in software development, applicable to a subject field.

Keep your technical nouns and technical verbs in a project glossary or
terminology database, and use that glossary as the source of truth.

Canonical examples:

- "run" is an approved verb in the controlled terminology.
- "UserAuthenticator" is a code-domain technical noun.
- "serialize" is a code-domain technical verb.

> **Non-STE:** Execute the script to do the task.
>
> **STE:** Run the script to do the task.

### Application by document type

**README files.** Procedural sections must start each step with an approved
imperative verb: "run" not "execute", "make" not "generate", "set" not
"configure". Descriptive sections must keep adjectives and adverbs to their
approved meanings: "large" not "substantial", "usual" not "conventional",
"correct" not "valid".

> **Non-STE:** To begin utilizing the build toolchain, you must first generate
> the distributable artifact. Then, execute the compiled binary to bootstrap the
> local development service, and utilize the environment variables to configure
> the runtime behavior before you initiate the server.
>
> **STE:** Use the build tool to make the binary. Run the binary to start the
> local service. Use the environment variables to set the runtime behavior of
> the application before you start the server.
>
> *Applied: utilizing → use; generate → make; execute → run; bootstrap → start;
> configure → set; initiate → start.*

**API documentation.** Function names, parameter names, type names, and endpoint
paths are code-domain technical nouns and pass Gate 2. The prose around them must
use approved words: "get" not "retrieve" or "fetch"; "send" not "transmit";
"remove" not "delete" or "purge"; "check" not "validate" or "verify".

> **Non-STE:** `@param {number} timeout` — The duration in milliseconds the
> client shall await a response prior to terminating the connection attempt.
>
> **STE:** `@param {number} timeout` — The time in milliseconds that the client
> waits for a response before it stops the connection.

**Docstrings and inline comments.** Use "do" not "perform", "check" not
"ensure", "make" not "construct". Comment markers `NOTE:`, `WARNING:`, and
`FIXME:` are permitted (approved nouns and code-domain technical nouns).

> **Non-STE:** `"""Performs validation on the input data to ensure it conforms
> to the expected schema."""`
>
> **STE:** `"""Checks the input data against the schema. Gives `True` when the
> data is correct and `False` when the data is not correct."""`

**Commit messages.** The most constrained form. Use the approved imperative
verbs "add", "fix", "remove", "update", "set", "make", "check", "run". Do not
use "implement" (use "add" or "make") or "optimize" (use "make faster" or "make
smaller"). "refactor" is a code-domain technical verb and is permitted under
Rule 1.12.

> **Non-STE:** `feat: implement JWT authentication middleware for API routes`
> / `perf: optimize database query performance in user listing endpoint`
>
> **STE:** `feat: add JWT authentication middleware for API routes`
> / `perf: make the database query faster in the user listing endpoint`

**Error messages.** Use "cannot" not "unable to"; "incorrect" or "not correct"
not "invalid" or "malformed"; "check" not "verify"; "try again" not "retry".

> **Non-STE:** `Error: Unable to establish connection to the database. Please
> verify your credentials and retry.`
>
> **STE:** `Error: Cannot connect to the database. Check your credentials and
> try again.`

### Paradigm notes

**Object-oriented (Java, C++, C#, Python classes).** Class, method, interface,
and design-pattern names are technical nouns (Rules 1.5 and 1.6). In prose: use
"make" not "instantiate" ("constructor" as a noun is permitted); "get" not
"retrieve"; "set" not "assign"; "call" for method invocation; "send" for message
passing; "keep" not "maintain"; "is a" and "has a" for inheritance and
composition.

> **Non-STE:** The UserRepository class is responsible for persisting and
> retrieving User entities. It leverages an ORM to abstract away the underlying
> SQL queries and encapsulates all data-access logic.
>
> **STE:** The UserRepository class keeps User records in the database and gets
> User records from the database. It uses an ORM to hide the SQL queries and
> holds all data-access logic.

**Functional (Haskell, Elixir, Clojure, Rust).** "pure function", "immutable",
"monad", "closure", and "higher-order function" are technical nouns. "fold",
"reduce", "filter", "compose", and "curry" are technical verbs (Rule 1.12).
"apply" and "pure" have both an approved general sense and a technical sense;
both are valid.

> **Non-STE:** This module furnishes a collection of pure utility functions for
> transforming and combining data structures in a declarative fashion.
>
> **STE:** This module gives a set of pure utility functions for changing and
> joining data structures.

**Procedural (C, Go, Bash).** Each step starts with an approved imperative verb:
"do", "make", "check", "set", "get", "run", "start", "stop", "send", "remove",
"keep". "allocate" is not approved — use "make" or "get". "free" and
"dereference" are technical verbs. Pointer terms are technical nouns.

> **Non-STE:** Allocate a buffer of the specified size on the heap. The caller
> is responsible for deallocating the buffer when it is no longer needed.
>
> **STE:** Make a buffer of the given size on the heap. The caller must free the
> buffer when the buffer is no longer necessary.

**Declarative (SQL, Terraform, Kubernetes YAML).** SQL keywords are technical
verbs; in code blocks they are quoted text (Rule 1.5, category 10). Terraform
resource types and Kubernetes kinds are technical nouns (category 5).
"provision" is not approved — use "make" or "set up". "orchestrate" is not
approved — use "control" or "manage". "declare" and "describe" are approved.

> **Non-STE:** This module provisions an auto-scaling group with a launch
> template. It orchestrates the deployment of EC2 instances across multiple
> availability zones to ensure high availability.
>
> **STE:** This module makes an auto-scaling group with a launch template. It
> controls the deployment of EC2 instances across many availability zones to
> give high availability.

**Systems (Rust ownership, C memory management).** "own", "borrow", and "move"
are technical verbs in Rust and are permitted even though their Rust meanings
differ from standard English. "dangling pointer" and "undefined behavior" are
compound technical nouns (category 15, defects and errors).

> **Non-STE:** The borrow checker ensures that references do not outlive the
> data they refer to, preventing dangling pointers and use-after-free bugs.
>
> **STE:** The borrow checker makes sure that references do not live longer than
> the data they point to. This prevents dangling pointers and use-after-free
> defects at compile time.

### More worked pairs

| Context | Non-STE | STE | Why |
|---|---|---|---|
| API return value | Returns a promise that resolves to an array of User objects, or rejects with an ApiError. | Gives a Promise that completes with a list of User objects. If the request does not complete, the Promise gives an ApiError. | "resolve"/"reject" replaced with approved "complete" and "gives an error"; split to keep each sentence short. |
| README feature | The application leverages machine learning algorithms to analyze user behavior patterns and generate personalized recommendations in real time. | The application uses machine learning to examine user behavior and make personal recommendations immediately. | leverage → use; analyze → examine; generate → make; personalized → personal; "real time" → "immediately"; redundant nouns removed. |
| Docstring | Validates the provided configuration object against the schema and populates default values for any missing fields. | Checks the given configuration object against the schema and adds default values for all missing fields. | validate → check; provided → given; populate → add; any → all. `ValidationError` stays (technical noun). |
| User-facing error | Unable to process your request at this time. Please verify your input and try again. If the problem persists, contact support. | Cannot process your request now. Check your input and try again. If the problem continues, speak to support. | unable to → cannot; at this time → now; verify → check; persists → continues; contact → speak to. |

### Edge cases

1. **Framework name that is also an unapproved word.** A product or framework
   name is a technical noun, even when the same string is an unapproved common
   word. Keep the name as written by its owner; do not translate it.
2. **Code keyword that conflicts with the rule.** Keywords inside code blocks
   are quoted text and are never rewritten. Only the surrounding prose is
   constrained.
3. **Generated documentation.** Text produced by a generator must still pass
   the three gates; fix it at the template or at the source docstring, not by
   hand-editing generated output.
4. **Technical verb used inside a compound noun.** A compound term such as
   "build step" or "parse tree" is a technical noun, not a verb-as-noun
   violation (see Rule 1.13).
5. **Non-English words and loanwords.** Do not use a loanword when an approved
   English word carries the meaning.

**Related:** Rules 1.2, 1.3, 1.4, 1.5, 1.6, 1.12.

---

## Rule 1.2 — Use approved words only as the specified part of speech

**Rule.** In the controlled terminology, each approved word has one specified
part of speech. Use the word only as that part of speech.

Canonical cases:

- "query" is an approved **noun**, not a verb. Do not write "Query the
  database"; write "Send a query to the database".
- "static" is an approved **adjective**, not a verb. Do not write "Static the
  variable"; write "Make the variable static".
- Some words are approved as more than one part of speech. "call" is an approved
  verb and an approved noun. The position in the sentence shows the function:
  "call the function" (verb), "a function call" (noun).

When you replace a word, check that the replacement does not change the meaning.
If the meaning changes, choose a different word or restructure the sentence.

If a word you want is not in the controlled terminology:

1. Find the word in a standard English dictionary.
2. Find the best synonym that is approved in the controlled terminology.
3. Use the approved word, or build a different sentence from other approved
   words.

### Preferred approved verbs (replacement table)

Choose the shortest approved verb that keeps the meaning. Both the Microsoft
Writing Style Guide and the Google developer documentation style guide warn
against inflated verbs such as "utilize", "leverage", "commence", "terminate",
and "initiate". STE-Code follows the same advice.

| Violating form (do not use) | Part-of-speech error | Approved replacement |
|---|---|---|
| Query the database / Cache the result / Queue the job / Log the error / Index the record | Technical noun used as verb | Send a query / Keep the result in the cache / Put the job in the queue / Write the error in the log / Use the index to find the record |
| Docker the app / Git the change / Kubectl the pod / Terraform the VPC | Tool name used as verb | Use Docker / Save with Git / Use `kubectl` / Use Terraform |
| Secure the endpoint / Empty the buffer / Silent the log | Adjective used as verb | Make the endpoint secure / Make the buffer empty / Make the log silent |
| Static the variable / Ready the worker / Live the connection | Adjective used as verb | Make the variable static / Make the worker ready / Make the connection live |
| Utilize the cache / Leverage the library / Employ the service | Unapproved verb (inflated) | Use the cache / Use the library / Use the service |
| Commence the build / Initiate the transfer / Terminate the process | Unapproved verb (inflated) | Start the build / Start the transfer / Stop the process |
| Orchestrate the services / Facilitate the sync | Unapproved verb | Control the services / Help the sync |

"clear" is approved as both a verb and an adjective, so "Clear the flag" is
allowed. The `make` + adjective pattern applies only to true adjectives such as
"secure" and "empty".

### Worked pairs

> **Non-STE:** Query the database for user records.
>
> **STE:** Send a query to the database for user records.

> **Non-STE (Docker Compose comment):**
> ```yaml
> # This compose file orchestrates three services:
> # - The API server, which endpoints the HTTP traffic
> # - The worker, which queues the background jobs
> # - The database, which stores the persistent data
> ```
>
> **STE:**
> ```yaml
> # This compose file controls three services:
> # - The API server, which handles HTTP traffic at its endpoints
> # - The worker, which puts background jobs in the queue
> # - The database, which keeps the persistent data
> ```

> **Non-STE:** `# Terraform the VPC, then Kubectl the pods into the cluster.`
>
> **STE:** `# Use Terraform to make the VPC. Use `kubectl` to apply the pod
> configuration to the cluster.`

**Related:** Rules 1.1, 1.3, 1.7 (technical nouns as verbs), 1.13 (technical
verbs as nouns).

---

## Rule 1.3 — Use approved words only with their approved meanings

**Rule.** Each approved word has a specified approved meaning, which is often
narrower than its meaning in standard English. Use the word only with that
meaning.

Carried over from the specification without change:

- "follow" means "come after, go after" — use it for the sequence of steps.
- "obey" means "to do what the procedures or instructions tell you" — use it to
  tell the reader to comply.

If you need a meaning the approved word does not have, choose another approved
word or restructure the sentence.

### Decision procedure

Run every approved verb, noun, adjective, and adverb through these four steps
before you publish:

1. **Identify the part of speech** as you actually used it. (Rule 1.2 governs
   this step; Rule 1.3 depends on it, because the part of speech selects the
   meaning.)
2. **Look up the approved meaning** for that part of speech in the controlled
   terminology.
3. **Ask the only question that matters:** does the sentence use the word with
   exactly that meaning? If not, the word fails — even when the word is approved
   and the sentence reads well.
4. **Replace or restructure.** Swap in an approved word whose meaning fits, or
   rewrite so the original word carries its approved meaning.

Worked check:

> **Sentence:** The background worker runs every night.
> **Step 1:** "runs" is a verb.
> **Step 2:** The approved meaning of the verb "run" is "execute a program or
> command".
> **Step 3:** The writer means "operates on a schedule", not "executes a
> program". The meaning does not match.
> **Step 4:** Rewrite as "The background worker operates every night."

This is the difference between documentation that is merely grammatical and
documentation that is unambiguous. A reader who sees "the job runs" assumes
execution; if you meant "the job continues", the documentation is wrong even
though "run" is an approved verb.

### Worked pairs

> **Non-STE:** Follow the configuration steps to set up the server.
>
> **STE:** Obey the configuration steps to set up the server.

> **Non-STE:** Apply the configuration to provision the resources. The plan will
> create three instances and join them to the load balancer.
>
> **STE:** Apply the configuration to make the resources. The plan will create
> three instances and connect them to the load balancer.

> **Non-STE:** Set this flag to "true" to enable debug mode. When enabled, the
> server will dump verbose logs to stdout. Setting this flag impacts performance
> significantly.
>
> **STE:** Set this flag to `true` to turn on debug mode. When debug mode is on,
> the server writes detailed logs to stdout. This setting decreases performance.
> Do not turn on debug mode in production.

> **Non-STE:** We call this pattern the Repository Pattern.
>
> **STE:** We name this pattern the Repository Pattern.
> *("call" is approved with the meaning "invoke", not "give a name to".)*

> **Non-STE:** The middleware serves the cached page to the user and then
> returns.
>
> **STE:** The middleware gives the cached page to the user and then goes back.

**Related:** Rules 1.1, 1.2, 1.4.

---

## Rule 1.4 — Use only the approved forms of verbs and adjectives

**Rule.** The controlled terminology gives each approved verb with its approved
forms, and each approved adjective in its base form with the comparative and
superlative forms where those use "-er"/"-est".

### The four-form model for verbs

Entry format: `COMPILE (v), COMPILES, COMPILED, COMPILED`

| Infinitive / imperative | Simple present | Simple past | Past participle (also adjective) |
|---|---|---|---|
| (to) compile / compile | compile(s) | compiled | compiled |

1. **Form 1 — infinitive and imperative.** The form used for every procedural
   step.
2. **Form 2 — simple present.** The form used for descriptive statements.
3. **Form 3 — simple past.** Used for events that already happened, mostly in
   changelogs and log output.
4. **Form 4 — past participle.** Used as an adjective and in the passive voice.
   For regular verbs it is identical to Form 3; the terminology lists it twice
   so the writer knows both uses are approved. Irregular verbs differ ("give" →
   "given" vs. "gave"; "run" → "run" vs. "ran").

Forms that are **not** in the model: the "-ing" form, the future with "will",
the conditional with "would", and any invented inflection ("compilating",
"compilates").

### The "-ing" restriction

The "-ing" form is the most frequent violation of Rule 1.4 in code
documentation, because it can be a continuous main verb ("the server is
running"), a gerund ("the running of the server"), or a participial adjective
("the running server"). The reader cannot always tell which.

In STE-Code the "-ing" form is permitted only when it is a code-domain technical
noun ("logging", "caching", "routing", "debugging") or part of a compound
technical term. It is never a main verb. The continuous aspect adds no
information: "the server runs" and "the server is running" describe the same
state, and the simple present is shorter.

> **Non-STE:** The operator is removing the panel. / The build is compiling the
> source files.
>
> **STE:** The operator removes the panel. / The build compiles the source
> files.

### The three-form model for adjectives

Entry format: `FAST (adj) (FASTER, FASTEST)`

1. **Base form:** fast, slow, large, small, clear.
2. **Comparative form:** faster, slower, larger, smaller, clearer — compares two
   items.
3. **Superlative form:** fastest, slowest, largest, smallest, clearest —
   identifies the extreme among three or more items.

Adjectives that form the comparative and superlative with "more" and "most" (for
example, "more correct", "most correct") have no listed forms, because "more"
and "most" are themselves approved words and the combination is predictable.

### Morphology of technical nouns and verbs

- **Technical nouns** have no verb forms, so the verb constraints do not apply.
  Compounds follow standard English morphology: "pod" → "pods".
- **Technical verbs** are not listed in the controlled terminology, so their
  forms must be predictable from standard English: "deploy, deploys, deployed,
  deployed". Where the pattern is irregular, the writer must apply the correct
  standard-English form. Rule 1.4 is therefore strictest for approved words and
  looser for technical terms.

### Why the limits help

The four-form model caps a verb at four surface forms and the three-form model
caps an adjective at three. Readers from any language background learn a small,
closed set of shapes, and never meet an invented form.

**Related:** Rules 1.1, 1.2, 1.3, 1.5, 1.7, 1.12, 1.13.

---

## Rule 1.10 — Do not use regional, slang, or jargon words as code-domain technical nouns

**Rule.** Do not use regional, slang, or jargon words as code-domain technical
nouns.

Some technical words are used only inside one community or one language
ecosystem. A reader from a different background or technology stack cannot
understand them. When you select a code-domain technical noun, always use a
well-known word. The same applies to slang and jargon: when only a small number
of persons understand a word, it causes confusion and non-effective
communication.

Code documentation is read by junior developers, by developers from other
language communities, and by non-native English speakers. A word that one
subculture finds clear can be opaque to every other reader.

### Worked pairs

| Kind | Non-STE | STE |
|---|---|---|
| Hacker jargon noun | Remove all the cruft from the legacy module. | Remove all the unnecessary code from the legacy module. |
| Slang verb | The `normalize()` function monkeys with the input data before validation. | The `normalize()` function changes the input data before validation. |
| Concept jargon | Bikeshedding delayed the API design by two weeks. | Unnecessary discussion about small details delayed the API design by two weeks. |
| Metaphor jargon | I spent the morning yak shaving before I could write the test. | I spent the morning completing unrelated prerequisite tasks before I could write the test. |
| Ops metaphor | Keep these nodes as cattle, not pets. | Treat these nodes as disposable resources that you can replace at any time. |

### Three problem categories

**Regional terms.** Words used only in one geographical area, and — in the code
domain — vocabulary from one technology ecosystem. A term common in the Ruby
community ("gem", "rake task") may be unknown to a Python developer. The danger
is that the reader thinks they understand the surface meaning and misses the
technical meaning.

**Slang.** Slang is usually metaphor: "spaghetti code", "brittle tests", "flaky
behavior". The pattern is adjective + noun where the adjective is not literal,
and the metaphor is culture-bound. Replace it with a literal description: "code
with complex control flow", "tests that fail intermittently", "behavior that is
not consistent".

**Jargon.** Technical vocabulary ("polymorphism", "memoization",
"serialization") has a precise, agreed meaning. Jargon ("grok", "cruft",
"bikeshedding") has a fuzzy, community-dependent meaning. Test: can you find the
term in a standard dictionary of computing with the same definition? If not, it
is probably jargon.

**Jargon abbreviations.** "DRY", "KISS", and "YAGNI" encode useful principles
but are not transparent. State the principle directly: "Remove duplicate code"
is clearer than "Apply DRY."

**Temporal jargon.** "modern", "legacy", "cutting-edge", and "state-of-the-art"
have no fixed meaning because time passes. Give the characteristic ("uses
async/await syntax") or the date ("written in 2018") instead.

### Edge cases

1. **Framework name that is also an unapproved word.** Rails, Spring, Django,
   Flask are technical nouns when used as proper nouns. Always capitalize them so
   the reader can tell them apart from the common noun.
2. **Code keyword that conflicts with the rule.** `goto`, `break`, `continue`,
   and `finally` have exact meanings in code. "The function breaks before the
   loop" is ambiguous. Write "the function exits before the loop" for the
   colloquial meaning, and "the function executes a break statement" for the
   keyword meaning.
3. **Generated documentation.** Auto-generated text (OpenAPI output, JSDoc
   stubs, godoc) reflects source code, not authored prose, so relaxed
   application is acceptable. Human-written descriptions inside generated docs
   must obey this rule.
4. **Community-standard abbreviations.** "API", "JSON", "SQL", and "HTML" are
   technical nouns. "AFAICT", "IIRC", and "IMHO" remain jargon — spell them out
   or remove them.
5. **When the jargon is the documented item.** A tool named with a jargon term
   keeps its name (it is a technical noun). The rule constrains the prose around
   the name: "Run ESLint to check your code", not "Run ESLint to lint your junk."

### Review checklist

1. Read the text aloud. Would a developer from another country understand every
   word?
2. Find every metaphor and idiom. Replace it with a literal description.
3. Find every abbreviation. Expand it on first use.
4. Find community nicknames. Replace them with standard terms.
5. Find temporal words ("modern", "legacy", "old"). Replace them with a specific
   date or characteristic.
6. Check every noun and verb against the controlled terminology (Rule 1.1) or
   justify it as a technical noun (Rule 1.5).
7. Confirm no slang verbs describe technical actions. "hit", "nuke", "yeet",
   "tweak", and "twiddle" are not approved.

Professional judgment is still necessary when you decide whether a term is
jargon or a necessary technical noun.

**Related:** Rules 1.1, 1.5, 1.6, 1.11, 1.12, 1.13, 1.14.

---

## Rule 1.11 — Do not use different code-domain technical nouns for the same item

**Rule.** When you select a code-domain technical noun for an item, use that same
noun everywhere in the documentation. Do not use a second noun for the same item.

Changing the name of one item between sections causes confusion: the reader must
work out whether you mean the same item or a different item. **The source of
truth for the noun is the code itself** — the class, function, module, table,
resource, environment variable, or configuration key as it is defined in the
repository.

Rule 1.11 is one of the most frequently violated rules in software
documentation, because projects accumulate names from many sources: class names,
route patterns, file paths, configuration keys, table names, and the colloquial
names developers use in conversation.

### Worked pairs

**Class name.** The repository defines one class, `UserService`.

> **Non-STE:**
> 1. Initialize the UserService class to start the session manager.
> 2. Call the authenticate method on the AccountManager to verify a user.
> 3. The UserHandler returns a session token that you send in later requests.
>
> **STE:**
> 1. Initialize the UserService class to start the session manager.
> 2. Call the authenticate method on the UserService to verify a user.
> 3. The UserService returns a session token that you send in later requests.

**API endpoint.** The OpenAPI file defines the path `/api/login`.

> **Non-STE:**
> 1. Send a request to the /api/login path to get a token.
> 2. The authentication route returns a JSON Web Token that you store in the
>    browser.
> 3. Include the token from the login endpoint in all later requests.
>
> **STE:**
> 1. Send a request to the /api/login endpoint to get a token.
> 2. The /api/login endpoint returns a JSON Web Token that you store in the
>    browser.
> 3. Include the token from the /api/login endpoint in all later requests.

Apply the same discipline to every named item:

| Item type | Source of truth | One name |
|---|---|---|
| Database table | The migration or schema file | `users`, not "the user table" then "the accounts table" |
| Configuration key | `config/database.yaml` | `database.pool_size`, not "pool size setting" then "connection limit" |
| CLI command | The command definition | `mycli sync`, not "the sync command" then "the sync tool" |
| Error type | The class definition | `ValidationError`, not "validation failure" then "schema error" |
| Environment variable | `.env` or the loader | `DATABASE_URL`, not "the DB string" then "the connection URL" |
| Git branch | The branch as pushed | `release/2.1`, not "the release branch" then "the 2.1 line" |

### Edge cases

1. **Framework names that are also unapproved words.** Keep the framework's own
   spelling and capitalization as the single name.
2. **Code keywords that conflict with the canonical noun.** When the canonical
   name collides with a language keyword, keep the code name and mark it as code
   with backticks.
3. **Different canonical names in different contexts.** When the same item has a
   code name and a user-facing name (for example, a class name and a UI label),
   state the mapping once and then use one name per audience consistently.
4. **Generated documentation.** The generator inherits the code names, so the
   fix belongs in the code, not in the generated file.
5. **Renaming during refactoring.** When you rename an item, rename it in every
   document in the same change. Do not leave both names in the corpus.

### Grammar notes

- **Definite article consistency.** Once you name an item, refer to it with the
  same article pattern each time.
- **Anaphora.** Do not replace the canonical noun with a pronoun when more than
  one item is in play; repeat the noun.
- **Compound nouns.** Keep the head noun fixed. "session token" must not become
  "token session" or "auth token" elsewhere.
- **Parallel structure in lists.** Every item in a list must name its subject in
  the same shape.

**Related:** Rules 1.1, 1.5, 1.6, 1.10, and Section 3 (verbs).
