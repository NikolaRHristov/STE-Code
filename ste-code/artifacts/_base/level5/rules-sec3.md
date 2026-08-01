<!-- a-sec3-rule3.1.md -->

# Rule 3.1 — Use only the verb forms that are given in the dictionary.

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.1

> Source: master.md#sec3-rule3.1

## Original Rule

The STE dictionary gives you the verb forms that you can use for each approved verb. Use only the verb forms that are given in the dictionary.

```
REMOVE (v)
REMOVES
REMOVED,
REMOVED

GIVE (v)
GIVES
GAVE,
GIVEN
```

> **Source:** Issue 9, Part 1 — Writing rules, Page 1-3-1, 2025-01-15

The introduction to the dictionary in part 2 gives you more information about the verb forms and how to use the approved verbs.

## STE-Code Adaptation

The STE-Code dictionary gives you the verb forms that you can use for each approved verb. Use only the verb forms that the dictionary gives for a verb. Do not use other forms (for example, gerunds, participles used as verbs with auxiliaries, or inflected forms that are not listed).

Every approved verb in the STE-Code dictionary appears with its allowed forms. Each entry shows four forms in this order: the base form, the third-person singular, the simple past, and the past participle. You use only those forms.

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

**How to read a dictionary entry**

| Line in the entry | Form | Example with WRITE | Where you use it |
|---|---|---|---|
| Line 1 | Base form (infinitive and imperative) | WRITE | "Write the log." / "to write the log" |
| Line 2 | Third-person singular, simple present | WRITES | "The logger writes the record." |
| Line 3 | Simple past | WROTE | "The job wrote the record." |
| Line 4 | Past participle (as an adjective) | WRITTEN | "the written log" |

If a form is not on one of those four lines, the form is not approved. The simple future is not a separate line: you make it with "will" and the base form ("will write").

The four approved verb categories in STE-Code are:

1. **Development operations** — build, compile, test, lint, format, commit, push, deploy, rollback
2. **Data operations** — read, write, serialize, deserialize, parse, encode, decode, query, insert, migrate
3. **Application operations** — handle, route, authenticate, authorize, validate, schedule, dispatch, resolve
4. **Communication operations** — send, receive, publish, subscribe, stream, poll, broadcast, connect

**How to apply the rule**

1. Find the verb in the STE-Code dictionary.
2. If the verb is not in the dictionary, do not use it. Use the approved verb that the dictionary gives instead. For example, use "make" and not "generate", use "get" and not "retrieve", use "check" and not "verify", use "use" and not "utilize", use "start" and not "initiate", use "stop" and not "terminate", use "remove" and not "delete", use "show" and not "render", use "do" and not "execute", and use "keep" and not "maintain".
3. If the verb is in the dictionary, use one of the four listed forms only.
4. Do not make a new form from an approved verb. "Parsing", "parseable", and "parser" are not verb forms of PARSE. A noun such as "parser" is approved only when the dictionary or a technical noun category gives it.
5. Use the past participle only as an adjective ("the parsed manifest", "the deprecated method"). Do not use it with "have", "has", "had", or "get" to make a verb.

> **Note: structural carryover — no code-domain equivalent** — The dictionary layout (base form, third-person singular, simple past, past participle shown for each verb) is a structural feature of the source standard. The code-domain version keeps the same layout with code verbs. No mapping is forced.

## Examples

> *Adapted from spec pair:* Non-STE: The tool is removing the given information from the tank. | STE: The tool removes the given information.

> **Non-STE:** The linter validates the file and is reporting the errors to the terminal.
> **STE:** The linter validates the file. It reports the errors to the terminal.
>
> *Adapted from spec principle: use only the verb forms that the dictionary gives. The progressive form "is reporting" is not one of the four listed forms of REPORT.*
>
> ```bash
> $ eslint src/index.js
> # STE: the linter validates the file. It reports the errors to the terminal.
> src/index.js
>   12:5  error  'config' is assigned a value but never used  no-unused-vars
> ✖ 1 problem (1 error, 0 warnings)
> ```

> **Non-STE:** The script has written the output to the log before the test starts.
> **STE:** The script wrote the output to the log. Then the test starts.
>
> *Adapted from spec principle: WRITE gives WRITE / WRITES / WROTE / WRITTEN. The present perfect "has written" is not a listed form.*
>
> ```python
> # STE: the script wrote the output to the log. Then the test starts.
> def main() -> None:
>     with open("build.log", "w", encoding="utf-8") as log:
>         log.write("build complete\n")   # write -> writes / wrote / written
>     run_tests()
> ```

> **Non-STE:** The service utilizes a token cache and leverages the parser for each request.
> **STE:** The service uses a token cache. The service parses each request.
>
> *Adapted from spec principle: "utilize" and "leverage" are not in the dictionary. Use the approved verbs USE and PARSE.*
>
> ```javascript
> // STE: the service uses a token cache. The service parses each request.
> const cache = new TokenCache();          // use -> uses / used / used
> app.post("/orders", (req, res) => {
>   const order = parseOrder(req.body);    // parse -> parses / parsed / parsed
>   res.json(order);
> });
> ```

> **Non-STE:** The parsing of the manifest is done by the loader, and the validating of the schema comes after.
> **STE:** The loader parses the manifest. Then the loader validates the schema.
>
> *Adapted from spec principle: "parsing" and "validating" are gerunds. A gerund is not one of the four forms in the dictionary entry. Use the simple present tense and name the actor.*
>
> ```python
> # STE: the loader parses the manifest. Then the loader validates the schema.
> manifest = loader.parse(path)      # parse -> parses / parsed / parsed
> loader.validate(manifest, schema)  # validate -> validates / validated / validated
> ```

> **Non-STE:** The migration had deleted the deprecated column and was terminating the open connections.
> **STE:** The migration removed the deprecated column. Then the migration stopped the open connections.
>
> *Adapted from spec principle: "delete" and "terminate" are not approved verbs; use REMOVE and STOP. The past perfect "had deleted" and the progressive "was terminating" are not listed forms.*
>
> ```sql
> -- STE: the migration removed the deprecated column.
> ALTER TABLE accounts DROP COLUMN legacy_token;
> -- Then the migration stopped the open connections.
> SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'orders';
> ```

> **Non-STE:** The client will be receiving the streamed records after the broker has been publishing them for one minute.
> **STE:** The broker publishes the records. The client will receive the streamed records after one minute.
>
> *Adapted from spec principle: the future progressive and the perfect progressive are not listed forms. Make the simple future with "will" and the base form. "Streamed" is correct because it is a past participle used as an adjective.*
>
> ```go
> // STE: the broker publishes the records.
> // The client will receive the streamed records after one minute.
> func (b *Broker) Publish(rec []byte) error { // publish -> publishes / published / published
>     return b.topic.Send(rec)                 // send -> sends / sent / sent
> }
> ```

> **Non-STE:** The given options get validated by the gateway, and the removed entries are gotten from the cache.
> **STE:** The gateway validates the given options. The gateway gets the removed entries from the cache.
>
> *Adapted from spec principle: "get validated" and "are gotten" are not listed forms. Name the actor and use the simple present tense. "Given" and "removed" are correct because they are past participles used as adjectives.*
>
> ```json
> {
>   "options": ["--release", "--strip"],
>   "validated": true,
>   "removedEntries": 12
> }
> ```

> **See also:** Rule 3.2 — Use Only These Verb Forms and Tenses of Verbs
> **See also:** Rule 3.3 — Use the Active Voice
> **See also:** Rule 3.4 — Do Not Leave Out a Verb or a Part of a Verb
> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** Rule 1.5 — Technical Noun Categories
> **See also:** The STE-Code dictionary (a-dictionary.md) — the full list of approved verbs and their allowed forms

---

<!-- a-sec3-rule3.2.md -->

# Rule 3.2 — Use only these verb forms and tenses of verbs.

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.2

> Source: master.md#sec3-rule3.2

## Original Rule

Use only these verb forms and tenses of verbs:

- The infinitive form
- The imperative form (command form)
- The simple present tense
- The simple past tense
- The simple future tense
- The past participle form (as an adjective).

Use only the verbs forms and the tenses of verbs that are approved.

| Infinitive form (base form) | Imperative form (command form) | Simple present tense | Simple past tense | Simple future tense | Past participle form (as an adjective) |
|---|---|---|---|---|---|
| (To) Adjust (regular verb) | Adjust + object | You/we/they adjust It adjusts | You/we/they adjusted It adjusted | You/we/they will adjust It will adjust | The adjusted linkage |
| (To) Give (irregular verb) | Give + object | You/we/they give It gives | You/we/they gave It gave | You/we/they will give It will give | The given information |

Do not use other forms and tenses that are not approved, for example:

- The present perfect (have/has adjusted)
- The past perfect (had adjusted)
- The present/past progressive (is/was adjusting)
- And all other complex verb constructions.

> **Source:** Issue 9, Part 1 — Writing rules, Page 64 of 434, 2025-01-15

The introduction to the dictionary in part 2 gives you more information about the verb forms and how to use the approved verbs.

## STE-Code Adaptation

Use only these verb forms and tenses of verbs:

- The infinitive form
- The imperative form (command form)
- The simple present tense
- The simple past tense
- The simple future tense
- The past participle form (as an adjective).

Use only the verb forms and the tenses of verbs that are approved in the STE-Code dictionary.

| Infinitive form (base form) | Imperative form (command form) | Simple present tense | Simple past tense | Simple future tense | Past participle form (as an adjective) |
|---|---|---|---|---|---|
| (To) Parse (regular verb) | Parse + object | You/we/they parse It parses | You/we/they parsed It parsed | You/we/they will parse It will parse | The parsed file |
| (To) Write (irregular verb) | Write + object | You/we/they write It writes | You/we/they wrote It wrote | You/we/they will write It will — It will write | The written log |
| (To) Build (irregular verb) | Build + object | You/we/they build It builds | You/we/they built It built | You/we/they will build It will build | The built artifact |
| (To) Send (irregular verb) | Send + object | You/we/they send It sends | You/we/they sent It sent | You/we/they will send It will send | The sent request |
| (To) Validate (regular verb) | Validate + object | You/we/they validate It validates | You/we/they validated It validated | You/we/they will validate It will validate | The validated token |

Do not use other forms and tenses that are not approved, for example:

- The present perfect (have/has parsed)
- The past perfect (had parsed)
- The present/past progressive (is/was parsing)
- The future progressive (will be parsing)
- The perfect progressive (has been parsing, had been parsing)
- The gerund used as a verb with an auxiliary (is parsing, keeps parsing)
- And all other complex verb constructions.

**How to select the correct form**

1. **Infinitive form.** Use the infinitive after a modal verb or to state a purpose: "Use this flag to parse the file."
2. **Imperative form.** Use the imperative for each step of a procedure: "Parse the file. Write the log."
3. **Simple present tense.** Use the simple present for a general fact, a repeated action, or the behavior of a system: "The parser reads the file."
4. **Simple past tense.** Use the simple past for an action that is complete: "The build failed."
5. **Simple future tense.** Use "will" with the base form for an action that comes later: "The job will start at 02:00."
6. **Past participle form.** Use the past participle only as an adjective before a noun: "the parsed file", "the deprecated method". Do not use it with "have", "has", "had", or "get" as a verb.

**How to correct an unapproved form**

- Present perfect ("has parsed") → simple past ("parsed").
- Past perfect ("had parsed") → simple past in two sentences with "Then".
- Progressive ("is parsing", "was parsing") → simple present or simple past. If two actions happen together, write two sentences and add "at the same time".
- Future progressive ("will be parsing") → simple future ("will parse").
- Passive with an unapproved auxiliary ("is being parsed") → name the actor and use the active voice ("the worker parses the file") (see Rule 3.6).

> **Note: structural carryover — no code-domain equivalent** — The six-column table of verb forms is a structural feature of the source standard. The code-domain version keeps the same table with approved code verbs. No mapping is forced.

## Examples

> *Adapted from spec pair:* Non-STE: The technician has adjusted the linkage. | STE: The technician adjusted the linkage.

> **Non-STE:** The linter has found three errors in the source file.
> **STE:** The linter found three errors in the source file.
>
> *Adapted from spec pair: the present perfect "have/has adjusted" is not approved. Use the simple past tense.*
>
> ```bash
> $ eslint src/index.js
> # STE comment: the linter found three errors in the source file.
> src/index.js: 3 problems (3 errors, 0 warnings)
> ```

