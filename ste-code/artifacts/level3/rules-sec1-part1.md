# Level 3 — STE-Code Section 1 Rules, Part 1 (Words)

LLM-optimized distillation of the STE-Code controlled standard, Section 1 (Words).
This document covers the vocabulary-control rules for code documentation:
which words you may use, how to use them, and how to spell them.

Scope of this slice:
- Rule 1.1 — Approved words, technical nouns, technical verbs (the three-gate model)
- Rule 1.2 — Approved words only as their specified part of speech
- Rule 1.3 — Approved words only with their approved meanings
- Rule 1.4 — Only approved verb and adjective forms
- Rule 1.10 — No slang, jargon, or regional terms
- Rule 1.11 — One term per concept (consistency)
- Rule 1.12 — Technical verbs are allowed (category list)
- Rule 1.13 — Do not use technical verbs as nouns
- Rule 1.14 — American English spelling

It is self-contained: every rule below is stated plainly with code-domain examples.
For the full controlled terminology (dictionary) and the 19 technical-noun categories,
see `a-dictionary.md` and `a-categories.md` in the same artifact set.

## Principle legend (recurs in the examples)

These codes label the fix applied in each before/after pair:
- P1 — use an approved word from the controlled terminology
- P2 — use the approved part of speech
- P3 — use the approved meaning of the word
- P4 — use only approved verb/adjective forms (no "-ing" main verbs, correct tense/mood)
- P6 — quoted text (code, keywords, third-party output) is exempt and kept as-is
- P7 — do not use a technical noun as a verb
- P8 — use standard, well-known technical nouns
- P9 — prefer short, clear technical nouns
- P10 — no slang / jargon / metaphor
- P11 — one term per concept
- P12 — technical verbs allowed only when no approved verb fits
- P13 — do not use a technical verb as a noun
- P14 — American English spelling

---

## Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs

Every word in code documentation must pass one of three gates:

1. **Approved word** — listed in the STE-Code controlled terminology (Part 2), used with its
   specified part of speech (Rule 1.2) and approved meaning (Rule 1.3).
2. **Code-domain technical noun** — not in the terminology (or listed UNAPPROVED) but fits one
   of the 19 technical-noun categories (Rule 1.5). Names a specific concept, component, tool, or
   entity in software (e.g. `UserAuthenticator`, `Promise`, `kubectl`). A word that passes here
   must not be used as a verb (Rule 1.7).
3. **Code-domain technical verb** — not in the terminology but names a specific software operation
   (Rule 1.12), e.g. `serialize`, `refactor`, `lint`. A word that passes here must not be used as a
   noun (Rule 1.13).

A word that passes none of the three gates must be replaced with an approved alternative or the
sentence restructured.

Applies to all documentation types (README, API docs, docstrings, commit messages, error messages).
In each type, imperative verbs must come from the approved list.

Short substitutions to internalize:
- "execute" → `run` · "generate" → `make` · "configure" → `set` · "utilize/leverage" → `use`
- "retrieve/fetch" → `get` · "transmit" → `send` · "delete/purge" → `remove` · "verify" → `check`
- "unable to" → `cannot` · "invalid" → `not correct` · "commence/initiate" → `start` · "terminate" → `stop`
- "implement" → `make`/`add` (not approved as a verb) · "optimize" → `make faster`/`make smaller`

Example (README setup):
> Non-STE: To begin utilizing the build toolchain, you must first generate the distributable
> artifact via `npm run build`. Then, execute the compiled binary to bootstrap the local
> development service.
> STE: Use the build tool to make the binary. Run the binary to start the local service.

Example (API docstring):
> Non-STE: Fetches a user record from the remote API.
> STE: Gets a user record from the remote API.

See also: Rules 1.2–1.14, and `a-dictionary.md` / `a-categories.md`.

---

## Rule 1.2 — Use Approved Words Only as the Specified Part of Speech

Each approved word in the controlled terminology carries a part-of-speech label
(verb, noun, adjective, adverb, preposition, conjunction, pronoun, article). Use it only in that role.

Most common violations:
- **Noun-as-verb** — a tool/library/data-structure name used as a verb.
  `Docker the app` → `Use Docker to make a container` · `Git the change` → `Save the change with Git`
  `Cache the result` → `Keep the result in the cache` · `Query the database` → `Send a query to the database`
