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

Every approved verb in the STE-Code dictionary appears with its allowed forms. The dictionary shows the base form, the third-person singular, the simple past, and the past participle. You use only those forms.

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

The four approved verb categories in STE-Code are:

1. **Development operations** — build, compile, test, lint, format, commit, push, deploy, rollback
2. **Data operations** — read, write, serialize, deserialize, parse, encode, decode, query, insert, migrate
3. **Application operations** — handle, route, authenticate, authorize, validate, schedule, dispatch, resolve
4. **Communication operations** — send, receive, publish, subscribe, stream, poll, broadcast, connect

When you write a verb, confirm that the form is one that the dictionary lists for that verb. If the verb is not in the dictionary, do not use it. Use an approved verb instead. For each approved verb the dictionary gives exactly these forms and no others:

| Base form (infinitive) | Third-person singular | Simple past | Past participle |
|---|---|---|---|
| validate | validates | validated | validated |
| write | writes | wrote | written |
| build | builds | built | built |
| read | reads | read | read |
| migrate | migrates | migrated | migrated |
| send | sends | sent | sent |
| resolve | resolves | resolved | resolved |

**How to check a verb form**

1. Find the verb in the dictionary. If the verb is not there, do not use it.
2. Use only the base form, the form that ends in "-s" for he/she/it, the simple past, or the past participle.
3. Do not add "-ing" to a verb and use it with a form of "be" (for example, "is validating", "was building").
4. Do not use "have", "has", or "had" with the past participle as a verb (for example, "has validated", "had written").
5. Do not use the verb with "will" except to state a future action in simple future tense ("the test will fail"), and do not build longer verb chains around the approved forms.

**Preferred simple verbs**

When the verb you want is not in the dictionary, use one of the approved simple verbs instead of a longer word:

- use, not utilize, leverage, or employ
- start, not initiate, commence, or bootstrap
- stop, not terminate, halt, or kill
- show, not display, render, or present
- make, not create, generate, or produce
- get, not retrieve, fetch, or obtain
- set, not configure, assign, or establish
- check, not verify, validate, or ensure
- do, not perform, execute, or carry out
- send, not transmit, dispatch, or forward
- remove, not delete, eliminate, or purge
- keep, not retain, preserve, or maintain

Note that some of these simple verbs are themselves approved verbs in the dictionary. Use only the forms that the dictionary lists for the verb you choose.

> **Note: structural carryover — no code-domain equivalent** — The dictionary layout (base form, third-person singular, simple past, past participle shown for each verb) is a structural feature of the source standard. The code-domain version keeps the same layout with code verbs. No mapping is forced.

## Examples

> *Adapted from spec pair:* Non-STE: The technician is removing the panel. | STE: The technician removes the panel.

> **Non-STE:** The linter is validating the file and is reporting the errors to the terminal while the build is compiling the modules.
> **STE:** The linter validates the file. It reports the errors to the terminal. The build compiles the modules.
>
> *Adapted from spec principle: use only the verb forms that the dictionary gives. The progressive forms "is validating", "is reporting", and "is compiling" are not approved forms.*
>
> ```python
> # STE: plain approved verb forms only
> def check_config(path):
>     """Validate the file. Report the errors to the terminal."""
>     errors = linter.validate(path)   # validate -> validates / validated / validated
>     for error in errors:
>         print(error)                 # print reports the result
>     build.compile_modules()          # compile -> compiles / compiled / compiled
> ```

> **Non-STE:** The script has written the output to the log before the test starts.
> **STE:** The script wrote the output to the log. Then the test starts.
>
> *Adapted from spec principle: use only the approved simple past form. The present perfect "has written" is not an approved form.*
>
> ```bash
> # STE: simple past tense, two clear steps
> ./run_parser.sh > output.log   # the script wrote the output to the log
> pytest tests/                  # then the test starts
> ```

> **Non-STE:** The migration job had already seeded the database before the service attempted to read the table.
> **STE:** The migration job seeded the database. Then the service read the table.
>
> *Adapted from spec principle: use only the approved simple past form. The past perfect "had seeded" is not an approved form. Break the sequence into separate sentences with "Then."*
>
> ```yaml
> # STE: two sequential steps, simple past in the comment
> steps:
>   - name: seed-database      # the migration job seeded the database
>     run: python migrate.py --seed
>   - name: read-table         # then the service read the table
>     run: python service.py --read
> ```