> **Non-STE:** The server was processing the request when the timeout occurred.
> **STE:** The server processed the request. Then the timeout occurred.
>
> *Adapted from spec pair: the past progressive "was adjusting" is not approved. Break the sentence into separate sentences.*
>
> ```python
> # STE: two complete actions, simple past tense in the comment
> # The server processed the request. Then the timeout occurred.
> try:
>     response = server.process(request)   # process -> processes / processed / processed
> except TimeoutError:
>     log.write("request timeout after 30 s")
> ```

> **Non-STE:** The framework had already initialized the connection pool before the query started.
> **STE:** The framework made the connection pool. Then the query started.
>
> *Adapted from spec pair: the past perfect "had adjusted" is not approved. Use the simple past tense and sequence with "Then." The approved verb is "make" (replaces create/initialize), not "utilize" or "commence".*
>
> ```yaml
> # STE: two sequential steps
> steps:
>   - name: make-pool        # the framework made the connection pool
>     run: python app.py --pool-size 10
>   - name: run-query        # then the query started
>     run: python app.py --query "SELECT 1"
> ```

> **Non-STE:** The scheduler is deploying the build to production while the tests are running.
> **STE:** The scheduler sends the build to production. The tests run at the same time.
>
> *Adapted from spec pair: the present progressive "is adjusting" is not approved. Use the simple present tense for each action. Use the approved verb "send" (replaces transmit/dispatch), not "deploy" with a progressive form.*
>
> ```yaml
> # .github/workflows/release.yml
> # STE: the scheduler sends the build to production. The test runs at the same time.
> jobs:
>   deploy:
>     runs-on: ubuntu-latest
>     steps:
>       - run: ./scripts/send-build.sh production
>   test:
>     runs-on: ubuntu-latest
>     steps:
>       - run: pytest tests/
> ```

> **Non-STE:** The cache has been keeping the serialized records since the service started, and the client will be reading them after the restart.
> **STE:** The cache keeps the serialized records. The client will read the records after the restart.
>
> *Adapted from spec pair: the perfect progressive "has been adjusting" and the future progressive "will be adjusting" are not approved. Use the simple present and the simple future. "Serialized" is correct here because it is a past participle used as an adjective.*
>
> ```go
> // STE: simple present and simple future in the documentation comment.
> // The cache keeps the serialized records.
> // The client will read the records after the restart.
> func (c *Cache) Keep(records []byte) error {
>     return c.store.Write(records) // write -> writes / wrote / written
> }
> ```

> **Non-STE:** To be parsing the configuration file, the loader must be having read access to the directory.
> **STE:** To parse the configuration file, the loader must have read access to the directory.
>
> *Adapted from spec pair: use the infinitive form, not a progressive infinitive. Use the base form after a modal verb.*
>
> ```python
> # STE: infinitive after "to" and base form after the modal verb
> def load_config(path):
>     """Read the file. To parse the file, the loader must have read access."""
>     if not os.access(path, os.R_OK):
>         raise PermissionError("no read access to the config directory")
>     return parse(open(path).read())   # parse -> parses / parsed / parsed
> ```

> **Non-STE:** You should be setting the timeout value and then you will be restarting the service.
> **STE:** Set the timeout value. Then start the service again.
>
> *Adapted from spec pair: use the imperative form for each step of a procedure. The progressive forms are not approved.*
>
> ```bash
> # STE: one imperative step for each line
> # Set the timeout value.
> export REQUEST_TIMEOUT=30
> # Then start the service again.
> systemctl restart api.service
> ```

> **Non-STE:** The payload is being validated by the gateway and the deprecated field gets removed by the migration.
> **STE:** The gateway validates the payload. The migration removes the deprecated field.
>
> *Adapted from spec pair: the passive progressive "is being adjusted" and "gets adjusted" are not approved forms. Name the actor and use the simple present tense. "Deprecated" is correct because it is a past participle used as an adjective.*
>
> ```javascript
> // STE: active voice, simple present tense
> // The gateway validates the payload.
> // The migration removes the deprecated field.
> gateway.validate(payload);            // validate -> validates / validated / validated
> migration.remove(record.legacyId);    // remove -> removes / removed / removed
> ```

> **Non-STE:** The written log and the parsed manifest are showing that the build had completed with the given options.
> **STE:** The written log and the parsed manifest show that the build completed with the given options.
>
> *Adapted from spec pair: "the adjusted linkage" and "the given information" show the past participle used as an adjective. This use is approved. The progressive "are showing" and the past perfect "had completed" are not approved.*
>
> ```json
> {
>   "log": "build.log",
>   "manifest": "parsed-manifest.json",
>   "status": "completed",
>   "options": ["--release", "--strip"]
> }
> ```

> **Non-STE:** We have been building the release artifact and the CI pipeline will have run the tests by the time you review the pull request.
> **STE:** We built the release artifact. The CI pipeline will run the tests. Then you can review the pull request.
>
> *Adapted from spec pair: the perfect progressive "have been building" and the future perfect "will have run" are not approved. Use the simple past and the simple future, and follow the sequence with "Then".*
>
> ```yaml
> # .github/workflows/ci.yml
> # STE: we built the release artifact. The CI pipeline will run the tests.
> jobs:
>   build:
>     steps:
>       - run: make release
>   test:
>     needs: build
>     steps:
>       - run: make test
> ```

> **Non-STE:** If the connection drops, the client is retrying the request until the server responds.
> **STE:** If the connection drops, the client retries the request. Then the server responds.
>
> *Adapted from spec pair: the present progressive "is retrying" is not approved. Use the simple present for each action and separate the sequence with "Then".*
>
> ```python
> # STE: simple present in the documentation comment
> # If the connection drops, the client retries the request. Then the server responds.
> def on_drop(client, server):
>     client.retry()    # retry -> retries / retried / retried
>     server.respond()  # respond -> responds / responded / responded
> ```

> **See also:** Rule 3.1 — Use Only the Verb Forms That Are Given in the Dictionary
> **See also:** Rule 3.3 — Use the Past Participle Form as an Adjective
> **See also:** Rule 3.4 — Do Not Use Auxiliary Verbs to Make Complex Verb Constructions
> **See also:** Rule 3.5 — Use the "-ing" Form of a Verb Only as a Technical Noun
> **See also:** Rule 3.6 — Use the Active Voice
> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** The STE-Code dictionary (a-dictionary.md) — the full list of approved verbs and their allowed forms

---

<!-- a-sec3-rule3.3.md -->

# Rule 3.3 — Use the past participle form as an adjective.

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.3

> Source: master.md#sec3-rule3.3

## Original Rule

When you use the past participle form as an adjective, it shows the condition of something. This is not passive voice. Use the past participle form of a verb as an adjective as follows:

- Before a noun
- After a verb form of the verbs "to be," "to become," or "to stay."

Do not use the past participle form if it is not in the dictionary.

> **STE:** Examine all parts of the disassembled unit for damage.
>
> ("Disassembled" is an adjective before the noun "unit." It shows the condition of the unit.)

> **STE:** When the unit is fully disassembled, clean all the parts.
>
> ("Disassembled" is an adjective after the verb "to be" that shows the condition of the unit.)

There are also approved adjectives in the dictionary that are the past participle form of verbs that are not approved. For example, "permitted," and "damaged." Their approved part of speech in the dictionary is "(adj)" and thus you can use them.

> **STE:** Do not put more than the permitted weight on the trolley.
>
> **STE:** Make sure that the mating surfaces are not damaged.

## STE-Code Adaptation

When you use the past participle form as an adjective, it shows the condition of something. This is not passive voice. Use the past participle form of an approved verb as an adjective as follows:

- Before a noun
- After a verb form of the verbs "to be," "to become," or "to stay."

Do not use the past participle form if it is not in the STE-Code dictionary.

There are also approved adjectives in the STE-Code dictionary that are the past participle form of verbs that are not approved. Their approved part of speech in the dictionary is "(adj)" and thus you can use them.

**How to know that the past participle is an adjective and not passive voice**

1. The word gives the **condition** of the thing, not an action that an actor does.
2. You can put the word directly before the noun: "the parsed file", "the deprecated method", "the closed connection".
3. You can put the word after "is", "becomes", or "stays": "the cache is initialized", "the endpoint becomes deprecated", "the record stays locked".
4. If the sentence names an actor and an action ("the file was parsed by the loader"), the sentence is passive voice. Write the active voice instead (see Rule 3.6).

**Common code-domain past participles that are approved as adjectives**

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

**Cautions**

- Do not make a new past participle from an unapproved verb. Write "the deleted branch" only if "delete" or "deleted (adj)" is in the dictionary; if it is not, use the approved verb "remove" and write "the removed branch".
- Do not use a past participle as a verb with "have", "has", or "had" (see Rule 3.2).
- Do not put more than one past participle before the same noun. Write "the parsed and validated payload" as two short sentences if the phrase becomes difficult.
- Prefer the plain word. Use "started", not "commenced". Use "used", not "utilized" or "leveraged". Use "stopped", not "terminated".

> **Note: structural carryover — no code-domain equivalent** — The source rule uses aerospace hardware ("disassembled unit", "mating surfaces") to show the grammar. The code-domain version keeps the same grammar and gives software conditions instead. No mapping is forced.

## Examples

> *Adapted from spec pair:* Non-STE: The unit was disassembled by the technician. | STE: Examine all parts of the disassembled unit for damage.

> **STE:** Inspect all fields of the deserialized object for corruption.
>
> ("Deserialized" is an adjective before the noun "object." It shows the condition of the object.)
>
> ```python
> # STE: "deserialized" gives the condition of the object.
> obj = json.loads(payload)          # the deserialized object
> for name, value in obj.items():
>     if value is None:
>         log.write(f"field {name} is corrupted")
> ```

> **STE:** When the cache is fully initialized, start the worker threads.
>
> ("Initialized" is an adjective after the verb "to be." It shows the condition of the cache.)
>
> ```go
> // STE: "initialized" comes after "is" and gives the condition of the cache.
> if cache.IsInitialized() {
>     pool.Start(workerCount)
> }
> ```

> **STE:** Do not exceed the allowed memory for the buffer.
>
> *Adapted from spec pair: "Do not put more than the permitted weight on the trolley." ("permitted" is an approved adjective with part of speech "(adj)".)*
>
> ```yaml
> # config/limits.yml
> # STE: the allowed memory for the buffer is 256 MB.
> buffer:
>   allowed_memory_mb: 256
> ```

> **STE:** Make sure that the input values are not corrupted.
>
> *Adapted from spec pair: "Make sure that the mating surfaces are not damaged." ("damaged" is an approved adjective with part of speech "(adj)".)*
>
> ```python
> # STE: "corrupted" gives the condition of the values.
> def check(values):
>     """Make sure that the input values are not corrupted."""
>     if any(v is None for v in values):
>         raise ValueError("the input values are corrupted")
> ```

> **Non-STE:** The parsed file was processed by the loader.
> **STE:** The parsed file is ready for the loader.
>
> *Adapted from spec principle: "parsed" is the past participle used as an adjective before the noun "file." It shows the condition of the file, not passive voice.*
>
> ```python
> # STE: "parsed" is an adjective. The sentence keeps the active voice.
> parsed_file = parse(path)   # the parsed file is ready for the loader
> loader.load(parsed_file)
> ```

> **Non-STE:** The method has been deprecated by the API team in release 4.2.
> **STE:** The method is deprecated in release 4.2. Do not use the deprecated method in new code.
>
> *Adapted from spec principle: "deprecated" is an approved adjective. Do not make a complex verb construction with "has been".*
>
> ```java
> /**
>  * STE: the method is deprecated in release 4.2.
>  * Use {@link #send(Request)} instead.
>  */
> @Deprecated
> public void transmit(Request request) { ... }
> ```

> **Non-STE:** After the record gets locked, the transaction which was started earlier is being committed.
> **STE:** The transaction writes the locked record. Then the transaction ends.
>
> *Adapted from spec principle: "locked" is the past participle as an adjective before the noun "record." "Gets locked" and "is being committed" are passive constructions that are not approved (see Rule 3.4 and Rule 3.6).*
>
> ```sql
> -- STE: the transaction writes the locked record. Then the transaction ends.
> BEGIN;
> SELECT * FROM orders WHERE id = 42 FOR UPDATE;  -- the locked row
> UPDATE orders SET status = 'sent' WHERE id = 42;
> COMMIT;
> ```

