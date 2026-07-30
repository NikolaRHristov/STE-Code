# Rule 1.2 — Use Approved Words Only as the Specified Part of Speech

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.2

## Original Rule

**Rule 1.2** Use approved words from the dictionary only as the specified part of speech.

In the dictionary, each approved word has a specified part of speech. When you use an approved word, make sure that you use it only as the specified part of speech.

Examples:

"Test" is an approved noun, but not an approved verb.

> **STE:** Test B is an alternative to test A.

> **Non-STE:** Test the system for leaks.
> **STE:** Do the leak test of the system.

or

> **STE:** Do a test for leaks in the system.

"Dim" is an approved adjective, but not an approved verb.

Some words are approved as more than one part of speech. For example, "clean" is an approved verb and an approved adjective. The position of the word in the sentence shows its function (and its meaning) because verbs and adjectives have different positions.

"Acceptable" is an adjective that is not approved. The dictionary gives three approved alternatives that have the same part of speech. You can use one of these alternatives to replace the word "acceptable" in the sentence with a word-for-word replacement.

"Operable" is an adjective that is not approved. The dictionary gives an approved alternative that has a different part of speech: "operate" as a verb. Thus, you must use a different sentence construction.

When you replace a word, always make sure that the approved alternative you select does not change the meaning of the sentence. If the meaning changes, select a different word or use a different sentence construction.

Each word in the dictionary has its part of speech in parentheses, abbreviated as specified in the introduction to the dictionary.

If a word that you want to use is not in the dictionary:
1. Find that word in an English dictionary.
2. Find which is the best synonym that is approved in the STE dictionary.
3. Use the approved STE word or find a different sentence construction with other approved words.

## STE-Code Adaptation

**Rule 1.2** Use approved words from the controlled terminology only as the specified part of speech.

In the controlled terminology, each approved word has a specified part of speech. When you use an approved word, make sure that you use it only as the specified part of speech.

"Query" is an approved noun, but not an approved verb. This adapts the spec example where "test" is an approved noun but not an approved verb: just as you cannot write "test the system" in STE, you cannot write "query the database" in STE-Code.

"Static" is an approved adjective, but not an approved verb. This adapts the spec example where "dim" is an approved adjective but not an approved verb: just as you cannot use "dim" as a verb in STE, you cannot use "static" as a verb in STE-Code.

Some words are approved as more than one part of speech. For example, "call" is an approved verb and an approved noun. This adapts the spec example where "clean" is an approved verb and an approved adjective: just as the position of "clean" in the sentence shows whether it is a verb or an adjective, the position of "call" shows whether it is a verb (to call a function) or a noun (a function call).

When you replace a word, always make sure that the approved alternative you select does not change the meaning of the sentence. If the meaning changes, select a different word or use a different sentence construction.

If a word that you want to use is not in the controlled terminology:
1. Find that word in a standard English dictionary.
2. Find which is the best synonym that is approved in the STE-Code controlled terminology.
3. Use the approved STE-Code word or find a different sentence construction with other approved words.

### Examples

> **Non-STE:** Query the database for user records.
> **STE:** Send a query to the database for user records.

> *Adapted from spec pair: "Test the system for leaks" → "Do the leak test of the system." Just as "test" is only an approved noun in STE and cannot be used as a verb, "query" is only an approved noun in STE-Code. The STE version uses the approved verb "send" with the approved noun "query."*

> **Non-STE:** Static the variable to prevent modification.
> **STE:** Make the variable static to prevent modification.

> *Adapted from spec example: "dim" is an approved adjective but not a verb. Just as you cannot use "dim" as a verb in STE, you cannot use "static" as a verb in STE-Code. The STE version uses the approved verb "make" with the approved adjective "static."*
