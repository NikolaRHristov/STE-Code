# Level 4 — Section 6: Writing Practice (Rules 6.1–6.6)

This slice distills **Section 6 (Writing Practice)** of the STE-Code controlled
standard for people who use LLMs to generate code documentation. Section 1 controls
*which words* you may use. Section 6 controls *how you assemble them* — sentence
length, sentence structure, connective signals, and paragraph shape.

Section 6 applies to **descriptive** code documentation: README files, API reference
docs, docstrings, inline comments, commit messages, error messages, log entries,
changelogs, release notes, and configuration file comments. Procedural steps are
governed by Section 5; Section 6 still applies to any note or rationale inside a step.

## The six rules at a glance

| Rule | Requirement | Failure signal |
|---|---|---|
| 6.1 | Give information gradually. One subject per sentence. | Two independent clauses joined by `and`/`but`/`while`. |
| 6.2 | Use key words and key phrases for logical structure. Do not vary them. | The same concept named `client`, then `connection`, then `handle`. |
| 6.3 | Write short sentences. Maximum 25 words. | A sentence that needs a comma to be parsed at all. |
| 6.4 | Use paragraphs to show related information. Start with a topic sentence. | A wall of prose with no lead sentence. |
| 6.5 | Each paragraph has only one topic. | The topic sentences do not form an outline. |
| 6.6 | No paragraph has more than six sentences. | Seven or more sentences under one topic. |

The rules compose in order. Apply 6.1 to split compound sentences. Apply 6.3 to check
each resulting sentence against the 25-word limit. Apply 6.2 to connect them. Apply
6.4 to group them, 6.5 to keep each group single-topic, and 6.6 to cap the group size.

## Approved connectives

Use only these connecting words and phrases:

`and`, `but`, `then`, `thus`, `also`, `however`, `therefore`, `for example`,
`as a result`, `at the same time`.

Put the connective at the start of the sentence so the reader sees the signal before
the content. Do **not** use `moreover`, `furthermore`, `nevertheless`, `subsequently`,
`utilize`, or `leverage` as connectors. They are not in the approved set.

---

## Rule 6.1 — Give information gradually

**Rule.** In descriptive code documentation, give information gradually. Make sure that
each sentence contains only one subject. If you give too much information too quickly,
the documentation is not easy to understand, and the developer must read it again.

Do not combine multiple actions, multiple conditions, or multiple subjects in one
sentence.

### The single-subject test

The subject is the noun phrase that performs the action of the main verb.

- `The function validates the input and returns a result.` — **OK.** One subject, two
  verbs that share it.
- `The function validates the input and the middleware logs the result.` — **Split.**
  Two subjects. Write: `The function validates the input. The middleware logs the result.`

Conjunction guidance:

- **Coordinating** (`and`, `or`, `but`): if the conjunction joins two independent
  clauses, split at the conjunction. If it joins two verbs or two objects that share
  one subject, keep the sentence.
- **Subordinating** (`because`, `since`, `although`, `while`, `when`, `if`, `unless`):
  one main clause plus one dependent clause is acceptable, provided the dependent
  clause does not introduce a new subject with its own chain of actions.
- **Relative** (`which`, `that`, `who`): a relative clause that describes the main
  subject is acceptable. A relative clause that introduces a new subject and new
  actions must become its own sentence.

### Worked example — authentication middleware

> **Non-STE:** The authentication middleware validates bearer tokens from the
> authorization header by calling the `validateToken` function in the security module
> which decodes the JWT payload using `HS256` and checks the `exp` claim against the
> current server time before extracting the `sub` and `role` claims and attaching them
> to `request.auth`, and if the token is expired or malformed the middleware returns a
> `401 Unauthorized` response with a JSON error body containing a `message` field and
> an `errorCode` field set to `TOKEN_EXPIRED` or `TOKEN_MALFORMED` respectively, while
> also logging the failure to the audit trail via `AuditLogger.log`.

> **STE:** The authentication middleware validates each incoming request. The
> middleware reads the bearer token from the `Authorization` header. It sends the token
> to the `validateToken` function in the `security` module. The `validateToken` function
> decodes the JWT payload. It uses the `HS256` algorithm from the `jwt-signer` library.
> Then it compares the `exp` claim with the current server time. If the token is not
> expired and not malformed, the function gets the `sub` and `role` claims. It attaches
> these claims to the `request.auth` object.
>
> If the token is expired, the middleware returns a `401 Unauthorized` response. The
> response body is a JSON object:
>
> - The `message` field contains a description of the error.
> - The `errorCode` field is set to `TOKEN_EXPIRED`.
>
> If the token is malformed, the middleware returns a `401 Unauthorized` response. The
> `errorCode` field is set to `TOKEN_MALFORMED`.
>
> The middleware also logs each failure to the audit trail. It calls the
> `AuditLogger.log` static method. This method writes a record to the `audit_events`
> table in the primary database. The write uses an asynchronous pattern that does not
> block the response pipeline.

```typescript
// STE: split the contract into one fact per comment line.
// The authenticate middleware checks each incoming request.
// It reads the bearer token from the Authorization header.
// It sends the token to validateToken in the security module.
// If the token is expired, the middleware returns 401 with errorCode TOKEN_EXPIRED.
// If the token is malformed, the middleware returns 401 with errorCode TOKEN_MALFORMED.
// The middleware logs each failure through AuditLogger.log.
function authenticate(req: Request, res: Response, next: NextFunction): void {
  const token = req.headers.authorization?.replace("Bearer ", "");
  if (!token) { return res.status(401).json({ message: "Missing token", errorCode: "TOKEN_MALFORMED" }); }
  const result = validateToken(token);
  if (result.status === "expired") { return res.status(401).json({ message: "Token expired", errorCode: "TOKEN_EXPIRED" }); }
  if (result.status === "malformed") { return res.status(401).json({ message: "Token malformed", errorCode: "TOKEN_MALFORMED" }); }
  req.auth = { sub: result.sub, role: result.role };
  next();
}
```

### By documentation type

| Type | What "one piece of information" means |
|---|---|
| README | One concept per section; one subject per sentence. Purpose, then install, then a basic usage example — each in its own section. |
| API reference | Method and path in one sentence. One sentence per parameter, per response field, per status code. |
| Docstrings / comments | One behavior per sentence. Three behaviors need three sentences. Comments explain one line or one block, never the whole function. |
| Commit messages | One logical change per commit. One sentence for the summary line; one sentence per sub-change in the body. |
| Error messages / logs | One problem per message; one event per log line. Split multi-cause messages into distinct messages with distinct error codes. |
| Changelogs | One change per entry. Do not mix a feature, a fix, and a deprecation in one sentence. |

### Paradigm-specific guidance