> **Non-STE:** If the token expires, the client is reconnecting and will be retrying the request until the server responds.
> **STE:** If the token expires, the client reconnects. It retries the request until the server responds.
>
> *Adapted from spec principle: use only the approved forms. The progressive "is reconnecting" and the future progressive "will be retrying" are not approved forms. Use the simple present "reconnects" and the simple present "retries."*
>
> ```javascript
> // STE: simple present for repeated or general actions
> function onTokenExpire(client) {
>   client.reconnects();        // reconnect -> reconnects / reconnected / reconnected
>   while (!client.hasResponse()) {
>     client.retries(request);   // retry -> retries / retried / retried
>   }
> }
> ```

> **Non-STE:** We are utilizing the cache to leverage the serialized data and to employ the parser for the input.
> **STE:** We use the cache. We serialize the data. We parse the input.
>
> *Adapted from spec principle: use only approved verbs and only their approved forms. "Utilize", "leverage", and "employ" are not in the dictionary; the approved verb is "use". "Serialize" and "parse" are approved, but the gerund forms "serializing" and "employing" are not approved verb forms.*
>
> ```python
> # STE: approved verbs, base or "-s" form only
> cache.use()              # use -> uses / used / used
> data = serialize(raw)    # serialize -> serializes / serialized / serialized
> result = parser.parse(text)  # parse -> parses / parsed / parsed
> ```

> **Non-STE:** The handler will be dispatching the event after the worker has resolved the task and the queue has published the message.
> **STE:** The handler dispatches the event. The worker resolves the task. The queue publishes the message.
>
> *Adapted from spec principle: use only the approved forms. The future progressive "will be dispatching", the present perfect "has resolved", and the present perfect "has published" are not approved forms. Use the simple present for each action.*
>
> ```go
> // STE: simple present in the documentation comment
> // The handler dispatches the event. The worker resolves the task.
> // The queue publishes the message.
> func Handle(ctx Context) {
>     worker.Resolve(task)   // resolve -> resolves / resolved / resolved
>     queue.Publish(message) // publish -> publishes / published / published
>     handler.Dispatch(event) // dispatch -> dispatches / dispatched / dispatched
> }
> ```

> **Non-STE:** The configuration was migrated by the tool and the records were deleted from the store.
> **STE:** The tool migrated the configuration. It removed the records from the store.
>
> *Adapted from spec principle: use only the approved verb forms. The passive progressive "was migrated" and "were deleted" are not approved. Name the actor (the tool) and use the simple past "migrated" and the approved verb "remove" (past "removed"), not "delete".*
>
> ```sql
> -- STE: name the actor, simple past tense
> -- The tool migrated the configuration.
> -- It removed the records from the store.
> UPDATE config SET status = 'migrated' WHERE id = 1;
> DELETE FROM store WHERE expired = true;  -- remove the records
> ```

> **Non-STE:** The validated token is accepted and the encrypted payload gets decoded by the gateway.
> **STE:** The gateway accepts the validated token. It decodes the encrypted payload.
>
> *Adapted from spec principle: the past participle "validated" is approved only as an adjective that modifies a noun ("the validated token"), not as a verb with an auxiliary. "Gets decoded" uses "get" with a past participle as a verb, which is not an approved form. Use the simple present "decodes".*
>
> ```python
> # STE: past participle as adjective only; verb in simple present
> validated_token = auth.validate(token)  # "validated" modifies token (adjective use)
> if gateway.accepts(validated_token):     # accept -> accepts / accepted / accepted
>     payload = gateway.decode(data)        # decode -> decodes / decoded / decoded
> ```

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** Rule 1.2 — Use Approved Words Only as the Specified Part of Speech
> **See also:** Rule 1.12 — Technical Verbs Are Allowed
> **See also:** Rule 3.2 — Use Only These Verb Forms and Tenses of Verbs
> **See also:** The STE-Code dictionary (a-dictionary.md) — the full list of approved verbs and their allowed forms
