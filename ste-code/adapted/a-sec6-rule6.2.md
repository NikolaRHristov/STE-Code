# Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.2

## Original Rule

Key words are words that occur in a text to connect different ideas, and key phrases are phrases that have the same function.

These key words and key phrases show how information in a text is related and give the text a logical structure.

You can also use connecting words and connecting phrases to help the reader understand the logical flow of ideas in the text. Connecting words and connecting phrases have the function of traffic signs, which tell the reader if the information is new, different, or a result of previous information. Examples of approved connecting words are: "and," "but," "then," "thus," and examples of connecting phrases are "as a result," and "at the same time."

When you use key words and key phrases, make sure that you do not change them in your text. The same terminology will keep your text clear and correct.

## STE-Code Adaptation

In code documentation, use key words and key phrases to connect related ideas across sentences. Key words are terms that occur multiple times in a documentation block to link different concepts together. Key phrases are multi-word expressions that serve the same connecting function.

These key words and key phrases show how information in the documentation is related and give the documentation a logical structure.

You can also use connecting words and connecting phrases to help the developer understand the logical flow of ideas. Connecting words and connecting phrases have the function of traffic signs, which tell the reader if the information is new, different, or a result of previous information. Examples of approved connecting words are: "and," "but," "then," "thus," and examples of connecting phrases are "as a result," and "at the same time."

When you use key words and key phrases, make sure that you do not change them in your documentation. The same terminology will keep your documentation clear and correct.

### Examples

The example that follows is the STE text from the adapted example for rule 6.1. In the text, you can see how the underlined key words and key phrases connect sentences and their related ideas. This makes the documentation much easier to read and understand.

**Sentence 1 and Sentence 2:**

> Sentence 1: The authentication middleware validates each incoming request.
> Sentence 2: The middleware reads the bearer token from the `Authorization` header.

Sentence 2 uses the key word "middleware" again to add more information about sentence 1.

**Sentence 2 and Sentence 3:**

> Sentence 2: The middleware reads the bearer token from the `Authorization` header.
> Sentence 3: It sends the token to the `validateToken` function in the `security` module.

Sentence 3 uses the key word "token" again and adds new information about what the middleware does with it.

**Sentence 3 and Sentence 4:**

> Sentence 3: It sends the token to the `validateToken` function in the `security` module.
> Sentence 4: The `validateToken` function decodes the JWT payload.

Sentence 4 uses the key phrase "`validateToken` function" again and gives more details about its behavior.

**Sentence 4 and Sentence 5:**

> Sentence 4: The `validateToken` function decodes the JWT payload.
> Sentence 5: It uses the `HS256` algorithm from the `jwt-signer` library.

Sentence 5 uses the key word "uses" to connect to "decodes" in sentence 4, showing the method by which the function operates.

**Sentence 8 and Sentence 9:**

> Sentence 8: If the token is expired, the middleware returns a `401 Unauthorized` response.
> Sentence 9: The response body is a JSON object.

Sentence 9 uses the key word "response" again to add more detail about what the response contains.

**Sentence 11 and Sentence 12:**

> Sentence 11: The `errorCode` field is set to `TOKEN_EXPIRED`.
> Sentence 12: If the token is malformed, the middleware returns a `401 Unauthorized` response.

Sentences 11 and 12 use the key word "token" again. Sentence 12 then introduces the alternative condition "malformed" by contrasting with the previous condition "expired."

**Sentence 14 and Sentence 15:**

> Sentence 14: The middleware also logs each failure to the audit trail.
> Sentence 15: It calls the `AuditLogger.log` static method.

Sentence 15 uses the key phrase "audit" again (from "audit trail") to connect the logging mechanism with the specific method name.

There is also a logical connection between the three groups of sentences:

- Group 1 (Sentences 1 thru 7): token validation, `validateToken`, JWT, claims, `request.auth`
- Group 2 (Sentences 8 thru 13): error responses, `401 Unauthorized`, `errorCode`, `TOKEN_EXPIRED`, `TOKEN_MALFORMED`
- Group 3 (Sentences 14 thru 17): audit trail, `AuditLogger.log`, database, `audit_events`, asynchronous write

> *The analysis above applies Rule 6.2 to the STE text from Rule 6.1, demonstrating how key words and key phrases create a logical structure across sentences.*

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence; Rule 6.4 — Use Paragraphs to Show Related Information; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic
