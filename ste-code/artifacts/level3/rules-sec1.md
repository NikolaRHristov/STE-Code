# Level 3 — Section 1 (Words): Rules 1.1–1.14

Section 1 of STE-Code governs **words**: which words you may use, in which part
of speech, with which meaning, and in which form. Every other section of the
standard assumes these fourteen rules already hold. This slice is the complete,
LLM-optimized form of Section 1 — no aerospace leakage, code-domain examples only.

## Three gates (the core model)

Every word in code documentation must pass **one** of three gates:

1. The word is **approved in the controlled terminology** (the STE-Code
   dictionary). It must be used with its specified part of speech (Rule 1.2) and
   its approved meaning (Rule 1.3), in its approved form (Rule 1.4).
2. The word is a **code-domain technical noun** (Rule 1.5 categories), permitted
   only when it names a precise software concept. It must not be used as a verb
   (Rule 1.7) and must be the standard/short/consistent name (Rules 1.8–1.11).
3. The word is a **code-domain technical verb** (Rule 1.12 categories), permitted
   only when it names a precise software operation. It must not be used as a noun
   (Rule 1.13).

A word that passes no gate must be replaced, or the sentence restructured so that
approved words carry the meaning. American English spelling is required
everywhere (Rule 1.14); keep quoted (third-party) text verbatim.

### Definitions

- **Controlled terminology** — the STE-Code approved-word list. Each entry gives
  one part of speech and one approved meaning, plus approved verb/adjective forms.
- **Code-domain technical noun** — a noun term for a specified concept in software
  development, applicable to a subject field (Rule 1.5, 19 categories).
- **Code-domain technical verb** — a verb term for a specified operation or
  process in software development (Rule 1.12, 4 categories).
- **Project glossary** — the source of truth for which technical nouns/verbs your
  project approves, and which part-of-speech each carries.

### Documentation-type applicability

The same 14 rules apply to every code-documentation type: README, API docs,
docstrings/inline comments, commit messages, error messages/logs, CLI help,
changelogs, tests. Each rule below notes the highest-risk pattern per type. The
*canonical noun* for any item is the name in the code itself (class, function,
module, table, resource, environment variable, config key).

---

## Rule 1.1 — Use approved words, code-domain technical nouns, or code-domain technical verbs

In code documentation, use words that are:

- approved in the project controlled terminology,
- code-domain technical nouns, or
- code-domain technical verbs.

The controlled terminology gives the most frequently used words and lists
**unapproved** words with approved alternatives. Your project glossary/terminology
database holds the technical nouns and verbs of your subject field — check it
first.

**Worked vocabulary swaps (common Non-STE → STE):**

| Do not write | Write | Why |
|---|---|---|
| execute the script | run the script | "run" is the approved verb for executing programs |
| generate the artifact | make the artifact | "make" is approved; "generate" is not |
| utilize / leverage the cache | use the cache | inflated verb |
| bootstrap / initiate the service | start the service | "start" is approved |
| configure the runtime | set the runtime behavior | "set" is approved |
| retrieve / fetch the record | get the record | "get" is approved |
| transmit the payload | send the data | "send" is approved |
| validate / verify the input | check the input | "check" is approved |
| unable to connect | cannot connect | "cannot" is approved |
| invalid / malformed data | incorrect data, data that is not correct | "correct" is the approved adjective |
| implement X | add X (or refactor if structural) | "implement" not approved; "add"/"make" are |
| optimize the query | make the query faster | "optimize" not approved |

Technical terms stay even when unapproved: `UserAuthenticator` is a code-domain
technical noun, `serialize` is a code-domain technical verb; both are permitted.

**Per documentation type:**
- *README* — imperative verbs in setup sections ("run", "make", "set", "start");
  approved adjectives in descriptive sections ("large" not "substantial").
- *API docs* — descriptive prose uses approved words: "get" not "retrieve",
  "send" not "transmit", "remove" not "delete/purge", "check" not "validate".
- *Docstrings* — "do" not "perform", "check" not "ensure", "make" not "construct".
- *Commit messages* — smallest approved verb: add, fix, remove, update, set,
  make, check, run. No "implement"/"refactor-for-clarity"/"optimize".
- *Error messages* — "cannot" not "unable to"; "incorrect" not "invalid/malformed".

**Paradigm notes:** OOP prose uses approved verbs (make, get, set, call, send,
keep); class/method names stay as technical nouns. Functional `map`/`fold`/`reduce`/
`filter`/`compose`/`curry` are code-domain technical verbs (Rule 1.12). Procedural
"allocate" is not approved → "make a buffer"; "free"/"dereference" are technical
verbs. Declarative SQL keywords and resource kinds are technical terms; "provision"
→ "make"/"set up", "orchestrate" → "control"/"manage". Systems Rust "own"/"borrow"/
"move" are technical verbs; "dangling pointer"/"undefined behavior" are compound
technical nouns.

---

## Rule 1.2 — Use approved words only as the specified part of speech

Each entry in the controlled terminology carries one label: verb (v), noun (n),
adjective (adj), adverb (adv), preposition (prep), conjunction (conj), pronoun
(pron), or article (art). Use the word only in that grammatical role.

