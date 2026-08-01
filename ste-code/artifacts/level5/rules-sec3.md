# Level 5 — Section 3: Verbs

Scope: Rules 3.1 to 3.7 of STE-Code. These rules control which verbs you use,
which forms of those verbs are legal, and how you build a sentence around them.
Source: ASD-STE100 Issue 9, Part 1, Section 3, adapted to the code domain.

Section contract, in one block:

```
Approved verbs      -> only the verbs in the STE-Code dictionary
Approved forms      -> base, third-person singular, simple past, past participle
Approved tenses     -> infinitive, imperative, simple present, simple past,
                       simple future ("will" + base)
Past participle     -> adjective only
Forbidden           -> perfect, progressive, perfect progressive, passive with
                       auxiliaries, gerund used as a verb
Voice               -> active; passive only when the agent is unknown
Action words        -> verbs, not nominalizations
```

Rule index:

| Rule | Statement |
|---|---|
| 3.1 | Use only the verb forms that the dictionary gives. |
| 3.2 | Use only these verb forms and tenses of verbs. |
| 3.3 | Use the past participle form as an adjective. |
| 3.4 | Do not use auxiliary verbs to make complex verb constructions. |
| 3.5 | Use the "-ing" form only as a technical noun or as a modifier in one. |
| 3.6 | Use the active voice. |
| 3.7 | Use an approved verb to describe an action, not a noun. |

The four approved verb categories (all rules in this section draw from them):

| Category | Verbs |
|---|---|
| Development operations | build, compile, test, lint, format, commit, push, deploy, rollback |
| Data operations | read, write, serialize, deserialize, parse, encode, decode, query, insert, migrate |
| Application operations | handle, route, authenticate, authorize, validate, schedule, dispatch, resolve |
| Communication operations | send, receive, publish, subscribe, stream, poll, broadcast, connect |

---

## Rule 3.1 — Use only the verb forms that the dictionary gives

