# Rule 3.5 — Use the "-ing" Form of a Verb Only as a Technical Noun or as a Modifier in a Technical Noun

## Original Rule Summary

Rule 3.5 restricts the "-ing" form of verbs to two specific functions: as a technical noun (used in procedural titles or headings such as "Cleaning," "Testing," "Troubleshooting") and as a modifier in a technical noun phrase (such as "air-conditioning system," "grinding wheel," "switching relay"). The "-ing" form must never appear as part of a compound verb tense (present progressive, past progressive) because the progressive aspect introduces ambiguity about when an action occurs. The ASD-STE100 dictionary permits only a small number of approved words with an "-ing" form: nouns (lighting, opening, routing, servicing), adjectives (mating, missing, remaining), the pronoun "something," and the preposition "during." All other "-ing" verb constructions must be rewritten using a simple tense or the imperative mood.

## STE-Code Adaptation

Rule 3.5 in STE-Code prohibits the "-ing" form in verb constructions across all code documentation — README files, API docs, docstrings, commit messages, error messages, and inline comments. The "-ing" form is permitted in only two code-domain contexts: as a technical noun in section titles or process names (Building, Testing, Deploying, Logging, Parsing, Routing) and as a modifier in a technical noun phrase that describes the function of a system or tool (building system, testing framework, routing module, logging service, rate-limiting gateway). When the "-ing" form appears as part of a compound verb ("is running," "was deploying," "are processing"), replace it with the simple present, simple past, or imperative mood. When an "-ing" participial phrase creates a long or ambiguous sentence, extract it into a separate sentence with a clear subject and a simple tense verb.

## Example Pairs

> **Non-STE:** When you are running the build command, check the terminal for error messages while the compiler is processing the source files.
>
> **STE:** When you run the build command, check the terminal for error messages. The compiler processes the source files.

>
> *(P4 applied: "are running" → "run" and "is processing" → "processes" — the progressive "-ing" forms are replaced with simple present and imperative. P3 applied: the single long sentence with two "-ing" constructions is split into two short sentences, each with one clear verb.)*

> **Non-STE:** Developers writing code without following the style guide can cause formatting conflicts and merge issues, leading to broken CI pipelines.
>
> **STE:** Obey the style guide when you write code. If you do not obey the style guide, formatting conflicts and merge issues can occur. These issues can cause CI pipelines to fail.

>
> *(P4 applied: "writing" and "following" as participial modifiers are restructured into simple verbs "write" and "obey." P3 applied: the single long sentence with three "-ing" forms is split into three short sentences. P9 applied: "leading to broken" is replaced with the clearer "can cause ... to fail.")*

> **Non-STE:** The script is processing all input files while logging results to the console and writing the summary to a report file.
>
> **STE:** The script processes all input files. It writes the results to the console. Then it writes the summary to a report file.

>
> *(P4 applied: "is processing," "logging," and "writing" are replaced with simple present "processes" and "writes." P3 applied: the single sentence with three simultaneous "-ing" actions is split into three sentences that show the sequence clearly. P12 applied: "processes" is a technical verb used in the approved simple present form.)*

## Principles Applied

**P4** — Use only approved verb and adjective forms. This is the primary principle for Rule 3.5. The "-ing" form is not an approved verb form. It may appear only as a technical noun in headings and process names (Building, Testing, Logging) or as a modifier in a technical noun phrase (testing framework, routing module). Every "-ing" form that functions as a verb — whether as part of a progressive tense ("is running"), as a participial modifier ("developers writing code"), or as a gerund subject ("Running the tests takes time") — must be rewritten using the simple present, simple past, or imperative mood.

**P2** — Use approved words only as the specified part of speech. Words with an "-ing" form that are approved as nouns (lighting, opening, routing, servicing) or adjectives (mating, missing, remaining) must stay in those roles. An approved "-ing" noun used as a verb ("The module is routing packets") violates the part-of-speech constraint. The same word in its approved noun role ("The routing module sends packets") is correct. Rule 3.5 and Rule 1.4 together define this boundary.

**P3** — Prefer the simpler construction. Sentences that contain "-ing" participial phrases are often long and complex because the "-ing" form packs multiple actions into a single clause. Replacing each "-ing" verb with a simple tense verb in its own sentence produces a sequence of short, clear statements. The reader no longer has to untangle which action is ongoing, which action depends on another, or what the temporal relationship between actions is.

**P12** — Technical verbs are allowed. Code-domain technical verbs such as run, build, test, deploy, parse, compile, serialize, and query are permitted in documentation when used in one of the six approved verb forms from Rule 3.2. A technical verb in the "-ing" form as part of a verb construction ("is compiling," "was deploying," "are serializing") violates Rule 3.5. The same technical verb in the simple present ("compiles," "deploys," "serializes") is correct. The rule restricts the form of the verb, not which technical verb you can use.
