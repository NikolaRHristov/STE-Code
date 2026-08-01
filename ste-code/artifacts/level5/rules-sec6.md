# Level 5 — Section 6: Sentence and Paragraph Structure (Rules 6.1–6.6)

This slice of the STE-Code standard governs how to organize sentences and
paragraphs in code documentation. It is part of the full standard (all rules +
extensions + dictionary + provenance) at Level 5.

## What this section is for

When an LLM generates code documentation (README, API docs, docstrings, inline
comments, commit messages, error messages, changelogs, config comments), apply
these six rules so the output is easy to read on the first pass:

- **Rule 6.1** — Give information gradually; one subject per sentence.
- **Rule 6.2** — Use key words and key phrases to give the text a logical structure.
- **Rule 6.3** — Write short sentences (max 25 words each).
- **Rule 6.4** — Use paragraphs to group related information (topic sentence first).
- **Rule 6.5** — Each paragraph has only one topic.
- **Rule 6.6** — No paragraph has more than six sentences.

The rules build on each other: 6.1 splits compound sentences → 6.2 links the
short sentences with repeated key words → 6.3 keeps each sentence short → 6.4
groups related sentences into paragraphs → 6.5 keeps each paragraph on one
topic → 6.6 caps paragraph length.

## Shared code-domain vocabulary

Across all six rules, prefer plain approved verbs and avoid unapproved synonyms:

- `make` (not "create"/"generate"), `start` (not "initiate"), `stop` (not
  "terminate"), `get` (not "retrieve"/"fetch"), `send` (not "transmit"),
  `show` (not "display"/"render"), `set` (not "configure"/"assign"),
  `check` (not "verify"/"ensure"), `use` (not "utilize"/"leverage").
- Approved connecting words: `and`, `but`, `then`, `thus`, `also`, `however`,
  `therefore`, `for example`, `as a result`, `at the same time`. Place them
  near the start of a sentence so the reader sees the signal first.
- Technical code nouns (class names, function names, library names, framework
  names) are allowed even when not in the approved dictionary (Rule 1.5). Do
  not use a technical noun as a verb.

---

## Rule 6.1 — Give Information Gradually

Adapted from ASD-STE100 Issue 9, Rule 6.1.

**Core rule.** In code documentation, give the reader one piece of information
at a time. Each sentence contains only one subject performing one action. Do
not combine multiple actions, multiple conditions, or multiple subjects in one
sentence. Applies to every form of documentation: README, API reference,
docstrings, inline comments, commit messages, error messages, log entries,
changelogs, config files.

**Why.** Human working memory holds ~4–7 items. A sentence with multiple
subjects and verbs forces the reader to hold all of them until the sentence
ends, raising cognitive load — especially when the reader is also parsing code.

**Single-subject constraint (grammar).**
- One subject + two verbs sharing that subject is OK: "The function validates
  the input and returns a result." (one subject "function").
- Two subjects is NOT OK: "The function validates the input and the middleware
  logs the result." → split: "The function validates the input. The middleware
  logs the result."

**Splitting rules.**
- Coordinating conjunction (`and`/`or`/`but`) joining two clauses, each with
  its own subject — split at the conjunction.
- Subordinating conjunction (`because`/`since`/`while`/`if`) — one main clause
  + one dependent clause is OK, unless the dependent clause introduces a new
  subject with its own chain of actions (then move it to its own sentence).
- Relative clause (`which`/`that`/`who`) describing the main subject is OK; one
  that introduces a new subject + new actions must be split.

**Code-domain example (auth middleware).**

Non-STE (one dense sentence, ~90 words):
> The authentication middleware validates bearer tokens from the authorization
> header by calling the `validateToken` function in the security module which
> decodes the JWT payload using the `HS256` algorithm from the `jwt-signer`
> library and checks the `exp` claim against the current server time before
> extracting the `sub` and `role` claims and attaching them as properties on
> the `request.auth` object, and if the token is expired or malformed the
> middleware returns a `401 Unauthorized` response with a JSON error body ...

