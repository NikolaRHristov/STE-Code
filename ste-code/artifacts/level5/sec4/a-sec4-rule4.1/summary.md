# Rule 4.1 — Write Short and Clear Sentences

## Original Rule Summary

Rule 4.1 requires that every sentence be short, clear, and accurate. In procedures, give short instructions directly to the reader using the imperative form. In descriptive text, each sentence must cover only one topic, with no imperative mood, and information must be delivered gradually across the sentences that follow. Text must never be abstract — it must clearly show how to do a task or how a system operates, with no ambiguous or inaccurate information.

## STE-Code Adaptation

Rule 4.1 in STE-Code requires short, clear sentences in all code documentation. In procedural writing (API methods, function descriptions, setup instructions), use the imperative mood and limit each step to one action and a maximum of 20 words. In descriptive writing (class summaries, module overviews, type descriptions), limit each sentence to one topic and a maximum of 25 words, with no imperative mood. All documentation must avoid abstract statements — it must clearly show how to use a function or how a module operates, with accurate and unambiguous information.

## Example Pairs

> **Non-STE:** To call the `initialize` method, first pass the three configuration parameters that set up the connection to the database, and then, after calling the method, check the return value for a success code or an error object.
>
> **STE:**
> 1. Call the `initialize` method as follows:
>    A. Pass the three configuration parameters that set the connection to the database.
>    B. Call the method.
>    C. Check the return value. The return value is a success code or an error object.

> **Non-STE:** The `HttpClient` class has two internal buffers connected together and linked with callbacks between the request handler and the response dispatcher.
>
> **STE:** The `HttpClient` class has two internal buffers. The internal buffers are connected together with callbacks. These callbacks link the request handler to the response dispatcher.

> **Non-STE:** No null values are permitted.
>
> **STE:** Make sure that the function does not return a null value.

## Principles Applied

**P1** — Use approved words from the controlled terminology. Short sentences are easier to write and read when every word is approved and unambiguous.

**P2** — Use only the approved parts of speech for each word. This prevents structural ambiguity that lengthens sentences.

**P3** — Use words only with their approved meanings. Accurate word meaning removes the need for clarifying clauses.

**P4** — Write one topic per descriptive sentence. Each sentence addresses a single subject or idea, with no nested clauses deeper than 2 levels.

**P5** — Write one instruction per procedural step. Each work step describes exactly one action and starts with an imperative verb (call, pass, set, get, check, run).

**P7** — Use the imperative mood for all procedural writing. Do not use "you should," "you must," or "the user should." Start each step with the base form of the verb.

**P13** — Do not use semicolons to join independent clauses. Use a period and start a new sentence. Use "and" or "but" only for two short, closely related clauses within the 25-word limit.

**P14** — Make sure documentation is not abstract. Every sentence must clearly show how to do a task or how a system operates. Do not give information that is inaccurate or has multiple meanings.