- **Object-oriented (Java, C++, C#, Python classes).** Describe one method or one class
  behavior per sentence. For an inheritance chain, describe the base class behavior
  first, then the override, then the side effect — each in its own sentence.
- **Functional (Haskell, Elixir, Clojure, Rust).** Describe one transformation per
  sentence. Break a `|>` pipeline or a `>>=` chain into one sentence per step.
- **Procedural (C, Go, Bash).** Describe one step or one branch per sentence. Do not
  combine an if-else chain, a loop body, and the cleanup code.
- **Declarative (SQL, Terraform, Kubernetes YAML).** Describe one resource, one
  constraint, or one column per sentence. Dependencies are listed one by one.
- **Systems (Rust ownership, C memory).** Describe one ownership rule, one lifetime
  constraint, or one memory operation per sentence. Allocation, ownership transfer,
  and the deallocation guarantee are separate subjects.

```elixir
# STE: document each pipeline step on its own line.
# process_order accepts an Order.
# It applies validate_order to the order.
# It applies calculate_total to the validated order.
# It applies create_invoice to the order with the total.
# It applies send_confirmation to the invoice.
def process_order(order) do
  order
  |> validate_order()
  |> calculate_total()
  |> create_invoice()
  |> send_confirmation()
end
```

```c
// STE: one memory contract rule per line.
// The allocate_buffer function allocates a buffer on the heap.
// It uses malloc for the allocation.
// The function returns a pointer to the buffer.
// The caller becomes the owner of the buffer.
// The caller must free the buffer with free.
// If the allocation fails, the function returns NULL.
// It also sets errno to ENOMEM.
void* allocate_buffer(size_t size, size_t* out_size) {
  void* buf = malloc(size);
  if (!buf) { errno = ENOMEM; return NULL; }
  *out_size = size;
  return buf;
}
```

### Edge cases

- **A framework name that contains several concepts.** Treat
  `UserAuthenticationAndAuthorizationService` as one technical noun. Do not split the
  identifier across sentences. The rule applies to the prose around it: `The
  UserAuthenticationAndAuthorizationService handles user login. It also handles
  permission checks.`
- **Generated documentation.** OpenAPI generators, JSDoc renderers, and Sphinx autodoc
  often emit compound sentences from structured metadata. If you cannot control the
  output, add a plain-language summary above it that obeys Rule 6.1. Generated content
  is exempt unless you edit the source annotations.
- **Control-flow keywords.** `if`, `else`, `while`, and `try`/`catch` describe branching
  with several outcomes. Use one sentence per branch. Describe the `try` block and the
  `catch` block in separate sentences.
- **Brevity contexts (CLI help, error codes).** Use the minimum number of sentences, but
  each one still has one subject. Use fragments only where the display format enforces
  them, as in a one-line usage string.
- **Rewriting existing documentation.** Check whether the compound structure hides a
  dependency. If action B depends on action A, describe A first in its own sentence.

### Grammar note

Working memory holds about four to seven items. A sentence with several subjects, verbs,
and objects forces the reader to hold all of them until the sentence ends. In code
documentation the reader is already processing technical concepts and control flow, so
the cognitive load is higher than in ordinary prose.

In procedures, each imperative step has the same implied subject (`you`), so imperative
steps follow this rule naturally. Still write `Stop the server. Then restart the
server.` — not `Stop and restart the server.`

---

## Rule 6.2 — Use key words and key phrases to give your text a logical structure

**Rule.** Key words are terms that occur several times in a documentation block to link
different concepts. Key phrases are multi-word expressions with the same function. Key
words and key phrases show how information is related and give the documentation a
logical structure. When you use a key word, do not change it. The same terminology keeps
the documentation clear and correct.

Connecting words and connecting phrases work like traffic signs. They tell the reader
whether the information is new, different, or a result of previous information.

### How the connectives signal

| Connective | Signal | Use it when |
|---|---|---|
| `and`, `also` | Addition | The new sentence adds information about the same key word. |
| `but`, `however` | Contrast | The new sentence differs from the expectation just set. |
| `then` | Sequence | The new sentence is the next step involving the key word. |
| `thus`, `therefore`, `as a result` | Consequence | The new sentence follows from the previous one. |
| `at the same time` | Concurrency | Two effects happen together. |
| `for example` | Illustration | The new sentence instantiates the previous claim. |

### Keeping the key word stable

> **Non-STE:** The parser reads the input stream. Invalid tokens are detected by the
> lexer. An error is returned to the caller.

> **STE:** The parser reads the input stream. The parser detects invalid tokens. The
> parser returns an error to the caller.

In the Non-STE version the topic shifts from `parser` to `invalid tokens` to `an error`,
and the reader must reconstruct that all three sentences are about the parser. In the
STE version, `parser` is the topic of every sentence.

**Multi-word key phrases stay whole.** When the key phrase is a multi-word technical
term (`connection pool`, `rate limiter`, `retry policy`), keep the full phrase. Do not
shorten `connection pool` to `pool` halfway through a block.

> **Non-STE:** The connection pool limits concurrent database connections. The pool size
> is configurable. Idle connections are recycled after the timeout.
>
> **STE:** The connection pool limits concurrent database connections. The connection
> pool size is configurable. The connection pool recycles idle connections after the
> timeout.

**Dangling key words.** A dangling key word is a term introduced once and never
repeated. The reader expects it to matter and never meets it again.

```text
# Non-STE
The build system compiles TypeScript and bundles static assets.
The output goes to the dist/ directory.
Deployment uses a Docker container.

# STE (resolved)
The build system compiles TypeScript and bundles static assets.
The build system writes the output to the dist/ directory.
The deploy system copies the dist/ directory into a Docker container.
```

### Cohesive ties

Three tie types are permitted:

1. **Repetition.** The same word appears again: `The middleware validates the request.
   The middleware reads the token.`
2. **Pronoun reference.** `it`, `they`, `this` refer back to the key word. Use pronouns
   sparingly. After two sentences, repeat the full key word to prevent ambiguity.
3. **Approved synonym or hypernym.** `The function returns a Result. The value contains
   the parsed data.` The STE-Code synonym table restricts which substitutions are safe.

### Edge cases

- **A framework name that is also an unapproved word.** Keep the exact identifier as the
  key word. Do not paraphrase a library name to satisfy the vocabulary rules.
- **A code keyword that conflicts with the rule.** Language keywords (`return`, `yield`,
  `import`) stay in code font and keep their exact spelling when used as key words.
- **Generated documentation.** If the generator varies terminology, fix the source
  annotations. If you cannot, add a hand-written summary that uses stable key words.
- **Multi-language repositories.** Choose one cross-language key word and give the
  language-specific names once as a clarification: `The configuration is stored in a map
  (Python: dict, Java: HashMap, Go: map). The map uses string keys.` Do not rotate
  `dict`, `HashMap`, and `map` as if they were three concepts.

### Supporting rules from Section 1

- **Rule 1.11 — One term per concept.** Key words work only if the same term names the
  same concept. Switching synonyms breaks the key word chain.
- **Rule 1.5 — Technical code nouns are allowed.** A class, function, or library name may
  be a key word even when it is not in the approved terminology.
- **Rule 1.8 — Use standard technical nouns.** An invented key word weakens the
  structure because the reader does not recognize it as a key term.
- **Rule 1.9 — Prefer short technical nouns.** A key word such as
  `AbstractAsynchronousDatabaseConnectionManager` is too long to repeat.

---

## Rule 6.3 — Write short sentences. Use a maximum of 25 words in each sentence

**Rule.** Good code documentation uses short sentences for complex topics. Short
sentences give a clear structure and make information easier to understand. In
descriptive code documentation the maximum sentence length is **25 words**, because
descriptive text is more complex than procedural text.

The limit is a ceiling, not a target. Most good sentences are much shorter.

### Worked examples

> **STE:** The authentication middleware validates each incoming request before the
> controller processes it. *(11 words)*

> **Non-STE:** This function provides the ability to run arbitrary software applications
> within a sandboxed execution environment that isolates system resources. *(21 words)*
>
> **STE:** This function lets you run software applications in a sandbox. The sandbox
> isolates system resources. *(9 and 5 words)*
>
> Splitting improves clarity even when the original is already under 25 words.

> **Non-STE:** The configuration loader reads the YAML manifest file from the filesystem
> and parses it into an in-memory representation that other modules can query at runtime
> to determine their operational parameters. *(32 words)*
>
> **STE:** The configuration loader reads the YAML manifest file from the filesystem. It
> parses the file into an in-memory representation. Other modules can query this
> representation at runtime. They use it to find their operational parameters.

> **Non-STE:** The cache invalidation strategy employs a time-to-live mechanism combined
> with a least-recently-used eviction policy to ensure that stale data is removed and
> memory consumption remains within the allocated heap budget. *(34 words)*
>
> **STE:** The cache invalidation strategy uses a time-to-live mechanism. It also uses a
> least-recently-used eviction policy. Together, these mechanisms remove stale data. They
> also keep memory consumption within the allocated heap budget.

```python
# config/loader.py — STE docstring: one behavior per line, each under 25 words.
def load_config(path: Path) -> Config:
    """Read the YAML manifest from the filesystem.

    Parse the file into an in-memory representation.
    Other modules query this representation at runtime.
    They use it to find their operational parameters.
    """
    raw = path.read_text()
    data = yaml.safe_load(raw)
    return Config(data)
```

### Counting rules

- Count words, not characters. A hyphenated technical term (`least-recently-used`,
  `time-to-live`) counts as one word.
- An identifier in code font (`ConnectionPool`, `req.headers.authorization`) counts as
  one word, however long it is.
- A type signature quoted inline counts as one word.
- Do not count the words inside a code block or a table cell.

### By documentation type

- **README.** One sentence for the project purpose, one for the prerequisites, one for
  the install command. A reader must find the install step without parsing a paragraph.
- **API reference.** One short sentence for the path and method. One per parameter. One
  per response field. Developers scan for the one detail they need.
- **Docstrings.** One line per behavior. A summary line, then one line per parameter,
  return value, and raised error.
- **Commit messages.** Keep the summary line short and put each detail on its own body
  line.
- **Error messages.** State one problem in one short sentence. Long error strings are
  truncated by log viewers and terminals.

### Edge cases

- **Long technical terms.** A required identifier may itself be long. It still counts as
  one word. Do not rename an API to satisfy the limit.
- **Compound type signatures.** `Map<String, List<Order>>` is one word. If the signature
  makes the sentence unreadable, move it to a code block and refer to it by name.
- **Legal and license text.** Legal wording is often fixed and cannot be edited. Quote it
  verbatim, then give a short plain-language summary that obeys the limit.
- **Generated documentation.** Long generated sentences are exempt. Fix them at the
  annotation source, or add a compliant summary above them.

### Grammar note

Sentence length is a proxy for clause density. A sentence with one main clause and at
most one dependent clause is normally under 25 words on its own. Prefer coordination that
shares one subject over subordination that stacks clauses. When you must connect two
independent ideas, use a connecting word at the start of the second sentence instead of a
comma splice.

---
