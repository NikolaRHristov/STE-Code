# Rule 4.3 — Use a Vertical List for Complex Text

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.3
> **Source:** [master.md#sec4-rule4.3](ste-code/grouped/)
> Source: master.md#sec4-rule4.3

## Original Rule

When your sentence is long and you must include many different items (for example, a list of components, parts, or documents) or actions, you can put them in a vertical list. Vertical lists make long and complex texts much easier to read and understand.

#### When you make a vertical list:

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

You can use vertical lists in procedural and descriptive writings, but you cannot mix the two types of writing in the same vertical list.

In safety instructions, include negative commands (DO NOT) where necessary for each item in the vertical list. This method will make the safety instruction more direct and easier to understand.

Always make sure that each item in the vertical list connects clearly and correctly to the first part of the vertical list (the text that is before the colon).

Always make sure that the layout of your vertical list is easy to read. In the example that follows, there is a second vertical list included in the primary vertical list. Use the same level for all items in the vertical list.

An item in a vertical list can contain a verb and not be a full sentence. Then, you do not use a period at the end of that item.

### Examples (from source):

> **Non-STE:** The wheel assembly comprises the tire, the tube, the spokes, the spoke fittings, the valve, and the hub.
>
> **STE:** The wheel assembly has these parts:
> - The tire
> - The tube
> - The spokes
> - The spoke fittings
> - The valve
> - The hub.

> **Non-STE:** The report must include each of the following: a completed REC-1 form, a three-view drawing of the unit, a photograph of the unit, a copy of the source data.
>
> **STE:** The report must include:
> - A completed REC-1 form
> - A three-view drawing of the unit
> - A photograph of the unit
> - A copy of the source data.

## STE-Code Adaptation

When a sentence in code documentation is long and must include many different items (for example, a list of parameters, return fields, error codes, configuration options, environment variables, dependencies, or test cases) or actions, put them in a vertical list. Vertical lists make complex documentation much easier to read and understand.

When you make a vertical list:

- Put a colon (:) at the end of the introductory sentence, before the first item.
- Identify each item with a number, letter, dash, or bullet.
- Start each item with an uppercase letter.
- Where applicable, use an article before the noun that is the subject of each item.
- Put a period at the end of an item if it is a full sentence (an imperative step such as "Set the timeout value" is a full sentence).
- Do not put a period at the end of an item if it is not a full sentence (for example, a noun phrase such as "The `timeout` parameter that controls the delay").
- Do not put a comma or a semicolon at the end of an item.
- Put a period at the end of the last item.

You can use vertical lists in procedural and descriptive documentation, but you cannot mix imperative instructions and descriptive statements in the same vertical list.

In safety instructions, include negative commands (DO NOT) where necessary for each item in the vertical list. This method makes the safety instruction more direct and easier to understand.

Always make sure that each item connects clearly and correctly to the introductory text (the text before the colon). Read "Introductory text [item]" as one sentence to test the connection.

Do not nest a second vertical list inside the primary vertical list. Use the same level for all items. If a sub-item needs its own list, start a new introductory sentence after the parent item, or describe the sub-fields with a table or a separate vertical list under a new heading.

An item can contain a verb and not be a full sentence. Then, do not use a period at the end of that item.

## Examples

> *Adapted from spec pair:* Non-STE: The wheel assembly comprises the tire, the tube, the spokes, the spoke fittings, the valve, and the hub.  |  STE: The wheel assembly has these parts: The tire, The tube, The spokes, The spoke fittings, The valve, The hub.
>
> *Adapted from spec pair:* Non-STE: The report must include each of the following: a completed REC-1 form, a three-view drawing of the unit, a photograph of the unit, a copy of the source data.  |  STE: The report must include: A completed REC-1 form, A three-view drawing of the unit, A photograph of the unit, A copy of the source data.

### Descriptive list of constructor parameters

> **Non-STE:** The `UserService` constructor accepts the database URL, the cache backend, and the maximum retry count.

> **STE:** The `UserService` constructor accepts these parameters:
> - The `database_url` for the PostgreSQL connection string.
> - The `cache_backend` for session storage.
> - The `max_retries` for transient failure handling.

```python
class UserService:
    """Manage application users and their sessions.

    The UserService constructor accepts these parameters:
    - The database_url for the PostgreSQL connection string.
    - The cache_backend for session storage.
    - The max_retries for transient failure handling.
    """

    def __init__(self, database_url, cache_backend, max_retries=3):
        self.database_url = database_url
        self.cache_backend = cache_backend
        self.max_retries = max_retries
```

### Procedural steps (one type only, no mixed items)

> **Non-STE:** To deploy the application: set the `DATABASE_URL` variable, the server binds to port 8080 after startup, run the migration command.

> **STE:** To deploy the application, do these steps:
> - Set the `DATABASE_URL` environment variable.
> - Run the `apply-migrations` command.
> - Start the server on port 8080.

````markdown
## Deploy the application

To deploy the application, do these steps:

- Set the `DATABASE_URL` environment variable.
- Run the `apply-migrations` command.
- Start the server on port 8080.

The server binds to port 8080 after startup.
````

### Error code reference for an HTTP API

> **Non-STE:** The API returns 400 for validation issues, 401 when the token is expired, 403 if permissions are not sufficient, and 404 when the resource is missing.

> **STE:** The API returns these error codes:
> - `400 Bad Request` for a failed input validation.
> - `401 Unauthorized` for an expired or missing token.
> - `403 Forbidden` for insufficient permissions.
> - `404 Not Found` for a missing resource.

```http
GET /api/v1/orders/8f2c HTTP/1.1
Authorization: Bearer <token>

HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": "unauthorized",
  "message": "The token is expired. Get a new token and send the request again."
}
```

The API returns these error codes:
- `400 Bad Request` for a failed input validation.
- `401 Unauthorized` for an expired or missing token.
- `403 Forbidden` for insufficient permissions.
- `404 Not Found` for a missing resource.

### Safety instruction with a negative command on each item

> **Non-STE:** CAUTION: WHEN YOU ACCESS THE CONFIGURATION THROUGH THE ADMIN PANEL, DO NOT CHANGE THE SECRET KEY. DO NOT DISABLE THE AUDIT LOG.

> **STE:** CAUTION: WHEN YOU ACCESS THE CONFIGURATION THROUGH THE ADMIN PANEL:
> - DO NOT CHANGE THE SECRET KEY.
> - DO NOT DISABLE THE AUDIT LOG.

```text
CAUTION: WHEN YOU ACCESS THE CONFIGURATION THROUGH THE ADMIN PANEL:

- DO NOT CHANGE THE SECRET KEY.
- DO NOT DISABLE THE AUDIT LOG.
```

### Declarative configuration options (YAML)

> **Non-STE:** The service reads a YAML file with the server port, the log level, the database pool size, and the feature flags.

> **STE:** The `config.yaml` file has these top-level fields:
> - The `server.port` that sets the listen port.
> - The `log.level` that sets the log verbosity.
> - The `database.pool_size` that sets the maximum open connections.
> - The `features` that lists the enabled feature flags.

```yaml
# The config.yaml file has these top-level fields:
# - The server.port that sets the listen port.
# - The log.level that sets the log verbosity.
# - The database.pool_size that sets the maximum open connections.
# - The features that lists the enabled feature flags.
server:
  port: 8080
log:
  level: info
database:
  pool_size: 20
features:
  - new_checkout
  - dark_mode
```

### Data-transfer-object fields

> **Non-STE:** The `CreateUserRequest` DTO has the email, the display name, and the role.

> **STE:** The `CreateUserRequest` object has these fields:
> - The `email` that gives the user login.
> - The `display_name` that gives the name that shows in the UI.
> - The `role` that gives the access level.

```json
{
  "email": "ada@example.com",
  "display_name": "Ada Lovelace",
  "role": "editor"
}
```

### Function return codes (procedural, Go)

> **Non-STE:** The `openFile` function returns 0 on success, -1 if the path is missing, and -2 if the user lacks permission.

> **STE:** The `openFile` function returns these codes:
> - `0` for a successful open.
> - `-1` for a missing path.
> - `-2` for insufficient permission.

```go
// The openFile function returns these codes:
// - 0 for a successful open.
// - -1 for a missing path.
// - -2 for insufficient permission.
func openFile(path string) (int, error) {
    if _, err := os.Stat(path); errors.Is(err, os.ErrNotExist) {
        return -1, fmt.Errorf("the path %q is missing", path)
    }
    f, err := os.Open(path)
    if err != nil {
        return -2, fmt.Errorf("the user lacks permission for %q", path)
    }
    defer f.Close()
    return 0, nil
}
```

### Test cases for a unit test

> **Non-STE:** The `parse_interval` function must accept "10s" and return 10 seconds, accept "0" and return an error, and accept "abc" and return an error.

> **STE:** The `parse_interval` function passes these test cases:
> - Accept `"10s"` and return 10 seconds.
> - Accept `"0"` and return an error.
> - Accept `"abc"` and return an error.

```python
def test_parse_interval():
    # The parse_interval function passes these test cases:
    # - Accept "10s" and return 10 seconds.
    # - Accept "0" and return an error.
    # - Accept "abc" and return an error.
    assert parse_interval("10s") == 10
    with pytest.raises(ValueError):
        parse_interval("0")
    with pytest.raises(ValueError):
        parse_interval("abc")
```

### Dependencies in a package manifest

> **Non-STE:** This project needs express for routing, pg for the database, and redis for caching.

> **STE:** The project uses these dependencies:
> - `express` for HTTP routing.
> - `pg` for the PostgreSQL database.
> - `redis` for cache storage.

```json
{
  "dependencies": {
    "express": "^4.19.2",
    "pg": "^8.11.3",
    "redis": "^4.6.10"
  }
}
```

The project uses these dependencies:
- `express` for HTTP routing.
- `pg` for the PostgreSQL database.
- `redis` for cache storage.

### Environment variables

> **Non-STE:** The worker reads LOG_LEVEL, QUEUE_URL, and MAX_WORKERS from the environment.

> **STE:** The worker reads these environment variables:
> - The `LOG_LEVEL` that sets the log verbosity.
> - The `QUEUE_URL` that sets the message queue address.
> - The `MAX_WORKERS` that sets the maximum concurrent tasks.

```bash
# The worker reads these environment variables:
# - The LOG_LEVEL that sets the log verbosity.
# - The QUEUE_URL that sets the message queue address.
# - The MAX_WORKERS that sets the maximum concurrent tasks.
export LOG_LEVEL=info
export QUEUE_URL=amqp://broker:5672/tasks
export MAX_WORKERS=8
```

## Paradigm-Specific Guidance

- **Object-Oriented:** Use a vertical list for constructor parameters, public methods, data-transfer-object fields, and exceptions that a method can send.
- **Functional:** Use a vertical list to document each variant of a sum type or each pattern-match arm.
- **Procedural (C, Go, Bash):** Use a vertical list for function return codes. Each item gives one code and its meaning.
- **Declarative (SQL, Terraform, YAML):** Use a vertical list for top-level fields. Use a separate list for the sub-fields of a complex field.
- **Systems (Rust, C memory):** Use a vertical list for ownership or lifecycle rules. Each item gives one constraint.

## Edge Cases

- **Nested fields:** Do not put a second vertical list inside the primary list. Describe the sub-fields with a new introductory sentence after the parent item, or with a table.
- **Generated documentation:** Generated API docs (JSDoc, Sphinx, rustdoc) may use tables. That is acceptable. Apply Rule 4.3 to prose that a human writes.
- **Very short lists:** A list of two or three very short items may stay inline. Use a vertical list when each item has more than five words or the inline sentence exceeds 25 words.
- **Code blocks in items:** Put the code block after the item text, indented under the item. The item still starts with an uppercase letter.
- **Mixed code and prose:** When an item needs a code sample, keep the item sentence first (starting with an uppercase letter), then add the code block. Do not start the item with a code fence.

## Grammar Notes

- Each item must complete the introductory sentence grammatically. Test by reading "Introductory text [item]" as one sentence.
- Use "the" or "a/an" consistently across all items. Put the article before the backticks when the item starts with a code identifier.
- A full sentence has a subject and a finite verb. An item with only a verb phrase (for example, "Set the timeout value") is a full imperative sentence and gets a period. An item such as "The `timeout` parameter that controls the delay" is a relative clause and gets no period until the last item.

## Cross-References

- **Rule 1.1** — Use approved words from the STE-Code dictionary.
- **Rule 1.6** — Non-approved words are permitted only as technical code nouns.
- **Rule 4.1** — Use short sentences. A vertical list helps you obey the length limit.
- **Rule 4.2** — Use one sentence per instruction in procedures.
- **Rule 5.1** — Use the active voice in procedural steps.

> **See also:** Rule 1.1 — Use approved words from the STE-Code dictionary.
> **See also:** Rule 1.6 — Non-approved words are permitted only as technical code nouns.
> **See also:** Rule 4.1 — Use short sentences.
> **See also:** Rule 4.2 — Use one sentence per instruction in procedures.
> **See also:** Rule 5.1 — Use the active voice in procedural steps.

## Summary Checklist

- [ ] The introductory sentence ends with a colon.
- [ ] Each item starts with an uppercase letter.
- [ ] Each item connects to the introductory text.
- [ ] No period on non-sentence items; period on the last item.
- [ ] No mixed procedural and descriptive items in one list.
- [ ] No nested vertical lists.
- [ ] Each code sample (if any) comes after its item sentence.
