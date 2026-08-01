# Level 3 — Section 8: Punctuation Rules (Rules 8.1–8.7)

This slice covers STE-Code **Section 8 — Punctuation**. It adapts ASD-STE100 Issue 9, Section 8 for code documentation. Use it when you generate or review:

- README files, API reference docs, docstrings, inline comments
- commit messages, error messages, configuration comments, specification documents

**Scope boundary:** These rules govern documentation *prose*. They do **not** apply to source code or to any text inside code blocks / inline code spans (backticks). A JavaScript example that shows `const x = 5;` is correct and keeps its semicolon.

**Word-count limits referenced throughout:** procedural sentences ≤ 20 words; descriptive sentences ≤ 25 words. Sentence boundaries are the period (`.`), question mark (`?`), and exclamation mark (`!`).

---

## Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon (;)

**Rule:** You can use all standard English punctuation marks but not the semicolon (;).

**Why:** The semicolon (;) lets you pack two or more independent clauses into one sentence. In code documentation this makes sentences hard to parse — especially for non-native English readers. The semicolon also means different things in C, C++, Java, JavaScript, Rust, Go (statement terminator), which causes cognitive interference when the same symbol appears in prose.

**The fix is always the same:** split the semicolon-joined sentence into two or more independent sentences. Each stands alone with its own subject and verb.

### Examples

Non-STE: `Call the function to parse the response data; handle any errors that occur.`
STE:    `Call the function to parse the response data. Handle any errors that occur.`

Non-STE: `The cache is invalid after a write operation; you must flush it before the next read.`
STE:    `The cache is invalid after a write operation. You must flush it before the next read.`

Non-STE: `POST /sessions creates a new session and returns a token; the token must be included in the Authorization header of subsequent requests.`
STE:    `A POST request to /sessions makes a new session and returns a token. You must include the token in the Authorization header of all later requests.`

Non-STE: `Invalid port number; specify a value between 1024 and 65535.`
STE:    `The port number is not valid. Specify a value between 1024 and 65535.`

### Per-document-type guidance

- **README files:** Write a feature as one sentence, its rationale as a second. Use a connecting word (Rule 4.4) only if the relationship needs to be explicit.
- **API docs:** Write the primary effect as one sentence, the secondary effect as a second.
- **Docstrings / inline comments:** Use a bullet list for multiple return conditions. Use separate sentences for multiple side effects.
- **Commit messages:** Each body sentence states one fact. If you want a semicolon, you are combining two facts — split them.
- **Error messages:** Write the condition as one sentence, the recovery action as a second. Prefer the pattern `X is not valid. Do Y to fix this.`
- **Config comments / test docs:** Write purpose as one sentence, trade-off or assertion as a second.

### Edge cases

1. **Code blocks** — Semicolons inside fenced/indented code and inline backticks (`const x = 5;`) are code syntax, not prose. Keep them.
2. **Generated docs** — Semicolons spliced in by OpenAPI/JSDoc/protobuf generators are generator defects; you are exempt, but apply the rule to the source comments you write.
3. **Quoted strings** — Keep semicolons inside quoted error/log text. Surrounding prose must obey the rule.
4. **Super-comma lists** — Do not use semicolons to separate complex list items. Use a bullet list or table instead:
   - Non-STE: `The endpoint accepts three query parameters: sort, which sets the sort field; order, which must be "asc" or "desc"; and limit, which caps the result count.`
   - STE: bullet list with one line per parameter.
5. **Chat / informal** — Rule applies to formal docs (README, API docs, docstrings, commits, errors). It does **not** apply to chat or PR-thread discussion; commit messages are permanent and always apply.
6. **Regex / data strings** — Keep the semicolon inside the code span holding the data; prose uses periods only.

### Cross-references
Rule 1.1 (approved connecting words), Rule 3.1 (simple sentences), Rule 4.1 (short sentences), Rule 4.4 (connecting words), Rule 8.2 (hyphens).

---

## Rule 8.2 — Use Hyphens (-) to Connect Words That Are Directly Related

**Rule:** Use hyphens (-) to connect words that are directly related. A hyphen signals that two or more words function as a single concept.

**Five categories of hyphenation** (apply the same in code documentation):

