# Level 3 — Section 3: Verbs

Scope: STE-Code Section 3, Rules 3.1 through 3.7. These rules control which verb
forms you can use, which tenses are approved, how to use the past participle,
how to avoid auxiliary constructions and "-ing" verbs, when to use the active
voice, and when to use a verb instead of a noun.

Audience: an LLM that writes or edits code documentation (README files, API
reference, docstrings, code comments, commit messages, error messages, CLI help,
configuration comments).

## Section 3 at a glance

| Rule | Statement | Primary test |
|---|---|---|
| 3.1 | Use only the verb forms that the dictionary gives. | Is the form one of the four listed lines of the entry? |
| 3.2 | Use only the approved verb forms and tenses. | Is the tense infinitive, imperative, simple present, simple past, simple future, or past participle as an adjective? |
| 3.3 | Use the past participle form as an adjective. | Does the word give a condition, before a noun or after be/become/stay? |
| 3.4 | Do not use auxiliary verbs to make complex verb constructions. | Does the sentence stack have/be/will/can/must + past participle? |
| 3.5 | Use the "-ing" form only as a technical noun or as a modifier in a technical noun. | Is the "-ing" word acting as a verb? Then it is not approved. |
| 3.6 | Use the active voice. | Ask "by whom or by what?" If the sentence answers it, the sentence is passive. |
| 3.7 | Use an approved verb to describe an action, not a noun. | Is the action hidden in a noun phrase such as "gives an indication of"? |

## Quick decision procedure

1. Find the verb in the STE-Code dictionary. If the verb is not there, replace it
   with the approved verb (Rule 3.1, Rule 3.7).
2. Choose one of the six approved forms (Rule 3.2).
3. Name the actor and put the actor in the subject position (Rule 3.6).
4. Remove every auxiliary chain (Rule 3.4).
5. Remove every "-ing" verb. Keep "-ing" only inside a technical noun (Rule 3.5).
6. Keep the past participle only as an adjective (Rule 3.3).
7. If a sentence becomes long, split it into two short sentences and join the
   sequence with "Then".

---

## Rule 3.1 — Use only the verb forms that the dictionary gives

The STE-Code dictionary gives the allowed forms of each approved verb. Use only
those forms. Do not use gerunds, participles with auxiliaries, or inflected forms
that the entry does not list.

Each entry shows four forms in this order: base form, third-person singular,
simple past, past participle.

```
VALIDATE (v)
VALIDATES
VALIDATED,
VALIDATED

WRITE (v)
WRITES
WROTE,
WRITTEN
```

### How to read a dictionary entry

| Line | Form | Example with WRITE | Where you use it |
|---|---|---|---|
| 1 | Base form (infinitive and imperative) | WRITE | "Write the log." / "to write the log" |
| 2 | Third-person singular, simple present | WRITES | "The logger writes the record." |
| 3 | Simple past | WROTE | "The job wrote the record." |
| 4 | Past participle (as an adjective) | WRITTEN | "the written log" |

If a form is not on one of those four lines, the form is not approved. The simple
future is not a separate line: you make it with "will" and the base form
("will write").

### The four approved verb categories

| Category | Verbs |
|---|---|
| Development operations | build, compile, test, lint, format, commit, push, deploy, rollback |
| Data operations | read, write, serialize, deserialize, parse, encode, decode, query, insert, migrate |
| Application operations | handle, route, authenticate, authorize, validate, schedule, dispatch, resolve |
| Communication operations | send, receive, publish, subscribe, stream, poll, broadcast, connect |

### How to apply the rule

1. Find the verb in the STE-Code dictionary.
2. If the verb is not in the dictionary, use the approved verb instead.
3. If the verb is in the dictionary, use one of the four listed forms only.
4. Do not make a new form from an approved verb. "Parsing", "parseable", and
   "parser" are not verb forms of PARSE. A noun such as "parser" is approved only
   when the dictionary or a technical noun category gives it.
