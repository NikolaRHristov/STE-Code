# Rule 1.7 — Do Not Use Words That Are Technical Nouns as Verbs

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.7

## Original Rule

**Rule 1.7** Do not use words that are technical nouns as verbs.

Use a technical noun only as a noun or as an adjective that is part of a different technical noun. Do not use the same word as a verb.

Examples:

"Oil" is a technical noun, category 4, materials, consumables, and unwanted material. Do not use "oil" as a verb. Use a different sentence construction that lets you use "oil" as a technical noun.

> **Non-STE:** Oil the steel surfaces.
> **STE:** Apply oil to the steel surfaces.

"Snow" is a technical noun, category 16, environmental and operational conditions. Do not use "snow" as a verb. Use a different sentence construction that lets you use "snow" as a technical noun.

In some contexts, the same word can be a technical noun and a technical verb. This condition occurs when you can put this word in a technical noun category (rule 1.5) and in a technical verb category (rule 1.12).

> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category

> **See also:** Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category

"Drill" is a technical noun, category 3, tools and support equipment, their parts, and locations on them.

> **STE:** Drill a hole at the intersection of the two lines.

("Drill" is a technical verb, rule 1.12, category 1 a), manufacturing processes, remove material.)

## STE-Code Adaptation

**Rule 1.7** Do not use words that are code-domain technical nouns as verbs.

Use a code-domain technical noun only as a noun or as an adjective that is part of a different code-domain technical noun. Do not use the same word as a verb. Use a different sentence construction that lets you use the word as a code-domain technical noun.

"Database" is a code-domain technical noun, category 18, database and storage terminology. This adapts the spec example where "oil" is a technical noun (category 4, materials). Do not use "database" as a verb. Use a different sentence construction that lets you use "database" as a code-domain technical noun.

> **Non-STE:** Database the user records before the migration.
> **STE:** Store the user records in the database before the migration.

This adapts the spec pair: "Oil the steel surfaces" becomes "Apply oil to the steel surfaces." Just as you cannot use "oil" as a verb in STE, you cannot use "database" as a verb in STE-Code. The STE version uses the approved verb "store" (analogous to "apply") and keeps "database" as a code-domain technical noun.

"Cache" is a code-domain technical noun, category 16, computer science, information and communication technology. This adapts the spec example where "snow" is a technical noun (category 16, environmental and operational conditions). Both "snow" and "cache" are technical nouns in their respective domains that must not be used as verbs.

> **Non-STE:** Cache the API responses to improve performance.
> **STE:** Store the API responses in the cache to improve performance.

In some contexts, the same word can be a code-domain technical noun and a code-domain technical verb. This condition occurs when you can put this word in a code-domain technical noun category (rule 1.5) and in a code-domain technical verb category (rule 1.12). This adapts the spec example where "drill" can be both a technical noun (a tool) and a technical verb (a manufacturing process).

> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category

> **See also:** Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category

> **STE:** Write a log entry for each failed request.

("Log" is a code-domain technical noun, category 18, database and storage terminology.)

> **STE:** Log each failed request.

("Log" is a code-domain technical verb, rule 1.12, category 2 c), computer processes and applications, system operations.)

### Examples

> **Non-STE:** Cache the API responses to improve performance.
> **STE:** Store the API responses in the cache to improve performance.

> *Adapted from spec pair: "Oil the steel surfaces" / "Apply oil to the steel surfaces."* Just as you cannot use "oil" as a verb in STE, you cannot use "cache" as a verb in STE-Code. The STE version uses the approved verb "store" and keeps "cache" as a code-domain technical noun.

> **Non-STE:** Database the user records before the migration.
> **STE:** Store the user records in the database before the migration.

> *Adapted from spec pair: "Oil the steel surfaces" / "Apply oil to the steel surfaces."* Just as "oil" is only a noun in STE, "database" is only a code-domain technical noun in STE-Code. The STE version uses the approved verb "store" with the code-domain technical noun "database."
