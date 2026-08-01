# Level 4 — Section 3: Verb Forms and Tenses

Section 3 of STE-Code controls how you write verbs in code documentation:
API docs, README sections, commit messages, runbooks, code comments, config
files, and test names.

Seven rules, one idea: **use only the simple, approved verb forms from the
STE-Code dictionary, in the active voice.**

| Rule | Statement | Watch for |
|---|---|---|
| 3.1 | Use only the verb forms that the dictionary gives. | Gerunds, participles used as verbs, unlisted inflections |
| 3.2 | Use only these verb forms and tenses of verbs. | Present/past perfect, progressive, future perfect |
| 3.3 | Use the past participle form as an adjective. | Past participle used as a verb with "have" |
| 3.4 | Do not use auxiliary verbs to make complex verb constructions. | "have/has/had + been + past participle" passives |
| 3.5 | Use the "-ing" form only as a technical noun or modifier. | Progressive verb forms ("is parsing") |
| 3.6 | Use the active voice. | Passive "is/are + past participle (by …)" |
| 3.7 | Use an approved verb, not a noun, to describe an action. | Noun phrases instead of verbs |

## Approved verb forms

Every approved verb in the STE-Code dictionary shows four forms, in this order:

```
WRITE (v)
WRITES
WROTE,
WRITTEN
```

| Line | Form | Example | Where used |
|---|---|---|---|
| 1 | Base (infinitive, imperative) | WRITE | "Write the log." / "to write the log" |
| 2 | Third-person singular, simple present | WRITES | "The logger writes the record." |
| 3 | Simple past | WROTE | "The job wrote the record." |
| 4 | Past participle (adjective only) | WRITTEN | "the written log" |

The simple future is not a separate line: make it with "will" + base form
("will write"). If a form is not on one of those four lines, it is not approved.

### Approved verb categories

1. **Development operations** — build, compile, test, lint, format, commit, push, deploy, rollback
2. **Data operations** — read, write, serialize, deserialize, parse, encode, decode, query, insert, migrate
3. **Application operations** — handle, route, authenticate, authorize, validate, schedule, dispatch, resolve
4. **Communication operations** — send, receive, publish, subscribe, stream, poll, broadcast, connect

Plain approved verbs (use instead of wordy substitutes): `use`, `start`,
`stop`, `show`, `make`, `get`, `set`, `check`, `do`, `send`, `remove`, `keep`.

### Only these six verb forms are approved

- Infinitive: "Use this flag to parse the file."
- Imperative: "Parse the file. Write the log."
- Simple present: "The parser reads the file."
- Simple past: "The build failed."
- Simple future: "The job will start at 02:00." (will + base form)
- Past participle as adjective: "the parsed file", "the deprecated method"

Not approved (convert away from these): present perfect (has parsed), past
perfect (had parsed), present/past progressive (is parsing, was parsing),
future progressive (will be parsing), perfect progressive (has been parsing),
gerunds used as verbs (parsing, validating), and all passive or compound
auxiliary constructions.

## Rule 3.1 — Use only the verb forms that the dictionary gives

Find the verb in the STE-Code dictionary. If the verb is not there, do not use
it; use an approved verb instead: `make` (not generate), `get` (not retrieve),
`check` (not verify), `use` (not utilize), `start` (not initiate),
`stop` (not terminate), `remove` (not delete), `show` (not render), `do`
(not execute), `keep` (not maintain).

If the verb is approved, use only its four listed forms. Do not invent new
forms:
- "Parsing", "parseable", and "parser" are not verb forms of PARSE. A noun
  such as "parser" is approved only when the dictionary or a technical-noun
  category gives it.
- Use the past participle only as an adjective ("the parsed manifest",
  "the deprecated method"). Do not build a verb with "have/has/had" or "get".

Example:
- Non-STE: The linter validates the file and is reporting the errors to the terminal.
- STE: The linter validates the file. It reports the errors to the terminal.

## Rule 3.2 — Use only these verb forms and tenses of verbs

Use only the six forms above. Do not use unapproved tenses.

| Unapproved form | Fix |
|---|---|
| present perfect ("has parsed") | simple past ("parsed") |
| past perfect ("had parsed") | simple past + "Then" ("parsed. Then …") |
| progressive ("is parsing", "was parsing") | simple present/past; if together, two sentences + "at the same time" |
| future progressive ("will be parsing") | simple future ("will parse") |
| passive with auxiliary ("is being parsed") | name the actor, active voice (Rule 3.6) |

