# Level 5 — Section 9: Sentence Construction & Word Usage (Rules 9.1–9.4)

This sub-document distills the four "writing-level" rules of STE-Code for use by an
LLM that generates or revises code documentation. It covers how to restructure
sentences when a word-for-word replacement fails (9.1), how to use each approved
word with its exact meaning and part of speech (9.2), why phrasal verbs are
prohibited (9.3), and why consistent terminology across a document or project is
mandatory (9.4).

These four rules sit at the top of the STE-Code writing stack. When a candidate
word is not in the controlled terminology, try a word-for-word replacement (9.2).
If no same-part-of-speech alternative keeps the meaning, restructure the sentence
(9.1). Never reach the meaning through a phrasal verb (9.3), and never vary the
term you picked (9.4).

All examples are code-domain. Code symbols (keywords, framework names, function
and variable names) are technical nouns and never change — only surrounding prose
is edited.

---

## Rule 9.1 — Restructure When a Word-for-Word Replacement Is Not Sufficient

**Core instruction.** Use a different sentence construction when you cannot replace
an unapproved word with an approved word of the same part of speech without
changing the meaning.

**When restructuring is required:**
1. You must change the grammatical structure to use the approved alternative.
2. A word-for-word replacement gives a meaningless or unclear result.
3. The approved alternative would change the meaning.
4. The word to replace is not in the controlled terminology at all.

**Procedure when a replacement fails:**
- Think about the *purpose* of the sentence, then select different words.
- Frequently you must: select different words, use a different verb form, write
  shorter sentences, remove unnecessary information, or get more detail from a
  developer.
- Keep code symbols unchanged (Rule 1.5). Only the prose around them changes.

**Code-domain examples (Non-STE → STE):**

| Non-STE | STE | Why |
|---|---|---|
| A timeout value of 5000 ms is **acceptable** for this endpoint. | A timeout value of 5000 ms is **permitted** for this endpoint. | "acceptable" not approved; "permitted" is same part of speech and keeps meaning → word-for-word replacement is enough, no restructure. |
| The stack trace in the console must be **visible** during the debugging session. | During the debugging session, **make sure that you can see** the stack trace in the console. | "visible" (adj) → "see" (verb); restructure around the agent "you." |
| **Loop** the function twice to remove null values from the array. | **Run** the function for two iterations to remove null values from the array. | "loop" not approved; "iteration" (noun) + "run" (verb) replace it; "twice" → "two" (technical). |
| Without this change, the behavior of the function can be **uncertain**. | Without this change, it is possible that the function will not behave as expected. | "uncertain" not in terminology; word-for-word fails → new sentence. |
| **Just** add a single log statement to the method. | **Only** add a single log statement to the method. | "just" → "only"; do NOT use "immediately" here (changes meaning). |

**Restructuring patterns (reuse these):**

- *Adjective → verb:* "X is visible/configurable/accessible" → "make sure that you
  can see/set/open X." Example: "The configuration panel is accessible only to
  administrators." → "Only administrators can open the configuration panel."
- *Noun → verb:* nominalizations ("retrieval", "validation", "execution") pair with
  light verbs ("perform", "carry out"). Drop the light verb: "perform the retrieval
  of X" → "get X." Example: "The service performs the validation of each request"
  → "The service checks each request."
- *Split long sentences* before a conjunction ("and", "or", "but"), a conditional
  ("if", "when"), or between cause/effect. After splitting, each sentence must
  stand alone.

**Per documentation type:**

- *README:* replace passive with active instructions; move complex detail to a
  separate doc; use bullets; drop marketing language.
  Non-STE: "This library leverages asynchronous I/O to facilitate high-throughput
  data processing." → STE: "This library uses async I/O. It can process large
  quantities of data quickly."
- *API docs:* keep parameter names unchanged (Rule 1.5); restructure the
  description around the approved word; use a different subject if the original
  subject depends on an unapproved word; split compound descriptions.
  Non-STE: "This endpoint facilitates the retrieval of user profiles." →
  STE: "This endpoint gets user profiles."
- *Docstrings/comments:* use the approved verb form even if longer; move complex
  detail out; never change a code symbol.
  Non-STE: `"""Computes the aggregate of the supplied metrics and persists them."""`
  → STE: `"""Gets the total of the metrics and saves them."""`