1. **Compound adjectives before a noun:** `high-priority task`, `read-only file`, `thread-safe method`, `event-driven architecture`, `type-safe interface`, `run-time error`, `end-to-end test`, `point-to-point connection`, `server-side rendering`, `client-side validation`, `just-in-time compilation`, `fire-and-forget pattern`.
2. **Two-word fractions or numbers:** `seventy-two`, `one hundred and twenty-eight`, `three-fourths`, `forty-seven`.
3. **Uppercase-or-number + noun (shape/configuration):** `L-shaped bracket`, `T-shaped connector`, `64-bit register`, `8-byte alignment`, `128-bit value`, `3-prong connector`.
4. **Verb whose first part is a noun/other part of speech:** `dry-run`, `hot-reload`, `cold-start`, `hard-code`, `soft-delete`, `short-circuit`.
5. **Prefix ends in vowel, root starts with vowel:** `pre-initialized`, `re-entrant`, `de-allocated`, `anti-aliasing`, `re-indexed`.

**A hyphen is different from a dash.** The hyphen joins words into one concept; the dash (—) separates ideas, shows a range (`lines 12-48`), or signals a pause. Keep the two distinct.

### Examples

- Non-STE: `// The high priority task must acquire the write lock before it can modify the shared data structure.`
- STE:    `// The high-priority task must get the write lock before it can change the shared data structure.`

- Non-STE: `A read only file descriptor to open the configuration for parsing.`
- STE:    `A read-only file descriptor to open the configuration for parsing.`

- Non-STE: `git commit -m "Add end to end test for auth flow"`
- STE:    `git commit -m "Add end-to-end test for auth flow"`

### Per-document-type guidance

- **README:** `battle-tested`, `production-ready`, `cross-platform`, `well-documented`, `auto-generated`, `multi-threaded`.
- **API docs:** `non-negative integer`, `null-terminated string`, `zero-based index`, `read-only reference`, `thread-safe access`, `idempotent operation`, `fail-fast strategy`.
- **Docstrings:** `well-formed JSON string`, `null-terminated buffer`, `deep-copied instance`, `newline-delimited list`.
- **Commit/error:** `thread-safe cache`, `null-terminated input`, `non-negative integer`.

### Paradigm-specific key terms

- **OOP:** `read-only property`, `lazy-initialized singleton`, `thread-safe collection`, `reference-counted pointer`.
- **Functional:** `pure-function semantics`, `higher-order function`, `persistent-data structure`, `lazily-evaluated sequence`, `lock-free CAS loop`.
- **Procedural:** `null-terminated string`, `zero-initialized struct`, `statically-linked binary`, `newline-delimited output`.
- **Declarative:** `left-joined table`, `fully-qualified column name`, `user-provided input`, `well-formed document`, `base64-encoded value`.
- **Systems:** `move-semantics transfer`, `borrow-checked reference`, `memory-mapped I/O`, `copy-on-write page`, `lock-free stack`, `use-after-free bug`.

### Edge cases

1. **Hyphenated tool names** (`create-react-app`, `eslint-plugin-react`): keep the name as-is; do not add a second hyphen when used as a modifier.
2. **Code keywords** (`typeof`, `nonlocal`, `FULL OUTER JOIN`): hyphenate in prose when used as a compound adjective, but reproduce the keyword exactly in code spans.
3. **Generated output:** do not manually hyphenate generator output; configure the generator if you control it, else add a NOTE.
4. **Established unhyphenated compounds** (`filename`, `namespace`): keep the established form if it is unambiguous and consistent.
5. **URL path segments** (kebab-case, e.g. `/api/user-settings`): keep the exact path form; hyphenate prose compound adjectives normally.

### Grammar notes

- **Attributive (before noun) = hyphen; predicative (after verb) = no hyphen:** `The thread-safe collection` vs `The collection is thread safe`.
- **Adverb ending in -ly: no hyphen** — `a fully qualified name`, NOT `a fully-qualified name`.
- **"self-" prefix always takes a hyphen:** `self-contained`, `self-signed`, `self-healing`.
- **Temporary compounds:** `write lock` (separate) vs `write-lock` (compound noun before another noun); `run time` (noun phrase) vs `run-time` (compound adjective).

