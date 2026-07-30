# Rule 1.13 — Do Not Use Technical Verbs as Nouns

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.13

## Original Rule

**Rule 1.13** Do not use technical verbs as nouns.

In English, words that look the same do not always have the same function in a sentence. Use technical verbs only as verbs, not as nouns.

Example:

> **STE:** Enter your password.

("Enter" is a technical verb, category 2 a), computer processes and applications, input and output processes.)

Words that can be technical verbs and technical nouns

In some contexts, the same word can be a technical verb and a technical noun. This condition occurs when you can put this word in a technical verb category (rule 1.12) and in a technical noun category (rule 1.5).

> **STE:** There are two methods to plate the ring nut (2).

("Plate" is a technical verb, category 1 c), manufacturing processes, attach material.)

## STE-Code Adaptation

**Rule 1.13** Do not use code-domain technical verbs as nouns.

> **See also:** Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category
> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category

In English, words that look the same do not always have the same function in a sentence. Use code-domain technical verbs only as verbs, not as nouns. If you need to use a word as a noun, find an approved noun or a code-domain technical noun that has the equivalent meaning.

This adapts the spec principle: just as you cannot use "enter" as a noun in STE (you must use it only as a verb, as in "Enter your password"), you cannot use code-domain technical verbs as nouns in STE-Code.

In some contexts, the same word can be a code-domain technical verb and a code-domain technical noun. This condition occurs when you can put this word in a code-domain technical verb category (rule 1.12) and in a code-domain technical noun category (rule 1.5). This adapts the spec example where "plate" can be a technical verb (a manufacturing process) — the spec explicitly acknowledges that some words can belong to both category systems.

### Examples

> **Non-STE:** Do a compile of the source files.
> **STE:** Compile the source files.

> *Adapted from spec example: "Enter your password" — "enter" must be used only as a verb. Just as you cannot use "enter" as a noun in STE, you cannot use "compile" as a noun in STE-Code. "Compile" is a code-domain technical verb (category 1 a), development processes, write and modify code). The non-STE version uses "compile" as a noun, which is not permitted. The STE version uses "compile" correctly as a verb.*

> **Non-STE:** The merge of the feature branch caused a conflict.
> **STE:** The merge operation of the feature branch caused a conflict.

> *Adapted from spec principle: technical verbs must be used only as verbs. "Merge" is a code-domain technical verb (category 1 c), development processes, build and package). The non-STE example uses "merge" as a noun. The STE version uses "merge" as an adjective that is part of the code-domain technical noun "merge operation."*

> **STE:** Run the deploy script.

("Deploy" is a code-domain technical verb, category 1 c), development processes, build and package.)

> **STE:** The deploy completed successfully.

> *Adapted from spec example: "There are two methods to plate the ring nut (2)" — "plate" can be both a technical verb and a technical noun. Just as "plate" in the spec can be a technical verb (category 1 c), attach material) and also a technical noun (a different context), "deploy" can be both a code-domain technical verb (category 1 c), build and package) and a code-domain technical noun (category 5, infrastructure, deployment, and platforms). In the second example, "deploy" refers to a deployment event or process as a noun — it fits into a code-domain technical noun category in the same way "plate" fits into a technical noun category in the spec.*
