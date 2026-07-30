# Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs

## Original Rule Summary

Rule 1.1 is the gatekeeping rule of Simplified Technical English (STE). Every word must pass one of three gates: it is an approved word in the STE dictionary, it is a technical noun belonging to a recognized subject field, or it is a technical verb describing a specific process within that subject field. The dictionary (part 2 of the spec) gives the most frequently used words in technical writing, along with a list of unapproved words and their approved alternatives. Technical nouns and technical verbs are not in the dictionary but are permitted because they name domain-specific concepts and operations.

## STE-Code Adaptation

Rule 1.1 in STE-Code applies the same three-gate model to code documentation. Every word must be an approved word in the project controlled terminology, a code-domain technical noun (one of 22 categories under Rule 1.5), or a code-domain technical verb (one of 4 categories under Rule 1.12). The controlled terminology gives the most frequently used words in code documentation and lists unapproved words with approved alternatives. Code-domain technical nouns and verbs name software-specific concepts, tools, and operations that have no simple approved-word alternative.

## Example Pairs

> **Non-STE:** Utilize the build tool to generate the artifact. Execute the binary to bootstrap the service. Utilize environment variables to configure runtime behavior.
>
> **STE:** Use the build tool to make the binary. Run the binary to start the service. Use environment variables to set the runtime behavior.
>
> *(P1 applied: "utilize" → "use"; "generate" → "make"; "execute" → "run"; "bootstrap" → "start"; "configure" → "set")*

> **Non-STE:** @param {number} timeout — The duration in milliseconds the client shall await a response prior to terminating the connection attempt.
>
> **STE:** @param {number} timeout — The time in milliseconds that the client waits for a response before it stops the connection.
>
> *(P1 applied: "duration" → "time"; "shall await" → "waits"; "prior to" → "before"; "terminating" → "stops")*

> **Non-STE:** Perform validation on the input data to ensure it conforms to the expected schema. Returns a boolean indicating whether the data is valid.
>
> **STE:** Check the input data against the schema. Gives `true` when the data is correct and `false` when the data is not correct.
>
> *(P1 applied: "perform" → "do"; "validation" restructured to "check"; "ensure" restructured; "conforms to" → "against"; "returns" → "gives"; "valid" → "correct")*

## Principles Applied

**P1** — Use approved words from the controlled terminology. This is the primary principle: every general-purpose word must come from the approved list. "Utilize" → "use", "execute" → "run", "configure" → "set", "validate" → "check", "duration" → "time".

**P6** — Use non-approved words only when they are technical nouns. Code-domain technical nouns like `UserAuthenticator`, `Promise`, `ApiError`, and `ValidationError` are permitted because they name specific software concepts. The approved-word restriction does not apply to them.

**P8** — Use standard, well-known technical nouns. Technical nouns must be recognized within the software domain. Terms like "build tool," "binary," "schema," and "parameter" are standard code-domain technical nouns.

**P9** — Prefer short, clear technical nouns. When a technical noun has multiple valid forms, use the shortest unambiguous one. For example, "time" instead of "duration," "connection" instead of "connection attempt."
