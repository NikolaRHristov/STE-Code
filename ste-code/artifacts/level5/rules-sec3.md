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

---

## Rule 3.4 — Do not use auxiliary verbs to make complex verb constructions

Source: ASD-STE100 Issue 9, Rule 3.4 (master.md#sec3-rule3.4).

Do not combine an auxiliary verb ("have", "be", "will", "can", "must", "should",
"is to be") with a past participle to build a compound tense or the passive
voice. These constructions make verb forms that STE-Code does not approve.

Conversion table:

| Construction | Replace with |
|---|---|
| have/has/had + past participle (perfect) | the simple past |
| be + past participle (passive) | the active voice with a named agent (Rule 3.6) |
| is to be + past participle | the imperative (command) form |
| can be + past participle | "you can" + base verb, when the reader is the agent |
| will be + past participle + by + agent | agent + "will" + base verb |

When a compound construction seems unavoidable, split it into separate simple
sentences. Rule 3.2 lists the only approved forms: infinitive, imperative,
simple present, simple past, simple future, and past participle as an adjective.

Examples:

| Non-STE | STE | Fix applied |
|---|---|---|
| The build has compiled the module before the test runs. | The build compiled the module. Then the test runs. | present perfect -> simple past |
| The migration is to be run before you deploy the service. | Before you deploy the service, run the migration. | "is to be" -> imperative |
| The cache can be cleared. | You can clear the cache. | "can be" -> "you can" + base verb |
| The timeout must be set before the job starts. | Set the timeout before the job starts. | "must be" -> imperative |
| The report will be generated by the scheduler. | The scheduler will generate the report. | agent to subject, keep "will" |
| The connection pool has been created before the first query is sent. | The connection pool was created. Then the first query is sent. | present perfect passive -> simple past |
| The configuration file must be validated before the server starts. | Validate the configuration file before the server starts. | imperative for a procedure |
| The user credentials are to be encrypted at rest and the key is rotated monthly. | Encrypt the user credentials at rest. Rotate the key every month. | two imperatives |
| The log entries can be exported to a CSV file by the admin. | The admin can export the log entries to a CSV file. | name the agent, keep the modal |
| An error message will be shown by the validator if the input is empty. | The validator will show an error message if the input is empty. | agent to subject |
| The temporary files had been deleted by the cleanup task before the backup started. | The cleanup task deleted the temporary files. Then the backup started. | past perfect passive -> simple past, sequence with "Then" |

See also: Rules 3.2, 3.3, 3.5, 3.6.

---

## Rule 3.5 — Use the "-ing" form only as a technical noun or as a modifier in a technical noun

Source: ASD-STE100 Issue 9, Rule 3.5 (master.md#sec3-rule3.5).

An "-ing" word can be a verb part, an adjective, a noun, or the head of a long
modifier group. That range causes ambiguity and long sentences. In STE-Code the
"-ing" form is not permitted as a verb.

Approved "-ing" words in STE-Code:

| Part of speech | Words |
|---|---|
| Nouns | logging, monitoring, routing, servicing |
| Adjectives | matching, missing, remaining |
| Pronoun | something |
| Preposition | during |

Why the progressive is not approved: Rule 3.2 permits only the infinitive, the
imperative, the simple present, the simple past, the simple future, and the past
participle as an adjective. The progressive ("is running", "are deploying", "was
processing") is not on that list, and the "-ing" form lives inside it. The
"-ing" form also hides auxiliary-verb constructions that Rule 3.4 forbids: write
"The service starts. Then it logs the request", not "the service is starting and
then it is logging the request".

Approved "-ing" technical nouns (section and document titles):

- Logging
- Monitoring
- Testing and Fault Isolation
- Handling
- Packaging
- Shipping
- Troubleshooting
- Building
- Deployment

Approved "-ing" modifiers inside technical nouns:

- logging service
- monitoring agent
- routing table
- switching relay
- caching layer
- building pipeline
- binding configuration
- streaming endpoint
- rendering engine

Do not pull the "-ing" word out of the technical noun and use it as a verb. "The
caching layer stores the result" is approved. "The layer is caching the result"
is not.

Examples:

| Non-STE | STE | Fix applied |
|---|---|---|
| When you are running this script, obey all the safety checks. | When you run this script, obey all the safety checks. | progressive -> simple present |
| Be careful while the process is starting. | Be careful while the process starts. | progressive -> simple present |
| While the deployment is starting, you must watch the logs and you must not stop the process because stopping it during startup can corrupt the state file. | The deployment starts. While it starts, watch the logs. Do not stop the deployment. If you stop the deployment during startup, the state file can become corrupt. | progressive and gerund clause -> short sentences |
| The background worker is processing the queue and it is writing the results to the cache while the main thread is waiting for the response, causing the request to time out and the user to see an error. | The background worker processes the queue. It writes the results to the cache. The main thread waits for the response. If the main thread waits too long, the request times out and the user sees an error. | three progressives and a cause clause split apart |
| The function is returning the value while the cache is loading the entry, which makes the result incorrect during the first request. | The function returns the value. The cache loads the entry. During the first request, the result is incorrect. | progressive -> simple present |
| The matching algorithm is comparing the remaining items during the iteration and it is removing the missing records from the list. | The matching algorithm compares the remaining items during the iteration. It removes the missing records from the list. | approved adjectives kept; progressive verbs removed |
| Something going wrong during the migration can make the database stay in a broken state. | If something goes wrong during the migration, the database can stay in a broken state. | "something" kept; gerund verb -> simple present |

Long "-ing" subjects become vertical lists:

> **Non-STE:** A script opening a socket without checking the firewall rules and
> sending data to an unknown host, using an unverified certificate without
> reading the security policy, is in danger of causing a breach and thus
> exposing private keys and credentials.
>
> **STE:** Before you open a socket, obey these precautions: (1) Read the
> security policy. (2) Make sure that the firewall rules allow the connection.
> (3) Verify the host certificate. (4) Get the correct credentials to send data
> to the host. If you do not obey these precautions, a breach of private keys
> and credentials can occur.

> **Non-STE:** Developers committing code without running the test suite and
> pushing directly to the main branch, ignoring the review policy, risk breaking
> the build and therefore blocking the release for all team members.
>
> **STE:** Before you commit code, obey these precautions: (1) Run the test
> suite. (2) Make sure that the tests pass. (3) Open a review before you merge to
> the main branch. If you do not obey these precautions, you can break the build
> and block the release for all team members.

See also: Rules 3.2, 3.4, 1.5.
