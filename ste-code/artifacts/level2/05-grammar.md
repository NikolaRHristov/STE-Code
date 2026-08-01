# Level 2 — Section-Specific Grammar Rules

Grammar rules of STE-Code, grouped by the section of the standard that owns
them. Each rule is stated as a directive, then shown with a minimal
code-domain pair. Use this file as the grammar layer on top of the Level 2
dictionary and approved-word tables.

Scope: code documentation only — README files, API reference, docstrings,
inline comments, commit messages, error messages, changelogs, configuration
comments. Source code inside code blocks is never subject to these rules.

Reading key:
- **Non-STE** — text that breaks the rule.
- **STE** — the compliant rewrite.
- Word counts, where given, follow the counting rules in Section 8.

Rule map:

| Section | Topic | Rules |
|---|---|---|
| 2 | Technical noun structure | 2.1–2.3 |
| 3 | Verbs, tense, and voice | 3.1–3.7 |
| 4 | Sentence structure | 4.1–4.5 |
| 5 | Procedural writing | 5.1–5.5 |
| 6 | Descriptive writing | 6.1–6.6 |
| 7 | Safety instructions | 7.1–7.3 |
| 8 | Punctuation and word count | 8.1–8.7 |
| 9 | Word choice and consistency | 9.1–9.4 |

## Section 2 — Technical noun structure

### Rule 2.1 — Keep technical nouns short
Use a maximum of three words in a technical noun. Use prepositions ("of," "on,"
"in," "for," "to") to split longer noun phrases and show which part owns which.

> **Non-STE:** the authentication token expiration refresh interval setting
>
> **STE:** the refresh interval for the expiration of the authentication token

Keep approved adjectives attached to the short noun that they modify:
`idempotent`, `immutable`, `thread-safe`, `atomic`, `nullable`, `deprecated`,
`stateless`, `backward-compatible`, `asynchronous`, `concurrent`,
`deterministic`.

### Rule 2.2 — Write long technical nouns in full
When a technical noun has more than three words, write it in full the first time
that it occurs. Then make it clear with one of these methods:

- Give a shorter form and use that shorter form in the remaining text.
- Use hyphens between the words that operate as one unit (Rule 2.3).
- Use prepositions to split the noun into short parts (Rule 2.1).

> **STE:** Before you start this procedure, initialize the user session cache
> invalidation lock handler (in this procedure, the "invalidation lock handler").

Do not divide a technical noun that your framework, schema, or API
specification defines. Write it in its approved form.

### Rule 2.3 — Use hyphens between words used as one unit
Use a hyphen to show that related words operate as one unit. A hyphenated group
counts as one word (Rule 8.7), so it fills only one of the three slots that
Rule 2.1 allows.

> **Non-STE:** Move the main-feature-flag-rollback-handler trigger.
>
> **STE:** Move the main-feature-flag rollback-handler trigger.

- Do not hyphenate words that are not related. The hyphen changes the meaning.
- Do not make hyphen groups of more than three words. Split longer chains with
  `of`, `on`, or `in`.
- Do not change an approved hyphenated term, for example `input-output stream`,
  `thread-safe queue`, or `backward-compatible API`.

## Section 3 — Verbs, tense, and voice

### Rule 3.1 — Use only the verb forms in the dictionary
Each approved verb appears with its allowed forms: base, third-person singular,
simple past, and past participle. Use only those forms.

```
VALIDATE (v)   VALIDATES   VALIDATED,   VALIDATED
WRITE (v)      WRITES      WROTE,       WRITTEN
```

Do not use gerunds as verbs, participles with auxiliaries, or inflected forms
that the dictionary does not list.

### Rule 3.2 — Use only the approved forms and tenses
Approved forms and tenses:

- The infinitive form
- The imperative (command) form
- The simple present tense
- The simple past tense
- The simple future tense
- The past participle form, as an adjective only.

| Form | Regular verb (parse) | Irregular verb (write) |
|---|---|---|
| Infinitive | (to) parse | (to) write |
| Imperative | Parse the payload. | Write the log entry. |
| Simple present | It parses | It writes |
| Simple past | It parsed | It wrote |
| Simple future | It will parse | It will write |
| Past participle (adj) | the parsed file | the written log |

