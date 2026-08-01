# Level 3 — Section 6: Sentence and Paragraph Structure

This slice covers STE-Code Rules 6.1 through 6.6. It is the structural layer of
the standard: how to shape sentences and paragraphs in code documentation so that
a developer can read and understand it on the first pass.

These rules apply to every form of code documentation: README files, API reference
docs, docstrings, inline comments, commit messages, error messages, log entries,
changelogs, and configuration files.

## How to use this slice

- Apply the rules in order 6.1 → 6.2 → 6.3 → 6.4 → 6.5 → 6.6. Each refines the
  output of the previous one.
- 6.1 splits compound thoughts into one subject per sentence.
- 6.2 threads key words through the resulting sentences so they stay connected.
- 6.3 keeps every sentence at 25 words or fewer.
- 6.4 groups related sentences into paragraphs that open with a topic sentence.
- 6.5 keeps each paragraph to a single topic.
- 6.6 keeps each paragraph to six sentences or fewer.

## Rules at a glance

| Rule | One-line requirement | Hard limit |
|------|----------------------|------------|
| 6.1 Give Information Gradually | One subject per sentence; introduce one fact at a time. | No compound multi-subject sentences. |
| 6.2 Use Key Words and Key Phrases | Repeat the key term across sentences; use approved connectors. | Connectors from the approved set only. |
| 6.3 Write Short Sentences | Keep each sentence short and single-idea. | 25 words maximum per sentence. |
| 6.4 Use Paragraphs for Related Info | Group related sentences; open with a topic sentence. | One topic sentence per paragraph. |
| 6.5 One Topic per Paragraph | A paragraph covers exactly one topic. | No topic drift within a paragraph. |
| 6.6 Six Sentences Max per Paragraph | Cap paragraph length to preserve the thread. | 6 sentences maximum per paragraph. |

---

## Rule 6.1 — Give Information Gradually

In code documentation, give information gradually and make sure that each sentence
contains only one subject. If you give too much information too quickly, your
documentation will not be easy to understand, and the reader must read it again.

Give the reader one piece of information at a time. Do not combine multiple
actions, multiple conditions, or multiple subjects in one sentence.

### Core requirement

- One subject per sentence. The subject is the noun phrase that performs the
  action of the main verb.
- One action per sentence where the verbs share that subject. "The function
  validates input and returns a result" is acceptable (one subject, two verbs).
- Two subjects require two sentences: "The function validates input. The
  middleware logs the result." — not "...and the middleware logs..."

### Code-domain example

Non-STE (one dense sentence, multiple subjects and actions):

> The authentication middleware validates bearer tokens from the authorization
> header by calling the `validateToken` function in the security module which
> decodes the JWT payload using the `HS256` algorithm from the `jwt-signer`
> library and checks the `exp` claim against the current server time before
> extracting the `sub` and `role` claims and attaching them as properties on the
> `request.auth` object, and if the token is expired or malformed the middleware
> returns a `401 Unauthorized` response with a JSON error body containing a
> `message` field and an `errorCode` field set to `TOKEN_EXPIRED` or
> `TOKEN_MALFORMED` respectively, while also logging the failure to the audit
> trail via the `AuditLogger.log` static method which writes to the
> `audit_events` table.

STE (one subject, one action per sentence):

> The authentication middleware validates each incoming request. The middleware
> reads the bearer token from the `Authorization` header. It sends the token to
> the `validateToken` function in the `security` module. The `validateToken`
> function decodes the JWT payload. It uses the `HS256` algorithm from the
> `jwt-signer` library. Then it compares the `exp` claim with the current server
> time. If the token is not expired and not malformed, the function gets the
> `sub` and `role` claims. It attaches these claims as properties on the
> `request.auth` object. If the token is expired, the middleware returns a `401
> Unauthorized` response. The response body is a JSON object:
> - The `message` field contains a description of the error.
> - The `errorCode` field is set to `TOKEN_EXPIRED`.
> If the token is malformed, the middleware returns a `401 Unauthorized`
> response. The `errorCode` field in the response is set to `TOKEN_MALFORMED`.
> The middleware also logs each failure to the audit trail. It calls the
> `AuditLogger.log` static method. This method writes a record to the
> `audit_events` table in the primary database. The write uses an asynchronous
> pattern that does not block the response pipeline.