- **Adjective-as-verb** — `Secure the endpoint` → `Make the endpoint secure` ·
  `Empty the buffer` → `Make the buffer empty` (note: `clear` IS approved as both, so `Clear the flag` is fine)

Preferred approved verbs to replace inflated or misused forms:
- "utilize/leverage/employ" → `use` · "commence/initiate" → `start` · "terminate" → `stop`
- "orchestrate" → `control` · "facilitate" → `help`

The fix patterns:
1. Prepositional phrase: `Git the changes` → `Save the changes with Git`
2. Infinitive: `Queue the jobs` → `Use the queue to hold the jobs`
3. Make + adjective: `Secure the endpoint` → `Make the endpoint secure`

A word approved as more than one part of speech (e.g. `call`, `set`, `clean`) is valid in each role,
but the sentence structure must make the role clear. If a word appears twice with different roles,
restructure (e.g. use "change history" instead of "commit history" to avoid double "commit").

Exceptions:
- Code-domain technical verbs under Rule 1.12 override this rule for that specific word/context
  (e.g. `serialize` is permitted as a verb even though not in the general approved list).
- Quoted code/CLI commands in code blocks are exempt (Rule 1.5, category 10).

Examples:
> Non-STE: Query the database for user records.
> STE: Send a query to the database for user records.
>
> Non-STE: Static the variable to prevent modification.
> STE: Make the variable static to prevent modification.
>
> Non-STE: refactor: interface the user repository and factory the database connection
> STE: refactor: add an interface to the user repository and use a factory for the database connection

Command/keyword edge case: `return` is an approved verb ("send a value back from a function") —
`Return the result` is fine. `import`/`export` are NOT approved verbs — use
`Use \`import\` to add the module` / `Use \`export\` to make the function available`.

See also: Rules 1.1, 1.3, 1.4, 1.5, 1.7, 1.10, 1.12, 1.13.

---

## Rule 1.3 — Use Approved Words Only with Their Approved Meanings

Each approved word has exactly ONE approved meaning in the controlled terminology. Using the right
word with the wrong meaning is a violation even when the sentence is grammatical.

Decision procedure before publishing:
1. Identify the part of speech you used (Rule 1.2 selects the meaning).
2. Look up the approved meaning for that part of speech in `a-dictionary.md`.
3. Does your sentence use it with exactly that meaning? If no, it fails.
4. Replace with an approved word whose meaning fits, or restructure.

Most-misused approved words (use only the approved meaning):

| Word | Approved meaning | Wrong meaning to avoid → use instead |
|------|------------------|--------------------------------------|
| run | execute a program or command | operate/manage/continue → `operate`/`continue` |
| return | send a value back from a function to its caller | go back to a state/location → `go back` |
| call | invoke a function/method | name something → `name` |
| get | fetch or retrieve data from a source | become/understand → `become`/`understand` |
| set | put a value into a variable/config | become solid/prepare → `become solid`/`prepare` |
| make | bring into existence by building | force/earn → `cause`/`earn` |
| send | transmit data to a destination | cause a person to go → `cause to go` |
| raise | cause an exception to occur | increase/lift → `increase`/`lift` |
| catch | handle or intercept an exception | capture a moving object → `capture` |
| pass | give data as an argument to a function | go past/succeed → `go past`/`succeed` |
| check | examine for correctness or state | stop/restrain → `stop`/`leave` |
| break | exit a loop/switch immediately | divide into parts/damage → `split`/`damage` |
| continue | skip to next loop iteration | keep doing without interruption → `keep` |
| fail | an operation did not complete | not pass a test → `not pass` |
| move (Rust) | transfer ownership of a value | change physical position → `go`/`change position` |
| borrow (Rust) | take a reference without ownership | take temporarily → `take temporarily` |

Paradigm-specific meanings matter: e.g. in OOP `extend` = "create a subclass", `override` = "replace an
inherited method"; in functional `map` = "transform each element", `reduce` = "combine into one value",
`pure` = "no side effects"; in declarative SQL `select` = "retrieve rows" (not "choose"), `drop` =
"remove a table permanently"; in systems `own`/`borrow`/`move`/`drop` carry Rust ownership meanings.

