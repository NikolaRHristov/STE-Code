# Rule 4.1 — Write Short and Clear Sentences

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.1

## Original Rule

Write short and clear sentences that give accurate instructions and information.

In procedures, give short and clear instructions directly to the reader (imperative form).

In a descriptive text, make sure that each sentence has only one topic (subject or idea) and does not contain the imperative form. Then, in the sentences that follow, gradually give information about that topic.

For the two types of writing, always make sure that your text is not abstract. Make sure that it clearly shows how to do a task or how a system operates. Be accurate. Do not give information that is not accurate or can have different meanings.

## STE-Code Adaptation

Write short and clear sentences in code documentation. Each sentence must give accurate information about the code.

In API method and function descriptions (procedural writing), give short and clear instructions directly to the reader in the imperative form. Each work step describes one action.

In class, module, and type descriptions (descriptive writing), make sure that each sentence has only one topic. Do not use the imperative form. Give information about the topic gradually across the sentences that follow.

Always make sure that your documentation is not abstract. Make sure that it clearly shows how to use a function or how a module operates. Be accurate. Do not give information that is not accurate or can have different meanings.

### Examples

**Procedural writing (function description):**

> **Non-STE:** To call the `initialize` method, first pass the three configuration parameters that set up the connection to the database, and then, after calling the method, check the return value for a success code or an error object.
> **STE:**
> 1. Call the `initialize` method as follows:
>    A. Pass the three configuration parameters that set the connection to the database.
>    B. Call the method.
>    C. Check the return value. The return value is a success code or an error object.

**Descriptive writing (class description):**

> **Non-STE:** The `HttpClient` class has two internal buffers connected together and linked with callbacks between the request handler and the response dispatcher.
> **STE:** The `HttpClient` class has two internal buffers. The internal buffers are connected together with callbacks. These callbacks link the request handler to the response dispatcher.

**Avoid abstract statements:**

> **Non-STE:** No null values are permitted.
> **STE:** Make sure that the function does not return a null value.