### Cross-references
Rule 1.1 (approved words), Rule 1.5 (technical nouns), Rule 1.9 (short technical nouns), Rule 1.11 (consistent terms), Rule 8.1 (punctuation), Rule 8.6 / 8.7 (hyphenated counts as one word).

---

## Rule 8.3 — Use of Parentheses

**Rule:** You can use parentheses for seven purposes:

1. References to code modules, diagrams, or text — `Call the request handler (Figure 3, Module A).`
2. Letters or numbers that identify items in a diagram or text — `Disconnect the endpoints (2) and (12) from the load balancer (8).`
3. Identifying work steps in a procedure — `(1) Install the dependency package (4) in the project directory (8).`
4. Including abbreviations — `A Command Line Interface (CLI) is a text-based interface...`
5. Giving singular and plural at once — `Before you run the test(s), set the environment variable(s).`
6. Explaining words or part of a sentence — `Increase the timeout slowly (not more than 1000 ms each step).`
7. Including an alternative — `Use the left (right) API key for the staging (production) environment.`

**Key patterns:**

- **Abbreviation placement:** always `Full Term (ABBR)` — never the reverse. After first definition, use only the abbreviation.
- **Never nest parentheses.** If you need a nested aside, split into sentences.
- **Parenthetical counts as a separate sentence** with its own word-count limit (Rule 8.5).
- **Period goes outside** the closing parenthesis for a sentence-ending parenthetical that is not a complete sentence (`Set the log level to debug (recommended for development).`). A complete-sentence parenthetical should instead be its own sentence.

### Examples

- Non-STE: `A Representational State Transfer Application Programming Interface, or REST API, is an architectural style...`
- STE:    `A Representational State Transfer Application Programming Interface (REST API) is an architectural style...`

- Non-STE: `Run the migration on all database shard servers, the primary and all replica instances, before you deploy.`
- STE:    `Run the migration on all database shard(s) before you deploy.`

- Non-STE: `Cannot find the config file you specified; looked in /etc/myapp/config.yaml, ~/.config/myapp/config.yaml, and ./config.yaml...`
- STE:    `Cannot find the configuration file (searched: /etc/myapp/config.yaml, ~/.config/myapp/config.yaml, ./config.yaml).`

### Per-document-type guidance

- **README:** define abbreviations on first use; reference related docs concisely `(refer to docs/getting-started.md)`.
- **API docs:** explain parameter constraints or units `(ms)`; wrap status codes `(404 Not Found)`.
- **Docstrings:** show types/ranges `(1 to 30000)`; only clarify what the type system cannot express.
- **Commit messages:** `(auth)`, `(issue #482)`, `(regression from v2.3)` — short scope/issue identifiers.
- **Error messages:** put diagnostic data (paths, line numbers, actual vs expected) at the end in parentheses.

### Edge cases

1. **Framework names that are common words** (`Flask`, `React`): add a brief parenthetical on first use — `React (a JavaScript UI library)`.
2. **Code keywords** (`()`, `<T>`): keep the code literal exact; explain in a separate sentence, not a nested parenthesis.
3. **Generated docs:** leave auto-inserted signatures/types untouched; apply the rule to human-written description fields.
4. **Nested parentheses:** split the sentence instead.
5. **CLI help text:** prefer alternative-use (`--verbose (--quiet)`) or explanation (`--timeout MS (default: 5000)`) patterns.

### Cross-references
Rule 1.1 (approved words), Rule 1.3 (approved meanings), Rule 1.9 (short technical nouns), Rule 5.1 / 6.3 (length, steps), Rule 8.2 (hyphens ≠ parentheses). Square brackets `[ ]` are reserved for optional parameters in code syntax — use parentheses, not brackets, for prose asides.

---

## Rule 8.4 — Colon in a Vertical List

**Rule:** In a vertical list, a colon (:) has the same effect on word count as a period and shows the end of a sentence.

- The introductory text before the colon obeys the length limits: ≤ 20 words (procedural), ≤ 25 words (descriptive).
- Each list item after the colon counts as a **new sentence** with its own limit (20 / 25 words).
- A colon before a vertical list is **always** a sentence boundary. Enumerated items are always vertical, never inline.

### Examples

