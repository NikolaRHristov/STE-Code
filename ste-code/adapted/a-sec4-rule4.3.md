# Rule 4.3 — Use a Vertical List for Complex Texts

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.3
> **STE-Code Principles:** P1, P2, P11

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

## Code-Domain Explanation

Rule 4.3 applies to these code documentation types:

### README Files

README files often describe many features, installation steps, or configuration options. Long inline lists make the reader scan a wall of text. Put these items in a vertical list. The reader can find each item quickly. For example, list the supported platforms in a vertical list instead of a comma-separated sentence.

### API Documentation

API references contain many parameters, return fields, error codes, and response shapes. A vertical list makes each field easy to scan. When you document a function with more than three parameters, use a vertical list. The introductory sentence tells the reader what the list contains.

### Docstrings and Inline Comments

Docstrings and inline comments have limited space. A vertical list is still correct when the list has many items. Use a compact form. Start each item with a dash. Do not add blank lines between items. The structure stays clear even in a small space.

### Commit Messages

A commit message body can use a vertical list to describe many changes. Put the summary on the first line. Put a blank line. Then put the list of changes as a vertical list. Each item describes one change.

### Error Messages

Error messages must be short. Do not use a vertical list in an error message string. Instead, put the list of possible causes in the error documentation. The error string itself must be one sentence.

### Changelogs and Release Notes

Changelogs are naturally vertical lists. Each item starts with a category label (Added, Changed, Fixed, Deprecated, Removed). Connect each item to its category. Make sure the category heading works as the introductory text.

## Paradigm-Specific Guidance

### Object-Oriented Documentation

When you document a class in Java, C++, C#, or Python, use vertical lists for:

- The constructor parameters
- The public methods
- The fields of a data transfer object (DTO)
- The exceptions that a method can send

Connect each item to the introductory sentence. For class fields, use a list of field-name and description pairs. Each item starts with the field name in backticks.

**Example — Python class constructor:**

> The `UserService` constructor accepts these parameters:
> - The `database_url` for the PostgreSQL connection
> - The `cache_backend` for session storage
> - The `max_retries` for transient failure handling.

### Functional Documentation

In functional languages (Haskell, Elixir, Clojure, Rust), pattern matches and sum types often have many variants. Use a vertical list to document each variant. The introductory sentence identifies the type. Each item describes one variant with its data.

**Example — Rust enum:**

> The `ParseError` enum has these variants:
> - `UnexpectedToken` that occurs when the lexer finds an unknown symbol
> - `UnterminatedString` that occurs when a string literal has no closing quote
> - `InvalidNumber` that occurs when a numeric literal has an incorrect format.

### Procedural Documentation

In C, Go, or Bash documentation, functions often return error codes. Use a vertical list to document each return code. The introductory sentence explains what the list contains. Each item gives one code and its meaning.

**Example — Go function return values:**

> The `OpenFile` function returns these values:
> - The file descriptor as an `*os.File`
> - An error that is `nil` when the operation succeeds
> - An error that contains the system error code when the operation fails.

### Declarative Documentation

In SQL schema docs, Terraform, or Kubernetes YAML, configuration blocks have many nested fields. Use a vertical list for the top-level fields. Use a separate list for sub-fields of a complex field. Do not nest lists. Instead, describe the sub-field with a new introductory sentence after its parent item.

**Example — Terraform resource:**

> The `aws_instance` resource accepts these arguments:
> - The `ami` that identifies the machine image to start
> - The `instance_type` that sets the compute capacity
> - The `subnet_id` that places the instance in a VPC subnet.
>
> The `instance_type` argument has these constraints:
> - It must be a string from the AWS instance type catalog
> - It must be compatible with the chosen AMI architecture
> - It must be available in the selected region.

### Systems Documentation

For Rust ownership and C memory documentation, use vertical lists to describe the lifecycle rules. Each item gives one ownership constraint or memory management requirement. The introductory sentence states the rule category.

**Example — Ownership constraints:**

> The `Buffer` type has these ownership rules:
> - The caller owns the buffer after the `allocate` function returns
> - The caller must call the `deallocate` function exactly once
> - The buffer must not be used after the `deallocate` function returns
> - The buffer must not be shared between threads without a mutex.

## Extended Examples

### Example 1: Configuration Options (Inline to Vertical)

