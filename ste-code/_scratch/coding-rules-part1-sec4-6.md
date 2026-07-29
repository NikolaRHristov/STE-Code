# STE-Code — Part 1: Sections 4–6

---

## Section 4 — Statements and Expressions

### Summary of the rules

**Rule 4.1** Write short and clear statements.
**Rule 4.2** Do not omit words or use contractions.
**Rule 4.3** Use a vertical list for complex text.
**Rule 4.4** Use connecting words to link related statements.
**Rule 4.5** Use an article or demonstrative adjective before a Technical Code Noun.

---

### Rule 4.1 — Short and clear statements

> **Non-STE-Code:**
> ```
> // To process the payment, first validate the request body to ensure
> // all required fields are present, then call the payment gateway with
> // the sanitized data, and finally update the order status in the database.
> ```
>
> **STE-Code:**
> ```
> // 1. Validate the request body.
> // 2. Send the sanitized data to the payment gateway.
> // 3. Update the order status in the database.
> ```

In descriptive documentation, each sentence should have one topic:

> **Non-STE-Code:**
> ```
> // The AuthService manages authentication, validates credentials against
> // the configured identity provider, issues JWT tokens on success, and
> // the tokens expire after 24 hours by default.
> ```
>
> **STE-Code:**
> ```
> // The AuthService manages authentication.
> // It validates credentials against the configured identity provider.
> // It issues a JWT token when authentication succeeds.
> // The token expires after 24 hours.
> ```

---

### Rule 4.2 — No omitted words or contractions

> **Non-STE-Code:** `// Don't call this fn w/out a valid auth token.`
> **STE-Code:** `// Do not call this function without a valid authentication token.`

> **Non-STE-Code:** `// It's recommended to use the cached version.`
> **STE-Code:** `// It is recommended to use the cached version.`

---

### Rule 4.3 — Vertical lists for complex text

> **Non-STE-Code:**
> ```
> // The API returns 200 for success, 400 for bad request when validation
> // fails or the payload is malformed, 401 for unauthorized when the token
> // is expired or missing, and 500 for internal server error.
> ```
>
> **STE-Code:**
> ```
> // The API returns these status codes:
> // - 200: The request succeeded.
> // - 400: The request is invalid. The payload is malformed or the validation failed.
> // - 401: The request is not authorized. The token is expired or missing.
> // - 500: An internal server error occurred.
> ```

**Vertical list rules:**
- Put a colon (:) at the end of the introductory sentence.
- Start each item with an uppercase letter.
- Use a period at the end of a full-sentence item.
- Do not use a period at the end of a non-sentence item.
- Do not use commas or semicolons at the end of items.

---

### Rule 4.4 — Connecting words

Approved connectors: `and`, `or`, `but`, `however`, `therefore`, `thus`, `because`,
`if`, `when`, `after`, `before`, `while`, `although`, `unless`, `until`, `so that`.

> **STE-Code:**
> ```
> // Call the validate function. If the validation succeeds, call the
> // process function. However, if the validation fails, return an error
> // to the client.
> ```

> **STE-Code:**
> ```
> // The cache stores results in memory. Thus, subsequent requests are
> // faster. But the cache can become stale. Therefore, the system
> // invalidates the cache after 60 seconds.
> ```

---

### Rule 4.5 — Articles and demonstrative adjectives

> **Non-STE-Code:** `// Call validate function on request object.`
> **STE-Code:** `// Call the validate function on the request object.`

> **Non-STE-Code:** `// Send response to client with status code.`
> **STE-Code:** `// Send the response to the client with a status code.`

Do not use articles with alphanumeric identifiers (proper nouns):

> **Incorrect:** `// Call the UserService.create() method.`
> **Correct:** `// Call UserService.create().`

---

## Section 5 — Procedural Code Documentation

### Summary of the rules

**Rule 5.1** Write short sentences. Maximum 20 words per procedural sentence.
**Rule 5.2** Write only one instruction per sentence unless actions occur simultaneously.
**Rule 5.3** Write instructions in the imperative (command) form.
**Rule 5.4** When there is a condition, start with a descriptive statement, then give the command.
**Rule 5.5** Write notes only to give information, not instructions.

---

### Rule 5.1 — Maximum 20 words per procedural sentence

Procedural documentation includes: commit messages, setup guides, runbooks,
code review action items.