- *Commit messages:* imperative summary ("Add feature"); put detail in the PR.
  Non-STE: "Implemented utilization of the cached connection pool to expedite
  request handling." → STE: "Use the cached connection pool to make requests
  faster."
- *Error messages:* state what happened and what to do; keep stack traces/symbols
  unchanged.
  Non-STE: "The application encountered an unrecoverable exception while attempting
  to instantiate the connection pool." → STE: "The application cannot start the
  connection pool. Look at the log for more data."

**Paradigm-specific notes:**

- *OOP (Java/C#/C++/Python classes):* "provides an abstraction that facilitates"
  → restructure to the concrete purpose. Non-STE:
  "The `BaseRepository` class provides an abstraction that facilitates data access
  operations across multiple database backends." → STE: "The `BaseRepository`
  class lets you use the same data access methods with different databases."
- *Functional (Haskell/Elixir/Rust):* type signatures stay unchanged; "maps over"/
  "folds" are technical verbs only when naming an op — in general prose use
  "applies a function to each element."
- *Procedural (C/Go/Bash):* "deallocate" → "free" or "release"; "pipe command A to
  command B" → "send the output of command A to command B" unless "pipe" is a
  keyword in context.
- *Declarative (SQL/Terraform/K8s):* naturally passive/stative — split and use
  active: Non-STE: "This Deployment manifest orchestrates the rollout of three
  replicated Pods, ensuring high availability through automated rescheduling." →
  STE: "This Deployment makes three copies of the Pod. If a Pod stops, the system
  starts a new Pod automatically."
- *Systems (Rust ownership/C memory):* keywords (`move`, `borrow`) keep their
  technical meaning in code font; in prose, "borrow" → "get a reference to", "own"
  → "has".

**Edge cases:**

- *Framework name = English word* (Flask, Vite, Express, Tailwind): keep the name
  unchanged; never use it as a verb. "Flask your application" → "Use Flask with
  your application."
- *Keyword = approved word* (Rust `use`, `move`; `return`; `break`): code font =
  technical noun; prose = approved meaning. "You must move the value with the
  `move` keyword, then give it back from the function."
- *Generated code symbols* with unapproved words (e.g. `utilizeData()`): keep the
  symbol; describe it with approved words — "The `utilizeData()` function uses the
  data to make a report."
- *Quoted log/error text:* keep verbatim (it is data); explain it with approved
  prose.
- *Restructuring loses precision* (e.g. security audit): (1) split + clarifying
  note, (2) keep the term in code font with a glossary definition, or (3) for an
  internal expert audience keep it as a technical noun with an approved-word
  definition on first use.
- *Algorithm names* (QuickSort, Two-Phase Commit): technical nouns, keep unchanged;
  describe behavior with approved words.

---

## Rule 9.2 — Use Each Approved Word Correctly

**Core instruction.** Use each approved word with its approved meaning and its
approved part of speech. In STE-Code, an approved word usually has exactly one
approved meaning; other standard-English meanings are not approved.

**Key facts:**
- Before using a word, check the STE-Code dictionary's approved-meaning column.
- A word may be approved for one meaning only (e.g. "wear" = "become damaged by
  friction", not "have on body"). Pick a different word for the other meaning.
- A small set of words is approved as more than one part of speech — each with a
  restricted meaning (see "Multiple parts of speech" below).
- Code symbols (keywords, framework/library names, function/var names) are
  technical nouns (Rule 1.5) and exempt from this rule — but your *prose* about
  them must follow it.

**Code-domain examples (Non-STE → STE):**

| Non-STE | STE | Why |
|---|---|---|
| Execute the initialization script before you start the server. | **Run** the initialization script before you start the server. | "execute" not approved; "run" is the one approved verb for "run a program". |
| When the error count goes down, restart the service. | When the error count **decreases**, restart the service. | "goes down" (physical movement) → "decreases" (number). |
| **Log** the exception details to the output stream. | **Write** the exception details to the log. | "log" approved as noun only, not verb. |
| The config **help** shows all command-line options. | The configuration **help text** shows all command-line options. | "help" approved as verb only, not noun. |
| The recursive call **damaged** the call stack. | The recursive call **caused damage** to the call stack. | "damage" approved as noun only, not verb. |
| This configuration option **governs** whether the linter enforces the rule set. | This configuration option **sets** how the linter applies the rules. | "governs"/"enforces" not approved; restructure around "sets". |
| The `render` method leverages a virtual DOM diffing algorithm to minimize expensive DOM manipulations. | The `render` method **uses** a virtual DOM diff algorithm. This algorithm **decreases** the number of DOM changes. | "leverages"→"uses"; "minimize"→split; "expensive"→restate; "manipulations"→"changes". |

**Words approved as multiple parts of speech** (restricted meaning each):

- **build** — verb: "construct software from source" (technical verb, Rule 1.12);
  noun: "the result of a build" or "a version". Be specific: "the build output"
  not "the build" when you mean the artifact.
- **run** — verb: "start and operate software"; noun only in compounds "test run",
  "dry run". Never "do a run" — "run the tests" or "do a test run".
- **set** — verb: "put into a specified state"; noun: "a group of related items".
  Avoid "the set timeout" (looks like an adjective) → "the timeout value that you
  set".
- **check** — verb: "make sure something is correct"; noun only in compounds
  "type check", "health check", "lint check". Never "do a check" — "check" or "do a
  health check".
- **flush** — verb: "remove remaining data from a buffer"; adjective: "where one
  surface fully touches a different surface". Primary spec example.
- **free** — verb: "release"; adjective: "not restricted".
- **close** — verb: "shut"; adjective: "near" (avoid the adjective in technical
  contexts; use "nearest port").

**Per documentation type:**

- *README:* every verb an approved verb in its approved meaning ("leverage"→"use",
  "facilitate"→"help"); every concept noun approved ("functionality"→"feature",
  "capability"→"can"); "build"/"run" handled per the table above.
- *API docs:* `GET` (uppercase, HTTP method) is a technical noun; "get" (verb) is
  approved. "Send a GET request to this endpoint to get the user data." "return" is
  a verb; "the return value" is allowed (noun adjunct) but "the return of the
  function" is not.
- *Docstrings:* "do" only for general actions (else specific verb); "make" = "create"
  (not "make a call"→"call", not "make a request"→"send a request", but "make a
  copy" ok); `using` keyword in code font = technical noun, prose "use" = verb.
- *Commit messages:* imperative approved verb ("Implement feature"→"Add feature",
  "Introduce breaking change"→"Add breaking change"); "fix" verb ok, "a fix" noun
  not; "update" verb only.
- *Error messages:* "cannot" not "unable to"/"failed to"; "must" only when the user
  must act to continue (else state the state: "The file does not exist" not "The
  file must exist"); "if" for conditional action.

**Paradigm-specific notes:**

- *OOP:* `extend`/`implements`/`override`/`abstract` are keywords in code font; in
  prose use "is a child of", "uses the interface", "replaces the parent method",
  "is a base class. You cannot make an instance of it." Non-STE: "This class
  implements the `Serializable` interface." → STE: "This class uses the
  `Serializable` interface."
- *Functional:* `map`/`reduce`/`filter`/`apply` are function names (technical
  nouns); in prose use "apply the function to each element", "combine the elements
  into a single value", "remove elements that do not match", "use the function on
  the value" — never the verb forms.
- *Procedural (C/Go):* `free()`/`open()`/`close()`/`read()` are function names;
  prose: "free the memory", "open the file", "the port is available" (not "open"),
  "read the data from the buffer" (not "do a read").
- *Declarative:* `CREATE`/`SELECT`/`DROP` are SQL keywords; in prose "make a table",
  "get rows from the table", "remove the table"; `terraform apply` stays in code
  font, prose "use `terraform apply` to make the changes".
- *Systems (Rust):* `move` as technical verb ok ("when you move a value"); `borrow`
  → "get a reference to"; `drop` as technical verb ok ("the value drops when it
  goes out of scope"); `own` → "has". "ownership" is a technical noun.

**Edge cases:**

- *Framework name = unapproved word* (Express, Flask, Fresh, FastAPI): technical
  noun, keep unchanged, never as a verb. "Express your API routes" → "Use the
  `Express` framework to write your API routes."
- *Keyword = approved word* (Rust `use`, `move`; `return`; `break`): code font =
  keyword; prose = approved meaning. "Do not break the API contract" → "Do not
  change the API contract."
- *Generated code:* keep unapproved symbol names; describe with approved words. If
  public API, wrap with an approved name that calls the generated function. If you
  own the generator, template approved symbol names from the start.
- *Quoted error/log text:* keep verbatim; explain with approved prose.

**Cross-references:** Rule 1.1 (approved words), 1.2 (part of speech), 1.3 (approved
meanings), 1.4 (approved forms), 1.5 (technical nouns), 1.7 (no technical-noun
verbs), 1.12 (technical verbs), 9.1, 9.3, 9.4, and the STE-Code Dictionary (source
of truth).

---

## Rule 9.3 — Do Not Make Phrasal Verbs

**Core instruction.** When you use two words together, do not make a phrasal verb.
A phrasal verb = an approved verb + a particle/preposition whose combined meaning
differs from the parts (e.g. "put out", "give off", "carry out"). Replace it with a
single approved verb of the same meaning. Only a small number of phrasal verbs are
approved, each with a restricted meaning (see below).

**Why it matters in code docs:** phrasal verbs are ambiguous (one phrase, many
meanings), hard for non-native readers, and unsearchable ("remove" won't match
"take off" or "strip out"). One approved verb is always preferred.

**Code-domain examples (Non-STE → STE):**

| Non-STE | STE | Why |
|---|---|---|
| The compiler **puts out** a warning. | The compiler **emits** a warning. | "put out" phrasal → single verb "emit". |
| The function **gives off** an error code. | The function **returns** an error code. | "give off" phrasal → "return". |
| The cleanup task **carries out** the deallocation. | The cleanup task **does** the deallocation. | "carry out" → "do". |
| The test runner **runs through** all suites and **prints out** a report. | The test runner **executes** all suites and **prints** a report. | "run through"→"execute"; "prints out"→"prints" ("out" adds nothing). |
| The framework **sets up** the routing table. | The framework **configures** the routing table. | "set up" → "configure" (or "install"/"create" by context). |
| The middleware **looks at** headers and **filters out** fields. | The middleware **examines** headers and **removes** fields. | "look at"→"examine"; "filter out"→"remove" (note: "filter" alone is an approved verb). |
| The cleanup job **kicks in** and **clears out** sessions. | The cleanup job **starts** and **removes** sessions. | "kick in"/"clear out" informal → "start"/"remove". |
| The compiler **breaks down** the source, then **goes on** to generate IR. | The compiler **divides** the source, then **continues** to generate IR. | "break down"→"divides"; "go on"→"continues". |
| The plugin lets you **hook into** the pipeline and **tap into** the stream. | The plugin lets you **connect to** the pipeline and **subscribe to** the stream. | "hook into"/"tap into" slang → "connect"/"subscribe". |

**README / type-specific replacements:**

- README: "set up"→"configure"/"install"; "run through"→"complete"; "check out"→
  "examine"; "go through"→"read"; "pick up where you left off"→"continue"; "break
  down the architecture"→"describe the architecture".
- API docs: verb must match the operation exactly — GET "gets", POST "creates"/
  "sends"; "looks up"→"finds", "hands off"→"sends", "takes in"→"receives", "spits
  out"→"returns", "fills in"→"completes".
- Commit messages: clean up→remove/delete/tidy; fix up→correct/repair; speed
  up→accelerate/make faster; cut down→reduce; rip out/strip out→remove; wire up→
  connect; flesh out→complete/expand.
- Error messages: "could not hook up"→"could not connect"; "blew up"→"failed";
  "out of whack"→"not consistent".
- Changelogs: "did away with"→"removed"; "added back"→"restored"; "ironed out"→
  "corrected"; "phased out"→"ended".

**Paradigm-specific notes:**

- *OOP:* "sets up the state"→"initializes"; "tears down"→"releases"; "hands off
  ownership"→"transfers ownership"; "looks up the dependency"→"finds"; "wraps up
  the transaction"→"completes".
- *Functional:* "maps over"→"applies a transformation to each element"; "pipes
  through"→"sends through"; "folds down"→"combines"; "reaches out to"→"sends a
  request to".
- *Procedural:* "reach out to the API"→"send a request"; "pull down"→"get"; "go
  through each record"→"examine"; "put together"→"make". C: "free up"→"release"/
  "free"; "hands back"→"returns".
- *Declarative:* "brings up instances"→"creates"; "spins up pods"→"starts"; "tears
  down"→"removes"; "joins together"→"joins ... with".
- *Systems:* "hands off ownership"→"transfers"; "holds onto"→"keeps a reference";
  "gives up the lock"→"releases"; "carves out"→"allocates".

**Approved phrasal verbs (restricted meaning — the only ones allowed):**

| Phrasal verb | Meaning | Example |
|---|---|---|
| log in / log out | start/end an authenticated session | "The user must log in before they can access the dashboard." |
| follow up | take further action after an initial step | "Follow up the installation with the configuration step." |
| back up | make a copy for safekeeping | "Back up the database before you apply the migration." |
| roll back | return to a previous state | "Roll back the deployment if the health check fails." |

Do not use "sign in/out", "log on/off". "Back up" (two words) means only "make a
copy" — not movement or support.

**Edge cases:**

- *Framework name contains a phrasal verb* (`setuptools`, `cleanup`, `rollback`):
  the name is a technical noun — keep it. But describe its behavior with an
  approved verb: "`setuptools` configures the package metadata" (not "sets up").
- *Code keyword = phrasal component* (`break`, `continue`, `throw`, `catch`): as a
  keyword/noun or technical verb it is fine ("the `break` statement exits the
  loop"); as a phrasal verb it is not ("breaks out of the loop"→"exits the loop";
  "catches up with the stream"→"synchronizes with the stream").
- *Not every verb+preposition is a phrasal verb.* If the preposition is a normal
  prepositional phrase (location/direction/target) and the verb keeps its meaning,
  it is allowed: "runs on the server", "flows from input to output", "write the
  configuration to the file". Test: remove the preposition — if the meaning stays
  roughly the same, it is allowed; if the meaning changes completely, it is a
  phrasal verb. ("write up the report" = compose formally → not allowed.)
- *Generated docs:* fix the source doc comments (JSDoc/Sphinx/rustdoc) so the
  published output is compliant. Third-party docs you cannot edit need not be
  corrected.
- *No single verb exists:* apply Rule 9.1. "calls back the caller with the result"
  → "sends the result to the caller through a callback". "warms up"→"loads the
  data"; "flags up"→"reports"/"marks"; "churns through"→"processes".

**Cross-references:** Rule 1.1 (dictionary), 1.2 (part of speech — the particle is
not a preposition of direction), 1.4 (approved forms), 1.11 (one term per concept —
mixing "set up" and "configure" violates consistency), 1.12 (technical verbs — do
not replace "serialize" with "turn into a string"), 9.1 (escape hatch), 9.2 (each
non-phrasal word must carry its approved meaning).

---

## Rule 9.4 — Always Use a Consistent Style

**Core instruction.** When you select terminology or wording, always use a
consistent style: the same term for the same thing, the same verb for the same
action, and the same sentence structure for the same type of instruction. Variation
is a defect, not a stylistic virtue.

**Why:** every synonym forces the reader to ask "is this the same thing or a
different thing?" — a cognitive tax that causes misidentification and bugs. In code
docs this means a parameter called "retry count" in one section and "max attempts"
in another gets misconfigured at runtime.

**Three consistency domains (each maintained independently):**

1. *Lexical* — one term per concept. Audit with grep. Pick one noun for one file
   ("configuration file", never alternating with "settings file"/"config").
2. *Syntactic* — same structure for the same action. All setup steps share one
   template (imperative verb + purpose clause); do not switch to passive/conditional
   for some steps.
3. *Semantic* — same meaning across files/modules/types. If "build" = "compile and
   link" in the README, it must not mean "compile, link, and package" in CI docs.

**Per documentation type:**

- *README:* one term for the artifact ("library" not "package" mid-doc).
- *API docs:* one name for each endpoint/method/parameter; prose must match the
  schema field name (`createdAt`, not "creation date"/"timestamp").
- *Docstrings:* use the parameter name from the signature (`max_retries`, not
  "maximum attempts"/"retry limit").
- *Commit messages:* one imperative verb per change category ("Add" for new
  features — not "Introduce"/"Insert"/"Create"; "Fix" — not "Resolve"/"Correct"/
  "Patch").
- *Error messages:* the same failure mode must produce identical text every time
  (`E_CONNECT_FAIL` = "Cannot connect to the remote host" in every module).
- *CLI help:* same template for every flag ("Enables/Disables [adjective] output").

**Code-domain examples (Non-STE → STE):**

- Setup verbs: "Install the dependencies. Then fetch the source. After that set up
  the environment. Finally get the database running." → "Install the dependencies.
  Then download the source. After that set the environment variables. Finally start
  the database." (one verb per action)
- Noun across docs: README "auth package" / API "auth package" / error "auth
  module" → all "authentication library".
- API reference: "Retrieves all items" / "Use this to create" / "Gets item by ID" /
  "Removes the specified item" → all third-person singular: "Returns all items" /
  "Creates a new item" / "Returns the item with the specified ID" / "Removes the
  item with the specified ID".
- Commit log: "Add" / "Introduce" / "Insert" / "Create" → all "Add".
- Error messages: "Connection refused by peer" / "Cannot establish link to remote"
  / "Failed to connect to upstream server" → all "Cannot connect to the remote
  host".
- CLI flags: "--verbose Enable verbose output / --quiet Suppress all logging /
  --debug Turns on debug-level messages" → "--verbose Enables verbose output /
  --quiet Disables all output / --debug Enables debug output".

**Paradigm-specific notes:**

- *OOP:* reuse the base-class docstring template in every subclass; don't abbreviate
  class names inconsistently (`UserRepository`, not `UserRepo`/"user repo").
- *Functional:* one anchor phrase for pure functions ("returns a new list"); don't
  mix "produces a result"/"yields output"; keep the monad metaphor constant.
- *Procedural:* predictable I/O step pattern; same error-check phrasing for every
  `if err != nil`.
- *Declarative:* same phrasing per resource type (`aws_instance` = "a virtual machine
  in AWS EC2" everywhere); Kubernetes resource names are proper nouns — `ConfigMap`,
  `Pod`, never "config map"/"configuration map".
- *Systems:* consistency is a safety property. Rust terms "ownership"/"move"/
  "borrow"/"lifetime" are precise — never substitute synonyms ("takes possession"/
  "relinquishes control" → "takes ownership"/"moves").

**Edge cases:**

- *Framework-mandated terminology* (React "props", "hooks"): the framework is the
  authority — use its term everywhere, never translate to an STE-Code synonym.
- *Generated docs:* fix the source docstrings; don't post-process output. For
  conventional-commits changelogs, enforce an allowed-verb convention and reject
  non-standard verbs in CI.
- *Cross-project (monorepo):* per-service docs follow the service glossary;
  system-level docs define a system-wide glossary mapping each system term to its
  service-level term.
- *Multiple valid industry names* (e.g. "GitHub Actions workflow" vs "pipeline"):
  pick one, document it in the project glossary, never alternate.
- *Version renames* ("packages" ↔ "workspaces"): each version's docs use that
  version's canonical name; migration guides must state the rename explicitly.

**Canonical synonym table — pick the preferred term and use it everywhere:**

| Preferred | Do NOT alternate with |
|---|---|
| use | utilize, leverage, employ |
| start | initiate, commence, bootstrap |
| show | display, render, present |
| make | create, generate, produce |
| get | retrieve, fetch, obtain |
| set | configure, assign, establish |
| check | verify, validate, ensure |
| remove | delete, eliminate, purge |
| keep | retain, preserve, maintain |
| send | transmit, dispatch, forward |

**Cross-references:** Rule 1.1 (approved words — consistency needs one approved
term), 1.3 (approved meanings — "set" can't mean both "configure" and "collection"),
1.5 (technical nouns must also be consistent), 1.11 (one term per concept — the
lexical foundation of 9.4), 9.1 (restructure rather than introduce a synonym), 9.2
(incorrect usage in one place breaks the chain).

---

*Section 9 covers the four writing-level rules. For the controlled terminology
(dictionary A–Z), the full rule set (Sections 1–8, 10+), extensions, and the
provenance catalogue, see the other Level 5 sub-documents.*
