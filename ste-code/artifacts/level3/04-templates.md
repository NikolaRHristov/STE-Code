# Level 3 — Document Templates (All Code-Documentation Types)

This slice gives ready-to-fill templates for the document types where STE-Code
matters most in daily engineering work, and the rules that govern how a sentence
in any of them is built. It pairs with `01-principles.md` (words) and
`03-dictionary.md` (terminology).

Level 1 gave the word-level gate (Rules 1.1–1.14). Level 2 applied it to review
and pull-request text. Level 3 widens the lens to **every** code-documentation
type and states the governing sentence-level rules directly so an LLM can apply
them without cross-referencing the full standard.

Every template below follows the same three constraints:

1. **Word gate** — each word you add passes one of: approved in the controlled
   terminology (the STE-Code dictionary), a code-domain technical noun (Rule 1.5,
   19 categories), or a code-domain technical verb (Rule 1.12).
2. **Imperative action** — every instruction line starts with a base verb, no
   "must", no modal verb, no passive voice (Rule 5.3).
3. **One technical noun per item** — name the same symbol the same way every
   time, in backticks, uninflected (Rules 1.5, 1.11).

---

## Governing rules

These four sentence-level rules apply to every template in this slice. Read them
once; apply them everywhere.

### Rule 5.3 — Imperative (command) form for instructions

Write every instruction in the imperative (command) form: start with a base verb,
omit the subject "you" (implied), and give a direct instruction.

- Do **not** use passive voice ("The tests are run by CI"), gerunds
  ("Running the tests…"), or modal verbs ("can", "could", "should", "may",
  "might", "would").
- Do **not** put "must" before the imperative in a standard instruction. Reserve
  "must" for WARNING / CAUTION blocks (security, data loss, safety). Example:
  "WARNING: IF YOU MUST DELETE THE DATABASE, FIRST MAKE A BACKUP."
- Use the base verb for the action: "Set the port to 8080", not "The port should
  be set to 8080".

Document-type boundaries:

- **README** — use the imperative only for procedural sections (install,
  configure, build, quick-start). Descriptive sections (project goals, feature
  lists, architecture summary) may use declarative sentences.