5. Use the past participle only as an adjective ("the parsed manifest", "the
   deprecated method"). Do not use it with "have", "has", "had", or "get".

### Frequent replacements

| Do not use | Use |
|---|---|
| generate | make |
| retrieve | get |
| verify | check |
| utilize, leverage | use |
| initiate | start |
| terminate | stop |
| delete | remove |
| render | show |
| execute | do |
| maintain | keep |

### Examples

| Non-STE | STE | Why |
|---|---|---|
| The linter validates the file and is reporting the errors to the terminal. | The linter validates the file. It reports the errors to the terminal. | "is reporting" is not a listed form of REPORT. |
| The script has written the output to the log before the test starts. | The script wrote the output to the log. Then the test starts. | The present perfect "has written" is not a listed form. |
| The service utilizes a token cache and leverages the parser for each request. | The service uses a token cache. The service parses each request. | "utilize" and "leverage" are not in the dictionary. |
| The parsing of the manifest is done by the loader, and the validating of the schema comes after. | The loader parses the manifest. Then the loader validates the schema. | Gerunds are not listed forms. Name the actor. |
| The migration had deleted the deprecated column and was terminating the open connections. | The migration removed the deprecated column. Then the migration stopped the open connections. | Use REMOVE and STOP. The past perfect and the progressive are not listed. |
| The client will be receiving the streamed records after the broker has been publishing them for one minute. | The broker publishes the records. The client will receive the streamed records after one minute. | Make the simple future with "will" and the base form. "streamed" is a participle used as an adjective. |
| The given options get validated by the gateway, and the removed entries are gotten from the cache. | The gateway validates the given options. The gateway gets the removed entries from the cache. | "get validated" and "are gotten" are not listed forms. |

Code context:

```python
# STE: the loader parses the manifest. Then the loader validates the schema.
manifest = loader.parse(path)      # parse -> parses / parsed / parsed
loader.validate(manifest, schema)  # validate -> validates / validated / validated
```

```javascript
// STE: the service uses a token cache. The service parses each request.
const cache = new TokenCache();          // use -> uses / used / used
app.post("/orders", (req, res) => {
  const order = parseOrder(req.body);    // parse -> parses / parsed / parsed
  res.json(order);
});
```

```go
// STE: the broker publishes the records.
// The client will receive the streamed records after one minute.
func (b *Broker) Publish(rec []byte) error { // publish -> publishes / published / published
    return b.topic.Send(rec)                 // send -> sends / sent / sent
}
```

See also: Rule 3.2, Rule 3.3, Rule 3.4, Rule 1.1, Rule 1.5, and the STE-Code
dictionary (the full list of approved verbs and their allowed forms).

---

## Rule 3.2 — Use only these verb forms and tenses of verbs

Approved forms and tenses:

- The infinitive form
- The imperative form (command form)
- The simple present tense
- The simple past tense
- The simple future tense
- The past participle form (as an adjective)

| Infinitive | Imperative | Simple present | Simple past | Simple future | Past participle (adj) |
|---|---|---|---|---|---|
| (To) parse (regular) | Parse + object | you/we/they parse; it parses | you/we/they parsed; it parsed | will parse | the parsed file |
| (To) write (irregular) | Write + object | you/we/they write; it writes | you/we/they wrote; it wrote | will write | the written log |
| (To) build (irregular) | Build + object | you/we/they build; it builds | you/we/they built; it built | will build | the built artifact |
| (To) send (irregular) | Send + object | you/we/they send; it sends | you/we/they sent; it sent | will send | the sent request |
| (To) validate (regular) | Validate + object | you/we/they validate; it validates | you/we/they validated; it validated | will validate | the validated token |

Not approved:

- The present perfect (have/has parsed)
- The past perfect (had parsed)
- The present or past progressive (is/was parsing)
- The future progressive (will be parsing)
- The perfect progressive (has been parsing, had been parsing)
- The gerund used as a verb with an auxiliary (is parsing, keeps parsing)
- All other complex verb constructions

### How to select the correct form

1. Infinitive — after a modal verb or to state a purpose: "Use this flag to parse the file."
2. Imperative — for each step of a procedure: "Parse the file. Write the log."
3. Simple present — for a general fact, a repeated action, or system behavior: "The parser reads the file."
4. Simple past — for an action that is complete: "The build failed."
5. Simple future — "will" plus the base form: "The job will start at 02:00."
6. Past participle — only as an adjective before a noun: "the parsed file".

### How to correct an unapproved form

| Unapproved | Correction |
|---|---|
| has parsed (present perfect) | parsed (simple past) |
| had parsed (past perfect) | simple past in two sentences joined with "Then" |
| is parsing, was parsing (progressive) | simple present or simple past; add "at the same time" for concurrent actions |
| will be parsing (future progressive) | will parse (simple future) |
| is being parsed (passive progressive) | name the actor and use the active voice (Rule 3.6) |

### Examples

| Non-STE | STE |
|---|---|
| The linter has found three errors in the source file. | The linter found three errors in the source file. |
| The server was processing the request when the timeout occurred. | The server processed the request. Then the timeout occurred. |
| The framework had already initialized the connection pool before the query started. | The framework made the connection pool. Then the query started. |
| The scheduler is deploying the build to production while the tests are running. | The scheduler sends the build to production. The tests run at the same time. |
| The cache has been keeping the serialized records since the service started, and the client will be reading them after the restart. | The cache keeps the serialized records. The client will read the records after the restart. |
| To be parsing the configuration file, the loader must be having read access to the directory. | To parse the configuration file, the loader must have read access to the directory. |
| You should be setting the timeout value and then you will be restarting the service. | Set the timeout value. Then start the service again. |
| The payload is being validated by the gateway and the deprecated field gets removed by the migration. | The gateway validates the payload. The migration removes the deprecated field. |
| The written log and the parsed manifest are showing that the build had completed with the given options. | The written log and the parsed manifest show that the build completed with the given options. |
| We have been building the release artifact and the CI pipeline will have run the tests by the time you review the pull request. | We built the release artifact. The CI pipeline will run the tests. Then you can review the pull request. |
| If the connection drops, the client is retrying the request until the server responds. | If the connection drops, the client retries the request. Then the server responds. |

Code context:

```bash
# STE: one imperative step for each line
# Set the timeout value.
export REQUEST_TIMEOUT=30
# Then start the service again.
systemctl restart api.service
```

```python
# STE: the server processed the request. Then the timeout occurred.
try:
    response = server.process(request)   # process -> processes / processed / processed
except TimeoutError:
    log.write("request timeout after 30 s")
```

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

See also: Rule 3.1, Rule 3.3, Rule 3.4, Rule 3.5, Rule 3.6, Rule 1.1.

---

## Rule 3.3 — Use the past participle form as an adjective

When you use the past participle form as an adjective, it shows the condition of
something. This is not passive voice. Use the past participle of an approved verb
as an adjective:

- Before a noun
- After a form of "to be", "to become", or "to stay"

Do not use the past participle form if it is not in the STE-Code dictionary. Some
approved adjectives in the dictionary are past participles of verbs that are not
approved; their part of speech is "(adj)", so you can use them.

### How to know that the participle is an adjective and not passive voice

1. The word gives the condition of the thing, not an action that an actor does.
2. You can put the word directly before the noun: "the parsed file", "the deprecated method", "the closed connection".
3. You can put the word after "is", "becomes", or "stays": "the cache is initialized", "the endpoint becomes deprecated", "the record stays locked".
4. If the sentence names an actor and an action ("the file was parsed by the loader"), the sentence is passive voice. Write the active voice instead (Rule 3.6).

### Approved code-domain past participles used as adjectives

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

### Cautions

- Do not make a new past participle from an unapproved verb. Write "the removed branch", not "the deleted branch", when "delete" is not in the dictionary.
- Do not use a past participle as a verb with "have", "has", or "had" (Rule 3.2).
- Do not put more than one past participle before the same noun. Split a difficult phrase into two short sentences.
- Prefer the plain word: "started" not "commenced"; "used" not "utilized" or "leveraged"; "stopped" not "terminated".

### Correct use (adjective)

| STE | Why it is correct |
|---|---|
| Inspect all fields of the deserialized object for corruption. | "deserialized" is an adjective before the noun "object". |
| When the cache is fully initialized, start the worker threads. | "initialized" comes after "to be" and gives a condition. |
| Do not exceed the allowed memory for the buffer. | "allowed" is an approved adjective. |
| Make sure that the input values are not corrupted. | "corrupted" is an approved adjective. |

### Correction pairs

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

Code context:

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

```javascript
// STE: the gateway validates the signed token on each request.
app.use((req, res, next) => {
  const signedToken = req.headers.authorization; // the signed token
  if (!gateway.validate(signedToken)) {
    return res.status(401).send("the signed token is not valid");
  }
  next();
});
```

See also: Rule 3.1, Rule 3.2, Rule 3.4, Rule 3.5, Rule 3.6, Rule 1.1.

---

## Rule 3.4 — Do not use auxiliary verbs to make complex verb constructions

Do not use the past participle form as a verb together with the auxiliary verb
"have". That construction makes a tense that is not approved.

Do not use auxiliary verbs ("have", "be", "will", "can", "must", "should",
"is to be") with a past participle to build compound tenses or the passive voice.
Write the action with a simple, approved verb form instead:

- Use the simple past instead of "have/has/had + past participle".
- Use the active voice with a clear agent instead of "be + past participle" (Rule 3.6).
- Use the imperative form for instructions instead of "is to be + past participle".
- Use "you can + base verb" instead of "can be + past participle" when the reader is the agent.
- Use "will + base verb" with a named agent instead of "will be + past participle + by + agent".

When a compound construction seems unavoidable, split it into separate simple
sentences. Rule 3.2 lists the only approved forms.

### Conversion table

| Construction | Non-STE | STE |
|---|---|---|
| Present perfect | The build has compiled the module before the test runs. | The build compiled the module. Then the test runs. |
| "is to be" | The migration is to be run before you deploy the service. | Before you deploy the service, run the migration. |
| "can be" | The cache can be cleared. | You can clear the cache. |
| "must be" | The timeout must be set before the job starts. | Set the timeout before the job starts. |
| "will be ... by" | The report will be generated by the scheduler. | The scheduler will generate the report. |
| Present perfect passive | The connection pool has been created before the first query is sent. | The connection pool was created. Then the first query is sent. |
| "must be" (procedure) | The configuration file must be validated before the server starts. | Validate the configuration file before the server starts. |
| "are to be" | The user credentials are to be encrypted at rest and the key is rotated monthly. | Encrypt the user credentials at rest. Rotate the key every month. |
| "can be ... by" | The log entries can be exported to a CSV file by the admin. | The admin can export the log entries to a CSV file. |
| "will be ... by" | An error message will be shown by the validator if the input is empty. | The validator will show an error message if the input is empty. |
| Past perfect passive | The temporary files had been deleted by the cleanup task before the backup started. | The cleanup task removed the temporary files. Then the backup started. |

See also: Rule 3.2, Rule 3.3, Rule 3.5, Rule 3.6.

---

## Rule 3.5 — Use the "-ing" form only as a technical noun or as a modifier in a technical noun

In code documentation, a word that has an "-ing" form can be part of a verb, an
adjective, a noun, or a long group of modifiers. These functions cause ambiguity
and long sentences. Therefore an "-ing" word is not permitted as a verb.

Use an "-ing" word only as a technical noun (for example, in a heading) or as a
modifier inside a technical noun.

### Approved "-ing" words in STE-Code

| Part of speech | Words |
|---|---|
| Nouns | logging, monitoring, routing, servicing |
| Adjectives | matching, missing, remaining |
| Pronoun | something |
| Preposition | during |

### Why the progressive verb form is not approved

Rule 3.2 lists the only permitted forms: infinitive, imperative, simple present,
simple past, simple future, and past participle as an adjective. The progressive
("is running", "are deploying", "was processing") is not on that list. Replace
the progressive with the simple present or the simple past, and break a long
continuous clause into short sentences.

The "-ing" form also hides auxiliary constructions that Rule 3.4 forbids. Do not
write "the service is starting and then it is logging the request". Write "The
service starts. Then it logs the request."

### Approved "-ing" technical nouns (headings and titles)

Logging · Monitoring · Testing and Fault Isolation · Handling · Packaging ·
Shipping · Troubleshooting · Building · Deployment

### Approved "-ing" modifiers (inside a technical noun)

logging service · monitoring agent · routing table · switching relay ·
caching layer · building pipeline · binding configuration · streaming endpoint ·
rendering engine

Do not pull the "-ing" word out of the technical noun and use it as a verb. "The
caching layer stores the result" is approved. "The layer is caching the result"
is not.

### Correction pairs

| Non-STE | STE |
|---|---|
| When you are running this script, obey all the safety checks. | When you run this script, obey all the safety checks. |
| While the deployment is starting, you must watch the logs and you must not stop the process because stopping it during startup can corrupt the state file. | The deployment starts. While it starts, watch the logs. Do not stop the deployment. If you stop the deployment during startup, the state file can become corrupt. |
| The background worker is processing the queue and it is writing the results to the cache while the main thread is waiting for the response, causing the request to time out and the user to see an error. | The background worker processes the queue. It writes the results to the cache. The main thread waits for the response. If the main thread waits too long, the request times out and the user sees an error. |
| Be careful while the process is starting. | Be careful while the process starts. |
| The function is returning the value while the cache is loading the entry, which makes the result incorrect during the first request. | The function returns the value. The cache loads the entry. During the first request, the result is incorrect. |
| The matching algorithm is comparing the remaining items during the iteration and it is removing the missing records from the list. | The matching algorithm compares the remaining items during the iteration. It removes the missing records from the list. |
| Something going wrong during the migration can make the database stay in a broken state. | If something goes wrong during the migration, the database can stay in a broken state. |

### Long "-ing" clauses become vertical lists

Non-STE:

> A script opening a socket without checking the firewall rules and sending data
> to an unknown host, using an unverified certificate without reading the
> security policy, is in danger of causing a breach and thus exposing private
> keys and credentials.

STE:

> Before you open a socket, obey these precautions: (1) Read the security policy.
> (2) Make sure that the firewall rules allow the connection. (3) Verify the host
> certificate. (4) Get the correct credentials to send data to the host. If you do
> not obey these precautions, a breach of private keys and credentials can occur.

Non-STE:

> Developers committing code without running the test suite and pushing directly
> to the main branch, ignoring the review policy, risk breaking the build and
> therefore blocking the release for all team members.

STE:

> Before you commit code, obey these precautions: (1) Run the test suite. (2) Make
> sure that the tests pass. (3) Open a review before you merge to the main branch.
> If you do not obey these precautions, you can break the build and block the
> release for all team members.

See also: Rule 3.2, Rule 3.4, Rule 1.5.

---

## Rule 3.6 — Use the active voice

Use the active voice in all code documentation. In descriptive writing, the
passive voice is permitted only when the agent (the person, service, or component
that does the action) is unknown.

In the active voice, the subject does the action. The reader immediately knows
who or what performs the operation.

- Active: The middleware parses the API response.
- Passive: The API response is parsed by the middleware.

### The "by" test

Ask "by whom or by what?" after the verb phrase. If the sentence answers the
question, the sentence is passive.

- *The data was encrypted…* → by the crypto module. (Passive.)
- *The file was saved.* → by the application. (Passive, agent omitted.)
- *The file is saved.* (Not passive — a condition, a past participle used as an adjective. See Rule 3.3.)

### Four conversion methods

| Method | Use it when | Non-STE | STE |
|---|---|---|---|
| 1 — Move the agent to the subject | A "by"-phrase names the agent | The API response is parsed by the middleware. | The middleware parses the API response. |
| 2 — Change an infinitive to an active verb | A purpose clause hides the actor | To calculate the memory usage from these values. | The profiler calculates the memory usage from these values. |
| 3 — Use the imperative | Procedural text; the reader is the agent | The dependencies can be installed with the following command. | Install the dependencies with this command: `npm install` |
| 4 — Insert "you" or "we" | No agent is given | The configuration file can be edited with a text editor. | You can edit the configuration file with a text editor. |

Use "you" when the agent is the reader. Use "we" when the agent is your project
or organization.

### Method 1 in context — request pipeline README

Non-STE:

```markdown
## How the request pipeline works

After the client sends a request, the raw HTTP body is read by the server.
The API response is parsed by the middleware. The parsed data is then
validated by the schema checker before the controller receives it.
```

STE:

```markdown
## How the request pipeline works

After the client sends a request, the server reads the raw HTTP body.
The middleware parses the API response. The schema checker then validates
the parsed data before the controller receives it.
```

### Method 2 in context — a profiling docstring

Non-STE:

```python
def report_memory(samples):
    """To calculate the memory usage from these values. The peak is
    returned as a percentage of the allocated heap."""
```

STE:

```python
def report_memory(samples):
    """Calculate the memory usage from these values. Return the peak
    as a percentage of the allocated heap."""
```

### Method 3 in context — a contributing guide

Non-STE:

```markdown
## Setup

The dependencies can be installed with the following command. The test
suite can then be run from the same directory.
```

STE:

```markdown
## Setup

Install the dependencies with this command:

    npm install

Then run the test suite from the same directory:

    npm test
```

### Method 4 in context — a getting-started page

Non-STE:

```markdown
## First run

The configuration file can be edited with a text editor. The server
can be started after you save your changes.
```

STE:

```markdown
## First run

You can edit the configuration file with a text editor. After you save
your changes, you can start the server.
```

### When the agent is unknown

- Passive (correct): During the network request, the data was corrupted. The agent is unknown.
- Active (correct): During the network request, something corrupted the data.
- Active (incorrect): The network request corrupted the data. "network request" is not the correct agent, so the sentence becomes technically wrong.

### Further correction pairs

| Non-STE | STE |
|---|---|
| The database connection is established by the connection pool at startup. | The connection pool establishes the database connection at startup. |
| The test results can be viewed in the terminal output. | You can see the test results in the terminal output. |
| The configuration is loaded by the bootstrap routine. | The bootstrap routine loads the configuration. |
| The linting errors are reported by the linter. | The linter reports the linting errors. |
| The coverage report is generated by the coverage tool. | The coverage tool makes the coverage report. |

## Rule 3.6 by document type

### README files

A README mixes procedural text (installation, build, usage) and descriptive text
(overview, features, architecture). Use the imperative in procedural sections and
a named agent in descriptive sections.

| Non-STE | STE |
|---|---|
| The package can be installed with pip install. | Install the package with this command: `pip install .` |
| Support for WebSocket connections is provided by this library. | This library supports WebSocket connections. |

```markdown
## Installation

Install the package with this command:

    pip install .

Create a virtual environment before you install the package.
```

### API reference and docstrings

| Non-STE | STE |
|---|---|
| The input string is validated and a boolean is returned by this method. | This method validates the input string and returns a boolean. |
| The URL is transformed by the callback before the request is sent. | The callback transforms the URL before the client sends the request. |
| A `Promise<User>` is returned by this function. | This function returns a `Promise<User>`. |
| """A hash of the input data is computed and then it is returned as a hex string.""" | """Compute a hash of the input data. Return the hash as a hex string.""" |

### Code comments

| Non-STE | STE |
|---|---|
| // The buffer is flushed before new data is written. | // The writer flushes the buffer before it writes new data. |
| // The connection is closed by the finally block. | // The finally block closes the connection. |

### Commit messages

| Non-STE | STE |
|---|---|
| The authentication bug was fixed. | Fix the token refresh in the authentication middleware. |
| Rate limiting was added to the API endpoints. | Add rate limiting to the API endpoints. |

### Error messages

| Non-STE | STE |
|---|---|
| An invalid configuration value was encountered while the file was being parsed. | The parser found an invalid configuration value at line 12. |
| The request was rejected by the rate limiter. | The rate limiter rejected the request. |

## Rule 3.6 by paradigm

### Object-oriented (Java, C++, C#, Python classes)

Classes, methods, and pattern components are the agents.

| Non-STE | STE |
|---|---|
| The dependency is resolved by the container at runtime. | The container resolves the dependency at runtime. |
| New instances are created by the factory method when they are requested by the client. | The factory method creates a new instance when the client requests one. |
| The `validate()` method is called before the data is processed by the handler. | The handler calls the `validate()` method before it processes the data. |

```java
/**
 * The handler calls the validate() method before it processes the data.
 * The handler throws a ValidationException when it rejects the record.
 */
interface RequestHandler { void handle(Request req); }
```

### Functional (Haskell, Elixir, Clojure, Rust)

Functions and combinators are the agents.

| Non-STE | STE |
|---|---|
| Each element in the list is transformed by the `map` function. | The `map` function transforms each element in the list. |
| The input is filtered, then mapped, and finally the result is reduced to a single value. | The `filter` function removes invalid items. The `map` function transforms each item. The `reduce` function combines the results into a single value. |
| Two functions are composed into a new function by the `compose` combinator. | The `compose` combinator combines two functions into a new function. |

```clojure
;; The filter function removes invalid items. The map function transforms
;; each item. The reduce function combines the results into a single map.
(->> items (filter valid?) (map enrich) (reduce merge {}))
```

### Procedural (C, Go, Bash)

The script, the tool, or the function is the agent. Use the imperative in
procedural text.

| Non-STE | STE |
|---|---|
| The file is opened, the contents are read, and the connection is closed. | The script opens the file. It reads the contents. Then it closes the connection. |
| Environment variables are checked before the build process is started. | The script checks the environment variables. Then it starts the build process. |
| The log file can be rotated with the --rotate flag. | Use the --rotate flag to rotate the log file. |

```makefile
# The script checks the environment variables. Then it starts the build.
# Use the --rotate flag to rotate the log file.
build:
	./configure && $(MAKE)
```

### Declarative (SQL, Terraform, Kubernetes YAML, Dockerfile)

The declaration does not act. The tool or engine that reads the declaration acts.

| Non-STE | STE |
|---|---|
| An AWS VPC with three subnets is provisioned by this Terraform module. | This Terraform module provisions an AWS VPC with three subnets. |
| All rows with a status of 'active' are selected by this query. | This query selects all rows with a status of 'active'. |
| Three replicas of the pod are maintained by the deployment controller. | The deployment controller maintains three replicas of the pod. |
| # The base image is set to Ubuntu 22.04. | # Use Ubuntu 22.04 as the base image. |

NOTE: YAML comments and Dockerfile comments are procedural. Use the imperative
form and the active voice, because they instruct the reader or the build engine.

```sql
-- This query selects all rows with a status of 'active'. The aggregate
-- then counts the matching accounts.
SELECT count(*) FROM accounts WHERE status = 'active';
```

### Systems programming (Rust ownership, C memory, concurrency)

The allocator allocates. The function takes ownership. The mutex locks. The
channel sends.

| Non-STE | STE |
|---|---|
| The memory block is allocated by the allocator and a pointer is returned. | The allocator allocates the memory block. It returns a pointer. |
| Ownership of the string is taken by the `process` function. | The `process` function takes ownership of the string. |
| Access to the shared state is controlled by the mutex. | The mutex controls access to the shared state. |

```rust
// The mutex controls access to the shared state. The channel sends the
// value to the worker.
let guard = state.lock().unwrap();
tx.send(guard.clone());
```

## Rule 3.6 — extended examples

### Example 1 — README feature description

Non-STE: Authentication via OAuth2 and JWT tokens is supported by this service.
Rate limiting is applied to all endpoints. Requests are logged to a centralized
logging system.

STE: This service supports authentication with OAuth2 and JWT tokens. It applies
rate limiting to all endpoints. It sends request logs to a centralized logging
system.

The original has three consecutive passive constructions. The STE version
establishes "this service" as the agent once, then uses active verbs.

### Example 2 — API method documentation

Non-STE: `createUser(payload)` — A new user is created with the provided payload.
The payload is validated before the user record is inserted into the database. A
`User` object is returned upon success.

STE: `createUser(payload)` — Create a new user with the provided payload. The
method validates the payload. Then it inserts the user record into the database.
It returns a `User` object on success.

The reader of the original cannot tell whether the method, the database, or the
caller validates the payload.

### Example 3 — class docstring

```python
class ConnectionPool:
    """Manage a pool of database connections. The class lends a connection
    when a request arrives. It returns the connection when the request is
    complete. The reaper thread closes idle connections."""
```

### Example 4 — commit message

Non-STE: The memory leak in the image processing pipeline was fixed. Redundant
allocations were removed and the buffer pool was refactored.

STE: Fix the memory leak in the image processing pipeline. Remove redundant
allocations. Refactor the buffer pool.

### Example 5 — error message

```json
{
  "level": "error",
  "msg": "The token validator found a malformed token. The server rejected the request."
}
```

### Example 6 — configuration comment

```toml
# This setting controls the maximum number of concurrent connections.
# The server queues requests beyond this limit.
max_connections = 100
```

## Rule 3.6 — edge cases

### Edge case 1 — unknown agent (the standard exception)

When the agent is genuinely unknown, the passive voice is correct. In code
documentation this applies to:

- Unexpected data corruption with no identifiable cause
- External network failures where the remote endpoint is unknown
- Hardware faults that appear as software errors
- Race conditions where the exact sequence of events is not reproducible

- Correct (passive): The data was corrupted before the checksum was computed.
- Incorrect (active): Something corrupted the data before the checksum was computed. ("something" adds no information.)

NOTE: Use "something" as the agent only when you can describe the type of agent
(for example, "some process", "some external service"). If you cannot describe
the type, keep the passive voice.

### Edge case 2 — topic-comment structure in descriptive text

When the object is the established topic of the paragraph and the agent is
irrelevant, the passive voice can be clearer.

- Active (awkward): The developer stores the configuration file in the `/etc/myapp` directory.
- Passive (acceptable): The configuration file is stored in the `/etc/myapp` directory.
- Active (correct for a responsibility section): You must store the configuration file in the `/etc/myapp` directory.

Decision rule: if the paragraph topic is the object and an active rewrite would
introduce a distracting agent, use the passive voice. If the paragraph topic is
the agent, use the active voice.

### Edge case 3 — quotations from RFCs and specifications

Keep the passive voice inside a quotation and add a NOTE that identifies the
non-STE source. Do not rewrite the quotation. The rule applies only to the text
that you write.

> NOTE: The following description quotes RFC 7230. The passive voice in the
> quotation is from the original RFC text.
>
> > "The request message is parsed by the server into its component parts."

### Edge case 4 — framework-generated documentation

If you control the generator template (a Sphinx theme, a JSDoc template),
configure it to use the active voice. If you do not control the output, add a
NOTE at the top of the generated document.

> NOTE: This document was generated by [tool name]. Some sentences use the
> passive voice. Refer to the source code comments for STE-Code compliant
> descriptions.

### Edge case 5 — passive voice in established error message standards

Do not rewrite error strings from external systems (POSIX strings, HTTP reason
phrases, database error codes). The rule applies only to the messages that you
write.

- Your message (STE): The server cannot connect to the database at host:port.
- System message (unchanged): Connection refused.

## Rule 3.6 — grammar notes

### Structures

```
Active:  Subject (Agent) + Verb + Object (Patient)
Passive: Subject (Patient) + be + Past Participle (+ by + Agent)
```

Active voice gives the agent and the action in the natural reading order. Passive
voice gives the action first and the agent last, or not at all.

### Common passive constructions and their active equivalents

| Passive construction | Active equivalent | Method |
|---|---|---|
| is returned by | returns | 1 — move agent to subject |
| can be used to | you can use … to | 4 — insert "you" |
| is configured by | configures | 1 |
| is called when | calls | 1 |
| was added in version | (we) added … in version | 4 — insert "we" |
| should be installed | install (imperative) | 3 |
| is designed to | (we) designed … to | 4 |
| has been deprecated | (we) deprecated | 4 |
| will be removed in | (we) will remove … in | 4 |

### Passive with a modal verb

Keep the modal verb and move the agent to the subject position.

| Passive with modal | Active with modal |
|---|---|
| The file can be opened with this command. | You can open the file with this command. |
| The setting must be configured before startup. | You must configure the setting before startup. |
| The output will be written to stdout. | The program will write the output to stdout. |

### Structural patterns

| Pattern | Input structure | Output structure | Example |
|---|---|---|---|
| A — agent in a "by"-phrase (Method 1) | Patient + be + past participle + by + Agent | Agent + active verb + Patient | The token is validated by the auth middleware. → The auth middleware validates the token. |
| B — no agent, procedural (Method 3) | Patient + modal + be + past participle | Imperative verb + Patient | The dependencies should be installed before the build. → Install the dependencies before the build. |
| C — no agent, descriptive (Method 4) | Patient + be + past participle | You/We + active verb + Patient | The configuration file is stored in the config directory. → You must store the configuration file in the config directory. |

### Work together with the Canonical Synonym Table

When you convert a passive sentence, also check the replacement verb against the
Canonical Synonym Table.

| Non-STE | STE | Fixes applied |
|---|---|---|
| The result is used by the downstream pipeline. | The downstream pipeline uses the result. | Passive → active (Rule 3.6). |
| The error is displayed on the console by the logger. | The logger shows the error on the console. | Passive → active; "display" → "show" (Rule 1.1). |
| The report is generated by the scheduler every night. | The scheduler makes the report every night. | Passive → active; "generate" → "make" (Rule 1.1). |

### Rule 3.6 cross-references

- Rule 1.1 — the new agent must be an approved word or a permitted technical noun.
- Rule 1.5 — technical nouns that name code entities (middleware, validator, container, allocator, mutex) are permitted as agents. The agent must be a real code entity, not a vague abstraction.
- Rule 1.12 — the active verb is often a technical verb (parse, compile, deploy, render, query, allocate). Use its approved simple form.
- Rule 3.1 and Rule 3.2 — active voice sentences use the simple tenses. Converting to active voice also simplifies the tense.
- Rule 3.4 — the passive voice uses the auxiliary "be" plus a past participle. Converting to active voice removes the auxiliary.
- Rule 3.5 — a passive progressive ("is being parsed") breaks both Rule 3.5 and Rule 3.6. Convert to active voice first, then check the remaining "-ing" forms.
- Rule 3.7 — sentences must not exceed 20 words in procedural text and 25 words in descriptive text. Converting to active voice usually shortens the sentence. If the sentence is still too long, split it.
