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

In this example, it is sufficient to use the words "fetch utility," "JSON data," and "API endpoint." This is because the code snippet on line 42 clearly identifies the function, and the terms "JSON" and "API" are well-known in the subject field.

> **Non-STE:** The continuous integration and continuous deployment automated pipeline configuration file specifies the build steps.
> **STE:** The CI/CD pipeline configuration file specifies the build steps.

"CI/CD" is a well-known abbreviation that is shorter and easier to understand than the full phrase. Use the abbreviated form when it is the standard term in your subject field.