Examples:
> Non-STE: This tool runs on Node.js and runs in the browser.
> STE: This tool operates on Node.js and operates in the browser. (first two "runs" = operates)
>
> Non-STE: Raises the value by 10% and passes it through the pipeline.
> STE: Increases the value by 10% and sends it through the pipeline.
>
> Non-STE: refactor: break the UserService into smaller classes
> STE: refactor: split the UserService into smaller classes  ("break" = exit a loop, not divide)

Edge case — multiple approved meanings: `set`, `run`, `file`, `test` have >1 approved meaning tied to
part of speech; `call` means "invoke" (verb) vs "invocation" (noun). Use "name", not "call", for
"we call this pattern X". Edge case — framework name shares spelling with an approved word
(`Express` the framework vs `express` the verb): capitalize the framework, do not use it as a verb.

See also: Rules 1.1, 1.2, 1.4, 1.7, 1.11, 1.13.

---

## Rule 1.4 — Use Only the Approved Forms of Verbs and Adjectives

The controlled terminology lists the approved inflected forms of each approved verb and adjective.
Use only those forms.

Verbs: use the imperative/base form for procedures, simple present (3rd-person `-s`) for descriptions,
simple past for completed actions. **Do not use the "-ing" form as the main verb of a procedural or
descriptive sentence** — this is the most common Rule 1.4 violation. Concentrate tenses: simple
present, simple past, simple future; not present/past perfect continuous.

Example approved verb table:

| Verb | Imperative | 3rd-person | Past | Past participle (adj) | Non-approved |
|------|-----------|------------|------|------------------------|--------------|
| make | Make | Makes | Made | Made | Making, Maked |
| get | Get | Gets | Got | Got (past only) | Getting, Getted |
| set | Set | Sets | Set | Set | Setting, Setted |
| call | Call | Calls | Called | Called | Calling |
| check | Check | Checks | Checked | Checked | Checking |
| give | Give | Gives | Gave | Given | Giving, Gived |
| run | Run | Runs | Ran | Run | Runned, Running (as main verb) |

Adjectives: use the dictionary-listed comparative/superlative forms (`fast`→`faster`/`fastest`,
`slow`→`slower`/`slowest`). Do not use "more fast" / "more slow". Adjectives that form comparatives
with `more`/`most` use those approved words instead. Do not invent forms like "compilating",
"membered", "performant".

Examples:
> Non-STE: The compiler is compilating the source files every time you save.
> STE: The compiler compiles the source files each time you save.
>
> Non-STE: This algorithm is more fast than the previous one.
> STE: This algorithm is faster than the previous one.
>
> Non-STE: Fixed memory leak and adding timeout configuration
> STE: Fix memory leak and add timeout configuration  (commit subjects: imperative, base form)
>
> Non-STE: Connection failed: the database is not running. Please verify and retrying the migration.
> STE: Connection failed: the database does not run. Check and try the migration again.

Code-domain technical verbs (Rule 1.12) follow standard English morphology and are exempt from the
closed approved-verb list, but still obey the tense/mood constraints (no "-ing" main verbs, correct
tense). `run` is irregular (run/runs/ran/run); `give` (give/gives/gave/given).

See also: Rules 1.1, 1.2, 1.3.

---

## Rule 1.10 — Do Not Use Regional, Slang, or Jargon Words as Technical Nouns

Use well-known words. Avoid regional terms (ecosystem-specific vocabulary), slang (metaphorical or
casual verbs), and jargon (community-dependent fuzzy terms) — even when they name a "concept".

Replace jargon with plain approved words:
- `cruft` → `unnecessary code` · `monkeys with` → `changes` · `grok` → `understand`
- `yak shaving` → `completing unrelated prerequisite tasks`
- `bikeshedding` → `unnecessary discussion about small details`
- `foo`/`bar` → `example`/`placeholder` · `pear-shaped` → `failed`
- `yeet` → `remove` · `dumpster fire`/`nuke` → state problem + action plainly
- `nerfed` → `decreased performance` · `shiny new hotness` → `current interface`
- `twiddle`/`tweak` → `change`/`set` · `pwn` → `control`

Community abbreviations that transcended jargon stay as technical nouns: `API`, `JSON`, `SQL`, `HTML`.
Less-universal ones remain jargon: `AFAICT`, `IIRC`, `IMHO` — spell out or omit. Initialisms that encode
principles (`DRY`, `KISS`, `YAGNI`) are jargon abbreviations; state the principle directly.