> **Non-STE:** The signed token which had been given to the client is validated by the gateway on each request.
> **STE:** The gateway validates the signed token on each request.
>
> *Adapted from spec principle: "signed" is a past participle as an adjective before the noun "token." The gateway is the actor, so use the active voice.*
>
> ```javascript
> // STE: the gateway validates the signed token on each request.
> app.use((req, res, next) => {
>   const signedToken = req.headers.authorization; // the signed token
>   if (!gateway.validate(signedToken)) {
>     return res.status(401).send("the signed token is not valid");
>   }
>   next();
> });
> ```

> **Non-STE:** When the index becomes corrupted it will have to be being rebuilt by the maintenance job.
> **STE:** When the index becomes corrupted, the maintenance job makes the index again.
>
> *Adapted from spec principle: "corrupted" comes after the verb "to become" and shows the condition of the index. Use the approved verb "make" and the active voice for the action.*
>
> ```bash
> # STE: when the index becomes corrupted, the maintenance job makes the index again.
> if ! sqlite3 app.db "PRAGMA integrity_check;" | grep -q "^ok$"; then
>   ./scripts/make-index.sh app.db
> fi
> ```

> **Non-STE:** The build artifact stays uncompiled until the pipeline has compiled the modified sources.
> **STE:** The artifact stays unbuilt until the pipeline builds the modified sources.
>
> *Adapted from spec principle: "unbuilt" and "modified" show conditions after "to stay" and before a noun. Do not use the present perfect "has compiled" (see Rule 3.2).*
>
> ```yaml
> # .github/workflows/ci.yml
> # STE: the pipeline builds the modified sources. Then the artifact is ready.
> jobs:
>   build:
>     steps:
>       - run: git diff --name-only HEAD~1   # the modified sources
>       - run: make build
> ```

> **Non-STE:** The user is shown a warning if the uploaded configuration file was found to be malformed.
> **STE:** The CLI shows a warning if the uploaded configuration file is malformed.
>
> *Adapted from spec principle: "uploaded" and "malformed" are adjectives that show the condition of the file. Name the actor ("the CLI") and use the active voice.*
>
> ```bash
> $ myapp config upload ./app.toml
> # STE: the CLI shows a warning if the uploaded configuration file is malformed.
> warning: the uploaded configuration file is malformed at line 12
> ```

> **Non-STE:** All of the returned records had already been serialized before the response was sent.
> **STE:** The API sends the serialized records in the response.
>
> *Adapted from spec principle: "serialized" is an adjective before the noun "records." Use the simple present tense and the approved verb "send".*
>
> ```json
> {
>   "records": [
>     { "id": 1, "state": "serialized" },
>     { "id": 2, "state": "serialized" }
>   ],
>   "count": 2
> }
> ```

> **Non-STE:** Make sure that the written log and the given options are not being modified by the plugin.
> **STE:** Make sure that the plugin does not change the written log or the given options.
>
> *Adapted from spec principle: "written" and "given" are approved past participles used as adjectives. Change the passive progressive to the active voice.*
>
> ```python
> # STE: make sure that the plugin does not change the written log or the given options.
> def run_plugin(plugin, log_path, options):
>     before = hash_file(log_path)
>     plugin.run(dict(options))          # the given options, as a copy
>     if hash_file(log_path) != before:
>         raise RuntimeError("the plugin changed the written log")
> ```

> **See also:** Rule 3.1 — Use Only the Verb Forms That Are Given in the Dictionary
> **See also:** Rule 3.2 — Use Only These Verb Forms and Tenses of Verbs
> **See also:** Rule 3.4 — Do Not Use Auxiliary Verbs to Make Complex Verb Constructions
> **See also:** Rule 3.5 — Use the "-ing" Form of a Verb Only as a Technical Noun
> **See also:** Rule 3.6 — Use the Active Voice
> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** The STE-Code dictionary (a-dictionary.md) — the approved adjectives with part of speech "(adj)"

---

<!-- a-sec3-rule3.4.md -->

# Rule 3.4 — Do not use auxiliary verbs to make complex verb constructions.

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.4

> Source: master.md#sec3-rule3.4

## Original Rule

Do not use the past participle form as a verb form together with the auxiliary verb "have." This construction will make a tense that is not approved.

> **Non-STE:** The operator has adjusted the linkage. (The present perfect tense is not approved.)
>
> **STE:** The operator adjusted the linkage. (The simple past tense is approved.)

Some complex verb constructions include other auxiliary verbs with the past participle form as a verb. Sentences with these constructions become complex sentences in the passive voice.

> **Non-STE:** The seat is to be installed before you install the cushion
>
> **STE:** Before you install the cushion, install the seat.
>
> **Non-STE:** The volume control can be adjusted.
>
> **STE:** You can adjust the volume control.
>
> **Non-STE:** The temperature must be adjusted.
>
> **STE:** Adjust the temperature.
>
> **Non-STE:** The sleeve will be adjusted by the robot.
>
> **STE:** The robot will adjust the sleeve.

## STE-Code Adaptation

Do not use the past participle form as a verb form together with the auxiliary verb "have." This construction will make a tense that is not approved in code documentation.

Do not use auxiliary verbs ("have," "be," "will," "can," "must," "should," "is to be") with a past participle to build compound tenses or passive voice. These constructions make complex verb forms that STE-Code does not approve. Write the action with a simple, approved verb form instead:

- Use the simple past instead of "have/has/had + past participle" (present or past perfect).
- Use the active voice with a clear agent instead of "be + past participle" (passive voice). See Rule 3.6.
- Use the imperative (command) form for instructions instead of "is to be + past participle."
- Use "you can + base verb" instead of "can be + past participle" when the reader is the agent.
- Use "will + base verb" with a named agent instead of "will be + past participle + by + agent."

Some complex verb constructions include other auxiliary verbs with the past participle form as a verb. Sentences with these constructions become complex sentences in the passive voice. Convert them to a simple active form.

When a compound construction is unavoidable for correctness (for example, a progressive state that the code is genuinely in), split it into separate simple sentences. Rule 3.2 lists the only approved verb forms: infinitive, imperative, simple present, simple past, simple future, and past participle as an adjective.

## Examples

> **Non-STE:** The build has compiled the module before the test runs. (The present perfect tense is not approved.)
>
> **STE:** The build compiled the module. Then the test runs. (The simple past tense is approved.)
>
> *Adapted from spec pair: Non-STE: "The operator has adjusted the linkage." (present perfect is not approved) | STE: "The operator adjusted the linkage." (simple past is approved)*

> **Non-STE:** The migration is to be run before you deploy the service.
>
> **STE:** Before you deploy the service, run the migration.
>
> *Adapted from spec pair: Non-STE: "The seat is to be installed before you install the cushion" | STE: "Before you install the cushion, install the seat."*

> **Non-STE:** The cache can be cleared.
>
> **STE:** You can clear the cache.
>
> *Adapted from spec pair: Non-STE: "The volume control can be adjusted." | STE: "You can adjust the volume control."*

> **Non-STE:** The timeout must be set before the job starts.
>
> **STE:** Set the timeout before the job starts.
>
> *Adapted from spec pair: Non-STE: "The temperature must be adjusted." | STE: "Adjust the temperature."*

> **Non-STE:** The report will be generated by the scheduler.
>
> **STE:** The scheduler will generate the report.
>
> *Adapted from spec pair: Non-STE: "The sleeve will be adjusted by the robot." | STE: "The robot will adjust the sleeve."*

> **Non-STE:** The connection pool has been created before the first query is sent.
>
> **STE:** The connection pool was created. Then the first query is sent.
>
> *Adapted from spec principle: "have/has + been + past participle" (present perfect passive) is not approved. Use the simple past and separate the clauses.*

> **Non-STE:** The configuration file must be validated before the server starts.
>
> **STE:** Validate the configuration file before the server starts.
>
> *Adapted from spec pair: Non-STE: "The temperature must be adjusted." | STE: "Adjust the temperature." (imperative for procedural instruction)*

> **Non-STE:** The user credentials are to be encrypted at rest and the key is rotated monthly.
>
> **STE:** Encrypt the user credentials at rest. Rotate the key every month.
>
> *Adapted from spec pair: Non-STE: "The seat is to be installed before you install the cushion" | STE: "Before you install the cushion, install the seat."*

> **Non-STE:** The log entries can be exported to a CSV file by the admin.
>
> **STE:** The admin can export the log entries to a CSV file.
>
> *Adapted from spec pair: Non-STE: "The volume control can be adjusted." | STE: "You can adjust the volume control." (name the agent, use active voice)*

> **Non-STE:** An error message will be shown by the validator if the input is empty.
>
> **STE:** The validator will show an error message if the input is empty.
>
> *Adapted from spec pair: Non-STE: "The sleeve will be adjusted by the robot." | STE: "The robot will adjust the sleeve."*

> **Non-STE:** The temporary files had been deleted by the cleanup task before the backup started.
>
> **STE:** The cleanup task deleted the temporary files. Then the backup started.
>
> *Adapted from spec principle: "had + been + past participle" (past perfect passive) is not approved. Use the simple past and sequence with "Then."*

> **See also:** Rule 3.2 — Use only these verb forms and tenses of verbs.
>
> **See also:** Rule 3.3 — Use the past participle form as an adjective.
>
> **See also:** Rule 3.5 — Use the "-ing" form of a verb only as a technical noun or as a modifier in a technical noun.
>
> **See also:** Rule 3.6 — Use the Active Voice.

---

<!-- a-sec3-rule3.5.md -->

# Rule 3.5 — Use the "-ing" form of a verb only as a technical noun or as a modifier in a technical noun.

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.5

> Source: master.md#sec3-rule3.5

## Original Rule

In English, words that have an "-ing" form can have different functions in a sentence (different parts of speech).

Words that have an "-ing" form can be part of a verb to describe an action in the present.

> **STE:** Be careful while the door is opening.

They can also be adjectives.

> **STE:** An opening door can be dangerous.

They can be nouns or parts of noun phrases.

> **STE:** Opening a door can be dangerous.

They can make long groups of modifiers, noun phrases, and dependent clauses.

> **STE:** A mechanic opening a door without obeying the specified safety precautions can easily cause injury to persons standing near the door.

These different functions for words that have an "-ing" form can frequently cause ambiguity or long, complex sentences. Thus, words that have an "-ing" form are usually not permitted.

> **Non-STE:** When you are doing this procedure, obey all the safety precautions.
>
> **STE:** When you do this procedure, obey all the safety precautions.
>
> **Non-STE:** Mechanics wearing insufficient protective clothing and opening containers containing hazardous materials in areas where there is a lack of ventilation, using inappropriate tools without observing the manufacturer's instructions, are in danger of coming into contact with these materials and thus suffering from skin irritation and breathing problems.
>
> **STE:** Before you use dangerous materials, obey these precautions: (1) Read the manufacturer's instructions. (2) Make sure that there is sufficient airflow in the work area. (3) Put on a face mask and protective clothing. (4) Get the correct tools to open the containers for these materials. If you do not obey these precautions, injury to your skin and your lungs can occur.

Words that have an "-ing" form and are technical nouns or parts of technical nouns:

You can use a word that has an "-ing" form as a technical noun (for example, in procedural titles or headings).

> **STE:** Cleaning, Testing and Fault Isolation, Handling, Package, Shipping, Troubleshooting

You can also use the "-ing" form of a verb as a modifier in a technical noun. This modifier is an adjective that is related to the function of a system, component, part, tool, material, or equipment.

> **STE:** Air-conditioning system, degreasing agent, grinding wheel, polishing disc, sanding machine, switching relay, welding torch

Approved words that have an "-ing" form:

Only a small number of approved words in the dictionary have an "-ing" form. They are:

- Nouns (lighting, opening, routing, and servicing)
- Adjectives (mating, missing, and remaining)
- A pronoun (something)
- A preposition (during).

## STE-Code Adaptation

In code documentation, words that have an "-ing" form can have different functions in a sentence. They can be part of a verb that describes an action in the present, an adjective, a noun, or a long group of modifiers. These different functions can cause ambiguity or long, complex sentences. Thus, words that have an "-ing" form are usually not permitted as verbs.

Use a word that has an "-ing" form only as a technical noun (for example, in procedural titles or headings) or as a modifier in a technical noun.

Approved words that have an "-ing" form in STE-Code:

- Nouns (logging, monitoring, routing, and servicing)
- Adjectives (matching, missing, and remaining)
- A pronoun (something)
- A preposition (during).

### Why the progressive verb form is not approved