Non-STE (31-word intro burying three cases):
`To handle all possible error conditions, the following exception types must be caught...: database connection timeouts..., authentication failures..., and validation errors...`

STE:
```
To handle possible error conditions, the error handler catches these exception types:
- Database connection timeout
- Authentication failure
- Validation error.
```

STE (config profiles):
```
The configuration file supports these environment profiles:
- Development
- Staging
- Production.
```

### Per-document-type guidance

- **README:** keep the introduction to the category; move version/compat notes into list items or a separate sentence.
- **API docs:** name the endpoint/resource and state what it enumerates; put type/default/optionality in each item.
- **Docstrings:** `Args:`, `Returns:`, `Raises:` introductions are usually trivially compliant; keep custom headers short.
- **Commit messages:** the subject line is NOT a list intro; keep any body intro short.
- **Error messages:** short intro (`The command failed for one of these reasons:`); each cause/recovery step is a separate sentence.

### Paradigm-specific guidance

- **OOP:** name the class/method in the intro; put type/default/constraint in each item.
- **Functional:** name the type/function; describe each variant/arm independently.
- **Procedural:** write a short goal before the colon, then imperative steps.
- **Declarative:** name the resource/option; one value/rule/setting per item.
- **Systems (safety-critical):** enumerate each precondition/safety condition as its own item; never bury it in the intro.

### Edge cases

1. **Inline code in intro:** each backtick token counts as one word (e.g. `docker-compose` = 1 word). Prefer intros with ≤ 15 words and few code tokens.
2. **Nested lists:** limit to one level; parent items are short category headings with their own colon.
3. **Code blocks inside list items:** the prose intro obeys the limit; the block itself is exempt.
4. **Long framework names:** move them into the list items; keep the intro generic.
5. **Generated docs:** obey the rule in the source comments you write; accept generator boilerplate (`Options:`, `Commands:`).

### Cross-references
Rule 1.1 (approved words in items), Rule 3.1 (one subject-verb-object per item), Rule 4.1 (length at two points: intro + each item), Rule 6.3 (procedural lists), Rule 8.1 (colon replaces semicolon-joined enumerations). Use a colon, **not** an em-dash (—), to introduce a vertical list.

---

## Rule 8.5 — Parentheses and Word Count

**Rule:** Text in parentheses counts as **one word** in the enclosing sentence. But the words inside the parentheses also form a **separate sentence** and must obey the length limit.

Identifiers in parentheses (a number, a letter, an alphanumeric identifier, or an abbreviation) count as one word.

Two categories of parentheticals:

- **Identifier parentheticals** — a number, letter, code, or abbreviation: `(10)`, `(EACCES)`, `(CI/CD)`, `(v2.1)`. Count as one word; no sentence-length limit (not prose).
- **Explanatory parentheticals** — prose that explains or qualifies: `(the DEBUG flag is off)`, `(the worker runs every 60 seconds)`. Count as one word in the main sentence but form a separate sentence subject to 20/25-word limits.

**Examples:**

- `Make sure that the DEBUG environment variable is set to false (the DEBUG flag is off).` — 12 words in the main sentence; the parenthetical is a 5-word separate sentence.
- `Remove the health check flag (10).` — 5 words; the identifier `(10)` is one word.
- `Configuration of a Continuous Integration/Continuous Deployment (CI/CD) Pipeline` — 7 words; `(CI/CD)` is one word.

**Key principle:** Use parentheses for clarifications, examples, and secondary qualifications. **Never** use parentheses for safety conditions, required steps, or warnings the reader must act on — those deserve their own sentence or a labeled block (`BREAKING`, `DEPRECATED`, `NOTE`).

### Examples

- Non-STE: `...production cluster (the DEBUG flag must be explicitly disabled for all production workloads to prevent accidental log leakage).`
- STE:    `Make sure that the DEBUG environment variable is set to false (the DEBUG flag is off).`

- Non-STE: `Cannot write to the configuration file (check that the file exists and is not read-only, that the parent directory is writable, and that your user account has the necessary file permissions...).`
- STE:
  ```
  Error: Cannot write to the configuration file.
  To fix this problem:
  - Make sure that the file exists.
  - Make sure that the file is not read-only.
  - Make sure that the parent directory is writable.
  - Make sure that your user account has the necessary permissions.
  ```