> **Non-STE:** The server supports logging in JSON format, text format, and syslog format, and can write to stdout, stderr, a file on disk, or a remote syslog daemon.
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
> *Principles Applied: P11 (one concept per item), Rule 4.3 (vertical list for many items). The original sentence mixed two categories (format and destination). The STE version separates them into two vertical lists. Each list has one clear topic.*

### Example 2: Error Code Reference

> **Non-STE:** The API returns 400 for validation issues, 401 when the token is expired or missing, 403 if permissions aren't sufficient to access the resource, 404 obviously when the resource can't be located, and 500 for any unhandled internal failure.
> **STE:** The API returns these error codes:
> - `400 Bad Request` for a failed input validation
> - `401 Unauthorized` for an expired or missing token
> - `403 Forbidden` for insufficient permissions
> - `404 Not Found` for a missing resource
> - `500 Internal Server Error` for an unhandled failure.
>
> *Principles Applied: P11 (consistent structure per item), Rule 4.3 (vertical list format). The non-STE version uses casual language ("obviously", "aren't sufficient"). The STE-Code version uses the same grammatical structure for each item and starts each item with the code and name.*

### Example 3: Procedural Steps (Mixed Types)

> **Non-STE:** To deploy the application:
> - Set the `DATABASE_URL` environment variable.
> - The `MIGRATIONS_DIR` points to the SQL files.
> - Run the `apply-migrations` command.
> - The server binds to port 8080 after startup.
> **STE:** To deploy the application, do these steps:
> - Set the `DATABASE_URL` environment variable.
> - Set the `MIGRATIONS_DIR` to the SQL files path.
> - Run the `apply-migrations` command.
> - Start the server on port 8080.
>
> *Principles Applied: Rule 4.3 (no mixed types in one list). The non-STE version mixes imperative instructions with descriptive statements. The STE-Code version uses only imperative instructions. Each item is an action the reader must do.*

### Example 4: Method Return Value with Connected Structure

> **Non-STE:** The `findUser` method returns these things:
> - `null` when the query finds no matching record.
> - Returns a `User` object with all profile fields populated from the database.
> - Throws `DatabaseError` if the connection pool is exhausted.
> **STE:** The `findUser` method returns:
> - A `User` object when the query finds a matching record
> - `null` when the query finds no matching record.
>
> The `findUser` method sends a `DatabaseError` when the connection pool is exhausted.
>
> *Principles Applied: Rule 4.3 (each item connects to the intro), P11 (one concept per list). The non-STE version mixes return values and exceptions. The STE-Code version separates the return values into one list and the exception into a separate sentence.*

### Example 5: Dependencies in a Package Manifest

> **Non-STE:** This project leverages express for HTTP routing, utilizes pg for database connections, employs redis for caching, and makes use of winston for structured logging.
> **STE:** The project uses these dependencies:
> - `express` for HTTP routing
> - `pg` for PostgreSQL database connections
> - `redis` for cache storage
> - `winston` for structured logging.
>
> *Principles Applied: P1 (use "use" instead of "leverage/utilize/employ"), Rule 4.3 (vertical list for four items). Each item follows the same pattern: package name, "for", purpose. The list makes the dependencies easy to scan.*

### Example 6: API Endpoint Documentation

