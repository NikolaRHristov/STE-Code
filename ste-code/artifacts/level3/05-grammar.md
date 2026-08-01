# Level 3 — Grammar

Grammar layer of STE-Code: the parts of the standard that constrain **form** —
word class, verb form, sentence shape, punctuation, and word count.
Vocabulary (which words you may use) is in `03-dictionary.md`; this file is
about how approved words are combined.

Scope: all code documentation — README files, API reference, docstrings, inline
comments, commit messages, error and log messages, changelogs, configuration
comments, specifications. Source code itself and the contents of fenced code
blocks are **out of scope**.

## Quick contract for a generator

| Constraint | Value |
|---|---|
| Approved verb forms | infinitive, imperative, simple present, simple past, simple future, past participle **as adjective only** |
| Forbidden verb forms | perfect, progressive, perfect-progressive, gerund-as-verb, auxiliary + past participle |
| Voice | active; passive only in descriptive text when the agent is unknown |
| Procedural sentence | max 20 words |
| Descriptive sentence / note | max 25 words |
| Instructions per sentence | 1 |
| Topics per sentence | 1 |
| Sentences per paragraph | max 6, one topic per paragraph |
| Technical noun length | max 3 words |
| Semicolon | forbidden — split into two sentences |
| Contractions | forbidden — write words in full |
| Phrasal verbs | forbidden unless explicitly approved |
| Articles | required before nouns; omitted before identifiers and abstract concepts |

## 1 — Words and parts of speech

**1.1 Use approved words only.** A word is usable if it is approved in the
controlled terminology, or is a code-domain technical noun, or is a code-domain
technical verb. Nothing else.

**1.2 Use an approved word only as its approved part of speech.** The
dictionary fixes the class. `TEST (n)` is not a licence to write "test the
build" unless `TEST (v)` is also approved.

**1.3 Use an approved word only with its approved meaning.** Approved words
normally carry exactly one meaning. Other standard-English senses are excluded.

**1.4 Use only the approved forms of verbs and adjectives.** See section 3.

**1.5 Technical nouns may be added by category.** A code-domain technical noun
names a specified software concept in a subject field (codebase, framework,
ecosystem). The controlled terminology cannot list them all; add them to the
project glossary, API reference, or ADRs, and only inside an approved category.

**1.6 An unapproved word is permitted only when it is (or is part of) a
code-domain technical noun.** Never as ordinary prose.

**1.7 Do not use technical nouns as verbs.**

> Do not write: The service *databases* the record.
>
> Write: The service writes the record to the database.

**1.8 Prefer technical nouns already approved in your project, company,
industry, or subject field** over invented ones.

**1.9 When you must coin a technical noun, make it short and clear** — not more
than three words. Add one or two adjectives only when the context does not
disambiguate.

> Do not write: Delete the four deprecated middleware registration statement entries that bind the request route to the legacy cover module.
>
> Write: Delete the four handler entries (lines 10–14) that bind the route to the cover module.

**1.10 Do not use regional words, slang, or jargon as technical nouns.**

**1.11 Do not use different technical nouns for the same item.** One item, one
name. Do not alternate `configuration file`, `settings file`, and `config`.

**1.12 Technical verbs may be added by category.** A code-domain technical verb
names a specified operation or process in software development.

**1.13 Do not use technical verbs as nouns.**

> Do not write: Run a *deploy* of the service.
>
> Write: Deploy the service.

**1.14 Use American English spelling** unless a project specification, style
guide, or contract directs otherwise. Do not change the spelling of quoted
text — error strings and UI labels stay verbatim.

### Approved technical verb categories

| Category | Verbs |
|---|---|
| Development operations | build, compile, test, lint, format, commit, push, deploy, rollback |
| Data operations | read, write, serialize, deserialize, parse, encode, decode, query, insert, migrate |
| Application operations | handle, route, authenticate, authorize, validate, schedule, dispatch, resolve |
| Communication actions | send, receive, publish, subscribe, stream, poll, broadcast, connect |

Prefer the plain approved verb — use, start, stop, show, make, get, set, check,
do, send, remove, keep — over *utilize*, *leverage*, *employ*, *commence*,
*terminate*, *initiate* when the simple verb already carries the meaning.

## 2 — Noun phrases

**2.1 Keep technical nouns short** — maximum three words. Split longer strings
with prepositions (of, on, in, for, to).

> Do not write: Request handler timeout retry policy value.
>
> Write: The retry policy for the timeout of the request handler.