### How it applies by documentation type

- **README.** Introduce one concept per section. Three separate sections for
  purpose, install, and usage — not one paragraph mixing all three.
- **API docs.** Describe the method and path in one sentence; one sentence per
  parameter; one sentence per response field or status code.
- **Docstrings / inline comments.** One behavior per sentence. Each parameter and
  each return condition gets its own sentence.
- **Commit messages.** One logical change per commit. Split a compound change
  into a summary line plus bullet points.
- **Error messages / logs.** One problem per message with a distinct error code.
  One event per log line.
- **Changelogs.** One change per entry; separate feature, fix, and deprecation.

### Paradigm-specific guidance

- **Object-oriented.** Describe one method or one class behavior per sentence.
  For override chains: base class first, then the override, then the side effect.
- **Functional.** Describe one transformation per sentence. A `>>=` or pipe chain
  becomes one sentence per step.
- **Procedural (C, Go, Bash).** One step or one branch per sentence. Do not
  combine an if-else chain, a loop body, and cleanup into one sentence.
- **Declarative (SQL, Terraform, K8s YAML).** One resource, constraint, or column
  per sentence. Do not describe the resource and all its relationships in one
  sentence.
- **Systems (Rust ownership, C memory).** One ownership rule, lifetime, or memory
  operation per sentence. Separate allocation, transfer, annotation, and
  deallocation into distinct sentences.

### Edge cases

- **Framework names with multiple concepts** (e.g. `UserAuthenticationService`):
  treat the whole identifier as one technical noun. Do not split it; apply the
  rule to the surrounding prose.
- **Generated documentation** (OpenAPI, JSDoc, Sphinx): if you cannot change the
  output, add a plain-language summary above it that follows Rule 6.1.
- **Control-flow keywords** (`if`, `else`, `while`, `try/catch`): one sentence
  per branch. Describe the try block and the catch block in separate sentences.
- **Brevity contexts** (CLI `--help`, error codes): use the minimum number of
  sentences, but each must still have one subject. Use fragments only when the
  display format enforces them.
- **Rewriting existing docs:** if a compound sentence hides a dependency, describe
  the dependency first, then the dependent step.

### Connects to

Rule 6.2 (thread the split sentences with key words) · Rule 6.3 (then check the
25-word limit) · Rule 6.4 (group the short sentences into paragraphs) · Rule 6.5
(one topic per resulting paragraph) · Rule 1.1 (use approved words) · Rule 1.11
(one term per concept).

---

## Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure

In code documentation, use key words and key phrases to connect related ideas
across sentences. Key words are terms that occur multiple times to link concepts.
Key phrases are multi-word expressions that serve the same connecting function.

These key words and phrases show how information is related and give the
documentation a logical structure. Do not change them in your text — the same
terminology keeps the documentation clear and correct.

### Approved connecting words and phrases

Use these at the start of a sentence so the reader sees the signal before the
content:

- **Connecting words:** `and`, `but`, `then`, `thus`, `also`, `however`,
  `therefore`.
- **Connecting phrases:** `for example`, `as a result`, `at the same time`.

Do **not** use `moreover`, `furthermore`, `nevertheless`, `subsequently`, or the
verbs `utilize` / `leverage` as connectors — they are not in the approved set.

### Core technique: repeat the key word

Pick the subject of the block (a class name, function name, parameter name,
resource name, or concept such as "middleware") and use it as the key word.

- Repeat it in the subject position of consecutive sentences.
- A pronoun (`it`, `they`) may refer back once, but after two sentences repeat the
  full key word to avoid ambiguity.
- Keep multi-word key phrases intact: "connection pool", "rate limiter",
  "retry policy". Do not shorten them to "pool" mid-documentation.

**Example chain:**

> The authentication middleware validates each incoming request.
> The middleware reads the bearer token from the `Authorization` header.
> It sends the token to the `validateToken` function in the `security` module.
> The `validateToken` function decodes the JWT payload.
> It uses the `HS256` algorithm from the `jwt-signer` library.

"middleware" and "validateToken" recur, so the reader follows the flow.

### How it applies by documentation type

