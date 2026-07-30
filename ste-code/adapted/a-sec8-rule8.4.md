# Rule 8.4 — Colon in a Vertical List

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.4

## Original Rule

**Rule 8.4** In a vertical list, a colon (:) has the same effect on word count as a period and shows the end of a sentence.

In a vertical list, a colon (:) divides the first part of the sentence from the subsequent items in the vertical list. This colon has the effect of a period (full stop). Thus:

- In procedural sentences, you can use a maximum of 20 words before the colon.
- In descriptive sentences, you can use a maximum of 25 words before the colon.

Each item in a vertical list that comes after the colon counts as a new sentence. Thus, the limit for each item in a vertical list is:

- 20 words for procedural sentences
- 25 words for descriptive sentences.

> **STE:** To extinguish a possible fire, portable fire extinguishers are installed in these areas: (13 words)
>
> - The cockpit (2 words)
> - The cabin (2 words)
> - The cabin sub-compartment (3 words)
> - The crew rest compartment. (4 words)

## STE-Code Adaptation

**Rule 8.4** In code documentation, a colon (:) in a vertical list has the same effect on word count as a period and shows the end of a sentence.

In a vertical list, a colon (:) divides the first part of the sentence from the subsequent items in the vertical list. This colon has the effect of a period (full stop). Thus:

- In procedural sentences, you can use a maximum of 20 words before the colon.
- In descriptive sentences, you can use a maximum of 25 words before the colon.

Each item in a vertical list that comes after the colon counts as a new sentence. Thus, the limit for each item in a vertical list is:

- 20 words for procedural sentences
- 25 words for descriptive sentences.

### Examples

> **Non-STE:** To handle all possible error conditions, the following exception types must be caught and processed by the error handler: database connection timeouts which occur when the primary node is unreachable, authentication failures caused by expired or invalid tokens, and validation errors due to malformed request payloads.
>
> **STE:** To handle possible error conditions, the error handler catches these exception types:
>
> - Database connection timeout (3 words)
> - Authentication failure (2 words)
> - Validation error. (2 words)
>
> *Adapted from spec pair: "To extinguish a possible fire, portable fire extinguishers are installed in these areas:" followed by a vertical list of locations with word counts.*

> **Non-STE:** The configuration file, which is located in the project root, supports these environment profiles that you can use for deployment: a development profile for local testing and debugging, a staging profile for pre-production integration verification, and a production profile for the live customer-facing environment.
>
> **STE:** The configuration file supports these environment profiles:
>
> - Development (1 word)
> - Staging (1 word)
> - Production. (1 word)
>
> *Adapted from spec pair: vertical list with colon introducing enumerated items, each counted as a separate sentence.*
