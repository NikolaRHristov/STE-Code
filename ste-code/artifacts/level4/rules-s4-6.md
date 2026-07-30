### Section 4 — Clarity and Sentence Structure

**Rule 4.1 — Write Short and Clear Sentences**
Every sentence must be short, clear, and accurate. In procedures, give short instructions in imperative form; in descriptive text, cover one topic per sentence with a maximum of 25 words. Never use abstract statements — clearly show how to do a task or how a system operates.

> **Non-STE:** The `processUpload` function validates the file type, checks the file size against the configured maximum, scans for malware using the integrated scanner, and then stores the file in the configured cloud storage bucket while logging the operation to the audit trail.
> **STE:** The `processUpload` function validates the file type. It checks the file size against the configured maximum. It scans for malware with the integrated scanner. Then it stores the file in the cloud storage bucket. It logs the operation to the audit trail.

> **Non-STE:** No null values are permitted.
> **STE:** Make sure that the method does not return a null value.

**Rule 4.2 — Do Not Omit Words or Use Contractions to Make Your Sentences Shorter**
Every sentence must include its subject, verb, nouns, and articles without omission. Contractions such as "don't," "isn't," and "won't" are prohibited because they obscure word forms and create ambiguity for non-native readers. Restore all omitted words so every sentence is self-contained and unambiguous.

> **Non-STE:** Can accept a string or a Buffer. Returns the parsed result. Doesn't throw on invalid input.
> **STE:** The function can accept a string or a Buffer object. The function returns the parsed result. The function does not throw an error on invalid input.

> **Non-STE:** Copy `.env.example` to `.env` and update database URL. The app won't run if this step isn't done.
> **STE:** Copy the `.env.example` file to a `.env` file. Update the database URL in the `.env` file. The application will not run if this step is not completed.

**Rule 4.3 — Use a Vertical List for Complex Texts**
Use vertical lists when a sentence must include many items such as function parameters, error codes, or configuration options. Start each item with an uppercase letter, use a colon before the first item, and never mix imperative instructions with descriptive statements in the same list. Nested vertical lists are not permitted.

> **Non-STE:** The API returns 400 for validation issues, 401 when the token is expired or missing, 403 if permissions are insufficient, 404 when the resource is not found, and 500 for any unhandled internal failure.
> **STE:** The API returns these error codes:
> - `400 Bad Request` for a failed input validation
> - `401 Unauthorized` for an expired or missing token
> - `403 Forbidden` for insufficient permissions
> - `404 Not Found` for a missing resource
> - `500 Internal Server Error` for an unhandled failure.

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

**Rule 4.4 — Use Connecting Words and Connecting Phrases to Connect Sentences That Contain Related Topics**
Use approved connecting words (and, but, then, thus) and connecting phrases (as a result, at the same time) to show logical relationships between sentences. Demonstrative adjectives (this, these) must refer to a specific code element named in the previous sentence, never to a vague or implied antecedent.

> **Non-STE:** The `AuthService` authenticates the request token. If the token is valid, the middleware forwards the request to the route handler. The route handler processes the business logic and returns a response.
> **STE:** The `AuthService` authenticates the request token. Then, if the token is valid, the middleware forwards the request to the route handler. And the route handler processes the business logic, thus returning a response.

> **Non-STE:** Configure the connection pool in the database client. The pool size limits the number of concurrent queries. Exceeding the limit causes connection timeouts on new requests.
> **STE:** Configure the connection pool in the database client. This pool size limits the number of concurrent queries. As a result, if the limit is exceeded, new requests get connection timeouts.

**Rule 4.5 — When Applicable, Use an Article (the, a, an) or a Demonstrative Adjective (this, these) Before a Noun or a Multi-Word Noun**
Use articles to show whether a noun refers to a specific instance (the configuration file) or a general concept (configuration). Do not use a definite article before a noun followed by a code identifier, because the identifier is already a proper noun. Omit articles for abstract concepts like "performance" or "scalability."

> **Non-STE:** Call callback function after request completes.
> **STE:** Call the callback function after the request completes.