Rule 3.2 lists the only permitted verb forms and tenses: the infinitive, the imperative, the simple present, the simple past, the simple future, and the past participle as an adjective. The present progressive (for example, "is running", "are deploying", "was processing") is not on that list. Because the "-ing" form appears inside the progressive tense, you must not use it to describe an action. Replace the progressive with the simple present or simple past, and break a long continuous clause into short separate sentences.

The "-ing" form also tends to hide complex verb constructions with auxiliary verbs, which Rule 3.4 forbids. A clause such as "the service is starting and then it is logging the request" stacks two progressive auxiliaries and is not approved; write "The service starts. Then it logs the request" instead.

### Approved "-ing" technical nouns (section and document titles)

Use the "-ing" form as a section heading or document title when it names a process, service, or procedure. These are technical nouns, not verbs:

- Logging
- Monitoring
- Testing and Fault Isolation
- Handling
- Packaging
- Shipping
- Troubleshooting
- Building
- Deployment

### Approved "-ing" modifiers (technical-noun adjectives)

Use the "-ing" form as an adjective that names the function of a component, service, tool, or layer. These modifiers stay inside the technical noun they describe:

- logging service
- monitoring agent
- routing table
- switching relay
- caching layer
- building pipeline
- binding configuration
- streaming endpoint
- rendering engine

Do not pull the "-ing" word out of the technical noun and use it as a verb. "The caching layer stores the result" is approved; "The layer is caching the result" is not.

## Examples

> *Adapted from spec pair:* Non-STE: "When you are doing this procedure, obey all the safety precautions."  |  STE: "When you do this procedure, obey all the safety precautions."

> **Non-STE:** When you are running this script, obey all the safety checks.
>
> **STE:** When you run this script, obey all the safety checks.
>
> *Adapted from spec pair: the present progressive "are running" is not approved. Use the simple present tense.*

> **Non-STE:** While the deployment is starting, you must watch the logs and you must not stop the process because stopping it during startup can corrupt the state file.
>
> **STE:** The deployment starts. While it starts, watch the logs. Do not stop the deployment. If you stop the deployment during startup, the state file can become corrupt.
>
> *Adapted from spec pair: the present progressive "is starting" is not approved; the "-ing" verb "stopping" in a dependent clause is not approved. Use the simple present and short separate sentences.*

> **Non-STE:** A script opening a socket without checking the firewall rules and sending data to an unknown host, using an unverified certificate without reading the security policy, is in danger of causing a breach and thus exposing private keys and credentials.
>
> **STE:** Before you open a socket, obey these precautions: (1) Read the security policy. (2) Make sure that the firewall rules allow the connection. (3) Verify the host certificate. (4) Get the correct credentials to send data to the host. If you do not obey these precautions, a breach of private keys and credentials can occur.
>
> *Adapted from spec pair: the long "-ing" construction becomes a vertical list of short, clear sentences.*

> **Non-STE:** The background worker is processing the queue and it is writing the results to the cache while the main thread is waiting for the response, causing the request to time out and the user to see an error.
>
> **STE:** The background worker processes the queue. It writes the results to the cache. The main thread waits for the response. If the main thread waits too long, the request times out and the user sees an error.
>
> *Adapted from spec pair: three progressive verbs ("is processing", "is writing", "is waiting") and a trailing "-ing" cause clause are not approved. Use the simple present and separate the steps into short sentences.*

> **Non-STE:** Developers committing code without running the test suite and pushing directly to the main branch, ignoring the review policy, risk breaking the build and therefore blocking the release for all team members.
>
> **STE:** Before you commit code, obey these precautions: (1) Run the test suite. (2) Make sure that the tests pass. (3) Open a review before you merge to the main branch. If you do not obey these precautions, you can break the build and block the release for all team members.
>
> *Adapted from spec pair: the long "-ing" subject ("Developers committing... and pushing... ignoring...") becomes a vertical list of short, clear steps.*

> **Non-STE:** Be careful while the process is starting.
>
> **STE:** Be careful while the process starts.
>
> *Adapted from spec pair: "Be careful while the door is opening." The progressive form "is starting" is not approved.*

> **Non-STE:** The function is returning the value while the cache is loading the entry, which makes the result incorrect during the first request.
>
> **STE:** The function returns the value. The cache loads the entry. During the first request, the result is incorrect.
>
> *Adapted from spec pair: the progressive verbs "is returning" and "is loading" and the "-ing" cause clause "which makes" are not approved. Use the simple present and short separate sentences.*

> **STE:** Logging, Testing and Fault Isolation, Handling, Package, Shipping, Troubleshooting
>
> *Adapted from spec pair: approved "-ing" technical nouns used as procedural titles or headings.*

> **STE:** Logging service, monitoring agent, routing table, switching relay, caching layer
>
> *Adapted from spec pair: the "-ing" form used as a modifier in a technical noun (related to the function of a component or service).*

> **Non-STE:** The matching algorithm is comparing the remaining items during the iteration and it is removing the missing records from the list.
>
> **STE:** The matching algorithm compares the remaining items during the iteration. It removes the missing records from the list.
>
> *Adapted from spec pair: the approved adjectives "matching", "remaining", and "missing" are permitted inside technical nouns, but the progressive verbs "is comparing" and "is removing" are not. Use the simple present.*

> **Non-STE:** Something going wrong during the migration can make the database stay in a broken state.
>
> **STE:** If something goes wrong during the migration, the database can stay in a broken state.
>
> *Adapted from spec pair: the pronoun "something" is an approved "-ing" word but the gerund "going" used as a verb is not approved. Use the simple present "goes".*

> **See also:** Rule 3.2 — Use only these verb forms and tenses of verbs. (The present progressive tense is not approved, which is why the "-ing" verb form is excluded.)
>
> **See also:** Rule 3.4 — Do not use auxiliary verbs to make complex verb constructions. (Progressive "-ing" forms usually hide auxiliary-verb constructions that Rule 3.4 forbids.)
>
> **See also:** Rule 1.5 — You can use words that you can include in a technical noun category. (The "-ing" modifier and technical noun uses in this rule depend on the technical-noun categories.)

---

<!-- a-sec3-rule3.6.md -->

# Rule 3.6 — Use the Active Voice

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.6

> Source: master.md#sec3-rule3.6

## Original Rule

Use the active voice. In descriptive writing, you can use the passive voice only if the agent is unknown.

Technical texts consist of procedural writing and descriptive writing. When you write in STE, always use the active voice. In descriptive writing, the passive voice is permitted only when the agent (the person or thing that does the action) is unknown.

What is active voice?

In the active voice, the subject of the sentence does the action of the sentence ("A" does "B"). Thus, the grammatical subject (A) is also the logical subject (agent).

What is passive voice?

In the passive voice, the subject of the sentence receives the action ("B" is done by "A"). Here, the grammatical subject is B, and the logical subject, or agent, is A.

General examples:

> **Active:** The manufacturer gives the safety procedures.
> **Passive:** The safety procedures are given by the manufacturer.

How do you know if a sentence is in the passive voice?

The best test for the passive voice is to think of the question "by whom or by what?" (the agent). If your text gives you an answer to this question, then the text is in the passive voice. When a sentence contains the preposition "by," it is a good indication that the sentence is in the passive voice. The object of the preposition "by" is then the agent and you can use the agent as the subject of a sentence in the active voice.

But a passive construction does not always contain an agent.

The dimensions are given in the table.

The main gear leg is held in its position.

A sentence in the active voice always has a grammatical subject (the agent), but in the passive sentence in the example below, the agent is unknown (and we do not know the cause of data corruption). In the active sentence, the agent ("transmission") is incorrect ("transmission" is not the cause of data corruption), and the meaning of the sentence is different. Thus, the active sentence becomes technically incorrect.

Example:

> **Passive:** During transmission, the data was corrupted. (Correct, the agent is unknown.)
> **Active:** During transmission, something corrupted the data. (Correct, you do not know the identity of "something," but you can use it as the agent.)
> **Active:** Transmission corrupted the data. (Incorrect, "transmission" is not the correct agent.)

In the example, if you use the word "something" ("a thing that is not determined or specified") as the agent, the active voice will be technically correct.

How do you change a sentence that is in the passive voice to the active voice?

To change a sentence from the passive voice to the active voice, you can use one of these four methods:

Method 1

When the sentence gives the agent (usually the object of the preposition "by"), put the agent at the start of the sentence. Then, use the agent as the subject. The subject must always be the noun that does the action in the sentence.

> **Non-STE:** The circuits are connected by a switching relay. (Passive)
>
> **STE:** A switching relay connects the circuits. (Active)

Method 2

Change an infinitive verb to an active verb.

> **STE:** The computer calculates the energy consumption from these values. (Active)

Method 3

In procedural writing, change the verb to the imperative ("command") form.

Method 4

When the agent (the person or thing that does the action) is not given in the sentence, you can use the pronouns "you" or "we" as subjects in the active form. If the agent is the reader, use "you." If the agent is your company, or organization, use "we."

Examples:

> **Non-STE:** On the ground, the valve can be opened with the override handle. (Passive)
>
> **STE:** On the ground, you can open the valve with the override handle. (Active)

When you find complex sentences in the passive voice that include auxiliary verbs, decide if you want to write a procedural sentence or a descriptive sentence.

> **STE:** This type of fuel does not contain additives. (Descriptive sentence)

## STE-Code Adaptation

Use the active voice in all code documentation. In descriptive writing, the passive voice is permitted only when the agent (the person, service, or component that does the action) is unknown.

In the active voice, the subject of the sentence does the action. This makes code documentation clearer because the reader immediately knows who or what performs the operation.

To test if a sentence is in the passive voice, ask "by whom or by what?" (the agent). If the sentence answers this question, it is passive. Convert it to active by using the agent as the subject.

To change a sentence from the passive voice to the active voice, use one of these four methods:

**Method 1:** When the preposition "by" identifies the agent, move the agent to the subject position:

> **Non-STE:** The API response is parsed by the middleware. (Passive)
>
> **STE:** The middleware parses the API response. (Active)
>
> *Adapted from spec pair: "The circuits are connected by a switching relay." / "A switching relay connects the circuits."*

Realistic context — a README section that documents an HTTP request pipeline:

> **Non-STE:**
> ```markdown
> ## How the request pipeline works
>
> After the client sends a request, the raw HTTP body is read by the server.
> The API response is parsed by the middleware. The parsed data is then
> validated by the schema checker before the controller receives it.
> ```
>
> **STE:**
> ```markdown
> ## How the request pipeline works
>
> After the client sends a request, the server reads the raw HTTP body.
> The middleware parses the API response. The schema checker then validates
> the parsed data before the controller receives it.
> ```

**Method 2:** Change an infinitive verb to an active verb:

> **STE:** The profiler calculates the memory usage from these values. (Active)
>
> *Adapted from spec pair: "The computer calculates the energy consumption from these values."*

Realistic context — a docstring for a profiling helper:

> **Non-STE:**
> ```python
> def report_memory(samples):
>     """To calculate the memory usage from these values. The peak is
>     returned as a percentage of the allocated heap."""
> ```
>
> **STE:**
> ```python
> def report_memory(samples):
>     """Calculate the memory usage from these values. Return the peak
>     as a percentage of the allocated heap."""
> ```

**Method 3:** In procedural writing, change the verb to the imperative ("command") form:

> **Non-STE:** The dependencies can be installed with the following command. (Passive)
>
> **STE:** Install the dependencies with this command: npm install (Active, imperative)
>
> *Adapted from original Method 3 principle — imperative ("command") form*

Realistic context — a contributing guide:

> **Non-STE:**
> ```markdown
> ## Setup
>
> The dependencies can be installed with the following command. The test
> suite can then be run from the same directory.
> ```
>
> **STE:**
> ```markdown
> ## Setup
>
> Install the dependencies with this command:
>
>     npm install
>
> Then run the test suite from the same directory:
>
>     npm test
> ```

**Method 4:** When the agent is not given in the sentence, use the pronouns "you" or "we" as subjects in the active form. If the agent is the reader, use "you." If the agent is your organization, use "we."

> **Non-STE:** The configuration file can be edited with a text editor. (Passive)
>
> **STE:** You can edit the configuration file with a text editor. (Active)
>
> *Adapted from spec pair: "On the ground, the valve can be opened with the override handle." / "On the ground, you can open the valve with the override handle."*

Realistic context — a getting-started page:

> **Non-STE:**
> ```markdown
> ## First run
>
> The configuration file can be edited with a text editor. The server
> can be started after you save your changes.
> ```
>
> **STE:**
> ```markdown
> ## First run
>
> You can edit the configuration file with a text editor. After you save
> your changes, you can start the server.
> ```

When the agent is unknown and you cannot identify it:

> **Passive:** During the network request, the data was corrupted. (Correct, the agent is unknown.)
> **Active:** During the network request, something corrupted the data. (Correct, you do not know the identity of "something.")
> **Active:** The network request corrupted the data. (Incorrect, "network request" is not the correct agent.)
>
> *Adapted from spec pair: "During transmission, the data was corrupted." / "During transmission, something corrupted the data." / "Transmission corrupted the data."*

Realistic context — an error report from a flaky integration test:

> **Passive (correct):**
> ```text
> During the network request, the payload was corrupted before the checksum
> was computed. The agent is unknown because the failure occurs only under
> heavy load and leaves no stack trace.
> ```
>
> **Active (incorrect):**
> ```text
> During the network request, the socket corrupted the payload.
> ```
> "socket" is not the true cause — the active sentence becomes technically
> wrong and misleads the reader about where to fix the bug.

### Examples

> *Adapted from spec pair: Non-STE: "The circuits are connected by a switching relay."  |  STE: "A switching relay connects the circuits." (Method 1) — and Non-STE: "On the ground, the valve can be opened with the override handle."  |  STE: "On the ground, you can open the valve with the override handle." (Method 4)*

> **Non-STE:** The database connection is established by the connection pool at startup.
>
> **STE:** The connection pool establishes the database connection at startup.
>
> *Adapted from spec pair: "The circuits are connected by a switching relay." / "A switching relay connects the circuits." (Method 1)*

Realistic context — an architecture overview for a backend service:

> **Non-STE:**
> ```markdown
> ## Startup sequence
>
> The configuration is loaded by the bootstrap routine. The database
> connection is established by the connection pool at startup. The cache
> is warmed by a background worker before the first request is served.
> ```
>
> **STE:**
> ```markdown
> ## Startup sequence
>
> The bootstrap routine loads the configuration. The connection pool
> establishes the database connection at startup. A background worker
> warms the cache before it serves the first request.
> ```

> **Non-STE:** The test results can be viewed in the terminal output.
>
> **STE:** You can see the test results in the terminal output.
>
> *Adapted from spec pair: "On the ground, the valve can be opened with the override handle." / "On the ground, you can open the valve with the override handle." (Method 4)*

Realistic context — a CI job summary in a pull-request template:

> **Non-STE:**
> ```markdown
> ## Checks
>
> The linting errors are reported by the linter. The test results can be
> viewed in the terminal output. The coverage report is generated by the
> coverage tool.
> ```
>
> **STE:**
> ```markdown
> ## Checks
>
> The linter reports the linting errors. You can see the test results in
> the terminal output. The coverage tool generates the coverage report.
> ```

## Code-Domain Explanation

This rule has different effects on each type of code documentation. The following sections explain the effects in detail.

### README Files

README files contain a mix of procedural instructions (installation, build, usage) and descriptive text (project overview, feature list, architecture summary). Both sections benefit from the active voice.

In procedural sections, use the imperative mood with "you" as the implied subject. The reader is the agent who performs the action. Passive voice in a procedural section hides the agent and makes the instruction less clear.

> **Non-STE:** The package can be installed with pip install. (Passive — who does the installation?)
>
> **STE:** Install the package with this command: pip install . (Active imperative — the reader is the agent.)

Realistic context — the install section of a Python library README:

> **Non-STE:**
> ```markdown
> ## Installation
>
> The package can be installed with `pip install`. A virtual environment
> should be created before the install is done.
> ```
>
> **STE:**
> ```markdown
> ## Installation
>
> Install the package with this command:
>
>     pip install .
>
> Create a virtual environment before you install the package.
> ```

In descriptive sections, use the active voice with the project, library, or tool as the subject. The passive voice in a descriptive section makes the project seem like a passive object instead of an active system.

> **Non-STE:** Support for WebSocket connections is provided by this library. (Passive)
>
> **STE:** This library supports WebSocket connections. (Active — the library is the agent.)

Realistic context — the feature list of a networking library README:

> **Non-STE:**
> ```markdown
> ## Features
>
> Support for WebSocket connections is provided by this library. Automatic
> reconnection is handled by the transport layer. Message compression is
> applied by the codec before each frame is sent.
> ```
>
> **STE:**
> ```markdown
> ## Features
>
> This library supports WebSocket connections. The transport layer handles
> automatic reconnection. The codec compresses each message before it sends
> the frame.
> ```

### API Documentation

API reference documentation describes what each method, function, or endpoint does. The active voice convention is well-established in API documentation. Use the method or function as the grammatical subject.

> **Non-STE:** The input string is validated and a boolean is returned by this method. (Passive)
>
> **STE:** This method validates the input string and returns a boolean. (Active)

Realistic context — a JSDoc block for an email validator:

> **Non-STE:**
> ```javascript
> /**
>  * Checks a user-supplied address.
>  * The input string is validated and a boolean is returned by this method.
>  * @param {string} address - the address to check
>  * @returns {boolean} true when the address is well formed
>  */
> ```
>
> **STE:**
> ```javascript
> /**
>  * Check a user-supplied address.
>  * This method validates the input string and returns a boolean.
>  * @param {string} address - the address to check
>  * @returns {boolean} true when the address is well formed
>  */
> ```

When you document a callback parameter, the callback is the agent that performs the action. Use the callback as the subject.

> **Non-STE:** The URL is transformed by the callback before the request is sent. (Passive)
>
> **STE:** The callback transforms the URL. Then the client sends the request. (Active)

Realistic context — an OpenAPI parameter description:

> **Non-STE:**
> ```yaml
> parameters:
>   - name: onRequest
>     description: >
>       A function that runs before the call. The URL is transformed by the
>       callback before the request is sent to the upstream service.
> ```
>
> **STE:**
> ```yaml
> parameters:
>   - name: onRequest
>     description: >
>       A function that runs before the call. The callback transforms the
>       URL. Then the client sends the request to the upstream service.
> ```

When you document a return value, use the method as the subject in the active voice. Do not use a passive construction that makes the return value the subject.

> **Non-STE:** A `Promise<User>` is returned by this function. (Passive)
>
> **STE:** This function returns a `Promise<User>`. (Active)

Realistic context — a TypeScript function signature comment:

> **Non-STE:**
> ```typescript
> /**
>  * Fetches the current user. A `Promise<User>` is returned by this function.
>  * The user record is read from the session store while the promise is pending.
>  */
> function getCurrentUser(): Promise<User>
> ```
>
> **STE:**
> ```typescript
> /**
>  * Fetch the current user. This function returns a `Promise<User>`.
>  * While the promise is pending, the function reads the user record from
>  * the session store.
>  */
> function getCurrentUser(): Promise<User>
> ```

### Docstrings and Inline Comments

Docstrings describe the purpose, parameters, return value, and behavior of a function or class. The summary line (first line) follows the imperative convention. The body uses the active voice with the function as the subject.

> **Non-STE:** """A hash of the input data is computed and then it is returned as a hex string."""
>
> **STE:** """Compute the hash of the input data. Return the result as a hex string."""

Realistic context — a Python hashing utility:

> **Non-STE:**
> ```python
> def sha256_hex(data: bytes) -> str:
>     """A hash of the input data is computed and then it is returned as a
>     hex string. The digest is calculated by the hashlib module."""
> ```
>
> **STE:**
> ```python
> def sha256_hex(data: bytes) -> str:
>     """Compute the hash of the input data. Return the result as a hex
>     string. The hashlib module calculates the digest."""
> ```

Inline comments explain a specific line or block of code. Use the active voice with the code entity or the developer as the subject. Passive voice in an inline comment can make the responsibility for an action unclear.

> **Non-STE:** // The buffer is flushed before new data is written.
>
> **STE:** // Flush the buffer before you write new data.

> **Non-STE:** // The connection is closed by the finally block.
>
> **STE:** // The finally block closes the connection.

Realistic context — a Go function that writes a record:

> **Non-STE:**
> ```go
> func (w *Writer) Write(rec Record) error {
>     // The buffer is flushed before new data is written.
>     if err := w.buf.Flush(); err != nil {
>         return err
>     }
>     // The connection is closed by the finally block.
>     defer w.conn.Close()
>     return w.conn.Send(rec)
> }
> ```
>
> **STE:**
> ```go
> func (w *Writer) Write(rec Record) error {
>     // Flush the buffer before you write new data.
>     if err := w.buf.Flush(); err != nil {
>         return err
>     }
>     // The finally block closes the connection.
>     defer w.conn.Close()
>     return w.conn.Send(rec)
> }
> ```

### Commit Messages

Commit messages follow the imperative mood convention, which is inherently active voice. The commit message describes what the commit does when applied to the codebase. Passive voice in a commit message breaks this convention and makes the message less direct.

> **Non-STE:** The authentication bug was fixed. (Passive — who fixed it? what did the commit do?)
>
> **STE:** Fix the authentication bug. (Active imperative — the commit is the agent.)

> **Non-STE:** Rate limiting was added to the API endpoints. (Passive)
>
> **STE:** Add rate limiting to the API endpoints. (Active imperative)

Realistic context — two commits in a feature branch:

> **Non-STE:**
> ```text
> git log --oneline
> a1b2c3d The authentication bug was fixed.
> e4f5g6h Rate limiting was added to the API endpoints.
> ```
>
> **STE:**
> ```text
> git log --oneline
> a1b2c3d Fix the authentication bug.
> e4f5g6h Add rate limiting to the API endpoints.
> ```

NOTE: Some projects use changelog auto-generation tools that extract commit messages. If the tool wraps commit messages in passive sentences (for example, "A fix was made for the authentication bug"), the generated changelog is not subject to this rule. The rule applies to the commit messages you write, not to the changelog the tool generates.

### Error Messages and Log Output

Error messages describe what went wrong and, when possible, what action to take. Active voice in an error message helps the user identify the component that detected the error.

> **Non-STE:** An invalid configuration value was encountered while the file was being parsed. (Passive — what encountered it? what was parsing?)
>
> **STE:** The parser found an invalid configuration value in the file. (Active — the parser is the agent.)

> **Non-STE:** The request was rejected by the rate limiter. (Passive)
>
> **STE:** The rate limiter rejected the request. (Active)

Realistic context — log lines from a config loader and an API gateway:

> **Non-STE:**
> ```text
> [warn]  An invalid configuration value was encountered while the file was
>         being parsed.
> [error] The request was rejected by the rate limiter.
> ```
>
> **STE:**
> ```text
> [warn]  The parser found an invalid configuration value in the file.
> [error] The rate limiter rejected the request.
> ```

When the agent is truly unknown (for example, a network timeout with no identifiable cause), the passive voice is correct. This is the exception defined in the original rule.

> **Correct:** The connection was reset. (The agent is unknown — no process or component can be identified as the cause.)

Realistic context — a raw socket error with no local cause:

> **Correct (passive):**
> ```text
> [error] The connection was reset. The peer closed the TCP session without
>         sending a FIN or RST that our client could observe.
> ```

## Paradigm-Specific Guidance

### Object-Oriented Paradigm (Java, C++, C#, Python Classes)

In object-oriented documentation, classes, methods, and design patterns are the agents of their documented behavior. Use the class or method as the grammatical subject in the active voice.

> **Non-STE:** The dependency is resolved by the container at runtime. (Passive)
>
> **STE:** The container resolves the dependency at runtime. (Active)

Realistic context — a Spring-style DI container description:

> **Non-STE:**
> ```markdown
> ## Dependency resolution
>
> The dependency is resolved by the container at runtime. The bean is
> created after all its prerequisites are satisfied by the registrar.
> ```
>
> **STE:**
> ```markdown
> ## Dependency resolution
>
> The container resolves the dependency at runtime. After the registrar
> satisfies all prerequisites, the container creates the bean.
> ```

When you document a design pattern, the pattern's components have clear agency. The factory creates objects. The observer receives notifications. The decorator wraps behavior. Use these components as subjects.

> **Non-STE:** New instances are created by the factory method when they are requested by the client. (Passive)
>
> **STE:** The factory method creates a new instance when the client requests one. (Active)

Realistic context — a factory pattern docstring:

> **Non-STE:**
> ```python
> class ConnectionFactory:
>     """New instances are created by the factory method when they are
>     requested by the client. The pool is checked before a connection
>     is made."""
> ```
>
> **STE:**
> ```python
> class ConnectionFactory:
>     """Create a new instance with the factory method when the client
>     requests one. The factory method checks the pool before it makes a
>     connection."""
> ```

When you document an abstract class or interface contract, use the implementing class as the grammatical subject. Passive voice in a contract description makes the obligation unclear.

> **Non-STE:** The `validate()` method is called before the data is processed by the handler. (Passive)
>
> **STE:** The handler calls the `validate()` method before it processes the data. (Active)

Realistic context — an interface contract in a Java service:

> **Non-STE:**
> ```java
> /**
>  * The validate() method is called before the data is processed by the
>  * handler. A ValidationException is thrown when the record is rejected.
>  */
> interface RequestHandler { void handle(Request req); }
> ```
>
> **STE:**
> ```java
> /**
>  * The handler calls the validate() method before it processes the data.
>  * The handler throws a ValidationException when it rejects the record.
>  */
> interface RequestHandler { void handle(Request req); }
> ```

### Functional Paradigm (Haskell, Elixir, Clojure, Rust)

Functional code documentation describes pure functions, data transformations, and pipelines. Functions are the agents in functional documentation. Use the function name as the grammatical subject.

> **Non-STE:** Each element in the list is transformed by the `map` function. (Passive)
>
> **STE:** The `map` function transforms each element in the list. (Active)

Realistic context — a Haskell list pipeline comment:

> **Non-STE:**
> ```haskell
> -- Each element in the list is transformed by the map function. The result
> -- is then filtered and the sum is computed by foldl.
> total = foldl (+) 0 . filter (>0) . map (*2) $ xs
> ```
>
> **STE:**
> ```haskell
> -- The map function transforms each element in the list. The filter function
> -- keeps the positive values. Then foldl computes the sum.
> total = foldl (+) 0 . filter (>0) . map (*2) $ xs
> ```

When you document a pipeline of composed functions, break the pipeline into active sentences. Each sentence names the function that performs an action.

> **Non-STE:** The input is filtered, then mapped, and finally the result is reduced to a single value. (Passive)
>
> **STE:** The `filter` function removes invalid items. The `map` function transforms each item. The `reduce` function combines the results into a single value. (Active)

Realistic context — a Clojure threading macro doc:

> **Non-STE:**
> ```clojure
> ;; The input is filtered, then mapped, and finally the result is reduced to
> ;; a single value by the reduce step.
> (->> items (filter valid?) (map enrich) (reduce merge {}))
> ```
>
> **STE:**
> ```clojure
> ;; The filter function removes invalid items. The map function transforms
> ;; each item. The reduce function combines the results into a single map.
> (->> items (filter valid?) (map enrich) (reduce merge {}))
> ```

When you document higher-order functions or combinators, use the combinator as the grammatical subject.

> **Non-STE:** Two functions are composed into a new function by the `compose` combinator. (Passive)
>
> **STE:** The `compose` combinator combines two functions into a new function. (Active)

Realistic context — a Rust combinator doc:

> **Non-STE:**
> ```rust
> /// Two functions are composed into a new function by the compose
> /// combinator. The result is cached by the memoize wrapper.
> fn compose<A, B, C>(f: fn(B) -> C, g: fn(A) -> B) -> impl Fn(A) -> C
> ```
>
> **STE:**
> ```rust
> /// The compose combinator combines two functions into a new function.
> /// The memoize wrapper caches the result.
> fn compose<A, B, C>(f: fn(B) -> C, g: fn(A) -> B) -> impl Fn(A) -> C
> ```

### Procedural Paradigm (C, Go, Bash)

Procedural documentation contains step-by-step instructions and descriptions of sequential execution. Each step has a clear agent: the program, the function, or the developer. Use the agent as the subject.

> **Non-STE:** The file is opened, the contents are read, and the connection is closed. (Passive — who does each step?)
>
> **STE:** The script opens the file. It reads the contents. Then it closes the connection. (Active)

Realistic context — a backup shell script header:

> **Non-STE:**
> ```bash
> # The file is opened, the contents are read, and the connection is closed
> # by the dump routine. The archive is written to /var/backups.
> pg_dump app > /var/backups/app.sql
> ```
>
> **STE:**
> ```bash
> # The script opens the file, reads the contents, and closes the connection.
> # Then it writes the archive to /var/backups.
> pg_dump app > /var/backups/app.sql
> ```

When you document a shell script or command-line tool, use the script or tool as the subject in descriptive text and the imperative mood in procedural text.

> **Non-STE:** Environment variables are checked before the build process is started. (Passive)
>
> **STE:** The script checks the environment variables. Then it starts the build process. (Active)

> **Non-STE:** The log file can be rotated with the --rotate flag. (Passive)
>
> **STE:** Use the --rotate flag to rotate the log file. (Active imperative)

Realistic context — a Makefile help target:

> **Non-STE:**
> ```makefile
> # Environment variables are checked before the build process is started.
> # The log file can be rotated with the --rotate flag.
> build:
> 	./configure && $(MAKE)
> ```
>
> **STE:**
> ```makefile
> # The script checks the environment variables. Then it starts the build.
> # Use the --rotate flag to rotate the log file.
> build:
> 	./configure && $(MAKE)
> ```

### Declarative Paradigm (SQL, Terraform, Kubernetes YAML, Dockerfile)

Declarative documentation describes the desired state that a system moves toward. The active voice names the tool or engine that applies the declaration. The declaration itself does not act — the tool that reads the declaration acts.

> **Non-STE:** An AWS VPC with three subnets is provisioned by this Terraform module. (Passive)
>
> **STE:** This Terraform module provisions an AWS VPC with three subnets. (Active)

Realistic context — a Terraform module README:

> **Non-STE:**
> ```markdown
> ## What this module builds
>
> An AWS VPC with three subnets is provisioned by this Terraform module.
> A NAT gateway is attached to the private subnet by the same module.
> ```
>
> **STE:**
> ```markdown
> ## What this module builds
>
> This Terraform module provisions an AWS VPC with three subnets. The same
> module attaches a NAT gateway to the private subnet.
> ```

When you document a SQL query, the database engine is the agent. Use the query or the engine as the subject.

> **Non-STE:** All rows with a status of 'active' are selected by this query. (Passive)
>
> **STE:** This query selects all rows with a status of 'active'. (Active)

Realistic context — a query comment in a migration file:

> **Non-STE:**
> ```sql
> -- All rows with a status of 'active' are selected by this query. The
> -- matching accounts are then counted by the aggregate.
> SELECT count(*) FROM accounts WHERE status = 'active';
> ```
>
> **STE:**
> ```sql
> -- This query selects all rows with a status of 'active'. The aggregate
> -- then counts the matching accounts.
> SELECT count(*) FROM accounts WHERE status = 'active';
> ```

When you document a Kubernetes manifest, the Kubernetes controller is the agent. Use the controller or the resource as the subject.

> **Non-STE:** Three replicas of the pod are maintained by the deployment controller. (Passive)
>
> **STE:** The deployment controller maintains three replicas of the pod. (Active)

Realistic context — a Deployment manifest description:

> **Non-STE:**
> ```markdown
> ## Scaling
>
> Three replicas of the pod are maintained by the deployment controller. The
> rollout is paused by the operator during a canary release.
> ```
>
> **STE:**
> ```markdown
> ## Scaling
>
> The deployment controller maintains three replicas of the pod. During a
> canary release, the operator pauses the rollout.
> ```

NOTE: YAML comments and Dockerfile comments are procedural by nature. Use the imperative mood and active voice in these comments because they instruct the reader or the build engine.

> **Non-STE:** # The base image is set to Ubuntu 22.04. (Passive)
>
> **STE:** # Use Ubuntu 22.04 as the base image. (Active imperative)

Realistic context — a Dockerfile preamble:

> **Non-STE:**
> ```dockerfile
> # The base image is set to Ubuntu 22.04. The working directory is created
> # at /app by the build stage.
> FROM ubuntu:22.04
> ```
>
> **STE:**
> ```dockerfile
> # Use Ubuntu 22.04 as the base image. The build stage creates the working
> # directory at /app.
> FROM ubuntu:22.04
> ```

### Systems Programming (Rust Ownership Docs, C Memory Docs)

Systems documentation describes ownership, lifetimes, memory allocation, and concurrency. These topics involve precise relationships between components. Active voice makes the relationship between the agent and the action explicit.

> **Non-STE:** The memory block is allocated by the allocator and a pointer is returned. (Passive)
>
> **STE:** The allocator allocates the memory block. It returns a pointer. (Active)

Realistic context — a C allocator doc:

> **Non-STE:**
> ```c
> /* The memory block is allocated by the allocator and a pointer is returned.
>    The block is zeroed before it is handed to the caller. */
> void *alloc_block(size_t bytes);
> ```
>
> **STE:**
> ```c
> /* The allocator allocates the memory block. It returns a pointer. The
>    allocator zeroes the block before it hands the block to the caller. */
> void *alloc_block(size_t bytes);
> ```

When you document ownership transfer in Rust, the function or scope that takes ownership is the agent. Use it as the subject.

> **Non-STE:** Ownership of the string is taken by the `process` function. (Passive)
>
> **STE:** The `process` function takes ownership of the string. (Active)

Realistic context — a Rust function that consumes a value:

> **Non-STE:**
> ```rust
> /// Ownership of the string is taken by the process function. The buffer
> /// is freed when the function returns.
> fn process(input: String) { /* ... */ }
> ```
>
> **STE:**
> ```rust
> /// The process function takes ownership of the string. The function frees
> /// the buffer when it returns.
> fn process(input: String) { /* ... */ }
> ```

When you document a concurrency primitive, the primitive is the agent. Mutexes lock. Channels send. Atomics store.

> **Non-STE:** Access to the shared state is controlled by the mutex. (Passive)
>
> **STE:** The mutex controls access to the shared state. (Active)

Realistic context — a Rust concurrency comment:

> **Non-STE:**
> ```rust
> // Access to the shared state is controlled by the mutex. The value is sent
> // to the worker by the channel.
> let guard = state.lock().unwrap();
> tx.send(guard.clone());
> ```
>
> **STE:**
> ```rust
> // The mutex controls access to the shared state. The channel sends the
> // value to the worker.
> let guard = state.lock().unwrap();
> tx.send(guard.clone());
> ```

## Extended Examples

### Example 1 — README Feature Description

> **Non-STE:** Authentication via OAuth2 and JWT tokens is supported by this service. Rate limiting is applied to all endpoints. Requests are logged to a centralized logging system.
>
> **STE:** This service supports authentication with OAuth2 and JWT tokens. It applies rate limiting to all endpoints. It sends request logs to a centralized logging system.
>
> **Principle applied:** P14 — Use American English spelling. P8 — Use standard, well-known technical nouns. Method 1 applied: the agent ("this service") moves to the subject position.
>
> **Explanation:** The original text has three consecutive passive constructions. The reader must work backward to find the agent. The STE version establishes "this service" as the agent once, then uses active verbs for each feature.

Realistic context — the full feature section of a gateway service README:

> **Non-STE:**
> ```markdown
> ## What this service does
>
> Authentication via OAuth2 and JWT tokens is supported by this service.
> Rate limiting is applied to all endpoints. Requests are logged to a
> centralized logging system. Health checks are exposed on port 8080.
> ```
>
> **STE:**
> ```markdown
> ## What this service does
>
> This service supports authentication with OAuth2 and JWT tokens. It applies
> rate limiting to all endpoints. It sends request logs to a centralized
> logging system. It exposes health checks on port 8080.
> ```

### Example 2 — API Method Documentation

> **Non-STE:** `createUser(payload)` — A new user is created with the provided payload. The payload is validated before the user record is inserted into the database. A `User` object is returned upon success.
>
> **STE:** `createUser(payload)` — Create a new user with the provided payload. The method validates the payload. Then it inserts the user record into the database. It returns a `User` object on success.
>
> **Principle applied:** P2 — Use words only as their specified part of speech. P4 — Use only approved verb forms. The passive constructions are replaced with active imperatives and indicative verbs.
>
> **Explanation:** The original text uses three passive constructions in a row. The reader does not know if "is validated" means the method does it, the database does it, or the caller must do it. The STE version names the method as the agent and uses active verbs.

Realistic context — the full JSDoc for the endpoint handler:

> **Non-STE:**
> ```javascript
> /**
>  * POST /users
>  * createUser(payload) — A new user is created with the provided payload.
>  * The payload is validated before the user record is inserted into the
>  * database. A User object is returned upon success.
>  */
> ```
>
> **STE:**
> ```javascript
> /**
>  * POST /users
>  * createUser(payload) — Create a new user with the provided payload. The
>  * method validates the payload. Then it inserts the user record into the
>  * database. It returns a User object on success.
>  */
> ```

### Example 3 — Docstring for a Class

> **Non-STE:** """A pool of database connections is managed by this class. Connections are borrowed when a request is received and they are returned when the request is complete."""
>
> **STE:** """Manage a pool of database connections. The class lends a connection when a request arrives. It returns the connection when the request is complete."""
>
> **Principle applied:** P1 — Use approved words. "Borrowed" and "received" are replaced with approved alternatives ("lends," "arrives"). Method 3 and Method 4 are applied.
>
> **Explanation:** The original docstring uses passive voice throughout. The reader cannot tell if the class manages the pool automatically or if the caller must manage it. The STE version uses imperatives and active voice to clarify the class's responsibility.

Realistic context — the full Python class docstring and a usage note:

> **Non-STE:**
> ```python
> class ConnectionPool:
>     """A pool of database connections is managed by this class. Connections
>     are borrowed when a request is received and they are returned when the
>     request is complete. Idle connections are closed by the reaper thread."""
> ```
>
> **STE:**
> ```python
> class ConnectionPool:
>     """Manage a pool of database connections. The class lends a connection
>     when a request arrives. It returns the connection when the request is
>     complete. The reaper thread closes idle connections."""
> ```

### Example 4 — Commit Message

> **Non-STE:** The memory leak in the image processing pipeline was fixed. Redundant allocations were removed and the buffer pool was refactored.
>
> **STE:** Fix the memory leak in the image processing pipeline. Remove redundant allocations. Refactor the buffer pool.
>
> **Principle applied:** P4 — Use only approved verb forms. P9 — Prefer short, clear technical nouns. Method 3 (imperative) applied throughout.
>
> **Explanation:** The original commit message uses three passive constructions. The STE version uses three imperative verbs. Each verb describes one change. The reader immediately knows what the commit does.

Realistic context — the commit shown in `git show`:

> **Non-STE:**
> ```text
> commit 9f2c1ab
> Author:Dev <dev@example.com>
>
>     The memory leak in the image processing pipeline was fixed. Redundant
>     allocations were removed and the buffer pool was refactored.
> ```
>
> **STE:**
> ```text
> commit 9f2c1ab
> Author:Dev <dev@example.com>
>
>     Fix the memory leak in the image processing pipeline. Remove redundant
>     allocations. Refactor the buffer pool.
> ```

### Example 5 — Error Message

> **Non-STE:** Error: A malformed token was encountered during request validation. The request was rejected.
>
> **STE:** Error: The token validator found a malformed token. The server rejected the request.
>
> **Principle applied:** P8 — Use standard, well-known technical nouns. Method 1 applied: the agent ("token validator") moves to subject position.
>
> **Explanation:** The original error message uses passive voice. The user does not know which component detected the error. The STE version names two agents: the token validator (which found the problem) and the server (which rejected the request).

Realistic context — the structured log entry for a failed request:

> **Non-STE:**
> ```json
> {
>   "level": "error",
>   "msg": "A malformed token was encountered during request validation. The request was rejected."
> }
> ```
>
> **STE:**
> ```json
> {
>   "level": "error",
>   "msg": "The token validator found a malformed token. The server rejected the request."
> }
> ```

### Example 6 — Configuration File Comment

> **Non-STE:** # The maximum number of concurrent connections is controlled by this setting. Requests beyond this limit are queued.
>
> **STE:** # This setting controls the maximum number of concurrent connections. The server queues requests beyond this limit.
>
> **Principle applied:** P11 — One term per concept. Method 1 applied: the agent ("this setting") moves to subject position. The second sentence adds a clear agent ("the server").
>
> **Explanation:** Configuration comments describe static behavior. Passive voice in a configuration comment can make the relationship between the setting and the behavior unclear. Active voice names the setting as the agent that controls the behavior.

Realistic context — the config block in a TOML file:

> **Non-STE:**
> ```toml
> # The maximum number of concurrent connections is controlled by this
> # setting. Requests beyond this limit are queued.
> max_connections = 100
> ```
>
> **STE:**
> ```toml
> # This setting controls the maximum number of concurrent connections.
> # The server queues requests beyond this limit.
> max_connections = 100
> ```

## Edge Cases

### Edge Case 1 — Unknown Agent (Standard Exception)

When the agent that performed an action is genuinely unknown, the passive voice is correct. This is the standard exception defined by the original ASD-STE100 rule. In code documentation, this applies to:

- Unexpected data corruption with no identifiable cause
- External network failures where the remote endpoint is unknown
- Hardware faults that manifest as software errors
- Race conditions where the exact sequence of events is not reproducible

> **Correct (passive):** The data was corrupted before the checksum was computed.
> **Incorrect (active):** Something corrupted the data before the checksum was computed. (Too vague — "something" adds no information.)

Realistic context — a crash report from a corrupted write:

> **Correct (passive):**
> ```text
> [fatal] The data was corrupted before the checksum was computed. The write
> completed without an error from the storage driver, so no component on our
> side can be named as the cause.
> ```
> **Incorrect (active):**
> ```text
> [fatal] Something corrupted the data before the checksum was computed.
> ```
> "something" adds no information and sends the reader looking for a phantom
> process.

NOTE: Use the word "something" as the agent only when you can describe the type of agent (for example, "some process," "some external service"). If you cannot even describe the type, keep the passive voice.

### Edge Case 2 — Topic-Comment Structure in Descriptive Text

In descriptive writing, a sentence sometimes needs to make the object the topic (the thing the paragraph is about). When the object is the established topic of the paragraph and the agent is irrelevant to the description, the passive voice can be clearer than the active voice.

> **Active (awkward):** The developer stores the configuration file in the `/etc/myapp` directory.
> **Passive (acceptable):** The configuration file is stored in the `/etc/myapp` directory.

In this pair, the configuration file is the topic of the documentation section. The developer is not relevant to the description. The passive voice keeps the topic consistent.

However, if the documentation section describes the developer's responsibilities, use the active voice with "you" as the subject.

> **Correct:** You must store the configuration file in the `/etc/myapp` directory.

Realistic context — a config reference table where the file is the topic:

> **Topic-comment (acceptable passive):**
> ```markdown
> ## Configuration files
>
> The configuration file is stored in the `/etc/myapp` directory. The
> environment file is stored in the same directory. The session file is
> written next to them at runtime.
> ```
> **Developer-responsibility (active):**
> ```markdown
> ## Before you deploy
>
> You must store the configuration file in the `/etc/myapp` directory. You
> must also copy the environment file to the same directory.
> ```

**Decision rule:** If the paragraph topic is the object (the thing acted upon) and changing to active voice would introduce an agent that distracts from the topic, use the passive voice. If the paragraph topic is the agent, use the active voice.

### Edge Case 3 — Academic or RFC-Style References in Code Documentation

Some code documentation includes references to academic papers, RFCs, or formal specifications. These external documents often use passive voice as a convention. When you quote or paraphrase an external document, you may keep the passive voice and add a NOTE that identifies the non-STE source.

> NOTE: The following description quotes RFC 7230. The passive voice in the quotation is from the original RFC text.
>
> > "The request message is parsed by the server into its component parts."

Do not rewrite the quotation. The rule applies only to the documentation text that you write.

Realistic context — a proxy server doc that quotes the RFC:

> **Your prose (STE):**
> ```markdown
> Our proxy reads the request line first. The server parses the headers after
> it reads the body.
> ```
> **Quoted RFC (unchanged passive):**
> ```markdown
> NOTE: The following description quotes RFC 7230. The passive voice in the
> quotation is from the original RFC text.
>
> > "The request message is parsed by the server into its component parts."
> ```

### Edge Case 4 — Framework-Generated Documentation

Some frameworks and tools generate API documentation automatically from code annotations, type definitions, or schema files (for example, OpenAPI/Swagger, JSDoc templates, Sphinx autodoc summaries). These generators sometimes produce passive voice constructions.

If you control the generator template (for example, a Sphinx theme or a JSDoc template), configure it to use active voice. If you do not control the generator output, add a NOTE at the top of the generated documentation.

> NOTE: This document was generated by [tool name]. Some sentences use the passive voice. Refer to the source code comments for STE-Code compliant descriptions.

Realistic context — a generated OpenAPI page:

> **Generated doc (passive, not yours to fix):**
> ```markdown
> NOTE: This document was generated by openapi-generator. Some sentences use
> the passive voice. Refer to the source code comments for STE-Code compliant
> descriptions.
>
> > The user object is returned by the GET /users endpoint.
> ```
> **Your source comment (STE, which the template should copy):**
> ```javascript
> /**
>  * Get the current user. The GET /users endpoint returns the user object.
>  */
> ```

### Edge Case 5 — Passive Voice in Established Error Message Standards

Some operating systems, language runtimes, and standard libraries produce error messages in the passive voice. Examples include POSIX error strings ("Permission denied"), HTTP status reason phrases ("Not Found"), and database error codes.

Do not rewrite error messages from external systems. The rule applies only to error messages that you write in your own application code.

> **Your error message (STE):** The server cannot connect to the database at host:port.
> **System error message (unchanged):** Connection refused.

Realistic context — an application catch block:

> **Your code (STE message you write):**
> ```go
> if err != nil {
>     return fmt.Errorf("the server cannot connect to the database at %s:%s", host, port)
> }
> ```
> **System string (unchanged, from the OS):**
> ```text
> Connection refused
> ```

## Cross-References

This rule interacts with several other STE-Code rules. Obey all related rules when you apply Rule 3.6.

- **Rule 1.1 (Approved Words):** When you convert a passive sentence to active voice, you may need to introduce a new agent as the subject. Make sure the agent is an approved word from the STE-Code dictionary or a permitted technical noun (Rule 1.5). Refer to the Canonical Synonym Table for preferred replacements.
- **Rule 1.5 (Technical Code Nouns):** Technical nouns that name code entities (for example, *middleware*, *validator*, *container*, *allocator*, *mutex*) are permitted as agents in active voice sentences. The agent must be a real code entity, not a vague abstraction.
- **Rule 1.12 (Technical Verbs):** When you write an active voice sentence, the verb is often a technical verb (for example, *parse*, *compile*, *deploy*, *render*, *query*, *allocate*). Use these verbs in their approved simple forms. Do not use them in compound passive constructions.
- **Rule 3.1 (Simple Verb Tenses):** Active voice sentences use the simple present or simple past tense. A passive sentence can hide a compound tense behind the auxiliary verb "be." When you convert to active voice, you also simplify the tense.
- **Rule 3.4 (Auxiliary Verbs):** Passive voice uses the auxiliary verb "be" plus a past participle. Converting a passive sentence to active voice removes the unnecessary auxiliary verb. If the passive construction also uses "have" (for example, "has been parsed"), refer to Rule 3.4 for guidance on removing compound auxiliaries.
- **Rule 3.5 (-ing Forms):** Passive progressive constructions (for example, "is being parsed") combine a passive auxiliary with an "-ing" form. These constructions violate both Rule 3.5 and Rule 3.6. Convert them to active voice first, then check for any remaining "-ing" forms.
- **Rule 3.7 (Sentence Length):** Sentences must not exceed 20 words in procedural text and 25 words in descriptive text. Passive constructions are often longer than their active equivalents. Converting to active voice usually shortens the sentence. If the active sentence is still too long, split it into two or more sentences.

> **See also:** Rule 1.1 — Use approved words (dictionary and Canonical Synonym Table)
> **See also:** Rule 1.5 — Use technical nouns from the code-domain categories
> **See also:** Rule 1.12 — Use approved technical verbs in their simple forms
> **See also:** Rule 3.1 — Use only the simple verb tenses
> **See also:** Rule 3.4 — Use only the approved auxiliary verbs
> **See also:** Rule 3.5 — Use the "-ing" form only as a technical noun or modifier
> **See also:** Rule 3.7 — Write sentences that do not exceed the word limit

## Grammar Notes

### The Linguistic Basis of the Rule

In English grammar, voice is a property of the clause that expresses the relationship between the verb and its arguments. The two voices in English — active and passive — assign different grammatical roles to the same logical participants.

**Active Voice Structure**

```
Subject (Agent) + Verb + Object (Patient)
```

The grammatical subject is the agent (the doer). The grammatical object is the patient (the receiver of the action).

**Passive Voice Structure**

```
Subject (Patient) + be + Past Participle (+ by + Agent)
```

The grammatical subject is the patient. The agent is either placed in an optional "by"-phrase or omitted entirely.

### Why Passive Voice Obscures Agency

In technical documentation, the reader needs to know two things about every action:

1. What action happens
2. Who or what performs the action

Active voice delivers both pieces of information in the natural reading order. Passive voice delivers the action first and the agent last (or not at all). This reversal makes the reader work harder to understand the sentence.

Consider this passive sentence from API documentation:

> *The request is validated by the middleware.*

The reader must:
1. Identify the action ("is validated")
2. Search for the agent in the "by"-phrase ("by the middleware")
3. Mentally reconstruct the active version ("The middleware validates the request")

In the active version, the reader gets the agent and the action in the natural subject-verb-object order.

### The "By" Test

The most reliable test for passive voice is the "by whom or by what?" test. Ask this question after the verb phrase:

> *The data was encrypted...* → by whom? → *by the crypto module.* (Passive detected.)

If the sentence does not contain a "by"-phrase but can accept one without changing the meaning, it is still passive:

> *The file was saved.* → The file was saved *by the application.* (Passive detected, agent omitted.)

If the sentence cannot accept a "by"-phrase with the same meaning, the construction is not passive. It may be a past participle used as an adjective (Rule 3.3) or a copular construction:

> *The file is saved.* (Adjective — describes the state of the file, not a passive action.)

### Common Passive Constructions in Code Documentation

The table below shows passive constructions that are common in code documentation and their active equivalents. Use this table as a quick reference when you edit documentation.

| Passive Construction | Active Equivalent | Conversion Method |
|---|---|---|
| *is returned by* | *returns* | Method 1: move agent to subject |
| *can be used to* | *you can use ... to* | Method 4: insert "you" |
| *is configured by* | *configures* | Method 1: move agent to subject |
| *is called when* | *calls* | Method 1: move agent to subject |
| *was added in version* | *(we) added ... in version* | Method 4: insert "we" |
| *should be installed* | *install* (imperative) | Method 3: imperative form |
| *is designed to* | *(we) designed ... to* | Method 4: insert "we" |
| *has been deprecated* | *(we) deprecated* | Method 4: insert "we" |
| *will be removed in* | *(we) will remove ... in* | Method 4: insert "we" |

### Interaction with Modal Verbs

Passive constructions that include modal verbs (can, must, should, may, will) require a two-step conversion:

1. Identify the agent.
2. Move the agent to the subject position and keep the modal verb.

| Passive with Modal | Active with Modal |
|---|---|
| *The file can be opened with this command.* | *You can open the file with this command.* |
| *The setting must be configured before startup.* | *You must configure the setting before startup.* |
| *The output will be written to stdout.* | *The program will write the output to stdout.* |

When the agent is the reader, use "you" with the modal verb. When the agent is a code component, use the component name with the modal verb.

### Structural Avoidance Patterns

When you edit documentation to convert passive voice to active voice, apply these three structural patterns. Each pattern maps to a specific type of passive construction.

**Pattern A — Agent in "by"-Phrase (Method 1)**

Use this pattern when the sentence contains a "by"-phrase that identifies the agent. Move the agent to the subject position and change the verb to the active form.

| Input Structure | Output Structure |
|---|---|
| *Patient + be + past participle + by + Agent* | *Agent + active verb + Patient* |

> **Input:** The token is validated by the auth middleware.
> **Output:** The auth middleware validates the token.

**Pattern B — No Agent, Procedural Context (Method 3)**

Use this pattern when the sentence is in a procedural section and the agent is the reader. Change the verb to the imperative form.

| Input Structure | Output Structure |
|---|---|
| *Patient + modal + be + past participle* | *Imperative verb + Patient* |

> **Input:** The dependencies should be installed before the build.
> **Output:** Install the dependencies before the build.

**Pattern C — No Agent, Descriptive Context (Method 4)**

Use this pattern when the sentence is in a descriptive section and the agent is the reader or your organization. Insert "you" or "we" as the subject.

| Input Structure | Output Structure |
|---|---|
| *Patient + be + past participle* | *You/We + active verb + Patient* |

> **Input:** The configuration file is stored in the config directory.
> **Output:** You must store the configuration file in the config directory.
> **Alternative:** We store the configuration file in the config directory. (If "we" refers to the project.)

### Interaction with the Canonical Synonym Table

When you convert a passive sentence to active voice, you must also check the replacement verb against the STE-Code Canonical Synonym Table. Many passive constructions contain avoided words that need replacement.

> **Non-STE:** The result is used by the downstream pipeline.
>
> **STE:** The downstream pipeline uses the result.

In this pair, three fixes work together:
1. Convert passive to active (*is used by* → active verb) — Rule 3.6.
2. Replace the avoided word (*used* → *uses*) — Rule 1.1 and Canonical Synonym Table.
3. Apply active voice correctly (*pipeline uses the result*) — Rule 3.6.

> **Non-STE:** The error is displayed on the console by the logger.
>
> **STE:** The logger shows the error on the console.

In this pair, two fixes work together:
1. Convert passive to active (*is displayed by* → *shows*) — Rule 3.6.
2. Replace the avoided word (*display* → *show*) — Rule 1.1 and Canonical Synonym Table.

> **Non-STE:** The report is generated by the scheduler every night.
>
> **STE:** The scheduler makes the report every night.

In this pair, two fixes work together:
1. Convert passive to active (*is generated by* → *makes*) — Rule 3.6 and Method 1.
2. Replace the avoided word (*generated* → *makes*) — Rule 1.1 and Canonical Synonym Table (approved verb: *make* replaces *generate*).

---

<!-- a-sec3-rule3.7.md -->

# Rule 3.7 — Use an approved verb to describe an action, not a noun or other parts of speech.

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.7
> **Source file:** master.md#sec3-rule3.7

## Original Rule

There can be different solutions to give the same information in STE. If there is an approved verb that describes an action, use the approved verb. Verbs describe actions more clearly than nouns or other parts of speech.

> **Non-STE:** Do not write: The ohmmeter gives an indication of 450 ohms.
> **STE:** WRITE: The ohmmeter shows 450 ohms.
> **Non-STE:** Do not write: Before the removal of the unit, make sure that the power supply is OFF.
> **STE:** WRITE: Before you remove the unit, make sure that the power supply is OFF.

In the examples, all sentences are in STE, but those with direct verbs describe the action more clearly.

If a word is not approved as a verb in the dictionary, do not use it as a verb. Use a different sentence construction to give the same information.

> **Non-STE:** Check the laptop battery.
> **STE:** Do a check of the laptop battery.

## STE-Code Adaptation

There can be different solutions to give the same information in STE-Code. If there is an approved verb that describes an action, use the approved verb. Verbs describe actions more clearly than nouns or other parts of speech.

The four approved Technical Code Verb categories give you the verbs that you can use to describe an action:

1. **Development operations** — build, compile, test, lint, format, commit, push, deploy, rollback
2. **Data operations** — read, write, serialize, deserialize, Parse, Encode, Decode, Query, Insert, Migrate
3. **Application operations** — handle, route, authenticate, authorize, validate, schedule, Dispatch, resolve
4. **Communication actions** — send, receive, publish, subscribe, stream, poll, broadcast, connect

If a word is not approved as a verb in the STE-Code dictionary, do not use it as a verb. Use a different sentence construction (usually the noun form of the word) to give the same information.

### Why verbs, not nouns, in code documentation

A noun names a thing; a verb names the work. When you write `validate the token`, the reader knows to run the check. When you write `validation of the token`, the reader must stop and ask: do I run it, log it, or skip it? Prefer the verb. Prefer the plain, approved verb — `use`, `start`, `stop`, `show`, `make`, `get`, `set`, `check`, `do`, `send`, `remove`, `keep` — over wordy substitutes such as *utilize*, *leverage*, *employ*, *commence*, *terminate*, or *initiate* when a simpler verb already does the job.

## Examples

> *Adapted from spec pair:* Non-STE: "The ohmmeter gives an indication of 450 ohms." | STE: "The ohmmeter shows 450 ohms."

---

### Example 1 — Profiler reports latency (development operations)

**Non-STE:**
```
# benchmark_report.py
def report_latency():
    # The profiler gives an indication of 200ms latency.
    return "profiler indicates 200ms"
```
> **Non-STE:** The profiler gives an indication of 200ms latency.

**STE:**
```
# benchmark_report.py
def report_latency():
    # The profiler shows 200ms latency.
    return "profiler shows 200ms"
```
> **STE:** The profiler shows 200ms latency.

*Adapted from spec pair: "The ohmmeter gives an indication of 450 ohms." / "The ohmmeter shows 450 ohms." The approved verb "show" describes the action more clearly than the noun phrase "gives an indication of."*

---

### Example 2 — Service initialization (application actions)

**Non-STE:**
```
# deploy.sh
# Before the initialization of the service, make sure that the config is valid.
cp config.default.yaml config.yaml
```
> **Non-STE:** Before the initialization of the service, make sure that the config is valid.

**STE:**
```
# deploy.sh
# Before you initialize the service, make sure that the config is valid.
./init-service.sh
```
> **STE:** Before you initialize the service, make sure that the config is valid.

*Adapted from spec pair: "Before the removal of the unit, make sure that the power supply is OFF." / "Before you remove the unit, make sure that the power supply is OFF." Use the approved verb "initialize" instead of the noun "initialization."*

---

### Example 3 — Caching a response (data + communication actions)

**Non-STE:**
```
// cache_client.go
func Get(r *http.Request) string {
    // Cache the response.
    return upstream(r)
}
```
> **Non-STE:** Cache the response.

**STE:**
```
// cache_client.go
func Get(r *http.Request) string {
    // Do a cache of the response.
    return cache.Do(upstream(r))
}
```
> **STE:** Do a cache of the response.

*Adapted from spec pair: "Check the laptop battery." / "Do a check of the laptop battery." "Cache" is an approved technical noun (category 1.5) but not an approved verb. Use the noun form "Do a cache" instead of the verb "Cache."*

---

### Example 4 — HTTP status from a function (communication actions)

**Non-STE:**
```
# handler.py
def status() -> str:
    # Do not write: The function gives a result of Put 500 OK.
    return "result 500"
```
> **Non-STE:** The function gives a result of 500 OK.

**STE:**
```
# handler.py
def status() -> str:
    # The function returns 500 OK.
    return "500 OK"
```
> **STE:** The function returns 500 OK.

*Adapted from spec principle: the approved verb "return" describes the action more clearly than the noun phrase "gives a result of."*

---

### Example 5 — Validate input (application actions)

**Non-STE:**
```
// validate.go
// The parser does a verification of the payload.
func Verify(p []byte) error { /* ... */ }
```
> **Non-STE:** The parser does a verification of the payload.

**STE:**
```
// validate.go
// You validate the payload before you store it.
func Validate(p []byte) error { /* ... */ }
```
> **STE:** You validate the payload before you store it.

---

### Example 6 — Read and write config (data actions)

**Non-STE:**
```
# config_io.py
# A read of the config, then a write of the config.
def load(): ...
def store(): ...
```
> **Non-STE:** A read of the config, then a write of the config.

**STE:**
```
# config_io.py
# Read the config, then write the config.
def read(): ...
def write(): ...
```
> **STE:** Read the config, then write the config.

---

### Example 7 — Send and receive messages (communication actions)

**Non-STE:**
```
// bus.go
// A transmission of the event, then a reception of the event.
func Transmit(e Event) { ... }
func Receive(e Event) { ... }
```
> **Non-STE:** A transmission of the event, then a reception of the event.

**STE:**
```
// bus.go
// Send the event, then receive the event.
func Send(e Event) { ... }
func Receive(e Event) { ... }
```
> **STE:** Send the event, then receive the event.

---

> **See also:**
> - Rule 3.2 — Use only these verb forms and tenses of verbs (infinitive, imperative, simple present, simple past, simple future, past participle).
> - Rule 1.5 — Technical noun categories: the noun-form fallback when a word is not an approved verb.
> - Extension approved verbs — use, start, stop, show, make, get, set, check, do, send, remove, keep.
> - Rule 3.3 — related verb and tense guidance in the STE-Code dictionary.
