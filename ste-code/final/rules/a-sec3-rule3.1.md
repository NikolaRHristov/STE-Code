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
