# Rule 8.5 — Parentheses and Word Count

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.5

## Original Rule

**Rule 8.5** When you put text in parentheses, it counts as one word in that sentence.

When you count words for sentence length, text in parentheses counts as one word of that sentence. But the words that you put between parentheses also make a new sentence. Thus, count them in that different sentence.

> **STE:** Make sure that the EMER pushbutton switch is released (the EMER legend is off).

(This sentence has 10 words, because the text in parentheses counts as one word. The sentence in parentheses has 5 words and counts as a different sentence.)

If there is an identifier in parentheses (a number, a letter, or an alphanumeric identifier), this identifier counts as one word in the sentence. Abbreviations in parentheses also count as one word.

> **STE:** Remove the safety pin (10). (5 words)
> **STE:** Installation of a Business Class (B/C) Seat (7 words)

| Example | Text |

|---------|------|

| | Hardware and Software Configuration Check of the In-Flight Entertainment (IFE) System (11 words) |

## STE-Code Adaptation

**Rule 8.5** In code documentation, when you put text in parentheses, it counts as one word in that sentence.

When you count words for sentence length, text in parentheses counts as one word of that sentence. But the words that you put between parentheses also make a new sentence. Thus, count them in that different sentence.

If there is an identifier in parentheses (a number, a letter, or an alphanumeric identifier), this identifier counts as one word in the sentence. Abbreviations in parentheses also count as one word.

### Examples

> **Non-STE:** Make sure that the DEBUG environment variable is set to false before you run the deployment script in the production cluster (the DEBUG flag must be explicitly disabled for all production workloads to prevent accidental log leakage).
> **STE:** Make sure that the DEBUG environment variable is set to false (the DEBUG flag is off). (12 words)
>
> *Adapted from spec pair: "Make sure that the EMER pushbutton switch is released (the EMER legend is off)." — text in parentheses counts as one word in the main sentence but forms a separate sentence.*

(This sentence has 12 words, because the text in parentheses counts as one word. The sentence in parentheses has 5 words and counts as a different sentence.)

> **Non-STE:** Remove the health check flag number ten from the deployment configuration.
> **STE:** Remove the health check flag (10). (5 words)
>
> *Adapted from spec pair: "Remove the safety pin (10)." — identifier in parentheses counts as one word.*

> **Non-STE:** Installation and Configuration of a Continuous Integration and Continuous Deployment Pipeline for the Application
> **STE:** Configuration of a Continuous Integration/Continuous Deployment (CI/CD) Pipeline (7 words)
>
> *Adapted from spec pair: "Installation of a Business Class (B/C) Seat" — abbreviation in parentheses counts as one word.*
