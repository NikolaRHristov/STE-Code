### Section 1 — Words

**Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs**
Every word must pass one of three gates: it is an approved word in the STE-Code controlled terminology, it is a code-domain technical noun (one of 19 categories), or it is a code-domain technical verb (one of 4 categories). The controlled terminology lists frequently used words and their unapproved alternatives. Words like "utilize," "execute," and "configure" are not approved and must be replaced.

> **Non-STE:** Utilize the build tool to generate the artifact. Execute the binary to bootstrap the service. Utilize environment variables to configure runtime behavior.
> **STE:** Use the build tool to make the binary. Run the binary to start the service. Use environment variables to set the runtime behavior.

> **Non-STE:** Perform validation on the input data to ensure it conforms to the expected schema. Returns a boolean indicating whether the data is valid.
> **STE:** Check the input data against the schema. Gives `true` when the data is correct and `false` when the data is not correct.

**Rule 1.2 — Use Approved Words Only as the Specified Part of Speech**
Each approved word in the controlled terminology carries a grammatical label (noun, verb, adjective, etc.) and must be used only in that role. A word like "query" is an approved noun — "Send a query" is correct, but "Query the database" is a violation because "query" cannot be used as a verb. When an unapproved word has an approved alternative with a different part of speech, the entire sentence must be restructured.

> **Non-STE:** Query the database for user records.
> **STE:** Send a query to the database for user records.

> **Non-STE:** Static the variable to prevent modification.
> **STE:** Make the variable static to prevent modification.

**Rule 1.3 — Use Approved Words Only with Their Approved Meanings**
Each approved word in the controlled terminology carries exactly one approved meaning. Using an approved word in a general-English sense that differs from its approved meaning creates ambiguity. For example, "run" is approved only as "execute a program" — not "operate"; "return" is approved only as "send a value back from a function" — not "go back" or "happen again."

> **Non-STE:** The function runs a validation check, returns the result, and raises the retry limit if the check fails.
> **STE:** The function does a check, gives the result, and increases the retry limit if the check does not complete.

> **Non-STE:** The connection failed: the server refused to make the handshake. Call the admin if the error returns.
> **STE:** The connection did not complete: the server refused the handshake. Tell the administrator if the error occurs again.

**Rule 1.4 — Use Only the Approved Forms of Verbs and Adjectives**
Every approved verb must appear only in its four listed forms (infinitive/imperative, simple present, simple past, past participle). The "-ing" form is never an approved main-verb form. Adjective comparatives and superlatives must use either the approved "-er"/"-est" suffix forms or the "more"/"most" construction. The imperative mood replaces "-ing" in commit messages and procedural writing.

> **Non-STE:** After installing the dependencies, you can start compiling the project by running the build script. The compiler will be generating the output in the dist directory.
> **STE:** After you install the dependencies, compile the project with the build script. The compiler makes the output in the dist directory.

> **Non-STE:** feat: adding user authentication middleware and updated the login endpoint
> **STE:** feat: add user authentication middleware and update the login endpoint

**Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category**
A code-domain technical noun is a noun that names a specific software concept and fits one of 19 recognized categories (code components, data structures, infrastructure, algorithms, interface elements, defects, database terms, network protocols, etc.). Every non-dictionary word must belong to at least one category. Vague placeholder words like "stuff" and "thing" fit no category and are not permitted.

> **Non-STE:** The dev spun up the thing on the cloud and it barfed because the DB connector was busted.
> **STE:** The developer deployed the application to AWS. The deployment failed because the PostgreSQL connection pool had a timeout defect.

> **Non-STE:** The endpoint expects the payload to have a user object with a nested array of things.
> **STE:** The `POST /users` endpoint expects a JSON body with a `user` object that contains an array of `permission` objects.

**Rule 1.6 — Use a Word That Is Not Approved in the Dictionary, Only When It Is a Technical Noun or Part of a Technical Noun**
An unapproved word may be used only when it is a recognized code-domain technical noun or part of a recognized compound technical noun. For example, "handler" is unapproved (alternative: "function"), but it is permitted within the compound "event handler." When the same word stands alone as general prose, it must be replaced with its approved alternative.

> **Non-STE:** The handler processes each incoming event and the base configuration is loaded first from the config file.
> **STE:** The function processes each incoming event and the primary configuration is loaded first from the config file.

