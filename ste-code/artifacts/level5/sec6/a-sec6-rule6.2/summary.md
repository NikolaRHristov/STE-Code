# Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure

## Original Rule Summary

Rule 6.2 requires that you use key words and key phrases to connect related ideas across sentences and give your text a logical structure. Key words are terms that occur multiple times in a text to link different concepts together, and key phrases are multi-word expressions that serve the same connecting function. You can also use connecting words such as "and," "but," "then," and "thus," and connecting phrases such as "as a result" and "at the same time," which act as traffic signs showing whether the information is new, different, or a result of previous information. When you use key words and key phrases, do not change them — the same terminology will keep your text clear and correct.

## STE-Code Adaptation

In code documentation, use key words and key phrases to connect related ideas across sentences within a documentation block. Key words are class names, function names, parameter names, variable names, and code-domain technical nouns that repeat from sentence to sentence. Key phrases are multi-word technical terms such as "connection pool," "authentication middleware," or "retry policy" that must stay intact across sentences. Use approved connecting words and connecting phrases to help the developer understand the logical flow of ideas, signaling whether information is new, a contrast, a sequence, or a result. Never change key words or key phrases mid-documentation — switch between names and the reader cannot follow the logical structure you are building.

## Example Pairs

> **Non-STE:** `redis.host` sets the Redis server address. The default is `localhost` on the usual port. You can override this with an environment variable.
>
> **STE:** The `redis.host` option sets the Redis server hostname. The default hostname is `localhost`. Set the `REDIS_HOST` environment variable to override the default hostname.

> **Non-STE:** The parser encounters invalid JSON. An exception gets raised with the position. The caller catches it and logs the incident.
>
> **STE:** The parser finds invalid JSON. The parser raises a `ParseError` exception. The caller catches the `ParseError`. The caller logs the `ParseError` to the error log.

> **Non-STE:** `ste-code lint` checks documentation files. It scans for rule violations and emits a report. The tool exits with a non-zero code on failure.
>
> **STE:** The `ste-code lint` command checks documentation files. The `lint` command scans for rule violations. The `lint` command writes a report. The `lint` command exits with code 1 on failure.

## Principles Applied

**P1** — Use approved words from the controlled terminology. Connecting words such as "and," "but," "then," "thus," "also," "however," and "therefore" must be from the approved dictionary of connecting words and connecting phrases.

**P2** — Use approved nouns from the dictionary. When the key word is a common noun (not a technical code noun), it must be an approved word. Do not use unapproved nouns as your primary key words.

**P6** — Use approved verbs and verb forms. When a connecting word signals a sequence or result ("then," "thus," "therefore"), the verb in the following sentence must be an approved verb from the STE-Code dictionary.

**P11** — Use one term per concept. This principle is the foundation of Rule 6.2. Key words work only if you use the same term for the same concept across all sentences. Switching between synonyms breaks the key word chain and forces the reader to reconstruct the logical relationship.
