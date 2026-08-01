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

Do not use the past participle form if it is not in the dictionary.

There are also approved adjectives in the STE-Code dictionary that are the past participle form of verbs that are not approved. Their approved part of speech in the dictionary is "(adj)" and thus you can use them. Examples in the code domain are "deprecated," "corrupted," "allowed," and "given."

**How to tell an adjective from passive voice**

1. **Look for the actor.** Passive voice hides who does the action ("The file was parsed by the loader"). An adjective states a condition and needs no actor ("The parsed file is ready").
2. **Try the position test.** If the word can go directly before the noun ("the parsed file", "the deprecated method"), it works as an adjective.
3. **Try the linking-verb test.** If the word follows "is", "becomes", or "stays" and answers "in what condition?", it is an adjective ("The cache is initialized").
4. **If the word adds "by <actor>", it is passive voice.** Rewrite it in the active voice. See Rule 3.6.

**How to correct a wrong use**

- Passive voice → active voice with a named actor: "The record was deleted by the job" → "The job deletes the record."
- Past participle used as a full verb → simple past: "The service has restarted" → "The service restarted."
- Past participle that is not in the dictionary → use an approved word: "the instantiated client" → "the new client"; "the leveraged cache" → "the used cache".
- Two or more stacked participles → one participle and one noun: "the parsed validated cached response" → "the parsed response. The cache keeps the response after the check."

## Examples

> *Adapted from spec pair:* Non-STE: The unit which had been taken apart must be looked at for damage.  |  STE: Examine all parts of the disassembled unit for damage.

> **Non-STE:** All fields of the object that was deserialized by the reader must be inspected for corruption by the caller.
> **STE:** Inspect all fields of the deserialized object for corruption.
>
> ("Deserialized" is an adjective before the noun "object." It shows the condition of the object.)
>
> ```python
> # STE: "deserialized" is an adjective before the noun "object".
> def inspect(deserialized_object: dict) -> None:
>     """Inspect all fields of the deserialized object for corruption."""
>     for name, value in deserialized_object.items():
>         if value is None:
>             raise ValueError(f"corrupted field: {name}")
> ```

> **Non-STE:** When the cache has been fully initialized by the bootstrap code, the worker threads are started.
> **STE:** When the cache is fully initialized, start the worker threads.
>
> ("Initialized" is an adjective after the verb "to be." It shows the condition of the cache.)
>
> ```go
> // STE: "initialized" is an adjective after the verb "to be".
> // When the cache is fully initialized, start the worker threads.
> if cache.IsInitialized() {
>     pool.Start(workerCount)
> }
> ```

> **Non-STE:** More memory than is permitted must not be given to the buffer by the allocator.
> **STE:** Do not exceed the allowed memory for the buffer.
>
> *Adapted from spec pair: "Do not put more than the permitted weight on the trolley." ("permitted" is an approved adjective with part of speech "(adj)".)*
>
> ```yaml
> # STE: "allowed" is an approved adjective before the noun "memory".
> limits:
>   allowed_memory_mb: 512
>   allowed_open_files: 1024
> ```

> **Non-STE:** It must be ensured that the input values have not been corrupted by the previous stage.
> **STE:** Make sure that the input values are not corrupted.
>
> *Adapted from spec pair: "Make sure that the mating surfaces are not damaged." ("damaged" is an approved adjective with part of speech "(adj)".)*
>
> ```javascript
> // STE: "corrupted" is an adjective after the verb "to be".
> function check(values) {
>   if (isCorrupted(values)) {
>     throw new Error("the input values are corrupted");
>   }
>   return values;
> }
> ```

> **Non-STE:** The parsed file was processed by the loader.
> **STE:** The parsed file is ready for the loader.
>
> *Adapted from spec principle: "parsed" is the past participle used as an adjective before the noun "file." It shows the condition of the file, not passive voice.*
>
> ```bash
> # STE: "parsed" shows the condition of the file. The loader is the actor.
> parse-config --in app.conf --out app.parsed.json
> loader --config app.parsed.json
> ```

> **Non-STE:** The method has been deprecated and will be removed by a future release, so it should not be called by new code.
> **STE:** The method is deprecated. A future release removes the method. Do not call the deprecated method in new code.
>
> *Adapted from spec principle: "deprecated" is an approved adjective. It shows the condition of the method. Use the active voice for the action of the release.*
>
> ```java
> /**
>  * The method is deprecated. Use {@link #send(Request)}.
>  * Do not call the deprecated method in new code.
>  */
> @Deprecated
> public void sendLegacy(Request request) { ... }
> ```

> **Non-STE:** After the token has been signed and been validated, access is granted to the stored records by the API.
> **STE:** When the token is signed and validated, the API gives access to the stored records.
>
> *Adapted from spec principle: "signed", "validated", and "stored" show conditions. The API is the actor of the action.*
>
> ```json
> {
>   "token": { "signed": true, "validated": true },
>   "access": "granted",
>   "records": "stored"
> }
> ```

> **Non-STE:** The written log stays unchanged until it is rotated by the daemon at midnight.
> **STE:** The written log stays unchanged. The daemon rotates the log at 00:00.
>
> *Adapted from spec principle: "written" and "unchanged" are adjectives after "to stay". Name the actor for the action of the daemon.*
>
> ```bash
> # STE: the written log stays unchanged. The daemon rotates the log at 00:00.
> logrotate --state /var/lib/logrotate.status /etc/logrotate.d/api
> ```

> **Non-STE:** The instantiated client object which was utilized by the test had been left in a connected state.
> **STE:** The test keeps the new client in a connected state.
>
> *Adapted from spec principle: "instantiated" and "utilized" are not in the dictionary. Use "new" and "use". "Connected" is an approved adjective that shows the condition of the client.*
>
> ```python
> # STE: use approved words. "connected" shows the condition of the client.
> def test_client_stays_connected():
>     client = new_client(url)
>     assert client.is_connected
> ```

> **Non-STE:** The failed build and the given options were recorded by the pipeline in the generated report.
> **STE:** The pipeline records the failed build and the given options in the report.
>
> *Adapted from spec pair: "The adjusted linkage" and "the given information" show the past participle used as an adjective. Keep the adjectives, but write the action in the active voice.*
>
> ```yaml
> # STE: "failed" and "given" are adjectives. The pipeline is the actor.
> report:
>   failed_build: 4821
>   given_options: ["--release", "--strip"]
> ```

> **See also:** Rule 3.2 — Use only these verb forms and tenses of verbs
> **See also:** Rule 3.4 — Do not use auxiliary verbs to make complex verb constructions
> **See also:** Rule 3.5 — Use the "-ing" form of a verb only as a technical noun or as a modifier in a technical noun
> **See also:** Rule 3.6 — Use the Active Voice
> **See also:** Rule 1.1 — Use words that are approved in the dictionary
> **See also:** The STE-Code dictionary (a-dictionary.md) — the approved adjectives with part of speech "(adj)"