STE (one subject per sentence):
> The authentication middleware validates each incoming request. The middleware
> reads the bearer token from the `Authorization` header. It sends the token to
> the `validateToken` function in the `security` module. The `validateToken`
> function decodes the JWT payload. It uses the `HS256` algorithm from the
> `jwt-signer` library. Then it compares the `exp` claim with the current
> server time. If the token is not expired and not malformed, the function gets
> the `sub` and `role` claims. It attaches these claims as properties on the
> `request.auth` object. If the token is expired, the middleware returns a
> `401 Unauthorized` response. The response body is a JSON object: the
> `message` field contains a description of the error; the `errorCode` field is
> set to `TOKEN_EXPIRED`. If the token is malformed, the middleware returns a
> `401 Unauthorized` response. The `errorCode` field in the response is set to
> `TOKEN_MALFORMED`. The middleware also logs each failure to the audit trail.
> It calls the `AuditLogger.log` static method. This method writes a record to
> the `audit_events` table in the primary database. The write uses an
> asynchronous pattern that does not block the response pipeline.

**Per-context guidance.**
- README: one concept per sentence. State the purpose, then the install
  command, then a usage example — each in its own sentence.
- API docs: one sentence for method+path, one per parameter, one per response
  field or status code. A reader who looks up one parameter must not read a
  paragraph about ten unrelated things.
- Docstrings/comments: one behavior per sentence. Each parameter and each
  return condition gets its own sentence.
- Commit messages: one logical change per sentence; use a summary line + bullet
  body, not "Add X, fix Y, update Z, refactor W" as one sentence.
- Error/log messages: one problem per message with a distinct error code; one
  event per log line.
- Changelogs: one change per entry; separate feature / fix / deprecation.

**Paradigm-specific.** Object-oriented: one method/behavior per sentence;
describe the override chain step by step. Functional: one transformation per
sentence; do not describe an entire `>>=` or pipe chain in one sentence.
Procedural: one step/branch per sentence — if/else and loop bodies stay separate
sentences. Declarative: one resource/constraint/column per sentence. Systems:
one ownership rule / lifetime constraint / memory operation per sentence.

**Edge cases.**
- A framework name combining multiple actions (e.g.
  `UserAuthenticationAndAuthorizationService`) is one technical noun — do not
  split it; keep the single-subject rule for the surrounding prose.
- Tool-generated docs (OpenAPI/JSDoc/Sphinx) may emit compound sentences. If
  you cannot change the output, add a one-subject-per-sentence summary above the
  generated block.
- Control-flow keywords (`if`/`else`/`while`/`try-catch`) naturally have
  multiple subjects — use one sentence per branch.
- CLI `--help`/error codes have limited space: still one subject per sentence;
  use fragments only when the display format enforces them.
- When rewriting existing compound docs, check for hidden logical dependency:
  if B depends on A, describe A first, then B.

**See also.** Rule 6.2, 6.3, 6.4, 6.5; Rule 1.1 (approved words); Rule 1.11
(one term per concept).

---

## Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure

Adapted from ASD-STE100 Issue 9, Rule 6.2.

**Core rule.** Use key words (terms repeated across a documentation block) and
key phrases (multi-word expressions) to connect related ideas across sentences.
Key words are the threads that bind a block into one coherent unit. Do not change
the key word within a block — the same term must carry the same meaning
everywhere (links to Rule 1.11). Place approved connecting words near the start
of a sentence so the reader sees the signal before the content.

**Approved connecting words/phrases.** `and`, `but`, `then`, `thus`, `also`,
`however`, `therefore`, `for example`, `as a result`, `at the same time`. Do NOT
use `moreover`, `furthermore`, `nevertheless`, `subsequently`, or
`utilize`/`leverage` as connectors.

**How key words work (example chain).** Across the auth-middleware block:
> Sentence 1: The authentication middleware validates each incoming request.
> Sentence 2: The middleware reads the bearer token from the `Authorization` header. (repeats "middleware")
> Sentence 3: It sends the token to the `validateToken` function in the `security` module. (repeats "token")
> Sentence 4: The `validateToken` function decodes the JWT payload. (repeats "`validateToken` function")
> Sentence 9: The response body is a JSON object. (repeats "response")

Three groups form by key word: (1) token validation, (2) error responses +
`errorCode`, (3) audit trail. The reader follows the chain sentence to sentence
without manual reconstruction.

**Key word by documentation type.**
- README: repeat the project/library name and core concept ("middleware",
  "pipeline", "plugin") as the key word across sections. Do not switch to "the
  library"/"this tool".