> **Non-STE:** POST /api/backup — Backups the main database nightly. Handlers errors and returns a backup ID for reference.
> **STE:** POST /api/backup — Makes an auxiliary copy of the primary database each night. Processes errors and returns a backup ID for reference.

**Rule 1.7 — Do Not Use Words That Are Technical Nouns as Verbs**
A word that belongs to a code-domain technical noun category must remain a noun. Words like "database," "cache," "Docker," and "interface" are technical nouns — they must stay as nouns with an approved verb carrying the action. The standard repair pattern uses an approved verb (store, put, add, make) with the technical noun inside a prepositional phrase.

> **Non-STE:** Database the user records before the migration.
> **STE:** Store the user records in the database before the migration.

> **Non-STE:** Interface the payment module with the order system.
> **STE:** Add an interface between the payment module and the order system.

**Rule 1.8 — Use Technical Nouns That Are Approved in Your Company, Industry, or Subject Field**
Use the approved, standard code-domain technical noun for every class, module, function, endpoint, or component you reference — the name from the source code, API spec, or project glossary. Do not invent descriptive phrases or synonyms. Readers must be able to map every documentation reference to the actual codebase element by its canonical name.

> **Non-STE:** The data display widget shows user information in a table format.
> **STE:** The `UserTable` component shows user information.

> **Non-STE:** Refactor the auth helper to use the new token validator.
> **STE:** Refactor `AuthService` to use `JwtValidator`.

**Rule 1.9 — When You Must Select a Technical Noun, Use One Which Is Short and Easy to Understand**
Select code-domain technical nouns that are short (not more than three words) and unambiguous in context. Rely on context — code references, diagrams, API specs, and preceding definitions — to carry the identifying detail. When context alone is not enough, add one or two adjectives for disambiguation, but never stack modifiers into a long descriptive phrase.

> **Non-STE:** This is a high-performance, event-driven, non-blocking I/O model JavaScript runtime environment built on Chrome's V8 JavaScript engine that uses an asynchronous, single-threaded event loop architecture for building scalable network applications.
> **STE:** Node.js is a JavaScript runtime. It uses an event-driven, non-blocking I/O model. Use it to build scalable network applications.

> **Non-STE:** The operation to establish a connection to the primary relational database management system server instance located at the network address 192.168.1.100 on the default Transmission Control Protocol port number 5432 has failed due to a network timeout condition after waiting for the configured connection timeout duration of 30 seconds.
> **STE:** Connection to the primary database at 192.168.1.100:5432 timed out after 30 seconds.

**Rule 1.10 — Do Not Use Regional, Slang, or Jargon Words as Technical Nouns**
Do not use regional, slang, or jargon words as code-domain technical nouns. Words that only a small community or specific programming language ecosystem understands cause confusion for developers from different backgrounds, junior developers, and non-native English speakers. Use well-known, approved words that are clear to a global audience.

> **Non-STE:** Remove all the cruft from the legacy module.
> **STE:** Remove all the unnecessary code from the legacy module.

> **Non-STE:** Take time to grok the authentication module before making changes.
> **STE:** Take time to understand the authentication module before making changes.

**Rule 1.11 — Do Not Use Different Technical Nouns for the Same Item**
When you select a code-domain technical noun for a class, endpoint, module, or parameter, use that same noun consistently throughout the entire document. Using multiple names for the same item forces the reader to decide whether each name refers to the same item or to different items. Use the canonical name from the most authoritative source — source code, API spec, or project glossary.

> **Non-STE:** Initialize the UserService class. Call the authenticate method on the AccountManager. The UserHandler returns a session token.
> **STE:** Initialize the UserService class. Call the authenticate method on the UserService. The UserService returns a session token.

> **Non-STE:** Send a request to the /api/login path. The authentication route returns a JSON Web Token. Include the token from the login endpoint in subsequent requests.
> **STE:** Send a request to the /api/login endpoint. The /api/login endpoint returns a JSON Web Token. Include the token from the /api/login endpoint in subsequent requests.

**Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category**
A code-domain technical verb names a precise software operation (transpile, refactor, deploy, serialize, authenticate) that has no single approved-verb equivalent. You may use such verbs if they fit one of four categories, but you must first verify that no approved verb works in its place. Do not use a technical noun as a technical verb — for example, do not use "Docker" as a verb.