> **Non-STE:** POST /api/orders accepts a JSON body with customerId (string, required, must be a valid UUID), items (array of objects with productId string and quantity integer, must not be empty), shippingAddress (object with street, city, zip, country strings, optional, defaults to the customer's default address), and paymentMethod (string enum of "card", "paypal", "invoice", required).
> **STE:** The `POST /api/orders` endpoint accepts a JSON body with these fields:
> - The `customerId` (string, required) that must be a valid UUID
> - The `items` (array, required) that must not be empty. Each item contains:
>   - A `productId` string
>   - A `quantity` integer.
> - The `shippingAddress` (object, optional) that contains a street, city, zip, and country. The default is the customer default address.
> - The `paymentMethod` (string, required) that must be one of: `"card"`, `"paypal"`, or `"invoice"`.
>
> *Principles Applied: Rule 4.3 (vertical list for complex API reference), P11 (consistent field documentation pattern). Each field is a separate list item. The nested structure uses a separate list for the `items` sub-fields instead of a nested vertical list.*

## Edge Cases

### Edge Case 1: Framework Name Conflicts with an Unapproved Word

Some framework names use words that are not approved in STE-Code. For example, the React hook `useMemo` contains "use" in its name. The JavaScript method `.catch()` uses "catch" as a noun-like method name. These are technical code nouns. Rule 1.6 permits non-approved words when they are technical code nouns. Use them in backticks inside a vertical list item. Do not change the framework name.

### Edge Case 2: Vertical List Items That Contain Code Blocks

When a vertical list item must include a code example, put the code block after the item text. Do not make the code block a separate list item. Indent the code block under the item. The item still starts with an uppercase letter. The period goes after the code block if the item is a full sentence.

### Edge Case 3: Generated Documentation

Generated API documentation (from JSDoc, Sphinx, rustdoc, godoc) often puts parameters in a table or a definition list format. This is acceptable. Rule 4.3 applies to text that a human writes. Generated output can use the format that the generator tool provides. When you write the docstring that feeds the generator, use the Rule 4.3 format in the prose parts.

### Edge Case 4: Very Short Lists (Two or Three Items)

When a list has only two or three very short items, an inline list is acceptable. Use a vertical list when:
- Each item has more than five words.
- The items are complex and need individual attention.
- The inline list makes the sentence longer than 25 words.

For a short list of three single-word items in a descriptive sentence, an inline list is clear enough.

### Edge Case 5: List Items That Are Themselves Vertical (Matrix Documentation)

Some documentation needs to show a matrix or a table. For example, a compatibility matrix between library versions and language versions. Do not force a vertical list for matrix data. Use a Markdown table instead. Rule 4.3 applies to prose lists, not to tabular data. When the table has a prose caption, apply the STE-Code rules to the caption text.

## Grammar Notes

### Syntactic Parallelism

The original ASD-STE100 rule requires each item in a vertical list to connect to the introductory text. This is syntactic parallelism. In code documentation, this means:

- Each item must complete the introductory sentence grammatically.
- Test each item: read "Introductory text [item]" as one sentence. It must be correct.
- If an item does not fit the introductory text, rewrite the introductory text or split the list.

### Article Consistency

The original rule says to use an article before the noun that is the subject of each item. In code documentation:

- Use "the" or "a/an" consistently across all items.
- When the item starts with a backtick-quoted identifier (`parameterName`), put the article before the backticks.
- Example: `- The `timeout` parameter sets the connection timeout.`

### Period Placement

An item with a verb but not a full sentence does not get a period. A full sentence has a subject and a finite verb. In code documentation:

- "The `timeout` parameter" is not a sentence. No period.
- "Set the `timeout` parameter to 30" is a full imperative sentence. Use a period.
- "The `timeout` parameter that controls the delay" has a verb ("controls") but is a relative clause without a main clause. No period on intermediate items. Period on the last item.

### Punctuation

Do not use a comma or a semicolon at the end of a vertical list item. The vertical layout replaces the punctuation that an inline list would use. The reader sees each item as a separate line. The line break is the separator.

### Nested Lists and Alternatives

Do not put a second vertical list inside a primary vertical list. Instead:

- Put the sub-items in the same item separated by commas (for two or three short sub-items).
- Start a new paragraph with a new introductory sentence after the parent item.
- Use a table when the data is complex.

## Cross-References

- **Rule 1.1**: Use approved words from the STE-Code dictionary. Vertical list items must use approved words.
- **Rule 1.2**: Use words only as their specified part of speech. Each list item must use words correctly.
- **Rule 1.6**: Non-approved words only when they are technical code nouns. Framework names in list items are permitted.
- **Rule 1.7**: Do not use technical nouns as verbs. Check each list item for noun-as-verb violations.
- **Rule 1.11**: One term per concept. Use the same word for the same concept across all items in a list.
- **Rule 3.1**: Use the imperative mood for procedures. When a vertical list contains steps, each item must be imperative.
- **Rule 4.1**: Use short sentences. A vertical list helps you obey the sentence-length limits by breaking one long sentence into many short items.
- **Rule 4.2**: Use one sentence per instruction in procedures. Each vertical list item in a procedural list must be one instruction.
- **Rule 5.1**: Use the active voice. Each item in a procedural vertical list must use the active voice.
- **STE-Code Dictionary**: See the canonical synonym table for preferred verbs to use in list items.

## Summary

Use a vertical list when a sentence in code documentation has many items. The list makes the text easy to scan. Put a colon at the end of the introductory sentence. Start each item with an uppercase letter. Use the same grammatical structure for all items. Do not mix imperative and descriptive items. Do not use nested lists. Connect every item to the introductory text. Apply the same rigor to your vertical lists that you apply to your code formatting.
