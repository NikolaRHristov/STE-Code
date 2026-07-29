# Rule 6.3 — Write Short Sentences (Maximum 25 Words)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.3

## Original Rule

Good technical writing uses short sentences for complex topics. Short sentences give a clear structure to your writing and make information easier to understand.

In descriptive writing, the maximum sentence length is 25 words. This is because descriptive text is more complex than procedural text.

## STE-Code Adaptation

Good code documentation uses short sentences for complex topics. Short sentences give a clear structure to your API references, module descriptions, and architecture overviews and make the information easier to understand.

In code documentation, the maximum sentence length is 25 words. This is because descriptive text about software systems is more complex than procedural text such as step-by-step setup instructions.

### Examples

The non-STE example below is one long sentence that tries to describe multiple capabilities of a system at once. The STE-Code text breaks the same information into short sentences. Each sentence describes one subject.

> **Non-STE:** The API Client Library provides the ability to send HTTP requests with automatic retry logic, request timeout configuration, response caching with configurable TTL values, and authentication token refresh when the current token expires or when the server returns a 401 Unauthorized status code. (42 words)

> **STE-Code:** The API Client Library can send HTTP requests. The library has automatic retry logic for failed requests. You can configure a timeout value for each request. The library can cache responses with a configurable TTL value. It can also refresh the authentication token. It refreshes the token when the current token expires. It also refreshes the token when the server returns a 401 Unauthorized status code.

The STE-Code text uses seven sentences. Each sentence has fewer than 25 words. Each sentence describes only one subject. The developer can understand each piece of information without having to parse a long, complex sentence.
