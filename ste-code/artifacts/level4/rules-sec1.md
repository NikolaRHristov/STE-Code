# Level 4 — Section 1: Words (Rules 1.1–1.14)

This slice distills **Section 1 (Words)** of the STE-Code controlled standard for
people who use LLMs to generate code documentation. It covers vocabulary selection:
approved words, technical nouns, technical verbs, parts of speech, meanings, forms,
and the prohibition of slang, jargon, and noun–verb / verb–noun conversions.

STE-Code is a controlled form of English for code documentation (README, API docs,
docstrings, commit messages, error messages, comments, tests, CI logs). Its purpose is
unambiguous, plain prose for a global, non-native-English-reading developer audience.

## The three-gate model for vocabulary

Every content word in a sentence must pass through exactly one of three gates:

1. **Gate 1 — Approved word** (Rule 1.1): the word is in the STE-Code controlled
   terminology. Use it only as its listed part of speech (Rule 1.2), only with its
   approved meaning (Rule 1.3), and only in its approved forms (Rule 1.4).
2. **Gate 2 — Code-domain technical noun** (Rules 1.5–1.6, 1.8–1.11): the word is not
   in the terminology but names a precise concept in one of the 19 categories. It must
   not be used as a verb (Rule 1.7) and must be the standard, short, consistent name
   (Rules 1.8–1.11).
3. **Gate 3 — Code-domain technical verb** (Rule 1.12): the word names a domain-specific
   operation with no simple approved-word equivalent. It must not be used as a noun
   (Rule 1.13).

A word that passes none of the three gates must be replaced with an approved alternative
or the sentence restructured. There is **no fourth category**.

> Cascade rule (Rule 1.12): if an approved verb gives the same meaning, use it. Use a
> technical verb only when no approved verb is sufficient.

---

## Rule 1.1 — Use approved words, technical nouns, or technical verbs

The controlled terminology ("dictionary") gives the words used most often in code
documentation: an approved verb (e.g. `run`, `get`, `set`, `make`, `check`, `send`,
`use`, `start`, `stop`, `call`, `show`, `remove`, `keep`), an approved noun, an
approved adjective (`correct`, `large`, `small`, `fast`, `clear`, `usual`, `primary`),
or an approved adverb.

Every word must pass Gate 1, Gate 2, or Gate 3. Gate 1 is the default for general
vocabulary. See the three-gate model above for the full decision flow.

**Code-domain note:** "run" = execute a program/command; "get" = fetch/retrieve data;
"set" = put a value into a variable/config; "call" = invoke a function. These are the
most common approved verbs in code docs.

---

## Rule 1.2 — Use approved words only as their specified part of speech

Each approved word has a labeled part of speech: verb (v), noun (n), adjective (adj),
adverb (adv), etc. **Use it only in that role.** This is the single most-violated rule
in code docs.

**Most common violation — noun used as verb** (`[TechnicalNoun] the [object]`):
- ✗ "Docker the app" → ✓ "Use Docker to make a container"
- ✗ "Git the changes" → ✓ "Save the changes with Git"
- ✗ "Cache the results" → ✓ "Keep the results in the cache"
- ✗ "Queue the jobs" → ✓ "Put the jobs in the queue"
- ✗ "Query the database" → ✓ "Send a query to the database" (`query` is a noun, not a verb)
- ✗ "Log the errors" → ✓ "Write the errors in the log"
- ✗ "Index the records" → ✓ "Use the index to find the records"
- ✗ "Factory the object" → ✓ "Make the object with a factory"
- ✗ "Param the input" → ✓ "Set the input parameter"

Three fix patterns: (a) **prepositional phrase**: approved verb + noun in a phrase;
(b) **infinitive**: approved verb + infinitive containing the noun; (c) **make + adjective**:
when the noun has a corresponding approved adjective.

**Second most common — adjective used as verb** (`[Adjective] the [object]`):
- ✗ "Secure the endpoint" → ✓ "Make the endpoint secure"
- ✗ "Empty the buffer" → ✓ "Make the buffer empty"
- ✗ "Static the variable" → ✓ "Make the variable static"
- ✗ "Silent the logs" → ✓ "Make the logs silent"
- Note: `clear` is approved as both adj and verb, so "Clear the cache" is allowed.

**Inflated verbs** (not approved) → use plain approved verbs:
- ✗ utilize / leverage → ✓ use
- ✗ commence / initiate → ✓ start
- ✗ terminate → ✓ stop
- ✗ orchestrate → ✓ control
- ✗ facilitate → ✓ help

**Dual-category words:** some words are approved as more than one part of speech
(`call` v+n, `clean` v+adj, `commit` v+n, `return` v). Context decides the role; if
the same word appears twice with different roles in one sentence, restructure
("Use `git commit` to add the files to the change history").

**CLI / framework names** are technical nouns. In prose, precede them with an approved
verb; in code blocks they are quoted text and exempt.
- ✗ "Kubectl the pods" → ✓ "Use `kubectl apply` to send the pods to the cluster"

---

## Rule 1.3 — Use approved words only with their approved meanings

An approved word carries exactly the meaning listed in the terminology. Standard-English
senses outside that meaning are not allowed. Before publishing, for each approved word:
(1) identify its part of speech in your sentence; (2) look up its approved meaning;
(3) confirm your sentence uses exactly that meaning; (4) replace or restructure if not.

**Most-misused approved words (use only with the listed meaning):**

| Word | Approved meaning | Wrong sense to avoid | Use instead |
|------|-----------------|----------------------|-------------|
| run | execute a program/command | operate, manage, continue | operate, manage, continue |
| return | send a value back from a function | go back to a state/location | go back |
| call | invoke a function/method | name something, shout | name, refer to as |
| get | fetch/retrieve data | become, understand | become, understand |
| set | put a value into a variable/config | become solid, prepare | become solid, prepare |
| make | bring into existence by building | force, earn | cause, earn |
| send | transmit data to a destination | cause a person to go | cause to go |
| raise | cause an exception to occur | increase, lift | increase, lift |
| catch | handle/intercept an exception | capture a moving object | capture |
| pass | give data as an argument | go past, succeed | go past, succeed |
| check | examine for correctness/state | stop, restrain | stop, leave |
| break | exit a loop/switch immediately | divide, damage | split, damage |
| continue | skip to next loop iteration | keep doing without pause | keep |
| fail | an operation did not complete | not pass a test | not pass |
| move | transfer ownership (Rust) | change physical position | go, change position |
| borrow | take a reference w/o ownership | take temporarily | take temporarily |
| follow | come after, go after | comply with (instructions) | obey |
| obey | do what procedures tell you | — | — |

Example: "The background worker runs every night" → "operates" (not "execute a program").
"Return to the login screen" → "go back" (`return` means send a value back).

---

## Rule 1.4 — Use only the approved forms of verbs and adjectives

Approved verbs have exactly **four permitted forms**; only these:

1. **Base/Infinitive/Imperative** — `compile`, `run`, `check`
2. **Simple present 3rd-person singular** — `compiles`, `runs`, `checks`
3. **Simple past** — `compiled`, `ran`, `checked`
4. **Past participle** — `compiled`, `run`, `checked` (also used as adjective)

**Never used:** the `-ing` (continuous/participle/gerund) form as a main verb, the
future with "will", the conditional with "would", and any non-standard inflection.

**The `-ing` restriction** (most common 1.4 violation): replace continuous forms with
simple present/past.
- ✗ "The server is running" → ✓ "The server runs"
- ✗ "The compiler will be generating bundles" → ✓ "The compiler makes bundles"
- ✗ "is verifying / is returning / is logging" → ✓ "checks / gives / logs"
- ✗ "wasn't responding" → ✓ "did not respond"
- Permitted: `-ing` as a **code-domain technical noun** ("the logging module", "caching
  layer") or as a compound technical term. Distinguish by grammatical function: noun use
  OK, main-verb use forbidden.

Adjectives follow a **three-form model**: base (`fast`), comparative `-er` (`faster`),
superlative `-est` (`fastest`). Adjectives compared with "more/most" (`more correct`,
`most clear`) need no special listing. Irregular approved comparatives: `far` →
`farther/further`. **`good`/`bad` are not approved** → use `correct`/`incorrect`,
`fast`/`slow`, `large`/`small`. ✗ "more large" → ✓ "larger".

Technical verbs follow standard English morphology; irregular ones keep their pattern
(run/ran/run, give/gave/given, set/set/set). Approved verbs in commit messages and
procedures use the **imperative (base) form**: "add", "fix", "update" — not "adding",
"fixed".

---

## Rule 1.5 — Code-domain technical noun categories (19)

A word not in the controlled terminology may be used if it names a precise concept in
one of these 19 categories. Register every such noun in the project glossary.

1. **Code components, modules, libraries** — class, controller, helper, hook, middleware,
   mixin, module, package, plugin, provider, repository, service, utility
2. **Computing devices & components** — CPU, disk, GPU, keyboard, laptop, memory, monitor,
   mouse, printer, screen, server, smartphone, tablet, terminal
3. **Development tools, environments, support** — CLI, compiler, debugger, Docker, editor,
   IDE, Git, Jest, linter, loader, Prettier, terminal, test runner, TypeScript, webpack
4. **Data structures, types, formats** — array, boolean, buffer, CSV, enum, hash map,
   integer, JSON, linked list, object, queue, stack, string, struct, tree, tuple, XML, YAML
5. **Infrastructure, deployment, platforms** — AWS, CI/CD, container, deployment, Heroku,
   Kubernetes, load balancer, Node.js, pipeline, pod, production, staging, Vercel
6. **Systems, subsystems, architectural components** — API gateway, authentication layer,
   caching layer, client, database layer, message broker, microservice, proxy, rate limiter,
   REST API, routing layer, server, WebSocket
7. **Mathematical, algorithmic, scientific** — Big O notation, binary search, coefficient,
   complexity, exponent, hash function, iteration, logarithm, matrix, recursion, regex,
   sorting algorithm, time complexity, traversal
8. **Interface elements & navigation** — button, checkbox, dialog, dropdown, footer, header,
   menu, modal, navigation bar, radio button, scrollbar, sidebar, tab, text field, toggle, tooltip
9. **Numbers, units, time** — byte, GB, Hz, hour, KB, MB, ms, minute, ns, second, TB
   (version numbers, HTTP status codes, port numbers are category 9 or quoted text)
10. **Quoted text** — verbatim strings: error messages, code snippets, UI labels, log output
    (`Cannot read properties of undefined`, `404 Not Found`, `Submit` button)
11. **Professional roles, teams, organizations** — administrator, backend developer,
    contributor, DevOps engineer, frontend developer, Google, maintainer, Microsoft,
    product owner, QA engineer, reviewer, scrum master, user
12. **Official documents, API references, standards** — API reference, changelog, code of
    conduct, contributing guide, diagram, figure, Getting Started guide, HTTP specification,
    note, paragraph, README, release notes, RFC, section, table, warning
13. **Runtime environments & operational conditions** — development, environment variable,
    garbage collection, heap, hot reload, live reload, memory leak, production, sandbox,
    stack trace, staging, test, thread, timeout, virtual machine
14. **Colors** — black, blue, cyan, gray, green, magenta, orange, red, white, yellow
    (adjectives, but treated as technical nouns; comparatives/superlatives of colors not allowed)
15. **Defects, errors, fault terminology** — assertion failure, bug, crash, deadlock, defect,
    exception, hang, infinite loop, memory leak, null pointer, race condition, regression,
    stack overflow, timeout, type error
16. **Computer science, information, communication tech** — AI, algorithm, authentication,
    authorization, blockchain, containerization, cryptography, database, encoding, encryption,
    firewall, hashing, internet, machine learning, metadata, neural network, protocol, query,
    sandbox, schema, token, virtualization
17. **Legal & licensing terms** — Apache 2.0, BSD license, compliance, copyright, GPL, license,
    MIT license, open source, proprietary, terms of service, third-party, trademark, warranty
18. **Database & storage terminology** — connection pool, cursor, foreign key, index, migration,
    NoSQL, ORM, PostgreSQL, primary key, query, Redis, relation, row, schema, seed, SQL, SQLite,
    stored procedure, table, transaction, view
19. **Network & protocol terminology** — DNS, endpoint, HTTP, HTTPS, IP address, localhost,
    middleware, packet, port, request, response, route, socket, SSH, TCP, TLS, UDP, URL, VPN,
    WebSocket

**Glossary requirement:** register each technical noun with its term, category, approved
meaning in context, and an example sentence. Unregistered internal names ("PhoenixCache")
violate Rule 1.6.

**Grammar of technical nouns:** use normal articles (`the UserController`, `a request`);
pluralize acronyms with lowercase "s" (`APIs`, `SQL queries`, not `API's`); proper nouns
keep capitalization (`TypeScript`), common nouns are lowercase (`controller`); possessive
`'s` only for category 11 (roles/orgs), else use "of" (`the configuration of the Docker
container`).

---

## Rule 1.6 — A non-approved word only when it is a technical noun (or part of one)

Rule 1.6 is the **technical-noun gate**. An unapproved word may stay only if it clears
all three tests:

- **Test 1 — Is it unapproved?** Approved words never enter this gate.
- **Test 2 — Is it a technical noun, or part of a compound technical noun?** Standalone,
  it must fit a category. Embedded in a recognized compound, the compound must fit a category.
- **Test 3 — Is it used as a noun?** If it is a verb/adjective/adverb, it fails (Rule 1.7).

**Worked trace:**
- "main config loader" → "main" is a general adjective → replace with "primary"
- "backups the data" → "backup" as verb → "makes an auxiliary copy"
- "handler pipeline" → "handler" alone is not a recognized compound → "processing pipeline"
- "main branch" (Git term, cat 5) → passes; "event handler" (cat 1) → passes; "base case"
  (cat 7) → passes; "base URL" (cat 8) → passes.

**Key dictionary entries:** BASE (unapproved; use BOTTOM/ROOT; permitted in "base case",
"base class", "base URL"). MAIN (adj unapproved; use PRIMARY; permitted in "main branch",
"main function"/`main()`). HANDLER (n unapproved; use FUNCTION; permitted in "event handler",
"request handler"). BACKUP (n/v unapproved; use AUXILIARY / "makes an auxiliary copy";
permitted in "backup_logs", "backup file", resource `/api/v1/backup`).

**Compound test:** a compound is a technical noun only if (1) it names one domain-recognized
concept, (2) fits a category, and (3) swapping the unapproved word for its approved
alternative would change the recognized name. If the swap keeps the name, it is NOT a
technical noun — make the replacement.

---

## Rule 1.7 — Do not use technical nouns as verbs

A code-domain technical noun (Gate 2) must stay a noun. Use an approved verb (or technical
verb) for the action. The prepositional-phrase pattern: **approved verb + technical noun
in a phrase**.

| Noun-verb (✗) | Repair (✓) | Verb | Prep |
|----------------|-----------|------|------|
| Cache the data | Put the data in the cache | put | in |
| Queue the job | Add the job to the queue | add | to |
| Buffer the output | Write the output to a buffer | write | to |
| Socket the connection | Send the connection through a socket | send | through |
| Database the records | Store the records in the database | store | in |
| Docker the app | Package the app in a container | package | in |
| Git the changes | Commit the changes | commit | — |
| JSON the response | Encode the response as JSON | encode | as |
| Schema the database | Apply a schema to the database | apply | — |
| Table the data | Store the data in a table | store | in |
| Malloc a block | Allocate a block with `malloc` | allocate | with |

**Multi-word nouns:** keep the full phrase; do not drop a word to make a verb.
- ✗ "Load balance the requests" → ✓ "Distribute the requests with a load balancer"
- ✗ "Circuit break the service" → ✓ "Apply a circuit breaker to the service"

**Dual-category exception** (also Rule 1.13 edge case): some words are both technical noun
and technical verb — `cache`, `log`, `queue`, `filter`, `sort`, `map`, `build`, `deploy`,
`merge`, `import`, `commit`. Use the verb form only in the matching verb context; keep the
noun form for entities. Pick the part of speech the project glossary assigns; do not mix in
one paragraph without clear signals. Example: `log` as verb = "Log the error"; as noun = "log
entry" / "log file" — keep them distinct ("Write the log entry to the log file").

---

## Rule 1.8 — Use standard, well-known technical nouns

When more than one name exists for a concept, use the **standard, approved** name from the
most authoritative source: source code (class/function names), API spec, language standard
library, design-pattern literature, RFC/IETF, provider docs.

| Avoid (invented) | Use (approved) | Authority |
|------------------|---------------|-----------|
| user maker / user handler | `UserRepository` | source code |
| save method / persist op | `save()` | source code |
| display part / watcher | View / `Observer` | pattern literature |
| maybe-type / nullable wrapper | `Option` / `Maybe` | language stdlib |
| heap allocation / data record | `malloc` / `struct` | C spec |
| compute instance | `aws_instance` | Terraform docs |
| secure web communication | HTTPS | IETF |
| splits list in half repeatedly | binary search algorithm | CS literature |

Do not invent names for items that already have established names. Consistency lets readers
find the exact element in the source tree.

---

## Rule 1.9 — Prefer short, clear technical nouns

When several legitimate technical nouns name the same concept, prefer the shorter, clearer
one. Keep `UserTable` over a longer descriptive phrase; prefer `observer pattern` over a
long homemade description. Shortness aids non-native readers and searchability.

---

## Rule 1.10 — No regional, slang, or jargon words

Technical documentation must be clear to a global audience. Replace slang, jargon, regional
idioms, and metaphor with approved words or precise technical nouns.

**Replacements:**
- ✗ cruft → ✓ unnecessary code
- ✗ monkeys with → ✓ changes
- ✗ bikeshedding → ✓ unnecessary discussion about small details
- ✗ yak shaving → ✓ completing unrelated prerequisite tasks
- ✗ foo / bar (placeholders) → ✓ example / placeholder
- ✗ grok → ✓ understand
- ✗ dumpster fire / nuke it from orbit → ✓ too complex and unreliable; remove and rewrite
- ✗ nerfed → ✓ decreased performance
- ✗ Gordian knot / strangle pattern → ✓ many tightly connected parts; gradual replacement
- ✗ shiny new hotness → ✓ current interface
- ✗ went pear-shaped → ✓ failed at 50 percent; check your network and try again
- ✗ yeet → ✓ remove
- ✗ snag / fire up / cd into → ✓ clone / start / change to
- ✗ tweak the knobs / twiddle the bits → ✓ change / set
- ✗ wonky / prod → ✓ incorrect / production

**Jargon categories:** regional terms (ecosystem-specific, e.g. Ruby "gem"); slang metaphors
("spaghetti code" → "code with complex control flow"); jargon with fuzzy meaning ("grok",
"cruft" not in a standard computing dictionary); abbreviation jargon ("DRY", "KISS", "YAGNI"
— spell out the principle: "remove duplicate code"); temporal jargon ("modern", "legacy",
"cutting-edge" → give specific date or characteristic, e.g. "written in 2018").

**Paradigm slang to avoid:** OOP "POJO-ify" → "convert to a plain object"; FP "eta-reduce" →
"simplify the function"; procedural "massage the buffer" → "adjust the buffer"; declarative
"cattle not pets" → "disposable resources"; systems "UB" → "undefined behavior".

**Review checklist:** (1) read aloud — would a foreign developer understand every word?
(2) replace metaphors with literal descriptions; (3) expand abbreviations on first use;
(4) replace community nicknames with standard terms; (5) replace temporal words with dates;
(6) verify every noun/verb is approved or a justified technical noun; (7) no slang verbs
("hit", "nuke", "yeet", "tweak", "twiddle").

---

## Rule 1.11 — One term per concept

Use the **same** code-domain technical noun for the same item everywhere. Do not use
different names for one component. The source of truth is the code: class, function, module,
table, resource, environment variable, or config key as defined in the repo.

| ✗ Different names | ✓ One consistent noun |
|-------------------|----------------------|
| UserService / AccountManager / UserHandler | `UserService` |
| /api/login path / authentication route / login endpoint | `/api/login` endpoint |
| user_accounts table / accounts relation / user table | `user_accounts` table |
| database_connection_timeout / DB timeout / connection deadline | `database_connection_timeout` |
| project-builder / build system / compiler | `project-builder` |
| ValidationFailure / InputError / validation exception | `ValidationError` |
| API_KEY env var / auth token / secret key | `API_KEY` environment variable |
| mainline / master / main branch | `main` branch |

**Grammar consequence:** consistent nouns keep English article and pronoun reference
chains intact ("the UserService … it returns a token"). Switching nouns breaks anaphora and
compound head-noun coherence.

**Edge cases:** framework/library names that are also common words (Rails, Spring, Make) —
use as technical nouns, capitalize. Code keywords in concept names (`async function`) — keep
the full compound consistently. Multiple canonical names in different contexts (Docker image
`myapp:latest` vs CI `myapp-image`) — choose one per document/section and declare the mapping.
Generated names — use the generated symbol; alias only if declared explicitly.

---

## Rule 1.12 — Technical verbs are allowed (4 categories)

Use a code-domain technical verb when no approved verb gives the same precision. Cascade:
prefer the approved verb. Technical verbs obey Section 3 (tense, mood, voice).

1. **Development processes**
   - a) Write/modify code: compile, concatenate, import, inject, instantiate, lint, minify,
     marshal, optimize, polyfill, refactor, resolve, shim, stub, substitute, tokenize,
     transpile, trace, vectorize
   - b) Test/verify: assert, benchmark, debug, fuzz, instrument, mock, profile, snapshot, spy,
     stub, unit-test
   - c) Build/package: bundle, deploy, package, publish, release, tag, version
   - d) Manage deps: hoist, install, link, lock, pin, update, upgrade
2. **Computer processes & applications**
   - a) I/O: click, copy, cut, digitize, enter, paste, press, print, scan, swipe, tap, type
   - b) UI/app ops: clear, close, delete, deselect, disable, drag, enable, encrypt, erase,
     filter, hide, highlight, invalidate, maximize, minimize, navigate, open, save, scroll,
     select, show, sort, store, submit, toggle, validate, zoom in/out
   - c) System ops: abort, authenticate, authorize, boot, cache, communicate, configure, debug,
     deserialize, download, format, hydrate, initialize, install, load, log, manage, mount,
     process, reboot, render, retry, serialize, spawn, synchronize, throttle, update, upgrade,
     upload
3. **Instructions for subject fields**
   - a) Algorithmic/data: aggregate, bisect, compute, concatenate, convert, count, decode,
     encode, escape, filter, hash, index, map, merge, normalize, parse, pipeline, precompute,
     recalculate, reduce, tokenize, transform, validate, verify
   - b) Database/storage: backup, compact, flush, index, migrate, persist, query, replicate,
     restore, roll back, seed, shard, upsert, vacuum, write-ahead
   - c) Network/comms: broadcast, connect, disconnect, establish, forward, handshake, intercept,
     listen, poll, proxy, reject, resolve, route, send, stream, timeout, tunnel, unsubscribe,
     webhook
   - d) Legal/licensing: acknowledge, assign, comply with, conform to, disclose, enforce,
     explain, grant, inform, license, modify, notify, permit, regulate, sign, supersede, waive
4. **Legal & licensing terms** (only for legal/regulatory text)

**Paradigm verb sets:** OOP — instantiate, inherit, override, extend, implement, encapsulate,
delegate, inject. FP — compose, curry, map, reduce, fold, recurse, memoize, lift. Procedural —
allocate, deallocate, dereference, flush, signal. Declarative — provision, converge, reconcile,
apply, destroy. Systems — borrow, own, drop, move, pin, acquire, release.

**Do not noun-verb or verb-noun:** see Rules 1.7 / 1.13. Use the verb form matching the method
name ("`serialize()` serializes the object"); keep imperative mood for procedures; do not split
multi-word technical verbs ("roll back the migration", not "roll the migration back").

---

## Rule 1.13 — Do not use technical verbs as nouns

Use code-domain technical verbs (Gate 3) only as verbs. If you need a noun, use an approved
noun or a technical noun.

- ✗ "does a compile of the source" → ✓ "compiles the source"
- ✗ "the merge of the branch" → ✓ "the merge operation of the branch" (or use "merge" as verb)
- ✗ "execute a rollback of the migration" → ✓ "roll back the migration"
- ✗ "a commit of your changes" → ✓ "commit your changes" (commit as noun = a snapshot object,
  a technical noun — dual-category exception)
- ✗ "make a build of the project" → ✓ "build the project"

**Gerunds as noun substitutes** ("The compiling takes ten seconds") are less direct; prefer
"The compilation takes ten seconds" or "It takes ten seconds to compile." In procedures, use
the imperative verb directly.

**Dual-category exception:** words like `deploy`/`build`/`merge`/`import`/`commit`/`log` can be
both technical verb and technical noun; use the noun form only when naming a recognized entity
(a Deployment resource, a `Build` stage, a commit object).

---

## Rule 1.14 — Use American English spelling

Use American spellings consistently: `color` not `colour`, `initialize` not `initialise`,
`behavior` not `behaviour`, `center` not `centre`. This is a spelling constraint on all words
that pass the gates. Regional terms are also prohibited by Rule 1.10.

---

## Cross-cutting: paradigm guidance (condensed)

- **Object-Oriented:** class/interface/pattern names are technical nouns (Gate 2). Prose uses
  approved verbs. Do not verb nouns ("singleton the pool" → "use a singleton pattern").
- **Functional:** `map`/`filter`/`fold`/`reduce`/`compose` are technical verbs (Gate 3) when
  used technically; as type names they are technical nouns. Keep the role consistent.
- **Procedural (C/Go/Bash):** `malloc`, `struct`, `pointer`, `goroutine` are technical nouns;
  use approved/technical verbs ("allocate a buffer with `malloc`"). "Free" is a technical verb.