> **Non-STE:** Call the function `validateInput` with the parameter `userId`.
> **STE:** Call function `validateInput` with parameter `userId`.

### Section 5 — Procedural Writing

**Rule 5.1 — Short Sentences (Maximum 20 Words)**
Every sentence in procedural text must use a maximum of 20 words. Break long procedural sentences into shorter sentences that each focus on one part of the task. Warnings, cautions, and safety instructions also obey the 20-word limit; notes may use up to 25 words.

> **Non-STE:** Run the database migration script from the project root directory and then restart the application server to apply all pending schema changes to the production environment.
> **STE:** Run the database migration script from the project root directory. Then, restart the application server to apply all pending schema changes.

> **Non-STE:** Build the Docker image using the Dockerfile in the project root and then run a container from that image with port 8080 on the host mapped to port 80 inside the container.
> **STE:** Build the Docker image. Use the Dockerfile in the project root. Then, run a container from that image. Map port 8080 on the host to port 80 inside the container.

**Rule 5.2 — One Instruction Per Sentence**
Each procedural sentence must contain exactly one instruction. Use numbered or bulleted lists to show the sequence of steps clearly, with only one instruction per list item. Two instructions may appear in one sentence with "and" only when both actions occur at the same time.

> **Non-STE:** Open the configuration file in a text editor and locate the database section and change the connection string to point to the staging server and then save the file and close the editor.
> **STE:**
> 1. Open the configuration file in a text editor.
> 2. Locate the database section.
> 3. Change the connection string to point to the staging server.
> 4. Save the file.
> 5. Close the editor.

> **Non-STE:** Make sure the environment variable DATABASE_URL is set correctly and then execute the initialization script to create the required database tables and populate them with the seed data.
> **STE:** Make sure that the environment variable DATABASE_URL is set correctly. Then, execute the initialization script. The script creates the required database tables and populates them with the seed data.

**Rule 5.3 — Imperative (Command) Form for Instructions**
All instructions must use the imperative mood — start each step with a verb such as run, set, open, save, or install. Do not use passive voice, gerunds, or modal verbs (can, could, should, may, might) for instructions. The imperative form eliminates ambiguity about who acts and when.

> **Non-STE:** The dependencies can be installed by running `npm install`, and then the server should be started with `npm run dev`.
> **STE:** Install the dependencies with `npm install`. Start the server with `npm run dev`.

> **Non-STE:** You can authenticate by sending a POST request to `/auth/login` with your credentials, and you should include the returned token in the `Authorization` header.
> **STE:** Send a POST request to `/auth/login` with your credentials. Include the returned token in the `Authorization` header.

**Rule 5.4 — Descriptive Statement Before the Command**
When an instruction depends on a prerequisite condition, place the descriptive statement before the command and separate the two with a comma. This structure ensures the reader evaluates the condition before executing the instruction, preventing errors from acting on incomplete or invalid state.

> **Non-STE:** Run the database migration script after you set the `DATABASE_URL` environment variable to your production database connection string and confirmed that the database server is accepting connections.
> **STE:** After you set the `DATABASE_URL` environment variable, run the database migration script.

> **Non-STE:** You can call the `/users` endpoint to retrieve a list of users but only after you have obtained a valid OAuth2 access token from the `/auth/token` endpoint and included it in the Authorization header of your request.
> **STE:** After you get a valid OAuth2 access token from the `/auth/token` endpoint, call the `/users` endpoint. Include the token in the `Authorization` header.

**Rule 5.5 — Notes Give Information Only, Not Instructions**
Notes must contain descriptive information only — never instructions, commands, requirements, or limits. If a note contains instructions, move them into numbered work steps. If a note contains critical safety information, move it into a WARNING or CAUTION instruction.

> **Non-STE:** NOTE: When you update the dependencies, run the command `npm audit fix` to resolve known vulnerabilities. If you skip this step, your application may have security issues.
> **STE:** (5) Run the command `npm audit fix` to resolve known vulnerabilities.

> **Non-STE:** NOTE: The response time must be less than 200 milliseconds under normal load conditions. If the response time is higher than 200 milliseconds, investigate the database query performance.
> **STE:** The response time must be less than 200 milliseconds under normal load conditions.