### Per-document-type guidance

- **README:** split long conditional asides into their own sentence before the instruction.
- **API docs:** keep parentheticals to identifiers/short qualifiers `(int, optional)`, `(default: 30)`; move conditional logic to a NOTE.
- **Docstrings:** keep parentheticals short; move algorithmic explanations out.
- **Commit messages:** issue refs `(#1234)` and scope `(auth)` are identifiers (one word each); put justification in the body, not parentheses.
- **Error messages:** each parenthetical `(Error code: EACCES)` is a separate sentence; recovery steps belong in separate sentences, not a parenthetical.

### Edge cases

1. **Function-call notation** (`authenticate()`, `parse(input)`): backtick-delimited code tokens are atomic — one word; the parens inside are not Rule 8.5 parentheticals.
2. **URLs in parentheses:** an identifier-like URL counts as one word; if the parenthetical also has explanatory text, that text forms a separate sentence.
3. **Nested parentheses:** do not use them; eliminate one level by making the outer aside its own sentence.
4. **Library names with parens** (`expect()`): keep in backticks (one word); parens are part of the identifier.
5. **Generated docs:** follow the rule for parentheticals you write; accept auto-inserted defaults.

### Cross-references
Rule 1.5 / 1.6 (technical nouns in parentheticals), Rule 3.1 (parenthetical is a simple sentence), Rule 3.3 (long parentheticals signal a paragraph restructure), Rule 4.1 (limit applies to the parenthetical too), Rule 8.1 (no semicolons inside parentheticals), Rule 8.4 (parenthetical inside a list item).

---

## Rule 8.6 — Elements That Count as One Word

**Rule:** When counting words for sentence length, count each of these as **one word**:

1. **Numbers** — `13`, `16`, `twenty-one`. (Do not count numbers that identify paragraphs or work steps — they are document numbering.)
2. **Numbers with units of measurement** — `10 ms`, `20 MB`, `10 μs`, `10 milliseconds`.
3. **Abbreviations** (acronyms/initialisms) — `VPN`, `OWASP`, `CI/CD`, `JWT`, `a.m.`.
4. **Alphanumeric identifiers** — `No. 1`, `E36L7`, `cache.miss.count`, `http.client.retry.max.attempts`.
5. **Quoted text** — `"Service Overview"`, backtick-quoted code (`C = (A - B) - 0.063 mm`), inline `<code>`, formulas. Each quoted span = one word.
6. **Titles, headings, and text on UI elements/labels** — `Operations Runbook`, `Error Handling and Recovery`, dialog/warning text you cannot change.
7. **Proper nouns** of individuals, groups, organizations, geopolitical entities — `Linus Torvalds`, `Apache Software Foundation`, `AWS Lambda`, `Azure AD B2C`.

**Why this matters:** applying Rule 8.6 collapses many multi-word elements into single-word counts, so sentences that look too long are often compliant. This is the largest reduction in API docs and README files (highest identifier/abbreviation density).

### Examples

- `The JWT authentication middleware must validate the signature of each incoming request. The token must have an expiry time of not more than 360 seconds to be valid for processing.` — `JWT` (1 word), `360 seconds` (1 word).
- `In application.properties, set http.client.retry.max.attempts to 5. Set http.client.retry.backoff.millis to 1000.` — each property name is an alphanumeric identifier (1 word); `5` and `1000` are numbers (1 word).
- `Call useUserProfile(userId) to get the current user profile.` — `useUserProfile(userId)` is quoted text (1 word).
- `In the Kubernetes manifest, set the checkout container to 250m CPU and 512Mi memory.` — `250m CPU`, `512Mi` are numbers with units (1 word each).

### Per-document-type guidance

- **README:** project names, badge URLs, version numbers, tool abbreviations each = 1 word.
- **API docs:** endpoint paths, HTTP status codes, parameter names each = 1 word.
- **Docstrings:** parameter/return/exception types each = 1 word.
- **Commit messages:** issue IDs, branch names, command names each = 1 word.
- **Error messages:** error codes, field names, type identifiers each = 1 word.

### Edge cases

