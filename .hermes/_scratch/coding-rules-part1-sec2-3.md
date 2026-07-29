# STE-Code — Part 1: Sections 2–3

---

## Section 2 — Compound Identifiers

### Summary of the rules

**Rule 2.1** Write compound identifiers of no more than three components.
**Rule 2.2** When a Technical Code Noun has more than three components, write it in full.
Then use a shorter form or hyphens to make it clear.

---

### Rule 2.1 — Maximum three components

A "component" is a semantic unit in an identifier, regardless of casing convention.
`user_email_validator` has three components. `UserEmailValidatorService` has four — too many.

> **Non-STE-Code:** `AbstractUserAuthenticationCredentialValidationServiceFactory`
> **STE-Code:** `AuthCredentialFactory` or `UserAuthFactory`

> **Non-STE-Code:** `getFilteredSortedPaginatedUserListFromDatabase`
> **STE-Code:** `queryUsers` with parameters: `{ filter, sort, page }`

---

### Rule 2.2 — Long Technical Code Nouns: shorter forms or hyphens

**Method 1 — Shorter form:**
Write the full identifier once, then define a shorter form.

```
Full: AbstractUserAuthenticationCredentialValidationService
Short form: AuthCredentialValidator (hereinafter "the validator")
```

**Method 2 — Hyphens:**
Use hyphens between words that operate as one unit. Hyphenated words count as one word.

| Non-STE-Code | STE-Code |
|---|---|
| `requestresponsehandler` | `request-response-handler` (3 words) |
| `readonlymodeflag` | `read-only mode flag` (3 words) |

Do not hyphenate when the Technical Code Noun is already three words or fewer.

> **Do not write:** `user-service` when your organization uses `UserService`.
> **Write:** `UserService`

---

## Section 3 — Functions and Operations

### Summary of the rules

**Rule 3.1** Use only the function signature forms given in the approved vocabulary.
**Rule 3.2** Use only these function patterns:
- Pure functions (no side effects)
- Command functions (imperative)
- Present tense descriptions
- Past tense for historical/log data
- Future tense for scheduled operations
- Past participle as a state descriptor

**Rule 3.3** Use the past participle form as a state descriptor.
**Rule 3.4** Do not use complex nested function compositions.
**Rule 3.5** Use the `-ing` form of a verb only as a Technical Code Noun or modifier.
**Rule 3.6** Use the active voice. Passive voice only when the agent is unknown.
**Rule 3.7** Use an approved verb to describe an action, not a noun.

---

### Rule 3.1 — Approved function signature forms

Each approved verb maps to a canonical function signature:

| Verb | Signature Pattern |
|------|------------------|
| VALIDATE | `validate(input: T) -> Result<V, E>` |
| SERIALIZE | `serialize(object: T) -> string` |
| PARSE | `parse(raw: string) -> AST` |
| RENDER | `render(template: T, context: C) -> string` |
| QUERY | `query(criteria: C) -> ResultSet<T>` |
| TRANSFORM | `transform(input: T, rules: R[]) -> U` |
| ENCODE | `encode(data: T, format: F) -> bytes` |
| DECODE | `decode(raw: bytes, format: F) -> T` |

---

### Rule 3.2 — Approved function patterns

**Pure functions** (no side effects):

> **Non-STE-Code:**
> ```
> // This function validates the data and also logs it and updates a counter
> function process(data) { log(data); counter++; return validate(data); }
> ```
>
> **STE-Code:**
> ```
> // Validate the data. The function does not cause side effects.
> function validate(data: Input): ValidationResult { ... }
> ```

**Command functions** (imperative):

> **Non-STE-Code:** `// This should probably deploy the build`
> **STE-Code:** `// Deploy the build to the staging environment.`

**Past participle as state descriptor:**

> **Non-STE-Code:** `// The data that was serialized by the encoder`
> **STE-Code:** `// The serialized data`

---

### Rule 3.3 — Past participle as state descriptor

> **Non-STE-Code:** `// The response that was compressed by the middleware`
> **STE-Code:** `// The compressed response`

> **Non-STE-Code:** `// The token that the auth service validated`
> **STE-Code:** `// The validated token`

Approved adjectives that are past participles (permitted, validated, serialized, encrypted)
can be used directly without the verb construction.

---

### Rule 3.4 — No complex nested function compositions

> **Non-STE-Code:**
> ```
> // The result of having been processing the deferred validation queue
> const x = await processQueue(deferredValidationQueue.filter(isPending).map(validate));
> ```
>
> **STE-Code:**
> ```
> // Filter the pending items from the deferred validation queue.
> // Validate each pending item.
> const pending = deferredValidationQueue.filter(isPending);
> const results = await Promise.all(pending.map(validate));
> ```

---

### Rule 3.5 — `-ing` form restrictions

Use the `-ing` form only as a Technical Code Noun or modifier:

**Permitted as Technical Code Noun:**
- `ProcessingQueue` (class name)
- `StreamingResponse` (type name)
- `RenderingEngine` (module name)

**Permitted as modifier:**
- `// Use a streaming connection for large files.`
- `// The caching layer stores results in memory.`

**Not permitted:**
> **Non-STE-Code:** `// The server is processing the request when the timeout occurs.`
> **STE-Code:** `// The server processes the request. If the request exceeds the timeout, the server returns an error.`

Approved `-ing` words in STE-Code vocabulary: `processing`, `streaming`, `rendering`,
`caching`, `logging`, `routing`, `scheduling`, `polling`, `batching`, `throttling`.

---

### Rule 3.6 — Active voice

Use active voice in code documentation. Passive voice is permitted only in descriptive
text when the agent (the entity performing the action) is unknown.

**Four methods to convert passive to active:**

**Method 1 — Put the agent first:**
> **Non-STE-Code:** `// The request is validated by the middleware.`
> **STE-Code:** `// The middleware validates the request.`

**Method 2 — Change infinitive to active verb:**
> **Non-STE-Code:** `// The data can be processed by the pipeline.`
> **STE-Code:** `// The pipeline processes the data.`

**Method 3 — Use imperative in procedures:**
> **Non-STE-Code:** `// The server should be restarted after the update.`
> **STE-Code:** `// Restart the server after the update.`

**Method 4 — Use "you" or "we" when agent is the reader or team:**
> **Non-STE-Code:** `// The configuration file can be edited to change the port.`
> **STE-Code:** `// You can edit the configuration file to change the port.`

**Permitted passive (agent unknown):**
> `// The connection was closed by the remote host.` (agent = remote host, unknown identity)
> `// The error was logged at 14:32:07 UTC.` (agent = logging system, implicit)

---

### Rule 3.7 — Use a verb to describe an action

> **Non-STE-Code:** `// The validator performs validation of the input data.`
> **STE-Code:** `// The validator validates the input data.`

> **Non-STE-Code:** `// Do a check of the database connection status.`
> **STE-Code:** `// Check the database connection status.`

If a word is not approved as a verb, restructure the sentence:

> **Non-STE-Code:** `// Cache the query result.` (cache = Technical Code Noun)
> **STE-Code:** `// Store the query result in the cache.`
