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
