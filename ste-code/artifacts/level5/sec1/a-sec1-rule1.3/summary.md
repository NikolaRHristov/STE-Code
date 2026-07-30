# Rule 1.3 — Use Approved Words Only with Their Approved Meanings

## Original Rule Summary

Rule 1.3 specifies that each approved word in the dictionary has exactly one approved meaning, and writers must use that meaning — not the word's broader standard-English meanings. Some approved words carry more restricted meanings than they do in general English. The rule gives the example of "follow," which is approved only in the sense "come after, go after." When the writer needs to express "act in accordance with instructions," the rule requires "obey" instead.

## STE-Code Adaptation

Rule 1.3 applies with equal force to code documentation. Each approved word in the controlled terminology carries a single approved meaning; using it in a general-English sense that differs creates ambiguity. High-risk words include "run" (approved: "execute a program" — not "operate"), "return" (approved: "send a value back from a function" — not "go back"), and "raise" (approved: "cause an exception" — not "increase"). When an approved word does not carry the intended meaning, the writer must substitute a different approved word or restructure the sentence. This rule is the semantic backbone of STE-Code: vocabulary control (Rule 1.1) tells you which words to use, and Rule 1.3 tells you what each word is allowed to mean.

## Examples

> **Non-STE:** The function runs a validation check, returns the result, and raises the retry limit if the check fails.
>
> **STE:** The function does a validation check, gives the result, and increases the retry limit if the check does not complete. *(P3 applied: "runs" → "does" — "run" means "execute a program," not "perform"; "returns" → "gives" — "return" means "send a value back from a function," the prose describes delivering a result; "raises" → "increases" — "raise" means "cause an exception," not "make larger"; "fails" → "does not complete" — uses the approved meaning of "fail" but restructured for clarity)*

>
> **Non-STE:** Set the `debug` flag to true to run the server in verbose mode. The server returns a detailed report when it finishes.
>
> **STE:** Set the `debug` flag to `true` to operate the server in detailed mode. The server gives a detailed report when it completes. *(P3 applied: "run" → "operate" — "run" means "execute," not "operate in a mode"; "returns" → "gives" — the server gives a report to the client, "return" is for function-to-caller value transfer; "verbose" → "detailed" — "verbose" is an approved adjective but "detailed" is more precise; "finishes" → "completes" — "finish" means "bring to an end," "complete" means "an operation finished successfully")*

>
> **Non-STE:** The connection failed: the server refused to make the handshake. Call the admin if the error returns.
>
> **STE:** The connection did not complete: the server refused the handshake. Tell the administrator if the error occurs again. *(P3 applied: "failed" → "did not complete" — "fail" means "did not complete successfully"; "make" → removed — "make" means "bring into existence by building," not "perform"; "call" → "tell" — "call" means "invoke a function," not "contact a person"; "admin" → "administrator" — abbreviation expanded per Rule 1.5; "returns" → "occurs again" — "return" means "send a value back," not "happen again")*

## Principles Applied

P1: Use approved words from the controlled terminology
P3: Use approved words only with their approved meanings
