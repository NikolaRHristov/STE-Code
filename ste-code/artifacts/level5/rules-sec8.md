# Level 5 — Punctuation and Word Count (Section 8)

Section 8 of STE-Code governs punctuation and word-count mechanics in code
documentation. It contains seven rules: 8.1 (no semicolon), 8.2 (hyphens),
8.3 (parentheses usage), 8.4 (colon in vertical lists), 8.5 (parentheses and
word count), 8.6 (elements that count as one word), and 8.7 (hyphenated words
count as one word).

This is the full-standard (Level 5) slice. Use it when an LLM generates or
revises code documentation: README files, API reference docs, docstrings, inline
comments, commit messages, error messages, configuration comments, and
specification documents. All guidance below is faithful to the STE-Code
standard and uses code-domain examples only.

Quick reference — the seven rules:

- 8.1 No semicolon (;) in documentation prose.
- 8.2 Hyphenate directly related words (compound adjectives / technical nouns).
- 8.3 Parentheses: references, abbreviations, item IDs, alternatives, singular/plural, explanations.
- 8.4 A colon before a vertical list acts as a period (sentence boundary) with word-count limits.
- 8.5 Parenthetical text counts as one word in the enclosing sentence but is its own separate sentence.
- 8.6 Numbers, units, abbreviations, identifiers, quoted text, titles/labels, and proper nouns each count as one word.
- 8.7 A hyphenated word group counts as one word.

## Rule 8.1 — No semicolon (;)

You may use all standard English punctuation marks in code documentation except
the semicolon (;). The semicolon is forbidden because it lets you pack two
independent clauses into one sentence, which is hard to read — especially for
non-native English readers — and because the semicolon is a statement terminator
in many languages (C, C++, Java, JavaScript, Rust, Go), causing cognitive
interference in documentation prose.

Fix every violation the same way: split the semicolon-separated sentence into two
or more independent sentences. Each new sentence stands alone with its own
subject and verb. This aligns with Rule 3.1 (simple sentences) and Rule 4.1
(short sentences).

Applies to: README, API reference docs, docstrings, inline comments, commit
messages, error messages, configuration comments, and specification documents.
Does NOT apply to source code (where the semicolon is syntax) or to code shown
inside code blocks / inline backticks.

### Examples

Non-STE: Call the function to parse the response data; handle any errors that occur.
STE:    Call the function to parse the response data. Handle any errors that occur.

Non-STE: The cache is invalid after a write operation; you must flush it before the next read.
STE:    The cache is invalid after a write operation. You must flush it before the next read.

Non-STE: The server supports WebSocket connections; these use a persistent channel instead of the standard request-response cycle.
STE:    The server supports WebSocket connections. These connections use a persistent channel instead of the standard request-response cycle.

Non-STE: POST /sessions creates a new session and returns a token; the token must be included in the Authorization header of subsequent requests.
STE:    A POST request to /sessions makes a new session and returns a token. You must include the token in the Authorization header of all later requests.

Non-STE: Invalid port number; specify a value between 1024 and 65535.
STE:    The port number is not valid. Specify a value between 1024 and 65535.

Non-STE: The authentication middleware now checks token expiry before decoding; expired tokens return a 401 before reaching the route handler.
STE:    The authentication middleware now checks token expiry before decoding. Expired tokens return a 401 status code before they reach the route handler.

### Paradigm notes
- Object-oriented: split constructor initialization from post-condition; for getter/setter pairs, write each method's description as its own sentence.
- Functional: describe the happy path as one sentence, the error path as a second sentence. Do not reinforce the `|>` / `>>` / `.` pipe with a semicolon in prose.
- Procedural (C, Go, Bash): write each step as its own sentence; use "then" at the start of the second sentence for tight sequences.
- Declarative (SQL, Terraform, Kubernetes): write each property and each effect as its own sentence.
- Systems (Rust ownership, C memory): write the safety rule as one sentence and the consequence as a second sentence introduced with "thus" or "as a result." For Undefined Behavior, never use a semicolon — the consequence must be a standalone sentence.