- **Declarative (SQL/Terraform/K8s):** resource/table/column names are technical nouns.
  SELECT/INSERT/etc. are technical verbs in code blocks (quoted text) and technical terms in
  prose (backtick-marked). Do not verb resource names ("schema the database" → "apply a schema").
- **Systems (Rust/C):** `own`/`borrow`/`move`/`drop` are technical verbs; `unsafe` is an
  approved adjective and a keyword noun. Use `Drop` as a noun, "runs the `Drop` implementation"
  not "drops the guard" without marking.

## Documentation-type patterns

- **README:** procedural steps use imperative approved verbs; descriptive prose uses approved
  adjectives. No slang, no noun-verbs, no framework names as verbs.
- **API docs:** endpoint/param/type names are technical nouns; describe them with approved verbs
  ("gets a user", "gives an error", "sends a query"). Match method names ("`serialize()`
  serializes").
- **Docstrings/comments:** concise; approved verbs; technical nouns unchanged; no `-ing` main
  verbs; imperative mood for procedure descriptions.
- **Commit messages:** imperative base-form verb (`add`, `fix`, `update`, `remove`, `set`,
  `make`, `check`, `run`); type prefix (`feat:`, `fix:`) is a technical noun and exempt.
- **Error messages:** approved verbs, complete sentences; name the exact component that failed;
  no slang ("went pear-shaped" → "failed at 50 percent; check your network and try again").
- **Tests/CI logs:** step names and echo strings are prose — obey part-of-speech and form rules;
  shell commands and code are exempt (quoted text).

## Key references

- Controlled terminology (approved words, parts of speech, meanings, forms): `a-dictionary.md`
- 19 technical noun categories: `a-categories.md`
- Verb rules (tense, mood, voice): Section 3
- This slice covers Section 1 only. Related sections: Section 2 (sentences), Section 3 (verbs),
  Section 4 (style), Section 5 (illustrations), Section 6 (procedure/prohibition).
