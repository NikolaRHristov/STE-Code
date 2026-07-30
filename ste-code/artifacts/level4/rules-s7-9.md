### Section 7 — Safety Instructions

**Rule 7.1 — Use an Applicable Word (WARNING or CAUTION) to Identify the Level of Risk**
Every safety instruction in code documentation must begin with a signal word — WARNING or CAUTION — to immediately show the reader the level of risk. Use WARNING when there is a risk of security vulnerabilities, data loss, or system corruption. Use CAUTION when there is a risk of unexpected behavior, performance degradation, or incorrect results.

> **Non-STE:** CAUTION: ALWAYS VALIDATE INPUT DATA.
> **STE:** WARNING: BEFORE YOU PROCESS INPUT DATA, MAKE SURE THAT YOU SANITIZE AND VALIDATE THE DATA. UNSANITIZED INPUT CAN CAUSE SECURITY BREACHES AND DATA LOSS.

> **Non-STE:** CAUTION: THE CONFIGURATION FILE MAY CONTAIN OUTDATED SETTINGS.
> **STE:** CAUTION: BEFORE YOU DEPLOY THE APPLICATION, COMPARE THE CONFIGURATION FILE AGAINST THE REFERENCE CONFIGURATION. OUTDATED SETTINGS CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.

**Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition**
Every safety instruction must begin with either a clear command (DO NOT, ALWAYS, MAKE SURE) or a clear condition (IF YOU, BEFORE YOU, WHEN). The reader must know the prohibition, requirement, or prerequisite within the first three words of the instruction body. Background information and explanatory text follow the command or condition — they never precede it.

> **Non-STE:** WARNING: It is important to consider that hardcoding database credentials in the configuration file can lead to serious security issues if the file is committed to version control.
> **STE:** WARNING: DO NOT HARDCODE DATABASE CREDENTIALS IN THE CONFIGURATION FILE. STORE CREDENTIALS IN A SECRETS MANAGER OR ENVIRONMENT VARIABLES. HARDCODED CREDENTIALS IN VERSION CONTROL CAN CAUSE UNAUTHORIZED DATABASE ACCESS.

> **Non-STE:** CAUTION: The `/search` endpoint returns results from a cache that is updated every 5 minutes, so recent changes may not be reflected immediately.
> **STE:** CAUTION: BEFORE YOU USE THE `/search` ENDPOINT, READ THE CACHE STALENESS NOTE. THE CACHE IS UPDATED EVERY 5 MINUTES. RECENT CHANGES ARE NOT VISIBLE UNTIL THE NEXT CACHE UPDATE. DO NOT USE THIS ENDPOINT FOR REAL-TIME DATA.

**Rule 7.3 — Give an Explanation to Show the Risk or Possible Result**
Every WARNING or CAUTION must include a specific, concrete explanation of what goes wrong when the instruction is ignored. A safety instruction without a risk explanation is a prohibition without justification. The risk explanation must match the signal word severity — WARNING maps to data loss, security breach, or system unavailability; CAUTION maps to incorrect results, degraded performance, or build failures.

> **Non-STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE.
> **STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. API KEYS IN SOURCE CODE CAN CAUSE UNAUTHORIZED ACCESS AND DATA BREACHES.

> **Non-STE:** CAUTION: DO NOT USE DEPRECATED FUNCTIONS.
> **STE:** CAUTION: DO NOT USE DEPRECATED FUNCTIONS. DEPRECATED FUNCTIONS CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.

### Section 8 — Punctuation and Word Count

**Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon (;)**
The semicolon is not permitted in STE because it enables writers to construct overly long sentences that combine multiple independent clauses. In code documentation, the semicolon creates an additional hazard — it has a different meaning in many programming languages (statement terminator), which causes cognitive interference when the same symbol appears in documentation prose. Every semicolon-joined sentence must be split into two or more independent sentences, each with its own subject and verb.

> **Non-STE:** The server supports WebSocket connections; these use a persistent channel instead of the standard request-response cycle.
> **STE:** The server supports WebSocket connections. These connections use a persistent channel instead of the standard request-response cycle.

