# Rule 6.1 — Give Information Gradually

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.1

## Original Rule

In a descriptive text, give information gradually and make sure that each sentence contains only one subject. If you give too much information too quickly, your text will not be easy to understand, and it will be necessary for the reader to read it again.

## STE-Code Adaptation

In code documentation, give information gradually and make sure that each sentence contains only one subject. If you give too much information too quickly, your documentation will not be easy to understand, and it will be necessary for the developer to read it again.

### Examples

> **Non-STE:** The authentication middleware validates bearer tokens from the authorization header by calling the `validateToken` function in the security module which decodes the JWT payload using the `HS256` algorithm from the `jwt-signer` library and checks the `exp` claim against the current server time before extracting the `sub` and `role` claims and attaching them as properties on the `request.auth` object, and if the token is expired or malformed the middleware returns a `401 Unauthorized` response with a JSON error body containing a `message` field and an `errorCode` field set to `TOKEN_EXPIRED` or `TOKEN_MALFORMED` respectively, while also logging the failure to the audit trail via the `AuditLogger.log` static method which writes to the `audit_events` table in the primary database using an asynchronous write pattern that does not block the response pipeline.

> **STE:** The authentication middleware validates each incoming request. The middleware reads the bearer token from the `Authorization` header. It sends the token to the `validateToken` function in the `security` module. The `validateToken` function decodes the JWT payload. It uses the `HS256` algorithm from the `jwt-signer` library. Then it compares the `exp` claim with the current server time. If the token is not expired and not malformed, the function gets the `sub` and `role` claims. It attaches these claims as properties on the `request.auth` object. If the token is expired, the middleware returns a `401 Unauthorized` response. The response body is a JSON object:
> - The `message` field contains a description of the error.
> - The `errorCode` field is set to `TOKEN_EXPIRED`.
> If the token is malformed, the middleware returns a `401 Unauthorized` response. The `errorCode` field in the response is set to `TOKEN_MALFORMED`. The middleware also logs each failure to the audit trail. It calls the `AuditLogger.log` static method. This method writes a record to the `audit_events` table in the primary database. The write uses an asynchronous pattern that does not block the response pipeline.
>
> *Code-domain example — each sentence in the STE version contains only one subject, giving information gradually.*

> **See also:** Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure; Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence; Rule 6.4 — Use Paragraphs to Show Related Information; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic
