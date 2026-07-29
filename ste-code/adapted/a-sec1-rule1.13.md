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

In English, words that look the same do not always have the same function in a sentence. Use code-domain technical verbs only as verbs, not as nouns. If you need to use a word as a noun, find an approved noun or a code-domain technical noun that has the equivalent meaning.

In some contexts, the same word can be a code-domain technical verb and a code-domain technical noun. This condition occurs when you can put this word in a code-domain technical verb category (rule 1.12) and in a code-domain technical noun category (rule 1.5).

### Examples

> **Non-STE:** Do a compile of the source files.
> **STE:** Compile the source files.

"Compile" is a code-domain technical verb (category 1 a), development processes, write and modify code). The non-STE version uses "compile" as a noun, which is not permitted. The STE version uses "compile" correctly as a verb.

> **Non-STE:** The merge of the feature branch caused a conflict.
> **STE:** The merge operation of the feature branch caused a conflict.

"Merge" is a code-domain technical verb (category 1 c), development processes, build and package). In the non-STE example, "merge" is used as a noun. The STE version uses "merge" as an adjective that is part of the code-domain technical noun "merge operation."

> **STE:** Run the deploy script.

("Deploy" is a code-domain technical verb, category 1 c), development processes, build and package.)

> **STE:** The deploy completed successfully.

("Deploy" is a code-domain technical noun (category 5, infrastructure, deployment, and platforms). In this context, "deploy" refers to a deployment event or process.)

"Deploy" can be both a code-domain technical verb and a code-domain technical noun because it fits into both category systems. When used as a verb, it follows rule 1.12. When used as a noun, it follows rule 1.5.
