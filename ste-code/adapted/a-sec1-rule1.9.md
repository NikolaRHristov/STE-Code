# Rule 1.9 — When You Must Select a Technical Noun, Use One Which Is Short and Easy to Understand

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.9

## Original Rule

**Rule 1.9** When you must select a technical noun, use one which is short and easy to understand.

When there is no technical noun that is approved in your company, industry, or subject field, select one that is short (not more than three words) and easy to understand.

Example:

> **Non-STE:** Remove the four stainless steel pan head machine screws (10) that attach the metallic machined flange (15) to the front housing cover (20).
> **STE:** Remove the four screws (10) that attach the flange (15) to the cover (20).

In this example, it is sufficient to use the words "screws," "flange," and "cover." This is because these parts have index numbers, and the related illustration clearly identifies them. Differently, add one or two adjectives to the noun to help your reader understand.

## STE-Code Adaptation

**Rule 1.9** When you must select a code-domain technical noun, use one which is short and easy to understand.

When there is no code-domain technical noun that is approved in your project, company, industry, or subject field, select one that is short (not more than three words) and easy to understand.

Do not use long descriptive phrases when a shorter term is sufficient. If the context clearly identifies the item (for example, a code snippet, a diagram, or an API reference), use the shortest term that is unambiguous. If additional clarification is necessary, add one or two adjectives to the noun to help your reader understand.

### Examples

> **Non-STE:** Call the asynchronous JavaScript XML HTTP request wrapper utility function (line 42) to get the serialized JSON payload from the remote application programming interface endpoint.
> **STE:** Call the fetch utility (line 42) to get the JSON data from the API endpoint.

This adapts the spec pair: "Remove the four stainless steel pan head machine screws (10) that attach the metallic machined flange (15) to the front housing cover (20)" becomes "Remove the four screws (10) that attach the flange (15) to the cover (20)." In the spec, the long descriptive phrase "stainless steel pan head machine screws" is reduced to "screws" because the index number (10) and the illustration identify the part. In STE-Code, the long phrase "asynchronous JavaScript XML HTTP request wrapper utility function" is reduced to "fetch utility" because the line number (42) and the code snippet identify the function. "JSON payload" becomes "JSON data" and "remote application programming interface endpoint" becomes "API endpoint" — both follow the spec principle of using the shortest unambiguous term.
