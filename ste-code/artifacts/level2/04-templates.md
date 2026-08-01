# Level 2 — Document Templates (Code Review / PR Feedback)

These templates apply STE-Code Level 2 to the two document types where controlled
words matter most in day-to-day engineering work: code review comments and pull
request feedback.

Level 1 gave the word-level gate (Rules 1.1–1.14) and the template shapes. Level 2
adds the **section-specific grammar rules** that govern how a review or PR sentence
is built once you have decided the words are allowed:

- the imperative (command) form for every action line (Rule 5.3),
- the descriptive-statement-before-command structure for findings and conditions
  (Rule 5.4),
- the technical-noun grammar for identifiers and code terms that appear in review
  text (Rule 1.5): backticks, one name per item, articles, possessive, plural,
  capitalization.

Each template below is a fill-in shape. Every word you add must pass one of the
three Level 1 gates:

1. It is approved in the controlled terminology (the STE-Code dictionary).
2. It is a code-domain technical noun (Rule 1.5, 19 categories).
3. It is a code-domain technical verb (Rule 1.12).

Identifiers, file paths, commands, and type names are technical nouns. Write them
in backticks and do not inflect them.

## Template selection

| Situation | Template |
|-----------|----------|
| One line or one hunk in a diff | T1 — Inline review comment |
| A defect the author must fix before merge | T2 — Blocking review finding |
| An optional improvement | T3 — Non-blocking suggestion |
| The summary you leave on the whole pull request | T4 — PR review summary |
| The description the author writes on the pull request | T5 — PR description |
| A reply to review feedback | T6 — Author response |

## Shared word rules for all templates

| Do not write | Write |
|--------------|-------|
| This looks a bit weird / smells off | This function returns `null` when the input list is empty. |
| Can we maybe just not do this? | Remove the call to `resetCache`. |
| It'd be great if you could refactor | Move the retry logic into `RetryPolicy`. |
| The code is broken | The `parseDate` function throws `TypeError` for an empty string. |
| We should probably handle errors | Catch `IOError` in `readConfig` and return a default value. |

Rules applied above: 1.1 (approved words only), 1.9 (short technical nouns),
1.10 (no slang or jargon), 1.11 (one noun per item).

The action line in every template uses the imperative form (Rule 5.3): start the
sentence with a base verb, no "must", no modal verb, no passive voice. The finding
and condition lines may be descriptive statements, but they still use approved words
and one technical noun per item (Rule 1.11).

## T1 — Inline review comment

Shape (three parts, in this order):

```
<observation>: one sentence, one subject, present tense.
<effect>: one sentence that gives the result of the observation.
<action>: one imperative sentence.
```

Example:

> The `getUser` function returns `undefined` when `id` is `0`.
> The caller in `UserController` then reads a property of `undefined`.
> Return `null` for an unknown `id`, and check the result in `UserController`.

Constraints:

- Use the imperative form for the action (Rule 5.3): start with a base verb,
  no "must", no modal ("can", "should", "may"), no passive voice.
- Name the item with the same technical noun each time (Rule 1.11). Do not write
  `getUser`, then "the getter", then "that helper".
- Do not use a technical noun as a verb (Rule 1.7). Write "Send a request to the
  `/users` endpoint", not "Endpoint the request".
- Use backticks for every identifier, path, and type name (Rule 1.5 grammar):
  `UserController`, `id`, `null` stay uninflected.

## T2 — Blocking review finding

```
**Finding:** <one sentence: what is wrong>
**Location:** `<path>:<line>` in `<symbol>`
**Cause:** <one sentence>
**Result:** <one sentence: what fails, and when>
**Required change:** <one imperative sentence>
```

Example:

> **Finding:** The `saveOrder` method does not validate the `quantity` field.
> **Location:** `src/orders/service.ts:142` in `OrderService.saveOrder`
> **Cause:** The method writes the request body to the database with no check.
> **Result:** A negative `quantity` value is written to the `orders` table.
> **Required change:** Reject a request when `quantity` is less than `1`.

Use "required change" for a defect. Write the change as a single imperative
sentence (Rule 5.3). Do not use "must" as an intensifier in the prose — the field
label already gives the obligation. The `Location` line names the item with one
technical noun each time (Rule 1.11); `src/orders/service.ts` and
`OrderService.saveOrder` stay in backticks and are not inflected.

## T3 — Non-blocking suggestion

```
**Suggestion (optional):** <one imperative sentence>
**Reason:** <one sentence>
```

Example:

> **Suggestion (optional):** Move the three retry constants into `RetryPolicy`.
> **Reason:** The same three values occur in `HttpClient` and in `QueueWorker`.

Mark the comment as optional in the first word. Write the suggestion as one
imperative sentence (Rule 5.3). Do not use hedge words such as "maybe", "perhaps",
or "just" to signal that a comment is optional (Rule 1.10).

## T4 — PR review summary

```
**Decision:** Approve | Request changes | Comment
**Scope:** <one sentence: what the pull request changes>
**Blocking findings:** <count>
1. <one sentence each, with `path:line`>
**Optional suggestions:** <count>
1. <one sentence each>
**Verification:** <one sentence: what you ran or read>
```

Example:

> **Decision:** Request changes
> **Scope:** The pull request adds a rate limiter to the `/api/v1/login` route.
> **Blocking findings:** 1
> 1. `src/middleware/rateLimit.ts:58` — The limiter counts a failed request and
>    a successful request in the same bucket.
> **Optional suggestions:** 1
> 1. Give the `WINDOW_MS` constant a unit in its name.
> **Verification:** I ran `npm test` and read the diff in `src/middleware`.

Write the decision as one of the three approved values. Do not invent a fourth
value, and do not write the decision as a sentence. Each finding line is one
sentence that names its item with one technical noun (Rule 1.11); each `path:line`
stays in backticks. The `Verification` line uses the first person only for the
actor ("I ran"), not to soften the obligation.

## T5 — PR description (author)