Temporal jargon has no fixed meaning: `modern`, `legacy`, `cutting-edge`, `state-of-the-art` → describe
the specific characteristic (`uses async/await`) or date (`written in 2018`).

Examples:
> Non-STE: Remove all the cruft from the legacy module.
> STE: Remove all the unnecessary code from the legacy module.
>
> Non-STE: I spent the morning yak shaving before I could write the test.
> STE: I spent the morning completing unrelated prerequisite tasks before I could write the test.
>
> Non-STE: This library lets you pwn the DOM.
> STE: This library lets you control the DOM.
>
> Non-STE: Replace the foo and bar placeholders with real values.
> STE: Replace the example and placeholder values with real values.
>
> Non-STE: The upload went pear-shaped halfway through.
> STE: The upload failed at 50 percent. Check your network connection and try again.

Paradigm slang to avoid: OO `POJO-ify`/`bean-ize` → `convert to a plain object`; FP `eta-reduce` →
`simplify the function`; procedural `massage the buffer` → `adjust the buffer`; declarative
`cattle not pets` → `disposable resources`; systems `UB`/`UAF` → `undefined behavior`/`use-after-free`
(spell out on first use).

Review checklist: (1) would a developer from another country understand every word? (2) replace
metaphors/idioms with literal descriptions; (3) expand abbreviations on first use; (4) replace
community nicknames with standard terms; (5) replace temporal words with dates/characteristics;
(6) verify every noun/verb is approved or a justified technical noun; (7) no slang verbs
(`hit`, `nuke`, `yeet`, `tweak`, `twiddle`).

See also: Rules 1.1, 1.5, 1.6, 1.11, 1.12, 1.13, 1.14.

---

## Rule 1.11 — Do Not Use Different Technical Nouns for the Same Item

Pick one code-domain technical noun for each component, service, module, endpoint, class, function,
table, resource, environment variable, or configuration key — and use it consistently everywhere.
The source of truth is the code itself (the class/function/module/table/resource name as defined in
the repo). Do not drift to colloquial synonyms.

Examples:
> Non-STE: Initialize the UserService class ... Call the authenticate method on the AccountManager ...
>          The UserHandler returns a session token.
> STE: Initialize the UserService class ... Call the authenticate method on the UserService ...
>       The UserService returns a session token.
>
> Non-STE: Send a request to the /api/login path ... The authentication route returns a JSON Web Token ...
> STE: Send a request to the /api/login endpoint ... The /api/login endpoint returns a JSON Web Token ...
>
> Non-STE: Set the database_connection_timeout ... The DB timeout parameter ... Increase the connection deadline ...
> STE: Set the database_connection_timeout ... The database_connection_timeout parameter ...
>       Increase the database_connection_timeout value ...

Per paradigm: the canonical noun is the class name (OO), the module/function name or type alias
(functional), the function/struct/file path (procedural), the resource/table name (declarative), the
language-spec or glossary term (systems, abstract concepts). Parallel lists must use one naming
convention. When a project genuinely has multiple components, introduce each explicitly rather than
drifting names.

Grammar consequence: consistent nouns keep English article and pronoun reference chains intact
(`the UserService ... it returns` — not `the AccountManager`, which breaks anaphora).

Edge cases: framework/library names that are also approved words (`Make`, `Act`, `Before`) — use the
framework name as a technical noun, capitalize to disambiguate (`Use the Make build tool to make the
project`). Generated code symbols — use the generated name as-is, define a declared alias if long.
Renaming during refactor — after commit, update all docs to the new name; keep `DEPRECATED` marker only
if the old name persists in a public API.

See also: Rules 1.1, 1.3, 1.5, 1.6, 1.8, 1.9, 1.10, 3.1, 3.6.

---

## Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category

Code-domain technical verbs are permitted even when not in the approved word list, IF they name a
specific software operation and no approved verb gives the same meaning. They obey the same tense/
mood/voice rules as approved verbs (Rule 1.4, Section 3).

**Prefer an approved verb when one fits** (e.g. `find` over `detect` when not a security context;
`run` + noun over `migrate`; `run` over `execute`; `check` over `verify`). Use the technical verb only
when precision needs it and an approved verb would be vague.

The four categories (examples — not an exhaustive list):

**1. Development processes**
- a) Write/modify code: `compile, concatenate, import, inject, instantiate, lint, minify, marshal,
  optimize, polyfill, refactor, resolve, shim, stub, substitute, tokenize, transpile, trace, vectorize`
