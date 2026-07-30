# Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 9.1

## Original Rule

Use a different sentence construction to write a sentence when a word-for-word replacement is not sufficient.

STE is a controlled natural language with a controlled dictionary. To help you use the approved words correctly, the dictionary gives approved alternatives for words that are not approved. If you find an alternative that has the same part of speech, you can use it to replace the word that is not permitted (a word-for-word replacement).

When you replace a word, always make sure that the alternative that you select does not change the meaning of the sentence. If the meaning changes, or if the alternative does not have the same part of speech, you must use a different sentence construction.

A different sentence construction is necessary because:

1. You must change the grammatical structure of the sentence to use the alternative that you selected.
2. The word-for-word replacement of the word that is not approved gives a meaningless result.
3. The approved alternative that you find changes the meaning of the sentence.
4. The word that you must replace is not in the dictionary.

## STE-Code Adaptation

> **See also:** Rule 9.2 — Use Each Approved Word Correctly; Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs; Rule 9.4 — When You Select Terminology or Wording, Always Use a Consistent Style

Use a different sentence construction to write a sentence when a word-for-word replacement is not sufficient.

In code documentation, when a word is not approved in the controlled terminology, the dictionary gives approved alternatives. If the alternative has the same part of speech and does not change the meaning, you can do a word-for-word replacement. If the meaning changes, the part of speech differs, or a word-for-word replacement gives a meaningless result, you must write a new sentence with a different structure that uses only approved words while keeping the same technical meaning.

A different sentence construction is necessary because:

1. You must change the grammatical structure to use the approved alternative.
2. The word-for-word replacement gives a meaningless or unclear result.
3. The approved alternative changes the meaning of the sentence.
4. The word to replace is not in the controlled terminology.

When you cannot do a word-for-word replacement, think about the purpose of the sentence and use different words to get the same result. Frequently, you must select different words, use different verb forms, write shorter sentences, remove information that is not necessary, or get more information from a developer.

### Examples

> **Non-STE:** A timeout value of 5000 ms is acceptable for this endpoint.
>
> **STE:** A timeout value of 5000 ms is permitted for this endpoint.

("Acceptable" is not approved. The approved adjective "permitted" has the same part of speech and does not change the meaning, so a word-for-word replacement is sufficient.)
*Adapted from spec pair: "A value of 2 mm is acceptable." / "A value of 2 mm is permitted."*

> **Non-STE:** The stack trace in the console must be visible during the debugging session.
>
> **STE:** During the debugging session, make sure that you can see the stack trace in the console.

(The approved verb "see" replaces the adjective "visible." To use the verb "see," replace "must be" with "make sure that you can.")
*Adapted from spec pair: "The oil level on the sight gauge must be visible during the test." / "During the test, make sure that you can see the oil level on the sight gauge."*

> **Non-STE:** Loop the function twice to remove null values from the array.
>
> **STE:** Run the function for two iterations to remove null values from the array.

(The approved noun "iteration" together with the approved verb "run" replaces the verb "loop." The technical noun "two" replaces the adverb "twice.")
*Adapted from spec pair: "Cycle the unit twice to remove air from the lines." / "Operate the unit for two cycles to remove air from the lines."*

> **Non-STE:** Without this configuration change, the behavior of the function can be uncertain.
>
> **STE:** Without this configuration change, it is possible that the function will not behave as expected.

("Uncertain" is not in the controlled terminology. A word-for-word replacement such as "cannot be sure" or "cannot be known" gives a meaningless result. You must think about the meaning and write a new sentence.)
*Adapted from spec pair: "Without this modification, the service life of the unit can be uncertain." / "Without this modification, it is possible that the service life of this unit will be shorter than usual."*

> **Non-STE:** Just add a single log statement to the method.
>
> **STE:** Only add a single log statement to the method.
>
> NOT: Immediately add a single log statement to the method.

("Immediately" is the approved alternative for "just." But if you use it in this context, the meaning of the instruction changes.)
*Adapted from spec pair: "Just apply very light pressure to the surface." / "Only apply very light pressure to the surface." NOT: "Immediately apply very light pressure to the surface."*

> **Non-STE:** The occurrence of type errors in the build output is a serious problem.
>
> **STE:** Type errors in the build output are a serious problem.

("Occurrence" is not in the controlled terminology. You must think of a different construction that keeps the same meaning without the unapproved word.)
*Adapted from spec pair: "The incidence of water in fuel is dangerous." / "Water in fuel is dangerous."*

> **Non-STE:** Scroll the editor pane so that it clears the minimap overlay.
>
> **STE:** Scroll the editor pane until it is away from the minimap overlay.
>
> NOT: Scroll the editor pane so that it cleans the minimap overlay.

("Clear" is not an approved verb. Its only alternative in the controlled terminology is "clean" as a verb, but "clean" does not have the intended meaning in this context. The intended meaning is "to increase the distance between" — use "until it is away from.")
*Adapted from spec pair: "Lift the seat so that it clears the track locks." / "Lift the seat until it is away from the track locks." NOT: "Lift the seat so that it cleans the track locks."*

> **Non-STE:** If linting errors are detected during this procedure, the developer must perform the correction within a certain number of commits depending on error severity. Refer to following table:
>
> | Error severity detected | Time before correction |
> |---|---|
> | Critical | 1 commit |
> | Major | 3 commits |
> | Minor | 5 commits |

> **STE:** If you find linting errors, refer to the table that follows:
>
> | If the error is of this severity | Do the correction before |
> |---|---|
> | Critical | 1 commit |
> | Major | 3 commits |
> | Minor | 5 commits |

(In the non-STE example: the underlined words are not approved; the verb form "are detected" is passive; the first sentence is too long; an article is missing before "following table"; the instruction is not imperative. The STE version uses approved words, active voice, imperative form, and moves the instruction into the table heading to avoid repeating information.)
*Adapted from spec pair: the crack detection and repair table example using "If you find cracks, refer to the table that follows:" — see spec pages 117–119 for the full original.*