### Section 6 — Descriptive Writing

**Rule 6.1 — Give Information Gradually**
Each descriptive sentence must contain only one subject so developers can absorb information on the first reading. Start with the main idea and add detail in subsequent sentences. Never pack multiple actions, conditions, return values, and error states into one compound sentence.

> **Non-STE:** The `findUsers` function connects to the MongoDB users collection and applies the filter criteria using the `query` parameter before sorting the results by the field in `sortBy` in ascending or descending order based on `sortDirection` and then limits the result set to `limit` while skipping the first `offset` documents for pagination.
> **STE:** The `findUsers` function connects to the `users` collection in MongoDB. It uses the `query` parameter to filter the documents. Then it sorts the results by the field in the `sortBy` parameter. The sort order is set by the `sortDirection` parameter. The function limits the result set to the number in the `limit` parameter. It skips the first `offset` documents. These two parameters enable pagination.

> **Non-STE:** The `server.config` file defines the application's runtime behavior including the HTTP port which defaults to 3000 and the database connection string that must point to a running PostgreSQL instance with credentials in `DB_USER` and `DB_PASS` and the log level which can be debug, info, warn, or error and controls the detail written to standard output.
> **STE:** The `server.config` file defines the runtime behavior of the application. The `port` setting controls the HTTP port number. Its default value is 3000. The `databaseUrl` setting points to a running PostgreSQL instance. The `DB_USER` and `DB_PASS` environment variables hold the credentials. The `logLevel` setting controls the detail written to standard output. Its values can be `debug`, `info`, `warn`, or `error`.

**Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure**
Use key words (class names, function names, technical nouns) and key phrases (multi-word terms like "connection pool") consistently across sentences to link related ideas. Approved connecting words (and, but, then, thus) act as traffic signs showing whether information is new, different, or a result of previous information. Never change key words mid-documentation.

> **Non-STE:** `redis.host` sets the Redis server address. The default is `localhost` on the usual port. You can override this with an environment variable.
> **STE:** The `redis.host` option sets the Redis server hostname. The default hostname is `localhost`. Set the `REDIS_HOST` environment variable to override the default hostname.

> **Non-STE:** The parser encounters invalid JSON. An exception gets raised with the position. The caller catches it and logs the incident.
> **STE:** The parser finds invalid JSON. The parser raises a `ParseError` exception. The caller catches the `ParseError`. The caller logs the `ParseError` to the error log.

**Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence.**
Descriptive text must use a maximum of 25 words per sentence. Long sentences hide important details inside dense clauses and make scanning difficult for developers. Split long sentences into multiple short sentences, each describing one concept.

> **Non-STE:** The `migrateDatabase` function connects to the source and target databases, compares their schemas to detect any structural differences, and then generates the SQL migration scripts that will bring the target database into alignment with the source schema.
> **STE:** The `migrateDatabase` function connects to the source database. It connects to the target database. It compares the two schemas. It finds structural differences. It then makes SQL migration scripts. These scripts align the target schema with the source schema.

> **Non-STE:** The GET /api/v1/reports endpoint returns a JSON array of report objects that includes metadata such as the report author, creation timestamp, and status field, and also supports pagination through the `page` and `per_page` query parameters with a default page size of 20.
> **STE:** The GET /api/v1/reports endpoint returns a JSON array of report objects. Each object includes metadata about the report. The metadata includes the author, creation timestamp, and status. Use the `page` and `per_page` query parameters for pagination. The default page size is 20.

**Rule 6.4 — Use Paragraphs to Show Related Information**
Use paragraphs to group related information with a clear topic sentence at the start of each paragraph. When a new paragraph starts, the reader knows the text introduces a new topic. Break walls of text into topic-focused paragraphs so developers can scan for the section they need.