- b) Test/verify: `assert, benchmark, debug, fuzz, instrument, mock, profile, snapshot, spy, stub, unit-test`
- c) Build/package: `bundle, deploy, package, publish, release, tag, version`
- d) Manage deps: `hoist, install, link, lock, pin, update, upgrade`

**2. Computer processes and applications**
- a) I/O: `click, copy, cut, digitize, enter, paste, press, print, scan, swipe, tap, type`
- b) UI/app ops: `clear, close, delete, deselect, disable, drag, drag and drop, enable, encrypt,
  erase, filter, hide, highlight, invalidate, maximize, minimize, navigate, open, save, scroll,
  select, show, sort, store, submit, toggle, validate, zoom in, zoom out`
- c) System ops: `abort, authenticate, authorize, boot, cache, communicate, configure, debug,
  deserialize, download, format, hydrate, initialize, install, load, log, manage, mount, process,
  reboot, render, retry, serialize, spawn, synchronize, throttle, update, upgrade, upload`

**3. Instructions for subject fields**
- a) Algorithmic/math/data: `aggregate, bisect, compute, concatenate, convert, count, decode, encode,
  escape, filter, hash, index, map, merge, normalize, parse, pipeline, precompute, recalculate,
  reduce, tokenize, transform, validate, verify`
- b) Database/storage: `backup, compact, flush, index, migrate, persist, query, replicate, restore,
  roll back, seed, shard, upsert, vacuum, write-ahead`
- c) Network/communication: `broadcast, connect, disconnect, establish, forward, handshake, intercept,
  listen, poll, proxy, reject, resolve, route, send, stream, timeout, tunnel, unsubscribe, webhook`
- d) Security/auth: `authenticate, authorize, decrypt, decode, encode, encrypt, hash, revoke, salt,
  sanitize, sign, validate, verify`

**4. Legal and licensing terms** (only for legal/regulatory text):
`acknowledge, assign, comply with, conform to, disclose, enforce, explain, grant, inform, license,
modify, notify, permit, regulate, sign, supersede, waive`

Paradigm-specific verb sets:
- OO: `instantiate, inherit, override, extend, implement, encapsulate, delegate, inject`
- Functional: `compose, curry, map, reduce, fold, recurse, memoize, lift`
- Procedural: `allocate, deallocate, dereference, flush, signal`
- Declarative: `provision, converge, reconcile, apply, destroy`
- Systems (Rust): `borrow, own, drop, move, pin, acquire, release`

Examples:
> Non-STE: If you detect broken wires, repair them.  →  STE: If you find broken wires, repair them.
> (general context: "detect" not approved → use approved `find`)
>
> Non-STE: The intrusion detection system detects unauthorized access ...  (security context)
> STE: The intrusion detection system detects unauthorized access ...  ("detect" is a technical verb here)
>
> Non-STE: migrate the database schema ... verify the row counts
> STE: run the migration of the database schema ... check the row counts  (approved verb + noun preferred)

Light-verb anti-pattern (see Rule 1.13): do not wrap a technical verb in `do/make/perform/execute`
as a noun. Multi-word technical verbs (`roll back`, `drag and drop`, `zoom in`, `write-ahead`) stay as
one unit — do not split them with an object.

See also: Rules 1.1, 1.2, 1.5, 1.7, 1.11, 1.13, Section 3.

---

## Rule 1.13 — Do Not Use Technical Verbs as Nouns

Code-domain technical verbs (Rule 1.12) must be used only as verbs, never as nouns. If you need a noun,
use an approved noun or a code-domain technical noun. The most common violation is the **light-verb
construction**: a weak verb (`do/make/perform/execute/run`) + a nominalized technical verb.

Fix: use the technical verb as the main verb.
- `Make a commit` → `Commit` · `Do a compile` → `Compile` · `Execute a deploy` → `Deploy`
- `Run a build` → `Build` (when "build" names an artifact/process, it is a dual-category noun — see below)
- `The /api/login endpoint` (noun) ✓ vs `Do a login` → `Log in`
- `merge` as noun → `merge operation` · `import` as noun → `import operation`