### Rule 3.3 — Use the past participle as an adjective
The past participle shows the condition of something. This is not passive voice.
Use it before a noun, or after "to be," "to become," or "to stay."

> **STE:** The parsed file stays in the cache. The endpoint becomes deprecated.

Tests that the word is an adjective and not passive voice:

1. The word gives a condition, not an action that an actor does.
2. You can put it directly before the noun: "the closed connection".
3. You can put it after "is", "becomes", or "stays": "the cache is initialized".
4. If the sentence names an actor and an action ("the file was parsed by the
   loader"), it is passive voice. Write the active voice instead (Rule 3.6).

Do not use a past participle that the dictionary does not approve.

### Rule 3.4 — Do not use auxiliary verbs for complex constructions
Do not put "have," "be," "will be," "can be," "must be," "should be," or
"is to be" with a past participle to make compound tenses or passive voice.

- Use the simple past instead of the present perfect or past perfect.
- Use the active voice with a named agent instead of "be + past participle."
- Use the imperative form instead of "is to be + past participle."
- Use "you can + base verb" instead of "can be + past participle."

> **Non-STE:** The loader has parsed the manifest.
>
> **STE:** The loader parsed the manifest.

If a compound construction seems necessary, split the sentence into two short
sentences with approved forms.

### Rule 3.5 — Use the "-ing" form only as a noun or a modifier
Use a word that has an "-ing" form only as a technical noun (for example, in a
heading) or as a modifier inside a technical noun. Do not use it as a verb.

Approved "-ing" words in STE-Code:

- Nouns: logging, monitoring, routing, servicing
- Adjectives: matching, missing, remaining
- A pronoun: something
- A preposition: during.

> **Non-STE:** The service is starting and then it is logging the request.
>
> **STE:** The service starts. Then it logs the request.

The present progressive is not an approved tense (Rule 3.2), and the "-ing"
form hides the auxiliary constructions that Rule 3.4 forbids.

### Rule 3.6 — Use the active voice
Use the active voice in all code documentation. In descriptive writing, the
passive voice is permitted only when the agent is unknown.

Test: ask "by whom or by what?" If the sentence answers that question, it is
passive. Move the agent into the subject position.

> **Non-STE:** The API response is parsed by the middleware.
>
> **STE:** The middleware parses the API response.

### Rule 3.7 — Use an approved verb for an action, not a noun
If an approved verb describes the action, use the verb. A noun names a thing; a
verb names the work.

> **Non-STE:** The endpoint performs validation of the token.
>
> **STE:** The endpoint validates the token.

The four Technical Code Verb categories:

| Category | Verbs |
|---|---|
| Development operations | build, compile, test, lint, format, commit, push, deploy, rollback |
| Data operations | read, write, serialize, deserialize, parse, encode, decode, query, insert, migrate |
| Application operations | handle, route, authenticate, authorize, validate, schedule, dispatch, resolve |
| Communication actions | send, receive, publish, subscribe, stream, poll, broadcast, connect |

Prefer the plain approved verb — `use`, `start`, `stop`, `show`, `make`, `get`,
`set`, `check`, `do`, `send`, `remove`, `keep` — over *utilize*, *leverage*,
*employ*, *commence*, *terminate*, or *initiate*.

## Section 4 — Sentence structure

### Rule 4.1 — One topic per sentence, no abstract text
In descriptive text (a class, module, or type description), give each sentence
one topic and do not use the imperative form. In procedural text (a function or
method description), give one instruction per sentence in the imperative form.
Do not write abstract text.

> **Non-STE:** The `HttpClient` class has two internal buffers connected
> together and linked with callbacks between the request handler and the
> response dispatcher.
>
> **STE:** The `HttpClient` class has two internal buffers. Callbacks connect
> the internal buffers. These callbacks link the request handler to the
> response dispatcher.

### Rule 4.2 — Do not omit words or use contractions
Each sentence must have all its parts.

- Do not omit the noun. The reader will not know which code element you mean.
- Do not omit the verb. The reader will not know the action.
- Do not omit the subject. The reader will not know which function, class, or
  module does the action.
- Do not omit articles ("the," "a," "an").
- Do not use contractions. Write "do not," "is not," and "are not."

> **Non-STE:** Can't be longer than 64 bytes.
>
> **STE:** The key can have a maximum length of 64 bytes.

### Rule 4.3 — Use a vertical list for complex text
When a sentence must include many items (parameters, return fields, error
codes, configuration options, environment variables, dependencies, or test
cases) or many actions, use a vertical list.

When you make a vertical list:

- Put a colon (:) at the end of the introductory sentence.
- Identify each item with a number, letter, dash, or bullet.
- Start each item with an uppercase letter.
- Where applicable, use an article before the noun that is the subject of the
  item.
- Put a period at the end of an item that is a full sentence.
- Do not put a period at the end of an item that is not a full sentence.

### Rule 4.4 — Use connecting words and connecting phrases
Connecting words and phrases link the topic of one sentence to the idea in the
sentence that follows.

- Approved connecting words: "and," "but," "then," "thus."
- Approved connecting phrases: "as a result," "at the same time."
- Demonstrative adjectives ("this," "these") also connect related sentences.

> **STE:** The middleware validates the token. Thus the controller receives
> only authenticated requests.

### Rule 4.5 — Use an article or a demonstrative adjective before a noun
Articles and demonstrative adjectives show the position of nouns in the
sentence. Do not remove them to make the text shorter.

- Do not use an article in a general statement or before an abstract concept
  ("performance," "scalability," "error handling," "concurrency," "backward
  compatibility").
- In short sentences, use an article before each noun.
- In a long series of items, use the article only before the first noun. If an
  adjective applies to the first item only, repeat the article.
- Do not use a definite article before a code identifier. A function name, a
  class name, a variable name, a file name, an environment variable, an error
  code, and a version tag are proper nouns.
- Always keep the noun after "this" or "these". Do not write "this" alone.

> **Non-STE:** Call the `parseConfig`. This returns a map.
>
> **STE:** Call `parseConfig`. This function returns a map.

## Section 5 — Procedural writing

### Rule 5.1 — Maximum of 20 words in a procedural sentence
Procedures include installation instructions, setup steps, deployment
checklists, debugging workflows, and API usage guides. Use a maximum of 20
words in each procedural sentence. Warnings and cautions obey the same limit.
A note has a maximum of 25 words in each sentence.

> **Non-STE:** Run the database migration script from the project root
> directory and then restart the application server to apply all pending schema
> changes to the production environment. (27 words)
>
> **STE:** Run the database migration script from the project root directory.
> Then restart the application server. (15 words)

Code snippets, command examples, and terminal output inside code blocks are not
subject to the word count.

### Rule 5.2 — One instruction per sentence
Write only one instruction in each sentence. Use numbered or bulleted lists to
show the sequence. A procedure can have any number of work steps.

You can write two instructions in one sentence with "and" only when both actions
occur at the same time. You can write more than one sentence in a work step
when:

- Two or more actions occur at the same time and you cannot separate them
- A result or measurement occurs immediately after the action.

### Rule 5.3 — Use the imperative (command) form for instructions
Start each procedural instruction with an imperative verb: "run," "set," "open,"
"save," "install," "configure," "restart," "copy," "delete," "create," "add,"
"enter," "select," "check."

> **Non-STE:** The configuration file should be edited before deployment.
>
> **STE:** Edit the configuration file before you deploy.

Do not use passive voice, gerunds, or modal verbs ("can," "could," "should,"
"may," "might") for instructions. Use "must" only for security warnings, data
loss cautions, and critical conditions.

In a README file, the imperative form applies to the procedural sections only
(installation, configuration, build, quick start). Descriptive sections can use
declarative sentences.

### Rule 5.4 — Put the descriptive statement before the command
When the reader must know a condition first, write the condition as a
descriptive statement, then a comma, then the instruction.

> **Non-STE:** Stop the service if the health check reports a failure.
>
> **STE:** If the health check reports a failure, stop the service.

The comma is the marker that makes the reader evaluate the condition before the
action. Do not bury the condition after the command.

### Rule 5.5 — Notes give information only
A note gives supplementary information. A note must not give an instruction, a
command, a requirement, a limit, or an expected result. Put that information in
the work step. A note must not contain an imperative verb.

> **STE:** NOTE: The API rate limiter permits a maximum of 1000 requests each
> minute for each client IP address on the free tier.

If the information prevents data loss, a security issue, or system damage, write
it as a WARNING or CAUTION instead (Section 7). To test a procedure, read it
without the notes. If the reader cannot complete it, move the missing
information into the work steps.

## Section 6 — Descriptive writing

### Rule 6.1 — Give information gradually
Give the reader one piece of information at a time. Each sentence has one
subject. Do not combine multiple actions, conditions, or subjects.

> **Non-STE:** The authentication middleware validates bearer tokens from the
> authorization header by calling the `validateToken` function which decodes
> the JWT payload and checks the `exp` claim before attaching the claims to the
> request and logging any failure to the audit trail.
>
> **STE:** The authentication middleware validates each incoming request. The
> middleware reads the bearer token from the `Authorization` header. It sends
> the token to the `validateToken` function. The function decodes the JWT
> payload. Then it compares the `exp` claim with the current server time.

### Rule 6.2 — Use key words and key phrases for logical structure
Key words are terms that occur again in a documentation block to link concepts.
Key phrases have the same function. Do not change a key word after you select
it (see also Rule 9.4).

Connecting words and phrases approved in STE-Code: `and`, `but`, `then`, `thus`,
`also`, `however`, `therefore`, `for example`, `as a result`, `at the same
time`. Put them at the start of the sentence.

Do not use `moreover`, `furthermore`, `nevertheless`, or `subsequently`.

### Rule 6.3 — Maximum of 25 words in a descriptive sentence
Descriptive text is more complex than procedural text, so the limit is 25 words.

> **STE:** The authentication middleware validates each incoming request before
> the controller processes it. (11 words)

### Rule 6.4 — Use paragraphs to show related information
A paragraph keeps related information together. Start each paragraph with a
topic sentence that tells the reader the topic. The sentences that follow
explain that topic or add information about it. A new paragraph tells the reader
that a new topic starts.

> **STE:** The data pipeline uses a sequence of stages to process events.
> Validation checks the event schema and rejects malformed events. Enrichment
> adds metadata to the event. Transformation converts the event into a target
> format. Persistence writes the event to the data store.

### Rule 6.5 — One topic in each paragraph
Each paragraph has one topic. The topic sentence is the first and most important
sentence. It gives new information and makes a logical connection to previous
information, usually with a key word or a connecting word.

If the reader collects the topic sentences of a document, those sentences make a
good outline of its content.

### Rule 6.6 — No more than six sentences in a paragraph
If a paragraph has more than six sentences, divide it into two paragraphs. Do
not put different topics in the same paragraph.

## Section 7 — Safety instructions

### Rule 7.1 — Use a signal word to show the level of risk

| Signal word | Use it when there is a risk of |
|---|---|
| WARNING | Security vulnerabilities, data loss, or system corruption |
| CAUTION | Unexpected behavior, performance degradation, or incorrect results |
| NOTE | No risk — supplementary information only (Rule 5.5) |

If the two levels of risk occur together, use a WARNING.

Severity mapping for release notes and changelogs: WARNING to BREAKING,
CAUTION to DEPRECATED, NOTE to NOTE.

A safety instruction must be specific. It must name the risk, not make a general
claim.

### Rule 7.2 — Start a safety instruction with a command or a condition
Start with a clear and accurate command. If the reader must know a condition
before they use a function, method, or API, give the condition first.

> **Non-STE:** WARNING: STORING API KEYS IN THE SOURCE CODE IS NOT RECOMMENDED.
>
> **STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. ALWAYS USE
> ENVIRONMENT VARIABLES OR A SECRETS MANAGER TO STORE API KEYS.

### Rule 7.3 — Give an explanation of the risk or possible result
Tell the reader what can occur if they do not obey the safety instruction. A
risk explanation has three parts:

1. The failure to obey the instruction
2. The immediate consequence
3. The final harm.

Write the chain in cause-first order: "If you do X, Y can occur."

> **Non-STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE.
>
> **STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. API KEYS IN
> SOURCE CODE CAN CAUSE UNAUTHORIZED ACCESS AND DATA BREACHES.