### Edge cases
1. Semicolons inside code blocks / inline backticks are language syntax, not prose. Keep them. The rule governs surrounding prose only.
2. Generator-inserted semicolons in auto-generated docs (OpenAPI, JSDoc, protobuf) are not your violation; apply 8.1 to the source comments you author.
3. Semicolons inside quoted strings (error output, logs) are quoted material — keep them; prose around must obey 8.1.
4. Do not use a semicolon as a "super-comma" in a complex list. Use a bullet list or table instead.
5. Chat / informal PR-thread messages: 8.1 is optional. Commit messages are permanent history and must follow 8.1.
6. A semicolon inside a regex, CSV row, or data string is data, not prose — keep it in the code span.

### Cross-references
Rule 1.1 (approved words for connecting clauses), Rule 3.1 (simple sentences),
Rule 4.1 (short sentences), Rule 4.4 (connecting words replace the semicolon),
Rule 8.2 (hyphen versus semicolon).

## Rule 8.2 — Use hyphens (-) to connect directly related words

Use a hyphen to connect two or more words that function as one concept, most
often a compound adjective before a noun. The hyphen signals to the reader that
the words form a single unit and removes ambiguity about which word modifies
which. A hyphen joins words; a semicolon/colon joins clauses. Keep the two
distinct.

The five code-domain hyphenation categories:

1. Compound adjectives before a noun: high-priority task, read-only file,
   thread-safe method, event-driven architecture, type-safe interface,
   run-time error, end-to-end test, point-to-point connection,
   server-side rendering, client-side validation, just-in-time compilation,
   fire-and-forget pattern.
2. Two-word fractions / numbers: seventy-two, three-fourths, one hundred and
   sixty-two.
3. Uppercase-or-number + noun giving shape/configuration: L-shaped bracket,
   T-shaped connector, 64-bit register, 8-byte alignment, 128-bit value,
   3-prong connector.
4. Verbs whose first part is a noun or different part of speech: dry-run,
   hot-reload, cold-start, hard-code, soft-delete, short-circuit.
5. Prefix ending in a vowel + root starting with a vowel: pre-initialized,
   re-entrant, de-allocated, anti-aliasing, re-indexed.

### Examples

Non-STE: The high priority task must acquire the write lock before it can modify the shared data structure.
STE:    The high-priority task must get the write lock before it can change the shared data structure.

Non-STE: A read only file descriptor to open the configuration for parsing.
STE:    A read-only file descriptor to open the configuration for parsing.

Non-STE: A non negative integer that sets the buffer size. / A read only reference to the internal cache.
STE:    A non-negative integer that sets the buffer size. / A read-only reference to the internal cache.

Non-STE: The thread safe singleton uses lazy initialization to defer object creation until the first access.
STE:    The thread-safe singleton uses lazy initialization to defer object creation until the first access.

Non-STE: The left joined table uses a fully qualified column name from the user provided input.
STE:    The left-joined table uses a fully-qualified column name from the user-provided input.

Non-STE: The memory mapped file uses a copy on write page that is atomically reference counted.
STE:    The memory-mapped file uses a copy-on-write page that is atomically-reference-counted.

### Paradigm key terms
- OO: read-only property, write-only field, lazy-initialized singleton, reference-counted pointer, thread-safe collection, lock-free algorithm.
- Functional: pure-function semantics, side-effect-free computation, higher-order function, copy-on-write map, lazily-evaluated sequence, lock-free CAS loop.
- Procedural: null-terminated string, zero-initialized struct, stack-allocated array, const-qualified parameter, short-circuit evaluation, newline-delimited output.
- Declarative: left-joined table, fully-qualified column name, read-only attribute, base64-encoded value, cluster-scoped resource, blue-green deployment.
- Systems: move-semantics transfer, borrow-checked reference, memory-mapped I/O, copy-on-write page, lock-free stack, use-after-free bug.

### Edge cases
1. Keep hyphenated tool/library names as-is (create-react-app). Do not add a second hyphen (correct: "the create-react-app template"; wrong: "create-react-app-template").
2. In prose, hyphenate code keywords used as compound adjectives ("the type-of operator", "a full-outer-join operation"); in code spans, reproduce exactly (`typeof x`, `FULL OUTER JOIN`).
3. Leave generated output as-is; add a NOTE in surrounding prose if the generator omits hyphens.
4. An established unhyphenated compound (codebase, filename, namespace) may stay if it is unambiguous and consistent project-wide; otherwise hyphenate.
5. API endpoints / URL paths use kebab-case as proper nouns — keep hyphens in the path (`/api/read-only-access`); prose hyphenation follows 8.2 separately.

### Grammar notes
- Attributive (before noun) takes a hyphen; predicative (after a linking verb) does not: "the thread-safe collection" vs "the collection is thread safe."
- Adverbs ending in "-ly" do NOT take a hyphen: "a fully qualified name", not "fully-qualified".
- "self-" prefix always takes a hyphen (self-contained, self-signed).
- Do not insert hyphens into code identifiers (`getUserProfile`, not "get-user-profile"); use the identifier verbatim in backticks.

### Cross-references
Rule 1.1 (approved words), Rule 1.5 (technical nouns as first element),
Rule 1.9 (shorten long compounds), Rule 1.11 (consistent form), Rule 8.1,
Rule 8.6 (hyphenated term counts as one word), Rule 8.7.

## Rule 8.3 — Use of parentheses

You may use parentheses in code documentation for seven purposes:

1. References to modules, diagrams, or text: "Call the request handler (Figure 3, Module A)." / "Deploy the service (refer to sections 2 thru 5)."
2. Letters or numbers that identify diagram or text items: "Disconnect the endpoints (2) and (12) from the load balancer (8)."
3. Work-step identification in a procedure: "(1) Install the dependency package (4) in the project directory (8)."
4. Abbreviations, placed immediately after the full term: "A Command Line Interface (CLI) is a text-based interface…"
5. Singular and plural at once: "Before you run the test(s), set the environment variable(s)."
6. Explanations of words or part of a sentence: "Increase the timeout slowly (not more than 1000 ms each step)."
7. An alternative: "Use the left (right) API key for the staging (production) environment."

Square brackets [ ] are reserved for optional parameters in code syntax. Parentheses are the only permitted brackets for parenthetical information in prose. Do not use commas before an opening parenthesis except when the parenthetical is an alternative at the end of a list.

### Examples by doc type

README: This project provides a Command Line Interface (CLI) for managing your deployment pipeline. Follow the setup guide (refer to docs/getting-started.md) before you run the server.

API docs: The timeout parameter accepts an integer in milliseconds (ms). To use seconds, set the unit flag to "s" (available in version 2.1 and later). If the request fails, the server returns a 404 (Not Found) status.

Docstrings: timeout: milliseconds to wait (1 to 30000). / "Calculate the factorial of n (a non-negative integer)."