**2.2 Write a long technical noun in full**, then make it usable by one of:

- Give a shorter form after the first full occurrence.
- Hyphenate the words that act as one unit.
- Split the noun with prepositions.

A term that comes from an official source (an API specification, a schema, an
OpenAPI file, an architecture diagram) is written in full at first occurrence,
explained, and then abbreviated for the rest of the document. Terms fixed by
your framework or subject field stay as they are.

**2.3 Use hyphens between words used as one unit.** See Rule 8.2 for the five
hyphenation categories and Rule 8.7 for their word count.

## 3 — Verbs

**3.1 Use only the verb forms that the dictionary gives.** Every approved verb
lists four forms in this order: base, third-person singular, simple past, past
participle.

```
VALIDATE (v)
VALIDATES
VALIDATED,
VALIDATED

BUILD (v)
BUILDS
BUILT,
BUILT
```

**3.2 Use only these forms and tenses.**

| Verb | Imperative | Simple present | Simple past | Simple future | Past participle (adjective) |
|---|---|---|---|---|---|
| (to) parse | Parse the file | It parses | It parsed | It will parse | the parsed file |
| (to) write | Write the log | It writes | It wrote | It will write | the written log |
| (to) build | Build the image | It builds | It built | It will build | the built artifact |
| (to) send | Send the request | It sends | It sent | It will send | the sent request |
| (to) validate | Validate the token | It validates | It validated | It will validate | the validated token |

Not approved: present perfect (has parsed), past perfect (had parsed),
progressive (is/was parsing), future progressive (will be parsing), perfect
progressive (has been parsing), gerund used as a verb (keeps parsing), and all
other complex constructions.

Selection:

1. Infinitive after a modal or to state a purpose — "Use this flag to parse the file."
2. Imperative for each procedure step — "Parse the file. Write the log."
3. Simple present for a fact or system behavior — "The parser reads the file."
4. Simple past for a completed action — "The build failed."
5. Simple future with `will` + base form — "The job will start at 02:00."
6. Past participle only as an adjective before a noun — "the deprecated method."

Repairs:

| Unapproved | Approved |
|---|---|
| has parsed | parsed |
| had parsed | simple past, split into two sentences with "Then" |
| is parsing / was parsing | simple present or simple past |
| will be parsing | will parse |
| is being parsed | name the actor: "the worker parses the file" |

**3.3 Use the past participle as an adjective**, not as part of a verb.

**3.4 Do not use auxiliary verbs to build complex verb constructions.** Do not
combine have, be, will, can, must, should, or "is to be" with a past participle
to make compound tenses or the passive voice.

> Do not write: The build has compiled the module before the test runs.
>
> Write: The build compiled the module. Then the test runs.
> Do not write: The migration is to be run before you deploy the service.
>
> Write: Before you deploy the service, run the migration.
> Do not write: The cache can be cleared.
>
> Write: You can clear the cache.

**3.5 Use an "-ing" form only as a technical noun or as a modifier inside a
technical noun** — never as a verb. Approved "-ing" words include the nouns
logging, monitoring, routing, servicing; the adjectives matching, missing,
remaining; the pronoun something; and the preposition during. The progressive
tense is excluded because it is not in the Rule 3.2 list.

**3.6 Use the active voice.** In descriptive text the passive is permitted only
when the agent is unknown. Test a sentence by asking "by whom or by what?" — if
the sentence answers it, it is passive.

> Do not write: The API response is parsed by the middleware.
>
> Write: The middleware parses the API response.

**3.7 Describe an action with an approved verb, not a noun.**

> Do not write: Validation of the token happens in the handler.
>
> Write: The handler validates the token.

## 4 — Sentences

**4.1 One topic per sentence. No abstract text.** Do not combine multiple
actions, conditions, or subjects.

**4.2 Do not omit words and do not use contractions.** Keep the subject, the
verb, the nouns, and the articles. Write "do not", "is not", "are not" — never
"don't", "isn't", "aren't". A shorter sentence is not automatically clearer.

> Do not write: Can be a maximum of five inches long.
>
> Write: A cache key can have a maximum length of 64 characters.

**4.3 Use a vertical list for complex text.** Use a list when a sentence must
carry many items — parameters, return fields, error codes, configuration
options, environment variables, dependencies, test cases.

- Put a colon at the end of the introductory sentence.
- Mark each item with a number, letter, dash, or bullet.
- Start each item with an uppercase letter.
- Use an article before the subject noun of an item where applicable.
- End a full-sentence item with a period; an imperative step is a full sentence.
- Do not end a fragment item with a period, a comma, or a semicolon.
- Put a period at the end of the last item.