Dual-category words (permitted as both verb and noun because they name a concrete artifact/event):
`build` (category 3 dev tools), `deploy` (cat 5 infra), `test` (cat 3), `commit` (cat 4 data structures),
`merge` (cat 4), `release` (cat 5), `patch` (cat 4), `log` (cat 13 runtime), `import` (cat 4).
Test: if you can put `a/an/the` before it and the sentence stays grammatical AND the word names a
concrete artifact/event in a technical-noun category, it is correct (`the build failed` ✓). If not
(`the compile failed`), it is a violation.

Article test: `the lint found errors` → VIOLATION (`lint` not dual-category) → `the linter found errors`.
`the serialize failed` → VIOLATION → `the serialization failed` or `the function serializes`.

Per paradigm: OOP — `do an instantiate` → `instantiate`; functional — `do a map over the list` →
`map over the list`; procedural — `do an allocate of memory` → `allocate memory`; declarative —
`do an apply of the manifest` → `apply the manifest`; systems — `the borrow of the reference` →
`the reference borrow` (or `borrow` as noun is fine for the Rust borrow concept, but `do a borrow` is wrong).

Examples:
> Non-STE: The `build` job does a compile of the source files, then starts the unit tests.
> STE: The `build` job compiles the source files, then starts the unit tests.
>
> Non-STE: Make a commit of your changes before you switch branches.
> STE: Commit your changes before you switch branches.
>
> Non-STE: If the error rate stays above five percent, execute a rollback of the migration.
> STE: If the error rate stays above five percent, roll back the migration.

Gerunds ("compiling takes ten seconds") are permitted in descriptive text but avoid as main verbs in
procedural sentences. Generated tool output (compiler messages) is quoted text — preserve as-is.

See also: Rules 1.12, 1.5, 1.7, 1.4, 1.10.

---

## Rule 1.14 — Use American English Spelling

Default to American English spelling in all prose. Exceptions: quoted text (third-party error
messages, terminal output, UI labels, code keywords) and proper names/technical nouns keep their
original spelling. An official project style guide mandating British English overrides this rule
(document it in CONTRIBUTING.md), but then the project is outside STE-Code for spelling.

Three spelling classes:
1. **Prose words** — American English only, no exceptions.
2. **Quoted text** — preserved as-is (Rule 1.5, category 10).
3. **Code-domain technical nouns** — use official spelling; surrounding prose stays American.

Suffix rules:
- **-ize / -ise**: use `-ize` (initialize, serialize, optimize, organize, recognize, synchronize,
  standardize, parameterize, customize, authorize, analyze, paralyze). Never `-ise` in prose.
- **-or / -our**: use `-or` (color, behavior, flavor, humor, labor, neighbor, rumor, harbor, honor,
  vapor, rigor). Not `-our`.
- **-er / -re**: use `-er` (center, theater, liter, meter [measuring device], fiber, caliber). Not `-re`.
  Note: "meter" (device) ≠ "metre" (length) — code docs always use "meter".
- **-l / -ll**: single `-l` in American (canceled, traveler, modeled, labeled, signaled). Not `-ll`.
  Exception: stress-final-syllable words double in both dialects (compelled, rebelled).

Common swaps:

| British | American | | British | American |
|---------|----------|---|---------|----------|
| colour | color | | licence (n) | license |
| behaviour | behavior | | defence | defense |
| centre | center | | programme | program |
| analyse | analyze | | practise (v) | practice |
| optimise | optimize | | catalogue | catalog |
| parametrise | parameterize | | analogue | analog |
| customise | customize | | judgement | judgment |

Same spelling both dialects (do NOT "fix"): address, all, committee, disappoint, necessary,
occurrence, parallel, recommend.

Examples:
> Non-STE: The log file shows the colour of each output line.
> STE: The log file shows the color of each output line.
>
> Non-STE: Initialise the variable before you use it.
> STE: Initialize the variable before you use it.
>
> Non-STE: The terminal shows the message `Colour profile not recognised`.
> STE: The terminal shows the message `Colour profile not recognised`. (quoted text preserved)
>
> Non-STE: The ColourPicker component uses the colour library for colour space conversions.
> STE: The `ColourPicker` component uses the `colour` library for color space conversions.
> (framework names preserved; prose uses American)

Enforcement: configure spell checker to en-US; pre-commit hook; CI step rejecting British spellings;
maintain a project dictionary of British-spelled technical nouns so the checker does not flag them.

See also: Rules 1.1, 1.5, 1.11, 8.6.