> **Non-STE:** The static analyzer detects null pointer dereferences in the source code.
> **STE:** The static analyzer finds null pointer dereferences in the source code.

> **Non-STE:** Docker the application and then ship the image to the registry.
> **STE:** Put the application in a Docker container and then push the image to the registry.

**Rule 1.13 — Do Not Use Technical Verbs as Nouns**
Technical verbs must be used only as verbs, never as nouns in instructional or descriptive prose. Words like build, parse, deploy, filter, and compile must carry the action directly. Commit messages, README instructions, and docstrings all benefit from the verb-first rule: "Build the project" is correct, but "Do a build of the project" nominalizes the verb and weakens the sentence.

> **Non-STE:** Do a build of the project before you do a deploy to production.
> **STE:** Build the project before you deploy to production.

> **Non-STE:** This function does a parse of the input string and does a validate of the tokens.
> **STE:** This function parses the input string and validates the tokens.

**Rule 1.14 — Use American English Spelling Unless Other Official Directives Tell You Differently**
Use American English spelling as the default in all code documentation — README files, API docs, docstrings, inline comments, and commit messages. Use British English spelling only when project specifications or official directives require it. When quoted text (such as terminal output or error messages) contains British English spelling, you must not change the quoted text.

> **Non-STE:** The log file shows the colour of each output line.
> **STE:** The log file shows the color of each output line.

> **Non-STE:** Initialise the variable before you use it in the loop.
> **STE:** Initialize the variable before you use it in the loop.

### Section 2 — Noun Phrases

**Rule 2.1 — Multi-word Nouns (Maximum Three Words)**
Multi-word nouns — chains of nouns and adjectives that function as a single part of speech — must not exceed three words. Long chains bury the head noun under many modifiers, creating ambiguity. Break multi-word nouns longer than three words into smaller units connected by prepositions such as "of," "for," "in," and "on."

> **Non-STE:** The project implements a distributed event sourcing aggregate root snapshot storage strategy.
> **STE:** The project implements a strategy for storage of snapshots of the aggregate roots in a distributed event sourcing system.

> **Non-STE:** ERROR: Authentication token validation failure recovery procedure initialization failed.
> **STE:** ERROR: Initialization of the procedure for recovery from failure of the validation of the authentication token failed.

**Rule 2.2 — Long Technical Nouns (Shorter Forms and Hyphens)**
When a technical noun has more than three words, use one of two methods: write it in full the first time then use a shorter form, or use hyphens to join related words so the hyphenated group counts as one word. Do not abbreviate technical nouns of three words or fewer. Do not create hyphenated groups of more than three words.

> **Non-STE:** Before you run this script, configure the HTTP request pipeline middleware authentication handler. The HTTP request pipeline middleware authentication handler must be configured with the correct credentials.
> **STE:** Before you run this script, configure the HTTP request pipeline middleware authentication handler (the component that checks requests in the middleware pipeline, referred to in this document as the "authentication handler"). The authentication handler must be configured with the correct credentials.

> **Non-STE:** Move the data-access-layer-query-builder handle. Set the main-menu-configuration-file path.
> **STE:** Move the data-access-layer query-builder handle. Set the main-menu configuration-file path.

### Section 3 — Verbs

**Rule 3.1 — Use Only the Verb Forms That Are Given in the Dictionary**
Every approved verb in the controlled terminology has exactly four listed forms: the base form (infinitive/imperative), the third-person singular present, the simple past, and the past participle. You must use only these listed forms. Never invent a form by adding a regular suffix to an irregular verb — "builded" is not permitted because the dictionary lists only BUILT as the past tense and past participle of BUILD.

> **Non-STE:** The compiler has builded the project with the new configuration. The builded binary is in the output directory.
> **STE:** The compiler built the project with the new configuration. The built binary is in the output directory.

> **Non-STE:** The function writed the output to the log file and gived a status code.
> **STE:** The function wrote the output to the log file and gave a status code.

**Rule 3.2 — Use Only These Verb Forms and Tenses of Verbs**
Only six verb forms and tenses are approved: the infinitive, the imperative, the simple present, the simple past, the simple future, and the past participle used only as an adjective. Compound tenses — present perfect (has deployed), past perfect (had committed), present progressive (is building), past progressive (was running), and future perfect (will have migrated) — are prohibited and must be rewritten using simple tenses.

