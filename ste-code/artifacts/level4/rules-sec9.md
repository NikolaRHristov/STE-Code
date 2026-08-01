# Level 4 — Section 9: Sentence Construction, Correct Word Use, Phrasal Verbs, Consistency

This sub-document distills **Section 9** of the STE-Code standard for use by
LLMs that generate, review, or rewrite code documentation. It covers the four
"fallback and quality" rules that apply *after* the dictionary (Rule 1.1) has
been consulted:

- **Rule 9.1** — When a word-for-word replacement is not enough, rebuild the sentence.
- **Rule 9.2** — Use every approved word with its approved meaning and part of speech.
- **Rule 9.3** — Do not combine approved words into phrasal verbs.
- **Rule 9.4** — Use one term and one construction for each concept, everywhere.

These rules are the repair and quality layer. Rule 1.1 says *which* words are
allowed; Section 9 says *how* to use them and what to do when a single word
will not fit.

## Quick reference

| Rule | One-line directive | Trigger |
|------|--------------------|---------|
| 9.1 | Rebuild the sentence when no approved word fits by replacement. | Word-for-word swap fails or changes meaning. |
| 9.2 | Every approved word keeps its one approved meaning + part of speech. | A word is used in a meaning/role not in the dictionary. |
| 9.3 | Replace verb+particle pairs with one approved verb. | A phrasal verb (new meaning from two approved words) appears. |
| 9.4 | Same concept = same term, same verb, same structure, everywhere. | You find synonyms or shifting phrasing for one thing. |

## Rule 9.1 — Rebuild the Sentence When a Word-for-Word Replacement Is Not Sufficient

**Source:** ASD-STE100 Issue 9, Rule 9.1 (code-domain adaptation).

### What it says

The dictionary gives approved alternatives for unapproved words. If an
alternative has the **same part of speech** and **does not change the meaning**,
do a word-for-word replacement. If any of these fail, you must write a new
sentence with a different structure that uses only approved words and keeps the
same technical meaning.

A different construction is required when:

1. You must change the grammar to use the approved alternative.
2. A word-for-word swap gives a meaningless or unclear result.
3. The approved alternative changes the meaning.
4. The word to replace is not in the controlled terminology.

### How to rebuild (the decision order)

1. Try a word-for-word replacement with the same part of speech. If it works and keeps the meaning, stop.
2. If it fails, think about *what the sentence is trying to say* and restructure:
   - select different words,
   - use different verb forms (simple present / past / imperative),
   - write shorter sentences,
   - drop information that is not necessary,
   - or get more detail from a developer when the meaning is unclear.

### Worked examples

| Non-STE | STE | Why a rebuild was needed |
|---------|-----|--------------------------|
| A timeout value of 5000 ms is **acceptable** for this endpoint. | A timeout value of 5000 ms is **permitted** for this endpoint. | No rebuild: "acceptable" → approved "permitted", same part of speech, same meaning. |
| The stack trace in the console **must be visible** during the debugging session. | **During the debugging session, make sure that you can see** the stack trace in the console. | Adjective "visible" → verb "see"; restructure around the agent "you". |
| **Loop** the function twice to remove null values from the array. | **Run** the function for two **iterations** to remove null values from the array. | "Loop" not approved; "iterate"/"run" + "iteration" + "two" replace it. |
| Without this change, the behavior **can be uncertain**. | Without this change, **it is possible that** the function **will not behave as expected**. | "Uncertain" not in terminology; word-for-word swap is meaningless, so rebuild. |
| **Just** add a single log statement to the method. | **Only** add a single log statement to the method. (NOT: "Immediately…") | "Just"→"Only"; "Immediately" is the approved alternative but changes the instruction's meaning. |
| The **occurrence** of type errors in the build output is a serious problem. | **Type errors** in the build output are a serious problem. | "Occurrence" not approved; drop the nominalization. |

### Per documentation-type guidance

- **README files** — replace passive with active instructions; move complex explanation to a separate doc; use bullets; drop marketing language.
  - Non-STE: *This library leverages asynchronous I/O to facilitate high-throughput data processing.*
  - STE: *This library uses async I/O. It can process large quantities of data quickly.*
- **API docs** — keep parameter/field names unchanged (Rule 1.5); restructure the description around the approved word; split compound descriptions.
  - Non-STE: *This endpoint facilitates the retrieval of user profiles.*
  - STE: *This endpoint gets user profiles.*
- **Docstrings / inline comments** — keep code symbols; if no replacement fits in the space, replace the sentence with a reference to a longer doc.
  - Non-STE: *"Computes the aggregate of the supplied metrics and persists them."*
  - STE: *"Gets the total of the metrics and saves them."*
