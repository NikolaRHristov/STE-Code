# Rule 9.4 — When You Select Terminology or Wording, Always Use a Consistent Style

## Original Rule Summary

When you select terminology or wording, always use a consistent style. In procedures, you frequently give the same type of instruction repeatedly. Use the same terminology or wording each time that type of instruction occurs so the reader identifies the pattern and quickly understands the action. Different terminology for the same thing causes confusion and delays. In descriptive writing, use words and sentences correctly and give a logical structure so the text is understood as a unit.

## STE-Code Adaptation

When you select terminology or wording in code documentation, always use a consistent style. In procedural code documentation, use the same terminology each time the same type of step occurs — the reader identifies the consistent wording and quickly understands the action. Use the same noun for the same item every time (do not alternate between "configuration file," "settings file," and "config") and use the same verb for the same action every time (do not alternate between "compile," "build," and "make"). In descriptive documentation, use words and sentences correctly and give a logical structure so the reader understands the text as a unit.

## Examples

> **Non-STE:** Open the configuration file in a text editor. Change the port number in the settings file. Save the config and close it.

>
> **STE:** Open the configuration file in a text editor. Change the port number in the configuration file. Save the configuration file and close it.
>
> *The non-STE text uses three different terms for the same file: "configuration file," "settings file," and "config." The STE text uses "configuration file" in all three steps.*

> **Non-STE:** Compile the project with the build command. Make the binary for the target platform. Construct the library for distribution.

>
> **STE:** Build the project with the build command. Build the binary for the target platform. Build the library for distribution.
>
> *The non-STE text uses three different verbs for the same action: "compile," "make," and "construct." The STE text uses "build" in all three steps.*

> **Non-STE:** `GET /items` — Retrieves all items. `POST /items` — Use this to create a new item. `GET /items/:id` — Gets item by ID. `DELETE /items/:id` — Removes the specified item.

>
> **STE:** `GET /items` — Returns all items. `POST /items` — Creates a new item. `GET /items/:id` — Returns the item with the specified ID. `DELETE /items/:id` — Removes the item with the specified ID.
>
> *The non-STE text uses inconsistent grammatical structures: third-person ("Retrieves"), imperative ("Use this"), bare verb ("Gets"), and passive phrasing. The STE text uses the same third-person singular verb template for every endpoint description.*

## Principles Applied

- **P1:** Use approved words from the controlled terminology — select one approved word for each concept and use it in every occurrence; "use" not "utilize," "start" not "initiate," "show" not "display."
- **P2:** Use approved words only as the specified part of speech — a word's approved part of speech must remain constant; do not use a noun as a verb or a verb as a noun inconsistently.
- **P3:** Use approved words only with their approved meanings — the approved meaning of each word is fixed; using the same word to mean different things in different places breaks semantic consistency.
- **P4:** Use the same grammatical structure for the same type of instruction — all setup steps, all configuration steps, and all verification steps share the same template so the structure signals the step type before the reader processes the content.
- **P5:** Use technical nouns consistently — framework-mandated terms like `ConfigMap`, `Pod`, and `props` are proper nouns with canonical forms; do not abbreviate, rephrase, or alternate them.
- **P11:** One term per concept — each concept maps to exactly one term across the entire document; synonymy is a defect, not a stylistic virtue, because every synonym forces the reader to pause and ask "is this the same thing or a different thing?"

---

*Adapted from ASD-STE100 Issue 9, Rule 9.4. See also: Rule 1.11 (One Term Per Concept), Rule 9.1 (Different Sentence Construction), Rule 9.2 (Use Each Approved Word Correctly).*
