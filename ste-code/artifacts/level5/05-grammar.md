# Level 5 — Grammar (Rules 2.1–2.3, 3.1–3.7)

Level 5 is the full STE-Code standard. This sub-document is the **grammar** slice:
the rules that govern how words combine into technical nouns (Section 2) and into
sentences (Section 3). These rules are the structural backbone that the vocabulary
rules in Section 1 and the clarity rules in Sections 4–9 assume already hold.

Use this file when you generate, review, or lint code documentation with an LLM and
need to enforce sentence shape — short technical nouns, approved verb forms, active
voice, and no auxiliary-verb constructions.

## What "grammar" covers here

- **Section 2 — Technical nouns:** keep multi-word nouns short (Rule 2.1), write long
  technical nouns in full then shorten them (Rule 2.2), hyphenate related words as one
  unit (Rule 2.3).
- **Section 3 — Sentence structure:** use only the approved verb forms (Rule 3.1),
  only the approved tenses (Rule 3.2), use the past participle as an adjective (Rule 3.3),
  do not build auxiliary-verb constructions (Rule 3.4), use "-ing" forms only as technical
  nouns/modifiers (Rule 3.5), use the active voice (Rule 3.6), and prefer a verb over a
  noun when an approved verb exists (Rule 3.7).

The three-word limit for a noun phrase (Rule 2.1) interacts with hyphenation: a hyphenated
unit counts as one word, so `main-feature-flag` + `rollback-handler` + `trigger` is three
words, not five.

---

## Rule 2.1 — Keep technical nouns short

To keep multi-word technical nouns short, use prepositions (for example "of," "on," "in,"
and "for") and explain the multi-word technical nouns. A technical noun that the code domain
uses — a module name, class name, configuration key, endpoint path, error type, or test
fixture — must stay short so the reader can parse it without effort.

When a phrase names a code component with more than a few words, break the phrase into small
nouns that connect with prepositions. Do not write one long noun that stacks modifiers.

Why this matters:

- A stacked noun such as `authentication_token_expiration_refresh_interval_setting` hides
  which part owns which. A short noun with prepositions shows the tree: the setting belongs
  to the interval, the interval to the expiration, the expiration to the token.
- Short technical nouns match how code is already structured. A config key, class, or JSON
  field is one short concept; prepositions in the sentence show how those concepts relate.
- Follow the Microsoft and Google style guides: use short, plain words. Do not use `utilize`,
  `leverage`, or `employ` when `use` is enough; do not use `commence`, `initiate`, or
  `terminate` when `start` and `stop` are enough.
- Approved code-domain adjectives stay attached to the short noun they modify: `idempotent`,
  `immutable`, `thread-safe`, `atomic`, `nullable`, `deprecated`, `stateless`,
  `backward-compatible`, `asynchronous`, `concurrent`, `deterministic`. Write
  `the idempotent retry policy`, not `idempotentretrypolicy`.

How to apply:

1. Find a noun that stacks two or more modifiers (a "noun chain").
2. Split the chain at the ownership or containment points.
3. Connect the parts with `of`, `on`, `in`, or `for`.
4. If a part is itself a code component, name it with its short technical noun (its class,
   key, or file), not a merged word.
5. In instruction text, use the approved verbs: `set`, `get`, `make`, `show`, `check`,
   `remove`, `send`, `start`, `stop`, `use`, `update`. Do not use `configure` for `set`,
   `retrieve` for `get`, `delete`/`purge` for `remove`, or `display` for `show`.

Worked pairs:

| Do not write | Write |
|---|---|
| Authentication token expiration refresh interval setting | Setting of the refresh interval of the expiration of the authentication token |
| Install the forward service request validator middleware config tags. | Install the config tags on the validator middleware of the request of the forward service. |
| Remove the database migration script output directory lock files. | Remove the lock files that lock the output directory of the migration script of the database. |
| Payment gateway timeout retry exhaustion notification handler | Handler of the notification of the exhaustion of the retry of the timeout of the payment gateway |