Do not mix imperative instructions and descriptive statements in one list. In
safety instructions, write the negative command (DO NOT) inside each item that
needs it.

**4.4 Use connecting words and connecting phrases.** Approved connectors:
`and`, `but`, `then`, `thus`, `also`, `however`, `therefore`, `for example`,
`as a result`, `at the same time`. Place the connector at the start of the
sentence so the reader sees the signal before the content. Do not use
*moreover*, *furthermore*, *nevertheless*, or *subsequently*. Demonstrative
adjectives (this, these) may also connect a sentence to the one before it.

**4.5 Use an article or a demonstrative adjective before a noun.**

- Use an article before each noun in a short sentence.
- In a series, use the article before the first noun only — unless an adjective
  applies to one item only, in which case repeat the article.
- Do not use an article before an abstract concept: performance, scalability,
  error handling, concurrency, backward compatibility.
- Do not use a definite article before a code identifier. A function, class,
  variable, file name, environment variable, error code, and version tag are
  proper nouns.
- Always keep the noun after `this` or `these`. Never write `this` alone.

## 5 — Procedures

**5.1 Maximum 20 words in a procedural sentence.** This covers installation
steps, setup guides, deployment checklists, debugging workflows, and API usage
guides. Warnings and cautions obey the same limit. Notes may reach 25 words.
Code blocks, command examples, terminal output, string literals, and identifier
names inside examples are excluded from the count.

> Do not write: Run the database migration script from the project root directory and then restart the application server to apply all pending schema changes to the production environment. (27 words)
>
> Write: Run the database migration script from the project root directory. Then restart the application server. (9 + 7 words)

**5.2 One instruction per sentence.** If a step contains two actions, write two
sentences or two numbered steps.

**5.3 Use the imperative form for instructions.** "Set the timeout value." Not
"The timeout value should be set."

**5.4 Put the descriptive statement before the command.** Give the condition
first, then the action, so the reader knows when the step applies.

**5.5 Notes give information only.** A note must not contain an instruction, a
command to run, a step, or an imperative verb. It must not give requirements,
limits, tolerances, or expected results of a step — that information belongs in
the step itself. Move anything critical for data loss, security, or system
damage into a WARNING or CAUTION. Each note sentence has a maximum of 25 words.

Verification: read the procedure without the notes. If the reader cannot
complete it, the missing information belongs in a step.

> NOTE: The API rate limiter allows a maximum of 1000 requests per minute per client IP address on the free tier.

## 6 — Text structure

**6.1 Give information gradually.** One subject per sentence. Do not pack a
request lifecycle, an error path, and a logging side effect into one sentence.

**6.2 Use key words and key phrases to give the text a logical structure.** Key
words repeat across a documentation block and link its concepts. Do not vary
them. Connecting words act as traffic signs: they tell the reader whether the
information is new, contrasting, or a result.

**6.3 Write short sentences — maximum 25 words in descriptive text.**
(Procedural text keeps the 20-word limit of Rule 5.1.)

**6.4 Use paragraphs to show related information.**

**6.5 One topic per paragraph.**

**6.6 Maximum six sentences per paragraph.**

## 7 — Safety instructions

**7.1 Use a signal word to show the level of risk.**

| Signal word | Use when | Release-note / changelog mapping |
|---|---|---|
| WARNING | Risk of security vulnerability, data loss, or system corruption | BREAKING |
| CAUTION | Risk of unexpected behavior, performance degradation, or incorrect results | DEPRECATED |
| NOTE | Supplementary information only | NOTE |

If both risk levels apply together, use WARNING.

**7.2 Start a safety instruction with a clear and accurate command or
condition.** If the reader must know a condition before using a function,
method, or API, give the condition first.

> Do not write: WARNING: STORING API KEYS IN THE SOURCE CODE IS NOT RECOMMENDED.
>
> Write: WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. USE ENVIRONMENT VARIABLES OR A SECRETS MANAGER.

**7.3 Explain the risk or the possible result.** A risk explanation has three
parts: the failure to obey the instruction, the immediate consequence, and the
final harm. Write it cause-first: "If you do X, Y can happen." An instruction
without a risk explanation is a prohibition the reader can dismiss.

> WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. API KEYS IN SOURCE CODE CAN CAUSE UNAUTHORIZED ACCESS AND DATA BREACHES.

## 8 — Punctuation and word count