- API docs: function names, parameter names, return-type names are the key
  words. Each sentence names the function or a pronoun referring to it.
- Docstrings: the function/class name is the key word; use parameter names and
  pronouns, not synonyms like "transmit"/"data"/"queue".
- Commit messages: the component name + action verb + affected module are the
  key words; do not switch to "pool"/"conn pool"/"connection manager".
- Error messages: the operation name + resource name are the key words; do not
  switch to "document"/"path".
- Cross-type consistency: the same key word means the same thing in README, API
  docs, docstrings, and commits (part of Rule 1.11).

**Paradigm-specific key words.**
- OOP: class names, method names, property names. For a builder/method chain,
  repeat the return type (e.g. "Stream") to show the flow.
- Functional: type names, function names, data constructors; the value flowing
  through transformations is the key word (e.g. "Result", the "changeset").
- Procedural: variable names, struct fields, error codes (e.g. "buffer").
- Declarative: resource names, column names, attribute names (e.g.
  "aws_instance").
- Systems: ownership terms, lifetime names, pointer names (e.g. "buffer",
  "borrow").

**Edge cases.**
- A framework name that is an unapproved word (e.g. a library named "Leverage")
  is a technical code noun — keep it as the key word; do not replace with a
  synonym.
- A short language keyword that carries little meaning (Go `go`, Rust `mut`) is
  not a good key word — use a descriptive key phrase that includes it (e.g.
  "goroutine").
- Generated code with verbose type names (e.g. `UserServiceClientImpl`) is the
  key word even though long — do not shorten to "client"/"stub"/"it".
- Multi-language repos: pick one key word for a cross-language concept (e.g.
  "map" for Python `dict` / Java `HashMap` / Go `map`) and note the
  language-specific names once.
- Multi-word key phrases ("connection pool", "rate limiter", "retry policy")
  stay intact — do not break them apart mid-document.