See also: Rule 1.5 (what counts as a technical noun), Rule 1.3 (keep verbs and nouns plain),
Rule 2.2 (when a noun must stay long), Rule 2.3 (hyphenate related pairs).

---

## Rule 2.2 — Write long technical nouns in full

When a technical code noun has more than three words, write it in full. Then use one of
these methods to make the technical code noun clear:

- Give a shorter form of the technical code noun.
- Use hyphens (-) between words that you use as one unit.
- Use prepositions (for example "of," "on," "in," "for," and "to") to split a long noun into
  short, separate parts (see Rule 2.1).

A long multi-word code noun can be a long technical noun, or a combination of shorter
technical nouns. Frequently it is not possible to divide technical code nouns into smaller
parts because they are the technical nouns your company, framework, or subject field uses.
Thus, write technical code nouns in their approved form.

**Method 1 — Shorter form.** If a long technical code noun comes from an official code
document (an API specification, a schema, an OpenAPI file, an architecture diagram), write it
in full the first time it occurs. Then, if possible, explain the noun and use a shorter form
or approved abbreviation in the rest of the document.

> Initialize the user session cache invalidation lock handler (the handler that locks the
> cache of the user session; in this procedure, we call it the "invalidation lock handler").
> Run the invalidation lock handler before the shutdown hook releases the cache.

> The Main Form Validation Module (MFVM) is a TypeScript module that includes a Main Export
> Controller Unit (MECU) and a Data Bridge (DB). The Dynamic Config Unit (DECU) sends events
> to operate the MFVM.

If an approved technical code noun has three words or fewer, you do not need an abbreviation.

**Method 2 — Prepositions.** When a long technical code noun is a chain of short nouns (for
example "user authentication token refresh failure retry policy"), put the key noun first,
then attach the modifiers with "of," "on," "in," "for," or "to."

| Do not write | Write |
|---|---|
| Configure the user authentication token refresh failure retry policy before you deploy. | Configure the retry policy for the failure of the refresh of the user authentication token before you deploy. |
| Install the background worker queue overflow alert suppression rule on the staging cluster. | Install the alert suppression rule on the overflow of the background worker queue on the staging cluster. |
| Remove the database connection pool exhaustion recovery timeout configuration parameter. | Remove the configuration parameter that sets the recovery timeout for the exhaustion of the database connection pool. |

**Method 3 — Hyphenate.** When two or more words act as a single modifier before a noun, use
a hyphen to show they are one unit. Do not hyphenate when the first word is an "-ly" adverb
(for example "a publicly documented API" stays open).

| Do not write | Write |
|---|---|
| Set the request response mapping handler to the new schema. | Set the request-response mapping handler to the new schema. |
| Run the build time configuration check after you compile. | Run the build-time configuration check after you compile. |
| Add an end to end test for the payment flow. | Add an end-to-end test for the payment flow. |
| Use the out of band signal to stop the long running job. | Use the out-of-band signal to stop the long-running job. |