- **README.** Repeat the project name, library name, and core concept across
  sections. Do not switch to "the library" or "this tool" later.
- **API docs.** Use function names, parameter names, and return-type names as key
  words. Consistent key words prevent the reader losing track of which parameter a
  sentence describes.
- **Docstrings.** Introduce the function or class name as the key word in the
  first sentence. Do not switch to synonyms like "transmit", "data", or "queue".
- **Commit messages.** Use the component name and action verb as key phrases. Do
  not switch to "conn pool" or "connection manager" within the same message.
- **Error messages.** Use the operation name and resource name as key words. A
  follow-up message must reuse the resource name, not switch to "document" or
  "path".

**Cross-type consistency:** the same key word must carry the same meaning across
all documentation types in a project (Rule 1.11). If the README says
"authentication middleware", the API docs and docstrings must say the same.

### Paradigm-specific guidance

- **Object-oriented.** Use class names, method names, property names as key words.
  For a method chain, repeat the return type as the key word.
- **Functional.** Use type names, function names, data constructors. The value
  that flows through transformations is the key word.
- **Procedural (C, Go, Bash).** Use variable names, struct fields, error codes.
  Each step must refer to the same variable by the same name.
- **Declarative (SQL, Terraform, K8s YAML).** Use resource names, column names,
  attribute names so the reader maps sentences to exact identifiers.
- **Systems (Rust ownership, C memory).** Use ownership terms, lifetime names,
  pointer names. Precision here prevents bugs.

### Edge cases

- **Framework name conflicts with an unapproved word** (e.g. a library named
  `Leverage`): it is a technical code noun (Rule 1.5). Use it as-is; do not replace
  with an STE synonym.