> **Non-STE-Code commit message (28 words):**
> ```
> Fix the race condition that occurs when multiple concurrent requests try
> to acquire a database connection from the pool at the same time without
> proper mutex synchronization
> ```
>
> **STE-Code commit message (20 words max each):**
> ```
> Fix race condition in the database connection pool
>
> Acquire the mutex before checking the connection state.
> Release the mutex after the state is updated.
> ```

---

### Rule 5.2 — One instruction per sentence

> **Non-STE-Code:**
> ```
> // Install the dependencies and then start the development server and
> // open the browser to localhost:3000.
> ```
>
> **STE-Code:**
> ```
> // 1. Install the dependencies.
> // 2. Start the development server.
> // 3. Open the browser at http://localhost:3000.
> ```

**Permitted simultaneous actions:**
> `// Run the linter and the type checker at the same time.`

---

### Rule 5.3 — Imperative (command) form

> **Non-STE-Code:** `// The server should be restarted after the configuration change.`
> **STE-Code:** `// Restart the server after the configuration change.`

> **Non-STE-Code:** `// The database migration can be run with the --force flag.`
> **STE-Code:** `// Run the database migration. Use the --force flag if necessary.`

---

### Rule 5.4 — Condition before command

> **STE-Code:**
> ```
> // If the database is not available, retry the connection after 5 seconds.
> ```

> **STE-Code:**
> ```
> // When the build fails, examine the error log before you run the build again.
> ```

---

### Rule 5.5 — Notes: information only

> **Correct note (information):**
> ```
> // NOTE: The default timeout for the HTTP client is 30 seconds.
> ```

> **Incorrect note (contains instruction):**
> ```
> // NOTE: Set the timeout to 30 seconds if you use the default client.
> ```
> **Correct as instruction:**
> ```
> // 4. Set the HTTP client timeout to 30 seconds.
> ```

---

## Section 6 — Declarative Code Documentation

### Summary of the rules

**Rule 6.1** Give information gradually.
**Rule 6.2** Use key words and key phrases to give your text a logical structure.
**Rule 6.3** Write short sentences. Maximum 25 words per descriptive sentence.
**Rule 6.4** Use paragraphs to show related information.
**Rule 6.5** Make sure that each paragraph has only one topic.
**Rule 6.6** Make sure that no paragraph has more than six sentences.

---

### Rule 6.1 — Give information gradually

> **Non-STE-Code:**
> ```
> // The PaymentService handles all payment operations including credit card
> // validation through the Stripe API, order total calculation with tax and
> // shipping, payment status tracking via webhooks, and automatic refund
> // processing for cancelled orders with configurable refund windows.
> ```
>
> **STE-Code:**
> ```
> // The PaymentService handles payment operations.
> // It validates credit cards through the Stripe API.
> // It calculates the order total with tax and shipping.
> // It tracks payment status through webhooks.
> // It processes automatic refunds for cancelled orders.
> // The refund window is configurable.
> ```

---

### Rule 6.2 — Key words and key phrases

Approved key phrases: `is responsible for`, `has these properties`, `returns`,
`accepts`, `requires`, `depends on`, `implements`, `extends`, `consists of`.

> **STE-Code:**
> ```
> // The CacheManager has these properties:
> // - It stores results in memory.
> // - It uses an LRU eviction policy.
> // - It supports time-to-live for each entry.
> // - It exposes a pub/sub interface for invalidation events.
> ```

---

### Rule 6.3 — Maximum 25 words per descriptive sentence

> **Non-STE-Code (32 words):**
> ```
> // The authentication middleware intercepts every incoming HTTP request
> // and validates the JWT token that is present in the Authorization header
> // before the request reaches any protected route handler.
> ```
>
> **STE-Code (14 + 15 words):**
> ```
> // The authentication middleware intercepts every incoming HTTP request.
> // It validates the JWT token in the Authorization header before the
> // request reaches a protected route handler.
> ```

---

### Rules 6.4–6.6 — Paragraphs

**Rule 6.4:** Use paragraphs to group related sentences.

**Rule 6.5:** Each paragraph covers one topic. Start a new paragraph when the topic changes.

**Rule 6.6:** Maximum six sentences per paragraph.

> **STE-Code (6-sentence paragraph):**
> ```
> // The UserService manages user accounts.
> // It provides methods to create, read, update, and delete users.
> // It validates email addresses and password strength.
> // It hashes passwords before storage.
> // It emits events when a user account changes.
> // Other services can subscribe to these events.
>
> // The UserService depends on the DatabaseService.
> // It uses the DatabaseService to persist user data.
> // It requires a configured DatabaseService instance at initialization.
> ```
