# Rule 1.7 — Do Not Use Words That Are Technical Nouns as Verbs

## Original Rule Summary

Rule 1.7 prohibits using words that are technical nouns as verbs. A word that belongs in a technical noun category (Rule 1.5) must be used only as a noun or as an adjective modifying another technical noun — never as the main verb of a clause. The writer must use a different sentence construction, typically an approved verb followed by the technical noun in a prepositional phrase. Some words like "drill" appear in both a technical noun category and a technical verb category (Rule 1.12); in that case the verb use is permitted only in the approved verb sense and context.

## STE-Code Adaptation

Rule 1.7 in STE-Code prohibits using code-domain technical nouns as verbs in code documentation. Words like "database," "cache," "Docker," "interface," "buffer," and "queue" are code-domain technical nouns that must remain as nouns — "Store the records in the database" is correct, "Database the records" is a violation. The standard repair pattern uses an approved verb (store, put, add, make, write, send) with the technical noun inside a prepositional phrase (in, to, through, with, as). When a word is cataloged in both a code-domain technical noun category (Rule 1.5) and a code-domain technical verb category (Rule 1.12) — such as "log" or "cache" — the verb use is permitted only in the approved verb context and only when the project glossary lists the word in both roles.

## Example Pairs

> **Non-STE:** Database the user records before the migration.
>
> **STE:** Store the user records in the database before the migration.
>
> *(P7 applied: "database" is a code-domain technical noun, category 18 — do not use it as a verb. P1 applied: "store" is an approved verb from the controlled terminology. The preposition "in" establishes the containment relationship between the records and the database. This adapts the spec pair "Oil the steel surfaces" → "Apply oil to the steel surfaces.")*

> **Non-STE:** To Docker the application, first Git the repository and then npm the dependencies.
>
> **STE:** To containerize the application, first clone the repository and then install the dependencies.
>
> *(P7 applied: "Docker," "Git," and "npm" are tool names and code-domain technical nouns — do not use them as verbs. P8 applied: use standard technical nouns. P12 applied: "containerize" is a code-domain technical verb (category 1 c), "clone" is a code-domain technical verb (category 2 c), and "install" is a code-domain technical verb (category 2 c). The tool names stay as nouns; the approved verbs carry the action.)*

> **Non-STE:** Interface the payment module with the order system.
>
> **STE:** Add an interface between the payment module and the order system.
>
> *(P7 applied: "interface" is a code-domain technical noun (category 6, systems and architectural components) — do not use it as a verb. P1 applied: "add" is an approved verb from the controlled terminology. P13 applied: the construction "between X and Y" follows the STE pattern for two entities. The technical noun "interface" stays as a noun; the approved verb "add" names the action.)*

## Principles Applied

**P7** — Do not use technical nouns as verbs (Rule 1.7). This is the primary principle: every code-domain technical noun — whether a tool name, data structure, architecture concept, protocol, or brand name — must stay as a noun. The fix pattern uses an approved verb with the technical noun in a prepositional phrase.

**P1** — Use approved words from the controlled terminology. When a noun-verb is prohibited by Rule 1.7, the replacement must use an approved verb from the dictionary: "store," "put," "add," "make," "write," "send," "apply," "use." The approved verb names the specific action that the noun-verb obscured.

**P8** — Use standard, well-known technical nouns. When you keep a code-domain technical noun as a noun, use its standard form. Do not drop part of a multi-word technical noun to make a verb ("load balance" from "load balancer" is a violation).

**P12** — Technical verbs are allowed (Rule 1.12). When a word is cataloged in both a code-domain technical noun category and a code-domain technical verb category, the verb use is permitted in the approved verb context. Words like "log," "cache," "queue," "filter," and "map" are dual-category words — their verb use is correct only when the project glossary lists them in both roles.

**P11** — One term per concept. When you choose an approved verb to replace a noun-verb, use the same approved verb consistently across all documentation for the same action. Do not use "store" in one file and "put" in another for the same operation.
