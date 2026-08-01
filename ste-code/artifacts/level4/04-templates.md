# Level 4 — Document Templates + Extension Vocabulary + Reference Catalogue

This slice gives the fill-in templates for every code-documentation type, the
sentence-level rules that govern them, the STE-Code extension vocabulary that
lower tiers omit, and the vendor/community reference catalogue.

It pairs with `01-principles.md` (word rules 1.1–1.14), `02-synonyms.md` (the 19
technical noun categories), and `03-dictionary.md` (controlled terminology).

Use this file when an LLM must **produce** or **review** a concrete document:
a review comment, a pull-request description, a README procedure, an API entry,
a docstring, a commit message, or an error message.

## Contract for every template

1. **Word gate** — each word passes one of: approved in the controlled
   terminology, a code-domain technical noun (Rule 1.5, 19 categories), or a
   code-domain technical verb (Rule 1.12).
2. **Imperative action** — every instruction line starts with a base verb. No
   modal verb, no passive voice, no gerund (Rule 5.3).
3. **One technical noun per item** — name the same symbol the same way every
   time, in backticks, uninflected (Rules 1.5, 1.11).
4. **Condition first** — a condition precedes its command and is separated by a
   comma (Rule 5.4).
5. **Active voice** — passive only when the agent is unknown (Rule 3.6).
6. **Consistent style** — one term, one syntax, one meaning per concept
   (Rule 9.4).

---

## Governing rules

### Rule 5.3 — Imperative (command) form for instructions

Write every instruction in the imperative: start with a base verb, omit the
implied subject "you", give one direct instruction.