- "Query" is an approved **noun**, not a verb. Write "Send a query to the
  database", not "Query the database".
- "Static" is an approved **adjective**, not a verb. Write "Make the variable
  static", not "Static the variable".
- Some words carry more than one label. "Call" is an approved verb and noun;
  sentence position shows the function.

If the word you want is not in the controlled terminology: (1) find it in a
standard English dictionary; (2) find the best approved synonym; (3) use that
approved word, or restructure the sentence.

**Most common violations (use the approved replacement):**

| Do not write | Error | Approved replacement |
|---|---|---|
| Query the database / Cache the result / Queue the job / Log the error / Index the record | technical noun used as verb | Send a query / Keep the result in the cache / Put the job in the queue / Write the error in the log / Use the index |
| Docker the app / Git the change / Kubectl the pod / Terraform the VPC | tool name used as verb | Use Docker / Save with Git / Use `kubectl` / Use Terraform |
| Secure the endpoint / Empty the buffer / Silent the log | adjective used as verb | Make the endpoint secure / Make the buffer empty / Make the log silent |
| Static the variable / Ready the worker / Live the connection | adjective used as verb | Make the variable static / Make the worker ready / Make the connection live |
| Utilize / Leverage / Employ the service | inflated verb | Use the service |
| Commence the build / Initiate the transfer / Terminate the process | inflated verb | Start the build / Start the transfer / Stop the process |
| Orchestrate the services / Facilitate the sync | unapproved verb | Control the services / Help the sync |

**Per documentation type:** README — no "Docker the app" / "Git your changes".
API docs — "Caches the profile" → "Keeps the profile in the cache"; "Errors on
duplicate email" → "Gives an error". Docstrings — "init the pool" → "Start the
connection pool"; "param the input" → "Set the input parameter". Commit messages —
"cache the query results" → "add a cache". Error messages — "fail" is a verb; use
"failure" as noun. "The request timed out" → "The request did not complete within
the timeout" (timeout is a noun).

**Paradigm notes:** OOP — "Factory the object"/"Singleton the instance" → "Make
with a factory"/"Make the logger a singleton". Functional — "map" stays a
technical verb; "pipe" as a verb → "apply the `pipe` function". Procedural —
"Malloc a buffer" → "Make a buffer with `malloc`"; "Goroutine the task" → "Run the
task in a goroutine". Declarative — "Terraform the VPC" → "Use Terraform to make
the VPC". SQL keywords in prose need backticks: "Use `SELECT` to get data".

---

## Rule 1.3 — Use approved words only with their approved meanings

Each approved word has one specified meaning, often narrower than standard
English. Do not use an approved word with any other meaning.

**Four-step check for every approved word:**
1. Identify the part of speech as used in the sentence.
2. Look up the approved meaning for that part of speech in the controlled
   terminology.
3. Does your sentence use exactly that meaning? If not, the word fails even when
   approved and the sentence reads well.
4. Replace with an approved alternative, or restructure.

**Worked check:** "The background worker runs every night." → "runs" is a verb;
approved meaning of "run" = "execute a program or command". Writer meant
"operates on a schedule" → rewrite "The background worker operates every night."

**Most-misused approved words:**

| Approved word | Use it only this way | Wrong meaning to avoid | Approved alternative |
|---|---|---|---|
| run | execute a program or command | operate, manage, continue | operate, manage, continue |
| return | send a value back from a function to its caller | go back to a state/location | go back |
| call | invoke a function/method/subroutine | name something, shout | name, refer to as |
| get | fetch or retrieve data from a source | become, understand, receive | become, understand, receive |
| set | put a value into a variable/config | become solid, prepare | become solid, prepare |
| make | bring into existence by building | force, earn | cause, earn |
| send | transmit data to a destination | cause to go (a person) | cause to go |
| raise | cause an exception/error to occur | increase, lift | increase, lift |
| catch | handle/intercept an exception | capture a moving object | capture, become trapped |
| pass | give data as an argument to a function | go past, succeed | go past, succeed, give |
| check | examine for correctness or state | stop, restrain, leave | stop, leave |
| break | exit a loop/switch immediately | divide, damage, interrupt | split, damage, interrupt |
| continue | skip to next loop iteration | keep doing without interruption | keep |
| fail | an operation did not complete | not pass a test | not pass |
| move | transfer ownership of a value (Rust) | change physical position | go, change position |
| borrow | take a reference without ownership | take temporarily | take temporarily |

**Commit-message meanings:** add = include new code/files; fix = correct a defect;
remove = delete so it no longer exists; update = change to newer state; set =
configure a value/flag.

**Test/changelog notes:** "pass"/"fail" in test reporting mean the test reached /
did not reach its expected result — not "go past" or "not pass an exam".
"support" (verb) = provide compatibility with; not "hold up" or "endorse".

**Paradigm-specific approved meanings:** OOP — "class"/"object"/"method"/"interface"
keep their code-domain senses; "extend" = create subclass; "override" = replace an
inherited method. Functional — "pure" = no side effects; "map"/"reduce"/"filter"/
"fold"/"compose"/"curry" keep their FP technical senses. Do not use them with
general-English meanings.

<!-- END -->
