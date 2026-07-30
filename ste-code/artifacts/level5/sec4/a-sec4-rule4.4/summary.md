# Rule 4.4 — Use Connecting Words and Connecting Phrases to Connect Sentences That Contain Related Topics

## Original Rule Summary

Rule 4.4 requires that connecting words and connecting phrases link a topic in one sentence with an idea in the sentence that follows. In descriptive text, these connectors give writing a logical structure and make information easy to understand. Approved connecting words include "and," "but," "then," and "thus"; approved connecting phrases include "as a result" and "at the same time." Demonstrative adjectives ("this," "these") can also serve as connecting words to refer back to a topic introduced in the previous sentence, and connectives are permitted in procedures when an explanation follows a work step or when safety instructions require related sentences.

## STE-Code Adaptation

Rule 4.4 in STE-Code applies the connecting-words principle across all code documentation types — README files, API documentation, docstrings, commit messages, and error messages. Writers must use approved connecting words ("and," "but," "then," "thus") and connecting phrases ("as a result," "at the same time") to show logical relationships between sentences instead of leaving the reader to infer the connection. Demonstrative adjectives ("this," "these") must refer back to a specific code element, class, function, or concept named in the previous sentence, never to a vague or implied antecedent. In procedural documentation, connecting words join a work step to its explanation or to a safety instruction; in descriptive documentation, they scaffold architectural overviews, parameter descriptions, and error recovery guidance into a coherent logical flow.

## Example Pairs

> **Non-STE:** The `AuthService` authenticates the request token. If the token is valid, the middleware forwards the request to the route handler. The route handler processes the business logic and returns a response.
>
> **STE:** The `AuthService` authenticates the request token. **Then**, if the token is valid, the middleware forwards the request to the route handler. **And** the route handler processes the business logic, **thus** returning a response.

> **Non-STE:** Configure the connection pool in the database client. The pool size limits the number of concurrent queries. Exceeding the limit causes connection timeouts on new requests.
>
> **STE:** Configure the connection pool in the database client. **This** pool size limits the number of concurrent queries. **As a result**, if the limit is exceeded, new requests get connection timeouts.

> **Non-STE:** The `mergeConfig` function applies default settings. The function does not overwrite user-specified values for keys that already exist. The function returns a new object instead of mutating the input parameters.
>
> **STE:** The `mergeConfig` function applies default settings. **But** the function does not overwrite user-specified values for keys that already exist. **Thus**, the function returns a new object instead of mutating the input parameters.

## Principles Applied

**P4** — Write one topic per descriptive sentence. Connecting words and phrases show the relationship between the topic of one sentence and the topic of the next sentence. Without connectors, a paragraph becomes a list of disconnected facts — the reader must infer whether sentence B is a consequence, a contrast, an addition, or a sequence relative to sentence A. Approved connecting words ("and," "but," "then," "thus") and phrases ("as a result," "at the same time") make these relationships explicit so that each sentence's topic is understood in relation to the topic that precedes it.

**P8** — Use clear, direct, unambiguous language. Connecting words remove ambiguity about how two sentences relate to each other. When a reader encounters two consecutive sentences without a connector, the reader must guess the logical relationship: is the second sentence a result, a sequence, a contrast, or an independent addition? Approved connecting words eliminate this guesswork — "thus" signals consequence, "but" signals exception, "then" signals sequence, and "and" signals addition. In code documentation, where misunderstanding the relationship between setup and result, between condition and behavior, or between input and output has operational consequences, explicit connectors are essential.

**P1** — Use approved words from the controlled terminology. Only the connecting words and phrases approved in the STE-Code dictionary are permitted to join sentences. Unapproved connectors such as "however," "therefore," "moreover," "nevertheless," "consequently," and "furthermore" are prohibited. The approved set — "and," "but," "then," "thus," "as a result," and "at the same time" — is deliberately small to force writers to choose the simplest and most direct logical relationship between sentences rather than an ornate or ambiguous one.

**P5** — Write one instruction per procedural step. In procedures, each step describes exactly one action and starts with an imperative verb. When a step requires an explanation, a connecting word ("and," "but," "then") joins the imperative step to the explanatory sentence that follows. This preserves the one-action-per-step structure while allowing the writer to supply context that the reader needs to execute the step correctly.

**P7** — Use the imperative mood for all procedural writing. Connecting words in procedures join an imperative work step to a descriptive explanation. The imperative step (imperative mood) is followed by an explanatory sentence (descriptive mood), and the connecting word between them signals the shift in function — the reader understands that the second sentence provides background, not another instruction. Without a connector, the reader may interpret the explanatory sentence as a continuation of the imperative instruction.