- **Code keyword too short to be a key word** (Go `go`, Rust `mut`): use a longer
  descriptive key phrase that includes it (e.g. "the `go` keyword starts a
  goroutine" — key word is "goroutine").
- **Generated code** (protobuf, OpenAPI, ORM): use the generated type names as key
  words even if verbose; do not abbreviate.
- **Multi-language repos:** choose one key word for a shared concept (e.g. "map";
  Python `dict`, Java `HashMap`, Go `map`) and note the language-specific names
  once.
- **Multi-word key phrases:** keep the full phrase as the key unit.

### Grammar notes

Rule 6.2 applies *lexical cohesion* to code docs: repetition, pronoun reference,
and approved synonym ties bind sentences into a chain. Keep one stable topic (key
word) in the subject position of every sentence in a block. Connecting words are
grammatical signals placed at the sentence start:

- `and` — addition about the same key word.
- `but` — contrast.
- `then` — next step involving the key word.
- `thus` / `therefore` — consequence.

A **dangling key word** (introduced once, never repeated) breaks the structure.
Repeat the important terms.

### Connects to

Rule 6.1 (the sentences to thread) · Rule 6.3 (short sentences keep key words
visible) · Rule 6.4 (a paragraph is a group of sentences that share a key word) ·
Rule 6.5 (the one topic is the key word) · Rule 1.5 (technical code nouns allowed)
· Rule 1.8 (use standard technical nouns) · Rule 1.9 (prefer short clear nouns) ·
Rule 1.11 (one term per concept).

---

## Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence.

Good code documentation uses short sentences for complex topics. Short sentences
give a clear structure and make information easier to understand. In descriptive
code documentation, the maximum sentence length is 25 words.

### Core requirement

- Keep every descriptive sentence at 25 words or fewer.
- A sentence under 25 words can still be too dense if it packs multiple subjects —
  apply Rule 6.1 first, then count words.
- The 25-word limit indirectly limits clause density: a long sentence with several
  clauses overloads working memory.

### Code-domain example

Non-STE (32 words, one sentence):

> The configuration loader reads the YAML manifest file from the filesystem and
> parses it into an in-memory representation that other modules can query at runtime
> to determine their operational parameters.

STE (four sentences, each under 25 words):

> The configuration loader reads the YAML manifest file from the filesystem. It
> parses the file into an in-memory representation. Other modules can query this
> representation at runtime. They use it to find their operational parameters.

### How it applies by documentation type

- **README.** One sentence for the project, one for prerequisites, one for the
  install command. A reader scans and finds each without parsing a dense paragraph.
- **API docs.** One short sentence per part: endpoint, each parameter, each
  response field, each status code.
- **Docstrings.** One sentence for purpose, one per parameter, one for the return
  value, one per exception. Each under 25 words.
- **Commit messages.** Subject line under 72 characters; one short sentence per
  logical change in the body. Makes `git log` and `git bisect` readable.
- **Error messages.** Two short sentences: the problem, then the action. Each
  under 25 words. Log lines stay easy to search.

### Paradigm-specific guidance

- **Object-oriented.** Break inheritance and behavior into separate sentences. A
  class with many methods gets one sentence per method, not one sentence for all.
- **Functional.** Split composition from error behavior: describe the pipeline,
  then the short-circuit, then the error accumulator — each its own sentence.
- **Procedural (C, Go, Bash).** Each step is naturally one sentence. For
  safety-critical detail, split allocation from copy, copy from return.
- **Declarative (SQL, Terraform, K8s YAML).** Document each resource block and
  each argument in its own sentence. Do not mix properties in one 28-word sentence.
- **Systems (Rust ownership, C memory).** Short sentences are essential for memory
  models and concurrency guarantees. Split borrowing, lifetime tracking, and
  compile-time checks into separate sentences.

### Edge cases

- **Long technical terms** (e.g. "single sign-on", "continuous integration and
  continuous deployment"): count the phrase as one word. If it pushes the sentence
  over 25, use the acronym after the first mention.
- **Verbose code keywords** (`synchronized`, `concurrent.futures`,
  `__attribute__((constructor))`): count the keyword as one word, but keep the rest
  short.
- **Compound type signatures** (TypeScript generics, Rust trait bounds): one
  sentence for the type shape, one for the constraints, one for the behavior.
- **Legal / license text** (MIT, Apache, GPL, copyright): exempt from the 25-word
  limit. Surrounding explanation still obeys it.
- **Generated documentation** (JSDoc, Sphinx, `go doc`): the generator may produce
  long sentences; fix the source docstrings, not the generated output.

### Grammar notes

- **Clause density:** most English clauses are 6–12 words. A 25-word sentence holds
  at most two clauses with connecting words — matching working-memory capacity.
- **Coordination vs. subordination:** prefer coordination across separate sentences
  over deep subordination. "The `parse` function throws a `SyntaxError`. This error
  occurs when the input string contains invalid JSON." beats a 27-word sentence with
  three levels of subordination.
- **Implicit connectives:** short sentences in documentation order (purpose → usage →
  edge cases) need no explicit glue; the reader infers the relationship.
- **Counting rules:** count hyphenated compounds as one word ("least-recently-used"
  = 1). Count acronyms as one word (JSON = 1). Count code tokens as one word
  (`Result<Vec<T>>` = 1). Do not count parenthetical word-count notes ("(12
  words)") in examples.

### Connects to

Rule 6.1 (short sentences enable gradual delivery) · Rule 6.2 (short sentences make
key words visible) · Rule 6.4 (short sentences form clear paragraphs) · Rule 6.5
(short sentences help each paragraph stay on topic) · Rule 1.1 (short sentences
reduce the need for complex vocabulary) · Rule 1.10 (short sentences expose jargon).

---

## Rule 6.4 — Use Paragraphs to Show Related Information

In descriptive code documentation, paragraphs keep related information together and
give a logical sequence to the text. A paragraph starts with a **topic sentence**
that tells the developer the topic. The sentences that follow explain or expand it.

When a new paragraph starts, the reader knows there will be a new topic or different
information.

### Core requirement

- Start each paragraph with a topic sentence in the simple present tense, naming the
  topic (a class, function, module, or concept) in subject position.
- Keep related sentences together; use paragraph breaks to separate different
  subjects or different phases of a process.
- Do not start a paragraph with a subordinate clause ("Because...", "When...",
  "If...", "Although..."). Start with the subject.

### Code-domain example

Non-STE (one dense paragraph, mixed topics):

> The data pipeline processes incoming events through a sequence of stages. Each
> stage transforms the event payload and passes it to the next stage. The first
> stage is validation, which checks the event schema and rejects malformed events.
> The second stage is enrichment, which adds metadata such as timestamps, source
> identifiers, and geolocation data from an external lookup service. The third
> stage is transformation, which converts the event into the target format required
> by downstream consumers such as the analytics warehouse and the real-time
> dashboard. The final stage is persistence, which writes the transformed event to
> the primary data store and to the event log for audit purposes. Error handling is
> implemented at each stage to catch exceptions without breaking the entire
> pipeline.

STE (each topic gets its own paragraph with a topic sentence):

> **1. Data Pipeline Overview**
> The data pipeline processes incoming events through a sequence of stages. Each
> stage transforms the event payload and passes it to the next stage. Error
> handling is implemented at each stage to catch exceptions without breaking the
> pipeline.
>
> **2. Validation Stage**
> The first stage is validation. This stage checks the event schema. It rejects
> events that are malformed.
>
> **3. Enrichment Stage**
> The second stage is enrichment. This stage adds metadata to the event:
> - Timestamps
> - Source identifiers
> - Geolocation data from an external lookup service.
>
> **4. Transformation Stage**
> The third stage is transformation. This stage converts the event into the target
> format. Downstream consumers use this format. These consumers include:
> - The analytics warehouse
> - The real-time dashboard.
>
> **5. Persistence Stage**
> The final stage is persistence. This stage writes the transformed event to two
> destinations. It writes the event to the primary data store. It also writes the
> event to the event log for audit purposes.

### How it applies by documentation type

- **README.** Each section starts with a clear topic sentence. Use section headings
  for major topics; paragraph breaks for sub-topics. Move install, configuration,
  and dependencies to separate paragraphs/sections.
- **API docs.** Each endpoint description starts with a topic sentence stating what
  it does. Give authentication, query parameters, response, and status codes
  separate paragraphs (or sub-sections).
- **Docstrings / inline comments.** A docstring starts with a one-line topic
  sentence, then a blank line, then more paragraphs. Each paragraph covers one
  sub-topic (parameters, returns, exceptions, side effects, examples). Inline
  comments are one-sentence paragraphs that state the topic of the following code.
- **Commit messages.** The first line is the topic sentence. The body uses
  paragraphs to group the problem, the changes, and the monitoring notes.
- **Error messages.** Multi-line error output uses paragraphs to separate the error
  description, the diagnostic items, and the stack trace.

### Paradigm-specific guidance

- **Object-oriented.** Separate class purpose, constructor details, public API, and
  internal design into paragraphs. Document each method as a paragraph group.
- **Functional.** Separate the type signature, the behavior, the purity note, and
  the internal composition into paragraphs. Document each pipeline stage separately.
- **Procedural (C, Go, Bash).** Separate initialization, the main loop, cleanup, and
  error handling into paragraphs (phases of execution).
- **Declarative (SQL, Terraform, K8s YAML).** Give each resource or constraint its
  own paragraph group. Separate resource identity, specification, and dependencies.
- **Systems (Rust ownership, C memory).** Separate each ownership relationship or
  memory lifecycle into its own paragraph.

### Edge cases

- **Auto-generated documentation** (JSDoc, Sphinx, `go doc`): insert a blank comment
  line between topics so the generator emits separate paragraphs.
- **Multi-author documents:** apply structural linting. Flag paragraphs over 5
  sentences or lacking a topic sentence. Break long paragraphs at topic boundaries.
- **Cross-cutting concerns** (security, performance): give them their own document or
  top-level section; in each module write a one-paragraph summary with a link.

### Grammar notes

- **Topic sentence as anchor:** the topic sentence carries the main clause; the
  following sentences carry subordinate information. It must be declarative,
  simple present, naming the topic in subject position.
- **Paragraph length:** most STE paragraphs have 2–4 sentences. A paragraph over 5
  sentences usually covers more than one topic — split it.
- **Paragraph breaks as signals:** place a break before a new concept, a code
  example, a warning, a list, or a change in abstraction level. Do not break between
  a topic sentence and its supporting sentences.
- In markdown, separate paragraphs with a blank line (not indentation alone).

### Connects to

Rule 6.1 (paragraphs implement the gradual sequence at section level) · Rule 6.2
(topic sentences use key words) · Rule 6.3 (short sentences make paragraphs
readable) · Rule 6.5 (one paragraph, one topic) · Rule 1.1 (topic sentences use
approved words) · Rule 1.5 (technical nouns allowed in topic sentences) · Rule 1.11
(one term per concept across paragraphs) · Rule 7.1 (use lists for three or more
items).

---

## Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic

In descriptive code documentation, paragraphs describe topics, and each paragraph
must have only one topic. The topic sentence is the first and most important
sentence in a paragraph. The other sentences add more information on that topic.

If you write down the topic sentences of a text, you get a good outline of its
content. The reader finds applicable information quickly.

### Core requirement

- One paragraph = one topic. The topic sentence names that topic.
- A paragraph that covers two topics must be split, even if it is short.
- The topic sentence usually contains a key word (Rule 6.2) and/or a connecting word
  (Rule 6.2) to link to the previous paragraph.
- Use deductive structure: the topic sentence is first, never last (developers scan).

### Code-domain example

Non-STE (five topics in one sentence):

> The authentication middleware validates each request and the logging system records
> all validation failures to the audit trail while the response pipeline returns JSON
> error bodies with error codes and the database connection pool maintains idle
> connections for reuse and the configuration module reloads settings when the
> manifest file changes on disk.

STE (three single-topic paragraphs; reading only the topic sentences gives the
outline):

> The authentication middleware validates each incoming request. The middleware reads
> the bearer token from the `Authorization` header. It sends the token to the
> `validateToken` function in the `security` module. The `validateToken` function
> decodes the JWT payload using the `HS256` algorithm from the `jwt-signer` library.
> Then it compares the `exp` claim with the current server time. If the token is not
> expired and not malformed, the function gets the `sub` and `role` claims and
> attaches them to the `request.auth` object.
>
> If the token is expired, the middleware returns a `401 Unauthorized` response. The
> response body is a JSON object with a `message` field and an `errorCode` field set
> to `TOKEN_EXPIRED`. If the token is malformed, the middleware returns a `401
> Unauthorized` response with the `errorCode` field set to `TOKEN_MALFORMED`.
>
> The middleware also logs each failure to the audit trail. It calls the
> `AuditLogger.log` static method. This method writes a record to the `audit_events`
> table in the primary database. The write uses an asynchronous pattern that does not
> block the response pipeline.

Outline from topic sentences: (1) "The authentication middleware validates each
incoming request." (2) "If the token is expired, the middleware returns a `401
Unauthorized` response." (3) "The middleware also logs each failure to the audit
trail."

### How it applies by documentation type

- **README.** One topic per section: "Installation" explains install only, not API
  design; "Configuration" shows config only, not usage.
- **API docs.** One paragraph per aspect: endpoint purpose, request format, each
  response status group, authentication. Do not mix `200 OK` with `404 Not Found`.
- **Docstrings / inline comments.** The docstring topic is the function's contract:
  inputs, outputs, behavior. Do not explain why it exists or list its callers.
- **Commit messages.** One commit = one topic. Two unrelated changes belong in two
  commits. The subject line summarizes the single topic; the body expands only on it.
- **Error messages.** One topic: what went wrong (one sentence), why (one sentence),
  how to fix (one sentence). No stack traces or unrelated state in the message body.

### Paradigm-specific guidance

- **Object-oriented.** One paragraph per concern: class purpose, constructor,
  public interface, inheritance, thread safety. Method implementation details go in
  the method docstring.
- **Functional.** One paragraph per transformation: input shape, transformation
  logic, output shape, edge cases. Document each pipeline stage separately.
- **Procedural (C, Go, Bash).** One paragraph per phase: initialization, main loop,
  cleanup, error handling. Do not merge `setup` with `teardown`.
- **Declarative (SQL, Terraform, K8s YAML).** One paragraph per table/view,
  resource block, or object. A Deployment and its Service are separate topics even
  though they work together.
- **Systems (Rust ownership, C memory).** One paragraph per ownership relationship or
  memory lifecycle. Allocation and deallocation share a paragraph only when they are
  one lifecycle (e.g. RAII).

### Edge cases

- **Framework names that are unapproved words** (e.g. a library named `Execute`):
  technical code noun (Rule 1.5), allowed. But do not use it as a verb in the same
  paragraph — write "Use the `Execute` library to run jobs", not "Execute jobs with
  `Execute`".
- **Large multi-topic functions:** list responsibilities as bullet points in the
  docstring; give each its own paragraph in module-level docs. The docstring is a
  topic index.
- **Generated documentation:** each individual docstring must still be a self-contained
  topic even though the page combines many.
- **Cross-cutting concerns:** give them their own document/section; in each module
  write a one-paragraph summary with a link.
- **Error-code reference tables:** the table is the container; each descriptive cell
  is a mini-paragraph that covers one error condition.

### Grammar notes

- **Topic sentence position:** always first (deductive). A topic sentence at the end
  is invisible to a scanning reader.
- **Key word repetition:** the topic sentence introduces a key word; supporting
  sentences repeat it or use a clear synonym. A new key word without connection means
  the paragraph has drifted.
- **Connecting words in the topic sentence:** "Also," (more on same topic), "However,"
  (contrast), "For example," (instance), "Therefore," (result).
- **Paragraph length:** 3–7 sentences. A 10+ sentence paragraph almost always has more
  than one topic.
- **Visual separation:** in markdown, separate paragraphs with a blank line; screen
  readers and renderers do not treat indentation as a break.

### Connects to

Rule 6.1 (gradual information) · Rule 6.2 (key words in topic sentences) · Rule 6.3
(short sentences make topic drift visible) · Rule 6.4 (paragraphs group related
info) · Rule 1.11 (consistent terms prevent false topic starts) · Rule 3.6 (topic
sentence usually starts with a simple-present verb) · Rule 5.1 (imperative procedural
paragraphs) · Rule 6.6 (six-sentence cap).

---

## Rule 6.6 — Make Sure That No Paragraph Has More Than Six Sentences

In code documentation, make sure that no paragraph has more than six sentences.
Paragraphs divide a documentation block into logical units and keep the developer's
attention. If a paragraph is too long, it cannot do this. Do not put different
topics in the same paragraph (see Rule 6.5). If a paragraph has more than six
sentences, divide it into two smaller paragraphs.

### Core requirement

- Cap each paragraph at six sentences. This is a ceiling, not a target — most good
  paragraphs use two to four sentences.
- Rule 6.6 works with 6.4 (use paragraphs) and 6.5 (one topic): 6.4 says use
  paragraphs, 6.5 says one topic each, 6.6 says keep them short.
- Split a paragraph when: it has more than six sentences, OR it covers two or more
  topics (Rule 6.5), OR a sentence introduces a new key word not used earlier (Rule
  6.2).

### Code-domain example

Non-STE (four components in one five-sentence paragraph):

> The connection pool manager has these primary components: a set of pre-allocated
> socket connections that the manager reuses across requests to avoid repeated TCP
> handshakes and TLS negotiation, a background reaper thread that closes idle
> connections and runs a periodic health probe, a bounded queue that holds pending
> acquire requests and rejects with a timeout error, and a metrics collector that
> records active connections and wait-time distribution for observability.

STE (one outline paragraph plus four short paragraphs, each under six sentences):

> The connection pool manager has these primary parts:
> - A set of pre-allocated socket connections.
> - A background reaper thread.
> - A bounded queue for pending acquire requests.
> - A metrics collector.
>
> The socket connections let the application reuse one link for many requests. The
> reuse avoids repeated TCP handshakes and TLS negotiation.
>
> The reaper thread closes connections idle longer than the idle timeout. The reaper
> thread also runs a periodic health probe to find dropped links.
>
> The bounded queue holds pending acquire requests when all connections are in use.
> The queue rejects new requests with a timeout error after the acquire timeout
> expires.
>
> The metrics collector records the number of active connections. The collector also
> records the wait-time distribution and the count of rejected acquires. The
> observability stack reads these metrics.

### How it applies by documentation type

- **README.** One feature = one short paragraph. A feature paragraph listing install,
  configure, and usage in eight sentences forces three topics at once — split them.
- **API docs.** One short paragraph per aspect: purpose, request, response, errors.
- **Docstrings.** Keep the summary paragraph short. One short paragraph per concern;
  move a long parameter list to a bulleted list and keep the prose under six
  sentences.
- **Error messages / logs.** An error message is usually one sentence; keep a
  multi-line diagnostic block to six lines or fewer, or split into a cause paragraph
  and a recovery paragraph.

### Paradigm-specific guidance

- **Object-oriented.** One responsibility per paragraph. Each collaborator of a class
  gets its own short paragraph.
- **Functional.** One transformation stage per paragraph; a map/filter/fold pipeline
  should not live in one paragraph.
- **Procedural (C, Go, Bash).** One phase per paragraph: setup, execution, cleanup.
  Do not document `setup` and `teardown` together.
- **Declarative (SQL, Terraform, K8s YAML).** One resource or block per paragraph; a
  module declaring a database, a cache, and a queue documents each separately.
- **Systems (Rust ownership, C memory).** One ownership rule per paragraph; memory
  contracts are easy to bury in a long paragraph.

### Edge cases

- **A topic needs more than six sentences:** keep the first paragraph under six
  sentences and continue the same topic in a second paragraph. Start the second with a
  connecting phrase ("Also,", "In addition,") so the reader knows the topic continues.
- **A list counts as one paragraph:** a bulleted/numbered list is one paragraph
  regardless of item count. Rule 6.6 limits the prose around it, not the list items.
  Keep the introductory sentence short; do not add a long closing sentence.
- **Generated docs that emit long paragraphs:** set the generator to break at sentence
  boundaries if you can. If you cannot, add a short human-written summary above the
  generated block; the summary must follow Rule 6.6. The generated block is exempt only
  if you do not edit its source annotations.
- **A short paragraph that mixes two topics:** Rule 6.6 and 6.5 are independent. A
  three-sentence paragraph describing both the cache and the queue must split even
  though it is under the sentence limit.

### Grammar notes

- **Why six:** a reader holds a paragraph's topic in working memory; after about six
  sentences the topic fades and they must re-read. The limit guards against drift.
- **Sentence count, not word count:** six short sentences or six long sentences both
  pass. Prefer two to four short sentences; apply Rule 6.3 together with 6.6.
- **Lists and tables reset the count:** the surrounding prose (introductory + closing
  sentence) is what counts. Keep that prose under six sentences.
- **Splitting technique:** split where the key word changes (Rule 6.2) or the topic
  changes (Rule 6.5). Start the new paragraph with a topic sentence naming the new key
  word.
- **Procedures:** each step is its own paragraph by convention, so 6.6 rarely applies;
  it applies when a step has a long note — keep the note under six sentences.

### Connects to

Rule 6.4 (6.6 is the size limit 6.4 assumes) · Rule 6.5 (6.6 limits sentence count,
6.5 limits topic count) · Rule 6.1 (short paragraphs support gradual delivery) · Rule
6.2 (the new paragraph starts with the new key word) · Rule 6.3 (short sentences make
it easier to stay under six).

---

## Applying Section 6 end to end (the pipeline)

When writing or checking documentation, apply the rules in sequence:

1. **6.1** — Split compound sentences so each has one subject and one action.
2. **6.2** — Thread the split sentences with repeated key words and approved connectors.
3. **6.3** — Check every sentence is 25 words or fewer.
4. **6.4** — Group related sentences into paragraphs opened by a topic sentence.
5. **6.5** — Verify each paragraph covers exactly one topic; split if it drifts.
6. **6.6** — Verify each paragraph has six sentences or fewer; split if longer.

A paragraph that passes 6.4, 6.5, and 6.6 is short, single-topic, and scannable. This
is the structural backbone that the vocabulary rules (Section 1) and the writing rules
(Sections 3, 5, 7) build on.

### Related rules outside Section 6

- Rule 1.1 — Use approved words from the STE-Code dictionary.
- Rule 1.5 — Technical code nouns are allowed.
- Rule 1.8 / 1.9 — Use standard, short, clear technical nouns as key words.
- Rule 1.10 — No slang, jargon, or regional terms.
- Rule 1.11 — One term per concept (keeps key words and topics stable).
- Rule 3.6 — Use approved forms of verbs.
- Rule 5.1 — Write instructions in the imperative mood.
- Rule 7.1 — Use lists for three or more items.
