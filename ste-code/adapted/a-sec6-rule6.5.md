# Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.5

## Original Rule

In descriptive writing, paragraphs describe topics, and it is important that each paragraph has only one topic. The topic sentence is the first and most important sentence in a paragraph. The topic sentence gives new information and makes a logical connection between the new information and previous information. To make a logical connection in a paragraph, the topic sentence usually contains a key word and/or a connecting word or connecting phrase.

From the topic sentences, the reader will understand the contents of your text and will find the applicable information quickly. If the reader writes down each of the topic sentences from a text, they will make a good outline of its content. The other sentences in each paragraph give the information a logical structure and add more information on the topic of the paragraph.

## STE-Code Adaptation

In descriptive code documentation, paragraphs describe topics, and it is important that each paragraph has only one topic. The topic sentence is the first and most important sentence in a paragraph. The topic sentence gives new information and makes a logical connection between the new information and previous information. To make a logical connection in a paragraph, the topic sentence usually contains a key word and/or a connecting word or connecting phrase.

From the topic sentences, the developer will understand the contents of your documentation and will find the applicable information quickly. If the developer writes down each of the topic sentences from the documentation, they will make a good outline of its content. The other sentences in each paragraph give the information a logical structure and add more information on the topic of the paragraph.

### Examples

> **Non-STE:** The authentication middleware validates each request and the logging system records all validation failures to the audit trail while the response pipeline returns JSON error bodies with error codes and the database connection pool maintains idle connections for reuse and the configuration module reloads settings when the manifest file changes on disk.

> **STE:**
>
> The authentication middleware validates each incoming request. The middleware reads the bearer token from the `Authorization` header. It sends the token to the `validateToken` function in the `security` module. The `validateToken` function decodes the JWT payload using the `HS256` algorithm from the `jwt-signer` library. Then it compares the `exp` claim with the current server time. If the token is not expired and not malformed, the function gets the `sub` and `role` claims and attaches them to the `request.auth` object.
>
> If the token is expired, the middleware returns a `401 Unauthorized` response. The response body is a JSON object with a `message` field and an `errorCode` field set to `TOKEN_EXPIRED`. If the token is malformed, the middleware returns a `401 Unauthorized` response with the `errorCode` field set to `TOKEN_MALFORMED`.
>
> The middleware also logs each failure to the audit trail. It calls the `AuditLogger.log` static method. This method writes a record to the `audit_events` table in the primary database. The write uses an asynchronous pattern that does not block the response pipeline.
>
> *Code-domain example — the Non-STE version combines multiple topics into one sentence; the STE version separates them into three paragraphs, each with one topic.*

In the STE text, the documentation is divided into three paragraphs:

- Paragraph 1 – The topic is: "How the authentication middleware validates a token."
- Paragraph 2 – The topic is: "What error responses the middleware returns."
- Paragraph 3 – The topic is: "How the middleware logs failures to the audit trail."

When you read only the topic sentences, you get an outline of the documentation:

- "The authentication middleware validates each incoming request."
- "If the token is expired, the middleware returns a `401 Unauthorized` response."
- "The middleware also logs each failure to the audit trail."

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure; Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence; Rule 6.4 — Use Paragraphs to Show Related Information