Commit messages: feat(auth): add PKCE support (issue #482). / fix(ui): correct z-index conflict between dropdown and modal (regression from v2.3).

Error messages: Cannot find the configuration file (searched: /etc/myapp/config.yaml, ~/.config/myapp/config.yaml, ./config.yaml). / Invalid value for --workers: 0 (valid range: 1 to 64).

### Paradigm notes
- OO: parentheses show method parameters, constructors, type parameters; "the `process` method (inherited from `BasePipeline`, which implements `core.Pipeline`)". Default values in tables: "milliseconds to wait before failure (default: 5000)."
- Functional: group type parameters; "the `State` monad passes an immutable state value… Use `StateT` (the transformer variant) to combine it with another monad."
- Procedural: return codes — "0 (success), -1 (I/O error), -2 (malformed input), -3 (timeout)"; ownership — "the caller must free the returned buffer (allocated by this function)."
- Declarative: enumeration values — "set the `provider` field to one of: "aws", "gcp", "azure" (lowercase only)"; "set `replicas` to the number of pod copies (range: 1 to 100, production minimum: 1)."
- Systems: ownership transfer — "this function takes ownership of the value (the caller cannot use it after the call)"; SAFETY invariants — "(invariant enforced by caller)."

### Edge cases
1. Framework/library names that are common words: clarify with a parenthetical on first use — "Use Flask (the Python web framework)…", "React (a JavaScript UI library)…".
2. Code keywords that are punctuation (Rust `()`, `<T>`): keep code literals distinct; explain in a separate sentence, do not nest.
3. Auto-generated docs (JSDoc, Sphinx, rustdoc): leave generated signatures untouched; apply 8.3 to human-written description fields.
4. Never nest parentheses. Restructure or split: "Set the cache TTL to 3600 (one hour). For production, set the cache TTL to 86400 (one day)." / "JWT is an abbreviation for JSON Web Token."
5. CLI help text: use parentheses sparingly — alternative or explanation patterns only; long descriptions belong in a man page.

### Cross-references
Rule 1.1 (abbreviation words), Rule 1.3 (approved meanings in explanations),
Rule 1.9 (short technical nouns), Rule 5.1 (parenthetical counts toward sentence
length), Rule 6.3 (one step per numbered line), Rule 8.2 (hyphens are not
parentheses). Period goes outside the closing parenthesis unless the
parenthetical is a complete sentence (then it becomes its own sentence).

## Rule 8.4 — Colon in a vertical list

In a vertical list, the colon (:) before the list acts as a period (full stop).
The introductory text before the colon is a complete sentence and must obey the
sentence-length limits: maximum 20 words for procedural text, 25 words for
descriptive text. Each list item after the colon is a new sentence with its own
limit (20 procedural / 25 descriptive).

The colon always ends the introductory sentence. Enumerated items must be
vertical (bullets or numbered), never inline. Em-dashes are not a substitute;
only the colon introduces a vertical list.

### Examples

Non-STE: To handle all possible error conditions, the following exception types must be caught and processed by the error handler: database connection timeouts which occur when the primary node is unreachable, authentication failures caused by expired or invalid tokens, and validation errors due to malformed request payloads.
STE:
To handle possible error conditions, the error handler catches these exception types:
- Database connection timeout
- Authentication failure
- Validation error.

Non-STE: ...supports these environment profiles that you can use for deployment: a development profile for local testing..., a staging profile..., and a production profile...
STE:
The configuration file supports these environment profiles:
- Development
- Staging
- Production.

Non-STE: A successful request to the GET /users/{id} endpoint returns a JSON response body that contains the following fields which describe the user account...: an id field..., a username field..., an email field..., a created_at field..., and a status field...
STE:
A GET request to /users/{id} returns a JSON response with these fields:
- `id` — The unique user identifier (UUID string)
- `username` — The display name
- `email` — The verified email address
- `created_at` — The account creation timestamp (ISO 8601)
- `status` — The account status (`active`, `suspended`, or `pending_verification`).

### Guidance by doc type
- README: keep the introduction to the category only; move version numbers, caveats, and compatibility notes into list items or a prior sentence.
- API docs: name the endpoint/resource and what the list enumerates; put type, default, and validation in each item (Args:/Returns:/Raises: sections align naturally).
- Docstrings: "This function handles these edge cases: - Empty input strings - Input with only whitespace…".
- Commit messages: the subject line is a standalone summary, not a list introduction; the body's intro must be short.
- Error messages: use a short intro ("The database migration failed for one of these reasons:") then one item per cause or recovery step.

### Paradigm notes
- OO: "The ConnectionPool constructor accepts these arguments: - url — A valid JDBC connection string… - maxConnections — The largest number of concurrent connections."
- Functional: "The ParseResult enum represents the result of parsing a configuration file. The enum has these variants: - Ok(Config) — … - Err(ParseError::Io) — …"
- Procedural: state the goal, then imperative steps — "Make sure that Go 1.21 or later is installed. … Then do these steps: - Clone the repository. - Run `go mod download`."
- Declarative: "The instance_type variable sets the EC2 instance size. The variable accepts these values: - t3.micro - t3.small - t3.medium." Put exclusions in a NOTE after the list.
- Systems: enumerate every precondition as its own bulleted item — "The caller must obey these safety conditions: - The pointer must not be null. - The pointer must be aligned to a 4-byte boundary. - …"

### Edge cases
1. Code tokens in backticks inside the introduction count as one word each, but prefer introductions with few code tokens and fewer than 15 total words.
2. Limit nested lists to one level; the parent item is a short category heading with its own colon.
3. A code block inside a list item is exempt from word count; keep the surrounding prose short.
4. Long framework/resource names belong in the list items, not the introduction.
5. Generator-produced colon-lists (OpenAPI, `--help`): obey 8.4 in source comments; accept the generator's boilerplate.

### Cross-references
Rule 1.1 (approved words in items), Rule 3.1 (one subject-verb-object per item),
Rule 3.3 (lists satisfy paragraph brevity), Rule 4.1 (limits apply at two
points: intro and each item), Rule 6.3 (procedural lists), Rule 8.1 (the colon
replaces semicolon-joined enumerations). The colon before a vertical list is the
approved replacement for semicolon-joined clause lists.

## Rule 8.5 — Parentheses and word count

When you put text in parentheses, it counts as ONE WORD in the enclosing
sentence. But the words inside the parentheses also form a separate sentence
with its own word-count limit (20 procedural / 25 descriptive). An identifier in
parentheses (a number, letter, or alphanumeric identifier) and an abbreviation
in parentheses each count as one word and do not need to obey the sentence-length
limit, because they are not prose.

Two types of parentheticals:
- Identifier parentheticals: (10), (EACCES), (CI/CD), (v2.1) — one word, no sentence limit.
- Explanatory parentheticals: (the DEBUG flag is off), (the worker runs every 60 seconds) — one word in the main sentence, but a complete separate sentence that must obey the limit.

Do not use parentheses to hide safety conditions, required steps, or warnings
the reader must act on. If the information is important enough to include, it is
important enough to be a main sentence.

### Examples

Non-STE: Make sure that the DEBUG environment variable is set to false before you run the deployment script in the production cluster (the DEBUG flag must be explicitly disabled for all production workloads to prevent accidental log leakage).
STE:    Make sure that the DEBUG environment variable is set to false (the DEBUG flag is off).

Non-STE: Remove the health check flag number ten from the deployment configuration.
STE:    Remove the health check flag (10).

Non-STE: Installation and Configuration of a Continuous Integration and Continuous Deployment Pipeline for the Application
STE:    Configuration of a Continuous Integration/Continuous Deployment (CI/CD) Pipeline

Non-STE: The timeout parameter sets the request timeout in seconds (this parameter is optional and defaults to 30 if not provided, but if you set retries greater than zero you should increase the timeout accordingly to account for the cumulative wait time across all retry attempts).
STE:    The timeout parameter sets the request timeout in seconds. The default value is 30. This parameter is optional. NOTE: If you set retries to a value larger than zero, increase the timeout to account for the cumulative wait time.

### Guidance by doc type
- README: do not bury conditional instructions in parentheses; split long asides into their own sentences.
- API docs: identifiers (200, 404, application/json, optional) count as one word; do not embed full conditional logic in a parameter description.
- Docstrings: short parentheticals ((int, optional), (default: 30)) are fine; move algorithmic explanations out.
- Commit messages: issue refs ((#1234)), (breaking), (auth) count as one word; put justification in the body, not in parentheses.
- Error messages: keep error codes and recovery hints short ((Error code: EACCES), (try: chmod 600)); never put the whole recovery procedure in parentheses — use a list.

### Paradigm notes
- OO: (User), (abstract), (Factory pattern) are identifier parentheticals, one word each; move inheritance rationale to its own paragraph.
- Functional: (Eq a), (when x > 0), (:else) are short; move transformation-chain descriptions to a list.
- Procedural: (exit code 1), (-v), (if root) are identifier parentheticals; promote error-branch logic to separate sentences.
- Declarative: (PostgreSQL 14+), (required), (default: true) are short; move migration/back-compat history out of parentheses into a NOTE/BREAKING block.
- Systems (stricter): never put safety-critical information in parentheses. Use the main sentence or a `# Safety` section — "The caller must obey these conditions: - The pointer must be valid for writes. - …"

### Edge cases
1. Function-call notation in backticks (`authenticate()`, `parse(input)`) is one atomic word; its internal parentheses are not Rule 8.5 parentheticals.
2. A URL in parentheses is an identifier (one word); if the parenthetical adds explanatory text after the URL, that text forms a separate sentence.
3. Never nest parentheses. Use an em-dash for the inner aside or split into a sentence.
4. Library/method names with parentheses as part of the canonical spelling (`expect()`) stay in backticks and count as one word.
5. Generator-inserted parentheticals (type hints, defaults) are accepted; follow 8.5 for any you write manually.

### Cross-references
Rule 1.5 (code nouns in parentheses), Rule 1.6 (non-approved words only as
technical nouns — parentheses are not a loophole), Rule 3.1 (the parenthetical
is a sentence), Rule 3.3 (long parentheticals signal a restructure), Rule 4.1
(word limits apply to the parenthetical sentence), Rule 8.1 (a semicolon inside
a parenthetical is still forbidden), Rule 8.4 (a parenthetical can hold a nested
list).

## Rule 8.6 — Elements that count as one word

For sentence-length counting, count each of these as ONE WORD:

1. Numbers: "Do steps 13 thru 16 a minimum of three times." / "The configuration file has twenty-one keys." Do NOT count numbers that identify paragraphs or work steps (document numbering).
2. Numbers with units of measurement: "Make sure that the timeout is 10 ms." / "The payload is 20 MB." / "The latency must be 10 μs." ("10 ms" is one word).
3. Abbreviations (acronyms and initialisms): "For remote access, use the VPN." / "During this security check, obey OWASP guidelines." / "a.m." with its number is one word.
4. Alphanumeric identifiers: "Tag error code E36L7." / "Examine the No. 1 handler installation." / `user_preferences`, `ERR_PG_TIMEOUT_0099`, `OrderPaymentFailed`.
5. Quoted text: words between quotation marks, backticks, or `<code>` tags count as one word — `"Service Overview"`, `C = (A - B) - 0.063 mm` (a formula is one word), `useUserProfile(userId)`.
6. Titles, headings, and text on UI elements / labels: "refer to the Operations Runbook for the applicable safety procedures." / "refer to Error Handling and Recovery, page block 1001." / dialog warnings quoted verbatim count as one word.
7. Proper nouns of individuals, groups, organizations, and geopolitical entities: "The creator of Linux was Linus Torvalds." / "the Apache Software Foundation."

Applying 8.6 collapses many seemingly-long sentences into compliance. A README
sentence that looks like 17 words may count as 12 once "GitHub Actions" (proper
noun), "CI/CD" (abbreviation), "AWS Lambda" (proper noun), and "Serverless
Framework" (proper noun) each become one word.

### Examples

Non-STE: ...validate the signature of each incoming request using the public key obtained from the OpenID Connect identity provider, and the token must have an expiry time of not more than three hundred and sixty seconds...
STE:    The JWT authentication middleware must validate the signature of each incoming request. The token must have an expiry time of not more than 360 seconds to be valid for processing. ("JWT" = 1 word; "360 seconds" = 1 word.)

Non-STE: ...set the property called http.client.retry.max.attempts to a numeric value of five and also set the property http.client.retry.backoff.millis to a numeric value of one thousand...
STE:    In `application.properties`, set `http.client.retry.max.attempts` to 5. Set `http.client.retry.backoff.millis` to 1000. (file path = 1; each prop name = 1; "5", "1000" = 1 each.)

Non-STE: ...freeze the checkout container to two hundred and fifty millicores of CPU and five hundred and twelve mebibytes of memory...
STE:    In the Kubernetes manifest, set the `checkout` container to 250m CPU and 512Mi memory. Set the limit to 500m CPU and 1Gi memory. ("checkout" = 1; "250m CPU", "512Mi", "500m CPU", "1Gi" = 1 each.)

### Paradigm notes
- OO: class/method/interface/package names are proper nouns or identifiers (1 word each); "Abstract Factory Pattern" is one word.
- Functional: type signatures and monad stacks quoted count as one word — `validate :: Config -> Either ValidationError Config`, `ReaderT Env (ExceptT AppError IO) a`.
- Procedural: `pthread_mutex_lock(&mtx)` (quoted, 1 word), `EAGAIN` (identifier, 1 word), `context.Context` (proper noun, 1 word).
- Declarative: `users(email_address, created_at)` (quoted, 1 word), `aws_lambda_function.main` (identifier, 1 word), `readinessProbe.httpGet.path` (identifier, 1 word).
- Systems: `fn process<'a>(data: &'a [u8]) -> Cow<'a, str>` (quoted, 1 word), `0x7fff5fbff8c0` (identifier, 1 word).

### Edge cases
1. Framework names with "unapproved" words (Express, Swift, React) are proper nouns (1 word); do not rewrite them to obey word rules.
2. Code keywords quoted in docs (`class`, `return`, `async`) count as one word; do not replace them with synonyms. When used in your own prose, apply the dictionary normally.
3. Generated text you cannot change (Javadoc `@see`, auto-generated OpenAPI descriptions) counts as one word (category 6).
4. Nested quoted text: the outer backtick/`<code>` boundary defines the unit; everything inside counts as one word.
5. Semantic versions (`1.2.3-alpha.1+build.456`), Git hashes (`a1b2c3d`), image digests (`sha256:abc123...`) are alphanumeric identifiers (1 word). "Version 1.2.3" = two words ("Version" + "1.2.3").
6. Document part numbers (rule/section numbers in cross-refs, step numbers, issue IDs as references) are structural and not counted as quantities.

### Cross-references
Rule 1.1 (proper nouns/identifiers exempt from approved-word rule), Rule 1.5
(framework/library names are technical nouns and proper nouns), Rule 1.6
(non-approved words inside proper nouns/identifiers allowed), Rule 1.14
(American spelling exemptions for proper nouns), Rule 8.7 (hyphenated words also
count as one), Rule 4.1 (the 20/25 limits these counts serve).

## Rule 8.7 — Hyphenated words count as one word

A hyphenated group of words counts as ONE WORD when you count sentence length.
The hyphen joins two or more words into a single unit the reader processes as one
concept, so the 20-word (procedural) / 25-word (descriptive) limits measure the
unit as one word, not as the number of words inside it.

Two cases:

Case 1 — Hyphenated compound adjectives (attributive, before a noun):
- `read-only file descriptor` — "read-only" is one word.
- `thread-safe singleton`, `event-driven architecture`, `low-latency cache`,
  `client-side rendering pipeline`, `end-to-end test suite`,
  `backward-compatible API`.
- After a linking verb / after the noun, do NOT hyphenate and count each word:
  "The singleton is thread safe" (5 words: "thread" and "safe" are separate).

Case 2 — Long hyphenated technical nouns:
- `cutoff-switch power connection` (3 words: `cutoff-switch` / `power` / `connection`)
- `main-gear-door retraction-winch handle` (3 words: `main-gear-door` / `retraction-winch` / `handle`)
- Code-domain: `build-time environment variable` (3 words), `client-side rendering pipeline` (3 words), `end-to-end test suite` (3 words), `check-out request handler` (3 words), `sign-in error message` (3 words), `look-up table index` (3 words). Words after the hyphenated unit are separate.

### Examples

Non-STE: The open function returns a read only file descriptor.
STE:    The open function returns a read-only file descriptor. ("read-only" = 1 word)

Non-STE: To calibrate the retry interval, use the try and error method.
STE:    To calibrate the retry interval, use the trial-and-error method. ("trial-and-error" = 1 word)

Non-STE: Set the build time environment variable to the path of the staging cluster...
STE:    Set the build-time environment variable to the path of the staging cluster... ("build-time" = 1 word)

Non-STE: The client side rendering pipeline builds the page in the browser.
STE:    The client-side rendering pipeline builds the page in the browser. ("client-side" = 1 word)

Non-STE: Use a thread safe singleton for the cache.
STE:    Use a thread-safe singleton for the cache. ("thread-safe" = 1 word)

Word-count proof: "The build-time environment variable must point to the staging cluster." = 10 words. `build-time` is one word, not two.

### Interaction with other rules
- With Rule 8.2: hyphenate per 8.2, then count the hyphenated unit as one word per 8.7. ("open-source" hyphenated per 8.2; counts as one word per 8.7. "JSON" is an abbreviation, one word per 8.6.)
- With Rule 8.6: a hyphenated term is a separate case — it is not an abbreviation or identifier, but still counts as one word. Do not double-count.
- Exception: a hyphen in a spelled-out numeral (twenty-one, forty-seven) or a range (pages 10-15) is covered by Rule 8.6 (numbers count as one word), not 8.7.

### Common code-domain hyphenated terms (each = one word before a noun)

| Term | Type |
|------|------|
| read-only, write-only, thread-safe, event-driven | compound adjective |
| client-side, server-side, end-to-end, backward-compatible, low-latency | compound adjective |
| build-time, run-time, sign-in, check-out, request-response | technical noun |

When a term in this table follows the noun or a linking verb, write it as separate words and count each word.

### Cross-references
Rule 8.2 (when to use hyphens), Rule 8.6 (other one-word elements),
Rule 4.1 (sentence-length limit), Rule 4.2 (do not omit words / use contractions).

---

### How an LLM should apply Section 8 when generating code documentation
1. Never write a semicolon in prose; split into sentences (8.1).
2. Hyphenate compound adjectives before nouns; keep predicates separate (8.2, 8.7).
3. Use parentheses only for the seven allowed purposes; never nest them; never hide safety info in them (8.3, 8.5).
4. Introduce vertical lists with a short colon sentence; each item is its own sentence under 20/25 words (8.4).
5. When counting length, collapse numbers+units, abbreviations, identifiers, quoted code, titles, and proper nouns to one word each, and hyphenated groups to one word (8.6, 8.7).