> **Non-STE:** POST /sessions creates a new session and returns a token; the token must be included in the Authorization header of subsequent requests.
> **STE:** A POST request to /sessions makes a new session and returns a token. You must include the token in the Authorization header of all later requests.

**Rule 8.2 — Use Hyphens (-) to Connect Words That Are Directly Related**
Use hyphens to connect words that form a compound adjective before a noun. This construction helps the reader parse which words are directly related and prevents ambiguity about what a modifier applies to. In code documentation, compound adjectives like "high-priority," "read-only," and "end-to-end" require hyphenation before the nouns they describe.

> **Non-STE:** The high priority task must acquire the write lock before it can modify the shared data structure.
> **STE:** The high-priority task must get the write lock before it can change the shared data structure.

> **Non-STE:** Use a read only file descriptor to open the configuration for parsing.
> **STE:** Use a read-only file descriptor to open the configuration for parsing.

**Rule 8.3 — Use of Parentheses**
Parentheses are permitted for specific purposes: to introduce abbreviations on first use, to explain parts of a sentence, to show singular and plural forms simultaneously, and to reference code modules or diagrams. Parentheses must not be nested, and the main sentence punctuation is not affected by the parenthetical content. Abbreviations defined in parentheses on first use must be used consistently thereafter.

> **Non-STE:** The application uses a DOM, or document object model, to represent the page structure, and an API, which stands for application programming interface, to fetch data from the server.
> **STE:** The application uses a Document Object Model (DOM) to represent the page structure and an Application Programming Interface (API) to fetch data from the server.

> **Non-STE:** Rate limit the endpoint to 100 requests per minute, which means you can send one request roughly every 600 milliseconds assuming uniform distribution.
> **STE:** Rate limit the endpoint to 100 requests per minute (approximately one request every 600 ms).

**Rule 8.4 — Colon in a Vertical List**
In a vertical list, the colon has the same effect on word count as a period and marks the end of a sentence. The introductory text before the colon must obey sentence-length limits (20 words for procedural, 25 words for descriptive). Each list item after the colon counts as a new sentence with its own length limit, and all items must be grammatically parallel.

> **Non-STE:** To handle all possible error conditions, the following exception types must be caught and processed by the error handler: database connection timeouts which occur when the primary node is unreachable, authentication failures caused by expired or invalid tokens, and validation errors due to malformed request payloads.
> **STE:** To handle possible error conditions, the error handler catches these exception types:
> - Database connection timeout
> - Authentication failure
> - Validation error.

> **Non-STE:** The configuration file, which is located in the project root, supports these environment profiles that you can use for deployment: a development profile for local testing and debugging, a staging profile for pre-production integration verification, and a production profile for the live customer-facing environment.
> **STE:** The configuration file supports these environment profiles:
> - Development
> - Staging
> - Production.

**Rule 8.5 — Parentheses and Word Count**
Text between parentheses counts as a single word in the enclosing sentence, regardless of how many words it contains internally. The words inside the parentheses form their own separate sentence with its own word-count limit. Safety-critical preconditions and warnings must never appear in parentheses — a reader scanning the documentation may skip the parenthetical content.

> **Non-STE:** Make sure that the DEBUG environment variable is set to false before you run the deployment script in the production cluster (the DEBUG flag must be explicitly disabled for all production workloads to prevent accidental log leakage).
> **STE:** Make sure that the DEBUG environment variable is set to false (the DEBUG flag is off).

> **Non-STE:** Failed to bind to port 8080 because the address is already in use by another process that was started previously and is still holding the socket open on that port number (you can identify the process using the lsof -i :8080 command and then terminate it with kill followed by the process ID, or you can configure this application to use a different port by setting the PORT environment variable to an alternative value such as 3000 or 9090 before restarting).
> **STE:** Cannot bind to port 8080 (EADDRINUSE). The address is in use. To find the process, run `lsof -i :8080`. To use a different port, set the PORT environment variable (example: 3000). Then restart the application.

**Rule 8.6 — Elements That Count as One Word**
When counting words for sentence length, certain multi-word elements each count as a single word: numbers, numbers with units of measurement, abbreviations, alphanumeric identifiers, quoted text, titles and headings, and proper nouns. This rule reduces the effective word count of technical sentences by 3 to 8 words compared to naive word counting, making it easier to obey sentence-length limits in API documentation and README files where identifiers and abbreviations occur at high density.