Example:
- Non-STE: The linter has found three errors in the source file.
- STE: The linter found three errors in the source file.

- Non-STE: The server was processing the request when the timeout occurred.
- STE: The server processed the request. Then the timeout occurred.

## Rule 3.3 — Use the past participle form as an adjective

Use the past participle of an approved verb as an adjective:
- before a noun: "the parsed manifest"
- after "is", "becomes", or "stays": "the cache is initialized"

This is not passive voice. It shows the **condition** of something, not an
action an actor performs. If the sentence names an actor and an action
("the file was parsed by the loader"), that is passive voice — rewrite it
active (Rule 3.6).

Approved code-domain past participles (adjectives):

| Participle | Phrase | Condition it shows |
|---|---|---|
| parsed | the parsed manifest | The parser read the file. |
| serialized | the serialized record | In a transport format. |
| deserialized | the deserialized object | In memory again. |
| initialized | the initialized cache | Ready for use. |
| deprecated | the deprecated method | Old; do not use it. |
| allowed | the allowed memory | The limit the config gives. |
| corrupted | the corrupted index | The data is not correct. |
| locked | the locked row | Another transaction holds the row. |
| written | the written log | On disk. |
| given | the given options | The caller sends them. |
| built | the built artifact | The build made it. |
| signed | the signed token | Has a valid signature. |

Cautions:
- Do not make a participle from an unapproved verb. "delete" is not approved;
  write "the removed branch" (use REMOVE).
- Do not use a participle as a verb with "have/has/had" (Rule 3.2).
- Prefer the plain word: "started" not "commenced", "used" not "utilized",
  "stopped" not "terminated".

Example:
- Non-STE: The method has been deprecated by the API team in release 4.2.
- STE: The method is deprecated in release 4.2. Do not use the deprecated method in new code.

## Rule 3.4 — Do not use auxiliary verbs to make complex constructions

Do not combine a past participle with an auxiliary verb ("have", "be", "will",
"can", "must", "should", "is to be") to build compound tenses or passive voice.
Write the action with a simple approved form instead:

- "have/has/had + past participle" (perfect) → simple past, or simple past + "Then".
- "be + past participle" (passive) → active voice with a clear agent (Rule 3.6).
- "is to be + past participle" → imperative.
- "can be + past participle" → "you can + base verb" (reader is the agent).
- "will be + past participle + by + agent" → "will + base verb" with the agent named.

Example:
- Non-STE: The report will be generated by the scheduler.
- STE: The scheduler will generate the report.

- Non-STE: The connection pool has been created before the first query is sent.
- STE: The connection pool was created. Then the first query is sent.

## Rule 3.5 — Use the "-ing" form only as a technical noun or modifier

The "-ing" form is not approved as a verb (it appears only inside the
progressive tenses, which Rule 3.2 forbids). Use it only as:

1. A technical noun in a title or heading — Logging, Monitoring, Handling,
   Packaging, Shipping, Troubleshooting, Building, Deployment.
2. A modifier inside a technical noun — logging service, monitoring agent,
   routing table, switching relay, caching layer, building pipeline,
   binding configuration, streaming endpoint, rendering engine.

Approved "-ing" words in STE-Code:
- Nouns: logging, monitoring, routing, servicing
- Adjectives: matching, missing, remaining
- Pronoun: something
- Preposition: during

Do not pull the "-ing" word out of the technical noun and use it as a verb.
"The caching layer stores the result" is approved; "The layer is caching the
result" is not.

Example:
- Non-STE: The matching algorithm is comparing the remaining items during the iteration and it is removing the missing records.
- STE: The matching algorithm compares the remaining items during the iteration. It removes the missing records.

## Rule 3.6 — Use the active voice

Always use the active voice: the subject of the sentence does the action
("A does B"). In descriptive writing, passive voice is permitted only when the
agent (who or what does the action) is genuinely unknown.

Test for passive voice: ask "by whom or by what?" after the verb. If the
sentence answers it (or could, with the same meaning), it is passive. Convert
it to active by making the agent the subject.

Four conversion methods:

