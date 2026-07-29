# Rule 1.8 — Use Technical Nouns That Are Approved in Your Company, Industry, or Subject Field

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.8

## Original Rule

**Rule 1.8** Use technical nouns that are approved in your company, industry, or subject field.

If your company, industry, or subject field, has an approved technical noun for a system, component, part, or process, use that technical noun. Usually, such technical nouns are included in official parts information and in company documentation.

Example:

> **STE:** The front panel of the phone has a touchscreen and a home button.

("Touchscreen" and "home button" are technical nouns that are approved in your company, industry, or subject field.)

## STE-Code Adaptation

**Rule 1.8** Use code-domain technical nouns that are approved in your project, company, industry, or subject field.

If your project, company, industry, or subject field has an approved code-domain technical noun for a class, module, function, method, variable, component, or process, use that code-domain technical noun. Usually, such code-domain technical nouns are included in your project glossary, API documentation, coding standards, or company documentation.

Do not invent your own names for items that already have established names in your codebase or domain. Consistency with the approved terminology helps all readers understand the documentation.

### Examples

> **Non-STE:** The account controller manages login and user profile operations.
> **STE:** The AccountController manages authentication and user profile operations.

"AccountController" is the code-domain technical noun that is approved in the project (the actual class name in the codebase). The non-STE version uses "account controller," which is not the approved name. The STE version uses the exact approved code-domain technical noun.

> **Non-STE:** Send a GET to the users path to fetch the list.
> **STE:** Send a GET request to the /api/users endpoint to get the list.

"/api/users" and "GET request" are the code-domain technical nouns that are approved in the project (the actual endpoint path and HTTP method). The non-STE version uses informal terms "users path" and "fetch," which are not the approved names. The STE version uses the exact approved code-domain technical nouns and the approved verb "get."
