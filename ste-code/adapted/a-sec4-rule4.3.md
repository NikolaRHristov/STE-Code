# Rule 4.3 — Use a Vertical List for Complex Texts

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.3

## Original Rule

When your sentence is long and you must include many different items (for example, a list of components, parts, or documents) or actions, you can put them in a vertical list. Vertical lists make long and complex texts much easier to read and understand.

When you make a vertical list:

- Put a colon (:) at the end of the first sentence, before the first item in the vertical list.
- Identify each item in the vertical list with a number, letter, punctuation mark, or symbol. For example, you can use:
  - A dash (-)
  - A bullet point (•)
  - A letter (a, b, c…)
  - A number (1, 2, 3…).
- Start each item in the vertical list with an uppercase letter.
- Where applicable, use an article before the noun that is the subject of each item in the vertical list.
- Put a period at the end of an item in the vertical list if it is a full sentence.
- Do not put a period at the end of an item in the vertical list if it is not a full sentence.
- Do not put a comma or a semicolon at the end of an item in the vertical list.
- Put a period at the end of the last item in the vertical list.

You can use vertical lists in procedural and descriptive writings, but you cannot mix the two types of writings in the same vertical list.

Always make sure that each item in the vertical list connects clearly and correctly to the first part of the vertical list (the text that is before the colon).

Always make sure that the layout of your vertical list is easy to read. Do not include a second vertical list inside the primary vertical list. Use the same level for all items in the vertical list.

An item in a vertical list can contain a verb and not be a full sentence. Then, you do not use a period at the end of that item.

## STE-Code Adaptation

When a sentence in code documentation is long and must include many different items (for example, a list of function parameters, return fields, error codes, or configuration options), put them in a vertical list. Vertical lists make complex documentation much easier to read and understand.

When you make a vertical list:

- Put a colon (:) at the end of the introductory sentence, before the first item.
- Identify each item with a number, letter, punctuation mark, or symbol.
- Start each item with an uppercase letter.
- Where applicable, use an article before the noun that is the subject of each item.
- Put a period at the end of an item if it is a full sentence.
- Do not put a period at the end of an item if it is not a full sentence.
- Do not put a comma or a semicolon at the end of an item.
- Put a period at the end of the last item.

You can use vertical lists in procedural and descriptive documentation, but you cannot mix imperative instructions and descriptive statements in the same vertical list.

Always make sure that each item in the vertical list connects clearly to the introductory text (the text before the colon).

Do not use nested vertical lists. Use the same level for all items in the vertical list.

### Examples

**Converting an inline list of parameters to a vertical list:**

> **Non-STE:** The `configure` method accepts the hostname, the port number, the connection timeout in milliseconds, the retry count, and the TLS certificate path.
> **STE:** The `configure` method accepts these parameters:
> - The hostname
> - The port number
> - The connection timeout in milliseconds
> - The retry count
> - The TLS certificate path.

**Connecting items to the introductory text:**

> **Non-STE:** Do not use the `parse` method for these input types after the validation step:
> - the XML documents,
> - the YAML configuration files with the inline comments,
> - data with embedded binary segments.
> **STE:** After the validation step, do not use the `parse` method for:
> - The XML documents
> - The YAML configuration files
> - The YAML inline comments
> - The data with embedded binary segments.

**Items with verbs but not full sentences:**

> **Non-STE:** The `Response` object has the properties that follow:
> - The `status` field that stores the HTTP status code.
> - The `headers` field that contains the response headers.
> - The `body` field that holds the response payload.
> **STE:** The `Response` object has the properties that follow:
> - The `status` field that stores the HTTP status code
> - The `headers` field that contains the response headers
> - The `body` field that holds the response payload.