> **Non-STE:** The endpoint located at the uniform resource locator path of /api/v2/organizations/{organizationId}/repositories/{repositoryId}/branches accepts a Hypertext Transfer Protocol Secure GET request and requires an OAuth two point zero bearer token in the Authorization header with the format Bearer followed by a space and then the access token, and it returns a JavaScript Object Notation response body with a two hundred status code.
> **STE:** The `GET /api/v2/orgs/{orgId}/repos/{repoId}/branches` endpoint needs an OAuth 2.0 bearer token in the `Authorization` header. It returns a JSON response body with a 200 status code.

> **Non-STE:** In the YAML Ain't Markup Language configuration file located at the path etc/application/configuration/production.yaml, set the property spring.datasource.hikari.maximumPoolSize to a value of fifty and set the property server.tomcat.maxThreads to a value of two hundred, then also make sure that the property logging.level.com.example is set to the value DEBUG and the property management.endpoints.web.exposure.include is set to the value health,info,metrics.
> **STE:** In `etc/application/config/production.yaml`, set `spring.datasource.hikari.maximumPoolSize` to 50. Set `server.tomcat.maxThreads` to 200. Set `logging.level.com.example` to `DEBUG`. Set `management.endpoints.web.exposure.include` to `health,info,metrics`.

### Section 9 — Writing Practices

**Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient**
When a word-for-word replacement using the dictionary fails — because the approved alternative has a different part of speech, would change the meaning, or does not exist — you must write a completely new sentence using only approved words while preserving the same technical meaning. This frequently requires changing the grammatical structure, selecting different verbs, splitting long sentences, or removing unnecessary information. After restructuring, verify each approved word against Rule 9.2 and Rule 9.3.

> **Non-STE:** The stack trace in the console must be visible during the debugging session.
> **STE:** During the debugging session, make sure that you can see the stack trace in the console.

> **Non-STE:** This configuration option governs whether the linter enforces the rule set in a strict or permissive fashion.
> **STE:** This configuration option sets how the linter applies the rules. You can set it to strict or permitted.

**Rule 9.2 — Use Each Approved Word Correctly**
Approved words have restricted meanings that apply only in specific contexts. Before you use a word, read its definition in the approved meaning column of the dictionary — other meanings the word carries in standard English are not approved. Also, use each approved word only as its approved part of speech; a word approved only as a noun must not be used as a verb.

> **Non-STE:** Execute the initialization script before you start the server.
> **STE:** Run the initialization script before you start the server.

> **Non-STE:** When the error count goes down, restart the service.
> **STE:** When the error count decreases, restart the service.

**Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs**
A verb combined with one or more prepositions can form a phrasal verb whose meaning differs from the meanings of its individual parts. To prevent ambiguity, do not use approved words together to make a new phrase unless the phrasal verb is specifically approved in the dictionary. Replace the phrasal verb with a single approved verb that has the same meaning.

> **Non-STE:** The compiler puts out a warning when the type annotation is missing.
> **STE:** The compiler emits a warning when the type annotation is missing.

> **Non-STE:** The function gives off an error code when the input is not valid.
> **STE:** The function returns an error code when the input is not valid.

**Rule 9.4 — When You Select Terminology or Wording, Always Use a Consistent Style**
In procedural code documentation, use the same terminology each time the same type of step occurs — do not alternate between synonyms like "configuration file," "settings file," and "config" for the same item. Use the same verb for the same action every time — do not alternate between "compile," "build," and "make." In descriptive documentation, use words and sentences correctly and give a logical structure so the reader understands the text as a unit.

> **Non-STE:** Open the configuration file in a text editor. Change the port number in the settings file. Save the config and close it.
> **STE:** Open the configuration file in a text editor. Change the port number in the configuration file. Save the configuration file and close it.

> **Non-STE:** Compile the project with the build command. Make the binary for the target platform. Construct the library for distribution.
> **STE:** Build the project with the build command. Build the binary for the target platform. Build the library for distribution.
