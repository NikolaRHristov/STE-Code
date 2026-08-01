# Rule 8.7 — Hyphenated Words Count as One Word

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.7

> **Source:** [master.md#sec8-rule8.7](ste-code/grouped/)

## Original Rule

**Rule 8.7** Hyphenated words count as one word.

Groups of words that are not usually adjectives but have the function of an adjective before a noun are hyphenated. Such groups of words count as one word.

Examples:

| Example | Word count |
|----------|-------------|
| Clean the surface with a soap-and-water solution. | (7 words) |
| Use the trial-and-error method. | (4 words) |

When you use hyphens in long technical nouns to make them clearer to the reader, a hyphenated group of words also counts as one word.

Examples:

| Example | Word count |
|----------|-------------|
| Cutoff-switch power connection | (3 words) |
| Main-gear-door retraction-winch handle | (3 words) |

## STE-Code Adaptation

**Rule 8.7** Hyphenated words count as one word.

Groups of words that are not usually adjectives but have the function of an adjective before a noun are hyphenated. Such groups of words count as one word.

In code documentation, this rule applies directly. A hyphenated technical term, whether it is a compound adjective or a long technical noun, counts as one word when you count words for sentence length. The hyphen joins two or more words into a single unit that the reader processes as one concept, so the word-count limits in Rules 4.1 and 4.2 measure the unit as one word, not as the number of words inside it.

### Examples

> *Adapted from spec pair:* Non-STE: "Clean the surface with a soap and water solution."  |  STE: "Clean the surface with a soap-and-water solution." (7 words — "soap-and-water" is a hyphenated compound adjective and counts as one word.)

> **Non-STE:** The open function returns a read only file descriptor. The caller parses the config from the descriptor and then closes it.
>
> **STE:** The open function returns a read-only file descriptor. The caller parses the config from the descriptor and then closes it.
>
> *Adapted from spec pair: "Clean the surface with a soap-and-water solution." → "read-only" is a hyphenated compound adjective and counts as one word.*

> *Adapted from spec pair:* Non-STE: "Use the trial and error method."  |  STE: "Use the trial-and-error method." (4 words — "trial-and-error" is a hyphenated compound adjective and counts as one word.)

> **Non-STE:** To calibrate the retry interval, use the try and error method. Run the probe, record the latency, and adjust the value until the timeout stops.
>
> **STE:** To calibrate the retry interval, use the trial-and-error method. Run the probe, record the latency, and adjust the value until the timeout stops.
>
> *Adapted from spec pair: "Use the trial-and-error method." → "trial-and-error" is a hyphenated compound adjective and counts as one word.*

> *Adapted from spec pair:* Non-STE: "Cutoff switch power connection"  |  STE: "Cutoff-switch power connection" (3 words: `cutoff-switch` / `power` / `connection`). The hyphenated noun group counts as one word.

> **Non-STE:** The cutoff switch power connection must stay isolated during the test. If the relay closes, the test fails and the harness records a short circuit.
>
> **STE:** The cutoff-switch power connection must stay isolated during the test. If the relay closes, the test fails and the harness records a short circuit.
>
> *Adapted from spec pair: "Cutoff-switch power connection" (3 words). The hyphenated noun group counts as one word.*

> *Adapted from spec pair:* Non-STE: "Main gear door retraction winch handle"  |  STE: "Main-gear-door retraction-winch handle" (3 words: `main-gear-door` / `retraction-winch` / `handle`). The hyphenated noun group counts as one word.

> **Non-STE:** The main gear door retraction winch handle must lock before the door opens. The controller checks the sensor and blocks the actuator until the latch engages.
>
> **STE:** The main-gear-door retraction-winch handle must lock before the door opens. The controller checks the sensor and blocks the actuator until the latch engages.
>
> *Adapted from spec pair: "Main-gear-door retraction-winch handle" (3 words). The hyphenated noun group counts as one word.*

> *Adapted from spec pair:* Non-STE: "The build-time environment variable points to staging."  |  STE: "The build-time environment variable must point to the staging cluster." (10 words — "build-time" is one word). Compound identifiers written as words use the same structure as the spec's long technical nouns.

> **Non-STE:** Set the build time environment variable to the path of the staging cluster before you run the pipeline. The job fails when the value is empty.
>
> **STE:** Set the build-time environment variable to the path of the staging cluster before you run the pipeline. The job fails when the value is empty.
>
> *Adapted from spec pair: "Cutoff-switch power connection" (3 words). "build-time" is a hyphenated technical noun and counts as one word; the two following words are separate.*

> *Adapted from spec pair:* Non-STE: "Run the end to end test suite in the pipeline."  |  STE: "Run the end-to-end test suite in the pipeline." (8 words — "end-to-end" is one word). The same pre-noun hyphen pattern applies to compound code-domain adjectives.

> **Non-STE:** The client side rendering pipeline builds the page in the browser. The server sends the data as JSON and the view updates after the fetch returns.
>
> **STE:** The client-side rendering pipeline builds the page in the browser. The server sends the data as JSON and the view updates after the fetch returns.
>
> *Adapted from spec pair: "soap-and-water solution" → "client-side" is a hyphenated compound adjective before "rendering pipeline" and counts as one word.*

> *Adapted from spec pair:* Non-STE: "Use a thread safe singleton for the cache."  |  STE: "Use a thread-safe singleton for the cache." (7 words — "thread-safe" is one word). Approved STE-Code adjectives (thread-safe, idempotent, stateless) keep the hyphen before the noun.

> **Non-STE:** The event driven architecture sends a message to the queue after the worker finishes the task. The consumer reads the event and updates the record.
>
> **STE:** The event-driven architecture sends a message to the queue after the worker finishes the task. The consumer reads the event and updates the record.
>
> *Adapted from spec pair: "trial-and-error method" → "event-driven" is a hyphenated compound adjective and counts as one word.*

## Code-Domain Explanation

Rule 8.7 tells you how to count words when a term is hyphenated. The hyphen joins two or more words into a single unit that the reader processes as one concept. For word-count limits in STE-Code (Rules 4.1 and 4.2), a hyphenated unit counts as one word, not as the number of words inside it.

There are two cases.

### Case 1: Hyphenated compound adjectives

When a group of words describes a noun and sits before that noun, you hyphenate it. Examples from the spec: "soap-and-water solution," "trial-and-error method." The same pattern appears throughout code documentation:

- `read-only file descriptor` — "read-only" is one word.
- `thread-safe singleton` — "thread-safe" is one word.
- `event-driven architecture` — "event-driven" is one word.
- `low-latency cache` — "low-latency" is one word.
- `client-side rendering pipeline` — "client-side" is one word.
- `end-to-end test suite` — "end-to-end" is one word.
- `backward-compatible API` — "backward-compatible" is one word.
- `idempotent retry handler` — "idempotent" is a single approved word; no hyphen needed, but when you write "exactly-once delivery" the hyphenated unit is one word.
- `stateless authentication service` — "stateless" is a single approved word; "request-response cycle" keeps "request-response" as one word.

If you put the same words after the noun, do not hyphenate them: "the cache is low latency." Hyphenation is a pre-noun signal only. The word count does not change; the hyphen group still counts as one word.

When the compound adjective follows a linking verb, write the words as separate words and count each one:

- Non-STE: "The singleton is thread safe."
- STE: "The singleton is thread safe." (5 words — "thread" and "safe" are two words because the adjective is after the noun.)

### Case 2: Long hyphenated technical nouns

When a technical noun is long and the hyphen makes it easier to read, the whole hyphenated group counts as one word. Examples from the spec: "cutoff-switch power connection" (3 words: `cutoff-switch` / `power` / `connection`), "main-gear-door retraction-winch handle" (3 words: `main-gear-door` / `retraction-winch` / `handle`).

In the code domain, the same structure applies to compound identifiers that are written as words:

- `build-time environment variable` (3 words: `build-time` / `environment` / `variable`)
- `client-side rendering pipeline` (3 words: `client-side` / `rendering` / `pipeline`)
- `end-to-end test suite` (3 words: `end-to-end` / `test` / `suite`)
- `check-out request handler` (3 words: `check-out` / `request` / `handler`)
- `sign-in error message` (3 words: `sign-in` / `error` / `message`)
- `look-up table index` (3 words: `look-up` / `table` / `index`)

The words after the hyphenated unit are separate words. Only the hyphenated group counts as one word.

### Why this matters for word count

STE-Code limits procedural sentences to 20 words and descriptive sentences to 25 words (Rules 4.1, 4.2). If you count each word inside a hyphenated term, you over-report the sentence length and may break a limit that the sentence actually meets. Count the hyphenated unit as one word.

Example:

> **STE:** The build-time environment variable must point to the staging cluster. (10 words)

Word count: `The` (1) `build-time` (2) `environment` (3) `variable` (4) `must` (5) `point` (6) `to` (7) `the` (8) `staging` (9) `cluster` (10). The hyphenated `build-time` is one word. The sentence has 10 words, not 11.

Another example with a hyphenated compound adjective:

> **STE:** The thread-safe singleton must cache the read-only file descriptor. (9 words)

Word count: `The` (1) `thread-safe` (2) `singleton` (3) `must` (4) `cache` (5) `the` (6) `read-only` (7) `file` (8) `descriptor` (9). Both `thread-safe` and `read-only` are one word each.

### Interaction with Rule 8.2

Rule 8.2 tells you when to use a hyphen to connect directly related words. Rule 8.7 tells you how to count those words after you hyphenate them. The two rules work together: hyphenate per Rule 8.2, then count the hyphenated unit as one word per Rule 8.7.

Example that joins both rules:

> **Non-STE:** Use the open source library to parse the json config in the build time phase.
>
> **STE:** Use the open-source library to parse the JSON config in the build-time phase.

`open-source` is hyphenated per Rule 8.2 and counts as one word per Rule 8.7. `build-time` is a hyphenated technical noun and counts as one word. `JSON` is an abbreviation and counts as one word per Rule 8.6.

### Interaction with Rule 8.6

Rule 8.6 lists elements that count as one word (numbers, units, abbreviations, alphanumeric identifiers, quoted text, titles, proper nouns). A hyphenated word is a separate case: it is not an abbreviation or an identifier, but it still counts as one word because the hyphen makes it a single unit. Do not double-count — a hyphenated term is one word under Rule 8.7, and it is not also an abbreviation or an identifier.

Example that shows both rules in one sentence:

> **STE:** Set API_TIMEOUT_MS to 5000 in the client-side test suite. (10 words)

Word count: `Set` (1) `API_TIMEOUT_MS` (2, identifier per Rule 8.6) `to` (3) `5000` (4, number per Rule 8.6) `in` (5) `the` (6) `client-side` (7, hyphenated adjective per Rule 8.7) `test` (8) `suite` (9). The sentence has 9 words, not 11.

### Exception: hyphen in a numeral or a range

A hyphen that joins the parts of a spelled-out numeral (`twenty-one`, `forty-seven`) or marks a range (`pages 10-15`) is covered by Rule 8.6 (numbers count as one word) and by standard number counting. Rule 8.7 applies to hyphenated word groups that are adjectives or technical nouns, not to numerals.

> **STE:** Do steps 13 thru 16 a minimum of three times. (10 words — "13" and "16" each count as one word under Rule 8.6.)

This is distinct from "cutoff-switch power connection," which Rule 8.7 covers as a hyphenated noun group.

### Common code-domain hyphenated terms

Use these approved patterns in your documentation. Each hyphenated unit counts as one word before a noun:

| Term | Type | Counts as |
|------|------|-----------|
| read-only | compound adjective | one word |
| write-only | compound adjective | one word |
| thread-safe | compound adjective | one word |
| event-driven | compound adjective | one word |
| client-side | compound adjective | one word |
| server-side | compound adjective | one word |
| end-to-end | compound adjective | one word |
| backward-compatible | compound adjective | one word |
| low-latency | compound adjective | one word |
| build-time | technical noun | one word |
| run-time | technical noun | one word |
| sign-in | technical noun | one word |
| check-out | technical noun | one word |
| request-response | technical noun | one word |

When a term in this table follows the noun or a linking verb, write it as separate words and count each word.

## Verification of the Adaptation

- Rule number preserved: 8.7.
- Each STE/non-STE pair replaced with a code-domain pair (`read only` → `read-only`, `try and error` → `trial-and-error`, `cutoff switch` → `cutoff-switch`, `main gear door retraction winch` → `main-gear-door retraction-winch`, `build time` → `build-time`, `client side` → `client-side`, `end to end` → `end-to-end`, `thread safe` → `thread-safe`, `event driven` → `event-driven`).
- No aerospace-domain terms outside the `## Original Rule` block.
- American English spelling, no contractions, no progressive or perfect tenses in the adapted text.
- Part of speech preserved: "hyphenated" (adjective), "count" (verb), "word" (noun) keep their STE source roles.

> **See also:** Rule 8.2 — Use Hyphens (-) to Connect Words That Are Directly Related

> **See also:** Rule 8.6 — Elements That Count as One Word

> **See also:** Rule 4.1 — One Topic Per Sentence, No Abstract Text

> **See also:** Rule 4.2 — Do Not Omit Words or Use Contractions
