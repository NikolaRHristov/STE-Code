# Rule 4.2 — Do Not Omit Words or Use Contractions

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.2
> **Source:** [master.md#sec4-rule4.2](ste-code/grouped/)
> Source: master.md#sec4-rule4.2

## Original Rule

Each sentence must have all its parts. When you write sentences, do not omit words or use contractions (for example, "don't," "isn't," "aren't"). If you do that, your sentence will be shorter, but it will not be easier to read. Write all the words in full.

Do not omit nouns to make short sentences. It will not be easy for the reader to understand the meaning of the sentence.

Do not omit verbs because the reader will not understand the action.

Do not omit the subject because the reader will not understand the action.

Do not omit articles to make the sentence shorter because omitted articles can cause ambiguity.

Do not omit parts of words to make contractions because contractions will not be easy to understand.


> *Adapted from spec pair:* Non-STE: The side stay assembly has two folding toggles hinged together and attached with hinges between the main gear strut and the side stay bracket. (This sentence contains more than one topic. To make this information clearer, you can write a new sentence for each topic.)  |  STE: <u>The side stay assembly has two folding toggles. The folding toggles are attached</u> together with hinges. These folding toggles are also attached with hinges between the main gear strut and the side stay bracket. (The new text has three sentences, and each sentence has its topic. Refer to the underlined text for the specified subjects in each sentence.)
### Examples:

> **Non-STE:** Can be a maximum of five inches long.
>
> **STE:** Cracks can have a maximum length of five inches.

> **Non-STE:** Rotary switch to INPUT.
>
> **STE:** Set the rotary switch to INPUT.

> **Non-STE:** If installed, remove the shims.
>
> **STE:** If shims are installed, remove them.

> **Non-STE:** WARNING: MAKE SURE THAT THE POTABLE WATER SYSTEM IS NOT PRESSURIZED. IF NOT, THIS CAN CAUSE INJURY TO PERSONS.
>
> **STE:** WARNING: MAKE SURE THAT THE POTABLE WATER SYSTEM IS NOT PRESSURIZED. A PRESSURIZED SYSTEM CAN CAUSE INJURY TO PERSONS.

> **Non-STE:** Remove the bolt and stop.
>
> **STE:** Remove the bolt and the stop.

> **Non-STE:** If your hands are wet, don't touch the USB power adapter.
>
> **STE:** If your hands are wet, do not touch the USB power adapter.

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** Rule 4.1 — One Topic Per Sentence, No Abstract Text
> **See also:** Rule 4.2 — Do Not Omit Words or Use Contractions
> **See also:** Rule 4.5 — Use an Article or a Demonstrative Adjective Before a Noun

## STE-Code Adaptation

Each sentence in code documentation must have all its parts. When you write sentences, do not omit words or use contractions (for example, "don't," "isn't," "aren't"). Write all words in full. A shorter sentence is not necessarily easier to read.

Do not omit nouns. If you omit a noun, the reader will not know which code element the sentence refers to.

Do not omit verbs. If you omit a verb, the reader will not understand the action that the code performs.

Do not omit the subject. If you omit the subject, the reader will not understand which function, class, or module performs the action.

Do not omit articles (the, a, an). If you omit an article, the sentence can become ambiguous about which code element is specified.

Do not use contractions. Write "do not" instead of "don't," "is not" instead of "isn't," and "are not" instead of "aren't."

### Code-Domain Examples

**Do not omit the subject:**

> **Non-STE:** Can be a maximum length of 256 characters.
>
> **STE:** The input string can have a maximum length of 256 characters.

**Do not omit the verb:**

> **Non-STE:** The return value a boolean that indicates success.
>
> **STE:** The return value is a boolean that indicates success.

**Do not omit the noun:**

> **Non-STE:** The function returns the parsed.
>
> **STE:** The function returns the parsed configuration object.

**Do not omit articles:**

> **Non-STE:** `validate` function checks input parameter.
>
> **STE:** The `validate` function checks the input parameter.

**Do not use contractions:**

> **Non-STE:** The method doesn't throw an exception when the input is null.
>
> **STE:** The method does not throw an exception when the input is null.

**Do not omit the subject in a safety statement:**

> **Non-STE:** BREAKING: MAKE SURE THAT THE DATABASE IS BACKED UP. IF NOT, THIS CAN CAUSE DATA LOSS.
>
> **STE:** BREAKING: MAKE SURE THAT THE DATABASE IS BACKED UP. A MISSING BACKUP CAN CAUSE DATA LOSS.

### Paradigm-Specific Guidance

- **Object-Oriented:** Method return descriptions often omit the subject. Write "The method returns…" Constructor documentation often omits the verb. Write "The constructor creates…"
- **Functional:** Pattern-match documentation often omits verbs. Write each arm as a full sentence with a verb. Type variable descriptions often omit subjects. Add a subject.
- **Procedural (C, Go, Bash):** Function synopses in headers often omit articles and subjects. Write "The function reads a configuration file."
- **Declarative (SQL, Terraform, YAML):** Comments often omit verbs and articles. Write each comment as a full sentence with a subject and a verb.
- **Systems (Rust, C memory):** Safety documentation with omitted subjects causes real bugs. Always write the subject, verb, and articles in full.

### Edge Cases

- **Commit message summary line:** The 72-character limit makes full sentences hard. The summary line may use a relaxed form. The body must follow the rule strictly.
- **CLI help text:** Terminal width limits cause omitted articles and subjects. The long-form documentation must use full sentences. The CLI help text may use a relaxed form.
- **When a code token is also a contraction:** A token such as `won't` (a test name) is a technical code noun. Keep it in backticks. Do not expand it.

### Grammar Notes

- Write "do not," "is not," "are not," "cannot," "will not" in full. Do not use apostrophe contractions.
- Every sentence needs a subject, a verb, and the required articles.

## Cross-References

- **Rule 1.1** — Use approved words from the STE-Code dictionary.
- **Rule 4.1** — Write short and clear sentences.
- **Rule 4.5** — Use an article or a demonstrative adjective before a noun.
- **Section 5 (Procedural Writing)** — Sentence structure for instructions.

## Summary Checklist

- [ ] Every sentence has a subject, a verb, and the required articles.
- [ ] No words are omitted to make the sentence shorter.
- [ ] No contractions are used.
- [ ] The reader knows which element performs the action.