- **Commit messages** — use imperative summary ("Add feature"); replace unapproved verbs; keep details in the PR, not the body.
  - Non-STE: *Implemented utilization of the cached connection pool to expedite request handling.*
  - STE: *Use the cached connection pool to make requests faster.*
- **Error messages** — tell the user what happened and what to do; use "cannot" / "do not"; keep code symbols.
  - Non-STE: *The application encountered an unrecoverable exception while attempting to instantiate the connection pool.*
  - STE: *The application cannot start the connection pool. Look at the log for more data.*

### Paradigm-specific patterns

- **OO (Java/C#/C++/Python):** "provides an abstraction that facilitates" → state the concrete purpose. *The `BaseRepository` class lets you use the same data access methods with different databases.*
- **Functional (Haskell/Rust):** type signatures are code (keep); "maps over" → "applies a function to each element"; monad descriptions → "lets you chain operations that can fail".
- **Procedural (C/Go/Bash):** "deallocate" → "free"/"release"; "pipe command A to command B" → "send the output of command A to command B" when "pipe" is prose.
- **Declarative (SQL/Terraform/K8s):** keep field names; "orchestrates the rollout of three replicated Pods" → "makes three copies of the Pod. If a Pod stops, the system starts a new Pod automatically."
- **Systems (Rust/C):** `borrow`/`own`/`move`/`drop` are keywords in code font (keep); in prose replace — "borrow"→"get a reference to", "own"→"has"/"controls".

### Edge cases

- **Framework names that are also common words** (Flask, Express, Vite): technical nouns — keep unchanged, use code font; never use as a verb ("Use Flask with…", not "Flask your application").
- **Code keywords that match approved words** (`use`, `move`, `return`, `break`): code font = keyword (technical noun); prose = approved meaning.
- **Generated code / quoted logs:** keep symbol names and quoted text exactly; your surrounding prose uses approved words.
- **When rebuilding loses precision** (e.g. security audits): split + add a clarifying note, or keep the term in code font with a glossary definition, or (internal audience) keep it as a technical noun with an approved-word definition on first use.

## Rule 9.2 — Use Each Approved Word Correctly

**Source:** ASD-STE100 Issue 9, Rule 9.2 (code-domain adaptation).

### What it says

Each approved word has **one approved meaning** and **one approved part of
speech** (a small set of words are approved as more than one — see below). Use
the word only with that meaning and in that role. Other standard-English
meanings are not approved.

### Core procedure

1. Before using a word, check its entry in the controlled terminology (approved meaning + part of speech).
2. Use the word only in its approved role.
3. If a word is unapproved in the meaning/role you need, find an approved alternative with the same part of speech → word-for-word swap; if none, apply Rule 9.1.

### Common part-of-speech traps

| Word | Approved as | NOT approved as | STE fix |
|------|-------------|-----------------|---------|
| `log` | noun ("the record of events") | verb | "write to the log" (not "log the error") |
| `help` | verb ("to assist") | noun | "help text" / "help information" |
| `damage` | noun ("harm") | verb | "cause damage" / "do damage" |
| `build` | verb (technical, Rule 1.12) **and** noun ("the result") | — | "Build the project" / "The build completed"; be specific, not just "the build" |
| `run` | verb | standalone noun | "Run the tests" / "Do a test run" |
| `set` | verb ("put into state") **and** noun ("a group") | adjective | "Set the timeout" / "a set of options"; not "the set timeout value" |
| `check` | verb ("make sure correct") | standalone noun | "Check before deploy" / "Do a health check" |
| `use` | verb | noun/prep | "Use this method" (not "Using this method…") |
| `return` | verb ("go/get back") | standalone noun | "The function returns a value" / "The return value" (not "the return of the function") |
| `execute` | — | verb (for "run a program") | "run" |
| `create` | — | verb | "make" (SQL `CREATE` keyword stays in code font) |
| `select` | — | verb | "choose" / "get" (SQL `SELECT` keyword stays in code font) |

### Multi-meaning / multi-part-of-speech words

- **flush** — verb ("remove remaining data from a buffer") **and** adjective ("where one surface fully touches another"). *"Flush the output buffer."* vs *"Make sure that the connector is flush with the port."*
- **build, run, set, check** — see table above; when a word is approved in two roles, context (position, determiners) must make the role clear.

### Per documentation-type notes

- **README:** every verb/noun is an approved word in its approved meaning. "leverage"→"use"; "functionality"→"feature"; "capability"→"can".
- **API docs:** HTTP `GET` (code font) ≠ the verb "get". "set the timeout value" (verb) vs "a set of endpoints" (noun). "return value" is allowed (noun adjunct); "the return of the function" is not.
- **Docstrings:** "do" = general action only; use the specific verb for specific actions ("Run the migration", not "Do a migration"). "make" = "create"; not a light verb ("Call the service", not "Make a call").
- **Commit messages:** imperative summary with approved verb ("Add feature", not "Implement feature"). "fix" is a verb; "a fix" (noun) is not — use "correction" or "Correct the bug".
- **Error messages:** use "cannot" (not "unable to"/"failed to"); "must" only when the user must act (else state the state: "The file does not exist"); "if" for conditional actions.

### Paradigm-specific notes

- **OO:** `extends`/`implements`/`override`/`abstract` are keywords in code font (technical nouns); in prose they are unapproved verbs — "inherits from", "uses the interface", "replaces the parent method", "base class".
- **Functional:** `map`/`reduce`/`filter` are function names (technical nouns); in prose use "apply a function to each element", "combine the elements into a single value", "remove elements that do not match". `apply` as a verb is not approved → "use the function on the value".
- **Procedural:** `free`/`open`/`close`/`read` are function names (technical nouns); in prose use them as approved verbs — "free the memory that the pointer points to", "the port is available" (not "open for connections"), "read the data".
- **Declarative:** `CREATE`/`SELECT`/`DROP` stay in code font; in prose "make a table", "get rows", "remove the table". `terraform apply` is a command (technical noun); in prose "use `terraform apply` to make the changes".
- **Systems (Rust):** `move`/`drop` as technical verbs are acceptable when the Rust meaning is clear; `borrow`→"get a reference to"; `own`→"has"/"controls"; "ownership" is a technical noun.

### Edge cases

- **Framework/tool names that are unapproved words** (Express, Flask, FastAPI): technical nouns — keep in code font/capitalization; never use as a verb.
- **Keywords that match approved words** (`use`, `move`, `return`, `break`): code font = keyword; prose = approved meaning. "Do not break the API contract" → "Do not change the API contract" (unless literal physical separation).
- **Generated code:** keep symbol names; describe function with approved words ("The `utilizeConfig()` function uses the configuration…"). Prefer a wrapper with an approved name for public APIs.
- **Quoted error/log text:** keep verbatim; explain with approved prose.

## Rule 9.3 — Do Not Make Phrasal Verbs

**Source:** ASD-STE100 Issue 9, Rule 9.3 (code-domain adaptation).

### What it says

A **phrasal verb** = an approved verb + a particle/preposition whose combined
meaning differs from the individual words ("put out" ≠ "put" + "out"). Do not
combine approved words into such phrases. Replace the phrasal verb with a single
approved verb of the same meaning. Only a small set of phrasal verbs are
specifically approved (see below).

**Test:** remove the preposition. If the meaning stays ≈ the same, it is a
prepositional phrase (allowed). If the meaning changes completely, it is a
phrasal verb (not allowed).
- Allowed: *"The application runs on the server."* ("on the server" = location.)
- Not allowed: *"The application runs on for too long."* ("run on" = continues — phrasal verb.)
- Allowed: *"Write the configuration to the file."* ("to the file" = target.)
- Not allowed: *"The team writes up the test plan."* ("write up" = compose — phrasal verb.)

### Common phrasal verbs → approved verb

| Avoid (phrasal) | Use (single verb) |
|-----------------|-------------------|
| put out (emit) | emit |
| give off | return / release |
| carry out | do |
| set up | configure / install / create |
| run through | execute / complete |
| check out | examine / see |
| go through | read / complete |
| pick up (where stopped) | continue |
| break down (analyze) | divide / separate / analyze |
| go on (proceed) | continue |
| look at | examine / inspect |
| filter out | remove |
| kick in | start |
| clear out | remove |
| hook into / tap into | connect / subscribe to |
| hands off | send / transfer |
| tears down | releases / closes |
| prints out | prints |
| writes up | compose |
| breaks out of | exits |

### Commit-message phrasal verbs

| Avoid | Use |
|-------|-----|
| clean up | remove / delete / tidy |
| fix up | correct / repair |
| speed up | accelerate / make faster |
| cut down | reduce / decrease |
| rip out / strip out | remove |
| wire up | connect |
| flesh out | complete / expand |

### Approved phrasal verbs (restricted meaning — keep as-is)

| Approved phrase | Meaning | Example |
|-----------------|---------|---------|
| log in / log out | start/end an authenticated session | "The user must log in before they can access the dashboard." |
| follow up | take further action after an initial step | "Follow up the installation with the configuration step." |
| back up | make a copy for safekeeping | "Back up the database before you apply the migration." |
| roll back | return to a previous state | "Roll back the deployment if the health check fails." |

NOTE: use "log in/out", not "sign in/out", "log on/off". "back up" (two words) = make a copy only.

### Per documentation-type guidance

- **README:** one approved verb per heading/step. "Set up"→"Configure"/"Install"; "Run through"→"Complete"; "Check out"→"Examine".
- **API docs:** verb matches the operation exactly. "Pulls down"→"Gets"; "Puts in"→"Creates"; "Looks up"→"Finds"; "Takes in"→"Receives"; "Spits out"→"Returns".
- **Docstrings:** edit quickly-written informal phrasal verbs. "Runs through… and picks out"→"Examines… and selects"; "Sets up… and kicks off"→"Configures… and starts".
- **Error messages:** "Could not hook up"→"Could not connect"; "blew up"→"failed"; "out of whack"→"not consistent".
- **Changelogs:** "did away with"→"removed"; "ironed out"→"corrected"; "phased out"→"ended"; "added back"→"restored".

### Paradigm-specific

- **OO:** "tears down"→"releases"/"closes"; "hands off ownership"→"transfers ownership"; "looks up"→"finds"; "wraps up"→"completes".
- **Functional:** "maps over"→"applies a transformation to each element"; "pipes through"→"sends through"; "folds down"→"combines"; "reaches out to"→"sends a request to".
- **Procedural:** "free up"→"release"/"free"; "reach out to"→"send a request to"; "put together"→"make".
- **Declarative:** "brings up"→"creates"; "spins up"→"starts"; "tears down"→"removes"; "joins together"→"joins".
- **Systems:** "hands off ownership"→"transfers ownership"; "holds onto"→"keeps a reference to"; "gives up the lock"→"releases the lock"; "carves out"→"allocates".

### Edge cases

- **Framework/tool name contains a phrasal verb** (`setuptools`, `cleanup`, `rollback`): the name is a noun (keep). Its *behavior description* must follow 9.3 ("`setuptools` configures…", not "sets up…").
- **Keyword is a phrasal-verb component** (`break`, `continue`, `throw`, `catch`): keyword as noun/technical verb is fine ("the `break` statement exits the loop"); "breaks out of" is a phrasal verb → "exits".
- **Two approved words that are NOT a phrasal verb:** location/direction/time prepositional phrases are allowed (see test above).
- **No single verb exists:** apply Rule 9.1 — rewrite. "warms up"→"loads the data"; "flags up"→"reports"/"marks"; "churns through"→"processes".
- **Generated docs:** apply 9.3 to the *source* doc comments so the generated output is compliant.

## Rule 9.4 — Always Use a Consistent Style

**Source:** ASD-STE100 Issue 9, Rule 9.4 (code-domain adaptation).

### What it says

When you choose a term or a construction for a concept, reuse it every time
that concept appears. One name per item, one verb per action, one sentence
structure per instruction type. Different wording for the same thing forces the
reader to ask "is this the same or different?" — that is a documentation failure.

### Three consistency domains (all must hold)

1. **Lexical** — one term per concept. Do not alternate "configuration file" / "settings file" / "config".
2. **Syntactic** — same structure per instruction type. Setup steps, config steps, and verification steps each keep one grammatical template.
3. **Semantic** — same meaning across files/modules/types. If "build" = "compile and link" in the README, it must not mean "compile, link, and package" in the CI docs.

### Per documentation-type guidance

- **README:** one term for the artifact ("library" everywhere, not "library" then "package").
- **API docs:** a field/parameter has exactly one name across all references — match prose to the schema (`createdAt` in schema → "created at", not "creation date"/"timestamp").
- **Docstrings:** use the same term as the function signature. Param `max_retries` → "max retries" in the body, not "maximum attempts"/"retry limit".
- **Commit messages:** one imperative verb per change category. If the convention is `Add`, do not mix in `Introduce`/`Insert`/`Create`.
- **Error messages:** one error code → identical text every time (a reliability property, not style).
- **CLI help:** the `--output` flag description is identical in `--help`, man pages, and error messages.

### Paradigm-specific

- **OO:** inherited/overridden methods reuse the base-class template, adding only subclass behavior. Do not abbreviate class names inconsistently (`UserRepository`, not `UserRepo`/`the user repo`).
- **Functional:** all pure functions use the same anchor phrase ("returns a new list with…"), not "produces a result"/"yields output".
- **Procedural (Go):** all `if err != nil` checks use the same pattern ("Check the return code. If the return code is not 0, stop the program.").
- **Declarative:** one phrase per resource type (`aws_instance` = "a virtual machine in AWS EC2" everywhere). Kubernetes `ConfigMap`/`Pod` are proper nouns — never "config map"/"configmap"/"configuration map".
- **Systems (Rust):** "ownership", "borrow", "lifetime", "move" are terms of art — never substitute synonyms ("moved", not "transferred"/"relinquished control").

### Worked examples

- **Verbs in setup:** Non-STE mixes install/fetch/set up/get running → STE: install / download / set the environment variables / start.
- **Noun across types:** Non-STE: "library" / "auth package" / "authentication module" → STE: "authentication library" everywhere; no "auth" abbreviation.
- **API reference structure:** every endpoint description starts with a third-person singular verb; "retrieves"/"gets" unified to "returns"; the `:id` wording identical across endpoints.
- **Commit convention:** one verb ("Add") for all new features.
- **Error messages:** same failure mode → same text ("Cannot connect to the remote host") so logs are searchable.
- **CLI flags:** each flag uses the template "Enables/Disables [adjective] output".

### Edge cases

- **Framework-mandated terms** (React "props", "hooks"): the framework is the authority — use its term consistently, do not translate to an STE-Code synonym.
- **Generated docs:** fix the *source* docstrings; consistency must be authored, not post-processed. CI should reject commits whose conventional-commit verb is non-standard.
- **Cross-project (monorepo):** per-service docs follow the service glossary; system-level docs define a system glossary that maps each system term to its service-level term.
- **Multiple valid industry names:** pick one, document it in the glossary, never alternate.
- **Version renames:** each version's docs use that version's canonical name; migration guides state the rename explicitly.

### Canonical synonym table (the preferred term per concept)

Pick the preferred term and use it in **every** sentence for that concept.
Variation in technical documentation is a defect, not a virtue.

| Concept | Use | Do NOT use |
|---------|-----|------------|
| use | use | utilize, leverage, employ |
| start | start | initiate, commence, bootstrap |
| show | show | display, render, present |
| make | make | create, generate, produce |
| get | get | retrieve, fetch, obtain |
| set | set | configure, assign, establish |
| check | check | verify, validate, ensure |
| remove | remove | delete, eliminate, purge |
| keep | keep | retain, preserve, maintain |
| send | send | transmit, dispatch, forward |

## LLM usage checklist

When generating or reviewing code documentation, apply Section 9 in this order:

1. **Rule 1.1 first** — is every word in the approved dictionary? If not, find an approved alternative with the same part of speech.
2. **Rule 9.2** — is each approved word used with its one approved meaning and part of speech? (Watch `log`/`help`/`damage` noun-verb splits; `build`/`run`/`set`/`check` dual roles.)
3. **Rule 9.3** — did two approved words combine into a phrasal verb? Replace with one verb (`set up`→`configure`, `put out`→`emit`). Exception: the four approved phrases (log in/out, follow up, back up, roll back).
4. **Rule 9.1** — if no single word fits, rebuild the sentence around a different structure; keep code symbols unchanged (Rule 1.5).
5. **Rule 9.4** — is the same concept always named and verbed the same way, in every file and message? Apply the canonical synonym table.

Keep code symbols, framework names, keywords, and quoted log/error text unchanged
(Rule 1.5). They are technical nouns, not prose, and are exempt from word-level
rules — only your surrounding explanation must comply.

## Cross-references

- **Rule 1.1** (Approved Words) — the dictionary; Section 9 repairs what 1.1 cannot fix by replacement.
- **Rule 1.2 / 1.3** (Part of speech / Approved meanings) — the constraints Rule 9.2 enforces.
- **Rule 1.4** (Approved verb/adjective forms) — single approved verbs avoid non-standard phrasal forms (9.3).
- **Rule 1.5** (Technical code nouns) — keywords, framework/tool names, symbols are exempt from 9.1–9.4; exclude them before applying any rule.
- **Rule 1.7** (No technical nouns as verbs) — reinforced by 9.2/9.3.
- **Rule 1.11** (One term per concept) — the lexical foundation of 9.4.
- **Rule 1.12** (Technical verbs) — `build`/`deploy`/`test`/`lint`/`compile`/`debug`/`parse`/`serialize` are approved; do not replace them with phrasal verbs.
- **Rule 3.1 / 5.1 / 6.1** (Simple tenses / short sentences / active voice) — apply when rebuilding under 9.1.
- **The STE-Code dictionary (A–Z)** — source of truth for approved meaning + part of speech; consult before writing.

*End of Section 9 distillation (Level 4).*