> **Non-STE:** To install, run `pip install mylib` and then create a config file at `~/.mylib.toml` with your API key. The library supports Python 3.9 and above and requires a Redis instance for caching, which you can start with `redis-server`. You can also use SQLite for development without Redis.
> **STE:**
> **Installation**
> Install the library with pip. Run this command: `pip install mylib`.
>
> **Configuration**
> Create a configuration file at `~/.mylib.toml`. Add your API key to this file.
>
> **Dependencies**
> The library supports Python 3.9 and above. A Redis instance is necessary for caching. Start Redis with this command: `redis-server`. For development without Redis, use SQLite as the cache backend.

> **Non-STE:** The `GET /api/v1/orders/:id` endpoint retrieves a single order by its ID and requires a valid bearer token in the Authorization header, returning a 404 if the order is not found or a 403 if the user does not have permission to view the order. The response body is a JSON object with fields for the order ID, customer name, list of line items, total amount, and status, and the status field can be one of `pending`, `confirmed`, `shipped`, or `delivered`.
> **STE:**
> **Endpoint**
> The `GET /api/v1/orders/:id` endpoint retrieves a single order. Use the `:id` path parameter to identify the order.
>
> **Authentication**
> This endpoint requires a valid bearer token. Include the token in the `Authorization` header. If the token is missing or invalid, the endpoint returns a `401 Unauthorized` response. If the user does not have permission to view the order, the endpoint returns a `403 Forbidden` response.
>
> **Response**
> The endpoint returns a JSON object. The object contains these fields:
> - `id` — the order identifier
> - `customerName` — the name of the customer
> - `lineItems` — a list of items in the order
> - `total` — the total amount
> - `status` — the current status of the order.
>
> **Status Values**
> The `status` field can have one of these values: `pending`, `confirmed`, `shipped`, or `delivered`.

**Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic**
Each paragraph must cover exactly one topic. The topic sentence is the first sentence and links to the previous paragraph through a key word or connecting phrase. When a paragraph drifts into a second topic, split it at the topic boundary so developers can find specific information by scanning only the first sentence of each paragraph.

> **Non-STE:** The `UserController` class handles all user-related API endpoints including registration, login, password reset, and profile management. To register a new user, send a POST request to `/api/users` with a JSON body containing `username`, `email`, and `password`. The controller validates the input against the `UserSchema` and stores a bcrypt hash of the password in the `users` table. The login endpoint at POST `/api/auth/login` accepts `email` and `password` and returns a JWT access token and a refresh token. The rate limiter allows 5 login attempts per minute per IP address to prevent brute force attacks, and failed attempts are logged to the `auth_audit` table for security monitoring.
> **STE:**
> The `UserController` class handles all user-related API endpoints. It manages registration, login, password reset, and profile management.
>
> To register a new user, send a POST request to `/api/users`. The request body must contain `username`, `email`, and `password` as a JSON object. The controller validates the input against the `UserSchema`. It stores a bcrypt hash of the password in the `users` table.
>
> To log in, send a POST request to `/api/auth/login`. The request body must contain `email` and `password`. The endpoint returns a JWT access token and a refresh token.
>
> The login endpoint uses a rate limiter. The rate limiter allows five login attempts per minute per IP address. Failed login attempts are logged to the `auth_audit` table for security monitoring.

> **Non-STE:** The `CacheManager` module provides a unified interface for caching data in either Redis or Memcached backends depending on the `CACHE_DRIVER` environment variable. It automatically serializes complex objects using MessagePack before storing them and handles TTL expiration by setting the `cache.ttl` configuration option to a value in seconds. The cache also supports tagging so you can group related cache entries under a shared tag and invalidate the entire group with a single `invalidateTag` call without knowing the individual keys ahead of time.
> **STE:**
> The `CacheManager` module gives a unified interface for caching data. It can use a Redis backend or a Memcached backend. Set the `CACHE_DRIVER` environment variable to choose the backend.
>
> The `CacheManager` serializes complex objects before storage. It uses the MessagePack format for serialization.
>
> The `CacheManager` supports time-to-live expiration. Set the `cache.ttl` configuration option to a value in seconds.
>
> The `CacheManager` supports cache tags. Group related cache entries under one tag. Use the `invalidateTag` method to invalidate all entries in the tag group. You do not need to know the individual keys.
