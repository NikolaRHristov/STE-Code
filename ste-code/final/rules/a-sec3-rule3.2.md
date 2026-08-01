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
| (To) Write (irregular verb) | Write + object | You/we/they write It writes | You/we/they wrote It wrote | You/we/they will write It will write | The written log |
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
- Passive with an unapproved auxiliary ("is being parsed") → name the actor and use the active voice ("the worker parses the file").

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
> *Adapted from spec pair: the past perfect "had adjusted" is not approved. Use the simple past tense and sequence with "Then." The approved verb is "make", not "initialize".*
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
> *Adapted from spec pair: the present progressive "is adjusting" is not approved. Use the simple present tense for each action.*
>
> ```yaml
> # .github/workflows/release.yml
> # STE: the scheduler sends the build to production. The tests run at the same time.
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
> gateway.validate(payload);        // validate -> validates / validated / validated
> migration.remove(record.legacyId); // remove -> removes / removed / removed
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

> **See also:** Rule 3.1 — Use Only the Verb Forms That Are Given in the Dictionary
> **See also:** Rule 3.3 — Use the Active Voice
> **See also:** Rule 3.4 — Do Not Leave Out a Verb or a Part of a Verb
> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** The STE-Code dictionary (a-dictionary.md) — the full list of approved verbs and their allowed forms
