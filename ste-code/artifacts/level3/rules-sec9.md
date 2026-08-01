# Level 3 — Section 9: Word & Sentence Rules (9.1–9.4)

STE-Code controlled-language rules for code documentation, distilled for LLM consumption.
Covers the four "word-level fallback and quality" rules: **9.1** (restructure when a
word-for-word replacement fails), **9.2** (use each approved word with its correct meaning
and part of speech), **9.3** (do not make phrasal verbs), and **9.4** (consistent style).

All examples are code-domain. No aerospace terms. Apply these rules whenever you generate
or rewrite code documentation (READMEs, API docs, docstrings, commit messages, error
messages, generated/AI output, infra-as-code, and systems docs).

## How to use this as an LLM reference

Apply the rules in this order for every sentence you write:

1. **Rule 1.1** — Use only approved words. Look up the word in the STE-Code dictionary
   (or the synonym preferences in Rule 9.4). Try a word-for-word replacement first.
2. **Rule 9.1** — If no approved word with the same part of speech exists, or a
   word-for-word replacement changes the meaning, restructure the sentence.
3. **Rule 9.2** — After you choose or restructure, check every approved word is used with
   its approved meaning and approved part of speech.
4. **Rule 9.3** — Replace any phrasal verb (verb + particle) with a single approved verb.
5. **Rule 9.4** — Use the same term, verb, and sentence structure for the same concept
   everywhere in the document and project.

Rule 9.1 is the escape hatch when the dictionary cannot supply a direct replacement.
Rules 9.2–9.4 are the quality gates that keep the result correct, unambiguous, and
consistent.

---

# Rule 9.1 — Use a Different Sentence Construction When a Word-for-Word Replacement Is Not Sufficient

**Core rule:** When a word is not approved, first try a word-for-word replacement with an
approved alternative of the same part of speech that keeps the meaning. If that is
impossible, rewrite the sentence with a different structure that uses only approved words
and keeps the same technical meaning.

**You must restructure when:**
1. The grammatical structure must change to fit the approved alternative.
2. A word-for-word replacement gives a meaningless or unclear result.
3. The approved alternative changes the meaning.
4. The word to replace is not in the controlled terminology at all.

When no replacement works, identify the purpose of the sentence and use different words,
verb forms, shorter sentences, or drop unnecessary information to get the same result.

## Quick check before restructuring
- Same part of speech? Approved alternative exists? Meaning unchanged? → **Replace** (no restructure).
- Otherwise → **Restructure** (Rule 9.1).

## Per-document-type guidance

**README files** — first doc a developer reads; keep clear and short.
- Passive descriptions → active instructions.
- Move complex explanations to a separate doc.
- Use bullet points, not long paragraphs.
- Remove marketing language ("leverages async I/O to facilitate…") → state the fact.

> Non-STE: This library leverages asynchronous I/O to facilitate high-throughput data processing.
> STE:     This library uses async I/O. It can process large quantities of data quickly.

**API documentation** — strict structure; keep parameter names unchanged (Rule 1.5).
- Restructure the description around the approved word.
- Use a different grammatical subject if the original subject depends on an unapproved word.
- Split compound descriptions into one sentence per parameter or behavior.

> Non-STE: This endpoint facilitates the retrieval of user profiles.
> STE:     This endpoint gets user profiles.

**Docstrings / inline comments** — most constrained; short, next to code.
- Keep code symbols unchanged. Never change a symbol to match an approved word.
- Use the approved verb form even if the sentence gets longer.
- If replacement is impossible in the space, drop the sentence and link to a longer doc.

> Non-STE: """Computes the aggregate of the supplied metrics and persists them."""
> STE:     """Gets the total of the metrics and saves them."""

**Commit messages** — short summary + blank line + body.
- Imperative summary ("Add feature", not "Added feature").
- Replace unapproved verbs with approved technical verbs.
- Complex change? Write a shorter message; put details in the PR.

