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
