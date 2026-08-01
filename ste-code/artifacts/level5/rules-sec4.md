---

## Rule 4.3 — Use a Vertical List for Complex Text

**Source:** Adapted from ASD-STE100 Issue 9, Rule 4.3.

### Requirement

When a sentence is long and must include many items (parameters, return fields, error
codes, config options, environment variables, dependencies, test cases) or actions,
put them in a vertical list. Vertical lists make complex text easier to read.

When you make a vertical list:

- Put a colon (`:`) at the end of the introductory sentence, before the first item.
- Identify each item with a number, letter, dash, or bullet.
- Start each item with an uppercase letter.
- Use an article before the noun that is the subject of each item, where applicable.
- Put a period at the end of an item if it is a full sentence (an imperative step such as "Set the timeout value" is a full sentence).
- Do not put a period at the end of an item that is not a full sentence (a noun phrase such as "The `timeout` parameter that controls the delay").
- Do not put a comma or semicolon at the end of an item.
- Put a period at the end of the last item.

Other rules:

- Use vertical lists in both procedural and descriptive docs, but do not mix imperative instructions and descriptive statements in the same list.
- In safety instructions, include negative commands (DO NOT) on each item where needed.
- Each item must connect clearly to the introductory text. Test by reading "Introductory text [item]" as one sentence.
- Do not nest a second vertical list inside the primary list. Use the same level for all items. For sub-items, start a new introductory sentence after the parent item, or use a table / separate list under a new heading.
- An item can contain a verb and not be a full sentence; then it takes no period.

### Code-domain examples

Descriptive list of constructor parameters:

> **Non-STE:** The `UserService` constructor accepts the database URL, the cache backend, and the maximum retry count.
> **STE:** The `UserService` constructor accepts these parameters:
> - The `database_url` for the PostgreSQL connection string.
> - The `cache_backend` for session storage.
> - The `max_retries` for transient failure handling.

Procedural steps (one type only):

```markdown
To deploy the application, do these steps:
- Set the `DATABASE_URL` environment variable.
- Run the `apply-migrations` command.
- Start the server on port 8080.
```

Error-code reference for an HTTP API:

> **STE:** The API returns these error codes:
> - `400 Bad Request` for a failed input validation.
> - `401 Unauthorized` for an expired or missing token.
> - `403 Forbidden` for insufficient permissions.
> - `404 Not Found` for a missing resource.

Safety instruction with a negative command on each item:

```text
CAUTION: WHEN YOU ACCESS THE CONFIGURATION THROUGH THE ADMIN PANEL:
- DO NOT CHANGE THE SECRET KEY.
- DO NOT DISABLE THE AUDIT LOG.
```

Declarative config options (YAML):

> **STE:** The `config.yaml` file has these top-level fields:
> - The `server.port` that sets the listen port.
> - The `log.level` that sets the log verbosity.
> - The `database.pool_size` that sets the maximum open connections.
> - The `features` that lists the enabled feature flags.

DTO fields, function return codes (Go), test cases, dependencies, and environment
variables follow the same pattern — one item per field/code/case/dependency with the
article and a short "that…" clause:

> **STE examples:** The `CreateUserRequest` object has these fields: … / The `openFile` function returns these codes: `0` for a successful open; `-1` for a missing path; `-2` for insufficient permission. / The project uses these dependencies: `express` for HTTP routing; `pg` for the PostgreSQL database; `redis` for cache storage. / The worker reads these environment variables: The `LOG_LEVEL` that sets the log verbosity; The `QUEUE_URL` that sets the message queue address; The `MAX_WORKERS` that sets the maximum concurrent tasks.

### Paradigm-specific guidance

- **Object-Oriented:** lists for constructor parameters, public methods, DTO fields, and exceptions a method can send.
- **Functional:** lists for each variant of a sum type or each pattern-match arm.
- **Procedural (C, Go, Bash):** lists for function return codes — one code and its meaning per item.
- **Declarative (SQL, Terraform, YAML):** lists for top-level fields; a separate list for sub-fields of a complex field.
- **Systems (Rust, C memory):** lists for ownership or lifecycle rules — one constraint per item.

### Edge cases

- **Nested fields:** do not nest a second vertical list; use a new introductory sentence or a table.
- **Generated documentation:** API-doc tables (JSDoc, Sphinx, rustdoc) are acceptable; apply 4.3 to human-written prose.
- **Very short lists:** two or three very short items may stay inline; use a vertical list when each item has more than five words or the inline sentence exceeds 25 words.
- **Code blocks in items:** put the code block after the item text, indented under the item. The item still starts with an uppercase letter; do not start an item with a code fence.

### Grammar notes

- Each item must complete the introductory sentence grammatically ("Introductory text [item]" reads as one sentence).
- Use "the" or "a/an" consistently across items; put the article before the backticks when the item starts with a code identifier.
- A full sentence has a subject and a finite verb. "Set the timeout value" is a full imperative sentence (period). "The `timeout` parameter that controls the delay" is a relative clause (no period until the last item).

### Summary checklist

- [ ] The introductory sentence ends with a colon.
- [ ] Each item starts with an uppercase letter.
- [ ] Each item connects to the introductory text.
- [ ] No period on non-sentence items; period on the last item.
- [ ] No mixed procedural and descriptive items in one list.
- [ ] No nested vertical lists.
- [ ] Each code sample (if any) comes after its item sentence.
