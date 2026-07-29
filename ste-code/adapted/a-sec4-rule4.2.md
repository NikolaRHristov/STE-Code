# Rule 4.2 — Do Not Omit Words or Use Contractions to Make Your Sentences Shorter

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.2

## Original Rule

Each sentence must have all its parts. When you write sentences, do not omit words or use contractions (for example, "don't," "isn't," "aren't"). If you do that, your sentence will be shorter, but it will not be easier to read. Write all the words in full.

Do not omit nouns to make short sentences. It will not be easy for the reader to understand the meaning of the sentence.

Do not omit verbs because the reader will not understand the action.

Do not omit the subject because the reader will not understand the action.

Do not omit articles to make the sentence shorter because omitted articles can cause ambiguity.

Do not omit parts of words to make contractions because contractions will not be easy to understand.

## STE-Code Adaptation

Each sentence in code documentation must have all its parts. When you write sentences, do not omit words or use contractions (for example, "don't," "isn't," "aren't"). Write all words in full. A shorter sentence is not necessarily easier to read.

Do not omit nouns. If you omit a noun, the reader will not know which code element the sentence refers to.

Do not omit verbs. If you omit a verb, the reader will not understand the action that the code performs.

Do not omit the subject. If you omit the subject, the reader will not understand which function, class, or module performs the action.

Do not omit articles (the, a, an). If you omit an article, the sentence can become ambiguous about which code element is specified.

Do not use contractions. Write "do not" instead of "don't," "is not" instead of "isn't," and "are not" instead of "aren't."

### Examples

**Do not omit the subject:**

> **Non-STE:** Can be a maximum length of 256 characters.
> **STE:** The input string can have a maximum length of 256 characters.

**Do not omit the verb:**

> **Non-STE:** The return value a boolean that indicates success.
> **STE:** The return value is a boolean that indicates success.

**Do not omit the noun:**

> **Non-STE:** The function returns the parsed.
> **STE:** The function returns the parsed configuration object.

**Do not use contractions:**

> **Non-STE:** The method doesn't throw an exception when the input is null.
> **STE:** The method does not throw an exception when the input is null.

**Do not omit articles:**

> **Non-STE:** `validate` function checks input parameter.
> **STE:** The `validate` function checks the input parameter.