> **Non-STE:** The CI pipeline has completed the build and is deploying the artifacts to staging.
> **STE:** The CI pipeline completed the build. It deploys the artifacts to staging.

> **Non-STE:** The parser was reading the input file when the error occurred, and it had already consumed the first 200 tokens.
> **STE:** The parser read the input file. Then the error occurred. The parser consumed the first 200 tokens before the error.

**Rule 3.3 — Use the Past Participle Form as an Adjective**
The past participle form of an approved verb may be used only as an adjective that describes a condition, not as part of a compound verb with "have." It may appear before a noun ("the compiled binary," "the encrypted payload") or after "to be," "to become," or "to stay" ("When the binary is compiled"). This construction shows a state without naming an agent.

> **Non-STE:** When you have compiled the binary and have encrypted the payload, run the deployment script that has validated the configuration.
> **STE:** When the binary is compiled and the payload is encrypted, run the deployment script that validated the configuration.

> **Non-STE:** /** This method has parsed the input, has filtered invalid entries, and has returned the validated result. */
> **STE:** /** This method parses the input, filters invalid entries, and gives the validated result. */

**Rule 3.4 — Do Not Use Auxiliary Verbs to Make Complex Verb Constructions**
Auxiliary verbs — especially "have," "has," and "had" — must not combine with past participles to create compound tenses. The present perfect ("has deployed"), past perfect ("had committed"), and future perfect ("will have started") are not approved. Replace every compound tense with the simple present, simple past, or imperative. The auxiliary "have" as a main verb ("the function has three parameters") is permitted.

> **Non-STE:** After the pipeline has deployed the application, the monitoring service will have started the health checks.
> **STE:** After the pipeline deploys the application, the monitoring service starts the health checks.

> **Non-STE:** The test runner has executed all the unit tests and has written the coverage report.
> **STE:** The test runner executed all the unit tests. Then it wrote the coverage report.

**Rule 3.5 — Use the "-ing" Form of a Verb Only as a Technical Noun or as a Modifier in a Technical Noun**
The "-ing" form is permitted in exactly two code-domain contexts: as a technical noun in section titles or process names ("Building," "Testing," "Deploying," "Logging") and as a modifier in a technical noun phrase ("testing framework," "routing module," "logging service"). The "-ing" form must never appear as part of a compound verb tense; replace it with the simple present, simple past, or imperative.

> **Non-STE:** When you are running the build command, check the terminal for error messages while the compiler is processing the source files.
> **STE:** When you run the build command, check the terminal for error messages. The compiler processes the source files.

> **Non-STE:** The script is processing all input files while logging results to the console and writing the summary to a report file.
> **STE:** The script processes all input files. It writes the results to the console. Then it writes the summary to a report file.

**Rule 3.6 — Use the Active Voice**
Use the active voice as the default in all code documentation. In the active voice, the subject performs the action, so the reader immediately knows which component, function, service, or person does what. The passive voice is permitted only when the agent is genuinely unknown. Four methods convert passive to active: move the "by" agent to subject position, change an infinitive to an active verb, use the imperative in procedural writing, and insert "you" or "we" when the agent is the reader.

> **Non-STE:** The API response is parsed by the middleware layer before it is forwarded to the client handler.
> **STE:** The middleware layer parses the API response before it sends the response to the client handler.

> **Non-STE:** The dependencies are installed by running the command `npm install` from the project root directory.
> **STE:** Install the dependencies: run `npm install` from the project root directory.

**Rule 3.7 — Use an Approved Verb to Describe an Action, Not a Noun or Other Parts of Speech**
Every action must be carried by an approved verb rather than a noun or another part of speech. Nominalized constructions such as "performs the initialization of" or "gives an indication of" must be replaced with the direct approved verb ("initializes," "shows"). When a code-domain technical noun has no approved verb form, pair it with an approved support verb such as "do" or "run."

> **Non-STE:** The linter gives an indication of three errors in the source file.
> **STE:** The linter shows three errors in the source file.

> **Non-STE:** The `validateInput` function performs validation of the user input and gives an indication of success or failure.
> **STE:** The `validateInput` function validates the user input and shows success or failure.
