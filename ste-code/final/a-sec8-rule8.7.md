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

> **See also:** Rule 8.2 — Use Hyphens (-) to Connect Words That Are Directly Related
> **See also:** Rule 8.6 — Elements That Count as One Word
> **See also:** Rule 8.7 — Hyphenated Words Count as One Word

## STE-Code Adaptation

**Rule 8.7** Hyphenated words count as one word.

Groups of words that are not usually adjectives but have the function of an adjective before a noun are hyphenated. Such groups of words count as one word.

In code documentation, this rule applies directly. A hyphenated technical term, whether it is a compound adjective or a long technical noun, counts as one word when you count words for sentence length.


> *Adapted from spec pair:* Non-STE: A value of 2 mm is acceptable. ("Acceptable" is not approved.)  |  STE: A value of 2 mm is permitted.
### Examples

> **Non-STE:** The build script uses a read only file descriptor to open the config for parsing.
>
> **STE:** The build script uses a read-only file descriptor to open the config for parsing.
>
> *Adapted from spec pair: "Clean the surface with a soap-and-water solution." → "read-only" is a hyphenated compound adjective and counts as one word.*

> **Non-STE:** Use the try and error method to calibrate the retry interval.
>
> **STE:** Use the trial-and-error method to calibrate the retry interval.
>
> *Adapted from spec pair: "Use the trial-and-error method." → "trial-and-error" is a hyphenated compound adjective and counts as one word.*

> **Non-STE:** The cutoff switch power connection must stay isolated during the test.
>
> **STE:** The cutoff-switch power connection must stay isolated during the test.
>
> *Adapted from spec pair: "Cutoff-switch power connection" (3 words). The hyphenated noun group counts as one word.*

> **Non-STE:** The main gear door retraction winch handle must lock before the door opens.
>
> **STE:** The main-gear-door retraction-winch handle must lock before the door opens.
>
> *Adapted from spec pair: "Main-gear-door retraction-winch handle" (3 words). The hyphenated noun group counts as one word.*

## Code-Domain Explanation

Rule 8.7 tells you how to count words when a term is hyphenated. The hyphen joins two or more words into a single unit that the reader processes as one concept. For word-count limits in STE-Code (Rules 4.1 and 4.2), a hyphenated unit counts as one word, not as the number of words inside it.

There are two cases.

### Case 1: Hyphenated compound adjectives

When a group of words describes a noun and sits before that noun, you hyphenate it. Examples from the spec: "soap-and-water solution," "trial-and-error method." The same pattern appears throughout code documentation:

- `read-only file descriptor` — "read-only" is one word.
- `thread-safe singleton` — "thread-safe" is one word.
- `event-driven architecture` — "event-driven" is one word.
- `low-latency cache` — "low-latency" is one word.

If you put the same words after the noun, do not hyphenate them: "the cache is low latency." Hyphenation is a pre-noun signal only. The word count does not change; the hyphen group still counts as one word.

### Case 2: Long hyphenated technical nouns

When a technical noun is long and the hyphen makes it easier to read, the whole hyphenated group counts as one word. Examples from the spec: "cutoff-switch power connection" (3 words: `cutoff-switch` / `power` / `connection`), "main-gear-door retraction-winch handle" (3 words: `main-gear-door` / `retraction-winch` / `handle`).

In the code domain, the same structure applies to compound identifiers that are written as words:

- `build-time environment variable` (3 words: `build-time` / `environment` / `variable`)
- `client-side rendering pipeline` (3 words: `client-side` / `rendering` / `pipeline`)
- `end-to-end test suite` (3 words: `end-to-end` / `test` / `suite`)

### Why this matters for word count

STE-Code limits procedural sentences to 20 words and descriptive sentences to 25 words (Rules 4.1, 4.2). If you count each word inside a hyphenated term, you over-report the sentence length and may break a limit that the sentence actually meets. Count the hyphenated unit as one word.

Example:

> **STE:** The build-time environment variable must point to the staging cluster. (9 words)

Word count: `The` (1) `build-time` (2) `environment` (3) `variable` (4) `must` (5) `point` (6) `to` (7) `the` (8) `staging` (9) `cluster` (10). The hyphenated `build-time` is one word. The sentence has 10 words, not 11.

### Interaction with Rule 8.2

Rule 8.2 tells you when to use a hyphen to connect directly related words. Rule 8.7 tells you how to count those words after you hyphenate them. The two rules work together: hyphenate per Rule 8.2, then count the hyphenated unit as one word per Rule 8.7.

### Interaction with Rule 8.6

Rule 8.6 lists elements that count as one word (numbers, units, abbreviations, alphanumeric identifiers, quoted text, titles, proper nouns). A hyphenated word is a separate case: it is not an abbreviation or an identifier, but it still counts as one word because the hyphen makes it a single unit. Do not double-count — a hyphenated term is one word under Rule 8.7, and it is not also an abbreviation or an identifier.

### Exception: hyphen in a numeral or a range

A hyphen that joins the parts of a spelled-out numeral (`twenty-one`, `forty-seven`) or marks a range (`pages 10-15`) is covered by Rule 8.6 (numbers count as one word) and by standard number counting. Rule 8.7 applies to hyphenated word groups that are adjectives or technical nouns, not to numerals.

> **STE:** Do steps 13 thru 16 a minimum of three times. (10 words — "13" and "16" each count as one word under Rule 8.6.)

This is distinct from "cutoff-switch power connection," which Rule 8.7 covers as a hyphenated noun group.

## Verification of the Adaptation

- Rule number preserved: 8.7.
- Each STE/non-STE pair replaced with a code-domain pair (`read only` → `read-only`, `try and error` → `trial-and-error`, `cutoff switch` → `cutoff-switch`, `main gear door retraction winch` → `main-gear-door retraction-winch`).
- No aerospace-domain terms outside the `## Original Rule` block.
- American English spelling, no contractions, no progressive or perfect tenses in the adapted text.
- Part of speech preserved: "hyphenated" (adjective), "count" (verb), "word" (noun) keep their STE source roles.
