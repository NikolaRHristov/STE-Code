# Rule 6.1 — Give Information Gradually

## Original Rule Summary

Rule 6.1 requires that descriptive text give information gradually by ensuring each sentence contains only one subject. When too much information arrives too quickly, the text becomes difficult to understand and the reader must read it again. Writers must start with the main idea and add detail in subsequent sentences, letting the reader absorb one fact before moving to the next. This rule applies to all descriptive text including documentation, explanations, introductions, and supplementary information.

## STE-Code Adaptation

In code documentation, Rule 6.1 requires each descriptive sentence to contain only one subject so that developers can absorb information on the first reading. Packing multiple actions, conditions, return values, error states, and architectural details into one sentence forces the reader to re-read and parse complex nesting. API documentation, README files, docstrings, commit message bodies, error messages, and changelog entries must all present information one subject at a time. When a function does three things, use three sentences — one per behavior — and do not chain parameter descriptions, response structures, and error conditions into a single compound sentence.

## Example Pairs

> **Non-STE:** The `findUsers` function connects to the MongoDB `users` collection and applies the given filter criteria using the `query` parameter before sorting the results by the field specified in `sortBy` in ascending or descending order based on the `sortDirection` parameter and then limits the result set to the number specified in `limit` while skipping the first `offset` documents to enable pagination.
>
> **STE:** The `findUsers` function connects to the `users` collection in MongoDB. It uses the `query` parameter to filter the documents. Then it sorts the results by the field in the `sortBy` parameter. The sort order is set by the `sortDirection` parameter. The function limits the result set to the number in the `limit` parameter. It skips the first `offset` documents. These two parameters enable pagination.

> **Non-STE:** The `server.config` file defines the application's runtime behavior including the HTTP port number which defaults to 3000 and the database connection string that must point to a running PostgreSQL instance with the credentials specified in the `DB_USER` and `DB_PASS` environment variables and the log level which can be set to debug, info, warn, or error and controls how much detail the application writes to the standard output stream.
>
> **STE:** The `server.config` file defines the runtime behavior of the application. The `port` setting controls the HTTP port number. Its default value is 3000. The `databaseUrl` setting points to a running PostgreSQL instance. The `DB_USER` and `DB_PASS` environment variables hold the credentials. The `logLevel` setting controls the detail written to standard output. Its values can be `debug`, `info`, `warn`, or `error`.

> **Non-STE:** The authentication middleware validates bearer tokens from the authorization header by calling the `validateToken` function in the security module which decodes the JWT payload using the `HS256` algorithm from the `jwt-signer` library and checks the `exp` claim against the current server time before extracting the `sub` and `role` claims and attaching them as properties on the `request.auth` object, and if the token is expired or malformed the middleware returns a `401 Unauthorized` response with a JSON error body containing a `message` field and an `errorCode` field set to `TOKEN_EXPIRED` or `TOKEN_MALFORMED` respectively, while also logging the failure to the audit trail via the `AuditLogger.log` static method which writes to the `audit_events` table in the primary database using an asynchronous write pattern that does not block the response pipeline.
>
> **STE:** The authentication middleware validates each incoming request. The middleware reads the bearer token from the `Authorization` header. It sends the token to the `validateToken` function in the `security` module. The `validateToken` function decodes the JWT payload. It uses the `HS256` algorithm from the `jwt-signer` library. Then it compares the `exp` claim with the current server time. If the token is not expired and not malformed, the function gets the `sub` and `role` claims. It attaches these claims as properties on the `request.auth` object. If the token is expired, the middleware returns a `401 Unauthorized` response. The response body is a JSON object:
> - The `message` field contains a description of the error.
> - The `errorCode` field is set to `TOKEN_EXPIRED`.
> If the token is malformed, the middleware returns a `401 Unauthorized` response. The `errorCode` field in the response is set to `TOKEN_MALFORMED`. The middleware also logs each failure to the audit trail. It calls the `AuditLogger.log` static method. This method writes a record to the `audit_events` table in the primary database. The write uses an asynchronous pattern that does not block the response pipeline.

## Principles Applied

**P4** — Write one topic per descriptive sentence. Each sentence in the STE examples addresses exactly one subject: one function behavior, one configuration setting, or one middleware action. Packing multiple subjects into one sentence forces the reader to re-read.

**P13** — Do not use semicolons or conjunctions to join independent clauses. The Non-STE examples chain many clauses with "and," "while," "before," and "which." Replacing these with periods between sentences naturally enforces one subject per sentence.

**P1** — Use approved words from the controlled terminology. Short, approved words reduce sentence complexity and make it easier to isolate one subject per sentence. Compound sentences often grow long because unapproved words need extra clauses for explanation.

**P8** — Use the approved active voice. Active voice keeps the subject-action relationship direct and clear. When every sentence starts with a clear subject performing a clear action, the reader can absorb each fact without re-parsing.