Source: ASD-STE100 Issue 9, Rule 3.1 (master.md#sec3-rule3.1).

Every approved verb appears in the STE-Code dictionary with exactly four forms,
in this order. If a form is not on one of those four lines, the form is not
approved.

```
VALIDATE (v)        WRITE (v)
VALIDATES           WRITES
VALIDATED,          WROTE,
VALIDATED           WRITTEN
```

How to read an entry:

| Line | Form | WRITE | Where you use it |
|---|---|---|---|
| 1 | Base form (infinitive and imperative) | WRITE | "Write the log." / "to write the log" |
| 2 | Third-person singular, simple present | WRITES | "The logger writes the record." |
| 3 | Simple past | WROTE | "The job wrote the record." |
| 4 | Past participle (as an adjective) | WRITTEN | "the written log" |

The simple future has no line of its own. You make it with "will" plus the base
form: "will write".

Procedure:

1. Find the verb in the STE-Code dictionary.
2. If the verb is not there, do not use it. Use the approved verb instead:
   make (not generate), get (not retrieve), check (not verify), use (not
   utilize), start (not initiate), stop (not terminate), remove (not delete),
   show (not render), do (not execute), keep (not maintain).
3. If the verb is there, use one of the four listed forms only.
4. Do not derive a new form. "Parsing", "parseable", and "parser" are not verb
   forms of PARSE. A noun such as "parser" is approved only when the dictionary
   or a technical noun category gives it.
5. Use the past participle only as an adjective ("the parsed manifest"). Do not
   pair it with "have", "has", "had", or "get" to make a verb.

Examples:

| Non-STE | STE | Why |
|---|---|---|
| The linter validates the file and is reporting the errors to the terminal. | The linter validates the file. It reports the errors to the terminal. | "is reporting" is not a listed form of REPORT. |
| The script has written the output to the log before the test starts. | The script wrote the output to the log. Then the test starts. | Present perfect is not a listed form. |
| The service utilizes a token cache and leverages the parser for each request. | The service uses a token cache. The service parses each request. | "utilize" and "leverage" are not in the dictionary. |
| The parsing of the manifest is done by the loader, and the validating of the schema comes after. | The loader parses the manifest. Then the loader validates the schema. | Gerunds are not listed forms. Name the actor. |
| The migration had deleted the deprecated column and was terminating the open connections. | The migration removed the deprecated column. Then the migration stopped the open connections. | "delete" and "terminate" are unapproved; past perfect and progressive are unapproved. |
| The client will be receiving the streamed records after the broker has been publishing them for one minute. | The broker publishes the records. The client will receive the streamed records after one minute. | Future progressive and perfect progressive are unapproved. "Streamed" is a participle adjective, so it stays. |
| The given options get validated by the gateway, and the removed entries are gotten from the cache. | The gateway validates the given options. The gateway gets the removed entries from the cache. | "get validated" and "are gotten" are unapproved. "Given" and "removed" are participle adjectives. |

```python
# STE: the loader parses the manifest. Then the loader validates the schema.
manifest = loader.parse(path)      # parse -> parses / parsed / parsed
loader.validate(manifest, schema)  # validate -> validates / validated / validated
```

Note (structural carryover): the four-line dictionary layout is a structural
feature of the source standard. The code-domain version keeps the layout with
code verbs. No mapping is forced.

See also: Rules 3.2, 3.3, 3.4, 1.1, 1.5, and the STE-Code dictionary.

---

## Rule 3.2 — Use only these verb forms and tenses of verbs

Source: ASD-STE100 Issue 9, Rule 3.2 (master.md#sec3-rule3.2).

Approved forms and tenses, and nothing else:

- The infinitive form
- The imperative form (command form)
- The simple present tense
- The simple past tense
- The simple future tense
- The past participle form (as an adjective)

| Infinitive | Imperative | Simple present | Simple past | Simple future | Past participle (adj) |
|---|---|---|---|---|---|
| (to) parse (regular) | Parse + object | you/we/they parse; it parses | you/we/they parsed; it parsed | will parse | the parsed file |
| (to) write (irregular) | Write + object | you/we/they write; it writes | you/we/they wrote; it wrote | will write | the written log |
| (to) build (irregular) | Build + object | you/we/they build; it builds | you/we/they built; it built | will build | the built artifact |
| (to) send (irregular) | Send + object | you/we/they send; it sends | you/we/they sent; it sent | will send | the sent request |
| (to) validate (regular) | Validate + object | you/we/they validate; it validates | you/we/they validated; it validated | will validate | the validated token |

Not approved:

- Present perfect (have/has parsed)
- Past perfect (had parsed)
- Present/past progressive (is/was parsing)
- Future progressive (will be parsing)
- Perfect progressive (has been parsing, had been parsing)
- The gerund used as a verb with an auxiliary (is parsing, keeps parsing)
- All other complex verb constructions

How to select the correct form:

1. Infinitive — after a modal verb or to state a purpose: "Use this flag to parse the file."
2. Imperative — for each step of a procedure: "Parse the file. Write the log."
3. Simple present — a general fact, a repeated action, or system behavior: "The parser reads the file."
4. Simple past — a complete action: "The build failed."
5. Simple future — "will" plus the base form: "The job will start at 02:00."
6. Past participle — as an adjective before a noun only: "the parsed file".

How to correct an unapproved form:

| Unapproved | Fix |
|---|---|
| has parsed (present perfect) | simple past: parsed |
| had parsed (past perfect) | two sentences in the simple past, joined by "Then" |
| is/was parsing (progressive) | simple present or simple past; if two actions overlap, write two sentences and add "at the same time" |
| will be parsing (future progressive) | simple future: will parse |
| is being parsed (passive with auxiliary) | name the actor, use the active voice (Rule 3.6) |

Examples:

| Non-STE | STE | Fix applied |
|---|---|---|
| The linter has found three errors in the source file. | The linter found three errors in the source file. | present perfect -> simple past |
| The server was processing the request when the timeout occurred. | The server processed the request. Then the timeout occurred. | past progressive -> two sentences |
| The framework had already initialized the connection pool before the query started. | The framework made the connection pool. Then the query started. | past perfect -> simple past; "make" replaces "initialize" |
| The scheduler is deploying the build to production while the tests are running. | The scheduler sends the build to production. The tests run at the same time. | progressive -> simple present, twice |
| The cache has been keeping the serialized records since the service started, and the client will be reading them after the restart. | The cache keeps the serialized records. The client will read the records after the restart. | perfect progressive and future progressive removed |
| To be parsing the configuration file, the loader must be having read access to the directory. | To parse the configuration file, the loader must have read access to the directory. | infinitive and base form after the modal |
| You should be setting the timeout value and then you will be restarting the service. | Set the timeout value. Then start the service again. | imperative for each step |
| The payload is being validated by the gateway and the deprecated field gets removed by the migration. | The gateway validates the payload. The migration removes the deprecated field. | passive progressive -> active simple present |
| The written log and the parsed manifest are showing that the build had completed with the given options. | The written log and the parsed manifest show that the build completed with the given options. | participle adjectives kept; progressive and past perfect removed |
| We have been building the release artifact and the CI pipeline will have run the tests by the time you review the pull request. | We built the release artifact. The CI pipeline will run the tests. Then you can review the pull request. | perfect progressive and future perfect removed |
| If the connection drops, the client is retrying the request until the server responds. | If the connection drops, the client retries the request. Then the server responds. | progressive -> simple present |

```yaml
# .github/workflows/ci.yml
# STE: we built the release artifact. The CI pipeline will run the tests.
jobs:
  build:
    steps:
      - run: make release
  test:
    needs: build
    steps:
      - run: make test
```

```python
# STE: the server processed the request. Then the timeout occurred.
try:
    response = server.process(request)   # process -> processes / processed / processed
except TimeoutError:
    log.write("request timeout after 30 s")
```

Note (structural carryover): the six-column table of verb forms is a structural
feature of the source standard, kept here with approved code verbs.

See also: Rules 3.1, 3.3, 3.4, 3.5, 3.6, 1.1, and the STE-Code dictionary.

---

## Rule 3.3 — Use the past participle form as an adjective

Source: ASD-STE100 Issue 9, Rule 3.3 (master.md#sec3-rule3.3).

A past participle used as an adjective shows the condition of something. This is
not passive voice. Use it:

- Before a noun
- After a form of "to be", "to become", or "to stay"

Do not use a past participle that the STE-Code dictionary does not give. Some
approved adjectives are past participles of verbs that are themselves not
approved; the dictionary marks them "(adj)" and you may use them.

How to tell adjective from passive voice:

1. The word gives the condition of the thing, not an action that an actor does.
2. You can put it directly before the noun: "the parsed file", "the deprecated method", "the closed connection".
3. You can put it after "is", "becomes", or "stays": "the cache is initialized", "the endpoint becomes deprecated", "the record stays locked".
4. If the sentence names an actor and an action ("the file was parsed by the loader"), it is passive voice. Write the active voice instead (Rule 3.6).

Approved code-domain participle adjectives:

| Past participle (adj) | Example noun phrase | Condition that it shows |
|---|---|---|
| parsed | the parsed manifest | The parser read the file. |
| serialized | the serialized record | The record is in a transport format. |
| deserialized | the deserialized object | The object is in memory again. |
| initialized | the initialized cache | The cache is ready for use. |
| deprecated | the deprecated method | The method is old. Do not use it. |
| allowed | the allowed memory | The limit that the configuration gives. |
| corrupted | the corrupted index | The data is not correct. |
| locked | the locked row | Another transaction holds the row. |
| written | the written log | The log file is on disk. |
| given | the given options | The options that the caller sends. |
| built | the built artifact | The build made the artifact. |
| signed | the signed token | The token has a valid signature. |

Cautions:

- Do not make a new past participle from an unapproved verb. Write "the removed branch", not "the deleted branch", unless the dictionary gives "delete" or "deleted (adj)".
- Do not use a past participle as a verb with "have", "has", or "had" (Rule 3.2).
- Do not stack more than one past participle before the same noun. If "the parsed and validated payload" becomes difficult, write two short sentences.
- Prefer the plain word: "started" not "commenced", "used" not "utilized" or "leveraged", "stopped" not "terminated".

Correct uses:

- "Inspect all fields of the deserialized object for corruption." ("deserialized" before a noun)
- "When the cache is fully initialized, start the worker threads." ("initialized" after "to be")
- "Do not exceed the allowed memory for the buffer." ("allowed" is an approved adjective)
- "Make sure that the input values are not corrupted." ("corrupted" is an approved adjective)

Corrections:

| Non-STE | STE |
|---|---|
| The parsed file was processed by the loader. | The parsed file is ready for the loader. |
| The method has been deprecated by the API team in release 4.2. | The method is deprecated in release 4.2. Do not use the deprecated method in new code. |
| After the record gets locked, the transaction which was started earlier is being committed. | The transaction writes the locked record. Then the transaction ends. |
| The signed token which had been given to the client is validated by the gateway on each request. | The gateway validates the signed token on each request. |
| When the index becomes corrupted it will have to be being rebuilt by the maintenance job. | When the index becomes corrupted, the maintenance job makes the index again. |
| The build artifact stays uncompiled until the pipeline has compiled the modified sources. | The artifact stays unbuilt until the pipeline builds the modified sources. |
| The user is shown a warning if the uploaded configuration file was found to be malformed. | The CLI shows a warning if the uploaded configuration file is malformed. |
| All of the returned records had already been serialized before the response was sent. | The API sends the serialized records in the response. |
| Make sure that the written log and the given options are not being modified by the plugin. | Make sure that the plugin does not change the written log or the given options. |

```go
// STE: "initialized" comes after "is" and gives the condition of the cache.
if cache.IsInitialized() {
    pool.Start(workerCount)
}
```

```sql
-- STE: the transaction writes the locked record. Then the transaction ends.
BEGIN;
SELECT * FROM orders WHERE id = 42 FOR UPDATE;  -- the locked row
UPDATE orders SET status = 'sent' WHERE id = 42;
COMMIT;
```

Note (structural carryover): the source rule uses hardware conditions to show the
grammar. The code-domain version keeps the grammar and gives software conditions.

See also: Rules 3.1, 3.2, 3.4, 3.5, 3.6, 1.1, and the dictionary adjectives "(adj)".