**Grammar notes.** Key-word repetition is lexical cohesion. Three cohesive ties:
(1) Repetition ("The middleware validates the request. The middleware reads the
token."); (2) Pronoun reference ("It reads the token.") — use sparingly, repeat
the full key word after two sentences; (3) Approved synonym/hypernym. Topic is
the subject of each sentence (topic-comment structure): keep the same key word in
subject position. A "dangling key word" (introduced once, never repeated) breaks
the structure. Use connecting words at the start of sentences, not buried.

**See also.** Rule 6.1, 6.3, 6.4, 6.5; Rule 1.5 (technical code nouns), Rule
1.8 (standard technical nouns), Rule 1.9 (short technical nouns), Rule 1.11 (one
term per concept).

---

## Rule 6.3 — Write Short Sentences. Maximum 25 Words per Sentence.

Adapted from ASD-STE100 Issue 9, Rule 6.3.

**Core rule.** In descriptive code documentation, the maximum sentence length is
25 words. Short sentences give clear structure and make information easier to
understand. This is a hard ceiling for descriptive text; procedures (imperative
steps) are naturally shorter.

**Why the limit.** A 25-word sentence can hold at most ~2 clauses with
connecting words — matching working-memory capacity. Most English clauses are
6–12 words, so the limit indirectly bounds clause density. Splitting one complex
sentence into several short ones improves clarity even when the original is under
25 words.

**Examples (code-domain).**
- Non-STE (32 w): "The configuration loader reads the YAML manifest file from
  the filesystem and parses it into an in-memory representation that other
  modules can query at runtime to determine their operational parameters."
  → STE: "The configuration loader reads the YAML manifest file from the
  filesystem. It parses the file into an in-memory representation. Other modules
  can query this representation at runtime. They use it to find their
  operational parameters." (20/8/7/8)
- Non-STE (34 w): "The cache invalidation strategy employs a time-to-live
  mechanism combined with a least-recently-used eviction policy to ensure that
  stale data is removed and memory consumption remains within the allocated heap
  budget."
  → STE: "The cache invalidation strategy uses a time-to-live mechanism. It also
  uses a least-recently-used eviction policy. Together, these mechanisms remove
  stale data. They also keep memory consumption within the allocated heap
  budget." (16/10/7/10)
- Non-STE (21 w): "This function provides the ability to run arbitrary software
  applications within a sandboxed execution environment that isolates system
  resources."
  → STE: "This function lets you run software applications in a sandbox. The
  sandbox isolates system resources." (8/5)

**Per-context guidance.**
- README: one sentence for the project, one for prerequisites, one for install.
- API docs: one short sentence each for path+method, each parameter, each
  response field, each error code.
- Docstrings: one sentence for purpose, one per parameter, one for return, one
  per exception — all under 25 words.
- Commit messages: subject line ≤72 chars; one short sentence per logical
  change in the body.
- Error messages: two short sentences — the problem, then the action. Log
  aggregation tools parse by line, so one sentence per line helps filtering.

**Paradigm-specific.**
- OOP: split inheritance + behavior into separate sentences ("The
  `AuthenticatedController` class extends `BaseController`. It implements the
  `Auditable` and `Loggable` interfaces.").
- Functional: split composition from error behavior.
- Procedural: each step = one sentence; for safety-critical code, split
  allocation from copy from return.
- Declarative: document each resource argument in its own sentence.
- Systems (Rust ownership, C memory): short sentences are safety-critical; split
  borrowing/lifetime explanation into discrete sentences.

**Edge cases.**
- Long technical terms ("single sign-on", "Hypertext Transfer Protocol Secure")
  count as one unit; if one still pushes over 25 words, introduce an acronym
  (SSO) after first mention to cut later counts.
- Verbose language keywords (`synchronized`, `__attribute__((constructor))`) count
  as one word — keep the rest of the sentence short.
- Compound type signatures (TypeScript/Rust generics) often exceed 25 words: one
  sentence for the type shape, one for constraints, one for behavior.
- Legal/license text (MIT, Apache, GPL, copyright) is exempt; the surrounding
  explanation still obeys the limit.
- Generated documentation (JSDoc/Sphinx/`go doc`) may exceed the limit — fix the
  source docstrings, not the generated output.

**Counting rules.** Hyphenated compounds count as one word ("least-recently-used"
= 1). Acronyms count as one word ("JSON" = 1). Code tokens count as one word
(`Result<Vec<T>>` = 1). Do not count parenthetical word counts in examples.

**Grammar notes.** Prefer coordination with separate sentences over heavy
subordination (e.g. "The `parse` function throws a `SyntaxError`. This error
occurs when the input string contains invalid JSON." rather than a 27-word
sentence with three levels of subordination). Code docs use implicit connectives
(order implies flow) rather than academic "therefore"/"furthermore".

**See also.** Rule 6.1, 6.2, 6.4, 6.5; Rule 1.1 (approved words); Rule 1.10 (no
slang/jargon).

---

## Rule 6.4 — Use Paragraphs to Show Related Information

Adapted from ASD-STE100 Issue 9, Rule 6.4.

**Core rule.** In code documentation, a paragraph starts with a topic sentence
that tells the developer the topic of that paragraph. The sentences that follow
explain it or add related information. A new paragraph signals a new topic or
different information. This applies to procedures (numbered steps) and
descriptive writing alike.

**Why.** Paragraphs group related sentences and give the text a logical
sequence. A paragraph that mixes unrelated topics (install steps + config
options + usage) is not compliant. Use section headings for major topics and
paragraph breaks for sub-topics.

**Examples (data pipeline split into topic-sentence-led paragraphs).**

Non-STE (one dense paragraph, mixed stages + error handling):
> The data pipeline processes incoming events through a sequence of stages. Each
> stage transforms the event payload and passes it to the next stage. The first
> stage is validation ... The second stage is enrichment ... The third stage is
> transformation ... The final stage is persistence ... Error handling is
> implemented at each stage ... If a stage fails, the pipeline logs the error and
> routes the event to the dead-letter queue ...

STE (each stage = its own paragraph with a topic sentence):
> **1. Data Pipeline Overview** — The data pipeline processes incoming events
> through a sequence of stages. Each stage transforms the event payload and
> passes it to the next stage. Error handling is implemented at each stage ...
> **2. Validation Stage** — The first stage is validation. This stage checks the
> event schema. It rejects events that are malformed.
> **3. Enrichment Stage** — The second stage is enrichment. This stage adds
> metadata to the event: Timestamps; Source identifiers; Geolocation data.
> **4. Transformation Stage** — The third stage is transformation. This stage
> converts the event into the target format. Downstream consumers use this
> format.
> **5. Persistence Stage** — The final stage is persistence. This stage writes
> the transformed event to the data store and to the event log for audit.

**Per-context guidance.**
- README: each section starts with a topic sentence. Separate Installation,
  Configuration, Dependencies, Usage into their own paragraphs.
- API docs: endpoint description = topic sentence first; give authentication its
  own paragraph (before endpoint details); separate request schema, response
  schema, and error descriptions with clear topic sentences.
- Docstrings/inline comments: start with a one-line topic sentence, then a blank
  line, then more paragraphs (parameters / returns / raises / side effects /
  usage). Each inline comment is a one-sentence paragraph stating the topic of
  the following code.
- Commit messages: the first line is the topic sentence; the body uses paragraphs
  to group the problem, the changes, and the monitoring separately.
- Error messages: a single sentence states the topic (what failed + why); a
  multi-line error uses paragraphs to separate the error description, the
  diagnostic checks, and the stack trace.

**Paradigm-specific.**
- OOP: separate class purpose, constructor details, public API, and internal
  design into paragraph groups; one paragraph per method description.
- Functional: separate the type signature explanation, the behavior, the
  purity/algebraic properties, and the internal composition.
- Procedural: separate initialization, main loop, and cleanup phases.
- Declarative: give each resource its own paragraph group (identity, spec,
  dependencies).
- Systems: separate the ownership model, lifetime annotations, and unsafe-code
  justifications.

**Edge cases.**
- Framework name = approved word (e.g. "Make" the build tool vs "make" the verb):
  capitalize the tool, use a topic sentence to establish meaning.
- Code keywords (`break`, `continue`, `return`, `yield`) are technical nouns
  (Rule 1.5), not verbs — set them in backticks and start the paragraph with a
  topic sentence naming the keyword.
- A long code block must sit in its own paragraph; start the preceding paragraph
  with a topic sentence that names what the code does, end it, insert the block,
  then start a new paragraph to explain important parts.
- Auto-generated docs (JSDoc/Sphinx/`go doc`): insert a blank comment line
  between topics so the tool emits separate paragraphs.
- Mixed-author documents: apply structural linting; flag paragraphs >5 sentences
  or lacking a topic sentence (a Vale `existence` rule works).

**Grammar notes.** The topic sentence is a declarative simple-present sentence
that names the topic in subject position with an approved verb — never start a
paragraph with a subordinate clause ("Because...", "When...", "If..."). A
paragraph of five sentences cannot exceed 125 words (due to Rule 6.3). Ideal
length: docstrings 1–3 sentences per topic, README 3–5, API endpoint 4–6, error
messages 1. Place a paragraph break before a new concept, a code example, a
warning, a list, or a change in abstraction level. Do NOT break between a topic
sentence and its supporting sentences.

**See also.** Rule 6.1, 6.2, 6.3, 6.5; Rule 1.1, 1.5, 1.11; Rule 7.1 (use lists
for three or more items).

---

## Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic

Adapted from ASD-STE100 Issue 9, Rule 6.5.

**Core rule.** Each paragraph in descriptive code documentation has only one
topic. The topic sentence is the first and most important sentence; it gives new
information and makes a logical connection to previous information (via a key
word and/or connecting word). If you write down the topic sentences of a
document, you get a good outline of its content.

**Why.** The topic sentence lets the developer find applicable information
quickly. When a paragraph drifts to a second topic, the reader loses the thread.
Rule 6.4 tells you to use paragraphs; Rule 6.5 tells you each paragraph gets one
topic.

**Example (auth middleware — one function, three topics).**

Non-STE (five topics in one sentence):
> The authentication middleware validates each request and the logging system
> records all validation failures to the audit trail while the response pipeline
> returns JSON error bodies with error codes and the database connection pool
> maintains idle connections for reuse and the configuration module reloads
> settings when the manifest file changes on disk.

STE (three single-topic paragraphs; topic sentences form an outline):
> The authentication middleware validates each incoming request. The middleware
> reads the bearer token from the `Authorization` header. It sends the token to
> the `validateToken` function ... Then it compares the `exp` claim ...
> If the token is expired, the middleware returns a `401 Unauthorized` response.
> The response body is a JSON object ... If the token is malformed, the middleware
> returns a `401 Unauthorized` response ...
> The middleware also logs each failure to the audit trail. It calls the
> `AuditLogger.log` static method ...

Outline from topic sentences: "The authentication middleware validates each
incoming request." / "If the token is expired, the middleware returns a `401
Unauthorized` response." / "The middleware also logs each failure to the audit
trail."

**Per-context guidance.** The "topic" definition changes with format, but one
topic per paragraph is constant.
- README: "What it does", "How to install", "How to configure", "How to
  contribute" are separate paragraphs.
- API docs: one paragraph for endpoint purpose, one for request format, one per
  response status group (success / client error / server error), one for auth.
- Docstrings: the topic is the function's contract (inputs, outputs, behavior) —
  do not explain why the function exists, side effects of other functions, or
  list callers.
- Commit messages: one commit = one topic; split unrelated changes into separate
  commits.
- Error messages: a one-topic paragraph — what went wrong, why, how to fix; put
  stack traces in a log, not the message.

**Paradigm-specific.**
- OOP: one paragraph per concern — class purpose, constructor, public interface,
  inheritance/interface, thread-safety. Method implementation detail belongs in
  the method docstring.
- Functional: one paragraph for input shape, transformation logic, output shape,
  edge cases; document each pipeline stage in its own paragraph.
- Procedural: one paragraph per phase — init, main loop, cleanup, error handling.
- Declarative: one paragraph per table/view, per Terraform resource, per K8s
  object (Deployment and its Service are separate topics even if related).
- Systems: one paragraph per ownership relationship or memory lifecycle
  (allocation, transfer, deallocation, unsafe invariants).

**Edge cases.**
- Framework name = unapproved word (e.g. "Execute" library): it is a technical
  noun, allowed; but do not use it as a verb in the same paragraph ("Use the
  `Execute` library to run background jobs.", not "Execute background jobs with
  the `Execute` library.").
- Large multi-topic legacy functions: use the docstring as a bullet-point topic
  index; give each responsibility its own paragraph in module-level docs.
- Generated API docs: each individual docstring must still follow the one-topic
  rule because the tool only combines them.
- Cross-cutting concerns (security, performance, accessibility): give them their
  own document/section with a one-paragraph summary + link per module.
- Error-code reference tables: the table is one container; each description cell
  is a mini-paragraph describing only one error condition.

**Grammar notes.** Always use deductive paragraphs (topic sentence first) — a
topic sentence at the end is invisible to a scanning reader. Repeat the key word
(or approved synonym) from the topic sentence in supporting sentences; a new
unconnected key word means drift. Use connecting words in the topic sentence:
"Also" (same topic, new angle), "However" (contrast), "For example" (instance),
"Therefore" (result). A paragraph is 3–7 sentences; a 10+ sentence paragraph
almost always has multiple topics. Separate paragraphs with a blank line (not
indentation-only).

**See also.** Rule 6.1, 6.2, 6.3, 6.4; Rule 1.11 (one term per concept); Rule
3.6 (approved verb forms); Rule 5.1 (imperative instructions); Rule 6.6 (≤6
sentences per paragraph).

---

## Rule 6.6 — Make Sure That No Paragraph Has More Than Six Sentences

Adapted from ASD-STE100 Issue 9, Rule 6.6.

**Core rule.** In code documentation, no paragraph has more than six sentences.
Paragraphs divide a block into logical units and keep the reader's attention. If
a paragraph has more than six sentences, divide it into two smaller paragraphs.
The six-sentence limit is a practical ceiling, not a target — most good
paragraphs use two to four sentences.

**Relationship to 6.4 and 6.5.** Rule 6.4 says use paragraphs; Rule 6.5 says
each paragraph has one topic; Rule 6.6 says don't let a paragraph grow past six
sentences. The three together produce short, single-topic paragraphs.

**When to split a paragraph.**
- It has more than six sentences.
- It covers two or more topics (Rule 6.5).
- A sentence introduces a new key word the earlier sentences don't use (Rule 6.2).
When splitting, group sentences that share a key word in the first paragraph;
start the new paragraph with a topic sentence that names the new key word.

**Code-domain examples.**
- ConnectionPool docstring: the Non-STE version packs four components (socket
  connections, reaper thread, bounded queue, metrics collector) into one 5-sentence
  paragraph; the STE version uses one outline paragraph + four short paragraphs,
  each under six sentences.
- POST /orders handler: the Non-STE version crams the whole lifecycle into one
  one-paragraph sentence; the STE version uses four paragraphs (parse, authorize,
  act, fail), each two to four sentences.
- AuthModule: five responsibilities in one paragraph → six paragraphs, each under
  six sentences, one topic per paragraph.
- Migration `upgrade()`: seven changes in one sentence/paragraph → six short
  paragraphs.
- Changelog v3.1.0: five unrelated changes in one paragraph → one short paragraph
  per change type; mark the API removal with DEPRECATED.

**Per-context guidance.**
- README: keep each feature description to a short paragraph; split
  install/configure/verify into separate paragraphs.
- API docs: keep each endpoint description short — purpose, request, response,
  errors each in its own paragraph under six sentences.
- Docstrings: keep the summary paragraph short; one short paragraph per concern
  (params, returns, raises); move a long parameter list to a bulleted list.
- Error/log diagnostics: a multi-line diagnostic block stays to six lines or
  fewer, or splits into a cause paragraph and a recovery paragraph.

**Paradigm-specific.** OOP: one responsibility per paragraph (e.g. each phase of
the order lifecycle). Functional: one pipeline stage per paragraph. Procedural:
one phase per paragraph (build/rollout/verify/fail). Declarative: one
resource/block per paragraph. Systems: one ownership rule per paragraph (memory
contracts are easy to bury in a long one).

**Edge cases.**
- A topic that needs >6 sentences: keep each paragraph under six sentences and
  continue the same topic in a second paragraph, starting it with "Also," or "In
  addition," (e.g. the garbage-collector description spans two paragraphs).
- A bulleted/numbered list is ONE paragraph regardless of item count. Rule 6.6
  limits the surrounding prose sentences, not the number of list items. Keep the
  intro sentence short; don't add a long closing sentence restating every item.
- Generated docs that emit one long paragraph per symbol: if you can't change the
  generator, add a short human-written summary above the block; the generated
  block is exempt only if you don't edit its source annotations.
- A short paragraph can still violate 6.5 by mixing two topics (e.g. three
  sentences covering both "cache" and "queue") — Rule 6.6 (sentence count) and
  6.5 (topic count) are independent; split even if under the limit.

**Grammar notes.** The six-sentence limit comes from reading psychology: the
topic fades from working memory after ~6 sentences, causing re-reading. Rule 6.6
counts sentences, not words — a paragraph can have six long or six short
sentences and still pass, but six 25-word sentences is at the edge of
readability; prefer 2–4 sentences. Lists/tables inside a paragraph don't add to
the surrounding prose sentence count. In procedural writing each step is its own
paragraph by convention, so 6.6 rarely applies — except when a step has a long
note/rationale (keep it under six sentences or move it to a note paragraph).

**See also.** Rule 6.4, 6.5, 6.1, 6.2, 6.3.

---

## Quick reference for LLM documentation generation

Apply this checklist to any code documentation you produce:

1. **6.1 Gradual** — one subject per sentence; split compound sentences at
   coordinating/subordinating conjunctions and relative clauses.
2. **6.2 Key words** — repeat the same technical noun/term as the key word
   across sentences; use approved connectors (`and`, `but`, `then`, `thus`,
   `also`, `however`, `therefore`, `for example`) at sentence start.
3. **6.3 Short** — every descriptive sentence ≤ 25 words (hyphenated terms,
   acronyms, and code tokens each count as one word).
4. **6.4 Paragraphs** — start each paragraph with a topic sentence; group
   related sentences; separate Installation/Config/Usage/API/etc.
5. **6.5 One topic** — each paragraph covers exactly one topic; topic sentences
   alone should outline the document.
6. **6.6 ≤6 sentences** — no paragraph exceeds six sentences; prefer 2–4; a list
   is one paragraph.

Cross-links within the standard: Section 1 (Vocabulary: approved words, technical
nouns, one term per concept), Section 3 (Verb forms), Section 5 (Imperative
instructions), Section 7 (Lists for three or more items). These six rules form
the sentence-and-paragraph backbone of STE-Code; they are necessary but not
sufficient — pair them with the vocabulary and writing-style rules for full
compliance.