> Non-STE: Implemented utilization of the cached connection pool to expedite request handling.
> STE:     Use the cached connection pool to make requests faster.

**Error messages** — short, clear, actionable; appear in logs/terminals.
- Tell the user what happened and what to do.
- Remove jargon the user cannot act on.
- Use "cannot" / "do not", keep code symbols and stack traces unchanged.

> Non-STE: The application encountered an unrecoverable exception while attempting to instantiate the connection pool.
> STE:     The application cannot start the connection pool. Look at the log for more data.

**Generated code / automated output** — the generated code itself is NOT subject to the
rules. Only your description of it must comply. Keep generated symbol names unchanged
(technical nouns, Rule 1.5); describe their function with approved words.

## Paradigm-specific guidance

**Object-oriented (Java, C++, C#, Python classes)** — class/interface/method names are
technical nouns.
- "provides an abstraction that facilitates" → "lets you use the same … methods".
- "contract" / "guarantee" / "enforce" (interfaces) → restructure ("All classes that use
  this interface must have a `save` method").
- Keywords "extend" / "override" / "specialize" are technical nouns when naming the
  keyword; unapproved verbs in prose → replace.

> Non-STE: The `BaseRepository` class provides an abstraction that facilitates data access operations across multiple database backends.
> STE:     The `BaseRepository` class lets you use the same data access methods with different databases.

**Functional (Haskell, Elixir, Clojure, Rust)** — type signatures are code (unchanged).
- "maps over" / "folds" / "lifts" are technical verbs when naming an operation; in general
  description, replace ("applies a function to each element").
- Monad/functor descriptions: state the practical effect, not abstract math.

> Non-STE: This function `fmap`s the provided transformation over the `Maybe` value, yielding a new `Maybe` that encapsulates the transformed result.
> STE:     This function applies the transformation to the `Maybe` value. If it is `Just x`, the result is `Just (f x)`. If it is `Nothing`, the result is `Nothing`.

**Procedural (C, Go, Bash)** — steps, memory, system calls.
- "allocate"/"free" are technical verbs; "deallocate" is not approved → "free"/"release".
- Shell "pipe"/"redirect"/"subshell" are technical nouns when naming features; unapproved
  as general verbs ("send the output of A to B").

> Non-STE: The program allocates a buffer on the heap, then deallocates it after processing to prevent memory leaks.
> STE:     The program gets a buffer from the heap. After it uses the buffer, it releases the memory to prevent memory leaks.

**Declarative (SQL, Terraform, Kubernetes YAML)** — desired state, not procedures.
- Keep field names as technical nouns; restructure the surrounding prose.
- "orchestrates the rollout of …" → "makes three copies of the Pod. If a Pod stops, the system starts a new Pod automatically."

**Systems (Rust ownership, C memory)** — keywords as code are unchanged; in prose check
the dictionary. "borrow"→"get a reference to"; "own"→"has"/"controls"; "move" is approved
but Rust-specific ("gives"/"moves").

## Edge cases
- **Framework names that are also unapproved words** (e.g. `Flask`, `Vite`, `Tailwind`):
  technical nouns, keep unchanged; never use as a verb ("Use Flask with the service", not
  "Flask the service").
- **Code keywords that conflict with approved words** (`use`, `move`, `return`, `break`):
  code-font keyword = technical noun; prose word follows the dictionary.
- **Quoted log/error output**: keep exact; your explanation follows the rules.
- **Restructuring loses precision** (e.g. security audit): split + add an approved-word
  clarifying note, or keep the term in code font with a glossary definition, or (internal
  expert audience) keep it as a technical noun with an approved-word definition on first use.

## Grammar patterns (reuse these)
- **Adjective → verb:** "X is visible" → "make sure that you can see X". ("is accessible" →
  "you can open"; "is extensible" → "you can add to".)
- **Noun → verb:** "perform the retrieval of X" → "get X". ("the service performs the
  validation of each request" → "the service checks each request".)
- **Split long sentences** before a conjunction/conditional, or between cause→effect,
  problem→solution. After splitting, each sentence must be self-contained.
- **Remove unnecessary info:** marketing adjectives, redundant modifiers, implementation
  detail that belongs in code, historical context that belongs in a changelog.

## Cross-references
Rule 1.1 (approved words — try first), Rule 1.4 (short sentences), Rule 1.5 (technical
nouns — do not replace), Rule 1.7 (don't verb technical nouns), Rule 1.12 (technical
verbs — do not replace), Rule 3.1 (simple tenses), Rule 5.1 (length limits), Rule 6.1
(active voice), Rule 9.2 / 9.3 / 9.4 (apply after restructuring).

---

# Rule 9.2 — Use Each Approved Word Correctly

**Core rule:** Every approved word in your documentation must be used with its **correct
meaning** and its **correct part of speech** (as listed in the STE-Code dictionary). Most
approved words have exactly one approved meaning; use only that meaning. Words approved as a
noun are not automatically approved as a verb, and vice versa.

**Decision rule:** Before using a word, read its dictionary entry. If the meaning or part of
speech you need is not the approved one, do a word-for-word replacement with a different
approved word, or restructure (Rule 9.1).

## Part-of-speech traps (most common violations)

- **"log"** — noun only (the record). Not a verb. "Log the error" → "Write the error to the log."
- **"help"** — verb only (to assist). Not a noun. "The config help" → "The configuration help text."
- **"damage"** — noun only. "The call damaged the stack" → "The call caused damage to the stack."
- **"execute"** — not approved. "Execute the script" → "Run the script."
- **"flush"** — approved as BOTH verb ("remove remaining data from a buffer") and adjective
  ("one surface fully touches a different surface"): "Flush the output buffer" vs "Make sure
  the connector is flush with the port."
- **"get"** (verb, obtain) vs **`GET`** (HTTP method, technical noun). "Send a GET request to get the data."
- **"set"** — verb ("put into a state") and noun ("a group of items"). "the set timeout" is
  ambiguous → "the timeout value that you set".
- **"run"** — verb only; noun only in "test run"/"dry run". "do a run" → "run the tests".
- **"build"** — verb and noun (the result/version). Prefer "build the project" / "the build
  output" over bare "the build".
- **"check"** — verb only; noun only in "health check"/"type check". "do a check" → "check".
- **"return"** — verb ("give back"); "the return value" OK (noun adjunct), but "the return of
  the function" is not. "The function returns a User object."
- **"fix"** — verb only. "a fix for the bug" → "correct the bug".
- **"update"** — verb only. "an update to the config" → "update the config".
- **"make"** — verb "to create". Avoid light-verb phrases: "make a call"→"call"; "make a
  request"→"send a request". "make a copy of the file" is OK (new thing created).
- **"use"** — verb; don't use "using" as a preposition ("Using this method, you can…" → "Use
  this method to…"). (`using` in C# is a keyword = technical noun.)

## Per-document-type guidance

**README** — every verb/noun must be approved and used in its approved sense. "leverage"→
"use"; "facilitate"→"help"/"let you"; "functionality"→"feature"; "capability"→"can".
"Run the tests after you build the project" (not "after the build").

**API docs** — precise. "GET" (method) vs "get" (verb); "set the timeout" vs "a set of
endpoints"; "the function returns a value" not "the return of the function".

**Docstrings** — "do" only as a general main verb ("Do the setup"); for specific actions use
the specific verb ("Run the migration"). "make a call"→"call"; "make a request"→"send a
request".

**Commit messages** — imperative summary with approved verb: "Add feature" not "Implement
feature"; "Add breaking change" not "Introduce breaking change". "fix" verb OK; "a fix" noun
not. "Update the config" not "Ship an update to the config".

**Error messages** — use "cannot" not "unable to"/"failed to": "Cannot open the config file".
Use "must" only when the user must act to continue. "If the problem continues, look at the
log for more data."

## Paradigm-specific guidance

**OO (Java/C++/C#/Python)** — keywords as code font are technical nouns; in prose they are
unapproved verbs: `extend`→"is a child of"/"inherits from"; `implements`→"uses the
interface"; `override`→"replaces the parent method"; `abstract`→"base class; you cannot make
an instance".

> Non-STE: The `PaymentProcessor` abstract class implements the `TransactionHandler` interface and provides a default implementation for the `validate` method, which subclasses can override.
> STE:     The `PaymentProcessor` base class uses the `TransactionHandler` interface. It gives a default `validate` method. Child classes can replace this method.

**Functional (Haskell/Elixir/Clojure/Rust)** — function names are technical nouns; in prose
use approved verbs: "maps over"→"applies … to each element"; "reduce"→"combine the elements
into a single value"; "filter"→"remove elements that do not match"; "apply"→"use".

**Procedural (C/Go/Bash)** — `free()` is a function name (technical noun); in prose "free the
memory" (verb) or "the memory is free" (adjective). "open" (verb) not adjective "available";
"close" (verb) not adjective "near". "read" verb, not noun ("read the data" not "do a read").

> Non-STE: After you allocate memory on the heap with `malloc`, you must deallocate it with `free` when the program no longer needs it. Failing to free allocated memory causes memory leaks.
> STE:     After you get memory from the heap with `malloc`, you must free the memory with `free` when the program does not need it. If you do not free the memory, the program uses more memory over time.

**Declarative (SQL/Terraform/K8s YAML)** — SQL keywords `CREATE`/`SELECT`/`DROP` are technical
nouns; in prose "make a table", "get rows", "remove the table". `terraform apply` is a
command; "use `terraform apply` to make the changes".

> Non-STE: The `Deployment` resource creates and manages a set of replicated Pods. It ensures that the specified number of Pods are running at all times.
> STE:     The `Deployment` resource makes and controls a set of Pod copies. It makes sure that the set number of Pods runs at all times.

**Systems (Rust/C)** — keyword meanings are technical: `move` (ownership) is an approved
technical verb; `borrow`→"get a reference to"; `drop` (Rust) is an approved technical verb;
"own"→"has". Keep `&`/`borrow checker`/`ownership` as technical nouns.

## Words approved as multiple parts of speech
- **build** — verb (construct) and noun (result/version). Be specific: "the build output", not bare "the build".
- **run** — verb; noun only in "test run"/"dry run".
- **set** — verb ("put into a state") and noun ("a group of items").
- **check** — verb; noun only in "health check"/"type check"/"lint check".
- **flush** — verb and adjective (see above).

## Edge cases
- **Framework/tool names that are also unapproved words** (`Express`, `Flask`, `Fresh`,
  `FastAPI`): technical nouns, keep in code font/capitalization; never verb them ("Use the
  `Express` framework to write your API routes" not "Express your API").
- **Keywords that are also approved words** (`use`, `move`, `return`, `break`): code-font
  keyword = technical noun; prose follows the dictionary. "Do not break the API contract" →
  "Do not change the API contract" (only physical separation uses "break").
- **Generated code symbols** — keep unchanged; describe their function with approved words.
  If public API, wrap with an approved name. If you author the generator, apply the rules to
  its templates.
- **Quoted errors/logs** — keep exact; explain with approved words.

## Grammar notes
- **One meaning per word:** each approved word has one approved meaning; express other
  meanings with a different word.
- **Noun-verb boundary:** approved-verb-only words must not be used as nouns ("run"→"run the
  program", not "do a run"); approved-noun-only words must not be used as verbs ("log"→"write
  to the log", not "log the error").
- **Dictionary is the source of truth:** when unsure, look it up. After restructuring
  (Rule 9.1), re-apply Rule 9.2 to the new sentence.

## Cross-references
Rule 1.1 (approved words), 1.2 (part of speech), 1.3 (approved meanings), 1.4 (approved
verb/adjective forms), 1.5 (technical nouns exempt), 1.7 (don't verb technical nouns), 1.12
(technical verbs — use their correct technical meaning), 9.1 (restructure when no replacement),
9.3 (no phrasal verbs), 9.4 (consistent style). The STE-Code Dictionary (A–Z) is the
authoritative reference.

---

# Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs

**Core rule:** Do not combine an approved verb with a preposition/particle to make a phrasal
verb (a phrase whose meaning differs from its parts). Replace a phrasal verb with a single
approved verb that has the same meaning. Only a few phrasal verbs are explicitly approved
(see list below), and they have a restricted meaning.

**Test:** If you can remove the preposition and the sentence keeps ~the same meaning, it is a
prepositional phrase (permitted, e.g. "write the config to the file"). If removing the
preposition changes the meaning completely, it is a phrasal verb (not approved, e.g. "write
up the report" = compose formally).

## Common phrasal-verb → approved-verb replacements
- put out → emit (compiler "puts out a warning" → "emits a warning")
- give off → return (function "gives off an error code" → "returns an error code")
- carry out → do (task "carries out the deallocation" → "does the deallocation")
- set up → configure / install / create (init with params = configure; place files = install; from nothing = create)
- run through → execute / complete
- look at → examine / inspect
- filter out → remove (note: "filter" alone is an approved technical verb)
- pick out → select
- kick off / kick in → start
- break down → divide / separate / analyze
- go on → continue
- hook into / tap into → connect to / subscribe to (also slang — doubly non-compliant)
- clean up → remove / delete / tidy
- fix up → correct / repair
- speed up → accelerate / make faster
- cut down → reduce / decrease
- wire up → connect
- strip out / rip out → remove
- flesh out → complete / expand
- hand off → send / transfer
- tear down → release
- spin up → start
- bring up → create
- hold onto → keep a reference to
- give up (lock) → release
- carve out → allocate
- reach out to → send a request to

## Per-document-type guidance
**README** — one approved verb per heading/paragraph: "Set up the project" → "Install the
project"; "Run through the quickstart" → "Complete the quickstart"; "Check out the examples" →
"Examine the examples".

**API docs** — verb must match the operation exactly: "Looks up a user" → "Finds a user"; GET
"gets" not "pulls down"; POST "creates"/"sends" not "puts in".

**Docstrings** — "Runs through and picks out" → "Examines and selects"; "Sets up and kicks off"
→ "Configures and starts".

**Commit messages** — one approved verb per change category (table above). "Clean up the
endpoints" → "Remove the endpoints".

**Error messages** — "Could not hook up to the database" → "Could not connect to the
database"; "blew up" → "failed"; "out of whack … sort it out" → "not consistent … correct it".

**Changelogs** — "did away with" → "removed"; "added back" → "restored"; "ironed out" →
"corrected"; "phased out" → "ended support for".

## Paradigm-specific guidance
**OO** — "sets up the object state" → "initializes"; "tears down resources" → "releases";
"hands off ownership" → "transfers ownership"; "looks up the dependency" → "finds"; "wraps up
the transaction" → "completes".

**Functional** — "maps over and filters out" → "applies a transformation to each element and
removes"; "pipes through" → "sends through"; "folds down" → "combines into"; "reaches out to"
→ "sends a request to".

**Procedural (C/Go/Bash)** — "free up" → "release"/"free"; "hands back" → "returns"; "reach
out and pull down" → "send a request and get"; "go through and pick out" → "examine and
select"; "put together and send off" → "make and send".

**Declarative** — "brings up EC2 instances" → "creates"; "spins up pods" → "starts"; "tears
down the index" → "removes"; "joins together" → "joins … with".

**Systems (Rust/C)** — "hands off ownership" → "transfers ownership"; "holds onto the
captured variable" → "keeps a reference to"; "gives up the lock" → "releases the lock";
"carves out a region" → "allocates".

## Approved phrasal verbs (restricted meaning — use as-is)
| Phrasal verb | Restricted meaning | Example |
|---|---|---|
| log in / log out | Start/end an authenticated session | "The user must log in before they can access the dashboard." |
| follow up | Take further action after an initial step | "Follow up the installation with the configuration step." |
| back up | Make a copy for safekeeping | "Back up the database before you apply the migration." |
| roll back | Return to a previous state | "Roll back the deployment if the health check fails." |

Do not use "sign in/out", "log on/off". "back up" is approved ONLY for copies, not movement
or support.

## Edge cases
- **Framework/tool names that are phrasal verbs** (`setuptools`, `cleanup`, `rollback`): the
  name is a technical noun (keep). Describe its behavior with an approved verb
  (`setuptools`.configures…, not `sets up`).
- **Keywords that are phrasal-verb components** (`break`, `continue`, `throw`, `catch`): as
  keywords/technical verbs they are approved ("the `break` statement exits the loop"; "the
  handler catches the error"). But "breaks out of the loop" / "catches up with the stream" are
  phrasal verbs → "exits the loop" / "synchronizes with the stream".
- **Not every verb+preposition is a phrasal verb** — prepositional phrases of location/direction/
  time are permitted ("runs on the server", "flows from A to B", "write the config to the file").
- **Generated docs** — apply the rule to the source docstrings; the generator output inherits
  compliance. Third-party generated docs you cannot edit need not be corrected.
- **No single approved verb exists** — apply Rule 9.1 (rewrite the sentence): "calls back the
  caller" → "sends the result to the caller through a callback"; "warms up" → "loads the data".

## Why this matters
Phrasal verbs cause **ambiguity** (multiple meanings), **non-native comprehension difficulty**,
and **poor searchability** (a search for "remove" misses "take off"/"strip out"). The
"one word where possible" principle: prefer a single approved verb over a 2–3 word phrase.

## Cross-references
Rule 1.1 (approved words), 1.2 (part of speech — the particle is not a direction preposition),
1.4 (approved verb forms), 1.11 (one term per concept — don't alternate "set up"/"configure"),
1.12 (technical verbs: don't replace "serialize" with "turn into a string"), 9.1 (rewrite when
no single verb fits), 9.2 (each word in a non-phrasal combo must carry its approved meaning).

---

# Rule 9.4 — When You Select Terminology or Wording, Always Use a Consistent Style

**Core rule:** Use the same term for the same thing, the same verb for the same action, and
the same sentence structure for the same type of instruction — everywhere in the document and
across the project. Different wording for the same concept forces the reader to ask "is this
the same thing?" and causes confusion and bugs.

**Three consistency domains (each maintained independently):**
1. **Lexical** — one term per concept (grep-auditable). Don't alternate "configuration file" /
   "settings file" / "config".
2. **Syntactic** — same structure for the same action. All setup steps start with an imperative
   verb + purpose clause; don't switch to passive/conditional for some.
3. **Semantic** — one meaning per term across files/modules/types. If "build" = "compile and
   link" in the README, it must not mean "compile, link, and package" in CI docs.

## Per-document-type guidance
- **README** — one term for the project artifact ("library" not "library"/"package").
- **API docs** — one name per endpoint/method/parameter; prose must match the schema field name
  (`createdAt` in schema → don't call it "creation date"/"timestamp"/"created time" in prose).
- **Docstrings** — use the same term as the function signature. Param `max_retries` → don't call
  it "maximum attempts"/"retry limit" in the body.
- **Commit messages** — one imperative verb per change category ("Add" for new features; don't
  mix "Introduce"/"Insert"/"Create").
- **Error messages** — same code → same text every time (`E_CONNECT_FAIL` must say the same
  string in every module so logs are searchable).
- **CLI help** — the `--output` description must match in `--help`, man pages, docs, and errors.

## Paradigm-specific guidance
**OO** — in a class hierarchy, reuse the base-class docstring template for overridden methods
(`connect()` everywhere says "Establishes a connection to the remote host, with …"). Don't
abbreviate class names inconsistently (`UserRepository` not `UserRepo`/`the user repo`).

**Functional** — one anchor phrase for pure functions ("returns a new list"); don't say
"produces a result"/"yields output". One metaphor for `IO` ("a description of an effect" not
"a computation"/"an action").

**Procedural (C/Go/Bash)** — predictable step structure on every I/O step ("Write the buffer to
the file descriptor" not "Output the data to the fd"). Same error-check pattern for every
`if err != nil`.

**Declarative** — same phrase per resource type ("a virtual machine in AWS EC2" not
"EC2 instance"/"AWS VM"/"cloud server"). Use `ConfigMap`/`Pod` consistently; never "config map"/
"configmap"/"configuration map".

**Systems (Rust/C)** — "ownership", "borrow", "lifetime", "move" are precise terms of art; never
substitute synonyms ("The function takes ownership of the buffer. The function moves the
buffer." not "takes possession"/"relinquishes control").

## Worked examples
- **Verb consistency:** "Install the dependencies. Then download the source. After that, set the
  environment variables. Finally, start the database." (not "fetch"/"set up"/"get … running")
- **Noun consistency across README/API/error:** "authentication library" is the only term (not
  "auth"/"module"/"package").
- **API reference structure:** every endpoint description starts with a third-person singular
  verb; "retrieves"/"gets" unified to "returns".
- **Commit convention:** all new features use "Add".
- **Error consistency:** one failure mode → one message "Cannot connect to the remote host" in
  every service (searchable across logs).
- **CLI flags:** each flag uses the same template "Enables/Disables [adjective] output".

## Edge cases
- **Framework-mandated terminology** — defer to the framework: use "props" (React) everywhere,
  never "properties"/"arguments". Consistency beats STE-Code synonym preference for proper names.
- **Generated docs** — fix the source docstrings, not the generated output. For conventional-
  commit changelogs, CI must reject non-standard verbs rather than emit inconsistent text.
- **Cross-project (monorepo)** — per-service docs follow the service glossary; system-level docs
  define a system-wide glossary that maps each system term to its service-level term.
- **Multiple valid industry names** — pick one ("GitHub Actions workflow" OR "pipeline"),
  document it in the glossary, never alternate.
- **Version rename** — each version's docs use that version's canonical name; migration guides
  must state the rename explicitly.

## Grammar notes
- **Cognitive load of synonymy** — every synonym forces a "is X the same as Y?" test that steals
  attention from content.
- **Structural parallelism** — a predictable template lets the reader scan for the action verb
  and skip scaffolding.
- **Term drift** — terminology drifts under multi-author maintenance. When you add content,
  search the existing doc for the terms you plan to use and match the convention.
- **Cross-language consistency** — Python `connect()` and TypeScript `connect()` must share the
  same description template.

## Preferred synonym table (pick one, use everywhere)
use (not utilize/leverage/employ) · start (not initiate/commence/bootstrap) · show (not
display/render/present) · make (not create/generate/produce) · get (not retrieve/fetch/obtain) ·
set (not configure/assign/establish) · check (not verify/validate/ensure) · remove (not
delete/eliminate/purge) · keep (not retain/preserve/maintain) · send (not transmit/dispatch/
forward). Variation in technical documentation is a defect, not a stylistic virtue.

## Cross-references
Rule 1.1 (approved words — cannot be consistent while alternating approved/unapproved),
Rule 1.3 (approved meanings — one meaning per word), Rule 1.5 (technical nouns exempt from the
dictionary but NOT from consistency), Rule 1.11 (one term per concept — lexical foundation of
9.4), Rule 9.1 (restructure rather than introduce a synonym), Rule 9.2 (a word used incorrectly
in one place breaks the consistency chain). The canonical synonym table (spec Section 1) is the
starting point; Rule 9.4 is the discipline that sustains it.