**8.1 Use all standard English punctuation except the semicolon.** The
semicolon lets you build long sentences that are hard to read in comments and
docs, and it is easy to misuse. Write two sentences instead. The rule does not
apply to source code or to text inside code blocks, where the semicolon is
language syntax.

> Do not write: Call the function to parse the response data; handle any errors that occur.
>
> Write: Call the function to parse the response data. Handle any errors that occur.

**8.2 Use hyphens to connect words that are directly related.** Five categories:

| Category | Code-domain examples |
|---|---|
| 1. Multi-word adjective before a noun | high-priority task, read-only file, thread-safe method, event-driven architecture, run-time error, end-to-end test, server-side rendering, just-in-time compilation |
| 2. Two-word fractions and numbers | seventy-two, one hundred and twenty-eight, three-fourths |
| 3. Uppercase letter or number plus a noun (shape or configuration) | L-shaped bracket, T-shaped connector, 64-bit register, 8-byte alignment, 128-bit value |
| 4. Verb whose first part is a noun or other part of speech | dry-run, hot-reload, cold-start, hard-code, soft-delete, short-circuit |
| 5. Prefix ending in a vowel before a root starting with a vowel | pre-initialized, re-entrant, de-allocated, anti-aliasing, re-indexed |

A hyphen joins words into one concept. A dash separates ideas or shows a range
("lines 12–48"). Keep them distinct.

**8.3 Use parentheses** to:

- Make references to code modules, diagrams, or text
- Include letters or numbers that identify items
- Identify the work steps in a procedure
- Include abbreviations
- Give the singular and plural forms of a noun at the same time
- Explain a word or part of a sentence
- Include an alternative.

**8.4 A colon in a vertical list counts as a period.** It marks the end of a
sentence. So the introductory part before the colon takes a maximum of 20 words
in procedural text and 25 words in descriptive text, and each item after the
colon counts as a new sentence with the same limits.

**8.5 Text in parentheses counts as one word** in the sentence that contains
it. The words inside the parentheses also form their own sentence, so count
them there. An identifier or an abbreviation in parentheses counts as one word.

> Write: Make sure that the DEBUG environment variable is set to false (the DEBUG flag is off). (12 words)

**8.6 Count each of these as one word:**

- Numbers
- Numbers together with units of measurement
- Abbreviations
- Alphanumeric identifiers
- Quoted text
- Titles, headings, and text on user interface elements and labels
- Proper nouns of individuals, groups, organizations, and geopolitical entities.

**8.7 A hyphenated word counts as one word.** A group of words hyphenated to act
as an adjective before a noun is one unit for the word-count limits.

> Do not write: The open function returns a read only file descriptor.
>
> Write: The open function returns a read-only file descriptor. ("read-only" = one word)

## 9 — Applying the standard

**9.1 Use a different sentence construction when a word-for-word replacement is
not sufficient.** When a word is unapproved, the dictionary gives alternatives.
Replace word-for-word only when the part of speech matches and the meaning does
not change. Rewrite the sentence when:

1. The grammatical structure must change to use the alternative.
2. The replacement gives a meaningless or unclear result.
3. The alternative changes the meaning.
4. The word to replace is not in the controlled terminology.

Then think about the purpose of the sentence: select different words, change
the verb form, write shorter sentences, remove unnecessary information, or ask
a developer for more information.

**9.2 Use each approved word correctly.** Read the approved meaning before you
use a word. Approved words normally have one approved meaning and one approved
part of speech. A small number are approved as more than one part of speech.

**9.3 Do not make phrasal verbs.** Two individually approved words can combine
into a phrasal verb whose meaning is different from its parts. Replace it with
a single approved verb. Only a few phrasal verbs are approved, and they have a
restricted meaning.

| Phrasal verb | Approved verb |
|---|---|
| put out (a warning) | emit |
| give off | release |
| carry out (a test) | do |
| shut down | stop |
| set up | configure |

> Do not write: The compiler puts out a warning when the type annotation is missing.
>
> Write: The compiler emits a warning when the type annotation is missing.

**9.4 Use a consistent style for terminology and wording.** The same type of
step gets the same wording every time. Use one name for one item (not
"configuration file", "settings file", and "config"). Use one verb for one
action (not "compile", "build", and "make"). Use the same sentence structure
for the same type of instruction.

> Do not write: Apply the patch to the main module. Wipe the module clean. Inspect the module assembly for errors.
>
> Write: Apply the patch to the module. Clean the module. Check the module for errors.