- **API docs** — endpoint descriptions are descriptive ("Returns a list of
  users"); the imperative applies to setup, auth walkthroughs, and "getting
  started" steps. Example request blocks are inherently imperative.
- **Docstrings / inline comments** — describe behavior, don't command the
  reader ("This function returns the profile for the user ID", not "Return the
  profile"). Exception: shell-script headers and Makefile target comments, which
  the reader executes.
- **Commit messages** — the subject line is imperative and completes "If
  applied, this commit will…": "Fix the race condition", not "Fixed the race
  condition". The body may use descriptive sentences.
- **Error messages** — describe what failed, then give a recovery instruction,
  separated by a period or newline: "The port 8080 is already in use. Set a
  different port with the `--port` option."

> **Non-STE:** The test suite can be executed with `npm test`.
> **STE:** Run the unit tests with `npm test`.

> **Non-STE:** Before you delete the branch, you must push all local commits.
> **STE:** Before you delete the branch, push all local commits to the remote.

### Rule 5.4 — Descriptive statement before the command

When the reader must know a condition before they act, write it as a descriptive
statement, then a **comma**, then the imperative command. The comma is required:
its position determines which verb an adverb modifies.

> **STE:** If the connection pool is full, reject the request.
> (comma after "full" → "reject" is the command)
> **STE:** If the connection pool is full automatically, reject the request.
> (comma after "automatically" → the pool fills on its own)

- Keep one condition per sentence. For multi-step procedures, write each
  condition–command pair as a separate step.
- Apply inside every template that has a "condition then action" shape (T2
  `Result` → `Required change`, T4 `Scope` sets the condition, T5 `How` steps).

> **Non-STE:** Run the database migration after you set `DATABASE_URL` and
> confirmed the server accepts connections.
> **STE:** After you set the `DATABASE_URL` variable, run the database migration.

### Rule 3.6 — Active voice

Use the active voice in all code documentation. The subject does the action.
Passive voice is permitted in descriptive writing **only** when the agent (the
person, service, or component that does the action) is unknown.

Test: ask "by whom or by what?" If the sentence answers that question, it is
passive — convert by making the agent the subject.

- **Passive:** The circuits are connected by a switching relay.
- **Active:** A switching relay connects the circuits.
- **Passive (agent unknown, allowed):** During transmission, the data was
  corrupted.

### Rule 9.4 — Consistent style

When you select terminology or wording, use the same style every time the same
type of step occurs. Three dimensions, each audited independently:

- **Lexical** — one term per concept ("config file", never "settings file" /
  "config" / "config file" alternating).
- **Syntactic** — same grammatical template for the same action type ("Install
  the package to add the CLI tool"; don't switch some steps to passive or
  conditional).
- **Semantic** — a term keeps the same meaning across every file, module, and
  doc type ("build" means the same thing in the README as in the CI docs).

Apply per doc type:

- **README** — one word for the project artifact ("library", not "package" in
  paragraph 3).
- **API docs** — an endpoint/parameter has exactly one name across all
  references; map prose to the schema by name.
- **Docstrings** — use the same term as the function signature (parameter
  `max_retries`, not "maximum attempts").
- **Commit messages** — same imperative verb for the same category of change
  across the project ("Add", never "Introduce"/"Insert"/"Create" mixed in).
- **Error messages** — one error code produces the same text every time;
  operators search logs by message.
- **CLI / help text** — a flag's description matches in `--help`, man pages,
  docs, and error messages.

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
technical nouns. Apply this grammar whenever one appears in template prose:

- **Backticks, no inflection.** Write `getUser`, `null`, `OrderService`. Not
  "the `getUser`s" or "two `null`s". Acronym plurals: `APIs`, not `API's`.
- **One name per item (Rule 1.11).** Name a symbol the same way in one thread:
  `getUser`, not "the getter", then "that helper".
- **Articles.** "the" for a specific instance, "a"/"an" for an indefinite one,
  no article for a plural general reference: "The `UserController` handles a
  request. Pods run in a namespace."
- **Possessive only for roles/orgs (category 11).** "the user's session data"
  but "the configuration of the `Docker` container", not "the `Docker`
  container's configuration".
- **Capitalization.** Proper nouns keep theirs (`TypeScript`, `PostgreSQL`);
  common technical nouns are lowercase unless first word (`controller`,
  `endpoint`, `middleware`).
- **Quoted keywords and status codes (category 10).** `if`, `return`, `class`
  and codes like `404 Not Found`, `500` are quoted text: "Return `500 Internal
  Server Error`", not a bare "500".

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
| Function / method docstring | T9 — Docstring |
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

Constraints: imperative action (Rule 5.3); one technical noun per item (Rule
1.11); no technical noun as a verb (Rule 1.7): "Send a request to the `/users`
endpoint", not "Endpoint the request"; identifiers in backticks, uninflected.

## T2 — Blocking review finding

```text
**Finding:** <one sentence: what is wrong>
**Location:** `<path>:<line>` in `<symbol>`
**Cause:** <one sentence>
**Result:** <one sentence: what fails, and when>
**Required change:** <one imperative sentence>
```

> **Finding:** The `saveOrder` method does not validate the `quantity` field.
> **Location:** `src/orders/service.ts:142` in `OrderService.saveOrder`
> **Cause:** The method writes the request body to the database with no check.
> **Result:** A negative `quantity` value is written to the `orders` table.
> **Required change:** Reject a request when `quantity` is less than `1`.

Write the change as one imperative sentence. Do not use "must" as an intensifier
— the field label gives the obligation. `Location` names each item with one
technical noun (Rule 1.11).

## T3 — Non-blocking suggestion

```text
**Suggestion (optional):** <one imperative sentence>
**Reason:** <one sentence>
```

> **Suggestion (optional):** Move the three retry constants into `RetryPolicy`.
> **Reason:** The same three values occur in `HttpClient` and in `QueueWorker`.

Mark optional in the first word. One imperative sentence. No hedge words
("maybe", "perhaps", "just") — Rule 1.10.

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

Decision is one of the three approved values — no fourth, no sentence. Each
finding line is one sentence naming its item with one technical noun (Rule 1.11).

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

`How` steps are all imperative (Rule 5.3). `What` and `Why` are descriptive but
still use one technical noun per item (Rule 1.11) and approved words only.

## T6 — Author response to feedback

```text
**Comment:** <link or `path:line`>
**Response:** Done | Changed | Not changed
**Detail:** <one sentence>
```

> **Comment:** `src/middleware/rateLimit.ts:58`
> **Response:** Changed
> **Detail:** The limiter now counts only a failed request in the login bucket.

One of the three approved values. No "LGTM", "nit", "wontfix", or other jargon
(Rule 1.10). `Comment` gives the item in backticks with one name each time.

## T7 — README procedure (install / configure / build)

Use the imperative only for the procedural steps. Keep one condition–command pair
per step (Rule 5.4). Name the same file, command, and variable identically across
all steps (Rule 9.4).

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
> **STE:** Make sure that Node.js version 18 or higher is installed. Run `npm
> install`. After the dependencies install without errors, run `npm run build`.

Descriptive README sections (About, Features, Architecture) use declarative
sentences — they do not instruct the reader to act.

## T8 — API doc entry (endpoint reference)

Endpoint behavior is descriptive ("Returns a list of users"). The imperative
applies to setup, auth walkthroughs, and "getting started" steps. State the
condition that triggers an error before you describe the response (Rule 5.4).

```text
### GET /users

Gets the list of users.

Request:
GET /users HTTP/1.1
Authorization: Bearer <token>

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
> **STE:** Send a POST request to `/auth/login` with your credentials. Include
> the returned token in the `Authorization` header.

## T9 — Docstring (function / method)

Describe what the code does, in the active voice (Rule 3.6), not what the reader
must do. State preconditions before behavior (Rule 5.4). Use the same term as the
function signature (Rule 9.4).

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
> **STE:** Gets a user record. The time in milliseconds that the client waits for
> a response before it stops the connection.

## T10 — Commit message

Subject line is imperative and completes "If applied, this commit will…"
(Rule 5.3). The body may use descriptive sentences for rationale. Use one
imperative verb for the same category of change across the project (Rule 9.4).

```text
Fix the race condition in the connection pool

The pool returned the same connection to two threads under load.
Add a lock around the checkout path so each thread gets a unique
connection. The retry test in tests/test_pool.py now passes.
```

> **Non-STE:** Fixed the race condition in the connection pool.
> **STE:** Fix the race condition in the connection pool.

> **Non-STE:** When the connection pool reaches max connections, add a mutex lock
> around pool access to prevent a race condition.
> **STE:** When the connection pool reaches its maximum capacity, add a mutex
> lock around pool access to prevent a race condition. (condition before command,
> comma after the clause — Rule 5.4)

## T11 — Error message

Describe what failed, then give a recovery instruction, separated by a period or
newline. Do not use the imperative unless you also tell the user how to recover
(Rule 5.3). One error code produces the same text every time (Rule 9.4).

```python
raise RuntimeError(
    "The port 8080 is already in use. "
    "Set a different port with the --port option."
)
```

> **Non-STE:** Port is already in use.
> **STE:** The port 8080 is already in use. Set a different port with the
> `--port` option.

> **Non-STE:** Invalid configuration file. Check the schema.
> **STE:** The configuration file failed schema validation. Check the
> `config.schema.json` file for required fields.

---

## Approved verbs for action lines

Use these code-domain technical verbs in the imperative line of any template. Use
the base form for an instruction (Rule 5.3) and the third-person form for a
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

## Checklist before you publish

1. Each sentence has one subject.
2. Each item has one name, used every time (Rule 1.11).
3. Each identifier is in backticks and is not inflected.
4. Each action is one imperative sentence (Rule 5.3).
5. Each condition comes before its command, separated by a comma (Rule 5.4).
6. Voice is active; passive appears only when the agent is unknown (Rule 3.6).
7. Terminology is consistent across the document and the project (Rule 9.4).
8. No word from the forbidden table is present.
9. Spelling is American English (Rule 1.14).

---

## Dictionary excerpt — instruction and template words

A focused slice of the STE-Code controlled terminology (full list in
`03-dictionary.md`). UPPERCASE = approved; lowercase = not approved, use the
listed alternative. Parts of speech: (v) verb, (n) noun, (adj) adjective,
(conj) conjunction, (TN/TV) code-domain technical noun/verb.

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

Key mapping notes for template authors:

- **execute → run**, **compile → build**, **delete → remove**, **create → make**,
  **instantiate → create**, **assign → set**, **utilize/leverage → use**,
  **press (UI) → click**, **choose → select**, **swap → replace**, **validate
  (verb) → do a check / verify**, **write (file) → save**.
- Prepositions **IF / WHEN / AFTER / BEFORE** are approved for condition and
  sequence clauses (Rule 5.4). Keep the comma between the clause and the command.
- **CHECK** is approved as a noun with "do a check of"; do not use it as a verb.
- **TYPE** is a technical noun for a data type; do not use it as a verb
  ("type the command" → "enter the command").