- Do not use passive voice ("The tests are run by CI"), gerunds ("Running the
  tests…"), or modal verbs ("can", "could", "should", "may", "might", "would").
- Do not put "must" before an imperative in a standard instruction. Reserve
  "must" for WARNING and CAUTION blocks (security, data loss, safety):
  "WARNING: IF YOU MUST REMOVE THE DATABASE, FIRST MAKE A BACKUP."
- Use the base verb: "Set the port to 8080", not "The port should be set to
  8080".

Document-type boundaries:

| Document type | Imperative applies to | Descriptive applies to |
|---|---|---|
| README | install, configure, build, quick-start | goals, features, architecture |
| API docs | setup, auth walkthroughs, getting started | endpoint behavior, responses |
| Docstrings / comments | shell-script headers, Makefile targets | function and method behavior |
| Commit messages | subject line | body rationale |
| Error messages | the recovery instruction | the failure statement |

> **Non-STE:** The test suite can be executed with `npm test`.
>
> **STE:** Run the unit tests with `npm test`.

> **Non-STE:** Before you delete the branch, you must push all local commits.
>
> **STE:** Before you remove the branch, push all local commits to the remote.

### Rule 5.4 — Descriptive statement before the command

When the reader must know a condition before they act, write the condition as a
descriptive statement, then a **comma**, then the imperative command. The comma
is required: its position decides which verb an adverb modifies.

> **STE:** If the connection pool is full, reject the request.
> (comma after "full" → "reject" is the command)
>
> **STE:** If the connection pool is full automatically, reject the request.
> (comma after "automatically" → the pool fills on its own)

- Keep one condition per sentence. Write each condition–command pair of a
  multi-step procedure as its own step.
- Apply this shape inside T2 (`Result` → `Required change`), T4 (`Scope` sets
  the condition), T5 (`How` steps), T7, T8, and T11.

> **Non-STE:** Run the database migration after you set `DATABASE_URL` and
> confirmed the server accepts connections.
>
> **STE:** After you set the `DATABASE_URL` variable, run the database migration.

### Rule 3.6 — Active voice

The subject does the action. Passive voice is permitted in descriptive writing
only when the agent is unknown.

Test: ask "by whom or by what?" If the sentence answers that question, it is
passive — make the agent the subject.

- **Passive:** The connections are opened by a pool manager.
- **Active:** A pool manager opens the connections.
- **Passive, agent unknown, allowed:** During transmission, the data was
  corrupted.

### Rule 9.4 — Consistent style

Use the same style every time the same type of step occurs. Audit three
dimensions independently:

- **Lexical** — one term per concept ("configuration file", never alternating
  with "settings file" or "config").
- **Syntactic** — the same grammatical template for the same action type.
- **Semantic** — a term keeps one meaning across every file, module, and
  document type.

Per document type:

| Document type | Consistency requirement |
|---|---|
| README | one word for the project artifact ("library", not "package" later) |
| API docs | one name per endpoint and parameter across all references |
| Docstrings | the same term as the signature (`max_retries`, not "maximum attempts") |
| Commit messages | one imperative verb per change category ("Add", never mixed with "Introduce") |
| Error messages | one error code produces the same text every time |
| CLI / help text | a flag description matches `--help`, man pages, docs, errors |

```markdown
## Non-STE (inconsistent)
1. Open the configuration file in a text editor.
2. Change the port number in the settings file.
3. Save the config and close it.
4. Compile the project with the build command.
5. Make the binary for the target platform.

## STE (consistent)
1. Open the configuration file in a text editor.
2. Change the port number in the configuration file.
3. Save the configuration file and close it.
4. Build the project with the build command.
5. Build the binary for the target platform.
```

### Rule 1.5 grammar — technical nouns in running text

Identifiers, file paths, type names, commands, and status codes are code-domain
technical nouns. Apply this grammar in all template prose:

- **Backticks, no inflection.** Write `getUser`, `null`, `OrderService`. Not
  "the `getUser`s". Acronym plurals: `APIs`, not `API's`.
- **One name per item (Rule 1.11).** `getUser` stays `getUser` — not "the
  getter", then "that helper".
- **Articles.** "the" for a specific instance, "a"/"an" for an indefinite one,
  no article for a plural general reference.
- **Possessive only for roles and organizations (category 11).** "the user's
  session data", but "the configuration of the `Docker` container".
- **Capitalization.** Proper nouns keep theirs (`TypeScript`, `PostgreSQL`);
  common technical nouns are lowercase unless they start the sentence.
- **Quoted keywords and status codes (category 10).** `if`, `return`, `class`,
  `404 Not Found`, `500` are quoted text, never a bare number.

---

## Template selection

| Situation | Template |
|-----------|----------|
| One line or one hunk in a diff | T1 — Inline review comment |
| A defect the author must fix before merge | T2 — Blocking review finding |
| An optional improvement | T3 — Non-blocking suggestion |
| Summary on the whole pull request | T4 — PR review summary |
| PR description the author writes | T5 — PR description |
| Reply to review feedback | T6 — Author response |
| Setup / install / build steps | T7 — README procedure |
| API endpoint reference entry | T8 — API doc entry |
| Function or method docstring | T9 — Docstring |
| A completed change | T10 — Commit message |
| A runtime failure the user sees | T11 — Error message |

---

## T1 — Inline review comment

```text
<observation>: one sentence, one subject, present tense.
<effect>: one sentence that gives the result of the observation.
<action>: one imperative sentence.
```

> The `getUser` function returns `undefined` when `id` is `0`.
> The caller in `UserController` then reads a property of `undefined`.
> Return `null` for an unknown `id`, and check the result in `UserController`.

Constraints: imperative action (Rule 5.3); one name per item (Rule 1.11); no
technical noun used as a verb (Rule 1.7) — "Send a request to the `/users`
endpoint", not "Endpoint the request".

## T2 — Blocking review finding

```text
**Finding:** <one sentence: what is wrong>
**Location:** `<path>:<line>` in `<symbol>`
**Cause:** <one sentence>
**Result:** <one sentence: what fails, and when>
**Required change:** <one imperative sentence>
```

> **Finding:** The `saveOrder` method does not do a check of the `quantity` field.
> **Location:** `src/orders/service.ts:142` in `OrderService.saveOrder`
> **Cause:** The method writes the request body to the database with no check.
> **Result:** A negative `quantity` value is written to the `orders` table.
> **Required change:** Reject a request when `quantity` is less than `1`.

The field label carries the obligation, so do not add "must" as an intensifier.

## T3 — Non-blocking suggestion

```text
**Suggestion (optional):** <one imperative sentence>
**Reason:** <one sentence>
```

> **Suggestion (optional):** Move the three retry constants into `RetryPolicy`.
> **Reason:** The same three values occur in `HttpClient` and in `QueueWorker`.

Mark the item optional in the first word. Use no hedge words ("maybe",
"perhaps", "just") — Rule 1.10.

## T4 — PR review summary

```text
**Decision:** Approve | Request changes | Comment
**Scope:** <one sentence: what the pull request changes>
**Blocking findings:** <count>
1. <one sentence each, with `path:line`>
**Optional suggestions:** <count>
1. <one sentence each>
**Verification:** <one sentence: what you ran or read>
```

> **Decision:** Request changes
> **Scope:** The pull request adds a rate limiter to the `/api/v1/login` route.
> **Blocking findings:** 1
> 1. `src/middleware/rateLimit.ts:58` — The limiter counts a failed request and a successful request in the same bucket.
> **Optional suggestions:** 1
> 1. Give the `WINDOW_MS` constant a unit in its name.
> **Verification:** I ran `npm test` and read the diff in `src/middleware`.

`Decision` is one of the three approved values — no fourth value, no sentence.

## T5 — PR description (author)

```text
## What
<one to three sentences. One subject in each sentence.>

## Why
<one to three sentences. Give the cause, then the result.>

## How
1. <imperative sentence>
2. <imperative sentence>

## Test
- <one sentence per check, with the command in backticks>

## Risk
<one sentence. Write "None." when there is no risk.>
```

> ## What
> This pull request adds a retry to the `PaymentClient.charge` method.
> ## Why
> The payment gateway returns `503` during a deployment. The current client fails
> the order on the first `503` response.
> ## How
> 1. Add a `RetryPolicy` class with three attempts and an exponential delay.
> 2. Call `RetryPolicy.execute` from `PaymentClient.charge`.
> ## Test
> - Run `npm test -- payment` to check the new unit tests.
> - Send a request to the sandbox gateway to check the delay values.
> ## Risk
> A retry can create a duplicate charge if the gateway accepted the first
> request. The client sends an idempotency key to prevent this result.

`How` steps are imperative (Rule 5.3). `What` and `Why` are descriptive but
still use approved words and one name per item.

## T6 — Author response to feedback

```text
**Comment:** <link or `path:line`>
**Response:** Done | Changed | Not changed
**Detail:** <one sentence>
```

> **Comment:** `src/middleware/rateLimit.ts:58`
> **Response:** Changed
> **Detail:** The limiter now counts only a failed request in the login bucket.

Use one of the three approved values. Use no "LGTM", "nit", or "wontfix"
(Rule 1.10).

## T7 — README procedure (install / configure / build)

Use the imperative only in procedural steps. Keep one condition–command pair per
step (Rule 5.4). Name the same file, command, and variable identically in all
steps (Rule 9.4).

```text
## Setup

Clone the repository.
Install the dependencies with `npm install`.
Set the `DATABASE_URL` environment variable in `.env`.
After the dependencies install without errors, run the development server with `npm run dev`.
```

> **Non-STE:** First you need to have Node.js version 18 or higher installed then
> run `npm install` and after all dependencies finish downloading if there are no
> errors you can run `npm run build`…
>
> **STE:** Make sure that Node.js version 18 or higher is installed. Run `npm
> install`. After the dependencies install without errors, run `npm run build`.

Descriptive README sections (About, Features, Architecture) use declarative
sentences — they do not instruct the reader to act.

## T8 — API doc entry (endpoint reference)

Endpoint behavior is descriptive. The imperative applies to setup, auth
walkthroughs, and getting-started steps. State the condition that triggers an
error before you describe the response (Rule 5.4).

```text
### GET /users

Gets the list of users.

Request:
GET /users HTTP/1.1
Authorization: Bearer ***

Response:
200 OK — a JSON array of user records.

Errors:
If the client sends more than 100 requests per minute, the API returns a
`429 Too Many Requests` status code. The response includes a `Retry-After`
header that shows the wait time.
```

> **Non-STE:** You can authenticate by sending a POST request to `/auth/login`
> with your credentials, and you should include the returned token in the
> Authorization header.
>
> **STE:** Send a POST request to `/auth/login` with your credentials. Include
> the returned token in the `Authorization` header.

## T9 — Docstring (function / method)

Describe what the code does, in the active voice (Rule 3.6), not what the reader
must do. State preconditions before behavior (Rule 5.4). Use the same term as
the signature (Rule 9.4).

```python
def get_profile(user_id: int) -> Profile:
    """Return the profile data for the given user ID.

    Query the database for the row that matches `user_id` and return
    a Profile object. If the user does not exist, raise ValueError.
    """
    return db.query(Profile).filter_by(id=user_id).one()
```

> **Non-STE:** Gets a user record. The duration in milliseconds the client shall
> await a response prior to terminating the connection attempt.
>
> **STE:** Gets a user record. The time in milliseconds that the client waits for
> a response before it stops the connection.

## T10 — Commit message

The subject line is imperative and completes "If applied, this commit will…"
(Rule 5.3). The body may use descriptive sentences. Use one imperative verb per
change category across the project (Rule 9.4).

```text
Fix the race condition in the connection pool

The pool returned the same connection to two threads under load.
Add a lock around the checkout path so each thread gets a unique
connection. The retry test in tests/test_pool.py now passes.
```

> **Non-STE:** Fixed the race condition in the connection pool.
>
> **STE:** Fix the race condition in the connection pool.

> **Non-STE:** When the connection pool reaches max connections, add a mutex lock
> around pool access to prevent a race condition.
>
> **STE:** When the connection pool reaches its maximum capacity, add a mutex
> lock around pool access to prevent a race condition.

## T11 — Error message

Describe what failed, then give a recovery instruction, separated by a period or
a newline. One error code produces the same text every time (Rule 9.4).

```python
raise RuntimeError(
    "The port 8080 is already in use. "
    "Set a different port with the --port option."
)
```

> **Non-STE:** Port is already in use.
>
> **STE:** The port 8080 is already in use. Set a different port with the
> `--port` option.

> **Non-STE:** Invalid configuration file. Check the schema.
>
> **STE:** The configuration file failed schema validation. Check the
> `config.schema.json` file for required fields.

---

## Approved verbs for action lines

Use these code-domain technical verbs in the imperative line of any template.
Use the base form for an instruction (Rule 5.3) and the third-person form for a
statement of fact.

| Verb | Use it for |
|------|-----------|
| add | New code, a new field, a new file |
| remove | Deleted code or a deleted field |
| replace | One item exchanged for another |
| move | Code relocated with no change in behavior |
| rename | A new name for the same item |
| return | The value a function gives back |
| throw / raise | An error the code emits |
| catch / handle | An error the code accepts |
| validate | A check on input |
| reject | A refused input or request |
| call | Invocation of a function or method |
| read / write | Access to a file, field, or record |
| log | A record written to the audit trail or log |
| test | A check that runs in the test suite |

Do not use a verb from this table as a noun (Rule 1.13): "The function returns a
value", not "The return of the function".

## Forbidden words in template prose

| Forbidden | Reason | Use instead |
|-----------|--------|-------------|
| nit, LGTM, WIP, PTAL, IMO | jargon (Rule 1.10) | the full template label |
| smelly, hacky, ugly, clean | subjective, not approved (Rule 1.1) | the concrete defect |
| stuff, thing, some code | not a technical noun (Rule 1.5) | the identifier in backticks |
| leverage, utilize | not approved (Rule 1.3) | use |
| behaviour, initialise, colour | British spelling (Rule 1.14) | behavior, initialize, color |
| we should maybe possibly | hedging (Rule 1.1) | one imperative sentence |
| delete (verb) | not approved (Rule 1.1) | remove |
| execute (verb) | not approved (Rule 1.1) | run |
| compile (verb) | not approved (Rule 1.1) | build |

## Dictionary excerpt — instruction and template words

A focused slice of the controlled terminology (full list in `03-dictionary.md`).
UPPERCASE = approved; ✗ = not approved, use the listed alternative. Parts of
speech: (v) verb, (n) noun, (adj) adjective, (conj) conjunction, (TN/TV)
code-domain technical noun/verb.

| Word | PoS | Approved? | STE example | Non-STE to replace |
|------|-----|-----------|-------------|--------------------|
| ADD | (v) | ✓ | Add 5 lines of configuration to the file. | Append 5 lines of configuration to the file. |
| AFTER | (conj) | ✓ | After you deploy the update, do a smoke test. | Following deployment of the update, do a smoke test. |
| BEFORE | (conj) | ✓ | Before you run the migration, read the release notes. | Prior to running the migration, read the release notes. |
| CHECK | (n) | ✓ | Do a check of the input values. | Validate the input values. |
| CHECK | (v) | ✗ | Do a check of the values. / Verify the data integrity. | Check the values. |
| CLICK | (v) (TV) | ✓ | Click the "Submit" button. | Press the "Submit" button. |
| CREATE | (v) | ✓ | Create a new instance of the class. | Instantiate a new object of the class. |
| DELETE | (v) | ✗ | Remove the file from the directory. | Delete the file from the directory. |
| IF | (conj) | ✓ | If the status code is 500, retry the request. | In the event of a 500 status code, retry the request. |
| INSTALL | (v) | ✓ | Install the package with npm. | Set up the package with npm. |
| MAKE | (v) | ✓ | Make a copy of the file. | Create a copy of the file. |
| OPEN | (v) | ✓ | Open the file for reading. | Read the file. |
| REMOVE | (v) | ✓ | Remove the deprecated function. | Delete the deprecated function. |
| REPLACE | (v) | ✓ | Replace the old library with the new one. | Swap the old library for the new one. |
| RUN | (v) | ✓ | Run the script from the terminal. | Execute the script from the terminal. |
| SAVE | (v) | ✓ | Save the file to disk. | Write the file to disk. |
| SELECT | (v) | ✓ | Select the database from the list. | Choose the database from the list. |
| SET | (v) | ✓ | Set the variable to 10. | Assign 10 to the variable. |
| TYPE | (n) (TN) | ✓ | The type of the variable is string. | The variable is a string. |
| USE | (v) | ✓ | Use the API to fetch data. | Utilize the API to fetch data. |
| WHEN | (conj) | ✓ | When the build finishes, deploy the artifact. | After the build finishes, deploy the artifact. |

Mapping notes for template authors:

- **execute → run**, **compile → build**, **delete → remove**, **instantiate →
  create**, **assign → set**, **utilize/leverage → use**, **press (UI) →
  click**, **choose → select**, **swap → replace**, **validate (verb) → do a
  check / verify**, **write (file) → save**.
- **IF / WHEN / AFTER / BEFORE** are approved for condition and sequence
  clauses (Rule 5.4). Keep the comma between the clause and the command.
- **CHECK** is approved as a noun with "do a check of"; do not use it as a verb.
- **TYPE** is a technical noun for a data type; do not use it as a verb
  ("type the command" → "enter the command").

---

## Extension vocabulary (level 4 and above)

These adjectives are approved additions to the controlled terminology for the
code domain. Lower tiers omit them. Each entry gives one part of speech and one
approved meaning. Use the adjective to describe a property of code or an
operation; do not use it as a noun or a verb.

### idempotent (adj)

Describes an operation that produces the same result when applied more than
once, with no extra side effects after the first run.

> **STE:** Make the retry handler idempotent so a second call with the same
> input does not duplicate the record.
>
> **Non-STE:** Leverage an idempotent retry handler so a duplicate invocation
> will not create a redundant record.

### immutable (adj)

Describes a data structure or value that cannot be changed after it is created,
which prevents accidental shared-state defects.

> **STE:** Keep the request context immutable so concurrent threads cannot
> overwrite each other's values during a single operation.
>
> **Non-STE:** Utilize an immutable request context so concurrent threads will
> not overwrite shared values during processing.

### atomic (adj)

Describes an operation that completes fully or not at all, with no partial
result visible to other processes.

> **STE:** Wrap the balance update in an atomic transaction so the debit and the
> credit always succeed or fail together.
>
> **Non-STE:** Employ an atomic transaction to encapsulate the balance update so
> debit and credit always commit or roll back together.

### thread-safe (adj)

Describes code that functions correctly when more than one thread accesses it at
the same time, without external locking.

> **STE:** Make the singleton constructor thread-safe so two threads can call it
> on first use without creating two instances.
>
> **Non-STE:** Leverage a thread-safe singleton constructor so concurrent
> threads will not instantiate duplicate objects on first access.

### asynchronous (adj)

Describes a call or task that starts and returns before its work finishes, so
the caller can do other work meanwhile.

> **STE:** Make the file upload asynchronous so the user interface stays
> responsive while the transfer runs in the background.
>
> **Non-STE:** Utilize an asynchronous upload mechanism so the user interface
> remains responsive while the transfer executes in the background.

### concurrent (adj)

Describes tasks that make progress within the same time period, interleaved by
the scheduler rather than strictly sequentially.

> **STE:** Run the test suites in concurrent processes so the full check
> finishes in less time.

Extension summary:

| Word | PoS | Approved | Applies to |
|------|-----|----------|-----------|
| idempotent | adj | ✓ | repeated operations, retries |
| immutable | adj | ✓ | values, data structures |
| atomic | adj | ✓ | transactions, all-or-nothing operations |
| thread-safe | adj | ✓ | shared code under multiple threads |
| asynchronous | adj | ✓ | calls that return before completion |
| concurrent | adj | ✓ | interleaved tasks |

---

## Reference catalogue (vendor and community)

These external references inform the STE-Code controlled vocabulary. They are
**not** part of the standard. They are kept outside the standard, in
`.agents/reference/`, and are listed here as a catalogue.

| Reference | Type | Source |
|---|---|---|
| Microsoft Writing Style Guide | page | https://learn.microsoft.com/en-us/style-guide/welcome/ |
| MicrosoftDocs/microsoft-style-guide | page | https://github.com/MicrosoftDocs/microsoft-style-guide |
| Google Style Guides | page | https://google.github.io/styleguide/ |
| Kong/apiglossary | page | https://github.com/Kong/apiglossary |
| dwyl/technical-glossary | raw | https://raw.githubusercontent.com/dwyl/technical-glossary/main/README.md |
| jvalentino/glossary | page | https://github.com/jvalentino/glossary |
| GitHub Official Glossary | page | https://docs.github.com/en/get-started/learning-about-github/github-glossary |
| DevOps Style Guide Glossary | page | https://tydukes.github.io/coding-style-guide/glossary/ |
| ryanwi software-terms.dic | raw | https://gist.githubusercontent.com/ryanwi/6135845/raw/software-terms.dic |
| OpenSTE.org | pointer | https://openste.org/ |
| en-wl/wordlist (SCOWL) | page | https://github.com/en-wl/wordlist |
| MichaelWehar 5000-more-common | raw | https://raw.githubusercontent.com/MichaelWehar/Public-Domain-Word-Lists/master/5000-more-common.txt |
| dwyl/english-words | pointer | https://github.com/dwyl/english-words |

Use the catalogue to check whether a candidate term already has an accepted
form. A term found only in a reference is **not** approved by that fact alone —
it must still pass the three gates in `01-principles.md`.

---

## Checklist before you publish

1. Each sentence has one subject.
2. Each item has one name, used every time (Rule 1.11).
3. Each identifier is in backticks and is not inflected.
4. Each action is one imperative sentence (Rule 5.3).
5. Each condition comes before its command, separated by a comma (Rule 5.4).
6. Voice is active; passive appears only when the agent is unknown (Rule 3.6).
7. Terminology is consistent across the document and the project (Rule 9.4).
8. No word from the forbidden table is present.
9. Extension adjectives are used as adjectives only.
10. Spelling is American English (Rule 1.14).

