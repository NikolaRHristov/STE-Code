# Rule 2.1 — Keep Technical Nouns Short

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 2.1

> **Source:** [master.md#sec2-rule2.1](ste-code/grouped/)

> Source: master.md#sec2-rule2.1

## Original Rule

To keep multi-word nouns short, you can use prepositions (for example, "of," "on," "in," and "for") and explain the multi-word nouns.

#### Examples

> **Non-STE:** _Runway light connection resistance calibration._ (5 words)
>
> **STE:** Calibration of the resistance of the runway light connection. (1 word, 1 word, and 3 words)
>
> **Non-STE:** _Install the forward turbine overheat thermocouple terminal tags._ (6 words)
>
> **STE:** Install the terminal tags on the forward overheat thermocouple of the turbine. (2 words and 3 words)
>
> **Non-STE:** _Remove the engine transmission housing attachment bolts._ (5 words)
>
> **STE:** Remove the bolts that attach the transmission housing to the engine. (1 word, 1 word, 2 words, and 1 word)
>
> **Non-STE:** _Adjust to obtain door operating rod alignment with the attachment point._ (4 words)
>
> **STE:** Adjust the door operating rod until it aligns with the attachment point. (3 words and 1 word)

## Adapted Rule

To keep multi-word technical nouns short, use prepositions (for example, "of," "on," "in," and "for") and explain the multi-word technical nouns. Write each multi-word technical noun as a short noun that uses prepositions to make the meaning clear. A technical noun that the code domain uses (for example, a module name, a class name, or a configuration key) must stay short so that the reader can parse it without effort.

When a phrase names a code component with more than a few words, break the phrase into small nouns that connect with prepositions. Do not write one long noun that stacks modifiers. Explain the relationship between the parts with "of," "on," "in," or "for."

### Examples in STE-Code

> **Non-STE:** Authentication token expiration refresh interval setting. (5 words)
>
> **STE:** Setting of the refresh interval of the expiration of the authentication token. (1 word, 1 word, and 3 words)
>
> **Non-STE:** Install the forward service request validator middleware config tags. (6 words)
>
> **STE:** Install the config tags on the validator middleware of the request of the forward service. (2 words and 3 words)
>
> **Non-STE:** Remove the database migration script output directory lock files. (5 words)
>
> **STE:** Remove the lock files that lock the output directory of the migration script of the database. (1 word, 1 word, 2 words, and 1 word)
>
> **Non-STE:** Adjust to obtain cache invalidation hook alignment with the event emitter. (4 words)
>
> **STE:** Adjust the cache invalidation hook until it aligns with the event emitter. (3 words and 1 word)
