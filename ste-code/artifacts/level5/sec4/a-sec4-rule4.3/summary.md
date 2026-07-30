# Rule 4.3 — Use a Vertical List for Complex Texts

## Original Rule Summary

Rule 4.3 instructs writers to use a vertical list when a sentence is long and must include many different items or actions. Vertical lists make complex texts easier to read and understand by giving each item its own line. Each item must connect grammatically to the introductory text before the colon, and all items must use the same level — nested vertical lists are not permitted. The rule also specifies formatting: start each item with an uppercase letter, use a colon before the first item, do not use commas or semicolons at item endings, and do not mix procedural and descriptive writing in the same vertical list.

## STE-Code Adaptation

Rule 4.3 in STE-Code applies the vertical list format to code documentation when a sentence must include many items such as function parameters, return fields, error codes, or configuration options. Put a colon at the end of the introductory sentence and start each list item with an uppercase letter. Do not mix imperative instructions with descriptive statements in the same vertical list — keep all items in a list uniform. Every item must connect grammatically to the introductory text, and nested vertical lists are not allowed; use a new introductory sentence after a parent item instead.

## Example Pairs

> **Non-STE:** The server supports logging in JSON format, text format, and syslog format, and can write to stdout, stderr, a file on disk, or a remote syslog daemon.
>
> **STE:** The server supports these log formats:
> - The JSON format
> - The text format
> - The syslog format.
>
> The server can write logs to these destinations:
> - The standard output stream
> - The standard error stream
> - A file on disk
> - A remote syslog daemon.
>
> *(P11 applied: one concept per list — formats and destinations are separate lists. The original sentence mixed two categories in a single inline sentence. The STE version separates them into two vertical lists, each with one clear topic.)*

> **Non-STE:** The API returns 400 for validation issues, 401 when the token is expired or missing, 403 if permissions are not sufficient to access the resource, 404 when the resource cannot be located, and 500 for any unhandled internal failure.
>
> **STE:** The API returns these error codes:
> - `400 Bad Request` for a failed input validation
> - `401 Unauthorized` for an expired or missing token
> - `403 Forbidden` for insufficient permissions
> - `404 Not Found` for a missing resource
> - `500 Internal Server Error` for an unhandled failure.
>
> *(P11 applied: consistent structure per item. P1 applied: \"are not sufficient\" → \"insufficient\", \"cannot be located\" → \"missing\". The STE version uses the same grammatical structure for each item and makes every error code easy to scan.)*

> **Non-STE:** To deploy the application:
> - Set the `DATABASE_URL` environment variable.
> - The `MIGRATIONS_DIR` points to the SQL files.
> - Run the `apply-migrations` command.
> - The server binds to port 8080 after startup.
>
> **STE:** To deploy the application, do these steps:
> - Set the `DATABASE_URL` environment variable.
> - Set the `MIGRATIONS_DIR` to the SQL files path.
> - Run the `apply-migrations` command.
> - Start the server on port 8080.
>
> *(Rule 4.3 applied: no mixed types in one list. The Non-STE version mixes imperative instructions with descriptive statements. The STE version uses only imperative instructions — every item is an action the reader must do. P2 applied: \"points to\" → \"set\" to maintain consistent part of speech across all items.)*

## Principles Applied

**P1** — Use approved words from the controlled terminology. Every word in vertical list items must come from the approved STE-Code dictionary. Replace non-approved words like \"utilize,\" \"leverage,\" and \"employ\" with \"use.\" Replace \"validate\" with \"check,\" \"configure\" with \"set,\" and \"return\" with \"give\" when appropriate.

**P2** — Use approved words only as the specified part of speech. Each item in a vertical list must use words in their approved grammatical role. When a list mixes items, check that verbs remain verbs and nouns remain nouns across all items. Do not use a noun as a verb inside a list item.

**P11** — One term per concept. Use the same word for the same concept across all items in a vertical list. If one item says \"parameter\" and another says \"argument\" for the same concept, the reader will be confused. Apply the same term consistently. Also, each vertical list should cover exactly one concept — split mixed-category lists into separate vertical lists, each with its own introductory sentence.