```
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

Example:

> ## What
> This pull request adds a retry to the `PaymentClient.charge` method.
>
> ## Why
> The payment gateway returns `503` during a deployment. The current client
> fails the order on the first `503` response.
>
> ## How
> 1. Add a `RetryPolicy` class with three attempts and an exponential delay.
> 2. Call `RetryPolicy.execute` from `PaymentClient.charge`.
>
> ## Test
> - Run `npm test -- payment` to check the new unit tests.
> - Send a request to the sandbox gateway to check the delay values.
>
> ## Risk
> A retry can create a duplicate charge if the gateway accepted the first
> request. The client sends an idempotency key to prevent this result.

The `How` steps are all imperative (Rule 5.3). The `What` and `Why` sections are
descriptive statements, but each sentence still uses one technical noun per item
(Rule 1.11) and approved words only (Rule 1.1).

## T6 — Author response to feedback

```
**Comment:** <link or `path:line`>
**Response:** Done | Changed | Not changed
**Detail:** <one sentence>
```

Example:

> **Comment:** `src/middleware/rateLimit.ts:58`
> **Response:** Changed
> **Detail:** The limiter now counts only a failed request in the login bucket.

Use one of the three approved response values. Do not use "LGTM", "nit", "wontfix",
or other jargon labels (Rule 1.10). The `Comment` line gives the item in backticks
with one name each time (Rule 1.11).

## Approved verbs for review and PR text

Use these code-domain technical verbs in the action line of any template. Use
the base form for an instruction (Rule 5.3), and the third-person form for a
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

Do not use a verb from this table as a noun (Rule 1.13). Write "The function
returns a value", not "The return of the function".

## Forbidden words in review and PR text

| Forbidden | Reason | Use instead |
|-----------|--------|-------------|
| nit, LGTM, WIP, PTAL, IMO | jargon (Rule 1.10) | the full template label |
| smelly, hacky, ugly, clean | subjective, not approved (Rule 1.1) | the concrete defect |
| stuff, thing, some code | not a technical noun (Rule 1.5) | the identifier in backticks |
| leverage, utilize | not approved (Rule 1.3) | use |
| behaviour, initialise, colour | British spelling (Rule 1.14) | behavior, initialize, color |
| we should maybe possibly | hedging (Rule 1.1) | one imperative sentence |

## Section-specific grammar rules for review and PR text

Level 2 adds the grammar that governs how a review or PR sentence is built. The
two rules below come from the STE-Code procedural-grammar set (Rules 5.3 and 5.4),
reshaped for review and PR text.

### Grammar rule G1 — Imperative form in the action line (Rule 5.3)

Every action line (T1 `action`, T2 `Required change`, T3 `Suggestion`, T5 `How`)
starts with a base verb and gives a direct instruction. Drop the subject "you"
(the reader is implied), and do not use passive voice, gerunds, or modal verbs.

- Do not add "must" before the imperative in a standard instruction. Reserve
  "must" for a security or data-loss warning (for example a finding where a
  leaked key can cause permanent loss).
- Do not soften the instruction with "can", "could", "should", "may", or
  "might". "Set the timeout to 30 seconds" leaves no room for "optional".

> **Non-STE:** The test suite can be executed with `npm test`.
> **STE:** Run the unit tests with `npm test`.

> **Non-STE:** Before you delete the branch, you must push all local commits.
> **STE:** Before you delete the branch, push all local commits to the remote.

### Grammar rule G2 — Descriptive statement before the command (Rule 5.4)

When a finding or condition must be known first, write it as a descriptive
statement, then a comma, then the imperative. The comma is required: it shows
where the condition ends and the command begins. Moving the comma changes which
verb an adverb modifies.

> **STE:** If the connection pool is full, reject the request.
> (The comma after "full" shows "automatically" would modify "reject".)
> **STE:** If the connection pool is full automatically, reject the request.
> (The comma after "automatically" changes the meaning — the pool fills on its
> own; reject it.)

Apply G2 inside T2 (`Result` then `Required change`) and T4 (`Scope` sets the
condition, findings follow). Keep conditions short — one condition per sentence.

### Grammar rule G3 — Technical-noun grammar inside review text (Rule 1.5)

Identifiers, paths, type names, and commands in review text are code-domain
technical nouns. Apply the following grammar:

- **Backticks, no inflection.** Write `getUser`, `null`, `OrderService`. Do not
  write "the `getUser`s" or "two `null`s". Use a lowercase "s" for acronym plurals
  without an apostrophe: `APIs`, not `API's`.
- **One name per item (Rule 1.11).** Name the same symbol the same way every time
  in one comment thread: `getUser`, not "the getter", then "that helper".
- **Articles.** Use "the" for a specific instance, "a"/"an" for an indefinite one,
  no article for a plural general reference: "The `UserController` handles a
  request. Kubernetes pods run in a namespace."
- **Possessive only for roles/orgs (category 11).** Write "the user's session
  data" but "the configuration of the `Docker` container", not "the `Docker`
  container's configuration".
- **Capitalization.** Proper nouns keep their capitalization (`TypeScript`,
  `PostgreSQL`); common technical nouns are lowercase unless first word
  (`controller`, `endpoint`, `middleware`).
- **Quoted keywords and status codes.** Code keywords (`if`, `return`, `class`)
  and status codes (`404 Not Found`, `500`) are quoted text (category 10). Write
  "Return `500 Internal Server Error`", not a bare "500".

## Checklist before you post

1. Each sentence has one subject.
2. Each item has one name, used every time (Rule 1.11).
3. Each identifier is in backticks and is not inflected.
4. Each action is one imperative sentence (Rule 5.3).
5. Each condition comes before its command, separated by a comma (Rule 5.4).
6. No word from the forbidden table is present.
7. Spelling is American English (Rule 1.14).