- **Method 1** (agent in "by"-phrase): move the agent to the subject.
  Non-STE: The API response is parsed by the middleware.
  STE: The middleware parses the API response.
- **Method 2**: change an infinitive verb to an active verb.
  STE: The profiler calculates the memory usage from these values.
- **Method 3** (procedural writing): change the verb to the imperative.
  Non-STE: The dependencies can be installed with the following command.
  STE: Install the dependencies with this command: npm install
- **Method 4** (agent not named): use "you" (reader) or "we" (your org).
  Non-STE: The configuration file can be edited with a text editor.
  STE: You can edit the configuration file with a text editor.

Per document type:
- **README:** imperative for install/build steps (reader is agent); active
  with the library/tool as subject in feature lists.
- **API docs:** method or function is the subject. "This method validates the
  input and returns a boolean." (not "is validated … is returned").
- **Docstrings/comments:** imperative summary line; active body with the
  function as subject.
- **Commit messages:** imperative ("Fix the authentication bug.") — the commit
  is the agent. (Generated changelogs are exempt.)
- **Error/log output:** name the component that detected the error
  ("The rate limiter rejected the request."). Passive is correct only when the
  agent is truly unknown ("The connection was reset.").

Paradigm guidance: in OO, the class/method is the agent; in functional, the
function is the agent ("The map function transforms each element"); in
procedural, the script/tool is the agent; in declarative (SQL, Terraform, k8s),
the engine/controller is the agent ("This query selects all rows", "The
deployment controller maintains three replicas"); in systems docs, the
allocator/mutex/channel is the agent ("The mutex controls access to the shared
state").

Quick reference:

| Passive | Active | Method |
|---|---|---|
| is returned by | returns | 1 |
| can be used to | you can use … to | 4 |
| is configured by | configures | 1 |
| is called when | calls | 1 |
| should be installed | install (imperative) | 3 |
| will be removed in | (we) will remove … in | 4 |

When converting, also check the replacement verb against the Canonical Synonym
Table: "The downstream pipeline uses the result" (not "is used by"); "The
scheduler makes the report every night" (not "is generated by").

## Rule 3.7 — Use an approved verb, not a noun, to describe an action

If an approved verb describes the action, use the verb. Verbs describe actions
more clearly than nouns: "validate the token" tells the reader to run the
check; "validation of the token" makes them ask whether to run, log, or skip it.

If a word is not approved as a verb, do not use it as a verb — use the noun
form instead (Rule 1.5). "Cache" is an approved technical noun but not an
approved verb, so write "Do a cache of the response" rather than "Cache the
response".

Preferred plain verbs: `use`, `start`, `stop`, `show`, `make`, `get`, `set`,
`check`, `do`, `send`, `remove`, `keep`. Avoid wordy substitutes: `utilize`→
`use`, `leverage`→`use`, `commence`→`start`, `terminate`→`stop`,
`initiate`→`start`, `generate`→`make`, `employ`→`use`.

Examples:
- Non-STE: The ohmmeter gives an indication of 450 ohms.
- STE: The ohmmeter shows 450 ohms.
- Non-STE: Before the initialization of the service, make sure that the config is valid.
- STE: Before you initialize the service, make sure that the config is valid.
- Non-STE: A read of the config, then a write of the config.
- STE: Read the config, then write the config.
- Non-STE: A transmission of the event, then a reception of the event.
- STE: Send the event, then receive the event.

## Cross-references

- Rule 1.1 — approved words (dictionary + Canonical Synonym Table)
- Rule 1.5 — technical noun categories (noun-form fallback when a word is not an approved verb)
- Rule 1.12 — approved technical verbs in their simple forms
- Rule 3.1 — only the dictionary's verb forms
- Rule 3.2 — only the six approved forms and tenses
- Rule 3.3 — past participle as adjective
- Rule 3.4 — no auxiliary-verb compounds
- Rule 3.5 — "-ing" only as technical noun or modifier
- Rule 3.6 — active voice
- Rule 3.7 — approved verb, not noun
- The STE-Code dictionary (a-dictionary.md) — full list of approved verbs and their four forms
- Extensions (06-extensions.md) — approved plain verbs (use, start, stop, show, make, get, set, check, do, send, remove, keep)
- Reference catalogue (07-catalogue.md) — full verb and noun reference