1. **Framework names with "unapproved" words** (`Express`, `Swift`, `React`): proper nouns, 1 word; do not rewrite them.
2. **Code keywords** (`class`, `return`): quoted text, 1 word; keep them — do not replace with synonyms.
3. **Generated code/comments:** count as one word (category 6/7) when you cannot change them.
4. **Nested quoted text:** the outer backtick/`<code>` boundary defines the span; everything inside = 1 word.
5. **Semantic versions / hashes:** `1.2.3-alpha.1+build.456`, commit `a1b2c3d`, digest `sha256:abc...` = 1 word each. `Version 1.2.3` = 2 words.
6. **Document part numbers:** rule/section numbers (`Rule 8.7`), step numbers (`Step 3`), and ticket IDs (`PROJ-4821`, alphanumeric identifier) are not quantity counts.

### Cross-references
Rule 1.1 (proper nouns/identifiers exempt from approved-word check), Rule 1.5 / 1.6 (technical nouns), Rule 1.14 (American spelling of proper nouns), Rule 8.7 (hyphenated = one word), Rule 4.1/4.2 (sentence-length limits this rule feeds).

---

## Rule 8.7 — Hyphenated Words Count as One Word

**Rule:** Hyphenated words count as one word. A hyphenated group (compound adjective or long technical noun) is a single unit and counts as one word for sentence-length measurement.

### Case 1: Hyphenated compound adjectives (before a noun)

`read-only file descriptor`, `thread-safe singleton`, `event-driven architecture`, `low-latency cache`, `client-side rendering pipeline`, `end-to-end test suite`, `backward-compatible API`. The hyphen is a pre-noun signal only: after the noun or a linking verb, write the words separately and count each — `The singleton is thread safe` (5 words, not 4).

### Case 2: Long hyphenated technical nouns

The whole hyphenated group counts as one word; the following words are separate:
- `build-time environment variable` → `build-time` / `environment` / `variable`
- `client-side rendering pipeline` → `client-side` / `rendering` / `pipeline`
- `end-to-end test suite` → `end-to-end` / `test` / `suite`
- `check-out request handler` → `check-out` / `request` / `handler`

### Why it matters

STE-Code limits procedural sentences to 20 words and descriptive to 25 (Rules 4.1, 4.2). Counting each word inside a hyphenated term over-reports length and may break a limit the sentence actually meets.

- `The build-time environment variable must point to the staging cluster.` → 10 words (`build-time` is 1).
- `The thread-safe singleton must cache the read-only file descriptor.` → 9 words (`thread-safe` and `read-only` are 1 each).

### Interaction with other rules

- **Rule 8.2 (hyphens):** hyphenate per 8.2, then count the unit as one word per 8.7.
- **Rule 8.6:** a hyphenated word is a separate case — it is not also an abbreviation or identifier. Do not double-count.

### Common code-domain hyphenated terms (each = one word before a noun)

| Term | Type |
|------|------|
| read-only, write-only, thread-safe, event-driven | compound adjective |
| client-side, server-side, end-to-end, backward-compatible, low-latency | compound adjective |
| build-time, run-time, sign-in, check-out, request-response | technical noun |

When a term in this table follows the noun or a linking verb, write it as separate words and count each.

### Cross-references
Rule 8.2 (when to hyphenate), Rule 8.6 (other one-word elements), Rule 4.1 / 4.2 (sentence-length limits).

---

## Quick Reference — Section 8 at a Glance

| Rule | One-line summary |
|------|------------------|
| 8.1 | No semicolons in prose. Split into two or more sentences. |
| 8.2 | Hyphenate directly related words (compound adjectives, number+noun, prefix-vowel). |
| 8.3 | Use parentheses for refs, IDs, steps, abbreviations, `(s)`, explanations, alternatives. Never nest. |
| 8.4 | A colon before a vertical list is a sentence boundary; intro ≤ 20/25 words, each item is a new sentence. |
| 8.5 | Parenthetical text = 1 word in the main sentence but a separate sentence with its own limit. |
| 8.6 | Numbers, units, abbreviations, identifiers, quoted text, titles, proper nouns each count as 1 word. |
| 8.7 | Hyphenated words count as 1 word. |

**Remember:** these rules govern documentation *prose* only. Source code and text inside code blocks / backticks are exempt.