Note: hyphenation groups words into one unit but does not make a long technical noun short.
If the hyphenated unit still has more than three words (for example "request-response mapping
handler"), write it in full the first time, then use the shorter form ("mapping handler").

How to apply in code documentation:

1. Find the long technical code noun (more than three words).
2. Write it in full the first time it occurs; keep the exact approved form from the source.
3. Give a shorter form or approved abbreviation in parentheses right after.
4. In the rest of the document, use only the shorter form or abbreviation.
5. If the noun is a chain of short nouns, split it with prepositions (Rule 2.1).
6. If two or more words act as one modifier, hyphenate them.
7. Do not fill a procedure with abbreviations; a short clear noun beats a string of letters.

See also: Rule 2.1 (three-word limit), Rule 1.5 (technical noun categories), Rule 1.3
(use, set, get, make, show, check, remove, send, start, stop).

---

## Rule 2.3 — Use hyphens between words used as one unit

A hyphen is a punctuation mark that connects words or parts of words. Use hyphens between
words to show how related words operate as one unit. This method makes the multi-word code
nouns agree with Rule 2.1. Hyphenated words always count as one word, so a hyphenated code
noun fills only one of the three-word slots that Rule 2.1 allows for a noun phrase.

Do not connect words that are not related, because the hyphen changes the meaning of the
multi-word code noun. If you are not sure, explain the noun in the clearest way, then use a
shorter form, an approved verb such as `get`, `set`, `make`, `start`, or an official approved
abbreviation from your glossary.

If an approved technical code noun includes hyphens — for example `input-output stream`,
`thread-safe queue`, or `backward-compatible API` — do not change it. If it is too long, write
it in full the first time it occurs, then use the shorter-technical-noun method.

Do not use hyphens to make groups of more than three words. Keep the hyphen group to at most
three words; split longer chains with prepositions such as `of`, `on`, or `in`.

Approved hyphenated code examples:

| Example | Note |
|---|---|
| Make sure that the fail-safe shutdown-handler connection is safe. | 3 words: make / sure / connection |
| Inspection of the request rate-limit device. | 3 words: inspection / of / device |
| The thread-safe queue keeps the order of the write operations. | 3 words: queue / keeps / order |
| Remove the backward-compatible API client before you make the change. | 3 words |

When a hyphen joins two related words, the pair counts as one unit. Apply this in procedural
and descriptive code documentation so the reader can parse the noun without re-reading.

| Do not write | Write |
|---|---|
| Move the `main-feature-flag-rollback-handler` trigger to start the test run. | Move the `main-feature-flag` rollback-handler trigger to start the test run. |
| Remove the `data-adapter` assembly (8) from the view body. | Remove the `data adapter` assembly (8) from the view body. |
| The `input output stream` is part of the logging system. | The `input-output stream` is part of the logging system. |

Cautions:

- Do not hyphenate a three-word approved technical noun (`data adapter`, `pipeline validator`);
  adding a hyphen changes the count and confuses the reader.
- Keep a hyphen the official name already has (`input-output stream`); removing it changes
  the term.

See also: Rule 2.1 (the three-word limit hyphenated units help you meet), Rule 1.5
(hyphenated code terms such as `thread-safe queue` and `backward-compatible API`),
Rule 2.2 (pair hyphenated nouns with short approved verbs).

---

## Section 3 — Sentence structure

Section 3 governs how approved words form sentences. The dictionary gives each approved verb
with four forms; Section 3 tells you which forms and tenses you may use, how to keep the
active voice, and how to avoid auxiliary-verb constructions.

### The four approved verb-form categories

1. **Development operations** — build, compile, test, lint, format, commit, push, deploy, rollback
2. **Data operations** — read, write, serialize, deserialize, parse, encode, decode, query, insert, migrate
3. **Application operations** — handle, route, authenticate, authorize, validate, schedule, dispatch, resolve
4. **Communication operations** — send, receive, publish, subscribe, stream, poll, broadcast, connect

The plain everyday verbs also apply: `use`, `start`, `stop`, `show`, `make`, `get`, `set`,
`check`, `do`, `send`, `remove`, `keep`.

---

## Rule 3.1 — Use only the verb forms given in the dictionary

The STE-Code dictionary gives the verb forms you can use for each approved verb. Use only
those forms. Do not use other forms (gerunds, participles used as verbs with auxiliaries, or
inflected forms that are not listed).

Every approved verb appears with four forms, in this order: base form, third-person singular,
simple past, past participle. The simple future is not a separate line; make it with "will"
and the base form.

| Line in the entry | Form | Example with WRITE |
|---|---|---|
| Line 1 | Base form (infinitive and imperative) | WRITE — "Write the log." / "to write the log" |
| Line 2 | Third-person singular, simple present | WRITES — "The logger writes the record." |
| Line 3 | Simple past | WROTE — "The job wrote the record." |
| Line 4 | Past participle (as an adjective) | WRITTEN — "the written log" |

How to apply:

1. Find the verb in the STE-Code dictionary.
2. If the verb is not in the dictionary, use the approved verb instead: `make` (not
   `generate`), `get` (not `retrieve`), `check` (not `verify`), `use` (not `utilize`), `start`
   (not `initiate`), `stop` (not `terminate`), `remove` (not `delete`), `show` (not `render`),
   `do` (not `execute`), `keep` (not `maintain`).
3. If the verb is in the dictionary, use only one of the four listed forms.
4. Do not make a new form from an approved verb. "Parsing," "parseable," and "parser" are not
   verb forms of PARSE; a noun such as "parser" is approved only when the dictionary or a
   technical-noun category gives it.
5. Use the past participle only as an adjective ("the parsed manifest," "the deprecated
   method"). Do not use it with "have," "has," "had," or "get" to make a verb.

| Do not write | Write |
|---|---|
| The linter validates the file and is reporting the errors. | The linter validates the file. It reports the errors to the terminal. |
| The script has written the output to the log. | The script wrote the output to the log. Then the test starts. |
| The service utilizes a token cache and leverages the parser. | The service uses a token cache. The service parses each request. |
| The loader does the parsing and the validating. | The loader parses the manifest. Then the loader validates the schema. |
| The migration had deleted the deprecated column. | The migration removed the deprecated column. Then the migration stopped the open connections. |

See also: Rule 3.2 (approved tenses), Rule 3.3 (past participle as adjective), Rule 3.4
(avoid auxiliary verbs), Rule 3.6 (active voice), Rule 1.1 (word gates), Rule 1.5
(technical noun categories), the STE-Code dictionary (a-dictionary.md).

---

## Rule 3.2 — Use only these verb forms and tenses

Use only these verb forms and tenses of verbs:

- The infinitive form
- The imperative form (command form)
- The simple present tense
- The simple past tense
- The simple future tense
- The past participle form (as an adjective)

Do not use other forms and tenses that are not approved:

- The present perfect (have/has parsed)
- The past perfect (had parsed)
- The present/past progressive (is/was parsing)
- The future progressive (will be parsing)
- The perfect progressive (has been parsing, had been parsing)
- The gerund used as a verb with an auxiliary (is parsing, keeps parsing)

Approved verb-form table (code verbs):

| Infinitive | Imperative + object | Simple present | Simple past | Simple future | Past participle (adj) |
|---|---|---|---|---|---|
| (To) Parse | Parse + object | It parses | It parsed | It will parse | The parsed file |
| (To) Write | Write + object | It writes | It wrote | It will write | The written log |
| (To) Build | Build + object | It builds | It built | It will build | The built artifact |
| (To) Send | Send + object | It sends | It sent | It will send | The sent request |
| (To) Validate | Validate + object | It validates | It validated | It will validate | The validated token |

How to select the correct form:

1. **Infinitive** — after a modal verb or to state a purpose: "Use this flag to parse the file."
2. **Imperative** — for each step of a procedure: "Parse the file. Write the log."
3. **Simple present** — for a general fact, repeated action, or system behavior: "The parser reads the file."
4. **Simple past** — for a complete action: "The build failed."
5. **Simple future** — "will" + base form for a later action: "The job will start at 02:00."
6. **Past participle** — only as an adjective before a noun: "the parsed file," "the deprecated method."

How to correct an unapproved form:

- Present perfect ("has parsed") → simple past ("parsed").
- Past perfect ("had parsed") → simple past in two sentences with "Then".
- Progressive ("is parsing," "was parsing") → simple present or simple past; if two actions
  happen together, write two sentences and add "at the same time".
- Future progressive ("will be parsing") → simple future ("will parse").
- Passive with unapproved auxiliary ("is being parsed") → name the actor and use the active
  voice (Rule 3.6).

| Do not write | Write |
|---|---|
| The linter has found three errors. | The linter found three errors in the source file. |
| The server was processing the request when the timeout occurred. | The server processed the request. Then the timeout occurred. |
| The framework had already initialized the pool. | The framework made the connection pool. Then the query started. |
| The scheduler is deploying the build while the tests are running. | The scheduler sends the build to production. The tests run at the same time. |
| You should be setting the timeout, then you will be restarting. | Set the timeout value. Then start the service again. |

See also: Rule 3.1 (dictionary forms), Rule 3.3 (past participle as adjective), Rule 3.4
(avoid auxiliary verbs), Rule 3.5 ("-ing" only as noun/modifier), Rule 3.6 (active voice),
Rule 1.1 (word gates), the STE-Code dictionary.

---

## Rule 3.3 — Use the past participle form as an adjective

When you use the past participle form as an adjective, it shows the condition of something.
This is not passive voice. Use the past participle form of an approved verb as an adjective:

- Before a noun
- After a verb form of "to be," "to become," or "to stay"

Do not use the past participle form if it is not in the STE-Code dictionary. Approved
adjectives in the dictionary that are the past participle of verbs that are not approved
(for example "permitted," "damaged") have part of speech "(adj)" and are permitted.

How to know it is an adjective and not passive voice:

1. The word gives the **condition** of the thing, not an action an actor does.
2. You can put it directly before the noun: "the parsed file," "the deprecated method,"
   "the closed connection".
3. You can put it after "is," "becomes," or "stays": "the cache is initialized," "the endpoint
   becomes deprecated," "the record stays locked".
4. If the sentence names an actor and an action ("the file was parsed by the loader"), it is
   passive voice — write the active voice instead (Rule 3.6).

Approved code-domain past participles used as adjectives:

| Past participle (adj) | Example noun phrase | Condition it shows |
|---|---|---|
| parsed | the parsed manifest | The parser read the file. |
| serialized | the serialized record | The record is in a transport format. |
| deserialized | the deserialized object | The object is in memory again. |
| initialized | the initialized cache | The cache is ready for use. |
| deprecated | the deprecated method | The method is old. Do not use it. |
| allowed | the allowed memory | The limit the configuration gives. |
| corrupted | the corrupted index | The data is not correct. |
| locked | the locked row | Another transaction holds the row. |
| written | the written log | The log file is on disk. |
| given | the given options | The options the caller sends. |
| built | the built artifact | The build made the artifact. |
| signed | the signed token | The token has a valid signature. |

Cautions:

- Do not make a new past participle from an unapproved verb. Write "the removed branch," not
  "the deleted branch," unless "delete"/"deleted (adj)" is in the dictionary.
- Do not use a past participle as a verb with "have," "has," or "had" (Rule 3.2).
- Do not put more than one past participle before the same noun; split into two short
  sentences if the phrase becomes difficult.
- Prefer the plain word: "started" not "commenced," "used" not "utilized," "stopped" not
  "terminated".

| Do not write | Write |
|---|---|
| The method has been deprecated by the API team. | The method is deprecated in release 4.2. Do not use the deprecated method in new code. |
| The record gets locked, then the transaction is committed. | The transaction writes the locked record. Then the transaction ends. |
| The gateway validates the signed token on each request. | (already active — "signed" is the adjective before "token") |
| The build artifact stays uncompiled until the pipeline has compiled. | The artifact stays unbuilt until the pipeline builds the modified sources. |

See also: Rule 3.1 (dictionary forms), Rule 3.2 (approved tenses), Rule 3.4 (avoid auxiliary
verbs), Rule 3.5 ("-ing" as noun/modifier), Rule 3.6 (active voice), Rule 1.1 (word gates),
the STE-Code dictionary (approved adjectives with "(adj)").

---

## Rule 3.4 — Do not use auxiliary verbs to make complex verb constructions

Do not use the past participle form as a verb together with the auxiliary verb "have." Do not
use auxiliary verbs ("have," "be," "will," "can," "must," "should," "is to be") with a past
participle to build compound tenses or passive voice. These constructions make complex verb
forms that STE-Code does not approve. Write the action with a simple, approved verb form:

- Use the simple past instead of "have/has/had + past participle" (present or past perfect).
- Use the active voice with a clear agent instead of "be + past participle" (passive voice,
  Rule 3.6).
- Use the imperative (command) form for instructions instead of "is to be + past participle."
- Use "you can + base verb" instead of "can be + past participle" when the reader is the agent.
- Use "will + base verb" with a named agent instead of "will be + past participle + by + agent."

When a compound construction is unavoidable for correctness, split it into separate simple
sentences. Rule 3.2 lists the only approved verb forms.

| Do not write | Write |
|---|---|
| The build has compiled the module before the test runs. | The build compiled the module. Then the test runs. |
| The migration is to be run before you deploy. | Before you deploy the service, run the migration. |
| The cache can be cleared. | You can clear the cache. |
| The timeout must be set before the job starts. | Set the timeout before the job starts. |
| The report will be generated by the scheduler. | The scheduler will generate the report. |
| The connection pool has been created before the first query is sent. | The connection pool was created. Then the first query is sent. |
| The configuration file must be validated before the server starts. | Validate the configuration file before the server starts. |
| The user credentials are to be encrypted at rest and the key is rotated. | Encrypt the user credentials at rest. Rotate the key every month. |
| The temporary files had been deleted before the backup started. | The cleanup task deleted the temporary files. Then the backup started. |

See also: Rule 3.2 (approved tenses), Rule 3.3 (past participle as adjective), Rule 3.5
("-ing" as noun/modifier), Rule 3.6 (active voice).

---

## Rule 3.5 — Use the "-ing" form only as a technical noun or modifier

Words with an "-ing" form can be a verb, an adjective, a noun, or a long group of modifiers.
These different functions can cause ambiguity or long complex sentences. Thus, words with an
"-ing" form are usually not permitted as verbs. Use an "-ing" word only as a technical noun
(for example a section title or heading) or as a modifier inside a technical noun.

Approved "-ing" words in STE-Code:

- Nouns: logging, monitoring, routing, servicing
- Adjectives: matching, missing, remaining
- A pronoun: something
- A preposition: during

Why the progressive verb form is not approved: Rule 3.2 lists the only permitted forms and
tenses. The present progressive ("is running," "are deploying," "was processing") is not on
that list, so you must not use "-ing" to describe an action. Replace the progressive with the
simple present or simple past, and break a long continuous clause into short separate
sentences. The "-ing" form also hides auxiliary-verb constructions that Rule 3.4 forbids.

Approved "-ing" technical nouns (titles/headings): Logging, Monitoring, Testing and Fault
Isolation, Handling, Packaging, Shipping, Troubleshooting, Building, Deployment.

Approved "-ing" modifiers (inside a technical noun): logging service, monitoring agent,
routing table, switching relay, caching layer, building pipeline, binding configuration,
streaming endpoint, rendering engine.

Do not pull the "-ing" word out of the technical noun and use it as a verb: "The caching layer
stores the result" is approved; "The layer is caching the result" is not.

| Do not write | Write |
|---|---|
| When you are running this script, obey the safety checks. | When you run this script, obey all the safety checks. |
| The background worker is processing the queue and writing results. | The background worker processes the queue. It writes the results to the cache. |
| Developers committing code without running tests risk breaking the build. | Before you commit code, run the test suite. Make sure the tests pass. |
| The matching algorithm is comparing the remaining items. | The matching algorithm compares the remaining items during the iteration. |
| Something going wrong during the migration can corrupt the database. | If something goes wrong during the migration, the database can stay in a broken state. |

See also: Rule 3.2 (present progressive not approved), Rule 3.4 (auxiliary-verb constructions
forbidden), Rule 1.5 (technical-noun categories that the "-ing" modifier/noun uses depend on).

---

## Rule 3.6 — Use the active voice

Use the active voice in all code documentation. In descriptive writing, the passive voice is
permitted only when the agent (the person, service, or component that does the action) is
unknown.

In the active voice, the subject does the action ("A does B"). In the passive voice, the
subject receives the action ("B is done by A"). To test for passive voice, ask "by whom or by
what?" If the sentence answers, it is passive — convert it to active by using the agent as the
subject.

Four methods to convert passive to active:

- **Method 1** — When "by" identifies the agent, move the agent to the subject position.
- **Method 2** — Change an infinitive verb to an active verb.
- **Method 3** — In procedural writing, change the verb to the imperative (command) form.
- **Method 4** — When the agent is not given, use "you" (reader) or "we" (your organization)
  as the subject.

| Do not write (passive) | Write (active) |
|---|---|
| The API response is parsed by the middleware. | The middleware parses the API response. |
| The database connection is established by the connection pool. | The connection pool establishes the database connection at startup. |
| The dependencies can be installed with this command. | Install the dependencies with this command: npm install |
| The configuration file can be edited with a text editor. | You can edit the configuration file with a text editor. |
| The package can be installed with pip install. | Install the package with this command: pip install . |
| Support for WebSocket connections is provided by this library. | This library supports WebSocket connections. |
| The input string is validated and a boolean is returned by this method. | This method validates the input string and returns a boolean. |
| The authentication bug was fixed. | Fix the authentication bug. |

When the agent is unknown and you cannot identify it, passive is correct:

> Passive (correct): During the network request, the payload was corrupted before the checksum
> was computed. The agent is unknown because the failure occurs only under heavy load.

> Active (incorrect): During the network request, the socket corrupted the payload. — "socket"
> is not the true cause; the active sentence misleads the reader about where to fix the bug.

Use the active voice in each documentation type:

- **README** — procedural sections use the imperative with "you" as the implied agent;
  descriptive sections use the project/library/tool as the subject.
- **API docs** — use the method/function as the subject; for callbacks, use the callback as the
  subject; for return values, use the function as the subject ("This function returns a
  `Promise<User>`", not "A `Promise<User>` is returned").
- **Docstrings/comments** — the summary line uses the imperative; the body uses the function as
  the subject.
- **Commit messages** — imperative mood, inherently active ("Fix the authentication bug", not
  "The authentication bug was fixed").

See also: Rule 3.1 (dictionary forms), Rule 3.2 (approved tenses), Rule 3.3 (past participle as
adjective), Rule 3.4 (avoid auxiliary verbs), Rule 3.5 ("-ing" as noun/modifier).

---

## Rule 3.7 — Use an approved verb to describe an action, not a noun

If there is an approved verb that describes an action, use the approved verb. Verbs describe
actions more clearly than nouns or other parts of speech. The four approved technical-code-verb
categories give you the verbs you can use (see the Section 3 table). If a word is not approved
as a verb in the dictionary, do not use it as a verb — use a different sentence construction
(usually the noun form of the word).

Why verbs, not nouns: a noun names a thing; a verb names the work. "validate the token" tells
the reader to run the check; "validation of the token" makes the reader ask whether to run it,
log it, or skip it. Prefer the plain approved verb — `use`, `start`, `stop`, `show`, `make`,
`get`, `set`, `check`, `do`, `send`, `remove`, `keep` — over wordy substitutes such as
*utilize*, *leverage*, *employ*, *commence*, *terminate*, or *initiate*.

| Do not write | Write |
|---|---|
| The ohmmeter gives an indication of 450 ohms. | The ohmmeter shows 450 ohms. |
| Before the removal of the unit, make sure the power is OFF. | Before you remove the unit, make sure the power is OFF. |
| The profiler gives an indication of 200ms latency. | The profiler shows 200ms latency. |
| Before the initialization of the service, check the config. | Before you initialize the service, check the config. |
| Cache the response. | Do a cache of the response. (cache is a technical noun, not an approved verb) |
| The function gives a result of 500 OK. | The function returns 500 OK. |
| The parser does a verification of the payload. | You validate the payload before you store it. |
| A read of the config, then a write of the config. | Read the config, then write the config. |
| A transmission of the event, then a reception. | Send the event, then receive the event. |

See also: Rule 3.2 (approved verb forms and tenses), Rule 1.5 (noun-form fallback when a word
is not an approved verb), the extension approved verbs — use, start, stop, show, make, get, set,
check, do, send, remove, keep.

